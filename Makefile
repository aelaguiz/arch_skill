.PHONY: install remote_install

install:
	mkdir -p ~/.codex/prompts
	cp prompts/*.md ~/.codex/prompts/

remote_install:
	@if [ -z "$(HOST)" ]; then echo "HOST is required. Usage: make remote_install HOST=<user@host>"; exit 1; fi
	@mkdir -p ~/.codex/prompts
	@for f in ~/.codex/prompts/arch-*.md; do \
		scp $$f $(HOST):~/.codex/prompts/; \
	done
	@for f in ~/.codex/prompts/maestro-*.md; do \
		scp $$f $(HOST):~/.codex/prompts/; \
	done
