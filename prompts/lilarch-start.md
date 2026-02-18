---
description: "lilarch 01) Start: small-feature intake → create/repair plan doc with North Star + requirements + minimal grounding."
argument-hint: "<Paste a small feature/improvement request. Optional: include docs/<...>.md to reuse an existing plan doc.>"
---
# /prompts:lilarch-start — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output should be short and high-signal (no logs); see OUTPUT FORMAT for required content.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2–3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.

# COMMUNICATING WITH USERNAME (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH, not in console output.

## What lilarch is (and isn’t)
`lilarch` is a **small-feature** version of the `arch` flow. It compresses:
- “new” + initial grounding + requirements capture → `lilarch-start`
- deep-dive plan + audits (internal + external) → `lilarch-plan`
- implement + review → `lilarch-finish`

This is NOT for new architectures or big migrations. It is for changes you can realistically ship in **1–3 phases**.

### Fit check (warn-first; do NOT hard-block)
Before writing anything, do a quick “is this too big?” check from $ARGUMENTS + a light repo scan:

Prefer **full arch flow** if ANY of these are true:
- The work implies **4+ phases**, or a broad migration/cutover/deletes sweep across many subsystems.
- You expect significant ambiguity/iteration in the plan (multiple competing approaches).
- The change touches correctness-critical domains where best practices materially affect design (security/crypto/payments/offline/concurrency/distributed systems).
- You will need multiple checkpoints / reviews.
Recommend: `/prompts:arch-new ...` → `/prompts:arch-flow ...` (regular flow).

Prefer the **bugs flow** if ANY of these are true:
- Root cause is unknown and investigation dominates the work.
- You primarily have symptoms, logs, and “why is this happening?” uncertainty.
Recommend: `/prompts:bugs-analyze ...` (then bugs-fix/review).

If it looks too large, warn clearly in console output and recommend switching. You may still create a doc as a bootstrap, but do not pretend lilarch is the right fit.

## DOC_PATH
- If $ARGUMENTS includes a `docs/<...>.md` path, use it.
- Otherwise create a new plan doc under `docs/USERNAME/` (create the directory if missing).
  - Naming rule:
    - `docs/USERNAME/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
    - TITLE_SCREAMING_SNAKE = derived from the blurb as a short 5–9 word title, uppercased, spaces → `_`, punctuation removed.
    - Date = today in `YYYY-MM-DD` (determine via `date +%F`; no user input).

Single-document rule:
- All planning/decisions live in DOC_PATH (no extra plan docs).

Documentation-only (planning):
- This prompt creates/edits docs only. DO NOT modify code.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

## Goal
After this prompt:
- North Star is **clear and falsifiable** (not vibes).
- Requirements are explicit (and include “won’t do” non-requirements).
- Key decisions are made with a recommended default path (opinionated).
- Any remaining clarifying questions are explicitly listed, and you ask the user to answer them.
- Minimal grounding exists (internal anchors + patterns; external best-practices only if truly needed).

## Procedure
1) Resolve DOC_PATH (create if needed) and ensure it contains the blocks below.
2) Draft/repair the TL;DR + North Star so they are immediately usable.
3) Fill/update the Requirements & Decisions block (opinionated defaults + clarifying questions).
4) Add minimal Research Grounding:
   - Internal ground truth anchors + reusable patterns (file paths; code as spec).
   - External best practices ONLY if needed (keep it tight; include sources).
5) STOP and ask clarifying questions that must be answered. Do not proceed to planning/implementation without answers.
6) Once the user answers and confirms the North Star/requirements, update `status:` in frontmatter from `draft` → `active`.

## Doc update rules (anti-fragile)
- Always prefer block markers if present; otherwise update in place by semantically matching headings; otherwise insert new top-level sections.
- If the doc uses numbered headings, preserve existing numbering; do not renumber the rest of the document.
- Do not paste the full doc to the console.

## Document blocks (write/update these)

### (A) Requirements & Decisions block
Placement rule (in order):
1) If `<!-- lilarch:block:requirements:start -->` exists, replace inside it.
2) Else insert after the North Star section if present, otherwise after TL;DR, otherwise after YAML front matter.

<!-- lilarch:block:requirements:start -->
# Requirements & Decisions (lilarch)

## Requirements (must)
- <requirement>

## Non-requirements (explicitly won’t do)
- <non-goal>

## Defaults (opinionated; we will do this unless you object)
- <decision> — because <why>

## Clarifying questions (must answer before `lilarch-plan`)
- Q1: <question> (default: <your recommended answer>)
- Q2: <question> (default: <your recommended answer>)
<!-- lilarch:block:requirements:end -->

### (B) Research Grounding block (minimal)
Write/update (use the same block marker shape as the arch flow, for compatibility):

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

### (C) Optional External Research block (ONLY if needed)
If you do web research, record it with sources (links) using this shape:

<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)
## Topics researched (and why)
- <topic> — <why it applies>

## Findings + how we apply them
### <Topic>
- Recommended default for this plan:
  - <bullet>
- Pitfalls / footguns:
  - <bullet>
- Sources:
  - <title> — <url> — <why it’s authoritative>
<!-- arch_skill:block:external_research:end -->

## If creating a new doc: initial template
If DOC_PATH did not exist, initialize it with this compact template (fill TL;DR + North Star; do not leave placeholders there):

---
title: "<PROJECT> — <CHANGE> — lilarch Plan"
date: <YYYY-MM-DD>
status: draft | active | complete
fallback_policy: forbidden
owners: [USERNAME]
reviewers: []
doc_type: lilarch_change
related: []
---

# TL;DR
- **Outcome:** <one sentence, falsifiable>
- **Problem:** <one sentence>
- **Approach:** <one sentence>
- **Plan:** <1–3 phases in 1 line>
- **Non-negotiables:** <3–7 bullets>

# North Star
## The claim (falsifiable)
> <If we do X, then Y is true, measured by Z, by date/condition W>

## In scope
- UX surfaces (what users will see change):
  - <screen/state/flow>
- Technical scope (what code will change):
  - <module/contract/boundary>

## Out of scope
- UX surfaces (what users must NOT see change):
  - <screen/state/flow>
- Technical scope (explicit exclusions):
  - <module/boundary we will not touch>

## Definition of done (acceptance evidence)
- <observable acceptance criteria, not vibes>
- Smallest credible signal (prefer existing checks):
  - Primary: <existing test/check OR log signature OR manual checklist>
  - Optional: <second signal only if truly needed>

## Key invariants (fix immediately if violated)
- <invariant>

---

# Decision Log (append-only)
## <YYYY-MM-DD> — Plan started
- Context: <why now>
- Decision: use lilarch flow
- Notes: <anything important>

## STOP and ask the user
After updating DOC_PATH, ask the clarifying questions from the Requirements block and ask for a “yes/no” North Star confirmation.
Do not proceed to `lilarch-plan` until those are answered.

OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line; what you need from USERNAME right now)
- What you updated/created (DOC_PATH)
- The clarifying questions you need answered (and their defaults)
- Next action (usually: user answers → then run `/prompts:lilarch-plan DOC_PATH`)
