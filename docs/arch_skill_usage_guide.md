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
- `arch-epic`

Use `miniarch-step` for full-arch work when you want the trimmed command surface. Use `arch-step` when you need the broader or helper-heavy full-arch surface.

Other shipped skills:

- `agent-definition-auditor`
- `agents-md-authoring`
- `prompt-authoring`
- `chatgpt-web`
- `skill-authoring`
- `figma-best-practices`
- `fal-ai-tools`
- `eli10`
- `pr-authoring`
- `commit-history-authoring`
- `skill-flow`
- `amir-publish`
- `codex-cleanup`
- `codex-review-yolo`
- `fresh-consult`
- `agent-delegate`
- `plan-audit`
- `plan-implement`
- `plan-swarm`
- `agent-history`
- `model-consensus`
- `contact-sheet-builder`
- `exhaustive-code-review`
- `stepwise`
- `thermo-nuclear-code-quality-review`

Examples in this guide use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

Automatic skill modes now rely on the host's native goal-mode continuation. Use Codex `/goal` or Claude Code `/goal` when you want a skill to keep moving across turns until its proof bar is met.

Install copies only the live runtime package surface. Source/build internals (`build/`, `prompts/`, `__pycache__/`, `*.pyc`, and hook cleanup helpers) are pruned from installed skills. This package no longer installs `Stop` or `SessionStart` hooks; install removes old arch_skill-owned hook entries from prior installs.

Restart Codex, Claude Code, or Gemini after install so the running process
reloads skills and drops any hook list cached before install removed old
arch_skill hook entries.

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
- `~/.agents/skills/agent-definition-auditor/`
- `~/.agents/skills/agents-md-authoring/`
- `~/.agents/skills/prompt-authoring/`
- `~/.agents/skills/chatgpt-web/`
- `~/.agents/skills/skill-authoring/`
- `~/.agents/skills/figma-best-practices/`
- `~/.agents/skills/fal-ai-tools/`
- `~/.agents/skills/eli10/`
- `~/.agents/skills/pr-authoring/`
- `~/.agents/skills/commit-history-authoring/`
- `~/.agents/skills/skill-flow/`
- `~/.agents/skills/amir-publish/`
- `~/.agents/skills/codex-cleanup/`
- `~/.agents/skills/codex-review-yolo/`
- `~/.agents/skills/fresh-consult/`
- `~/.agents/skills/agent-delegate/`
- `~/.agents/skills/plan-audit/`
- `~/.agents/skills/plan-implement/`
- `~/.agents/skills/plan-swarm/`
- `~/.agents/skills/agent-history/`
- `~/.agents/skills/model-consensus/`
- `~/.agents/skills/contact-sheet-builder/`
- `~/.agents/skills/exhaustive-code-review/`
- `~/.agents/skills/stepwise/`
- `~/.agents/skills/arch-epic/`
- `~/.agents/skills/thermo-nuclear-code-quality-review/`

The vendored maintainability rubric is also installed at `~/.claude/skills/thermo-nuclear-code-quality-review/` for Claude Code and `~/.gemini/skills/thermo-nuclear-code-quality-review/` for Gemini.

Codex reads the same installed skills from `~/.agents/skills/`. `make install` also removes older `~/.codex/skills/<skill>` mirrors from previous installs and removes old arch_skill-owned hook entries from prior installs.

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
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `agent-definition-auditor`
  - `agents-md-authoring`
  - `prompt-authoring`
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `eli10`
  - `pr-authoring`
  - `commit-history-authoring`
  - `skill-flow`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-swarm`
  - `agent-history`
  - `model-consensus`
  - `contact-sheet-builder`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`
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
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `agent-definition-auditor`
  - `agents-md-authoring`
  - `prompt-authoring`
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `eli10`
  - `pr-authoring`
  - `commit-history-authoring`
  - `skill-flow`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-swarm`
  - `agent-history`
  - `model-consensus`
  - `contact-sheet-builder`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`
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
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `eli10`
  - `pr-authoring`
  - `commit-history-authoring`
  - `skill-flow`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-swarm`
  - `model-consensus`
  - `contact-sheet-builder`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`

