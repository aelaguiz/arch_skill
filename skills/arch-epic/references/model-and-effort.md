# Role dispatch and external execution policy

Resolve transport before model settings. Ordinary same-host planner, worker,
and critic roles prefer clean native children of the active host, briefed from
the epic doc, sub-plan DOC_PATH, worklog, and relevant arch-step references.
Do not invent a native model, effort, permission set, worktree, or lifecycle the
host cannot confirm.

An external Claude, Codex, or Grok process remains valid when a concrete
provider, exact model/profile, durable or detached lifecycle, worktree/process
isolation, automation surface, structured receipt, or another deliberate
benefit warrants the additional process and integration cost. These examples
are recognition aids, not an allowlist. External repair resumes the exact
planner or implementation session; every external critic starts clean.

## Interactive mode

Interactive and same-session modes prefer one clean native critic. The legacy
frontmatter still supports an external critic execution block:

- `critic_runtime`: `claude`, `codex`, or `grok`
- `critic_model`: runnable CLI model identifier
- `critic_effort`: `low | medium | high | xhigh | max`

These values live in the epic doc frontmatter for compatibility with existing
epic docs. They may remain null for a native critic or while an explicit
external-harness role table is pending. External-harness critics use the
`auto_execution.roles.critic` block.

## Explicit external-harness mode

The external-harness lane asks for a role table after decomposition approval:

| Role | What it controls |
| --- | --- |
| `epic_planner` | sub-plan DOC_PATH creation, North Star drafting, Epic Requirement Coverage, planning repairs |
| `implementation_worker` | implementation, verification, worklog updates, ordinary in-scope code/docs edits |
| `critic` | North Star critic, plan-readiness critic, implementation/scope critic, final epic critic |

Example table:

```text
epic_planner: claude fable 5 high
implementation_worker: codex gpt-5.6-sol xhigh
critic: codex gpt-5.6-sol xhigh
poll_seconds: 180
quiet_floor_seconds: 900
stuck_floor_seconds: 1800
max_runtime_seconds: 7200
```

The resolved external policy is stored under `auto_execution` in the epic doc
and in the external-harness run directory's `state.json`.

Existing policies may contain a legacy `repair_worker` role. Load it for
compatibility, but do not ask for it in new runs and do not use it for ordinary
critic failures. Resume the exact failing planner or implementation worker session
instead.

The external monitor policy is part of the same execution choice because it changes
how much trust the parent gives long-running children. Planners and
implementation workers routinely need 5+ minutes; broad `xhigh` or `max`
children can reasonably take 20-40 minutes. A missing final file after a short
window is only "not done yet" when process state and stream activity show life.

In the external harness, use foreground mode when the expected child is short enough that blocking
keeps the orchestration simpler. Use detached mode when the child is expected
to plan, implement, audit, or run verification for many minutes. Detached
mode must produce live `events.jsonl`, `stderr.log`, `stream.log`,
`heartbeat.json`, and `monitor.json` artifacts, then be finalized after exit.

## Shared resolver owner

The deterministic helper is `../../_shared/model_resolution.py`. It encodes
the same doctrine used by Stepwise and fresh-consult:

- preserve model family and numeric version exactly
- infer runtime only from unambiguous family evidence
- accept `sol`, `luna`, and `terra` as the exact Codex 5.6 variants and use
  `gpt-5.6-sol` when a Codex role omits its model
- inspect `codex debug models` when ordinary Codex model availability matters
- resolve `fugu` and `fugu-ultra` as Codex profiles, not model-list ids
- inspect `grok models` when Grok model availability matters
- prefer `claude-<family>-<version-with-hyphens>` for supported Claude
  family+version
  phrases
- ask for the runnable ID when discovery is unavailable, ambiguous, or missing
- never run paid trial prompts to discover whether a Claude model exists

Do not add another local model-name lookup table in arch-epic. If the rule
needs to change, update the shared helper and the shared doctrine references.

## Acceptable user phrasing

All of these explicitly request an external provider or exact model/profile;
that deliberate value selects the external harness. They are valid when they
include a role:

- "planner on Claude Fable 5 high"
- "implementation worker on Codex gpt-5.6-sol xhigh"
- "implementation worker on Luna xhigh"
- "critic on Terra high"
- "implementation worker on Codex Fugu Ultra xhigh"
- "planner on Grok Build high"
- "critics on gpt-5.6-sol xhigh"
- "codex gpt-5.6-sol high everywhere"

