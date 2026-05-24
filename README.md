# arch_skill

This repo ships installable agent skills centered on the arch suite for Codex CLI, Claude Code, and Gemini CLI.

## Community

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Support: [SUPPORT.md](SUPPORT.md)

The live arch suite is:

- `arch-step` — the broad full-arch execution surface; owns the full staged workflow, extended helper passes, bounded `auto-plan`, implementation-frontier `implement-loop`, compact `status`, and guided `advance`
- `miniarch-step` — the trimmed full-arch surface; keeps canonical arch docs, phasing, and real auto controllers without the broader `arch-step` helper surface
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and hook-backed `auto` docs cleanup in Codex and Claude Code
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `miniarch-step` or `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `audit-loop` — exhaustive map-first repo audit loop with a root audit ledger, mandatory post-change self-audit, and hook-backed `auto` continuation in Codex and Claude Code
- `comment-loop` — exhaustive map-first repo comment hardening loop with a root comment ledger and hook-backed `auto` continuation in Codex and Claude Code
- `audit-loop-sim` — exhaustive map-first real-app automation audit loop with a root simulator ledger, mandatory post-change self-audit, and hook-backed `auto` continuation in Codex and Claude Code
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill
- `arch-epic` — multi-plan orchestrator that wraps `arch-step` for goals too big for a single canonical plan. Captures the goal, drafts a plain-English one-sentence-per-sub-plan decomposition with inter-plan gates, gets user approval, then runs sub-plans depth-first. Interactive mode drives each sub-plan through arch-step's `new` → `auto-plan` → `implement-loop` → `audit-implementation` arc and uses a fresh Claude/Codex critic after completion. Automatic mode asks for role-based execution choices for planner, implementation worker, and critic, resolves shorthand to exact runnable model IDs, pins the policy, then uses streamed hook-suppressed spawned harnesses with detached long-run monitoring and a 180s default child-wait cadence. Planner and implementation sessions are resumable; fresh critics report observation-only verdicts, and in-scope failures resume the same role session instead of spawning a separate repair worker.

Use `miniarch-step` when the work still needs a real full-arch artifact and auto continuation, but you want the trimmed command surface instead of the broader `arch-step` helper surface. Use `arch-step` when the work is broader, more ambiguous, or needs the full helper surface.

Other shipped skills are:

- `arch-loop` — generic hook-backed completion loop for Codex and Claude Code that takes free-form requirements, optional named-skill audit obligations (e.g. `$agent-linter`), and optional runtime/cadence/iteration caps, then drives repeat turns through the installed `Stop` hook until a fresh unsandboxed Codex `gpt-5.4` `xhigh` external evaluator emits a `clean` or `blocked` verdict. Distinct from `delay-poll` (condition-polling only, no work done between checks) and from specialized loops like `audit-loop` (prescribed map-first audit flow).
- `delay-poll` — delay-and-check controller for Codex and Claude Code that waits inside the installed `Stop` hook, re-runs a read-only condition check on a fixed interval, and resumes the same thread when the condition becomes true
- `wait` — one-shot delay-then-resume controller for Codex and Claude Code that sleeps inside the installed `Stop` hook for a parsed duration (`30m`, `1h30m`, `90s`, `2d`) and then injects a literal resume prompt back into the same thread exactly once. Use this for plain "wait N and continue" work. For condition re-checking use `delay-poll`; for recurring or scheduled work use `/loop` or `schedule`.
- `agent-definition-auditor` — cold-reader scoring and findings for `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompts, and other agent-definition markdown
- `agents-md-authoring` — writes, edits, refactors, and audits concise repo-present `AGENTS.md` files
- `prompt-authoring` — writes, edits, refactors, and audits prompts, reusable prompt contracts, and compact Codex `/goal` mission briefs
- `skill-authoring` — writes, edits, refactors, and audits prompt-first reusable agent skill packages
- `figma-best-practices` — prompt-only Figma file-craft doctrine for creating, auditing, or repairing structurally honest Figma files, libraries, variables, components, Dev Mode prep, Code Connect mapping, and Make/Sites/Buzz/Slides/MCP readiness
- `fal-ai-tools` — prompt-first fal.ai tool workflow for model discovery, schema and pricing lookup, file upload, background removal, media generation or editing, inference, polling, and result receipts using MCP when available and SDK/HTTP fallback otherwise
- `eli10` — answers in maximum-readability ELI10 style: reduces reader working-memory load, leads with the point, preserves exact technical truth, defines load-bearing jargon, explains mechanisms plainly, avoids fake memory and baby talk, and uses scan markers or tables only when they clarify
- `pr-authoring` — writes and publishes high-quality GitHub pull requests from real repo changes
- `commit-history-authoring` — rewrites the current branch's branch-span commit messages from its nearest parent branch into informative history while preserving commit boundaries, patches, trailers, and backup recovery; it never pushes rewritten history
- `skill-flow` — designs, repairs, and audits ordered multi-skill flows with distinct skill jobs, concrete handoffs, clear peer boundaries, and no prompt-runner scaffolding; for 30+ skill suites, the DAG-grounded audit sub-mode parallel-walks the suite, builds a labeled-edge substrate, and surfaces wasted-energy patterns (over-promotion, redundancy, dead skills, broken refs)
- `amir-publish` — personal shortcut for publishing this skills repo across Amir's usual machines
- `codex-cleanup` — dry-run-first local cleanup skill for stale `~/.codex` state that relieves multi-instance SQLite/WAL and log bloat without touching live config or credentials
- `codex-review-yolo` — external Codex `-p yolo` reviewer for substantial diffs, plans, docs, and completion checks, with live `--json` stream logs
- `fresh-consult` — prompt-only fresh Claude Opus or Codex GPT/GBT second opinions for cold reads, parallel consults, flow consistency audits, completion checks, and readability/confusion checks; asks once for runtime/model/effort when missing and reports each child result back to the parent skill
- `agent-delegate` — prompt-only Claude Opus, Codex GPT/GBT, or Cursor Composer workers for delegated implementation, editing, investigation-and-fix, command execution, or installed-skill use in the shared worktree; fresh one-shot is the default, explicit parallel workers are supported when requested, explicit same-session resume is available for one worker when continuity is required, and the skill reports changed files, verification, blockers, session id when present, and run directories
- `plan-audit` — prompt-first generic audit for existing planning artifacts in any format, plus plan-backed implementation-audit code review after code exists; checks plan quality before work starts and reviews implemented code against the plan for owner path, SSOT, side-door closure, drift, caller fit, and elegance without running tests, asking for logs, or dictating workflow
- `plan-implement` — prompt-first plan-backed implementation loop that keeps the plan, plan-audit log, implementation log, proof freshness, and warm code review aligned while coding so work survives compaction and avoids duplicate rereads, duplicate checks, late review, and external worker-swarm ceremony
- `plan-swarm` — prompt-first implementation swarm orchestrator that extracts one phase contract from an existing plan, decomposes it into independently delegable slices, launches or resumes parallel Codex GPT/GBT, Claude Opus, or Cursor Composer workers through `agent-delegate`, batches review/test findings into delegated repair and impact-aware verification waves, commits local progress checkpoints freely, writes worklogs next to the plan, and closes only after arbiter and thermonuclear findings are triaged
- `agent-history` — searches local Codex or Claude Code session history for prior prompts, goals, commands, corrections, tool use, and timelines from natural-language asks, using bundled read-only JSONL/SQLite helpers and concise evidence summaries
- `model-consensus` — prompt-only parent-agent orchestration for two selected Claude Opus, Codex GPT/GBT, or Cursor Composer model sessions to cross-check, critique, and converge on a plan, architecture, investigation, design, or concept until they agree or expose the smallest unresolved decision; preserves child discovery freedom for investigations and requires repo-backed participants to read real evidence before agreeing
- `contact-sheet-builder` — builds quick local contact sheet PNGs from existing images, folders, globs, or attached local image paths using a lean prompt contract plus one Pillow renderer; defaults to dense labeled sheets, dynamic near-native edge-to-edge canvas sizing, safe temp output, Preview opening on macOS, and concise receipts
- `code-review` — deterministic general code-review skill that always shells out to fresh unsandboxed Codex `gpt-5.4` `xhigh` (with parallel `gpt-5.4-mini` `xhigh` review lenses) for diffs, branches, paths, or completion-claim audits; supports direct and hook-backed invocation, and keeps Codex as the reviewer even when Claude hosts the Stop hook
- `thermo-nuclear-code-quality-review` — vendored Cursor Team Kit rubric for unusually strict maintainability reviews focused on code-judo simplification, 1k-line file growth, spaghetti branching, abstraction boundaries, and structural quality
- `stepwise` — diagnostic orchestrator for ordered multi-step processes defined in another repo's doctrine; spawns a fresh Claude or Codex worker session per step, runs an independent observational critic, and on failure diagnoses with the involved sessions before authoring a source-grounded repair at root cause. Model and effort for worker and critic are supplied by the user at invocation; both runtimes run dangerous / skip-permissions / no-sandbox. Distinct from `arch-loop` (requirement-satisfaction, not ordered steps), `arch-step` (plan-doc-backed full-arch), and `code-review` (one-shot review).

