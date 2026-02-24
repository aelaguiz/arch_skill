---
description: "Customer.io campaign evaluation: build a full campaign spec (MCP-first) and assess correctness, event/trait contract alignment, and likely drop-off points; validate with BigQuery read-only when needed."
argument-hint: "<Campaign id or name + workspace (prod/staging). Optional: DOC_PATH=tmp/CIO/campaign-<id>-<slug>.md; optionally include screenshots/links and BigQuery project/dataset hints.>"
---
# /prompts:cio-campaign-evaluate — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list.
$ARGUMENTS is freeform steering. Process it intelligently.

## Purpose
Produce a single “north star” campaign evaluation doc that contains:
- A copy/paste “Campaign Spec” (workflow text + segment/action-condition definitions).
- A correctness assessment (config vs intent, event/trait contracts vs code behavior).
- A drop-off analysis identifying **unintentional** audience collapse points.
- Verification notes (what is MCP-verified vs UI-verified vs inferred).

This prompt should produce an assessment comparable to:
- `tmp/CIO/campaign-30-high-intent-paywall-route.md` (in the target repo)

## Safety / scope
- Read-only analysis: do **not** change Customer.io campaign config in this prompt.
- BigQuery is **read-only** (SELECT-only).
- Do not apply DB migrations.
- Do not modify app code unless explicitly asked. (This prompt is evaluation + documentation.)

## Capability gate (early exits)
You MUST detect missing capability early and stop if essential:
1) **Customer.io MCP** is required to MCP-verify the campaign graph.
   - Attempt a minimal call early: `mcp__customerio__list_workspaces`.
   - If it fails (missing auth/permissions/tools), STOP and ask Dev for the minimum needed.
2) **Codebase access** is required to validate event/trait semantics.
   - If you cannot read files / repo is missing, STOP and ask.
3) **BigQuery** (`db` MCP) is optional but often needed to quantify drop-off.
   - If `db` MCP is missing, proceed with config+code analysis, but explicitly mark “production validation: blocked”.
4) **PostHog** MCP is optional. Use only if it materially helps (event discovery, funnel validation) and you have the needed project context.

## Question policy (strict)
- You MUST answer anything discoverable from code/MCP/warehouse; do not ask Dev.
- Allowed questions only:
  - Missing access/permissions (Customer.io MCP, BigQuery/db MCP, repo filesystem)
  - Campaign identity ambiguity (top 2–3 candidates; ask Dev to choose)
  - Product intent/UX decisions not encoded in campaign description/config

Essential info gate:
- Explicitly check: “Is any essential information missing to proceed?”
- If yes, STOP and ask the smallest possible set of questions.

## Where to store the evaluation doc (DOC_PATH)

Resolve DOC_PATH:
- If $ARGUMENTS includes `DOC_PATH=tmp/CIO/...md`, use it.
- Else, after you identify `campaign_id` + `campaign_name`, set:
  - `DOC_PATH = tmp/CIO/campaign-<campaign_id>-<kebab-slug-from-campaign-name>.md`
- If `tmp/CIO/` does not exist, create it.

Single-document rule:
- All evaluation content lives in DOC_PATH.
- Do not create multiple competing “spec” docs unless explicitly requested.

## Seed resources (high-signal repo anchors)

If the target repo is Poker Skill mobile (Flutter-first), these are typically the SSOT anchors:
- Telemetry event registry: `apps/flutter/lib/core/telemetry/telemetry_catalog.dart`
- Customer.io lifecycle trait keys: `apps/flutter/lib/core/telemetry/customer_io/customer_io_lifecycle_contract.dart`
- Customer.io user attributes SSOT: `docs/SSOT/CUSTOMERIO_USER_ATTRIBUTES.md`
- Notification preference keys (backend-owned traits): `apps/flutter/lib/data/notifications/notification_preferences_models.dart`

If these paths don’t exist, find equivalents by searching for:
- `paywall_opened`, `push_permission_granted`, `CustomerIoLifecycleTraitKeys`, `setProfileAttributes`, `identify(traits`, `notif_reminders_push`.

## Campaign Spec template requirement

The “Campaign Spec” section in DOC_PATH must follow the shared template.

