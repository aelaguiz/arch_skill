# arch_skill (Codex CLI prompts)

This repo is a set of **Codex custom prompts** (slash commands) plus a small HTML template used by some prompts.

In addition, it includes an optional **Codex skill** (`arch-skill`) that acts as a router + invariants layer (single SSOT doc, question policy, flow selection). The skill is a **parallel mechanism**: prompts are still installed and used as-is.

## Install

```bash
@channel

git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs:
- Prompts → `~/.codex/prompts/`
- Templates → `~/.codex/templates/arch_skill/`
- Skill (`arch-skill`) → `~/.codex/skills/arch-skill/`

Note: `make install` personalizes prompts by replacing `Amir`/`AMIR` with your local `whoami` username at install time. Override with `make install PROMPT_USER=Amir` (or any name) to keep different wording.

Restart your Codex instance so it reloads the installed prompts/skill.

## Usage

- Start typing `/prompts:` in Codex CLI and pick the command you want (`arch-new`, `arch-mini-plan-agent`, `arch-implement`, etc.).
- Optional: in conversation, you can ask Codex to “use arch-skill” to activate the router + invariants layer (prompts remain the SSOT procedures).
- Shortcut for “run automation on an existing sim/emulator and reopen plan issues if it fails”: `/prompts:arch-qa-autotest`
- Regular flow vs mini flow guide: `docs/arch_skill_usage_guide.md`
