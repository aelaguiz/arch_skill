.PHONY: install install_skill agents_install_skill clean_codex_skill_mirror clean_installed_hooks clean_codex_installed_hooks clean_claude_installed_hooks claude_install_skill gemini_install gemini_install_skill hermes_install_skill verify_install verify_agents_install verify_codex_install verify_claude_install verify_gemini_install verify_hermes_install remote_install clean_codex_stale_surfaces clean_claude_stale_surfaces clean_gemini_stale_surfaces

# Purge removed packages from installed skill dirs before copying the active set.
REMOVED_SKILLS := arch-skill arch-plan codemagic-builds customerio arch-loop delay-poll wait code-review
# Shared doctrine directories that ship alongside the named skills. Multiple
# SKILL.md files reference shared planning/model-resolution files,
# so these dirs must land in every install root next to the per-skill dirs.
SHARED_DIRS := _shared
# `SKILLS` is the active agents/Codex surface. Claude mirrors it.
SKILLS := arch-step miniarch-step arch-docs arch-mini-plan lilarch bugs-flow audit-loop comment-loop audit-loop-sim goal-loop north-star-investigation arch-flow arch-skills-guide agent-definition-auditor agents-md-authoring prompt-authoring chatgpt-web skill-authoring figma-best-practices fal-ai-tools flutter-reference eli10 pr-authoring pr-review-followthrough commit-history-authoring skill-flow amir-publish codex-review-yolo fresh-consult agent-delegate plan-audit plan-implement plan-swarm agent-history model-consensus contact-sheet-builder exhaustive-code-review stepwise arch-epic codex-cleanup thermo-nuclear-code-quality-review
CLAUDE_SKILLS := arch-step miniarch-step arch-docs arch-mini-plan lilarch bugs-flow audit-loop comment-loop audit-loop-sim goal-loop north-star-investigation arch-flow arch-skills-guide agent-definition-auditor agents-md-authoring prompt-authoring chatgpt-web skill-authoring figma-best-practices fal-ai-tools flutter-reference eli10 pr-authoring pr-review-followthrough commit-history-authoring skill-flow amir-publish codex-review-yolo fresh-consult agent-delegate plan-audit plan-implement plan-swarm agent-history model-consensus contact-sheet-builder exhaustive-code-review stepwise arch-epic codex-cleanup thermo-nuclear-code-quality-review
GEMINI_SKILLS := arch-step miniarch-step arch-docs arch-mini-plan lilarch bugs-flow audit-loop comment-loop audit-loop-sim goal-loop north-star-investigation arch-flow arch-skills-guide agent-definition-auditor agents-md-authoring prompt-authoring chatgpt-web skill-authoring figma-best-practices fal-ai-tools flutter-reference eli10 pr-authoring commit-history-authoring skill-flow amir-publish codex-review-yolo fresh-consult agent-delegate plan-audit plan-implement plan-swarm model-consensus contact-sheet-builder exhaustive-code-review stepwise arch-epic codex-cleanup thermo-nuclear-code-quality-review
CURSOR_TEAM_KIT_SKILLS_DIR := vendor/cursor/plugins/cursor-team-kit/skills
VENDORED_CURSOR_TEAM_KIT_SKILLS := thermo-nuclear-code-quality-review
LOCAL_SKILLS := $(filter-out $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(SKILLS))
LOCAL_CLAUDE_SKILLS := $(filter-out $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(CLAUDE_SKILLS))
LOCAL_GEMINI_SKILLS := $(filter-out $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(GEMINI_SKILLS))
VENDORED_SKILLS := $(filter $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(SKILLS))
VENDORED_CLAUDE_SKILLS := $(filter $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(CLAUDE_SKILLS))
VENDORED_GEMINI_SKILLS := $(filter $(VENDORED_CURSOR_TEAM_KIT_SKILLS),$(GEMINI_SKILLS))
NON_CLAUDE_SKILLS := $(filter-out $(CLAUDE_SKILLS),$(SKILLS))
NON_GEMINI_SKILLS := $(filter-out $(GEMINI_SKILLS),$(SKILLS))
# Prompt-era command files are no longer runtime sources; these names drive
# stale-install cleanup and verification for older Codex, Claude, and Gemini paths.
ARCHIVED_COMMAND_FILES := \
	arch-ascii.md \
	arch-audit-agent.md \
	arch-audit-implementation-agent.md \
	arch-audit-implementation.md \
	arch-audit.md \
	arch-codereview.md \
	arch-context-load.md \
	arch-debug-brutal.md \
	arch-debug.md \
	arch-deep-dive-agent.md \
	arch-deep-dive.md \
	arch-devx-agent.md \
	arch-devx.md \
	arch-external-research-agent.md \
	arch-flow.md \
	arch-fold-in.md \
	arch-html-full.md \
	arch-implement-agent.md \
	arch-implement.md \
	arch-kickoff.md \
	arch-mini-plan-agent.md \
	arch-new.md \
	arch-open-pr.md \
	arch-overbuild-protector.md \
	arch-phase-plan-agent.md \
	arch-phase-plan-granularize-agent.md \
	arch-phase-plan-granularize.md \
	arch-phase-plan.md \
	arch-plan-audit-agent.md \
	arch-plan-audit.md \
	arch-plan-enhance.md \
	arch-progress.md \
	arch-qa-autotest.md \
	arch-ralph-enhance.md \
	arch-ralph-retarget.md \
	arch-ramp-up-agent.md \
	arch-ramp-up.md \
	arch-reformat.md \
	arch-research-agent.md \
	arch-research.md \
	arch-review-gate.md \
	arch-ui-ascii.md \
	bugs-analyze.md \
	bugs-fix.md \
	bugs-review.md \
	cio-campaign-evaluate.md \
	goal-loop-context-load.md \
	goal-loop-flow.md \
	goal-loop-iterate.md \
	goal-loop-new.md \
	lilarch-finish.md \
	lilarch-plan.md \
	lilarch-start.md \
	maestro-autopilot.md \
	maestro-kill.md \
	maestro-rerun-last.md \
	new-arch-from-docs.md \
	north-star-investigation-bootstrap.md \
	north-star-investigation-loop.md \
	qa-autopilot.md \
	sentry-triage.md
