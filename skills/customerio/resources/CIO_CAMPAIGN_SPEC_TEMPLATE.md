# Customer.io Campaign Spec Template (Draft Standard)

This document defines a **copy/paste-friendly** template for turning a Customer.io workflow (Campaign/Journey) into a durable text spec that can be reviewed, diffed, and audited against code + production data.

The goals:
- Make CIO workflows understandable outside the UI (Slack, PRs, incident notes).
- Enable **correctness reviews** against event/trait contracts in the codebase.
- Make it easy to spot likely misconfigurations that cause unexpected drop-off.

Non-goals:
- Replacing Customer.io as the source of truth for the “live config”.
- Capturing every UI field on day 1. This is a **v0.1** draft optimized for readability and correctness.

Related:
- Build guide (step-by-step): `tmp/CIO/CIO_CAMPAIGN_SPEC_BUILD_GUIDE.md`

---

## Terminology

- **Workflow**: A Customer.io Campaign (a Journey/Workflow builder).
- **Trigger**: The event that enrolls a person into the workflow.
- **Segment**: A reusable audience definition (conditions on events/attributes).
- **Action conditions**: Per-message “send only if” gating (often a segment or boolean conditions).
- **Node**: A step in the workflow (delay, branch, message, exit, etc).

---

## Campaign Spec Format (SSOT for human review)

Use this structure for every workflow. Keep it in a single markdown doc so it’s easy to share and diff.

### 1) Metadata (required)

```md
## Metadata
- Campaign ID: campaign-XX-some-slug
- CIO workspace: <name or id>
- CIO campaign id: <numeric id if known>
- CIO campaign name: <exact UI name>
- Channels: push | email | sms | in_app | webhook (list)
- Status: draft | running | stopped | archived (as seen in CIO)
- Owner: <team/person>
- Last reviewed: YYYY-MM-DD
- Screenshot / link: <optional>
```

### 2) Goal + intent (required)

Capture both the UI description and the inferred behavior.

```md
## Goal
<paste the workflow description from CIO>

## Intent (hypothesis)
- What the workflow is trying to do in behavioral terms.
- What “success” means (conversion / re-engagement / retention).

## Questions for Dev (confirm intent)
- <list unknowns that must be confirmed>
```

### 3) Entry (required)

```md
## Entry
- Trigger: EVT:<event_name> (+ filters)
- Entry filters (segment): SEG-XXX <name>
- Re-entry: <allow once / allow multiple / time window / “only once per X” if visible>
- Enrollment notes: <quiet hours / timezone / start schedule if applicable>
```

### 4) Reusable definitions (required if referenced)

Define every referenced Segment and Action Condition exactly once, then reference by ID.

**Segment definition format**

```md
### SEG-001 <segment name> (matches all|any)
- ATTR:<key> <operator> <value>
- EVT:<event_name> performed [within <window>] [count >= N]
- (…)
```

**Action condition definition format**

```md
### AC-001 <action condition name>
send if:
- IN SEG-010 <segment name>
- AND IN SEG-011 <segment name>
```

Notes:
- Always include **matches all vs matches any**.
- Always specify the **time window** and/or **count threshold** when present.
- For “does not exist”, treat it as an attribute condition:
  - `ATTR:<key> does not exist`

### 5) Node graph + step list (required)

Provide two representations:
1) A small ASCII diagram for quick reading
2) A step-by-step list for precision

**ASCII diagram conventions**
- `-->` indicates a transition.
- `B?` indicates a True/False branch.
- `Exit` indicates leaving the workflow.
- Put the **branch condition name** in brackets, and reference the segment ID.

Example:

```txt
Trigger EVT:paywall_opened + SEG-001
  --> WAIT 2m
  --> B1? [SEG-002 Converted or Re-Engaged]
      True  --> Exit
      False --> MSG-001 Push 1 (AC-001)
                --> WAIT 12h
                --> B2? [SEG-002 Converted or Re-Engaged]
                    True  --> Exit
                    False --> MSG-002 Push 2 (AC-001)
                              --> Exit
```

**Step list conventions**
- Number steps in the order they occur in the primary path.
- Branches get sub-ids (`B1.T`, `B1.F`) so references remain stable as the flow changes.

