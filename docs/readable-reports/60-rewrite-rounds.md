# Rewrite Rounds: Codex Astra Low Against The Skill

Method: a fresh Codex `gpt-6-astra` session at `low` reasoning effort, with no
context beyond the brief, reads the installed `readable-reports` skill and
rewrites two real reports. The parent (this session) then reads the rewrites
as the reader would and judges them against the bar: a smart,
engineering-minded executive can read them at a glance without decoding any
sentence, and nothing is dumbed down. Where the rewrite fails, the parent
names the mechanism, decides whether the skill or the worker was at fault,
edits the skill, and runs the next round. Up to three rounds.

Inputs for every round:

- Morning priorities, September 6, 2026 (the trigger report).
- Android monetization replay audit, September 1, 2026.

## Round 1

- Run dir: `/tmp/agent-delegate/readable-reports-round1-20260906T175839Z`
- Codex thread: `01a077df-53a1-7280-af58-19fa11b640d4`
- Account: `qa` (chosen through `aim codex use qa`, 1% weekly use)
- Skill version: as committed before this round (SKILL.md 11.1 KB; two references).
- Outputs: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/rounds/round-1/`

Verdict: pending.

Verdict: not there. Better than the originals at naming and linking; worse at
density and voice. Amir would say "This is way too fucking wordy" and "sounds
like AI".

What improved (keep):

- Things are named and linked with titles: "[the Customer.io mission-day
  trigger repair (psmobile #4792)](...)". The four stacked checkout fixes are
  listed individually with what each one does.
- The division is done: "Within 30 days, 0.56% of July paid installs paid (15
  of 2,694), down from 1.48% in April (96 of 6,500)."
- The top line is a message. Method and coverage moved to an appendix.
- Unknowns are written as unknowns ("The exact blocking check was not
  checked") instead of labels.

What failed, by mechanism:

1. Column headers became stilted sentences. Every table: "| The priority has a
   business outcome. | The current evidence supports this next step. |",
   "| Each platform has a reconciled checkout population. |". 17 such header
   cells in the priorities rewrite, 25 in the audit. The skill said headings
   are messages and the worker applied it to column headers. Column headers
   and row labels are labels.
2. Every row wears the same shape. "Priority 1 is ...", "Amir is working on
   ... through ...", "Tim's historical campaign comparison serves profitable
   acquisition.", "X should Y" (35 times). Four checkout fixes got the same
   three sentences with the name swapped. Formula reads as robotic.
3. Source links were narrated into sentences. Every cell ends with one:
   "The [campaign confirmation](...), [SDK response](...) and [team
   evidence](...) support this account." / "establish the distinction" /
   "retain the small-sample limit" / "preserves the check" / "records the
   disagreement" (50 such verbs). This is padding plus elegant variation. The
   skill's "every sentence has a subject and a verb" was applied to link tags.
4. Paragraph cells. Five to eight sentences per cell in the status table.
   The priorities report doubled from 2,338 to 4,802 words; the audit grew
   from 4,725 to 5,813. "I don't want fucking paragraphs."
5. Number tables turned into prose tables. "Android players purchased in 73
   of 353 starts (20.7%) and cancelled in 232 of 353 (65.7%)." repeated per
   row with "of 353" each time, where a grid of numbers with units in the
   header would read at a glance.
6. House terms still undefined: "offering" 41 times, "paygate" 26,
   "canonical" 14, "exact-owner" 7, never defined once at the top.
7. Voice switches: "Amir is working on ..." then "You delivered comparison
   worksheets" in the same cell. Recommendations to Amir written as "Amir
   should ship ...".
8. Every heading, including appendix subsections, is a full declarative
   sentence with a period: "The source inventory retains the full working
   evidence." Body headings should carry the message; appendix headings can
   be labels; none need a period.
9. Links to local file paths (65 in the priorities rewrite) in a report meant
   to be shared. Link to what the reader can open from where he reads.
10. False precision kept: "66.253 seconds".

Fault: the skill, mostly. Its sentence rule lacked the boundary (labels are
not sentences), it had no cell or document density check, its anti-formula
line was too abstract for a low-effort worker, and "define house terms once"
lived only in a reference. The worker did what the text said.

Skill changes for round 2: see the diff summary under Round 2.

## Round 2

- Run dir: `/tmp/agent-delegate/readable-reports-round2-20260906T190831Z`
- Codex thread: `01a0781f-524d-7e01-9f67-68ff2beeea3d`
- Account: whichever `aim` label was active at launch (`coder`; another agent had rotated it after `qa` was selected)
- Skill changes before this round (SKILL.md 11.1 KB to 13.7 KB; `references/reader-and-shapes.md` gained three worked shapes):
  1. Sentence rule bounded: prose and cells are sentences; column headers, row labels, and source tails are labels; imperatives count.
  2. Density: a status cell is one to three short sentences (about forty words); more means a subsection; number tables stay grids with one sentence above.
  3. Length check: a rewrite lands near the original's length; more than a quarter longer means narration, formula, or restated numbers.
  4. Source links ride on the fact or sit in a bare "Sources:" tail; never a sentence whose only job is to cite.
  5. "Words used here" block: any house, vendor, or tool term used more than twice is defined once at the top.
  6. No repeated shape: rows do not all open alike; the same sentence with a name swapped is banned; shared states are said once with the items listed.
  7. One voice; recommendations as imperatives in person-labeled rows.
  8. Body headings short, no trailing period; appendix headings may be labels.
  9. Links point to what the reader can open (URL first, local path only if none).
  10. Round to the precision the decision needs.
- Outputs: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/rounds/round-2/`

Verdict: pending.

