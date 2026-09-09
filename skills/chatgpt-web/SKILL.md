---
name: chatgpt-web
description: "Query logged-in ChatGPT through BrowserOS after reading and applying $browseros and $prompt-authoring. Use for an explicit ChatGPT web consultation, attachments, a pushed PR review through the GitHub connector, or an exact conversation continuation. Defaults to GPT-6 Astra with the literal Pro option and Extended thinking in Chat, never Extra High, xhigh, Ultra, Thinking, or another substitute. Uses one tab at a time, the applicable project, deliberate thread selection, serial prompts, and a heartbeat during long waits. If Pro is missing or rate limited, try the next configured BrowserOS account: Work, Pro1 / Pro One, Pro2, Pro3, and others; all should have the same projects. Pause only the blocked Pro consultation after available accounts are exhausted; continue independent authorized work. Not for OpenAI API work, generic browser automation, automated login, or scripts."
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
ChatGPT-specific workflow, including selection among `Work`, `Pro1` / `Pro One`,
`Pro2`, `Pro3`, and other configured ChatGPT profiles when Pro is unavailable.

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
- BrowserOS has separate ChatGPT accounts in profiles such as `Work`, `Pro1`
  (also called `Pro One`), `Pro2`, and `Pro3`; check other configured Pro
  profiles too. All should have the same projects set up. Be
  careful which window you are in. Choose one window deliberately for the
  run, prove it under `$browseros` (the page's window or browser-context
  evidence plus a safe in-app account or workspace marker, never an email,
  token, or session payload), and name it in the receipt. If you cannot
  prove which profile a page belongs to, stop and ask instead of guessing.
- Use one BrowserOS `https://chatgpt.com/` tab at a time in the chosen window.
  Reuse an eligible current-agent-controlled ChatGPT page in that
  window when one can be safely task-adopted under `$browseros`; otherwise
  open exactly one ChatGPT page as a tab in that window, landing and
  verifying it the way `$browseros` prescribes.
- Never create a new BrowserOS window. Use existing profile windows under
  `$browseros`. Do not open pages hoping one lands in the
  right profile.
- Reusing the page does not mean reusing its conversation. Do login check,
  conversation selection, mode selection, attachment upload, submission,
  waiting, and response reading in that same page.
- Do not open extra ChatGPT tabs for polling, attachment handling, retries,
  separate prompts, or readback. During account failover, select or open one
  eligible page in the next profile and continue there alone; clean up any
  page this run created in the previous profile under `$browseros`.
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
- Default to **GPT-6 Astra Pro** in the `Chat` picker: select GPT-6 Astra and
  the literal **`Pro`** option, with `Extended` thinking when that is a
  separate control. **Pro is not Extra High, xhigh, Ultra, Thinking, or
  whatever happens to be the highest available setting.** A `5/5` indicator
  alone does not establish Pro; verify the actual `Pro` selection. If Pro is
  missing, try the next account instead of selecting a substitute. Only
  deviate when the user explicitly requests a different model or mode.
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
- A missing or disabled literal `Pro` option in the verified `Chat` picker
  probably means that account is temporarily rate limited. An explicit
  usage-cap message confirms a limit. In either case, switch to the next
  configured account under `$browseros`; check `Work`, `Pro1` / `Pro One`,
  `Pro2`, `Pro3`, and any others before declaring Pro unavailable. Do not
  retry the capped account or substitute `Extra High`, `xhigh`, `Ultra`,
  `Thinking`, another model, or the API. If no available account offers Pro,
  report the accounts checked and pause the blocked Pro consultation or
  decision. Continue independent authorized work; pause the whole run only
  when no useful independent work remains. Wait for the user to say Pro is
  available again; never count a pending review as passed.
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
4. Choose among the configured ChatGPT profile windows (`Work`, `Pro1` /
   `Pro One`, `Pro2`, `Pro3`, and others). Start with an explicitly requested
   profile. Otherwise prefer the window whose account already holds this
   workstream's live Pro thread; with no live thread, use an available account.
   If its Pro option is missing or capped, follow account failover below.
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
8. Set the surface radio to `Chat` and verify the requested model and mode,
   defaulting to GPT-6 Astra with literal `Pro`. If required Pro is missing or
   disabled, switch to the next account below. Never send a Pro request from
   `Work` or substitute Extra High.

## Profile Windows And Rate Limits

Read and apply `$browseros`, including its profile/account operating details,
before inspecting or switching accounts. Discover the configured profiles and
their existing windows: `Work`, `Pro1` (also called `Pro One`), `Pro2`, `Pro3`,
and any additional Pro accounts. Use live profile identity rather than assuming
these labels exactly match every machine. All accounts should have the same
projects; verify the same-named project after switching. Conversations are per
account, so carry the needed thread context into the destination conversation.

In ChatGPT's `Chat` surface, inspect GPT-6 Astra's model and reasoning controls,
including `Configure...` / `Intelligence` when present. If the literal `Pro`
option is absent or disabled, treat it as a probable temporary account rate
limit. Do not redefine Pro as the highest remaining option. `Extra High` is
still not Pro even if it is now the top setting. An explicit usage-cap message,
including `You've hit your rate limit. Please try again later`, triggers the
same account switch:

