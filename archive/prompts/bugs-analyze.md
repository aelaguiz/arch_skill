---
description: "Bug analysis: create/update bug doc, ingest evidence, form hypotheses, and decide fix-readiness."
argument-hint: "<Paste the bug report, symptoms, Sentry links, logs, or QA notes. Optional: include a docs/bugs/<...>.md path to pin the bug doc.>"
---
# /prompts:bugs-analyze — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
Inputs: $ARGUMENTS is freeform steering. Process it intelligently.

Resolve DOC_PATH:
- If $ARGUMENTS includes a docs/bugs/<...>.md path, use it.
- Else if a single obvious bug doc exists (docs/bugs/BUG_*.md), use it.
- Else create a new bug doc in docs/bugs/ using this rule:
  - docs/bugs/BUG_<TITLE>.md
  - TITLE = 4–8 words derived from $ARGUMENTS, uppercased, spaces → _, punctuation removed.
  - Avoid date stamps or “updated/real/new” naming.
  - If docs/bugs/ does not exist, create it.
Single-document rule: all investigation detail lives in DOC_PATH. Do not create extra planning docs.

Question policy (strict):
- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2–3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.
Essential info gate (stop-and-ask when required):
- During evidence gathering and North Star definition, explicitly check: “Is any essential information missing to proceed?” If yes, stop and ask Dev for the smallest missing items needed.
- If the report references a Sentry issue but the ID/URL is missing, malformed, or clearly wrong, stop and ask Dev for the correct ID/URL before continuing (unless you can recover it unambiguously from Sentry MCP using the provided error signature/title).
- Keep questions minimal and specific; ask only what is essential to move forward.

# COMMUNICATING WITH DEV (IMPORTANT)
- Start console output with a 1 line reminder of our Bug North Star.
- Then give the punch line in plain English.
- Then give a short update in natural English (bullets optional; use them only if they improve clarity).
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH, not in console output.

Documentation-only (investigation):
- DO NOT modify code in this prompt.
- You may read code and run read-only searches to ground hypotheses.
- Prefer first-party evidence: Sentry, logs, traces, QA notes, reproducible steps.
- docs/FLUTTER/REF may contain relevant system documentation — check it if relevant.
- Avoid external research unless it is clearly necessary to resolve ambiguous library/framework behavior; if needed, confirm the current date first.

Sentry evidence handling (required when an issue ID or Sentry URL is provided):
- Always evaluate via Sentry MCP.
- Organization is always `funcountry`.
- Project defaulting:
  - If the Sentry issue URL implies the project, trust it.
  - Otherwise default to `psmobile-production`, unless staging is explicitly referenced; then use `psmobile-staging`. If ambiguous and the environment matters, ask.
- Gather and record essential issue facts in Evidence:
  - title/exception/message, top stack frames, frequency/users affected, first/last seen, and key tags (environment/release/url/device) if relevant.
- Use the most specific tool first:
  - If a Sentry issue URL is provided: use `get_issue_details(issueUrl=...)`.
  - If only issue ID is provided: use `get_issue_details(organizationSlug='funcountry', issueId='<ID>')`.
- Attempt Seer analysis:
  - Use `analyze_issue_with_seer(issueUrl=...)` or `analyze_issue_with_seer(organizationSlug='funcountry', issueId='<ID>')` and capture any root-cause/fix hints.
- If breadcrumbs or per-event context are needed:
  - Use `search_issue_events` (small limit) to pull recent events and pick a representative `eventId`.
  - Try `get_issue_details(organizationSlug='funcountry', eventId='<eventId>')` to fetch the full event payload (this may include breadcrumbs/context).
  - If attachments are relevant, use `get_event_attachment(organizationSlug='funcountry', projectSlug='<project>', eventId='<eventId>')` and derive `<project>` from the issue URL/details when possible (otherwise use the default project above).
  - If breadcrumbs are not available via MCP, note the limitation in DOC_PATH and ask whether REST API access is available.
- Optional (fast scope check): use `get_issue_tag_values` for `environment`, `release`, or `url` distributions when it will materially impact triage/fix design.

