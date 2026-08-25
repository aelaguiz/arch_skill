<!--
Template note:
- This file is a PR body scaffold.
- Do not copy the old heading text ("PR Templates That Actually Help")
  into PR titles or PR body content.
- Start filling from the relevant section below.
-->

## User-Facing Changes (required in every PR — never delete this section)

Pick exactly one shape:

**None:**

```
None. Nothing a user can see, read, hear, or do changes in this PR.
```

**Enumerated** (the default when anything visible changes):

```
1. **<what changed, named from the user's seat>** — screen/flow: <where>.
   ![<caption>](<https image URL that renders>)
```

**Waived:**

```
Waived by <human>: <date>, "<their words, quoted>". Changes: <one-line list anyway>.
```

Rules: the enumerated list is exhaustive — every loader, spinner, skeleton,
empty state, error toast, copy edit, layout shift, color/animation/timing
change, re-sequenced or removed screen. Screenshots come from the running app
on this PR's head build; before/after pairs when modifying an existing
surface; a screen recording or frame series for timing/animation changes.
Verify every image URL returns HTTP 200 with an image or video content type
before publishing. Only a human can approve or waive; never write a waiver
the human did not utter, and never downgrade an enumerated list to `None`.

## QA Test Plan (required whenever User-Facing Changes are enumerated)

Answer from the tester's seat, not the debugger's:

1. **Steps:** numbered, on a real build, with the expected result per step. A
   non-engineer must be able to run them: no code, no debugger, no shell.
2. **Setup:** how the tester reaches the state this PR changes: account type,
   seeded data, dev-menu toggle, internal/TestFlight build. If setup needs an
   engineer, name exactly what the engineer hands the tester.
3. **Visual guide:** link an annotated walkthrough when the path is more than
   a couple of steps.

Omit only when the User-Facing Changes claim is a truthful `None` and no
behavior a human could verify changed. "Verified locally" and test-file names
are not a test plan.

## Plan Scope Receipt (plan-backed changes only)

- Canonical plan: `<path and Scope and Simplicity Contract anchor>`
- Human-authorized outcome: `<one line>`
- Approved initial convergence closure: `<items or none>`
- Later human-approved expansions: `<approval anchors or none>`
- Material out-of-scope findings not built: `<items or none>`

Keep this compact and anchor-based. It is a review receipt, not a second plan.
Omit the section for changes with no governing plan.

## 🐛 Bug Fix

### The Problem
[One sentence. What's broken from the user's perspective.]

**Symptoms observed:**
- What users/systems actually see happening
- Error messages, incorrect states, data corruption patterns

**Affected platforms/devices:** [iOS 14 and below / Android API < 28 / 32-bit ARM only / Safari / etc.]

### Reproduction: Before And After

[Required for every bug fix. The pair is the proof: exact steps that made
the bug happen on a build without the fix, then the same steps re-run clean
on the fixed build, with build identity (version/build or commit) named on
both sides. Compressed triggers, seeded state, and direct entry at the
failing step beat soaks and full-journey replays; name the compression so
the reader knows why it is equally valid. If reproduction was genuinely
impossible, write `not attempted because <blocking fact>` and the evidence
that substitutes.]

**Before — build without the fix:** `<version/build or commit>`
1. [Exact step]
2. [Exact step]

**Observed:** [the failure, quoted or screenshotted]

**After — fixed build:** `<version/build or commit>`
1. [Same steps]

**Observed:** [the corrected behavior]

### Root Cause Analysis

**The bug lives here:**
```
path/to/file.ts:142  →  The actual line(s) where things go wrong
```

**Why it happens:**

[Explain the causal chain. Not "X was null" but WHY X was null.]

Example: "When a user completes checkout but closes the browser before the webhook fires, we mark the order as `pending`. The nightly cleanup job treats `pending` orders older than 24h as abandoned and deletes them. But webhook retries can take up to 72h. So paid orders get deleted."

**How we missed it:**
- Gap in test coverage
- Assumption that proved false
- Edge case outside normal flows

### The Fix

**Strategy:** [Delete/rewrite/patch/workaround - and WHY this approach]

**Changes:**

- `order_service.ts` — Added `webhook_pending` state. Distinguishes "waiting for payment" from "waiting for webhook confirmation"
- `cleanup_job.ts` — Exclude `webhook_pending` from cleanup. Prevents deletion of orders awaiting webhook
- `webhook_handler.ts` — Transition from `webhook_pending` → `completed`. Completes the state machine

**State machine before:**
```
created → pending → completed
              ↓
           abandoned (deleted)
```

**State machine after:**
```
created → pending → completed
              ↓
           abandoned (deleted)

created → webhook_pending → completed
              ↓ (72h timeout)
           flagged_for_review
```

### What I Considered But Didn't Do

- **Extending cleanup timeout to 72h** — Rejected because it delays fraud detection
- **Disabling cleanup entirely** — Too much cruft accumulates

### Blast Radius

