---
name: arch-loop
description: "Run a generic hook-backed completion loop from free-form requirements until a fresh external Codex gpt-5.4 xhigh audit says the requirements are clean, more work is needed, the loop should wait/recheck on a parsed cadence, blocked, or a parsed runtime/cadence/iteration cap is reached. Use when the user explicitly asks to keep working or keep checking until stated requirements, named audits, or completion conditions are satisfied. Not for specialized full-arch plans, repo audits, comment loops, pure delay polling better owned by delay-poll, one-shot reviews, or ordinary implementation that should finish in one turn."
metadata:
  short-description: "Generic hook-backed completion loop with external Codex audit"
---

# Arch Loop

Use this skill when the user wants the same visible Codex or Claude Code thread to keep working or keep checking against free-form requirements until a fresh external Codex `gpt-5.4` `xhigh` audit says the requirements are clean, blocked, or capped out.

## When to use

- The user names a stop contract in prose: "implement this and do not stop until `$agent-linter` is clean", "keep checking this host every 30 minutes for the next 6 hours", "iterate up to 5 times until tests pass".
- The user wants real hook-backed continuation in Codex or Claude Code, not prompt-only repetition.
- The user explicitly wants the termination decision to come from a fresh external auditor, not from the parent agent's self-assessment.
- The user wants to bind a named skill audit such as `$agent-linter` or `$audit` into the loop's stop condition.

## When not to use

- The user wants the canonical full-arch flow with a plan doc. Use `arch-step` (`implement-loop` / `auto-implement`).
- The user wants a repo-wide audit pass with a root ledger. Use `audit-loop`, `audit-loop-sim`, or `comment-loop`.
- The user wants the docs-only suite continuation. Use `arch-docs auto`.
- The request is pure "wait until this external condition is true, then continue once" — that belongs to `delay-poll`.
- The runtime is neither Codex nor Claude Code, or the installed Stop hook is unavailable.
- The work fits in one turn and does not actually need an external auditor.
- The user wants a background daemon or remote scheduling that survives the session.

## Non-negotiables

- `arch-loop` must be real hook-backed behavior. The installed runner is the shared suite hook at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`. In Codex that runner is wired through `~/.codex/hooks.json` with `--runtime codex`; in Claude Code through `~/.claude/settings.json` with `--runtime claude`. If the runner or the active runtime's repo-managed `Stop` entry is missing, fail loud.
- The termination verdict comes from a fresh unsandboxed Codex `gpt-5.4` `xhigh` evaluator. The parent agent never self-certifies completion.
- Free-form prose is the product surface. Preserve the user's full request literally in `raw_requirements`. Do not collapse it into a synthetic flag grammar.
- Cap and cadence enforcement is deterministic. Only unambiguous duration/window, iteration, and cadence phrases parse into machine constraints; ambiguous cap/cadence text fails loud before the loop arms (see `references/cap-extraction.md`).
- Cadence windows that cannot fit inside the installed Stop-hook timeout fail loud. Do not turn an interval request into a manual reminder.
- Named skill audits such as `$agent-linter` are real audit obligations. The parent runs the named skill during work passes; the external evaluator verifies passing evidence before allowing `clean`.
- One session may arm multiple arch_skill auto controllers; the installed Stop hook drives one per turn. `arch-loop` is one of them and shares the duplicate-controller registry.
- Do not run the Stop hook yourself. After the controller is armed, end the turn naturally and let the installed Stop hook own continuation.
- Do not introduce a separate `arch_loop_controller.py` runner. `arch-loop` is owned by the shared suite hook.
- Do not use this skill as a long-form alternative to `delay-poll` for pure waiting; route pure `wait-until-true` requests there.

## First move

1. Read `references/controller-contract.md`.
2. Read `references/cap-extraction.md`.
3. Read `references/evaluator-prompt.md`.
4. Resolve the active host runtime, then run the runtime preflight described in `references/controller-contract.md`.
5. Capture the raw user requirements verbatim and parse only the unambiguous caps documented in `references/cap-extraction.md`.

## Workflow

### 1) Initial invocation

- Capture `raw_requirements` literally. Do not normalize, summarize, or shorten the user's request.
- Run the deterministic cap/cadence parser. Preserve every source phrase in `cap_evidence`.
- Detect explicitly named audits (for example `$agent-linter`, `$audit`) and add them to `required_skill_audits` as `pending` with the success condition copied from `raw_requirements`.
- Run runtime preflight. If any prerequisite is missing, name it and stop.
- Write the runtime-specific `arch-loop` state file before any work pass starts so the loop cannot be forgotten mid-turn.
- Do one bounded work pass toward the requirements, or one immediate grounded check when the request is cadence/check-only.
- Run the requested named audits inside that pass and update their evidence in state.
- Update `last_work_summary` and `last_verification_summary`.
- End the turn naturally. The installed Stop hook now owns continuation.

### 2) Hook-owned continuation

The installed Stop hook is the only actor that may launch the external evaluator and decide whether the loop continues. The shared runner:

- validates the state and session,
- enforces `deadline_at` and the installed hook timeout against the requested cadence,
- launches the fresh Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`,
- parses the structured verdict, and
- transitions state per the contract in `references/controller-contract.md`.

`clean` and `blocked` clear state. `continue` with `parent_work` keeps state armed and blocks with a continuation prompt that names `$arch-loop` plus the next concrete task. `continue` with `wait_recheck` keeps state armed, sleeps until the next due time, and reruns the evaluator without waking the parent thread.

### 3) Continuation invocation by the parent

- Read the armed state file. Do not ask the user to restate `raw_requirements`.
- Treat `last_next_task` as guidance, not as a replacement for the original requirements.
- Do one bounded work pass, refresh named-audit evidence, and end the turn.
- If `last_continue_mode` is `wait_recheck`, do not act as the parent until the hook decides parent work is useful or the loop stops.

## Output expectations

- Initial invocation:
  - one-line North Star reminder of the captured requirement
  - punchline: armed or already clean
  - parsed caps and cadence, with the source phrase
  - named audits detected
  - exact next move (typically: end the turn and let the installed Stop hook run)
- Continuation invocation:
  - one-line reminder of `raw_requirements`
  - what the last evaluator said and what the next bounded pass will do
  - end naturally

## Reference map

- `references/controller-contract.md` - state schema, runtime state paths, lifecycle, continuation outcomes, timeout/max-iteration handling, and named-audit evidence
- `references/cap-extraction.md` - duration/window, cadence, and iteration phrase families, ambiguity handling, strictest-cap selection, and hook-timeout fit
- `references/evaluator-prompt.md` - the canonical prompt-authored contract for the fresh Codex `gpt-5.4` `xhigh` external evaluator
- `references/examples.md` - canonical asks and an anti-case
