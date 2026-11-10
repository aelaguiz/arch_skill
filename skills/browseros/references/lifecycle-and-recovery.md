# Lifecycle and Recovery in BrowserOS neo

Read the relevant section before cleanup, recovery of an unknown outcome, or
browser work divided among agents.

## Contents

- Task notes and reconciliation
- Lifecycle
- Mutation safety
- Failure classification and recovery
- Parallel ownership
- Completion receipt

## Task notes and reconciliation

Use the task's existing notes; no new tracking system is needed. Record the
bound profile and directory, your tab group id, pages and windows you
created (including a created window's starting tab, which reads as `user`),
pages of others you were asked to work in, exact paths of local artifacts,
and anything retained or unknown.

At completion reconcile unique resources, not calls:

```text
pages created = closed + intentionally retained + unknown/orphan
windows created = closed + intentionally retained + unknown/orphan
artifacts created = removed + intentionally retained + unknown
```

Retry and read back in the same page you created. If you must replace it,
verify the replacement before closing the old one. Never close a page with
an unresolved change on it just to make the counts balance.

## Lifecycle

`ownership` in `browser.pages.list()` tells you whose a page is now, but
your notes tell you what you created: after a reconnect your own pages read
`other-agent`, and a created window's starting tab reads `user`. Duplicate
pages can share a URL and title, so match on page ID plus your notes, not
on title.

List pages after any action that can open a tab, a callback, a download
page, or a window, and once at final cleanup. Do not claim a page just
because it appeared after you started; a concurrent user or agent may have
opened it. Report a page you may have caused but cannot attribute as an
orphan.

A timed-out open, close, navigation, or window call has an unknown outcome:
list before opening another page, prove a page is gone before reusing its ID,
and read the page's current URL before navigating again.

Before closing a tab group with `tab_groups` `close`, list it and prove every
member is yours. Before closing a window you created, prove every page in it
is yours. Never close a window you did not create. Turn off focus emulation
on pages you keep.

When the bound profile was loaded only for this task, leave it loaded; other
agents may be using it.

## Mutation safety

Treat a timed-out change as unknown, not failed: saves, sends, publishes,
schedules, uploads, purchases, deletes. A single read of the old value can
race an operation still running. Retry only after the application shows a
settled state that proves the change did not land, or the change is safe to
repeat by nature. Otherwise report it as unknown; a sleep is not proof.

Do not use broad destructive selectors or loops. Check the exact object and
how many elements a selector matches immediately before acting. Permission
for named objects does not cover every matching control in a container.

Recovery does not license changing the user's workflow: do not cancel a
schedule, switch accounts, change a purchase path, or revoke a credential
because it makes recovery easier.

## Failure classification and recovery

| Symptom | Class | First response |
| --- | --- | --- |
| Argument validation error | Call error | Read the tool's live schema and correct the call. |
| Missing or stale ref | Page changed | Snapshot again and retry once with a fresh ref. |
| A handle from an earlier turn fails instantly | Tab gone or no longer yours | Do not retry it; relist `mine` pages or open a fresh one. |
| `page_out_of_scope` | Popup or a page outside the bound profile | Check the binding; popups are not reachable (`logins-and-oauth.md`). |
| `profile_gone`, `pinned_window_closed`, `default_profile_unavailable` | Stale binding | `browser_target` `get`, then `set` or `clear` explicitly. |
| `target_change_in_run` | Rebinding inside `run` | Rebind with `browser_target` between calls. |
| Run died at about 30 seconds | Wall-clock cap | Split the work into smaller runs; the timeout cannot be raised. |
| Success reported, page unchanged | Site ignored input or wrong target | Reread the application state. |
| Sparse snapshot | Page readiness or extraction | Use `read`, `grep`, or a bounded `evaluate_in_page`. |
| `browser session not connected` | Neo not running or paired | Tell the user to start BrowserOS neo; do not switch browsers. |
| HTTP 5xx or closed channel | Transport | Reconnect, `browser_target` `get`, then one small read-only listing. |
| Login page or account chooser | Wrong profile until proved otherwise | `get`; outside `Work`, reopen the site in `Work`. |
| CAPTCHA, code prompt, or password | Sign-in gate | Work it yourself (`logins-and-oauth.md`). |

Recovery order:

1. Read the exact error; a failed `run` returns it with captured logs.
2. Do not repeat the same expensive call unchanged.
3. Reacquire the binding, page, or refs when stale.
4. Read back ambiguous state before any retry.
5. Use a smaller honest proof when the requested one is not available.
6. Restart neo only as a last step, with the user's say-so and after
   making sure no other agent's work or unresolved change is in flight.
   Afterwards rebind and rediscover every page and ref.

If the same operation fails twice, change approach or name the exact
blocker. An unknown change is not a failed attempt and is never repeated to
reach that count.

## Parallel ownership

Give each agent its own browser task, not the parent's pages. Each agent
binds its own profile in its own session, opens its own pages, and returns
created, closed, retained, and unknown counts. Never let two agents drive or
poll the same page at once. Neo runs at most a handful of pages per agent
comfortably; serialize large screenshots and long scripts.

If a child leaves a page open, resume that child for cleanup. If it cannot
be resumed, the parent closes the pages that child's receipt records
creating, after matching each live page to the receipt. A page no receipt
explains stays an orphan to report.

## Completion receipt

Return the result first, then:

```text
Browser result: <outcome or exact blocker>
Target: <non-sensitive site/workspace/object label>
Profile: <bound profile name, read back with browser_target get>
Proof: <what proves it, and its limits>
Change outcome: <not applicable, verified, or unknown, with readback>
Pages: created <n> = closed <n> + retained <n> + unknown/orphan <n>
Focus: none taken; site-caused tab or window changes <none, or which>
```

Add windows or artifacts only when the task touched them, and retained or
unknown detail only when there is some. Never invent a zero for state you
did not look at. Keep emails, account IDs, signed URLs, callback URLs,
session data, and sensitive file links out of the receipt.
