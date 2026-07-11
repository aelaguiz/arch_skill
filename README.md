# arch_skill

This repo ships installable agent skills centered on the arch suite for Codex CLI, Claude Code, and Gemini CLI.

## Community

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Support: [SUPPORT.md](SUPPORT.md)

The live arch suite is:

All fixed-scope lanes use the same scope law: initial architecture may include
only the smallest evidenced same-contract convergence closure, scope freezes
before implementation, and later expansion requires explicit human approval.
Workers and reviewers cannot create scope; the cynical reviews hard-fail
unauthorized scope cycling.

- `arch-step` — the broad full-arch execution surface; owns the full staged workflow, a frozen Scope and Simplicity Contract, extended helper passes, receipt-gated `auto-plan`, implementation-frontier `implement-loop`, re-entrant `full-auto`, compact `status`, and guided `advance`
- `arch-step-goal-prompt` — writes Markdown-backed goal prompt files for ArcStep `auto-plan`, `implement-loop`, `auto-implement`, and `full-auto` runs without copying the controlling plan into a second source of truth
- `miniarch-step` — the trimmed full-arch surface; keeps canonical arch docs, the same frozen scope contract, phasing, doctrine-only `full-auto`, and native goal-mode auto flow without the broader `arch-step` helper surface
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and native goal-mode `auto` docs cleanup
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `miniarch-step` or `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow whose analyze stage freezes the smallest same-contract fix closure before code
- `audit-loop` — exhaustive map-first repo audit loop with a root audit ledger, mandatory post-change self-audit, and native goal-mode `auto` continuation
- `comment-loop` — exhaustive map-first repo comment hardening loop with a root comment ledger and native goal-mode `auto` continuation
- `audit-loop-sim` — exhaustive map-first real-app automation audit loop with a root simulator ledger, mandatory post-change self-audit, and native goal-mode `auto` continuation
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill
- `arch-epic` — approved multi-plan orchestration around `arch-step`: same-host planner, worker, and critic roles prefer new clean native children with exact-role repair resume; the explicit external harness remains available for deliberate provider, exact-model/profile, lifecycle, isolation, automation, or receipt benefits

Use `miniarch-step` when the work still needs a real full-arch artifact and auto continuation, but you want the trimmed command surface instead of the broader `arch-step` helper surface. Use `arch-step` when the work is broader, more ambiguous, or needs the full helper surface.

Other shipped skills are:
- `agent-definition-auditor` — cold-reader scoring and findings for `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompts, and other agent-definition markdown
- `agents-md-authoring` — writes, edits, refactors, and audits concise repo-present `AGENTS.md` files
- `prompt-authoring` — writes, edits, refactors, and audits prompts, reusable prompt contracts, Markdown-backed Codex goal prompt files, and paste-sized `/goal` mission briefs
- `chatgpt-web` — explicit ChatGPT web-provider/browser lane with optional attachments; defaults to a new clean conversation, continues an exact conversation only when requested, and defaults to Pro with Extended thinking unless the user specifies another mode or effort
- `skill-authoring` — writes, edits, refactors, and audits prompt-first reusable agent skill packages
- `figma-best-practices` — prompt-only Figma file-craft doctrine for creating, auditing, or repairing structurally honest Figma files, libraries, variables, components, Dev Mode prep, Code Connect mapping, and Make/Sites/Buzz/Slides/MCP readiness
- `fal-ai-tools` — prompt-first fal.ai tool workflow for model discovery, schema and pricing lookup, file upload, background removal, media generation or editing, inference, polling, and result receipts using MCP when available and SDK/HTTP fallback otherwise
- `flutter-reference` — doctrine-only Flutter app and game-building reference for architecture, Dart style, state management, lifecycle, performance, testing, CI, accessibility, localization, security, platform integration, and Flame/game-loop guidance
- `eli10` — answers in maximum-readability ELI10 style: reduces reader working-memory load, leads with the point, preserves exact technical truth, defines load-bearing jargon, explains mechanisms plainly, avoids fake memory and baby talk, and uses scan markers or tables only when they clarify
- `pr-authoring` — writes and publishes high-quality GitHub pull requests from real repo changes, including an anchor-based frozen-scope receipt for plan-backed work
- `pr-review-followthrough` — explicit-invocation follow-through loop for an already-open GitHub PR: polls review feedback and checks, classifies comments against the frozen plan scope, replies on-thread with accept/decline/escalation rationale, pushes authorized fixes to the same branch, and stops at merge-ready
- `commit-history-authoring` — rewrites the current branch's branch-span commit messages from its nearest parent branch into informative history while preserving commit boundaries, patches, trailers, and backup recovery; it never pushes rewritten history
- `skill-flow` — designs, repairs, and audits ordered multi-skill flows; large-suite DAG audits use clean native read-only walkers, semantic backticked-peer extraction, a labeled-edge substrate, and evidence-backed wasted-energy findings
- `amir-publish` — personal shortcut for publishing this skills repo across Amir's usual machines
- `codex-cleanup` — dry-run-first local cleanup skill for stale `~/.codex` state that relieves multi-instance SQLite/WAL and log bloat without touching live config or credentials
- `codex-babysit` — watches an already-running Codex goal-mode tmux pane, rotates `aim` accounts only on real usage limits, restarts and resumes the same session, and keeps checking until Codex's own goal finishes
- `codex-review-yolo` — external Codex `-p yolo` reviewer for substantial diffs, plans, docs, and completion checks, with live `--json` stream logs and strict `approve | not-approved | inconclusive` verdicts
- `fresh-consult` — transport-neutral clean read-only opinions: ordinary same-host reviews use clean native children, while cross-provider or otherwise deliberate external lanes keep exact model/profile resolution, strict verdicts, resumable follow-ups, and receipts
- `agent-delegate` — explicit external editful worker/session adapter for cross-provider, load-bearing exact model/profile, durable-session, process-isolation, automation, or receipt benefits; ordinary same-host work uses native children directly
- `plan-audit` — prompt-first generic audit for existing planning artifacts plus plan-backed implementation code review; verifies human scope provenance and the pre-freeze minimal convergence closure, never adds scope from audit, and blocks unauthorized built scope without running tests or dictating workflow
- `plan-implement` — prompt-first plan-backed implementation loop that advances only through the frozen authorized frontier, dispositions warm-review findings before repair, subtracts unauthorized work, and keeps plan/audit/implementation logs and proof freshness aligned
- `plan-conductor` — prompt-first whole-plan implementation conductor with parent-owned architecture/review and per-worker native-or-external transport; its explicit Terra shortcut remains the deliberate external exact-model/worktree/PR lane
- `agent-history` — searches local Codex or Claude Code session history for prior prompts, goals, commands, corrections, tool use, and timelines from natural-language asks, using bundled read-only JSONL/SQLite helpers and concise evidence summaries
- `model-consensus` — prompt-only parent-relayed dialogue between two exact participants, resolving native or external transport separately for each, resuming each exact handle across rounds, and converging or exposing the smallest unresolved decision
- `contact-sheet-builder` — builds quick local contact sheet PNGs from existing images, folders, globs, or attached local image paths using a lean prompt contract plus one Pillow renderer; defaults to dense labeled sheets, dynamic near-native edge-to-edge canvas sizing, safe temp output, Preview opening on macOS, and concise receipts
- `fc-branded-pdf` — converts Markdown or document content into local FC / Poker Skill branded PDFs using bundled letterhead CSS, logo assets, and a local Markdown-to-PDF renderer; it verifies the rendered file and does not upload or archive to Drive
- `cynical-code-review` — prompt-only skeptical implementation-integrity review that also reconstructs human scope provenance and hard-fails unauthorized scope ratchets/cycling as `not-approved`, normally targeting subtraction
- `cynical-architecture-review` — prompt-only subtraction-first review that requires durable concepts to trace to human scope or the frozen initial closure and hard-fails architecture made "required" through review cycling as `not-approved`
- `cynical-cruft-removal` — prompt-only skeptical cleanup review that treats current reachability as separate from authorization and reports scope-laundered live code/tests/config/docs/dependencies as a `cruft-found` deletion cluster
- `exhaustive-code-review` — prompt-only exhaustive review with coverage-led clean native slices, proportional host-aware fanout, parent accounting, frozen-scope discipline, and a saved artifact under `/tmp/exhaustive-code-review/`
- `thermo-nuclear-code-quality-review` — vendored Cursor Team Kit rubric for unusually strict maintainability reviews focused on code-judo simplification, 1k-line file growth, spaghetti branching, abstraction boundaries, and structural quality
- `stepwise` — diagnostic orchestrator for ordered multi-step processes defined in another repo's doctrine; uses a new clean same-host native worker and critic when capable, resumes the exact worker for repair, and retains its subprocess machinery as the deliberate external lane

