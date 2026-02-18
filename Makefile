.PHONY: install env install_prompts install_templates install_skill claude_install_prompts claude_install_skill verify_install verify_claude_install remote_install

ENV_FILE ?= .env
DEFAULT_USERNAME := $(shell whoami)
SKILLS := arch-skill arch-flow codemagic-builds
CLAUDE_SKILLS := arch-skill arch-flow

install: env install_prompts install_templates install_skill claude_install_prompts claude_install_skill

env:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "USERNAME=$(DEFAULT_USERNAME)" > "$(ENV_FILE)"; \
	fi
	@if ! grep -q '^USERNAME=' "$(ENV_FILE)"; then \
		echo "USERNAME=$(DEFAULT_USERNAME)" >> "$(ENV_FILE)"; \
	fi

install_prompts: env
	mkdir -p ~/.codex/prompts
	@# Keep renamed/deprecated prompt names from lingering (safe: move to backup, no deletes).
	@mkdir -p ~/.codex/prompts/_backup
	@[ -f ~/.codex/prompts/goal-loop-bootstrap.md ] && mv -f ~/.codex/prompts/goal-loop-bootstrap.md ~/.codex/prompts/_backup/ || true
	@USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		dst=~/.codex/prompts/$$(basename $$src); \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$dst"; \
	done

install_templates:
	mkdir -p ~/.codex/templates/arch_skill
	cp templates/*.html ~/.codex/templates/arch_skill/

install_skill:
	mkdir -p ~/.codex/skills
	@for skill in $(SKILLS); do \
		rm -rf ~/.codex/skills/$$skill; \
		cp -R skills/$$skill ~/.codex/skills/$$skill; \
	done

claude_install_prompts: env
	mkdir -p ~/.claude/commands/prompts
	@# Keep renamed/deprecated prompt names from lingering (safe: move to backup, no deletes).
	@mkdir -p ~/.claude/commands/prompts/_backup
	@[ -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ] && mv -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ~/.claude/commands/prompts/_backup/ || true
	@USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		dst=~/.claude/commands/prompts/$$(basename $$src); \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$dst"; \
	done

claude_install_skill:
	mkdir -p ~/.claude/skills
	@for skill in $(CLAUDE_SKILLS); do \
		rm -rf ~/.claude/skills/$$skill; \
		cp -R skills/$$skill ~/.claude/skills/$$skill; \
	done

verify_install: verify_claude_install
	@test -f ~/.codex/prompts/arch-new.md
	@test -f ~/.codex/prompts/arch-flow.md
	@test -f ~/.codex/prompts/lilarch-start.md
	@test -f ~/.codex/prompts/lilarch-plan.md
	@test -f ~/.codex/prompts/lilarch-finish.md
	@test -f ~/.codex/prompts/bugs-analyze.md
	@test -f ~/.codex/prompts/bugs-fix.md
	@test -f ~/.codex/prompts/bugs-review.md
	@test -f ~/.codex/prompts/goal-loop-new.md
	@test -f ~/.codex/prompts/goal-loop-iterate.md
	@test -f ~/.codex/templates/arch_skill/arch_doc_template.html
	@test -f ~/.codex/skills/arch-skill/SKILL.md
	@test -f ~/.codex/skills/arch-flow/SKILL.md
	@test -f ~/.codex/skills/codemagic-builds/SKILL.md
	@echo "OK: Codex prompts + templates + skill installed"

verify_claude_install:
	@test -f ~/.claude/commands/prompts/arch-new.md
	@test -f ~/.claude/commands/prompts/lilarch-start.md
	@test -f ~/.claude/commands/prompts/goal-loop-new.md
	@test -f ~/.claude/skills/arch-skill/SKILL.md
	@test -f ~/.claude/skills/arch-flow/SKILL.md
	@echo "OK: Claude Code prompts + skills installed"

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@$(MAKE) --no-print-directory env
	@ssh $(HOST) "mkdir -p ~/.codex/prompts ~/.codex/templates/arch_skill ~/.codex/skills"
	@ssh $(HOST) "mkdir -p ~/.claude/commands/prompts ~/.claude/skills"
	@# Keep old names from shadowing new ones (safe: move to backup, no deletes).
	@ssh $(HOST) "mkdir -p ~/.codex/prompts/_backup && for f in arch-impl-audit.md arch-impl-audit-agent.md goal-loop-bootstrap.md; do [ -f ~/.codex/prompts/$$f ] && mv -f ~/.codex/prompts/$$f ~/.codex/prompts/_backup/ || true; done"
	@ssh $(HOST) "mkdir -p ~/.claude/commands/prompts/_backup && [ -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ] && mv -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ~/.claude/commands/prompts/_backup/ || true"
	@tmpdir=$$(mktemp -d); \
	USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$tmpdir/$$(basename $$src)"; \
	done; \
	scp $$tmpdir/*.md $(HOST):~/.codex/prompts/; \
	scp $$tmpdir/*.md $(HOST):~/.claude/commands/prompts/; \
	rm -rf "$$tmpdir"
	@scp templates/*.html $(HOST):~/.codex/templates/arch_skill/
	@ssh $(HOST) "rm -rf ~/.codex/skills/arch-skill ~/.codex/skills/arch-flow ~/.codex/skills/codemagic-builds"
	@scp -r skills/arch-skill skills/arch-flow skills/codemagic-builds $(HOST):~/.codex/skills/
	@ssh $(HOST) "rm -rf ~/.claude/skills/arch-skill ~/.claude/skills/arch-flow"
	@scp -r skills/arch-skill skills/arch-flow $(HOST):~/.claude/skills/
