# Profiles and Focus in BrowserOS neo

Read before binding a profile, creating a window, or working a page that
misbehaves in the background. `SKILL.md` owns the rules; this file has the
mechanics. Tool descriptions are the source of truth for exact arguments.

## Contents

- Bind and verify the profile
- A profile with no window
- Background work and hidden pages
- Calls that take focus, and what to use instead
- Identity beyond the profile

## Bind and verify the profile

```text
browser_profiles action="list"            -> names, directories, loaded or not
browser_target   action="set" name="pro3" -> binds this task's session
browser_target   action="get"             -> binding + live status
browser_target   action="clear"           -> back to Work (Default)
```

`set` takes the exact, case-sensitive name or a `browserProfileId`. It only
records intent: it loads nothing and opens nothing. `get` reports the bound
name and directory, whether the profile is loaded, its normal windows, and
any error such as `profile_gone` or `pinned_window_closed`. A stale binding
never falls back to whatever window is focused; it fails until you rebind or
clear.

Inside `run`, `browser.target({action: 'get'})` reads the same status, and
`page.info()` returns the page's `browserProfileId`, `windowId`, and
`isActive`. A page whose `browserProfileId` matches the binding's is in that
profile. `browserProfileId` values last one browser run; the name and
directory are what go in notes.

Every listing and page call sees only the bound profile's normal windows.
That is why the binding is the proof: an unbound session that lists a
ChatGPT tab is looking at `Work`'s ChatGPT, whatever the tab title says.

`browser_target` `set_window` chooses which of the profile's windows new
pages go to; `strict=true` pins every call to it. Use it when the profile
has several windows and the user wants your work in one of them.

## A profile with no window

Most profiles are not loaded until someone uses them. When `get` shows no
windows:

1. `browser_profiles` `action="load"` (no name loads the bound profile).
2. `windows` `action="create"`: an inactive normal window in that profile.
3. Find the window's starting tab in `browser.pages.list()` (it reads
   `ownership: "user"` and `chrome://newtab/`) and put your first page there
   with `browser.page(id).goto(url)`. Opening a second tab with
   `browser.open` while the window holds only its starting tab has brought
   neo to the front of the user's screen; navigating the starting tab has
   not.
4. Record the window and that tab as created by this task. Later
   `browser.open` calls in that window open background tabs normally.

Keep that window for the rest of the task. Close it at the end only when
every page in it is one you created.

## Background work and hidden pages

Every page tool and every `run` page method addresses a page ID or handle
and works on an unselected tab: read, snapshot, grep, act, navigate, wait,
screenshot, upload, download, pdf. `act` `kind="focus"` focuses an element
inside the page, not the window.

Neo's background tabs normally report `document.visibilityState` as
`visible` and `document.hasFocus()` as true, so pages render and respond as
if in front. If a page still shows the hidden-tab symptoms (a menu marked
closed that stays in the DOM and blocks clicks, a dialog or iframe that
stays empty, a Save bar that never appears, a button waiting for focus such
as GitHub's OAuth Authorize), check and repair it in one `run`:

```js
const page = browser.page(PAGE_ID);
const state = async () => (await page.evaluateInPage(() =>
  ({vis: document.visibilityState, focus: document.hasFocus()}))).value;
const before = await state();
await page.cdp('Emulation.setFocusEmulationEnabled', JSON.stringify({enabled: true}));
return {before, after: await state(), tabSelected: (await page.info()).isActive};
// expect after = {vis: 'visible', focus: true} and tabSelected false.
// When the step is done:
// await page.cdp('Emulation.setFocusEmulationEnabled', JSON.stringify({enabled: false}));
```

Reload after enabling it when the page settled its state at load.
A failure that persists with the page visible and focused is usually your
own call: a stale ref, the wrong element (a hidden fallback textarea), a
menu you left half-open (a reload clears it), or an input method the page
ignores. Read the live element and fix the call.

## Calls that take focus, and what to use instead

| Never | Use instead |
| --- | --- |
| `Page.bringToFront`, `Target.activateTarget`, `Browser.activateTab` through `page.cdp` or `browser.cdp` | Focus emulation on that page, when it acts hidden |
| `browser.open` into a window that holds only its starting tab | `goto` on the starting tab |
| `windows` `create` when the profile already has a window | The existing window; `browser_target` `set_window` to choose among several |
| `osascript`, `open -a`, or anything that activates an app | Nothing; leave the desktop alone |
| Handing a URL to the system's default browser (`open <url>`, a CLI's browser launch) | `browser.open` in the right profile |

A site action can still open a tab or a popup. Relist, report it, and leave
it; activating something to undo it interrupts the user twice.

When a step truly needs the user, leave the page as it is, name the profile
and tab title, and let them switch to it when they are ready. After they say
it is done, relist and reread the page and binding before acting.

## Identity beyond the profile

The profile says which cookie jar a page uses. It does not say which account
or workspace the site is signed into, and matching titles or project names
across profiles prove nothing. Before authenticated work, read a safe
in-site marker (the workspace or project name) on the page itself, and keep
it in the notes beside the profile, page ID, and sanitized origin and path.
Leave query strings, fragments, emails, and tokens out of notes.

Page IDs, window IDs, and refs change when tabs close, the browser restarts,
or the page rerenders. They address something you verified; they are not
the verification. Never navigate a page you are preserving away just to
check where it is.
