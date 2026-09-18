# BrowserOS Profiles and Focus

Read before selecting a profile, creating a page, changing focus or visibility,
or arranging manual browser input.

## Contents

- Target an existing profile window
- Focus, visibility, and hidden surfaces
- Identity and profile constraints

## Target an existing profile window

Read only the safe profile labels and directory keys needed from
`profile.info_cache` in
`~/Library/Application Support/BrowserOS/Local State`; do not dump the file or
personal account fields. Correlate them with current `Browser.getWindows`
results through BrowserOS `run`. Saved profile and window IDs are hints until
matched to live evidence.

When a new page is justified, use the live-supported
`browser.pages.newPage(url, {background: true, windowId})` targeting the verified
existing window. Require a normal, non-hidden result under the entry contract;
verify the returned page's actual window/context, visibility, and active state.
If the route exposes a hidden flag, set it false. If it cannot establish those
facts, do not proceed through that page.

Keep the working profile label, window, page, and safe application marker in
the current task notes. Verify the site's authenticated context independently
of the browser profile. Do not navigate a preserved page away for diagnostics.

## Focus, visibility, and hidden surfaces

Routine page work is background-targetable. `snapshot`, `diff`, `grep`,
`read`, `navigate`, `act`, `evaluate`, `screenshot`, `upload`, `download`,
`pdf`, and `wait` address a verified page ID and normally do not need its tab
selected or its window activated. `act` with `kind="focus"` focuses a DOM
element inside that page; it does not mean the BrowserOS window or desktop
application needs foreground focus.

Protecting the user's focus is a primary requirement on this shared machine.
An unexpected activation can interrupt typing or redirect input. Judge the
actual operation and work through viable background methods, including supported
page-targeted interaction, extraction, and file transfer, before taking focus.
This is not a fixed retry count or a checkbox satisfied by one failed call.

Background-targetable does not promise identical foreground semantics. A page
that is not selected may report a different visibility state, throttle timers
or media, defer paint, or need browser-chrome permission UI. Verify the real
postcondition and investigate whether supported background methods can complete
the operation. If it needs foreground behavior, use the minimum necessary
takeover without a separate approval question. Say why once, keep the work in
one brief phase, and return to background operation. Restore prior browser
focus when the tools support it and the user has not since chosen another
target. Do not claim to restore desktop focus the tools cannot observe.

`background` and `hidden` are different:

- Request `tabs new` with `hidden=false` and `background=true`. When the host
  routes it into an existing visible window, this creates a regular unselected
  tab in the normal tab strip. The flags are the required request shape, not
  proof of the result: verify the page's actual containing window, visibility,
  and active state. If those facts cannot be established, do not work through
  the new page; reconcile or report it.
- `tabs new` or `windows create` with `hidden=true` creates a browser surface
  outside the normal user-visible tab/window surface. Never use it. Hidden
  surfaces still consume resources, are easy to orphan, delay user inspection
  or takeover, and can carry an unintended hidden-window profile context.
- Do not hide a task window as a workaround. If an action unexpectedly creates
  a hidden task-owned surface, stop working through it and reconcile it under
  the lifecycle rules.
- If no visible target window exists, report the missing prerequisite.
  Do not let `tabs new` implicitly create one without the user's request.

Treat these operations as foreground-capable shared-state changes:

| Operation | Contract |
| --- | --- |
| `tabs new` with `background=false` | Selects the new page; use only when the operation needs foreground behavior after working through viable background methods. No separate focus approval is required. |
| `windows activate` | Focuses a BrowserOS window; never use for routine targeting, observation, polling, screenshots, or profile guessing. |
| `windows set_visibility` with `activate=true` | Shows and activates a window; use `activate=false` when visibility alone is sufficient. |
| `windows create` | Requires an explicit user request; ordinary work reuses existing windows. |
| Closing the selected task page | May select another tab; treat it as focus-capable cleanup. |
| Site-created popup or window | May change active state; relist, attribute, and avoid reinforcing the takeover. |

