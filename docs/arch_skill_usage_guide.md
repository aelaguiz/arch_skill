# arch_skill Usage Guide

This guide describes the live workflow surface for the repo.

The current skill suite is:

- `arch-step`
- `miniarch-step`
- `arch-docs`
- `arch-mini-plan`
- `lilarch`
- `bugs-flow`
- `audit-loop`
- `comment-loop`
- `audit-loop-sim`
- `goal-loop`
- `north-star-investigation`
- `arch-flow`
- `arch-skills-guide`

Use `miniarch-step` for full-arch work when you want the trimmed command surface. Use `arch-step` when you need the broader or helper-heavy full-arch surface.

Other shipped skills:

- `arch-loop`
- `delay-poll`
- `wait`
- `agent-definition-auditor`
- `agents-md-authoring`
- `prompt-authoring`
- `skill-authoring`
- `amir-publish`
- `codex-review-yolo`
- `code-review`

Examples in this guide use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

For Codex automatic `auto-plan`, `implement-loop`, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, `arch-loop`, `delay-poll`, and `wait`, also enable the Codex feature once:

```bash
codex features enable codex_hooks
```

Claude Code uses the installed settings-level `Stop` hook and does not depend on the Codex feature flag. Claude controllers that need fresh child review or check passes launch hook-suppressed child runs with `claude -p --settings '{"disableAllHooks":true}'`, so that child path must work with the machine's normal Claude auth.

For any supported auto controller in Codex or Claude Code, do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run.

Default local path:

- `~/.agents/skills/arch-step/`
- `~/.agents/skills/miniarch-step/`
- `~/.agents/skills/arch-docs/`
- `~/.agents/skills/arch-mini-plan/`
- `~/.agents/skills/lilarch/`
- `~/.agents/skills/bugs-flow/`
- `~/.agents/skills/audit-loop/`
- `~/.agents/skills/comment-loop/`
- `~/.agents/skills/audit-loop-sim/`
- `~/.agents/skills/goal-loop/`
- `~/.agents/skills/north-star-investigation/`
- `~/.agents/skills/arch-flow/`
- `~/.agents/skills/arch-skills-guide/`
- `~/.agents/skills/arch-loop/`
- `~/.agents/skills/delay-poll/`
- `~/.agents/skills/wait/`
- `~/.agents/skills/agent-definition-auditor/`
- `~/.agents/skills/agents-md-authoring/`
- `~/.agents/skills/prompt-authoring/`
- `~/.agents/skills/skill-authoring/`
- `~/.agents/skills/amir-publish/`
- `~/.agents/skills/codex-review-yolo/`
- `~/.agents/skills/code-review/`

Codex reads the same installed skills from `~/.agents/skills/`. `make install` also writes one arch_skill-managed Codex `Stop` hook through `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, writes one arch_skill-managed Claude Code `Stop` hook through `~/.claude/settings.json` pointing at the same installed runner with `--runtime claude`, repairs older repo-managed hook entries down to one active entry per runtime, and removes older `~/.codex/skills/<skill>` mirrors from previous installs.

Installed skills:

- Codex:
  - `arch-step`
  - `miniarch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `audit-loop`
  - `comment-loop`
  - `audit-loop-sim`
  - `arch-loop`
  - `delay-poll`
  - `wait`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `agent-definition-auditor`
  - `agents-md-authoring`
  - `prompt-authoring`
  - `skill-authoring`
  - `amir-publish`
  - `codex-review-yolo`
  - `code-review`
- Claude Code:
  - `arch-step`
  - `miniarch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `audit-loop`
  - `comment-loop`
  - `audit-loop-sim`
  - `arch-loop`
  - `delay-poll`
  - `wait`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `agent-definition-auditor`
  - `agents-md-authoring`
  - `prompt-authoring`
  - `skill-authoring`
  - `amir-publish`
  - `codex-review-yolo`
  - `code-review`
- Gemini:
  - `arch-step`
  - `miniarch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `audit-loop`
  - `comment-loop`
  - `audit-loop-sim`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `agent-definition-auditor`
  - `agents-md-authoring`
  - `prompt-authoring`
  - `skill-authoring`
  - `amir-publish`
  - `codex-review-yolo`

