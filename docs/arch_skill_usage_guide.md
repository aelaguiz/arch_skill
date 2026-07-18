# arch_skill Usage Guide

This guide describes the live workflow surface for the repo.

## Scope And Architectural Convergence

Fixed-scope plans build the human-authorized outcome with the smallest
sufficient solution. During initial architecture only, a planner may include
the smallest evidenced same-contract caller migration, owner move, cutover, or
delete needed to avoid competing authority. That initial convergence closure
is recorded in the plan's Scope and Simplicity Contract and freezes before
implementation.

After freeze, only explicit human approval can expand scope. Workers, audits,
critics, cold verifiers, plan edits, Decision Log entries, tests, PR comments,
and already-built code cannot. A newly discovered adjacent path becomes a human
decision; unauthorized built work is normally subtracted. The three cynical
reviews hard-fail scope cycling when agent-created work is later used to justify
more work: code and architecture return `not-approved`, and cruft returns
`cruft-found`.

The current skill suite is:

- `arch-step`
- `arch-step-goal-prompt`
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
- `browseros`
- `chatgpt-web`
- `skill-authoring`
- `figma-best-practices`
- `fal-ai-tools`
- `eli10` (source-retained; not installed by default)
- `pr-authoring`
- `commit-history-authoring`
- `amir-publish`
- `codex-cleanup`
- `codex-babysit` (source-retained; not installed by default)
- `codex-review-yolo`
- `fresh-consult`
- `agent-delegate`
- `plan-audit`
- `plan-implement`
- `plan-conductor`
- `agent-history`
- `model-consensus`
- `contact-sheet-builder`
- `cynical-code-review`
- `cynical-architecture-review`
- `cynical-cruft-removal`
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

Install copies only the live runtime package surface. Source/build internals (`build/`, `prompts/`, `__pycache__/`, `*.pyc`, and hook cleanup helpers) are pruned from installed skills. The source-retained `codex-babysit` package is excluded from the default surface, and install removes previously installed copies. This package no longer installs `Stop` or `SessionStart` hooks; install removes old arch_skill-owned hook entries from prior installs. When a Hermes Agent home exists on the machine, install also mirrors the same surface into every existing Hermes skill root (`~/.hermes/skills/` and each `~/.hermes/profiles/<name>/skills/`) under the `arch_skill/` category directory; pass `NO_HERMES=1` to skip, and machines without Hermes are skipped automatically.

Restart Codex, Claude Code, Gemini, or Hermes Agent after install so the running process
reloads skills and drops any hook list cached before install removed old
arch_skill hook entries.

Default local path:

- `~/.agents/skills/arch-step/`
- `~/.agents/skills/arch-step-goal-prompt/`
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
- `~/.agents/skills/browseros/`
- `~/.agents/skills/chatgpt-web/`
- `~/.agents/skills/skill-authoring/`
- `~/.agents/skills/figma-best-practices/`
- `~/.agents/skills/fal-ai-tools/`
- `~/.agents/skills/pr-authoring/`
- `~/.agents/skills/commit-history-authoring/`
- `~/.agents/skills/amir-publish/`
- `~/.agents/skills/codex-cleanup/`
- `~/.agents/skills/codex-review-yolo/`
- `~/.agents/skills/fresh-consult/`
- `~/.agents/skills/agent-delegate/`
- `~/.agents/skills/plan-audit/`
- `~/.agents/skills/plan-implement/`
- `~/.agents/skills/plan-conductor/`
- `~/.agents/skills/agent-history/`
- `~/.agents/skills/model-consensus/`
- `~/.agents/skills/contact-sheet-builder/`
- `~/.agents/skills/cynical-code-review/`
- `~/.agents/skills/cynical-architecture-review/`
- `~/.agents/skills/cynical-cruft-removal/`
- `~/.agents/skills/exhaustive-code-review/`
- `~/.agents/skills/stepwise/`
- `~/.agents/skills/arch-epic/`
- `~/.agents/skills/thermo-nuclear-code-quality-review/`

