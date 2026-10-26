# Maintenance And Portability

Use this file when maintaining `AGENTS.md` over time, keeping multi-tool setups coherent, or deciding when the file should change.

## Table of contents

- Maintain one source of truth
- Self-improving AGENTS loop
- When to update the file
- Validation loop
- Portability across coding-agent tools
- Source notes

## Maintain one source of truth

If the repo serves multiple coding-agent tools, keep `AGENTS.md` as the canonical instruction file whenever the toolchain supports it.

Why:

- one authoritative file is easier to audit
- drift between `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and other mirrors is expensive and confusing
- path-local scoping is more manageable when one hierarchy owns the truth

If mirrors are still needed for tool compatibility:

- generate or symlink them from `AGENTS.md`
- treat manual divergence as a bug
- document the mirroring rule in the repo's contributing or agent docs, not inside every local file

## Learning from agent mistakes

A good `AGENTS.md` grows from real failures, not from listing every possible rule up front. When agents keep making a mistake, work out what they were missing: what the person who corrected them saw, why it matters, and where it applies and where it doesn't. Then change the guidance that should have covered it, so the file says one thing, instead of adding an instruction shaped like the incident. `$intuition-building` shows how. Some lessons are facts, such as an exact command, a path, or a required approval, and those belong as plain lines.

Check that the change carries by picturing an agent in a case that looks nothing like the incident, including one where the right move is different. Retire or tighten guidance when the repo or tooling changes; a line nobody needs any more still costs every run.

## When to update the file

Update `AGENTS.md` when:

- the verify commands changed
- the repo added a new dangerous workflow or approval boundary
- a local subtree now needs its own commands or red lines
- the docs map or skill triggers changed materially
- a repeated mistake keeps happening because the agent lacks repo-specific context

Do not update it just because:

- the team has a new philosophy slogan
- you want to summarize recent work
- a one-off incident happened but does not imply a durable repo rule
- you can point to an existing doc instead

## Validation loop

When authoring or editing:

1. Verify the commands are current.
2. Confirm the file's rules match the owning directory and workflow.
3. Check that deeper docs or local files still exist at the named paths.
4. Read the file top-to-bottom and remove anything inferable or repetitive.
5. Remove any sentence about the drafting process, future cleanup plans, or the skill used to write the file unless that text is itself a real repo rule.
6. If the file includes plain-speak guidance, keep it short, concrete, and example-driven rather than turning it into abstract communication philosophy.
7. If the file names required checks, run them after editing whenever feasible.

When auditing:

- distinguish stale commands from stale scope
- distinguish missing commands from missing docs routing
- distinguish too much content from missing content

## Portability across coding-agent tools

Portable instruction design tends to share these properties:

- short, literal headings
- exact commands and paths
- no vendor-specific magic unless clearly labeled
- scope defined by directory structure, not by brand-specific features alone

Safe portable patterns:

- root plus path-local files
- exact command sections
- compact docs maps
- explicit red lines and ask-first rules

Less portable patterns:

- tool-specific slash commands without fallback explanation
- assumptions about a single agent's hidden system prompt
- long sections describing UI behavior instead of repo behavior

If the file includes vendor-specific notes, keep them small and isolate them near the bottom or under a clear heading.

## Source notes

Derived from:

- OpenAI Codex project-instruction guidance
- OpenAI `agents.md` examples and override patterns
- GitHub Copilot repository-instructions guidance
- cross-tool compatibility notes collected in the repo research pack
