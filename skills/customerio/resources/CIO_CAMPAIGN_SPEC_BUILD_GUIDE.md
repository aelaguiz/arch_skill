# Customer.io Campaign Spec Build Guide (Step-by-Step)

This guide documents the repeatable process to build a **Campaign Spec** document for a Customer.io workflow/campaign, including pulling every referenced segment/action-condition and recursively expanding segment→segment references until the dependency tree is complete.

It also documents known gaps in our current Customer.io MCP/API surface.

Related docs:
- Spec template (format SSOT): `tmp/CIO/CIO_CAMPAIGN_SPEC_TEMPLATE.md`
- Example spec (filled): `tmp/CIO/campaign-30-high-intent-paywall-route.md`

---

## Goals

Build a campaign spec that is:
- **Readable** (copy/paste into Slack/PRs).
- **Reviewable** (diffable, stable IDs, explicit matches-any/all, windows).
- **Verifiable** against:
  - codebase event/trait contracts, and
  - production data (BigQuery read-only).

---

## Inputs / prerequisites

You need:
- Customer.io workspace access (via MCP or UI).
- Campaign identifier (campaign name and/or numeric id).
- Repo access (for event/trait names and meaning).
- Optional: BigQuery access for validation (read-only).

Recommended starting point:
- Use a screenshot only when you must; prefer pulling the config via MCP first.

---

## Output artifact

Create one markdown file per campaign:
- Path: `tmp/CIO/campaign-<id>-<kebab-slug>.md`
- Example: `tmp/CIO/campaign-30-high-intent-paywall-route.md`

This file should contain:
- Metadata
- Goal + inferred intent (+ questions for Dev)
- Campaign spec (flow + segment/action-condition definitions)
- Correctness findings + recommended changes
- MCP verification notes (+ limitations)
- Production data checks (if run)

---

## Step-by-step: build the spec using Customer.io MCP

### Step 1) Identify the workspace + campaign id

1. List workspaces:
   - MCP: `mcp__customerio__list_workspaces`
2. Find the campaign:
   - MCP: `mcp__customerio__list_campaigns` with a `search` string (e.g. `paywall`)
3. Record:
   - `workspace_id`
   - `campaign_id`
   - campaign `name`, `description`, `state` (running/stopped/etc)

Add this to the spec file under **Metadata**.

---

### Step 2) Pull the campaign definition (nodes + edges)

1. Fetch the campaign:
   - MCP: `mcp__customerio__get` with `action=get_campaign`
2. From the response, build a map:
   - `action_id → action object`
3. Extract the node graph:
   - Each node has `NextActionIDs` (edges).
   - Node types to expect:
     - `DelaySeconds` (waits)
     - `ConditionalBranch` (branches)
     - Message nodes: `Push`, `Email`, etc.
     - `Exit`

4. For each action, record the important config:
   - `Type`
   - `Delay` (seconds) for delays
   - `ConditionalFilter` for branches (often references segment ids)
   - `Preconditions` for message nodes (action conditions, often segment ids)
   - Message-specific IDs (ex: `TemplateID`, `Name`, `SendingState`)

5. Write the **Flow** section in the spec (ASCII + step list) using this graph.

Notes:
- Keep the step list stable by using node IDs for message actions when possible.
- Prefer referencing segment ids explicitly (ex: “uses segment `103`”).

---

### Step 3) Collect referenced segment ids from the campaign graph

From the campaign actions:
- Branches (`ConditionalBranch`) commonly reference segments in `ConditionalFilter`.
  - Example shape:
    - `ConditionalFilter: { and: [ { or: [ { segment: { id: 103 } } ] } ] }`
- Messages reference segments in `Preconditions`.
  - Example shape:
    - `Preconditions: { and: [ { or: [ { segment: { id: 96 } } ] }, ... ] }`

Algorithm (manual or scripted):
1. Initialize a set `segment_ids = {}`.
2. For each action:
   - If `ConditionalFilter` contains `segment.id`, add it.
   - If `Preconditions` contains `segment.id`, add it.
3. Add these segment ids to a queue for recursive expansion.

In the spec file:
- List the “top-level” segments referenced directly by the campaign.

---

### Step 4) Recursively expand segments (segment → segment)

This is the “fill out the tree” step.

For each segment id in the queue:
1. Fetch the segment:
   - MCP: `mcp__customerio__get` with `action=get_segment`
2. Record core metadata:
   - id, name, description, type, state, count, url
3. Inspect its `filters` tree:
   - The tree is usually an `And` or `Or` root with `children`.
   - Each child can be either:
     - A reference to another segment (`SegmentID`), OR
     - A leaf condition reference (`ConditionID`)

4. If a child has a non-zero `SegmentID`:
   - Add that segment id to the queue (if not already processed).
   - In the spec, represent this as “IN SEG-xxx <segment name>”.

5. If a child has a non-zero `ConditionID`:
   - Record it as an unresolved leaf (see “Known gaps” below).
   - In the spec, keep the screenshot/UI version of the leaf if available.