Install removes stale pre-skill command surfaces, removed skill packages, older Codex skill mirrors, old arch_skill-owned hook entries, and source/build internals from installed skill packages. It does not install new hooks.

`arch-loop`, `delay-poll`, `wait`, and `code-review` are removed from the live installed surface; use native `/goal` for free-form completion, the host's native scheduling/reminder surface for timed waiting or polling, and ordinary host review behavior for generic code review. `agent-history` is installed on the agents/Codex and Claude Code surfaces because its storage map covers Codex and Claude Code local history. `contact-sheet-builder` is installed on all three skill surfaces and requires Python with Pillow at runtime. `figma-best-practices`, `fal-ai-tools`, `chatgpt-web`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `plan-swarm`, `codex-cleanup`, `exhaustive-code-review`, and `thermo-nuclear-code-quality-review` are installed on all three skill surfaces, but subprocess skills still require the selected local `claude`, `codex`, `agent`, or `grok` CLI to exist on the host at invocation time. `chatgpt-web` is prompt-only and requires BrowserOS MCP plus an already logged-in ChatGPT browser session; it does not automate login. `thermo-nuclear-code-quality-review` is sourced unchanged from the vendored Cursor Team Kit plugin at `vendor/cursor/plugins/cursor-team-kit/skills/`; only that skill package is installed, not Cursor Team Kit agents or rules. `fresh-consult` is read-only: first turns start clean, second/third same-line follow-ups resume a captured exact child session id by default, turn four rotates fresh, and explicitly requested parallel consults create multiple child chains. `agent-delegate` may write to the shared worktree when invoked with an allowed write scope and can run multiple fresh-resumable workers when explicitly requested. Provider routing is fixed: Codex runs GPT/GBT/OpenAI models, Claude Code runs supported Claude models, Cursor Agent runs `composer-2.5-fast`, and Grok CLI runs `grok-build` or `grok-composer-2.5-fast`. `plan-implement` is prompt-first and local: it keeps plan-backed implementation state, proof freshness, and warm review aligned without external worker orchestration. `plan-swarm` is prompt-first: the parent agent coordinates parallel workers through `agent-delegate` and keeps human worklogs next to the plan. `exhaustive-code-review` is prompt-only and review-only: it maximizes native parallel agents, saves the review artifact under `/tmp/exhaustive-code-review/`, and does not dictate the user's workflow.

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

