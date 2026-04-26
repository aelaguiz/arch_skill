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


VALID_RUNTIMES = {"claude", "codex"}
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


def resolve_execution_phrase(
    source_quote: str,
    *,
    codex_models: list[str] | None = None,
) -> ResolvedExecution:
    """Resolve a compact user phrase into runtime/model/effort.

    Examples:
    - "Claude Opus 4.7 xhigh" -> claude / claude-opus-4-7 / xhigh
    - "codex gpt 5.4 mini high" -> codex / gpt-5.4-mini / high

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
            f"could not infer runtime from {raw!r}; name claude or codex"
        )
    if effort is None:
        raise ModelResolutionError(
            f"could not infer effort from {raw!r}; use one of {sorted(VALID_EFFORTS)}"
        )

    if runtime == "claude":
        model = _resolve_claude_model(raw)
    else:
        model = _resolve_codex_model(raw, codex_models=codex_models)

    return ResolvedExecution(
        runtime=runtime,
        model=model,
        effort=effort,
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
    if has_codex and has_claude:
        raise ModelResolutionError(
            "execution phrase names both Claude and Codex families; split the roles"
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


def _same_as_role(value: str) -> str | None:
    match = re.fullmatch(r"same\s+as\s+([a-zA-Z0-9_-]+)", value.strip(), re.IGNORECASE)
    if not match:
        return None
    role = match.group(1).replace("-", "_").lower()
    return _ROLE_ALIASES.get(role, role)
