---
description: "07) DevX: CLI-output mocks + artifacts."
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Add a Dev Experience section to $DOC_PATH.
Capture developer-facing outputs and commands:
- CLI/console mockups (startup + summary)
- Structured output schemas and canonical artifact paths
- Debugging/inspection shortcuts
- DX acceptance tests
Update the section in place if it already exists.
Write the section into $DOC_PATH (insert after #8 Test Strategy). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT (insert after #8 Test Strategy):
# 8.5 Dev Experience (DX) Targets
## 8.5.1 CLI / Console UX (if relevant)
- Principles:
- Canonical commands:
  - `<command>`
- Startup banner mock (exact):
```text
<CLI startup banner mockup>
```
- Per-epoch / summary mock (exact):
```text
<CLI per-epoch or summary block mockup>
```

## 8.5.2 Structured outputs + artifacts
- Canonical output paths:
  - `runs/<run_id>/...`
- Schema expectations:
```json
{
  "field": "example"
}
```

## 8.5.3 Debugging / inspection shortcuts
- `rg -n "<pattern>" <log_path>`
- `jq -r "<filter>" <json_path>`

## 8.5.4 DX acceptance tests
- `<command>` — expected artifacts + pass/fail signal

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
