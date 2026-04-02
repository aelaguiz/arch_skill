---
description: "Goal loop flow status: check DOC_PATH + running log readiness and recommend the single best next /prompts:* step."
argument-hint: "<Optional: docs/<...>.md path. If omitted, it infers the most recent GOAL_LOOP doc.>"
---
# /prompts:goal-loop-flow — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Console output should be short and high-signal; see OUTPUT FORMAT for required content.

$ARGUMENTS is freeform steering. Infer what you can.

Operating mode (non-negotiable):
- **Iteration velocity + compounding learning**.
- This prompt is read-only routing; it should not “teach the whole process” or bloat context.

CRITICAL: Running Log / Worklog is first-class
- If WORKLOG_PATH is missing, we are not iteration-safe after restarts.
- The next step should usually be to create/repair the worklog (bootstrap) before iterating.

Question policy (strict):
- You MUST answer anything discoverable from repo files; do not ask me.
- Allowed questions only:
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions

Read-only:
- Do NOT modify code or docs.

---

## 0) Resolve DOC_PATH + WORKLOG_PATH

DOC_PATH:
- If $ARGUMENTS contains a `docs/<...>.md` path, use it.
- Else prefer the most recent `docs/GOAL_LOOP_*.md` excluding `*_WORKLOG.md`.
- If ambiguous, ask once with the top 2–3 candidates.

WORKLOG_PATH:
- `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

---

## 1) Readiness checklist (evidence-based; no vibes)

Required controller blocks in DOC_PATH:
- `goal_loop:block:contract`
- `goal_loop:block:anti_sidetrack`
- `goal_loop:block:scoreboard`
- `goal_loop:block:levers`
- `goal_loop:block:iteration_protocol`
- `goal_loop:block:de_dupe`

Checklist output format (required; full list):
- Print a "Goal Loop checklist" section.
- Include EVERY line below with a status prefix:
  - `- [DONE] ...` / `- [PENDING] ...` / `- [UNKNOWN] ...`
- Each line must include an evidence note:
  - `— evidence: <marker present>` / `— evidence: missing <marker>` / `— evidence: file missing`

Checklist items:
1) DOC_PATH exists and is readable
2) WORKLOG_PATH exists (restart safety)
3) North Star confirmed (`status: active` in DOC_PATH frontmatter)
4) Contract block present
5) Anti-sidetrack block present
6) Scoreboard block present
7) Levers block present
8) Iteration protocol block present
9) De-dupe block present
10) At least one iteration entry exists in WORKLOG_PATH (optional; informational)

---

## 2) Choose the single best next prompt

Selection rule:
- If DOC_PATH is missing or any required block is missing → recommend `/prompts:goal-loop-new DOC_PATH` (or run without DOC_PATH to create one).
- Else if DOC_PATH is `status: draft` (or missing/unknown) → recommend `/prompts:goal-loop-new DOC_PATH` (confirm North Star first).
- Else if WORKLOG_PATH is missing → recommend `/prompts:goal-loop-new DOC_PATH` (worklog is required for restart safety).
- Else → recommend `/prompts:goal-loop-iterate DOC_PATH`

Always print the exact next command with DOC_PATH filled in.

---

OUTPUT FORMAT (console only; USERNAME-style; keep it short):
- North Star reminder (1 line; from DOC_PATH if possible, otherwise “set up the goal loop controller”)
- Punchline (1 line): the exact next command to run
- DOC_PATH + WORKLOG_PATH
- Goal Loop checklist (full; every line)
- Next command to run (exact `/prompts:*` invocation)