To expose a uniquely task-owned containing window without focusing it, use
the live equivalent of:

```text
windows action="set_visibility" windowId=<current-window-id> visible=true activate=false
```

`set_visibility` operates on a window. It does not select an existing
background tab. Its result may supply a replacement window ID, so track the
returned ID instead of reusing a stale handle.

Before a focus-capable task phase, record `tabs active` when available and the
BrowserOS active/visible window state. BrowserOS can prove only the
browser-internal state exposed by its current tools. It cannot observe or
restore the previously focused non-BrowserOS desktop application. The compact
surface may also lack a symmetrical action to reselect the exact baseline
tab. Report only the restoration current state proves.

For CAPTCHA, 2FA, login, secure-field entry, consent, or another manual gate,
verify and identify the safe page/window without sensitive details, then ask
the user to switch to BrowserOS when ready. A manual input requirement does not
itself justify taking focus while the user is doing other work. After the user
finishes, relist and revalidate the page, profile/account, and target before
continuing.

## Identity and profile constraints

Expect the user's `Work` profile and a variable number of ChatGPT consultation
profiles, labeled `Pro 1`, `Pro2`, and so on, to have
windows open at the same time. Inspect their actual mapping and keep the
working profile/window/page identified in the existing task notes. Recheck the
target before every interaction and readback, with fresh live membership and
safe application identity after navigation, switching, recovery, or resuming,
and before sends, mutations, and cleanup. This attention continues throughout
the task; a successful startup check is not enough. Matching titles, projects,
or URLs across profiles do not identify the account, and foreground activation
does not prove which profile a page belongs to.

For ChatGPT, select only the existing consultation profiles: the ones labeled
`Pro 1` through `Pro5` or whichever are configured. The `Work` profile is
reserved for the user's personal ChatGPT use and rate-limit capacity. Do not
use it when a consultation profile is limited, lacks a connector, or contains
no matching conversation.

A profile label is a name the user typed for a browser profile. `Pro 1` says
which profile and login a page belongs to, exactly as `Work` does. It does not
select, imply, or prove the ChatGPT model, mode, or plan in that page. Record
the label on the profile line of the task notes and nowhere else; the selected
model is separate in-site state that `$chatgpt-web` reads from the page.

Build page identity from both ephemeral handles and semantic evidence:

```text
current-agent dispatch control
+ current-task authorization
+ creation receipt handles when returned
+ intended window/profile or browser context
+ sanitized origin and stable path
+ application title or shell
+ safe account/workspace marker
+ exact object being read or changed
```

Keep query strings and fragments out of the ledger. Page IDs, window IDs,
target IDs, context IDs, session IDs, and refs can drift; they address a
verified identity but never replace it.

The current compact `tabs new` schema has no target-window or profile
argument, and `windows create` has no profile selector. Tab inventories may
be flat and may omit page-to-window mapping. Derive ownership only from the
task ledger, creation receipts, and fields actually returned. Do not combine
separate lists and invent an association.

For a selected current-agent-controlled page, a bounded
`browser.pages.getInfo(pageId)` call through `run` may provide window or
browser-context evidence when the live schema supports it. Use that only for
identity, not broad inventory or dispatch bypass. Do not assume a window
result's `activeTabId` is an MCP page ID: it can be a native tab ID. Correlate
it only through a supported page-info result that returns both identities.
A `browserContextId` can support a profile mapping but does not prove which
account or workspace is authenticated inside the application.

Use the explicit existing-window targeting route above. Do not activate
a window as a profile fallback or open repeated pages hoping one lands in the
right profile. If supported targeting cannot establish the intended context,
report that blocker. A user-opened page remains user-owned under the current
no-claim schema.

A diagnostic profile-path page is not a profile-acquisition mechanism. Never
navigate a preserved application page away merely to inspect its profile.
