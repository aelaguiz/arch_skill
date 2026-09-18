---
name: chatgpt-web
description: "Consult logged-in ChatGPT through BrowserOS after applying $browseros, writing the submission from its consultation templates in the user's voice with sources attached whole. Use for expert interpretation and planning, data questions, pushed PR reviews, attachments, and exact conversation continuation. Preserve Pro's independent judgment and verify the full submitted input before accepting its answer. Requires literal GPT-6 Astra Pro selected and read back in the model picker (a browser profile labeled Pro never proves the model), real @BigQuery access for data and @GitHub access for repo work, existing consultation profile windows only, and 3–5-minute generation checks. Never use the user's Work profile. Switch temporarily limited accounts without substituting another tier. Not for API work, generic browser automation, automated login, or a consultation the user did not request."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

**"Pro" is the model. It is never the browser profile.** Two unrelated things
carry that word on this machine:

- **Pro, the model:** GPT-6 Astra with the literal `Pro` option selected in
  the ChatGPT composer's model picker. In this skill, "Pro" alone always
  means this.
- **The consultation profiles:** the BrowserOS browser profiles the user keeps
  for agent ChatGPT work. Their labels start with `Pro` (`Pro 1`, `Pro2`,
  `Pro One`, and so on). A label is a name the user typed, the same kind of
  thing as `Work`. It says which ChatGPT login the page uses. It never
  selects, implies, or proves the model.

**Being in a consultation profile does not make a consultation Pro.** A page
in `Pro 1` sends to whatever model its composer holds, and the composer goes
back to ChatGPT's default on a new chat or a project page, even when the
thread you just left was on Pro. Two readings prove the model, and nothing
else does:

1. **Before Send, the composer's model pill on this page.** It reads `6 Pro`
   when Pro is selected. `Medium`, `High`, `Extra High`, `Instant`, or a
   model name without `Pro` means Pro is not selected: open the pill, keep
   `Latest` under `Select model`, move `Power` to its top position, `Pro, 5 of
   5`, close the menu, and read the pill again. Pro is a power level of
   `Latest`, not an entry in the model list: a list showing only `Latest`,
   `GPT-5.6 Sol`, and `GPT-5.5` is normal and never means Pro is missing. If
   the control looks different, open it and read which model and power are
   selected.
2. **After Send, the model slug on the response turn that answers your
   message:** `gpt-6-pro` for Pro. A tag or footer on an earlier turn says
   what served that turn, not yours.

Take both readings in every conversation you send into, unless the user named
another configuration, and write each with its time in the task notes. The
page carries other "Pro" text that says nothing about the model: the account
button (`Pro 1 Pro, open profile menu` is the account's display name and its
plan badge), `Used GPT-6 Pro` footers and `Pro feedback` buttons on earlier
turns, thread and project titles, and the word Pro in your own prompt.
Searching the page for "Pro" is not a reading, and "it was in `Pro 1`"
describes the browser profile. If a send went out without the first reading,
read the pill now and the slug as soon as answer text arrives; anything other
than Pro is a wrong-model submission, stopped and resent as described below.

**No Pro, no send.** When this composer's pill cannot be made to read `6 Pro`,
do not send the consultation from it on any model. A run on `Latest`,
`GPT-5.6 Sol`, `Extra High`, or anything else is not a weaker Pro
consultation. It is a different reviewer the user did not ask for, and saying
so afterward does not repair it: its answer, its interim notes, and its
sign-off are not evidence, not an interpretation, and not a review. Only the
user naming another model for this consultation changes that. Look for Pro in
another composer instead: an existing Pro thread in the same project, then the
same project in another consultation profile. If none reads `6 Pro`, pause this
consultation, tell the user what each composer read, and continue other work.
A menu click that did not change the pill selected nothing; the closed pill is
the only confirmation.

**Use only the existing consultation profiles.** Discover whichever are
configured; their number and spelling can vary.
**Never use the BrowserOS `Work` profile for ChatGPT.** It is reserved for the
user's personal use and rate-limit capacity, including when every consultation
profile is unavailable. This restriction also applies to retries and
continuation of an old conversation.

Consult Pro as an expert on the user's actual problem. For interpretation and
planning, give it the original objective, relevant history, and current
evidence so it can reconsider the question, diagnosis, and approach. The
parent reads that judgment as a whole and then reports it in the user's
preferred form. Calling Pro a peer does not compensate for restricting what
it may conclude.

**Every review brief hands over the original issue as filed and asks whether
the work is complete to its full scope and requirements, not only whether the
code is right.** The work is not done until Pro says it is implemented right,
the PR is ready, and it is complete to that scope; the templates carry the
wording.

