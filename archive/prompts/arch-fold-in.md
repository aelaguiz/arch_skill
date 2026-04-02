---
description: "Optional) Fold in references: inline reference docs/links into DOC_PATH and wire them into phases so implementation can’t miss them."
argument-hint: "<Paste a blurb that includes the plan doc path (optional) plus any number of reference doc paths/URLs. Example: docs/PLAN.md docs/spec.md docs/ux.md https://… “Fold these in; Phase 2 must obey the UX contract.”>"
---
# /prompts:arch-fold-in — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.

$ARGUMENTS is freeform steering (intent + constraints + refs). There are NO required flags/tags/modes.

Resolve inputs from the blurb (no friction):
- DOC_PATH: infer the *single* plan doc we will update.
- REFS: every other doc/link in the blurb (and any obvious ref links already in DOC_PATH) that should be folded into the plan.

Question policy (strict):
- You MUST answer anything discoverable from the referenced docs/links by reading them; do not ask.
- Allowed questions only:
  - Doc-path ambiguity you truly cannot resolve (top 2–3 candidates)
  - Missing access/permissions (can’t read a referenced file, or URL requires auth)
  - A critical UX/product decision is required and is truly missing from ALL provided materials (rare; include your default)
- If you think you need to ask, first state what you read/looked at; ask only after exhausting evidence.


# COMMUNICATING WITH USERNAME (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, long excerpts) in DOC_PATH, not in console output.


Documentation-only (planning):
- This prompt edits markdown documentation only. DO NOT modify code.
- Apply the single-document rule: fold the reference material into DOC_PATH so implementation can’t miss it.
- Do not create additional planning docs.
- Do not commit/push unless explicitly requested in $ARGUMENTS.


## North Star (authoritative)
When reference materials live “out of line” (separate docs, diagrams, best-practice notes), they get missed during implementation.
Fix that by folding them *into the plan doc itself* and wiring them into the relevant phases as explicit “must satisfy” obligations.


## Procedure (do this order; keep it deterministic)

### 1) Resolve DOC_PATH + REFS from $ARGUMENTS (no flags)
1) Extract all candidate paths/URLs from $ARGUMENTS:
   - Local files/folders: things that look like paths (prefer real paths that exist on disk).
   - URLs: http/https links.
2) Identify Markdown/text docs mentioned explicitly:
   - Treat `.md`, `.mdx`, `.txt`, `.rst`, `.adoc` as doc candidates.
   - Ignore code paths by default (`.ts`, `.tsx`, `.dart`, `.kt`, `.java`, `.py`, etc.) — those are anchors, not “refs to fold”.
3) Pick DOC_PATH (single plan doc) using best-effort scoring (do not ask unless truly ambiguous):
   - Strong signals (prefer):
     - contains any `<!-- arch_skill:block:` markers
     - contains `Holistic North Star` and `# TL;DR`
     - has YAML frontmatter with `status:` / `doc_type:`
   - Anti-signals:
     - `*_WORKLOG.md` (never pick as DOC_PATH)
     - repo guides/indexes like `docs/arch_skill_usage_guide.md` (avoid unless user explicitly points at it as the plan)
   - If multiple candidates still tie, ask USERNAME to choose from the top 2–3 (and stop).
   - If no doc candidates were provided:
     - Search `docs/` for likely plan docs (exclude `*_WORKLOG.md`) and pick the most recently modified plan-like doc.
     - If still not credible, stop and ask for DOC_PATH explicitly.
4) Define REFS:
   - REFS = (all extracted doc paths/URLs) MINUS DOC_PATH.
   - Also include “obvious reference materials” already listed in DOC_PATH frontmatter `related:` (if present) and any “References/Design/Spec” links in the doc.
   - Do NOT recursively pull in every `docs/...` mention; only treat it as a reference if it’s clearly being used as a spec/design/best-practices input.

### 2) Read DOC_PATH fully; locate the phases
- Read DOC_PATH end-to-end.
- Locate the phase plan section (best effort):
  - Prefer the block markers:
    - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
  - Otherwise find a heading that contains “Phase Plan” / “Phased Implementation”.
- Extract the phases as they exist in the doc:
  - Typical shape: `## Phase <n> — <name>`
  - If no phases exist yet, that’s OK — we will still fold the references and provide a phase-alignment suggestion.

