---
name: readable-reports
description: "Write or rewrite reports, status updates, morning and weekly reports, audit summaries, delivery reports, decks, sheet notes, and status answers so a smart, busy expert reader can parse them in one pass: every sentence has a subject and a verb, every thing is named in plain words with its code or number after it, every PR, issue, document, or message is a labeled link, every status carries its cause and next step, numbers arrive with their comparison, the answer comes first, and the report never talks about itself. Use when a reader says an artifact is confusing, hard to parse, too dense, jargon-heavy, or a wall of text, when an artifact must be rewritten so it can be read at a glance without being dumbed down, or as the final writing pass of any skill that publishes a report. Not for public-facing voice or AI-tell gating of marketing prose, HTML report styling, spreadsheet layout, prompt or skill authoring, or deciding what the report should conclude."
metadata:
  short-description: "Make reports readable in one pass by a smart, busy expert"
---

# Readable Reports

Use this skill when the work is the words of an artifact a busy expert will
read: a report, a status table, a morning or weekly update, an audit summary,
a delivery report, a deck, a sheet's notes column, or a chat answer that
reports state. The facts stay exactly as rich as they were. What changes is
how much the reader has to reconstruct to understand them.

The complaint this skill exists to end, in the reader's words: "I could parse
it if I had to ... It's just fucking confusing." And its mirror: "It either
treats me like a child or it writes it in a way that requires full
concentration to even figure out what they're saying."

The bar: a smart, engineering-minded executive can read it at a glance and
understand it without dropping everything to focus on every word.

This is a prompt-only skill. It ships doctrine and worked repairs; no scripts.

## When to use

- The user says a report, update, deck, or answer is confusing, dense,
  jargon-heavy, hard to parse, or a wall of text, and wants it readable
  without losing precision.
- A skill that produces a report (morning priorities, weekly ops, audits,
  replay reviews, delivery reports) is about to publish; run this as the
  writing pass on the body before rendering or sharing.
- The user asks for a status, summary, or explanation "in plain English" and
  is an expert who will reject being talked down to.
- A table, status row, or alert reads like the tool that produced it
  (merge states, flag names, job statuses, internal ids) instead of English.

## When not to use

- Public or community copy that needs the house voice and the AI-tell gate:
  use the surface's voice skill and `fc-authored-copy`. This skill may still
  run first for parse cost; the gate owns publication.
- The HTML theme, CSS, or page chrome of a report: the report theme skill.
- Spreadsheet layout, freeze panes, cell formats: `$spreadsheet-formatting`.
  This skill owns the words in a notes cell, not the grid.
- Writing a prompt or a skill: `$prompt-authoring`, `$skill-authoring`.
- Deciding what the report should find or recommend. Resolve the substance
  first; bring the result here.

## The reader

A senior engineer who owns or built the system and has not been inside this
work today. He does not hold yesterday's plan, the agent's session, or the
tool's vocabulary in working memory. He wants the plain sentence first and
the exact term second: "what does that mean in plain English" and then "are
you saying it's a reverse incompatible build?" He will not be told what any
engineer knows, and he will not be made to look up what only the writer
knows. He reads to decide.

Two failures, one cause: the writer chunked the work into private labels
(the stacked PR chain becomes "root" and "children"; GitHub's merge state
becomes "clean") and forgot the reader has not. Over-correcting produces the
other failure: explaining what a pull request is. Never explain the field.
Always name the thing.

## Non-negotiables

- Prose and table cells are sentences with a subject and a verb. Column
  headers, row labels, and source tails are labels, not sentences: write
  "| Person | Where it stands | Next |", never "| Each person owns current
  work. |". An imperative is a complete sentence ("Ship the purchase
  repairs."). No arrow, slash, or "=" where a verb belongs. Name the actor:
  "the player tapped one of the two buttons and the screen recovered", not
  "a manual action was followed by recovery". When a sentence is too long,
  cut a fact; never cut the grammar.
- Do not make it wordier. A cell holds the state, not the history. A grid of
  numbers stays a grid, with units in the header and one sentence above it
  saying what the numbers show. A rewrite that comes out longer than the
  original has almost always added something the reader did not ask for:
  narrated sources, a repeated shape, restated numbers, hedges, or notes
  about what was not checked. Find it and cut it. The exception is a
  fragment that had to become a sentence.
