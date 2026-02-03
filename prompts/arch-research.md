---
description: "03) Research grounding: external + internal anchors."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-research — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):

- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.


# COMMUNICATING WITH USERNAME (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to ground the doc.
- If you discover code changes we likely need, write them into DOC_PATH as plan items with file anchors (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Alignment check: North Star (keep it light)
- Concrete + scoped: state a clear claim and the smallest credible acceptance signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Avoid inventing new harnesses/frameworks by default.
- Coherent: in-scope/out-of-scope does not contradict the TL;DR/plan.
If unclear or contradictory, pause and ask for a quick doc edit before proceeding.

Alignment check: UX scope (keep it light)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If unclear or contradictory, pause and ask for a quick doc edit before proceeding.

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

OUTPUT FORMAT (console only; USERNAME-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did / what changed
- Issues/Risks (if any)
- Next action
- Need from USERNAME (only if required)
- Pointers (DOC_PATH / WORKLOG_PATH / other artifacts)
