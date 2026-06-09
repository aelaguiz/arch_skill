# Execution defaults: user-supplied, asked if missing

Six base values must be known before Phase 2 can draft a runnable manifest:

- `execution_defaults.step.runtime` - `claude`, `codex`, or `grok` for worker steps
- `execution_defaults.step.model` - model for worker steps
- `execution_defaults.step.effort` - reasoning effort for worker steps
- `execution_defaults.critic.runtime` - `claude`, `codex`, or `grok` for critics
- `execution_defaults.critic.model` - model for critics
- `execution_defaults.critic.effort` - reasoning effort for critics

These are defaults, not a promise that every step uses the same runtime. The
manifest may contain per-step overrides resolved from explicit user
preferences or hard target-repo doctrine. See `execution-routing.md`.

## Why the user supplies defaults

Different work deserves different price points. A lesson-authoring run may
want strong worker steps and a strong critic. A many-step drill may want cheap
workers and a stronger critic. The right baseline is a user judgment, not a
value the skill should invent.

Asking once at the start is cheap. Guessing wrong is expensive: wrong runtime
or model wastes money or quality; wrong effort blows budget on trivial work or
under-powers hard work.

## Acceptable shapes in the user's prompt

The intake phase parses whatever the user wrote. Any of these is clear:

- "use Claude Fable 5 high for steps and Codex gpt-5.5 xhigh for critic"
- "Codex gpt-5.5 high everywhere" (one value reused for all defaults)
- "Grok Build high for steps and Codex gpt-5.5 xhigh for critic"
- "steps on gpt-5.5 high, critic on gpt-5.5 xhigh"
- "default to Codex gpt-5.5 high, but use Claude Fable 5 for copywriting"

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
  `claude-<family>-<version-with-hyphens>`. For example, "Claude Fable 5",
  "claude fable-5", and "fable 5" under a Claude runtime all resolve to
  `claude-fable-5`; "opus 4.7" resolves to `claude-opus-4-7`. Family-only
  aliases such as `fable` or `opus` are acceptable only when the user did not
  pin a version.
- For Codex, inspect the installed CLI's model list when needed
  (`codex debug models`) and choose the available identifier with the same
  family and exact version. For example, "gpt 5.5" resolves to `gpt-5.5` if
  that exact model appears, and "gpt 5.3 codex" resolves to `gpt-5.3-codex`.
- For Grok, use `grok-build` by default when the user says `grok`,
  `grok cli`, `grok build`, or `grok-build`. Use
  `grok-composer-2.5-fast` only when the user names Grok Composer, such as
  `grok composer`, `grok composer 2.5`, or `grok-composer-2.5-fast`. Inspect
  `grok models` when availability matters.
- Bare `composer`, `composer 2.5`, or bare `2.5` is ambiguous unless the user
  explicitly names Cursor Agent or Grok in the same execution choice.
- If the user says `gpt 5.4` or a `gpt-5.4` variant while choosing a model,
  pause before execution and ask whether they meant `gpt-5.5` or explicitly
  want `gpt-5.4`. This is an intent check, not an alias rule: do not rewrite
  the version yourself.
- If the runtime is unavailable, model discovery is unavailable, the exact
  version is not present, or the phrase could map to multiple runnable
  identifiers, ask the user for the runnable model id.
- Do not run paid trial prompts to discover whether a Claude model exists.
  Use the CLI's help/list surface when available; otherwise ask.

Always announce the raw-to-resolved mapping before execution, for example:
`Claude Fable 5 high -> runtime=claude, model=claude-fable-5,
effort=high` or `Grok Build high -> runtime=grok, model=grok-build,
effort=high`.

For deterministic script plumbing that needs these same resolution rules, use
`skills/_shared/model_resolution.py` instead of adding another hidden model
alias table. The helper keeps Stepwise-style flows, fresh-consult,
agent-delegate, model-consensus, and arch-epic automatic harnesses aligned on
exact-version preservation and fail-loud behavior.

## Asking when missing

If one or more required defaults is unspecified and cannot be inferred
unambiguously, ask ONE consolidated question listing what is missing and what
it controls:

```
I need base execution choices before planning steps.

- step runtime/model/effort: runs each step unless a confirmed per-step
  preference overrides it.
- critic runtime/model/effort: independently checks each step. Worker routing
  preferences do not apply to critics unless you say so.

What should I use?
```

Do not ask six separate questions. Do not default to a favorite model "just
this once". Ask and wait.

If the user answers with one complete value ("Codex gpt-5.5 medium
everywhere"), apply it to both worker and critic defaults and announce that
before executing. If they answer with a worker-only override ("copywriting on
Claude Fable 5") but no baseline, still ask for the missing defaults.
Do not ask merely because the user used spaces, dots, or omitted a runtime
prefix when the runtime and exact version are otherwise clear; resolve the
same-version spelling first.

## Runtime inference

Runtime is separate from model and effort.

Infer runtime only when the evidence is unambiguous:

- a target repo says "run with Codex"
- the user says "Claude Fable 5", "Codex gpt-5.5", or "Grok Build"
- an installed CLI supports only the named model family and the user clearly
  intended that family

When inference is ambiguous, ask. Do not build a hidden model-name lookup
table. The runtime choice must be explainable in the Phase 1 announcement.
Once runtime is known, resolve the model phrase using the exact-version rules
above instead of passing raw shorthand through to the CLI.

Critic runtime defaults to the critic default from intake. If the user gives
only one "everywhere" choice, critic and step defaults match. If the user gives
worker-specific preferences, critics keep critic defaults unless explicitly
overridden.

## Pinning

Once set, the full execution policy is written into `state.json` and pinned
with `execution_sha256`. The policy includes resolved runnable defaults and
the raw routing preference quotes plus their resolved execution blocks.
Changing it mid-run clears run state.

Per-step repair attempts reuse the same resolved execution block as the
original try. A user who wants a different model for repair attempts should
re-invoke the skill with new execution choices; this skill does not change
horses mid-stream.