1. Note the profile and observed condition: Pro missing/disabled or an explicit
   rate-limit message. The missing option alone is a probable limit, not proof.
2. Try the next configured account not yet checked. Under `$browseros`, select
   or open one eligible ChatGPT page in its existing window, prove its profile,
   and verify login. Keep all interaction backgrounded.
3. Set the surface to `Chat` and verify GPT-6 Astra's literal `Pro` option.
   If unavailable there too, continue through the remaining accounts, including
   `Pro2`, `Pro3`, and any additional configured Pro profiles.
4. When Pro is available, open the same-named project and start a conversation
   with the necessary goal, decisions, and prior thread context. Re-attach files
   or re-tag `@GitHub` with the PR URL, verify `Pro` and the requested thinking
   effort, and submit the same ask. Continue in that page alone.
5. Clean up pages this run created and no longer needs under `$browseros`.
   Record the profiles checked, the successful profile, and continuation thread.

Only after checking the available accounts should the run report that Pro
cannot be used right now. Name the profiles and observed conditions, pause the
blocked Pro consultation or decision, and continue independent authorized work.
Pause the whole run only when no useful independent work remains. Wait for the
user to say Pro is available again; do not poll capped accounts or count a
pending review as passed. There is no substitute for GPT-6 Astra Pro: never
Extra High, xhigh, Ultra, Thinking, another model, provider, reviewer, or API.

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
   if the live thread is in another profile window, that window is the one
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
surfaces, `Chat` and `Work`. Select GPT-6 Astra Pro in `Chat`. Work's model picker
and reasoning slider do not select Chat's Pro mode. A review sent from
`Work` does not count as a Pro verdict; redo it in `Chat`.

Before touching the model pill, and again before every send:

1. Read the surface radio group and make sure `Chat` is the checked radio.
   If `Work` is checked, select `Chat` and re-read the composer; the pill
   changes with the surface.
2. For a Pro run, confirm GPT-6 Astra and the literal `Pro` option are selected, with
   `Extended` thinking where offered. Extra High, xhigh, Ultra, or a numeric
   power level alone do not establish Pro. If Pro is unavailable, switch
   accounts under the profile-window section before sending.
3. When continuing a thread, confirm it is a Chat-surface thread. The
   sidebar labels Work-surface chats with `Work`; a Work thread cannot carry
   a Pro conversation, so start a new `Chat` conversation in the project
   instead.

Naming trap: the BrowserOS profile window called `Work` has nothing to do
with ChatGPT's `Work` surface. In every BrowserOS profile, including `Work`,
the ChatGPT surface is `Chat`.

## Mode And Effort

Default when the user does not specify:

```text
surface = Chat (never Work)
mode = literal Pro option (never Extra High, xhigh, Ultra, or Thinking)
effort = Extended
model = GPT-6 Astra Pro
```

Use the ChatGPT model pill beside the composer, in the `Chat` surface.
Prefer `Configure...` when available because it exposes the `Intelligence`
dialog with explicit model options and thinking effort.

Observed controls to select from:

- surface: `Chat`, `Work` - always `Chat`
- mode: `Instant`, `Thinking`, `Pro`
- effort: `Light`, `Standard`, `Extended`, `Heavy`
- model: GPT-6 Astra, with the literal `Pro` option verified in the live Chat
  picker unless the user explicitly requests another model or mode

**Pro means the literal `Pro` option on GPT-6 Astra.** It is not shorthand for
maximum available reasoning. `Extra High` / `xhigh`, `Ultra`, `Thinking`, and
every other non-Pro setting are different configurations and cannot satisfy a
Pro request or required review. `Extended` is a separate thinking choice when
offered; it does not turn a non-Pro selection into Pro. Neither a numeric
`5/5` indicator nor a BrowserOS profile named `Pro` proves the selected mode.

Re-open the live `Chat` picker and inspect the model's nested controls before
concluding Pro is missing. If GPT-6 Astra's literal `Pro` option is absent or
disabled, follow account failover; this is probably a temporary rate limit on
that account. Do not select the highest remaining setting. Before every Pro
send, confirm `Chat`, GPT-6 Astra, `Pro`, and the requested thinking effort.

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
   match the request or default, GPT-6 Astra with literal `Pro` and Extended
   thinking. If required Pro is missing or disabled, switch accounts before
   sending. If the checked surface is `Work`, switch to `Chat` and reselect.
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
- verified profile window used and any account failovers, with the profiles
  checked and whether Pro was missing/disabled or explicitly rate limited
- conversation placement used: the project name plus `continue-exact`,
  `continue-recent-pro`, `new-in-project`, or `new-root` with a one-line reason
  when the choice was `new-root`
- attachment filenames, if any, and the PR URL when the GitHub connector was
  used
- a short note if the prompt was shaped before submission
- a short note when the run waited for a long Pro response, including that the
  heartbeat was set and cleared

If the run fails, name the exact failed condition and the next manual repair.
When no available profile offers Pro after checking the configured accounts,
say so plainly with the observed conditions, name the Pro
consultation or decision that is paused and any independent work continuing,
and wait for the user to say Pro is back.
