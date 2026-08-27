---
name: chatgpt-web
description: "Query logged-in ChatGPT through one BrowserOS ChatGPT tab after applying the canonical $browseros operating contract and shaping the prompt with $prompt-authoring discipline. Use when the user explicitly wants the ChatGPT web provider/capability, optional attachments, a pushed PR reviewed through the ChatGPT GitHub connector, or an exact existing conversation continued. Defaults to Pro with Extended thinking on the latest GPT Pro model (currently GPT-5.6 Pro), places chats in the most applicable ChatGPT project rather than context-free root chats, reuses a same-workstream Pro thread from the last 24-48 hours unless it is already ~6+ turns deep, keeps a cleared-on-response heartbeat during long Pro waits, runs serially, and waits patiently. Not for OpenAI API work, generic browser automation, automated login, scripts, runners, or hidden harnesses."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

Use this skill when the user wants a head start querying ChatGPT through the
already logged-in BrowserOS browser session.

This is a prose-only helper skill. It uses BrowserOS MCP directly. It ships no
scripts, runners, controllers, harnesses, schemas, or automation infrastructure.

Read and apply `../browseros/SKILL.md` before the first BrowserOS call. The
canonical BrowserOS skill owns page provenance, lifecycle, proof, recovery,
secrets, and cleanup; this skill owns the ChatGPT-specific workflow.

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
- Use one BrowserOS `https://chatgpt.com/` tab for the whole run. Reuse an
  eligible current-agent-controlled ChatGPT page when one can be safely
  task-adopted under `$browseros`; otherwise open exactly one ChatGPT page.
- Never open a new BrowserOS window when a BrowserOS window is already open.
  Open the ChatGPT page as a new tab in the existing window; a new window is
  allowed only when BrowserOS has no window at all.
- Reusing the page does not mean reusing its conversation. Do login check,
  conversation selection, mode selection, attachment upload, submission,
  waiting, and response reading in that same page.
- Do not open extra ChatGPT tabs for polling, attachment handling, retries,
  separate prompts, or readback.
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
- Default to ChatGPT `Pro` with `Extended` thinking when the user does not name
  a mode or effort. Default the model to the latest GPT Pro model, currently
  `GPT-5.6 Pro`; if that exact name is missing from the picker, choose the
  newest GPT Pro entry instead. Only deviate when the user explicitly names a
  different model.
- Respect explicit user choices for `Instant`, `Thinking`, `Pro`, `Light`,
  `Standard`, `Extended`, or `Heavy`.
- Do not downgrade or upgrade the requested mode silently.
- Never automate login. If ChatGPT is not logged in, fail loudly and tell the
  user to log in manually in BrowserOS.
- Treat `Pro`, especially `Extended` or `Heavy`, as a long-running mode. A
  response can take 10+ minutes. Wait patiently in the same tab until generation
  finishes before reading or submitting anything else.
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
4. Under `$browseros`, select the single current-agent-controlled ChatGPT page
   for the run: safely task-adopt an eligible `https://chatgpt.com/` page, or
   open exactly one new page as a tab in the already-open BrowserOS window.
   Never create a new window when one exists.
5. Verify that page is logged in before doing anything else.
6. In that page, open the resolved conversation: a new chat inside the chosen
   project, the recent Pro thread, or the exact requested conversation. Verify
   the thread before submitting into it. Do not submit while the page is merely
   showing an arbitrary prior thread.

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
   the same workstream, not just a similar title.
3. Continue that thread when it matches and is under about 6 prompt/response
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

## Mode And Effort

Default when the user does not specify:

```text
mode = Pro
effort = Extended
model = latest GPT Pro model (currently GPT-5.6 Pro)
```

Use the ChatGPT model pill beside the composer. Prefer `Configure...` when
available because it exposes the `Intelligence` dialog with explicit model
options and thinking effort.

Observed controls to select from:

- mode: `Instant`, `Thinking`, `Pro`
- effort: `Light`, `Standard`, `Extended`, `Heavy`
- model: select `GPT-5.6 Pro`, or the newest GPT Pro entry when that exact
  name is missing, unless the user explicitly names another model

Do not run a Pro prompt merely to test the skill. Only use Pro when the user's
actual request needs the default or explicitly asks for it.

Because the default is `Pro` with `Extended` thinking, the default path also
requires patient waiting. Do not treat a long silent period as failure by itself.

## Attachments

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
2. Fill the ChatGPT composer with the final prompt.
3. Confirm the selected mode and effort match the request or default.
4. Confirm every attachment chip is present.
5. Click `Send prompt`.
6. Wait in the same tab until generation finishes. For `Pro`, `Extended`, or
   `Heavy`, 10+ minutes can be normal; poll slowly and let ChatGPT finish. For
   a `Pro` run, set the check-in heartbeat (default about every 5 minutes)
   before settling into the long wait so the run cannot wedge silently.
7. Do not refresh, resubmit, open another tab, or start another ChatGPT prompt
   while a response is still generating.
8. Treat failure as concrete, not time-based: visible ChatGPT error, lost
   login/session, required manual user action, missing attachment before send,
   or a clearly inactive page with no generation indicator and no response
   progress after a patient wait.
9. Read the latest assistant response from the page.
10. Clear the check-in heartbeat as soon as the response is read or the run
    terminally fails. Do not leave it running past the run.

## Output

Return:

- ChatGPT's answer
- model, mode, and effort used
- conversation placement used: the project name plus `continue-exact`,
  `continue-recent-pro`, `new-in-project`, or `new-root` with a one-line reason
  when the choice was `new-root`
- attachment filenames, if any, and the PR URL when the GitHub connector was
  used
- a short note if the prompt was shaped before submission
- a short note when the run waited for a long Pro response, including that the
  heartbeat was set and cleared

If the run fails, name the exact failed condition and the next manual repair.