AGENTS_SKILLS_DIR ?= $(HOME)/.agents/skills
CODEX_SKILLS_DIR ?= $(HOME)/.codex/skills
CODEX_HOOKS_FILE ?= $(HOME)/.codex/hooks.json
CLAUDE_SKILLS_DIR ?= $(HOME)/.claude/skills
CLAUDE_SETTINGS_FILE ?= $(HOME)/.claude/settings.json
GEMINI_SKILLS_DIR ?= $(HOME)/.gemini/skills
# Hermes Agent reads skills from category subdirectories under per-profile
# skill roots. Install mirrors the agents surface into every Hermes root that
# already exists on this machine; it never creates a Hermes home or profile.
HERMES_HOME ?= $(HOME)/.hermes
HERMES_SKILLS_SUBDIR := arch_skill

ifeq ($(NO_GEMINI),1)
INSTALL_GEMINI :=
VERIFY_GEMINI :=
else
INSTALL_GEMINI := gemini_install
VERIFY_GEMINI := verify_gemini_install
endif

ifeq ($(NO_HERMES),1)
INSTALL_HERMES :=
VERIFY_HERMES :=
else
INSTALL_HERMES := hermes_install_skill
VERIFY_HERMES := verify_hermes_install
endif

install: clean_codex_stale_surfaces clean_claude_stale_surfaces clean_installed_hooks install_skill claude_install_skill $(INSTALL_GEMINI) $(INSTALL_HERMES)

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

install_skill: agents_install_skill clean_codex_skill_mirror

