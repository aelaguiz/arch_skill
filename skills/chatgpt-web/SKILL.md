---
name: chatgpt-web
description: "Consult logged-in ChatGPT through BrowserOS after applying $browseros and $prompt-authoring. Use for expert interpretation and planning, data questions, pushed PR reviews, attachments, and exact conversation continuation. Preserve Pro's independent judgment and verify the full submitted input before accepting its answer. Requires literal GPT-6 Astra Pro, real @BigQuery access for data and @GitHub access for repo work, existing Work/Pro profile windows, and 3–5-minute generation checks. Switch temporarily limited accounts without substituting another tier. Not for API work, generic browser automation, automated login, or a consultation the user did not request."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

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
- **Use an account that actually offers Pro.** Discover the already-open
  `Work` and variable number of Pro profiles, including Pro2, Pro3, or others
  present. Missing or disabled literal Pro probably means a temporary account
  limit; an explicit cap confirms it. Note unavailable accounts and the account
  that works, with check times and connector status. Switch to another account
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
  Never poll every 10 seconds. Pro can take 10+ minutes. Elapsed time, a short
  host wait, or a self-imposed review budget does not justify cancelling it or
  substituting an older answer. Keep decisions that require this review pending
  until a usable response arrives; continue independent authorized work.

## Prepare the consultation

Apply [the shared orchestration policy](../_shared/agent-orchestration-policy.md)
before querying. This is an explicitly chosen web consultation, not the default
route for ordinary parallel work. Decide whether the task needs a new context
or continuation of a particular conversation; do not inherit whichever thread
happens to be open.

Read and apply [the prompt-authoring skill](../prompt-authoring/SKILL.md) to the
actual outgoing request before every submission: composer text, instructions
inside attachments, and relevant assumptions carried by the thread. Loading
the skill or checking a reusable template does not perform this review.

Begin with the decision the user needs help making. For new results, restore
the original goal and explain what was tried, what was observed,
and what remains uncertain. Supply the relevant evidence without replacing it
with the parent's preferred interpretation. Present the current plan and
candidate explanations as proposals unless the user actually made them binding.
Invite Pro to decide what matters and change, reorder, or discard the approach.
A useful recognition test is whether Pro could reject the parent's question or
preferred experiment and still fulfill the user's request.

Keep the brief concise without capping the expert's assessment to the parent's
final-summary format. Ask for the judgment needed in whatever structure best
explains it; do not impose fixed bullet counts, closed choices, or a preserved
plan merely to make the answer easy to summarize. Read Pro's full assessment
before condensing it for the user. Real constraints and specific questions
remain useful; a named source-repair review can legitimately have a narrow
verdict. Infer that scope from the task, not from a habitual review template.
Preserve explicit verbatim relays.

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
polling, retries, or readback. During account switching, continue in the new
verified page alone and clean up task-created pages no longer needed. If the
user requests parallel ChatGPT runs, explain the serial constraint and proceed
serially unless simultaneity is mandatory, in which case report the mismatch.

## Supply the inputs and send

For a plan or any multi-paragraph body, attach a file and use only a short
single-paragraph composer message pointing to it. Keyboard-based fills can
turn newlines into Enter and submit a fragment during the fill itself.
Check absolute paths, existence, and the maximum of 10 attachments. Never drop
requested files silently. Read
[composer-and-attachments.md](references/composer-and-attachments.md) before
attaching files, invoking connectors, or diagnosing composer interaction.

For a code review, commit and push the reviewable work to its PR branch and
include the exact PR URL with `@GitHub`. Pasted diffs or descriptions do not
replace the connector's access to the branch. Name the relevant repository or
data scope so retrieval addresses the actual question.

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
message. Inspect collapsed text fully; a matching prefix or a whole-page text
search is insufficient. If it split or truncated, the resulting answer cannot
be used: stop that invalid generation if still running, using a freshly
verified control, repair the input, and submit correctly. If Send times out or
disconnects, apply BrowserOS unknown-outcome handling before retrying. Do not
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

At each scheduled check, read the visible thinking summary, interim messages,
partial answer, errors, and connector activity. A spinner-only check is
insufficient. If a snapshot is sparse or contains empty paragraph nodes, use
bounded visible-text reads; tool-output truncation or omitted text does not
prove Pro is silent. Read the full final response and relevant visible interim
output before accepting it.

Do not refresh, resubmit, open another polling tab, or cancel while a valid
response is generating. Cancellation needs the user's stop instruction or a
concrete invalid run, such as wrong input, failed required access, or an explicit
error. Inspect fresh state and the exact control before cancelling; an old Stop
ref may be stale or the response may have completed. A pending required review
is never a passed review, and prior guidance does not replace the requested answer.

Act on concrete failures when observed. For missing or broken connectors,
switch to another suitable already-open Pro account or stop and name the failed
access. For a cap or missing Pro, follow account switching. Dismiss transient
blocker dialogs, but do not resubmit unless readback proves no prompt was
submitted; after a transient submission failure, wait about 5 minutes before
retrying in the same page. A lost session or required manual action needs the
specific manual repair. A long-running generation alone is not failure.

Accept only a response that serves the user's original consultation purpose
and addresses the verified submitted ask using the required inputs, with actual
successful connector retrieval where required. If the parent asked the wrong
question, repair the prompt before treating its answer as the requested review.
A completed response that guesses around a missing file, inaccessible repo, or failed data
query is invalid. Repair access or inputs before resubmission; do not relay that
response as a verdict or use it to publish dependent changes.
Refusals, empty replies, and answers that omit the requested work also fail
this completion check; diagnose and repair the specific cause.

If no available account offers the required Pro configuration, report the
profiles checked and observed conditions, pause the blocked consultation or
decision, and continue useful independent work. Wait for the user to say Pro is
available again rather than polling capped accounts.

## Return the result

Return the answer plus a short receipt: actual surface/model/mode/effort;
verified working profile/window/page and account availability observations;
project and conversation link or identity; attachment filenames and the data
or code actually retrieved through connectors, including the PR URL when used.
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
