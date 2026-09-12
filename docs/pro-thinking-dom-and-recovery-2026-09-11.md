# Observe Pro's actual progress and recover without cancelling it

Pro consultations should run to a usable answer while the user is away. Long
thinking is expected; recovery should repair a stale page or failed request
without cutting off research or replacing the original question with an order
to finish immediately.

## Scope and authoring plan

This revision applies `skill-authoring` and `prompt-authoring` to three requests:

1. A Pro review is still researching after roughly 30 minutes. Observe its
   actual progress and let it continue without an agent-defined deadline.
2. A page has shown no substantive progress for at least 15 minutes across
   scheduled observations. Reload once, inspect the recovered state, and
   continue the consultation autonomously.
3. A reload leaves a failed/incomplete request. Resubmit the full original ask,
   with its evidence and connectors; use a branch if the same conversation
   cannot recover. Verify delivery and the resulting answer.

The owning surface is `skills/chatgpt-web/`: waiting/recovery in the entry
file, concrete DOM observations in a directly linked reference, and invocation
metadata aligned with the entry. BrowserOS retains ownership of browser
mechanics and profile/focus protection. Its generic unknown-mutation rules
still apply to external writes. No polling controller, new browser tool, or
external consultation is needed to author this change.

The implementation sequence is evidence collection, a focused prose revision,
live read-only validation of the DOM example plus recorded-case walkthroughs,
package checks, and the previously requested `amir-publish` distribution.

## Evidence sources

The primary incident is home Codex session
`01a09327-b4c6-7ca1-92e6-e19977102ef4`, retrieved by exact ID from the read-only
Codex state index, then inspected in its rollout:

`/home/aelaguiz/.codex/sessions/2026/09/11/rollout-2026-09-11T20-07-28-01a09327-b4c6-7ca1-92e6-e19977102ef4.jsonl`

Live inspection used the existing BrowserOS MCP server on home, with page 2,
native tab 1442306247, window 1442306244, and browser context `Profile 2` mapped
to safe profile label `pro2`. The conversation is PS Architecture's
`Inspect RustAI Brief`, ID `6aa4a865-5b80-83ea-b490-8fe4a5293f92`.
These are evidence identities, not handles to reuse without live verification.

Temporary raw observations and the retrieved rollout are retained locally in
`/tmp/pro-progress-dom-audit/`. No authentication/session payloads were collected.

## What the recorded cancellation established

All timestamps in this table are September 11, 2026, Central time.

| Time | Direct observation | Implication |
| --- | --- | --- |
| 8:13:54 p.m. | Rollout line 257 contains the current ChatGPT Web entry, including the prohibition on cancelling because of elapsed time. | The installed update was available and loaded. |
| 8:18:06 p.m. | A context compaction occurs at line 448. | Retention of every instruction after compaction is not established. |
| 8:18:29 p.m. | Send click at line 488; the following DOM read reports one user message, the brief, and generation. | The first consultation began here. |
| 8:32:54 p.m. | Extracted `main` content is 2,142 characters, with a new substantive interim finding and additional research. | Pro was making visible progress. |
| 8:35:02 p.m. | Content reaches 2,211 characters, adding a review of abstraction, loader policy, and showdown dispatch. | This later progress resets an inactivity observation window. |
| 8:39:18 p.m. | The last pre-cancellation read still shows Stop answering and the same visible progress text. | About 4 minutes 16 seconds of unchanged visible text does not establish a stalled backend. |
| 8:39:27 p.m. | The parent labels the run stuck and clicks the Stop answering ref at line 724. | It deliberately interrupts after 20 minutes 58 seconds total. |
| 8:39:37 p.m. | Its replacement begins “Turn the completed repository investigation into the deliverable now. Do not perform more research or narrate progress.” | The recovery changes the expert's working instructions without evidence that research is complete. |
| 8:42:17–32 p.m. | Following the user's reload request, navigation reloads the page; Send becomes enabled and the replacement request is sent. | Reload recovers the composer without needing another Stop click. |
| 8:49:05–20 p.m. | The parent clicks Stop again, then reloads; the recovered page contains a long architecture answer and a Stopped thinking disclosure. | Reload changes what is visible. Because Stop preceded it, this is not a controlled demonstration of reload-only recovery or proof that no research was lost. |

The parent later paraphrased “can take 30 minutes” as “allow Pro up to 30
minutes.” The revised wording must explicitly reject that upper-bound reading.

## What the live DOM actually looks like

The September 11 evening observations used page-targeted BrowserOS reads and
opened the current response's thinking disclosure. They did not submit a new
prompt, stop or reload an active generation, branch a chat, or take browser
foreground focus deliberately. The chat was still being operated by its own
agent; this investigation's permission was limited to inspecting its UI.