Investigation discipline (depth + speed):
- Ingest evidence; record concrete anchors (issue IDs, log snippets, file paths, symbols).
- Map symptoms to likely control paths; list 2–4 candidate vectors max.
- Develop hypotheses with confidence estimates and disconfirming evidence.
- If a single root cause is >=90% likely, mark it as “Most likely root cause” and set status to fix-ready.
- If not, rank hypotheses and list the minimal next evidence needed to decide (do not do wide, speculative exploration).

DOC UPDATE RULES (anti-fragile; do NOT assume section numbers):
A) If DOC_PATH does not exist, create it using the template below.
B) Update blocks in-place:
1) If block markers exist, replace the content inside them:
   - <!-- bugs:block:tldr:start --> … <!-- bugs:block:tldr:end -->
   - <!-- bugs:block:analysis:start --> … <!-- bugs:block:analysis:end -->
2) Else update in place if headings include (case-insensitive):
   - “TL;DR”
   - “Bug North Star”, “Bug Summary”, “Evidence”, “Investigation”
3) Else insert missing top-level sections after YAML front matter.
Do not paste full doc content to the console.
Keep status consistent:
- When status changes, update both YAML front matter `status` and the TL;DR `Status` line.

DOCUMENT TEMPLATE (create if missing):
---
title: "<BUG TITLE> — Bug Investigation"
date: <YYYY-MM-DD>
status: triage | investigating | fix-ready | fixing | verifying | resolved | blocked
owners: [<name>, ...]
reviewers: [<name>, ...]
related:
  - <links to Sentry / issues / PRs>
---

<!-- bugs:block:tldr:start -->
# TL;DR
- **Symptom:** <one line>
- **Impact:** <one line>
- **Most likely cause:** <one line>
- **Next action:** <one line>
- **Status:** <triage/investigating/fix-ready/...>
<!-- bugs:block:tldr:end -->

<!-- bugs:block:analysis:start -->
# 0) Bug North Star (falsifiable)
## 0.1 Claim (fix definition)
> <If we do X, then Y no longer happens under Z, evidenced by W>

## 0.2 In scope / out of scope
- In scope:
- Out of scope:

## 0.3 Definition of done (evidence)
- Primary signal (prefer existing tests/logs/metrics):
- Secondary signal (optional):
- Manual QA checklist (short; optional):

## 0.4 Guardrails / invariants
- <must not break>

# 1) Bug Summary
## 1.1 User-facing symptom
## 1.2 Expected vs actual
## 1.3 Impact / severity / blast radius
## 1.4 Environments / versions / devices
## 1.5 Fastest repro (if known)
## 1.6 Regression window (first seen / last known good)

# 2) Evidence (ground truth)
## 2.1 Sentry / error logs / traces
## 2.2 User reports / QA notes
## 2.3 Metrics / dashboards
## 2.4 Code anchors (paths + behavior)
## 2.5 What we inspected (searches/tests/logs)

# 3) Investigation
## 3.1 Candidate vectors (code areas)
## 3.2 Hypotheses (ranked, with confidence)
## 3.3 Most likely root cause (if >=90% confident)
## 3.4 Disproved hypotheses (and why)
## 3.5 Next evidence to gather (if unresolved)
<!-- bugs:block:analysis:end -->

<!-- bugs:block:fix_plan:start -->
# 4) Fix Plan (authoritative)
## 4.1 Proposed fix (minimal)
## 4.2 Alternatives considered (and rejected)
## 4.3 Step-by-step plan
## 4.4 Risks / mitigations
## 4.5 Verification (tests/logs/metrics)
## 4.6 Rollback / mitigation
<!-- bugs:block:fix_plan:end -->

<!-- bugs:block:implementation:start -->
# 5) Implementation & Verification
## 5.1 Changes made
## 5.2 Tests run + results
## 5.3 Manual QA (if any)
## 5.4 Outcome / status
<!-- bugs:block:implementation:end -->

# 6) Decision Log (append-only)
## <YYYY-MM-DD> — <decision>
- Context:
- Decision:
- Consequences:
- Follow-ups:

OUTPUT FORMAT (console only; Dev-style):
This is the information it should contain but you should communicate it naturally in english not as a bulleted list that is hard to parse for the user.
Include:
- Bug North Star reminder (1 line)
- Punchline (1 line)
- What you did / what changed
- Issues/Risks (if any)
- Next action
- Need from Dev (only if required)
- Pointers (DOC_PATH / other artifacts)
