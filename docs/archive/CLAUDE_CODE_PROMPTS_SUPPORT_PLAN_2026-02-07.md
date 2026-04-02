---
title: "arch_skill — Claude Code Prompt Support (Install + Parity) — Plan"
date: 2026-02-07
status: draft
owners: ["Amir Elaguizy", "Codex"]
reviewers: ["Amir Elaguizy"]
doc_type: phased_refactor
related:
  # Our installer + prompt sources
  - Makefile
  - prompts/
  - skills/arch-skill/SKILL.md
  - docs/suggested_custom_prompts.md
  - docs/GOAL_SEEKING_LOOP_PROMPTS_PROPOSAL_2026-02-07.md
  # Claude Code docs (external research; keep links stable)
  - https://code.claude.com/docs/advanced-usage/custom-slash-commands
  - https://code.claude.com/docs/advanced-usage/skills
  - https://docs.anthropic.com/en/docs/claude-code/slash-commands
---

# TL;DR

- **Outcome:** arch_skill prompts are usable in **Claude Code** (in addition to Codex) with the *same command names* (e.g. `/prompts:arch-new`, `/prompts:goal-loop-new`) by installing them into Claude Code’s custom command directory structure.
- **Problem:** `make install` currently only installs to **Codex** locations (`~/.codex/prompts`, `~/.codex/skills`, templates). Claude Code won’t see these prompts unless we also install them into Claude’s expected directories.
- **Approach:** Treat Claude Code support as an **install target + format compatibility** problem:
  1) install our prompt `.md` files into `~/.claude/commands/prompts/` so they surface in Claude as `/prompts:<name>` commands,
  2) keep prompt bodies single-source-of-truth in this repo (`prompts/*.md`) and copy them into both tools (idempotent install),
  3) optionally add a Claude “skill” wrapper later, but get parity via commands first (fast win).
- **Plan:** Add `make claude_install` + `make claude_remote_install` + `make verify_claude_install` (idempotent), then harden prompt metadata compatibility, then update `skills/arch-skill/SKILL.md` to list **all prompts** (including the new goal-loop ones).
- **Non-negotiables:**
  - No second SSOT for prompt bodies (repo `prompts/` stays canonical).
  - Install steps must be idempotent and avoid leaving stale names shadowing new ones.
  - Goal-loop prompts must remain **running-log-first** (restart safety) in both tools.

---

# 0) Research Grounding (what Claude Code expects)

## 0.1 How Claude Code stores “saved prompts”

Claude Code uses **custom slash commands** stored as Markdown files on disk:
- **Project scope:** `.claude/commands/` (inside the repo)
- **Personal scope:** `~/.claude/commands/` (user home)

Claude Code supports **namespacing via subdirectories**:
- Example from docs: `.claude/commands/git/status.md` becomes `/git:status`.

Source:
- `custom-slash-commands` docs: https://code.claude.com/docs/advanced-usage/custom-slash-commands
- Anthropic docs (slash commands): https://docs.anthropic.com/en/docs/claude-code/slash-commands

## 0.2 Skills vs commands (forward-compat)

Claude Code “skills” exist at:
- **Personal skills:** `~/.claude/skills/<skill-name>/SKILL.md`
- **Project skills:** `.claude/skills/<skill-name>/SKILL.md`

Docs note: custom slash commands have been merged into skills, but `.claude/commands/` continues to work.

Source:
- Skills docs: https://code.claude.com/docs/advanced-usage/skills

---

# 1) Current State (in this repo)

## 1.1 What `make install` does today

From `Makefile`:
- Copies `prompts/*.md` to `~/.codex/prompts/` (with `USERNAME` substitution)
- Copies `templates/*.html` to `~/.codex/templates/arch_skill/`
- Copies `skills/<skill>/` directories to `~/.codex/skills/`

There is **no Claude Code install step** today.

## 1.2 Prompt naming constraint

We already rely on a stable invocation namespace: `/prompts:<name>`.

That is great for Claude Code, because we can install to:
- `~/.claude/commands/prompts/<name>.md`

…which should surface the same command name:
- `/prompts:<name>`

This avoids rewriting prompt bodies or “dual command name” drift.

---

# 2) Target Behavior (North Star)

## 2.1 The claim (falsifiable)
> If we add Claude Code install targets that copy our canonical `prompts/*.md` into `~/.claude/commands/prompts/` (and optionally `.claude/commands/prompts/` for project-local installs), then Claude Code will surface our full prompt suite as slash commands with the same names we use in Codex (e.g. `/prompts:arch-new`, `/prompts:goal-loop-new`) and we can execute the same prompt-driven workflows in either tool without rewriting instructions.

## 2.2 Definition of done (acceptance evidence)
- Local:
  - `make install` continues to work for Codex.
  - `make claude_install` installs prompts to `~/.claude/commands/prompts/`.
  - In Claude Code, typing `/prompts:` shows our commands with descriptions.
