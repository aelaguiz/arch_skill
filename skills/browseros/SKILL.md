---
name: browseros
description: "Canonical preflight and operating contract for direct BrowserOS MCP use. Read and apply before the first BrowserOS MCP call whenever an agent will operate tabs, windows, or authenticated pages; upload or download files; capture screenshots; read or mutate web or BrowserOS-managed connector state; recover from BrowserOS errors; or coordinate browser work across agents. It owns non-hidden background operation, foreground-focus discipline, page lifecycle, dispatch-versus-task authorization, target and profile verification, observe-act-verify, timeout recovery, secrets, proof, and cleanup. Use it alongside narrower site skills such as $chatgpt-web, which own the site workflow while this skill owns BrowserOS mechanics. Not for BrowserOS installation or vendor development, generic connectors, or browsing that does not use BrowserOS MCP."
---

# BrowserOS

Apply this contract before the first direct BrowserOS MCP call. The
goal is to complete the user's requested browser outcome while leaving the
shared authenticated browser no less understandable, safe, or clean than it
was at the start.

For page work, reuse one normal non-hidden, task-designated page. If a new page
is necessary, request exactly one with `hidden=false` and `background=true`.
When routed into an existing visible window, this produces a regular
unselected tab in the normal tab strip. Treat the flags as a request, not
proof: verify the new page's actual window, visibility, and active state, and
do not work through it if those facts cannot be established or host routing
placed it in a hidden window. Reconcile or report that page instead. Prove the
requested result, then clean up every page, window, or group the task created
and no longer needs.

## Scope

This skill owns BrowserOS mechanics: page selection and provenance, tab and
window lifecycle, interaction, proof, recovery, secrets, and cleanup. A
narrower site skill still owns its site-specific workflow. When `$chatgpt-web`
or another BrowserOS-backed skill applies, use both contracts; this one goes
first and governs every BrowserOS call.

For a connector-only task, skip page inventory and lifecycle work. Still apply
the exact-target, authorization, live-schema, mutation, unknown-outcome,
secret, and proof rules in this contract and its connector reference.

Do not use this skill for BrowserOS installation, server development, vendor
debugging, or generic web research performed through another browser tool.

## Required context

Treat the user's request, applicable repository instructions, and the live
BrowserOS schema and results as ground truth. Tool names and result shapes
drift; live tool-specific schemas outrank remembered names, shared overview
text, saved configuration, and old traces.

Read [references/operating-details.md](references/operating-details.md) before
opening a new page; profile- or account-specific work; focus- or
visibility-capable lifecycle work; recording or manual takeover;
BrowserOS-managed connector work or other external mutations; OAuth or
secret-bearing flows; uploads or downloads; timeout recovery; raw `run` or CDP
use; or live browser work split across agents. The core contract is sufficient
for an ordinary single-page read-only task on a compatible current page.

## Non-negotiables

- For page work, list tabs before opening one. List windows when profile,
  account, visibility, or recording context matters.
- Reuse one normal non-hidden page. A new page needs a concrete
  simultaneous-state requirement, explicit user request, or lack of a safe
  authorized page for the task. When justified, request exactly one with
  `hidden=false` and `background=true`, then verify its actual window,
  visibility, and active state; convenience is not enough.
- Never create or work from hidden tabs or hidden windows, and never hide a
  task window as a focus workaround. Hidden surfaces consume resources while
  staying outside the normal user-visible tab strip and are easy to orphan.
- Ordinary page-targeted tools operate against a page ID without requiring
  tab or window activation. Keep reads, navigation, interaction, screenshots,
  uploads, downloads, waits, and verification backgrounded unless a concrete
  observed constraint requires foreground state.
- Default to zero deliberate foreground takeovers. Do not use
  `windows activate`, `tabs new` with `background=false`, or
  `windows set_visibility` with `activate=true` for routine work. When the
  user explicitly requests a foreground handoff or a proved constraint has no
  background-safe alternative, warn once, serialize it, and avoid repeated
  activation.
- Creating a visible window is focus-capable. This includes `windows create`
  with `hidden=false` and `tabs new` when no visible target window exists and
  the host must create one. Use either only when genuinely required, capture
  the focus baseline, warn that focus may move, and serialize the call.
- Window activation is never profile or account proof and is not a direct or
  general profile selector. Verify supported page-to-window/context evidence
  and an in-application account or workspace marker before credentialed or
  mutating work.