Examples in this repo use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, writes one arch_skill-managed Codex `Stop` hook in `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, writes one arch_skill-managed Claude Code `Stop` hook plus one `SessionStart` hook in `~/.claude/settings.json` pointing at the same installed runner with `--runtime claude`, removes older `~/.codex/skills/<skill>` mirrors from previous installs, and also installs the Claude Code and Gemini CLI skill directories. Source/build internals (`build/`, `prompts/`, `__pycache__/`, and `*.pyc`) are pruned from installed skill packages. The `thermo-nuclear-code-quality-review` package is sourced unchanged from the vendored Cursor Team Kit plugin at `vendor/cursor/plugins/cursor-team-kit/skills/`; the installer copies only that skill package, not Cursor Team Kit agents or rules. Every loop-skill arm also reruns the same idempotent, flock-guarded `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` so the canonical hook entries cannot drift between runs. Drift is fail-loud at dispatch: any non-canonical group, missing `SessionStart` on Claude, or stale runner path makes the Stop hook exit 2 with the exact repair command rather than silently migrate.

Codex automatic `auto-plan`, `implement-loop`, `auto-implement`, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, `arch-loop`, `delay-poll`, and `wait` also require the Codex feature flag:

```bash
codex features enable codex_hooks
```

Claude Code uses the installed settings-level `Stop` hook and does not depend on the Codex feature flag. Claude controllers that need fresh child review or check passes launch hook-suppressed child runs with `claude -p --settings '{"disableAllHooks":true}'`, so that child path must work with the machine's normal Claude auth.

Hook-backed skills all follow the **arm first, disarm never** controller contract at `skills/_shared/controller-contract.md`. That document owns the state-file paths, the arm-time ensure-install rule, the dispatch-time loud verify, the session-scoped conflict gate, the staleness sweep, and the manual recovery procedure. Do not run the Stop hook yourself — arm the controller, end the turn, and let the installed runner own the rest.

For manual recovery when a controller wedges, see the shared contract's Manual recovery section, or run the shared runner's disarm flags directly:

```bash
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --list-controllers
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm <name> [--session <id>]
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm-all --yes
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --doctor
```

To skip Gemini:

```bash
make install NO_GEMINI=1
```

Installed skills:

- Default local path:
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
  - `~/.agents/skills/code-review/`
  - `~/.agents/skills/thermo-nuclear-code-quality-review/`
  - `~/.agents/skills/stepwise/`
  - `~/.agents/skills/arch-epic/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
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
  - `~/.claude/skills/arch-loop/`
  - `~/.claude/skills/delay-poll/`
  - `~/.claude/skills/wait/`
  - `~/.claude/skills/agent-definition-auditor/`
  - `~/.claude/skills/agents-md-authoring/`
  - `~/.claude/skills/prompt-authoring/`
  - `~/.claude/skills/skill-authoring/`
  - `~/.claude/skills/figma-best-practices/`
  - `~/.claude/skills/fal-ai-tools/`
  - `~/.claude/skills/eli10/`
  - `~/.claude/skills/pr-authoring/`
  - `~/.claude/skills/commit-history-authoring/`
  - `~/.claude/skills/skill-flow/`
  - `~/.claude/skills/amir-publish/`
  - `~/.claude/skills/codex-cleanup/`
  - `~/.claude/skills/codex-review-yolo/`
  - `~/.claude/skills/fresh-consult/`
  - `~/.claude/skills/agent-delegate/`
  - `~/.claude/skills/plan-audit/`
  - `~/.claude/skills/plan-implement/`
  - `~/.claude/skills/plan-swarm/`
  - `~/.claude/skills/agent-history/`
  - `~/.claude/skills/model-consensus/`
  - `~/.claude/skills/contact-sheet-builder/`
  - `~/.claude/skills/code-review/`
  - `~/.claude/skills/thermo-nuclear-code-quality-review/`
  - `~/.claude/skills/stepwise/`
  - `~/.claude/skills/arch-epic/`
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
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
  - `~/.gemini/skills/skill-authoring/`
  - `~/.gemini/skills/figma-best-practices/`
  - `~/.gemini/skills/fal-ai-tools/`
  - `~/.gemini/skills/eli10/`
  - `~/.gemini/skills/pr-authoring/`
  - `~/.gemini/skills/commit-history-authoring/`
  - `~/.gemini/skills/skill-flow/`
  - `~/.gemini/skills/amir-publish/`
  - `~/.gemini/skills/codex-cleanup/`
  - `~/.gemini/skills/codex-review-yolo/`
  - `~/.gemini/skills/fresh-consult/`
  - `~/.gemini/skills/agent-delegate/`
  - `~/.gemini/skills/plan-audit/`
  - `~/.gemini/skills/plan-implement/`
  - `~/.gemini/skills/plan-swarm/`
  - `~/.gemini/skills/model-consensus/`
  - `~/.gemini/skills/contact-sheet-builder/`
  - `~/.gemini/skills/thermo-nuclear-code-quality-review/`
  - `~/.gemini/skills/stepwise/`
  - `~/.gemini/skills/arch-epic/`

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed skill packages, older `~/.codex/skills/<skill>` mirrors, and local source/build internals so runtime routing stays unambiguous.

