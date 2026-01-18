---
description: "07) DevX: CLI-output mocks + artifacts."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-devx — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc, or to disambiguate between multiple equally plausible docs.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask “what do you want to do?”).

Stop-the-line gates (must pass before writing DevX targets)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.
Add a Dev Experience section to DOC_PATH.
Capture developer-facing outputs and commands:
- CLI/console mockups (startup + summary)
- Structured output schemas and canonical artifact paths
- Debugging/inspection shortcuts
- DX acceptance tests (cheap, signal-only; avoid overbuilt harnesses)
Update the section in place if it already exists.
Write/update the section into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:devx:start -->` … `<!-- arch_skill:block:devx:end -->`
2) Else insert after the most relevant existing testing section (heading match, case-insensitive):
   - "Test Strategy", "Testing", "Verification"
3) Else insert near the end of the doc, before the Decision Log (if present), otherwise append.
Numbering rule:
- If the doc uses numbered headings, preserve numbering; do not renumber the rest of the document.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:devx:start -->
# Dev Experience (DX) Targets
## CLI / Console UX (if relevant)
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

## Structured outputs + artifacts
- Canonical output paths:
  - `runs/<run_id>/...`
- Schema expectations:
```json
{
  "field": "example"
}
```

## Debugging / inspection shortcuts
- `rg -n "<pattern>" <log_path>`
- `jq -r "<filter>" <json_path>`

## DX acceptance tests
- Principle: keep these fast and runnable; prefer smoke-level checks over “proof ladders.” Do not block the plan on flaky device/sim steps.
- `<command>` — expected artifacts + pass/fail signal
<!-- arch_skill:block:devx:end -->

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
