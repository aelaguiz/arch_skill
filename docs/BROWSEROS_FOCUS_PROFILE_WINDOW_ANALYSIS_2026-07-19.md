# BrowserOS Focus, Profile, and Window Analysis

Date: 2026-07-19

## Executive verdict

Yes: the pre-change BrowserOS skill and operating guide already told agents to
open new pages in the background, minimize focus changes, list windows when
profile or visibility matters, prove the requested profile/account, and stop
rather than guess when the current tools cannot target the intended profile.
Those are the right foundations.

They were not a complete focus-management contract. The accompanying skill
revision closes the runtime gaps: it prohibits hidden surfaces, names the
foreground-changing calls that ordinary work must avoid, requires the
relevant active-page/window baseline, separates browser-internal state from
desktop application focus, and makes clear that window activation is neither
a direct/general profile selector nor profile or account proof.

The desired behavior is:

> BrowserOS should consume zero foreground takeovers by default. It should do
> normal page work against a normal non-hidden page ID in the background,
> never create or work from hidden tabs or windows, expose a task-owned
> containing window without activating it when window visibility alone is
> sufficient, and move desktop or browser focus only when the user explicitly
> asks to see or take over the page or a proven tool/site constraint requires
> it. When a focus change is unavoidable, warn once, batch the foreground work
> into one short phase, and report only the restoration that the tools can
> actually prove.

This report separates the issues that were previously conflated, evaluates the
live compact BrowserOS MCP surface, connects the behavior to recurring local
trace corrections, and records the runtime contract now folded into the
canonical `$browseros` skill.

## What the pre-change package already covered

The pre-change package was directionally strong. This is not a case where
focus or profile handling was omitted entirely.

| Pre-change rule | Owning location | What it got right | What was underspecified |
| --- | --- | --- | --- |
| List tabs before opening a page; list windows when profile, account, visibility, or recording matters. | `skills/browseros/SKILL.md`, Non-negotiables and First move | Prevented blind page/window creation and created a place to reason about context. | It did not separately require `tabs active`, identify the internally active window, or define which active state could be restored. |
| Use one normal non-hidden page and open it in the background when new. | `skills/browseros/SKILL.md`, opening rule | Directly reduced focus theft, hidden work, and tab accumulation. | It presented non-hidden as a default instead of directly prohibiting hidden tabs/windows, did not explicitly require `background=true`, and did not ban foreground creation except under a named exception. |
| Track temporary visibility or focus changes and restore pre-existing visibility when safe. | `skills/browseros/SKILL.md`, Lifecycle; `references/operating-details.md`, Lifecycle | Recognized focus and visibility as shared browser state. | Visibility and focus were conflated. The rule did not say which tool calls altered each layer or what was impossible to restore. |
| Prefer a normal non-hidden background tab and activate the exact window only when needed. | `docs/browseros_mcp_operating_guide.md`, Visibility and focus | Captured the correct default and acknowledged legitimate foreground needs. | "When needed" was not operationally defined, so agents could still activate for convenience, screenshots, polling, or manual-gate preparation. |
| Resolve the requested profile/account and fail closed if it cannot be targeted or proved. | `skills/browseros/SKILL.md`, First move; `references/operating-details.md`, Identity | Prevented wrong-profile mutations and false login blockers. | It did not say sharply enough that activation was never profile proof and was not a direct/general compact-schema profile selector; the current host's indirect placement behavior was a narrow, race-prone exception. |
| Do not open repeated pages hoping one lands in the right profile. | Core skill and operating details | Directly addressed a recurrent failure. | The safe alternative needed a clearer decision tree when the only correct-profile page was user-owned or another agent's page. |
| Report `Visibility/focus: restored, intentionally retained, or unknown`. | `skills/browseros/SKILL.md`, Completion receipt | Made browser-state side effects visible at completion. | "Restored" was too broad unless split into browser-internal state and desktop application focus. |

The pre-change operating guide also named focus stealing and wrong-profile work
in its failure register and its historical correction summary. The problem was
therefore not lack of awareness. The most important behavior was spread across
the core skill, a deep reference, and a long guide instead of being expressed
as a short, executable focus contract in the runtime path.

## Prioritized pre-change findings

| Priority | Finding | Consequence |
| --- | --- | --- |
| Critical | Deliberate BrowserOS activation was being used where page-targeted background operations already worked. | BrowserOS could interrupt the user's live typing at an unintended moment and make the workstation difficult to use safely. |
| Critical | Agents sometimes used active-window state as a proxy for profile/account identity. | Work happened in the wrong profile, or a signed-out default profile became a false login blocker. |
| High | The pre-change skill did not name the foreground-changing calls and their allowed exceptions. | The right high-level advice was easy to ignore at the exact call site. |
| High | The compact MCP cannot observe or restore the preceding non-BrowserOS desktop application. | A generic claim that "focus was restored" can be false or unprovable. |
| High | Parallel page ownership existed, but foreground focus had no single owner. | Independent agents could bounce BrowserOS windows into the foreground and make the machine difficult to use. |
| High | Compact page creation has no supported profile/window selector. | Agents are tempted to activate a window and hope the next page opens in the right context. |
| High | The pre-change runtime skill left room for hidden tabs/windows because non-hidden was phrased as a default instead of a prohibition. | Hidden surfaces consume browser resources, are absent from the normal user-visible tab strip, are easy to orphan, prevent immediate UI inspection/takeover until exposed, and may silently reuse an unintended hidden-window profile context. |
| Medium | Visibility, active window, active tab, DOM focus, and desktop focus were conflated. | Recording, manual handoff, interaction, and cleanup used stronger focus changes than the task required. |
| Medium | Foreground page creation made final cleanup itself focus-changing. | Closing the task page could select another page and create a second disruption. |