### Conversation turns are larger than assistant message nodes

The page had **zero `article` elements**. Its turns were `section` elements:

```html
<section data-testid="conversation-turn-8"
         data-turn="assistant"
         data-turn-id="91ed8509-8596-4f1d-9b2f-1e6542b18f80">
  <!-- visible response/thinking UI -->
</section>
```

At 9:02:55 p.m. that section's rendered text was only `Pro thinking`, with no
`[data-message-author-role="assistant"]` descendant yet. The preceding full
user message was `b3ea4de0-f239-48c3-89f9-16c26b760e6e`. An earlier completed
answer did have an assistant-message node and approximately 50,000 characters.

Looking only for the last assistant-message node would therefore retrieve the
old answer. Looking only for `article` would retrieve nothing. The current
user message and its following outer response turn are the necessary anchor.

At 9:19 p.m. the owner had sent another request, and the page had unmounted
the inspected user message and intervening turns. The mounted sequence included
turn 1 followed immediately by turn 8, then newer turns. An initial example
that re-paired a user with the next mounted response incorrectly associated the
original architecture question with the later issue-creation answer. This live
validation failure changed the implementation: record the user/response pair
when submission is verified, then read by the recorded outer response ID.
Do not reconstruct historical associations from DOM adjacency after virtualization.

The final example correctly retrieved the recorded completed response even
when its user node was unmounted, flagged that later user work existed, and
excluded that newer request's Activity text. For the older unmounted response
and an absent ID it returned an observation gap instead of another answer.
Global Stop was present for the newer request while the recorded answer was
already complete, directly demonstrating why that control needs request context.

### The Activity panel is outside `main`

Clicking the current turn's `Pro thinking` disclosure through a fresh
BrowserOS ref opened the visible Activity panel. Its outer selector was:

```css
section[aria-label="Reasoning details"][data-testid="screen-threadFlyOut"]
```

Its header was `[data-testid="bar-search-sources-header"]`, and the actual
activity body was its `[slot="content"]` descendant. The panel was not inside
`main`; `get_page_content(selector="main")` alone missed it.

The activity body included the heading `Preparing the implementation plan`,
a GitHub icon at `/images/ecosystem/apps/github/icon.png`, a prose progress
summary, and further displayed detail. The summary was rendered in `.markdown`
content with paragraph `data-start`/`data-end` attributes. These attributes,
generated CSS classes, and icons are implementation observations, not stable
progress APIs or proof that a connector succeeded.

### The timer moves even when the activity does not

| Observation, Central time | Activity header | Activity body | Current response |
| --- | --- | --- | --- |
| 9:04:14 p.m. | `Activity · 9m 51s` | 3,262 characters | `Pro thinking` |
| 9:06:59 p.m. | `Activity · 12m 36s` | The identical full 3,262-character body | `Pro thinking`; no answer-message node |
| 9:09:36 p.m. | `Activity · 15m 13s` | Still the identical body | Still `Pro thinking` |
| 9:12:47 p.m. | Completion transition | The Activity body has emptied | The same response turn now has a 3,480-character outer text and `Worked for 16m 37s` |

The comparison excluded the header and compared the complete body text, not
just its length. Thus a clock tick, shimmering CSS, spinner animation, or
generic `Pro thinking` label is not substantive progress. New/revised activity
entries, changed summaries, new results, and growing/revised answer text are.
An unchanged observation remains uncertainty, not proof of backend death.

The directly observed unchanged-content interval was **5 minutes 22 seconds**
(9:04:14–9:09:36); the answer was observed **8 minutes 33 seconds** after the
first body capture. It would overstate this sampling evidence to call the whole
eight-minute interval proven inactivity. The owner's rollout after 9:06 p.m.
contains no Stop/reload before this completion, only later answer extraction.

Opening the completed turn's `Worked for 16m 37s` disclosure exposed additional
research history inline. Outer turn text grew from 3,480 to 4,789 characters;
the actual assistant answer was 3,451 characters. This was disclosure expansion,
not additional model progress. The still-open Activity panel's body remained
empty. Completion can change which UI contains the trace history.

### Controls are evidence about their own state

The live composer used `button[data-testid="stop-button"]` with
`aria-label="Stop answering"`; enabled state required checking both `disabled`
and `aria-disabled`. An older answer simultaneously exposed a `Stopped
thinking` disclosure. Neither the older label nor a global text search should
decide the current request's state.

A Send button becoming available after recovery shows that input is possible.
It does not establish which response completed, whether its full input arrived,
or whether external connector writes happened. Inspect the anchored response
and relevant external results before repeating an instruction with side effects.