Examples in this repo use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, removes old
arch_skill-owned Codex and Claude hook entries from previous installs, removes
older `~/.codex/skills/<skill>` mirrors, and also installs the Claude Code and
Gemini CLI skill directories. Run `make crg-setup` separately when you want to
install `code-review-graph` and build this checkout's local structural graph;
normal skill installation does not rebuild it. Source/build internals
(`build/`, `prompts/`, `__pycache__/`, `*.pyc`, and hook cleanup helpers) are
pruned from installed skill packages. The
`thermo-nuclear-code-quality-review` package is sourced unchanged from the
vendored Cursor Team Kit plugin at
`vendor/cursor/plugins/cursor-team-kit/skills/`; the installer copies only that
skill package, not Cursor Team Kit agents or rules.

Agent-using skills share one runtime contract, installed at
`~/.agents/skills/_shared/agent-orchestration-policy.md`,
`~/.claude/skills/_shared/agent-orchestration-policy.md`, and
`~/.gemini/skills/_shared/agent-orchestration-policy.md`. It prefers host-native children
for ordinary same-host work, requires explicit clean/bounded/full starting
context and resume/replace semantics, and keeps external sessions available
when their provider, exact model/profile, lifecycle, isolation, automation, or
receipt benefit is worth the added process and integration cost. This is a
reasoning policy, not an external-process ban or fixed concurrency rule.

Automatic skill modes now rely on the host's native goal-mode continuation. Use Codex `/goal` or Claude Code `/goal` when you want a skill to keep moving across turns until its proof bar is met. This package no longer installs `Stop` or `SessionStart` hooks.

To skip Gemini:

```bash
make install NO_GEMINI=1
```

Installed skills:

- Default local path:
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
  - `~/.agents/skills/chatgpt-web/`
  - `~/.agents/skills/skill-authoring/`
  - `~/.agents/skills/figma-best-practices/`
  - `~/.agents/skills/fal-ai-tools/`
  - `~/.agents/skills/flutter-reference/`
  - `~/.agents/skills/eli10/`
  - `~/.agents/skills/pr-authoring/`
  - `~/.agents/skills/pr-review-followthrough/`
  - `~/.agents/skills/commit-history-authoring/`
  - `~/.agents/skills/skill-flow/`
  - `~/.agents/skills/amir-publish/`
  - `~/.agents/skills/codex-cleanup/`
  - `~/.agents/skills/codex-babysit/`
  - `~/.agents/skills/codex-review-yolo/`
  - `~/.agents/skills/fresh-consult/`
  - `~/.agents/skills/agent-delegate/`
  - `~/.agents/skills/plan-audit/`
  - `~/.agents/skills/plan-implement/`
  - `~/.agents/skills/plan-conductor/`
  - `~/.agents/skills/agent-history/`
  - `~/.agents/skills/model-consensus/`
  - `~/.agents/skills/contact-sheet-builder/`
  - `~/.agents/skills/fc-branded-pdf/`
  - `~/.agents/skills/cynical-code-review/`
  - `~/.agents/skills/cynical-architecture-review/`
  - `~/.agents/skills/cynical-cruft-removal/`
  - `~/.agents/skills/exhaustive-code-review/`
  - `~/.agents/skills/thermo-nuclear-code-quality-review/`
  - `~/.agents/skills/stepwise/`
  - `~/.agents/skills/arch-epic/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
  - `~/.claude/skills/arch-step-goal-prompt/`
  - `~/.claude/skills/miniarch-step/`
  - `~/.claude/skills/arch-docs/`
  - `~/.claude/skills/arch-mini-plan/`
  - `~/.claude/skills/lilarch/`
  - `~/.claude/skills/bugs-flow/`
  - `~/.claude/skills/audit-loop/`
  - `~/.claude/skills/comment-loop/`
  - `~/.claude/skills/audit-loop-sim/`
  - `~/.claude/skills/goal-loop/`
  - `~/.claude/skills/north-star-investigation/`
  - `~/.claude/skills/arch-flow/`
  - `~/.claude/skills/arch-skills-guide/`
  - `~/.claude/skills/agent-definition-auditor/`
  - `~/.claude/skills/agents-md-authoring/`
  - `~/.claude/skills/prompt-authoring/`
  - `~/.claude/skills/chatgpt-web/`
  - `~/.claude/skills/skill-authoring/`
  - `~/.claude/skills/figma-best-practices/`
  - `~/.claude/skills/fal-ai-tools/`
  - `~/.claude/skills/flutter-reference/`
  - `~/.claude/skills/eli10/`
  - `~/.claude/skills/pr-authoring/`
  - `~/.claude/skills/pr-review-followthrough/`
  - `~/.claude/skills/commit-history-authoring/`
  - `~/.claude/skills/skill-flow/`
  - `~/.claude/skills/amir-publish/`
  - `~/.claude/skills/codex-cleanup/`
  - `~/.claude/skills/codex-babysit/`
  - `~/.claude/skills/codex-review-yolo/`
  - `~/.claude/skills/fresh-consult/`
  - `~/.claude/skills/agent-delegate/`
  - `~/.claude/skills/plan-audit/`
  - `~/.claude/skills/plan-implement/`
  - `~/.claude/skills/plan-conductor/`
  - `~/.claude/skills/agent-history/`
  - `~/.claude/skills/model-consensus/`
  - `~/.claude/skills/contact-sheet-builder/`
  - `~/.claude/skills/fc-branded-pdf/`
  - `~/.claude/skills/cynical-code-review/`
  - `~/.claude/skills/cynical-architecture-review/`
  - `~/.claude/skills/cynical-cruft-removal/`
  - `~/.claude/skills/exhaustive-code-review/`
  - `~/.claude/skills/thermo-nuclear-code-quality-review/`
  - `~/.claude/skills/stepwise/`
  - `~/.claude/skills/arch-epic/`
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
  - `~/.gemini/skills/arch-step-goal-prompt/`
  - `~/.gemini/skills/miniarch-step/`
  - `~/.gemini/skills/arch-docs/`
  - `~/.gemini/skills/arch-mini-plan/`
  - `~/.gemini/skills/lilarch/`
  - `~/.gemini/skills/bugs-flow/`
  - `~/.gemini/skills/audit-loop/`
  - `~/.gemini/skills/comment-loop/`
  - `~/.gemini/skills/audit-loop-sim/`
  - `~/.gemini/skills/goal-loop/`
  - `~/.gemini/skills/north-star-investigation/`
  - `~/.gemini/skills/arch-flow/`
  - `~/.gemini/skills/arch-skills-guide/`
  - `~/.gemini/skills/agent-definition-auditor/`
  - `~/.gemini/skills/agents-md-authoring/`
  - `~/.gemini/skills/prompt-authoring/`
  - `~/.gemini/skills/chatgpt-web/`
  - `~/.gemini/skills/skill-authoring/`
  - `~/.gemini/skills/figma-best-practices/`
  - `~/.gemini/skills/fal-ai-tools/`
  - `~/.gemini/skills/flutter-reference/`
  - `~/.gemini/skills/eli10/`
  - `~/.gemini/skills/pr-authoring/`
  - `~/.gemini/skills/commit-history-authoring/`
  - `~/.gemini/skills/skill-flow/`
  - `~/.gemini/skills/amir-publish/`
  - `~/.gemini/skills/codex-cleanup/`
  - `~/.gemini/skills/codex-babysit/`
  - `~/.gemini/skills/codex-review-yolo/`
  - `~/.gemini/skills/fresh-consult/`
  - `~/.gemini/skills/agent-delegate/`
  - `~/.gemini/skills/plan-audit/`
  - `~/.gemini/skills/plan-implement/`
  - `~/.gemini/skills/plan-conductor/`
  - `~/.gemini/skills/model-consensus/`
  - `~/.gemini/skills/contact-sheet-builder/`
  - `~/.gemini/skills/fc-branded-pdf/`
  - `~/.gemini/skills/cynical-code-review/`
  - `~/.gemini/skills/cynical-architecture-review/`
  - `~/.gemini/skills/cynical-cruft-removal/`
  - `~/.gemini/skills/exhaustive-code-review/`
  - `~/.gemini/skills/thermo-nuclear-code-quality-review/`
  - `~/.gemini/skills/stepwise/`
  - `~/.gemini/skills/arch-epic/`

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed skill packages, older `~/.codex/skills/<skill>` mirrors, and local source/build internals so runtime routing stays unambiguous.

`arch-loop`, `delay-poll`, `wait`, and `code-review` are removed from the live installed surface; use native `/goal` for free-form completion, the host's native scheduling/reminder surface for timed waiting or polling, and ordinary host review behavior for generic code review. `agent-history` and `pr-review-followthrough` are installed on the agents/Codex and Claude Code surfaces. `agent-history` covers Codex and Claude Code local history; `pr-review-followthrough` owns live GitHub PR follow-through with replies and same-branch fixes. `contact-sheet-builder` is installed on all three skill surfaces and requires Python with Pillow at runtime. `fc-branded-pdf` is installed on all three skill surfaces and requires `pandoc` plus Chrome or Chromium at runtime. `arch-step-goal-prompt`, `figma-best-practices`, `fal-ai-tools`, `flutter-reference`, `chatgpt-web`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `plan-conductor`, `codex-cleanup`, `codex-babysit`, `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, `exhaustive-code-review`, and `thermo-nuclear-code-quality-review` are installed on all three skill surfaces. `chatgpt-web` is prompt-only and requires BrowserOS MCP plus an already logged-in ChatGPT browser session; it does not automate login.

External lanes still require the selected local `claude`, `codex`, `agent`, or
`grok` CLI at invocation time. Ordinary same-host work uses the active host's
native child system instead. External provider routing remains exact: Codex
runs OpenAI model ids and Fugu profiles, Claude Code runs supported Claude
models, Cursor Agent runs `composer-2.5-fast`, and Grok runs its own models;
model ids never cross runtimes.

`agent-delegate` owns external editful sessions and receipts. `fresh-consult`
and `model-consensus` select native or external transport per role while
preserving exact continuation. `plan-implement` is the parent-implemented
native lane; `plan-conductor`, `stepwise`, and `arch-epic` are transport-neutral
orchestrators with deliberate external modes. The cynical and exhaustive
reviews use clean native read-only slices and remain prompt-only.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface, including the shared agent
orchestration policy under Agents/Codex, Claude, and Gemini; confirms old
arch_skill-owned Codex and Claude hook entries and old
`~/.codex/skills/<skill>` mirrors are absent; and confirms removed packages are
absent for the supported runtimes.

Restart your Codex, Claude Code, or Gemini CLI session after install so it
reloads skills and drops any hook list cached before install removed old
arch_skill hook entries.

## Shipped skills

### `arch-step`

Use `arch-step` for broad or ambiguity-heavy full-arch work. It owns the standalone full-arch workflow, including:

- `new`
- `reformat`
- `research`
- `deep-dive`
- `external-research`
- `phase-plan`
- `auto-plan`
- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `consistency-pass`
- `review-gate`
- `implement`
- `implement-loop`
- `auto-implement`
- `full-auto`
- `audit-implementation`
- `status`
- `advance`

`consistency-pass` is the optional end-to-end cold-read helper before
implementation. It uses two new clean same-host native read-only explorers with
disjoint scope/authority and architecture/proof lenses. They run concurrently
only when host slots and parent integration capacity support it, otherwise
sequentially; the parent alone integrates. `auto-plan` runs the pass after
`phase-plan`, and `Decision: proceed to implement? yes` remains legal only for
a decision-complete artifact with no unresolved plan-shaping decisions.

`auto-plan` is the automatic planning command. The user-facing command is still just `$arch-step auto-plan` in Codex or `/arch-step auto-plan` in Claude Code, with an optional `docs/MY_PLAN.md` argument. `DOC_PATH` is always the planning ledger. It resumes from the first incomplete stage through `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`, and each stage command must write a generated receipt through `skills/arch-step/scripts/arch_stage_gate.py`. Marker-only plan text is not enough to unlock the next stage. `auto-plan` emits the `implement-loop` handoff only when the receipt gate is ready and the artifact is decision-complete. In native `/goal`, it keeps moving across turns until that proof bar is met or a true blocker stops it. Outside goal mode, it runs one bounded stage and names the exact next command.

