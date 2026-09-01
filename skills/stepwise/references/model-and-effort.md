# Dispatch and external execution defaults

Resolve transport before model settings. Ordinary same-host steps and critics
prefer clean native children of the active host. A native dispatch records
`transport: native`, `starting_context: clean`, the host, and its continuation
contract; do not invent a model, effort, permission set, worktree, or durable
lifecycle that the host does not expose.

An external lane remains valid when its provider, exact model/profile, durable
session, worktree/process isolation, automation surface, structured receipt, or
another concrete benefit is deliberate. These examples are not an allowlist.
Resolve the following values for each role assigned to the external adapter; a
fully external worker-and-critic policy has six values:

- `execution_defaults.step.runtime` - `claude`, `codex`, `grok`, or `kimi`
- `execution_defaults.step.model` - external model or Codex profile
- `execution_defaults.step.effort` - external reasoning effort
- `execution_defaults.critic.runtime` - external critic runtime
- `execution_defaults.critic.model` - external critic model or profile
- `execution_defaults.critic.effort` - external critic reasoning effort

External runtime and normally effort come from the user or target doctrine.
Models do too, except that an external Codex worker or critic with no named
model uses `gpt-5.6-sol`; that Sol lane uses `ultra` when effort is omitted. An
external Kimi lane uses `kimi-code/k3` and defaults an omitted effort to `max`.
When an external Codex lane uses Fugu, its execution block also stores
`codex_profile` as `fugu` or `fugu-ultra`.

The manifest may contain per-step transport and external-execution overrides
resolved from explicit user preferences or hard target-repo doctrine. See
`execution-routing.md`.

## Why external defaults come from the user

Different external work deserves different price points. A lesson-authoring
run may want strong worker steps and a strong critic. A many-step drill may want
cheap workers and a stronger critic. The right runtime and effort baseline is a
user judgment. The narrow preference exceptions are the established Codex
fallback and its Sol effort default: omitted model means `gpt-5.6-sol`, and
omitted effort on that Sol lane means `ultra`.

Ask only after the orchestrator has selected an external lane. Guessing wrong
is expensive: wrong runtime or model wastes money or quality; wrong effort
blows budget on trivial work or under-powers hard work.

## Acceptable shapes in the user's prompt

The intake phase parses whatever the user wrote. Each example below makes a
provider/model choice load-bearing. Honor it natively only when the active host
exposes and confirms that choice; otherwise the external adapter supplies the
requested capability. Any of these is clear:

- "use Claude Fable 5.1 high for steps and Codex gpt-5.6-sol ultra for critic"
- "use Codex Fugu high for steps and Codex Fugu Ultra xhigh for critic"
- "Codex gpt-5.6-sol high everywhere" (one value reused for all defaults)
- "Codex luna high for steps and terra xhigh for critic"
- "Codex high everywhere" (`gpt-5.6-sol` is the omitted model default)
- "Grok Build high for steps and Codex gpt-5.6-sol ultra for critic"
- "Kimi K3 high for steps and Kimi max for critic"
- "steps on gpt-5.6-sol high, critic on gpt-5.6-sol ultra"
- "default to Codex gpt-5.6-sol high, but use Claude Fable 5.1 for copywriting"

None of these is magic. The intake reads the phrase, maps the baseline into
execution defaults, records routing preferences separately, and prints back
the interpretation before executing.

## Model phrase resolution

Treat the user's model text as intent, not necessarily the exact CLI token.
Resolve it to a runnable model identifier before writing it into execution
defaults, per-step execution blocks, or subprocess commands.

This is reasoning, not a lookup table:

- Preserve the model family and numeric version exactly. You may add a
  required provider prefix or change spaces/dots to the runtime's separator,
  but you may not change the family or version. `4.7` must stay `4.7`/`4-7`;
  `5.5` must stay `5.5`, never `5.4`.
- For Claude, if the runtime is Claude and the user names a supported family
  plus a version, prefer the full Claude CLI identifier:
  `claude-<family>-<version-with-hyphens>`. For example, "Claude Fable 5.1",
  "claude fable-5.1", and "fable 5.1" under a Claude runtime all resolve to
  `claude-fable-5-1`; "opus 4.7" resolves to `claude-opus-4-7`. Family-only
  aliases such as `fable` or `opus` are acceptable only when the user did not
  pin a version.
- For ordinary Codex model ids, accept `sol`, `luna`, and `terra` as
  `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra`. Compact forms such as
  `GPT56LUNAXI` and `GPT56TERRAXI` preserve the variant and imply `xhigh`.
  When a Codex lane names no model or profile, use `gpt-5.6-sol` and report
  `model_source=default`. When that Sol lane names no effort, use `ultra` and
  report `effort_source=preference_default`. Inspect the installed CLI's model
  list when needed (`codex debug models`) and choose the available identifier
  with the same family and exact version. For example, "gpt-5.6-sol" resolves
  to `gpt-5.6-sol` if that exact model appears, and "gpt 5.3 codex" resolves
  to `gpt-5.3-codex`. Fugu is different: resolve `fugu` and `fugu-ultra` as
  Codex profiles, preserve those profile names exactly, and launch them with
  `-p`.
- For Grok, natural `grok`, `grok cli`, and `grok build` wording resolves to
  `grok-4.6`. “Grok Build” names the harness, not a model id. If that wording
  names a numeric version other than `4.6`, fail loud rather than discarding
  it. Preserve an
  explicit legacy slug such as `grok-build` or `grok-composer-2.5-fast`
  exactly and require discovery to confirm it; never rewrite it.