**Every submission requires checking the full draft before Send and the new
submitted user turn afterward.** Accept an answer only when it belongs to that
verified request and serves the user's consultation purpose. Read this entry
file completely; retrieve any truncated portion before proceeding. After a
context compaction or a resume, read it again before the next browser phase: a
summary that says "work with Pro" does not carry these rules.

**Pro's wait is yours, never the user's.** A consultation is finished when
Pro's answer has been read and acted on, not when it was sent. Arm the host's
wake-up for it (a heartbeat or an equivalent automatic wake) and end the turn;
do the next useful work and read the answer when the wake fires. Never hand
"Pro is running" to the user as something for them to watch or come back for,
and never hold a turn open with sleeps to wait for it.

**Let Pro finish. It regularly takes around 30 minutes and can take longer.**
That is an expectation, never a deadline. Do not click **Stop answering** on a
correct submission unless the user explicitly asks to stop. **A submission
that went out wrong is the one case to stop at once:** a missing attachment
chip or connector pill, duplicated or truncated text, or the wrong model or
surface makes the answer unusable, so click Stop, fix the submission, and
resend it whole. Letting it finish and "sending the files in a follow-up" is
not a repair; Pro has already answered without them, and "the prompt is
self-contained" is the agent's restatement standing in for the sources.
Observe actual thinking/activity and answer changes on a correct submission;
after at least 15 minutes without progress, reload once and recover
the consultation autonomously as described below.

## Critical operating rules

- **Apply `$browseros` before every browser phase.** Read
  [the BrowserOS skill](../browseros/SKILL.md) before the first call and obey it
  throughout. Protect the user's foreground focus and continually verify the
  working profile/window/page. Use existing windows and one eligible ChatGPT
  tab at a time. Never substitute another browser, the API, shell browser
  scripts, cookie handling, or automated login.
- **Pro means GPT-6 Astra with the literal `Pro` option.** Use ChatGPT's
  `Chat` surface and `Extended` thinking when separately offered, unless the
  user explicitly requests another configuration. **Extra High, xhigh, Ultra,
  Thinking, a `5/5` indicator that does not say `Pro`, the highest remaining
  setting, or a browser profile labeled `Pro` is not Pro.** Browser profile labels and ChatGPT's own
  controls share words by coincidence: the profile labeled `Pro 1` does not
  select the `Pro` model, and the profile labeled `Work` is separate from
  ChatGPT's `Work` surface. A Pro request uses the `Chat` surface and the
  picker's `Pro` option in every profile.
- **Use a consultation profile whose account currently offers Pro.** Discover
  the already-open consultation profiles, such as `Pro 1`, `Pro2`, `Pro3`,
  `Pro4`, `Pro5`, or others present; exclude `Work` from the pool.
  Pro is missing from a composer only when `Power` cannot reach it: the slider
  ends at `Extra High, 4 of 4` and a disabled `Pro` entry appears under the
  model list. Hover that entry to read why; `Limit reached. Try again after
  ...` is the account's rate limit and its reset time. A model list without
  any `Pro` entry says nothing, and a pill reading `6 Pro` proves that composer
  offers it. Note
  unavailable accounts and the account that works, with check times and
  connector status. Switch to another consultation profile
  instead of substituting a different tier, and select and read back `Pro`
  again there. All should have the same projects;
  verify the destination and carry the needed conversation context and inputs.
- **Require real source access.** For data, attach `@BigQuery`; for GitHub or
  repository work, attach `@GitHub`; attach both when needed. Verify the
  connector pill in the draft and on the submitted turn, and verify retrieval
  of the required data or code.
  A badge, typed name, or confident assertion is insufficient. Missing or broken
  access means switch to a suitable consultation profile's window or stop
  and tell the user.
  Never accept or act on guesses about sources Pro could not access.
- **Wait for the requested review.** After submission readback, check generation
  every **3–5 minutes**, defaulting to 5, with the heartbeat at the same cadence.
  Keep waiting while substantive traces or answer content advance, however long
  the run takes. A ticking clock or spinner is not progress. Keep the requested
  review pending until its usable answer arrives; continue independent work.
  **The agent watches for Pro's answer, never the user.** Sending is not
  done. A progress update that says Pro is running is fine when the wake-up is
  armed and the update says what will read the answer; telling the user the
  answer is pending for them to read is not. The consultation is done when the
  answer is read and acted on.

## Prepare the consultation

Apply [the shared orchestration policy](../_shared/agent-orchestration-policy.md)
before querying. This is an explicitly chosen web consultation, not the default
route for ordinary parallel work. Decide whether the task needs a new context
or continuation of a particular conversation; do not inherit whichever thread
happens to be open.
The shared policy's deadlines and stall actions for owned processes do not
set a timeout for a ChatGPT web response; this skill owns its recovery.

