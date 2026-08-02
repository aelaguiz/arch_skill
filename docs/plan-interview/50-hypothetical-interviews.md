# Hypothetical Interviews

Date: 2026-08-02, revised as Amir's calibration lands. Five mock transcripts of
the future `plan-interview` skill, written to be critiqued. **A:** is Amir,
**I:** is the interviewer. Lines in *italics* are design annotations.

What changed from rev 1: the ramp-up stage now returns **facts and a blank
template, never a drafted plan**; the interview leads with **open questions
framed by evidence and Amir's own history** ("typically your requirements
here are… what are you thinking?"); options with recommendations are the
fallback, not the lead; every UX-touching interview asks about **mocks and
target images**; the interview walks the must-always-know list so nothing
gets a line by assumption; **a user journey map is required wherever the
work touches a journey** — a one-line confirm of the existing journey in
the usual mature-product case, the tweak marked on it, or every journey a
bigger feature creates; and every interview closes with the **two-gate
handoff** — a clean decision table ("is this good?"), then "ready for me to
run the plan step?" with `$arch-mini-plan` as the default and a one-sentence
steer accepted (different planning skill, adversarial reviewer, straight to
conductor). And the interview is a **loop, not a line**: answers trigger
investigation — "give me a few minutes to figure out what that means" —
with findings written into the pack and new questions on return, multiple
cycles as needed (Interviews 2, 3, and 6 each show a real cycle).

---

## Interview 1 — psmobile performance repair ("make lesson screens instant")

**A:** the lesson intro screens are janky as hell, sometimes 2-3 seconds
before anything renders. make them instant.

**I:** Two orienting questions before I go educate myself, so I read the
right things: (1) lesson intros only, or is this the tip of "the app feels
slow generally"? (2) standalone fix, or part of something bigger you're
planning?

**A:** just lesson intros. standalone.

**I:** Ramping up on the intro rendering path, PR history there, existing
automation, and what you've asked for in past perf work. Back with facts —
not a plan.

*Education runs. Returns a facts briefing + blank template. Nothing decided.*

**I:** What I found — facts only:

- Intro screens block on a lesson-content fetch plus two image decodes
  before first paint. Measured 1.9–3.1s on the pinned sim.
- The home screen had the same class of problem in June; it was fixed with a
  skeleton-first pattern.
- Zero automation currently measures intro timing.
- The puzzle intro screen uses the same fetch pattern (noting it — not
  including it).

Template's open, nothing filled in. Interview — intent first:

**What does "instant" mean to you here — a number, a comparison, or a
feel?** (In past perf work you've set a measurable bar; you don't have to.)

**A:** it should feel like the home screen does now. whatever that is.

**I:** Home screen first-paints under ~300ms with its skeleton. Adopting
"intro matches home-screen paint behavior" as the bar — that's your
comparison made measurable. Approved?

**A:** yes

**I:** UX delta — open question: the home-screen fix shows a skeleton flash
before content lands. Are you okay with intros getting that same flash, or
is any visible change off the table?

**A:** skeleton is fine, same as home. nothing else changes.

**I:** Written: UX delta = skeleton on intro (reusing the existing pattern),
everything else frozen. Journey map — required whenever we touch a journey,
and here it's the confirm-only kind: home → tap a lesson → intro screen →
start. No step added, removed, or reordered; this work only makes the intro
step paint faster. Is that the whole journey story?

**A:** that's it.

**I:** Mapped in the pack as unchanged. Proof — you usually ask for a full
test grid with all the possible edge cases. Want that here? And at what
altitude — sim automation that measures paint time and fails on regression,
or is this a hand-check-on-your-phone situation?

**A:** full grid, sim automation, goes in the default suite

**I:** Then here's the grid, built from your answer plus what I found in
the code — each case and what it proves. What's missing?

| Case | Proves |
|---|---|
| Cold start → lesson intro | The main journey paints like home |
| Warm re-entry | No regression coming back to the screen |
| Slow network | Skeleton holds; never a blank screen |
| Largest lesson in the catalog | Biggest content still meets the bar |
| First run, empty cache | Brand-new users get the same experience |
| Mid-scroll re-entry | The historically flakiest path stays smooth |