`arch-loop`, `delay-poll`, and `wait` are installed on Codex and Claude Code because both runtimes have a native `Stop` hook surface; all three are omitted from Gemini because Gemini still has no hook-backed auto-controller surface and there is no way for the parsed duration, condition re-check, or evaluator-backed verdict to resume the same thread there. `arch-loop` evaluator turns additionally always shell out to fresh unsandboxed Codex `gpt-5.4` `xhigh` for the external verdict; the Claude host can arm and drive the loop, but the evaluator subprocess itself is always Codex, mirroring the `code-review` exception below. `agent-history` is installed on the agents/Codex and Claude Code surfaces because its v1 storage map covers Codex and Claude Code local history. `contact-sheet-builder` is installed on all three skill surfaces and requires Python with Pillow at runtime. `figma-best-practices`, `fal-ai-tools`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `plan-swarm`, and `thermo-nuclear-code-quality-review` are installed on all three skill surfaces. Subprocess skills still require the selected local `claude`, `codex`, or `agent` CLI to exist on the host at invocation time. Provider routing is fixed: Codex runs GPT/GBT/OpenAI models, Claude Code runs Opus, and Cursor Agent runs only `composer-2.5-fast`; do not use Cursor Agent as a host for GPT/GBT or Claude model ids. `fresh-consult` and `model-consensus` report read-only or planning results; `fresh-consult` can run multiple fresh read-only children when explicitly requested. `agent-delegate` may write to the shared worktree when invoked with an allowed write scope, can run multiple fresh workers when explicitly requested, and may resume an explicit same-runtime delegated session when the caller requires continuity. `plan-audit` is doctrine-only and prompt-first: it audits planning artifacts in whatever format they use, may keep a Markdown audit log beside file-backed plans, and includes a plan-backed implementation-audit code-review mode that does not run tests, ask for logs, prove CI, require external coding-harness CLIs, or add scripts/controllers. `plan-implement` is doctrine-only and prompt-first: it implements from existing plans while keeping a lightweight implementation log, proof freshness, and warm plan-backed review aligned without external coding-harness spawning or deterministic control. `plan-swarm` is prompt-first: the parent agent coordinates parallel workers through `agent-delegate` and keeps human worklogs next to the plan. `code-review` is installed on the agents/Codex and Claude Code surfaces only; the Claude host can trigger the skill, but the actual review subprocess always shells out to fresh Codex.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface in `~/.agents/skills/`, checks that exactly one arch_skill-managed Codex `Stop` hook exists in `~/.codex/hooks.json` and points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, checks that exactly one arch_skill-managed Claude Code `Stop` hook plus one `SessionStart` hook exist in `~/.claude/settings.json` and point at the same installed runner with `--runtime claude`, confirms the old `~/.codex/skills/<skill>` mirrors are absent, and confirms removed skill packages are absent for the supported runtimes. The Stop hook itself also re-runs the same verify on every dispatch and exits 2 with the exact repair command if it finds drift — there is no silent migration, no legacy fallback, no transitional shim.

