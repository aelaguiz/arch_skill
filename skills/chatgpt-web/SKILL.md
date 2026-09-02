---
name: chatgpt-web
description: "Query logged-in ChatGPT through one BrowserOS ChatGPT tab in a deliberately chosen profile window (`Pro One` or `Work`, same projects in both) after applying the canonical $browseros contract and $prompt-authoring discipline. Use when the user explicitly wants the ChatGPT web provider/capability, optional attachments, a pushed PR reviewed through the ChatGPT GitHub connector, or an exact existing conversation continued. Always uses ChatGPT's Chat surface, never Work (Work tops out at Ultra; Ultra is not Pro); defaults to the newest model generation at maximum reasoning power (Pro / 5/5) with Extended thinking, places chats in the most applicable project, reuses a same-workstream Pro thread from the last 24-48 hours unless ~6+ turns deep, keeps a heartbeat during long Pro waits, runs serially, and fails over to the other profile window when Pro is rate limited. No substitute for Pro: when both windows are rate limited it stops and waits for the user. Not for OpenAI API work, automated login, or scripts."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

Use this skill when the user wants a head start querying ChatGPT through the
already logged-in BrowserOS browser session.

This is a prose-only helper skill. It uses BrowserOS MCP directly. It ships no
scripts, runners, controllers, harnesses, schemas, or automation infrastructure.

Read and apply `../browseros/SKILL.md` before the first BrowserOS call. The
canonical BrowserOS skill owns page provenance, window and profile identity,
lifecycle, proof, recovery, secrets, and cleanup; this skill owns the
ChatGPT-specific workflow, including which of the two ChatGPT profile windows
(`Pro One` or `Work`) a run uses and what to do when Pro is rate limited.

Read `../_shared/agent-orchestration-policy.md` before the query. ChatGPT Web is
an intentional provider/browser-capability lane rather than a generic local
child-agent route. Starting a new conversation and continuing an exact existing
conversation are different context choices; never inherit whatever conversation
happens to be open without deciding which one the user wants.

## Use When

- The user asks to ask ChatGPT, consult ChatGPT, get ChatGPT's opinion, or run a
  prompt through the ChatGPT web UI.
- The user wants BrowserOS MCP to drive logged-in ChatGPT instead of using the
  OpenAI API.
- The user wants local attachments included in a ChatGPT web prompt.
- The user wants ChatGPT Pro to review code that lives on a pushed branch or PR
  through the ChatGPT GitHub connector.
- The user has a rough prompt and wants it shaped before sending.

## Do Not Use When

- The user wants OpenAI API usage or product/API guidance.
- The user wants generic web automation unrelated to ChatGPT.
- BrowserOS MCP is unavailable in the current host.
- ChatGPT is not already logged in in BrowserOS.
- The task would require automated login.
- The user requests more than 10 attachments.

## Non-Negotiables

- Read and apply `../browseros/SKILL.md` before the first direct BrowserOS MCP
  call and obey it throughout this workflow; a name-drop of the skill without
  reading it does not count.
- Use BrowserOS MCP, not `web.run`, OpenAI API calls, shell browser scripts, or
  direct cookie/session handling.
- BrowserOS runs two profile windows for ChatGPT: `Pro One` and `Work`. Each
  is its own ChatGPT login, and both have the same projects set up. Be
  careful which window you are in. Choose one window deliberately for the
  run, prove it under `$browseros` (the page's window or browser-context
  evidence plus a safe in-app account or workspace marker, never an email,
  token, or session payload), and name it in the receipt. If you cannot
  prove which profile a page belongs to, stop and ask instead of guessing.
- Use one BrowserOS `https://chatgpt.com/` tab in the chosen window for the
  whole run. Reuse an eligible current-agent-controlled ChatGPT page in that
  window when one can be safely task-adopted under `$browseros`; otherwise
  open exactly one ChatGPT page as a tab in that window, landing and
  verifying it the way `$browseros` prescribes.
- Never create a new BrowserOS window. The two profile windows already exist;
  a run works inside one of them. Do not open pages hoping one lands in the
  right profile.
