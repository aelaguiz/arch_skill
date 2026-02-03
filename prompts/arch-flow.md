---
description: "00) Flow status: detect where you are in the arch flow and recommend/run the next /prompts:* step."
argument-hint: "<Optional: docs/<...>.md path. Optional: FLOW=regular|mini. Optional: RUN=1 to immediately execute the next step.>"
---
# /prompts:arch-flow — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
$ARGUMENTS is freeform steering. Infer what you can.

# COMMUNICATING WITH USERNAME (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Purpose:
- Read DOC_PATH and infer which arch flow steps are DONE vs PENDING.
- Print a FULL checklist (all steps) and recommend the single best next `/prompts:*` command to run.
- Offer to run the next step:
  - Default: recommend only (no file edits).
  - If `$ARGUMENTS` includes `RUN=1`: immediately execute the next step by loading the next prompt markdown and following it as the procedure.

Safety:
- Default mode is read-only: DO NOT modify code or docs.
- Only do writes if `RUN=1` causes you to run the next prompt (which may write docs/code depending on that prompt).

## 0) Resolve DOC_PATH
- If $ARGUMENTS contains a `docs/<...>.md` path, use it.
- Else, search `docs/` for candidate plan docs (exclude `*_WORKLOG.md`) and pick the top 2–3 most recent by mtime.
  - If ambiguous, ask the user to pick one from those candidates.
- Derive WORKLOG_PATH from DOC_PATH:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

## 1) Infer flow (regular vs mini)
- If $ARGUMENTS includes `FLOW=mini` or the word `mini`, select Mini Flow.
- Else if $ARGUMENTS includes `FLOW=regular`, select Regular Flow.
- Else infer:
  - If DOC_PATH contains `<!-- arch_skill:block:phase1_kickoff:start -->`, select Regular Flow.
  - Else if DOC_PATH contains `<!-- arch_skill:block:phase_plan:start -->` AND does NOT contain `<!-- arch_skill:block:phase1_kickoff:start -->`, select Mini Flow.
  - Else default to Regular Flow.

## 2) Determine step completion (from DOC_PATH / WORKLOG_PATH)
Parse DOC_PATH as plain text and use these evidence rules (no vibes):

Shared signals:
- `status:` in YAML frontmatter:
  - If `status: active` or `status: complete`, treat "North Star confirmed" as DONE.
  - If missing or `status: draft`, treat as PENDING (soft; do not hard-block).
- Kickoff: `<!-- arch_skill:block:phase1_kickoff:start -->`
- Research grounding: `<!-- arch_skill:block:research_grounding:start -->`
- External research: `<!-- arch_skill:block:external_research:start -->` OR planning passes line `external_research_grounding: done`
- Deep dive:
  - Current: `<!-- arch_skill:block:current_architecture:start -->`
  - Target: `<!-- arch_skill:block:target_architecture:start -->`
  - Call-site audit: `<!-- arch_skill:block:call_site_audit:start -->`
- UI ASCII (optional): both
  - `<!-- arch_skill:block:ui_ascii_current:start -->`
  - `<!-- arch_skill:block:ui_ascii_target:start -->`
- Plan enhancer (optional): `<!-- arch_skill:block:plan_enhancer:start -->`
- Phase plan: `<!-- arch_skill:block:phase_plan:start -->`
- Review gate (optional): `<!-- arch_skill:block:review_gate:start -->`
- Gaps & concerns (optional): `<!-- arch_skill:block:gaps_concerns:start -->`
- Implementation vs plan audit (optional): `<!-- arch_skill:block:implementation_audit:start -->`
- Worklog exists: WORKLOG_PATH exists on disk.

## 3) Produce a checklist + choose the next step
Build a complete checklist (DONE/PENDING/OPTIONAL/UNKNOWN) for the selected flow (do not truncate):

Checklist output format (required):
- Print a "Flow checklist" section.
- Include EVERY step line (in order) with a status prefix:
  - `- [DONE] ...` for completed steps
  - `- [PENDING] ...` for required-but-not-done steps
  - `- [OPTIONAL] ...` for optional-and-not-done steps
  - `- [UNKNOWN] ...` only if you truly cannot determine from DOC_PATH/WORKLOG_PATH
- For each line, include a short evidence note like:
  - `— evidence: <marker present>` or `— evidence: missing <marker>` or `— evidence: status: draft`

Regular Flow (recommended):
1) Plan doc exists (DOC_PATH readable)
2) North Star confirmed (soft; based on `status:`)
3) Phase 1 kickoff (`/prompts:arch-kickoff`)
4) Research grounding (`/prompts:arch-research` or `arch-research-agent`)
5) External research (optional; `/prompts:arch-external-research-agent`)
6) Deep dive (`/prompts:arch-deep-dive` or `arch-deep-dive-agent`)
7) UI ASCII (optional; `/prompts:arch-ui-ascii`)
8) Plan enhancer (optional; `/prompts:arch-plan-enhance`)
9) Phase plan (`/prompts:arch-phase-plan` or `arch-phase-plan-agent`)
10) Review gate (optional; `/prompts:arch-review-gate`)
11) Implement (`/prompts:arch-implement` or `arch-implement-agent`) + WORKLOG_PATH exists
12) Post-checks (optional): `/prompts:arch-audit`, `/prompts:arch-audit-implementation`, `/prompts:arch-qa-autotest`
13) Code review: `/prompts:arch-codereview`
14) PR finalization (optional): `/prompts:arch-open-pr`

Mini Flow (small tasks):
1) Plan doc exists (DOC_PATH readable)
2) North Star confirmed (soft; based on `status:`)
3) Mini plan (`/prompts:arch-mini-plan-agent`)
4) Implement (`/prompts:arch-implement-agent`) + WORKLOG_PATH exists
5) Post-checks (optional): `/prompts:arch-audit-agent`, `/prompts:arch-audit-implementation-agent`, `/prompts:arch-qa-autotest`
6) Code review: `/prompts:arch-codereview`
7) PR finalization (optional): `/prompts:arch-open-pr`

Next step selection rule:
- Choose the earliest PENDING **non-optional** step in the selected flow.
- If all non-optional steps are DONE:
  - Recommend the most sensible next optional step (prefer `/prompts:arch-codereview`, then `/prompts:arch-open-pr`).
- Always print the exact next command with DOC_PATH filled in.
- Offer to proceed: “Reply ‘run next’ to execute it” (or instruct to rerun with `RUN=1`).

## 4) If RUN=1, execute the next step
If `$ARGUMENTS` includes `RUN=1`, then:
- Load the next prompt procedure file from the installed prompts (preferred) or repo fallback:
  1) `~/.codex/prompts/<next>.md`
  2) `prompts/<next>.md`
- Follow it exactly as the procedure, using the same DOC_PATH.
- Do not run multiple doc-writing prompts concurrently against the same DOC_PATH.

OUTPUT FORMAT (console only; USERNAME-style):
Communicate naturally in English, but include (briefly):
- North Star reminder (1 line)
- Punchline (1 line; what the next command is)
- DOC_PATH + inferred flow (regular/mini)
- Checklist (FULL: list every step for the selected flow, each labeled DONE/PENDING/OPTIONAL/UNKNOWN)
- Next command to run (exact `/prompts:*` invocation)
- Ask: “Run it now? (yes/no)” and mention `RUN=1` option
