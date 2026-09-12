# ChatGPT received a fragment while the agent treated the draft as delivered

This report preserves the investigation and the premature submission-only
changes made during it. The user subsequently authorized a combined plan,
skill revision, and publication; that work is tracked in the
[improvement plan](chatgpt-web-consultation-improvement-plan-2026-09-11.md).

**The home-server incident is a confirmed partial submission followed by incorrect delivery verification.** The agent gave BrowserOS an 838-character, four-paragraph prompt. ChatGPT received its first 64-character sentence. The fuller text remained in the visible composer, and whole-page extraction included that draft after Pro's response. The agent treated the extracted draft as part of the delivered conversation and reported that the complete pushback had landed.

The input implementation explains the trigger: the inspected BrowserOS `fill` path types characters, and its newline branch emits an ordinary Enter keypress. The agent did not separately press Enter or click Send before the fragment appeared. This is a tool-semantics problem combined with an agent verification failure. Better wording for the consultation would not repair delivery.

The investigation used the exact home Codex trace, a read-only inspection of the existing ChatGPT page through home's BrowserOS MCP, BrowserOS source in `~/workspace/BrowserOS`, and a mock event-capture execution of the source's typing function. No prompt was sent during this audit and no browser focus or page state was changed.

## What actually happened

The incident is in Codex session `01a0906a-c125-7c43-b500-e38ed4dfda31` on home. All JSONL anchors below refer to:

```text
/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T07-21-50-01a0906a-c125-7c43-b500-e38ed4dfda31.jsonl
```

Times below are September 11, 2026, America/Chicago (CDT). The UTC date becomes September 12 at 7 p.m. CDT.

| Time | Direct evidence | Consequence |
| --- | --- | --- |
| 7:09:55 p.m. | Line 10091 calls `fill({page:5, element:10, text:prompt, clear:true})`. The prompt contains six newline characters separating four paragraphs. | The agent sends a multiline body through a keyboard-based fill. |
| Immediately afterward | Line 10094 acknowledges 838 typed characters. Lines 10098–10108 read the page and saved output. Its final conversation section says `You said:` followed by only the first sentence. The full draft appears later, after `ChatGPT said: Pro thinking`. | There is already enough evidence to question whether the whole prompt arrived. No separate Send call has occurred. |
| 7:10:24 p.m. | Line 10113 claims the multiline prompt submitted during filling and that the submitted message is exactly the drafted pushback. | It notices automatic submission but does not check the submitted body. |
| 7:11–7:12 p.m. | Line 10138 contains Pro's answer ending “What is your objection to the premise?” followed by the unsent full draft. Line 10151 reports that the pushback landed and Pro conceded. | The parent interprets an answer to the fragment as an answer to the full objection. |
| 7:21–7:24 p.m. | After two user corrections, the agent inspects the DOM, then finally clicks Send at line 10254. | The fuller text becomes a separate submitted user message. |

The two submitted messages are both still present in the live DOM. They disprove the agent's later claim that nothing had been sent:

| Message | Actual body | Identity |
| --- | --- | --- |
| Accidental fragment | `I want to challenge the premise of the proposed next experiment.` — **64 characters** | `1d5529d8-a920-401d-89dc-4fa109ef6e21` |
| Later manual Send | The full challenge, with the six newline characters removed — **832 characters** | `0eb39dd1-a028-4aee-9c58-79d1a680f63d` |

The repaired message matches the intended 838-character prompt after removing line breaks. This comparison establishes the recovery's text coverage, not preservation of paragraph formatting. It is the original challenge prompt; the later seven-question consultation proposed in the agent's apology is not what this recovered message contains.

