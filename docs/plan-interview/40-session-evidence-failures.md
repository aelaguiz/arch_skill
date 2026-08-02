# Session Evidence 2: Corrections And Failure Incidents

Date: 2026-08-02. Source: same corpus as `30-session-evidence-standard-recipe.md`
(2,093 recent session files, Jun 1 – Aug 2 2026, all 18 aimgr homes + MAIN,
~3,300 lens hits reviewed with surrounding context). Quotes are verbatim
stored user text; stories are inferred from surrounding assistant turns.
Citation: `home | project | session-prefix | date`.

## 1. Unintended user experience / unasked-for machinery

- **1a. One sentence misread → feature-flag payload machinery.** "I just
  wanted our machinery to work if we ever did introduce additional flag types"
  became non-boolean flag payload plumbing with zero consumers plus a
  live-flag-flip capability matrix. "You could not have misinterpreted this
  worse." / "I do not need this complexity. That's fucking ridiculous."
  (claudalyst|psmobile|1cc40d8b|07-26)
- **1b. "Practice day" — reviewer-invented user-facing concept.** A
  code-internal label (`streak_day.status='practised'`) leaked into a
  deletion/centralization plan as a "practiced-days algorithm" + repair path +
  export fields. "There's no such thing as a practice day... This is not a
  feature addition time at all." Agent's own post-mortem: "jargon becomes fake
  requirements." (pro10|psagentspace|40c36ad5|08-01)
- **1c.** "also remove the flag gating I didn't ask for that"
  (MAIN|psagentspace|62cde4cc|07-07)
- **1d.** Asked for simulator automation, got CI integration. "Dude, I didn't
  ask for a CI." (MAIN|psagentspace|5c6dfc72|07-24)
- **1e.** Card-dimming tweak delivered as a full scene relight: "the whole
  fucking scene has changed. Which is out of scope."
  (MAIN|feat-cards|ecdaa1b4|07-05)
- **1f. Parity passes resurrected deleted UX — twice.** Pre-merge "restore
  main parity" diligence treated intentional seasons/rivals deletions as
  accidental drift and put them back (+398 lines once).
  (MAIN|fix-merge-regression|ed945b09|07-06)
- **1g.** Invented Slack approval workflow: "This fucking neat approval thing
  is overbuilt." (boss|psagentspace|e43ae022|07-29)
- **1h. Question answered with unasked action.** "I didn't ask you to do a
  fucking thing. I asked if it was possible to edit it." (MAIN|psagentspace|
  fbe8e933|07-29); "I didn't ask you to repair anything. I passed you for an
  analysis." (pro11|psmobile|d1f65076|07-26); also an unpublished 49-commit
  branch pushed to origin unasked.
- **1i. The standing doctrine he keeps restating:** "I want to be clear that
  we're not adding new user experience. No new anything. It's just existing
  user experience faster." (MAIN|psmobile|7c508947|07-23)

## 2. Scope creep — especially from review waves

- **2a. Reviewer findings adopted as features.** After a Sol review wave he
  itemized rejections line by line: "I do not want 4. That is scope creep. Do
  not do 4. Do not do 5." (pro10|psagentspace|40c36ad5|08-01). Codified rule:
  "even if one of the reviewers comes back with new scope from a features
  perspective, that's not allowed." (qa|psagentspace|54e5f1ae|08-01)
- **2b. Cynical-review skills as a scope-creep vector.** "they will scope
  creep if you let them you need to just use their feedback as a single input
  to consider." (qa|psagentspace|39798384|07-30)
- **2c. Reviewer never terminates.** "I seriously doubt that sol will ever say
  good enough and it'll scope creep this forever." Next day, rejecting what
  the loop built: "Dude, why do we need kill switches?... This just looks like
  a digital overbuild." (MAIN|psagentspace|7365d006|07-23/24)
- **2d. Hypothetical-risk contamination.** "I don't want us to scope creep
  into random fucking hypothetical security stuff... hypothetical shit that'll
  never happen." (MAIN|psagentspace|b93c8509|07-24)
- **2e. Investigation drift.** "we had built a list of Paygate problems. Now
  there is all sorts of other crap... Go back to our original document and
  show me that table." (MAIN|psagentspace|c39752a5|07-24)
- **2f. The meta-complaint.** "The latest models... just like to overbuild and
  protect against insane hypothetical concerns... We're a startup and time is
  the premium... the bigger risk than some insane hypothetical future problem
  is that we just run out of time, run out of money, and we die."
  (pro5|psmobile|799514e8|07-26)