Install removes stale pre-skill command surfaces, removed skill packages, and older Codex skill mirrors. It installs one repo-managed Codex `Stop` hook in `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex` and one repo-managed Claude Code `Stop` hook in `~/.claude/settings.json` pointing at the same installed runner with `--runtime claude`. Those entries back `arch-step` automatic controllers, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, `arch-loop`, and `delay-poll`.

`arch-loop`, `delay-poll`, and `wait` are installed on Codex and Claude Code because both runtimes have a native `Stop` hook surface. Gemini still has no hook-backed auto-controller surface, so none of those three are installed there. `arch-loop` evaluator turns additionally always shell out to fresh unsandboxed Codex `gpt-5.4` `xhigh` for the external verdict, mirroring the `code-review` exception: the Claude host can arm and drive the loop, but the evaluator subprocess itself must always be Codex. `code-review` is installed on the agents/Codex and Claude Code surfaces only; Claude may host the Stop hook, but the review subprocess itself always shells out to fresh Codex.

## Shared conventions

### One planning artifact

- Full-arch and mini-plan work keep one canonical `DOC_PATH`.
- Implementation work derives `WORKLOG_PATH` from `DOC_PATH`.
- Do not create sidecar planning docs or competing checklists.

### Code is ground truth

- Anchor claims in files, symbols, tests, logs, or explicit sources.
- Ask only when repo evidence cannot answer the question.

### No hidden fallbacks

- Default to fail-loud behavior, hard cutover, and explicit deletes.
- Runtime shims, compatibility paths, and silent alternate behavior require explicit approval in the governing doc.

### Converge on canonical paths

- When full-arch work touches duplicated or drifting logic, converge onto the canonical existing path or extract one clean shared path.
- Internal convergence work may widen beyond the directly touched file set when needed to remove duplicate truth or prevent a new parallel path.
- Convergence work must not be used as an excuse to invent new product functionality, modes, or speculative infrastructure.

### Preserve behavior during refactor

- Any refactor, consolidation, or shared-path extraction needs a credible behavior-preservation check.
- Prefer existing tests, typecheck, build, instrumentation, or stable behavior-level checks before adding new tests.
- Do not write negative-value tests that only assert implementation details, deletions, or visual constants.

### Capability-first for agent-backed systems

- Understand current prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- Lean into prompt engineering, grounding, and native capabilities before inventing custom harnesses, wrappers, parsers, OCR layers, fuzzy matchers, or scripts.
- If custom tooling is still needed, the plan should say why prompt-first and capability-first options were insufficient and keep the tool narrow.
- When the real lever is prompt repair, call that out plainly and use `prompt-authoring` instead of building deterministic scaffolding around the model.

### Preserve instruction fidelity when porting

- When moving prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit process structure by default.
- Do not silently condense ordered steps, conditions, hard negatives, or escalation logic into vague summary bullets.
- If condensation is truly appropriate, record why it is safe and keep the original text recoverable in the artifact.

### Delete dead truth

- Git is the history for retired code paths, docs, comments, and instructions.
- Do not keep dead competing truth surfaces around for legacy or archaeology.
- If a touched live doc, comment, or instruction still matters after the change, rewrite it to present reality in the same run. If it no longer matters, delete it.

## Choosing a skill

### `arch-step`

Use for broad or ambiguity-heavy full-arch planning, continuation, implementation, helper-assisted hardening, full-frontier implement/audit delivery, or implementation audit.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step auto-plan`
- `Use $arch-step consistency-pass docs/MY_PLAN.md`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step implement docs/MY_PLAN.md`
- `Use $arch-step implement-loop docs/MY_PLAN.md`
- `Use $arch-step auto-implement docs/MY_PLAN.md`
- `Use $arch-step audit-implementation docs/MY_PLAN.md`

Practical rule:

