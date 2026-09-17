# ChatGPT Composer, Connectors, and Attachments

Read the relevant section before attaching files or connectors, or when a
composer interaction fails. BrowserOS owns profile, focus, mutation, and secret
handling; use its live tool schemas and current page refs.

Sections: [connectors](#attach-the-actual-connectors),
[files](#attach-plans-and-longer-bodies),
[sources whole](#attach-the-sources-whole),
[composer diagnosis](#diagnose-a-composer-interaction),
[delivery verification](#verify-delivery-on-every-submission).

## Attach the actual connectors

For data questions, type `@` and select BigQuery from the connector picker.
For GitHub or repository questions, select GitHub. Use both when both kinds of
sources are required. Confirm the actual attached mentions before sending;
plain text naming a connector does not invoke it. Because the brief is
inserted as one paragraph, place the mention in steps: insert the text up to
the `@GitHub` or `@BigQuery`, type `@` and pick the connector from the picker
so the pill lands in place, then insert the rest. A pasted `@GitHub` string,
including one typed because the picker did not mount, is not a chip.

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

Put every plan, export, and evidence body in a file. The ask itself is typed
into the composer as one paragraph, however long, because pasted newlines can
send prematurely; do not move the ask into a file and point at it.
Preflight absolute paths, existence, and the maximum of 10 attachments. Do not
omit files to fit that limit.

Use the upload path supported by the live ChatGPT page and BrowserOS schema.
The established temporary-input route is:

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
the PR or branch by typing `@GitHub` and selecting it from the picker, and at
data by typing `@BigQuery` the same way; the words "GitHub connector" attach
nothing. Never pin a commit SHA in the ask.
When continuing a thread, re-attach the sources on every round rather than
telling Pro to scroll up.

## Diagnose a composer interaction

Read the exact schema for the available input tool, including whether it
inserts text or types keystrokes. A tool named `fill` can type character by
character and turn each newline into unmodified Enter. Use the
one-paragraph composer ask above; a fill acknowledgment and its character
count describe the attempted input, not a verified field value or submission.

Locate the live visible editor. ChatGPT can render a hidden fallback
`textarea[name="prompt-textarea"]` beside the actual
`div#prompt-textarea[contenteditable="true"]` ProseMirror editor. Both may have
the accessible name `Chat with ChatGPT`. Read the visible editor's full text;
the hidden textarea's empty value does not establish an empty composer. If
argument validation failed, fix that call and verify the intended text; do not
continue to Send with an old draft still present.

If a normal background interaction is acknowledged but the UI does not change,
read the live element and verify the postcondition. Some React inputs require
the native value setter plus an `input` event. Some menus require supported
pointer events before a click. Use the BrowserOS background methods for the
observed control before deciding foreground focus is necessary; verify any menu
or dialog actually mounted before interacting with it.

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
fragment arrived, invalidate its answer and repair that submission before
continuing. An assistant response or Stop button proves activity, not delivery
of the intended ask. A transport timeout remains an unknown mutation until
readback establishes what happened.
