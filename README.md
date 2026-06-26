# arch_skill

This repo ships installable agent skills centered on the arch suite for Codex CLI, Claude Code, and Gemini CLI.

## Community

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Support: [SUPPORT.md](SUPPORT.md)

The live arch suite is:

- `arch-step` — the broad full-arch execution surface; owns the full staged workflow, extended helper passes, receipt-gated `auto-plan`, implementation-frontier `implement-loop`, re-entrant `full-auto`, compact `status`, and guided `advance`
- `arch-step-goal-prompt` — writes Markdown-backed goal prompt files for ArcStep `auto-plan`, `implement-loop`, `auto-implement`, and `full-auto` runs without copying the controlling plan into a second source of truth
- `miniarch-step` — the trimmed full-arch surface; keeps canonical arch docs, phasing, doctrine-only `full-auto`, and native goal-mode auto flow without the broader `arch-step` helper surface
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and native goal-mode `auto` docs cleanup
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `miniarch-step` or `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `audit-loop` — exhaustive map-first repo audit loop with a root audit ledger, mandatory post-change self-audit, and native goal-mode `auto` continuation
- `comment-loop` — exhaustive map-first repo comment hardening loop with a root comment ledger and native goal-mode `auto` continuation
- `audit-loop-sim` — exhaustive map-first real-app automation audit loop with a root simulator ledger, mandatory post-change self-audit, and native goal-mode `auto` continuation
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill
- `arch-epic` — multi-plan orchestrator that wraps `arch-step` for goals too big for a single canonical plan. Captures the goal, drafts a plain-English one-sentence-per-sub-plan decomposition with inter-plan gates, gets user approval, then runs sub-plans depth-first. Interactive mode drives each sub-plan through arch-step's `new` → `auto-plan` → `implement-loop` → `audit-implementation` arc and uses a fresh Claude, Codex, or Grok critic after completion. Same-session `auto-plan` is a strict sequential driver: it runs the real `$arch-step auto-plan <DOC_PATH>` flow for each approved sub-plan, requires the generated receipt gate to pass for that exact DOC_PATH, and only then marks that sub-plan `planned` before moving on. Same-session `auto-implement` is the matching strict implementation driver: it runs one planned sub-plan at a time through real `$arch-step auto-implement <DOC_PATH>` until ArcStep audit is COMPLETE, then runs the epic critic and advances only after critic `pass`. The separate spawned-harness automatic mode asks for role-based execution choices for planner, implementation worker, and critic, resolves shorthand to exact runnable model IDs, pins the policy, then uses streamed child harnesses with detached long-run monitoring and a 180s default child-wait cadence.

Use `miniarch-step` when the work still needs a real full-arch artifact and auto continuation, but you want the trimmed command surface instead of the broader `arch-step` helper surface. Use `arch-step` when the work is broader, more ambiguous, or needs the full helper surface.

Other shipped skills are:
- `agent-definition-auditor` — cold-reader scoring and findings for `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompts, and other agent-definition markdown
- `agents-md-authoring` — writes, edits, refactors, and audits concise repo-present `AGENTS.md` files
- `prompt-authoring` — writes, edits, refactors, and audits prompts, reusable prompt contracts, Markdown-backed Codex goal prompt files, and paste-sized `/goal` mission briefs
- `chatgpt-web` — prompt-only helper for shaping a prompt with prompt-authoring discipline, then querying logged-in ChatGPT through BrowserOS MCP with optional attachments; defaults to Pro with Extended thinking unless the user specifies another mode or effort
- `skill-authoring` — writes, edits, refactors, and audits prompt-first reusable agent skill packages
- `figma-best-practices` — prompt-only Figma file-craft doctrine for creating, auditing, or repairing structurally honest Figma files, libraries, variables, components, Dev Mode prep, Code Connect mapping, and Make/Sites/Buzz/Slides/MCP readiness
- `fal-ai-tools` — prompt-first fal.ai tool workflow for model discovery, schema and pricing lookup, file upload, background removal, media generation or editing, inference, polling, and result receipts using MCP when available and SDK/HTTP fallback otherwise
- `flutter-reference` — doctrine-only Flutter app and game-building reference for architecture, Dart style, state management, lifecycle, performance, testing, CI, accessibility, localization, security, platform integration, and Flame/game-loop guidance
- `eli10` — answers in maximum-readability ELI10 style: reduces reader working-memory load, leads with the point, preserves exact technical truth, defines load-bearing jargon, explains mechanisms plainly, avoids fake memory and baby talk, and uses scan markers or tables only when they clarify
- `pr-authoring` — writes and publishes high-quality GitHub pull requests from real repo changes
- `pr-review-followthrough` — explicit-invocation follow-through loop for an already-open GitHub PR: polls review feedback and checks, replies on-thread with accept/decline rationale, pushes fixes to the same branch, and stops at merge-ready
- `commit-history-authoring` — rewrites the current branch's branch-span commit messages from its nearest parent branch into informative history while preserving commit boundaries, patches, trailers, and backup recovery; it never pushes rewritten history
- `skill-flow` — designs, repairs, and audits ordered multi-skill flows with distinct skill jobs, concrete handoffs, clear peer boundaries, and no prompt-runner scaffolding; for 30+ skill suites, the DAG-grounded audit sub-mode parallel-walks the suite, builds a labeled-edge substrate, and surfaces wasted-energy patterns (over-promotion, redundancy, dead skills, broken refs)
- `amir-publish` — personal shortcut for publishing this skills repo across Amir's usual machines
- `codex-cleanup` — dry-run-first local cleanup skill for stale `~/.codex` state that relieves multi-instance SQLite/WAL and log bloat without touching live config or credentials
- `codex-babysit` — watches an already-running Codex goal-mode tmux pane, rotates `aim` accounts only on real usage limits, restarts and resumes the same session, and keeps checking until Codex's own goal finishes
- `codex-review-yolo` — external Codex `-p yolo` reviewer for substantial diffs, plans, docs, and completion checks, with live `--json` stream logs and strict `approve | not-approved | inconclusive` verdicts
- `fresh-consult` — prompt-only Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok read-only second opinions with strict pass/fail verdicts for cold reads, bounded same-session follow-up consults, parallel consults, flow consistency audits, completion checks, and readability/confusion checks; first turns start clean, second/third same-line follow-ups resume the captured child session by default, and turn four rotates fresh
- `agent-delegate` — prompt-only Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok workers for delegated implementation, editing, investigation-and-fix, command execution, or installed-skill use in the shared worktree; fresh-resumable is the default, explicit parallel workers are supported when requested, stateless one-shot is available when explicitly requested, explicit same-session resume is available for one worker by exact handle, and the skill reports changed files, verification, blockers, session id when present, and run directories
- `plan-audit` — prompt-first generic audit for existing planning artifacts in any format, plus plan-backed implementation-audit code review after code exists; checks plan quality before work starts and reviews implemented code against the plan for owner path, SSOT, side-door closure, duplicate truth, stale docs/prompts, proof gaps, drift, caller fit, and elegance without running tests, asking for logs, or dictating workflow
- `plan-implement` — prompt-first plan-backed implementation loop that keeps the plan, plan-audit log, implementation log, proof freshness, and warm code review aligned while coding so work survives compaction and avoids duplicate rereads, duplicate checks, late review, and external worker-swarm ceremony
- `plan-swarm` — prompt-first implementation swarm orchestrator that extracts one phase contract from an existing plan, decomposes it into independently delegable slices, launches or resumes parallel Codex GPT/GBT/Fugu, Claude Fable/Opus, Cursor Composer, or Grok workers through `agent-delegate`, batches review/test findings into delegated repair and impact-aware verification waves, commits local progress checkpoints freely, writes worklogs next to the plan, and closes only after arbiter and thermonuclear findings are triaged
- `agent-history` — searches local Codex or Claude Code session history for prior prompts, goals, commands, corrections, tool use, and timelines from natural-language asks, using bundled read-only JSONL/SQLite helpers and concise evidence summaries
- `model-consensus` — prompt-only parent-agent orchestration for two selected Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok model sessions to cross-check, critique, and converge on a plan, architecture, investigation, design, or concept until they agree or expose the smallest unresolved decision; preserves child discovery freedom for investigations and requires repo-backed participants to read real evidence before agreeing
- `contact-sheet-builder` — builds quick local contact sheet PNGs from existing images, folders, globs, or attached local image paths using a lean prompt contract plus one Pillow renderer; defaults to dense labeled sheets, dynamic near-native edge-to-edge canvas sizing, safe temp output, Preview opening on macOS, and concise receipts
- `cynical-code-review` — prompt-only skeptical implementation-integrity code review for implemented code, diffs, paths, plan-backed completion claims, and suspicious "done" stories; assumes names/docs/status/tests may be misleading, hunts name-only completion, split-brain owners, side doors, partial unification, stale authority paths, stopped-short user workflows, overbuilt machinery, scope contamination, and fake proof receipts, and saves the review artifact under `/tmp/cynical-code-review/`
- `cynical-architecture-review` — prompt-only subtraction-first architecture review for branches, diffs, subsystems, plan-backed implementations, and code areas that may have grown accidentally through iteration; preserves the intended UX and hard experiment requirements while hunting sprawl, invalid split ownership, duplicate truth, accidental abstractions, compatibility shims, flags-as-architecture, registries, adapters, state spread, wrong decomposition, future-copy traps, and needless complexity, and saves the review artifact under `/tmp/cynical-architecture-review/`
- `cynical-cruft-removal` — prompt-only skeptical cleanup review for repos, branches, diffs, subsystems, test suites, dependencies, generated artifacts, and docs/examples/prompt surfaces; assumes references are not proof of value, hunts dead code, self-referential islands, retired V1/V2 paths, stale flags, worthless tests, fake coverage, unused dependencies, obsolete configs/scripts, stale generated artifacts, and point-in-time docs/examples, and saves a deep deletion report under `/tmp/cynical-cruft-removal/`
- `exhaustive-code-review` — prompt-only exhaustive code review for branches, diffs, paths, plan scopes, and completion claims; maximizes native parallel agents, treats duplicate paths, side doors, stale truth, and competing owners as default coverage, and saves the review artifact under `/tmp/exhaustive-code-review/`
- `thermo-nuclear-code-quality-review` — vendored Cursor Team Kit rubric for unusually strict maintainability reviews focused on code-judo simplification, 1k-line file growth, spaghetti branching, abstraction boundaries, and structural quality
- `stepwise` — diagnostic orchestrator for ordered multi-step processes defined in another repo's doctrine; spawns a fresh Claude, Codex, or Grok worker session per step, runs an independent observational critic, and on failure diagnoses with the involved sessions before authoring a source-grounded repair at root cause. Model and effort for worker and critic are supplied by the user at invocation; child runtimes run dangerous / skip-permissions / no-sandbox. Distinct from `arch-step` (plan-doc-backed full-arch), `goal-loop` (bet-and-learn optimization), and one-shot review work.

