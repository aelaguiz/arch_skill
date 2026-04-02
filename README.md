# arch_skill (skills first; legacy prompts included)

This repo now ships a **skill suite** for **Codex CLI**, **Claude Code**, and **Gemini CLI**, plus the legacy prompt catalog and a small HTML template used by some prompts.

The primary skill surface is:

- `arch-plan` — full research, deep dive, external research, phase plan, local implementation, and implementation audit
- `arch-step` — explicit standalone full-arch step operator with command-level control, compact `status`, and guided `advance`
- `arch-mini-plan` — one-pass mini architecture planning
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right subskill

Prompts are still installed for legacy or non-skill use, but the new skills do not depend on saved prompts at runtime.
For Codex specifically, default installs now remove this repo's legacy prompts from `~/.codex/prompts/` and install only the skill suite plus templates.

## Compatibility

| Tool | Prompts | Skills | Templates |
| --- | --- | --- | --- |
| **Codex CLI** | `~/.codex/prompts/` | `~/.codex/skills/` | `~/.codex/templates/` |
| **Claude Code** | `~/.claude/commands/prompts/` | `~/.claude/skills/` | (not applicable) |
| **Gemini CLI** | `~/.gemini/arch_skill/prompts/` | `~/.gemini/skills/` | (not applicable) |

All tools discover prompts as `/prompts:<name>` slash commands after install.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs to **Codex CLI**, **Claude Code**, and **Gemini CLI** directories.

To skip Gemini (leave existing behavior unchanged):

```bash
make install NO_GEMINI=1
```

**Codex CLI:**
- Prompts → not installed by default; existing arch_skill prompts are moved to `~/.codex/prompts/_backup/`
- Templates → `~/.codex/templates/arch_skill/`
- Skills → `~/.codex/skills/arch-plan/`, `arch-step/`, `arch-mini-plan/`, `lilarch/`, `bugs-flow/`, `goal-loop/`, `north-star-investigation/`, `arch-flow/`, `arch-skills-guide/`, `codemagic-builds/`

**Claude Code:**
- Prompts → `~/.claude/commands/prompts/`
- Skills → `~/.claude/skills/arch-plan/`, `arch-step/`, `arch-mini-plan/`, `lilarch/`, `bugs-flow/`, `goal-loop/`, `north-star-investigation/`, `arch-flow/`, `arch-skills-guide/`

**Gemini CLI:**
- Commands → `~/.gemini/commands/prompts/*.toml` (invoked as `/prompts:<name>`)
- Prompts → `~/.gemini/arch_skill/prompts/`
- Skills → `~/.gemini/skills/arch-plan/`, `arch-step/`, `arch-mini-plan/`, `lilarch/`, `bugs-flow/`, `goal-loop/`, `north-star-investigation/`, `arch-flow/`, `arch-skills-guide/`

Note: prompts use a `USERNAME` placeholder. `make install` creates a `.env` file (if missing), ensures it contains `USERNAME=<whoami>`, then substitutes that value into the installed prompts. Edit `.env` to override.

Gemini CLI note: `make install` generates per-command `.toml` files for Gemini using `python3`.

### Remote install

```bash
make remote_install HOST=user@host
```

Installs prompts + skills to Codex + Claude Code + Gemini CLI directories on the remote host via SSH/SCP.

### Verify

```bash
make verify_install
```

Checks that Codex is using the skill-only install path and that Claude Code and Gemini still have the expected prompt and skill files.

Restart your Codex/Claude Code/Gemini CLI instance so it reloads the installed prompts/skills.

## Skill suite

The split plan and prompt-coverage mapping live in `docs/ARCH_SKILL_SUITE_SPLIT_PLAN_2026-03-30.md`.

### `arch-plan`
Use for the full arch workflow: real architecture planning, research grounding, deep dives, external research, phased plans, local implementation, and implementation audits.

### `arch-step`
Use when you want literal command-level control over one canonical full-arch plan doc: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, `implement`, `audit-implementation`, `status`, and `advance`. `status` stays compact; `advance` owns the full checklist and optional one-step execution.

### `arch-mini-plan`
Use when you want the one-pass "mini plan" version of arch: canonical blocks in one pass, without running the whole multi-step arch flow.

### `lilarch`
Use for small features or improvements that should fit in 1-3 phases.

### `bugs-flow`
Use for Sentry/log-driven bug analysis, minimal localized fixes, verification, and explicit-review-only follow-up.

### `goal-loop`
Use when the goal is clear but the path is not, and you want an SSOT controller doc plus append-only iteration log.

### `north-star-investigation`
Use for quant-heavy investigations where ranked hypotheses and fastest-learning brutal tests are the main job.

### `arch-flow`
Use when the question is "what's next?" on an arch or lilarch doc and you want the single best next move.

### `arch-skills-guide`
Use when the question is "which arch skill should I use?" or "what is the difference between these subskills?"

## Legacy prompt families

The prompt pack is still in `prompts/` for legacy use and for surfaces that still want slash commands.

### Architecture planning flow (`arch-*`)
The core prompt family for structured architecture planning + execution. Supports a regular flow (multi-prompt, phase-gated) and a mini flow (one-pass planning for small tasks). Key prompts:

- `/prompts:arch-new` — create a new canonical plan doc
- `/prompts:arch-mini-plan-agent` — one-pass research + deep dive + phase plan
- `/prompts:arch-phase-plan-granularize` — optional: rewrite the Phase Plan into micro-phases + microtasks (single SSOT; good for smaller/dumber coding agents)
- `/prompts:arch-overbuild-protector` — optional: scope triage to prevent overbuild; move scope creep to intentional follow-ups
- `/prompts:arch-implement` / `arch-implement-agent` — ship the plan end-to-end
- `/prompts:arch-fold-in` — fold reference docs/links into phases (high leverage when you have specs)
- `/prompts:arch-audit-implementation` — strict "is code actually complete vs plan?" audit
- `/prompts:arch-codereview` / `arch-open-pr` — on-demand review + PR finalization

### Mini-arch flow (`lilarch-*`)
A **tiny** version of the arch flow intended for **small features or improvements** that can ship in **1–3 phases**. It compresses “new + research”, “plan + audit”, and “implement + self-audit” into three prompts:

- `/prompts:lilarch-start` — create/repair a compact plan doc: North Star + requirements + minimal grounding (optional external best practices)
- `/prompts:lilarch-plan` — deep dive + 1–3 phase plan + internal plan audit + optional self-review (write back to DOC_PATH)
- `/prompts:lilarch-finish` — implement + self-audit (write back to DOC_PATH + worklog)

If the work expands beyond 3 phases, the prompts warn and recommend switching to the full `arch-*` flow (or `bugs-*` if investigation dominates).

### Goal-seeking loops (`goal-loop-*`)
Autonomous iteration loops for open-ended goals (optimization, investigation, metric improvement). Instead of a fixed plan, you define a North Star and iterate with bets:

- `/prompts:goal-loop-new` — create/repair the Goal Loop SSOT doc + append-only running log
- `/prompts:goal-loop-iterate` — execute ONE bet, append to the running log, compound learning
- `/prompts:goal-loop-flow` — check readiness, recommend the single best next step
- `/prompts:goal-loop-context-load` — write Context Digest so restarts don't redo work

**When to use goal loops vs arch flow:** Use arch flow when you know _what_ to build and need structured planning. Use goal loops when you're exploring, optimizing, or investigating — the goal is clear but the path isn't.

### Bug workflow (`bugs-*`)
Structured bug analysis + fix cycle: `/prompts:bugs-analyze` → `/prompts:bugs-fix` → `/prompts:bugs-review`.

### North Star investigation (`north-star-investigation-*`)
Deep investigation for optimization or root-cause analysis. Commander's Intent style: bootstrap an investigation doc, then iterate with hypothesis-driven brutal tests.

- `/prompts:north-star-investigation-bootstrap` — create the investigation doc
- `/prompts:north-star-investigation-loop` — iterate: hypothesize, test, learn, refine

### Other families
- **Debug:** `arch-debug`, `arch-debug-brutal`
- **Rendering:** `arch-html-full`, `arch-ascii`, `arch-ui-ascii`
- **Maestro/QA:** `maestro-autopilot`, `maestro-rerun-last`, `maestro-kill`, `qa-autopilot`
- **Ralph:** `arch-ralph-retarget`, `arch-ralph-enhance`
- **DevX:** `arch-devx`, `arch-devx-agent`
- **Misc:** `new-arch-from-docs`

## Usage

- Primary surface: ask the agent to use `arch-plan`, `arch-step`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `arch-flow`, or `arch-skills-guide`.
- Explicit standalone full-arch surface via `arch-step`:
  - `Use $arch-step new "do this"`
  - `Use $arch-step reformat docs/OLD_PLAN.md`
  - `Use $arch-step research docs/MY_PLAN.md`
  - `Use $arch-step deep-dive docs/MY_PLAN.md`
  - `Use $arch-step external-research docs/MY_PLAN.md`
  - `Use $arch-step phase-plan docs/MY_PLAN.md`
  - `Use $arch-step plan-enhance docs/MY_PLAN.md`
  - `Use $arch-step fold-in docs/MY_PLAN.md docs/spec.md docs/ux.md`
  - `Use $arch-step overbuild-protector docs/MY_PLAN.md MODE=report`
  - `Use $arch-step review-gate docs/MY_PLAN.md`
  - `Use $arch-step implement docs/MY_PLAN.md`
  - `Use $arch-step audit-implementation docs/MY_PLAN.md`
  - `Use $arch-step status docs/MY_PLAN.md`
  - `Use $arch-step advance docs/MY_PLAN.md`
  - `Use $arch-step advance docs/MY_PLAN.md RUN=1`
- Legacy surface: start typing `/prompts:` in Claude Code or Gemini CLI and pick the command you want.
- Codex intentionally uses the skill suite only by default.
- Optional (high leverage when you have specs/design docs you don't want missed): `/prompts:arch-fold-in`
  - Example: `/prompts:arch-fold-in docs/MY_PLAN.md docs/spec.md docs/ux_notes.md https://… "Fold these in; Phase 2 must obey the UX contract."`
- Optional (when you want microtasks without creating a second checklist): `/prompts:arch-phase-plan-granularize docs/MY_PLAN.md LEVEL=2`
- Sentry top-problems triage (client + server): `/prompts:sentry-triage`
- Shortcut for "run automation on an existing sim/emulator and reopen plan issues if it fails": `/prompts:arch-qa-autotest`
- Skill-suite split and prompt coverage: `docs/ARCH_SKILL_SUITE_SPLIT_PLAN_2026-03-30.md`
- Regular flow vs mini flow guide: `docs/arch_skill_usage_guide.md`

## Known limitations (Gemini CLI)

Some prompts assume Codex CLI is installed/configured and will reference Codex-specific paths or commands (for example, `~/.codex/templates/...` or `codex exec`). Gemini CLI can still *invoke* these prompts, but running them end-to-end may require Codex CLI to be installed as a dependency.
