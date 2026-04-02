---
description: "Goal loop iterate: execute ONE bet, append to the running log, and compound learning (anti-sidetrack, no-reruns)."
argument-hint: "<Optional: include docs/<...>.md to pin DOC_PATH. Otherwise it will infer the most recent GOAL_LOOP doc.>"
---
# /prompts:goal-loop-iterate — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
$ARGUMENTS is freeform steering (intent, constraints, random notes). Infer what you can.

Operating mode (non-negotiable):
- **Iteration velocity + compounding learning**.
- We are not writing a scientific paper; we are converging by tight loops.

CRITICAL: Running Log / Worklog is first-class (non-negotiable)
- The **WORKLOG_PATH is the memory** of what was already tried and learned.
- Every run of this prompt MUST:
  1) read WORKLOG_PATH first (de-dupe),
  2) avoid redoing work already recorded there,
  3) append exactly one new iteration entry.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

Anti-check-spiral policy (hard):
- Checks exist only if they change a decision, validate the current bet, or prevent a likely regression.
- No “full suite” runs unless the bet explicitly requires it.
- No broad call-site audits unless the bet explicitly is “do an audit”.

---

## 0) Resolve DOC_PATH + WORKLOG_PATH

1) Resolve DOC_PATH:
   - If $ARGUMENTS contains a `docs/<...>.md` path, use it.
   - Else, infer the most recent goal loop doc:
     - Prefer `docs/GOAL_LOOP_*.md` excluding `*_WORKLOG.md`.
     - If multiple candidates are plausible, ask once with the top 2–3.

2) Derive WORKLOG_PATH from DOC_PATH:
   - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

3) If WORKLOG_PATH is missing:
   - Create it using the template in `/prompts:goal-loop-new`.
   - Add cross-links between doc and worklog.

---

## 1) Required-elements + confirmation gate (self-heal where safe)

Before running an iteration, ensure DOC_PATH is **confirmed** and has the required controller blocks:

Confirmation gate (required; do not skip):
- If DOC_PATH frontmatter `status:` is `draft` (or missing/unknown), DO NOT run an iteration.
- Instead: ask the user to confirm/correct the drafted North Star and instruct to run `/prompts:goal-loop-new DOC_PATH`.
- Only proceed with iterations once `status: active`.

Required controller blocks:
- `goal_loop:block:contract`
- `goal_loop:block:anti_sidetrack`
- `goal_loop:block:scoreboard`
- `goal_loop:block:levers`
- `goal_loop:block:iteration_protocol`
- `goal_loop:block:de_dupe`

If any are missing or still placeholders:
- Run the minimal “bootstrap in-place” behavior:
  - fill/repair the missing blocks
  - keep them short (controller-style)
  - do NOT ask for confirmation by default
  - only ask a question if it’s truly a product/UX decision or external unknown

---

## 2) Iteration protocol (ONE bet)

Do this sequence in order, every time:

1) Re-read DOC_PATH controller blocks (treat as law):
   - Contract
   - Anti-sidetrack
   - Scoreboard

2) Read WORKLOG_PATH first (de-dupe):
   - Read the last 1–3 iteration entries.
   - Extract:
     - what bets already ran,
     - what evidence was produced,
     - what changed (files/commands),
     - the current best belief and the last “next bet”.
   - **If the next bet you’re about to choose already appears in the worklog**, do not redo it:
     - change ONE lever,
     - add ONE disambiguating trap/negative proof,
     - or move to the next best bet.

3) Pick ONE bet (highest info gain, best lever for North Star):
   - Write the bet in 1–2 sentences.
   - Pre-commit the decision rule (pass/fail), in plain English.
   - Define the smallest credible evidence signal you will run/produce.

4) Execute the minimum work for the bet:
   - Make the smallest change that answers the question or moves the lever.
   - Temporary instrumentation is allowed if it is the fastest path to disambiguate.
   - If you discover tangents:
     - add them to the Parking Lot in WORKLOG_PATH with anchors,
     - then return to the bet immediately.

5) Run the smallest credible evidence signal:
   - Prefer existing targeted tests/checks/queries.
   - If none exist, use a minimal manual checklist or a diagnostic signature directly tied to the bet.
   - Do not run more checks “to feel safe”.

6) Append exactly one WORKLOG entry (required):
   - timestamp (local)
   - iteration number (increment if possible)
   - bet + decision rule
   - what changed (files touched)
   - commands run
   - artifacts produced (logs, screenshots, query results)
   - result (raw facts)
   - conclusion (what we believe now, why)
   - learnings (durable; also add to Key Learnings Ledger if truly durable)
   - next bet (exactly ONE)
   - parking lot updates (if any)

7) Update DOC_PATH “Loop State” block (short):
   - Current best belief
   - Biggest uncertainty
   - Next bet
   - Last updated timestamp
   Keep it short; details stay in WORKLOG_PATH.

Stop conditions (do not plow ahead):
- If progress requires a true product/UX decision not encoded in repo/docs: ask one well-formed question with options + recommendation.
- If a locked invariant in DOC_PATH is violated: stop and fix immediately, then re-run the smallest check that catches it.
- If access/permissions block progress: ask for the missing access explicitly.

---

## Output to the user (console only; USERNAME-style)

Communicate naturally in English, but include:
- North Star reminder (1 line)
- Punchline (1 line): what this iteration proved/shipped
- What changed this iteration (high level)
- What we learned (1–3 bullets max)
- Next bet (ONE)
- Pointers: DOC_PATH + WORKLOG_PATH (details live in the worklog)