Examples in this repo use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, removes old arch_skill-owned Codex and Claude hook entries from previous installs, removes older `~/.codex/skills/<skill>` mirrors, and also installs the Claude Code and Gemini CLI skill directories. When a Hermes Agent home exists on the machine, the same surface is mirrored into every existing Hermes skill root (`~/.hermes/skills/` and each `~/.hermes/profiles/<name>/skills/`) under the `arch_skill/` category directory; machines without Hermes are skipped automatically. Source/build internals (`build/`, `prompts/`, `__pycache__/`, `*.pyc`, and hook cleanup helpers) are pruned from installed skill packages. The `thermo-nuclear-code-quality-review` package is sourced unchanged from the vendored Cursor Team Kit plugin at `vendor/cursor/plugins/cursor-team-kit/skills/`; the installer copies only that skill package, not Cursor Team Kit agents or rules.

Automatic skill modes now rely on the host's native goal-mode continuation. Use Codex `/goal` or Claude Code `/goal` when you want a skill to keep moving across turns until its proof bar is met. This package no longer installs `Stop` or `SessionStart` hooks.

To skip Gemini:

```bash
make install NO_GEMINI=1
```

To skip Hermes Agent propagation:

```bash
make install NO_HERMES=1
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
  - `~/.agents/skills/plan-swarm/`
  - `~/.agents/skills/agent-history/`
  - `~/.agents/skills/model-consensus/`
  - `~/.agents/skills/contact-sheet-builder/`
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
  - `~/.claude/skills/plan-swarm/`
  - `~/.claude/skills/agent-history/`
  - `~/.claude/skills/model-consensus/`
  - `~/.claude/skills/contact-sheet-builder/`
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
  - `~/.gemini/skills/plan-swarm/`
  - `~/.gemini/skills/model-consensus/`
  - `~/.gemini/skills/contact-sheet-builder/`
  - `~/.gemini/skills/cynical-code-review/`
  - `~/.gemini/skills/cynical-architecture-review/`
  - `~/.gemini/skills/cynical-cruft-removal/`
  - `~/.gemini/skills/exhaustive-code-review/`
  - `~/.gemini/skills/thermo-nuclear-code-quality-review/`
  - `~/.gemini/skills/stepwise/`
  - `~/.gemini/skills/arch-epic/`

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed skill packages, older `~/.codex/skills/<skill>` mirrors, and local source/build internals so runtime routing stays unambiguous.

`arch-loop`, `delay-poll`, `wait`, and `code-review` are removed from the live installed surface; use native `/goal` for free-form completion, the host's native scheduling/reminder surface for timed waiting or polling, and ordinary host review behavior for generic code review. `agent-history` and `pr-review-followthrough` are installed on the agents/Codex and Claude Code surfaces. `agent-history` covers Codex and Claude Code local history; `pr-review-followthrough` owns live GitHub PR follow-through with replies and same-branch fixes. `contact-sheet-builder` is installed on all three skill surfaces and requires Python with Pillow at runtime. `arch-step-goal-prompt`, `figma-best-practices`, `fal-ai-tools`, `flutter-reference`, `chatgpt-web`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `plan-swarm`, `codex-cleanup`, `codex-babysit`, `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, `exhaustive-code-review`, and `thermo-nuclear-code-quality-review` are installed on all three skill surfaces. `chatgpt-web` is prompt-only and requires BrowserOS MCP plus an already logged-in ChatGPT browser session; it does not automate login. Subprocess skills still require the selected local `claude`, `codex`, `agent`, or `grok` CLI to exist on the host at invocation time. Provider routing is fixed: Codex runs GPT/GBT/OpenAI models plus Fugu (`fugu`) and Fugu Ultra (`fugu-ultra`), Claude Code runs supported Claude models, Cursor Agent runs only `composer-2.5-fast`, and Grok CLI runs `grok-build` or `grok-composer-2.5-fast`; do not pass model ids across runtimes. `fresh-consult` reports strict pass/fail read-only verdicts and `model-consensus` reports planning results; both can use Cursor Agent only for `composer-2.5-fast` and Grok only for Grok models. `fresh-consult` starts clean on the first consult turn, resumes second/third same-line read-only follow-ups from a captured exact session id, rotates fresh on turn four, and can run multiple read-only child chains when explicitly requested. `agent-delegate` may write to the shared worktree when invoked with an allowed write scope, starts fresh-resumable workers by default, can run multiple fresh-resumable workers when explicitly requested, and may resume an explicit same-runtime delegated session by exact handle. `plan-audit` is doctrine-only and prompt-first: it audits planning artifacts in whatever format they use, may keep a Markdown audit log beside file-backed plans, and includes a plan-backed implementation-audit code review mode that does not run tests, ask for logs, prove CI, require external coding-harness CLIs, or add scripts/controllers. `plan-implement` is doctrine-only and prompt-first: it implements from existing plans while keeping a lightweight implementation log, proof freshness, and warm plan-backed review aligned without external coding-harness spawning or deterministic control. `plan-swarm` is prompt-first: the parent agent coordinates parallel workers through `agent-delegate` and keeps human worklogs next to the plan. `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, and `exhaustive-code-review` are prompt-only and review-only: cynical code review owns skeptical implementation-integrity audits under `/tmp/cynical-code-review/`, cynical architecture review owns subtraction-first accidental architecture audits under `/tmp/cynical-architecture-review/`, cynical cruft removal owns deep deletion reports under `/tmp/cynical-cruft-removal/`, and exhaustive review owns coverage-led audits under `/tmp/exhaustive-code-review/`.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface in `~/.agents/skills/`, confirms old arch_skill-owned Codex and Claude hook entries are absent, confirms the old `~/.codex/skills/<skill>` mirrors are absent, confirms removed skill packages are absent for the supported runtimes, and validates the mirrored surface in every existing Hermes Agent skill root.

Restart your Codex, Claude Code, Gemini CLI, or Hermes Agent session after install so it
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

`consistency-pass` is the optional end-to-end cold-read helper before implementation. In Codex it uses two parallel cold reads; `auto-plan` runs it automatically after `phase-plan`. When it runs, `Decision: proceed to implement? yes` is only legal if the artifact is decision-complete and has no unresolved plan-shaping decisions left.

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

`miniarch-step implement-loop` and `miniarch-step auto-implement` share the same implementation-frontier delivery command. They implement the current approved ordered implementation frontier and use `audit-implementation` to decide whether the loop is clean or more work remains. Named later expansion is not current missing work until its proof gate is due. In Codex, miniarch fresh audit uses `gpt-5.4-mini` at `xhigh` reasoning effort when a fresh child audit is launched.

Use `miniarch-step` when the work needs full-arch execution but does not need `arch-step`'s broader helper surface.

### `arch-epic`

Use when one goal is too large for a single `arch-step` plan and should be decomposed into approved, ordered sub-plans. The epic doc owns the raw goal, decomposition, inter-plan gates, sub-plan DOC_PATHs, and append-only orchestration history; each sub-plan remains a real arch-step plan.

Interactive mode is re-entrant: `arch-epic` invokes or observes one arch-step transition at a time, runs a fresh Claude, Codex, or Grok scope-drift critic after each completed sub-plan, and advances only after the critic passes. Same-session `auto-plan` is the epic-level strict planning driver: after decomposition approval, it sets up the next sub-plan DOC_PATH, runs the real `$arch-step auto-plan <DOC_PATH>` sequence, requires `arch_stage_gate.py ready --doc <DOC_PATH>` to pass, and marks that sub-plan `planned` only after generated receipts prove readiness. Marker-only or copied planning text is not enough. Same-session `auto-implement` requires all non-complete sub-plans to be `planned`, then handles one planned sub-plan at a time: it re-checks readiness, runs real `$arch-step auto-implement <DOC_PATH>` until ArcStep `audit-implementation` is COMPLETE, runs the epic critic, and marks the sub-plan `complete` only after critic `pass`. One invocation, local proof, worklog text, or ArcStep audit alone is not enough. The separate spawned-harness automatic mode asks once for a role table (`epic_planner`, `implementation_worker`, `critic`), resolves shorthand to runnable model IDs, pins the policy, and drives one sub-plan at a time through spawned child harnesses with a 180s default child-wait cadence.

Use `arch-epic` instead of `stepwise` when the subprocesses are implementing one epic through arch-step-style sub-plans. Use `stepwise` when a foreign repo's doctrine already defines an ordered process to execute.

### `arch-docs`

Use when the job is leaving repo docs healthier: cleaning up stale, overlapping, misleading, or obviously dated docs, updating stale survivors, clarifying confusing docs, and promoting grounded missing truth into evergreen docs. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one grounded DGTFO docs-health pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, use git history when staleness or datedness matters, consolidate each topic to one canonical home, update stale surviving docs, clarify confusing docs, and add grounded missing docs when the canonical result is either a standard public-repo doc or a differentiated evergreen doc that deserves its own home. Repo posture is evidence-based: default to `private/internal` when unclear, but in `public OSS` repos treat `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` as expected standalone docs. Then delete stale, duplicate, or dated one-off truth and repair links or nav for the surviving docs.

`arch-docs auto` is the repeated docs-cleanup mode. In native `/goal`, it runs a grounded pass, fresh review, and repeats until the docs cleanup is clean or a real blocker stops it. Outside goal mode, it runs one bounded pass plus review and names the next command.

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

Use when the user wants to ask ChatGPT, consult ChatGPT in the browser, get a ChatGPT web opinion, or run a prompt with optional local attachments through the logged-in ChatGPT UI using BrowserOS MCP. The skill shapes rough prompts with `prompt-authoring` discipline, verifies that BrowserOS is already logged in to ChatGPT, defaults to Pro with Extended thinking when no mode or effort is specified, respects explicit Instant/Thinking/Pro and Light/Standard/Extended/Heavy requests, and returns ChatGPT's answer with a short receipt. It is prose-only: no scripts, runners, harnesses, OpenAI API calls, or automated login.

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

Use when the user wants to design, repair, or audit an ordered flow of multiple agent skills so each skill has a distinct job, concrete handoff artifact, clear peer boundary, and lean prompt contract. For 30+ skill suites or any multi-skill audit by scope phrase ("audit every skill in this project", "audit the skills for flow F1"), the DAG-grounded audit sub-mode parallel-walks the suite, builds a labeled-edge DAG substrate at `<doc-dir>/<doc-slug>_DAG.md` (mermaid graph + edge table + unresolved-reference list), then reasons over the substrate to surface wasted-energy patterns: over-promotion (helper installed as canonical stage), duplicate canonical-stage acceptance criteria, dead/lone-wolf skills, broken peer references, and high-fan-in primitives that look like hand-coded loops. Findings use the existing audit template; the `Owner` field names affected files only — the audit never invokes another skill at runtime. Optional d2 + SVG render via `skills/skill-flow/scripts/render_dag_d2.py` (requires `d2` binary on PATH; fails loudly when missing). Use `skill-authoring` for one isolated package, `prompt-authoring` for one prompt contract, `arch-epic` for decomposing one execution goal into `arch-step` sub-plans, and `stepwise` for deterministic process execution.

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

### `codex-cleanup`

Use when `~/.codex` is multi-GB, old session JSONL/log/cache files are bloated, or many parallel Codex instances are stalling on SQLite `database is locked`. The skill ships a local bash helper that defaults to dry-run, refuses to run `--apply` while any `codex` process is alive, prunes stale dated/cache/temp files, checkpoints SQLite WALs, and rotates `log/codex-tui.log` without touching live config, credentials, memories, plugins, skills, prompts, or history indexes.

### `codex-babysit`

Use when the user wants to keep an already-running Codex goal-mode tmux pane alive across real usage limits or process death. It watches the pane, rotates `aim` accounts only when Codex is actually blocked, restarts, resumes the same session, and verifies work resumed.

### `fresh-consult`

Use when the user or another skill wants one or more read-only second opinions from Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok subprocesses on concrete artifacts, completion checks, flow consistency questions, or readability/confusion checks. The skill is prompt-only: it writes consult prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed, captures each child chain under `/tmp/fresh-consult/...`, and reports each strict pass/fail child verdict back to the parent.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5`, `GBT55XI`, `fugu`, or `fugu-ultra` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions are preserved; there is no silent downgrade, provider switch, or effort substitution.

