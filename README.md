# arch_skill (Codex CLI prompts)

This repo is a set of **Codex CLI custom prompts** (slash commands) plus a small HTML template used by some prompts.

You don’t use this repo “inside your codebase” as a skill — you install the prompts into Codex so they show up as `/prompts:*`.

## Install

```bash
@channel

git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

Restart your Codex instance so it reloads the installed prompts.

## Usage

- Start typing `/prompts:` in Codex CLI and pick the command you want (`arch-new`, `arch-mini-plan-agent`, `arch-implement`, etc.).
- Shortcut for “run automation on an existing sim/emulator and reopen plan issues if it fails”: `/prompts:arch-qa-autotest`
- Regular flow vs mini flow guide: `docs/arch_skill_usage_guide.md`
