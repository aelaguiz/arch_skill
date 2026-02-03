---
description: "05) UI ASCII: current-target mockups (if UI)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-ui-ascii — $ARGUMENTS
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

Alignment checks (keep it light before adding UI ASCII)
- North Star: concrete + scoped, with a smallest-credible acceptance signal.
- UX scope: explicit in-scope / out-of-scope (what users see changes vs does not change).
If either is missing or contradictory, pause and ask for a quick doc edit before proceeding.
If the change touches UI/UX, add ASCII mockups for current and target states in DOC_PATH.
Keep them contract-level, not illustrative.
Write/update the ASCII blocks into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If marker blocks exist, replace content inside them:
   - `<!-- arch_skill:block:ui_ascii_current:start -->` … `<!-- arch_skill:block:ui_ascii_current:end -->`
   - `<!-- arch_skill:block:ui_ascii_target:start -->` … `<!-- arch_skill:block:ui_ascii_target:end -->`
2) Else, if the doc has "Current Architecture"/"As-is" and "Target Architecture"/"To-be" sections, add a `## UI surfaces (ASCII)` subsection under each (or update it if it exists).
3) Else, append a standalone `# UI Surfaces (ASCII)` section near the architecture content with both blocks.
Do not paste the full blocks to the console.

DOCUMENT INSERT FORMAT (use wherever it fits best per the rules above):
<!-- arch_skill:block:ui_ascii_current:start -->
Current UI ASCII:
```ascii
<ASCII mockups for current UI states>
```
<!-- arch_skill:block:ui_ascii_current:end -->

<!-- arch_skill:block:ui_ascii_target:start -->
Target UI ASCII:
```ascii
<ASCII mockups for target UI states>
```
<!-- arch_skill:block:ui_ascii_target:end -->

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