- **Database migrations:** None / Yes (reversible) / Yes (destructive)
- **API contract changes:** None / Additive only / Breaking
- **Affected services:** List downstream consumers
- **Rollback complexity:** Instant / Requires data backfill / Requires coordination

---

## ✨ New Feature

### What This Enables

[One paragraph. What can users DO now that they couldn't before?]

### System Context

**Where this fits in the architecture:**

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │ ──── │   Gateway   │ ──── │  This PR    │
└─────────────┘      └─────────────┘      └──────┬──────┘
                                                 │
                                          ┌──────▼──────┐
                                          │  Postgres   │
                                          └─────────────┘
```

**New dependencies introduced:**
- `libfoo@2.3.1` — Why we need it, what alternatives we considered
- New external API calls to X — Rate limits, failure modes, cost

### Data Model

**New tables/collections:**

```sql
-- What business entity this represents
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),

    -- Preferences stored as JSONB for flexibility, but with
    -- CHECK constraint to enforce schema at DB level
    preferences JSONB NOT NULL,

    CONSTRAINT valid_preferences CHECK (
        preferences ? 'theme' AND
        preferences ? 'notifications'
    )
);
```

**New fields on existing tables:**

- `users.onboarding_completed_at` (timestamp) — Null = not completed. Timestamp = when. Avoids boolean + separate timestamp.

**Indexes added:**
```sql
-- Speeds up the dashboard query that filters by date range + status
-- Chose BRIN over B-tree because data is naturally time-ordered
CREATE INDEX idx_orders_created ON orders USING BRIN (created_at);
```

### Object Model / Domain Design

```
Subscription
├── id: UUID
├── user_id: UUID
├── plan: Plan (enum: FREE | PRO | ENTERPRISE)
├── status: Status (enum: ACTIVE | PAUSED | CANCELLED)
├── billing_cycle: BillingCycle
│   ├── anchor_day: int (1-28)
│   ├── period: MONTHLY | ANNUAL
│   └── next_billing_at: DateTime
└── entitlements: Entitlement[]
    ├── feature: string
    ├── limit: int | null (null = unlimited)
    └── used: int
```

**Invariants this code maintains:**
1. `next_billing_at` is always in the future for ACTIVE subscriptions
2. `used` never exceeds `limit` (enforced at service layer, not DB)
3. CANCELLED subscriptions retain entitlements until `next_billing_at`

### API Design

**New endpoints:**

```
POST /api/v2/subscriptions
  → Creates subscription, idempotent on (user_id, plan)
  → Returns: Subscription
  → Errors: 409 if active subscription exists

PATCH /api/v2/subscriptions/:id
  → Allowed transitions: ACTIVE→PAUSED, PAUSED→ACTIVE, *→CANCELLED
  → Returns: Subscription
  → Errors: 422 for invalid transitions
```

**Why v2:** Breaking change from v1 where subscriptions were embedded in user object.

### File-by-File Walkthrough

```
src/
├── domain/
│   └── subscription/
│       ├── subscription.ts      # Pure domain object, no I/O
│       ├── billing_cycle.ts     # Value object with date math
│       └── entitlements.ts      # Collection wrapper with limit enforcement
├── services/
│   └── subscription_service.ts  # Orchestrates domain + repositories
├── repositories/
│   └── subscription_repo.ts     # Postgres implementation
└── api/
    └── subscription_controller.ts  # HTTP concerns only
```

### Edge Cases Handled

- **Upgrade mid-cycle** — Prorate immediately, bill difference. Industry standard, users expect this.
- **Downgrade mid-cycle** — Apply at next cycle. Prevents gaming (upgrade, use, downgrade).
- **Payment fails** — 3 retries over 7 days, then PAUSED. Balances revenue recovery vs. user experience.
- **Account deletion** — CANCELLED, data retained 30 days. Legal/compliance requirement.

### What's NOT in This PR (Intentionally)

- Admin UI for managing subscriptions → Separate PR to keep this reviewable
- Webhook integration with Stripe → Depends on this PR, comes next
- Migration of existing users → Needs product decision on grandfather rules

---

## 🔧 Ops / Infrastructure

### What Changed

[One sentence: "We now do X instead of Y" or "We added X"]

### Motivation

**The pain:**
- Concrete incident/metric that triggered this
- Cost being incurred (downtime, engineer hours, infra spend)

**Why now:** What changed to make this worth the investment

### Architecture Change

**Before:**
```
┌─────────┐     ┌─────────┐
│  App    │────▶│  Redis  │  (single node, no persistence)
└─────────┘     └─────────┘
```

**After:**
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  App    │────▶│  Redis  │────▶│  Redis  │  (primary + replica)
└─────────┘     │ Primary │     │ Replica │
                └────┬────┘     └─────────┘
                     │
                     ▼
                ┌─────────┐
                │   EBS   │  (persistence)
                └─────────┘
```

### Configuration Changes

- `maxmemory-policy`: `noeviction` → `allkeys-lru` — Prevents OOM crashes
- `appendonly`: `no` → `yes` — Enables persistence
- `replica-read-only`: (new) `yes` — Prevents split-brain writes

