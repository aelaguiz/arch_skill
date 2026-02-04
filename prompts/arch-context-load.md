---
description: "00b) Context load: derive a high-signal brief from DOC_PATH (+ worklog + code anchors) so a new agent can take over."
argument-hint: "<Freeform guidance. Include a docs/justin/<...>.md path anywhere to pin the plan doc (recommended).>"
---
# /prompts:arch-context-load — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Console output should be short and high-signal; see OUTPUT FORMAT for required content.

$ARGUMENTS is freeform steering (intent, constraints, random notes). Process it intelligently.

Resolve DOC_PATH from $ARGUMENTS + the current conversation. If DOC_PATH is not obvious, ask the user to choose from the top 2–3 candidates.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by reading existing docs; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2–3 candidates)
  - Missing access/permissions
  - A referenced *local* doc is required but you cannot locate it (ask for the path; do not continue guessing)
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.


# COMMUNICATING WITH AMIR (IMPORTANT)
- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH (Context Digest block), not in console output.


What this prompt is for (context load)
This prompt is for “bringing a fresh agent up to speed” so they can immediately:
- understand the North Star and constraints,
- understand the as-is architecture + key components,
- understand the chosen solution(s) and tradeoffs,
- understand the plan and what’s done vs not done,
- understand reviews/audits/follow-ups,
- understand open questions / deferred work,
- and correctly identify where we are in the arch_skill pipeline and what the best next prompt(s) are.

This is NOT:
- a full deep-dive call-site enumeration (use `/prompts:arch-deep-dive(-agent)`),
- a new plan write-up (use `/prompts:arch-new` / `/prompts:arch-reformat` / `/prompts:arch-phase-plan`),
- implementation (use `/prompts:arch-implement`).


Documentation-only (context digest):
- This prompt MUST NOT modify code.
- You MAY update DOC_PATH with a “Context Digest” block (required).
- Do not create additional planning docs.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Derive WORKLOG_PATH (if it exists) using the same rule as other arch prompts:
- `<DOC_BASENAME>_WORKLOG.md` next to DOC_PATH.
- If it exists, read it. If it does not exist, do NOT create it here (just note it).


Context load rules (avoid trivia; stay high-signal)
- Prefer the plan doc as the source of truth for *intent and decisions*.
- Prefer code as the source of truth for *what exists today*.
- Only read/scan code that is necessary to:
  - validate the doc’s “ground truth anchors” actually exist,
  - identify the 2–4 primary runtime/control paths and key ownership boundaries,
  - understand the chosen solution’s core primitives/contracts,
  - or resolve contradictions between doc and reality.
- Do not expand into repo-wide archaeology. Stay scoped to what the doc says matters.


Optional subagents (use only when DOC_PATH is large)
- Use subagents when DOC_PATH is large, references many anchors, or worklog/audits are long enough to bloat main context.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or create artifacts.
  - Shared environment: avoid commands that generate/overwrite outputs; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Close subagents once their results are captured.

Spawn at most TWO subagents (disjoint scopes; read-only):
1) Subagent: Doc + Worklog Extractor
   - Task: read DOC_PATH (+ WORKLOG_PATH if present) and extract the minimum to orient a new agent:
     - North Star (claim + scope + acceptance evidence + invariants)
     - Current plan status (phases + completed/in-progress)
     - Explicit decisions/tradeoffs (Decision Log + “Known tradeoffs” sections)
     - Open questions / follow-ups / deferred work
     - References/anchors (paths, symbols, commands)
   - Output format (bullets only):
     - North Star:
       - <bullet>
     - Scope:
       - In scope: <bullets>
       - Out of scope: <bullets>
     - Plan status:
       - <phase> — <status>
     - Decisions/tradeoffs:
       - <decision> — <why>
     - Open questions / follow-ups:
       - <item> (or "None")
     - Anchors:
       - <path> — <what it defines>

2) Subagent: Code Anchor Spot-Check
   - Task: validate the doc’s anchors against code reality:
     - confirm anchors exist
     - identify the 2–4 primary control paths relevant to the North Star
     - flag any obvious doc-vs-code mismatches (facts only; no edits)
   - Output format (bullets only):
     - Primary flows (as-is):
       - <flow> — <evidence anchors>
     - Anchor sanity:
       - <path> — <exists|missing> — <note>
     - Doc-vs-code mismatches (if any):
       - <mismatch> — <evidence anchor>


