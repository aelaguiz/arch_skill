# BrowserOS Lifecycle and Recovery

Read the relevant section before resource cleanup, recovery of an unknown
outcome, or browser work divided among agents.

## Contents

- Task notes and reconciliation
- Lifecycle and state-change reconciliation
- Mutation safety
- Failure classification and recovery
- Parallel ownership
- Completion receipt

## Task notes and reconciliation

Use the existing task notes; no new tracking system is needed. Record baseline
resources, the verified profile/window/page, adopted pages and allowed use,
created resources and exact local artifact paths, and retained or unknown state.
When focus changes, record only browser state the tools can actually observe.

At completion reconcile unique resources, not the number of calls:

```text
pages created = closed + intentionally retained + unknown/orphan
windows created = closed + intentionally retained + unknown/orphan
groups created = removed + intentionally retained + unknown
artifacts created = removed + intentionally retained + unknown
```

Navigate the same task-created page for retries and readback. If replacement is
necessary, verify one replacement before closing the uniquely identified old
page. Never close an unresolved mutation merely to reconcile the counts.

If an unknown mutation's original page is wedged, use at most one separately
recorded read-only verifier page in the proved correct profile. Read authoritative
state before deciding whether the original action can be repeated.

## Lifecycle and state-change reconciliation

Store creation receipt handles and sanitized semantic identity when a page is
opened. Duplicate pages can share the same URL and title, so semantic matching
alone may be insufficient for safe closure.

Relist after any action that can spawn a popup, callback, preview, download
page, or window, and once at final cleanup. Match new resources to the action
receipt and sanitized application evidence. Do not claim an unrelated
concurrent user or agent page merely because it appeared after the baseline;
record a possibly task-caused but unattributable resource as unknown/orphan.

Browser lifecycle calls change shared state. A timeout during `tabs new` or
`close`, navigation, `windows create`, `close`, `activate`, or
`set_visibility`, or a tab-group change has an unknown outcome:

- after a timed-out open, relist before opening another page;
- after a timed-out close, prove whether the page disappeared and never reuse
  a stale page number blindly;
- after timed-out navigation, inspect current identity before navigating
  again; and
- after a timed-out window or group operation, relist its contents and state.

If several task-created pages need a group, group only those pages. Before
closing a group, relist it and prove every current member is task-created and
intended to close. Otherwise close pages individually or ungroup retained
pages.

Before closing a task-created window, prove every current page inside it is
task-created and intended to close. If the live schema cannot establish page
membership, close only individually verified task-created pages and retain or
report the window rather than risking a user or other-agent page.

Track temporary focus and visibility changes. Restore a pre-existing window's
visibility when safe unless the user requested the final visible state. Never
close a pre-existing window.

Task calls should deliberately create zero hidden surfaces. If a task action
unexpectedly causes one, attribute it from the action receipt and current
identity evidence. Expose the containing window with `activate=false` only
when that window is task-controlled and its current page membership and
profile context are proved safe to reveal. If only the page is proved or
window membership is unknown, close only the verified page when safe or retain
and report it; do not expose the whole window.
Keep window visibility, selected/active BrowserOS state, and desktop
application focus separate: restore and report each only when the applicable
tool evidence proves it.

## Mutation safety

Treat a timed-out mutation as unknown rather than failed. This applies to
saves, sends, publishes, schedules, uploads, purchases, deletes, and connector
actions. A single old-value read can race an operation that is still running.
Retry only after authoritative readback proves the mutation did not land and
the application presents a terminal state, or its processing indicator has
cleared and authoritative state stays stable across a bounded reread. An
inherently idempotent, duplicate-safe operation is the only exception.
Otherwise report the mutation as unknown; an arbitrary sleep is not settlement
proof.

Do not use broad destructive selectors or loops. Validate exact object
identity and selector cardinality immediately before acting. Authorization for
named objects does not authorize every matching control in a container.

Recovery does not authorize changing the user's workflow. Do not cancel a
schedule, switch accounts, alter a purchase path, revoke a credential, or
change another user-visible choice merely because it simplifies recovery.

## Failure classification and recovery