The first request in a consult line starts clean and captures a session handle. The second and third same-line requests resume that exact child session by default. Strict pass/fail review is not a reason to start fresh. The fourth same-line request starts a new clean chain unless the user explicitly asks to continue. Cold, independent, fresh-eyes, changed-runtime, changed-model, changed-effort, or changed-work-root requests start a new chain. The skill never resumes a "latest" session.

Each chain keeps `chain.json` plus per-turn `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, `execution.json`, and `session_id.txt`; resume turns also keep `resume_from.txt`. Consult children commonly take 5+ minutes; broad `xhigh` or `max` reads can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Use `fresh-consult` for cold reads, bounded read-only follow-up consults, parallel consults, consistency audits, completion checks, and general second opinions. The child receives the user's ask, consult mode, exact user-named artifacts, hard constraints, and strict pass/fail report contract; it chooses what evidence to inspect. Use `agent-delegate` when the child should implement, edit, investigate-and-fix, run commands, use installed skills in the shared worktree, run multiple fresh-resumable workers, or resume an editful delegated worker session. Use `codex-review-yolo` when the user specifically wants the existing Codex `-p yolo` review pattern. Use `stepwise` or `arch-epic` when subprocesses are part of a larger ordered workflow with manifests, critics, repair loops, or persistent orchestration.

### `agent-delegate`

Use when the user wants one or more Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok subprocesses to do concrete work in the current workspace: implementation, editing, investigation-and-fix, command execution, verification, installed-skill use, or explicit same-session continuation of a previous delegated worker. The skill is prompt-only: it writes delegation prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed in the shared worktree, captures each child `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, `execution.json`, and normally `session_id.txt` under `/tmp/agent-delegate/...`, then reports mode, status, changed files, verification, blockers, follow-up, session id when present, and run directories.