Use for broad or ambiguity-heavy full-arch planning, continuation, implementation, helper-assisted hardening, implementation-frontier implement/audit delivery, or implementation audit.

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
- Before Section 7 hardens, `arch-step` should inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story, such as sibling formats, readers/writers, examples, fixtures, mirrored config, generated artifacts, or live docs. It should include them now, assign them to a named later phase, explicitly exclude them, or ask one exact blocker question instead of silently leaving them contradictory.
- Compatibility posture is separate from `fallback_policy`: the plan should say whether it preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge.
- `arch-step status` is the concise readout.
- `arch-step advance` owns the full checklist and exact next-command selection.
- `arch-step consistency-pass` is the optional end-to-end cold-read helper before implementation. In Codex it uses two parallel explorer reads, and `auto-plan` includes it automatically after `phase-plan`. When it runs, `Decision: proceed to implement? yes` is only legal if the artifact is decision-complete and has no unresolved plan-shaping decisions left.
- `arch-step auto-plan` is the explicit bounded planning command after North Star approval. `DOC_PATH` is the planning ledger. It resumes from the first incomplete stage through `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`. Each stage command must write a generated receipt through `skills/arch-step/scripts/arch_stage_gate.py`; marker-only plan text is not enough to unlock the next stage. `auto-plan` says the doc is decision-complete and ready for `implement-loop` only when the receipt gate and consistency pass both approve it. In native `/goal`, it keeps moving until that proof bar is met or a true blocker stops it. Outside goal mode, it runs one bounded stage and names the exact next command.
- `arch-step` does not get to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, it must ask the user instead of guessing.
- Section 7 phase plans should protect the full destination map while building depth-first: first prove one real path through the canonical owner path and highest-risk seam, then expand along named axes.
- Phase count follows proof gates, dependency edges, reversibility or migration boundaries, and user-review boundaries rather than a preset number.
- New phase plans should use an explicit `Checklist (must all be done)` plus `Exit criteria (all required)` so a phase cannot be called complete while required obligations are still implicit.
- `arch-step implement-loop` is the explicit implementation-frontier command when the user wants repeated implement then audit passes until the audit is clean or a real blocker stops the run. It must refuse to start until `arch_stage_gate.py ready` says planning receipts are complete.
- `arch-step auto-implement` is an exact user-facing synonym for `implement-loop`.
- In that controller, implementation scope is the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this arc. Named later expansion is not current missing work until its proof gate is due; silent removal from the destination map is still a scope cut.
- After a clean full-arch code audit, `arch-step` hands off to `arch-docs` for docs cleanup using the finished artifact as context.
- In Codex or Claude Code, use native `/goal` when you want `auto-plan`, `implement-loop`, `auto-implement`, or `full-auto` to keep moving across turns until the command's proof bar is met.

### `miniarch-step`

Use when the work still needs a canonical full-arch doc, phased execution, and native goal-mode auto flow, but does not need the broader `arch-step` helper surface. This is a trimmed command surface, not a lower-effort workflow.

Examples:

- `Use $miniarch-step for this feature`
- `Use $miniarch-step auto-plan`
- `Use $miniarch-step implement docs/MY_PLAN.md`
- `Use $miniarch-step implement-loop docs/MY_PLAN.md`
- `Use $miniarch-step auto-implement docs/MY_PLAN.md`
- `Use $miniarch-step audit-implementation docs/MY_PLAN.md`

Practical rule:

- If the task no longer fits `lilarch`, but does not need `arch-step`'s broader helper surface, use `miniarch-step`.
- `miniarch-step auto-plan` is the planning command for the trimmed surface. `DOC_PATH` is the planning ledger. It resumes from the first incomplete stage through `research`, `deep-dive`, and `phase-plan`, then says the doc is decision-complete and ready for `implement-loop`.
- `miniarch-step implement-loop` is the explicit implementation-frontier command when the user wants repeated implement then audit passes until the audit is clean or a real blocker stops the run.
- `miniarch-step auto-implement` is an exact user-facing synonym for `implement-loop`.
- In that command, implementation scope is the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this arc. It hands control to fresh audit only after that frontier is done or genuinely blocked. In Codex, that fresh miniarch audit child runs with `gpt-5.4-mini` at `xhigh` reasoning effort.
- After a clean code audit, `miniarch-step` hands off to `arch-docs` for docs cleanup using the finished artifact as context.
- In Codex or Claude Code, use native `/goal` when you want the auto commands to keep moving across turns until their proof bar is met.

### `arch-epic`

Use when one execution goal is too large for a single `arch-step` plan and should be decomposed into approved, ordered sub-plans with inter-plan gates. The epic doc owns the raw goal, decomposition, sub-plan DOC_PATHs, orchestration log, decision log, and critic verdict pointers. Each sub-plan remains a real arch-step-style plan; the epic doc is not a replacement for the sub-plan plan docs.

Examples:

- `Use $arch-epic to break this migration into sub-plans and run them in order`
- `Use $arch-epic docs/EPIC_AUTH_MIGRATION_2026-04-26.md`
- `Use $arch-epic auto-plan docs/EPIC_AUTH_MIGRATION_2026-06-07.md`
- `Use $arch-epic auto-implement docs/EPIC_AUTH_MIGRATION_2026-06-07.md`
- `Use $arch-epic to automatically implement this approved epic end to end`

