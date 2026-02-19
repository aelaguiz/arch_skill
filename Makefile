.PHONY: install env install_prompts install_templates install_skill claude_install_prompts claude_install_skill gemini_install gemini_install_prompts gemini_install_commands gemini_install_skill generate_gemini_commands verify_install verify_claude_install verify_gemini_install remote_install

ENV_FILE ?= .env
DEFAULT_USERNAME := $(shell whoami)
SKILLS := arch-skill arch-flow codemagic-builds
CLAUDE_SKILLS := arch-skill arch-flow
GEMINI_SKILLS := arch-skill arch-flow

ifeq ($(NO_GEMINI),1)
INSTALL_GEMINI :=
VERIFY_GEMINI :=
else
INSTALL_GEMINI := gemini_install
VERIFY_GEMINI := verify_gemini_install
endif

install: env install_prompts install_templates install_skill claude_install_prompts claude_install_skill $(INSTALL_GEMINI)

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

gemini_install: env gemini_install_prompts gemini_install_commands gemini_install_skill

gemini_install_prompts: env
	mkdir -p ~/.gemini/arch_skill/prompts
	@USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		dst=~/.gemini/arch_skill/prompts/$$(basename $$src); \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$dst"; \
	done

gemini_install_commands:
	@mkdir -p ~/.gemini/commands
	@mkdir -p ~/.gemini/_backup/commands
	@ts=$$(date +%Y%m%d_%H%M%S); \
	if [ -f ~/.gemini/commands/prompts.toml ]; then \
		mv -f ~/.gemini/commands/prompts.toml ~/.gemini/_backup/commands/prompts.toml.$$ts.bak; \
	fi; \
	if [ -d ~/.gemini/commands/prompts ]; then \
		mv -f ~/.gemini/commands/prompts ~/.gemini/_backup/commands/prompts.$$ts; \
	fi
	@# Gemini scans ~/.gemini/commands recursively for *.toml (including dot-dirs). Ensure legacy backups don't keep loading.
	@if [ -d ~/.gemini/commands/_backup ]; then \
		find ~/.gemini/commands/_backup -maxdepth 1 -type f -name '*.toml' -exec sh -c 'for f in "$$@"; do mv -f "$$f" "$$f.bak"; done' _ {} + 2>/dev/null || true; \
	fi
	@tmpdir=$$(mktemp -d); \
	python3 scripts/generate_gemini_commands.py --out-dir "$$tmpdir/prompts"; \
	cp -R "$$tmpdir/prompts" ~/.gemini/commands/prompts; \
	rm -rf "$$tmpdir"

generate_gemini_commands:
	python3 scripts/generate_gemini_commands.py

gemini_install_skill:
	mkdir -p ~/.gemini/skills
	@for skill in $(GEMINI_SKILLS); do \
		rm -rf ~/.gemini/skills/$$skill; \
		cp -R skills/$$skill ~/.gemini/skills/$$skill; \
		f=~/.gemini/skills/$$skill/SKILL.md; \
		tmp=$$f.tmp; \
		awk 'NR==1 && $$0=="---" {front=1; next} front && $$0=="---" {front=0; next} !front {print}' "$$f" > "$$tmp" && mv "$$tmp" "$$f"; \
	done

verify_install: verify_claude_install $(VERIFY_GEMINI)
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