- Remote:
  - `make claude_remote_install HOST=<...>` installs prompts to `<HOST>:~/.claude/commands/prompts/`.
- No drift:
  - Prompt bodies remain SSOT in this repo.
  - Install is idempotent (re-running does not accumulate stale duplicates).

---

# 3) Proposed Implementation Plan

## Phase 1 — Fast win: install prompts into Claude’s command dir

Add Makefile targets (do not change prompt bodies yet):
- `claude_install_prompts`
  - Create `~/.claude/commands/prompts/`
  - Copy all `prompts/*.md` to that directory
  - Apply the same `USERNAME` substitution we use for Codex installs
  - Keep renamed/deprecated files from lingering (move to backup, no deletes)
- `claude_install` meta-target
  - Runs `claude_install_prompts`
- `verify_claude_install`
  - Check that a small set of critical prompts exist at `~/.claude/commands/prompts/`
  - At minimum:
    - `arch-new.md`
    - `arch-implement.md`
    - `goal-loop-new.md`
    - `goal-loop-iterate.md`
- `claude_remote_install HOST=...`
  - Mirror `remote_install` behavior:
    - create dirs on host
    - copy prompt files
    - backup deprecated names

Why this is the first win:
- It makes the **same command names** work in Claude Code without rewriting a single prompt.
- It keeps our “prompt bodies are SSOT” invariant.

## Phase 2 — Metadata hardening for Claude UX

Claude’s docs emphasize `description` frontmatter for discoverability.

Audit:
- Ensure every prompt intended as a slash command begins with YAML frontmatter and includes:
  - `description: ...`
  - (optional) keep `argument-hint:`; unknown keys should be ignored safely.

Concrete repo action:
- Add minimal YAML frontmatter to the two prompt files that currently lack it:
  - `prompts/north-star-investigation-bootstrap.md`
  - `prompts/north-star-investigation-loop.md`

## Phase 3 — “List all prompts” in `skills/arch-skill/SKILL.md`

Goal:
- Make `skills/arch-skill/SKILL.md` a complete, reviewable inventory of the prompt suite (including goal-loop prompts).

Approach options:
1) Manual list (simple; higher maintenance):
   - Add a “Full Prompt Catalog” table listing:
     - command name
     - purpose (1 line)
     - typical args
2) Auto-generated list (preferred; lower maintenance):
   - Add a small script that reads `prompts/*.md`, extracts frontmatter `description`, and rewrites a marked block in `skills/arch-skill/SKILL.md`.
   - This keeps the list accurate as new prompts are added.

Non-negotiable:
- The list must include the new goal-loop prompts:
  - `/prompts:goal-loop-new`
  - `/prompts:goal-loop-iterate`
  - `/prompts:goal-loop-flow`
  - `/prompts:goal-loop-context-load`

## Phase 4 — Optional: project-local `.claude/commands/prompts/`

Depending on how we want to use Claude Code:
- If we want these prompts available *only in specific repos*, we can support a “project install” mode:
  - `make claude_project_install ROOT=<repoRoot>`
  - copies into `<repoRoot>/.claude/commands/prompts/`

Tradeoff:
- Personal install is easiest (one-time setup).
- Project install is safer (per-repo explicitness) but more steps.

---

# 4) Risks / Open Questions (call out now; fix in Phase 2)

## 4.1 Will Claude Code accept our existing frontmatter fields?
Hypothesis: yes — unknown keys are ignored, `description` is used.
Mitigation: keep `description` present everywhere; avoid relying on `argument-hint` semantics.

## 4.2 Tool-specific assumptions inside prompt bodies
Example:
- `prompts/arch-html-full.md` references `~/.codex/templates/arch_skill/arch_doc_template.html`.

Options:
1) Document as “Codex-only” and accept partial parity in Claude Code.
2) Add a template install for Claude (e.g. `~/.claude/templates/arch_skill/`) and update the prompt to search both locations.

Recommendation:
- Start with (1) for velocity; handle (2) only if it’s a recurring need.

## 4.3 Collision risk for `/prompts:*`
Using the `prompts/` namespace in Claude is intentional (directory namespace → command prefix).
It should not collide with built-ins, but we should verify in practice after implementation.

---

# 5) Proposed user workflow (once implemented)

One-time setup:
1) `make install` (Codex)
2) `make claude_install` (Claude)

Day-to-day usage in either tool:
- Use the same command names:
  - `/prompts:arch-new ...`
  - `/prompts:arch-implement docs/<...>.md`
  - `/prompts:goal-loop-new ...`
  - `/prompts:goal-loop-iterate docs/<...>.md`

The goal-loop system remains running-log-first:
- Worklog lives next to doc as `<DOC_BASENAME>_WORKLOG.md`.
- Iteration prompts always read the worklog before acting.

