# ChatGPT Composer, Connectors, and Attachments

Read the relevant section before attaching files or connectors, or when a
composer interaction fails. BrowserOS owns profile, focus, mutation, and secret
handling; use its live tool schemas and current page refs.

Sections: [enter the brief](#enter-the-brief),
[connectors](#attach-the-actual-connectors),
[files](#attach-plans-and-longer-bodies),
[sources whole](#attach-the-sources-whole),
[composer diagnosis](#diagnose-a-composer-interaction),
[delivery verification](#verify-delivery-on-every-submission).

## Enter the brief

The composer is a ProseMirror editor in which Enter sends. Never `fill` or
`type` the brief: keystroke fills turn every newline into Enter and submit a
fragment mid-fill, which is what drove agents to put the ask in a file. Enter
the brief with a synthetic paste in page context instead. It keeps paragraphs,
blank lines, and bullet lines exactly, never submits, and turns a literal
`@GitHub` or `@BigQuery` in the text into the connector pill. Verified
2026-09-17 on a 540-word Template A brief with two mentions.

```javascript
// page-context JS (evaluate), TEXT = the full brief as written
const ed = document.querySelector('#prompt-textarea');   // the visible ProseMirror div
ed.focus();
const dt = new DataTransfer(); dt.setData('text/plain', TEXT);
ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
// verify before Send: pills resolved, and the draft equals TEXT with pills read back as @Keyword
const c = ed.cloneNode(true);
c.querySelectorAll('[data-inline-selection-pill]').forEach(p => p.replaceWith('@' + p.getAttribute('data-keyword')));
return JSON.stringify({pills: [...ed.querySelectorAll('[data-inline-selection-pill]')].map(p => p.getAttribute('data-keyword')),
  matches: c.innerText.trim() === TEXT.trim(), userTurns: document.querySelectorAll('[data-message-author-role="user"]').length});
```

Send only when `matches` is true, every required pill is listed, every
required attachment chip is present, and the user-turn count has not changed
since before the paste. Run this check immediately before the click, on
every send path, including after a reload, a clear, or a retry; a reload
keeps the text draft and drops the attachments. A paste that timed out may
have landed: read the editor's text length before repeating it, and if the
brief appears twice, clear the editor and paste once. Click
`button[data-testid="send-button"]` (accessible name `Send prompt`) with a
page-JS `click()`, which works in a background tab, then verify the submitted
turn as described below. If a mention did not resolve into a pill, delete it,
insert `@` with `document.execCommand('insertText', false, '@')`, which opens
the picker, turn on focus emulation for the page (`$browseros`), and pick the
connector with a real click at the item's viewport coordinates (`act`
`click_at`). Without emulation that click does not register in a background
tab, and synthetic DOM clicks on picker items never do. Then paste the rest of
the brief.

## Attach the actual connectors

For data questions the brief carries `@BigQuery`; for GitHub or repository
questions it carries `@GitHub`; both when both kinds of sources are required.
The paste in the section above resolves each into a pill; confirm the pills
in the draft and again on the submitted turn before accepting an answer.
Plain text naming a connector, such as "GitHub connector attached", attaches
nothing.

Name the relevant data scope or repository in the ask. For code review, include
the exact pushed PR URL with the GitHub mention; file dumps and pasted diffs do
not replace repository access. Before accepting the result, inspect visible
connector activity and retrieved source material for successful access to the
specific data or code needed. A connected badge or Pro's claim of access alone
is insufficient.

If a required connector is missing or fails, switch to another suitable Pro
account or stop and tell the user the precise access failure. Reattach and verify
all required mentions after switching. Do not automate authorization or accept
an answer based on guessed data or imagined code.

## Attach plans and longer bodies

Put every plan, export, and evidence body in a file. The brief itself goes
into the composer with the paste method above, paragraphs intact; do not
move the ask into a file and point at it.
Preflight absolute paths, existence, and the maximum of 10 attachments. Do not
omit files to fit that limit.

**Never click ChatGPT's own upload controls.** `Add files and more`, `Add
photos & files`, and any file input open the operating system's file dialog,
whether clicked by ref, by coordinates, or from script. No BrowserOS tool can
see, fill, or close that dialog. It stays open over the user's window, takes
their focus, and waits for a person to cancel it. BrowserOS `upload` sets
files on an `input[type=file]` directly and never needs the dialog. If
`upload` answers `Node is not a file input element`, the ref was a button or
menu item; fix the ref, do not reach for the dialog. If a dialog did open,
name its profile and window in your next update so the user can cancel it, and
carry on through the route below.

Attach through the temporary-input route:

1. Create a temporary visible file input on the selected page and snapshot it.
2. Use BrowserOS `upload` with that exact ref and the absolute file paths.
3. Transfer the selected `File` objects to ChatGPT's hidden `#upload-files`
   input and dispatch `input` and `change` events on the ChatGPT input.
4. Verify every filename appears as a ChatGPT attachment chip and processing
   has finished before Send. Remove the temporary input after transfer.

Stop before submitting if any required chip is missing. A successful upload
acknowledgment does not prove the message contains the intended attachment.
After Send, verify the submitted user turn includes the files and full ask.
An upload input retaining a filename, including `C:\fakepath\...`, is not an
attachment receipt. Inspect the attachment chips on the submitted turn; they
may be siblings of its text node. If deliberately reusing an earlier file,
verify that attachment in the selected thread and its relevance to this ask;
do not describe it as newly attached.
During generation, reject claims based on a file Pro says it could not read.

## Attach the sources whole

The consultation templates require the canonical sources as files, not links
or summaries. The issue, epic, or plan usually links the workbook, spec, or
design record it was written from; that link is the source, and it is
exported whole even when the issue restates it. Build the files before
opening the composer:

- **A Google Sheet**: export every tab with the `gws` sheets tooling into one
  Markdown file, tab by tab, with row numbers kept. The rows the agent thinks
  are relevant are not the export; the whole workbook is.
- **The plan and the design record**: the current file as it sits on disk or
  in the issue, unedited.
- **The user's words**: a small file of his verbatim messages and rulings
  about this work, each dated, gathered from the session and the thread.
- **Raw evidence**: test output, logs, data pulls, and screenshots as the
  files the tools produced.
- **The repo's review policy**, when it has one, for a review brief.

Pack within the 10-attachment limit by concatenating related items into one
file with clear headings (for example the user's words and the issue as filed)
rather than dropping any source. Name each file for what it is. Point Pro at
the PR or branch with `@GitHub` in the brief, and at data with `@BigQuery`;
the paste resolves them into pills, and the words "GitHub connector" attach
nothing. Never pin a commit SHA in the ask.
When continuing a thread, re-attach the sources on every round rather than
telling Pro to scroll up.

## Diagnose a composer interaction

Read the exact schema for the available input tool, including whether it
inserts text or types keystrokes. A tool named `fill` can type character by
character and turn each newline into unmodified Enter. Enter the brief with
the paste method above; a fill acknowledgment and its character count
describe the attempted input, not a verified field value or submission.

Locate the live visible editor. ChatGPT can render a hidden fallback
`textarea[name="prompt-textarea"]` beside the actual
`div#prompt-textarea[contenteditable="true"]` ProseMirror editor. Both may have
the accessible name `Chat with ChatGPT`. Read the visible editor's full text;
the hidden textarea's empty value does not establish an empty composer. If
argument validation failed, fix that call and verify the intended text; do not
continue to Send with an old draft still present.

If a normal background interaction is acknowledged but the UI does not change,
read the live element and verify the postcondition. Foreground focus is never
the fix.
- Some React inputs require the native value setter plus an `input` event.
- Menus open with a dispatched `pointerdown`, not `.click()`.
- A menu opened and closed in a background tab stays half-closed on the page.
  It blocks typing and the @ picker until you turn on focus emulation for the
  page (`$browseros`) or reload it. A reload keeps the text draft and drops
  attachments.
- A modal left open, such as the temporary-chat explainer, holds keyboard
  focus until it is dismissed.

Verify any menu or dialog actually mounted before interacting with it.

## Verify delivery on every submission

Use fresh refs after a rerender and apply the entry file's before/after checks.
Keep the observations separate: intended input, current draft, submitted user
turn, and the response following that turn. Read these through BrowserOS in the
verified page; do not infer one from another.

Submitted text currently lives under `[data-message-author-role="user"]`,
with `data-message-id` identifying the message. Record the prior latest message
before filling, then identify the new message after submission. A scoped full
read of its body must match the intended ask, including its ending. Inspect
`[data-testid="collapsible-user-message-content"]` when present or expand the
message through supported controls; `Show more` is not part of the prompt.
Verify attachments on the containing turn as well as the text. Treat these
selectors as observations to confirm against the live DOM, not permanent API
guarantees.

Whole-page text can include the unsent editor directly after an assistant's
answer. A text match anywhere on the page, the first matching ancestor, or the
last few matches from `main *` cannot establish message authorship or absence.
Use message roles and identity, and inspect the visible composer separately.
If a tool truncates its output, retrieve the saved output or make a scoped
read; do not equate an output limit with a truncated ChatGPT message.

Check immediately after filling for an accidental new user turn. If only a
fragment arrived, or the submitted turn lacks a required attachment or
connector pill, invalidate its answer: click Stop answering, then resend the
whole submission with everything re-attached and re-verified. A follow-up
message carrying the missing files does not repair a review already running
without them. An assistant response or Stop button proves activity, not delivery
of the intended ask. A transport timeout remains an unknown mutation until
readback establishes what happened.
