---
description: "03) Research grounding: external + internal anchors."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-research — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):
- Do NOT ask the user technical questions you can answer by reading code or the plan doc; go look and decide.
- Ask the user only for true product decisions / external constraints not present in the repo/doc, or to disambiguate between multiple equally plausible docs.
- If multiple viable technical approaches exist, pick the most idiomatic default and note alternatives in the doc (do not ask “what do you want to do?”).
Do not ask the user questions during investigation. Resolve by reading more code and searching the repo. Ask only if required by a stop-the-line gate or if required information is not present in the repo/doc and cannot be inferred.

Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to ground the doc.
- If you discover code changes we likely need, write them into DOC_PATH as plan items with file anchors (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line: North Star Gate (must pass before research grounding)
- Falsifiable + verifiable: the North Star states a concrete claim AND the smallest credible pass/fail signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Do NOT invent new harnesses/screenshot frameworks or drift scripts by default.
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before research grounding)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

You are doing research. Good research looks like:
- Internal ground truth (code as spec): concrete file paths + the behaviors/contracts they define (what is authoritative and why).
- Existing patterns to reuse: concrete file paths + a short name for the pattern (so we don't reinvent).
- External anchors (optional): papers/systems/prior art with explicit adopt/reject and why it applies here (no cargo cult).
- Open questions framed as evidence: what information would settle the question; do not leave vague TODOs.

Write/update a Research Grounding section in DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:research_grounding:start -->` … `<!-- arch_skill:block:research_grounding:end -->`
2) Else, if the doc already has a section whose heading contains "Research" or "Grounding" or "Anchors" (case-insensitive), update it in place.
3) Else insert a new top-level "Research Grounding" section:
   - Prefer inserting after the Problem Statement / "What exists today" section if present,
   - otherwise after TL;DR,
   - otherwise after YAML front matter,
   - otherwise at the top.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal “ground truth”)
## External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>

## Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>
