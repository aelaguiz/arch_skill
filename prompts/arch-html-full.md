---
description: "16) Arch HTML (full fidelity): render doc with zero omissions."
argument-hint: <doc path or guidance>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: Generate a clean, static HTML view of an architecture doc using the framework in
`arch_skill/templates/arch_doc_template.html`, with ZERO omissions (every line of source content must appear somewhere).

1) Resolve DOC_PATH:
   - If $ARGUMENTS includes a docs/<...>.md path, use it.
   - Otherwise infer the most relevant arch doc from $ARGUMENTS + conversation.
   - If ambiguous, ask the user to choose from the top 2–3 candidates.

2) Use a subagent (Codex CLI) to produce HTML:
   - Model: gpt-5.2
   - Reasoning: xhigh
   - The subagent must:
     - Read DOC_PATH fully.
     - Read `arch_skill/templates/arch_doc_template.html` and follow its structure.
     - Produce a static HTML file (no React/JS interactivity).
     - Preserve full content with ZERO omissions.
     - If any text does not fit a section, include it in a final “Unclassified content” block.
     - Append a final “Full Source (verbatim)” appendix that includes the entire doc inside a <pre>.
     - Output ONLY the HTML.

   Command:
   `codex exec --model gpt-5.2 --reasoning-effort high --output-last-message /tmp/arch_html_full.html "<SUBAGENT_PROMPT>"`

3) Write output to:
   `docs/prototypes/<DOC_BASENAME>_full.html`
4) Open in Chrome.

OUTPUT FORMAT (console only):
Summary:
- Doc: <path>
- Output: <path>
- Omissions: none (verbatim appendix included)
Next:
- <what to do next>
