# arch_skill

This repo ships a skills-only arch suite for Codex CLI, Claude Code, and Gemini CLI.

The live skill surface is:

- `arch-step` — the only full-arch execution surface; owns the standalone full-arch workflow, command-level control, compact `status`, and guided `advance`
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

This installs to Codex CLI, Claude Code, and Gemini CLI directories.

To skip Gemini:

```bash
make install NO_GEMINI=1
```

Installed skills:

- Codex:
  - `~/.codex/skills/arch-step/`
  - `~/.codex/skills/arch-mini-plan/`
  - `~/.codex/skills/lilarch/`
  - `~/.codex/skills/bugs-flow/`
  - `~/.codex/skills/goal-loop/`
  - `~/.codex/skills/north-star-investigation/`
  - `~/.codex/skills/arch-flow/`
  - `~/.codex/skills/arch-skills-guide/`
  - `~/.codex/skills/codemagic-builds/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
  - `~/.claude/skills/arch-mini-plan/`
  - `~/.claude/skills/lilarch/`
  - `~/.claude/skills/bugs-flow/`
  - `~/.claude/skills/goal-loop/`
  - `~/.claude/skills/north-star-investigation/`
  - `~/.claude/skills/arch-flow/`
  - `~/.claude/skills/arch-skills-guide/`
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
  - `~/.gemini/skills/arch-mini-plan/`
  - `~/.gemini/skills/lilarch/`
  - `~/.gemini/skills/bugs-flow/`
  - `~/.gemini/skills/goal-loop/`
  - `~/.gemini/skills/north-star-investigation/`
  - `~/.gemini/skills/arch-flow/`
  - `~/.gemini/skills/arch-skills-guide/`

`make install` also removes stale pre-skill command surfaces and removed competing skill packages, so runtime routing stays unambiguous.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface and confirms removed competing skill packages are absent.

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
- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`
- `implement`
- `audit-implementation`
- `status`
- `advance`

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `arch-mini-plan`

Use when the task still needs canonical arch blocks, but the planning should be done in one pass and follow-through should happen later via `arch-step`.

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

- Primary surface: ask the agent to use `arch-step`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `arch-flow`, or `arch-skills-guide`.
- Full-arch execution defaults to `arch-step`.
- Read-only checklist and next-step inspection uses `arch-flow`.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step new "build this"`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step advance docs/MY_PLAN.md RUN=1`
- `Use $arch-mini-plan docs/MY_PLAN.md`
- `Use $lilarch for this small feature`
- `Use $bugs-flow on this Sentry issue`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