- Require both current-agent dispatch control and current-task authorization
  before acting. A technically reachable page is not automatically safe for
  this task.
- Record every task-created page, window, and tab group immediately. Do not
  rely on BrowserOS to return ownership metadata consistently.
- Validate the page, profile/account context, site, and exact object before a
  credentialed or mutating action. A numeric page ID is only an ephemeral
  handle.
- Observe, act once, inspect the change, and verify the requested
  postcondition. An acknowledged click is not proof.
- Treat every timed-out or disconnected state-changing call as unknown. Read
  current state before retrying or cleaning up.
- Prefer semantic reads over screenshots. Use pixels only when the claim is
  visual.
- Keep secrets, callback query strings, signed URLs, and raw session data out
  of authored scripts, ledgers, logs, screenshots, and receipts.
- Never use `run`, CDP, another agent, or another browser to bypass an
  ownership rejection or broaden the user's authorization.
- Stop BrowserOS work immediately when the user says stop.

## First move for page work

1. Resolve the requested outcome, intended site/account/profile, mutation
   authority, and the proof needed to call the task complete.
2. Inspect the live BrowserOS tool-specific schema for any nontrivial call.
3. List tabs. When profile, visibility, recording, manual takeover, or a
   focus-capable lifecycle action matters, also read the current active page
   and list windows.
4. Record a sanitized baseline: page handle, origin plus stable path without
   query or fragment, title, any returned window/context evidence, known
   provenance, and relevant BrowserOS active-page/window and visibility state.
   The previously focused non-BrowserOS desktop application is not observable
   or restorable through BrowserOS MCP.
5. If profile or account context matters and the live schema cannot target or
   prove the intended context, stop for a supported targeting handoff or ask
   the user to complete that browser step manually. Do not open pages hoping
   one lands in the right profile; a user-opened page does not become
   agent-controlled automatically.
6. Otherwise choose one current-agent-controlled page that this task may use.
   Only when no compatible authorized page exists, request exactly one with
   `hidden=false` and `background=true`, then verify its actual containing
   window, visibility, and active state. If no visible target window existed,
   treat any implicit visible-window creation as focus-capable. If the page
   state cannot be established or it landed hidden, do not work through it;
   reconcile or report it under the lifecycle rules.

## Page provenance

Classify pages on two independent axes:

1. **Dispatch control:** current-agent controlled, user-owned,
   other-agent-owned, or unknown.
2. **Task authorization:** task-created, safely task-adopted for one workflow,
   or not authorized for action.

Act only when both axes allow it.

- A **task-created** page was opened by this task and entered in its ledger.
  Navigate and close it as the authorized workflow requires.
- A **task-adopted** page predates the task but is current-agent controlled,
  unambiguously matches the requested workflow, and has no unsaved, scheduled,
  transient, or unrelated state. Use only that workflow. Do not navigate it
  away or close it unless the user authorized that lifecycle change or the
  page is proven disposable.
- A **user-owned, other-agent-owned, pre-existing ambiguous, or unknown** page
  is inventory only. Do not navigate, mutate, group, or close it. BrowserOS
  has no general claim or ownership-transfer operation.

Tab inventories may be flat and do not themselves establish ownership.
Derive dispatch provenance from task creation receipts, the task ledger, and
ownership fields actually returned by the current tool. Tool actionability is
not current-task authorization.

## Main loop

Use this loop for interaction:

```text
list/select -> snapshot -> act once -> inspect diff -> verify postcondition
```

- Use refs from a fresh `snapshot` instead of coordinate guesses.
- Treat every ref as stale after navigation or a substantial rerender.
- Keep ordinary page operations addressed to the verified page ID; they do
  not require selecting the tab or activating its window. Read the focus and
  background-behavior caveats in the operating details before relying on a
  site feature that may behave differently when its tab is not selected.
- Use `diff`, `grep`, or a bounded `read` for semantic state.
- Use `screenshot` only for visual proof and bound its size and frequency.
- Wait for a real text, selector, processing, or object-state condition. Do
  not open another page merely to poll.
- Match proof to the claim: a DOM read is not visual proof, and a screenshot
  alone is not durable-save proof.

## Lifecycle

Navigate the same task-created page for retries, redirects, polling, and
readback. If replacement is genuinely required, open and verify exactly one
replacement, then close the verified task-created old page.