- Reusing the page does not mean reusing its conversation. Do login check,
  conversation selection, mode selection, attachment upload, submission,
  waiting, and response reading in that same page.
- Do not open extra ChatGPT tabs for polling, attachment handling, retries,
  separate prompts, or readback. The only second page a run may open is the
  one in the other profile window during a rate-limit failover, and the run
  then continues in that page alone.
- Run ChatGPT Web prompts serially. If the user gives multiple ChatGPT asks,
  process them one at a time in the same ChatGPT tab. Keep them in one
  conversation only when they are explicit follow-ups; otherwise start a new
  clean conversation in that tab for each independent ask. If the user asks for
  parallel ChatGPT Web runs, explain that this skill runs serially to avoid web
  session rate limits, then proceed sequentially. If simultaneous ChatGPT Web
  runs are mandatory, fail loudly instead of opening parallel tabs.
- Read and apply `../prompt-authoring/SKILL.md` to the actual populated prompt
  before every submission; a name-drop of the skill without reading it does not
  count. Preserve the user's intent and any explicitly requested verbatim
  relay; otherwise remove hidden caller assumptions, leading success criteria,
  and closed evidence paths before sending.
- Do not over-prompt Pro. Pro is a frontier model, not a junior worker: send
  the ask, the essential context it cannot infer, and the desired output shape,
  then stop. Do not stack roles, personas, invented rubrics, step-by-step
  methodologies, output schemas, repeated constraints, motivational framing, or
  restated context the thread already has. When in doubt, cut; a short faithful
  prompt beats an engineered one.
- Always work in ChatGPT's `Chat` surface, never `Work`. The composer's
  `Select chat surface` radio decides which picker you get; Pro exists only
  in `Chat`. `Work` tops out at `Ultra`, and `Ultra` is not Pro. Check the
  radio before touching the model pill and again before every send. A
  prompt sent from `Work` was not a Pro run: redo it in `Chat`.
- Default to the absolute latest, absolute most powerful configuration the
  `Chat` picker offers: the newest model generation, at its maximum
  reasoning power (`Pro`, `5/5`, or whatever the UI calls the top), with
  `Extended` thinking when effort is a separate control. Model names written
  in this skill are examples that go stale, never requirements: enumerate
  the live Chat picker fresh and let it win over any remembered name. Only
  deviate when the user explicitly names a different model or mode.
- Respect explicit user choices for `Instant`, `Thinking`, `Pro`, `Light`,
  `Standard`, `Extended`, or `Heavy`.
- Do not downgrade or upgrade the requested mode silently.
- Never automate login. If ChatGPT is not logged in, fail loudly and tell the
  user to log in manually in BrowserOS.
- Treat `Pro`, especially `Extended` or `Heavy`, as a long-running mode. A
  response can take 10+ minutes. Wait patiently in the same tab until generation
  finishes before reading or submitting anything else.
- Actually read everything Pro emits - interim messages, the visible thinking
  or reasoning summary, and the final response - during heartbeat check-ins
  and at the end, and act on what it says. Errors often surface first in the
  thinking trace or an interim message, such as Pro noting it cannot open a
  file or reach a repo, long before the final text. A completed generation is
  not automatically a success: if Pro says it cannot see an attachment, repo,
  PR, or connector, if it improvised around a missing input, if
  it answers a different question than the one submitted, if it reports an
  error, refuses, or returns something empty or degenerate, treat that as a
  failed run. Fix the input and resubmit in the same tab; never relay a broken
  response as the answer or report success without having read the text.
- Submit any plan, and any other multi-paragraph body, as an attached file,
  never typed or pasted into the composer. Newlines in the composer can send
  early and split the message, so the composer gets only a short single-
  paragraph ask that points at the attached file. After sending, read back the
  submitted user message and confirm the full body arrived.
- A response built on an input Pro never actually received is invalid even
  when it reads as polished and confident. If Pro did not get something it was
  supposed to get and worked around it - "I don't have the file, so I'll
  assume...", reviewing a plan from its description instead of the attachment,
  imagining repo contents it could not open - discard the response, fix the
  delivery of the missing input, and resubmit. Never relay or build on an
  answer Pro invented around a missing input.