- If the ask is generic full arch, the live answer is `arch-step`.
- If the ask names a full-arch command, the live answer is also `arch-step`.
- `arch-step` may widen internal refactor scope to converge on one tested path and remove duplicate truth, but it must not invent extra product functionality while doing it.
- If capability-first analysis shows the main lever is prompt repair, `arch-step` should say so plainly and point to `prompt-authoring`.
- Before Section 7 hardens, `arch-step` should inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story, such as sibling formats, readers/writers, examples, fixtures, mirrored config, generated artifacts, or live docs. It should include them now, explicitly defer or exclude them, or ask one exact blocker question instead of silently leaving them contradictory.
- Compatibility posture is separate from `fallback_policy`: the plan should say whether it preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge.
- `arch-step status` is the concise readout.
- `arch-step advance` owns the full checklist and exact next-command selection.
- `arch-step consistency-pass` is the optional end-to-end cold-read helper before implementation. In Codex it uses two parallel explorer reads, and `auto-plan` includes it automatically after `phase-plan`. When it runs, `Decision: proceed to implement? yes` is only legal if the artifact is decision-complete and has no unresolved plan-shaping decisions left.
- `arch-step auto-plan` is the explicit bounded planning controller after North Star approval. `DOC_PATH` is the planning ledger and the armed controller state lives under `.codex/` in Codex or `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent pass runs only `research`, then ends its turn. On reruns, the installed Stop hook reads the doc and feeds `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, or `consistency-pass` from the first incomplete stage it finds, then stops and says the doc is decision-complete and ready for `implement-loop`. If a real unresolved decision remains, `auto-plan` must stop and ask the user the exact blocker question; the Stop hook clears controller state.
- `arch-step` does not get to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, it must ask the user instead of guessing.
- Section 7 phase plans should split work into one coherent self-contained unit per phase, with the most fundamental units first and later phases clearly building on earlier ones.
- When two decompositions are both valid, `arch-step` should prefer more, smaller phases than fewer blended phases.
- New phase plans should use an explicit `Checklist (must all be done)` plus `Exit criteria (all required)` so a phase cannot be called complete while required obligations are still implicit.
- `arch-step implement-loop` is the explicit full-frontier controller when the user wants repeated implement then audit passes until the audit is clean or a real blocker stops the run.
- `arch-step auto-implement` is an exact user-facing synonym for `implement-loop`.
- In that controller, implementation scope is the full approved Section 7 frontier in order. It must arm loop state before implementation work, resume from the earliest incomplete or reopened phase, continue through later reachable phases, and only then hand control to fresh audit unless a real blocker stops progress.
- After a clean full-arch code audit, `arch-step` hands off to `arch-docs` for docs cleanup using the finished artifact as context.
- In Codex, the user still invokes only `auto-plan`, `implement-loop`, or `auto-implement`; the last two are the same controller. In Codex they require the repo-managed `Stop` entry in `~/.codex/hooks.json` plus enabled `codex_hooks`. In Claude Code they require the repo-managed `Stop` entry in `~/.claude/settings.json`.
- Do not run the Stop hook yourself for any of those controllers. After the controller is armed, just end the turn and let the installed Stop hook run.
- If the active runtime's hook entry, the installed runner path, or Codex's `codex_hooks` feature flag is missing, those commands should fail loud with the remediation commands instead of pretending a prompt-only loop exists. Do not check for a copied hook file under `~/.codex/hooks/`.

### `miniarch-step`

Use when the work still needs a canonical full-arch doc, phased execution, and real auto controllers in Codex or Claude Code, but does not need the broader `arch-step` helper surface. This is a trimmed command surface, not a lower-effort workflow.

Examples:

- `Use $miniarch-step for this feature`
- `Use $miniarch-step auto-plan`
- `Use $miniarch-step implement docs/MY_PLAN.md`
- `Use $miniarch-step implement-loop docs/MY_PLAN.md`
- `Use $miniarch-step auto-implement docs/MY_PLAN.md`
- `Use $miniarch-step audit-implementation docs/MY_PLAN.md`