- Name the thing in the reader's words. The failure is the writer's private
  label: a code minted or copied from a tool ("W3", "MW-064", CLEAN,
  BLOCKED), a noun that only makes sense inside the writer's session
  ("root", "children", "the reset", "the stack"), a coined metaphor ("three
  links"), or a phrase lifted from a query column, a JSON field, a log, or
  the writer's own method ("store grants", "client purchase completions",
  "controls", "canonical terminal", "await integration"). Say what a person
  did or saw: "29 people bought through the store and got Plus; the app
  recorded none of them as a finished purchase." Put the code, number, or
  exact term in parentheses after the plain name when someone will search
  for it. The reader's own vocabulary is not the failure: he says paygate,
  offering, checkout conversion, cohort, canonical, attribution, and he is
  not to be told what they mean. The test is ownership, not frequency: does
  this word come from the reader's world or from the writer's process?
- Every PR, issue, commit, document, dashboard, message, or file the text
  mentions is a clickable link labeled with what it is and its number or
  title. Never a bare number the reader has to go find. Never a raw URL as
  the label. Link to what the reader can open from where he reads: the
  GitHub, Slack, or Google URL first; an absolute local path only when no
  URL exists.
- A source is the specific thing: the message, the PR, the query result,
  the row. Link it on the fact it supports, or in a short tail after the
  cell. Never a sentence whose only job is to say a source supports the
  claim, and never a generic pointer repeated on every cell ("Sources:
  Communications evidence · Business metrics"); a collection the reader
  cannot check a claim against is linked once, in the appendix, or not at
  all. He does not care about receipts; he cares whether the sentence is
  true and what to do.
- Anything the report says the reader said, decided, or asked for is his
  words, quoted, with the message linked, or it is cut. "Your later
  assessment credits the partnership" with no quote is invented framing.
- Tool states and system words become sentences about the work as the
  reader would see it. "CLEAN" becomes "can merge now"; "BLOCKED" becomes
  "cannot merge until the base merges"; a flag name becomes what the user
  now sees; a Sentry group id becomes the error it is.
- Every status carries the named subject, what is true now, why (the cause
  or the blocker), and what happens next or who acts. Make the state visible
  without reading the cell: lead with the state and its cause in a few
  words ("Blocked: the two mission-event PRs have not shipped." "Merged,
  not in a store build."), then the sentence with the names and links.
  "Aligned; blocked" gives one of the four. When several items share one
  state and cause, say it once and list the items.
- Say what you know; stop there. Write "unknown" or "not checked" only where
  the reader needs that answer to act: the cause of a blocker, the owner of
  a next step, a number the decision turns on. A fact nobody asked about is
  not announced as missing, and a status row never carries a note about
  what the writer did not check. State findings decisively; qualify once,
  where the qualification changes the decision, not in every sentence. He
  needs useful decisions, not proof.
- The answer comes first. One unhedged sentence on top carries the message.
  Each section's first sentence is its message. A body heading is a short
  message the reader can act on without the body ("Lifecycle is stuck on
  two unshipped PRs"), not a thesis, not a topic label, not a noun stack;
  appendix headings may be plain labels. If there is one caveat, the caveat
  is the answer.
- Numbers arrive with their comparison and their meaning in the same
  sentence: the rate, its raw counts, the baseline, and what it means for
  the decision. Do the division for the reader. Give a percent only when
  the base supports it; "21 to 29" is eight people, not "up 38.1%". Keep
  the precision the decision needs: "66 seconds", not "66.253 seconds".
- One idea per sentence. Bold the one line a skimmer must not miss, if any;
  bolding several lines cancels all of them.
- No repeated shape. Rows do not all open the same way, cells do not all
  close the same way, recommendations are not all "X should Y". Write the
  sentence the fact needs. If you notice you are swapping a name into the
  sentence you just wrote, stop and say it once.
- One voice. Pick "you" or the reader's name for him and keep it; third
  person for everyone else; recommendations as imperatives in a row labeled
  by person.
- The report is about the business, not about itself. The body holds
  everything he would act on or decide from, including the table that says
  which theories are dead and which are alive. The appendix holds only what
  he would use to check a claim: which sources were read, as of when, and
  what each could not show. Render sizes, file hashes, run ids, model
  names, which worker did what, rules applied, and what was suppressed are
  not facts about the business and do not survive the rewrite. No sentence
  describes the report's own behavior. The artifact stands alone: no
  "earlier", "the previous turn", "above", or "below".
- Do not talk down and do not editorialize. Keep real component names and
  real numbers. No definitions of terms the reader uses, no analogies in
  place of mechanisms, no stating the obvious as insight. Report what was
  observed and how often; do not assert the business's intent, scold the
  reader, or dramatize an expected cost.
- One name per thing across the page and across reports. One clock per
  page, the reader's, stated once. Newest first in vertical lists.
- A question to the reader is one plain question with the choices in words
  and what each one changes, answerable from that paragraph alone.
- No em dashes anywhere. No AI tells: the measured AI vocabulary, negative
  parallelism, triads, mirrored contrasts, reveal bridges, recap loops,
  ceremonial closers. Remove a banned word by repairing the sentence, never
  by swapping a synonym. The canonical banned list is one file; point at it,
  do not copy it:
  `/Users/aelaguiz/workspace/psagentspace/skills/fc-authored-copy/references/editorial-judgment.md`.
- Preserve every fact about the business: number, name, date, finding,
  decision, link. A rewrite that drops one to fit is a failure; a rewrite
  that adds one the source does not support is worse.

## The test

Read the sentence once, cold. Can you say who did what to what, what is true
now, why, and what happens next, without looking anywhere else on the page?
If not, one of the mechanisms in `references/mechanisms-and-repairs.md` is
in it. Find which one and repair that. Shortening is not a repair; most
failures in this class are already short.

## Workflow

1. Find the reader's question. What decision or check does this artifact
   serve? Write that question down; the top line must answer it.
2. Collect the facts before the words: the plain name of each thing, its
   code or number, its link, the number and its baseline, the time in the
   reader's clock, and for every status its cause and next step. If writing
   a full sentence exposes a fact you do not have (why is it blocked? who
   owns it? which four PRs?), go get it from the source. If it is not
   there and the reader needs it to act, write that it is unknown; if he
   does not, say what you know and stop.
3. Write the top line: one unhedged sentence that carries the message.
   Then the sections, business outcome before initiative before task,
   each heading a message, each first sentence the point.
4. Write status as tables when there are many subjects, with every cell a
   full sentence: subject, state, cause, next or owner. Write findings and
   explanations as short prose with the number beside its comparison.
5. Move method, coverage, run details, and verification to an appendix or a
   separate working file.
6. Run the test on every sentence and cell. Classify each failure by
   mechanism and repair it. Then sweep: em dashes, bare codes and numbers,
   arrows and slashes, unlinked references, sentences that only cite a
   source, column headers written as sentences, rows that share one shape,
   unlabeled times, drifting names, AI tells, sentences about the report
   itself. If the rewrite is longer than the original, find what you added
   that the reader did not need and cut it.
7. Read the whole thing once more as the reader: at reading speed, not study
   speed. Where you slowed down, repair again.

## Output expectations

- Author: the finished artifact, in the requested format, meeting every
  non-negotiable, with method in an appendix.
- Rewrite: the rewritten artifact with every business fact preserved, plus
  a short list (outside the artifact) of facts the source needed and did
  not contain. Only the ones the reader needs to act appear in the text,
  as "unknown". Do not fill gaps by guessing.
- Audit: findings first, each with the exact passage, the mechanism, what the
  reader would have to know or guess, and the repaired sentence when the
  facts allow one.

## Reference map

- `references/mechanisms-and-repairs.md`: the mechanisms that raise parse
  cost, why each costs, and before/after repairs drawn from real reports.
  Read it when a passage fails the test and the fix is not obvious, or
  before auditing.
- `references/reader-and-shapes.md`: the reader's own words on both failure
  edges, the calibration between them, and the page shapes he has accepted
  for reports, status tables, numbers, decisions, and appendices. Read it
  before authoring a report from scratch or when unsure how much to explain.