- Dismiss transient blocker popups immediately. They are UI noise, not part
  of the response; closing one never counts as altering the run. If a
  submission does not go through for a transient reason, wait about 5
  minutes, dismiss any blocker, and resubmit the same prompt in the same tab.
- A Pro rate limit is not transient. `You've hit your rate limit. Please try
  again later`, or an equivalent usage-cap message, means that window's
  account is capped for Pro. Do not sit and retry it, and do not substitute:
  never drop to `Extra High (4/5)`, `Thinking`, a lower effort, an older
  generation, or the API to keep moving. Switch to the other profile window
  and continue there per the profile-window section below. If both `Pro One`
  and `Work` are rate limited, stop the Pro-dependent work: report the rate
  limit, clear or pause any goal that depends on Pro, and wait for the user
  to say Pro is available again.
- Do not print, save, summarize, or inspect account details, cookies, tokens,
  raw session payloads, or other secrets.
- Enforce a maximum of 10 attachments. Do not silently drop files.
- Keep the result simple: ChatGPT's answer plus a short receipt.
- Place every conversation in the most applicable ChatGPT project. A root chat
  outside any project has no project context, so its review is useless; use a
  root chat only when no existing project plausibly fits, and say so in the
  receipt.
- Before starting a new conversation for continuing work, check whether the
  workstream already has a live Pro thread: look in the most applicable project
  for a Pro thread from the last 24-48 hours on this same work and continue it
  instead of starting fresh. If that thread is already about 6 or more
  prompt/response turns deep, start a new conversation in the same project
  instead of overloading it. An explicit user choice of an exact thread or a
  new chat always wins over this default.
- Continue an exact conversation the user names only when the intended
  conversation can be identified. If it cannot, stop and ask for the missing
  conversation choice rather than sending into an unrelated history.
- While a `Pro` response is generating, keep a periodic check-in heartbeat,
  defaulting to about every 5 minutes, using the host's heartbeat capability
  when one exists, so the run never wedges silently during a long wait. Clear
  the heartbeat as soon as the response is read or the run terminally fails;
  never leave a stale heartbeat running.
- Whenever the ask touches our repositories at all, tag `@GitHub` in the
  composer so ChatGPT can see the repos through the ChatGPT GitHub connector.
  To show code, do not paste large diffs. Commit and push the work to its PR
  branch, then tag `@GitHub` and paste the PR URL so Pro reviews the actual
  branch through the connector. Never automate connecting or authorizing the
  connector; if it is not connected, fail loudly and tell the user to connect
  it manually.

## First Move

1. Resolve the user's desired ChatGPT ask and any explicit mode, effort, model,
   or attachment requests.
2. Read `../prompt-authoring/SKILL.md` and apply it to the populated prompt
   before touching ChatGPT. Keep it faithful to the user's intent, preserve an
   explicitly requested verbatim relay, and make caller hypotheses
   challengeable rather than task truth. Keep the prompt lean per the
   over-prompting rule above: cut scaffolding instead of adding it.
3. Resolve conversation placement: identify the most applicable ChatGPT
   project, then resolve
   `conversation = continue-exact | continue-recent-pro | new-in-project |
   new-root`. `continue-exact` requires an explicit user request and an
   identifiable target. `continue-recent-pro` applies when the ask continues a
   workstream with a Pro thread from the last 24-48 hours in that project and
   the thread is under about 6 turns. Otherwise use `new-in-project`, or
   `new-root` only when no project fits.
4. Choose the profile window, `Pro One` or `Work`. An explicit user choice
   wins. Otherwise prefer the window whose account already holds this
   workstream's live Pro thread; with no live thread, either window is fine.
   A window known to be rate limited for Pro is not a choice.
5. Under `$browseros`, select the single current-agent-controlled ChatGPT page
   for the run inside that window: safely task-adopt an eligible
   `https://chatgpt.com/` page there, or open exactly one new page as a tab
   in that window. Prove the page is in the chosen window before using it.
   Never create a new window.
6. Verify that page is logged in before doing anything else.
7. In that page, open the resolved conversation: a new chat inside the chosen
   project, the recent Pro thread, or the exact requested conversation. Verify
   the thread before submitting into it. Do not submit while the page is merely
   showing an arbitrary prior thread.