Practical rule:

- Interactive mode runs one visible transition at a time: draft decomposition, get approval, invoke or observe the next arch-step step, then run a fresh Claude, Codex, or Grok critic after each completed sub-plan.
- Same-session `auto-plan` is explicit and opt-in after decomposition approval. It is a strict sequential driver: it sets up the next sub-plan DOC_PATH, runs the real `$arch-step auto-plan <DOC_PATH>` sequence, requires `arch_stage_gate.py ready --doc <DOC_PATH>` to pass, marks that sub-plan `planned` only after generated receipts prove readiness, and does not start implementation. Marker-only or copied planning text is not enough.
- Same-session `auto-implement` requires all non-complete sub-plans to be `planned`, then handles one planned sub-plan at a time. It re-checks ArcStep readiness, runs real `$arch-step auto-implement <DOC_PATH>` until `audit-implementation` is COMPLETE, runs the epic critic, and marks that sub-plan `complete` only after critic `pass`. One invocation, local proof, worklog text, or ArcStep audit alone is not enough.
- The separate spawned-harness automatic mode is explicit and opt-in after decomposition approval. It asks once for a role execution table: `epic_planner`, `implementation_worker`, and `critic`.
- Role choices are resolved with the shared exact-version model resolver. Shorthand such as `fable 5 high` becomes `claude-fable-5`; `gpt 5.5 high` becomes `gpt-5.5`. There is no silent downgrade, provider switch, or effort substitution. If the user says `gpt 5.4` while choosing a model, clarify whether they meant `gpt-5.5` before launching children.
- Spawned-harness automatic mode drives sub-plans depth-first. It does not plan or implement sub-plan N+1 until sub-plan N has passed the relevant critic gates.
- Spawned automatic workers apply arch-step doctrine directly from disk and do not invoke nested `auto-plan`, `implement-loop`, or other automatic continuation commands.
- Planner and implementation worker sessions are resumable. When a fresh critic finds ordinary in-scope unfinished work, the orchestrator resumes the same planner or implementation session with observation-only evidence instead of starting a separate repair worker.
- The default child wait cadence is 180 seconds while waiting for spawned harnesses; avoid tight two-second polling loops. Long planner and implementation children can run detached with live `events.jsonl`, `stderr.log`, and `stream.log` artifacts, and the orchestrator should treat recent stream activity as progress rather than expecting an early final artifact.

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
- Use `arch-docs auto` when you want repeated cleanup passes with fresh review. In native `/goal`, it keeps going until review says clean or blocked.
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

Use when the user wants to write, edit, refactor, or audit a prompt or reusable prompt contract so it fits the user's intent, evidence needs, constraints, stop rules, and output shape without becoming brittle or overbuilt. The user does not need to name a prompt type or mode; the skill infers the shape from normal language.

Examples:

- `Use $prompt-authoring to refactor this prompt`

### `chatgpt-web`

Use when the user wants to ask ChatGPT, consult ChatGPT in the browser, get a
ChatGPT web opinion, or run a prompt with optional local attachments through
the logged-in ChatGPT UI using BrowserOS MCP. It shapes rough prompts with
`prompt-authoring` discipline, verifies that BrowserOS is already logged in to
ChatGPT, defaults to Pro with Extended thinking when no mode or effort is
specified, respects explicit Instant/Thinking/Pro and
Light/Standard/Extended/Heavy requests, and returns ChatGPT's answer with a
short receipt. It is prose-only: no scripts, runners, harnesses, OpenAI API
calls, or automated login.

Examples:

- `Use $chatgpt-web to ask ChatGPT for a Pro Extended second opinion on this plan`

### `skill-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable agent skill package with precise triggers, lean packaging, and self-contained references.

Examples:

- `Use $skill-authoring to audit this skill package`

### `figma-best-practices`