## Focus is five different states

The word "focus" hides five independent concepts. An operating agent must
name the layer it is changing.

| Layer | Meaning | Typical operation | User-visible risk | What BrowserOS MCP can prove |
| --- | --- | --- | --- | --- |
| Desktop application focus | Which macOS application receives the user's keyboard input: IDE, terminal, BrowserOS, and so on. | Focusing a BrowserOS window can bring the app to the foreground. | High: interrupts typing and changes the user's workspace. | The compact MCP does not expose the previously foreground macOS application and cannot restore it. |
| BrowserOS active window | Which BrowserOS window is internally active. | `windows activate`; some visibility or creation operations may also affect it. | Usually high because activation can also bring BrowserOS forward. | `windows list` can report BrowserOS window state, but not the preceding non-BrowserOS application. |
| Active tab/page | Which tab is selected inside a BrowserOS window. | Foreground page creation, popup behavior, tab activation in other surfaces, or closing the selected tab. | Medium to high: changes what the user sees and may redirect keyboard input. | `tabs active` can read the current front page, but the compact tool has no dedicated `tabs activate` restoration action. |
| In-page DOM/input focus | Which form control inside the target page receives synthetic page input. | `act` with `kind="focus"`, `fill`, `type`, `press`, or click. | Usually low when sent through the target's browser protocol session; it can still alter page state. | The page can usually be reread, but this is not proof of desktop or window focus. |
| Profile/account identity | Which browser profile/context and authenticated application account own the page. | Page/window selection plus context and in-app identity verification. | Critical if wrong: can cause false login blockers or mutate the wrong account. | Current tools provide incomplete mapping and no compact profile selector. Active state is not identity proof. |

These layers must not be inferred from one another. In particular:

- A tab can be non-hidden and discoverable in a visible window without that
  window being active; the tab's contents need not be selected.
- A BrowserOS window can be internally active while another macOS app is in
  front.
- A page can receive protocol-level click, keyboard, and DOM operations while
  its tab remains in the background.
- The active tab is not necessarily in the requested profile or account.
- Focusing a DOM element is not permission to focus the BrowserOS application.
- Making a page visible for inspection does not automatically justify moving
  the user's desktop focus.

## What the live compact MCP can and cannot do

The live tool-specific schema observed on 2026-07-19 is the authority for this
analysis. It was checked against the installed BrowserOS application
`0.47.13`, bundled server `0.0.126`, and a read-only inspection of that
installed implementation. A local BrowserOS source checkout at commit
`c656f623` is useful unminified corroboration, but it is older and has a wider
tool surface; it must not override the installed compact MCP schema or binary.
No live BrowserOS call was made for this analysis, and no page, tab, window,
profile, focus state, or external service was mutated.

### The older embedded-agent prompt is not protecting MCP callers

The local BrowserOS checkout's embedded prompt already contains unusually
direct focus guidance for BrowserOS's own built-in agent. It says, in effect,
that new pages should open in the background, page tools work against
background tabs by page ID, the agent should never force-switch the user's
active tab, and login or CAPTCHA handoff should let the user switch manually.
That is strong corroboration for the operating model in this report.

Ordinary Codex and Claude clients calling BrowserOS through MCP do not receive
that embedded `apps/server/src/agent/prompt.ts` prompt. They receive their own
agent instructions plus the exposed MCP tool schemas/descriptions. This is
why the rule must live in the canonical `$browseros` skill even though a local
BrowserOS source file appears to "already say it." The embedded prompt also
contains lifecycle assumptions—such as multi-tab grouping and leaving source
tabs open—that are not the desired canonical behavior for these external MCP
tasks. It is evidence about capabilities, not a contract to copy wholesale.

### Background-safe operations

The normal page tools accept a numeric `page` target and expose no activation
argument: `snapshot`, `diff`, `grep`, `read`, `navigate`, `act`, `evaluate`,
`screenshot`, `upload`, `download`, `pdf`, and `wait`. The local BrowserOS
implementation likewise resolves a protocol session for the target page and
does not call a bring-to-front primitive before ordinary navigation, reads,
screenshots, clicks, fills, or keyboard events. This supports the operational
conclusion that routine page work normally does not require foregrounding the
tab or window.

That is a capability statement, not a guarantee that a website will never
cause a popup or that an application bug can never move focus. It means an
agent should not deliberately activate a page or window merely to interact
with it. If a site action unexpectedly changes active state, the agent should
relist and reconcile it as a side effect instead of repeatedly reinforcing the
focus change.

Background-targetable is not identical to foreground semantics. A background
page can expose a different `document.visibilityState`, throttle timers or
media, defer paint, or require browser-chrome permission UI. Verify the real
postcondition, and move foreground only after a concrete constraint is
observed—not preemptively.

`tabs` with `action="new"` has the key option:

```text
background: true  # open without stealing focus
```

Supply it explicitly together with `hidden=false` for normal task pages, then
verify the page's actual containing window, visibility, and active state. The
schema also offers `hidden`, but hidden and background are not synonyms. Under
the user's explicit contract, do not create or work from hidden tabs or hidden
windows: do not use `tabs new hidden=true`, `windows create hidden=true`, or
hide a task window. Hidden surfaces still consume browser resources, are
absent from the normal user-visible tab strip, are easy to orphan, and prevent
immediate UI inspection or takeover until explicitly exposed. When host
routing places the requested page in an existing visible window,
`background=true` leaves the normal tab unselected. If no visible target
window exists, implicit visible-window creation may still affect focus; a host
default may also route unexpectedly. The flags are a request, not proof of the
result.

### Explicit or potentially foreground-changing operations

The following calls deserve special treatment:

| Operation | Effect or uncertainty | Default rule |
| --- | --- | --- |
| `tabs new` with `background=false` | Selects the newly created page and can change what the user sees. | Forbidden for ordinary automation. Use only for an explicit user-visible handoff or a proven constraint. |
| `windows activate` | Explicitly focuses the BrowserOS window. | This is a real focus takeover, not setup boilerplate. Do not use it for page reads, clicks, screenshots, polling, uploads, downloads, or profile guessing. |
| `windows set_visibility` with `activate=true` | Makes the window visible and focuses it. | Use `activate=false` when visibility alone is required. |
| `windows create` | The compact schema does not promise that creating a visible window preserves current focus. | Treat visible-window creation as possibly focus-changing and avoid it unless a separate window is genuinely required. |
| `tabs new hidden=true` or `windows create hidden=true` | Creates a user-UI-hidden but still resource-consuming browser surface that is easy to forget and may reuse a hidden context. | Do not use hidden tabs or windows. Background a normal non-hidden tab instead. |
| Closing the currently selected task-created tab | The browser may select another tab and change visible state. | Avoid making task tabs active in the first place. If one is active, treat closure as a focus-changing cleanup operation. |
| Popup, OAuth, download, or site-created window | Site/browser behavior can change active state outside the initiating call's obvious contract. | Relist immediately, attribute the new resource, and avoid extra activation. |

The compact MCP currently has no dedicated `tabs activate` action. Therefore,
if an agent deliberately foregrounds a new tab, it may be able to observe the
previous front page with `tabs active`, but it does not have a symmetrical,
documented compact operation to restore that exact tab. That asymmetry is an
additional reason to stay backgrounded.

The live `tabs` description also claims that inventory is grouped by current
agent, user, and other agents. The installed handler and the 2026-07-18 live
inventory recorded in the main guide instead return a flat page/URL/title
list. Focus, ownership, page-to-window membership, and browser context must
therefore come from the fields actually returned by a current call and from
the task ledger—not from the shared namespace description.

### Visibility without takeover

When the user needs a window to be visible—for recording, inspection, or an
upcoming manual step—but does not need BrowserOS to interrupt their current
application, the intended path is:

```text
windows action="set_visibility" windowId=<current-window-id> visible=true activate=false
```

This is materially different from `windows activate`. An agent should not
translate "make it visible," "leave it where I can inspect it," or "use the
recorded window" into "bring BrowserOS to the foreground" unless the request
actually requires that result.

`set_visibility` is window-only. Use it only after proving that the containing
window is task-controlled and its current membership and profile context are
safe to reveal; ownership of one page is not enough. It can expose the window
without focusing it, but it does not select an existing background tab. If the
exact tab contents must be displayed, the compact surface may require the user
to select it or an explicitly authorized deeper mechanism; do not pretend that
showing the window selected the page.

### Restoration limits

BrowserOS MCP can inspect BrowserOS-internal page/window state. It does not
expose the macOS application that had focus before the task, nor an operation
to return focus to that application. As a result:

- If the agent never uses a focus-changing call, it can report that it made no
  deliberate foreground change.
- If the agent changes a BrowserOS window's visibility and successfully
  restores that visibility, it can report that specific restoration. A
  visibility transition can replace the window and return a new window ID, so
  restoration must track the returned current ID rather than reuse a stale
  baseline handle blindly.
- If the agent changes the active BrowserOS window and later restores the
  previously active BrowserOS window, it can report browser-window restoration
  only if current state proves it.
- It cannot honestly claim that desktop application focus was restored unless
  another explicitly authorized, capable OS-level mechanism proves it.
- If the active tab changed and the compact surface cannot reactivate the
  baseline tab, the tab-focus result is intentionally retained or unknown—not
  "restored."

The implemented completion receipt therefore splits the pre-change combined
field into these evidence-sized statements:

```text
Foreground takeover: <none, intentional, unexpected, or unknown>
Browser window/tab state: <unchanged, restored, changed/unrestored, intentionally retained, or unknown>
Window visibility: <unchanged, restored, changed/unrestored, intentionally retained, or unknown>
Desktop app focus: <not changed deliberately, user-controlled, or not observable>
```

## Why focus stealing kept happening

The recurring failures were not one bug. They came from several agent habits
and pre-change tool-contract gaps that compounded one another.

### 1. Activation is treated as harmless setup

An agent sees several windows, chooses one, and calls `windows activate`
before every subsequent operation as if activation were required to target
the page. It is not. Normal page tools target a page ID directly. Activation
adds user disruption without adding page identity, ownership, or mutation
authorization.

### 2. Foreground creation is used to make automation feel observable

An agent opens a new tab in front so it can "see" what it is doing. The MCP's
semantic and visual tools already address the target page directly. A
foreground tab is not needed for snapshots, screenshots, readback, polling,
uploads, downloads, or ordinary interaction.

### 3. Visible and active were conflated

Recording and manual-takeover requirements often require a normal page in a
visible BrowserOS window. They do not always require BrowserOS to seize the
desktop immediately. The pre-change guide acknowledged this distinction but
did not turn it into a hard call-level rule; the revision now does.

### 4. Profile selection is attempted through focus

The agent activates a window it believes is the Work window and then opens a
tab, assuming the new tab will inherit that window/profile. The current
compact `tabs new` schema has no `windowId`, browser-context, or profile
argument. The schema does not promise an activate-then-open handoff.
Activation is never profile proof and is not a direct/general compact-schema
profile selector. A narrow current-host indirect placement behavior is
documented below and must not be generalized.

### 5. Manual gates are "helpfully" foregrounded

When a CAPTCHA, 2FA prompt, login, secure-field entry, or approval gate
appears, the agent may bring BrowserOS forward before asking the user to take
over. The user can switch when ready. Unless the user asked the agent to show
the page, an unrequested activation interrupts whatever the user was doing at
exactly the moment the agent is pausing.