8. Set the surface radio to `Chat` and confirm the model pill reads `Pro`
   before composing. Never send from `Work`.

## Profile Windows And Rate Limits

Two BrowserOS profile windows exist for ChatGPT, `Pro One` and `Work`. They
are separate ChatGPT logins with the same projects set up, so either can host
any run, but conversations do not carry across them: a thread that lives in
`Work` cannot be continued from `Pro One`. Rate limits are per account, so
the two windows are each other's fallback. Under `$browseros`, list windows
and tabs before choosing, prove which profile the selected page is in, and
work only in that page.

When a Pro submission in the current window is refused with `You've hit your
rate limit. Please try again later` or an equivalent usage-cap message:

1. Record that window as rate limited for this run.
2. Switch to the other profile window: select or open one ChatGPT page there
   under `$browseros`, prove the profile, and verify login.
3. Open the same-named project in that window and start a new conversation.
   Restate the goal context the original thread had, and re-attach the files
   or re-tag `@GitHub` with the PR URL; the new account has none of that.
4. Submit the same prompt and continue the run there. Close the
   rate-limited page if this run created it, per `$browseros` cleanup, and
   name the failover and both windows in the receipt.

If the other window is also rate limited, the run cannot get Pro right now.
There is no substitute for Pro: do not use `Extra High (4/5)`, `Thinking`, a
lower effort, an older generation, another provider, or the API in its place.
Stop the Pro-dependent work, report the rate limit and both windows, clear or
pause any goal that depends on Pro, and wait for the user to say Pro is
available again. Do not poll for the limit to lift on your own.

## Login Check

From the ChatGPT page, use BrowserOS MCP page JavaScript to fetch:

```javascript
fetch('/api/auth/session', { credentials: 'include' })
```

Use only the safe boolean result: whether the parsed JSON has a `user` value.
Do not display or store the returned user, account, token, cookie, or session
fields.

If the session does not prove a logged-in user, stop with:

```text
BrowserOS is not logged in to ChatGPT. Open https://chatgpt.com/ in BrowserOS,
log in manually, then rerun $chatgpt-web.
```

If the endpoint cannot be checked, fail loudly. Do not infer login from visible
page controls.

## Projects And Conversation Selection

Root chats without a project have none of the project's files, instructions, or
prior threads, so a review sent there is context-free and useless. Pick where
the conversation lives before composing anything:

1. Read the project list in the ChatGPT sidebar and judge which project
   actually matches the current ask: same repo, product, or workstream.
2. If the ask continues work that recently went through Pro, open that
   project's thread list and look for a Pro thread from the last 24-48 hours on
   this same work. Open the candidate and skim enough of it to confirm it is
   the same workstream, not just a similar title. Threads are per account:
   if the live thread is in the other profile window, that window is the one
   to use unless it is rate limited.
3. Continue that thread when it matches, is a `Chat`-surface thread (not
   labeled `Work` in the sidebar), and is under about 6 prompt/response
   turns. Around 6 or more turns, treat it as saturated and start a new
   conversation in the same project instead.
4. With no matching recent thread, start a new conversation inside the chosen
   project.
5. Use a root chat only when no existing project plausibly fits the ask, and
   note that choice in the receipt.

An explicit user request for a specific thread, a specific project, or a fresh
chat overrides all of the defaults above.

## Repo Visibility Via GitHub

Tag `@GitHub` in the composer for any repo-grounded ask - code review, design
or architecture questions about our code, or anything where ChatGPT should see
the actual repository - so the connector gives it direct repo visibility
instead of relying on pasted fragments.

When the material to review is code, do not paste diffs or file dumps into the
composer:

1. Make sure the work is committed and pushed to its PR branch, and have the
   exact PR URL.
2. In the composer, @mention GitHub to invoke the ChatGPT GitHub connector and
   paste the PR URL, then ask for the review of that PR on its branch.
3. Confirm the GitHub mention is attached before sending. If the connector is
   not connected or cannot see the repo, fail loudly and tell the user to
   connect it manually in ChatGPT settings; never automate connector
   authorization.

## Chat Surface: Chat, Never Work

