# OpenClaw Skills

Use this file when the target runtime is OpenClaw or any environment that mirrors OpenClaw skill semantics.

Apply the normal skill-authoring rules first. Then apply the OpenClaw-specific loader, frontmatter, gating, and deployment rules here.

## Table of contents

- Mental model
- OpenClaw-only frontmatter and metadata
- Loader, gating, and snapshot behavior
- Description and prompt-budget doctrine
- Deterministic slash commands and command-dispatch
- Filesystem placement and fleet isolation
- Security and secret handling
- Validation and deployment checks
- OpenClaw-specific anti-patterns

## Mental model

OpenClaw skills are markdown runbooks, not code plugins.

- `SKILL.md` teaches the agent what to do and how to use tools.
- Tool permissions and capability boundaries live in the host runtime, such as `tools.allow` and OpenClaw config, not in skill prose.
- Machine-readable frontmatter is part of runtime behavior, not documentation.

If you need a new ability, start with tools and config. If you need reusable operational guidance, that is the skill.

## OpenClaw-only frontmatter and metadata

OpenClaw supports more frontmatter than a generic Codex-style skill. Treat these fields as operational switches:

```yaml
---
name: example-skill
description: "Short semantic trigger phrase."
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata: {"openclaw":{"os":["darwin"],"requires":{"bins":["uv"],"env":["API_KEY"]}}}
---
```

The key rules:

- always quote `description`
- keep `metadata` as a single-line JSON object
- prefer `metadata.openclaw` over legacy aliases unless compatibility requires otherwise
- use `user-invocable` when a slash command should be exposed to the user
- use `disable-model-invocation` when the skill should stay available as a command but not participate in model matching
- use `command-dispatch` only when the slash command should bypass model reasoning entirely

Useful `metadata.openclaw` fields:

- `always`
  - force inclusion even when normal gating would exclude the skill; use sparingly
- `os`
  - restrict by platform
- `requires.bins`
  - require every listed binary to exist
- `requires.anyBins`
  - require at least one binary to exist
- `requires.env`
  - require environment variables or mapped config-backed secrets
- `requires.config`
  - require specific OpenClaw config paths to be truthy
- `primaryEnv`
  - bind the skill to its main credential slot
- `skillKey`
  - override invocation key
- `install`
  - declare installer instructions for OpenClaw UI surfaces

## Loader, gating, and snapshot behavior

OpenClaw builds an eligible skill snapshot at session start.

- skills are discovered from configured directories
- gating is applied before the model sees the skill
- the model only sees compact skill metadata, not the full body, until it chooses to read the skill
- edits do not reliably affect an active session unless you restart or enable the skills watcher

Design implications:

- load-time gating is not optional polish; it is part of the skill contract
- use `requires` and `os` aggressively to keep irrelevant skills out of the prompt
- if the skill depends on a binary, secret, or config flag, gate it at load time rather than hoping the prose prevents misuse
- when debugging "why did this not trigger?", separate eligibility failure from model-matching failure

## Description and prompt-budget doctrine

In OpenClaw, every eligible skill costs prompt budget every turn.

- keep names and descriptions terse
- use nouns users actually type
- include action verbs plus domain nouns
- avoid semantic overlap between nearby skills
- prefer distinct, concrete trigger language over clever branding

Do not design descriptions as taglines. They are semantic routing surfaces.

If a skill is command-first and should not consume model-matching budget, consider `disable-model-invocation: true`.

## Deterministic slash commands and command-dispatch

Use slash-command behavior intentionally.

Use normal model invocation when:

- the work needs reasoning
- the body of `SKILL.md` contains a real runbook
- the command must inspect context before acting

Use `command-dispatch: tool` when:

- the slash command is a deterministic wrapper
- the tool contract is stable and well-documented
- raw argument forwarding is the real interface

If you use `command-dispatch`:

- document the argument contract clearly
- test both the slash-command surface and the underlying tool call
- do not pretend there is meaningful model discretion if the runtime bypasses the model

## Filesystem placement and fleet isolation

OpenClaw skill placement changes visibility and precedence.

- workspace `skills/`
  - highest precedence; visible only to that agent or workspace
- `~/.openclaw/skills`
  - shared machine-global skills
- bundled skills
  - lower precedence than user-installed shared skills
- `skills.load.extraDirs`
  - lowest-precedence extra sources

For multi-agent fleets:

- put specialist skills in the relevant agent workspace
- put shared utilities only in the shared directory
- keep orchestrator-only routing skills local to the orchestrator
- avoid shared-directory accidents that make niche skills eligible for every agent

If a specialist skill appears in every agent prompt, that is usually a placement bug, not a description bug.

## Security and secret handling

Treat OpenClaw skill delivery as part of the threat model.

- never put secrets in `SKILL.md`
- prefer OpenClaw config and secret mapping surfaces for credentials
- treat frontmatter and metadata as untrusted inputs; never derive filesystem destinations or privileged paths from them
- assume web content, tool stdout, PDFs, and third-party skill packs can carry adversarial instructions
- respect the difference between host-process env injection and sandbox env expectations

The skill should tell the agent how to work safely, but the runtime must still enforce permissions and secret boundaries.

## Validation and deployment checks

For OpenClaw-targeted skills, validate more than the generic package shape.

Structural checks:

- quoted `description`
- parseable frontmatter
- single-line `metadata` JSON
- correct machine-readable fields for invocation behavior

Eligibility and placement checks:

- confirm the skill appears where expected and nowhere else
- verify load-time gating with OpenClaw's eligibility inspection tools
- if you edit the skill, restart the session or enable the watcher before judging the result

Operational checks:

- test slash-command behavior if `user-invocable` is enabled
- test both enabled and disabled model invocation behavior when `disable-model-invocation` matters
- test command-dispatch argument forwarding if present
- run `openclaw config validate --json` when shipping configs or documented config surfaces
- smoke-test any bundled scripts and confirm required bins or env vars match the gating metadata

## OpenClaw-specific anti-patterns

Avoid these mistakes:

- multi-line `metadata` JSON
- unquoted `description`
- marketing descriptions that never match the user's words
- shipping specialist skills into `~/.openclaw/skills` and causing fleet-wide skill bleed
- assuming skill edits hot-reload without a watcher or new session
- putting secrets or token values in the skill body
- treating skills as the place to grant tool permissions
- using `command-dispatch` for tasks that still need judgment
- letting operational runbooks omit stop conditions, anti-looping rules, or failure handling