Use when the user wants to create, audit, or repair a Figma file, component library, variable/token system, prototype, Dev Mode surface, Code Connect mapping, Make kit, Sites page, Buzz template, Slides deck, or MCP-readable design artifact. The skill is prompt-only and applies bundled Figma file-craft doctrine; use implementation or Figma automation skills instead when the task is building code from a design or operating the Figma UI.

Examples:

- `Use $figma-best-practices to audit this Figma library for Dev Mode and MCP readiness`

### `eli10`

Use when the user wants any answer, explanation, plan, review, recommendation, or status update in ELI10/ELI16 plain-English style. It defines jargon on first use, names stakes, preserves exact commands/metrics/file names, and uses the decision-brief contract only when the answer is asking the user to choose.

Examples:

- `Use $eli10 to explain why this test failed`
- `Use $eli10 to format this decision question`

### `commit-history-authoring`

Use when the user wants the current branch's local-only commit messages rewritten into an informative history before sharing. The skill inspects the local commit range, diffs, old messages, trailers, and any evidenced active arch plan; then it applies a message-only rewrite with a backup branch while preserving commit boundaries, patch content, author metadata, and final tree state. It refuses dirty worktrees, remote-reachable commits, upstream-ahead branches, protected branches by default, and merge commits. It never pushes or force-pushes.

Examples:

- `Use $commit-history-authoring to rewrite this branch's WIP commits into informative local history`

### `skill-flow`

Use when the user wants to design, repair, or audit an ordered flow of multiple agent skills. It owns the flow-level question: which skills should exist, what each one owns, what artifact it hands to the next skill, and where specialist skills like `skill-authoring` or `prompt-authoring` should be used. For 30+ skill suites or any multi-skill audit by scope phrase ("audit every skill in this project", "audit the skills for flow F1"), the DAG-grounded audit sub-mode parallel-walks the suite, builds a labeled-edge DAG substrate at `<doc-dir>/<doc-slug>_DAG.md`, and surfaces wasted-energy patterns (over-promotion, redundancy, dead skills, broken peer references). The audit is read-only against the target — findings name affected files; the audit never invokes another skill at runtime. Use `arch-epic` instead for decomposing one execution goal into `arch-step` sub-plans, and use `stepwise` instead for deterministic process execution.

Examples:

- `Use $skill-flow to design the authoring and audit flow for this skill suite`
- `Use $skill-flow to audit every skill in /Users/aelaguiz/workspace/lessons_studio/`
- `Use $skill-flow to audit the skills for flow F1 in lessons_studio and render the DAG`

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

Examples:

- `Use $amir-publish`

### `fresh-consult`

Use when the user or another skill wants one or more read-only second opinions from Claude, Codex, Cursor Agent, or Grok subprocesses on concrete artifacts, completion checks, flow consistency questions, or readability/confusion checks. It is prompt-only: it writes consult prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed, captures each child chain under `/tmp/fresh-consult/...`, and reports each child verdict back to the parent.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions are preserved; there is no silent downgrade, provider switch, or effort substitution. Cursor Agent effort is encoded in the model id.

The first request in a consult line starts clean and captures a session handle. The second and third same-line requests resume that exact child session by default. The fourth same-line request starts a new clean chain unless the user explicitly asks to continue. Cold, independent, fresh-eyes, changed-runtime, changed-model, changed-effort, or changed-work-root requests start a new chain. The skill never resumes a "latest" session.

