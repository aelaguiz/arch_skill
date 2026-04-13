# arch_skill

This repo ships installable agent skills centered on the arch suite for Codex CLI, Claude Code, and Gemini CLI.

The live arch suite is:

- `arch-step` — the only full-arch execution surface; owns the standalone full-arch workflow, command-level control, bounded `auto-plan` and `implement-loop` controllers, compact `status`, and guided `advance`
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and hook-backed Codex `auto` docs cleanup
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `audit-loop` — exhaustive map-first repo audit loop with a root audit ledger and Codex-only `auto` continuation
- `comment-loop` — exhaustive map-first repo comment hardening loop with a root comment ledger and Codex-only `auto` continuation
- `audit-loop-sim` — exhaustive map-first real-app automation audit loop with a root simulator ledger and Codex-only `auto` continuation
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill

`arch-step` is the only full-arch execution surface.

Other shipped skills are:

- `delay-poll` — Codex-only delay-and-check controller that waits inside the installed `Stop` hook, re-runs a read-only condition check on a fixed interval, and resumes the same thread when the condition becomes true
- `agent-definition-auditor` — cold-reader scoring and findings for `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompts, and other agent-definition markdown
- `codemagic-builds` — Codemagic CI/CD build monitoring and build control via the Codemagic REST API

Historical pre-skill materials are archived under `archive/` and `docs/archive/`. They are repo history, not part of the runtime surface.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, writes one arch_skill-managed Codex `Stop` hook in `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, repairs older two-hook arch_skill installs down to that one repo-managed entry, removes older `~/.codex/skills/<skill>` mirrors from previous installs, and also installs the Claude Code and Gemini CLI skill directories.

Codex automatic `auto-plan`, `implement-loop`, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, and `delay-poll` also require the Codex feature flag:

```bash
codex features enable codex_hooks
```

For any of those Codex auto controllers, do not run the Stop hook yourself. After the controller is armed, just end the turn and let Codex run the installed Stop hook.

Each Codex auto controller now uses a session-scoped repo-local state file such as
`.codex/auto-plan-state.<SESSION_ID>.json`, `.codex/audit-loop-state.<SESSION_ID>.json`, `.codex/comment-loop-state.<SESSION_ID>.json`, `.codex/audit-loop-sim-state.<SESSION_ID>.json`, or `.codex/delay-poll-state.<SESSION_ID>.json`,
where `<SESSION_ID>` is the current `CODEX_THREAD_ID`. Separate Codex sessions can
run their own auto controllers concurrently in one repo. One session still must not
arm more than one controller at once.

To skip Gemini:

```bash
make install NO_GEMINI=1
```

Installed skills:

- Default local path:
  - `~/.agents/skills/arch-step/`
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
  - `~/.agents/skills/delay-poll/`
  - `~/.agents/skills/agent-definition-auditor/`
  - `~/.agents/skills/codemagic-builds/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
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
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
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

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed competing skill packages, and older `~/.codex/skills/<skill>` mirrors so runtime routing stays unambiguous.

`delay-poll` is installed only on the agents/Codex surface because it depends on the Codex `Stop` hook runtime and is not a real feature on Claude Code or Gemini CLI.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface in `~/.agents/skills/`, checks that exactly one arch_skill-managed Codex `Stop` hook exists in `~/.codex/hooks.json` and points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, confirms the old `~/.codex/skills/<skill>` mirrors are absent, and confirms removed competing skill packages are absent for the supported runtimes.

To confirm the Codex feature gate is enabled:

```bash
codex features list | rg '^codex_hooks\\s+.*\\strue$'
```

Restart your Codex, Claude Code, or Gemini CLI session after install so it reloads skills.

## Shipped skills

### `arch-step`

Use `arch-step` for real full-arch work. It owns the standalone full-arch workflow, including:

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

`auto-plan` is the Codex-only automatic planning controller. The user-facing command is still just `Use $arch-step auto-plan` or `Use $arch-step auto-plan docs/MY_PLAN.md`. In Codex, the parent `auto-plan` pass runs only `research`, then ends its turn; the installed Stop hook feeds one later planning command per turn through `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`, then owns the successful `implement-loop` handoff. That handoff is allowed only when the artifact is decision-complete. If any unresolved plan-shaping decision remains, `auto-plan` must stop, clear controller state, and ask the user the exact blocker question. It is real only when `~/.codex/hooks.json` contains the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` and `codex_hooks` is enabled. Preflight must verify that `hooks.json` entry and runner path, not a copied hook file under `~/.codex/hooks/`. Otherwise it must fail loud instead of pretending prompt-only chaining is enough.