`full-auto` is a re-entrant mode, not a new controller. It reads the plan, worklog, and audit block, then routes to the next existing command: `new` or `reformat` when the doc is missing or non-canonical, `auto-plan` while planning is incomplete, `implement-loop` only after the stage receipt gate and `consistency-pass` prove the artifact is decision-complete and ready for implementation, or `$arch-docs` after a clean code audit. It never starts implementation before planning readiness and never bypasses North Star confirmation.

`arch-step` does not have authority to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, the skill must ask the user instead of guessing.

Before Section 7 is allowed to harden, `arch-step` should inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story, such as sibling formats, readers/writers, examples, fixtures, mirrored config, generated artifacts, or live docs. It should include those surfaces now, assign them to a named later phase, explicitly exclude them, or ask one exact blocker question instead of silently leaving them contradictory.

Compatibility posture is separate from `fallback_policy`. The plan should say whether it preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. `arch-step` should not assume backward compatibility by default just because it feels safer.

Section 7 phase plans should protect the full destination map while building depth-first. The first working slice should prove one real path through the canonical owner path and highest-risk seam; later phases should expand along named axes. Phase count follows proof gates, dependency edges, reversibility or migration boundaries, and user-review boundaries rather than a preset number. New phase plans should use an explicit `Checklist (must all be done)` plus `Exit criteria (all required)` so a phase cannot be called complete while planned obligations are still implicit.

`implement-loop` is the automatic implementation-frontier delivery command. `auto-implement` is an exact user-facing synonym. The user-facing command is `$arch-step implement-loop docs/MY_PLAN.md` or `$arch-step auto-implement docs/MY_PLAN.md` in Codex, and the same `/arch-step ...` command in Claude Code. It first requires `arch_stage_gate.py ready` to pass, then runs the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this arc, then runs `audit-implementation`. Named later expansion is not current missing work until its proof gate is due; silent removal from the destination map is still a scope cut. In native `/goal`, it keeps implementing and auditing until the audit is clean or a true blocker stops it. Outside goal mode, it runs one bounded implementation/audit cycle and names the next command.

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `arch-step-goal-prompt`

Use `arch-step-goal-prompt` when the user wants a durable Markdown goal prompt file for an ArcStep run rather than executing ArcStep immediately. It takes a rough ask plus an optional canonical `DOC_PATH`, writes a goal prompt for `$arch-step auto-plan`, `implement-loop`, `auto-implement`, or `full-auto`, points to source truth by path, and adds false-finish and reviewer gates without copying the plan into a second source of truth. It is prompt-only: no scripts, runners, controllers, or harnesses.

### `miniarch-step`

Use `miniarch-step` when the work still needs a canonical full-arch doc, phased execution, and native goal-mode auto flow, but does not need `arch-step`'s broader staged helper surface. It keeps the trimmed command surface without changing the full-work posture.

It keeps the same full-arch artifact shape and the same clean-audit handoff to `arch-docs`, but with a shorter command surface:

- `new`
- `reformat`
- `research`
- `deep-dive`
- `phase-plan`
- `auto-plan`
- `implement`
- `implement-loop`
- `auto-implement`
- `full-auto`
- `audit-implementation`
- `status`
- `advance`

`miniarch-step auto-plan` is the automatic planning command for the trimmed full-arch surface. `DOC_PATH` is the planning ledger. It resumes from the first incomplete stage through `research`, `deep-dive`, and `phase-plan`, then emits the `implement-loop` handoff when the plan is decision-complete. In native `/goal`, it keeps moving across turns until that proof bar is met or a true blocker stops it.

`miniarch-step full-auto` is also doctrine-only and re-entrant. It routes over the existing miniarch `auto-plan` and `implement-loop` commands, but it does not add or invoke `consistency-pass`; before implementation it must use the normal miniarch section-quality readiness bar to confirm the artifact, research, deep dive, and phase plan are strong enough to proceed without guessing.

`miniarch-step implement-loop` and `miniarch-step auto-implement` share the same
implementation-frontier delivery command. They use a new clean native auditor
for each independent gate when the host supports it. `gpt-5.4-mini` with
`xhigh` is a preference only when the native schema can select and confirm it;
otherwise the audit uses inherited native capability without claiming a model
it cannot prove. An external exact-model audit remains available when that
identity is genuinely load-bearing and worth the added process cost.

Use `miniarch-step` when the work needs full-arch execution but does not need `arch-step`'s broader helper surface.

### `arch-epic`

Use when one goal is too large for a single `arch-step` plan and should be decomposed into approved, ordered sub-plans. The epic doc owns the raw goal, decomposition, inter-plan gates, sub-plan DOC_PATHs, and append-only orchestration history; each sub-plan remains a real arch-step plan.

Interactive and automatic modes preserve the same role lifecycle. A same-host
planner or implementation worker starts as a new clean native child from the
epic/sub-plan artifacts; accepted repair resumes that exact role, while every
independent critic starts as a different new clean child. Same-session
`auto-plan` still requires the real ArcStep receipt gate for each exact
`DOC_PATH`, and `auto-implement` still requires ArcStep COMPLETE plus an epic
critic pass before advancing. The explicit external-harness mode remains
available when its provider, exact model/profile, lifecycle, process/worktree
isolation, automation, or structured receipts are the deliberate benefit;
`run_arch_epic.py` owns only that external invocation and receipt plumbing.

Use `arch-epic` for one epic expressed as ordered arch-step sub-plans. Use
`stepwise` when another repo's doctrine already defines the ordered process.

### `arch-docs`

Use when the job is leaving repo docs healthier: cleaning up stale, overlapping, misleading, or obviously dated docs, updating stale survivors, clarifying confusing docs, and promoting grounded missing truth into evergreen docs. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one grounded DGTFO docs-health pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, use git history when staleness or datedness matters, consolidate each topic to one canonical home, update stale surviving docs, clarify confusing docs, and add grounded missing docs when the canonical result is either a standard public-repo doc or a differentiated evergreen doc that deserves its own home. Repo posture is evidence-based: default to `private/internal` when unclear, but in `public OSS` repos treat `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` as expected standalone docs. Then delete stale, duplicate, or dated one-off truth and repair links or nav for the surviving docs.

`arch-docs auto` is the repeated docs-cleanup mode. In native `/goal`, it runs
a grounded pass, a new clean same-host native review, and repeats until the
docs cleanup is clean or a real blocker stops it. Outside goal mode, it runs
one bounded pass plus review and names the next command.

### `arch-mini-plan`

Use when the task still needs canonical arch blocks, but the planning should be done in one pass and follow-through should happen later via `miniarch-step` or `arch-step`, then `arch-docs` for later docs cleanup.

### `lilarch`

