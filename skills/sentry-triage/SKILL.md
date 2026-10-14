---
name: sentry-triage
description: "Triage recurring Sentry alert noise and duplicate error issues. Use when asked to hide or mute a known error, merge duplicate issues, stabilize their grouping, or verify that a Sentry noise change preserves actionable alerts. Owns Sentry issue disposition and grouping; a request to fix the underlying application bug alone does not select this workflow."
metadata:
  short-description: "Group recurring errors and silence accepted noise"
---

# Sentry Triage

Make recurring failures arrive as useful issues, with an explicit decision about
which ones deserve alerts. Preserve the evidence needed to diagnose real faults.
Success includes explaining what prevents the next variation from creating a
fresh issue; archiving today's issue alone may provide only temporary relief.

A request to hide a confirmed error family authorizes its narrow, reversible
Sentry triage without repeated confirmations. Preserve the user's scope:
inspection stays read-only, merging does not imply archiving, and hiding does not
authorize deleting history, discarding events, or suppressing unrelated alerts.
Archive accepted noise; resolve only a defect that has actually been fixed.

## Establish the family and available access

Start from the supplied issue, project, or alert. Inspect representative events,
current status and archive conditions, and prior triage decisions. Search likely
duplicates in the same project, including archived issues. Compare fingerprints,
contributing stack frames, error categories, releases, platforms, and user
impact. Similar titles or an AI actionability label alone do not establish a
shared cause or harmlessness. Keep unrelated or uncertain failures separate.

Use the connected Sentry tools first. Discover operations and read their current
schemas rather than assuming that a general project updater supports grouping.
Tool availability, credential permissions, and a successful mutation are three
different facts. Do not write to production just to test permission.

When a needed operation is absent, use the documented Sentry API or an available
authenticated browser under its operating instructions; apply `$browseros`
before a BrowserOS fallback. Use existing authorized
credentials without exposing them. Release-upload credentials can lack issue
and project permissions; an `org:ci` token is not sufficient for this workflow.
If access is missing, complete the independent authorized work and identify the
exact remaining operation and required access. Do not describe an archive as a
completed merge or a proposed fingerprint as an installed rule.

## Choose the smallest durable change

Keep actionable failures open under a canonical issue. For confirmed accepted
noise, choose Archive Forever when the user wants lasting silence while keeping
events. For a failure that becomes actionable with frequency, choose an explicit
count, user-count, or time condition that reflects that concern. Do not silently
substitute Sentry's default archive-until-escalating behavior for forever.

Inspect the actual grouping inputs before changing them. Leave ordinary
exceptions on default grouping. For a family split by irrelevant variation,
choose the owning correction:

- A narrow project fingerprint rule can give installed app versions a stable
  identity immediately. Preserve existing rules and their ordering; the first
  matching rule wins, and project rules can override SDK fingerprints.
- An SDK fingerprint can use a stable failure code or category. Keep changing
  identifiers and diagnostics in structured context. Propose or implement that
  code change according to the user's authorized scope and repository rules.
- A stack-trace rule can remove a specific irrelevant wrapper from the grouping
  calculation while retaining the diagnostic stack.

Avoid grouping a broad class such as every timeout into one issue merely because
the titles look alike. A fully custom fingerprint bypasses AI similarity
grouping; including `{{ default }}` preserves the default distinctions rather
than forcing different default hashes together. Prefer one owner for the rule.
If a server rule bridges old builds during an SDK rollout, keep the identity
consistent and record the condition for removing that bridge.

Apply the future grouping correction, consolidate confirmed existing duplicates,
then set the intended disposition on the surviving issue. Check the actual merge
result rather than assuming which issue survives. A changed fingerprint can
create another issue on its next occurrence; account for it in verification.
Manual merging preserves the merged fingerprints but does not infer a rule for
unseen variations. Recheck the final status after merging.

## Use the correct Sentry operation