Fresh-resumable is the default. When the caller explicitly requests parallel workers, `agent-delegate` creates a group directory and launches ordinary fresh-resumable child workers, then inspects repo state before reporting the combined result. Stateless one-shot is available only when explicitly requested. Explicit resume uses a same-runtime session id or prior run directory. Claude resume uses `-r <session_id>` from the original work root; Codex resume uses `codex exec resume <thread_id>` and never `--last`; Cursor Agent and Grok resume use `--resume <session_id>` and never latest-session selection. The skill does not resume "latest" sessions, cross runtimes, or use external continuation controllers as a strategy.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5`, `GBT55XI`, `fugu`, or `fugu-ultra` for Codex, `Claude Fable 5` for Claude, `Cursor Agent composer 2.5` for Cursor Agent, or `Grok Build` for Grok. Cursor Agent Composer resolves to `composer-2.5-fast`; Grok resolves to `grok-build` unless Grok Composer is named. Exact model versions are preserved; there is no silent downgrade, provider switch, effort substitution, detached fallback, separate-worktree fallback, or ambiguous resume fallback.

Delegated children commonly take 5+ minutes; broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Use `agent-delegate` for operational worker paths where children may write files, fresh-resumable by default, stateless only when explicitly requested, and resumed only by exact handle. Use `fresh-consult` for read-only second opinions and completion checks. Use `plan-audit` for existing planning-document quality audits before implementation. Use `plan-implement` for ordinary plan-backed implementation that keeps lightweight logs and proof freshness without external worker orchestration. Use `model-consensus` for two-model plan convergence. Use `stepwise` or `arch-epic` when subprocesses are part of an ordered workflow with manifests, critics, repair loops, or persistent orchestration.

### `plan-audit`

Use when the user wants an existing planning artifact audited before work starts, in whatever format it already uses: PRD, migration plan, architecture plan, checklist, issue body, inline plan, or design doc. It improves plan quality by checking the North Star, done-state requirements, real ambiguity, constraints and non-constraints, repo/code truth when relevant, depth-first implementation risk, tiny-team simplicity, existing-pattern fit, drift-proofing, side doors, required deletes, and proof gaps.

Use `plan-audit implementation-audit` when the user wants code already written for a plan reviewed against that plan. This mode reviews code shape, owner path, SSOT, side-door closure, duplicate truth, stale docs/prompts, proof gaps, drift, caller fit, changed tests as code, and elegance. It is not generic diff review, does not run tests or CI, does not ask for logs, and does not investigate whether a completion claim is truthful.

The skill is prompt-first and doctrine-only. It may maintain `<PLAN_STEM>_PLAN_AUDIT.md` beside file-backed plans for repeat audits, but it does not write the plan, implement it, choose workflows, or add deterministic scripts, runners, controllers, scorers, or harnesses.

### `plan-implement`

Use when the user wants to implement an existing plan, phase, section, checklist, issue-body plan, or design doc while keeping implementation state easy to resume. The skill works depth-first from narrow proven slices, keeps `<PLAN_STEM>_IMPLEMENTATION_LOG.md` beside non-trivial file-backed plans, reuses proof until a real invalidator makes it stale, runs checks for impact rather than habit, and uses plan-audit implementation lenses for warm review while code is still easy to repair.

The plan remains source of truth, the plan-audit log owns `PLA-*` and `IMP-*` review findings, and the implementation log is only speed/resume state. Native subagents or parallel-agent features are encouraged when available for independent read, review, or safe low-collision work. The skill does not create plans, run generic code review, police CI logs, manually spawn `codex`, `claude`, `agent`, or `grok`, or replace `plan-swarm` for explicit delegated worker swarms.

Use `plan-implement` for normal plan-backed implementation with lightweight live review. Use `plan-audit` before implementation or for review-only implementation audits. Use `plan-swarm` when the user explicitly wants delegated external worker swarms, resumable child sessions, arbiter gates, or phase-swarm orchestration.

### `plan-swarm`

Use when the user wants to implement one named phase or explicit phase range from an existing plan document as fast as possible without dropping the quality bar. The skill extracts a compact phase contract, decomposes the work into independently delegable slices, launches or resumes Codex GPT/GBT/Fugu, Claude Fable/Opus, Cursor Composer, or Grok workers through `agent-delegate`, batches review/test findings into delegated repair and impact-aware verification waves, commits local progress checkpoints freely, writes human worklogs next to the plan, and closes only after arbiter and thermonuclear findings are triaged.

The parent agent owns orchestration: plan interpretation, decomposition, worker prompts, parallel delegation, session reuse, review triage, and completion judgment. Coordination stays readable in the phase contract, swarm ledger, worker logs, review notes, and final phase report next to the plan.

When the user chooses Cursor Agent implementation, Composer 2.5 means `composer-2.5-fast`, including shorthand like `composer`, `composer 2.5`, `composer-2.5`, or bare `2.5` in Cursor Agent context. When the user chooses Grok implementation, plain Grok means `grok-build`; Grok Composer means `grok-composer-2.5-fast`. Review policy is independent: GPT/GBT/Fugu review runs through Codex, Claude review runs through Claude Code, and Cursor or Grok implementation never causes review to run through that implementation runtime. The skill does not create worktrees, push, open PRs, use latest-session resume, or continue beyond the requested phase boundary. Local commits are ordinary checkpoints, including dirty inherited work that looks like resumed plan work.

Use `plan-swarm` for accelerated delegated plan-doc-backed implementation. Use `plan-implement` for ordinary plan-backed implementation with lightweight logs, proof freshness, and warm review but without external worker orchestration. Use `agent-delegate` for one-off delegation, `stepwise` for strict ordered external processes, `arch-epic` for multi-plan epic decomposition, and `fresh-consult` for read-only second opinions.

### `model-consensus`

Use when the user wants two selected Claude Fable/Opus, Codex GPT/GBT/Fugu, Cursor Composer, or Grok models to cross-check, critique, and iterate on a plan, architecture, investigation, design, or concept until they converge, or until they expose the smallest unresolved decision. The skill is prompt-only: the parent agent orchestrates directly, prepares prompt-authoring-quality briefs, launches resumable hook-suppressed child sessions where supported, relays critiques, and reports only child-agreed material. It does not add a deterministic runner, script, controller, or harness layer.

For investigations, root-cause work, and "read everything" cross-checks, the parent preserves discovery freedom. It records the raw user goal, exact user-named artifacts, desired output, and hard constraints. The child models choose and cite the code, docs, research, tests, commands, and local evidence they need.

For architecture or implementation-plan work, the skill keeps the existing single-path pressure: both models inspect canonical owners, adjacent patterns, duplicate pathways, and proof surfaces before agreeing on where the work should live.

The user supplies the two participant runtime/model/effort choices, or the skill asks once. It follows the shared model-resolution doctrine for shorthand such as `gpt 5.5 xhigh`, `GBT55XI`, `fugu high`, `fugu-ultra xhigh`, `Claude Fable 5 high`, `Cursor Agent composer 2.5`, and `Grok Build high`, preserves exact versions, and reports the raw-to-resolved mapping before execution. Cursor Agent always means `composer-2.5-fast`; Grok means `grok-build` unless Grok Composer is named.

Participant sessions preserve live event streams by default. Normal rounds often take 5+ minutes; broad repo-grounded `xhigh` or `max` rounds can reasonably take 20-40 minutes.

Use `model-consensus` for collaborative or adversarial plan refinement, two-model cross-checks, and repo-grounded investigation convergence. Use `fresh-consult` for read-only second opinions, including cold first-turn reads and bounded same-session follow-ups. Use `agent-delegate` for foreground workers that may edit the shared worktree, and `stepwise` or `arch-epic` for ordered implementation workflows.

### `contact-sheet-builder`

Use when the user wants a quick local contact sheet from existing image files, folders, globs, or attached local image paths. The skill uses one Pillow renderer script and defaults to dense labeled PNG sheets, dynamic near-native edge-to-edge canvas sizing, `0px` outside margin, `2px` gutters, Preview opening on macOS, overwrite protection, and concise receipts. Use `--margin` and `--gutter` only when spacing needs to change. Use `--no-open` for headless or batch runs. Use `--page-width` and `--page-height` only when a fixed page-style overview is wanted. Invoke the script directly with the `python3` that has Pillow installed. It is not for generating or editing images, video frame extraction, Figma boards, slide/doc layouts, provider APIs, or theme-specific generation flows.

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

Use when the user wants a prompt-only exhaustive code review over a branch, diff, path set, plan scope, or completion claim and wants the review saved to disk. The skill maximizes native parallel agents, inspects touched files, changed hunks, abstractions, callers, duplicate paths, side doors, stale truth, tests/proof, docs, generated artifacts, prompts, configs, and other live truth surfaces, then writes `target.md`, `coverage.md`, `findings.md`, and `verdict.md` under `/tmp/exhaustive-code-review/...`. Its verdicts are `approve`, `not-approved`, or `coverage-incomplete`.

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
- Use `codex-review-yolo` or `fresh-consult` for broader fresh-eyes second opinions.

## Usage

- Primary surface: ask the agent to use `arch-step`, `arch-step-goal-prompt`, `miniarch-step`, `arch-epic`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `chatgpt-web`, `skill-authoring`, `figma-best-practices`, `fal-ai-tools`, `flutter-reference`, `eli10`, `pr-authoring`, `pr-review-followthrough`, `commit-history-authoring`, `skill-flow`, `amir-publish`, `codex-cleanup`, `codex-babysit`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `contact-sheet-builder`, `cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`, `exhaustive-code-review`, `thermo-nuclear-code-quality-review`, `stepwise`, or `codex-review-yolo`.
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