Use the `customerio` skill procedure for the spec-building phase (MCP-first, recursive segment expansion, UI fallback):
- Reference: `~/dev/src/arch_skill/skills/customerio/SKILL.md`

Preferred: ensure these files exist in the target repo:
- `tmp/CIO/CIO_CAMPAIGN_SPEC_TEMPLATE.md`
- `tmp/CIO/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md`

If missing, copy them from the installed `customerio` skill resources (do not reinvent):
- `~/dev/src/arch_skill/skills/customerio/resources/CIO_CAMPAIGN_SPEC_TEMPLATE.md`
- `~/dev/src/arch_skill/skills/customerio/resources/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md`

## Process (MCP-first; UI fallback where MCP is incomplete)

### 1) Identify the campaign (MCP)
- `mcp__customerio__list_workspaces` → select the correct `workspace_id`.
- `mcp__customerio__list` (`list_campaigns`, `search=...`) → find the campaign.
- `mcp__customerio__get` (`get_campaign`) → pull the full action graph.

Record `workspace_id`, `campaign_id`, `name`, `description`, `state`, `url`, and action ids.

### 2) Build the campaign spec (north star doc section)
Follow the campaign spec build guide (recursive segment expansion):
- Extract node graph + action ids.
- Extract referenced segment ids from:
  - branch `ConditionalFilter`, and
  - message `Preconditions` (action conditions).
- Recursively fetch segments to expand segment→segment references.
- Fetch templates (`get_template`) for each message node and summarize content.

Important MCP gaps to handle explicitly:
- Trigger details may not be present in MCP (`triggers: []`).
- Segment leaf conditions may appear as `ConditionID` references without condition bodies.
  - Use Customer.io UI to fill leaf conditions.
  - If UI access is unavailable, STOP (do not guess leaf condition bodies).

### 3) Intent + correctness walkthrough (step-by-step)
For each node in the workflow:
- State what the node is doing and why (relative to stated goal).
- Confirm the exit conditions correctly represent “converted” vs “re-engaged” vs “abandoned”.
- Confirm action conditions align with deliverability reality (push/email eligibility).
- Identify likely unintentional drop-off points:
  - attribute keys that don’t exist or are misspelled
  - events that are not emitted (or only emitted in rare cases)
  - overly strict “matches all” segments
  - missing time windows / wrong windows
  - “does not exist” logic that unintentionally includes/excludes cohorts

### 4) Codebase contract mapping
For each event and attribute used in segments/action conditions:
- Find its canonical definition (event registry, trait keys).
- Document when it fires and what it means.
- Call out semantics that can collapse audience:
  - events emitted only on explicit user action
  - traits only updated on identify or on specific refreshes
  - backend-owned attributes with delayed sync

### 5) Production validation (BigQuery read-only; minimal queries)
Only run queries that answer specific questions raised by the config+code review.
Typical high-signal queries:
- Entry cohort size (7d/30d).
- Gate coverage by condition (which gate collapses volume?).
- Sends by action id:
  - `customerio_production.push_sent` / `email_sent` filtered by `campaign_id` and grouped by `action_id`.

Constraints:
- Do not assume Customer.io export includes app track events; verify what’s available.
- Keep queries minimal (2–5).

Optional (PostHog):
- If you have the PostHog `projectId` and the campaign relies on PostHog-only events/properties, use:
  - `mcp__posthog__event-definitions-list` to confirm event names exist
  - `mcp__posthog__properties-list` to confirm property keys/values

### 6) Conclusions + recommended edits (config-only)
Provide:
- “Is this campaign correctly set up for the desired outcome?” (yes/no/partially, with reasons)
- Ranked list of fixes (highest impact first)
- What to verify after each fix (MCP/UI counts + warehouse metrics)

## DOC UPDATE RULES (use block markers; do NOT assume section numbers)

A) If DOC_PATH does not exist: create it from the template below.
B) If block markers exist, replace content inside them:
- `<!-- cio:block:tldr:start --> … <!-- cio:block:tldr:end -->`
- `<!-- cio:block:spec:start --> … <!-- cio:block:spec:end -->`
- `<!-- cio:block:assessment:start --> … <!-- cio:block:assessment:end -->`
- `<!-- cio:block:data:start --> … <!-- cio:block:data:end -->`
- `<!-- cio:block:gaps:start --> … <!-- cio:block:gaps:end -->`
C) Else update in place if headings include (case-insensitive):
- “TL;DR”
- “Campaign North Star”
- “Campaign Spec”
- “Assessment”
- “Production Data”
- “Gaps / Unknowns”
D) Else insert missing sections after YAML front matter.