### 3) Ingest every reference material (do not “hand-wave”)
For each ref in REFS:
- If it’s a local file:
  - Read it fully (for folders: recursively include likely docs inside).
  - Record a stable identifier `R1`, `R2`, … and keep a source pointer (path).
- If it’s a URL:
  - Fetch it and extract the human-readable content as best as possible.
  - If it requires auth or can’t be fetched, stop and ask USERNAME to paste the content or provide an export (do not guess).
- If it’s an image/diagram:
  - Embed it (markdown image link if local) AND extract a textual “UX contract”:
    - states, transitions, copy constraints, acceptance criteria, and any “must not change” notes.

For each `R#`, produce TWO layers:
1) **Binding obligations (distilled):** the parts implementation must satisfy (invariants, requirements, UX contract, edge cases, “must nots”).
2) **Folded source (verbatim):** inline the source content into DOC_PATH so it can’t be missed.
   - Keep it readable by nesting under `R#` headings.
   - When inlining a Markdown doc verbatim, wrap it so it doesn’t break the plan’s heading structure:
     - Prefer a fenced block with tildes:
       - `~~~~markdown`
       - <verbatim content>
       - `~~~~`

### 4) Phase-align the obligations (no extra questions)
Goal: make it impossible to implement a phase without seeing the relevant constraints.

Phase alignment rules:
- If $ARGUMENTS explicitly mentions “Phase X” guidance, honor it.
- Otherwise, map refs to phases by best-effort keyword/ownership matching:
  - UX refs → phases that change UI/flows/interaction behavior
  - API/contract refs → foundation phases that define/lock contracts
  - Migration/deletes refs → cleanup/consolidation phases
- If uncertain: treat the obligation as “Global (all phases)” rather than asking a question.

Output of this step:
- A per-phase “Reference obligations (must satisfy)” bullet list.
- A global “Non-negotiables from references” list (if any).

### 5) Write/update DOC_PATH (idempotent; stable marker)
Insert/replace this block in DOC_PATH:
1) If the marker exists, replace the content inside it:
   - `<!-- arch_skill:block:reference_pack:start -->` … `<!-- arch_skill:block:reference_pack:end -->`
2) Else, insert near the phase plan section:
   - Prefer immediately before the phase plan section,
   - otherwise immediately after it,
   - otherwise after Research Grounding / External Research,
   - otherwise after TL;DR/North Star.

Also, if DOC_PATH has YAML frontmatter with `related:`, ensure all REFS are listed there (deduped). Do not invent unrelated links.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:reference_pack:start -->
# Reference Pack (folded materials; phase-aligned)
Updated: <YYYY-MM-DD>

## Inventory
- R1 — <title> — <source path/URL>
- R2 — <title> — <source path/URL>

## Binding obligations (distilled; must satisfy)
- <obligation> (From: R#)

## Phase alignment (must satisfy per phase)
### Global (applies across phases)
- <obligation> (From: R#)

### Phase 1 — <phase name (from the plan, if present)>
- Reference obligations (must satisfy):
  - <obligation> (From: R#)
- References:
  - R#, R#

### Phase 2 — <phase name>
- Reference obligations (must satisfy):
  - <obligation> (From: R#)
- References:
  - R#

## Folded sources (verbatim; inlined so they can’t be missed)
### R1 — <title> — <source>
~~~~markdown
<verbatim content (or extracted text)>
~~~~

### R2 — <title> — <source>
~~~~markdown
<verbatim content (or extracted text)>
~~~~
<!-- arch_skill:block:reference_pack:end -->

### 6) Wire the obligations into the phase plan (when present)
If the doc has a phase plan section:
- For each phase, add/update a bullet named exactly:
  - `* Reference obligations (must satisfy):`
- Populate it with the phase-aligned obligations (each bullet should cite `R#`).
- Do not bloat phases with entire docs; keep phases skimmable and binding.
  - The full verbatim content lives in the Reference Pack block above.


OUTPUT FORMAT (console only; USERNAME-style)
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- DOC_PATH chosen + how many refs were folded
- What changed in DOC_PATH (reference pack inserted + phases wired)
- Any missing/inaccessible refs (if any) + what you need from USERNAME
- Next action (usually: continue planning or proceed to implementation)
