# Model and reasoning effort: user-supplied, asked if missing

Four values must be known before Phase 2 can start:

- `step_model` — model used for each step sub-session
- `step_effort` — reasoning effort for each step sub-session
- `critic_model` — model used for each critic sub-session
- `critic_effort` — reasoning effort for each critic sub-session

They come from the user. The skill does not silently default. The skill picks
only when it genuinely has no choice (see "Asking" below).

## Why the user supplies these

Different work deserves different price points. A lesson-authoring step in a
lesson-studio repo may want a strong step model and a strong critic. A drill
of many small steps may want cheap step + strong critic. The right choice is a
user judgment, not a skill heuristic.

Asking once at the start is cheap. Guessing wrong is expensive: wrong model
wastes money or quality; wrong effort blows budget on trivial work or
under-powers hard work.

## Acceptable shapes in the user's prompt

The intake phase parses whatever the user wrote. Any of these is clear:

- "use opus 4.7 xhigh for steps and sonnet 4.6 xhigh for critic"
- "haiku medium everywhere" (one value reused for all four)
- "steps on gpt-5.4 high, critic on gpt-5.4-mini xhigh"

None of these is magic. The intake reads the phrase, maps it to the four
values, and prints back the interpretation before executing.

## Asking when missing

If one or more of the four values is unspecified and cannot be inferred
unambiguously, the skill asks ONE consolidated question listing each missing
value with the runtime it applies to and what it controls:

```
I need model/effort choices before planning steps.

- step_model + step_effort: runs each step of the process. Needs to be
  strong enough to do the actual work.
- critic_model + critic_effort: independently checks each step. Needs to
  be strong enough to catch fabrication and skipped sub-steps.

What should I use?
```

The skill does not ask four separate questions. It does not default to
gpt-5.4 xhigh "just this once". It asks and waits.

If the user answers with one value ("haiku medium"), apply to all four and
announce that before executing.

## Pinning

Once set, the four values are written into `state.json` and pinned with a
hash (same discipline as `raw_instructions`). Changing them mid-run clears
run state. This prevents the orchestrator from "upgrading" or "downgrading"
the step runtime on fail — retries use the same model and effort as the
original try, because the failure is almost always about the step's
instructions or the sub-session's attention, not the model.

A user who wants a different model for retries should re-invoke the skill
with the new choice; this skill does not change horses mid-stream.

## Runtime choice (claude vs codex)

Separate from model/effort, the step manifest declares the runtime per step
(`claude` or `codex`). The default is inferred from the target repo's
doctrine when possible (e.g., a target that says "run with codex" points the
default at codex). When inference is ambiguous, the skill asks — same rule
as above.

Critic runtime defaults to the same runtime family as the step it is
checking unless the user specified otherwise. This keeps the transcript
interpretation within one family and avoids cross-runtime format mismatches
on the critic's input.