Practical rule:

- If the task no longer fits `lilarch`, but does not need `arch-step`'s broader helper surface, use `miniarch-step`.
- `miniarch-step auto-plan` is the planning controller for the trimmed surface. `DOC_PATH` is the planning ledger and the armed controller state lives under `.codex/` in Codex or `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent pass runs only `research`, then ends its turn. On reruns, the installed Stop hook reads the doc and feeds `deep-dive` or `phase-plan` from the first incomplete stage it finds, then stops and says the doc is decision-complete and ready for `implement-loop`.
- `miniarch-step implement-loop` is the explicit full-frontier controller when the user wants repeated implement then audit passes until the audit is clean or a real blocker stops the run.
- `miniarch-step auto-implement` is an exact user-facing synonym for `implement-loop`.
- In that controller, implementation scope is the full approved Section 7 frontier in order. It must arm runtime-local controller state under `.codex/` in Codex or `.claude/arch_skill/` in Claude Code before implementation work, resume from the earliest incomplete or reopened phase, continue through later reachable phases, and only then hand control to fresh audit unless a real blocker stops progress. In Codex, that fresh miniarch audit child runs with `gpt-5.4-mini` at `xhigh` reasoning effort.
- After a clean code audit, `miniarch-step` hands off to `arch-docs` for docs cleanup using the finished artifact as context.
- These commands still rely on the repo-managed `Stop` entry for the active host runtime: `~/.codex/hooks.json` plus enabled `codex_hooks` in Codex, or `~/.claude/settings.json` in Claude Code.
- Do not run the Stop hook yourself for any of those controllers. After the controller is armed, just end the turn and let the installed Stop hook run.

### `arch-docs`

Use when the code is clean enough to trust and the job is aggressively retiring stale point-in-time docs, folding durable truth into real evergreen homes, and only keeping surviving docs that still earn a current-reader need from code.

Examples:

- `Use $arch-docs`
- `Use $arch-docs auto`

Practical rule:

- With no extra mode, `arch-docs` runs the normal one-pass DGTFO docs-health pass, should resolve scope from explicit user context, active arch context, or the repo docs surface, should use git history when keep/delete judgment depends on whether a doc is an obsolete point-in-time artifact, and should treat point-in-time docs older than 30 days as presumptively stale unless the pass can show an explicit code-grounded current-reader need.
- Repo posture is evidence-based: default to `private/internal` when unclear, but in `public OSS` repos treat `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` as expected standalone docs.
- Do not trust folder names or freshness headers such as `docs/living`, `Status: LIVING`, or `Last verified`; those are claims to verify against code, not evidence that a doc should survive.
- Beyond that public baseline, create a focused new doc only when the topic is durable, differentiated, and something readers would likely seek directly, and when forcing it into the current home would make the docs worse. Otherwise fold the durable truth into an existing evergreen home and delete the stale wrapper.
- Use `arch-docs auto` in Codex or Claude Code when you want hook-backed repeated cleanup passes with fresh external evaluation.
- If a clean arch plan/worklog exists, `arch-docs` should use it as narrowing context rather than as the whole scope.

### `arch-flow`

Use for read-only checklist and next-step inspection on an arch-style doc.

Examples:

- `Use $arch-flow docs/MY_PLAN.md`
- "What’s next on this doc?"

### `arch-mini-plan`

Use when the task still needs canonical architecture blocks, but the planning should happen in one pass and follow-through should later happen in `miniarch-step` or `arch-step`, then `arch-docs` for later docs cleanup.

Examples:

- `Use $arch-mini-plan docs/MY_PLAN.md`
- "Give me the mini plan version"

### `lilarch`

Use for contained feature work that should fit in 1-3 phases.

Examples:

- `Use $lilarch for this small feature`
- "Use little arch for this improvement"

If lilarch stops fitting, escalate to `miniarch-step reformat` first, and to `arch-step reformat` when the work needs the broader full-arch helper surface.

### `bugs-flow`

Use for regressions, crashes, incidents, or Sentry/log-driven fixes.

### `audit-loop`

Use for repo-wide audit passes or "find and fix the biggest real problems" requests when the agent should first exhaustively map the codebase and current proof surface, then choose work from a consequence-first ranking rather than just picking something. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

Examples:

- `Use $audit-loop`
- `Use $audit-loop review`
- `Use $audit-loop auto`

### `comment-loop`

Use for repo-wide code comment hardening passes or "deeply understand this repo, then explain the conventions and gotchas in code" requests when the agent should first exhaustively map the repo, current proof surface, and current explanatory coverage before choosing where comments actually matter.

Examples:

- `Use $comment-loop`
- `Use $comment-loop review`
- `Use $comment-loop auto`

### `audit-loop-sim`

Use for repo-wide real-app automation passes, simulator or emulator gap hunts, impactful mobile end-to-end coverage work, or "find the biggest automation blind spots in the real app" requests when the agent should first exhaustively map the app, journeys, and current automation surface, then choose work from a consequence-first ranking rather than just picking something. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

Examples:

- `Use $audit-loop-sim`
- `Use $audit-loop-sim review`
- `Use $audit-loop-sim auto`

### `goal-loop`

Use when the goal is clear but the path is unknown and you want a controller doc plus append-only iteration log.

### `arch-loop`

Use when the user wants a generic hook-backed completion loop with no prescribed map-first flow: free-form requirements, optional named-skill audit obligations such as `$agent-linter` or `$code-review`, optional runtime/cadence/iteration caps, and a fresh unsandboxed Codex `gpt-5.4` `xhigh` external evaluator that is the only authority allowed to emit `clean` or `blocked` and stop the loop.

Examples:

- `Use $arch-loop tighten the onboarding copy across the marketing site until it reads cleanly on mobile`
- `Use $arch-loop rewrite this AGENTS.md file with $agent-linter as a required clean audit`
- `Use $arch-loop every 30 minutes check whether staging.api.internal is reachable and keep fixing infra until it is, max 8 hours`

Practical rule:

- Use `arch-loop` for open-ended "keep going until this is done" work that does not map cleanly to `audit-loop`, `comment-loop`, `audit-loop-sim`, or any of the full-arch auto controllers.
- Use `delay-poll` instead when the job is purely "wait and re-check a condition" with no parent work happening between checks.
- Use the specialized audit loops (`audit-loop`, `comment-loop`, `audit-loop-sim`) instead when the user actually wants that skill's prescribed map-first flow and artifact contract.
- Named audits are declared by writing `$skill-name` in the requirements; the evaluator treats each named audit as a required clean verdict before `clean` is legal.
- Runtime caps come from the requirements themselves (`max 8 hours`, `every 30 minutes`, `max 12 iterations`). The evaluator extracts the strictest cap and must fail loud on ambiguous duration text rather than guess.
- Continue verdicts split between `parent_work` (run another parent implementation turn now) and `wait_recheck` (sleep `cadence_seconds` inside the installed `Stop` hook, then re-run the evaluator without spending a parent turn).
- Controller state lives under `.codex/arch-loop-state.<SESSION_ID>.json` in Codex and `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json` in Claude Code.
- The evaluator subprocess is always fresh Codex `gpt-5.4` `xhigh` with `-p yolo --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox`, even when Claude hosts the Stop hook.
- Preflight must verify the active runtime's repo-managed `Stop` entry, the installed shared runner, and in Codex the `codex_hooks` feature flag. Do not preflight against a copied hook file under `~/.codex/hooks/`.
- Do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run.

### `delay-poll`

Use when the user wants Codex or Claude Code to wait on some external condition, re-check it every 30 minutes, every hour, or similar, and continue the same visible thread only after that condition becomes true.

Examples:

- `Use $delay-poll every 30 minutes check whether branch blah has been fully pushed; when it is, pull it and integrate it in`

### `wait`

Use when the user wants Codex or Claude Code to sleep for a specific parsed duration (for example `30m`, `1h30m`, `90s`, `2d`) and then continue the same visible thread with a literal resume prompt exactly once. The Stop hook sleeps and fires one resume, with no polling, no re-checking, and no fresh child run during the wait. For condition re-checking use `delay-poll`; for recurring or scheduled work use `/loop` or `schedule`.

Examples:

- `Use $wait 1h30m then continue investigating the flaky test`

### `north-star-investigation`

Use when the work is a quantified investigation with ranked hypotheses and brutal tests.

### `arch-skills-guide`

Use when the question is which live arch skill should handle the task.

### `agent-definition-auditor`

Use when the user wants a cold-read score, rationale, and improvement plan for an `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompt, or other agent-definition markdown.

