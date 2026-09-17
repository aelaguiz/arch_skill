---
name: chatgpt-web
description: "Consult logged-in ChatGPT through BrowserOS after applying $browseros, writing the submission from its consultation templates in the user's voice with sources attached whole. Use for expert interpretation and planning, data questions, pushed PR reviews, attachments, and exact conversation continuation. Preserve Pro's independent judgment and verify the full submitted input before accepting its answer. Requires literal GPT-6 Astra Pro, real @BigQuery access for data and @GitHub access for repo work, existing numbered Pro profile windows only, and 3–5-minute generation checks. Never use the user's Work profile. Switch temporarily limited Pro accounts without substituting another tier. Not for API work, generic browser automation, automated login, or a consultation the user did not request."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

**Use only the existing numbered Pro profiles, such as Pro 1 through Pro 5.**
Discover whichever are configured; their number and spelling can vary.
**Never use the BrowserOS `Work` profile for ChatGPT.** It is reserved for the
user's personal use and rate-limit capacity, including when all Pro profiles
are unavailable. This restriction also applies to retries and continuation of
an old conversation.

Consult Pro as an expert on the user's actual problem. For interpretation and
planning, give it the original objective, relevant history, and current
evidence so it can reconsider the question, diagnosis, and approach. The
parent reads that judgment as a whole and then reports it in the user's
preferred form. Calling Pro a peer does not compensate for restricting what
it may conclude.

**Every submission requires checking the full draft before Send and the new
submitted user turn afterward.** Accept an answer only when it belongs to that
verified request and serves the user's consultation purpose. Read this entry
file completely; retrieve any truncated portion before proceeding.

**Let Pro finish. It regularly takes around 30 minutes and can take longer.**
That is an expectation, never a deadline. Do not click **Stop answering** unless
the user explicitly asks to stop. Observe actual thinking/activity and answer
changes; after at least 15 minutes without progress, reload once and recover
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
  Thinking, a `5/5` indicator, or the highest remaining setting is not Pro.**
  The BrowserOS profile named `Work` is separate from ChatGPT's `Work` surface;
  a Pro request must use the `Chat` surface in every profile.
- **Use a numbered Pro account that actually offers Pro.** Discover the
  already-open Pro profiles, including Pro 1, Pro2, Pro3, Pro4, Pro5, or other
  numbered Pro profiles present; exclude `Work` from the account pool.
  Missing or disabled literal Pro probably means a temporary account
  limit; an explicit cap confirms it. Note unavailable accounts and the account
  that works, with check times and connector status. Switch to another Pro account
  instead of substituting a different tier. All should have the same projects;
  verify the destination and carry the needed conversation context and inputs.
- **Require real source access.** For data, attach `@BigQuery`; for GitHub or
  repository work, attach `@GitHub`; attach both when needed. Select the actual
  connector in the picker and verify retrieval of the required data or code.
  A badge, typed name, or confident assertion is insufficient. Missing or broken
  access means switch to a suitable Pro window or stop and tell the user.
  Never accept or act on guesses about sources Pro could not access.
- **Wait for the requested review.** After submission readback, check generation
  every **3–5 minutes**, defaulting to 5, with the heartbeat at the same cadence.
  Keep waiting while substantive traces or answer content advance, however long
  the run takes. A ticking clock or spinner is not progress. Keep the requested
  review pending until its usable answer arrives; continue independent work.
  **The agent watches for Pro's answer, never the user.** Sending is not
  done. Do not end the turn by telling the user Pro's answer is pending for
  them to read; the consultation is done when the answer is read and acted on.

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
branch with `@GitHub` typed and picked in the composer (the words "GitHub
connector" attach nothing). Offer the agent's status as a belief and ask
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

The ask itself goes in the composer as one paragraph, however long it runs:
keyboard-based fills can turn newlines into Enter and submit a fragment
during the fill itself, so the brief carries no line breaks. Plans, exports,
evidence, and any other long body go in files the ask names; a one-line
composer message pointing at an "ask file" is not a brief. Check absolute
paths, existence, and the maximum of 10 attachments. Never drop requested
files silently. Read
[composer-and-attachments.md](references/composer-and-attachments.md) before
attaching files, invoking connectors, or diagnosing composer interaction.

For a code review, commit and push the reviewable work to its PR branch and
include the PR URL with `@GitHub`; do not pin a commit SHA, Pro reads the
latest. Pasted diffs or descriptions do not replace the connector's access to
the branch. Attach the canonical requirements source whole, exported as
described in the composer reference. Name the relevant repository or data
scope so retrieval addresses the actual question.

Before sending, verify the intended profile/window/page and conversation,
`Chat` surface, model, literal mode and effort, every attachment chip, and each
required connector. Record the latest submitted user-message identity, then
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
search is insufficient. If it split or truncated, the resulting answer cannot
be used: preserve the full intended input and repair delivery through the
recovery procedure below, without clicking Stop. If Send times out or
disconnects, read back its outcome before deciding whether to retry. Do not
claim delivery or interpret the answer until this readback succeeds.

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

If no eligible numbered Pro account offers the required configuration, report the
profiles checked and observed conditions, pause the blocked consultation or
decision, and continue useful independent work. Wait for the user to say Pro is
available again rather than polling capped accounts. Never fall back to `Work`.

## Return the result

Return the answer plus a short receipt: actual surface/model/mode/effort;
verified working profile/window/page and account availability observations;
project and conversation link or identity; attachment filenames and the data
or code actually retrieved through connectors, including the PR URL when used.
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