Write the submission the way the user would say it to a colleague, not as a
request form. Before writing, read the shape and the pre-send check in
[consultation-templates.md](references/consultation-templates.md), then the
family that matches the ask: reviewing a PR, after fixes, checking a
written-up plan, planning an issue, an on-track check, a design round, a
diagnosis, an audit, a retry, or a new thread. That family's shape,
anti-patterns, and attach list are the contract for the submission.
`$prompt-authoring`'s rules hold underneath; where its scaffold and the
user's phrasing disagree, the phrasing wins.

Hand over the sources whole: the canonical requirements source as a full
export, the plan, the user's own words verbatim, raw evidence, and the PR or
branch with `@GitHub` written in the brief so it becomes the connector pill
(the words "GitHub connector" attach nothing). Offer the agent's status as a
belief and ask
about intent. Wherever something is being authored (a plan, a design, a
diagnosis, an issue set) Pro writes it; the agent brings context, asks
questions, goes back and forth until it is fully formed, then carries the
agreed result into the artifact verbatim.

Never ask for a verdict token, cap the answer, fence what Pro may conclude,
pin a commit SHA, or restate a source in place of attaching it. Narrowing the
work never narrows what Pro sees. Read Pro's full assessment before condensing
it for the user; the agent, not Pro, writes any verdict. A lane the user
selected for a strict verdict, such as `$fresh-consult` or
`$codex-review-yolo`, keeps its own footer by design. Preserve explicit
verbatim relays.

Before Send, run the reference's pre-send check on the actual draft; a failed
question means a rewrite. That check is the pre-send review for a Pro
submission; a dispatch-dimension checklist does not replace it.

Read [accounts-and-conversations.md](references/accounts-and-conversations.md)
before choosing or switching the account, project, thread, or model controls.
Prefer the applicable project and an appropriate existing workstream thread;
an explicit user choice of exact thread or fresh chat wins. If an exact requested
conversation cannot be identified, ask rather than sending into unrelated
history. Use a root chat only when no existing project fits and report that choice.

Under `$browseros`, choose one authorized page in the selected existing window.
Verify login with the safe boolean session check in that reference. Never
inspect or output account details, tokens, cookies, or raw session data. Login
and connector authorization repairs are manual.

Run prompts serially in the same tab. Continue a conversation for follow-ups;
start a clean conversation for independent asks. Do not add tabs for uploads,
polling, or readback. Retry in place first; if recovery needs a branch and the
site creates a destination tab, verify it and continue there alone.
During account switching, continue in the new
verified page alone and clean up task-created pages no longer needed. If the
user requests parallel ChatGPT runs, explain the serial constraint and proceed
serially unless simultaneity is mandatory, in which case report the mismatch.

## Supply the inputs and send

Enter the brief into the composer with the paste method in the composer
reference: it keeps paragraphs and bullets as written, never submits on its
own, and turns a literal `@GitHub` or `@BigQuery` into the connector pill.
Never `fill` or `type` the brief; keystroke newlines are Enter and submit a
fragment mid-fill. Plans, exports, evidence, and any other source go in files
the brief names; a one-line composer message pointing at an "ask file" is not
a brief. Check absolute paths, existence, and the maximum of 10 attachments.
Never drop requested files silently. Attach only through the temporary-input
route in the composer reference; never click ChatGPT's `Add files and more` or
`Add photos & files`, which open an operating-system file dialog that no tool
can close and the user then has to cancel. Read
[composer-and-attachments.md](references/composer-and-attachments.md) before
attaching files, invoking connectors, or diagnosing composer interaction.

For a code review, commit and push the reviewable work to its PR branch and
include the PR URL with `@GitHub`; do not pin a commit SHA, Pro reads the
latest. Pasted diffs or descriptions do not replace the connector's access to
the branch. Attach the canonical requirements source whole, exported as
described in the composer reference. Name the relevant repository or data
scope so retrieval addresses the actual question.

Before sending, verify the intended profile/window/page and conversation,
`Chat` surface, the picker's selected model, literal `Pro` option, and effort
as read from this page, every attachment chip, and each
required connector pill, immediately before the click and on every send path.
The profile check and the model check are two separate readings; the profile
label never answers the model check.
Attachments do not survive a page reload; the text draft does. Any reload,
clear, or retry resets this verification: a chip seen earlier is not a chip
now. An insert or paste that timed out may have landed; read the composer
before repeating it, and if the text is duplicated, clear it and enter it
once. Record the latest submitted user-message identity, then
fill the live visible composer and compare its complete text with the intended
message before clicking Send. Check that filling did not itself create a new
user message. A failed fill must not send a stale draft. Use the current tool
schema and fresh refs.