### 6. Polling and proof cause repeated foreground churn

Agents sometimes reactivate a page before every snapshot, wait, screenshot,
or readback. This can produce repeated focus flicker even when one initial
takeover might have been defensible. Page-targeted polling and proof should
remain backgrounded.

### 7. Cleanup changes the selected tab

If the agent opened its task tab in front, closing it at the end can select a
different tab. This creates a second visible disruption and makes restoration
ambiguous. Background creation avoids both the initial and cleanup focus
changes.

### 8. Parallel workers had no focus owner

Independent agents can safely operate independent page IDs in the background,
but two agents activating windows can fight over the same human desktop. A
per-page ownership ledger alone did not prevent that. The revision now treats
foreground operations as a global shared resource and serializes them under
one focus owner.

### 9. The pre-change receipt overstated recovery

A generic `Visibility/focus: restored` line encouraged the agent to collapse
visibility, active BrowserOS window, active tab, and desktop application into
one success claim. Because the MCP cannot observe the preceding macOS app,
that claim could be stronger than the evidence. The revision splits these
states into separate receipt fields.

### 10. Hidden tabs make lifecycle and resource use invisible

A hidden tab can look attractive because it avoids visible focus changes, but
it still consumes browser memory, CPU, timers, network activity, and server
bookkeeping. Because it is absent from the normal tab strip, the user cannot
immediately see, inspect, take over, or close it through the ordinary UI until
it is exposed, and an agent can easily forget it during cleanup. The installed
server can also reuse a cached hidden window, making hidden creation a
particularly bad way to acquire a requested profile. Focus discipline must use
normal non-hidden background tabs, not user-UI-hidden browser state.

## Correct profile and window selection

Focus discipline and profile correctness are related, but one cannot solve the
other.

### The identity gate

Before credentialed or mutating work, the target needs this evidence:

```text
current agent has dispatch control over the page
+ current task authorizes this exact workflow
+ supported window/profile or browser-context evidence
+ sanitized origin and stable path
+ expected application shell or title
+ stable authenticated account/workspace marker
+ exact object to read or change
```

Neither an active marker nor a window number satisfies that tuple by itself.
The user can have the same site open in several profiles; the active window can
be the default profile; a remembered ID can drift; and a login page in one
context does not prove logout in another.

### What `windows list` contributes

Window inventory is necessary when profile, visibility, recording, or manual
takeover matters. It can establish BrowserOS window IDs, visibility, active
state, and sometimes an active-tab handle. In the current compact contract it
does not provide a reliable human profile name, and a flat tab inventory may
not establish page-to-window membership.

Therefore:

- List windows, but do not pretend the inventory proves profile identity.
- Do not join independent tab and window results by numeric resemblance or
  list position.
- A window's `activeTabId` is a native tab ID, not an MCP `page` ID. Correlate
  it only through a selected page's separately returned native `tabId`, such as
  from a supported `browser.pages.getInfo(page)` result.
- For a current-agent-controlled candidate page, use only a bounded supported
  page-info/context query when the live schema provides it.
- A returned `browserContextId` can support current profile mapping; it still
  does not prove the site account or workspace.
- Verify the authenticated account or workspace inside the application before
  mutation.
- Never infer profile from "active," newest tab, title, or tab order.

### The current targeting hole

The live compact `tabs new` call cannot name a target window or profile, and
`windows create` cannot name a profile. This creates a real boundary:

1. If the current agent already owns a compatible page whose profile and
   account can be proved, use it in the background.
2. If another agent owns the correct page, resume that exact agent. Do not use
   raw CDP to cross the ownership boundary.
3. If the user owns the correct page, ask the user to complete the step or use
   a future supported claim/handoff mechanism. A page becoming visible does
   not transfer ownership.
4. If no current-agent-owned page can be placed in and proved against the
   required profile, stop. Do not activate windows and open repeated pages
   until one happens to work.

This can be frustrating, but it is the only honest current behavior. Acting in
the wrong profile is worse than reporting that the compact MCP lacks the
necessary targeting primitive.

### Why "activate the Work window, then open" is not a general rule

An older BrowserOS server surface accepted a `windowId` when opening a page.
The live compact tool observed for this report does not. Old traces or local
source can therefore make an activate-then-open sequence look more supported
than it currently is.

The canonical skill permits such a sequence only if a current repository
runbook plus installed behavior supports the handoff and the resulting page's
context/account is immediately verified. Otherwise, `windows activate` steals
focus without establishing profile placement.

There is a dated current-host nuance. Read-only installed-code/config
inspection—not a live behavior test—indicates that, when the host supplies no
request-default window and no concurrent actor changes the active window
between calls, a visible `tabs new` falls back to the active visible BrowserOS
window. Thus activate-then-open is an implementation-backed, focus-changing,
race-prone inference on this host, not a compact-schema guarantee. A
host-supplied default window can also override the fallback. Verify the
result immediately: `tabs new` itself returns only an MCP page ID, so query
supported page-info/context evidence for that new page, such as a bounded
authorized `browser.pages.getInfo(page)` call, and then verify the in-app
account. Treat this as an explicitly justified exception—not general setup for
every profile-bound task.

The installed lower-level page manager can technically accept a `windowId`
through privileged `run`/CDP use. The current skill correctly forbids using
that undocumented lane for normal page creation because it bypasses the
compact lifecycle contract and can become an ownership side door. It is a
product capability lead, not permission for ordinary agents to route around
the skill.

Hidden page creation is prohibited by the user's operating contract and is
also unusable as a profile-acquisition trick: the installed server can reuse a
cached hidden window from another browser context. A normal non-hidden
background page in a verified window remains the right profile-bound shape.

