.PHONY: install env install_prompts install_templates install_skill verify_install remote_install

ENV_FILE ?= .env
DEFAULT_USERNAME := $(shell whoami)
SKILLS := arch-skill arch-flow

install: env install_prompts install_templates install_skill

env:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "USERNAME=$(DEFAULT_USERNAME)" > "$(ENV_FILE)"; \
	fi
	@if ! grep -q '^USERNAME=' "$(ENV_FILE)"; then \
		echo "USERNAME=$(DEFAULT_USERNAME)" >> "$(ENV_FILE)"; \
	fi

install_prompts: env
	mkdir -p ~/.codex/prompts
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

verify_install:
	@test -f ~/.codex/prompts/arch-new.md
	@test -f ~/.codex/prompts/arch-flow.md
	@test -f ~/.codex/templates/arch_skill/arch_doc_template.html
	@test -f ~/.codex/skills/arch-skill/SKILL.md
	@test -f ~/.codex/skills/arch-flow/SKILL.md
	@echo "OK: prompts + templates + skill installed"

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@$(MAKE) --no-print-directory env
	@ssh $(HOST) "mkdir -p ~/.codex/prompts ~/.codex/templates/arch_skill ~/.codex/skills"
	@# Keep old names from shadowing new ones (safe: move to backup, no deletes).
	@ssh $(HOST) "mkdir -p ~/.codex/prompts/_backup && for f in arch-impl-audit.md arch-impl-audit-agent.md; do [ -f ~/.codex/prompts/$$f ] && mv -f ~/.codex/prompts/$$f ~/.codex/prompts/_backup/ || true; done"
	@tmpdir=$$(mktemp -d); \
	USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$tmpdir/$$(basename $$src)"; \
	done; \
	scp $$tmpdir/*.md $(HOST):~/.codex/prompts/; \
	rm -rf "$$tmpdir"
	@scp templates/*.html $(HOST):~/.codex/templates/arch_skill/
	@ssh $(HOST) "rm -rf ~/.codex/skills/arch-skill ~/.codex/skills/arch-flow"
	@scp -r skills/arch-skill skills/arch-flow $(HOST):~/.codex/skills/