Send once, then identify the new submitted user message separately from the
composer. Compare its full body and attachment list with the intended input,
verify the visible composer cleared, and associate the response with that
message. Record the user-message and outer response-turn IDs together when
the response appears; virtualized history can later omit intervening turns.
Inspect collapsed text fully; a matching prefix or a whole-page text
search is insufficient. If the submitted turn is missing any required
attachment or connector pill, carries duplicated or truncated text, or went
to the wrong model or surface, the answer cannot be used: click Stop
answering now, then resend the complete submission (family I) with every
file re-attached and every chip and pill re-verified. Do not let a wrong
submission run to completion, and do not patch it with a follow-up message.
If Send times out or disconnects, read back its outcome before deciding
whether to retry. Do not claim delivery or interpret the answer until this
readback succeeds.

When repairing delivery or access, preserve the consultation's substantive
question, evidence, and scope. A technical retry does not authorize replacing
an open assessment with a narrower debate or acceptance checklist.

## Wait, read, and judge the result

Use the 3–5 minute generation-check cadence from the critical rules. Between
checks, do independent work or use host waits; short host wakeups and user-facing
updates do not require another browser call. Set the host's check-in heartbeat
when available and clear it when the response is read or the run terminally
fails. Do not claim a heartbeat was set if the host has none.

Before monitoring, read
[generation-progress-and-recovery.md](references/generation-progress-and-recovery.md).
Anchor observations to the verified user message and its following response
turn. Read the actual thinking summary, research/tool entries, interim messages,
and answer text. Open that response's thinking disclosure when needed: the
Activity panel can contain the traces outside `main` while the inline response
says only `Pro thinking`. An assistant-message node may not exist yet.

Keep the last substantive content and its observation time in the task notes.
Compare content at each scheduled check, including same-length revisions;
new/revised traces, results, or answer text reset the inactivity window. A
timer tick, spinner, old answer, or mere DOM remount does not. Missing selectors,
sparse snapshots, and truncated tool output require a better read, not a stall
diagnosis. Restore this state after compaction; if it was lost, observe again
rather than inventing how long the page has been inactive.

After **at least 15 minutes without substantive progress across multiple
checks**, preserve the request and reload the same page once. This is a UI
recovery trigger, not proof Pro is dead or permission to cancel it. An explicit
page/response error or a verified bad submission can enter recovery immediately.
Reidentify the conversation and response, reopen its Activity panel as needed,
and read the recovered state. If the answer is complete, read it; if progress
resumes, keep waiting. If it remains incomplete and not progressing after the
page settles, retry the complete original request through the available retry
or Send control and verify its delivery. If the same conversation cannot
recover, branch from the last useful context and continue in the verified
destination. Follow the reference for disabled input and branch mechanics.

Do not turn routine stalls into a user handoff or stop at an error report. Keep
recovering toward the requested answer without requiring the user to be present.
Never shorten recovery into repeated Stop clicks, refresh loops, or a demand to
stop researching and answer immediately. Preserve required evidence, connectors,
Pro configuration, and expert freedom on every retry. Reconcile any external
writes Pro was authorized to perform before repeating those instructions.
For missing/broken connectors or an account cap, use the account-switching
procedure; actual login or authorization repairs remain manual.

Accept only a response that serves the user's original consultation purpose
and addresses the verified submitted ask using the required inputs, with actual
successful connector retrieval where required. If the parent asked the wrong
question, repair the prompt before treating its answer as the requested review.
A completed response that guesses around a missing file, inaccessible repo, or failed data
query is invalid. Repair access or inputs before resubmission; do not relay that
response as a verdict or use it to publish dependent changes.
Refusals, empty replies, and answers that omit the requested work also fail
this completion check; diagnose and repair the specific cause.

If no consultation profile's account offers the required configuration, report the
profiles checked and observed conditions, pause the blocked consultation or
decision, and continue useful independent work. Wait for the user to say Pro is
available again rather than polling capped accounts. Never fall back to `Work`.

## Return the result

Return the answer plus a short receipt: the surface, model, option, and
effort quoted as read from the page before Send and from the response turn,
on their own line; the verified working profile/window/page and account
availability observations on a separate line;
project and conversation link or identity; attachment filenames and the data
or code actually retrieved through connectors, including the PR URL when used.
The model line comes only from those page readings, never from the profile
label, the request, or the plan; without a reading, say the model was not
verified and do not call the answer a Pro review.
Keep three things separate in the receipt: what Pro was shown, what Pro said,
and the agent's own conclusion. "Pro signed off" alone is not a receipt.
Mention material prompt shaping and long waits, and report heartbeat cleanup
accurately. Follow BrowserOS resource cleanup and identify any retained or
unknown state. Keep secrets and sensitive URLs out of receipts.

On failure, name the exact condition and next repair, plus the dependent
consultation or decision still pending. Do not report success based only on
finished generation.

Use this skill for explicit ChatGPT web consultations, data questions, pushed
PR reviews, attachments, and conversation continuation. Use other guidance for
OpenAI API work, generic browser tasks, or BrowserOS installation. Do not send
a Pro prompt merely to test this skill.