## Trace evidence

### Method

Two independent history sweeps used the `$agent-history` helper across all
available projects from 2026-06-01 through the end of 2026-07-19:

- The two Codex queries inspected 5,484 and 5,485 helper source rows
  respectively, with zero parse errors. Their broad match totals were not used
  as incident counts; exact submitted prompts were deduplicated by full text
  and confirmed in bounded rollout context.
- The Claude sweep covered 3,375 helper-indexed sources—1 global prompt-recall
  file, 1,563 root project transcripts, and 1,811 sidechain transcripts—with
  zero parse errors. It counted direct human-authored turns once, even when
  also stored in a project transcript, and excluded tool results, task
  notifications, compaction summaries, and assistant-authored delegation
  prompts that happen to be stored with a transport-level `user` role.

Counts below are deduplicated direct-user correction, constraint,
target-routing, or analysis/request turns—not independent BrowserOS defects.
Several turns can belong to one incident, and one resumed session can be
copied into several physical rollout files. Dates and opaque session/thread
IDs are included only where they materially establish recurrence; snippets,
private paths, page contents, account details, URLs, and tool payloads are
omitted or sanitized.

The following operational census is separately sourced from the
[main operating guide's evidence section](browseros_mcp_operating_guide.md#evidence-basis-and-dated-local-findings),
ends on 2026-07-18, and was not recalculated by the focused correction-history
sweeps:

| Runtime | Deduplicated BrowserOS calls | Successful tab opens | Successful tab closes |
| --- | ---: | ---: | ---: |
| Codex | 14,398 | 428 | 307 |
| Claude | 8,173 | 158 | 90 |
| Combined | 22,571 | 586 | 397 |

The 189-call open/close gap is not a count of unwanted tabs: some opens were
intentional deliverables, and some closes may have targeted older pages. It is
evidence of accumulation risk when combined with the direct corrections and
the prior live inventory of 33 open pages.

### Focused correction counts

| Runtime | Exact direct-user evidence | Interpretation |
| --- | --- | --- |
| Codex | 14 distinct prompts explicitly paired focus theft with a correction, constraint, or analysis request, across 7 sessions and 7 working directories. Six were reactive and eight were preventive/follow-up. | Focus theft is recurrent, not one isolated task. The distinction between reactive and preventive is semantic and therefore inferred. |
| Codex | 10 broad target-routing/reuse prompts involving one tab, an already-open tab, the right window, or equivalent active-target language. | Some are proactive routing requests rather than corrections. Collectively they show repeated need for explicit target binding; only a subset directly concerns wrong-profile selection. |
| Codex | 2 visibility directives, 1 exact typing-interruption correction, and 1 exact suspicion that mouse commands were pulling a window forward. | The user impact included actual keyboard-input disruption, not merely aesthetic annoyance. |
| Claude | 9 exact wrong-profile/window/browser correction turns across 6 sessions from July 3–9. | The dominant qualifying Claude correction family in this targeted sweep was wrong surface selection. Nine turns do not mean nine independent incidents. |
| Claude | 1 exact BrowserOS focus-stealing complaint, 2 visibility/recording directives, and 1 BrowserOS-generated modal-interruption complaint. | Claude independently exhibited focus/visibility friction, but its direct corpus did not contain the same explicit keyboard-impact wording as Codex. |
| Claude | 5 additional direct requests or recovery steps about reusing an existing tab/window, reducing to one window/tab, closing excess windows, or closing old tabs. | Lifecycle sprawl and correct-window selection reinforce one another. |

The focused sweeps and the user's current explicit requirements resolve into
the same operating families across both runtimes:

- stop opening extra tabs and windows;
- reuse the already-open BrowserOS page;
- use the requested Work profile/window instead of a convenient default or
  personal profile;
- keep the relevant page visible when the user is recording or expects to
  inspect or take over it;
- use visible, takeover-friendly BrowserOS surfaces; the user's current
  operating contract now explicitly forbids hidden pages and windows;
- preserve the user's focus and do not bring BrowserOS forward for every
  interaction; and
- close old or excess related pages that no longer serve a purpose. Automatic
  cleanup remains limited separately to pages proved task-created and owned.

### Representative incidents

#### Repeated interaction pulled BrowserOS forward

The strongest Codex cluster is session
`019f1ecd-995c-7630-aee8-95409c2ac560`, from July 1–5. On July 1, three direct
corrections in four minutes asked whether the interaction method was stealing
focus, told the agent to stop, and clarified the intended policy: opening a
necessary window can be acceptable; bringing the browser forward every time
the agent taps is not. On July 2 and July 3, the same thread explicitly asked
for one tab, minimal focus theft, and reuse of an already logged-in page.

On July 4, the user reported that repeated focus stealing caused them to be
"randomly typing" when focus moved. The stored turn does not prove the exact
destination of those keystrokes, but it establishes live keyboard interruption.
That makes unnecessary focus takeover a correctness and workstation-usability
problem, not just a preference.

The assistant's contemporaneous explanation named repeated profile launches,
`Page.bringToFront`, real coordinate clicks, and visible-tab navigation as
plausible causes and proposed background protocol/DOM interaction for routine
work. This is exact assistant-authored context, not proof of current tool
behavior; the installed implementation audit establishes the current
activation semantics separately in this report's capability section.

#### The already-open Work page was not selected

In Codex session `019f0ae0-dab8-71e2-8144-47d6e8b8ec32`, the user repeatedly
specified one tab, the Work profile, and an already-open page. A later direct
correction explained that the required page was already open in the Work
profile. The immediate assistant response admitted it had treated the first
exposed tab as the only session instead of proving the available Work-profile
target. This is exactly the identity-binding failure the skill must prevent.

Claude shows the same pattern independently. The fresh sweep found nine
wrong-profile/window/browser correction turns across sessions including
`a005bc78-e177-4bd0-baa7-d94f5cd261ba`,
`187b7475-3947-463e-a4f2-303153a85d7c`, and
`09f07230-eca2-4d83-839c-4bd5e3ac80ce`. The corrections included using
BrowserOS rather than Chrome, staying in the Work profile, reusing the Work
window already open, and stopping the creation of additional windows.

One especially clear Claude case in session
`187b7475-3947-463e-a4f2-303153a85d7c` drove a page in the wrong window/profile,
reached a signed-out SSO screen, and reported a login blocker. The user twice
redirected it to the Work window, saying the application was already open
there. Subsequent tool evidence showed that the Work-window page was
authenticated, and the task proceeded. This incident demonstrates two
separate points:

1. A login page in the active or conveniently created page is not evidence
   that the requested account is logged out.
2. Bringing a window forward is not the same as proving that a task page is in
   the correct profile and account.

#### Non-hidden and background answer different requirements

The evidence says not to hide this automation. A June 23 Codex instruction
required visible BrowserOS tabs, and a July 9 instruction required that
BrowserOS never use hidden tabs for this work. Claude had two direct
visibility cases: one asked that possibly hidden work be made visible;
surrounding turns show an hCaptcha challenge immediately before and the user
completing it ten seconds later. The other required the exact visible tab
because it was the only one being recorded.

The history supports a combined requirement: keep the task tab non-hidden and
discoverable, select/display it when recording or immediate takeover actually
requires that state, and avoid unnecessary foreground activation. The current
capability audit separately establishes that ordinary operations can target a
normal non-hidden page in the background. "Background" describes
selection/focus; "non-hidden" describes whether the user can find the tab in
the ordinary UI. They are not opposites. Hidden tabs are not a
focus-preservation strategy under this contract.

#### Background flags do not explain every perceived focus event

Claude's exact focus complaint in session
`187b7475-3947-463e-a4f2-303153a85d7c` arrived shortly after a BrowserOS page
had been created with both background and hidden flags and before another
BrowserOS screenshot. The sequence is exact, but the history does not prove
which individual call moved focus. A site popup, hidden-window transition,
a separate screencast subscription, or another concurrent action could have
been involved. The installed ordinary screenshot operation itself does not
bring the page forward. This is why the contract needs both safe explicit
calls and after-the-fact reconciliation of unexpected side effects.

Another Claude complaint reported repeated BrowserOS "leave" confirmation
modals that demanded manual input. That is not necessarily desktop focus
theft, but it is another form of avoidable user interruption consistent with
navigation or close side effects. The trace does not identify which page
triggered the modal or whether it was the wrong target.

#### Parallel foreground ownership makes the machine unusable

Codex sessions `019f5c32-3a41-7303-bdb7-30a11e5de9fb` and
`019f621a-c57d-73a1-b581-7b4aced6c17e` show the broader shared-desktop
failure. One prompt asked whether mouse commands were pulling windows forward
and ordered that behavior stopped. Another reported multiple agents fighting
over foreground ownership and making the computer effectively unusable.
Although the latter incident involved simulator tooling as well as the same
desktop-control problem, it demonstrates that uncoordinated foreground actions
from parallel workers can make the workstation unusable. It therefore
motivates a single-owner or otherwise serialized foreground protocol; the
history does not by itself select that implementation mechanism.

#### Explicit focus remains allowed

The desired rule is not "BrowserOS may never take focus." On July 18, Codex
session `019f7524-0088-7bd2-b0af-4ad942127771` contained an explicit request to
focus a tab. Together with the July 1 clarification that necessary windows may
be opened, this supports the operational boundary: foreground when the user
explicitly asks or when the workflow genuinely requires it, rather than as
routine setup for every interaction. Requiring the agent to prove and announce
that necessity is the recommended contract derived from the evidence.

The history findings are behavioral evidence, not a promise that old tool
names or exact flows still work. The live compact schema and installed
implementation control current operation.

## Canonical focus contract

The following rules now live in the runtime path of the `$browseros` skill.
They are intentionally specific enough to change tool behavior.

### Default: zero foreground takeovers

- Treat foreground focus as a scarce shared resource with a default budget of
  zero deliberate takeovers.
- Run normal page-targeted reads, navigation, interaction, screenshots,
  uploads, downloads, waits, and verification in the background.
- When a new page is justified, request exactly one with `hidden=false` and
  `background=true`, then verify its actual containing window, visibility, and
  active state. When routed to an existing visible window, this produces the
  intended normal unselected tab; the flags are not proof against every host
  routing or window-creation side effect.
- If no visible target window exists, treat any implicit visible-window
  creation as focus-capable. If host routing places the page in a hidden
  window, do not work through it.
- Never create or use hidden tabs or hidden windows. Do not hide a task window
  to avoid focus; keep a normal tab non-hidden and operate it in the
  background.
- Do not activate a tab or window to make automation observable to the agent.
  Use BrowserOS observation tools.
- Do not activate before polling, retrying, screenshotting, or cleanup.

This is a default, not an absolute ban. A site or browser defect may still
cause an unexpected focus change, and some user-facing steps legitimately
need the foreground.

### Capture the right baseline

Before a task that might affect windows, visibility, profile context, or user
takeover:

1. Call `tabs list` for lifecycle inventory. Derive provenance and ownership
   from the task ledger, creation receipts, and fields actually returned—not
   the generic grouped-ownership description.
2. Call `tabs active` to record the current front BrowserOS page when the
   result is available.
3. Call `windows list` to record BrowserOS active/visible window state.
4. Record that desktop application focus is not observable through BrowserOS
   MCP.
5. Do not expose sensitive URL queries, fragments, account IDs, or session
   values in the baseline.

For a read-only background task that cannot alter focus, full window
inventory remains unnecessary. The baseline should be proportional to the
operations the task may perform.

### Name the only normal exceptions

A deliberate foreground change is justified when one of these is true:

- The user explicitly asked to bring up, show, select, or focus the page now.
- The user is recording/watching and the requested result specifically
  requires the exact page to be the selected visible page.
- A manual security or approval step is ready and the user explicitly asks
  the agent to present it.
- A current tool/site constraint has been proved to require foreground state,
  and no background-safe alternative completes the authorized task.

Convenience, agent confidence, screenshots, ordinary input, waits, downloads,
uploads, stale refs, retries, and profile guessing are not exceptions.

### Warn once and batch foreground work

When an exception applies:

1. Tell the user briefly that BrowserOS focus is about to move and why.
2. Perform one short, serialized foreground phase.
3. Avoid repeated activation between steps.
4. Complete all required user-visible operations in that phase.
5. Restore only the BrowserOS-internal state the tools can prove, unless the
   user requested the page remain visible/active.
6. Report desktop app focus as unobservable rather than claiming restoration.

### Use window visibility without activation

- If the requirement is merely that a containing window be visible, use
  `set_visibility` with `activate=false` only after proving that the window is
  task-controlled and its current membership and profile context are safe to
  reveal. This does not select an existing background tab.
- Keep "visible," "selected tab," "active BrowserOS window," and "foreground
  macOS application" separate in reasoning and receipts.
- Do not create or work from hidden pages or windows. They consume resources,
  conceal lifecycle state from the normal user-visible tab strip, and prevent
  immediate UI inspection or takeover until exposed.
- If a task-caused page unexpectedly appears hidden, do not continue working
  invisibly. Safely attribute it. Expose its window without activation only
  when window-level ownership, membership, and profile context are proved;
  otherwise close only the verified page when safe or retain/report it.
- Do not activate a visible equivalent page merely because it is easier to
  describe.

### Keep manual gates user-controlled

For CAPTCHA, 2FA, login, secure-field entry, consent, or a manual approval:

- Pause and identify the safe page/window context without sensitive details.
- Ask the user to switch to BrowserOS when ready.
- Do not activate the window unless the user asked to have it presented.
- After the user finishes, relist and revalidate the page, profile/account,
  and object before continuing.

### Serialize focus across agents

- Background page work may run in parallel on independent agent-owned pages.
- Any operation that can activate, show-and-activate, foreground-create, create
  a visible window directly or implicitly, or close the selected page must
  have one coordinator-designated focus owner.
- Workers that do not own the focus phase must not call those operations.
- Batch all unavoidable foreground work under that owner; do not let workers
  bounce the desktop between windows.
- Page ownership still applies independently: focus ownership does not permit
  one agent to act on or clean another agent's page.

### Make cleanup focus-safe

- Prefer task-created pages that were backgrounded and never selected; they
  can usually be closed without changing what the user sees.
- If a task-created page is currently selected, classify closure as a
  potential focus change and compare it to the recorded BrowserOS baseline.
- Close transient pages promptly so later cleanup does not require a large
  visible state change.
- Perform cleanup before any final user-requested presentation of a page, so
  cleanup does not undo the intended visible end state.

### Use an honest receipt

Replace the combined focus field with evidence-sized statements. Examples:

```text
Foreground takeover: none deliberately made
Browser window/tab state: unchanged
Window visibility: unchanged
Hidden browser surfaces: deliberately created 0; task-caused observed 0; unknown 0
Desktop app focus: not changed deliberately; not observable through BrowserOS MCP
```

```text
Foreground takeover: one intentional handoff at the user's request
Browser window/tab state: intentionally left on the requested page
Window visibility: unchanged
Hidden browser surfaces: deliberately created 0; task-caused observed 0; unknown 0
Desktop app focus: user-controlled after handoff
```

```text
Foreground takeover: unexpected site-created popup
Browser window/tab state: changed/unrestored; popup closed but prior active tab could not be restored
Window visibility: unchanged
Hidden browser surfaces: deliberately created 0; task-caused observed 0; unknown 0
Desktop app focus: not observable
```

If no applicable window inventory was performed, report `not inventoried`
instead of asserting that no unexpected hidden surface existed. `Deliberately
created 0` refers to the current task's own calls; it does not claim that the
shared browser had no pre-existing hidden state or that a site could not spawn
a hidden surface as a task-caused side effect.

## Implemented BrowserOS package changes

This analysis accompanies the implementation. The revision touches the
smallest owning surfaces below.

### `skills/browseros/SKILL.md`

The revised core skill establishes:

- Normal page tools operate against page IDs and do not justify window/tab
  activation.
- Request `hidden=false` and `background=true` for new normal pages, then
  verify actual routing, visibility, and active state.
- Prohibit `hidden=true`, hidden-window creation, and hiding task windows;
  background work uses a normal non-hidden page.
- Do not call `windows activate`, `tabs new background=false`, or
  `windows set_visibility activate=true` unless a named foreground exception
  applies.
- Window activation is never profile proof and is not a direct/general profile
  selector. Document the current-host indirect handoff only as a verified,
  race-prone exception.
- Expose a containing window without activation only when the window is
  task-controlled and its membership/profile context are proved safe; do not
  claim that this selects the page.

For focus-capable work, First move now requires:

- Record `tabs active` and BrowserOS active/visible window state before a
  focus-capable lifecycle call.
- State that preceding desktop application focus is outside BrowserOS MCP's
  observable/restorable state.

Parallel browser work now requires:

- Assign one focus owner and serialize foreground operations.
- Allow other workers to continue independent background operations.

For page work, the completion receipt replaces the combined field with
separate applicable foreground, browser-internal state, hidden-surface, and
desktop-focus statements; connector-only work omits irrelevant browser
lifecycle boilerplate.

### `skills/browseros/references/operating-details.md`

The reference adds a compact operation-level contract covering:

- background-capable page tools;
- the prohibition on hidden tabs/windows and its resource, visibility,
  takeover, cleanup, and profile-context rationale;
- explicit foreground-changing calls;
- visible versus active;
- manual-gate behavior;
- current restoration limitations; and
- focus-owner serialization for parallel agents.

The profile section now allows an indirect activate-then-open exception only
when a current runbook and inspected host/configuration establish the
fallback, no request-default window overrides it, the race is controlled, and
the result is immediately verified. Activation alone is not presented as the
general solution; dated host-specific details remain in docs rather than
timeless runtime doctrine.

### `skills/browseros/agents/openai.yaml`

The default prompt now advertises safe task-authorized reuse, a verified normal
non-hidden background tab, minimized foreground takeover, relevant
profile/account proof, and lifecycle cleanup at the point where direct
BrowserOS use is routed.

### `docs/browseros_mcp_operating_guide.md`

The guide links to this focused analysis and carries the same explicit
operation-level contract so the runtime skill and deep guide do not diverge.

## Acceptance scenarios for this revision

These are behavior scenarios, not wording tests.

### Background research while the user types in an IDE

- Agent lists pages and reuses a safe task-authorized page or requests one with
  `hidden=false` and `background=true`, then verifies its actual window,
  visibility, and active state.
- Agent snapshots, navigates, acts, waits, screenshots, and reads the page by
  ID.
- Agent never calls a window activation operation.
- Agent closes its unused task page.
- Agent creates no hidden page or window.
- Receipt reports no deliberate foreground takeover and does not claim to have
  measured the macOS foreground application.

### A business site must use the Work profile

- Agent lists tabs and windows and checks supported page/context evidence.
- Active/default state is not accepted as profile proof.
- Agent verifies an in-app account/workspace marker before mutation.
- If the compact MCP cannot create or own a page in the Work profile, the
  agent stops for a supported handoff or manual completion instead of
  repeatedly activating windows and opening guesses. The current-host
  activate-then-open exception is used only when explicitly justified and
  immediately reverified.

### The user asks for a visible page but does not ask to be interrupted

- If "visible" means discoverable for later takeover, the agent uses a normal
  non-hidden background tab in a visible window.
- If the user needs the page contents displayed now, the agent does not claim
  that `set_visibility` selected the background tab. It asks the user to select
  it or uses an explicitly authorized supported handoff.
- Agent does not create, adopt for work, or hide pages/windows as a focus
  workaround.
- BrowserOS is not deliberately brought to the desktop foreground.

### The user says "bring it up so I can finish 2FA"

- Agent verifies the exact page/profile/account first.
- Agent warns once that focus will move.
- One focus owner activates the exact window once. If the compact surface
  cannot select the required existing tab, the user selects it rather than the
  agent pretending that window activation displayed the page.
- Agent pauses for the user and does not keep polling with repeated
  activations.
- After confirmation, agent relists and revalidates before continuing.

### A site unexpectedly opens a popup in front

- Agent treats it as an unexpected side effect, relists, and records it.
- Agent does not repeatedly activate either window.
- Agent completes or closes only the task-owned popup when safe.
- Receipt distinguishes popup cleanup from unknown desktop focus restoration.

### Several agents use BrowserOS in parallel

- Each worker owns a distinct page and lifecycle ledger.
- Background work proceeds independently.
- One coordinator owns the only foreground phase.
- No worker calls an activating operation outside that phase.
- Each worker reconciles its own pages; the coordinator reports the shared
  focus outcome.

## Product-level improvements that would remove ambiguity

Skill doctrine can prevent unnecessary takeovers, but several MCP additions
would make correct profile and focus behavior much easier to guarantee.

1. Add `windowId` or browser-context/profile targeting to compact `tabs new`.
   Return the actual window/context used.
2. Include page-to-window and browser-context mapping in `tabs list`, with a
   safe stable profile label when available.
3. Add an explicit tab-selection operation and a symmetric browser-internal
   focus restoration primitive.
4. Return before/after active page, active window, visibility, and a
   `focusChanged` indicator from lifecycle calls.
5. Make non-activating behavior the schema-level default everywhere,
   especially `set_visibility` and any future show-page operation.
6. Distinguish "BrowserOS internally active" from "BrowserOS is the foreground
   desktop application" if the platform can expose that safely.
7. Add an explicit page ownership handoff/claim workflow instead of forcing a
   choice between manual work and a new, potentially wrong-profile page.
8. Document whether visible-window creation preserves desktop focus and
   whether closing a background/active page changes the selected tab.
9. Make hidden lifecycle state obvious in inventory and resource accounting
   until hidden creation can be disabled at the policy/schema layer.

These changes would reduce both focus theft and wrong-profile automation. In
particular, a targetable `tabs new` would remove the temptation to use
`windows activate` as an undocumented profile-selection side door.

## Bottom line

The pre-change BrowserOS package addressed the user's complaint, but not with
enough precision to make the behavior reliable. The revision retains its
correct high-level foundations—background pages, window inventory, profile
proof, visibility tracking, and fail-closed targeting—and adds an explicit
zero-focus budget, a prohibition on hidden tabs/windows, a five-layer focus
model in the analysis, call-level prohibitions, a single focus owner for
parallel work, and an honest statement of what the current MCP cannot restore.

The most important operational sentence is simple:

> Target the page in the background. Do not activate BrowserOS merely to use
> it, never hide the page from the user, and never treat focus as profile proof
> or as a general profile-targeting mechanism.