| Symptom | Class | First response |
| --- | --- | --- |
| Argument validation error | Schema/call error | Read the live schema and correct the call. |
| Missing or stale ref | Page changed | Snapshot again and retry once with a fresh ref. |
| Element not visible | UI/viewport state | Scroll, snapshot, and retry once. |
| Unknown, closed, or wrong page/window | Identity/lifecycle | Relist and revalidate the full identity tuple. |
| Success acknowledgment without UI change | Site input or wrong target | Reread actual application state. |
| Empty or sparse snapshot | Extraction/page readiness | Try bounded `grep`, `read`, or small `evaluate`. |
| Screenshot timeout | Large-response pressure | Use a small semantic probe or a smaller screenshot. |
| One page hangs after a long evaluation | Execution still running | Stop stacking calls on that target. |
| HTTP 500/503 or closed channel | Transport/server lifecycle | Wait once, rediscover, and issue one small read-only tab probe. |
| Login page or account chooser | Wrong window until proved otherwise | Prove the profile; outside `Work`, reopen the site in `Work` (`SKILL.md`, "Logins, SSO, and OAuth"). |
| CAPTCHA or 2FA | Manual security gate | Pause for the user. |

Use this recovery order:

1. Read the exact error and classify the failed boundary.
2. Do not repeat the same expensive call unchanged.
3. Reacquire identity or refs when stale.
4. Use one small read-only inventory probe for transport recovery.
5. Read back ambiguous state before any retry.
6. Use a smaller honest proof when the requested proof rail is unhealthy.
7. Use a repository-authorized deeper MCP or CDP rail only to preserve the
   existing authenticated session, never to broaden authority.
8. Restart BrowserOS only at the final rung with user authority and after
   coordination proves no other active user or agent work and no unresolved in-flight
   mutation would be interrupted. If that cannot be proved, do not restart.
9. After restart, rediscover every page, window, context, and ref.

If the same operation fails twice, change diagnostic layer or name the exact
blocker. An unknown mutation is not a failed attempt and must not be repeated
to satisfy this threshold. Do not call every schema, site, or page failure
“BrowserOS instability.”

## Parallel ownership

Assign independent browser tasks, not parent-owned pages. Each agent selects
or creates its own page, records exact paths for its own local outputs, and
returns created, closed or removed, retained, and unknown resource counts.
Never let two agents act or poll the same page concurrently.

Designate one focus owner for any phase that can activate a window,
foreground-create a tab, create a visible window directly or implicitly,
show-and-activate a window, or close a selected page. Serialize those
operations. Other agents may continue independent background work, but must
not make foreground-capable calls. Focus ownership does not transfer page
ownership.

Saved-artifact analysis can be parallel only after authorization and
sanitization. Serialize large screenshots and long evaluations so agents do
not overload the shared BrowserOS transport.

If a child leaves a page open, resume that exact child for cleanup. If it
cannot be resumed, report the page as an orphan for manual cleanup. A fresh
agent or deeper rail must not defeat the ownership boundary.

## Completion receipt

Return the requested result first, then these core receipt fields:

```text
BrowserOS result: <completed outcome or exact blocker>
Target: <non-sensitive site/workspace/object label>
Proof: <proof rail and limitation>
Mutation outcome: <not applicable, verified, or unknown; safe readback evidence>
```

For page work, add this page-state block:

```text
Pre-existing pages adopted/reused: <unique count>
Working profile/window/page: <verified safe profile label and current handles>
Pages: created <n> = closed <n> + retained <n> + unknown/orphan <n>
Hidden browser surfaces: deliberately created 0; task-caused observed <n>; unknown <n or not inventoried>
Foreground takeover: <none deliberately made, intentional, unexpected, or unknown>
```

Add resource reconciliation for windows, groups, or artifacts only when the
task touched them. Add browser window/tab state, window visibility, and
desktop app focus when focus- or visibility-capable work occurred or those
states were inventoried. Add retained-state or unknown/orphan detail only when
nonempty. Never fabricate a zero for shared state that was not inventoried.

```text
Windows: created <n> = closed <n> + retained <n> + unknown/orphan <n>
Groups: created <n> = removed <n> + retained <n> + unknown <n>
Artifacts: created <n> = removed <n> + retained <n> + unknown <n>
Browser window/tab state: <unchanged, restored, changed/unrestored, intentionally retained, or unknown>
Window visibility: <unchanged, restored, changed/unrestored, intentionally retained, or unknown>
Desktop app focus: <not changed deliberately, user-controlled, or not observable>
Retained or unknown state: <safe identity, reason, and risk>
```

For connector-only work, omit browser lifecycle fields and add the
BrowserOS-managed connector/service, exact safe action or query, structured
outcome, and readback limitation.

Do not put emails, account IDs, signed URLs, raw callback URLs, session data,
or sensitive artifact links in the receipt.
