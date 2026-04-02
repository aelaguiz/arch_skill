---
description: "Goal loop context load: write a short Context Digest from DOC_PATH + running log so restarts don’t redo work."
argument-hint: "<Optional: include docs/<...>.md to pin DOC_PATH.>"
---
# /prompts:goal-loop-context-load — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Console output should be short and high-signal; see OUTPUT FORMAT for required content.

$ARGUMENTS is freeform steering. Infer what you can.

Operating mode (non-negotiable):
- **Iteration velocity + compounding learning**.
- This prompt exists to prevent “restart amnesia” and **avoid redoing work**.

CRITICAL: Running Log / Worklog is first-class
- The worklog is the memory and must be read first in future iterations.
- This digest should point to worklog entries; it must not replace them.

Question policy (strict):
- You MUST answer anything discoverable from repo files; do not ask me.
- Allowed questions only:
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions

Documentation-only:
- MUST NOT modify production code.
- MAY update DOC_PATH by inserting/replacing a Context Digest block.
- Do not create additional planning docs.

---

## Procedure (keep it tight)

1) Resolve DOC_PATH:
   - If $ARGUMENTS contains a `docs/<...>.md` path, use it.
   - Else infer the most recent `docs/GOAL_LOOP_*.md` excluding `*_WORKLOG.md`.
   - If ambiguous, ask once with the top 2–3 candidates.

2) Derive WORKLOG_PATH:
   - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

3) Read DOC_PATH controller blocks:
   - Contract (North Star + invariants)
   - Anti-sidetrack
   - Scoreboard
   - Loop State (if present)

4) Read WORKLOG_PATH if it exists:
   - Summarize the last 1–3 iteration entries:
     - bet attacked
     - smallest evidence signal run
     - result + conclusion
     - next bet
   - Extract:
     - Key Learnings Ledger (last ~5 bullets)
     - Parking Lot (open items)
   If WORKLOG_PATH is missing, call it out in the digest (restart safety risk).

5) Write/update the Context Digest block in DOC_PATH (idempotent; replace in place).

---

DOC UPDATE RULES (anti-fragile)
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- goal_loop:block:context_digest:start -->` … `<!-- goal_loop:block:context_digest:end -->`
2) Else insert immediately after the TL;DR section if present.
3) Else insert immediately after YAML front matter if present.
4) Else insert at the top of the document.

Keep the digest concise and skimmable; details live in WORKLOG_PATH.

DOCUMENT INSERT FORMAT (write into DOC_PATH; do not paste full block to console):

<!-- goal_loop:block:context_digest:start -->
# Context Digest (restart-safe)
Updated: <YYYY-MM-DD HH:MM>

## North Star (1–2 sentences)
<one-liner claim + acceptance signal>

## Scoreboard snapshot
- Acceptance signal(s):
  - <item>
- Guardrails:
  - <item>

## Current state (what we believe / what we’ll do next)
- Current best belief:
- Biggest uncertainty:
- Next bet (ONE):

## Recent iterations (from WORKLOG_PATH)
- <Iteration N> — <bet> — <result/conclusion> — evidence: <worklog heading anchor>
- <Iteration N-1> — ...

## Key learnings (durable)
- <learning> — evidence: <worklog entry>

## Parking lot (deferred tangents; anchors included)
- <item> — anchors: <paths/commands>

## Restart rule (do not redo work)
- Before doing work: open WORKLOG_PATH and confirm the bet is not already attempted.
- If it was attempted: change ONE lever or move to the next bet (no reruns).
<!-- goal_loop:block:context_digest:end -->

---

OUTPUT FORMAT (console only; USERNAME-style; keep it short):
- North Star reminder (1 line)
- Punchline (1 line): context digest updated
- What changed (DOC_PATH only)
- Next action (usually `/prompts:goal-loop-iterate DOC_PATH`)
- Pointers: DOC_PATH + WORKLOG_PATH

