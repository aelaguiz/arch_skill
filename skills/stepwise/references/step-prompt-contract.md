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
  first run the safe read/help/list command or inspect the owning
  doctrine path that would prove the blocker, then say so explicitly
  and stop with that evidence.
- Do not invoke any step other than the one declared above.
- Do not invoke other skills or slash commands. The doctrine path
  above carries everything you need; picking up a second skill
  (e.g. `/loop`, `/goal-loop`) takes you outside this step's scope.

When done, end your turn. A critic will inspect your work.
```

## Resume prompt

The resume prompt is the critic's `resume_hint` rendered with a fixed,
direct failure wrapper. The orchestrator does not add its own repair ideas,
commentary, apology, or "does this make sense?" question. The step session
already has the full context of the prior attempt in its session history.

```
Your prior attempt failed this step. The critic's findings below are binding.

Do not justify the prior attempt. Do not summarize these instructions back.
Execute the required fixes in order. If a required path, tool, command, or
write primitive is unavailable, stop and report the exact blocker with the
command or path that proved it.

## Failure

{{resume_hint.headline}}

## Required fixes

{{numbered_list_of_resume_hint.required_fixes}}

## Do not redo

{{bulleted_list_of_resume_hint.do_not_redo}}

When the fixes are in place, end your turn.
```

That is the whole resume prompt. No "hope this helps" line. No "let me
know if you need clarification." The step gets a binding recovery order,
not a suggestion to re-interpret the failure.

## Why the discipline

Two temptations must be resisted:

**Tempt 1:** pad the initial prompt with generic advice ("remember to
test thoroughly"). Don't. The runbook at `doctrine_path_for_this_step`
is the authoritative guide. Our job is to point the step at it, not
restate it badly.

**Tempt 2:** on retry, re-explain the whole step. Don't. The session
already has the initial prompt, the work it did, and any tool output.
Re-explaining wastes tokens and muddies the critic's request. Send the
fixed wrapper plus only the critic's delta.

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
- Resolve obvious safe blockers inside its own step before stopping:
  missing-path claims need the exact path checked, command-availability
  claims need the help/list output or owning doctrine read, and owner-path
  claims need evidence from the owner path.
- End its turn.

A step session is not expected to:

- Plan multi-step work beyond its single step.
- Validate its own work. (The critic does that.)
- Adjust the process or the manifest. (That is a user decision handled
  outside this skill.)

If a step session finds that the declared step is genuinely impossible
(missing prerequisite, contradicted doctrine, unavailable owner primitive,
etc.), it should say so plainly with the exact path, command, or doctrine
evidence and end its turn. The critic will decide whether this is a fail,
an abstain with a known unblock, or a true user-facing blocker.
