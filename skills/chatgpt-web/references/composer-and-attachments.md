# ChatGPT Composer, Connectors, and Attachments

Read the relevant section before attaching files or connectors, or when a
composer interaction fails. BrowserOS owns profile, focus, mutation, and secret
handling; use its live tool schemas and current page refs.

## Attach the actual connectors

For data questions, type `@` and select BigQuery from the connector picker.
For GitHub or repository questions, select GitHub. Use both when both kinds of
sources are required. Confirm the actual attached mentions before sending;
plain text naming a connector does not invoke it.

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

Put every plan or multi-paragraph body in a file. Use a short single-paragraph
composer ask that names the attachment; pasted newlines can send prematurely.
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
After Send, verify the submitted user message includes the files and full ask.
During generation, reject claims based on a file Pro says it could not read.

## Diagnose a composer interaction

Read the exact schema for `act`, including its current field names. After a
fill, inspect the composer's actual value before Send. If argument validation
failed, fix that call and verify the intended text; do not continue to Send
with an old draft still present.

If a normal background interaction is acknowledged but the UI does not change,
read the live element and verify the postcondition. Some React inputs require
the native value setter plus an `input` event. Some menus require supported
pointer events before a click. Use the BrowserOS background methods for the
observed control before deciding foreground focus is necessary; verify any menu
or dialog actually mounted before interacting with it.

Use fresh refs after a rerender. Before Send, verify the conversation, selected
configuration, composer text, attachment chips, and actual connector mentions.
After Send, inspect the new user message rather than assuming an acknowledged
click submitted it. A transport timeout is an unknown mutation until readback
establishes what happened.
