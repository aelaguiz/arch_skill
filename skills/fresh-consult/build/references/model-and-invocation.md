# Model and Runtime Resolution

Shared model and runtime resolution doctrine for arch_skill subprocess skills. This document owns the decision truth about runtime inference, model preservation, effort validation, and fail-loud substitution rules.

## Runtime inference

Runtime can be inferred only from unambiguous model families.

- `gpt-5.4`, `gpt-5.4-mini`, and any `gpt-*` or `codex-*` pattern resolve to the `codex` runtime.
- `Claude Opus 4.7`, `opus`, `sonnet`, `haiku`, and any `claude-*` pattern resolve to the `claude` runtime.
- If an execution phrase names both Claude and Codex families, the resolution fails loud instead of picking one.
- If the user explicitly names a runtime (claude or codex), that overrides inference.

## Model preservation

Exact model versions are preserved. There is no silent downgrade, provider switch, or effort substitution.

- The user's model phrase resolves to exactly one runnable model id. If the phrase matches multiple runnable models with the same family and exact version, resolution fails loud rather than guessing.
- If the phrase does not match any discovered runnable model, resolution fails loud rather than substituting a nearby model.
- The resolved mapping (raw phrase → runnable id) is reported back to the caller before execution begins.

## Effort validation

Effort must be one of: `low`, `medium`, `high`, `xhigh`, `max`. If the phrase does not contain a recognized effort level, resolution fails loud instead of defaulting.

## Default model choices

When the user does not specify a model or runtime, skills use these defaults:

- External evaluator turns (arch-loop, code-review): Codex `gpt-5.4` `xhigh`.
- Fresh audit children (arch-step implement-loop, miniarch-step implement-loop): Codex `gpt-5.4` `xhigh` (or `gpt-5.4-mini` `xhigh` for miniarch).
- Fresh consult children: the user must supply runtime/model/effort, or the skill asks once before invoking.
- Delegated workers: the user must supply runtime/model/effort, or the skill asks once before invoking.

## Codex evaluator always Codex

Even when Claude hosts the Stop hook, the external evaluator subprocess for `arch-loop` and the review subprocess for `code-review` always shell out to a fresh unsandboxed Codex process. The Claude host can arm and drive the loop, but the evaluator subprocess itself is always Codex. Generic Claude auto-controllers stay Claude-native; `arch-loop` and `code-review` do not.

## Child run settings

Claude child runs that need fresh review or check passes launch hook-suppressed via `claude -p --settings '{"disableAllHooks":true}'` so that child path works with the machine's normal Claude auth. Codex child runs use `codex exec` with appropriate model and effort flags.

## Role resolution for arch-epic

`arch-epic` automatic mode resolves a role table where each role maps to an execution phrase. Roles may reference other roles with `same as <role>`. Cycles and unknown role references fail loud. The Python helper at `skills/_shared/model_resolution.py` owns the deterministic resolution logic.

- `epic_planner` — resolves the planner's runtime/model/effort.
- `implementation_worker` — resolves the implementation worker's runtime/model/effort.
- `critic` — resolves the critic's runtime/model/effort (always fresh, never resumed).
- Role aliases (`planner` → `epic_planner`, `worker` → `implementation_worker`) are accepted and expanded by the helper.

## Child run timing expectations

Subprocess children commonly take 5+ minutes. Broad `xhigh` or `max` reads can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.