`arch-step` does not have authority to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, the skill must ask the user instead of guessing.

`implement-loop` is the Codex-only automatic bounded delivery controller. `auto-implement` is an exact user-facing synonym for the same controller. The user-facing command is `Use $arch-step implement-loop docs/MY_PLAN.md` or `Use $arch-step auto-implement docs/MY_PLAN.md`. It is real only when `~/.codex/hooks.json` contains the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` and `codex_hooks` is enabled. Preflight must verify that `hooks.json` entry and runner path, not a copied hook file under `~/.codex/hooks/`. Otherwise it must fail loud instead of pretending prompt-only repetition is enough.

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `arch-docs`

Use when the job is leaving repo docs healthier: cleaning up stale, overlapping, misleading, or obviously dated docs, updating stale survivors, clarifying confusing docs, and promoting grounded missing truth into evergreen docs. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one grounded DGTFO docs-health pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, use git history when staleness or datedness matters, consolidate each topic to one canonical home, update stale surviving docs, clarify confusing docs, add grounded evergreen docs when the repo clearly lacks a viable home, delete stale, duplicate, or dated one-off truth, and repair links or nav for the surviving docs.

`arch-docs auto` is the Codex-only hook-backed controller for repeated docs-cleanup passes. The user-facing command is still just `Use $arch-docs auto`. It is real only when `~/.codex/hooks.json` contains the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` and `codex_hooks` is enabled. Otherwise it must fail loud instead of pretending prompt-only looping is enough.

For any of these Codex auto controllers, do not run the Stop hook yourself. After the controller is armed, just end the turn and let Codex run the installed Stop hook.

### `arch-mini-plan`

Use when the task still needs canonical arch blocks, but the planning should be done in one pass and follow-through should happen later via `arch-step`, then `arch-docs` for later docs cleanup.

### `lilarch`

Use for contained features or improvements that should fit in 1-3 phases.

### `bugs-flow`

Use for Sentry/log-driven bug analysis, narrow fixes, and explicit-review-only follow-up.

### `audit-loop`

Use for repo-wide audit passes where the agent should exhaustively map the codebase and current proof surface before editing, then rank and attack the biggest real unresolved risks by consequence instead of picking something convenient.

### `comment-loop`

Use for repo-wide code comment hardening passes where the agent should exhaustively map the repo, current proof surface, and current explanatory coverage before editing, then rank and attack the biggest shared explanation gaps around contracts, conventions, gotchas, and subtle behavior instead of writing narration wherever it feels helpful.

### `audit-loop-sim`

Use for repo-wide real-app automation passes where the agent should exhaustively map the app, journeys, and current automation surface before editing, then rank and attack the biggest unresolved automation risks by consequence instead of cashing out on tiny safe test tweaks.

### `delay-poll`

Use when the user wants Codex to wait on some external condition, re-check it every 30 minutes, every hour, or similar, and continue the same visible thread only after that condition becomes true.

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

## Usage

- Primary surface: ask the agent to use `arch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `delay-poll`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, or `agent-definition-auditor`.
- Full-arch execution defaults to `arch-step`.
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
- `Use $delay-poll every 30 minutes check whether branch blah has been fully pushed; when it is, pull it and integrate it in`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
- `Use $agent-definition-auditor to audit this AGENTS.md`