Use for contained features or improvements that should fit in 1-3 phases.

### `bugs-flow`

Use for Sentry/log-driven bug analysis, narrow fixes, and explicit-review-only follow-up.

### `audit-loop`

Use for repo-wide audit passes where the agent should exhaustively map the codebase and current proof surface before editing, then rank and attack the biggest real unresolved risks by consequence instead of picking something convenient. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

### `comment-loop`

Use for repo-wide code comment hardening passes where the agent should exhaustively map the repo, current proof surface, and current explanatory coverage before editing, then rank and attack the biggest shared explanation gaps around contracts, conventions, gotchas, and subtle behavior instead of writing narration wherever it feels helpful.

### `audit-loop-sim`

Use for repo-wide real-app automation passes where the agent should exhaustively map the app, journeys, and current automation surface before editing, then rank and attack the biggest unresolved automation risks by consequence instead of cashing out on tiny safe test tweaks. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

### `goal-loop`

Use when the goal is clear but the path is not, and you want a controller doc plus append-only iteration log.

### `north-star-investigation`

Use for quantified investigations where ranked hypotheses and brutal tests are the main job.

### `arch-flow`

Use when the question is "what's next?" on an arch-style doc and you want the single best read-only recommendation.

### `arch-skills-guide`

Use when the question is "which arch skill should I use?" or "what is the difference between these live subskills?"

### `agent-definition-auditor`

Use when the user wants a cold-read score, rationale, and prioritized improvements for an `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompt, or other agent-definition markdown.

### `agents-md-authoring`

Use when the user wants to write, edit, refactor, or audit a repo-root or path-local `AGENTS.md` so it stays command-first, scope-aware, and about current repo truth only.

### `prompt-authoring`

Use when the user wants to write, edit, refactor, or audit a prompt, reusable prompt contract, Markdown-backed Codex goal prompt file, or paste-sized `/goal` mission brief so it fits the user's intent, evidence needs, constraints, stop rules, and output shape without becoming brittle or overbuilt. The user does not need to name a prompt type or mode; the skill infers the shape from normal language. For goal prompts, it prefers Markdown files for substantial source-doc-backed work and paste-sized `/goal` text only when needed, always using source truth pointers, quality bar, evidence, stop rules, and first-class signoff rather than rigid field forms or duplicated plan docs.

### `chatgpt-web`

Use when the user explicitly wants the ChatGPT web provider, BrowserOS-backed
capabilities, or local attachments. The skill shapes rough prompts with
`prompt-authoring` discipline, verifies that BrowserOS is already logged in,
and uses one tab without silently inheriting its arbitrary conversation.
`new-clean` is the default; `continue-exact` is used only when the user asks to
continue an identifiable conversation. Independent asks remain serial but
start clean, while explicit follow-ups preserve the intended thread. It
defaults to Pro with Extended thinking when mode or effort is omitted and is
prose-only: no scripts, runners, harnesses, API calls, or automated login.

### `skill-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable agent skill package so it stays prompt-first, simple by default, generalized from user intent, anti-heuristic, and clear about peer boundaries, packaging, references, and validation.

### `figma-best-practices`

Use when the user wants to create, audit, or repair a Figma file, component library, variable/token system, prototype, Dev Mode surface, Code Connect mapping, Make kit, Sites page, Buzz template, Slides deck, or MCP-readable design artifact. The skill is prompt-only: it applies bundled Figma file-craft doctrine so the file is structurally honest, tokenized, componentized, semantically named, and ready for downstream human, developer, publishing, and AI consumers. Use implementation or Figma automation skills instead when the task is building code from a Figma design or operating the Figma UI itself.

### `fal-ai-tools`

Use when the user wants to use fal.ai tools, models, MCP, SDK/API calls, background removal, media generation or editing, model discovery, schema lookup, pricing checks, file upload, inference, polling, or result receipts. The skill is prompt-first: it prefers visible fal MCP tools, falls back to `fal_client` or raw HTTP when MCP is unavailable, checks live schemas and pricing before paid calls, and keeps fal keys redacted. Use provider-specific implementation or frontend skills instead when the task does not call fal.

### `flutter-reference`

Use when the user wants Flutter-specific guidance for building, reviewing, repairing, or diagnosing mobile apps or games. The skill is doctrine-only: it collects grouped Flutter references for architecture, Dart style, state management, lifecycle, performance, rendering, memory, testing, CI, accessibility, localization, security, platform integration, assets, input, and Flame/game-loop guidance. Use current official docs first when the request depends on latest Flutter, Dart, Android, iOS, or package behavior.

### `eli10`

Use when the user wants any answer, explanation, plan, review, recommendation, rewrite, or status update in ELI10/ELI16 maximum-readability style. The skill teaches the agent to spend the reader's working memory on the idea, not on parsing: lead with the point, explain at the right layer, unstack dense phrases, define load-bearing jargon, preserve exact commands/metrics/file names, avoid fake memory and baby talk, and skip next steps unless asked. It uses native tables only when they improve understanding, and avoids tables when long prose, paths, commands, or root-cause explanations would be clearer as bullets or sections. It uses the decision-brief contract only when the answer is asking the user to choose. Use `prompt-authoring` for prompts and reusable prompt contracts and `skill-authoring` for skill packages.

### `pr-authoring`

Use when the user wants a high-quality GitHub pull request written and published from real repo changes. The skill inspects repo truth, uses its vendored PR scaffold as a quality reference, creates or updates the GitHub PR, and returns the PR link instead of only printing suggested text.

### `pr-review-followthrough`

Use when the user explicitly wants an already-open GitHub pull request followed through until merge-ready. The skill polls live PR state, handles actionable review comments and checks, replies on the exact thread or comment surface, pushes accepted fixes to the same branch, and stops before merging.

### `commit-history-authoring`

Use when the user wants the current branch's commit messages rewritten into an informative history from the point where the branch diverged from its nearest parent branch. The skill inspects the inferred branch-span range, diffs, old messages, trailers, and any evidenced active arch plan; it then applies a message-only rewrite with a backup branch while preserving commit boundaries, patch content, author metadata, and final tree state. It allows commits already reachable from the current branch's own remote-tracking ref, but refuses dirty worktrees, unrelated shared remote refs, current-branch remotes ahead of local `HEAD`, protected branches by default, and merge commits. It never pushes or force-pushes.

### `skill-flow`

Use when the user wants to design, repair, or audit an ordered flow of multiple
agent skills so each skill has a distinct job, concrete handoff artifact, clear
peer boundary, and lean prompt contract. For a large or scope-phrase audit, the
DAG-grounded sub-mode resolves the full suite, assigns every slug to a clean
read-only native walker with no nested fanout, and keeps concurrency
proportionate to host slots and parent integration capacity. Its semantic
extractor counts live backticked `$skill-name` peer references while excluding
shell/code variables, then writes the Mermaid graph, labeled edge table, and
unresolved-reference list at `<doc-dir>/<doc-slug>_DAG.md`. Findings remain
read-only and evidence-backed. Optional d2/SVG rendering stays a narrow helper.

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