Stop when:
- the queue is empty (no new `SegmentID` references discovered).

Practical tip:
- Even when condition bodies are not resolvable via MCP, this recursion is still valuable:
  - it confirms segment composition (e.g., “Pushable = Recent App Openers AND True Push Permission Granted”).

---

### Step 5) Pull message templates for each message node

For each message action node:
1. Read its `TemplateID` from the campaign action.
2. Fetch the template:
   - MCP: `mcp__customerio__get` with `action=get_template`
3. Record:
   - channel type (push/email/etc)
   - subject/title/body (at least a short summary)

Add a **Messages** section in the spec.

---

### Step 6) Identify the trigger (and re-entry/frequency rules)

This should be part of the spec, but **may not be available via MCP**.

Attempt:
- Read `triggers` from `get_campaign`.

If `triggers` is empty:
- Treat this as a tooling gap and use the UI (see next section).
- If you have a screenshot, include the trigger inferred from it (explicitly label as “from screenshot / not MCP-verified”).

Also capture:
- re-entry / restart behavior (once vs multiple, min interval, debounce)
- quiet hours / time zone behaviors if configured

Note:
- `get_campaign` includes fields like `RestartMode`, `RestartMinInterval`, `DebounceSecs`, but we should not assume semantics without an authoritative mapping to CIO UI settings.

---

## Step-by-step: fill in condition bodies using the Customer.io UI (when MCP can’t)

Because the MCP segment response typically returns **ConditionIDs**, the UI is currently the reliable way to fetch the leaf condition definitions.

For each segment id referenced by the campaign:
1. Open the segment URL from `get_segment`:
   - `.../journeys/segments/<id>/overview`
2. In the segment builder UI:
   - Copy the **matches any/all** setting.
   - Copy each leaf condition:
     - Event name + time window + count threshold
     - Attribute key + operator + value
     - “does not exist” checks
3. Paste these into the spec under that segment definition.

Repeat until every segment definition in the spec is fully “expanded” (no placeholders).

If segments are deeply nested:
- Expand top-down:
  - fetch segment `A`
  - note it includes segment `B`
  - open `B` and repeat

---

## Step-by-step: codebase contract cross-check

For every event name and attribute key used in the campaign:
1. Locate its SSOT definition in code/docs.
2. Confirm:
   - the name matches exactly (case + underscores)
   - semantics match the intended segment logic
3. If the campaign uses keys not present in the repo SSOT:
   - record the presumed source:
     - backend-owned attribute
     - Customer.io SDK auto events
     - third-party ingestion (AppsFlyer, RevenueCat, etc)
   - add a “Question for Dev” if uncertain

Outcome:
- A “Data Contract Cross-Check” section that makes the campaign spec auditable.

---

## Step-by-step: production validation (BigQuery read-only)

Use the warehouse to answer two questions:
1) “Is the workflow configured as intended?”
2) “Which gate is collapsing volume?”

Recommended minimal queries:
- Entry cohort size (last 7d / 30d).
- Gate coverage:
  - users who match each key condition (pushability, subscription status, etc)
- Send volumes by action id:
  - `customerio_production.push_sent WHERE campaign_id = <id>`

Important constraints:
- Customer.io export tables may include messaging events (push/email) but not necessarily the app track events (even if the app sends them to CIO). Validate what’s actually exported before relying on it.

---

## Known gaps (current MCP/API limitations)

These are the main blockers to producing a **fully self-contained** spec via MCP alone:

1) **Campaign trigger details missing**
   - `get_campaign` responses observed returning `triggers: []` even for “Event” campaigns.
   - Impact: trigger event name and trigger filters can’t be MCP-verified today.

2) **Segment leaf condition bodies are not resolvable**
   - `get_segment.filters` returns a boolean tree of:
     - `SegmentID` references (resolvable by fetching the referenced segment), and
     - `ConditionID` leaf references (NOT resolvable via MCP today).
   - Impact: MCP can confirm segment composition but not the actual leaf conditions (event names, attribute keys, windows).

3) **No MCP tool to resolve `ConditionID → condition definition`**
   - What we’d want is an endpoint/tool that returns something like:
     - `ConditionID=104` → “attribute `subscription_status` is not `active`”
     - `ConditionID=57` → “event `Application Opened` within 30 days”

4) **Re-entry / restart policy not reliably inferable**
   - `RestartMode`, `DebounceSecs`, etc appear in campaign action payloads.
   - Without a mapping to the Customer.io UI semantics, we should treat these as opaque.

---

## Practical “done” definition

A campaign spec is “done” when:
- Every campaign node is represented (graph + step list).
- Every referenced segment is listed exactly once, with:
  - matches any/all,
  - full leaf condition bodies (from UI if needed),
  - nested segment membership expanded (segment→segment recursion complete).
- Every message node includes:
  - action id, template id, channel, content summary, action conditions.
- Every event/trait key is mapped to its source (client, backend, SDK, 3P).
- Known tool gaps are explicitly listed so readers understand which parts are inferred.

