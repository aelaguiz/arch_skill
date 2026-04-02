---
description: "Goal loop new: create/repair the Goal Loop SSOT doc + append-only running log (North Star confirmation, autonomy-first, idempotent)."
argument-hint: "<Freeform objective + context. Optional: include a docs/<...>.md path to pin DOC_PATH.>"
---
# /prompts:goal-loop-new — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.

Operating mode (non-negotiable):
- **Iteration velocity + compounding learning** is the objective function for this prompt family.
- This prompt is doc-first: it creates/repairs the loop controller so future iterations run fast and don’t derail.

CRITICAL: Running Log / Worklog is first-class (non-negotiable)
- The **WORKLOG_PATH is the memory** of what was already tried and learned.
- It must be **append-only** (never rewrite prior entries).
- Any future iteration prompt must **read WORKLOG_PATH first** to avoid redoing work after restarts.
- DOC_PATH is the controller; WORKLOG_PATH is the evidence + learnings log.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

Documentation-only (planning/controller setup):
- This prompt creates/edits docs only. DO NOT modify production code here.
- You may run minimal read-only commands (rg, ls, reading files) only when needed to ground the doc.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

CRITICAL: New-doc North Star confirmation (arch-new style)
- When creating a new Goal Loop doc (or when DOC_PATH is still `status: draft`), you MUST:
  1) infer/draft the North Star + scope + out-of-scope from $ARGUMENTS + repo reality (do not leave placeholders there),
  2) then pause and ask the user to confirm/correct the North Star (yes/no),
  3) if the user provides edits, update DOC_PATH and re-ask until the user says “yes”.
- Only after the user confirms “yes” do you set `status: active`.
- This confirmation loop is intentionally short-lived and high-leverage; it prevents fast iterations from compounding in the wrong direction.

Idempotence rules (do not drift / do not duplicate):
- Use the block markers below as the stable API.
- If a block exists, **replace content inside the block** (do not append a second copy).
- Never create a second “plan” doc for the same loop. One DOC_PATH is the SSOT controller.

---

## 0) Resolve DOC_PATH + WORKLOG_PATH