### Terraform / IaC Changes

```hcl
# New resources
aws_elasticache_replication_group.main
aws_elasticache_parameter_group.custom
aws_security_group_rule.redis_replica

# Modified resources
aws_elasticache_cluster.main → removed (replaced by replication group)
```

### Runbook Updates

**New alerts:**
- `redis_replication_lag > 10s` → Page oncall, potential data loss risk
- `redis_memory_usage > 80%` → Warn, scale up or investigate leak

**New dashboards:** Link to Grafana/Datadog

**Failure modes and recovery:**

- **Primary dies** — Healthcheck fails. Auto-recovery: replica promotes (< 30s). Manual steps: none required.
- **Both nodes die** — Alert fires. No auto-recovery. Manual: restore from EBS snapshot.
- **Replication lag** — Metric alert. No auto-recovery. Manual: check network, primary load.

### Rollout Plan

1. **Deploy replica alongside existing primary** (this PR)
2. **Monitor for 48h** — Verify replication healthy
3. **Enable persistence** — Separate PR
4. **Cutover reads to replica** — Separate PR
5. **Decommission old infrastructure** — Separate PR

### Rollback

- **Instant:** Revert this PR, replica disappears, primary unchanged
- **Data impact:** None, replica is read-only copy
- **Dependencies:** None downstream depend on replica yet

---

## 🏗️ Refactor

### Why This Refactor

**Code smell addressed:** [Name the specific problem]

Example: "Shotgun surgery — every new payment method requires changes in 7 files"

**Trigger:** What made this urgent (upcoming feature, bug frequency, onboarding pain)

### Design Change

**Before (implicit architecture):**
```
PaymentController
├── processStripe()
├── processPaypal()
├── processApplePay()
└── processGooglePay()  ← Adding this required touching 7 files
```

**After (explicit architecture):**
```
PaymentController
└── process(provider: PaymentProvider)

PaymentProvider (interface)
├── StripeProvider
├── PaypalProvider
├── ApplePayProvider
└── GooglePayProvider  ← Adding this = 1 new file, 1 line registration
```

### Migration Path

This refactor is **behavior-preserving**. The old and new code produce identical outputs.

**Verification:**
- [ ] Existing tests pass without modification
- [ ] Ran both implementations in parallel in staging for 24h
- [ ] Diff'd outputs: 0 discrepancies

### File Changelog

- `payment_controller.ts` — Simplified, -200 lines. Delegates to providers.
- `providers/base.ts` — New, +50 lines. Interface definition.
- `providers/stripe.ts` — New, +80 lines. Extracted from controller.
- `providers/paypal.ts` — New, +75 lines. Extracted from controller.

**Net change:** +5 lines, but cyclomatic complexity reduced from 47 to 8

### What Stays Ugly (For Now)

- Error handling still inconsistent across providers → Separate PR
- Logging format varies → Waiting on observability team's new standard

---

## ⚡ Performance

### The Problem

**Observed:** [Concrete metric — p99 latency, CPU usage, memory growth]

**Target:** [Where we need to get]

**Affected platforms/devices:** [Low-end Android / older iPhones / high-latency regions / etc.]

### Investigation

**Profiling results:**

```
Total request time: 2,340ms

├── DB query (users):     45ms
├── DB query (orders):   890ms  ← 38% of time, N+1 query
├── DB query (items):    780ms  ← 33% of time, N+1 query
├── JSON serialization:  580ms  ← 25% of time, huge payload
└── Other:                45ms
```

**Root cause:** Loading 1000 orders, then 1 query per order for items = 1001 queries

### The Fix

**Strategy:** Batch queries + pagination + lazy loading

**Query before:**
```sql
SELECT * FROM orders WHERE user_id = ?;
-- Then for each order:
SELECT * FROM items WHERE order_id = ?;  -- Runs 1000 times
```

**Query after:**
```sql
SELECT * FROM orders WHERE user_id = ? LIMIT 50 OFFSET ?;
SELECT * FROM items WHERE order_id IN (?, ?, ?, ...);  -- Runs once
```

### Results

- **p50 latency:** 1,200ms → 180ms (-85%)
- **p99 latency:** 4,500ms → 420ms (-91%)
- **DB queries/request:** 1,001 → 2 (-99.8%)
- **Response size:** 2.4MB → 180KB (-92%)

### Tradeoffs

- **Pagination added** — Users now see 50 orders at a time instead of all. Product approved.
- **Index added** — `orders(user_id, created_at)`. Adds ~2% to write latency, acceptable.
- **Memory usage** — Down 80% per request due to smaller result sets.

---

## Quick Reference: What Makes a PR Elite

1. **Explain WHY, not just WHAT** — Code shows what. PR explains why.
2. **Show the before/after** — Architecture diagrams, state machines, query plans
3. **Acknowledge tradeoffs** — What you considered and rejected
4. **Scope the blast radius** — What could break, how to roll back
5. **Leave breadcrumbs** — What's intentionally deferred, what comes next