Round 2 (first launch) was killed after Amir's correction. Its partial
outputs are kept in `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/rounds/round-2-killed/` for the record only.

Amir's correction, verbatim: "Hold on, paygate and offering are words I
would use. You can't make it define every single fucking normal business
term, right? I especially know terms that I myself use. I think you're
fucking missing the point with that: house terms are never defined. By the
way, making it wordier is not helpful." and "Yeah you need to make it
non-fucking heuristic. If you're making stupid rules about things used more
than twice, you're treating me like a fucking child, right? How about this:
you set up a cold reader agent who is me, right? Have it read everything
about me, everything I've written, and have it give my fucking perspective
and use that as the external validator for this because you clearly suck at
it."

Skill changes after the correction (SKILL.md 13.3 KB):
- Deleted the "Words used here" rule and every mention of defining house terms.
- Naming rule now turns on ownership: the writer's private label (minted code, tool state, session-local noun, coined metaphor) is the failure; the reader's own vocabulary is never defined.
- Removed every numeric threshold (forty words per cell, twelve-word headings, 25-word sentences, "a quarter longer") in favor of judgment tests.
- "Do not make it wordier" is now a non-negotiable: a rewrite longer than the original has almost always added something the reader did not ask for.
- The calibration table in `references/reader-and-shapes.md` now lists his own words (paygate, offering, checkout conversion, canonical, attribution, entitlement) under "never explain or define".

Validator: a cold-reader child (`amir-cold-reader`) immersed in his corrections,
verdicts, messages, and sent writing now judges each round in his voice. The
parent no longer judges alone.

Round 2 relaunch:
- Run dir: `/tmp/agent-delegate/readable-reports-round2-20260906T192144Z`
- Codex thread: `01a0782b-87cb-74b1-86c4-48148623c770`
- Outputs: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/rounds/round-2/`

Verdict: pending (from the cold reader).

Verdict (cold reader, as Amir), morning priorities: FAIL, close. "Top half I
can read and act on. Bottom half is a 2,400-word essay about how you built
the page. Cells are still paragraphs."

Stops, in his order: the appendix is about the page (render sizes, an HTML
SHA-256, which investigators resumed which roles); writer's private labels
that survived ("store grants", "client purchase completions", "await
integration", "objections"); "Your later September 5 assessment credits the
partnership" with no quote or link; "not checked" notes inside people's
status rows; 51 identical generic "Sources: Communications evidence ·
Business metrics and freshness" tails; no scannable state per person
("Make the status obvious so I don't have to guess"); a percent on a base
of eight ("Cached new payers rose 38.1%, from 21 to 29").

Keep: the one-sentence top line; the paragraph naming and linking all five
stacked checkout PRs ("That's what 'root clean, children blocked' should
have been"); "Her lifecycle work is blocked because the mission events have
not shipped."; the 30-day payer sentence with the division done; the
per-person deliveries table shape.

Fault: mostly the instructions. "Preserve every fact" plus "mark anything
not verified in the text" plus "move method to an appendix" produced the
page-about-itself appendix, the not-checked notes inside rows, and a source
tail on every cell. The surviving private labels are the writer's.

Verdict (cold reader, as Amir), Android audit: FAIL, narrowly. "First screen
is good: the number, the gap, the three repairs, the five actions. The
middle reads like a lawyer wrote it."

Stops: "unknown" 16 times, "unresolved" 24, "does not establish" 6 ("You
can't be so scientific. I need useful decisions, not proof."); a noun-stack
heading ("Canonical checkout coverage needs one reconciled session model");
the writer's method words as nouns ("controls" read as buttons; "canonical
terminal"; "purchase-attributed coverage"); agentless passive ("A manual
action in the two-control error area was followed by recovery"); "4.986 and
66.253 seconds" four times; sentences about the audit's own process.

Keep: the one-line answer with the gap and its decomposition; the "even if
all 17 errors became purchases" sentence; code pointers with line numbers;
the five numbered repairs and the do-not-build list; the theory
dispositions table ("That's what I actually want to see and it's buried in
the appendix"); headings that say something.

Fault: mostly the writer, except "mark anything not verified in the text",
which put unknown or unresolved forty times into one report.

Skill changes for round 3 follow.

## Round 3

Skill changes before this round (SKILL.md 15.0 KB), each traced to a
round-2 stop:
1. "Preserve every fact" now means facts about the business. Render sizes,
   hashes, run ids, model names, worker roles, rules applied, and what was
   suppressed do not survive the rewrite. The appendix holds only what he
   would use to check a claim; the body holds everything he would act on,
   including the theory dispositions table.
2. "Say what you know; stop there." Unknown or not checked appears only
   where the reader needs that answer to act; never inside a status row;
   findings are stated decisively and qualified once.
3. A source is the specific message, PR, query result, or row, linked on
   the fact or in a short tail; generic collection pointers are not
   repeated per cell.
4. Anything the report says he said or decided is quoted and linked, or cut.
5. Status cells lead with the state and its cause in a few words, then the
   sentence with names and links, so the state is visible without reading
   the cell.
6. Private-label test widened to phrases lifted from a query column, JSON
   field, log, or the writer's method ("store grants", "controls",
   "canonical terminal"), with the repair: say what a person did or saw.
7. Name the actor; no agentless passive.
8. Percent only when the base supports it; precision the decision needs.

- Run dir: `/tmp/agent-delegate/readable-reports-round3-20260906T194558Z`
- Codex thread: `01a07841-9ed3-72a2-8b17-85e3f0d8d26b`
- Account: `qa`
- Outputs: `/Users/aelaguiz/workspace/arch_skill/docs/readable-reports/rounds/round-3/`

Verdict: pending (from the cold reader).
