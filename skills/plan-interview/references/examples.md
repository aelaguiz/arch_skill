# Examples

Six worked interviews followed by counter-examples. These are illustrations
of the moves — not a script to replay. **User:** is the human;
**Interviewer:** is the agent running this skill. Lines in *italics* are
design annotations.

The moves on display: education returns facts and a blank template; open
questions lead, framed by evidence and the user's own history; options with
recommendations are the fallback; journey maps and the full test grid are
approved inside the interview; investigate-and-return cycles happen whenever
an answer demands one; every close is a decision table, then a steerable
plan-step gate. The interview always runs in the user's own conversation —
never on a background agent. For brevity these transcripts mostly abridge
the running decisions-so-far table that opens each questioning round
(Example 3 shows one); the closing decision table is that table's final
form, not a reveal.

---

## Example 1 — mobile performance repair ("make lesson screens instant")

**User:** the lesson intro screens are janky as hell, sometimes 2-3 seconds
before anything renders. make them instant.

**Interviewer:** Two orienting questions before I go educate myself, so I
read the right things: (1) lesson intros only, or is this the tip of "the
app feels slow generally"? (2) standalone fix, or part of something bigger
you're planning?

**User:** just lesson intros. standalone.

**Interviewer:** Ramping up on the intro rendering path, PR history there,
existing automation, and what you've asked for in past perf work. Back with
facts — not a plan.

*Education runs. Returns a facts briefing plus a blank template. Nothing
decided.*

**Interviewer:** What I found — facts only:

- Intro screens block on a lesson-content fetch plus two image decodes
  before first paint. Measured 1.9–3.1s on the pinned sim.
- The home screen had the same class of problem recently; it was fixed
  with a skeleton-first pattern.
- Zero automation currently measures intro timing.
- The puzzle intro screen uses the same fetch pattern (noting it — not
  including it).

Template's open, nothing filled in. Interview — intent first:

**What does "instant" mean to you here — a number, a comparison, or a
feel?** (In past perf work you've set a measurable bar; you don't have to.)

**User:** it should feel like the home screen does now. whatever that is.

**Interviewer:** Home screen first-paints under ~300ms with its skeleton.
Adopting "intro matches home-screen paint behavior" as the bar — that's
your comparison made measurable. Approved?

**User:** yes

**Interviewer:** UX delta — open question: the home-screen fix shows a
skeleton flash before content lands. Are you okay with intros getting that
same flash, or is any visible change off the table?

**User:** skeleton is fine, same as home. nothing else changes.

**Interviewer:** Written: UX delta = skeleton on intro (reusing the
existing pattern), everything else unchanged. Journey map — required whenever
we touch a journey, and here it's the confirm-only kind: home → tap a
lesson → intro screen → start. No step added, removed, or reordered; this
work only makes the intro step paint faster. Is that the whole journey
story?

**User:** that's it.

**Interviewer:** Mapped in the pack as unchanged. Proof — you usually ask
for a full test grid with all the possible edge cases. Want that here? And
at what altitude — sim automation that measures paint time and fails on
regression, or is this a hand-check-on-your-phone situation?

**User:** full grid, sim automation, goes in the default suite

**Interviewer:** Then here's the grid, built from your answer plus what I
found in the code — each case and what it proves. What's missing?

| Case | Proves |
|---|---|
| Cold start → lesson intro | The main journey paints like home |
| Warm re-entry | No regression coming back to the screen |
| Slow network | Skeleton holds; never a blank screen |
| Largest lesson in the catalog | Biggest content still meets the bar |
| First run, empty cache | Brand-new users get the same experience |
| Mid-scroll re-entry | The historically flakiest path stays smooth |

**User:** nothing. that's the grid.

**Interviewer:** Approved and in the pack. Architecture — typically your
requirements in a perf fix are: no new caching infrastructure, and the
slow path gets deleted rather than bypassed. What are you thinking here?

**User:** exactly that. no new infra. delete the old path.

**Interviewer:** Recorded as hard requirements. One discovery question:
puzzle intro shares the slow fetch pattern. In scope or logged as a
follow-up?

