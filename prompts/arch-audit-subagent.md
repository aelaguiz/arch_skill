---
description: "08a) Audit (subagent): code vs plan gaps list."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.

Use a subagent (non‑interactive Codex CLI) to perform the audit, then insert its output into $DOC_PATH.
Do not paste the full gaps list to the console; only summarize and list open questions.

Steps:
1) Build a subagent prompt that:
   - reads $DOC_PATH
   - inspects the current repo code
   - outputs ONLY the canonical “Gaps & Concerns List” block below
2) Run the subagent via `codex exec` (codex model, high reasoning) and capture its final message:
   - `codex exec -m gpt-5-codex -c reasoning_effort="high" --output-last-message /tmp/arch_audit_subagent.txt "<SUBAGENT_PROMPT>"`
3) Replace any existing “Gaps & Concerns List” block in $DOC_PATH; if none exists, insert it immediately **before** the Decision Log.

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