The ChatGPT composer has a `Select chat surface` radio group with two
surfaces, `Chat` and `Work`. Pro exists only in `Chat`. The `Work` surface
has its own picker - a six-level power slider (`Max`, `Ultra`) over `5.6 Sol`,
`5.6 Terra`, `5.6 Luna`, and `5.5`, plus a fast mode - and nothing in it is
Pro. `Ultra` is Work's ceiling, not Pro. `Sol Ultra` is not Pro. A run that
sends from `Work` did not get Pro no matter how high its slider sat, and its
verdict does not count: redo it in `Chat`.

Before touching the model pill, and again before every send:

1. Read the surface radio group and make sure `Chat` is the checked radio.
   If `Work` is checked, select `Chat` and re-read the composer; the pill
   changes with the surface.
2. Confirm the model pill reads `Pro` and its picker says `Pro, 5 of 5` (or
   whatever the Chat picker calls its top level). A pill reading `5.6 Sol
   Max`, `Ultra`, or a power slider with six levels means you are in `Work`;
   go back to step 1.
3. When continuing a thread, confirm it is a Chat-surface thread. The
   sidebar labels Work-surface chats with `Work`; a Work thread cannot carry
   a Pro conversation, so start a new `Chat` conversation in the project
   instead.

Naming trap: the BrowserOS profile window called `Work` has nothing to do
with ChatGPT's `Work` surface. In either profile window, `Pro One` or
`Work`, the ChatGPT surface is `Chat`.

## Mode And Effort

Default when the user does not specify:

```text
surface = Chat (never Work)
mode = maximum reasoning power the Chat picker offers (`Pro` / `5/5`)
effort = Extended
model = newest generation in the Chat picker, at its most powerful tier
```

Use the ChatGPT model pill beside the composer, in the `Chat` surface.
Prefer `Configure...` when available because it exposes the `Intelligence`
dialog with explicit model options and thinking effort.

Observed controls to select from:

- surface: `Chat`, `Work` - always `Chat`
- mode: `Instant`, `Thinking`, `Pro`
- effort: `Light`, `Standard`, `Extended`, `Heavy`
- model: the newest generation the Chat picker offers, configured to its
  most powerful tier, unless the user explicitly names another model

`Pro` is shorthand for the maximum reasoning option on the newest model in
the `Chat` surface - shown as `Pro` or `5/5` when the UI renders levels as
a scale - not a frozen label. The ban runs one direction only: never
select less power than the maximum available in `Chat`, and never select
an older generation because its label matches a remembered name. `Extra
High (4/5)` instead of the top level is a downgrade; so is an older model
labeled `Pro` chosen over a newer generation whose own top tier carries a
different name (an agent once stuck with `GPT-5.5 Pro` and ignored the
newer Sol generation's top tier because doctrine said Sol was not Pro -
that is exactly wrong). The rule is scoped to the Chat surface: the top of
the `Work` picker (`Ultra`) is not "maximum power" for this purpose, and
selecting it is the same failure as a downgrade (an agent once ran a
review as `5.6 Sol Ultra` in `Work` and called it max power - that review
had to be redone in `Chat` on Pro). The picker changes between sessions:
in `Chat`, re-open the model pill and the `Intelligence` dialog, enumerate
every model and every power level - including tiers nested inside a newer
entry - and select the newest generation at its top power before
concluding anything is missing. If you genuinely cannot reach a
maximum-power configuration in `Chat`, fail loudly and tell the user
instead of silently approximating. Before sending, confirm the surface is
`Chat` and the picker displays the selection you resolved, not a stand-in.

Do not run a Pro prompt merely to test the skill. Only use Pro when the user's
actual request needs the default or explicitly asks for it.

Because the default is `Pro` with `Extended` thinking, the default path also
requires patient waiting. Do not treat a long silent period as failure by itself.

## Attachments

When the material to send is a plan or any multi-paragraph body, write it to a
file (a temp file is fine) and attach it through the upload path below instead
of typing it into the composer. The composer then carries only a short
single-paragraph ask that references the attached file by name.

Preflight attachments before browser interaction:

- every path must be absolute
- every path must exist
- count must be 10 or fewer

