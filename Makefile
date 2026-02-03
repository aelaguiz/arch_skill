.PHONY: install install_prompts install_templates install_skill verify_install remote_install

PROMPT_USER ?= $(shell whoami)

install: install_prompts install_templates install_skill

install_prompts:
	mkdir -p ~/.codex/prompts
	@for src in prompts/*.md; do \
		dst=~/.codex/prompts/$$(basename $$src); \
		sed \
			-e "s/AMIR/$(PROMPT_USER)/g" \
			-e "s/Amir/$(PROMPT_USER)/g" \
			"$$src" > "$$dst"; \
	done

install_templates:
	mkdir -p ~/.codex/templates/arch_skill
	cp templates/*.html ~/.codex/templates/arch_skill/

install_skill:
	mkdir -p ~/.codex/skills
	rm -rf ~/.codex/skills/arch-skill
	cp -R skills/arch-skill ~/.codex/skills/arch-skill

verify_install:
	@test -f ~/.codex/prompts/arch-new.md
	@test -f ~/.codex/templates/arch_skill/arch_doc_template.html
	@test -f ~/.codex/skills/arch-skill/SKILL.md
	@echo "OK: prompts + templates + skill installed"

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@ssh $(HOST) "mkdir -p ~/.codex/prompts ~/.codex/templates/arch_skill ~/.codex/skills"
	@# Keep old names from shadowing new ones (safe: move to backup, no deletes).
	@ssh $(HOST) "mkdir -p ~/.codex/prompts/_backup && for f in arch-impl-audit.md arch-impl-audit-agent.md; do [ -f ~/.codex/prompts/$$f ] && mv -f ~/.codex/prompts/$$f ~/.codex/prompts/_backup/ || true; done"
	@scp prompts/*.md $(HOST):~/.codex/prompts/
	@scp templates/*.html $(HOST):~/.codex/templates/arch_skill/
	@ssh $(HOST) "rm -rf ~/.codex/skills/arch-skill"
	@scp -r skills/arch-skill $(HOST):~/.codex/skills/
