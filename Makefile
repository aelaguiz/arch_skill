.PHONY: install install_skill claude_install_skill gemini_install gemini_install_skill verify_install verify_claude_install verify_gemini_install remote_install clean_codex_stale_surfaces clean_claude_stale_surfaces clean_gemini_stale_surfaces

REMOVED_SKILLS := arch-skill arch-plan
SKILLS := arch-step arch-mini-plan lilarch bugs-flow goal-loop north-star-investigation arch-flow arch-skills-guide codemagic-builds
CLAUDE_SKILLS := arch-step arch-mini-plan lilarch bugs-flow goal-loop north-star-investigation arch-flow arch-skills-guide
GEMINI_SKILLS := arch-step arch-mini-plan lilarch bugs-flow goal-loop north-star-investigation arch-flow arch-skills-guide
ARCHIVED_COMMAND_FILES := $(notdir $(wildcard archive/prompts/*.md))

ifeq ($(NO_GEMINI),1)
INSTALL_GEMINI :=
VERIFY_GEMINI :=
else
INSTALL_GEMINI := gemini_install
VERIFY_GEMINI := verify_gemini_install
endif

install: clean_codex_stale_surfaces clean_claude_stale_surfaces install_skill claude_install_skill $(INSTALL_GEMINI)

clean_codex_stale_surfaces:
	@mkdir -p ~/.codex/prompts/_backup
	@ts=$$(date +%Y%m%d_%H%M%S); \
	backup_dir=~/.codex/prompts/_backup/arch_skill_disabled_$$ts; \
	mkdir -p "$$backup_dir"; \
	for file in $(ARCHIVED_COMMAND_FILES); do \
		if [ -f ~/.codex/prompts/$$file ]; then \
			mv -f ~/.codex/prompts/$$file "$$backup_dir"/; \
		fi; \
	done; \
	rmdir "$$backup_dir" 2>/dev/null || true

clean_claude_stale_surfaces:
	@mkdir -p ~/.claude/commands/prompts/_backup
	@ts=$$(date +%Y%m%d_%H%M%S); \
	backup_dir=~/.claude/commands/prompts/_backup/arch_skill_disabled_$$ts; \
	mkdir -p "$$backup_dir"; \
	for file in $(ARCHIVED_COMMAND_FILES); do \
		if [ -f ~/.claude/commands/prompts/$$file ]; then \
			mv -f ~/.claude/commands/prompts/$$file "$$backup_dir"/; \
		fi; \
	done; \
	rmdir "$$backup_dir" 2>/dev/null || true

clean_gemini_stale_surfaces:
	@mkdir -p ~/.gemini/_backup/commands ~/.gemini/_backup/arch_skill ~/.gemini/commands/prompts ~/.gemini/arch_skill/prompts
	@ts=$$(date +%Y%m%d_%H%M%S); \
	prompt_backup=~/.gemini/_backup/arch_skill/prompts_$$ts; \
	command_backup=~/.gemini/_backup/commands/prompts_$$ts; \
	mkdir -p "$$prompt_backup" "$$command_backup"; \
	for file in $(ARCHIVED_COMMAND_FILES); do \
		if [ -f ~/.gemini/arch_skill/prompts/$$file ]; then \
			mv -f ~/.gemini/arch_skill/prompts/$$file "$$prompt_backup"/; \
		fi; \
		command_file=$${file%.md}.toml; \
		if [ -f ~/.gemini/commands/prompts/$$command_file ]; then \
			mv -f ~/.gemini/commands/prompts/$$command_file "$$command_backup"/; \
		fi; \
	done; \
	if [ -f ~/.gemini/commands/prompts.toml ]; then \
		mv -f ~/.gemini/commands/prompts.toml ~/.gemini/_backup/commands/prompts.toml.$$ts.bak; \
	fi; \
	rmdir "$$prompt_backup" 2>/dev/null || true; \
	rmdir "$$command_backup" 2>/dev/null || true

install_skill:
	mkdir -p ~/.codex/skills
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		rm -rf ~/.codex/skills/$$skill; \
	done
	@for skill in $(SKILLS); do \
		cp -R skills/$$skill ~/.codex/skills/$$skill; \
	done

claude_install_skill:
	mkdir -p ~/.claude/skills
	@for skill in $(REMOVED_SKILLS) $(CLAUDE_SKILLS); do \
		rm -rf ~/.claude/skills/$$skill; \
	done
	@for skill in $(CLAUDE_SKILLS); do \
		cp -R skills/$$skill ~/.claude/skills/$$skill; \
	done

gemini_install: clean_gemini_stale_surfaces gemini_install_skill

gemini_install_skill:
	mkdir -p ~/.gemini/skills
	@for skill in $(REMOVED_SKILLS) $(GEMINI_SKILLS); do \
		rm -rf ~/.gemini/skills/$$skill; \
	done
	@for skill in $(GEMINI_SKILLS); do \
		cp -R skills/$$skill ~/.gemini/skills/$$skill; \
		f=~/.gemini/skills/$$skill/SKILL.md; \
		tmp=$$f.tmp; \
		awk 'NR==1 && $$0=="---" {front=1; next} front && $$0=="---" {front=0; next} !front {print}' "$$f" > "$$tmp" && mv "$$tmp" "$$f"; \
	done

verify_install: verify_claude_install $(VERIFY_GEMINI)
	@for skill in $(SKILLS); do \
		test -f ~/.codex/skills/$$skill/SKILL.md; \
	done
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.codex/prompts/$$file; \
	done
	@test ! -d ~/.codex/skills/arch-plan
	@test ! -d ~/.codex/skills/arch-skill
	@echo "OK: Codex active skills installed; stale command surfaces removed"

verify_claude_install:
	@for skill in $(CLAUDE_SKILLS); do \
		test -f ~/.claude/skills/$$skill/SKILL.md; \
	done
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.claude/commands/prompts/$$file; \
	done
	@test ! -d ~/.claude/skills/arch-plan
	@test ! -d ~/.claude/skills/arch-skill
	@echo "OK: Claude Code active skills installed; stale command surfaces removed"

verify_gemini_install:
	@for skill in $(GEMINI_SKILLS); do \
		test -f ~/.gemini/skills/$$skill/SKILL.md; \
	done
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.gemini/arch_skill/prompts/$$file; \
		command_file=$${file%.md}.toml; \
		test ! -f ~/.gemini/commands/prompts/$$command_file; \
	done
	@test ! -f ~/.gemini/commands/prompts.toml
	@test ! -d ~/.gemini/skills/arch-plan
	@test ! -d ~/.gemini/skills/arch-skill
	@echo "OK: Gemini active skills installed; stale command surfaces removed"

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@ssh $(HOST) "mkdir -p ~/.codex/skills ~/.codex/prompts/_backup"
	@ssh $(HOST) "mkdir -p ~/.claude/skills ~/.claude/commands/prompts/_backup"
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		ssh $(HOST) "mkdir -p ~/.gemini/skills ~/.gemini/commands/prompts ~/.gemini/_backup/commands ~/.gemini/arch_skill/prompts ~/.gemini/_backup/arch_skill"; \
	fi
	@ssh $(HOST) "ts=\$$(date +%Y%m%d_%H%M%S); backup_dir=~/.codex/prompts/_backup/arch_skill_disabled_\$$ts; mkdir -p \"\$$backup_dir\"; for file in $(ARCHIVED_COMMAND_FILES); do if [ -f ~/.codex/prompts/\$$file ]; then mv -f ~/.codex/prompts/\$$file \"\$$backup_dir\"/; fi; done; rmdir \"\$$backup_dir\" 2>/dev/null || true"
	@ssh $(HOST) "ts=\$$(date +%Y%m%d_%H%M%S); backup_dir=~/.claude/commands/prompts/_backup/arch_skill_disabled_\$$ts; mkdir -p \"\$$backup_dir\"; for file in $(ARCHIVED_COMMAND_FILES); do if [ -f ~/.claude/commands/prompts/\$$file ]; then mv -f ~/.claude/commands/prompts/\$$file \"\$$backup_dir\"/; fi; done; rmdir \"\$$backup_dir\" 2>/dev/null || true"
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		ssh $(HOST) "ts=\$$(date +%Y%m%d_%H%M%S); prompt_backup=~/.gemini/_backup/arch_skill/prompts_\$$ts; command_backup=~/.gemini/_backup/commands/prompts_\$$ts; mkdir -p \"\$$prompt_backup\" \"\$$command_backup\"; for file in $(ARCHIVED_COMMAND_FILES); do if [ -f ~/.gemini/arch_skill/prompts/\$$file ]; then mv -f ~/.gemini/arch_skill/prompts/\$$file \"\$$prompt_backup\"/; fi; command_file=\$${file%.md}.toml; if [ -f ~/.gemini/commands/prompts/\$$command_file ]; then mv -f ~/.gemini/commands/prompts/\$$command_file \"\$$command_backup\"/; fi; done; [ -f ~/.gemini/commands/prompts.toml ] && mv -f ~/.gemini/commands/prompts.toml ~/.gemini/_backup/commands/prompts.toml.\$$ts.bak || true; rmdir \"\$$prompt_backup\" 2>/dev/null || true; rmdir \"\$$command_backup\" 2>/dev/null || true"; \
	fi
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		ssh $(HOST) "rm -rf ~/.codex/skills/$$skill"; \
	done
	@for skill in $(SKILLS); do \
		scp -r skills/$$skill $(HOST):~/.codex/skills/; \
	done
	@for skill in $(REMOVED_SKILLS) $(CLAUDE_SKILLS); do \
		ssh $(HOST) "rm -rf ~/.claude/skills/$$skill"; \
	done
	@for skill in $(CLAUDE_SKILLS); do \
		scp -r skills/$$skill $(HOST):~/.claude/skills/; \
	done
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		for skill in $(REMOVED_SKILLS) $(GEMINI_SKILLS); do \
			ssh $(HOST) "rm -rf ~/.gemini/skills/$$skill"; \
		done; \
		for skill in $(GEMINI_SKILLS); do \
			scp -r skills/$$skill $(HOST):~/.gemini/skills/; \
		done; \
		ssh $(HOST) "for skill in $(GEMINI_SKILLS); do f=~/.gemini/skills/\$$skill/SKILL.md; tmp=\$$f.tmp; awk 'NR==1 && $$0==\"---\" {front=1; next} front && $$0==\"---\" {front=0; next} !front {print}' \"\$$f\" > \"\$$tmp\" && mv \"\$$tmp\" \"\$$f\"; done"; \
	fi