- **Archive:** the connector's `update_issue` uses `status="ignored"`. Set
  `ignoreMode="forever"` explicitly for permanent archiving, or supply the
  chosen conditional mode and its inputs. Inspect its schema when changing an
  already archived issue: some connectors require reopening before applying a
  different mode. Keep any intermediate state brief and read back the result.
- **Merge:** discover a merge operation. If none exists, the documented project
  issues API supports `PUT /api/0/projects/{org}/{project}/issues/` with repeated
  numeric `id` query parameters and `{"merge":true}`. It requires `event:write`.
  Always supply the exact issue IDs. A successful HTTP response can be a no-op
  for out-of-scope IDs; verify the resulting issue and fingerprints.
- **Grouping rules:** the project API accepts `fingerprintingRules` and
  `groupingEnhancements` through `PUT /api/0/projects/{org}/{project}/` with
  suitable project write access. Read the existing configuration first, retain
  unrelated rules, and read back the update. A connector that only edits
  project name, slug, or platform cannot apply these fields.
- **Alerts:** inspect notification workflows with `get_alert_rule` and metric
  monitors with `get_metric_monitor_details`, or their current equivalents.
  Use `update_alert_rule` for notification behavior and `update_metric_monitor`
  for queries or detection thresholds. Native monitor IDs differ from legacy
  alert IDs. Preserve complete arrays when an update replaces action groups,
  conditions, or connected workflows. Do not widen an issue-specific request
  into project-wide alert retuning.

For aggregate notifications, check whether the query includes archived events.
`is:unresolved` excludes archived and resolved issues. Preserve health or volume
measurements that intentionally count all failures. Lowering priority alone does
not remove events from an unresolved-error count. Read actual queries and
aggregations; a monitor's name may not describe its current calculation.

## Verify grouping and alert behavior separately

Before applying a rule, compare representative matching events and a nearby
failure that needs a different fix. Verify that the proposed identity keeps the
first together and the second separate. For SDK changes, use focused tests in
the existing reporting path and the repository's required checks. A code test
does not establish the behavior of a server-side rule or a shipped app.

Read back the saved rule, merged issue identity, and exact archive condition.
Then inspect a naturally arriving event after the change, its fingerprint, and
the issue it entered. When none has arrived, report the change as configured
and production grouping as awaiting an event. Do not manufacture production
errors or wait indefinitely to claim completion.

Inspect the relevant alert query, connected workflow, filters, and recent
actionable events. Check affected platform and release cohorts, especially when
a latest-release filter could exclude a still-supported build. Distinguish
eligibility under the configuration from evidence that a notification was
actually delivered. Silence alone proves neither correct grouping nor safety.

Sentry documents that escalation detection does not work for merged/unmerged
issues. Verify current behavior before relying on archive-until-escalating for a
merged group. Use an explicit condition, review time, or authorized narrowly
scoped volume monitor when growth must remain visible.

## Record the decision and report the result

When the user explicitly invokes this skill or asks for an issue note, leave one
concise note on the canonical issue: why the family shares a disposition, the
grouping change, merged issue identities, archive condition, and verification
state. Include the prior rule text when needed to reverse a configuration edit.
The connector's archive `reason` can supply that note; do not duplicate it.
Otherwise include those facts in the response. Do not send Slack or email
messages as part of this workflow unless requested.

Return the canonical issue link, the concrete changes made, what was verified,
and any remaining access, code-release, or next-event dependency. Name temporary
relief explicitly when lasting grouping could not be implemented. Keep this
proportional to the requested family; no separate suppression ledger is needed.

Consult these first-party references when checking API fields or current behavior:
[issue status](https://docs.sentry.io/product/issues/states-triage/),
[merging](https://docs.sentry.io/concepts/data-management/event-grouping/merging-issues/),
[bulk issue mutation](https://docs.sentry.io/api/events/bulk-mutate-a-list-of-issues/),
[project updates](https://docs.sentry.io/api/projects/update-a-project/), and
[grouping rules](https://docs.sentry.io/concepts/data-management/event-grouping/).