**User:** out. log it.

**Interviewer:** Deferral ledger. Last two lines, both defaults: standard
execution setup — any changes? And will you be around during the run, or
should the pack carry full overnight autonomy?

**User:** standard. I'll be around today.

**Interviewer:** All must-know lines have content. Here's what we decided —
is this good?

| Area | Decision |
|---|---|
| Outcome | Lesson intros paint like the home screen: skeleton, <~300ms first paint |
| Why | 2-3s of jank on a core daily surface |
| Must (hard) | Intro paint behavior matches the home screen |
| Must (hard) | Sim automation measures it and joins the default suite |
| Must (hard) | The old fetch path is deleted; no new caching infrastructure |
| UX delta | Skeleton only, existing pattern; everything else unchanged |
| Journey | Existing lesson-entry journey confirmed, unchanged |
| Visuals | None needed — target is existing in-app behavior |
| Non-goals | Puzzle intro (deferred, logged); anything visually new |
| Test grid | The 6 cases you approved above |
| Done | Grid green on the pinned sim + adversarial reviewer signs off |
| Execution | Standard (pins in the doc) |
| Assumption (mine) | Bar applies to iPhone-class sims — flag if wrong |

**User:** good

**Interviewer:** Ready for me to run the plan step? Default:
`$arch-mini-plan` against this pack. Steer me if you want something else.

**User:** run the mini plan, then adversarial review it with fable xhigh,
two rounds max

**Interviewer:** Running `$arch-mini-plan`, then a Fable xhigh adversarial
pass capped at two rounds, then conductor.

*Moves: education returned facts, not decisions; "instant" was elicited,
not assumed; the number entered as the user's comparison made measurable,
then approved; the grid was built and approved on the spot; the adjacent
surface surfaced as a question, not as included scope; the close was a
decision table, then a steerable plan-step gate.*

---

## Example 2 — centralization ("one streak owner, delete the rest")

**User:** streak logic is spread across like four places and they disagree.
centralize it, delete the duplicates.

**Interviewer:** One orienting question: is "streak" here the user-visible
home-screen streak, or everything streak-shaped including internal
counters?

**User:** the real user streak. whatever feeds it.

**Interviewer:** Ramping up on every reader and writer of user-streak
state, plus how it got this way. Facts when I'm back.

*Education returns: four writer paths, two reader helpers, a nightly job,
an export field — with real divergence found in the data. Template blank.*

**Interviewer:** Facts: four writers, two readers, one nightly job, one
export field. The writers genuinely disagree — I found accounts where the
visible streak and the nightly job's number differ. Nothing decided;
interview:

**Intent check first — say back what you want in your words: is the
outcome "one owner, users see zero change," or is fixing the wrong
displayed values part of the job?**

**User:** one owner. users see zero change. the displayed number is the
truth as far as they're concerned.