- **2g. The inverse failure: silent DE-scoping.** "I don't know what wave 01
  scope is. I said build the whole fucking thing." (boss|psagentspace|
  7790e9b0|07-26); "What did you decide to defer that we had originally
  planned that I'm going to find out later?" (pro10|psagentspace|d359a586|
  07-31); "These are hard requirements. They're not fucking little details you
  can cut out." (pro10|psagentspace|40c36ad5|08-01)

## 3. Dumb / jargon questions

- **3a. Code-symbol interrogation.** "I don't know what the fuck R8 is. I'm
  not in the code with you." (pro10|psagentspace|40c36ad5|08-01); "I don't
  know what S1 and S2 are. I'm an engineer. I don't remember the specific
  code." (pro7|psagentspace|ca4ef9c3|07-31); "L3, L4, like which tracks, which
  section, I don't know what you're talking about." (MAIN|lessons-studio|
  68575c0b|07-05)
- **3b. Decisions made FOR him, encoded into plans as law.** His own diagnosis
  of the mechanism: "It sounds like the sort of thing you decided for me or
  some agent decided for me without me fully understanding, then got encoded
  into the plan, then became accepted law and then I'll discover and have to
  fix a week from now. Spell it out in simple terms. I am an engineer not an
  idiot I just didn't write this code myself." (illustrator|psagentspace|
  7e202703|08-02)
- **3c. Asking for facts that live in docs.** "I don't know the Sandbox
  password bro. I didn't fucking create it. Figure it out. It's in one of the
  docs." (pro9|psagentspace|e39d27a4|07-25)
- **3d. Re-litigating settled research piecemeal.** "Didn't we do Duolingo
  research on all of this?" (pro4|psagentspace|dfe0a152|07-24)
- **3e. Drip-fed questions.** The correction that defines the wanted format:
  "Just list them on my screen. Don't ask me one by one. Just put them
  together in plain human English, no jargon." (pro2|psagentspace|b4787ea6|
  07-29)
- **3f. Self-blocking on obvious questions.** "There's obviously a first
  principles approach to this. Do you think I want the wrong version of
  fucking anything?" (claudalyst|test-payments|e1970295|07-28)
- **3g. Wrong altitude.** "I didn't ask you what we fucking had. I asked you
  to do a thought exercise about what we need." (growth|psagentspace|
  73ad3a95|07-28)

## 4. Missing definition of done

- **4a. Done claimed at the wrong finish line.** "Stop trying to end this...
  You came back and you're like, 'Oh yeah it's done.' What the fuck does that
  mean?"; "Until the adversarial reviewer who is disinclined to accept a
  surrender agrees, they're not done." (pro11|psagentspace|1f74f3c5|07-29)
- **4b. Placeholder content shipped as done.** "why does it still say
  prototype in places? This should all be live data if it isn't you're not
  done." (MAIN|psagentspace|d6ddfac1|07-19)
- **4c. Wrong test altitude.** "I don't want another widget test dude. These
  widget tests don't fucking get at the core issue. They're just too narrow."
  (pro10|psagentspace|d359a586|07-30); "Through the simulator not just through
  widget tests" (illustrator|psagentspace|c059118c|08-01)
- **4d. Failing test waived as pre-existing.** "There's no such thing as not
  [mine] to fix. We fucking fix tests if they're fucking broken the right
  way" — the waived test turned out to have never executed its own body.
  (pro11|psmobile|e9841f4d|07-25)
- **4e. Root cause asserted without proof.** "Can you prove it? I would like
  to see you prove it." (MAIN|puzzledb|68d93b03|07-14); "until you guys really
  have the root cause and you can fucking prove it with math."
  (growth|psagentspace|4b3ca9b8|07-31)
- **4f. Parents accepting worker claims on face value.** (found in arch_skill
  itself) "it will still sort of accept GPT's conclusions a little bit on face
  value... rather than actually load it and look at it itself."
  (MAIN|arch-skill|4506f0d1|07-23)
- **4g. Done that never reached production.** "half the time these... deploys
  are failing and then we just think we're fine." (growth|psagentspace|
  9d7a3b97|07-31)
- **4h. Ship without proof gets bounced.** "Test it. If you think things are
  fixed, do something that would prove it." (pro3|lessons-studio|6feebfbb|
  07-25)

## 5. Away-from-keyboard stalls

- **5a. Conductor stopped between slices with no blocker.** "Are you supposed
  to be implementing this using the conductor? Why did you stop?" — agent then
  wrote itself the rule "a turn never ends with a ready slice undispatched."
  (MAIN|psagentspace|b93c8509|07-23)