To confirm the Codex feature gate is enabled:

```bash
codex features list | rg '^codex_hooks\\s+.*\\strue$'
```

Restart your Codex, Claude Code, or Gemini CLI session after install so it reloads skills.

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
- `audit-implementation`
- `status`
- `advance`

`consistency-pass` is the optional end-to-end cold-read helper before implementation. In Codex it uses two parallel cold reads; `auto-plan` runs it automatically after `phase-plan`. When it runs, `Decision: proceed to implement? yes` is only legal if the artifact is decision-complete and has no unresolved plan-shaping decisions left.

`auto-plan` is the automatic planning controller in Codex and Claude Code. The user-facing command is still just `$arch-step auto-plan` in Codex or `/arch-step auto-plan` in Claude Code, with an optional `docs/MY_PLAN.md` argument. `DOC_PATH` is always the planning ledger. The armed controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent `auto-plan` pass runs only `research`, then ends its turn. On reruns, the installed Stop hook reads the doc and resumes from the first incomplete stage through `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`, then owns the successful `implement-loop` handoff. That handoff is allowed only when the artifact is decision-complete. If any unresolved plan-shaping decision remains, `auto-plan` must stop and ask the user the exact blocker question; the Stop hook clears controller state. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). If `--ensure-installed` fails loud, repair the named prerequisite and rerun.

`arch-step` does not have authority to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, the skill must ask the user instead of guessing.

Before Section 7 is allowed to harden, `arch-step` should inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story, such as sibling formats, readers/writers, examples, fixtures, mirrored config, generated artifacts, or live docs. It should include those surfaces now, assign them to a named later phase, explicitly exclude them, or ask one exact blocker question instead of silently leaving them contradictory.

Compatibility posture is separate from `fallback_policy`. The plan should say whether it preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. `arch-step` should not assume backward compatibility by default just because it feels safer.

Section 7 phase plans should protect the full destination map while building depth-first. The first working slice should prove one real path through the canonical owner path and highest-risk seam; later phases should expand along named axes. Phase count follows proof gates, dependency edges, reversibility or migration boundaries, and user-review boundaries rather than a preset number. New phase plans should use an explicit `Checklist (must all be done)` plus `Exit criteria (all required)` so a phase cannot be called complete while planned obligations are still implicit.

`implement-loop` is the automatic implementation-frontier delivery controller in Codex and Claude Code. `auto-implement` is an exact user-facing synonym for the same controller. The user-facing command is `$arch-step implement-loop docs/MY_PLAN.md` or `$arch-step auto-implement docs/MY_PLAN.md` in Codex, and the same `/arch-step ...` command in Claude Code. It arms loop state before implementation work, then runs the current approved ordered implementation frontier: the earliest incomplete or reopened phase plus later phases whose prerequisites and proof gates are reachable in this arc. Named later expansion is not current missing work until its proof gate is due; silent removal from the destination map is still a scope cut. The controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). Claude fresh-audit cycles additionally require working hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'`.

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `miniarch-step`

Use `miniarch-step` when the work still needs a canonical full-arch doc, phased execution, and real auto controllers in Codex or Claude Code, but does not need `arch-step`'s broader staged helper surface. It keeps the trimmed command surface without changing the full-work posture.

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
- `audit-implementation`
- `status`
- `advance`

`miniarch-step auto-plan` is the planning controller for the trimmed full-arch surface in Codex and Claude Code. `DOC_PATH` is the planning ledger and the armed controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent pass runs only `research`, then ends its turn. On reruns, the installed Stop hook resumes from the first incomplete stage through `deep-dive` and `phase-plan`, then owns the successful `implement-loop` handoff.

`miniarch-step implement-loop` and `miniarch-step auto-implement` share the same implementation-frontier delivery controller. They arm runtime-local controller state under `.codex/` in Codex or `.claude/arch_skill/` in Claude Code, implement the current approved ordered implementation frontier, and let fresh `audit-implementation` decide whether the loop is clean or more work remains. Named later expansion is not current missing work until its proof gate is due. In Codex, that fresh miniarch audit child runs with `gpt-5.4-mini` at `xhigh` reasoning effort.

Use `miniarch-step` when the work needs full-arch execution but does not need `arch-step`'s broader helper surface.

### `arch-epic`

Use when one goal is too large for a single `arch-step` plan and should be decomposed into approved, ordered sub-plans. The epic doc owns the raw goal, decomposition, inter-plan gates, sub-plan DOC_PATHs, and append-only orchestration history; each sub-plan remains a real arch-step plan.

Interactive mode is re-entrant: `arch-epic` invokes or observes one arch-step transition at a time, runs a fresh Claude or Codex scope-drift critic after each completed sub-plan, and advances only after the critic passes. Automatic mode is explicit and opt-in after decomposition approval. It asks once for a role table (`epic_planner`, `implementation_worker`, `critic`), resolves shorthand such as `opus 4.7 xhigh` or `gpt 5.5 high` to runnable model IDs, writes a pinned policy, then drives one sub-plan at a time through spawned hook-suppressed harnesses. Planner and implementation sessions are resumed after in-scope critic failures; critics stay fresh, stateless, and observation-only. The default child wait cadence is 180 seconds; long planner and implementation children run detached with live `events.jsonl`, `stderr.log`, and `stream.log` artifacts rather than tight polling.

Use `arch-epic` instead of `stepwise` when the subprocesses are implementing one epic through arch-step-style sub-plans. Use `stepwise` when a foreign repo's doctrine already defines an ordered process to execute.

### `arch-docs`