verify_gemini_install:
	@test -f ~/.gemini/commands/prompts/arch-new.toml
	@test -f ~/.gemini/arch_skill/prompts/arch-new.md
	@test -f ~/.gemini/arch_skill/prompts/arch-flow.md
	@test -f ~/.gemini/skills/arch-skill/SKILL.md
	@test -f ~/.gemini/skills/arch-flow/SKILL.md
	@echo "OK: Gemini commands + prompts + skills installed"

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@$(MAKE) --no-print-directory env
	@ssh $(HOST) "mkdir -p ~/.codex/prompts ~/.codex/templates/arch_skill ~/.codex/skills"
	@ssh $(HOST) "mkdir -p ~/.claude/commands/prompts ~/.claude/skills"
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		ssh $(HOST) "mkdir -p ~/.gemini/commands ~/.gemini/arch_skill/prompts ~/.gemini/skills ~/.gemini/_backup/commands"; \
	fi
	@# Keep old names from shadowing new ones (safe: move to backup, no deletes).
	@ssh $(HOST) "mkdir -p ~/.codex/prompts/_backup && for f in arch-impl-audit.md arch-impl-audit-agent.md goal-loop-bootstrap.md; do [ -f ~/.codex/prompts/$$f ] && mv -f ~/.codex/prompts/$$f ~/.codex/prompts/_backup/ || true; done"
	@ssh $(HOST) "mkdir -p ~/.claude/commands/prompts/_backup && [ -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ] && mv -f ~/.claude/commands/prompts/goal-loop-bootstrap.md ~/.claude/commands/prompts/_backup/ || true"
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		ssh $(HOST) "ts=$$(date +%Y%m%d_%H%M%S); if [ -f ~/.gemini/commands/prompts.toml ]; then mv -f ~/.gemini/commands/prompts.toml ~/.gemini/_backup/commands/prompts.toml.$$ts.bak; fi; if [ -d ~/.gemini/commands/prompts ]; then mv -f ~/.gemini/commands/prompts ~/.gemini/_backup/commands/prompts.$$ts; fi"; \
	fi
	@tmpdir=$$(mktemp -d); \
	USERNAME=$$(grep -E '^USERNAME=' "$(ENV_FILE)" | tail -n 1 | cut -d= -f2-); \
	if [ -z "$$USERNAME" ]; then USERNAME="$(DEFAULT_USERNAME)"; fi; \
	ESCAPED_USERNAME=$$(printf '%s' "$$USERNAME" | sed -e 's/[\\/&]/\\&/g'); \
	for src in prompts/*.md; do \
		sed -e "s/USERNAME/$$ESCAPED_USERNAME/g" "$$src" > "$$tmpdir/$$(basename $$src)"; \
	done; \
	scp $$tmpdir/*.md $(HOST):~/.codex/prompts/; \
	scp $$tmpdir/*.md $(HOST):~/.claude/commands/prompts/; \
	if [ "$(NO_GEMINI)" != "1" ]; then scp $$tmpdir/*.md $(HOST):~/.gemini/arch_skill/prompts/; fi; \
	rm -rf "$$tmpdir"
	@scp templates/*.html $(HOST):~/.codex/templates/arch_skill/
	@ssh $(HOST) "rm -rf ~/.codex/skills/arch-skill ~/.codex/skills/arch-flow ~/.codex/skills/codemagic-builds"
	@scp -r skills/arch-skill skills/arch-flow skills/codemagic-builds $(HOST):~/.codex/skills/
	@ssh $(HOST) "rm -rf ~/.claude/skills/arch-skill ~/.claude/skills/arch-flow"
	@scp -r skills/arch-skill skills/arch-flow $(HOST):~/.claude/skills/
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		tmpdir=$$(mktemp -d); \
		python3 scripts/generate_gemini_commands.py --out-dir "$$tmpdir/prompts"; \
		scp -r "$$tmpdir/prompts" $(HOST):~/.gemini/commands/; \
		rm -rf "$$tmpdir"; \
		ssh $(HOST) "rm -rf ~/.gemini/skills/arch-skill ~/.gemini/skills/arch-flow"; \
		scp -r skills/arch-skill skills/arch-flow $(HOST):~/.gemini/skills/; \
		ssh $(HOST) "for skill in $(GEMINI_SKILLS); do f=~/.gemini/skills/$$skill/SKILL.md; tmp=$$f.tmp; awk 'NR==1 && $$0==\"---\" {front=1; next} front && $$0==\"---\" {front=0; next} !front {print}' \"$$f\" > \"$$tmp\" && mv \"$$tmp\" \"$$f\"; done"; \
	fi