### `agents-md-authoring`

Use when the user wants to write, edit, refactor, or audit a repo-root or path-local `AGENTS.md` so it stays command-first, scope-aware, and about current repo truth only.

Examples:

- `Use $agents-md-authoring to tighten this AGENTS.md`

### `prompt-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable prompt contract so it stays intent-driven, section-correct, and anti-heuristic.

Examples:

- `Use $prompt-authoring to refactor this prompt`

### `skill-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable agent skill package with precise triggers, lean packaging, and self-contained references.

Examples:

- `Use $skill-authoring to audit this skill package`

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

Examples:

- `Use $amir-publish`

### `code-review`

Use when the user wants a real, deterministic code review — on an uncommitted diff, a branch comparison, a commit range, an explicit path set, or a "is this approved plan phase actually complete?" completion-claim. `code-review` never makes the caller model the reviewer. It always shells out to a fresh unsandboxed Codex `gpt-5.4` `xhigh` synthesis subprocess, with parallel fresh Codex `gpt-5.4-mini` `xhigh` subprocesses for the required per-lens review coverage (`correctness`, `architecture`, `proof`, `docs-drift`, `security`, and a conditional `agent-linter` lens when the change touches agent-building or instruction-bearing surfaces).

The runner writes a namespaced per-run artifact tree (per-lens prompts, stream logs, final outputs, and a single synthesized `ReviewVerdict`). Direct invocation runs the runner as a one-shot. Hook-backed invocation arms state under `.codex/code-review-state.<SESSION_ID>.json` or `.claude/arch_skill/code-review-state.<SESSION_ID>.json`; the shared `arch-step` Stop-hook dispatcher then invokes the same runner. The Claude-host path is an intentional exception to the broader native-auto-loop direction: the Stop hook runs under Claude, but the review subprocess itself must always be Codex. Generic Claude auto-controllers stay Claude-native; `code-review` does not. `code-review` is review-only — it never edits the reviewed repo and never writes a "suggested patch" block.