Use when the job is leaving repo docs healthier: cleaning up stale, overlapping, misleading, or obviously dated docs, updating stale survivors, clarifying confusing docs, and promoting grounded missing truth into evergreen docs. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one grounded DGTFO docs-health pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, use git history when staleness or datedness matters, consolidate each topic to one canonical home, update stale surviving docs, clarify confusing docs, and add grounded missing docs when the canonical result is either a standard public-repo doc or a differentiated evergreen doc that deserves its own home. Repo posture is evidence-based: default to `private/internal` when unclear, but in `public OSS` repos treat `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` as expected standalone docs. Then delete stale, duplicate, or dated one-off truth and repair links or nav for the surviving docs.

`arch-docs auto` is the hook-backed controller for repeated docs-cleanup passes in Codex and Claude Code. The user-facing command is still just `$arch-docs auto` in Codex or `/arch-docs auto` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude).

For any of these supported auto controllers, do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run.

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

### `arch-loop`

Use when the user wants Codex or Claude Code to drive a generic hook-backed completion loop: free-form requirements go in, optional named-skill audit obligations (e.g. `$agent-linter`, `$code-review`) and optional runtime/cadence/iteration caps, and the loop runs repeat parent turns through the installed `Stop` hook until an external Codex evaluator returns `clean` or `blocked`. Every evaluator turn always shells out to a fresh unsandboxed Codex `gpt-5.4` `xhigh` subprocess — even when Claude hosts the Stop hook — and the evaluator's structured verdict is the only thing that can stop the loop. Continue verdicts choose between `parent_work` (run another implementation turn now) and `wait_recheck` (sleep `cadence_seconds` inside the hook, then re-run the evaluator without spending a parent turn). Controller state lives under `.codex/arch-loop-state.<SESSION_ID>.json` in Codex and under `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). Distinct from `delay-poll` (condition-polling only, no work done between checks) and from specialized loops like `audit-loop` / `comment-loop` / `audit-loop-sim` (prescribed map-first flows with their own artifact contracts).

### `delay-poll`

Use when the user wants Codex or Claude Code to wait on some external condition, re-check it every 30 minutes, every hour, or similar, and continue the same visible thread only after that condition becomes true.

### `wait`

Use when the user wants Codex or Claude Code to sleep a specific parsed duration (`30m`, `1h30m`, `90s`, `2d`) and then continue the same visible thread with a literal follow-up prompt exactly once. No polling, no re-checking, no fresh child run during the wait. For condition re-checking use `delay-poll`; for recurring or scheduled work use `/loop` or `schedule`.

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

Use when the user wants to write, edit, refactor, or audit a prompt, reusable prompt contract, or Codex `/goal` mission brief so it fits the user's intent, evidence needs, constraints, stop rules, and output shape without becoming brittle or overbuilt. The user does not need to name a prompt type or mode; the skill infers the shape from normal language. For `/goal` prompts, it writes compact outcome-driven mission briefs with source truth pointers, quality bar, evidence, stop rules, and first-class signoff when needed, rather than rigid field forms or duplicated plan docs.

### `skill-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable agent skill package so it stays prompt-first, simple by default, generalized from user intent, anti-heuristic, and clear about peer boundaries, packaging, references, and validation.

### `figma-best-practices`

Use when the user wants to create, audit, or repair a Figma file, component library, variable/token system, prototype, Dev Mode surface, Code Connect mapping, Make kit, Sites page, Buzz template, Slides deck, or MCP-readable design artifact. The skill is prompt-only: it applies bundled Figma file-craft doctrine so the file is structurally honest, tokenized, componentized, semantically named, and ready for downstream human, developer, publishing, and AI consumers. Use implementation or Figma automation skills instead when the task is building code from a Figma design or operating the Figma UI itself.

### `fal-ai-tools`

Use when the user wants to use fal.ai tools, models, MCP, SDK/API calls, background removal, media generation or editing, model discovery, schema lookup, pricing checks, file upload, inference, polling, or result receipts. The skill is prompt-first: it prefers visible fal MCP tools, falls back to `fal_client` or raw HTTP when MCP is unavailable, checks live schemas and pricing before paid calls, and keeps fal keys redacted. Use provider-specific implementation or frontend skills instead when the task does not call fal.

### `eli10`

Use when the user wants any answer, explanation, plan, review, recommendation, rewrite, or status update in ELI10/ELI16 maximum-readability style. The skill teaches the agent to spend the reader's working memory on the idea, not on parsing: lead with the point, explain at the right layer, unstack dense phrases, define load-bearing jargon, preserve exact commands/metrics/file names, avoid fake memory and baby talk, and skip next steps unless asked. It uses native tables only when they improve understanding, and avoids tables when long prose, paths, commands, or root-cause explanations would be clearer as bullets or sections. It uses the decision-brief contract only when the answer is asking the user to choose. Use `prompt-authoring` for prompts and reusable prompt contracts and `skill-authoring` for skill packages.

### `pr-authoring`

Use when the user wants a high-quality GitHub pull request written and published from real repo changes. The skill inspects repo truth, uses its vendored PR scaffold as a quality reference, creates or updates the GitHub PR, and returns the PR link instead of only printing suggested text.

### `commit-history-authoring`

Use when the user wants the current branch's commit messages rewritten into an informative history from the point where the branch diverged from its nearest parent branch. The skill inspects the inferred branch-span range, diffs, old messages, trailers, and any evidenced active arch plan; it then applies a message-only rewrite with a backup branch while preserving commit boundaries, patch content, author metadata, and final tree state. It allows commits already reachable from the current branch's own remote-tracking ref, but refuses dirty worktrees, unrelated shared remote refs, current-branch remotes ahead of local `HEAD`, protected branches by default, and merge commits. It never pushes or force-pushes.

### `skill-flow`

