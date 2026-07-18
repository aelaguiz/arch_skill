---
name: chatgpt-web
description: "Query logged-in ChatGPT through one BrowserOS ChatGPT tab after applying the canonical $browseros operating contract and shaping the prompt with $prompt-authoring discipline. Use when the user explicitly wants the ChatGPT web provider/capability, optional attachments, or an exact existing ChatGPT conversation continued. New clean conversation is the default; exact-conversation continuation must be explicit. Defaults to Pro with Extended thinking, runs serially, and waits patiently. Not for OpenAI API work, generic browser automation, automated login, scripts, runners, or hidden harnesses."
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
- The user has a rough prompt and wants it shaped before sending.

## Do Not Use When

- The user wants OpenAI API usage or product/API guidance.
- The user wants generic web automation unrelated to ChatGPT.
- BrowserOS MCP is unavailable in the current host.
- ChatGPT is not already logged in in BrowserOS.
- The task would require automated login.
- The user requests more than 10 attachments.

## Non-Negotiables

- Apply `$browseros` before the first direct BrowserOS MCP call and obey it
  throughout this workflow.
- Use BrowserOS MCP, not `web.run`, OpenAI API calls, shell browser scripts, or
  direct cookie/session handling.
- Use one BrowserOS `https://chatgpt.com/` tab for the whole run. Reuse an
  eligible current-agent-controlled ChatGPT page when one can be safely
  task-adopted under `$browseros`; otherwise open exactly one ChatGPT page.
  Reusing the page does not mean reusing its conversation. Do login check,
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
- Use `$prompt-authoring` discipline before submission when the user's prompt is
  rough, underspecified, high-stakes, or likely to benefit from a stronger
  reusable prompt shape.
- Default to ChatGPT `Pro` with `Extended` thinking when the user does not name
  a mode or effort.
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
- Default to a new clean ChatGPT conversation. Continue an exact conversation
  only when the user asks to continue it and the intended conversation can be
  identified. If it cannot, stop and ask for the missing conversation choice
  rather than sending into an unrelated history.

## First Move

1. Resolve the user's desired ChatGPT ask and any explicit mode, effort, model,
   or attachment requests.
2. If the prompt needs shaping, apply `$prompt-authoring` before touching
   ChatGPT. Keep the prompt faithful to the user's intent.
3. Resolve `conversation = new-clean | continue-exact`. Default to `new-clean`;
   use `continue-exact` only from an explicit user request and an identifiable
   target conversation.
4. Under `$browseros`, select the single current-agent-controlled ChatGPT page
   for the run: safely task-adopt an eligible `https://chatgpt.com/` page, or
   open exactly one new page.
5. Verify that page is logged in before doing anything else.
6. In that page, open a new chat for `new-clean`, or navigate to and verify the
   exact requested conversation for `continue-exact`. Do not submit while the
   page is merely showing an arbitrary prior thread.

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

## Mode And Effort

Default when the user does not specify:

```text
mode = Pro
effort = Extended
model family = current ChatGPT default
```

Use the ChatGPT model pill beside the composer. Prefer `Configure...` when
available because it exposes the `Intelligence` dialog with explicit model
options and thinking effort.

Observed controls to select from:

- mode: `Instant`, `Thinking`, `Pro`
- effort: `Light`, `Standard`, `Extended`, `Heavy`
- model family: leave as current unless the user explicitly names one

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

1. Verify the selected conversation mode one final time. For a new clean run,
   the page must be a new chat; for continuation, the visible thread must be the
   exact requested conversation.
2. Fill the ChatGPT composer with the final prompt.
3. Confirm the selected mode and effort match the request or default.
4. Confirm every attachment chip is present.
5. Click `Send prompt`.
6. Wait in the same tab until generation finishes. For `Pro`, `Extended`, or
   `Heavy`, 10+ minutes can be normal; poll slowly and let ChatGPT finish.
7. Do not refresh, resubmit, open another tab, or start another ChatGPT prompt
   while a response is still generating.
8. Treat failure as concrete, not time-based: visible ChatGPT error, lost
   login/session, required manual user action, missing attachment before send,
   or a clearly inactive page with no generation indicator and no response
   progress after a patient wait.
9. Read the latest assistant response from the page.

## Output

Return:

- ChatGPT's answer
- mode and effort used
- conversation mode used (`new-clean` or `continue-exact`)
- attachment filenames, if any
- a short note if the prompt was shaped before submission
- a short note when the run waited for a long Pro response

If the run fails, name the exact failed condition and the next manual repair.
