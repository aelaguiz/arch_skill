---
name: comment-loop
description: "Run the standalone repo comment-hardening workflow with a root comment ledger: exhaustively map the repo, current proof surface, and current explanatory coverage before any edits, then add or repair only high-leverage code comments, docstrings, and doc comments for shared contracts, conventions, gotchas, and subtle behavior without changing contracts or spamming obvious narration. Use when the user wants a repo-wide code-comment pass, wants the agent to deeply understand the codebase before explaining it, or wants to leave the comment audit running in Codex or Claude Code until no credible high-impact explanation gaps remain. Not for generic docs cleanup, a one-off local comment tweak, or bug fixing."
metadata:
  short-description: "Exhaustive map-first repo comment hardening loop"
---

# Comment Loop

Use this skill when the job is to exhaustively map a repo, its proof surface, and its current explanatory coverage before adding or repairing only the comments that matter most.

## When to use

- The user wants a repo-wide code-comment pass rather than one local comment tweak.
- The user wants the agent to deeply understand the repo before explaining conventions, contracts, or gotchas.
- The user wants to explain shared contracts, subtle behavior, counterintuitive flows, or high-impact conventions in code comments without changing behavior.
- The user wants to run one manual pass now or leave the explanatory hardening loop running in Codex or Claude Code until no credible high-impact comment work remains.

## When not to use

- The task is generic docs cleanup, stale README consolidation, or working-doc retirement. Use `arch-docs`.
- The task is a concrete known bug, crash, regression, or broken behavior. Use `bugs-flow`.
- The work is a repo-wide bug hunt, dead-code pass, or duplication cleanup. Use `audit-loop`.
- The task is a one-off local comment tweak with no need for exhaustive map-first triage.

## Non-negotiables