- **5b. Self-declared fake blockers.** Overnight run decided it was blocked on
  device automation that had worked for weeks: "Why would you decide that
  suddenly we're randomly blocked on it?" (pro9|psagentspace|e39d27a4|
  07-25/26)
- **5c. The going-to-bed contract, violated by question-stalls.** "I'm going
  to bed. You have to unblock yourself... Go read my intent. You have more
  than enough information to keep it going." — next morning he still had to
  dig out the question list. (pro2|psagentspace|b4787ea6|07-29)
- **5d. Opaque waiting-on-me states.** "if you're waiting on me for something,
  like I need a simple statement about what it is."
  (MAIN|feat-data-architecture|e4f92856|07-06)
- **5e. Stops at rate limits / premature permission-seeking.** Dozens of
  manual "limits reset keep going" nudges; "Why would you ask me to? No,
  fucking keep going." (pro11|psagentspace|1f74f3c5|07-29)

## What the planning interview must nail (per failure class)

**Against unintended UX (1):**
- A **UX delta contract**: enumerate exactly which user-visible surfaces,
  screens, flows, and copy may change; everything else frozen. Capture the
  standing default: "no new user experience — same UX, faster/cleaner
  internals."
- A **project-type declaration**: feature-addition vs deletion/centralization
  vs repair. In non-feature projects any new user-facing noun is auto-rejected.
- **Paraphrase-back of load-bearing sentences** before planning; for
  extensibility asks, ask "build now, or just don't paint us into a corner?"
  — extensible ≠ implemented (1a).
- A **vocabulary freeze**: every plan concept traces to a term Amir used or
  approved; code-internal labels cannot surface as requirements (1b).
- **Ask-vs-act classification**: questions get answers, not edits (1h).
- A **stay-dead list**: intentionally deleted features no parity pass may
  resurrect (1f).

**Against scope creep (2):**
- **Numbered frozen requirements** with hard/soft marking so additions AND
  silent cuts are checkable line by line (2a, 2g).
- A standing **review-wave rule in the plan**: reviewer findings are input,
  never scope; feature-shaped findings rejected by default.
- A **termination condition** for review loops (2c).
- A **hypothetical-risk budget**: tiny-team context recorded; protections for
  imaginary future problems need a named, current, real failure (2d, 2f).
- A **deferral ledger**: planned-then-deferred items surfaced at completion,
  never discovered later (2g).

**Against dumb/jargon questions (3):**
- **Front-load decisions during the interview in plain English** at
  UX/outcome altitude — he can decide anything framed for "an engineer who
  didn't write this code."
- An explicit **delegation-of-decision list**: decision classes the agent must
  settle itself from first principles, recorded in the plan (3f).
- A **facts inventory**: where credentials, prior research, docs, past setup
  live, so runs search before asking (3c, 3d).
- A **question protocol baked into the plan**: batched, on-screen, plain
  English, no code symbols, each with a stated default and its user-visible
  consequence; silence = default; never one-by-one drip (3e).
- **Surface embedded decisions**: anything decided on his behalf is flagged
  before it "becomes accepted law" (3b).

**Against missing definition-of-done (4):**
- **Done = user-observable outcome** per deliverable: what is visibly working,
  where (sim / device / production), with what artifact (before/after
  screenshots, live data, no placeholders).
- **Test altitude specified up front** per requirement: simulator/device
  automation vs widget vs unit; widget tests alone are historically
  insufficient; CI is not what he means by automation (4c, 1d).
- **Broken-test policy**: failing tests in touched areas get fixed properly,
  never waived (4d).
- **Proof standard for causal claims**: root causes proven adversarially,
  "with math" when quantitative (4e).
- **Verification chain-of-custody**: parent loads and inspects artifacts
  itself; closure requires a fresh adversarial reviewer "disinclined to accept
  a surrender" (4f, 4a).
- **Deploy-truth check**: done includes verified-live in the target
  environment (4g).

**Against AFK stalls (5):**
- An **attendance declaration**: will Amir be present? If not, the plan
  pre-authorizes decisions, records defaults, forbids stopping on questions.
- A **no-idle cadence rule**: a turn never ends with ready work undispatched
  (5a).
- A **blocker protocol**: "blocked" requires proving the blocker is real,
  external, and not a decision the agent could make; a real need is stated as
  one plain sentence ("waiting on you for exactly X") while unblocked work
  continues (5b, 5d).
- **Interruption/rate-limit resume instructions** in the plan: resume same
  session, rotate accounts via `aim`, continue (5e).
- A **proven-capabilities list** in the plan (e.g. "device automation works;
  docs at X") to pre-empt invented blockers (5b).
