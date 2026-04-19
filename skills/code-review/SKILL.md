---
name: code-review
description: "Run a high-signal code review on any codebase, diff, commit range, or completion claim by shelling out to a fresh unsandboxed Codex `gpt-5.4` `xhigh` reviewer. Use when the user says \"review this\", \"code review this diff\", \"audit the changes\", \"review the PR\", \"run code-review on branch X\", or wants drift-proof findings before merge/ship. Do NOT use to ask the caller model to be the reviewer (Claude/Gemini/host are never the reviewer); for `codex-review-yolo`'s narrower manual second-opinion pattern; for doc-only reviews unrelated to code behavior; or when `codex` is not installed."
metadata:
  short-description: "General code review powered by fresh unsandboxed Codex gpt-5.4 xhigh"
---

# code-review

General code review across any codebase, language, or framework. The caller model (Codex, Claude, Gemini, or another host) prepares the review, but the actual review is always performed by a fresh unsandboxed Codex `gpt-5.4` `xhigh` subprocess with no inherited session context. That independence is the point: the reviewer reads repo truth directly and returns findings-first, evidence-backed output.

The skill is review-only. It never fixes code, never asks the reviewer to fix code, and never substitutes the host model's opinion for the Codex verdict.

## When to use

- User says: "review this", "code review this diff", "audit this change", "review the PR", "run code-review".
- User has finished non-trivial work (uncommitted diff, commit range, branch diff, checklist completion claim) and wants fresh-eyes findings before merge, ship, or mark-complete.
- User wants docs-drift, duplication, test/proof adequacy, or agent-surface lint coverage rolled into one review pass.
- User wants hook-backed review triggered by Codex or Claude Code after each implementation stop.

## When not to use

- User wants the caller model to author the review. This skill always shells out to Codex.
- User wants the narrower manual second-opinion pattern with the `yolo` profile — use `$codex-review-yolo` instead.
- User wants a doc-only review unrelated to changed code behavior — use the appropriate docs skill.
- `codex` is not installed on the host. Stop and tell the user.
- No concrete review target exists (no diff, no branch, no claim). Don't spin up review on vapor.

## Non-negotiables

- **The reviewer is always fresh Codex `gpt-5.4` `xhigh`.** The caller model is not review authority.
- **Unsandboxed by default** using the explicit flags `--dangerously-bypass-approvals-and-sandbox` plus `--model gpt-5.4 -c model_reasoning_effort="xhigh"`. This matches the repo's existing pattern and is intentionally unsafe outside hardened local environments. See `references/invocation.md`.
- **No fallback reviewer.** If Codex is unavailable, parallel lens fan-out fails, or required agent-linter coverage is missing on an agent-surface target, the review fails loud rather than silently downgrading.
- **Map before findings.** The reviewer must build a repo-grounded map of changed behavior, call sites, and adjacent contracts before emitting findings. Findings without a map are noise.
- **Parallel lens coverage is required, not optional.** Correctness/regression, architecture/duplication, tests/proof, docs/contracts/telemetry drift, risk-triggered security, and `$agent-linter` when applicable each run as separate parallel `codex exec` subprocess agents at `gpt-5.4-mini` `xhigh`. The final synthesis is `gpt-5.4` `xhigh`.
- **Findings-first, sparse, evidence-backed.** No placeholder sections. No "None." filler. No style-only nits unless they create material correctness, maintainability, or drift risk. Every blocking finding cites file, symbol, line, and concrete risk.
- **Docs drift is review scope whenever behavior, commands, install paths, APIs, examples, comments, prompts, telemetry, or user-facing contracts change.** Stale touched truth surfaces are first-class findings.
- **Agent-project targets must invoke `$agent-linter`.** If the target builds or edits agents, prompts, skills, flows, or instruction-bearing runtime surfaces, the runner requires agent-linter coverage in the final synthesis. If `$agent-linter` is unavailable, report a coverage failure.
- **External research is grounding, not authority.** Best-practice claims that depend on current framework/API/security behavior must cite primary or authoritative sources. Repo truth, user intent, and authoritative local contracts outrank external advice.
- **Repo-local conventions outrank generic style.** Derive naming, idioms, and policy from `AGENTS.md`, `CLAUDE.md`, `README.md`, language config, lint/formatter config, and nearby files before reaching for external rules.

## First move

1. Confirm Codex is present and the requested model is reachable: `which codex && codex --version`.
2. Resolve the review target from the user's ask or the repo:
   - `uncommitted-diff` (default when the worktree has unstaged or staged changes and the ask is ambiguous)
   - `branch-diff` (compare two refs)
   - `commit-range` (inclusive range)
   - `paths` (explicit files or directories)
   - `completion-claim` (plan doc phase or checklist the review must validate)
3. Read `references/invocation.md` and launch the runner:
   ```bash
   python3 skills/code-review/scripts/run_code_review.py \
     --repo-root "$(git rev-parse --show-toplevel)" \
     --target uncommitted-diff \
     --output-root /tmp/code-review
   ```
4. Wait for the runner to emit the run directory path; read the final synthesis verdict from that directory.
5. Relay the verdict to the user verbatim. Spot-check any blocking finding against the cited file before acting on it.

The runner is deterministic orchestration only — target resolution, artifact capture, parallel subprocess fan-out, fail-loud coverage accounting. Review judgment lives in the Codex prompts (`references/reviewer-prompt.md`) and in the child agents, not in the Python.

## Workflow

1. **Prepare.** Resolve target, confirm Codex is reachable, and decide whether this is a direct invocation or a hook-backed invocation. For hook-backed runs, arm `.codex/code-review-state.<SESSION_ID>.json` (Codex host) or `.claude/arch_skill/code-review-state.<SESSION_ID>.json` (Claude host) with the target and objective, then let the installed Stop hook drive the run.
2. **Run.** Invoke `scripts/run_code_review.py`. The runner writes prompts, stream logs, per-lens outputs, a final synthesis output, and a coverage summary into a namespaced run directory under the chosen output root.
3. **Consume.** Read the final synthesis output. It begins with findings and ends with the `ReviewVerdict` block defined in `references/output-contract.md`.
4. **Relay.** Report the verdict to the user. Name the run directory so they can read the full synthesis and per-lens outputs.
5. **Do not fix code here.** If blocking findings need fixing, that is a separate turn. This skill is review-only.

## Output expectations

- A short user-facing summary: verdict verbatim, blocking findings quoted, non-blocking findings summarized, coverage notes (docs drift, external research, subreviews, agent-linter).
- The run directory path so the user can read the full synthesis and per-lens outputs.
- Honest coverage failures when a required lens was unavailable or the target was ambiguous. Do not hand-write a verdict on the reviewer's behalf.

## Reference map

- `references/reviewer-prompt.md` — the canonical prompt contract the runner instantiates per lens and for final synthesis
- `references/review-requirements.md` — portable review requirements: duplication/drift, platform boundaries, self-describing code, proof proportional to risk, docs drift, spam guardrails
- `references/output-contract.md` — the `ReviewVerdict` shape, findings schema, coverage notes, malformed-output handling, no-findings state
- `references/invocation.md` — direct and hook-backed invocation, exact Codex flags, run artifact layout, default model and reasoning effort, unsandboxed posture, failure behavior