**A:** nothing. that's the grid.

**I:** Approved and in the pack. Architecture — typically your requirements
in a perf fix are: no new caching infrastructure, and the slow path gets
deleted rather than bypassed. What are you thinking here?

**A:** exactly that. no new infra. delete the old path.

**I:** Recorded as hard requirements. One discovery question: puzzle intro
shares the slow fetch pattern. In scope or logged as a follow-up?

**A:** out. log it.

**I:** Deferral ledger. Last two lines, both defaults: standard execution
setup (Sol Ultra via conductor, Terra xhigh cynicals, Fable xhigh
adversarial, worktree + pinned sim in the doc, one branch one PR) — any
changes? And will you be around during the run, or should the pack carry
full overnight autonomy?

**A:** standard. I'll be around today.

**I:** All 13 lines have content. Here's what we decided — is this good?

| Area | Decision |
|---|---|
| Outcome | Lesson intros paint like the home screen: skeleton, <~300ms first paint |
| Why | 2-3s of jank on a core daily surface |
| Must (hard) | Intro paint behavior matches the home screen |
| Must (hard) | Sim automation measures it and joins the default suite |
| Must (hard) | The old fetch path is deleted; no new caching infrastructure |
| UX delta | Skeleton only, existing pattern; everything else frozen |
| Journey | Existing lesson-entry journey confirmed, unchanged |
| Visuals | None needed — target is existing in-app behavior |
| Non-goals | Puzzle intro (deferred, logged); anything visually new |
| Test grid | The 6 cases you approved above |
| Done | Grid green on the pinned sim + adversarial reviewer signs off |
| Execution | Standard (Sol Ultra / Terra xhigh / Fable xhigh, pins in doc) |
| Assumption (mine) | Bar applies to iPhone-class sims — flag if wrong |

**A:** good

**I:** Ready for me to run the plan step? Default: `$arch-mini-plan`
against this pack. Steer me if you want something else.

**A:** run the mini plan, then adversarial review it with fable xhigh, two
rounds max

**I:** Running `$arch-mini-plan`, then a Fable xhigh adversarial pass
capped at two rounds, then conductor. Your time so far: ~8 minutes.

*Moves: ramp-up returned facts, not decisions; "instant" was elicited, not
assumed; the 300ms number entered as HIS comparison made measurable, then
approved; the test grid was requested by him with framing from his own
habits; the puzzle screen surfaced as a question, not as included scope;
the close was a decision table gate, then a steerable plan-step gate.*

---

## Interview 2 — psagentspace centralization ("one streak owner, delete the rest")

**A:** streak logic is spread across like four places and they disagree.
centralize it, delete the duplicates.

**I:** One orienting question: is "streak" here the user-visible home-screen
streak, or everything streak-shaped including internal counters?

**A:** the real user streak. whatever feeds it.

**I:** Ramping up on every reader and writer of user-streak state, plus how
it got this way. Facts when I'm back.

*Education returns: 4 writer paths, 2 reader helpers, a nightly job, an
export field, mapped in `research/streak-owners.md` with real divergence
found in the data. Template blank.*

**I:** Facts: four writers, two readers, one nightly job, one export field.
The writers genuinely disagree — I found accounts where the visible streak
and the nightly job's number differ. Nothing decided; interview:

**Intent check first — say back what you want in your words: is the outcome
"one owner, users see zero change," or is fixing the wrong displayed values
part of the job?**

**A:** one owner. users see zero change. the displayed number is the truth
as far as they're concerned.

