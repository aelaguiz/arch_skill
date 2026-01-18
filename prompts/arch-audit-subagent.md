---
description: "08a) Audit (subagent): code vs plan gaps list."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-audit-subagent — $ARGUMENTS
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

Use a subagent (non‑interactive Codex CLI) to perform the audit, then insert its output into DOC_PATH.
Do not paste the full gaps list to the console; only summarize and list open questions.

Steps:
1) Build a subagent prompt that:
   - reads DOC_PATH
   - inspects the current repo code
   - outputs ONLY the canonical “Gaps & Concerns List” block below
2) Run the subagent via `codex exec` (codex model, high reasoning) and capture its final message:
   - `codex exec -m gpt-5-codex -c reasoning_effort="high" --output-last-message /tmp/arch_audit_subagent.txt "<SUBAGENT_PROMPT>"`
3) Write the subagent output into DOC_PATH (anti-fragile placement):
   - If `<!-- arch_skill:block:gaps_concerns:start -->` … `<!-- arch_skill:block:gaps_concerns:end -->` exists: replace the content inside it.
   - Else if a "Gaps & Concerns" section exists (heading match): replace that section.
   - Else insert near the end of the doc, before the Decision Log if present, otherwise append.
   Wrap the inserted block with:
   - `<!-- arch_skill:block:gaps_concerns:start -->`
   - `<!-- arch_skill:block:gaps_concerns:end -->`

SUBAGENT OUTPUT FORMAT (MUST MATCH EXACTLY):
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

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