The vendored maintainability rubric is also installed at `~/.claude/skills/thermo-nuclear-code-quality-review/` for Claude Code and `~/.gemini/skills/thermo-nuclear-code-quality-review/` for Gemini.

Codex reads the same installed skills from `~/.agents/skills/`. `make install` also removes older `~/.codex/skills/<skill>` mirrors from previous installs and removes old arch_skill-owned hook entries from prior installs.

Installed skills:

- Codex:
  - `arch-step`
  - `arch-step-goal-prompt`
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
  - `browseros`
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `pr-authoring`
  - `commit-history-authoring`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-conductor`
  - `agent-history`
  - `model-consensus`
  - `contact-sheet-builder`
  - `cynical-code-review`
  - `cynical-architecture-review`
  - `cynical-cruft-removal`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`
- Claude Code:
  - `arch-step`
  - `arch-step-goal-prompt`
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
  - `browseros`
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `pr-authoring`
  - `commit-history-authoring`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-conductor`
  - `agent-history`
  - `model-consensus`
  - `contact-sheet-builder`
  - `cynical-code-review`
  - `cynical-architecture-review`
  - `cynical-cruft-removal`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`
- Gemini:
  - `arch-step`
  - `arch-step-goal-prompt`
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
  - `browseros`
  - `chatgpt-web`
  - `skill-authoring`
  - `figma-best-practices`
  - `fal-ai-tools`
  - `pr-authoring`
  - `commit-history-authoring`
  - `amir-publish`
  - `codex-cleanup`
  - `codex-review-yolo`
  - `fresh-consult`
  - `agent-delegate`
  - `plan-audit`
  - `plan-implement`
  - `plan-conductor`
  - `model-consensus`
  - `contact-sheet-builder`
  - `cynical-code-review`
  - `cynical-architecture-review`
  - `cynical-cruft-removal`
  - `exhaustive-code-review`
  - `stepwise`
  - `arch-epic`
  - `thermo-nuclear-code-quality-review`

Install removes stale pre-skill command surfaces, removed or default-disabled skill packages such as `codex-babysit`, older Codex skill mirrors, old arch_skill-owned hook entries, and source/build internals from installed skill packages. It does not install new hooks.

The shared agent policy is installed on all supported skill surfaces. Ordinary
same-host work uses native children; deliberate external lanes still require
the matching local `claude`, `codex`, `agent`, or `grok` CLI. Provider and
model ids remain exact and never cross runtimes. `agent-delegate` owns external
editful sessions, while `fresh-consult`, `model-consensus`, `plan-conductor`,
`stepwise`, and `arch-epic` select transport for each role under the shared
policy. `browseros` is the canonical preflight before direct BrowserOS MCP
calls. `chatgpt-web` applies it and still requires BrowserOS plus a logged-in
ChatGPT session, and the vendored thermonuclear rubric remains unchanged.

## Shared conventions

### Choose agent transport and context explicitly

Agent-using workflows read
`skills/_shared/agent-orchestration-policy.md`. Prefer the active host's native
child for ordinary same-host implementation or review, then choose clean,
bounded, or full starting context deliberately. Resume the exact child when
the same role continues its own work; start a new clean child when independence
is the point.

Use an external session when it supplies a concrete benefit the native child
does not, such as another provider, a load-bearing exact model/profile,
durability beyond the parent turn, process/worktree isolation, a required
automation surface, or a structured receipt. Same-provider external Codex
processes carry extra lifecycle and shared SQLite/WAL contention cost, so weigh
that cost without turning it into a prohibition or fixed process limit.

Context isolation does not imply filesystem or permission isolation. Give
parallel editors non-overlapping ownership, keep fanout parent-owned, and make
every child return integration-ready evidence.

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
- `arch-step consistency-pass` is the optional end-to-end cold-read helper
  before implementation. It uses two new clean same-host native read-only
  explorers with disjoint scope/authority and architecture/proof lenses. They
  run concurrently only when host slots and parent integration capacity allow,
  otherwise sequentially; the parent integrates both. `auto-plan` includes it
  after `phase-plan`.
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

### `arch-step-goal-prompt`

