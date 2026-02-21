# arch_skill (Codex CLI + Claude Code + Gemini CLI prompts)

This repo is a set of **custom prompts** (slash commands) for **Codex CLI**, **Claude Code**, and **Gemini CLI**, plus a small HTML template used by some prompts.

In addition, it includes an optional **skill** (`arch-skill`) that acts as a router + invariants layer (single SSOT doc, question policy, flow selection). The skill is a **parallel mechanism**: prompts are still installed and used as-is.

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
- Prompts → `~/.codex/prompts/`
- Templates → `~/.codex/templates/arch_skill/`
- Skills → `~/.codex/skills/arch-skill/`, `~/.codex/skills/arch-flow/`, `~/.codex/skills/codemagic-builds/`

**Claude Code:**
- Prompts → `~/.claude/commands/prompts/`
- Skills → `~/.claude/skills/arch-skill/`, `~/.claude/skills/arch-flow/`

**Gemini CLI:**
- Commands → `~/.gemini/commands/prompts/*.toml` (invoked as `/prompts:<name>`)
- Prompts → `~/.gemini/arch_skill/prompts/`
- Skills → `~/.gemini/skills/arch-skill/`, `~/.gemini/skills/arch-flow/`

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

Checks that key files are in place for Codex CLI, Claude Code, and Gemini CLI.

Restart your Codex/Claude Code/Gemini CLI instance so it reloads the installed prompts/skills.

## Prompt families (60 prompts)

The full catalog is in `skills/arch-skill/SKILL.md` and `skills/arch-skill/resources/PROMPT_INDEX.md`.

### Architecture planning flow (`arch-*`)
The core prompt family for structured architecture planning + execution. Supports a regular flow (multi-prompt, phase-gated) and a mini flow (one-pass planning for small tasks). Key prompts:

- `/prompts:arch-new` — create a new canonical plan doc
- `/prompts:arch-mini-plan-agent` — one-pass research + deep dive + phase plan
- `/prompts:arch-phase-plan-granularize` — optional: rewrite the Phase Plan into micro-phases + microtasks (single SSOT; good for smaller/dumber coding agents)
- `/prompts:arch-overbuild-protector` — optional: scope triage to prevent overbuild; move scope creep to intentional follow-ups
- `/prompts:arch-implement` / `arch-implement-agent` — ship the plan end-to-end
- `/prompts:arch-fold-in` — fold reference docs/links into phases (high leverage when you have specs)
- `/prompts:arch-audit-implementation` — strict "is code actually complete vs plan?" audit
- `/prompts:arch-codereview` / `arch-open-pr` — external review + PR finalization

### Mini-arch flow (`lilarch-*`)
A **tiny** version of the arch flow intended for **small features or improvements** that can ship in **1–3 phases**. It compresses “new + research”, “plan + audits”, and “implement + review” into three prompts:

- `/prompts:lilarch-start` — create/repair a compact plan doc: North Star + requirements + minimal grounding (optional external best practices)
- `/prompts:lilarch-plan` — deep dive + 1–3 phase plan + internal plan audit + external plan audit (write back to DOC_PATH)
- `/prompts:lilarch-finish` — implement + self-audit + external code review (write back to DOC_PATH + worklog)

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

- Start typing `/prompts:` in Codex CLI, Claude Code, or Gemini CLI and pick the command you want.
- Optional: in conversation, you can ask the agent to "use arch-skill" to activate the router + invariants layer (prompts remain the SSOT procedures).
- Optional (high leverage when you have specs/design docs you don't want missed): `/prompts:arch-fold-in`
  - Example: `/prompts:arch-fold-in docs/MY_PLAN.md docs/spec.md docs/ux_notes.md https://… "Fold these in; Phase 2 must obey the UX contract."`
- Optional (when you want microtasks without creating a second checklist): `/prompts:arch-phase-plan-granularize docs/MY_PLAN.md LEVEL=2`
- Sentry top-problems triage (client + server): `/prompts:sentry-triage`
- Shortcut for "run automation on an existing sim/emulator and reopen plan issues if it fails": `/prompts:arch-qa-autotest`
- Regular flow vs mini flow guide: `docs/arch_skill_usage_guide.md`

## Known limitations (Gemini CLI)

Some prompts assume Codex CLI is installed/configured and will reference Codex-specific paths or commands (for example, `~/.codex/templates/...` or `codex exec`). Gemini CLI can still *invoke* these prompts, but running them end-to-end may require Codex CLI to be installed as a dependency.
