# arch_skill

This repo ships a skills-only arch suite for Codex CLI, Claude Code, and Gemini CLI.

The live skill surface is:

- `arch-step` — the only full-arch execution surface; owns the standalone full-arch workflow, command-level control, bounded `auto-plan` and `implement-loop` controllers, compact `status`, and guided `advance`
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and hook-backed Codex `auto` docs cleanup
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill

`arch-step` is the only full-arch execution surface.

Historical pre-skill materials are archived under `archive/` and `docs/archive/`. They are repo history, not part of the runtime surface.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, wires the Codex runtime support for `auto-plan`, `implement-loop`, and `arch-docs auto` through `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, removes older `~/.codex/skills/<skill>` mirrors from previous installs, and also installs the Claude Code and Gemini CLI skill directories.

Codex automatic `auto-plan`, `implement-loop`, and `arch-docs auto` also require the Codex feature flag:

```bash
codex features enable codex_hooks
```

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
  - `~/.agents/skills/goal-loop/`
  - `~/.agents/skills/north-star-investigation/`
  - `~/.agents/skills/arch-flow/`
  - `~/.agents/skills/arch-skills-guide/`
  - `~/.agents/skills/codemagic-builds/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
  - `~/.claude/skills/arch-docs/`
  - `~/.claude/skills/arch-mini-plan/`
  - `~/.claude/skills/lilarch/`
  - `~/.claude/skills/bugs-flow/`
  - `~/.claude/skills/goal-loop/`
  - `~/.claude/skills/north-star-investigation/`
  - `~/.claude/skills/arch-flow/`
  - `~/.claude/skills/arch-skills-guide/`
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
  - `~/.gemini/skills/arch-docs/`
  - `~/.gemini/skills/arch-mini-plan/`
  - `~/.gemini/skills/lilarch/`
  - `~/.gemini/skills/bugs-flow/`
  - `~/.gemini/skills/goal-loop/`
  - `~/.gemini/skills/north-star-investigation/`
  - `~/.gemini/skills/arch-flow/`
  - `~/.gemini/skills/arch-skills-guide/`

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed competing skill packages, and older `~/.codex/skills/<skill>` mirrors so runtime routing stays unambiguous.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface in `~/.agents/skills/`, checks that the Codex runtime support for `auto-plan`, `implement-loop`, and `arch-docs auto` exists in `~/.codex/hooks.json` and points at the installed runner under `~/.agents/skills/`, confirms the old `~/.codex/skills/<skill>` mirrors are absent, and confirms removed competing skill packages are absent for the supported runtimes.

To confirm the Codex feature gate is enabled:

```bash
codex features list | rg '^codex_hooks\\s+.*\\strue$'
```

Restart your Codex, Claude Code, or Gemini CLI session after install so it reloads skills.

## Skill suite

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
- `review-gate`
- `implement`
- `implement-loop`
- `audit-implementation`
- `status`
- `advance`

`auto-plan` is the Codex-only automatic planning controller. The user-facing command is still just `Use $arch-step auto-plan` or `Use $arch-step auto-plan docs/MY_PLAN.md`. It is real only when the installed Codex runtime support is present in `~/.codex/hooks.json` and `codex_hooks` is enabled. Otherwise it must fail loud instead of pretending prompt-only chaining is enough.

`implement-loop` is the Codex-only automatic bounded delivery controller. The user-facing command is still just `Use $arch-step implement-loop docs/MY_PLAN.md`. It is real only when the installed Codex runtime support is present in `~/.codex/hooks.json` and `codex_hooks` is enabled. Otherwise it must fail loud instead of pretending prompt-only repetition is enough.

After a clean full-arch code audit, the required next move is `Use $arch-docs`, not another `arch-step` command. `arch-step` owns code delivery; `arch-docs` owns the docs-audit cleanup pass and uses the finished arch artifact as context when present.

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `arch-docs`

Use when the job is cleaning up stale, overlapping, or misleading docs and current code truth is stable enough to ground them. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one bounded DGTFO cleanup pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, consolidate each topic to one canonical home, delete stale or duplicate truth, and repair links or nav for the surviving docs.

`arch-docs auto` is the Codex-only hook-backed controller for repeated docs-cleanup passes. The user-facing command is still just `Use $arch-docs auto`. It is real only when the installed Codex runtime support is present in `~/.codex/hooks.json` and `codex_hooks` is enabled. Otherwise it must fail loud instead of pretending prompt-only looping is enough.

### `arch-mini-plan`

Use when the task still needs canonical arch blocks, but the planning should be done in one pass and follow-through should happen later via `arch-step`, then `arch-docs` for later docs cleanup.

### `lilarch`

Use for contained features or improvements that should fit in 1-3 phases.

### `bugs-flow`

Use for Sentry/log-driven bug analysis, narrow fixes, and explicit-review-only follow-up.

### `goal-loop`

Use when the goal is clear but the path is not, and you want a controller doc plus append-only iteration log.

### `north-star-investigation`

Use for quantified investigations where ranked hypotheses and brutal tests are the main job.

### `arch-flow`

Use when the question is "what's next?" on an arch-style doc and you want the single best read-only recommendation.

### `arch-skills-guide`

Use when the question is "which arch skill should I use?" or "what is the difference between these live subskills?"

## Usage

- Primary surface: ask the agent to use `arch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `arch-flow`, or `arch-skills-guide`.
- Full-arch execution defaults to `arch-step`.
- Docs cleanup loops default to `arch-docs`.
- Read-only checklist and next-step inspection uses `arch-flow`.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step new "build this"`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step advance docs/MY_PLAN.md RUN=1`
- `Use $arch-step auto-plan`
- `Use $arch-step implement-loop docs/MY_PLAN.md`
- `Use $arch-docs`
- `Use $arch-docs auto`
- `Use $arch-mini-plan docs/MY_PLAN.md`
- `Use $lilarch for this small feature`
- `Use $bugs-flow on this Sentry issue`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
