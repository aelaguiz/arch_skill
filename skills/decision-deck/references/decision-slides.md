# Decision Slides

Read this when writing or fixing a round's spec. The spec keys themselves are
in `python3 <this skill>/scripts/decision_deck.py --help`; this file is about
choosing what goes in them.

## Contents

- Start from what the decision turns on
- Sizing each kind of evidence
- Options
- Writing it so it reads cold
- Worked example: the bakery round

## Start from what the decision turns on

Before writing a slide, name the one thing the owner's answer depends on. That
picks the evidence kind, and the slide shows that thing and nothing that only
explains how you got there.

| The answer depends on | Evidence kind | What goes in it |
| --- | --- | --- |
| how something looks | `images` | the region that changes, near full size |
| exact wording | `diff` | the old and new text, and the rule as it will read |
| a number that differs between options | `chart` | one bar per option, the recommended one emphasised |
| several attributes per option | `table` | one row per option, one column per attribute |

If two of these seem needed, there are probably two decisions; give each its
own slide. A chart or table goes on a decision slide only when it is the thing
decided or the proof of the recommendation. How you checked the work, review
findings and history go in the chat message or a linked file.

## Sizing each kind of evidence

**Images.** Show a crop of the region that changes, at close to the size the
owner will meet it, never a shrunken full page where the change is a few
pixels. Show a whole screen only to say where the detail sits, as a second
view. Pictures common to every option go in `shared`; screenshots to compare
against that are not options go in `references`. For a proposed change against
what exists today, put the proposal first as the option and today's version
after it, as a reference titled as the current version, for comparison only.
Words and numbers are slide text, never painted into a picture.

**Diff.** Paste the text as it is written (Markdown included) into `before` and
`after`, keeping only the paragraphs that change, and put the whole rule as it
will read in `rule_now`. The context line recaps what the change does in plain
words; the checker refuses a diff without one (`NORECAP`). More than eight
changed paragraphs is too many to judge on one slide (`TOOBIG`): when the same
change repeats across many places, ask it once as a rule with two or three
examples and a count, and the checker refuses the same change shown twice
(`REPEAT`).

**Chart.** One bar per option or outcome, with a unit, the recommended bar
emphasised, and a `source` line saying where the numbers come from. Use a
chart whenever the owner compares numbers; a table of numbers makes them do
the comparison themselves.

**Table.** One row per option, in the same order as the options, recommended
first; one column per attribute the decision weighs. Keep cells short so the
table stays a table on a phone.

## Options

Give two to four options, recommended first, each labelled the way the owner
would say the answer ("Use the new wording", not "Approve D2"). For a text
approval, add a "Needs change" option with `ask_note` so picking it asks for
the change. A question with several parts gives each part its own decision, or
lists the combinations as the options; never leave a multi-part question to
the comment box.

## Writing it so it reads cold

The owner may open the deck hours later, on a phone, about work they did not
watch. Each slide must stand on its own.

- **Words the owner already knows.** No label you coined during the work, no
  ticket numbers, commit hashes or file paths as the explanation. A technical
  term appears only with its plain meaning. An earlier decision is described by
  what it decided ("the menu has said News since the last round"), never by its
  id.
- **Each fact once.** The title is the question; the callout is only the why;
  captions never repeat option labels; there is no agenda, progress count or
  footer text.
- **Short question.** A question up to 62 characters is the slide title; a
  longer one moves under the evidence, so shorten it when you can.
- **Plain text outside a diff.** Markdown shows as typed everywhere except a
  diff's `before`, `after` and `rule_now` (the checker's `MARKUP`).

The `text` subcommand prints every word a slide shows, which is what the cold
reader in step 3 of the round reads.

## Worked example: the bakery round

`examples/bakery-site/spec.json` asks a bakery owner four things before a
website relaunch, one per evidence kind.

- **D1, the homepage hero, is `images`.** The owner judges a layout by eye, so
  each option carries its mockup and the context line says what the two share
  ("same photo, headline and button; only the layout differs"). A weaker slide
  would describe the layouts in words.
- **D2, the returns policy, is `diff`.** The answer depends on exact wording, so
  the slide shows the redline and the rule as it will read, and offers "Needs
  change" for a third answer:

  ```json
  "evidence": {
    "kind": "diff",
    "before": "Baked goods can be exchanged on the day of purchase. We do not offer refunds.",
    "after": "Baked goods can be exchanged or refunded within one day of purchase. Please bring your receipt.",
    "rule_now": "Baked goods can be exchanged or refunded within one day of purchase. Please bring your receipt."
  }
  ```

  A weaker slide would show a screenshot of the policy page, where the owner
  has to find the change, or paraphrase it ("allows refunds"), which asks them
  to approve words they cannot see.
- **D3, the delivery fee, is `chart`.** The answer turns on one number per
  option (orders a week), so each option is a bar, the recommended one is
  emphasised and the source line says the figures are a projection.
- **D4, opening hours, is `table`.** Each option differs on three attributes
  (weekdays, Saturday, Sunday), which a chart cannot hold. Rows follow the
  option order, recommended first.

The spec's `decided` list carries one answer from an earlier round, in words
("Pickup orders only at launch"), so the summary slide shows it without asking
it again.