- `_comment_ledger.md` at repo root is the source of truth. Add it to the root `.gitignore` immediately.
- Triage before comment edits. Do not jump to adding comments because one line looks confusing.
- Exhaustively map shipped code surfaces, the current proof surface, and the current explanatory surface before any comment edits. If the map is incomplete, update the ledger and stop.
- When the runtime supports delegation, use parallel read-only agents during mapping. Otherwise build the same exhaustive map sequentially.
- Rank consequence of misunderstanding first, then sharedness and blast radius, then explanation weakness, then confusion and staleness signals.
- Select a comment front from the completed map, not from a hunch.
- Comments explain existing contracts, behavior, and conventions. They do not create or change them.
- If the only honest next move is a bug fix, contract clarification, or broader docs rewrite, log that and stop or route to the owning skill instead of papering over it with comments.
- Verification depth must be proportional to the downstream consequence and blast radius of the surface being explained.
- Prefer authoritative comments at canonical owner boundaries over duplicated call-site narration.
- Do not spend the pass on low-value narration while outcome-critical shared contracts or gotchas remain unexplained.
- Do not add comments that restate names, signatures, or obvious mechanics.
- Update or delete touched stale comments in the same pass. Do not preserve stale explanation for history.
- Keep comments concise and use the smallest local form that makes the truth unmistakable.
- Examples belong only when they are the clearest way to show intended use or a counterintuitive gotcha.
- Unrelated dirty or untracked files are not a blocker. Leave them alone unless they directly conflict with the current comment front or make verification unsafe.
- Default invocation with no mode is `run`.
- `review` is docs-only.
- `auto` is hook-backed in Codex and Claude Code and must fail loud when the active host runtime lacks the repo-managed `Stop` entry for the installed runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` (Codex reads it from `~/.codex/hooks.json`; Claude Code reads it from `~/.claude/settings.json`). In Codex that also includes the `codex_hooks` feature gate.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Read `references/commenting-principles.md`.
4. Resolve the mode:
   - `run`
   - `review`
   - `auto`
5. Resolve repo root, root `.gitignore`, `_comment_ledger.md`, and the host-aware `auto` controller state path described in `references/comment-loop-controller.md`.
6. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) `run`

- Create or repair `_comment_ledger.md` and the `.gitignore` entry.
- Build or refresh the exhaustive map of shipped code surfaces, the current proof surface, and the current explanatory surface.
- If the map is incomplete, record the next unfinished mapping tranche in `Next Area`, update the ledger, and stop without comment edits.
- Once the map is complete, rank comment fronts by consequence of misunderstanding first, then sharedness, then explanation weakness, then confusion and staleness signals.
- Pick the highest-priority unresolved comment front from that ranking and record the pre-edit proof plan.
- Read the implementation before writing explanation. Read tests, callers, and nearby owner boundaries as needed to prove the explanation is truthful.
- Add or repair only the high-leverage comments, docstrings, or doc comments that materially reduce misunderstanding across that front.
- Verify the changed explanation with proof proportional to the front's consequence, update the ledger, and stop only when further useful work would require a genuinely different explanation story, a new reconnaissance pass, or a real blocker.

### 2) `review`

- Stay docs-only.
- Repair the ledger if it is missing or malformed.
- Re-read the ledger and current repo state from fresh context.
- Confirm whether the map is complete, whether the current or next front comes from the ranked map, whether recent comments are truthful and high leverage, and whether verification depth matched the consequence of the touched surfaces.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next mapping tranche, comment front, or blocker plainly.

### 3) `auto`

**Arm first, disarm never.** This skill is hook-owned for `auto`. The very first step of every invocation writes a session-scoped controller state file; the very last step of the parent turn is to end the turn. Parent turns do not run the Stop hook, do not delete state, and do not clean up early — the Stop hook is the only process that clears state, and it does so only on `CLEAN`, `BLOCKED`, or deadline. Core doctrine, arm-time ensure-install, session-id rules, conflict gate, staleness sweep, and manual recovery live in `skills/_shared/controller-contract.md`. The rules below describe only what is specific to `comment-loop auto`. State lives at `.codex/comment-loop-state.<SESSION_ID>.json` (Codex) or `.claude/arch_skill/comment-loop-state.<SESSION_ID>.json` (Claude Code); see `references/comment-loop-controller.md` for the state schema.

Workflow:

1. **Arm**: run `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` → resolve session id → write state file → end the turn. The parent pass may run one truthful `run` pass (mapping-only is correct on the first turns) before ending. On Claude Code, resolve the session id first via `arch_controller_stop_hook.py --current-session`; abort with the tool's error message if it fails.
2. **Body** (hook-owned): the Stop hook launches a fresh `review` pass in the active host runtime, reads the verdict from `_comment_ledger.md`, and on `CONTINUE` starts the next `$comment-loop` pass.
3. **Disarm** (hook-owned): on `CLEAN`, the hook clears state, deletes `_comment_ledger.md`, and removes the `.gitignore` entry; on `BLOCKED`, the hook clears state and stops honestly.

`comment-loop`-specific rules:

- User-facing invocation is just `comment-loop auto`.
- Dirty or untracked files are not a blocker. Do not refuse to arm only because the repo has unrelated dirty or untracked files.
- `auto` must not degrade into low-value narration while outcome-critical shared contracts or gotchas remain unexplained.
- Do not auto-commit changes.

## Output expectations

- Update `_comment_ledger.md` in every mode.
- Keep console output short:
  - comment North Star reminder
  - punchline
  - current mapping tranche, comment front, or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, controller block, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, explanation discipline, and anti-patterns
- `references/commenting-principles.md` - distilled external best practices for useful comments
- `references/run.md` - mapping-aware comment or cleanup pass
- `references/review.md` - fresh docs-only verdict pass
- `references/comment-loop-controller.md` - comment-loop controller state schema and verdict source (core doctrine lives in `skills/_shared/controller-contract.md`)
- `references/quality-bar.md` - strong vs weak triage, findings, comments, and stop decisions