- For Kimi, `kimi`, `kimi code`, `kimi k3`, `k3`, and `moonshot` resolve to
  `runtime=kimi`, `model=kimi-code/k3`. Do not auto-resolve older
  Kimi-for-coding/K2.7 aliases. Inspect top-level `.models` keys from
  `kimi provider list --json` when availability matters.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If the user says `gpt 5.4`, `gpt 5.5`, or a variant of either while choosing
  a model, do not execute it. Say that the old model is blocked and ask whether
  they meant `gpt-5.6-sol`. This is an intent check, not an alias rule: do not
  rewrite the version yourself.
- If the runtime is unavailable, model discovery is unavailable, the exact
  version is not present, or the phrase could map to multiple runnable
  identifiers, ask the user for the runnable model id.
- Do not run paid trial prompts to discover whether a Claude model exists.
  Use the CLI's help/list surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution, for example:
`Claude Fable 5.1 high -> runtime=claude, model=claude-fable-5-1,
effort=high` or `Grok Build high -> runtime=grok, model=grok-4.6,
effort=high`. `Kimi -> runtime=kimi, model=kimi-code/k3, effort=max,
effort_source=model_default` records the K3 default explicitly.
`Codex -> runtime=codex, model=gpt-5.6-sol, effort=ultra,
model_source=default, effort_source=preference_default` records the Sol
preference defaults.
`Fugu Ultra xhigh -> runtime=codex, model=fugu-ultra,
codex_profile=fugu-ultra, effort=xhigh` is the same kind of exact Codex
mapping.

For Fugu profiles, omit Codex `-c model_reasoning_effort=...` at the profile
default (`fugu` defaults to `high`; `fugu-ultra` defaults to `xhigh`). Add the
`-c` override only when the user explicitly requests a supported non-default
Fugu Ultra effort.

`grok-4.6` supports only `low`, `medium`, and `high`. Kimi K3 advertises `low`,
`high`, and `max`, with omitted effort defaulting to `max`; pass it through
`KIMI_MODEL_THINKING_EFFORT`. Preserve an explicit `medium` or `xhigh` verbatim
as a forced override, but never choose either by default or inference. Every
Kimi process also sets `KIMI_CODE_NO_AUTO_UPDATE=1`. Print mode's automatic
approval is not a full permission, hook, or static-denial bypass.

For deterministic script plumbing that needs these same resolution rules, use
`../../_shared/model_resolution.py` instead of adding another hidden model
alias table. The helper keeps Stepwise-style flows, fresh-consult,
agent-delegate, model-consensus, and arch-epic automatic harnesses aligned on
exact-version preservation and fail-loud behavior.

## Asking when missing

Do not ask for runtime/model/effort merely to run a capable same-host native
child. After an external lane has been selected, apply the Codex
`gpt-5.6-sol`/`ultra` preference defaults and Kimi's
`kimi-code/k3`/`max` defaults; if a load-bearing external value is still
unspecified and cannot be inferred unambiguously, ask ONE consolidated
question listing what is missing and what it controls:

```
I need the external execution choices before dispatching these roles.

- step runtime plus any non-default effort and a model/profile outside the
  Codex and Kimi defaults: runs each step
  unless a confirmed per-step preference overrides it.
- critic runtime plus any non-default effort and a model/profile outside the
  Codex and Kimi defaults:
  independently checks each step. Worker routing
  preferences do not apply to critics unless you say so.

What should I use?
```

Do not ask six separate questions. Do not invent runtime, model, or effort
defaults beyond the documented Sol and Kimi exceptions. Ask and wait. If
native children can do the job and no external benefit was requested or
discovered, proceed natively instead of manufacturing this question.

If the user answers with one complete value ("Codex gpt-5.6-sol medium
everywhere"), apply it to both worker and critic defaults and announce that
before executing. If they answer with a worker-only override ("copywriting on
Claude Fable 5.1"), resolve only the affected steps externally and leave other
roles on their confirmed native/default policy unless the user says otherwise.
Do not ask merely because the user used spaces, dots, or omitted a runtime
prefix when the runtime and exact version are otherwise clear; resolve the
same-version spelling first.

## External runtime inference

External runtime is separate from model and effort.

Infer runtime only when the evidence is unambiguous:

- a target repo says "run with Codex"
- the user says "Claude Fable 5.1", "Codex gpt-5.6-sol", "Luna", "Terra",
  "Grok Build", "Kimi", or "K3"
- the user says "Codex Fugu", "Fugu high", or "Fugu Ultra xhigh"
- an installed CLI supports only the named model family and the user clearly
  intended that family

When inference is ambiguous, ask. Do not build a hidden model-name lookup
table. The runtime choice must be explainable in the Phase 1 announcement.
Once runtime is known, resolve the model phrase using the exact-version rules
above instead of passing raw shorthand through to the CLI.

An external critic runtime defaults to the external critic default from intake.
If the user gives one complete "everywhere" choice, critic and step defaults
match. If the user gives worker-specific preferences, critics stay on their
native/default policy unless explicitly overridden.

## Pinning

Once set, the full dispatch policy is written into `state.json` and pinned
with `execution_sha256`. It records transport and starting context for every
role plus resolved external defaults and raw routing-preference quotes when
the external adapter is used.
Changing it mid-run clears run state.

Per-step repair attempts resume the exact worker through the original
transport and reuse the same resolved execution block. A user who wants a
different external model for repair attempts should
re-invoke the skill with new execution choices; this skill does not change
horses mid-stream.

Kimi worker turns run from the original target-repo cwd and resume only through
`kimi -r <exact-session-id>`. Require a fresh `session.resume_hint` receipt
after every continuation turn. Missing assistant text or a required hint is
unrecoverable; never reuse the input id, select the latest session, or fall back
to another runtime, model, or effort. Kimi critics receive the verdict schema
inline and are new clean sessions that are never resumed, although Kimi still
persists them on disk.