**Interviewer:** That answers the hardest question in this project before
I had to ask it: **when the paths disagree, the user-visible value wins.**
Writing the hard requirement in plain words: user-visible streak values
are identical before and after. Project type: this reads as centralization
plus deletion — your strictest standing rules (not feature time, delete
don't quarantine, no new user-facing anything). Agree with that
classification?

**User:** yes. zero new features.

**Interviewer:** Architecture — typically your requirements in a
centralization are: one named owner path, every other writer deleted,
readers migrated, and no compatibility shim keeping old paths alive "for
safety." What are you thinking, and is there anywhere you'd deviate?

**User:** no deviation. one owner. everything else dies.

**Interviewer:** Recorded. Vocabulary flag — the code has an internal
state label on streak days that sounds like a product concept but isn't
one you've ever named. I'm treating it as internal-only: nothing in the
plan may surface it or build on it as if it were a requirement. Correct?

**User:** correct. there's no such thing.

**Interviewer:** In the glossary as banned-from-requirements. The
stay-dead list I'm proposing for your approval — these get deleted and no
reviewer or parity pass may resurrect them: the profile updater's local
write, the lesson-complete hook's copy, the export-time recompute. The
nightly job is the open one:

**Does anything you know of still need the nightly job, or should it die
unless I find a live consumer?**

**User:** kill it unless something real needs it. if so it reads from the
owner.

**Interviewer:** Rather than record that as a conditional, give me two
minutes to go find out.

*Investigates: traces every consumer of the nightly job's output.*

**Interviewer:** Answered — the job's output feeds only the export field,
and that export recompute is already on the deletion list. Nothing real
consumes it. Writing it as a plain deletion, no conditional. Proof — my
proposal for your approval: a before/after diff of visible streak values
across all real accounts (that directly proves the values-identical
requirement), plus existing streak tests green. Want anything above that —
full test grid, or is the account diff the decisive proof here?

**User:** account diff is the proof. add automation only if it's cheap.

**Interviewer:** Recorded with your wording. Checkpoint: I can sign off now.
One area would benefit from three more minutes: the two accounts I found
with corrupted streak history (they'll diff no matter what we do). Handle
them, or leave-as-is and log?

**User:** leave and log.

**Interviewer:** Standard execution setup, and attendance?

**User:** standard. I'm out tonight — full autonomy, flag anything
user-visible for morning.

**Interviewer:** Autonomy contract written: overnight authority,
user-visible decisions provisional and flagged, blockers must be proven
external. The decision table — is this good?

| Area | Decision |
|---|---|
| Outcome | One owner for streak truth; users see zero change |
| Hard requirement | User-visible streak values identical before and after |
| Truth rule | When paths disagree, the user-visible value wins |
| Deletions | Profile updater write, lesson-hook copy, export recompute |
| Deletion (verified) | Nightly job — traced its consumers, only the retired export field used it |
| Vocabulary | The internal day-state label is internal-only; banned from requirements |
| UX delta | None; no new features of any kind |
| Journey | No journey work — users' flow untouched |
| Proof | Before/after account diff + existing streak tests green |
| Known exception | 2 corrupted accounts: leave as-is, logged |
| Reviewer rule | This pack IS the scope; feature-shaped findings rejected |
| Execution | Standard; overnight autonomy, user-visible flags for morning |

**User:** good. run it

**Interviewer:** Default plan step: `$arch-mini-plan` against this pack —
running it now, conductor when the plan is signed off.

*Moves: the disagreement resolution came out of the user's own intent
statement; the classification and stay-dead list were derived then
approved; a conditional the code could answer was investigated and written
as a verified fact instead of transcribed.*

---

## Example 3 — new UX (a "daily challenge" card) — the deep lane

*The one scenario where the UX interview goes deep, because new UX is the
one thing standing doctrine can't default.*

**User:** I want a daily challenge card on the home screen. one hand a
day, streak-adjacent, should feel special.

**Interviewer:** New user experience — this is the one interview that goes
deep on UX, and architecture stays out of it. Orienting: is this its own
thing, or step one of a bigger daily-engagement push I should know about
while reading?

**User:** its own thing for now.

**Interviewer:** Ramping up on the home screen layout system, how puzzles
get served, how streaks hook in, and what you've said about daily-habit
features before. Facts when back.

*Education returns; template blank; open questions queued by how much they
shape everything else.*

**Interviewer:** Facts: home screen is a slot-based rail layout; puzzles
are served per-user from the puzzle database; streak state has one visible
surface. Nothing decided. This interview is mostly you talking — broad
strokes first:

**Before anything else: do we have mocks, target images, a reference app —
anything visual to align on for this card?**

**User:** no mocks. the feel I want is like Duolingo's daily quest — that
energy, not their look.

**Interviewer:** Recorded: reference = that daily-quest energy, not a
visual clone; no mocks exist. Given that, I'm proposing a **mock gate**:
2–3 visual options for the card before implementation starts, you pick.
Now the shape, open questions:

**1. What's the job of this card — why does it exist?**

**User:** it's the reason you open the app today. habit anchor.

**2. Walk me through the moment: user opens the app, sees the card — what
happens, in your head, start to finish?**

**User:** they see today's hand, it feels like an event, they tap, they
play it like a normal puzzle, they get a result, the card shows done and
teases tomorrow. one a day, no grinding.

**Interviewer:** That's the journey — writing it as you said it. Three
things your walk implies that I want explicit:

- "Feels like an event" → distinct art treatment (the mock gate covers
  what that means).
- "Like a normal puzzle" → existing puzzle player, no new mechanics.
- "Shows done and teases tomorrow" → the card has a done-state; it
  doesn't disappear.

Anything wrong in those three?

**User:** no that's right.

**Interviewer:** Then the journey map — a bigger feature usually creates
more than one journey, and this one creates three. All go in the pack:

1. **Daily play** — open → see today's card → tap → solve → done-state.
2. **Same-day return** — open again after solving: card sits in
   done-state, no second hand.
3. **Next-day reset** — card is fresh again at local midnight.

Anything about journeys two or three that isn't obvious?

**User:** no. midnight local is right.

**Interviewer:** Where we are so far, then two more shape questions:

| Area | Decided so far |
|---|---|
| Job of the card | Habit anchor — the reason to open the app today |
| Done-state | Card flips to done + teases tomorrow; never disappears |
| Journeys (3 mapped) | Daily play; same-day return; next-day reset at local midnight |
| Visuals | No mocks; daily-quest energy as reference; mock gate pending |

**3. Who gets it — everyone including free users, or is the paygate
involved?** (Flagging: if free users see it locked, that's a paygate
change, which is currently out of scope.)

**User:** everyone. paygate untouched.

**4. Does it touch the real streak, or is it its own little counter?**

**User:** own counter. real streak untouched.

**Interviewer:** Both recorded as hard requirements — and both keep this
project off two out-of-scope surfaces (paygate, streak logic), which keeps it
small. One thing your answers raise that I can't answer from what I've
read so far: how the daily hand actually gets picked. Give me a few
minutes with the puzzle-serving code.

*Investigates: how puzzles are tagged, served, and whether anything can
mark a hand as "today's."*

**Interviewer:** Back — findings are in the pack. Puzzles are tagged by
difficulty and street, and served per-user by a rating-matched picker;
nothing anywhere marks a hand as "today's." That raises two questions I
couldn't have asked before looking:

1. Is the daily hand the same for everyone that day, or matched to each
   player's level like normal puzzles?
2. Auto-selected by rules, or a hand-picked queue someone curates?

**User:** same hand for everyone — that's what makes it an event.
auto-picked but it has to be solvable at every level.

**Interviewer:** Recorded: one global daily hand, auto-selected with a
solvable-at-every-level constraint — that constraint is real work and goes
in as a hard requirement. Scope knife — MVP as I'll write it: card + one
global daily hand + done-state + own counter + distinct art (mock-gated).
Explicitly NOT in: push notifications, share button, gems/reward hook,
history screen, difficulty tuning. Say the word to move any in.

**User:** notifications eventually but not now.

**Interviewer:** Deferral ledger: notifications = intended later, not now.
Proof — you usually want the full grid for anything user-facing. Proposal:
sim automation covering card-appears, solve flow, done-state, midnight
rollover, fresh install; plus before/after home-screen screenshots in the
PR. What's missing from that grid?

**User:** what happens with no connectivity. and the card better not shove
the lesson rail around.

**Interviewer:** Both added: offline behavior (needs one answer — what
should the card show offline? I'll bring options with the mock round) and
a layout requirement — card insertion must not reflow existing rail
content. Checkpoint: sign off now with the mock gate pending, or spend five
more minutes on done-state copy and edge details?

**User:** sign off. copy and the offline thing both come with the mocks.

**Interviewer:** Standard setup + attendance?

**User:** standard. around.

**Interviewer:** Decision table — is this good?

| Area | Decision |
|---|---|
| Outcome | Daily challenge card: the reason to open the app today |
| Journeys (3 mapped) | Daily play (see hand → tap → solve → done-state); same-day return (done-state holds); next-day reset at local midnight |
| Visuals | No mocks; reference = daily-quest energy, our look; **mock gate: you pick from 2–3 options before implementation** |
| Audience | Everyone; paygate untouched (out of scope) |
| Streak | Own counter; real streak untouched (out of scope) |
| Daily hand | Same for everyone; auto-selected, solvable at every level |
| Layout (hard) | Card must not reflow existing rail content |
| Non-goals | Push, share, gems hook, history screen, difficulty tuning |
| Deferral | Notifications — intended later, not now |
| Test grid | 7 cases incl. offline + fresh install; before/after shots in PR |
| Open (parked by you) | Offline card display + done-state copy ride with the mock round |
| Execution | Standard |

**User:** good — mocks first, then run the mini plan

**Interviewer:** Mock round first, then `$arch-mini-plan` with the pack.

*Moves: visuals asked first and the answer reshaped everything downstream;
the journey came from the user narrating with the agent extracting
implicit requirements; an investigation cycle produced the two best
questions of the interview; "special" became a human approval gate instead
of an adjective.*

---

## Example 4 — the quick lane (small repair)

**User:** the settings screen crashes when you background the app
mid-scroll. fix it.

**Interviewer:** Quick lane — educating briefly on the crash logs and that
screen's lifecycle handling first. *(returns)* Facts: reproducible in the
logs, one screen, looks contained. Three questions, one round:

1. Proof bar: regression test, or do you want sim automation reproducing
   the background-mid-scroll sequence? (Lifecycle bugs have slipped past
   plain tests here before — your call.)
2. I found no other screens with this crash signature in the logs — do
   you know of any I should include anyway?
3. Standard setup, straight to conductor, no full plan?

**User:** sim automation. just settings. yes.

**Interviewer:** Quarter-page pack written. The table — good to dispatch?

| Area | Decision |
|---|---|
| Outcome | Settings screen survives backgrounding mid-scroll |
| Proof | Sim automation reproducing the sequence + fix |
| Scope | That screen's lifecycle handling only; bigger = comes back as a question |
| Plan step | None — straight to conductor, as you just said |

**User:** go

**Interviewer:** Dispatching.

*Move: proportionality — but even the quick lane asks its three questions
instead of deciding, and still closes on a table.*

---

## Example 5 — proxy mode (the user leaves, a model stands in)

*Continuation of an interview like Example 3, midway through.*

**User:** I'm going to bed. have fable answer the rest as me. nothing that
changes what users see without flagging it for morning

**Interviewer:** Proxy engaged: a clean Fable session answers as you —
armed with the pack so far, your north stars, and your standing doctrine.
Rules per your instruction: user-visible decisions get provisional answers
plus morning flags; everything else the proxy settles for real. The proxy
gets the same open questions you would have — it doesn't get to
rubber-stamp my suggestions either.

*Overnight, in the decision log:*

- Q: what should the card show when the day's hand fails to load? →
  **[PROXY-fable]** retry once silently, then the card's existing
  empty-state — no new error UI. *(final — introduces no new UX)*
- Q: does the counter survive reinstall? → **[PROXY-fable]** no —
  device-local, consistent with practice history. *(final)*
- Q: done-state copy? → **[PROXY-fable]** drafted 3 options in app voice.
  *(provisional — user-visible, flagged)*

**Interviewer (morning):** While you were out: 7 questions resolved — 5
final by proxy, 2 flagged for you: (1) done-state copy, pick one of the
three drafted options; (2) confirm the proxy's empty-state reuse for load
failures. Nothing else outstanding; the run never stopped.

**User:** first option. confirmed.

**Interviewer:** Both final, decision log updated.

*Moves: the proxy answers open questions under the same rules; its answers
are labeled and auditable; the morning cost was two genuinely-user
decisions.*

---

## Example 6 — "build this" (three words and a screenshot)

**User:** build this *(screenshot: a competitor app's shareable
hand-replay card)*

**Interviewer:** Before I ask you anything I'll go figure out what "this"
is and what it would mean here — what's in the image, what we already have
that's close, what it would touch. Back shortly.

*First cycle: reads the screenshot, maps existing replay and share
surfaces, checks how hands render outside the table view.*

**Interviewer:** What I found, now in the pack: the screenshot is a share
card — a finished hand rendered as a static image with hero cards, board,
pot, and a result line, sized for a social post. On our side: we render
hands in the replayer, we have no image-export path anywhere, and our
share button sends a plain text link. Nothing decided. First question,
because it changes everything downstream:

**What's the job — growth (hands showing up where non-players see them),
or a feature for existing users to save their hands?**

**User:** growth. i want hands showing up in group chats.

**Interviewer:** Group chats means the card is the product and link
previews matter. I don't know what our links look like when pasted into a
chat today — give me a few more minutes.

*Second cycle: checks link-preview metadata end to end.*

**Interviewer:** Found it: our links unfurl as the generic app icon with
no preview image — so even a beautiful card dies in a group chat today.
The questions that only exist because I looked:

1. Share from where — end of a hand, the replayer, or both? (End-of-hand
   is the emotional moment; the replayer is more surface area.)
2. The card itself: is that screenshot the target look, or reference-only
   with our brand doing its own thing?
3. Does fixing the link preview ride along as a requirement, or is the
   image file itself enough for group chats?

**User:** end of hand only for v1. reference only — ours looks like us.
and yes the preview fix is part of it, otherwise what's the point.

**Interviewer:** All three recorded — the preview fix goes in as a hard
requirement with your reasoning attached. Continuing the normal walk from
here: journey maps (there are at least two — sharing a hand, and a
non-player tapping what lands in the chat), the grid, mocks for the card,
then the decision table.

*The point of this example: three words in, two investigation cycles out,
and every question the interview asked existed only because it went and
looked. "Build this" was never transcribed as a requirement — it was
decompiled into ones.*

---

## Counter-examples (the failures these examples avoid)

> ~~Ramp up, then return with: "Here's the plan I drafted — correct
> anything wrong."~~ → Education returns facts and a blank template. Pack
> content enters only as the user's answers, approved derivations, or
> confirmed defaults. A pre-filled draft is a pile of decisions the user
> never made, formatted to be rubber-stamped.
>
> ~~"For C8, should the retry budget be 2 or 3?"~~ → The agent decides
> from first principles, records it as an owned assumption with a one-line
> rationale, and moves on.
>
> ~~"What should `_resolveStreakWindow()` do when the offset is stale?"~~
> → Never ask about a symbol. If the question is real it becomes: "if the
> app and the server disagree about what day it is, who wins?" — and only
> if the answer changes what users see.
>
> ~~Fifteen sequential questions, each spawned by the last answer~~ → The
> must-always-know list walked breadth-first, budgeted follow-ups,
> checkpoints offering depth, "good enough" always accepted, always ending
> with the decision table and the assumption list.
>
> ~~"R1 is done, R2 is blocked, see Q3"~~ → The agent never invents its
> own codes either. Requirements are said in words and referred to by name
> ("the delete-the-old-path requirement") in tables, summaries, and
> follow-ups alike. Plain numbered lists are fine; alphanumeric shorthand
> is not.
>
> ~~Multiple-choice everything~~ → Options with a recommendation are the
> fallback (small confirms, defaults, sharpening), never the lead for
> intent, requirements, UX, or architecture. The user's thinking comes
> first.
>
> ~~Sign off silently and auto-run the next skill~~ → The close is always
> two gates: the decision table ("is this good?"), then "ready for me to
> run the plan step?" — where a bare yes runs `$arch-mini-plan` and a
> sentence of steering runs exactly that instead.
>
> ~~"The test grid will come to you for approval with the pack."~~ →
> Everything is approved up front. The grid is built on the spot and
> approved or edited in the flow; "later" exists only for items the user
> explicitly parked.
>
> ~~"Recorded: 'build this.' Next question:…"~~ → Never transcribe what
> you don't yet understand. Go figure out what the words mean in this
> codebase, write the findings into the pack, and return with the
> questions those findings raise. One-shot linear interviews produce
> dictation; the loop produces understanding.
