"""Shared runtime/model/effort resolution for arch_skill subprocesses.

This module is deterministic plumbing for skill scripts. It encodes the
repo's existing Stepwise/fresh-consult doctrine: preserve the user's model
family and exact version, use local model discovery when needed, and fail loud
instead of substituting a nearby model.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any


VALID_RUNTIMES = {"agent", "claude", "codex"}
VALID_EFFORTS = {"low", "medium", "high", "xhigh", "max"}

_CLAUDE_FAMILIES = {"opus", "sonnet", "haiku"}
_CODEX_FAMILY_RE = re.compile(
    r"\bgpt[\s_-]*(?P<version>\d+(?:\.\d+)?)"
    r"(?P<suffix>(?:[\s_-]*(?:mini|codex|spark))*)\b",
    re.IGNORECASE,
)
_CLAUDE_FAMILY_RE = re.compile(
    r"\b(?P<family>opus|sonnet|haiku)"
    r"(?:[\s_-]*(?P<version>\d+(?:[\.-]\d+)*))?\b",
    re.IGNORECASE,
)
_ROLE_ALIASES = {
    "planner": "epic_planner",
    "plan": "epic_planner",
    "implementation": "implementation_worker",
    "implementer": "implementation_worker",
    "worker": "implementation_worker",
    "repair": "repair_worker",
    "fixer": "repair_worker",
    "critics": "critic",
}


@dataclass(frozen=True)
class ResolvedExecution:
    runtime: str
    model: str
    effort: str
    runtime_source: str
    model_source: str
    effort_source: str
    source_quote: str
    resolution_reason: str

    def to_dict(self) -> dict[str, str]:
        return {
            "runtime": self.runtime,
            "model": self.model,
            "effort": self.effort,
            "runtime_source": self.runtime_source,
            "model_source": self.model_source,
            "effort_source": self.effort_source,
            "source_quote": self.source_quote,
            "resolution_reason": self.resolution_reason,
        }


class ModelResolutionError(ValueError):
    """Raised when a model phrase cannot be safely resolved."""


def execution_sha256(payload: dict[str, Any]) -> str:
    """Hash a resolved execution policy with stable JSON ordering."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def discover_codex_models() -> list[str]:
    """Return model ids from `codex debug models` when available.

    This is intentionally conservative. If the CLI is absent or the command
    shape drifts, callers get an empty list and must ask for a runnable id
    instead of guessing.
    """

    if shutil.which("codex") is None:
        return []
    proc = subprocess.run(
        ["codex", "debug", "models"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    candidates: set[str] = set()
    for token in re.findall(r"\b(?:gpt|o)\S+", proc.stdout):
        cleaned = token.strip("`'\",:;()[]{}")
        if cleaned:
            candidates.add(cleaned)
    return sorted(candidates)


def discover_agent_models() -> list[str]:
    """Return model ids from the local Cursor Agent CLI when available."""

    if shutil.which("agent") is None:
        return []
    candidates: set[str] = set()
    for argv in (["agent", "models"], ["agent", "--list-models"]):
        proc = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            continue
        for token in re.findall(r"\b[a-z][a-z0-9]*(?:[-_.][a-z0-9]+)+\b", proc.stdout.lower()):
            cleaned = token.strip("`'\",:;()[]{}")
            if _looks_like_agent_model_id(cleaned):
                candidates.add(cleaned)
        if candidates:
            break
    return sorted(candidates)


def resolve_execution_phrase(
    source_quote: str,
    *,
    codex_models: list[str] | None = None,
    agent_models: list[str] | None = None,
) -> ResolvedExecution:
    """Resolve a compact user phrase into runtime/model/effort.

    Examples:
    - "Claude Opus 4.7 xhigh" -> claude / claude-opus-4-7 / xhigh
    - "codex gpt 5.4 mini high" -> codex / gpt-5.4-mini / high
    - "cursor agent composer-2.5-fast" -> agent / composer-2.5-fast / encoded-in-model
    - "cursor agent composer 2.5" -> agent / composer-2.5-fast / encoded-in-model

    The function raises ModelResolutionError when a required value is missing
    or when exact-version-preserving model discovery is impossible.
    """

    raw = source_quote.strip()
    if not raw:
        raise ModelResolutionError("execution phrase is empty")

    lowered = raw.lower()
    effort = _extract_effort(lowered)
    runtime, runtime_source = _infer_runtime(lowered)
    if runtime is None:
        raise ModelResolutionError(
            f"could not infer runtime from {raw!r}; name claude, codex, or agent"
        )
    if effort is None and runtime != "agent":
        raise ModelResolutionError(
            f"could not infer effort from {raw!r}; use one of {sorted(VALID_EFFORTS)}"
        )

    if runtime == "claude":
        model = _resolve_claude_model(raw)
    elif runtime == "codex":
        model = _resolve_codex_model(raw, codex_models=codex_models)
    else:
        model = _resolve_agent_model(raw, agent_models=agent_models)
        effort = f"encoded-in-model:{effort}" if effort else "encoded-in-model"

    return ResolvedExecution(
        runtime=runtime,
        model=model,
        effort=effort or "",
        runtime_source=runtime_source,
        model_source="explicit",
        effort_source="explicit",
        source_quote=source_quote,
        resolution_reason=(
            f"{source_quote!r} resolved to runtime={runtime}, model={model}, "
            f"effort={effort} with exact model family/version preservation."
        ),
    )


def resolve_role_execution_policy(
    role_sources: dict[str, str],
    *,
    codex_models: list[str] | None = None,
    agent_models: list[str] | None = None,
    poll_seconds: int = 180,
    quiet_floor_seconds: int = 900,
    stuck_floor_seconds: int = 1800,
    max_runtime_seconds: int = 7200,
    approval_policy: str = "auto_after_decomposition",
) -> dict[str, Any]:
    """Resolve arch-epic automatic-mode role execution choices.

    Role values may be ordinary execution phrases or `same as <role>`.
    References are resolved after the target role has a concrete execution
    block. Cycles and unknown roles fail loud.
    """

    if poll_seconds <= 0:
        raise ModelResolutionError("poll_seconds must be a positive integer")
    if quiet_floor_seconds <= 0:
        raise ModelResolutionError("quiet_floor_seconds must be a positive integer")
    if stuck_floor_seconds < quiet_floor_seconds:
        raise ModelResolutionError(
            "stuck_floor_seconds must be greater than or equal to quiet_floor_seconds"
        )
    if max_runtime_seconds < stuck_floor_seconds:
        raise ModelResolutionError(
            "max_runtime_seconds must be greater than or equal to stuck_floor_seconds"
        )

    pending = dict(role_sources)
    resolved: dict[str, dict[str, str]] = {}

    while pending:
        progressed = False
        for role, phrase in list(pending.items()):
            phrase_clean = phrase.strip()
            same_as = _same_as_role(phrase_clean)
            if same_as is not None:
                if same_as not in role_sources:
                    raise ModelResolutionError(
                        f"role {role!r} references unknown role {same_as!r}"
                    )
                if same_as not in resolved:
                    continue
                inherited = dict(resolved[same_as])
                inherited.update(
                    {
                        "source": f"same_as:{same_as}",
                        "source_quote": phrase,
                        "resolution_reason": (
                            f"{role} inherits runtime/model/effort from {same_as}."
                        ),
                    }
                )
                resolved[role] = inherited
            else:
                block = resolve_execution_phrase(
                    phrase_clean,
                    codex_models=codex_models,
                    agent_models=agent_models,
                ).to_dict()
                block["source"] = "user_table"
                resolved[role] = block
            del pending[role]
            progressed = True
        if not progressed:
            cycle = ", ".join(sorted(pending))
            raise ModelResolutionError(
                f"could not resolve role references, possible cycle among: {cycle}"
            )

    policy = {
        "schema_version": 1,
        "approval_policy": approval_policy,
        "poll_seconds": poll_seconds,
        "quiet_floor_seconds": quiet_floor_seconds,
        "stuck_floor_seconds": stuck_floor_seconds,
        "max_runtime_seconds": max_runtime_seconds,
        "roles": resolved,
        "source_quotes": role_sources,
    }
    policy["execution_sha256"] = execution_sha256(policy)
    return policy


def _extract_effort(lowered: str) -> str | None:
    found = [effort for effort in VALID_EFFORTS if re.search(rf"\b{effort}\b", lowered)]
    if len(found) == 1:
        return found[0]
    return None


def _infer_runtime(lowered: str) -> tuple[str | None, str]:
    has_codex = bool(re.search(r"\b(codex|openai|gpt)\b", lowered))
    has_claude = bool(re.search(r"\b(claude|anthropic|opus|sonnet|haiku)\b", lowered))
    has_agent = bool(
        re.search(r"\b(cursor(?:[-\s]+agent)?|cursor-agent|agent)\b", lowered)
    )
    if has_agent:
        explicit_other_runtime = bool(re.search(r"\b(codex|openai|anthropic)\b", lowered))
        if not explicit_other_runtime:
            return "agent", "inferred_from_runtime_name"
    if sum(bool(v) for v in [has_codex, has_claude, has_agent]) > 1:
        raise ModelResolutionError(
            "execution phrase names multiple runtime families; split the roles"
        )
    if has_codex:
        return "codex", "inferred_from_model_family"
    if has_claude:
        return "claude", "inferred_from_model_family"
    return None, "unresolved"


def _resolve_claude_model(raw: str) -> str:
    match = _CLAUDE_FAMILY_RE.search(raw)
    if not match:
        raise ModelResolutionError(
            f"could not find a Claude model family in {raw!r}"
        )
    family = match.group("family").lower()
    version = match.group("version")
    if family not in _CLAUDE_FAMILIES:
        raise ModelResolutionError(f"unsupported Claude family: {family}")
    if not version:
        return family
    normalized_version = version.replace(".", "-").replace("_", "-")
    return f"claude-{family}-{normalized_version}"


def _resolve_codex_model(raw: str, *, codex_models: list[str] | None) -> str:
    match = _CODEX_FAMILY_RE.search(raw)
    if not match:
        raise ModelResolutionError(f"could not find a Codex/GPT model in {raw!r}")

    version = match.group("version")
    suffix_words = re.findall(r"(mini|codex|spark)", match.group("suffix"), re.IGNORECASE)
    candidate = f"gpt-{version}"
    if suffix_words:
        candidate += "-" + "-".join(word.lower() for word in suffix_words)

    models = codex_models
    if models is None:
        models = discover_codex_models()

    if not models:
        return candidate
    if candidate in models:
        return candidate
    compatible = [
        model for model in models if _same_codex_family_and_version(candidate, model)
    ]
    if len(compatible) == 1:
        return compatible[0]
    if len(compatible) > 1:
        raise ModelResolutionError(
            f"{raw!r} matches multiple runnable Codex models: {compatible}"
        )
    raise ModelResolutionError(
        f"{raw!r} did not match an available Codex model with the same family "
        f"and exact version; candidate was {candidate!r}"
    )


def _same_codex_family_and_version(candidate: str, model: str) -> bool:
    return model == candidate


def _looks_like_agent_model_id(token: str) -> bool:
    return token.startswith(("composer-", "gpt-", "claude-", "sonnet-", "opus-", "haiku-"))


def _resolve_agent_model(raw: str, *, agent_models: list[str] | None) -> str:
    models = agent_models
    if models is None:
        models = discover_agent_models()
    normalized_models = [model.lower() for model in models]
    lowered = raw.lower()

    candidate = _extract_agent_model_candidate(lowered)
    if candidate == "composer-2.5-fast":
        if not normalized_models or candidate in normalized_models:
            return candidate
        raise ModelResolutionError(
            f"{raw!r} did not match an available Cursor Agent model id; candidate was {candidate!r}"
        )

    for model in normalized_models:
        if re.search(rf"(?<![a-z0-9_.-]){re.escape(model)}(?![a-z0-9_.-])", lowered):
            return model

    if candidate is None:
        raise ModelResolutionError(
            f"could not find a Cursor Agent model id in {raw!r}; use an exact id from `agent models`"
        )

    if not normalized_models:
        return candidate
    if candidate in normalized_models:
        return candidate
    raise ModelResolutionError(
        f"{raw!r} did not match an available Cursor Agent model id; candidate was {candidate!r}"
    )


def _extract_agent_model_candidate(lowered: str) -> str | None:
    composer_mention = re.search(r"(?<![a-z0-9])composer(?![a-z0-9])", lowered)
    composer_version = re.search(r"composer[-_.\s]*(\d+(?:[-_.]\d+)?)", lowered)
    composer_25 = re.search(r"composer[-_.\s]*2[-_.\s]*5", lowered)
    bare_25 = re.search(r"(?<![\d])2[-_.]5(?![\d])", lowered)
    other_family_25 = re.search(
        r"\b(?:gpt|claude|sonnet|opus|haiku)[-_.\s]*2[-_.\s]*5",
        lowered,
    )
    if composer_25 or (composer_mention and composer_version is None) or (composer_mention and bare_25):
        return "composer-2.5-fast"
    if not composer_mention and bare_25 and not other_family_25:
        return "composer-2.5-fast"

    for token in re.findall(r"\b[a-z][a-z0-9]*(?:[-_.][a-z0-9]+)+\b", lowered):
        token = token.strip("`'\",:;()[]{}")
        if token == "cursor-agent":
            continue
        if _looks_like_agent_model_id(token):
            return token
    return None


def _same_as_role(value: str) -> str | None:
    match = re.fullmatch(r"same\s+as\s+([a-zA-Z0-9_-]+)", value.strip(), re.IGNORECASE)
    if not match:
        return None
    role = match.group(1).replace("-", "_").lower()
    return _ROLE_ALIASES.get(role, role)