Use when the user wants to design, repair, or audit an ordered flow of multiple agent skills so each skill has a distinct job, concrete handoff artifact, clear peer boundary, and lean prompt contract. For 30+ skill suites or any multi-skill audit by scope phrase ("audit every skill in this project", "audit the skills for flow F1"), the DAG-grounded audit sub-mode parallel-walks the suite, builds a labeled-edge DAG substrate at `<doc-dir>/<doc-slug>_DAG.md` (mermaid graph + edge table + unresolved-reference list), then reasons over the substrate to surface wasted-energy patterns: over-promotion (helper installed as canonical stage), duplicate canonical-stage acceptance criteria, dead/lone-wolf skills, broken peer references, and high-fan-in primitives that look like hand-coded loops. Findings use the existing audit template; the `Owner` field names affected files only — the audit never invokes another skill at runtime. Optional d2 + SVG render via `skills/skill-flow/scripts/render_dag_d2.py` (requires `d2` binary on PATH; fails loudly when missing). Use `skill-authoring` for one isolated package, `prompt-authoring` for one prompt contract, `arch-epic` for decomposing one execution goal into `arch-step` sub-plans, and `stepwise` for deterministic process execution.

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

### `codex-cleanup`

Use when `~/.codex` is multi-GB, old session JSONL/log/cache files are bloated, or many parallel Codex instances are stalling on SQLite `database is locked`. The skill ships a local bash helper that defaults to dry-run, refuses to run `--apply` while any `codex` process is alive, prunes stale dated/cache/temp files, checkpoints SQLite WALs, and rotates `log/codex-tui.log` without touching live config, credentials, memories, plugins, skills, prompts, or history indexes.

### `fresh-consult`

Use when the user or another skill wants one or more clean-context second opinions from fresh Claude Opus or Codex GPT/GBT subprocesses on concrete artifacts, completion checks, flow consistency questions, or readability/confusion checks. The skill is prompt-only: it writes consult prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed, captures each child `prompt.md`, `final.txt`, `events.jsonl`, and `stderr.log` under `/tmp/fresh-consult/...`, and reports each child verdict back to the parent.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5` or `GBT55XI` for Codex, or `Claude Opus 4.7` for Claude. Cursor Agent is not a consult host. Exact model versions are preserved; there is no silent downgrade, provider switch, or effort substitution.

Consult children commonly take 5+ minutes; broad `xhigh` or `max` reads can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Use `fresh-consult` for cold reads, parallel consults, consistency audits, completion checks, and general second opinions. The child receives the user's ask, exact user-named artifacts, hard constraints, and report contract; it chooses what evidence to inspect. Use `agent-delegate` when the child should implement, edit, investigate-and-fix, run commands, use installed skills in the shared worktree, run multiple fresh workers, or explicitly resume the same delegated worker session. Use `code-review` when the user wants the deterministic full code-review product with Codex lens fan-out and coverage guarantees. Use `codex-review-yolo` when the user specifically wants the existing Codex `-p yolo` review pattern. Use `stepwise` or `arch-epic` when subprocesses are part of a larger ordered workflow with manifests, critics, repair loops, or persistent orchestration.

### `agent-delegate`

Use when the user wants one or more Claude Opus, Codex GPT/GBT, or Cursor Composer subprocesses to do concrete work in the current workspace: implementation, editing, investigation-and-fix, command execution, verification, installed-skill use, or explicit same-session continuation of a previous delegated worker. The skill is prompt-only: it writes delegation prompts, runs the selected local CLI hook-suppressed where supported and unsandboxed in the shared worktree, captures each child `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, and `execution.json` under `/tmp/agent-delegate/...`, then reports mode, status, changed files, verification, blockers, follow-up, session id when present, and run directories.

Fresh one-shot is the default. When the caller explicitly requests parallel workers, `agent-delegate` creates a group directory and launches ordinary fresh child workers, then inspects repo state before reporting the combined result. When the caller explicitly requires continuity, `agent-delegate` can start a fresh-resumable worker or resume an explicit same-runtime session id / prior run directory. Claude resume uses `-r <session_id>` from the original work root; Codex resume uses `codex exec resume <thread_id>` and never `--last`; Cursor Agent resume uses `--resume <session_id>` and never `--continue`, `agent resume`, or `agent ls`. The skill does not resume "latest" sessions, cross runtimes, or use hook-backed controllers as a continuation strategy.

The user supplies runtime, model, and effort, or the skill asks once before invoking. Runtime can be inferred only from unambiguous model families such as `gpt-5.5` or `GBT55XI` for Codex, `Claude Opus 4.7` for Claude, or `Cursor Agent composer 2.5` for Cursor Agent. Composer 2.5 always resolves to `composer-2.5-fast`; Cursor Agent never hosts GPT/GBT or Claude model ids. Exact model versions are preserved; there is no silent downgrade, provider switch, effort substitution, detached fallback, separate-worktree fallback, or ambiguous resume fallback.

Delegated children commonly take 5+ minutes; broad edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live streams every few minutes, not every few seconds.

Use `agent-delegate` for operational worker paths where children may write files, fresh by default and resumable only by explicit handle. Use `fresh-consult` for read-only second opinions and completion checks. Use `plan-audit` for existing planning-document quality audits before implementation. Use `plan-implement` for ordinary plan-backed implementation that keeps lightweight logs and proof freshness without external worker orchestration. Use `model-consensus` for two-model plan convergence. Use `stepwise` or `arch-epic` when subprocesses are part of an ordered workflow with manifests, critics, repair loops, or persistent orchestration.

### `plan-audit`

Use when the user wants an existing planning artifact audited before work starts, in whatever format it already uses: PRD, migration plan, architecture plan, checklist, issue body, inline plan, or design doc. It improves plan quality by checking the North Star, done-state requirements, real ambiguity, constraints and non-constraints, repo/code truth when relevant, depth-first implementation risk, tiny-team simplicity, existing-pattern fit, drift-proofing, side doors, required deletes, and proof gaps.

