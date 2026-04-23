# Step prompt contract

Each step sub-session receives one of two prompts:

- **Initial prompt** on first attempt (`try-1`)
- **Resume prompt** on retry (`try-k` for `k >= 2`)

The content of both is strictly bounded. Anything outside these contracts
is orchestrator overreach.

## Initial prompt

```
You are executing step {{step_n}} of {{total_steps}} in a multi-step
process. Your job is this step only. Do not touch steps outside your
scope. End your turn when this step's work is complete.

## Process

{{target_process_name}} — defined in {{target_repo_absolute_path}}.

## Step

{{step_label}}

## How to do this step

Follow the skill or instruction:

{{skill_or_instruction}}

Its runbook lives at {{doctrine_path_for_this_step}}. Read it fully
before acting, then execute it.

## Expected artifact

{{expected_artifact_block}}

## Rules

- Work inside {{target_repo_absolute_path}} only. Do not edit files
  outside it.
- Follow the runbook's ordering. If it says read doctrine first, do
  that before editing.
- Do not claim work you did not do. If a sub-step is infeasible,
  say so explicitly and stop.
- Do not invoke any step other than the one declared above.

When done, end your turn. A critic will inspect your work.
```

## Resume prompt

The resume prompt is the critic's `resume_hint` rendered minimally. The
orchestrator does not add commentary. It does not add apology. It does
not ask "does this make sense?". The step session already has the full
context of the prior attempt in its session history.

```
A critic reviewed your last turn and flagged issues.

## Headline

{{resume_hint.headline}}

## Required fixes

{{numbered_list_of_resume_hint.required_fixes}}

## Do not redo

{{bulleted_list_of_resume_hint.do_not_redo}}

Apply the required fixes. Do not restart the whole step. When the fixes
are in place, end your turn.
```

That is the whole resume prompt. No "hope this helps" line. No "let me
know if you need clarification." The step gets a tight, actionable list.

## Why the discipline

Two temptations must be resisted:

**Tempt 1:** pad the initial prompt with generic advice ("remember to
test thoroughly"). Don't. The runbook at `doctrine_path_for_this_step`
is the authoritative guide. Our job is to point the step at it, not
restate it badly.

**Tempt 2:** on retry, re-explain the whole step. Don't. The session
already has the initial prompt, the work it did, and any tool output.
Re-explaining wastes tokens and muddies the critic's request. Send
only the critic's delta.

## Session continuity

Initial prompt goes to a fresh session (capture session id per
`session-resume.md`). Resume prompt goes to the same session via
`-r <session-id>` (Claude) or `codex exec resume <session-id>` (Codex).
Do not start a fresh session on retry — that discards the attempt
history the step session can learn from.

## Step session boundaries

A step session is expected to:

- Read the doctrine path it was pointed at.
- Execute the declared skill or instruction.
- Produce the declared artifact.
- End its turn.

A step session is not expected to:

- Plan multi-step work beyond its single step.
- Validate its own work. (The critic does that.)
- Adjust the process or the manifest. (That is a user decision handled
  outside this skill.)

If a step session finds that the declared step is genuinely impossible
(missing prerequisite, contradicted doctrine, etc.), it should say so
plainly and end its turn. The critic will record abstain, and the
orchestrator will halt and ask the user.
