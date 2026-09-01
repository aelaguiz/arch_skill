"""Shared runtime/model/effort resolution for arch_skill subprocesses.

This module is deterministic plumbing for skill scripts. It encodes the
provider-owned routing rule: Codex runs GPT/GBT/OpenAI models and Fugu profiles,
Claude Code runs supported Claude models, Cursor Agent runs Composer 2.5 Fast,
Grok CLI runs Grok models, and Kimi Code runs Kimi models.
Cross-provider phrases fail loud instead of routing an expensive model through
the wrong harness.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any


VALID_RUNTIMES = {"agent", "claude", "codex", "grok", "kimi"}
VALID_EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
PREFERRED_CODEX_MODEL = "gpt-5.6-sol"
PREFERRED_CODEX_EFFORT = "ultra"
PREFERRED_GROK_MODEL = "grok-4.6"
PREFERRED_KIMI_MODEL = "kimi-code/k3"
KIMI_DEFAULT_EFFORT = "max"
KIMI_EFFORT_ENV = "KIMI_MODEL_THINKING_EFFORT"
KIMI_NO_AUTO_UPDATE_ENV = "KIMI_CODE_NO_AUTO_UPDATE"
CODEX_56_VARIANTS = ("sol", "luna", "terra")
BLOCKED_CODEX_MODELS = frozenset({"gpt-5.4", "gpt-5.5"})

_CLAUDE_FAMILIES = {"fable", "opus"}
_CODEX_56_VARIANT_PATTERN = "|".join(CODEX_56_VARIANTS)
_CODEX_SUFFIX_PATTERN = "|".join(("mini", "codex", "spark", *CODEX_56_VARIANTS))
_CODEX_FAMILY_RE = re.compile(
    r"\b(?:gpt|gbt)[\s_-]*(?P<version>\d+(?:\.\d+)?)"
    rf"(?P<suffix>(?:[\s_-]*(?:{_CODEX_SUFFIX_PATTERN}))*)\b",
    re.IGNORECASE,
)
_CODEX_56_COMPACT_RE = re.compile(
    rf"\b(?:gpt|gbt)[\s_-]*56[\s_-]*(?P<variant>{_CODEX_56_VARIANT_PATTERN})"
    r"(?:[\s_-]*(?:xhigh|xi|x))?\b",
    re.IGNORECASE,
)
_CODEX_56_BARE_VARIANT_RE = re.compile(
    rf"\b(?P<variant>{_CODEX_56_VARIANT_PATTERN})\b", re.IGNORECASE
)
_BLOCKED_GPT55_COMPACT_RE = re.compile(
    r"\b(?:gpt|gbt)[\s_-]*55(?:[\s_-]*(?:xhigh|xi|x))?\b",
    re.IGNORECASE,
)
_FUGU_MODEL_RE = re.compile(r"\bfugu(?:[\s_-]*ultra)?\b", re.IGNORECASE)
_FUGU_EFFORTS = {
    "fugu": {"high"},
    "fugu-ultra": {"high", "xhigh", "max"},
}
_FUGU_PROFILE_DEFAULT_EFFORTS = {
    "fugu": "high",
    "fugu-ultra": "xhigh",
}
_CODEX_ULTRA_MODELS = {"gpt-5.6-sol", "gpt-5.6-terra"}
_CLAUDE_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
_KIMI_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
_CLAUDE_FAMILY_RE = re.compile(
    r"\b(?P<family>fable|opus|sonnet|haiku)"
    r"(?:[\s_-]*(?P<version>\d+(?:[\.-]\d+)*))?\b",
    re.IGNORECASE,
)
_GROK_MODEL_RE = re.compile(r"\bgrok(?:[-_][a-z0-9.]+)+\b", re.IGNORECASE)
_KIMI_MODEL_RE = re.compile(
    r"(?<![a-z0-9])(?:kimi-code/k3|kimi(?:[-_\s]+code)?[-_\s]+k3|k3)(?![a-z0-9])",
    re.IGNORECASE,
)
_KIMI_ALIAS_RE = re.compile(
    r"(?<![a-z0-9])kimi-code/(?P<alias>[a-z0-9._-]+)",
    re.IGNORECASE,
)
_KIMI_VERSION_RE = re.compile(
    r"(?<![a-z0-9])k(?P<version>\d+(?:\.\d+)?)(?![a-z0-9])",
    re.IGNORECASE,
)
_NATURAL_GROK_VERSION_RE = re.compile(
    r"\bgrok(?:[\s_]+(?:cli|build))?"
    r"(?:[\s_]+(?:version|model))?[\s_]+v?"
    r"(?P<version>\d+(?:\.\d+)*)(?![a-z0-9])",
    re.IGNORECASE,
)
_GROK_CATALOG_EFFORTS = {"low", "medium", "high"}
_GROK_MODELS_WITH_CATALOG_EFFORTS = frozenset({"grok-4.5", "grok-4.6"})
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
    codex_profile: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "runtime": self.runtime,
            "model": self.model,
            "effort": self.effort,
            "codex_profile": self.codex_profile,
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


def codex_model_or_profile_args(
    model: str,
    effort: str,
    *,
    codex_profile: str = "",
) -> list[str]:
    """Return Codex CLI argv for a normal model id or local profile.

    Fugu runs through Codex profiles so the selected provider and custom model
    catalog load from `$CODEX_HOME/<profile>.config.toml`. Ordinary Codex
    models still use `--model`.
    """

    if codex_profile:
        args = ["-p", codex_profile]
        default_effort = _FUGU_PROFILE_DEFAULT_EFFORTS.get(codex_profile)
        if effort and effort != default_effort:
            args.extend(["-c", f'model_reasoning_effort="{effort}"'])
        return args
    _reject_blocked_codex_model(model)
    return ["--model", model, "-c", f'model_reasoning_effort="{effort}"']


def kimi_model_args(model: str) -> list[str]:
    """Return the Kimi Code CLI argv that pins an exact model alias."""

    return ["-m", model]


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
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        for item in payload.get("models", []):
            slug = item.get("slug") if isinstance(item, dict) else item
            if isinstance(slug, str) and slug.strip():
                candidates.add(slug.strip().lower())
        if candidates:
            return sorted(candidates)

    for token in re.findall(
        r"\b(?:(?:gpt|gbt)-[a-z0-9._-]+|o\d[a-z0-9._-]*)\b",
        proc.stdout,
        re.IGNORECASE,
    ):
        cleaned = token.strip("`'\",:;()[]{}")
        if cleaned:
            candidates.add(cleaned.lower())
    return sorted(candidates)


def discover_grok_models() -> list[str]:
    """Return model ids from `grok models` when available."""

    if shutil.which("grok") is None:
        return []
    proc = subprocess.run(
        ["grok", "models"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    candidates: set[str] = set()
    for token in re.findall(r"\bgrok-\S+", proc.stdout):
        cleaned = token.strip("`'\",:;()[]{}")
        if cleaned:
            candidates.add(cleaned)
    return sorted(candidates)


def discover_kimi_models() -> list[str]:
    """Return provider/model aliases from `kimi provider list --json`.

    Kimi Code exposes the runnable aliases as keys of the top-level `models`
    object. Treat any other output shape as unavailable rather than guessing.
    """

    if shutil.which("kimi") is None:
        return []
    proc = subprocess.run(
        ["kimi", "provider", "list", "--json"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, dict):
        return []
    models = payload.get("models")
    if not isinstance(models, dict):
        return []
    return sorted(
        alias.strip().lower()
        for alias in models
        if isinstance(alias, str) and alias.strip()
    )


def resolve_execution_phrase(
    source_quote: str,
    *,
    codex_models: list[str] | None = None,
    agent_models: list[str] | None = None,
    grok_models: list[str] | None = None,
    kimi_models: list[str] | None = None,
) -> ResolvedExecution:
    """Resolve a compact user phrase into runtime/model/effort.

    Examples:
    - "Claude Fable 5.1 high" -> claude / claude-fable-5-1 / high
    - "Claude Opus 4.7 xhigh" -> claude / claude-opus-4-7 / xhigh
    - "codex gpt 5.4 mini high" -> codex / gpt-5.4-mini / high
    - "GPT56SOLXI" -> codex / gpt-5.6-sol / xhigh
    - "codex" -> codex / gpt-5.6-sol / ultra
    - "gpt-5.6-sol" -> codex / gpt-5.6-sol / ultra
    - "luna xhigh" -> codex / gpt-5.6-luna / xhigh
    - "GPT56TERRAXI" -> codex / gpt-5.6-terra / xhigh
    - "codex high" -> codex / gpt-5.6-sol / high
    - "Fugu high" -> codex / profile fugu / high
    - "Fugu Ultra xhigh" -> codex / profile fugu-ultra / xhigh
    - "cursor agent composer-2.5-fast" -> agent / composer-2.5-fast / encoded-in-model
    - "cursor agent composer 2.5" -> agent / composer-2.5-fast / encoded-in-model
    - "grok build high" -> grok / grok-4.6 / high
    - "grok composer 2.5 high" -> grok / grok-composer-2.5-fast / high
    - "kimi k3" -> kimi / kimi-code/k3 / max
    - "kimi-code/k3 xhigh" -> kimi / kimi-code/k3 / xhigh

    The function raises ModelResolutionError when a required value is missing
    or when exact-version-preserving model discovery is impossible. Cursor
    Agent is Composer-only even if the local CLI lists other model ids.
    """

    raw = source_quote.strip()
    if not raw:
        raise ModelResolutionError("execution phrase is empty")

    lowered = raw.lower()
    effort = _extract_effort(lowered)
    runtime, runtime_source = _infer_runtime(lowered)
    if runtime is None:
        raise ModelResolutionError(
            f"could not infer runtime from {raw!r}; name claude, codex, agent, grok, or kimi"
        )
    fugu_candidate = (
        _extract_fugu_model_candidate(lowered) if runtime == "codex" else None
    )

    codex_profile = ""
    model_source = "explicit"
    if runtime == "claude":
        model = _resolve_claude_model(raw)
    elif runtime == "codex":
        model, model_source = _resolve_codex_model(
            raw, codex_models=codex_models
        )
        if fugu_candidate is not None:
            codex_profile = model
    elif runtime == "agent":
        model = _resolve_agent_model(raw, agent_models=agent_models)
    elif runtime == "grok":
        model, model_source = _resolve_grok_model(raw, grok_models=grok_models)
    else:
        model, model_source = _resolve_kimi_model(raw, kimi_models=kimi_models)

    effort_source = "explicit"
    if effort is None and fugu_candidate is not None:
        effort = _FUGU_PROFILE_DEFAULT_EFFORTS[fugu_candidate]
        effort_source = "profile_default"
    if (
        effort is None
        and runtime == "codex"
        and model == PREFERRED_CODEX_MODEL
    ):
        effort = PREFERRED_CODEX_EFFORT
        effort_source = "preference_default"
    if effort is None and runtime == "kimi":
        effort = KIMI_DEFAULT_EFFORT
        effort_source = "model_default"
    if effort is None and runtime != "agent":
        raise ModelResolutionError(
            f"could not infer effort from {raw!r}; name an effort supported "
            "by the selected runtime and model"
        )

    if runtime == "claude":
        _validate_claude_effort(effort or "", raw)
    elif runtime == "codex":
        _validate_codex_effort(model, effort or "", raw)
    elif runtime == "agent":
        _validate_agent_effort(effort or "", raw)
        effort = f"encoded-in-model:{effort}" if effort else "encoded-in-model"
    elif runtime == "grok":
        _validate_grok_effort(model, effort or "", raw)
    else:
        _validate_kimi_effort(effort or "", raw)

    return ResolvedExecution(
        runtime=runtime,
        model=model,
        effort=effort or "",
        runtime_source=runtime_source,
        model_source=model_source,
        effort_source=effort_source,
        source_quote=source_quote,
        resolution_reason=(
            f"{source_quote!r} resolved to runtime={runtime}, model={model}, "
            f"effort={effort}, model_source={model_source}, "
            f"codex_profile={codex_profile or '<none>'} "
            "with exact model family/version preservation."
        ),
        codex_profile=codex_profile,
    )


def resolve_role_execution_policy(
    role_sources: dict[str, str],
    *,
    codex_models: list[str] | None = None,
    agent_models: list[str] | None = None,
    grok_models: list[str] | None = None,
    kimi_models: list[str] | None = None,
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
                    grok_models=grok_models,
                    kimi_models=kimi_models,
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
    normalized = re.sub(
        r"\bfugu[\s_-]*ultra\b",
        " fugu_profile ",
        lowered,
    )
    normalized = re.sub(
        r"\b(?:extra[\s_-]*high|x[\s_-]*high)\b",
        " xhigh ",
        normalized,
    )
    normalized = re.sub(
        rf"\b(?:gpt|gbt)[\s_-]*(?:55|56[\s_-]*(?:{_CODEX_56_VARIANT_PATTERN}))"
        r"[\s_-]*(?:xhigh|xi|x)\b",
        " xhigh ",
        normalized,
    )
    found = sorted(
        effort
        for effort in VALID_EFFORTS
        if re.search(rf"\b{effort}\b", normalized)
    )
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        raise ModelResolutionError(
            "execution phrase names multiple distinct effort levels "
            f"{found}; choose exactly one"
        )
    return None


def _infer_runtime(lowered: str) -> tuple[str | None, str]:
    has_codex = bool(
        re.search(r"\b(codex|openai|gpt|gbt|sakana)\b", lowered)
        or _CODEX_56_COMPACT_RE.search(lowered)
        or _CODEX_56_BARE_VARIANT_RE.search(lowered)
        or _BLOCKED_GPT55_COMPACT_RE.search(lowered)
        or _FUGU_MODEL_RE.search(lowered)
    )
    has_claude = bool(
        re.search(r"\b(claude|anthropic|fable|opus|sonnet|haiku)\b", lowered)
    )
    has_agent = bool(
        re.search(r"\b(cursor(?:[-\s]+agent)?|cursor-agent|agent)\b", lowered)
    )
    has_grok = bool(
        re.search(r"\b(grok|xai|x\.ai)\b", lowered)
        or _GROK_MODEL_RE.search(lowered)
    )
    has_kimi = bool(
        re.search(r"\b(kimi|moonshot|k3)\b", lowered)
        or _KIMI_MODEL_RE.search(lowered)
        or _KIMI_ALIAS_RE.search(lowered)
        or _KIMI_VERSION_RE.search(lowered)
    )
    has_composer = bool(
        re.search(r"(?<![a-z0-9])composer(?![a-z0-9])", lowered)
        or re.search(r"(?<![\d])2[-_.]5(?![\d])", lowered)
    )
    families = {
        "Codex": has_codex,
        "Claude": has_claude,
        "Cursor Agent": has_agent,
        "Grok": has_grok,
        "Kimi": has_kimi,
    }
    selected = [name for name, present in families.items() if present]
    if len(selected) > 1:
        raise ModelResolutionError(
            "execution phrase names multiple runtime families "
            f"({', '.join(selected)}); split the roles"
        )
    if has_kimi:
        return "kimi", "inferred_from_model_family"
    if has_grok:
        return "grok", "inferred_from_model_family"
    if has_agent:
        return "agent", "inferred_from_runtime_name"
    if has_codex:
        return "codex", "inferred_from_model_family"
    if has_claude:
        return "claude", "inferred_from_model_family"
    if has_composer:
        raise ModelResolutionError(
            "Composer phrasing is ambiguous now that Cursor Agent and Grok both "
            "have Composer models; name Cursor Agent or Grok explicitly"
        )
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


def _resolve_codex_model(
    raw: str,
    *,
    codex_models: list[str] | None,
) -> tuple[str, str]:
    candidate = _extract_fugu_model_candidate(raw.lower())
    if candidate is not None:
        return candidate, "codex_profile"

    match = _CODEX_FAMILY_RE.search(raw)
    compact_variant = _CODEX_56_COMPACT_RE.search(raw)
    bare_variant = _CODEX_56_BARE_VARIANT_RE.search(raw)
    blocked_compact = _BLOCKED_GPT55_COMPACT_RE.search(raw)

    model_source = "explicit"
    if compact_variant:
        candidate = f"gpt-5.6-{compact_variant.group('variant').lower()}"
    elif blocked_compact:
        candidate = "gpt-5.5"
    elif match:
        version = match.group("version")
        suffix_words = re.findall(
            rf"({_CODEX_SUFFIX_PATTERN})",
            match.group("suffix"),
            re.IGNORECASE,
        )
        candidate = f"gpt-{version}"
        if suffix_words:
            candidate += "-" + "-".join(word.lower() for word in suffix_words)
    elif bare_variant:
        candidate = f"gpt-5.6-{bare_variant.group('variant').lower()}"
    else:
        candidate = PREFERRED_CODEX_MODEL
        model_source = "default"

    resolved = _resolve_codex_candidate(raw, candidate, codex_models=codex_models)
    return resolved, model_source


def _resolve_codex_candidate(
    raw: str,
    candidate: str,
    *,
    codex_models: list[str] | None,
) -> str:
    _reject_blocked_codex_model(candidate)
    models = codex_models
    if models is None:
        models = discover_codex_models()
    normalized_models = [model.lower() for model in models]

    if not normalized_models:
        return candidate
    if candidate in normalized_models:
        return candidate
    compatible = [
        model
        for model in normalized_models
        if _same_codex_family_and_version(candidate, model)
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


def _reject_blocked_codex_model(model: str) -> None:
    normalized = model.strip().lower()
    if normalized not in BLOCKED_CODEX_MODELS:
        return
    raise ModelResolutionError(
        f"blocked Codex model {normalized!r}; use {PREFERRED_CODEX_MODEL!r} instead"
    )


def _same_codex_family_and_version(candidate: str, model: str) -> bool:
    return model == candidate


def _extract_fugu_model_candidate(lowered: str) -> str | None:
    if re.search(r"\bfugu[\s_-]*ultra\b", lowered):
        return "fugu-ultra"
    if re.search(r"\bfugu\b", lowered):
        return "fugu"
    return None


def _validate_codex_effort(model: str, effort: str, raw: str) -> None:
    allowed = _FUGU_EFFORTS.get(model)
    if allowed is not None and effort not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        raise ModelResolutionError(
            f"{raw!r} uses effort {effort!r}, but {model!r} supports only: {allowed_text}"
        )
    if effort != "ultra" or model in _CODEX_ULTRA_MODELS:
        return
    raise ModelResolutionError(
        f"{raw!r} uses effort 'ultra', but {model!r} does not advertise ultra"
    )


def _validate_claude_effort(effort: str, raw: str) -> None:
    if effort in _CLAUDE_EFFORTS:
        return
    allowed_text = ", ".join(sorted(_CLAUDE_EFFORTS))
    raise ModelResolutionError(
        f"{raw!r} uses effort {effort!r}, but Claude supports only: {allowed_text}"
    )


def _validate_agent_effort(effort: str, raw: str) -> None:
    if effort != "ultra":
        return
    raise ModelResolutionError(
        f"{raw!r} requests ultra, but Cursor Agent effort is encoded in the model id"
    )


def _validate_kimi_effort(effort: str, raw: str) -> None:
    if effort in _KIMI_EFFORTS:
        return
    allowed_text = ", ".join(sorted(_KIMI_EFFORTS))
    raise ModelResolutionError(
        f"{raw!r} uses effort {effort!r}, but Kimi supports only: {allowed_text}"
    )


def _looks_like_agent_model_id(token: str) -> bool:
    return token.startswith("composer-")


def _resolve_agent_model(raw: str, *, agent_models: list[str] | None) -> str:
    normalized_models = [
        model.lower() for model in (agent_models or []) if model.lower().startswith("composer-")
    ]
    lowered = raw.lower()

    candidate = _extract_agent_model_candidate(lowered)
    if candidate == "composer-2.5-fast":
        if not normalized_models or candidate in normalized_models:
            return candidate
        raise ModelResolutionError(
            f"{raw!r} did not match an available Cursor Agent model id; candidate was {candidate!r}"
        )

    if candidate is None:
        raise ModelResolutionError(
            f"could not find Composer 2.5 in {raw!r}; Cursor Agent is limited to composer-2.5-fast"
        )

    raise ModelResolutionError(
        f"unsupported Cursor Agent model in {raw!r}; Cursor Agent is limited to composer-2.5-fast"
    )


def _resolve_grok_model(
    raw: str,
    *,
    grok_models: list[str] | None,
) -> tuple[str, str]:
    models = grok_models
    if models is None:
        models = discover_grok_models()
    normalized_models = [model.lower() for model in models]
    candidate, model_source = _extract_grok_model_candidate(raw.lower())
    if candidate is None:
        raise ModelResolutionError(f"could not find a Grok model in {raw!r}")

    if not normalized_models or candidate in normalized_models:
        return candidate, model_source
    raise ModelResolutionError(
        f"{raw!r} did not match an available Grok model id; candidate was {candidate!r}"
    )


def _extract_grok_model_candidate(lowered: str) -> tuple[str | None, str]:
    match = _GROK_MODEL_RE.search(lowered)
    if match:
        token = match.group(0).replace("_", "-")
        if token == "grok-composer" or token.startswith("grok-composer-2-5"):
            return "grok-composer-2.5-fast", "explicit"
        return token, "explicit"

    if re.search(
        r"\bgrok[-_\s]*composer(?:[-_\s]*2[-_\s]*5(?:[-_\s]*fast)?)?\b",
        lowered,
    ):
        return "grok-composer-2.5-fast", "explicit"
    if re.search(r"\bgrok[\s_]+build\b", lowered):
        _validate_natural_grok_version(lowered)
        return PREFERRED_GROK_MODEL, "default"

    if re.search(r"\bgrok\b", lowered):
        _validate_natural_grok_version(lowered)
        return PREFERRED_GROK_MODEL, "default"
    return None, "unresolved"


def _validate_natural_grok_version(lowered: str) -> None:
    match = _NATURAL_GROK_VERSION_RE.search(lowered)
    preferred_version = PREFERRED_GROK_MODEL.removeprefix("grok-")
    if match is None or match.group("version") == preferred_version:
        return
    raise ModelResolutionError(
        "natural Grok wording names unsupported numeric version "
        f"{match.group('version')!r}; use {PREFERRED_GROK_MODEL!r} or an exact "
        "grok-* model id"
    )


def _validate_grok_effort(model: str, effort: str, raw: str) -> None:
    if model not in _GROK_MODELS_WITH_CATALOG_EFFORTS or effort in _GROK_CATALOG_EFFORTS:
        return
    allowed_text = ", ".join(sorted(_GROK_CATALOG_EFFORTS))
    raise ModelResolutionError(
        f"{raw!r} uses effort {effort!r}, but {model!r} supports only: {allowed_text}"
    )


def _resolve_kimi_model(
    raw: str,
    *,
    kimi_models: list[str] | None,
) -> tuple[str, str]:
    lowered = raw.lower()
    alias_match = _KIMI_ALIAS_RE.search(lowered)
    if alias_match and alias_match.group("alias") != "k3":
        raise ModelResolutionError(
            f"unsupported Kimi model id {alias_match.group(0)!r}; this rollout "
            f"supports only {PREFERRED_KIMI_MODEL!r}, so name K3"
        )
    version_match = _KIMI_VERSION_RE.search(lowered)
    if version_match and version_match.group("version") != "3":
        raise ModelResolutionError(
            f"unsupported Kimi K{version_match.group('version')} model phrase; "
            f"this rollout supports only {PREFERRED_KIMI_MODEL!r}, so name K3"
        )
    if not (
        re.search(r"\b(kimi|moonshot|k3)\b", lowered)
        or _KIMI_MODEL_RE.search(lowered)
    ):
        raise ModelResolutionError(f"could not find a Kimi model in {raw!r}")

    models = kimi_models
    if models is None:
        models = discover_kimi_models()
    normalized_models = [model.strip().lower() for model in models if model.strip()]
    if normalized_models and PREFERRED_KIMI_MODEL not in normalized_models:
        raise ModelResolutionError(
            f"{raw!r} did not match an available Kimi model id; "
            f"candidate was {PREFERRED_KIMI_MODEL!r}"
        )
    explicit = bool(re.search(r"\bk3\b", lowered) or _KIMI_MODEL_RE.search(lowered))
    return PREFERRED_KIMI_MODEL, "explicit" if explicit else "default"


def _extract_agent_model_candidate(lowered: str) -> str | None:
    composer_mention = re.search(r"(?<![a-z0-9])composer(?![a-z0-9])", lowered)
    composer_version = re.search(r"composer[-_.\s]*(\d+(?:[-_.]\d+)?)", lowered)
    composer_25 = re.search(r"composer[-_.\s]*2[-_.\s]*5", lowered)
    bare_25 = re.search(r"(?<![\d])2[-_.]5(?![\d])", lowered)
    other_family_25 = re.search(
        r"\b(?:gpt|claude|fable|sonnet|opus|haiku)[-_.\s]*2[-_.\s]*5",
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