**I:** That answers the hardest question in this project before I had to
ask it: **when the paths disagree, the user-visible value wins.** Writing
the hard requirement in plain words: user-visible streak values are
identical before and after. Project type:
this reads as centralization + deletion — your strictest standing rules
(not feature time, delete don't quarantine, no new user-facing anything).
Agree with that classification?

**A:** yes. zero new features.

**I:** Architecture — typically your requirements in a centralization are:
one named owner path, every other writer deleted, readers migrated, and no
compatibility shim keeping old paths alive "for safety." What are you
thinking, and is there anywhere you'd deviate?

**A:** no deviation. one owner. everything else dies.

**I:** Recorded. Vocabulary flag — the code has an internal state called
`practised` on streak days. I'm treating that as an internal label only:
nothing in the plan may surface it or build on it as if it were a product
concept. Correct?

**A:** correct. there's no such thing as a practice day.

**I:** Glossary: banned-from-requirements. The stay-dead list I'm proposing
for your approval — these get deleted and no reviewer or parity pass may
resurrect them: the profile updater's local write, the lesson-complete
hook's copy, the export-time recompute. The nightly job is the open one:

**Does anything you know of still need the nightly job, or should it die
unless I find a live consumer?**

**A:** kill it unless something real needs it. if so it reads from the
owner.

**I:** Rather than record that as a conditional, give me two minutes to go
find out.

*Investigates: traces every consumer of the nightly job's output.*

**I:** Answered — the job's output feeds only the export field, and that
export recompute is already on the deletion list. Nothing real consumes it.
Writing it as a plain deletion, no conditional. Proof — my proposal for
your approval: a
before/after diff of visible streak values across all real accounts (that
directly proves the values-identical requirement), plus existing streak
tests green. Want anything above
that — full test grid, or is the account diff the decisive proof here?

**A:** account diff is the proof. add automation only if it's cheap.

**I:** Recorded with your wording. Checkpoint: I can freeze now. One area
would benefit from 3 more minutes: the two accounts I found with corrupted
streak history (they'll diff no matter what we do). Handle them, or
leave-as-is and log?

**A:** leave and log.

**I:** Standard execution setup, and attendance?

**A:** standard. I'm out tonight — full autonomy, flag anything
user-visible for morning.

**I:** Autonomy contract written: overnight authority, user-visible
decisions provisional + flagged, blockers must be proven external. The
decision table — is this good?

| Area | Decision |
|---|---|
| Outcome | One owner for streak truth; users see zero change |
| Hard requirement | User-visible streak values identical before and after |
| Truth rule | When paths disagree, the user-visible value wins |
| Deletions | Profile updater write, lesson-hook copy, export recompute |
| Deletion (verified) | Nightly job — traced its consumers, only the retired export field used it |
| Vocabulary | `practised` is internal-only; "practice day" banned |
| UX delta | None; no new features of any kind |
| Journey | No journey work — users' flow untouched |
| Proof | Before/after account diff + existing streak tests green |
| Known exception | 2 corrupted accounts: leave as-is, logged |
| Reviewer rule | This pack IS the scope; feature-shaped findings rejected |
| Execution | Standard; overnight autonomy, user-visible flags for morning |

**A:** good. run it

**I:** Default plan step: `$arch-mini-plan` against this pack — running it
now, conductor when the plan freezes.

*Moves: the disagreement resolution came out of HIS intent statement rather
than a multiple-choice; classification and stay-dead list were derived then
approved; proof standard was proposed, he chose the bar.*

---

## Interview 3 — new UX (psmobile "daily challenge" card) — the deep lane

**A:** I want a daily challenge card on the home screen. one hand a day,
streak-adjacent, should feel special.

**I:** New user experience — this is the one interview that goes deep on UX,
and architecture stays out of it. Orienting: is this its own thing, or step
one of a bigger daily-engagement push I should know about while reading?

**A:** its own thing for now.

**I:** Ramping up on the home screen layout system, how puzzles get served,
how streaks hook in, and what you've said about daily-habit features
before. Facts when back.

*Education returns. Template blank; 9 open questions queued, orderd by how
much they shape everything else.*

**I:** Facts: home screen is a slot-based rail layout; puzzles are served
from puzzledb with difficulty tags; streak state has one visible surface.
Nothing decided. This interview is mostly you talking — broad strokes
first:

**Before anything else: do we have mocks, target images, a reference app —
anything visual to align on for this card?**

**A:** no mocks. the feel I want is like Duolingo's daily quest — that
energy, not their look.

**I:** Recorded: reference = Duolingo daily quest (energy, not visual
clone), no mocks exist. Given that, I'm proposing a **mock gate**: 2–3
visual options for the card before implementation starts, you pick.
Standing question answered — now the shape, open questions:

**1. What's the job of this card — why does it exist?**

**A:** it's the reason you open the app today. habit anchor.

**2. Walk me through the moment: user opens the app, sees the card — what
happens, in your head, start to finish?**

**A:** they see today's hand, it feels like an event, they tap, they play
it like a normal puzzle, they get a result, the card shows done and teases
tomorrow. one a day, no grinding.

**I:** That's the journey — writing it as you said it. Three things your
walk implies that I want explicit:

- "Feels like an event" → distinct art treatment (the mock gate covers
  what that means).
- "Like a normal puzzle" → existing puzzle player, no new mechanics.
- "Shows done and teases tomorrow" → the card has a done-state; it doesn't
  disappear.

Anything wrong in those three?

**A:** no that's right.

**I:** Then the journey map — a bigger feature usually creates more than
one journey, and this one creates three. All go in the pack:

1. **Daily play** — open → see today's card → tap → solve → done-state.
2. **Same-day return** — open again after solving: card sits in done-state,
   no second hand.
3. **Next-day reset** — card is fresh again at local midnight.

Anything about journeys two or three that isn't obvious?

**A:** no. midnight local is right.

**3. Who gets it — everyone including free users, or is the paygate
involved?** (Flagging: if free users see it locked, that's a paygate
change, which is currently a frozen surface.)

**A:** everyone. paygate untouched.

**4. Does it touch the real streak, or is it its own little counter?**

**A:** own counter. real streak untouched.

**I:** Both recorded as hard requirements — and both keep this project off
two frozen surfaces (paygate, streak logic), which keeps it small. One
thing your answers raise that I can't answer from what I've read so far:
how the daily hand actually gets picked. Give me a few minutes with the
puzzle-serving code.

*Investigates: how puzzles are tagged, served, and whether anything can
mark a hand as "today's."*

**I:** Back — findings are in the pack. Puzzles are tagged by difficulty
and street, and served per-user by a rating-matched picker; nothing
anywhere marks a hand as "today's." That raises two questions I couldn't
have asked before looking:

1. Is the daily hand the same for everyone that day, or matched to each
   player's level like normal puzzles?
2. Auto-selected by rules, or a hand-picked queue someone curates?

**A:** same hand for everyone — that's what makes it an event. auto-picked
but it has to be solvable at every level.

**I:** Recorded: one global daily hand, auto-selected with a
solvable-at-every-level constraint — that constraint is real work and goes
in as a hard requirement. Scope knife — MVP as I'll write it: card + one
global daily hand + done-state + own counter + distinct art (mock-gated).
Explicitly NOT in: push notifications, share button, gems/reward hook,
history screen, difficulty tuning. Say the word to move any in.

**A:** notifications eventually but not now.

**I:** Deferral ledger: notifications = intended later, not now. Proof —
you usually want the full grid for anything user-facing. Proposal: sim
automation covering card-appears, solve flow, done-state, midnight
rollover, fresh install; plus before/after home-screen screenshots in the
PR. What's missing from that grid?

**A:** what happens with no connectivity. and the card better not shove
the lesson rail around.

**I:** Both added: offline behavior (needs one answer — what should the
card show offline? I'll bring options with the mock round) and a layout
requirement — card insertion must not reflow existing rail content.
Checkpoint: freeze now with the mock gate pending, or spend 5 more minutes
on done-state copy and edge details?

**A:** freeze. copy comes with the mocks.

**I:** Standard setup + attendance?

**A:** standard. around.

**I:** Decision table — is this good?

| Area | Decision |
|---|---|
| Outcome | Daily challenge card: the reason to open the app today |
| Journeys (3 mapped) | Daily play (see hand → tap → solve → done-state); same-day return (done-state holds); next-day reset at local midnight |
| Visuals | No mocks; reference = Duolingo daily quest energy; **mock gate: you pick from 2–3 options before implementation** |
| Audience | Everyone; paygate untouched (frozen surface) |
| Streak | Own counter; real streak untouched (frozen surface) |
| Daily hand | Same for everyone; auto-selected, solvable at every level |
| Layout (hard) | Card must not reflow existing rail content |
| Non-goals | Push, share, gems hook, history screen, difficulty tuning |
| Deferral | Notifications — intended later, not now |
| Test grid | 7 cases incl. offline + fresh install; before/after shots in PR |
| Open | Offline card behavior + done-state copy ride with the mock round |
| Execution | Standard |

**A:** good — mocks first, then run the mini plan

**I:** Mock round first, then `$arch-mini-plan` with the pack. Your time:
~15 minutes, and the only decisions I made alone are listed as 2
assumptions in the pack.

*Moves: visuals asked first (his answer reshaped everything downstream);
the journey came from HIM narrating, with the skill extracting implicit
requirements and confirming them; the grid gaps came from asking "what's
missing" instead of presenting a finished grid as fact.*

---

## Interview 4 — the quick lane (small repair)

**A:** the settings screen crashes when you background the app mid-scroll.
fix it.

**I:** Quick lane — educating briefly on the crash logs and that screen's
lifecycle handling first. *(returns)* Facts: reproducible in the logs, one
screen, looks contained. Three questions, one round:

1. Proof bar: regression test, or do you want sim automation reproducing
   the background-mid-scroll sequence? (Lifecycle bugs have slipped past
   plain tests here before — your call.)
2. I found no other screens with this crash signature in the logs — do you
   know of any I should include anyway?
3. Standard setup, straight to conductor, no full plan?

**A:** sim automation. just settings. yes.

**I:** Quarter-page pack written. The table — good to dispatch?

| Area | Decision |
|---|---|
| Outcome | Settings screen survives backgrounding mid-scroll |
| Proof | Sim automation reproducing the sequence + fix |
| Scope | That screen's lifecycle handling only; bigger = comes back as a question |
| Plan step | None — straight to conductor, as you just said |

**A:** go

**I:** Dispatching.

*Move: proportionality — but even the quick lane asks its three questions
instead of deciding; the proof-bar question carries framing from history.*

---

## Interview 5 — proxy mode (Amir bails, a model stands in)

*Continuation of an interview like #3, mid-way through.*

**A:** I'm going to bed. have fable answer the rest as me. nothing that
changes what users see without flagging it for morning

**I:** Proxy engaged: a clean Fable session answers as you — armed with the
pack so far, your north stars, the standing doctrine, and your phrasing
bank. Rules per your instruction: user-visible decisions get provisional
answers + morning flags; everything else the proxy settles for real. The
proxy gets the same open questions you would have — it doesn't get to
rubber-stamp my suggestions either.

*Overnight, in the decision log:*

- Q: what should the card show when the day's hand fails to load? →
  **[PROXY-fable]** retry once silently, then the card's existing
  empty-state — no new error UI. *(final — introduces no new UX)*
- Q: does the counter survive reinstall? → **[PROXY-fable]** no —
  device-local, consistent with practice history. *(final)*
- Q: done-state copy? → **[PROXY-fable]** drafted 3 options in app voice.
  *(provisional — user-visible, flagged)*

**I (morning):** While you were out: 7 questions resolved — 5 final by
proxy, 2 flagged for you: (1) done-state copy, pick: A "Nice. Same time
tomorrow." B "Solved. Streak's alive." C "Done. New hand at midnight."
(2) confirm the proxy's empty-state reuse for load failures. Nothing else
outstanding; the run never stopped.

**A:** A. confirmed.

**I:** Both final, decision log updated.

*Moves: the proxy answers open questions under the same rules; its answers
are labeled, auditable, and the morning cost was two genuinely-his
decisions.*

---

## Interview 6 — "build this" (three words and a screenshot)

**A:** build this *(screenshot: a competitor app's shareable hand-replay
card)*

**I:** Before I ask you anything I'll go figure out what "this" is and
what it would mean here — what's in the image, what we already have that's
close, what it would touch. Back shortly.

*First cycle: reads the screenshot, maps existing replay and share
surfaces, checks how hands render outside the table view.*

**I:** What I found, now in the pack: the screenshot is a share card — a
finished hand rendered as a static image with hero cards, board, pot, and
a result line, sized for a social post. On our side: we render hands in
the replayer, we have no image-export path anywhere, and our share button
sends a plain text link. Nothing decided. First question, because it
changes everything downstream:

**What's the job — growth (hands showing up where non-players see them),
or a feature for existing users to save their hands?**

**A:** growth. i want hands showing up in group chats.

**I:** Group chats means the card is the product and link previews matter.
I don't know what our links look like when pasted into a chat today — give
me a few more minutes.

*Second cycle: checks link-preview metadata end to end.*

**I:** Found it: our links unfurl as the generic app icon with no preview
image — so even a beautiful card dies in a group chat today. The questions
that only exist because I looked:

1. Share from where — end of a hand, the replayer, or both? (End-of-hand
   is the emotional moment; the replayer is more surface area.)
2. The card: is that screenshot the target look, or reference-only with
   our brand doing its own thing?
3. Does fixing the link preview ride along as a requirement, or is the
   image file itself enough for group chats?

**A:** end of hand only for v1. reference only — ours looks like us. and
yes the preview fix is part of it, otherwise what's the point.

**I:** All three recorded — the preview fix goes in as a hard requirement
with your reasoning attached. Continuing the normal walk from here:
journey maps (there are at least two — sharing a hand, and a non-player
tapping what lands in the chat), the grid, mocks for the card, then the
decision table.

*The point of this mock: three words in, two investigation cycles out,
and every question the interview asked existed only because it went and
looked. "Build this" was never transcribed as a requirement — it was
decompiled into ones.*

---

## The failures the design must not reproduce (annotated counter-examples)

> ~~Ramp up, then return with: "Here's the plan I drafted — correct
> anything wrong."~~ → The education stage returns facts and a blank
> template. Plan content enters only as his answers, approved derivations,
> or confirmed defaults. A pre-filled draft is a pile of decisions he never
> made, formatted to be rubber-stamped.
>
> ~~"For C8, should the retry budget be 2 or 3?"~~ → The skill decides from
> first principles, records it as an assumption with a one-line rationale,
> and moves on.
>
> ~~"R1 is done, R2 is blocked, see Q3"~~ → The skill never invents its own
> codes either. Requirements are said in words and referred to by name
> ("the delete-the-old-path requirement"), in tables, summaries, and
> follow-ups alike. Plain numbered lists are fine; alphanumeric shorthand
> is not.
>
> ~~"What should `_resolveStreakWindow()` do when the offset is stale?"~~ →
> Never asks about a symbol. If the question is real it becomes: "if the
> app clock and the server disagree about what day it is, who wins?" — and
> only if the answer changes what users see.
>
> ~~Fifteen sequential questions, each spawned by the last answer~~ → The
> must-always-know list walked breadth-first, budgeted follow-ups,
> checkpoints offering depth, "good enough" always accepted, always ends
> with "freezing now" + the assumption list.
>
> ~~Multiple-choice everything~~ → Options with a recommendation are the
> fallback (small confirms, defaults, sharpening), never the lead for
> intent, requirements, UX, or architecture. His thinking comes first.
>
> ~~Freeze silently and auto-run the next skill~~ → The close is always two
> gates: the decision table ("is this good?"), then "ready for me to run
> the plan step?" — where a bare yes runs `$arch-mini-plan` and a sentence
> of steering ("full arch-step", "adversarial with Fable xhigh") runs
> exactly that instead.
>
> ~~"Recorded: 'build this.' Next question:…"~~ → Never transcribe what you
> don't yet understand. The skill goes and figures out what the words mean
> in this codebase, writes the findings into the pack, and returns with the
> questions those findings raise. One-shot linear interviews produce
> dictation; the loop produces understanding.