Do not paste full doc content to console output.

## NORTH STAR DOCUMENT TEMPLATE (create DOC_PATH if missing)

---
title: "<CAMPAIGN NAME> — Customer.io Campaign Evaluation"
date: <YYYY-MM-DD>
status: draft | investigating | verified | blocked
owners: [<name>, ...]
reviewers: [<name>, ...]
cio:
  workspace: "<workspace name>"
  workspace_id: <int>
  campaign_id: <int>
  campaign_name: "<exact CIO name>"
  campaign_state: "<running|stopped|archived|draft>"
  campaign_url: "<url>"
artifacts:
  source_inputs:
    - "<screenshot paths/urls if any>"
  mcp_verified: false
  ui_verified: false
  bigquery_validated: false
  posthog_validated: false
tooling:
  customerio_mcp: unknown
  bigquery_db_mcp: unknown
  posthog_mcp: unknown
  codebase_access: unknown
related:
  - "<links>"
---

<!-- cio:block:tldr:start -->
# TL;DR
- **Goal (stated):** <paste CIO description>
- **Intent (hypothesis):** <what it’s trying to do in plain english>
- **Punchline:** <is it correct? what’s the main issue?>
- **Top unintentional drop-offs:** <1–3 bullets>
- **Recommended changes (highest impact):** <1–3 bullets>
- **Status:** <draft/investigating/verified/blocked>
<!-- cio:block:tldr:end -->

<!-- cio:block:spec:start -->
# 0) Campaign Spec (SSOT for review)

> Use the shared campaign spec template:
> - `tmp/CIO/CIO_CAMPAIGN_SPEC_TEMPLATE.md`
> - `tmp/CIO/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md`

## 0.1 Metadata
## 0.2 Goal + intent + questions for Dev
## 0.3 Entry (trigger + entry filters + re-entry rules)
## 0.4 Segments (fully expanded; matches any/all + windows)
## 0.5 Action conditions
## 0.6 Flow (ASCII + step list)
## 0.7 Messages (templates + content summary)
## 0.8 MCP verification summary (what was/wasn’t verifiable)
<!-- cio:block:spec:end -->

<!-- cio:block:assessment:start -->
# 1) Assessment (correctness + completeness)

## 1.1 Campaign North Star (falsifiable)
> <If config is correct, then X should happen; if incorrect, we expect Y evidence>

## 1.2 What the workflow is doing (node-by-node)
## 1.3 Data contract cross-check (codebase)
## 1.4 Likely misconfigurations (ranked)
## 1.5 Unintentional drop-off points (where + why)
## 1.6 What to change (config-only)
## 1.7 What to verify after changes
<!-- cio:block:assessment:end -->

<!-- cio:block:data:start -->
# 2) Production Data (read-only validation)

## 2.1 Questions we needed data to answer
## 2.2 Queries run (BigQuery; paste SQL + summarize results)
## 2.3 Interpretation (what the data implies)
<!-- cio:block:data:end -->

<!-- cio:block:gaps:start -->
# 3) Gaps / Unknowns / Tooling limitations

## 3.1 Tool gaps (MCP limitations, export coverage)
## 3.2 Unknowns requiring Dev confirmation
## 3.3 Follow-ups (smallest next evidence)
<!-- cio:block:gaps:end -->

# 4) Decision Log (append-only)
## <YYYY-MM-DD> — <decision>
- Context:
- Decision:
- Consequences:
- Follow-ups:

## Output format (console only; Dev-style)
Communicate naturally in English (not a dense checklist). Include:
- 1-line reminder of Campaign North Star
- Punchline (1 line)
- What you verified via MCP/UI/code/BQ (short)
- Main drop-off(s) and why
- Recommended changes (ranked)
- Need from Dev (only if essential)
- Pointers (DOC_PATH + any key artifacts)