### `codex-cleanup`

Use when `~/.codex` is multi-GB, old session JSONL/log/cache files are bloated, or many parallel Codex instances are stalling on SQLite `database is locked`. The skill ships a local bash helper that defaults to dry-run, refuses to run `--apply` while any `codex` process is alive, prunes stale dated/cache/temp files, checkpoints SQLite WALs, and rotates `log/codex-tui.log` without touching live config, credentials, memories, plugins, skills, prompts, or history indexes.

### `codex-babysit`

Use when the user wants to keep an already-running Codex goal-mode tmux pane alive across real usage limits or process death. It watches the pane, rotates `aim` accounts only when Codex is actually blocked, restarts, resumes the same session, and verifies work resumed.

### `fresh-consult`

Use when the user or another skill wants a clean, independent read-only second
opinion on a concrete artifact, completion claim, flow-consistency question, or
readability check. Ordinary same-host work uses a new clean native child
(`fork_turns: "none"` in Codex or a clean named/custom subagent in Claude).
Cross-provider, unavailable exact-model/profile, lifecycle, isolation,
automation, or structured-receipt needs use the external CLI lane. Reviewers
do not edit or create children; the parent checks workspace state and
integrates the verdict.

For an external consult, the user supplies runtime and effort plus a
model/profile for non-Codex lanes, or the skill asks once. Codex aliases remain
exact (`sol`, `luna`, `terra`), and an omitted external Codex model defaults to
`gpt-5.6-sol`. Exact model versions and profiles are preserved without silent
downgrade or provider switch.

The first request in a consult line starts clean and preserves the exact native
child handle or external session id. The second and third same-line requests
resume that exact reviewer by default. The fourth starts a new clean reviewer
unless the user explicitly asks to continue. A new independent gate, changed
runtime/model/effort, or changed work root also starts clean; the skill never
resumes a merely "latest" session.

External chains keep `chain.json` plus per-turn prompt, final, event, stderr,
execution, session-id, and resume receipts under `/tmp/fresh-consult/...`.
Native runs preserve the host child handle and return contract. Long reviews
are monitored patiently without tight polling.

Use `fresh-consult` for clean read-only opinions and exact-reviewer follow-ups.
Use `agent-delegate` only when an editful **external** worker/session is the
deliberate lane; dispatch ordinary same-host editful work natively. Use
`codex-review-yolo` for the exact external `-p yolo` profile/receipt pattern,
and `stepwise` or `arch-epic` for ordered role lifecycles.

### `agent-delegate`

Use when an editful external worker/session provides a concrete benefit: a
different provider, a load-bearing exact model/profile, durable exact-session
continuation, process isolation, automation, or structured receipts. These are
recognition examples, not an allowlist or approval gate. Ordinary same-host
implementation, investigation, and repair use the host's native children
directly. The adapter preserves exact model resolution, hook-suppressed CLI
invocation, namespaced receipts, shared-worktree reporting, and exact-handle
resume.

Fresh-resumable is the default. When the caller explicitly requests parallel workers, `agent-delegate` creates a group directory and launches ordinary fresh-resumable child workers, then inspects repo state before reporting the combined result. Stateless one-shot is available only when explicitly requested. Explicit resume uses a same-runtime session id or prior run directory. Claude resume uses `-r <session_id>` from the original work root; Codex resume uses `codex exec resume <thread_id>` and never `--last`; Cursor Agent and Grok resume use `--resume <session_id>` and never latest-session selection. The skill does not resume "latest" sessions, cross runtimes, or use external continuation controllers as a strategy.

The user supplies runtime and effort plus a model/profile for non-Codex lanes, or the skill asks once before invoking. A Codex lane accepts `sol`, `luna`, and `terra` as the exact `gpt-5.6-sol`, `gpt-5.6-luna`, and `gpt-5.6-terra` choices; an omitted Codex model defaults to `gpt-5.6-sol`. Runtime can be inferred from unambiguous model families such as `Luna`, `Terra`, `GPT56SOLXI`, `fugu`, or `fugu-ultra` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions and profile names are preserved; there is no silent downgrade, provider switch, effort substitution, detached fallback, separate-worktree fallback, or ambiguous resume fallback.

Delegated children commonly take 5+ minutes; broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Use `agent-delegate` for deliberate external editful delegation,
fresh-resumable by default and resumed only by exact handle. Keep parallel
external fanout proportionate to independent scope, current host state, and
the parent's integration capacity. Use `fresh-consult` for read-only opinions,
`plan-implement` for ordinary native plan-backed work, `model-consensus` for
two-participant convergence, and `stepwise` or `arch-epic` for ordered role
lifecycles.

### `plan-audit`

Use when the user wants an existing planning artifact audited before work starts, in whatever format it already uses: PRD, migration plan, architecture plan, checklist, issue body, inline plan, or design doc. It improves plan quality by checking the North Star, done-state requirements, real ambiguity, constraints and non-constraints, repo/code truth when relevant, depth-first implementation risk, tiny-team simplicity, existing-pattern fit, drift-proofing, side doors, required deletes, and proof gaps.

Use `plan-audit implementation-audit` when the user wants code already written for a plan reviewed against that plan. This mode reviews code shape, owner path, SSOT, side-door closure, duplicate truth, stale docs/prompts, proof gaps, drift, caller fit, changed tests as code, and elegance. It is not generic diff review, does not run tests or CI, does not ask for logs, and does not investigate whether a completion claim is truthful.

The skill is prompt-first and doctrine-only. It may maintain `<PLAN_STEM>_PLAN_AUDIT.md` beside file-backed plans for repeat audits, but it does not write the plan, implement it, choose workflows, or add deterministic scripts, runners, controllers, scorers, or harnesses.

### `plan-implement`

Use when the user wants to implement an existing plan, phase, section, checklist, issue-body plan, or design doc while keeping implementation state easy to resume. The skill works depth-first from narrow proven slices, keeps `<PLAN_STEM>_IMPLEMENTATION_LOG.md` beside non-trivial file-backed plans, reuses proof until a real invalidator makes it stale, runs checks for impact rather than habit, and uses plan-audit implementation lenses for warm review while code is still easy to repair.

The plan remains source of truth, the plan-audit log owns `PLA-*` and `IMP-*`
findings, and the implementation log is speed/resume state. Independent native
children start clean, accepted repairs return to the exact implementer, and
independent rechecks use new clean critics. The parent owns scope, integration,
and proof. An explicitly requested external worker or conductor remains a
deliberate route under the shared policy.

Use `plan-implement` when the parent implements with optional native children.
Use `plan-conductor` when the parent should remain a non-implementing architect
and reviewer while transport-selected workers drive the plan.

### `plan-conductor`

Use when the user wants an entire existing plan document, or an explicit phase
range, implemented by phase workers while the parent remains the
non-implementing architect and deeply cynical reviewer. The parent extracts an
execution map into `<PLAN_STEM>_CONDUCTOR_LOG.md` and stops before dispatch if
the plan has no observable done-state or defensible frozen scope.