If the user gives one complete "everywhere" value, the orchestrator may fill
all three required roles with that value, but it must announce the interpretation before
running.

## Model phrase resolution

Treat model text as intent, not a loose alias:

- `sol`, `luna`, and `terra` normalize to `gpt-5.6-sol`, `gpt-5.6-luna`, and
  `gpt-5.6-terra`. Compact forms such as `GPT56LUNAXI` and `GPT56TERRAXI`
  preserve the named variant and imply `xhigh`. A Codex role with no model or
  profile uses `gpt-5.6-sol`, reported with `model_source=default`.
- An explicit `gpt-5.6-luna` may normalize to `gpt-5.6-luna`; it must not
  become `gpt-5.6-sol`, `gpt-5.4`, or `gpt-5.5`.
- `gpt 5.3 codex` may normalize to `gpt-5.3-codex`.
- `fugu` and `fugu-ultra` are Codex profile names; preserve them as `fugu` and
  `fugu-ultra` and launch them with `codex exec -p`.
- `fable 5` under Claude may normalize to `claude-fable-5`; `opus 4.7` may
  normalize to `claude-opus-4-7`. Neither may become another Claude family or
  version.
- `grok`, `grok cli`, `grok build`, or `grok-build` may normalize to
  `grok-build`.
- `grok composer`, `grok composer 2.5`, or `grok-composer-2.5-fast` may
  normalize to `grok-composer-2.5-fast`.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-5.6-sol`. This is an intent check, not an alias rule: do not
  rewrite the version yourself.
- Family-only supported Claude aliases such as `fable` or `opus` are allowed
  only when the user did not pin a version.
- If the phrase names multiple runtime families, ask the user to split the role
  choices.

For Fugu profiles, omit Codex `-c model_reasoning_effort=...` at the profile
default (`fugu` defaults to `high`; `fugu-ultra` defaults to `xhigh`). Add the
`-c` override only when the user explicitly requests a supported non-default
Fugu Ultra effort.

Always print the raw-to-resolved mapping before execution:

```text
critic: "codex gpt-5.6-sol xhigh" -> runtime=codex, model=gpt-5.6-sol, effort=xhigh
implementation_worker: "codex high" -> runtime=codex, model=gpt-5.6-sol, effort=high, model_source=default
implementation_worker: "luna xhigh" -> runtime=codex, model=gpt-5.6-luna, effort=xhigh
critic: "terra high" -> runtime=codex, model=gpt-5.6-terra, effort=high
critic: "Fugu Ultra xhigh" -> runtime=codex, model=fugu-ultra, codex_profile=fugu-ultra, effort=xhigh
planner: "Claude Fable 5 high" -> runtime=claude, model=claude-fable-5, effort=high
implementation_worker: "Grok Build high" -> runtime=grok, model=grok-build, effort=high
```

## Asking when missing

Do not ask for a model table merely to use capable native children. After the
external harness has been deliberately selected, ask one consolidated question
that names the missing roles and what they control. Do not ask one question per
field.

Use this shape:

```text
Before I run the external epic harness, I need its role execution table. These
choices control real external processes and model budget.

- epic_planner: drafts/repairs sub-plan North Stars and requirement coverage
- implementation_worker: edits code/docs and runs verification
- critic: checks North Star, plan readiness, completion, and scope drift

Please give runtime/effort for each role plus a model/profile for non-Codex
roles, or say which roles should be "same as" another role. A Codex role with
no model uses gpt-5.6-sol. Ordinary critic failures resume the exact relevant
planner or implementation worker session; there is no separate repair-worker
choice in new external-harness policies.
```

If one role is complete and another is missing, preserve the complete role and
ask only for the missing ones.

## Pinning

External-harness mode writes:

- `source_quotes`: the raw user role text
- `roles`: resolved runtime/model/effort blocks
- `poll_seconds`: default `180` unless explicitly overridden
- `quiet_floor_seconds`: default `900`; before this floor, silence is normal
  for long planner/worker runs
- `stuck_floor_seconds`: default `1800`; after this floor without any stream
  activity, the run needs attention but is not automatically terminated
- `max_runtime_seconds`: default `7200`; exceeding it is an attention signal,
  not a silent kill switch
- `execution_sha256`: stable hash of the resolved policy

Changing any role mid-run creates a new policy hash. The orchestrator must log
the change in the epic Decision Log and apply it only to future child runs.
Past worker and critic artifacts keep the invocation they actually used.