Use `plan-audit implementation-audit` when the user wants code already written for a plan reviewed against that plan. This mode reviews code shape, owner path, SSOT, side-door closure, drift, caller fit, changed tests as code, and elegance. It is not generic diff review, does not run tests or CI, does not ask for logs, and does not investigate whether a completion claim is truthful.

The skill is prompt-first and doctrine-only. It may maintain `<PLAN_STEM>_PLAN_AUDIT.md` beside file-backed plans for repeat audits, but it does not write the plan, implement it, choose workflows, or add deterministic scripts, runners, controllers, scorers, or harnesses.

### `plan-implement`

Use when the user wants to implement an existing plan, phase, section, checklist, issue-body plan, or design doc while keeping implementation state easy to resume. The skill works depth-first from narrow proven slices, keeps `<PLAN_STEM>_IMPLEMENTATION_LOG.md` beside non-trivial file-backed plans, reuses proof until a real invalidator makes it stale, runs checks for impact rather than habit, and uses plan-audit implementation lenses for warm review while code is still easy to repair.

The plan remains source of truth, the plan-audit log owns `PLA-*` and `IMP-*` review findings, and the implementation log is only speed/resume state. Native subagents or parallel-agent features are encouraged when available for independent read, review, or safe low-collision work. The skill does not create plans, run generic code review, police CI logs, manually spawn `codex`, `claude`, or `agent`, or replace `plan-swarm` for explicit delegated worker swarms.

Use `plan-implement` for normal plan-backed implementation with lightweight live review. Use `plan-audit` before implementation or for review-only implementation audits. Use `plan-swarm` when the user explicitly wants delegated external worker swarms, resumable child sessions, arbiter gates, or phase-swarm orchestration.

### `plan-swarm`

Use when the user wants to implement one named phase or explicit phase range from an existing plan document as fast as possible without dropping the quality bar. The skill extracts a compact phase contract, decomposes the work into independently delegable slices, launches or resumes Codex GPT/GBT, Claude Opus, or Cursor Composer workers through `agent-delegate`, batches review/test findings into delegated repair and impact-aware verification waves, commits local progress checkpoints freely, writes human worklogs next to the plan, and closes only after arbiter and thermonuclear findings are triaged.

The parent agent owns orchestration: plan interpretation, decomposition, worker prompts, parallel delegation, session reuse, review triage, and completion judgment. Coordination stays readable in the phase contract, swarm ledger, worker logs, review notes, and final phase report next to the plan.

When the user chooses Cursor Agent implementation, Composer 2.5 means `composer-2.5-fast`, including shorthand like `composer`, `composer 2.5`, `composer-2.5`, or bare `2.5` in Cursor Agent context. Review policy is independent: GPT/GBT review runs through Codex, Opus review runs through Claude Code, and Cursor implementation never causes review to run through Cursor. The skill does not create worktrees, push, open PRs, use latest-session resume, or continue beyond the requested phase boundary. Local commits are ordinary checkpoints, including dirty inherited work that looks like resumed plan work.

Use `plan-swarm` for accelerated delegated plan-doc-backed implementation. Use `plan-implement` for ordinary plan-backed implementation with lightweight logs, proof freshness, and warm review but without external worker orchestration. Use `agent-delegate` for one-off delegation, `stepwise` for strict ordered external processes, `arch-epic` for multi-plan epic decomposition, `fresh-consult` for read-only second opinions, and `code-review` for deterministic code-review findings.

### `model-consensus`

Use when the user wants two selected Claude Opus, Codex GPT/GBT, or Cursor Composer models to cross-check, critique, and iterate on a plan, architecture, investigation, design, or concept until they converge, or until they expose the smallest unresolved decision. The skill is prompt-only: the parent agent orchestrates directly, prepares prompt-authoring-quality briefs, launches resumable hook-suppressed child sessions where supported, relays critiques, and reports only child-agreed material. It does not add a deterministic runner, script, controller, or harness layer.

For investigations, root-cause work, and "read everything" cross-checks, the parent preserves discovery freedom. It records the raw user goal, exact user-named artifacts, desired output, and hard constraints. The child models choose and cite the code, docs, research, tests, commands, and local evidence they need.

For architecture or implementation-plan work, the skill keeps the existing single-path pressure: both models inspect canonical owners, adjacent patterns, duplicate pathways, and proof surfaces before agreeing on where the work should live.

The user supplies the two participant runtime/model/effort choices, or the skill asks once. It follows the shared model-resolution doctrine for shorthand such as `gpt 5.5 xhigh`, `GBT55XI`, `Claude Opus 4.7 high`, and `Cursor Agent composer 2.5`, preserves exact versions, and reports the raw-to-resolved mapping before execution. Cursor Agent always means `composer-2.5-fast`, never GPT/GBT or Claude.

Participant sessions preserve live event streams by default. Normal rounds often take 5+ minutes; broad repo-grounded `xhigh` or `max` rounds can reasonably take 20-40 minutes.

Use `model-consensus` for collaborative or adversarial plan refinement, two-model cross-checks, and repo-grounded investigation convergence. Use `fresh-consult` for one-shot cold opinions, `agent-delegate` for foreground workers that may edit the shared worktree, `code-review` for deterministic review findings, and `stepwise` or `arch-epic` for ordered implementation workflows.

### `contact-sheet-builder`

Use when the user wants a quick local contact sheet from existing image files, folders, globs, or attached local image paths. The skill uses one Pillow renderer script and defaults to dense labeled PNG sheets, dynamic near-native edge-to-edge canvas sizing, `0px` outside margin, `2px` gutters, Preview opening on macOS, overwrite protection, and concise receipts. Use `--margin` and `--gutter` only when spacing needs to change. Use `--no-open` for headless or batch runs. Use `--page-width` and `--page-height` only when a fixed page-style overview is wanted. Invoke the script directly with the `python3` that has Pillow installed. It is not for generating or editing images, video frame extraction, Figma boards, slide/doc layouts, provider APIs, or theme-specific generation flows.