1) Resolve DOC_PATH:
   - If $ARGUMENTS includes a `docs/<...>.md` path, use it.
   - Else if a goal-loop doc already exists, prefer it (choose the most recent by mtime).
   - Else create a new doc using:
     - `docs/GOAL_LOOP_<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
     - TITLE_SCREAMING_SNAKE: 5–9 words derived from the objective; uppercased; spaces → `_`; punctuation removed.
   - If you created a new doc: start it as `status: draft` until the user confirms the North Star.

2) Derive WORKLOG_PATH from DOC_PATH:
   - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

3) Ensure cross-links:
   - DOC_PATH should link to WORKLOG_PATH near the top.
   - WORKLOG_PATH should link back to DOC_PATH at the top.

---

## 1) Create/repair WORKLOG_PATH (append-only memory)

Worklog rules (hard):
- If WORKLOG_PATH does not exist: create it using the template below.
- If it exists:
  - Do NOT rewrite prior entries.
  - You may add missing sections (Key Learnings Ledger, Parking Lot) if absent.
  - Prefer appending new structure at the end instead of rearranging existing content.

WORKLOG TEMPLATE (write to WORKLOG_PATH; do not paste to console):

---
title: "<Same title as DOC_PATH> — Worklog"
date: <YYYY-MM-DD>
status: active
related:
  - <DOC_PATH>
---

# Worklog (append-only)

This is the **append-only running log** for:
- `<DOC_PATH>`

It is the memory that prevents redoing work after restarts.

Rules:
- Never rewrite old entries; only append.
- Every iteration appends exactly one entry with: bet, decision rule, evidence, result, learnings, next bet.

---

## Key Learnings Ledger (append-only)

Append bullets here only when a learning is durable and changes future decisions.
- <YYYY-MM-DD> — <learning> — evidence: <worklog entry anchor / file / command>

---

## Parking Lot (anti-sidetrack)

If something is important but out-of-scope for the current bet, park it here with anchors.
- <item> — anchors: <paths/commands> — why deferred: <reason>

---

## Iteration Entries (append-only)

### <YYYY-MM-DD HH:MM> — Iteration <N> — <Short bet name>
- Bet:
- Decision rule (pre-committed):
- Scope (what we changed):
- Work performed:
- Evidence (tests/queries/artifacts):
- Result (raw facts):
- Conclusion:
- Learnings:
- Next bet:
- Parking lot updates (if any):

---

## 2) Create/repair DOC_PATH controller blocks

DOC_PATH must contain all required controller blocks below.
If any block is missing, create it.
If present but placeholder/contradictory, fix it.

Required blocks (must exist):
- `<!-- goal_loop:block:contract:start --> … end -->`
- `<!-- goal_loop:block:anti_sidetrack:start --> … end -->`
- `<!-- goal_loop:block:scoreboard:start --> … end -->`
- `<!-- goal_loop:block:levers:start --> … end -->`
- `<!-- goal_loop:block:iteration_protocol:start --> … end -->`
- `<!-- goal_loop:block:de_dupe:start --> … end -->`
- Optional but recommended:
  - `<!-- goal_loop:block:state:start --> … end -->` (1-page current state)
  - `<!-- goal_loop:block:context_digest:start --> … end -->` (for restarts / context compression)

DOC TEMPLATE (write/update in DOC_PATH; do not paste the full doc to console):

---
title: "<PROJECT> — <NORTH STAR> — Goal Loop"
date: <YYYY-MM-DD>
status: draft | active | complete
owners: [<name>, ...]
reviewers: [<name>, ...]
doc_type: goal_loop
related:
  - <links to relevant docs, code, dashboards, etc>
worklog:
  - <WORKLOG_PATH>
---

# TL;DR

- **North Star:** <1 sentence; falsifiable>
- **Operating mode:** iteration velocity + compounding learning
- **What we do every iteration:** read contract → read worklog (de-dupe) → pick ONE bet → minimal work + smallest credible signal → append worklog → tighten next bet

---

<!-- goal_loop:block:contract:start -->
## Contract (read this every iteration)

### North Star (falsifiable claim)
> If we do X, then Y becomes true, measured by Z, by condition/date W.

### Operating Mode
- Iteration velocity + compounding learning is the objective function.
- Prefer the best lever for the North Star over the closest fix (avoid local maxima).

### Non-negotiables / invariants
- <invariants that must hold; if broken, fix immediately>

### Stop conditions (when to ask the user / stop the line)
- A true product/UX decision is required and not encoded anywhere.
- External access/permissions are missing.
- A locked invariant is violated and cannot be repaired autonomously.
<!-- goal_loop:block:contract:end -->

---

<!-- goal_loop:block:anti_sidetrack:start -->
## Anti-sidetrack contract (law)

### Out of scope
- <explicitly out-of-scope items>

### Anti-goals (tempting, but forbidden)
- Do not do exhaustive audits “just in case”.
- Do not run full test suites unless the current bet requires it.
- Do not start refactors that do not directly unblock the current bet.

### Parking Lot rule
- If you discover a tangent: add it to WORKLOG_PATH → Parking Lot with anchors, then resume the bet.
<!-- goal_loop:block:anti_sidetrack:end -->

---

<!-- goal_loop:block:scoreboard:start -->
## Scoreboard (how we know we’re done)

### Acceptance signal(s)
- Primary: <what “done” means; observable>

### Guardrails (what would make us stop/rollback)
- <guardrail> — <threshold> — evidence source: <test/query/log>

### Evidence sources (what counts)
- Prefer existing tests/queries/dashboards/log signatures.
- Avoid “proof burdens” that don’t change a decision.
<!-- goal_loop:block:scoreboard:end -->

---

<!-- goal_loop:block:state:start -->
## Loop State (1 page; overwrite as we learn)
- Current best belief:
- Biggest uncertainty:
- Next bet:
- Last updated:
<!-- goal_loop:block:state:end -->

---

<!-- goal_loop:block:levers:start -->
## Lever inventory (small; 5–15 max)

Ranked candidates (best lever first):
1) <lever> — why it moves North Star — smallest credible test/signal
2) <lever> — ...
<!-- goal_loop:block:levers:end -->

---

<!-- goal_loop:block:iteration_protocol:start -->
## Iteration protocol (idempotent; repeat forever)

Rules:
- One iteration = **one bet** = one main lever change.
- No reruns: do not repeat an identical test/config hoping for a different result.
- Running log is authoritative: read WORKLOG_PATH first; append one entry per iteration.

Protocol:
1) Re-read Contract + Anti-sidetrack + Scoreboard.
2) Read the last 1–3 WORKLOG entries and ensure you’re not redoing work.
3) Choose ONE bet and pre-commit a decision rule.
4) Do the minimum work to ship/test that bet.
5) Run the smallest credible evidence signal.
6) Append a WORKLOG entry with evidence + learnings + next bet.
7) Update Loop State (short) only if evidence changes the best belief/next bet.
<!-- goal_loop:block:iteration_protocol:end -->

---

<!-- goal_loop:block:de_dupe:start -->
## De-dupe / Do-not-redo (restart safety)

Before doing work:
- Open WORKLOG_PATH.
- If the same bet/lever was already attempted:
  - Do not redo it.
  - Either change ONE lever, add ONE disambiguating trap, or move to the next best bet.
<!-- goal_loop:block:de_dupe:end -->

---

## 3) Output (console only; USERNAME-style)

OUTPUT FORMAT (console only; communicate naturally in English):
- North Star reminder (1 line)
- Punchline (1 line):
  - If DOC_PATH is `status: draft`: ask the user to confirm/correct the drafted North Star (yes/no)
  - If DOC_PATH is `status: active`: doc/worklog are ready for iterations
- What you created/changed (brief)
- Next action:
  - If `status: draft`: re-run bootstrap after edits until confirmed (then we can iterate)
  - If `status: active`: run `/prompts:goal-loop-iterate DOC_PATH`
- Pointers: DOC_PATH + WORKLOG_PATH