Use when the user wants a durable Markdown goal prompt file for an ArcStep run instead of executing ArcStep immediately. It turns a rough ask plus an optional canonical `DOC_PATH` into a prompt for `$arch-step auto-plan`, `implement-loop`, `auto-implement`, or `full-auto`; it points to source truth by path, names false finish lines, and adds reviewer gates without copying the controlling plan into a second source of truth.

Examples:

- `Use $arch-step-goal-prompt to write a Markdown goal prompt for $arch-step auto-plan docs/MY_PLAN.md`
- `Use $arch-step-goal-prompt to strengthen this auto-implement goal with strict external auditors`

Practical rules:

- The ArcStep plan stays the source of truth; the goal prompt is an execution brief.
- Use `prompt-authoring` discipline for prompt quality and `arch-step` doctrine for command behavior.
- Do not add scripts, runners, controllers, launchers, or harnesses.

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
- In that command, implementation scope is the current approved ordered
  implementation frontier. It hands control to a new clean independent audit
  only after that frontier is done or genuinely blocked. `gpt-5.4-mini` with
  `xhigh` is used only when the active native schema can select and confirm it;
  otherwise the auditor uses inherited native capability. An external exact
  model is a deliberate lane only when that identity is load-bearing.
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

- Interactive mode runs one visible transition at a time, then starts a new
  clean same-host native critic after each completed sub-plan when the host can
  satisfy the role. A deliberate external critic remains available for a
  concrete provider/model/lifecycle/isolation/receipt benefit.
- Same-session `auto-plan` is explicit and opt-in after decomposition approval. It is a strict sequential driver: it sets up the next sub-plan DOC_PATH, runs the real `$arch-step auto-plan <DOC_PATH>` sequence, requires `arch_stage_gate.py ready --doc <DOC_PATH>` to pass, marks that sub-plan `planned` only after generated receipts prove readiness, and does not start implementation. Marker-only or copied planning text is not enough.
- Same-session `auto-implement` requires all non-complete sub-plans to be `planned`, then handles one planned sub-plan at a time. It re-checks ArcStep readiness, runs real `$arch-step auto-implement <DOC_PATH>` until `audit-implementation` is COMPLETE, runs the epic critic, and marks that sub-plan `complete` only after critic `pass`. One invocation, local proof, worklog text, or ArcStep audit alone is not enough.
- Role-based `auto-run` is explicit and opt-in after decomposition approval.
  Same-host planner, implementation-worker, and critic roles prefer clean
  native children; the separate external harness is selected only for a
  deliberate external benefit.
- Role choices are resolved with the shared exact-version model resolver. Shorthand such as `fable 5 high` becomes `claude-fable-5`; `gpt-5.6-sol high` becomes `gpt-5.6-sol`; `Fugu Ultra xhigh` becomes Codex profile `fugu-ultra`. There is no silent downgrade, provider switch, or effort substitution. `gpt-5.4` and `gpt-5.5` are blocked execution choices; if the user names either while choosing a model, stop and ask whether they meant `gpt-5.6-sol` before launching children.
- Role-based automatic mode drives sub-plans depth-first. Planner and
  implementation roles are resumable by exact handle; a new clean critic's
  accepted findings return to the owning role instead of creating a repair
  role. Children do not invoke nested auto workflows.
- The external harness keeps its 180-second monitoring cadence and streamed
  receipts; `run_arch_epic.py` does not choose transport or own agent judgment.

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
- Use `arch-docs auto` when you want repeated cleanup passes with a new clean
  same-host native review after each pass. In native `/goal`, it keeps going
  until review says clean or blocked.
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

Use when the user wants to write, edit, refactor, or audit a prompt, reusable prompt contract, Markdown-backed Codex goal prompt file, or paste-sized `/goal` mission brief so it fits the user's intent, evidence needs, constraints, stop rules, and output shape without becoming brittle or overbuilt. The user does not need to name a prompt type or mode; the skill infers the shape from normal language. For goal prompts, it prefers Markdown files for substantial source-doc-backed work and paste-sized `/goal` text only when needed, without duplicating linked source truth.