Examples:

- `Use $code-review on the uncommitted diff`
- `Use $code-review branch-diff --base main --head feature/ingest-fix`
- `Use $code-review paths src/ingest/pipeline.py src/ingest/schema.py`
- `Use $code-review completion-claim docs/MY_PLAN.md 3`

Practical rule:

- Use `code-review` when the user wants an automated finding-set with explicit coverage guarantees, including docs-drift and agent-surface checks.
- Use `codex-review-yolo` when the user wants a narrower, more interactive `-p yolo` fresh-eyes consult on a specific artifact rather than a full lens-by-lens review.
- Gemini is intentionally not supported; the skill package is never installed on Gemini because the runner always launches fresh Codex subprocesses.

## Full-arch doc conventions

`arch-step`, `miniarch-step`, and `arch-mini-plan` all work against a canonical full-arch doc shape. Across those surfaces, the main stable markers include the following; some are owned only by the broader `arch-step` surface:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:reference_pack`
- `arch_skill:block:plan_enhancer`
- `arch_skill:block:overbuild_protector`
- `arch_skill:block:consistency_pass`
- `arch_skill:block:review_gate`
- `arch_skill:block:gaps_concerns`
- `arch_skill:block:implementation_audit`

Practical rule:

- Do not delete or rename these markers once the doc is live.