Main-agent procedure (do this order; keep it tight)
1) Resolve DOC_PATH (+ WORKLOG_PATH if present).
2) Read DOC_PATH fully. Skim for (these may be blocks or headings):
   - TL;DR + North Star
   - Scope (in/out)
   - Definition of done / acceptance evidence
   - Key invariants / non-negotiables
   - Research Grounding + External Research (if any)
   - Current + Target Architecture
   - Call-Site Audit
   - Phase plan
   - Decision Log
   - Gaps & Concerns, Review Gate, Implementation Audit, QA/DevX blocks (if present)
3) If DOC_PATH references other *local* docs that are required to interpret the plan (e.g., “see docs/...”), open them. If you cannot locate them, stop and ask for the path.
4) Do the minimum code spot-check:
   - Validate key anchors exist (paths/symbols).
   - Identify primary control paths and the key boundary/SSOT modules.
   - If the doc and code disagree on a material fact, record it in the digest as a “Doc-vs-code mismatch”.
5) Infer pipeline status (choose the best match; don’t overthink):
   - If no canonical plan doc exists → needs `/prompts:arch-new` or `/prompts:arch-reformat`
   - If research grounding is missing → needs `/prompts:arch-research(-agent)`
   - If current/target architecture + call-site audit are missing → needs `/prompts:arch-deep-dive(-agent)`
   - If phase plan is missing → needs `/prompts:arch-phase-plan(-agent)`
   - If code work is pending → needs `/prompts:arch-implement`
   - If code is done but completeness is uncertain → needs `/prompts:arch-audit-implementation(-agent)`
   - If code is done and we want idiomatic/completeness second opinions → needs `/prompts:arch-review-gate`
   - If ready to ship → needs `/prompts:arch-open-pr`
6) Write/update the Context Digest block in DOC_PATH using the format below. Do not paste the full block to console.


DOC UPDATE RULES (anti-fragile; do NOT assume section numbers)
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:context_digest:start -->` … `<!-- arch_skill:block:context_digest:end -->`
2) Else insert immediately after the TL;DR section if present.
3) Else insert immediately after YAML front matter if present.
4) Else insert at the top of the document.

Keep the digest concise and skimmable (optimize for “new agent reads this and can answer questions immediately”).


DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:context_digest:start -->
# Context Digest (for new agents)
Updated: <YYYY-MM-DD>

## North Star (1–2 sentences)
<one-liner claim + acceptance signal>

## Scope (what changes vs must not change)
- In scope:
  - <bullets>
- Out of scope:
  - <bullets>

## Current status (pipeline + truth)
- Pipeline stage: <e.g., phase plan complete; implementation in progress; audit pending>
- What’s done (high-level):
  - <bullets>
- What’s in progress / next:
  - <bullets>

## Key components + anchors (code entry points)
- `<path>` — <what it owns / why it matters>
- `<path>` — <...>

## Solution options + tradeoffs (what we chose and why)
- Chosen approach:
  - <summary>
- Alternatives considered:
  - <alt> — <why rejected/deferred>
- Key tradeoffs (explicit):
  - <tradeoff> — <impact>

## Plan snapshot (minimum)
- Phases:
  - Phase <n>: <goal> — <status>
- Verification (smallest signals):
  - <command/check> — <what it proves>

## Reviews / audits / follow-ups (if any)
- Reviews/audits captured in DOC_PATH:
  - <what> — <date> — <outcome>
- Open issues / deferred work:
  - <item> — <why deferred> — <anchor if available>

## Open questions (only if truly unresolved)
- <question> — <evidence needed to settle>

## Suggested next prompts (based on status)
- `/prompts:<...>` — <why>
<!-- arch_skill:block:context_digest:end -->


OUTPUT FORMAT (console only; Amir-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- North Star reminder (1 line)
- Punchline (1 line)
- What you did (read DOC_PATH + spot-checked code anchors + updated digest)
- Issues/Risks (doc gaps, doc-vs-code mismatches, missing referenced docs)
- Next action (what prompt to run next and why)
- Need from Amir (only if required)
- Pointers (DOC_PATH / WORKLOG_PATH if present)