### `code-review`

Use when the user wants a real, deterministic code review against a diff, branch, path set, or "is this plan phase actually complete?" completion-claim. The skill does not review with the caller model. Every review subprocess is a fresh unsandboxed Codex process at `gpt-5.4` `xhigh` for the final synthesis, with parallel `gpt-5.4-mini` `xhigh` Codex subprocesses for per-lens review coverage (`correctness`, `architecture`, `proof`, `docs-drift`, `security`, and a conditional `agent-linter` lens when the change touches agent-building or instruction-bearing surfaces). The runner writes a namespaced artifact tree under `/tmp/code-review/...` (or a caller-supplied `--output-root`) that includes per-lens prompts, live `--json` stream logs, final outputs, and a single synthesized `ReviewVerdict`.

Review children commonly take 5+ minutes; xhigh synthesis or broad lens coverage can reasonably take 20-40 minutes. Poll stream logs every few minutes, not every few seconds.

Direct invocation runs the runner as a one-shot command. The skill also wires into the shared `arch-step` Stop-hook dispatcher so Codex and Claude Code can trigger the same runner via `.codex/code-review-state.<SESSION_ID>.json` or `.claude/arch_skill/code-review-state.<SESSION_ID>.json`. The Claude-host path is an intentional exception to the broader native-auto-loop direction: the Stop hook runs under Claude, but the review subprocess itself must always be Codex. Generic Claude auto-controllers stay Claude-native; `code-review` does not. `code-review` is review-only — it never edits the reviewed repo and never writes a "suggested patch" block.

Use `code-review` when the user wants an automated finding-set with explicit coverage guarantees. Use `plan-audit implementation-audit` when the user wants prompt-first code review against a specific plan without running tests, proving CI, or launching the code-review runner. Use `fresh-consult` when the user wants a general Claude Opus or Codex GPT/GBT second opinion without the code-review runner. Use `codex-review-yolo` when the user wants a narrower, more interactive `-p yolo` fresh-eyes consult on a specific artifact.

### `thermo-nuclear-code-quality-review`

Use when the user explicitly asks for a thermo-nuclear / thermonuclear review, a code-judo review, an especially harsh maintainability review, or a strict audit of structural quality, file sprawl, spaghetti branching, abstraction boundaries, and codebase health. This is a vendored Cursor Team Kit skill installed from `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/`.

It is a rubric-only review skill. It has no local runner, no Stop-hook controller, and no subprocess requirement. The installer copies the skill package only; it does not install Cursor Team Kit's Cursor-specific agents or rules.

Examples:

- `Use $thermo-nuclear-code-quality-review on this diff`
- `Run a thermonuclear maintainability review`
- `Use the code-judo quality rubric on this PR`

Practical rule:

- Use `thermo-nuclear-code-quality-review` only when the user wants this unusually strict maintainability rubric.
- Use `code-review` for ordinary code review requests and deterministic lens coverage.
- Use `codex-review-yolo` or `fresh-consult` for broader fresh-eyes second opinions.

## Usage

- Primary surface: ask the agent to use `arch-step`, `miniarch-step`, `arch-epic`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `arch-loop`, `delay-poll`, `wait`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `skill-authoring`, `figma-best-practices`, `fal-ai-tools`, `eli10`, `pr-authoring`, `commit-history-authoring`, `skill-flow`, `amir-publish`, `codex-cleanup`, `fresh-consult`, `agent-delegate`, `plan-audit`, `plan-implement`, `model-consensus`, `contact-sheet-builder`, `code-review`, `thermo-nuclear-code-quality-review`, `stepwise`, or `codex-review-yolo`.
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
- `Use $miniarch-step for this feature`
- `Use $miniarch-step auto-plan`
- `Use $miniarch-step implement-loop docs/MY_PLAN.md`
- `Use $miniarch-step auto-implement docs/MY_PLAN.md`
- `Use $arch-epic to break this migration into sub-plans and run them in order`
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
- `Use $arch-loop tighten the onboarding copy across the marketing site until it reads cleanly on mobile`
- `Use $arch-loop rewrite this AGENTS.md file with $agent-linter as a required clean audit`
- `Use $arch-loop every 30 minutes check whether staging.api.internal is reachable and keep fixing infra until it is, max 8 hours`
- `Use $delay-poll every 30 minutes check whether branch blah has been fully pushed; when it is, pull it and integrate it in`
- `Use $wait 1h30m then continue investigating the flaky test`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
- `Use $agent-definition-auditor to audit this AGENTS.md`
- `Use $agents-md-authoring to tighten this AGENTS.md`
- `Use $prompt-authoring to refactor this prompt`
- `Use $skill-authoring to audit this skill package`
- `Use $figma-best-practices to audit this Figma library for Dev Mode and MCP readiness`
- `Use $fal-ai-tools to remove the background from this image with fal.ai`
- `Use $eli10 to explain why this test failed`
- `Use $eli10 to format this decision question`
- `Use $pr-authoring to write and publish a PR for this branch`
- `Use $commit-history-authoring to rewrite this branch's WIP commits into informative branch history`
- `Use $skill-flow to design the authoring and audit flow for this skill suite`
- `Use $amir-publish`
- `Use $code-review on the uncommitted diff`
- `Use $code-review branch-diff --base main --head feature/ingest-fix`
- `Use $code-review paths src/ingest/pipeline.py src/ingest/schema.py`
- `Use $code-review completion-claim docs/MY_PLAN.md 3`
- `Use $thermo-nuclear-code-quality-review on this diff`