Example:

```md
## Flow
1. Trigger: EVT:paywall_opened (Entry: SEG-001)
2. WAIT: 2 minutes
3. BRANCH B1: SEG-002 Converted or Re-Engaged?
   - B1.T: Exit
   - B1.F: Continue
4. MESSAGE MSG-001: Push 1 (gated by AC-001)
5. WAIT: 12 hours
6. BRANCH B2: SEG-002 Converted or Re-Engaged?
   - B2.T: Exit
   - B2.F: Continue
7. MESSAGE MSG-002: Push 2 (gated by AC-001)
8. Exit
```

### 6) Message inventory (recommended)

For each message node:
- Channel + name (as in CIO).
- Action conditions.
- CTA/deep link intent (if known/important).
- Expected volume or audience constraints.

```md
## Messages
### MSG-001 Push 1
- Send if: AC-001
- Content: <optional summary>
- Links: <optional>
```

### 7) Data contract mapping (required for correctness reviews)

This is where the workflow becomes “code-reviewable”.

For each event/trait used in segments/action conditions:
- Confirm it exists in code (or explicitly note it is backend-owned / SDK-owned).
- Note the canonical key name and semantics.

Template:

```md
## Data Contract Cross-Check
### Events
- EVT:paywall_opened
  - Source: Flutter telemetry (`TelemetryEventNames.paywallOpened`)
  - Notes: emitted with paywallSessionId/sessionGroupId/source/planId/entryScreen

### Attributes
- ATTR:subscription_status
  - Source: lifecycle traits (`CustomerIoLifecycleTraitKeys.subscriptionStatus`)
  - Values: trial | billing_issue | cancelled | active | expired | free
```

### 8) Completeness + correctness checklist (required)

Use this checklist during reviews:

```md
## Correctness Checklist
- [ ] Every event/trait key exists in code or is explicitly backend/SDK-owned.
- [ ] Segment “matches any/all” reflects intent.
- [ ] Time windows are present and correct (avoid missing windows).
- [ ] Conversion/exit conditions are reachable (events actually fire for users).
- [ ] Push/email eligibility gates match reality (don’t rely on rare events).
- [ ] Re-entry rules do not accidentally suppress intended retries.
- [ ] Message sends are gated only by conditions that are measurable and correct.
```

### 9) Production data validation (optional but strongly recommended)

When in doubt, validate assumptions with read-only warehouse queries:
- How many users match entry conditions (last 7d / 30d)?
- How many users match message gates?
- If gates are unexpectedly strict, identify which condition is collapsing volume.

Keep queries minimal and focused (two to five max).

---

## How to Produce a Campaign Spec (process notes)

### A) From a Customer.io screenshot (fast, but incomplete)
1. Identify the **Trigger** and any visible trigger filters.
2. Walk the workflow top-to-bottom and list the nodes.
3. Extract every referenced Segment/Action Condition:
   - Black boxes → Segments.
   - Red boxes → Action conditions.
4. De-duplicate definitions:
   - If multiple arrows point to the same segment, define it once.
5. Capture ambiguity as “Questions for Dev”.
6. Cross-check every event/trait name against code SSOT docs.

Limitations of screenshot-only specs:
- Re-entry rules, scheduling/quiet hours, and some per-node settings may be hidden.
- Segment definitions might be truncated or not include all filters.

### B) From Customer.io config via MCP/API (preferred for verification)
1. Find the campaign in the correct workspace.
2. Pull the campaign definition (nodes, delays, message actions).
3. Pull referenced segments and message action conditions.
4. Update the spec with **actual IDs** and any hidden settings:
   - Re-entry policy
   - Frequency caps
   - Start/stop state
   - Message template IDs

---

## Recommended Naming + IDs

- **Campaign ID (internal docs)**: `campaign-<number>-<kebab-slug>`
  - Example: `campaign-30-high-intent-paywall-route`
- **Segment IDs in docs**: `SEG-001`, `SEG-002`, etc (stable within the doc).
- **Action condition IDs in docs**: `AC-001`, `AC-002`, etc.
- **Message IDs in docs**: `MSG-001`, `MSG-002`, etc.

