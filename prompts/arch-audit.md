---
description: "08) Audit: code vs plan gaps list."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-audit — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc, or to disambiguate between multiple equally plausible docs.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask “what do you want to do?”).

Stop-the-line gates (must pass before audit)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.
Compare the architecture doc at DOC_PATH against the actual code in the current repo.
Find gaps, drift, missed call sites, and violations of conventions/patterns.
Update the doc with a **Gaps & Concerns List** using the exact format below.
Write/update the block into DOC_PATH (anti-fragile placement; do not assume specific section numbering).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:gaps_concerns:start -->` … `<!-- arch_skill:block:gaps_concerns:end -->`
2) Else, if a "Gaps & Concerns" section already exists (heading match), update it in place.
3) Else, insert near the end of the doc:
   - Prefer inserting before the Decision Log (if present),
   - otherwise append.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:gaps_concerns:start -->
# Gaps & Concerns List (audit vs code)
## Summary
- Coverage: <what % or rough completeness>
- Primary risk areas:
  - <risk>

## Gaps Table
| Area | File | Symbol / Call site | Expected (per plan) | Actual (in code) | Impact | Fix | Status |
| ---- | ---- | ------------------ | ------------------- | ---------------- | ------ | --- | ------ |
| <module> | <path> | <fn/cls> | <plan intent> | <observed> | <risk> | <proposed> | open |

## Drift / Convention violations
- <rule violated> — <where> — <why it matters>

## Missed spots (unimplemented or partially implemented)
- <spot> — <symptom> — <what remains>

## Follow-ups / questions
- <question>
<!-- arch_skill:block:gaps_concerns:end -->

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