Each chain keeps `chain.json` plus per-turn `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, `execution.json`, and `session_id.txt`; resume turns also keep `resume_from.txt`. Consult children commonly take 5+ minutes; broad `xhigh` or `max` reads can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Examples:

- `Use $fresh-consult with Codex gpt-5.5 xhigh to audit whether this plan is complete`
- `Use $fresh-consult with Claude Fable 5 high for a cold read of this skill flow`
- `Use $fresh-consult to tell me whether this doc is linear and not confusing`
- `Use $fresh-consult to run three parallel cold reads on this plan`
- `Use $fresh-consult to resume that same consult and check the edited section`

Practical rule:

- Use `fresh-consult` for general Claude, Codex, Cursor Agent, or Grok second opinions, bounded read-only follow-up consults, parallel consults, cold reads, consistency audits, and completion checks. Give the child the user's ask, consult mode, exact user-named artifacts, hard constraints, and report contract; let it choose what evidence to inspect.
- Use `agent-delegate` when the fresh-resumable child should implement, edit, investigate-and-fix, run commands, or use installed skills in the shared worktree.
- Use `codex-review-yolo` when the user specifically asks for the existing Codex `-p yolo` pattern.

### `agent-delegate`

Use when the user wants one or more fresh-resumable Claude, Codex, Cursor Agent, or Grok subprocesses to do concrete work in the current workspace: implementation, editing, investigation-and-fix, command execution, verification, or installed-skill use. It is prompt-only: it writes delegation prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed in the shared worktree, captures each child `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, `execution.json`, and normally `session_id.txt` under `/tmp/agent-delegate/...`, then reports status, changed files, verification, blockers, follow-up, run directories, and session id when present.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions are preserved; there is no silent downgrade, provider switch, effort substitution, detached fallback, or separate-worktree fallback. Cursor Agent effort is encoded in the model id.

Delegated children commonly take 5+ minutes; broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Examples:

- `Use $agent-delegate with Codex gpt-5.5 xhigh to implement this README and Makefile update`
- `Use $agent-delegate with Claude Fable 5 high to fix this failing test`
- `Use $agent-delegate to run $skill-authoring on this one skill package`
- `Use $agent-delegate to run two parallel workers on these fixes`

Practical rule:

- Use `agent-delegate` for fresh-resumable or explicit parallel operational delegation where children may write files; use stateless one-shot only when explicitly requested.
- Use `fresh-consult` for read-only second opinions and completion checks.
- Use `plan-implement` for ordinary plan-backed implementation that should stay local, resumable, and review-aware.
- Use `model-consensus` for two-model plan convergence.
- Use `stepwise` or `arch-epic` when subprocesses are part of an ordered workflow with manifests, critics, repair loops, or persistent orchestration.

### `plan-audit`

Use when the user wants an existing planning artifact audited before work starts, or when code already written for a plan needs prompt-first review against that plan. It checks outcome clarity, real ambiguity, constraints, repo/code truth, depth-first risk, side doors, deletes, drift-proofing, owner path, SSOT, duplicate truth, stale docs/prompts, proof gaps, caller fit, and elegance.

`plan-audit implementation-audit` is review-only. It uses strict `approve`, `not-approved`, or `scope-inconclusive` verdicts. It does not implement, run tests, prove CI, ask for logs, investigate honesty, or replace ordinary diff or PR review.

Practical rule:

- Use `plan-audit` before implementation or for plan-backed implementation review only.
- Use `plan-implement` when the user wants implementation to proceed.
- Handle ordinary diff or PR review with the host agent's normal review response.

### `plan-implement`

Use when the user wants to implement an existing plan, phase, section, checklist, issue-body plan, or design doc while keeping implementation state easy to resume. It keeps `<PLAN_STEM>_IMPLEMENTATION_LOG.md` beside non-trivial file-backed plans, reuses proof until stale, runs checks for impact rather than habit, and uses warm plan-backed review while code is still easy to repair.

The plan remains source of truth. The plan-audit log owns `PLA-*` and `IMP-*` findings. The implementation log is only speed/resume state. Native subagents are encouraged when available for independent read, review, or safe low-collision work; manual `codex`, `claude`, `agent`, or `grok` spawning is not the default path.

Examples:

- `Use $plan-implement to implement Phase 3 of docs/example-plan.md and keep the implementation log current`
- `Use $plan-implement to continue this plan from its implementation log without rerunning proof unless it is stale`

Practical rule:

- Use `plan-implement` for normal plan-backed implementation with lightweight logs, proof freshness, and warm review.
- Use `plan-audit` for review-only work.
- Use `plan-swarm` when the user explicitly wants delegated external worker swarms.

### `plan-swarm`

Use when the user wants to implement one named phase or explicit phase range from an existing plan document as fast as possible without dropping the quality bar. It extracts a compact phase contract, decomposes the work into independently delegable slices, launches or resumes Codex, Claude, Cursor Agent, or Grok workers through `agent-delegate`, batches review/test findings into delegated repair and impact-aware verification waves, writes human worklogs next to the plan, and closes only after arbiter and thermonuclear findings are triaged.

The parent agent owns orchestration: plan interpretation, decomposition, worker prompts, parallel delegation, session reuse, review triage, and completion judgment. Coordination stays readable in the phase contract, swarm ledger, worker logs, review notes, and final phase report next to the plan.

When the user chooses Cursor Agent implementation, Composer 2.5 means `composer-2.5-fast`, including shorthand like `composer`, `composer 2.5`, `composer-2.5`, or bare `2.5` in Cursor Agent context. When the user chooses Grok implementation, plain Grok means `grok-build`; Grok Composer means `grok-composer-2.5-fast`. Review runtime/model/effort must be explicit, or the user must say review should use the same execution policy. The skill does not create worktrees, push, open PRs, use latest-session resume, or continue beyond the requested phase boundary. Local commits are ordinary checkpoints.

Examples:

- `Use $plan-swarm to finish Phase 14 of docs/PACKS/example-plan.md with Cursor Agent workers`
- `Use $plan-swarm to run the current open phase with Codex workers and a Codex review gate`

Practical rule:

- Use `plan-swarm` for accelerated delegated plan-doc-backed implementation.
- Use `plan-implement` for ordinary plan-backed implementation with lightweight logs, proof freshness, and warm review but without external worker orchestration.
- Use `agent-delegate` for one-off delegation.
- Use `stepwise` for strict ordered external processes.
- Use `arch-epic` for multi-plan epic decomposition.
- Use `fresh-consult` for read-only second opinions and completion checks.

### `model-consensus`

Use when the user wants two selected Claude, Codex, Cursor Agent, or Grok models to cross-check, critique, and iterate on a plan, architecture, investigation, design, or concept until they converge, or until they expose the smallest unresolved decision. It is prompt-only: the parent agent is the runner, orchestrates directly, launches resumable hook-suppressed child sessions where supported, and relays critiques. Do not add a deterministic runner, script, controller, or harness layer.

The user supplies runtime/model/effort for both participants, or the skill asks once. Shorthand such as `gpt 5.5 xhigh`, `Claude Fable 5 high`, `Cursor Agent composer 2.5`, or `Grok Build high` follows the shared model-resolution doctrine: Cursor Agent Composer resolves to `composer-2.5-fast`, Grok resolves to `grok-build` unless Grok Composer is named, exact versions are preserved, CLI model discovery is used when availability matters, and ambiguous IDs fail loud instead of silently downgrading.

For repo-backed investigations, root-cause work, and "read everything" cross-checks, both participants must read real evidence before agreeing. The parent records the raw user goal, exact user-named artifacts, desired output, and hard constraints. The child models choose and cite the code, docs, research, tests, commands, and local evidence they need.

For architecture or implementation-plan work, both participants must inspect canonical owner paths, repo conventions, adjacent patterns to adopt, duplicate or drifting pathways, and tests/proof surfaces. This keeps the dialogue focused on one existing way of doing the work whenever possible instead of creating a second bug path.

Participant sessions preserve live event streams by default. Normal rounds often take 5+ minutes; broad repo-grounded `xhigh` or `max` rounds can reasonably take 20-40 minutes.

Examples:

- `Use $model-consensus with Claude Fable 5 high and Codex gpt-5.5 xhigh to find the simplest architecture for this repo change`
- `Use $model-consensus with Codex gpt-5.5 xhigh in adversarial mode against Claude Sonnet 4.6 high`
- `Use $model-consensus with gpt 5.5 xhigh and Opus 4.7 max to read everything and figure out why this training path is failing`
- `Use $model-consensus to have two models iterate on this concept until they agree or name the unresolved tradeoff`

Practical rule:

- Use `model-consensus` for multi-model convergence, adversarial simplification, repo-grounded investigation convergence, and architecture refinement.
- Use `fresh-consult` for read-only second opinions, including cold first-turn
  reads and bounded same-session follow-ups.
- Use `agent-delegate` for fresh-resumable workers that may edit the shared worktree.
- Use `stepwise` or `arch-epic` when the desired output is ordered implementation, not a consensus plan.

### `contact-sheet-builder`

Use when the user wants a quick local contact sheet from existing image files,
folders, globs, or attached local image paths. It defaults to a dense labeled
PNG sheet, dynamic near-native edge-to-edge canvas sizing, `0px` outside margin,
`2px` gutters, safe temp output under `/tmp/contact-sheet-builder/`, automatic
pagination, Preview opening on macOS, and a concise receipt. The skill uses one
Pillow renderer script because
image layout, alpha handling, overwrite checks, Preview opening, and manifests
are deterministic work. Use `--margin` and `--gutter` only when spacing needs to
change. Use `--no-open` for headless or batch runs. Use `--page-width` and
`--page-height` only when a fixed page-style overview is wanted. Invoke the
script directly with the `python3` that has Pillow installed.

Examples:

- `Use $contact-sheet-builder to make a labeled contact sheet from this folder`
- `Use $contact-sheet-builder on these before and after shots`
- `Use $contact-sheet-builder with no labels and 4 columns`

Practical rule:

- Use `contact-sheet-builder` for arranging existing images only.
- Use theme/image-generation skills when the user wants new images or generated
  variants.
- Use Figma, slide, doc, PDF, or video tools when the requested artifact is not
  a local image contact sheet.

### `exhaustive-code-review`

Use when the user wants a prompt-only exhaustive code review over a branch,
diff, path set, plan scope, or completion claim, and wants the review saved to
disk. It maximizes native parallel agents, reviews touched files, changed
hunks, abstractions, callers, duplicate paths, side doors, stale truth,
tests/proof, docs, generated artifacts, prompts, config, and other live truth
surfaces, then saves
`target.md`, `coverage.md`, `findings.md`, and `verdict.md` under
`/tmp/exhaustive-code-review/...`. Its verdicts are `approve`, `not-approved`,
or `coverage-incomplete`.

Examples:

- `Use $exhaustive-code-review on this full branch`
- `Use $exhaustive-code-review on the current diff`
- `Use $exhaustive-code-review for Phase 4 of docs/MY_PLAN.md`

Practical rule:

- Use `exhaustive-code-review` when coverage itself is the deliverable.
- Use `plan-audit implementation-audit` for plan-backed code review.
- Use `thermo-nuclear-code-quality-review` for maintainability-only review.

### `thermo-nuclear-code-quality-review`

Use when the user explicitly asks for a thermo-nuclear / thermonuclear review, a code-judo review, an especially harsh maintainability review, or a strict audit of structural quality, file sprawl, spaghetti branching, abstraction boundaries, and codebase health.

This is a vendored Cursor Team Kit rubric installed from `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/`. It has no local runner, no Stop-hook controller, and no subprocess requirement. The installer copies only this skill package; Cursor Team Kit agents and rules are not installed.

Examples:

- `Use $thermo-nuclear-code-quality-review on this diff`
- `Run a thermonuclear maintainability review`
- `Use the code-judo quality rubric on this PR`

Practical rule:

- Use `thermo-nuclear-code-quality-review` only when the user wants this unusually strict maintainability rubric.
- Handle ordinary code review requests with the host agent's normal review response unless the user names a specific review skill.
- Use `codex-review-yolo` or `fresh-consult` for broader fresh-eyes second opinions.

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
