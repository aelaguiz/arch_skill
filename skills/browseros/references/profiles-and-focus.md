# BrowserOS Profiles and Focus

Read before selecting a profile, creating a page, working a page that
misbehaves while hidden, changing window visibility, or arranging manual
browser input.

## Contents

- Target an existing profile window
- Background work and hidden pages
- Identity and profile constraints

## Target an existing profile window

`SKILL.md` owns the profile check and the rule that pages open only through
`newPage` with a `windowId`. Read only the safe profile labels and directory
keys from `profile.info_cache`; do not dump the file or personal account
fields. Saved profile and window IDs are hints until matched to live evidence.

When a new page is justified, use
`browser.pages.newPage(url, {background: true, windowId})` targeting the verified
existing window. Require a normal, non-hidden result under the entry contract;
verify the returned page's actual window/context, visibility, and active state.
If the route exposes a hidden flag, set it false. If it cannot establish those
facts, do not proceed through that page.

Keep the working profile label, window, page, and safe application marker in
the current task notes. Verify the site's authenticated context independently
of the browser profile. Do not navigate a preserved page away for diagnostics.

## Background work and hidden pages

Routine page work runs on an unselected tab. `snapshot`, `diff`, `grep`,
`read`, `navigate`, `act`, `evaluate`, `screenshot`, `upload`, `download`,
`pdf`, and `wait` address a page ID and never need the tab selected or its
window activated. `act` with `kind="focus"` focuses an element inside the page,
not the window.

### When a hidden page misbehaves

An unselected tab reports `document.visibilityState === 'hidden'` and
`document.hasFocus() === false`, and runs no animation frames. Pages react in
recognizable ways:

- a menu or popover is marked closed but stays in the DOM, blocking clicks and
  typing behind it;
- a dialog or iframe loads but stays empty;
- a Save/Discard bar never appears after an edit;
- a button waits for page focus before enabling, as GitHub's OAuth Authorize
  button does;
- a picker lists its items, but a coordinate click on an item does nothing.

Turn on focus emulation for that page, confirm it took effect, retry the step,
and turn it off when the step is done:

```js
const P = PAGE_ID;
await browser.cdpJsonForPage(P, 'Emulation.setFocusEmulationEnabled', JSON.stringify({enabled: true}));
const r = await browser.cdpJsonForPage(P, 'Runtime.evaluate', JSON.stringify({
  expression: 'JSON.stringify({vis: document.visibilityState, focus: document.hasFocus()})', returnByValue: true}));
return {page: JSON.parse(r.result.value), tabSelected: (await browser.pages.getInfo(P)).isActive};
// expect {vis: 'visible', focus: true} and tabSelected false; after the step:
// await browser.cdpJsonForPage(P, 'Emulation.setFocusEmulationEnabled', JSON.stringify({enabled: false}));
```

Emulation stays on across a reload of that page. Reload after enabling it when
the page settled its state at load, such as a button that enables only once
the page has focus. Finishing animations from script
(`document.getAnimations()` then `finish()`) does not help a hidden page,
because the animation's end event still waits for a rendered frame.

A failure that persists with emulation on is usually in your own call. Common
causes:
- a selector that does not match;
- the wrong element, such as a hidden fallback textarea;
- a stale ref;
- a menu you opened and left half-closed (a reload clears it);
- an input method the page ignores.

Read the live element and fix the call.

### Calls that take focus, and what to use instead

| Never | Use instead |
| --- | --- |
| `newPage` or `tabs new` with `background: false` | `newPage(url, {background: true, windowId})` |
| `windows activate` or `Browser.activateWindow`, including to target or inspect a window | `windowId` on `newPage`; `Browser.getWindows` and `pages.list` for window and tab state |
| `Page.bringToFront`, `Target.activateTarget`, `Browser.activateTab` | Focus emulation on that page |
| `windows create` | An existing window of the right profile; a new window only when the user asks for one |
| `windows set_visibility` with `activate=true` | `activate=false` |
| `osascript` or `open -a` activating any app | Nothing; leave desktop focus alone |

Close only tabs this task created. They are unselected, so closing them moves
no selection. A site action can still change the selected tab or open a
window, for example a popup, a link that opens a tab, or a "branch in new chat"
control. When that happens, relist, report it, and leave it. Activating
something to undo it would interrupt the user a second time.

`background` and `hidden` are different:

- Open a page with `newPage`, `background: true`, and the target `windowId`;
  set `hidden` false where the live schema offers it. This creates a regular
  unselected tab in that window's normal tab strip. The arguments are the
  request, not proof of the result: verify the page's actual containing
  window, visibility, and active state. If those facts cannot be established, do not work through
  the new page; reconcile or report it.
- A tab or window created with `hidden=true` is a browser surface
  outside the normal user-visible tab/window surface. Never use it. Hidden
  surfaces still consume resources, are easy to orphan, delay user inspection
  or takeover, and can carry an unintended hidden-window profile context.
- Do not hide a task window as a workaround. If an action unexpectedly creates
  a hidden task-owned surface, stop working through it and reconcile it under
  the lifecycle rules.
- If no visible target window exists, report the missing prerequisite.
  Do not let a tab call implicitly create one without the user's request.

To expose a uniquely task-owned containing window without focusing it, use
the live equivalent of:

```text
windows action="set_visibility" windowId=<current-window-id> visible=true activate=false
```

`set_visibility` operates on a window. It does not select an existing
background tab. Its result may supply a replacement window ID, so track the
returned ID instead of reusing a stale handle.

For a sign-in gate (password, code prompt, CAPTCHA, consent), first prove the
page is in `Work`; a gate elsewhere is the wrong window, not a gate. Then work
it yourself in the background tab as `logins-and-oauth.md` says, with focus
emulation when the page misbehaves hidden. When a step truly needs the user
(their phone, a passkey, a secret only they hold), keep the page as a
background tab, name the profile and tab title, and let them switch to
BrowserOS when ready. After the user finishes, relist
and revalidate the page, profile/account, and target before continuing.
`logins-and-oauth.md` owns the sign-in mechanics.

## Identity and profile constraints

Expect the user's `Work` profile, a variable number of ChatGPT consultation
profiles labeled `pro1`, `pro2`, and so on, and other profiles the user keeps
to have windows open at the same time. Inspect their actual mapping and keep the
working profile/window/page identified in the existing task notes. Recheck the
target before every interaction and readback, with fresh live membership and
safe application identity after navigation, switching, recovery, or resuming,
and before sends, mutations, and cleanup. This attention continues throughout
the task; a successful startup check is not enough. Matching titles, projects,
or URLs across profiles do not identify the account, and foreground activation
does not prove which profile a page belongs to.

For ChatGPT, select only the existing consultation profiles: the ones labeled
`pro1`, `pro2`, and so on, whichever are configured. The `Work` profile is
reserved for the user's personal ChatGPT use and rate-limit capacity. Do not
use it when a consultation profile is limited, lacks a connector, or contains
no matching conversation.

The Terms table in `SKILL.md` owns what each label and word means. Record the
label on the profile line of the task notes and nowhere else; the selected
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

The `tabs new` schema has no target-window or profile argument, so it is
never used to open a page, and `windows create` has no profile selector. Tab inventories may
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