Examples:

- `Use $prompt-authoring to refactor this prompt`

### `browseros`

Use before the first direct BrowserOS MCP call. It owns one-page-by-default
reuse, page provenance and task authorization, target/profile identity,
observe-act-verify, unknown timeout outcomes, proof selection, connector
discovery, secrets, parallel ownership, and cleanup reconciliation. Use it
alongside a narrower BrowserOS-backed skill; that skill owns its site workflow
while `browseros` owns BrowserOS mechanics. It is not for BrowserOS
installation or vendor development.

Examples:

- `Use $browseros before updating this record in the already-open authenticated web app`

### `chatgpt-web`

Use when the user explicitly wants the ChatGPT web provider, BrowserOS-backed
capabilities, or local attachments. It shapes rough prompts with
`prompt-authoring` discipline, applies the canonical `browseros` contract,
verifies that BrowserOS is already logged in, and uses one eligible tab without
silently inheriting whatever conversation is open.
`new-clean` is the default; `continue-exact` is used only when the user asks to
continue an identifiable conversation. Independent asks remain serial but
start clean, while explicit follow-ups preserve the intended thread. It
defaults to Pro with Extended thinking when mode or effort is omitted and is
prose-only: no scripts, runners, harnesses, API calls, or automated login.

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

This package remains available in the repository for manual use but is not installed by `make install` or `make remote_install`. Normal Codex, Claude Code, and Gemini sessions therefore do not discover it from the arch_skill installed surface.

### `commit-history-authoring`

Use when the user wants the current branch's local-only commit messages rewritten into an informative history before sharing. The skill inspects the local commit range, diffs, old messages, trailers, and any evidenced active arch plan; then it applies a message-only rewrite with a backup branch while preserving commit boundaries, patch content, author metadata, and final tree state. It refuses dirty worktrees, remote-reachable commits, upstream-ahead branches, protected branches by default, and merge commits. It never pushes or force-pushes.

Examples:

- `Use $commit-history-authoring to rewrite this branch's WIP commits into informative local history`

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

Examples:

- `Use $amir-publish`

### `codex-babysit`

This package remains available in the repository for manual use but is not installed by `make install` or `make remote_install`. When used manually, it keeps an already-running Codex goal-mode tmux pane alive across real usage limits, process death, restarts, and same-session resumes. It watches the pane and verifies that Codex resumed real work after every rotation.

Examples:

- `Use $codex-babysit to keep my running Codex goal alive`

### `fresh-consult`

Use when the user or another skill wants a clean, independent read-only opinion
on a concrete artifact, completion claim, flow-consistency question, or
readability check. Ordinary same-host reviews use a new clean native child
(`fork_turns: "none"` in Codex or a clean named/custom subagent in Claude).
Cross-provider, unavailable exact-model/profile, lifecycle, isolation,
automation, or receipt needs use the external CLI lane. The parent owns fanout,
workspace-state checks, and synthesis.

For an external consult, the user supplies runtime, model/profile, and effort,
or the skill asks once. Exact versions and profiles are preserved without
silent downgrade or provider switch.

The first request starts clean and preserves the exact native child handle or
external session id. The second and third same-line requests resume that exact
reviewer by default. The fourth starts clean unless explicitly continued. A new
independent gate or changed runtime/model/effort/work root also starts clean;
the skill never resumes a merely "latest" session.

External chains keep their prompt, final, event, stderr, execution, session,
and resume receipts under `/tmp/fresh-consult/...`; native runs preserve the
host child handle and return contract. Monitor long work patiently.

Examples:

- `Use $fresh-consult with Codex gpt-5.6-sol xhigh to audit whether this plan is complete`
- `Use $fresh-consult with Fugu Ultra xhigh to audit whether this plan is complete`
- `Use $fresh-consult with Claude Fable 5 high for a cold read of this skill flow`
- `Use $fresh-consult to tell me whether this doc is linear and not confusing`
- `Use $fresh-consult to run three parallel cold reads on this plan`
- `Use $fresh-consult to resume that same consult and check the edited section`

Practical rule:

- Use `fresh-consult` for clean read-only opinions and exact-reviewer follow-ups.
- Use `agent-delegate` only for a deliberate external editful worker/session;
  dispatch ordinary same-host editful work natively.
- Use `codex-review-yolo` when the user specifically asks for the existing Codex `-p yolo` pattern.

### `agent-delegate`

Use when an editful external worker/session supplies a concrete benefit such as
another provider, a load-bearing exact model/profile, durable exact-session
continuation, process isolation, automation, or structured receipts. These are
recognition examples rather than an allowlist or approval gate. Ordinary
same-host work uses native children directly. The adapter preserves exact model
resolution, CLI invocation, namespaced receipts, shared-worktree reporting, and
exact-handle resume.

The user supplies runtime, model or profile, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.6-sol`, `GPT56SOLXI`, `fugu`, or `fugu-ultra` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions and profile names are preserved; there is no silent downgrade, provider switch, effort substitution, detached fallback, or separate-worktree fallback. Cursor Agent effort is encoded in the model id.

Delegated children commonly take 5+ minutes; broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Examples:

- `Use $agent-delegate with Codex gpt-5.6-sol xhigh to implement this README and Makefile update`
- `Use $agent-delegate with Fugu high to implement this README and Makefile update`
- `Use $agent-delegate with Claude Fable 5 high to fix this failing test`
- `Use $agent-delegate to run $skill-authoring on this one skill package`
- `Use $agent-delegate to run two parallel workers on these fixes`

Practical rule:

- Use `agent-delegate` for deliberate external editful delegation; keep any
  parallel external fanout proportionate to independent scope, current host
  state, and parent integration capacity.
- Use `fresh-consult` for read-only second opinions and completion checks.
- Use `plan-implement` for ordinary plan-backed implementation that should stay local, resumable, and review-aware.
- Use `model-consensus` for two-model plan convergence.
- Use `stepwise` or `arch-epic` when new clean workers, exact-role repair,
  independent critics, and durable orchestration are part of an ordered flow.

### `plan-audit`

Use when the user wants an existing planning artifact audited before work starts, or when code already written for a plan needs prompt-first review against that plan. It checks outcome clarity, real ambiguity, constraints, repo/code truth, depth-first risk, side doors, deletes, drift-proofing, owner path, SSOT, duplicate truth, stale docs/prompts, proof gaps, caller fit, and elegance.

`plan-audit implementation-audit` is review-only. It uses strict `approve`, `not-approved`, or `scope-inconclusive` verdicts. It does not implement, run tests, prove CI, ask for logs, investigate honesty, or replace ordinary diff or PR review.

Practical rule:

- Use `plan-audit` before implementation or for plan-backed implementation review only.
- Use `plan-implement` when the user wants implementation to proceed.
- Handle ordinary diff or PR review with the host agent's normal review response.

### `plan-implement`

Use when the user wants to implement an existing plan, phase, section, checklist, issue-body plan, or design doc while keeping implementation state easy to resume. It keeps `<PLAN_STEM>_IMPLEMENTATION_LOG.md` beside non-trivial file-backed plans, reuses proof until stale, runs checks for impact rather than habit, and uses warm plan-backed review while code is still easy to repair.

The plan remains source of truth. New independent native children start clean,
accepted repairs return to the exact implementer, and independent rechecks use
new clean critics. The parent owns scope, integration, and proof. An explicitly
requested external worker or conductor remains available under the shared
policy.

Examples:

- `Use $plan-implement to implement Phase 3 of docs/example-plan.md and keep the implementation log current`
- `Use $plan-implement to continue this plan from its implementation log without rerunning proof unless it is stale`

Practical rule:

- Use `plan-implement` for normal plan-backed implementation with lightweight logs, proof freshness, and warm review.
- Use `plan-audit` for review-only work.
- Use `plan-conductor` when the parent should remain the non-implementing
  architect/reviewer while transport-selected workers execute the plan.

### `plan-conductor`

Use when the user wants an existing plan, or an explicit phase range,
implemented by phase workers while the parent remains the non-implementing
architect and cynical reviewer. The parent extracts a conductor log and stops
before dispatch when done-state or frozen scope is not defensible.

Each phase-sized slice starts as a new clean same-host native child by default.
The parent uses `$agent-delegate` only when a concrete external benefit is worth
the added process cost. Accepted findings resume the exact worker through its
original transport; independent review gates start clean. The parent audits
every claim, delegates proof, records checkpoints, and closes only on the
plan-required proof and final whole-plan gate.

The parent never edits source code or accepts worker self-reports as truth.
Runtime/model/effort are requested only for a selected external lane; native
roles use capabilities the host can confirm.

The explicit `plan-conductor terra` shortcut remains the external end-to-end
lane: dedicated worktree, Terra xhigh roles, three new clean external cynical
reviews, repair/re-review, PR publication, and review follow-through. Merely
naming Terra does not activate that shortcut.

Examples:

- `Use $plan-conductor to implement docs/PAYMENTS_MIGRATION_2026-07-01.md end to end with Cursor Agent workers`
- `Use $plan-conductor to drive phases 2-4 of docs/example-plan.md with two Codex gpt-5.6-luna medium workers; you review everything`
- `Use $plan-conductor terra on docs/example-plan.md`

Practical rule:

- Use `plan-conductor` for whole-plan worker execution with parent review.
- Use `plan-implement` when the parent should implement the plan itself.
- Use `agent-delegate` for one concrete external delegated task.
- Use `plan-audit` to audit a plan rather than implement it.

### `model-consensus`

Use when the user wants two selected model participants to cross-check,
critique, and converge. The parent resolves transport per participant:
same-host roles use separate new clean native children when capable;
cross-provider or unavailable exact-model/profile roles use external resumable
sessions. Every round resumes each exact participant, parent relay is the
default topology, and no deterministic runner or controller is added.

The user names the participant identities. Native roles use only model
capabilities the host can confirm; an unavailable load-bearing identity selects
the external lane. External shorthand follows the shared exact model resolver.

For repo-backed investigations, root-cause work, and "read everything" cross-checks, both participants must read real evidence before agreeing. The parent records the raw user goal, exact user-named artifacts, desired output, and hard constraints. The child models choose and cite the code, docs, research, tests, commands, and local evidence they need.

For architecture or implementation-plan work, both participants must inspect canonical owner paths, repo conventions, adjacent patterns to adopt, duplicate or drifting pathways, and tests/proof surfaces. This keeps the dialogue focused on one existing way of doing the work whenever possible instead of creating a second bug path.

External participants preserve event/final receipts; native participants
preserve exact host child handles. Both are read-only and parent-integrated.

Examples:

- `Use $model-consensus with Claude Fable 5 high and Codex gpt-5.6-sol xhigh to find the simplest architecture for this repo change`
- `Use $model-consensus with Fugu Ultra xhigh and Claude Fable 5 high to test this plan`
- `Use $model-consensus with Codex gpt-5.6-sol xhigh in adversarial mode against Claude Sonnet 4.6 high; use an external Claude participant if the active host cannot confirm that exact native model`
- `Use $model-consensus with gpt-5.6-sol xhigh and Opus 4.7 max to read everything and figure out why this training path is failing`
- `Use $model-consensus to have two models iterate on this concept until they agree or name the unresolved tradeoff`

Practical rule:

- Use `model-consensus` for multi-model convergence, adversarial simplification, repo-grounded investigation convergence, and architecture refinement.
- Use `fresh-consult` for read-only second opinions, including cold first-turn
  reads and bounded same-session follow-ups.
- Use `agent-delegate` for an explicitly external editful worker/session;
  ordinary same-host work uses native children directly.
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

### `cynical-code-review`

Use when the user wants a prompt-only skeptical implementation-integrity code
review over implemented code, a branch, diff, path set, completion claim, or
optional plan-backed implementation and wants the review saved to disk. It
assumes the completion story may be misleading, treats names/docs/status/tests
as claims rather than proof, hunts name-only completion, split-brain owners,
side doors, partial unification, stale authority paths, stopped-short user
workflows, overbuilt machinery, scope contamination, fake proof receipts, and
docs/status/tests that mask broken code, then saves the review artifact under
`/tmp/cynical-code-review/...`.

Examples:

- `Use $cynical-code-review to audit this implemented plan and assume we missed the point`
- `Use $cynical-code-review on this completion claim`
- `Use $cynical-code-review to find split-brain owners and stopped-short behavior`

Practical rule:

- Use `cynical-code-review` when distrust of the implementation story is the
  job.
- Use `cynical-architecture-review` when accidental architecture and
  subtraction are the job.
- Use `exhaustive-code-review` when coverage itself is the deliverable.

### `cynical-architecture-review`

Use when the user wants a prompt-only skeptical architecture review over a
branch, diff, subsystem, plan-backed implementation, or code area and wants the
review saved to disk. It assumes the architecture may have emerged accidentally
through iteration, preserves the intended UX and hard experiment requirements,
hunts sprawl, invalid split ownership, duplicate truth, accidental
abstractions, compatibility shims, flags-as-architecture, registries, adapters,
state spread, wrong decomposition, and needless complexity, then saves
`target.md`, `architecture-map.md`, `complexity-ledger.md`,
`subtraction-map.md`, `coverage.md`, `findings.md`, and `verdict.md` under
`/tmp/cynical-architecture-review/...`.

It is not a QA/test/doc review. Tests, docs, fixtures, examples, generated
artifacts, and status text matter only when they reveal architecture truth,
architecture lies, or future-copy risk, unless the user explicitly asks for
that lane.

Examples:

- `Use $cynical-architecture-review on this subsystem`
- `Use $cynical-architecture-review to find accidental architecture and simplify it without changing the UX`
- `Use $cynical-architecture-review on this plan-backed implementation; assume the architecture just happened`

Practical rule:

- Use `cynical-architecture-review` when accidental architecture and
  subtraction are the job.
- Use `cynical-code-review` when distrust of the implementation story is the
  job.
- Use `thermo-nuclear-code-quality-review` for maintainability-only review.

### `cynical-cruft-removal`

Use when the user wants a prompt-only skeptical cleanup review over a repo,
branch, diff, subsystem, test suite, dependency set, generated artifact set, or
docs/examples/prompt surface and wants a deep deletion report saved to disk. It
assumes references are not proof of value, identifies live roots and current
purpose, hunts dead code, self-referential islands, retired V1/V2 paths, stale
feature flags, worthless tests, fake coverage, unused dependencies, obsolete
configs/scripts, stale generated artifacts, point-in-time docs/examples, and
other low-value artifacts, then saves the report under
`/tmp/cynical-cruft-removal/...`.

It is not normal QA, test coverage review, docs polish, architecture review, or
automated deletion. Tests and docs matter when they are low-value artifacts or
when they keep stale code, workflows, or APIs alive.

Examples:

- `Use $cynical-cruft-removal on this repo and give me a deep report of low-value items that should go away`
- `Use $cynical-cruft-removal on this test suite; find worthless tests and tests keeping dead code alive`
- `Use $cynical-cruft-removal to find retired V1/V2 paths, stale flags, dead configs, and generated junk`

Practical rule:

- Use `cynical-cruft-removal` when deletion value and low-value artifact
  discovery are the job.
- Use `cynical-code-review` when distrust of the implementation story is the
  job.
- Use `cynical-architecture-review` when accidental architecture and
  subtraction are the job.
- Use `arch-docs` for docs-only cleanup.

### `exhaustive-code-review`

Use when the user wants a prompt-only exhaustive code review over a branch,
diff, path set, plan scope, or completion claim, and wants the review saved to
disk. It uses coverage-led clean native read-only slices, bounds fanout by host
slots, collision risk, and parent integration capacity, reviews touched files, changed
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
- Use `cynical-architecture-review` when accidental architecture and
  subtraction are the deliverable.
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
- Use `fresh-consult` for broader fresh-eyes second opinions. Use
  `codex-review-yolo` only when the user wants the explicit Codex `-p yolo`
  profile or its external receipt contract.

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
