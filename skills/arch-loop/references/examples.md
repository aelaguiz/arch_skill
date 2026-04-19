# `arch-loop` Examples

These examples illustrate how `arch-loop` preserves free-form requirements, parses caps and cadence, seeds named audits, and defers the stop verdict to the fresh external Codex `gpt-5.4` `xhigh` evaluator. They are not a finite rulebook; the skill should understand similar requests that combine these patterns.

## 1) Named-audit clean loop

**Ask:** "Implement `docs/AGENTS_MD_AUTHORING_SKILL_2026-04-17.md` and don't stop until the plan is fully implemented and you get a clean audit by `$agent-linter`. Max runtime 5h."

**What `arch-loop` does on the initial invocation:**

- captures the full ask literally in `raw_requirements`
- parses `max runtime 5h` → `deadline_at = created_at + 18000`, `cap_evidence: [{type: "runtime", source_text: "Max runtime 5h", normalized: "deadline_at=<+18000s>"}]`
- detects `$agent-linter` → `required_skill_audits: [{skill: "agent-linter", target: "skills/agents-md-authoring", requirement: "clean bill of health", status: "pending", ...}]`
- runs runtime preflight; aborts loudly if the active host runtime's repo-managed Stop entry or the installed runner is missing
- writes the runtime-specific state file (`.codex/arch-loop-state.<SESSION_ID>.json` or `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json`)
- does one bounded implementation pass toward the plan doc's Section 7 frontier
- runs `$agent-linter` during that pass, updates its `required_skill_audits` entry with `status`, `latest_summary`, and an optional `evidence_path`
- updates `last_work_summary` and `last_verification_summary`
- ends the turn naturally

**What the Stop hook does on subsequent turns:**

- if `deadline_at` is past, clears state and stops with a timeout summary
- otherwise launches the fresh external Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`
- on `continue` + `parent_work` + a concrete `next_task`, blocks with a continuation prompt naming `$arch-loop` and the next task
- on `blocked`, clears state and stops with the evaluator's `blocker`
- on `clean`, clears state and stops with the evaluator's `summary`

**Stop condition:** the evaluator verifies that `$agent-linter` has passing evidence, the plan doc is concretely implemented, and no unsatisfied requirement remains. Only then can it return `clean`.

## 2) Cadence-driven host reachability loop

**Ask:** "Every 30 minutes, check whether host `example.com` is reachable, for the next 6 hours."

**What `arch-loop` does on the initial invocation:**

- captures the ask literally in `raw_requirements`
- parses `every 30 minutes` → `interval_seconds = 1800`
- parses `for the next 6 hours` → `deadline_at = created_at + 21600`
- `cap_evidence` records both source phrases
- `required_skill_audits` is empty (no named audit)
- runs one immediate grounded reachability check using a read-only probe appropriate for the target (for example a single `curl -sSf --max-time 10 https://example.com/` or equivalent network check)
- writes `last_verification_summary` with the probe result
- ends the turn naturally

**What the Stop hook does on subsequent turns:**

- launches the fresh external evaluator
- if the probe shows the host is reachable and `raw_requirements` is satisfied, the evaluator returns `clean`
- otherwise the evaluator returns `continue` with `continue_mode: wait_recheck` and a specific `next_task` (for example: "retry the same read-only reachability probe against example.com")
- the Stop hook sets `next_due_at = now + 1800`, sleeps until `min(next_due_at, deadline_at)`, and reruns the evaluator/check without waking the parent thread
- if `deadline_at` is reached with the host still unreachable, the hook clears state and stops with a timeout summary

**Stop condition:** the host becomes reachable before the deadline, or the deadline expires. The parent thread is only woken if the evaluator switches to `parent_work` (for example, if the user's request required follow-up work after reachability) or if the loop stops.

## 3) Iteration-capped "try twice" loop

**Ask:** "Implement the fix, run the smoke script, and stop after two attempts. If it still fails, surface the blocker."

**What `arch-loop` does:**

- captures the ask literally
- parses `stop after two attempts` (word-form magnitude) → `max_iterations = 2`
- runs one bounded implementation pass, runs the smoke script, writes `last_work_summary` and `last_verification_summary`
- ends the turn naturally

**What the Stop hook does:**

- evaluator returns `continue` + `parent_work` if the smoke still fails and more work is possible
- the hook blocks with the next task; the parent does one more bounded pass
- after the second parent pass, `iteration_count` reaches `max_iterations`; if the evaluator still returns `continue`, the hook clears state and stops with a max-iterations summary that includes `unsatisfied_requirements`
- if the evaluator returns `clean` before the cap, the loop stops clean

## Anti-case: pure wait-until-true (use `$delay-poll` instead)

**Ask:** "Wait until the remote branch `feature/x` is pushed, then pull it and integrate."

This is a pure wait-until-true request with no free-form requirement set, no external-audit contract, and no named skill audit. The canonical owner is `$delay-poll`:

- `delay-poll` already has literal `check_prompt`/`resume_prompt` preservation, interval-based waiting inside the installed Stop hook, and clean resume-on-true semantics.
- Routing this request to `arch-loop` would add an unnecessary external Codex evaluator and a heavier controller state for a purpose `delay-poll` already covers.

`arch-loop` should route the user to `$delay-poll` (by invocation guidance, not by silently re-armig the wrong controller). If the user explicitly asks for `$arch-loop` for a pure wait or names a real external-audit requirement, `arch-loop` may own it. Otherwise prefer the narrower skill.

## Anti-case: canonical full-arch plan (use `$arch-step implement-loop` instead)

**Ask:** "Run the implement-loop against `docs/SOMETHING.md` until the plan's Section 7 frontier is clean and the implementation audit is clean."

This is the canonical full-arch plan flow. `$arch-step implement-loop` (also callable as `$arch-step auto-implement`) already owns:

- the `implement`/`audit-implementation` cycle
- the fresh Stop-hook-owned implementation audit
- the approved Section 7 frontier as the authoritative scope
- the `Use $arch-docs` handoff after a clean audit

`arch-loop` should route the user to `$arch-step implement-loop` and not attempt to be a second full-arch controller.

## What these examples intentionally omit

- Exact evaluator JSON output (see `evaluator-prompt.md` for the contract).
- State file shape and write ownership (see `controller-contract.md`).
- Cap/cadence parser phrase families and ambiguity rules (see `cap-extraction.md`).
- Specialized loops that already own narrower workflows (`$audit-loop`, `$comment-loop`, `$audit-loop-sim`, `$arch-docs auto`, `$goal-loop`).