Use the BrowserOS file-upload path that works with ChatGPT in the selected
ChatGPT page:

1. Create a temporary visible file input in the page for BrowserOS MCP to use.
2. Snapshot the temporary input and use the live BrowserOS MCP `upload` tool
   with its exact ref and the user's absolute paths.
3. Transfer the selected `File` objects into ChatGPT's hidden `#upload-files`
   input.
4. Dispatch `input` and `change` events on the ChatGPT input.
5. Confirm visible attachment chips by filename.
6. Remove the temporary visible input.

If any requested filename does not appear as an attachment chip, stop before
submitting.

## Submission

1. Verify the resolved conversation placement one final time. For
   `new-in-project` the page must be a new chat inside the chosen project; for
   `continue-recent-pro` or `continue-exact` the visible thread must be the
   resolved thread; for `new-root` the page must be a new root chat.
2. Fill the ChatGPT composer with the final prompt. If the ask includes a plan
   or any multi-paragraph body, that body must already be an attached file and
   the composer text must be a short single-paragraph ask referencing it.
3. Confirm the surface radio is `Chat` and the selected mode and effort
   match the request or default. A pill reading `5.6 Sol Max` or `Ultra`
   means `Work`: switch to `Chat` and reselect before sending.
4. Confirm every attachment chip is present.
5. Click `Send prompt`, then read back the just-submitted user message and
   confirm it contains the full intended text and attachments. If it was
   truncated or split, stop the resulting generation and resubmit correctly.
6. Wait in the same tab until generation finishes. For `Pro`, `Extended`, or
   `Heavy`, 10+ minutes can be normal; poll slowly and let ChatGPT finish. For
   a `Pro` run, set the check-in heartbeat (default about every 5 minutes)
   before settling into the long wait so the run cannot wedge silently. At
   each check-in, read what is actually on the page - the visible thinking or
   reasoning summary, interim assistant messages, partial response text, error
   banners, connector failures - not just whether a spinner exists. If the
   thinking trace or an interim message already shows the run going wrong,
   such as a missing attachment or an unreachable repo, act on it then rather
   than waiting out the full generation.
7. Do not refresh, resubmit, open another tab, or start another ChatGPT prompt
   while a response is still generating. Dismissing a transient blocker
   dialog is always allowed. If the submission did not go through for a
   transient reason, wait about 5 minutes and resubmit the same prompt in the
   same tab. If it was refused with the rate-limit message, follow the
   profile-window failover instead of retrying here.
8. Treat failure as concrete, not time-based: visible ChatGPT error, lost
   login/session, required manual user action, missing attachment before send,
   or a clearly inactive page with no generation indicator and no response
   progress after a patient wait.
9. Read the latest assistant response from the page in full, plus its visible
   thinking or reasoning summary and any interim messages, and check them
   against the submitted ask. Error signals anywhere in that output count as
   failures even though generation completed: Pro saying it cannot access or
   see the attachment, repo, PR, or connector; Pro improvising around a
   missing input by assuming, imagining, or working from a description of an
   artifact it never opened; Pro answering a different or partial question; a
   refusal; an empty or degenerate reply. On any of these, diagnose the input,
   repair it, and resubmit in the same tab instead of relaying the broken
   response - a polished answer built on an input Pro never received is still
   invalid.
10. Clear the check-in heartbeat as soon as the response is read or the run
    terminally fails. Do not leave it running past the run.

## Output

Return:

- ChatGPT's answer
- surface (`Chat`), model, mode, and effort used
- profile window used, `Pro One` or `Work`, plus any rate-limit failover
  between them
- conversation placement used: the project name plus `continue-exact`,
  `continue-recent-pro`, `new-in-project`, or `new-root` with a one-line reason
  when the choice was `new-root`
- attachment filenames, if any, and the PR URL when the GitHub connector was
  used
- a short note if the prompt was shaped before submission
- a short note when the run waited for a long Pro response, including that the
  heartbeat was set and cleared

If the run fails, name the exact failed condition and the next manual repair.
When both profile windows are rate limited, say so plainly, name the goal or
work that is paused on Pro, and wait for the user to say Pro is back.
