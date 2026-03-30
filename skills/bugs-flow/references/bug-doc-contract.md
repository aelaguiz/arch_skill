# Bugs Flow Doc Contract

## DOC_PATH

- Use `docs/bugs/<...>.md` when the user gives a bug doc.
- Otherwise reuse the obvious active bug doc or create one under `docs/bugs/`.
- Keep one bug doc as the SSOT for the incident or regression.

## New-doc minimum contract

When creating a new bug doc, include at least:

- YAML frontmatter with:
  - `title`
  - `date`
  - `status`
  - `owners`
  - `reviewers`
  - `related`
- TL;DR with:
  - symptom
  - impact
  - most likely cause
  - next action
  - status
- analysis sections for:
  - Bug North Star
  - bug summary
  - evidence
  - investigation
- fix-plan and implementation sections, even if initially skeletal

## Status progression

Common status values:

- `triage`
- `investigating`
- `fix-ready`
- `fixing`
- `verifying`
- `resolved`
- `blocked`

Update both frontmatter status and the TL;DR status line together.

## Required blocks

- `bugs:block:tldr`
- `bugs:block:analysis`
- `bugs:block:fix_plan`
- `bugs:block:implementation`

## Evidence rules

- Analyze mode is docs-only.
- Prefer first-party evidence:
  - Sentry issue details and events when available
  - logs and traces
  - QA notes and repro steps
  - repo searches and code anchors
- Use external research only when a library or framework behavior is genuinely ambiguous.

## Essential-info gate

Stop and ask only when a truly essential input is missing.

Examples:

- the report references a specific Sentry issue but the ID or URL is missing or malformed
- environment or access differences materially affect the investigation and cannot be inferred

Keep the ask minimal and specific.

## Sentry defaults

When a Sentry issue is part of the bug evidence:

- default organization: `funcountry`
- default project:
  - `psmobile-production` unless staging is explicitly indicated
  - `psmobile-staging` when staging is explicitly indicated
- gather at least:
  - title or exception
  - top stack frames
  - first seen / last seen
  - frequency or affected users when available
  - relevant tags such as environment, release, URL, or device when they materially change the fix shape

If a tool can provide Seer-style analysis or representative events, capture that evidence in the doc rather than paraphrasing from memory.

## Review rule

- Cross-model or external review is explicit-review-only.
- If the user did not ask for review or code review, stop after local analysis/fix/verification.