Keep a task-local ledger containing:

```text
baseline pages/windows/groups
task-adopted pages and their allowed workflow
task-created pages/windows/groups, purpose, and lifecycle state
task-created local artifacts, exact returned path, purpose, and lifecycle state
task-created hidden surfaces: expected 0; observed and attributed exceptions
relevant baseline active page/window and window visibility
foreground takeovers, window visibility changes, and provable restoration
retained state and reason
unknown or orphan state
```

Relist immediately after any action that can spawn a popup, callback, preview,
or window, and relist once more before completion. Attribute new resources by
the action receipt plus sanitized semantic evidence; never assume every
baseline delta belongs to this task when the user or another agent may be
active. Record a possibly task-caused but unattributable resource as unknown or
orphan instead of omitting it from the ledger.

If an action unexpectedly causes a hidden page or window, do not continue
working through it. Attribute it using the action receipt and current identity
evidence. Expose the containing window without activation only when that
window is task-controlled and its current membership and profile context are
proved safe to reveal. If only the page is proved, close that page when safe
or retain and report it; never expose a whole window on page ownership alone.

Before closing a page, relist and match the creation receipt handles plus
sanitized semantic identity. If the match is not unique, leave it open and
report an orphan instead of guessing. Before closing a task-created window,
prove every current page inside it is task-created and intended to close. If
page membership cannot be proved, close only individually verified pages and
retain or report the window.

After the final inventory, reconcile unique resources rather than action
counts:

```text
pages created = closed + intentionally retained + unknown/orphan
windows created = closed + intentionally retained + unknown/orphan
groups created = removed + intentionally retained + unknown
artifacts created = removed + intentionally retained + unknown
```

Never mass-close pages that predated the task merely because they look old or
duplicated.

## Mutations and unknown outcomes

For any save, submit, send, publish, schedule, upload, purchase, delete, or
other external mutation:

1. Verify the exact target and precondition.
2. Issue one mutation.
3. Inspect the immediate change.
4. Verify the exact postcondition independently.

If the call times out, disconnects, or returns ambiguous transport state,
label the outcome **unknown**. Reconnect read-only and inspect the exact object
before any retry. Retry only after authoritative readback proves the first
mutation did not land and the application presents a terminal state, or its
processing indicator has cleared and authoritative state stays stable across
a bounded reread. An inherently idempotent, duplicate-safe operation is the
only exception. If neither condition is proved, leave the mutation unknown and
report it. If the original page is wedged and the correct profile can be
proved, use at most one separately ledgered read-only verifier page. Do not
reload or close the unknown page just to make cleanup appear complete.

## Recovery

Classify the boundary before changing the recovery rail: schema, stale ref,
page identity, site behavior, long page execution, or BrowserOS transport.
Correct an invalid call; resnapshot a stale ref; relist a stale page; and use
one small read-only inventory probe after a transport interruption.

After two failed attempts at the same operation, change diagnostic layer or
report the exact blocker. An unknown mutation is not a failed attempt and must
not be repeated merely to reach that threshold. Restart the shared BrowserOS
application only as the final recovery rung, with user authority, and after
coordination proves no other active user or agent work and no unresolved
in-flight mutation would be interrupted. If that cannot be proved, do not
restart. After a restart, rediscover all pages, windows, contexts, and refs.

## Parallel browser work

Parallelize browser work only across genuinely independent tasks and pages.
Each agent must select or create its own page, keep its own lifecycle ledger,
record any local artifacts it creates, and return its own cleanup
reconciliation. A parent-created page cannot be assigned to a child as an
ownership transfer. Never let two agents act or poll the same page concurrently.

Designate one focus owner for any phase that can activate a window,
foreground-create a tab, create a visible window directly or implicitly,
expose-and-activate a window, or close the selected page. Serialize those
foreground-capable calls. Other agents may continue independent background
page work, but they must not spend the shared focus budget. Focus ownership
does not transfer page ownership.

Resume the exact owning agent to clean up its retained page. If that agent
cannot be resumed, report an orphan for manual cleanup; do not send a fresh
agent or raw CDP around the ownership boundary.

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

## Reference map

- [references/operating-details.md](references/operating-details.md) — current
  compact tool roles; focus, visibility, hidden-surface, and manual-gate
  handling; identity and profile constraints; BrowserOS-managed connectors;
  state-change recovery; secrets; proof selection; and parallel ownership.