agents_install_skill:
	mkdir -p $(AGENTS_SKILLS_DIR)
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		rm -rf $(AGENTS_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(LOCAL_SKILLS); do \
		cp -R skills/$$skill $(AGENTS_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(VENDORED_SKILLS); do \
		cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(AGENTS_SKILLS_DIR)/$$skill; \
	done
	@for shared in $(SHARED_DIRS); do \
		rm -rf $(AGENTS_SKILLS_DIR)/$$shared; \
		cp -R skills/$$shared $(AGENTS_SKILLS_DIR)/$$shared; \
	done
	@for item in $(SKILLS) $(SHARED_DIRS); do \
		find $(AGENTS_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; \
		find $(AGENTS_SKILLS_DIR)/$$item -name '*.pyc' -delete; \
		find $(AGENTS_SKILLS_DIR)/$$item -name 'upsert_*hook.py' -delete; \
		find $(AGENTS_SKILLS_DIR)/$$item -name 'arch_controller_stop_hook.py' -delete; \
	done

clean_codex_skill_mirror:
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		rm -rf $(CODEX_SKILLS_DIR)/$$skill; \
	done

clean_installed_hooks: clean_codex_installed_hooks clean_claude_installed_hooks

clean_codex_installed_hooks:
	@python3 skills/arch-step/scripts/upsert_codex_stop_hook.py --remove --hooks-file "$(CODEX_HOOKS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"

clean_claude_installed_hooks:
	@python3 skills/arch-step/scripts/upsert_claude_stop_hook.py --remove --settings-file "$(CLAUDE_SETTINGS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"
	@python3 skills/arch-step/scripts/upsert_claude_session_start_hook.py --remove --settings-file "$(CLAUDE_SETTINGS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"

claude_install_skill:
	mkdir -p $(CLAUDE_SKILLS_DIR)
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		rm -rf $(CLAUDE_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(LOCAL_CLAUDE_SKILLS); do \
		cp -R skills/$$skill $(CLAUDE_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(VENDORED_CLAUDE_SKILLS); do \
		cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(CLAUDE_SKILLS_DIR)/$$skill; \
	done
	@for shared in $(SHARED_DIRS); do \
		rm -rf $(CLAUDE_SKILLS_DIR)/$$shared; \
		cp -R skills/$$shared $(CLAUDE_SKILLS_DIR)/$$shared; \
	done
	@for item in $(CLAUDE_SKILLS) $(SHARED_DIRS); do \
		find $(CLAUDE_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; \
		find $(CLAUDE_SKILLS_DIR)/$$item -name '*.pyc' -delete; \
		find $(CLAUDE_SKILLS_DIR)/$$item -name 'upsert_*hook.py' -delete; \
		find $(CLAUDE_SKILLS_DIR)/$$item -name 'arch_controller_stop_hook.py' -delete; \
	done

gemini_install: clean_gemini_stale_surfaces gemini_install_skill

gemini_install_skill:
	mkdir -p $(GEMINI_SKILLS_DIR)
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		rm -rf $(GEMINI_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(LOCAL_GEMINI_SKILLS); do \
		cp -R skills/$$skill $(GEMINI_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(VENDORED_GEMINI_SKILLS); do \
		cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(GEMINI_SKILLS_DIR)/$$skill; \
	done
	@for skill in $(GEMINI_SKILLS); do \
		f=$(GEMINI_SKILLS_DIR)/$$skill/SKILL.md; \
		tmp=$$f.tmp; \
		awk 'NR==1 && $$0=="---" {front=1; next} front && $$0=="---" {front=0; next} !front {print}' "$$f" > "$$tmp" && mv "$$tmp" "$$f"; \
	done
	@for shared in $(SHARED_DIRS); do \
		rm -rf $(GEMINI_SKILLS_DIR)/$$shared; \
		cp -R skills/$$shared $(GEMINI_SKILLS_DIR)/$$shared; \
	done
	@for item in $(GEMINI_SKILLS) $(SHARED_DIRS); do \
		find $(GEMINI_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; \
		find $(GEMINI_SKILLS_DIR)/$$item -name '*.pyc' -delete; \
		find $(GEMINI_SKILLS_DIR)/$$item -name 'upsert_*hook.py' -delete; \
		find $(GEMINI_SKILLS_DIR)/$$item -name 'arch_controller_stop_hook.py' -delete; \
	done

# Mirror the agents skill surface into every Hermes Agent skill root that
# already exists: the default profile root ($(HERMES_HOME)/skills) and each
# named profile root ($(HERMES_HOME)/profiles/<name>/skills). Skills land
# under the $(HERMES_SKILLS_SUBDIR) category directory. Machines without a
# Hermes home are skipped; pass NO_HERMES=1 to opt out entirely.
hermes_install_skill:
	@roots=""; \
	if [ -d "$(HERMES_HOME)/skills" ]; then roots="$(HERMES_HOME)/skills"; fi; \
	for profile in $(HERMES_HOME)/profiles/*/; do \
		if [ -d "$$profile" ]; then roots="$$roots $${profile%/}/skills"; fi; \
	done; \
	if [ -z "$$roots" ]; then \
		echo "SKIP: no Hermes skill roots under $(HERMES_HOME); nothing to install"; \
		exit 0; \
	fi; \
	for root in $$roots; do \
		dest="$$root/$(HERMES_SKILLS_SUBDIR)"; \
		mkdir -p "$$dest"; \
		for skill in $(REMOVED_SKILLS) $(SKILLS); do \
			rm -rf "$$dest/$$skill"; \
		done; \
		for skill in $(LOCAL_SKILLS); do \
			cp -R skills/$$skill "$$dest/$$skill"; \
		done; \
		for skill in $(VENDORED_SKILLS); do \
			cp -R $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill "$$dest/$$skill"; \
		done; \
		for shared in $(SHARED_DIRS); do \
			rm -rf "$$dest/$$shared"; \
			cp -R skills/$$shared "$$dest/$$shared"; \
		done; \
		for item in $(SKILLS) $(SHARED_DIRS); do \
			find "$$dest/$$item" \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; \
			find "$$dest/$$item" -name '*.pyc' -delete; \
			find "$$dest/$$item" -name 'upsert_*hook.py' -delete; \
			find "$$dest/$$item" -name 'arch_controller_stop_hook.py' -delete; \
		done; \
		echo "OK: Hermes skills installed to $$dest"; \
	done

verify_install: verify_agents_install verify_codex_install verify_claude_install $(VERIFY_GEMINI) $(VERIFY_HERMES)
	@echo "OK: active skill surface installed for agents, Claude Code, requested Gemini targets, and existing Hermes skill roots; no arch_skill hooks installed"

verify_agents_install:
	@for skill in $(SKILLS); do \
		test -f $(AGENTS_SKILLS_DIR)/$$skill/SKILL.md; \
	done
	@for item in $(SKILLS) $(SHARED_DIRS); do \
		if find $(AGENTS_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -print -quit | grep -q .; then echo "ERROR: source/build internals installed under $(AGENTS_SKILLS_DIR)/$$item"; exit 1; fi; \
		if find $(AGENTS_SKILLS_DIR)/$$item -name '*.pyc' -print -quit | grep -q .; then echo "ERROR: Python bytecode installed under $(AGENTS_SKILLS_DIR)/$$item"; exit 1; fi; \
	done
	@for skill in $(REMOVED_SKILLS); do \
		test ! -d $(AGENTS_SKILLS_DIR)/$$skill; \
	done
	@test -f $(AGENTS_SKILLS_DIR)/_shared/depth-first-planning.md
	@test -f $(AGENTS_SKILLS_DIR)/_shared/model_resolution.py
	@test ! -e $(AGENTS_SKILLS_DIR)/arch-step/scripts/arch_controller_stop_hook.py
	@test ! -e $(AGENTS_SKILLS_DIR)/arch-step/scripts/upsert_codex_stop_hook.py
	@test ! -e $(AGENTS_SKILLS_DIR)/arch-step/scripts/upsert_claude_stop_hook.py
	@test ! -e $(AGENTS_SKILLS_DIR)/arch-step/scripts/upsert_claude_session_start_hook.py
	@echo "OK: agents skills installed"

verify_codex_install:
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.codex/prompts/$$file; \
	done
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		test ! -d $(CODEX_SKILLS_DIR)/$$skill; \
	done
	@python3 skills/arch-step/scripts/upsert_codex_stop_hook.py --verify-absent --hooks-file "$(CODEX_HOOKS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"
	@echo "OK: no arch_skill Codex hooks installed; stale command surfaces and old Codex skill mirrors removed"

verify_claude_install:
	@for skill in $(CLAUDE_SKILLS); do \
		test -f $(CLAUDE_SKILLS_DIR)/$$skill/SKILL.md; \
	done
	@for item in $(CLAUDE_SKILLS) $(SHARED_DIRS); do \
		if find $(CLAUDE_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -print -quit | grep -q .; then echo "ERROR: source/build internals installed under $(CLAUDE_SKILLS_DIR)/$$item"; exit 1; fi; \
		if find $(CLAUDE_SKILLS_DIR)/$$item -name '*.pyc' -print -quit | grep -q .; then echo "ERROR: Python bytecode installed under $(CLAUDE_SKILLS_DIR)/$$item"; exit 1; fi; \
	done
	@for skill in $(NON_CLAUDE_SKILLS); do \
		test ! -d $(CLAUDE_SKILLS_DIR)/$$skill; \
	done
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.claude/commands/prompts/$$file; \
	done
	@for skill in $(REMOVED_SKILLS); do \
		test ! -d $(CLAUDE_SKILLS_DIR)/$$skill; \
	done
	@test -f $(CLAUDE_SKILLS_DIR)/_shared/depth-first-planning.md
	@test -f $(CLAUDE_SKILLS_DIR)/_shared/model_resolution.py
	@test ! -e $(CLAUDE_SKILLS_DIR)/arch-step/scripts/arch_controller_stop_hook.py
	@test ! -e $(CLAUDE_SKILLS_DIR)/arch-step/scripts/upsert_codex_stop_hook.py
	@test ! -e $(CLAUDE_SKILLS_DIR)/arch-step/scripts/upsert_claude_stop_hook.py
	@test ! -e $(CLAUDE_SKILLS_DIR)/arch-step/scripts/upsert_claude_session_start_hook.py
	@python3 skills/arch-step/scripts/upsert_claude_stop_hook.py --verify-absent --settings-file "$(CLAUDE_SETTINGS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"
	@python3 skills/arch-step/scripts/upsert_claude_session_start_hook.py --verify-absent --settings-file "$(CLAUDE_SETTINGS_FILE)" --skills-dir "$(AGENTS_SKILLS_DIR)"
	@echo "OK: Claude Code active skills installed; no arch_skill Claude hooks installed; stale command surfaces removed"

verify_gemini_install:
	@for skill in $(GEMINI_SKILLS); do \
		test -f $(GEMINI_SKILLS_DIR)/$$skill/SKILL.md; \
	done
	@for item in $(GEMINI_SKILLS) $(SHARED_DIRS); do \
		if find $(GEMINI_SKILLS_DIR)/$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -print -quit | grep -q .; then echo "ERROR: source/build internals installed under $(GEMINI_SKILLS_DIR)/$$item"; exit 1; fi; \
		if find $(GEMINI_SKILLS_DIR)/$$item -name '*.pyc' -print -quit | grep -q .; then echo "ERROR: Python bytecode installed under $(GEMINI_SKILLS_DIR)/$$item"; exit 1; fi; \
	done
	@for skill in $(NON_GEMINI_SKILLS); do \
		test ! -d $(GEMINI_SKILLS_DIR)/$$skill; \
	done
	@for file in $(ARCHIVED_COMMAND_FILES); do \
		test ! -f ~/.gemini/arch_skill/prompts/$$file; \
		command_file=$${file%.md}.toml; \
		test ! -f ~/.gemini/commands/prompts/$$command_file; \
	done
	@test ! -f ~/.gemini/commands/prompts.toml
	@for skill in $(REMOVED_SKILLS); do \
		test ! -d $(GEMINI_SKILLS_DIR)/$$skill; \
	done
	@test -f $(GEMINI_SKILLS_DIR)/_shared/depth-first-planning.md
	@test -f $(GEMINI_SKILLS_DIR)/_shared/model_resolution.py
	@test ! -e $(GEMINI_SKILLS_DIR)/arch-step/scripts/arch_controller_stop_hook.py
	@test ! -e $(GEMINI_SKILLS_DIR)/arch-step/scripts/upsert_codex_stop_hook.py
	@test ! -e $(GEMINI_SKILLS_DIR)/arch-step/scripts/upsert_claude_stop_hook.py
	@test ! -e $(GEMINI_SKILLS_DIR)/arch-step/scripts/upsert_claude_session_start_hook.py
	@echo "OK: Gemini active skills installed; stale command surfaces removed"

verify_hermes_install:
	@roots=""; \
	if [ -d "$(HERMES_HOME)/skills" ]; then roots="$(HERMES_HOME)/skills"; fi; \
	for profile in $(HERMES_HOME)/profiles/*/; do \
		if [ -d "$$profile" ]; then roots="$$roots $${profile%/}/skills"; fi; \
	done; \
	if [ -z "$$roots" ]; then \
		echo "OK: no Hermes skill roots under $(HERMES_HOME); nothing to verify"; \
		exit 0; \
	fi; \
	for root in $$roots; do \
		dest="$$root/$(HERMES_SKILLS_SUBDIR)"; \
		for skill in $(SKILLS); do \
			if [ ! -f "$$dest/$$skill/SKILL.md" ]; then echo "ERROR: missing $$dest/$$skill/SKILL.md"; exit 1; fi; \
		done; \
		for skill in $(REMOVED_SKILLS); do \
			if [ -d "$$dest/$$skill" ]; then echo "ERROR: removed skill still installed at $$dest/$$skill"; exit 1; fi; \
		done; \
		if [ ! -f "$$dest/_shared/depth-first-planning.md" ]; then echo "ERROR: missing $$dest/_shared/depth-first-planning.md"; exit 1; fi; \
		if [ ! -f "$$dest/_shared/model_resolution.py" ]; then echo "ERROR: missing $$dest/_shared/model_resolution.py"; exit 1; fi; \
		for item in $(SKILLS) $(SHARED_DIRS); do \
			if find "$$dest/$$item" \( -name build -o -name prompts -o -name __pycache__ \) -type d -print -quit | grep -q .; then echo "ERROR: source/build internals installed under $$dest/$$item"; exit 1; fi; \
			if find "$$dest/$$item" -name '*.pyc' -print -quit | grep -q .; then echo "ERROR: Python bytecode installed under $$dest/$$item"; exit 1; fi; \
			if find "$$dest/$$item" \( -name 'upsert_*hook.py' -o -name 'arch_controller_stop_hook.py' \) -print -quit | grep -q .; then echo "ERROR: hook scripts installed under $$dest/$$item"; exit 1; fi; \
		done; \
		echo "OK: Hermes skills verified at $$dest"; \
	done

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@ssh $(HOST) "mkdir -p ~/.agents/skills ~/.codex/prompts/_backup"
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
		ssh $(HOST) "rm -rf ~/.agents/skills/$$skill"; \
	done
	@for skill in $(LOCAL_SKILLS); do \
		scp -r skills/$$skill $(HOST):~/.agents/skills/; \
	done
	@for skill in $(VENDORED_SKILLS); do \
		scp -r $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(HOST):~/.agents/skills/; \
	done
	@for shared in $(SHARED_DIRS); do \
		ssh $(HOST) "rm -rf ~/.agents/skills/$$shared"; \
		scp -r skills/$$shared $(HOST):~/.agents/skills/; \
	done
	@ssh $(HOST) "python3 ~/.agents/skills/arch-step/scripts/upsert_codex_stop_hook.py --remove --hooks-file ~/.codex/hooks.json --skills-dir ~/.agents/skills"
	@ssh $(HOST) "python3 ~/.agents/skills/arch-step/scripts/upsert_claude_stop_hook.py --remove --settings-file ~/.claude/settings.json --skills-dir ~/.agents/skills"
	@ssh $(HOST) "python3 ~/.agents/skills/arch-step/scripts/upsert_claude_session_start_hook.py --remove --settings-file ~/.claude/settings.json --skills-dir ~/.agents/skills"
	@ssh $(HOST) "for item in $(SKILLS) $(SHARED_DIRS); do if [ -d ~/.agents/skills/\$$item ]; then find ~/.agents/skills/\$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; find ~/.agents/skills/\$$item -name '*.pyc' -delete; find ~/.agents/skills/\$$item -name 'upsert_*hook.py' -delete; find ~/.agents/skills/\$$item -name 'arch_controller_stop_hook.py' -delete; fi; done"
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		ssh $(HOST) "rm -rf ~/.codex/skills/$$skill"; \
	done
	@for skill in $(REMOVED_SKILLS) $(SKILLS); do \
		ssh $(HOST) "rm -rf ~/.claude/skills/$$skill"; \
	done
	@for skill in $(LOCAL_CLAUDE_SKILLS); do \
		scp -r skills/$$skill $(HOST):~/.claude/skills/; \
	done
	@for skill in $(VENDORED_CLAUDE_SKILLS); do \
		scp -r $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(HOST):~/.claude/skills/; \
	done
	@for shared in $(SHARED_DIRS); do \
		ssh $(HOST) "rm -rf ~/.claude/skills/$$shared"; \
		scp -r skills/$$shared $(HOST):~/.claude/skills/; \
	done
	@ssh $(HOST) "for item in $(CLAUDE_SKILLS) $(SHARED_DIRS); do if [ -d ~/.claude/skills/\$$item ]; then find ~/.claude/skills/\$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; find ~/.claude/skills/\$$item -name '*.pyc' -delete; find ~/.claude/skills/\$$item -name 'upsert_*hook.py' -delete; find ~/.claude/skills/\$$item -name 'arch_controller_stop_hook.py' -delete; fi; done"
	@if [ "$(NO_GEMINI)" != "1" ]; then \
		for skill in $(REMOVED_SKILLS) $(SKILLS); do \
			ssh $(HOST) "rm -rf ~/.gemini/skills/$$skill"; \
		done; \
		for skill in $(LOCAL_GEMINI_SKILLS); do \
			scp -r skills/$$skill $(HOST):~/.gemini/skills/; \
		done; \
		for skill in $(VENDORED_GEMINI_SKILLS); do \
			scp -r $(CURSOR_TEAM_KIT_SKILLS_DIR)/$$skill $(HOST):~/.gemini/skills/; \
		done; \
		ssh $(HOST) "for skill in $(GEMINI_SKILLS); do f=~/.gemini/skills/\$$skill/SKILL.md; tmp=\$$f.tmp; awk 'NR==1 && $$0==\"---\" {front=1; next} front && $$0==\"---\" {front=0; next} !front {print}' \"\$$f\" > \"\$$tmp\" && mv \"\$$tmp\" \"\$$f\"; done"; \
		for shared in $(SHARED_DIRS); do \
			ssh $(HOST) "rm -rf ~/.gemini/skills/$$shared"; \
			scp -r skills/$$shared $(HOST):~/.gemini/skills/; \
		done; \
		ssh $(HOST) "for item in $(GEMINI_SKILLS) $(SHARED_DIRS); do if [ -d ~/.gemini/skills/\$$item ]; then find ~/.gemini/skills/\$$item \( -name build -o -name prompts -o -name __pycache__ \) -type d -prune -exec rm -rf {} +; find ~/.gemini/skills/\$$item -name '*.pyc' -delete; find ~/.gemini/skills/\$$item -name 'upsert_*hook.py' -delete; find ~/.gemini/skills/\$$item -name 'arch_controller_stop_hook.py' -delete; fi; done"; \
		fi