Each phase-sized slice starts as a new clean same-host native child by default.
The parent uses `$agent-delegate` only when a concrete external provider,
exact-model/profile, lifecycle, worktree/process isolation, automation, or
receipt benefit is worth the added cost. Accepted findings return to the exact
worker through its original transport; independent reviewers and the cold
verifier start clean. The parent audits every claim against code, delegates
proof, records checkpoints, and closes only on plan-required proof plus the
final whole-plan gate.

The parent never edits source code during the conductor stage or accepts worker
self-reports as truth. Runtime/model/effort are requested only for a selected
external lane; native roles use only capabilities the active host can confirm.

`$plan-conductor terra` remains the explicit external delivery shortcut. Its
dedicated worktree, Codex `gpt-5.6-terra` at `xhigh`, three new clean external
reviews, repair/re-review loop, PR publication, and PR follow-through are the
point of that lane. Merely naming Terra in an ordinary conductor request does
not activate it.

Use `plan-conductor` for whole-plan worker execution with parent review. Use
`plan-implement` when the parent should implement the plan itself. Use
`agent-delegate` for one concrete **external** delegated task, and `plan-audit`
to audit a plan rather than implement it.

### `model-consensus`

Use when the user wants two selected model participants to cross-check,
critique, and converge on a plan, architecture, investigation, design, or
concept. The parent resolves transport separately: same-host roles use
separate new clean native children when the host can honor the requested
capability; cross-provider or unavailable exact-model/profile roles use
external resumable sessions. Every round resumes each exact participant, and
parent relay remains the default topology. No deterministic runner,
controller, or harness is added.

For investigations, root-cause work, and "read everything" cross-checks, the parent preserves discovery freedom. It records the raw user goal, exact user-named artifacts, desired output, and hard constraints. The child models choose and cite the code, docs, research, tests, commands, and local evidence they need.

For architecture or implementation-plan work, the skill keeps the existing single-path pressure: both models inspect canonical owners, adjacent patterns, duplicate pathways, and proof surfaces before agreeing on where the work should live.

The user names the two participant identities. Native roles use only model
capabilities the active host can confirm; an unavailable load-bearing exact
identity selects the external lane. External shorthand follows the shared
model resolver, preserves exact versions/profiles, and defaults an omitted
external Codex model to `gpt-5.6-sol`.

External participants preserve event/final receipts; native participants
preserve exact host child handles. Both remain read-only, and the parent checks
workspace state before synthesis.

Use `model-consensus` for collaborative or adversarial convergence and
`fresh-consult` for one read-only opinion. Use `agent-delegate` only for an
explicitly external editful worker/session; ordinary same-host work uses native
children directly. Use `stepwise` or `arch-epic` for ordered implementation.

### `contact-sheet-builder`

Use when the user wants a quick local contact sheet from existing image files, folders, globs, or attached local image paths. The skill uses one Pillow renderer script and defaults to dense labeled PNG sheets, dynamic near-native edge-to-edge canvas sizing, `0px` outside margin, `2px` gutters, Preview opening on macOS, overwrite protection, and concise receipts. Use `--margin` and `--gutter` only when spacing needs to change. Use `--no-open` for headless or batch runs. Use `--page-width` and `--page-height` only when a fixed page-style overview is wanted. Invoke the script directly with the `python3` that has Pillow installed. It is not for generating or editing images, video frame extraction, Figma boards, slide/doc layouts, provider APIs, or theme-specific generation flows.

### `fc-branded-pdf`

Use when the user wants Markdown, a memo, a report, exported document content, pasted notes, or a small packet turned into a local FC / Poker Skill branded PDF. The skill keeps a Markdown source file, renders it with the bundled `scripts/render_markdown_to_pdf.sh` helper, and verifies page count, extracted text, and visual preview when layout matters. It is local-file only: it does not upload to Drive, archive to Drive, or manage Drive folders. It requires `pandoc` plus Chrome or Chromium on the host.

### `cynical-code-review`

Use when the user wants a prompt-only skeptical implementation-integrity code review over implemented code, a branch, diff, path set, completion claim, or optional plan-backed implementation and wants the review saved to disk. The skill assumes the completion story may be misleading, treats names/docs/status/tests as claims rather than proof, hunts name-only completion, split-brain owners, side doors, partial unification, stale authority paths, stopped-short user workflows, overbuilt machinery, scope contamination, fake proof receipts, and docs/status/tests that mask broken code, then writes `target.md`, `suspicion-map.md`, `coverage.md`, `findings.md`, and `verdict.md` under `/tmp/cynical-code-review/...`. Its verdicts are `approve`, `not-approved`, or `coverage-incomplete`.

It is review-only and workflow-neutral. It does not fix code, run a runner, dictate the user's next workflow, invoke external review/delegation skills, manually spawn `codex`, `claude`, `agent`, or `grok` subprocesses, or turn review into a test/doc nit pass.

Use `cynical-code-review` when distrust of the implementation story is the job. Use `exhaustive-code-review` when coverage is the deliverable, `plan-audit implementation-audit` when plan fit is the main question, `codex-review-yolo` for an explicit Codex `-p yolo` fresh-eyes review, and `thermo-nuclear-code-quality-review` for maintainability-only review.

### `cynical-architecture-review`

Use when the user wants a prompt-only skeptical architecture review over a branch, diff, subsystem, plan-backed implementation, or code area and wants the review saved to disk. The skill assumes the architecture may have emerged accidentally through iteration, preserves the intended UX and hard experiment requirements, hunts sprawl, invalid split ownership, duplicate truth, accidental abstractions, compatibility shims, flags-as-architecture, registries, adapters, state spread, wrong decomposition, and needless complexity, then writes `target.md`, `architecture-map.md`, `complexity-ledger.md`, `subtraction-map.md`, `coverage.md`, `findings.md`, and `verdict.md` under `/tmp/cynical-architecture-review/...`. Its verdicts are `approve`, `not-approved`, or `scope-incomplete`.

It is review-only and workflow-neutral. It does not fix code, run a runner, dictate the user's next workflow, invoke external review/delegation skills, manually spawn `codex`, `claude`, `agent`, or `grok` subprocesses, redesign the product, or turn review into a QA/test/doc pass unless the user explicitly asks.

Use `cynical-architecture-review` when accidental architecture and subtraction are the job. Use `cynical-code-review` when distrust of the implementation story is the job, `exhaustive-code-review` when coverage is the deliverable, `plan-audit implementation-audit` when plan fit is the main question, and `thermo-nuclear-code-quality-review` for maintainability-only review.

### `cynical-cruft-removal`

