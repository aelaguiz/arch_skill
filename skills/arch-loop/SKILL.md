---
name: arch-loop
description: "Run a hook-backed completion loop from free-form user requirements until a fresh external Codex gpt-5.4 xhigh auditor says the requirements are satisfied, blocks, or a parsed runtime/cadence/iteration cap fires. Use when the user explicitly asks to keep working or keep checking against stated requirements or named audits (for example `keep iterating until $agent-linter is clean` or `every 30 min check host X for 6h`). Not for canonical full-arch plans (use `arch-step`), repo-wide audit ledgers (use `audit-loop`), pure wait-until-true polling (use `delay-poll`), one-shot reviews, or work that fits in one turn."
metadata:
  short-description: "Hook-backed completion loop with fresh external Codex audit"
---

# Arch Loop

Hook-backed loop that keeps the parent agent working against the user's literal requirements until a fresh external Codex `gpt-5.4` `xhigh` auditor says the loop may stop.

## When to use

- The user names a stop contract in prose: "implement this and do not stop until `$agent-linter` is clean", "keep checking this host every 30 minutes for the next 6 hours", "iterate up to 5 times until tests pass".
- The user wants real hook-backed continuation in Codex or Claude Code, not prompt-only repetition.
- The user wants the termination decision from a fresh external auditor, not the parent agent's self-assessment.
- The user wants a named skill audit (such as `$agent-linter` or `$audit`) bound into the stop condition.

## When not to use

- The user wants the canonical full-arch flow with a plan doc. Use `arch-step` (`implement-loop` / `auto-implement`).
- The user wants a repo-wide audit pass with a root ledger. Use `audit-loop`, `audit-loop-sim`, or `comment-loop`.
- The user wants the docs-only suite continuation. Use `arch-docs auto`.
- The request is pure "wait until this external condition is true, then continue once". Use `delay-poll`.
- The runtime is neither Codex nor Claude Code, or the installed Stop hook is unavailable.
- The work fits in one turn and does not actually need an external auditor.
- The user wants a background daemon or remote scheduling that survives the session.

## Non-negotiables

- **Real hook-backed behavior.** The installed runner is `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`. Codex wires it via `~/.codex/hooks.json` with `--runtime codex`; Claude Code wires it via `~/.claude/settings.json` with `--runtime claude`. If the runner or the repo-managed `Stop` entry for the active runtime is missing, fail loud.
- **Fresh external verdict.** Termination comes from a Codex `gpt-5.4` `xhigh` child launched by the hook. The parent never self-certifies completion.
- **`raw_requirements` is pinned.** Capture the user's full request literally and never edit it across turns. The runner stores `sha256(raw_requirements)` as `raw_requirements_hash` at arm time and recomputes it on every read; mismatch clears state with `raw_requirements mutation detected`.
- **Audit status is evaluator-owned.** After the initial `pending` seed at arm, parent passes may update `latest_summary` and `evidence_path` but must not touch `required_skill_audits[].status`. The runner pins `(skill, target, requirement, status)` as `audits_authoritative_fingerprint`; any parent-side edit to those four fields clears state with `audit status mutation detected`.
- **Allowed status vocabulary is `pending`, `pass`, `fail`, `missing`, `inapplicable`.** Use `pending` while proof is in progress; put narrative words like `completed` or `fixing_in_progress` in `latest_summary`.
- **Deterministic cap parsing.** Only unambiguous runtime/iteration/cadence phrases parse into machine constraints; ambiguous text fails loud before the loop arms (see `references/cap-extraction.md`).
- **One controller per session.** `arch-loop` shares the duplicate-controller registry, so any other armed controller state for the same session is a conflict.
- **Do not run the Stop hook yourself.** After arming, end the turn naturally and let the hook own continuation.
- **No separate runner.** `arch-loop` is owned by the shared suite hook; do not fork a dedicated controller binary.

## First move

Read these in order before writing state:

1. `references/controller-contract.md` — state schema (including `raw_requirements_hash` and `audits_authoritative_fingerprint`), runtime state paths, lifecycle, continuation outcomes, writes matrix, and named-audit evidence shape.
2. `references/cap-extraction.md` — duration/window, cadence, and iteration phrase families; ambiguity handling; strictest-cap selection; hook-timeout fit.
3. `references/evaluator-prompt.md` — the fresh Codex evaluator's contract and its structured JSON output shape.

Then resolve the active host runtime, run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` (it fails loud if the canonical Stop entry cannot be written), and only once that succeeds capture `raw_requirements` verbatim and parse the unambiguous caps.

## Workflow

**Arm first, disarm never.** This skill is hook-owned. The first step of every invocation writes a session-scoped controller state file; the last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and only on a fresh evaluator verdict (`clean` / `blocked`), a deadline, the iteration cap, or a controller failure.

### 1) Initial invocation

1. **Arm.** Ensure-install the Stop hook (`arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>`; fails loud on any drift) → resolve the session id (on Claude Code via `arch_controller_stop_hook.py --current-session`; abort with the tool's error if it fails) → capture `raw_requirements` literally → run the deterministic cap/cadence parser → detect named audits → seed `required_skill_audits` with `status: pending` → compute `raw_requirements_hash = sha256(raw_requirements)` and write the session-scoped state file at version 2 before any work pass starts → do one bounded work pass (or one immediate grounded check when cadence-only) → refresh named audits' `latest_summary` / `evidence_path` only (do not touch `status`) → update `last_work_summary` and `last_verification_summary` → end the turn.
2. **Body** (hook-owned). The hook validates hash + fingerprint, enforces `deadline_at` and cadence fit, launches the fresh Codex evaluator, copies each audit's `status` + evidence pointer out of the evaluator JSON into state, recomputes the fingerprint, and dispatches the verdict.
3. **Disarm** (hook-owned). On `clean` or `blocked`, the hook clears state. Deadline, iteration cap, and controller failures also clear state.

### 2) Continuation invocation by the parent

- Read the armed state file. Do not ask the user to restate `raw_requirements`.
- Treat `last_next_task` as guidance, not a replacement for `raw_requirements`.
- Do one bounded work pass, refresh named-audit `latest_summary` / `evidence_path`, and end the turn. Never edit `raw_requirements`, `required_skill_audits[].status`, or the two hash fields — the runner clears state on any such mutation.
- If `last_continue_mode` was `wait_recheck`, do not act as the parent until the hook switches back to `parent_work` or the loop stops.

## Output expectations

- Initial invocation:
  - one-line North Star reminder of the captured requirement
  - punchline: armed or already clean
  - parsed caps and cadence with their source phrase
  - named audits detected
  - exact next move (typically: end the turn and let the Stop hook run)
- Continuation invocation:
  - one-line reminder of `raw_requirements`
  - what the last evaluator said and what the next bounded pass will do
  - end naturally

## Reference map

- `references/controller-contract.md` — state schema, writes matrix (including the hook-owned audit-status fingerprint), runtime state paths, lifecycle, continuation outcomes, timeout/max-iteration handling, and named-audit evidence.
- `references/cap-extraction.md` — duration/window, cadence, and iteration phrase families, ambiguity handling, strictest-cap selection, hook-timeout fit.
- `references/evaluator-prompt.md` — the canonical prompt contract for the fresh Codex `gpt-5.4` `xhigh` external evaluator, including the structured JSON output shape with `satisfied_requirements[].evidence` and `required_skill_audits[].status`.
- `references/examples.md` — canonical asks, a drift-catching example where the evaluator reverses a parent-claimed `pass`, and anti-cases.
