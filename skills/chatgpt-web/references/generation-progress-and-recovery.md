# Observe Pro's progress and recover the consultation

Read before monitoring a response or recovering a stalled/incorrect submission.
Use BrowserOS on the verified profile/window/page. These are observed DOM shapes,
not permanent selectors; inspect the current structure when they change.

Sections: [find the current response](#find-the-current-response),
[read activity](#read-the-activity-panel),
[compare observations](#compare-substantive-content),
[DOM read example](#scoped-dom-read-example),
[recover](#recover-without-stop-answering).

## Find the current response

Start from the user-message ID verified after Send, currently on
`[data-message-author-role="user"][data-message-id]`. Find its containing
`[data-testid^="conversation-turn-"]`, then the response turn(s) after it and
before the next user turn. Observed outer turns are `section` elements with
`data-turn="user"` or `"assistant"` and `data-turn-id`; other layouts can use
`article`. Do not assume a particular tag or reuse turn numbers across chats.

During thinking, the outer assistant turn can exist without any
`[data-message-author-role="assistant"]` inside it. That inner message may only
appear when answer text arrives. Selecting the last assistant-message node can
therefore return an older answer. Keep the pending user ID and response turn
identity together. If a turn is not mounted or another user message appeared,
reidentify the requested work before deciding whether it progressed.

Record that association when the new submission and response first appear.
Long chats can unmount intervening turns: observed mounted turns included
`conversation-turn-1` immediately followed by `conversation-turn-8`. They were
not a question/answer pair. Later reads must locate the recorded response ID,
not re-pair whichever nodes are adjacent now. If either ID changes during
reload or placeholder replacement, inspect the actual request and response to
reestablish the pair. Use a supported page-targeted scroll/read to reveal missing
context when needed; do not invent an association from incomplete DOM history.

## Read the Activity panel

The inline turn can contain only a `Pro thinking` button while more detailed
activity is available in its disclosure. Use a fresh BrowserOS snapshot and
open the thinking/activity control **inside the current response turn**.
Confirm which response you opened; an already-open panel can belong to an
older answer. Do not click the composer's Stop control or an old answer's
`Stopped thinking` disclosure by mistake.

Observed panel structure:

```html
<section aria-label="Reasoning details" data-testid="screen-threadFlyOut">
  <!-- header: [data-testid="bar-search-sources-header"] -->
  <!-- Activity · 12m 36s: elapsed time, not evidence of progress -->
  <div slot="content">
    <!-- thinking summaries, research/tool activity, displayed details -->
  </div>
</section>
```

This panel can be **outside `main`**. Read its `[slot="content"]` separately
from the current response turn. A `get_page_content` call scoped only to `main`
or an interactive-element snapshot can omit the very traces needed to judge
progress. Use bounded BrowserOS DOM/content reads, not internal application
state or private network endpoints. If output is saved to a file, read that
file; missing tool output is not missing model activity.

After completion, the Activity body can empty while the answer and a
`Worked for 16m 37s` disclosure appear in the conversation. Opening that
disclosure can reveal the research history inline. Read the completed turn;
do not diagnose failure from the now-empty panel or count disclosure expansion
as newly generated content.

## Compare substantive content

At the entry file's 3–5-minute cadence, compare the current response and its
Activity body with the previous observation. Retain the latest substantive
text and `last_progress_at` in the existing task state. Reset that time when
new/revised summaries, research results, tool entries, or answer content appear.
Compare content, not just character counts: a summary can change without growing.

Examples that teach the distinction:

| Observation | Interpretation |
| --- | --- |
| A research entry is added, such as `Reviewed card abstraction, loader policy, and showdown dispatch logic`. | New visible activity; reset the inactivity window and wait. |
| `Preparing the implementation plan` gains or revises its explanatory paragraph. | Substantive summary progress, even if no final answer exists. |
| New answer paragraphs or a revised section appear after the anchored user turn. | Answer progress; keep reading at the normal cadence. |
| `Activity · 9m 51s` becomes `Activity · 12m 36s`, with identical body text. | Only the clock advanced; do not reset the inactivity window. |
| `Pro thinking` shimmers, a spinner animates, an old answer changes layout, or a section remounts. | UI activity alone does not establish progress on this request. |

Opening a collapsed panel can reveal earlier work. Establish a content baseline;
do not claim that all newly exposed text was generated since the last check.
If observation was unavailable, repair it and establish a baseline rather than
counting the gap as proven inactivity. An unchanged trace does not prove the
backend has stopped thinking; prolonged observed inactivity calls for reload.

## Scoped DOM read example

Adapt this expression to the live BrowserOS evaluate schema. Supply the user
and outer response IDs recorded during submission verification. First verify
the conversation identity and open/verify this response's
Activity panel through its own disclosure; the panel has no reliable message-ID
attribute to establish that association by itself. This expression only reads.

```javascript
(() => {
  const userId = 'VERIFIED_USER_MESSAGE_ID';
  const responseId = 'VERIFIED_RESPONSE_TURN_ID';
  const turns = [...document.querySelectorAll('main [data-testid^="conversation-turn-"]')];
  const matches = turns.filter(e => e.getAttribute('data-turn-id') === responseId);
  if (matches.length !== 1) return {observation: 'Response turn absent or ambiguous; reidentify it.'};
  const response = matches[0];
  const user = document.querySelector(`[data-message-author-role="user"][data-message-id="${CSS.escape(userId)}"]`);
  const laterUserTurn = turns.slice(turns.indexOf(response) + 1).some(e =>
    e.getAttribute('data-turn') === 'user' || e.querySelector('[data-message-author-role="user"]'));
  const visible = e => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const panel = [...document.querySelectorAll('section[aria-label="Reasoning details"]')].find(visible);
  const state = testid => {
    const e = document.querySelector(`button[data-testid="${testid}"]`);
    return {present: visible(e), enabled: visible(e) && !e.disabled && e.getAttribute('aria-disabled') !== 'true'};
  };
  return {
    observedAt: new Date().toISOString(),
    conversation: location.origin + location.pathname,
    userMessageId: userId, userMounted: !!user, laterUserTurn,
    response: {
      turnId: responseId, text: response.innerText,
      answerMessages: [...response.querySelectorAll('[data-message-author-role="assistant"]')].map(m => ({id: m.getAttribute('data-message-id'), text: m.innerText}))
    },
    activityPanelVisible: visible(panel),
    activityText: laterUserTurn ? null : panel?.querySelector('[slot="content"]')?.innerText ?? null,
    stop: state('stop-button'), send: state('send-button')
  };
})()
```

The Activity header is deliberately excluded. Save large returned text to a
local artifact and compare the full normalized content while returning only
the meaningful delta to context. Do not use a fixed prefix or tail as the sole
comparison: middle sections can change. Inspect what changed before labelling
it progress; disclosure, virtualization, and completion can reshape the DOM.
If `laterUserTurn` is true, global composer controls and the open panel may
belong to that later request; reidentify the current work before using them.
`userMounted: false` can mean virtualization; it does not undo the recorded
association or prove a missing submission. A missing/ambiguous response ID
requires reidentification, never substitution of another mounted response.

## Recover without Stop answering

The entry file sets the timing: roughly 30 minutes is normal, with no completion
deadline; 15+ minutes of observed inactivity permits one same-page reload.
Never translate this into “allow up to 30 minutes.” Preserve the complete ask,
attachment paths, required connectors, and pending turn identity before reload.

1. **Reload once and reacquire state.** Reverify profile/window/conversation,
   locate the submitted turn, and open its Activity disclosure again if needed.
   Let the page settle and make a scoped reread. A remount or timer reset is
   not resumed work. If substantive traces resume, return to ordinary waiting.
2. **Read any recovered answer fully.** Associate it with the submitted ask
   and inspect whether generation finished. A disabled Stop button can be a
   transitional state; an enabled Send button or an older `Stopped thinking`
   label alone does not prove this answer is complete. Apply the entry file's
   source-access and answer-quality checks.
3. **Retry the complete request when recovery still shows a failed/incomplete,
   non-progressing response.** Use the current response's retry/regenerate
   control if it preserves the verified full input, or resubmit through the
   visible composer. For a partial original submission, send the corrected
   complete input. Reattach and verify needed files/connectors. If the original
   user message exists but its response failed, that does not prohibit a
   deliberate retry. Verify the new turn or response attempt before waiting.
4. **Branch if the same conversation cannot recover.** A composer that remains
   disabled after reload is a reason to use the conversation's supported branch
   control, not Stop. Branch from the last useful complete context before the
   failed exchange. The observed response menu is `More actions` → `Open new
   branch`; other layouts may say `Branch in new chat`. Use fresh controls.
   Reidentify the destination, verify project/Pro and
   required inputs, restore missing context, and send the full original ask.
   If branching is unavailable, continue in a fresh chat in the same project
   with that context. Keep one active consultation; retain the original as
   evidence and identify any task-created destination under BrowserOS.

Carry the same expert question through recovery. Do not replace it with “no
more research,” “answer now,” a smaller checklist, or an older verdict. Routine
stalls are yours to recover; do not end at a report asking the user to rescue
the session. If the retried run progresses, give it the same patient treatment.

For requests that authorized external writes, inspect the actual destination
before repeating them and resume only the outstanding work. A failed-looking
ChatGPT UI does not prove that issue creation or another write failed. Required
account/connector failures follow the entry file's account-switching rules;
recovery never authorizes guessed source access or automated login.