Use when the user wants a prompt-only skeptical cleanup review over a repo, branch, diff, subsystem, test suite, dependency set, generated artifact set, or docs/examples/prompt surface and wants a deep deletion report saved to disk. The skill assumes references are not proof of value, identifies live roots and current purpose, hunts dead code, self-referential islands, retired V1/V2 paths, stale feature flags, worthless tests, fake coverage, unused dependencies, obsolete configs/scripts, stale generated artifacts, point-in-time docs/examples, and other low-value artifacts, then writes `target.md`, `live-root-map.md`, `purpose-map.md`, `reference-graph-notes.md`, `low-value-catalog.md`, `test-bloat-report.md`, `deletion-candidates.md`, `keep-decisions.md`, `coverage.md`, `findings.md`, and `verdict.md` under `/tmp/cynical-cruft-removal/...`. Its verdicts are `cruft-found`, `no-material-cruft-found`, `scope-incomplete`, or `unsafe-to-judge`.

It is review-only and workflow-neutral. It does not fix code, delete files, run a runner, dictate the user's next workflow, invoke external review/delegation skills, manually spawn `codex`, `claude`, `agent`, or `grok` subprocesses, or turn review into a QA/test/doc pass.

Use `cynical-cruft-removal` when deletion value and low-value artifact discovery are the job. Use `cynical-code-review` when distrust of the implementation story is the job, `cynical-architecture-review` when accidental architecture and subtraction are the job, `arch-docs` for docs-only cleanup, `exhaustive-code-review` when coverage is the deliverable, and `thermo-nuclear-code-quality-review` for maintainability-only review.

### `exhaustive-code-review`

Use when the user wants a prompt-only exhaustive code review over a branch,
diff, path set, plan scope, or completion claim and wants the review saved to
disk. The skill divides real coverage needs into non-overlapping new clean
native read-only slices, bounds fanout by host slots, collision risk, and parent
integration capacity, and accounts for every return before writing `target.md`,
`coverage.md`, `findings.md`, and `verdict.md` under
`/tmp/exhaustive-code-review/...`. Its verdicts are `approve`, `not-approved`,
or `coverage-incomplete`.

It is review-only and workflow-neutral. It does not fix code, run a runner, dictate the user's next workflow, invoke external review/delegation skills, or manually spawn `codex`, `claude`, `agent`, or `grok` subprocesses.

Use `exhaustive-code-review` when coverage is the deliverable. Use `cynical-code-review` when distrust of the implementation story is the main question, `plan-audit implementation-audit` for plan-backed code review, `codex-review-yolo` for an explicit Codex `-p yolo` fresh-eyes review, and `thermo-nuclear-code-quality-review` for maintainability-only review.

### `thermo-nuclear-code-quality-review`

Use when the user explicitly asks for a thermo-nuclear / thermonuclear review, a code-judo review, an especially harsh maintainability review, or a strict audit of structural quality, file sprawl, spaghetti branching, abstraction boundaries, and codebase health. This is a vendored Cursor Team Kit skill installed from `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/`.

It is a rubric-only review skill. It has no local runner, no Stop-hook controller, and no subprocess requirement. The installer copies the skill package only; it does not install Cursor Team Kit's Cursor-specific agents or rules.

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

## Usage

- Primary surface: ask the agent to use `arch-step`, `arch-step-goal-prompt`, `miniarch-step`, `arch-epic`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `chatgpt-web`, `skill-authoring`, `figma-best-practices`, `fal-ai-tools`, `flutter-reference`, `eli10`, `pr-authoring`, `pr-review-followthrough`, `commit-history-authoring`, `skill-flow`, `amir-publish`, `codex-cleanup`, `codex-babysit`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `contact-sheet-builder`, `fc-branded-pdf`, `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, `exhaustive-code-review`, `thermo-nuclear-code-quality-review`, `stepwise`, or `codex-review-yolo`.
- Full-arch execution defaults to `miniarch-step` when the trimmed command surface is enough and `arch-step` when the broader or helper-heavy surface is needed.
- Docs cleanup loops default to `arch-docs`.
- Read-only checklist and next-step inspection uses `arch-flow`.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step new "build this"`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step advance docs/MY_PLAN.md RUN=1`
- `Use $arch-step auto-plan`
- `Use $arch-step consistency-pass docs/MY_PLAN.md`
- `Use $arch-step implement-loop docs/MY_PLAN.md`
- `Use $arch-step auto-implement docs/MY_PLAN.md`
- `Use $arch-step full-auto docs/MY_PLAN.md`
- `Use $arch-step-goal-prompt to write a Markdown goal prompt for $arch-step auto-plan docs/MY_PLAN.md`
- `Use $arch-step-goal-prompt to strengthen this auto-implement goal with strict reviewers`
- `Use $miniarch-step for this feature`
- `Use $miniarch-step auto-plan`
- `Use $miniarch-step implement-loop docs/MY_PLAN.md`
- `Use $miniarch-step auto-implement docs/MY_PLAN.md`
- `Use $miniarch-step full-auto docs/MY_PLAN.md`
- `Use $arch-epic to break this migration into sub-plans and run them in order`
- `Use $arch-epic auto-plan docs/EPIC_AUTH_MIGRATION_2026-06-07.md`
- `Use $arch-epic auto-implement docs/EPIC_AUTH_MIGRATION_2026-06-07.md`
- `Use $arch-epic to automatically implement this approved epic end to end`
- `Use $arch-docs`
- `Use $arch-docs auto`
- `Use $arch-mini-plan docs/MY_PLAN.md`
- `Use $lilarch for this small feature`
- `Use $bugs-flow on this Sentry issue`
- `Use $audit-loop`
- `Use $audit-loop review`
- `Use $audit-loop auto`
- `Use $comment-loop`
- `Use $comment-loop review`
- `Use $comment-loop auto`
- `Use $audit-loop-sim`
- `Use $audit-loop-sim review`
- `Use $audit-loop-sim auto`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
- `Use $agent-definition-auditor to audit this AGENTS.md`
- `Use $agents-md-authoring to tighten this AGENTS.md`
- `Use $prompt-authoring to refactor this prompt`
- `Use $chatgpt-web to ask ChatGPT for a Pro Extended second opinion on this plan`
- `Use $skill-authoring to audit this skill package`
- `Use $figma-best-practices to audit this Figma library for Dev Mode and MCP readiness`
- `Use $fal-ai-tools to remove the background from this image with fal.ai`
- `Use $flutter-reference to review this Flutter app architecture`
- `Use $eli10 to explain why this test failed`
- `Use $eli10 to format this decision question`
- `Use $pr-authoring to write and publish a PR for this branch`
- `Use $pr-review-followthrough on PR #1234`
- `Use $commit-history-authoring to rewrite this branch's WIP commits into informative branch history`
- `Use $skill-flow to design the authoring and audit flow for this skill suite`
- `Use $amir-publish`
- `Use $cynical-code-review to audit this implemented plan and assume we missed the point`
- `Use $cynical-architecture-review to find accidental architecture and simplify it without changing the UX`
- `Use $cynical-cruft-removal to find low-value code, tests, docs, configs, and generated artifacts that should go away`
- `Use $exhaustive-code-review on this full branch`
- `Use $thermo-nuclear-code-quality-review on this diff`