The [branched CFR conversation](https://chatgpt.com/g/g-p-6aa0dafcdd388191a537f6f43978f6a6-cfr/c/6aa48bdf-ae94-83ea-aaa3-6f9f54867816) was verified on home as BrowserOS profile `pro2` (`Profile 2`), window `1442306244`, native tab `1442306268`, MCP page `5`. The window and page were already active and visible. Those IDs are investigation receipts, not reusable handles for future work.

## Why filling the field sent a fragment

Home's live `fill` tool describes character-by-character typing. The inspected implementation calls `keyboard.typeText` after focusing and clearing the field. It does not set the complete string atomically. Its result's character count comes from the argument length; it does not compare the final editor value with that argument. [BrowserOS input tool](https://github.com/browseros-ai/BrowserOS/blob/fd53dc3a46d22d4b8a822aacc24945245629c98e/packages/browseros-agent/apps/server/src/tools/input.ts#L188), [fill implementation](https://github.com/browseros-ai/BrowserOS/blob/fd53dc3a46d22d4b8a822aacc24945245629c98e/packages/browseros-agent/apps/server/src/browser/browser.ts#L1129).

For every `\n`, the typing function emits Enter key-down, a carriage-return character event, and Enter key-up, without a Shift modifier. This allows an application's Enter-to-submit behavior to run while a fill is still in progress. [BrowserOS keyboard implementation](https://github.com/browseros-ai/BrowserOS/blob/fd53dc3a46d22d4b8a822aacc24945245629c98e/packages/browseros-agent/apps/server/src/browser/keyboard.ts#L140).

I executed that actual source function with a mock `Input.dispatchKeyEvent`, without connecting it to a browser. For input `alpha\n\nbeta`, it emitted two unmodified Enter key-down events and zero Shift+Enter events. That verifies the source behavior independently of its comments or tool description.

The source checkout is commit `fd53dc3a46d22d4b8a822aacc24945245629c98e`; the three inspected source files have no local changes. Home's installed browser package reports `146.0.7821.31`, and BrowserOS Local State records server version `0.0.79`. The running server executable is `/usr/lib/browseros/BrowserOSServer/default/resources/bin/browseros_server`.

**Confidence boundary:** the trace proves a fragment appeared during the fill, and the source plus live tool contract explain how that happens. This audit did not establish a binary-to-source build identity or record the production keystroke stream. It also did not reconstruct the precise React event ordering that left the first sentence duplicated in the draft. No live failure was deliberately reproduced in the user's conversation.

The practical correction does not depend on that remaining timing detail: do not route paragraph separators through a fill that treats them as Send. Use the existing file-plus-single-paragraph approach, inspect the complete draft, and check for accidental submission immediately after filling.

## The DOM made three different states look alike

### The hidden textarea is not the live editor

The inspected page has both of these elements:

```html
<textarea name="prompt-textarea" aria-label="Chat with ChatGPT"
          style="display: none;"></textarea>

<div id="prompt-textarea" class="ProseMirror" contenteditable="true"
     role="textbox" aria-label="Chat with ChatGPT">...</div>
```

At trace line 10220, the textarea is empty while the visible contenteditable contains the full draft. An agent checking only `textarea.value` can therefore report an empty composer when the actual editor still contains unsent text. Both controls sharing an accessible name makes a name-only lookup insufficient.

This was directly observed again during the audit: the textarea remains hidden and the visible editor is a ProseMirror `DIV`. Both are now empty after the actual Send.

### Whole-page text includes the draft after the answer

The historical readback at line 10138 is effectively:

```text
You said:
I want to challenge the premise of the proposed next experiment.

ChatGPT said:
[Answer to that sentence]
What is your objection to the premise?

I want to challenge the premise of the proposed next experiment.We are not
starting from an unvalidated learner. ... [the unsent editor continues]
```

The last text is editor content, not another submitted message and not part of Pro's answer. Searching for a phrase anywhere in the document loses that distinction. A response being present, a Stop control, or a successful fill acknowledgment cannot restore it.

The 5,000-character tool-output cap is a separate issue. It truncates the returned preview and provides a saved file containing the fuller extraction; it does not establish that ChatGPT truncated a message. In this incident, the agent read the saved file's tail and still misinterpreted its provenance. Simply increasing the preview limit would not fix that error.

### A broad DOM search produced a false correction

At line 10224, the agent searches `main *` for text beginning with the challenge or response, then returns only the last ten matching elements. Nested composer containers produce many matching descendants. The resulting sample at line 10227 consists of composer nodes with no message role.

That query cannot prove that no submitted challenge exists elsewhere in the conversation. Nevertheless, line 10232 claims “The prompt was never sent” and says Pro answered an earlier prompt. The actual state is more specific: **the first sentence was submitted, its answer was real, and the rest of the intended message had not been delivered.**

Submitted user bodies instead appear under `[data-message-author-role="user"]` with a `data-message-id`. The latest full user body uses `[data-testid="collapsible-user-message-content"]` inside that message. The surrounding turn contains attachment controls, which need not be descendants of the inner text node. These are current DOM observations, not a promise that ChatGPT will keep those selectors indefinitely.

## Attachment state also needs a submitted-turn check

The agent saw `C:\fakepath\HU_SNG_DECONFOUNDING_WORKING_STATE.md` in the file input and initially described the file as still attached. That proves selection in an HTML upload input. It does not prove that the next message carries an attachment.

During this audit, the native upload input still retained a 27,672-byte file while the two challenge-message turns had no attachment controls. Earlier turns did contain working-state attachments, including a filename with a `(1)` suffix. Reusing a verified earlier attachment can be intentional, but it is different from attaching the current file to the new turn. Filename presence alone also does not prove that an earlier upload contains later edits to the working document.

The recovery's statement that a prior attachment remains in context is therefore weaker than proof of a newly attached, current document. The mandatory delivery check must cover both the intended text and where the required files actually arrived.

## The check required on every send

The invariant is simple: **the submitted turn must contain the intended input, and the answer must belong to that turn.** This is a correctness check on delivery, not a constraint on Pro's reasoning or answer format.

1. **Before filling, identify the conversation and its latest user message.** Keep that identity so an old message cannot be mistaken for the new submission. Use the live profile/window/page mapping.
2. **After filling, compare the entire visible editor with the intended text.** Inspect its ending as well as its beginning, required attachment chips, and actual connector mentions. Check whether filling itself created a new user turn. A fragment already sent is an invalid consultation to repair.
3. **After one explicit Send, find the new submitted user turn.** Read its complete body, including collapsed content, and check the attachment controls on that turn. Compare it with the intended input; a prefix match is insufficient.
4. **Check the visible editor and associate the answer.** Confirm the draft cleared and that the response follows the verified new user message. An unrelated or fragment-based response cannot support the full request. If state is uncertain, inspect it before another Send.

For larger prompts, continue to put the complete consultation in an attachment and use a short, single-paragraph composer message. This avoids the demonstrated newline hazard without restricting the substance of the consultation. Do not replace paragraph breaks with a lossy truncation of the question.

A future BrowserOS improvement could offer a separate text-insertion operation that does not translate newlines into submission keys, and return observed field state instead of only the requested character count. That would reduce this input hazard. It would still not replace verification of ChatGPT's submitted turn, attachments, and response association.

## Existing guidance, changes made, and remaining limits

The pre-audit [ChatGPT Web entry](../skills/chatgpt-web/SKILL.md) already warned about newlines, required a file for multi-paragraph bodies, and required submitted-message readback. [BrowserOS](../skills/browseros/SKILL.md) already required field-value and outcome checks. The earlier SNG trace records successful loading of those entries. Lines 9913–9916 additionally show a complete read of the composer-and-attachments reference, including its newline warning, about 55 minutes before the failed fill. This is not an entirely missing rule. The mechanical failure and the agent's reasoning show why “verify it sent” needed a more precise definition.

This change strengthens three existing ChatGPT Web package files:

| File | Change |
| --- | --- |
| `skills/chatgpt-web/SKILL.md` | Makes the before/after check explicit at the top, checks whether fill itself submitted, and requires matching the complete new user turn before interpreting its answer. |
| `skills/chatgpt-web/references/composer-and-attachments.md` | Explains the live editor versus hidden fallback, message identity, collapsed text, draft contamination in page reads, and attachment placement. |
| `skills/chatgpt-web/agents/openai.yaml` | Carries the same delivery requirement in the skill's default prompt. |

The three reviewed files were installed into `~/.agents/skills/chatgpt-web` both locally and on home using the existing `make agents_install_files` target. Before replacement, all six installed files matched the reviewed repository baseline. Previous versions are backed up at `/Users/aelaguiz/.agents/skill-backups/arch_skill.GXdjiV` and `/home/aelaguiz/.agents/skill-backups/arch_skill.uAXr89`. No other skill package was installed. The repository changes have not been committed or pushed.

The BrowserOS executable was not changed, and the live SNG agent was not interrupted. An already-running agent must read the updated skill to receive the new instructions; changing files does not rewrite its existing context.

The [earlier prompt-quality analysis](pro-consultation-prompt-failures-2026-09-11.md) addresses a different failure: constraining the expert's judgment before sending. Both protections are needed. A well-authored draft that never reaches Pro does not constitute a consultation; a perfectly delivered but overconstrained prompt can still defeat its purpose.

This audit establishes one exact partial-send incident with its recovery. Bounded seven-day home history searches and the retained September 9 BrowserOS survey also show related composer uncertainty: timeout despite successful insertion, empty editors after failed typing, and upload acknowledgments without attachment proof. Those are related risks, not additional confirmed instances of this exact newline failure. No fleet-wide frequency is claimed.

## Evidence retained and validation

Temporary raw receipts are under `/tmp/chatgpt-submission-audit-20260911`. This document retains the facts needed to understand the incident even if those temporary files are later removed.

| Evidence | Location or anchor |
| --- | --- |
| Actual fill, partial user message, and false success claim | Home rollout lines 10091, 10094, 10108, 10113, 10138, 10151 |
| Hidden fallback, visible draft, and false absence claim | Home rollout lines 10217–10232 |
| Explicit Send and submitted-body recovery | Home rollout lines 10254, 10269–10286; message IDs above |
| Live DOM capture and exact intended-text comparison | `home-page5-dom-value.json`, `intended-prompt.txt`, and `home-sng-9450-10550.jsonl` in the temporary receipt directory |
| Input mechanism | Pinned BrowserOS source links above; actual `typeText` function executed against a mock event sink |

Verification includes the original prompt's 838-character length and six newlines, the 64-character fragment, the recovered body's exact match after line-break removal, the visible-versus-hidden editor distinction, and source behavior for newline events. The required `npx skills check` completed with exit code 0. It checks installed upstream updates, not the semantic quality of this edit, and reported unrelated upstream-path warnings for four Impeccable skills while skipping deletion. The edited entry, reference, and runtime metadata also received direct review; local links and `git diff --check` passed. SHA-256 comparisons confirmed all three installed files match the edited repository files on both hosts. No test sends were made to Pro.