The completed response's `More actions` menu exposed an enabled `Open new
branch` item. The investigation inspected the menu but did not execute a branch.
The menu, completed thinking disclosure, and Activity panel opened for inspection
were closed afterward. Final inventory still had the original seven pages;
page 2 retained the same window, URL, and active/non-hidden state.

## Policy derived from the evidence and the user's instruction

The user's timing policy is roughly 30 minutes as a normal expectation, no
completion deadline, observations every 3–5 minutes, and one reload after at
least 15 minutes without substantive progress across multiple observations.
Opening a disclosure, remounting a turn, or losing the page does not manufacture
progress or establish inactivity; recover the observation first.

After reloading: accept a complete grounded answer, wait if progress resumes,
or resubmit the original complete request if the response is failed/incomplete
and still not progressing. If necessary, branch from the last useful context
and continue in the verified destination. Stop answering is not a recovery
operation. Routine stalls do not require the user to return and rescue the
session. Actual unavailable authentication or exhausted required accounts remain
real constraints; they do not permit guessed sources or a substitute model.

The generic shared process-monitoring requirement for deadlines and stall
actions does not define a timeout for this browser consultation. That boundary
belongs beside ChatGPT's waiting instructions.

[OpenAI's troubleshooting article](https://help.openai.com/en/articles/7996703-troubleshooting-chatgpt-error-messages)
also documents refreshing and restarting a conversation for stalled UI. Its
generic advice includes a short wait and Stop/Regenerate. That is not the
user's selected policy for these long Pro consultations and is not copied
into this skill. The article does not document the DOM selectors or guarantee
that reload preserves/completes a particular server-side generation.

## Validation record

The ChatGPT Web entry now places patient waiting and the no-Stop rule near the
top, removes cancellation as a partial-submission repair, and replaces the
absolute no-retry-after-submission rule with deliberate recovery of a failed
response. It also distinguishes owned-process deadlines from browser
consultations and permits a recovery branch without adding polling tabs.
The new bundled reference owns DOM examples and detailed recovery; invocation
metadata and the README describe the same behavior.

The DOM example was extracted from the reference and executed through
BrowserOS against real conversation states. An earlier read was observed during
generation; the final example retrieved the recorded completed response with
its exact answer ID and all 3,451 answer characters, even after virtualization.
It excludes the Activity timer, reports separate answer messages and later user
work, and returns an observation gap for missing response IDs. The example was
revised after its first historical-association check failed, as described above.

Recorded-state walkthroughs cover the first premature cancellation, timer-only
changes, a quiet trace followed by completion, an old Stopped thinking label,
partial-input repair, a disabled composer after reload, and a verified branch
menu. Branch creation, resubmission, and reload-only recovery were not executed
as experiments on the user's active task. Those remain instructed recovery
operations, not claims of end-to-end runtime validation.

`npx skills check` completed successfully. It reported existing upstream-path
warnings for the Impeccable skills `audit`, `critique`, `frontend-design`, and
`teach-impeccable` and skipped deletion in noninteractive mode. That command
checks installed-source updates, not the quality of this prose. YAML and local
reference-path checks and `git diff --check` provide the package checks; no
tests assert exact doctrine wording. The system Python lacked PyYAML, so YAML
validation used `uv run --no-project --with pyyaml` without changing repo
dependencies. The structural graph returned no nodes for this Markdown entry;
reference and consistency inspection used scoped repository reads.

Final measurements use character count divided by four as an explicitly
approximate token estimate: the entry is 226 body lines/about 3,470 tokens; the
generation reference is 190 lines/about 2,822 tokens. BrowserOS and
prompt-authoring entry bodies add about 2,084 and 2,842 tokens, respectively,
before their applicable references and the shared policy. These are separate
bounded reads, not one combined output. The 668-character description remains
within the metadata limit. The evidence report is not a runtime dependency.

Distribution uses the requested `amir-publish` workflow with `NO_HERMES=1`,
preserving the user's instruction that Hermes is not used. No Hermes-specific
cleanup or unrelated skill repair is part of this revision.

### Publication results

Implementation commit `edf8d75` was pushed to `origin/main`. Standard install
and `make verify_install NO_HERMES=1` succeeded on the local M5 and every
reachable configured remote:

| Machine | Install and verification |
| --- | --- |
| Local `Amir-M5` (`amir-m5` SSH target skipped) | Passed |
| `amirs-m3-max-new` | Passed |
| `amir-m3-36gb` | Passed |
| `agents@amirs-mac-studio` | Passed |
| `home` | Passed |

Each machine's entry, generation reference, and invocation metadata were also
compared with the published source in the agents/Codex, Claude, and Gemini
installations: nine files per machine matched. Gemini's documented frontmatter
removal was accounted for. These checks verify installed content; they cannot
force an already-running agent to reread instructions after publication.
