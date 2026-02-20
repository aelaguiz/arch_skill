---
name: customerio
description: "Build a full Customer.io Campaign Spec (workflow → copy/paste text) using the Customer.io MCP, recursively expanding all referenced segments/action-conditions, documenting gaps, and optionally validating with BigQuery + repo contracts."
metadata:
  short-description: "Customer.io campaign spec builder"
---

# Customer.io Campaign Spec Builder

This skill standardizes how we turn a Customer.io workflow/campaign into a **durable, reviewable** markdown “Campaign Spec” document.

It is optimized for:
- copy/paste sharing (Slack, PRs, incident notes),
- correctness reviews (event/trait keys must exist and be meaningful),
- fast detection of misconfigurations that cause unexpected drop-off.

## Resources (this skill’s SSOT)

Use these as the canonical building blocks:
- Template: `resources/CIO_CAMPAIGN_SPEC_TEMPLATE.md`
- Build guide (step-by-step): `resources/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md`

## When to use

Use this skill when the user asks for any of:
- “Create/compile a campaign spec for <workflow>”
- “Analyze a Customer.io workflow” (especially from a screenshot)
- “Verify our workflow config vs code / BigQuery”
- “Why is this campaign not sending / dropping off?”

## Output rules

Unless project-specific instructions override:
- Put artifacts under `tmp/CIO/`
- Campaign spec filename: `tmp/CIO/campaign-<id>-<kebab-slug>.md`
- Also ensure the repo has:
  - `tmp/CIO/CIO_CAMPAIGN_SPEC_TEMPLATE.md` (copy from this skill resource if missing)
  - `tmp/CIO/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md` (copy from this skill resource if missing)

## Workflow (MCP-first, UI fallback when needed)

### 0) Confirm minimal inputs

You need at least one of:
- campaign id (best), or
- campaign name (partial ok), and the workspace environment (prod/staging).

If the user only provides a screenshot:
- proceed, but explicitly mark trigger/segment leaves as “from screenshot” until MCP/UI verification is done.

---

### 1) Locate the campaign in Customer.io (MCP)

1. `mcp__customerio__list_workspaces`
2. Choose `workspace_id` (prod vs staging matters).
3. `mcp__customerio__list` with `action=list_campaigns` and `search=<query>`
4. Record in the spec:
   - `workspace_id`, `campaign_id`, campaign name/description/state

---

### 2) Pull the campaign action graph (MCP)

1. `mcp__customerio__get` with `action=get_campaign`
2. Build a map: `action_id → action`
3. Extract the flow graph:
   - Each node has `NextActionIDs`
   - Common node types:
     - `DelaySeconds` (read `Delay`)
     - `ConditionalBranch` (read `ConditionalFilter`)
     - Message nodes (`Push`, `Email`, etc): read `TemplateID`, `Name`, `Preconditions`
     - `Exit`
4. Write the campaign flow in the spec:
   - ASCII diagram (small + readable)
   - Step list (precise, stable IDs)

---

### 3) Extract referenced segments + templates (MCP)

From campaign actions:
- Branch nodes:
  - segments referenced in `ConditionalFilter` (often `segment.id`)
- Message nodes:
  - segments referenced in `Preconditions` (action conditions)
  - template ids referenced in `TemplateID`

Create four sets:
- `segment_ids_direct` (segments referenced directly by campaign actions)
- `template_ids` (message templates)
- `condition_ids_unresolved` (leaf conditions discovered later in segments)
- `segment_ids_recursive` (segments referenced by other segments)

---

### 4) Recursively expand all segment → segment dependencies (MCP)

This is how we “pull all segments within the campaign” even when segments are nested.

Algorithm:
1. Initialize `queue = segment_ids_direct` and `seen = {}`.
2. While `queue` not empty:
   - Pop `segment_id`.
   - Skip if already in `seen`.
   - Fetch: `mcp__customerio__get` with `action=get_segment`.
   - Add to `seen`.
   - Inspect `segment.filters`:
     - Root keys like `And` or `Or` imply matches all / matches any.
     - Each child is either:
       - `SegmentID` (segment membership) → enqueue that segment id
       - `ConditionID` (leaf condition) → record in `condition_ids_unresolved`

In the spec:
- For each segment id, add a section:
  - segment id + name
  - matches all/any (derived from the filter tree shape)
  - nested segment membership lines (“IN segment <id>”)
  - leaf conditions: include the real condition (UI) or placeholder + `ConditionID` until resolved

---

### 5) Resolve segment leaf conditions (UI fallback; MCP gap)

Current MCP limitation:
- Segment filters include `ConditionID` references but do not provide the condition bodies.

So to fully populate leaf conditions:
1. Use `get_segment.url` and open in Customer.io UI.
2. Copy each leaf condition exactly:
   - event name, time window, and count thresholds
   - attribute key, operator, value
   - “does not exist” checks
3. Replace placeholders in the spec.

If UI access is not available:
- ask the user for screenshots of the segment builder, or
- document leaf conditions as unknown (do not guess).

---

### 6) Pull message template contents (MCP)

For each `TemplateID`:
1. `mcp__customerio__get` with `action=get_template`
2. Record in the spec:
   - subject/title/body (short summary is ok)
   - channel type
   - template id + action id

---

### 7) Trigger + re-entry rules (MCP gap + UI fallback)

Attempt to read trigger config from `get_campaign.triggers`.

If `triggers` is empty:
- treat as a tooling gap
- use the Customer.io UI (campaign entry settings) and/or a screenshot
- explicitly label trigger details as “UI-verified” or “inferred”

Also capture:
- re-entry / restart policy
- frequency caps / message limits (global + per-action)
- quiet hours / time zone behavior if configured

---

### 8) Data contract cross-check (repo grounding)

For every event name / attribute key used:
- Find its source of truth (code, backend, Customer.io SDK, third-party pipeline).
- Confirm name correctness (exact casing/underscores).
- Record semantics + any known footguns.

If a key does not exist in the repo’s SSOT:
- don’t assume it’s wrong; identify the likely source (backend / AppsFlyer / RevenueCat / SDK)
- add a “Question for Dev” if uncertain.

---

### 9) Optional: BigQuery read-only validation

Use minimal queries to validate:
- entry cohort size (last 7d / 30d)
- gate coverage (which condition collapses volume)
- message sends:
  - `customerio_production.push_sent` / `email_sent` filtered by `campaign_id` and `action_id`

Important: Customer.io exports sometimes include messaging events but not app track events. Verify what’s in the export before relying on it.

---

### 10) Final verification summary (spec vs MCP)

End the spec with a “Verification” section that states:
- what was confirmed by MCP (action graph, referenced segment ids, template ids, action preconditions)
- what required UI (trigger config, leaf conditions)
- what remains unknown (if any)

## Known MCP gaps (document in every spec)

1) `get_campaign.triggers` may be empty for Event campaigns → trigger not MCP-verifiable.
2) `get_segment.filters` returns leaf `ConditionID`s without the condition definitions.
3) No tool available to resolve `ConditionID → condition definition`.
4) Restart/re-entry semantics aren’t reliably inferable from raw fields without an official mapping to CIO UI.

