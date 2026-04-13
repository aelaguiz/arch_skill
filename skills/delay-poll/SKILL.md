---
name: delay-poll
description: "Arm a Codex-only delay-and-check controller that waits inside the installed Stop hook, re-runs a read-only condition check on a fixed interval, and resumes the same thread when the condition becomes true. Use when the user wants Codex to keep checking something every 30 minutes, every hour, or similar and continue later when it becomes true. Not for background daemons, non-Codex runtimes, or one-shot checks."
metadata:
  short-description: "Codex wait and recheck controller"
---

# Delay Poll

Use this skill when the user wants the same visible Codex thread to wait, re-check some external condition on a fixed interval, and continue only after that condition becomes true.

## When to use

- The user wants Codex to keep checking whether something external has changed before continuing the same task.
- The user names an interval such as every 30 minutes, every hour, or similar.
- The user wants real hook-backed waiting in Codex rather than a manual reminder or a one-shot check.

## When not to use

- The task only needs one immediate check right now.
- The user wants a background scheduler, notification daemon, or work that must survive after the Codex session or host goes away.
- The runtime is not Codex, or the installed Stop-hook path is unavailable.
- The user wants open-ended repeated work rather than "wait until this condition is true, then continue." Use the owning workflow instead.

## Non-negotiables

- `delay-poll` is Codex-only and must be real hook-backed behavior. If the installed Stop-hook path or `codex_hooks` is missing, fail loud.
- Keep the waited-on condition as a literal `check_prompt` and the continuation as a literal `resume_prompt`. Do not invent git-specific, CI-specific, or service-specific heuristics.
- Do one immediate grounded check before arming the wait state. If the condition is already true, do not arm the controller.
- Default maximum wait window is 24 hours unless the user explicitly sets a different cap.
- Later polling checks stay read-only. Mutation belongs only to the resumed main thread after the condition becomes true.
- One session can arm only one arch_skill auto controller at a time.
- Do not run the Stop hook yourself. After the controller is armed, just end the turn and let Codex run the installed Stop hook.
- Internal `check` mode is suite-only. Do not advertise it as a public user workflow.

## First move

1. Resolve the mode:
   - default arm mode
   - `check` only when the invocation explicitly says `check`
2. Read the matching reference:
   - `references/arm.md`
   - `references/check.md`
3. Resolve repo root and `SESSION_ID` from `CODEX_THREAD_ID`.
4. In default arm mode, run the runtime preflight before creating controller state.

## Workflow

### 1) Default arm mode

- Resolve the literal `check_prompt`, polling interval, maximum wait window, and `resume_prompt`.
- If the user did not supply a resume prompt, use: `The waited-on condition is now satisfied. Continue the same task using this new truth and the latest check summary below.`
- Verify all runtime prerequisites:
  - Codex is the active host runtime
  - installed Stop-hook support exists in `~/.codex/hooks.json`
  - the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
  - `codex features list` shows `codex_hooks` enabled
- Run one immediate grounded read-only check against the literal `check_prompt`.
- If the condition is already true, continue immediately from the current turn with the `resume_prompt` plus the latest summary and do not arm state.
- If the condition is not yet true, create `.codex/delay-poll-state.<SESSION_ID>.json` and keep it aligned with the live wait.
- Once the controller is armed, end the turn naturally. The installed Stop hook now owns sleeping, re-checking, timeout handling, and continuation.

### 2) `check` mode

- Stay read-only.
- Evaluate only the literal `check_prompt` passed in the current invocation.
- Ground the answer in current repo truth, current external truth, or both, depending on what the prompt actually asks for.
- Return structured JSON only with:
  - `ready`
  - `summary`
  - `evidence`

## Output expectations

- Default arm mode: keep console output short:
  - waited-on condition reminder
  - punchline
  - interval and deadline
  - whether the controller armed or the condition was already ready
  - exact next move
- `check` mode: return structured JSON only. `summary` must be non-blank. `evidence` should be a short list of concrete facts, not a prose paragraph.

## Reference map

- `references/arm.md` - runtime preflight, state file contract, and arm-mode behavior
- `references/check.md` - suite-only read-only checker contract and JSON output rules
