# PLAN: `plan-interview` — Full End-To-End Build Plan

Date: 2026-08-02 (rev 8 — complete build plan, all calibration learnings
encoded). Status: for Amir's approval, then execution. Doc pack:
`docs/plan-interview/` (00 intent + calibration record, 10 suite survey,
20 external research, 30/40 session evidence, 50 hypothetical interviews).

## TL;DR

Build `skills/plan-interview/`: a prompt-first skill that, given an opening
ask, educates itself (facts and a blank template, never a pre-drafted plan),
then runs the interview as a **loop, not a line** — open questions framed by
evidence and Amir's own history, investigate-and-return cycles where his
answers send it back to the code, journey maps and the full test grid built
and approved inside the interview — closing with a decision table and a
steerable plan-step gate defaulting to `$arch-mini-plan`. The interview
transcripts in this doc pack ship inside the skill as its examples. The
build itself runs under `$skill-authoring` with `$prompt-authoring` applied
to every piece of skill prose.

## North Star

- **Claim:** every conducted run starts from an Intent Pack precise enough
  that nothing user-visible changes unless the pack names it, review
  findings triage mechanically against a frozen boundary, an
  away-from-keyboard run never stalls on a question the pack could have
  answered, done-ness and required proof are stated before dispatch, and
  every decision in the pack is one Amir made or approved.
- **In scope:** one new skill package (SKILL.md + references, including the
  interview examples); routing entries in `AGENTS.md`, `README.md`, and
  `arch-skills-guide`; install; one live validation run.
- **Out of scope:** changes to conductor, arch-*, cynical skills,
  plan-audit; any runner, script, controller, or state machine;
  auto-invoking downstream skills without the plan-step gate.
- **Definition of done:** `npx skills check` passes; a clean cold reader
  can run the skill from the package alone; the package carries the
  interview examples in self-contained form; routing and README updated;
  one real interview produced a pack that `$arch-mini-plan` turned into a
  plan without re-asking anything the pack answered, with zero decisions in
  the pack Amir never made.
- **Invariants:** prompt-first; plain English to Amir — never code symbols,
  never invented shorthand; the interview always advances; the skill never
  decides intent, requirements, UX, or architecture on Amir's behalf — it
  elicits, derives with approval, or defaults with confirmation.

## What this iteration process taught us (encoded, not commentary)

Building the mock interviews and revising them through eight corrections
was itself the cheapest validation the skill will ever get. Each failure I
made while authoring mirrors a failure class the skill exists to prevent —
proof the anti-patterns are real attractors, not hypotheticals:

1. Rev 1 pre-drafted the plan from one sentence and asked confirming
   questions on top → became the **presumptive drafter** anti-pattern.
2. Rev 4 caught me inventing my own shorthand (R1/Q3) while writing the
   no-jargon skill → the jargon ban must cover the skill's own output.
3. Rev 5 caught the grid deferred to "later with the pack" → everything is
   approved up front; "later" exists only for items Amir explicitly parks.
4. Rev 7 caught the one-shot linear shape → the investigate-and-return
   loop is structural, not optional.

Build-process rules derived from this:

- **Mock transcripts before code.** Doctrine changes get validated by
  showing transcripts, not by shipping and discovering. The examples file
  in the package is therefore load-bearing, and Phase 5 feedback updates
  the examples first.
- **Corrections arrive incrementally; keep a binding record.** The
  calibration log pattern (00-intent-and-notes.md) worked; the skill's
  validation loop reuses it.
- **Self-review must target the skill's own failure modes** — drafting,
  shorthand, deferral, transcription — not just generic quality.

## The three anti-patterns (named in the skill itself)

1. **The driller.** Ever-deeper in-the-weeds questions until Amir gets fed
   up; never advances. Fix: breadth-first walk of the must-always-know
   list, ~2 follow-ups per topic in the broad pass, checkpoints that offer
   depth instead of imposing it, unresolved details become owned
   assumptions with recommendations.
2. **The presumptive drafter.** Drafts the plan from the opening sentence,
   then runs a confirmation ritual. The read-back format anchors Amir into
   rubber-stamping decisions he never made. Fix: education produces facts
   and a blank template, zero decisions; content enters the pack only as
   his answers, approved derivations, or confirmed defaults.
3. **The transactional transcriber.** One-shot linear pass: ask, record,
   freeze. He might say no more than "build this" — recording it is not
   understanding it. Fix: the investigate-and-return loop — answers
   trigger investigation, findings grow the pack, the skill returns with
   questions it couldn't have known to ask before looking. Cycles repeat
   until the must-know lines are understanding, not dictation.

## The Must-Always-Know List (the interview's backbone)

Every pack has a written line for each item, even when the line is "none"
or "standard." Complexity scales how much discovery an item gets — never
whether it exists. Tags: **[you]** elicited by open question, **[default]**
standing answer with one confirm, **[derived]** agent works it out from
evidence and Amir approves.

**Intent**
1. What are we doing — the outcome in Amir's words. [you]
2. Why / why now — the problem, first principles. [you]
3. Success signals — how anyone would observe it worked. [you]

**Shape**
4. Project type — feature / centralization+deletion / repair /
   investigation; decides which standing rules bite hardest. [derived]
5. UX delta — exactly what users see change; everything else frozen;
   new-UX-or-not declared; stay-dead list; **user journey map required
   wherever the work touches a journey** (mature product: usually the
   existing journey confirmed unchanged or the tweak marked on it; bigger
   features map every journey they create, sometimes several); **visual
   references** — do mocks, target images, or reference apps exist, and
   where? New UX with no visuals gets an offered mock-approval gate. [you]
6. Requirements — a plain numbered list, hard/soft marked, each stated in
   words and referred to by name afterward, never by code. [you, agent
   structures]
7. Non-goals + scope boundary — what's explicitly out; the triage line for
   reviewer findings; the deferral ledger. [you, agent proposes candidates
   from discovery]

**Build**
8. Architecture requirements — Amir's constraints (one owner, no duplicate
   patterns, what gets deleted, cutover-vs-compat), asked with framing:
   "typically your requirements here are X and Y — what are you
   thinking?" [you]
9. Test grid + proof — full grid with edge cases, right altitude per
   requirement (sim/device automation vs widget vs unit), where proven
   (sim / device / production), artifacts required (before/after
   screenshots, live data). **Built and approved inside the interview,
   before freeze — part of the approval, never a follow-up.** [you set the
   bar, agent builds the grid on the spot, you approve or edit it there]

**Finish**
10. Definition of done — the observable finish line and who signs off (an
    adversarial reviewer disinclined to accept a surrender). [you]

**Run**
11. Execution policy — models per role, worktree/sim pins, review waves +
    caps, PR contract, aim rotation. [default]
12. Autonomy contract — attendance, delegated decisions, question
    protocol, what counts as a real blocker. [default + one question]

**Residue**
13. Open decisions & assumptions — every remaining unknown with an owner
    (Amir vs agent) and a default. Nothing unwritten. [derived, listed at
    freeze]

## Standing Core Requirements (baked in, not asked)

From the session evidence (`30-session-evidence-standard-recipe.md`) —
written into every Intent Pack by default; the interview mentions them in
one line and asks only about deviations:

1. No new user experience unless this pack names it; same UX,
   faster/cleaner internals is the standing default.
2. No duplicate patterns — one source of truth, one way, never old+new.
3. Reduce code; prefer subtraction over addition.
4. Delete, don't quarantine.
5. No hypothetical overbuild — tiny team, wall-clock is the scarcest
   resource; imaginary future problems need a named, current, real failure.
6. Reviewer findings are input, never scope; review rounds capped.
7. Proof at the right altitude, wall-clock efficient; new automation joins
   the default suite; broken tests get fixed properly, never waived.
8. Human-readable surfaces — labels/copy stay human; PRs carry before/after
   journey screenshots as embeds plus an exhaustive user-facing change
   list.

## Standing Execution Policy (defaults, one confirm)

| Role | Default |
|---|---|
| Implementation | Codex `gpt-5.6-sol` at `ultra` via `$conductor` fleet |
| Three cynical reviews | Terra (`gpt-5.6-terra`) xhigh, new clean sessions |
| Adversarial reviewer | Fable xhigh, ≤2 rounds |
| Optional extra cheap reviewer | Luna Max |
| PR authoring + follow-through | Sol Ultra delivery worker, never the parent |
| Secrets/keys/credentials | Opus 5 sub-agent, scoped to that step |
| Rate limits | `aim codex use` rotation + exact-session resume |
| Environment | Worktree off origin/main pinned in the doc; for psmobile a new renamed sim pinned in the doc; one branch, one PR |
| Plan review before dispatch | Sol Ultra and/or Fable xhigh, 1–3 rounds cap |

## The Intent Pack (output artifact contract)

One directory per effort in the target repo: `docs/<SLUG>_INTENT/` with
`INTENT.md` as the single authoritative doc plus `research/` for education
evidence (facts briefings, journey inventories, key-file maps, visuals).
`INTENT.md` sections map 1:1 to the must-always-know list, plus a decision
log (every question and answer, proxy answers marked, rejected
alternatives, flagged derivations) and an approval-and-freeze block that
maps onto the suite's Scope and Simplicity Contract.

The pack does **not** contain target architecture — that stays with
`$arch-mini-plan` / `$arch-step`. Architecture *requirements* (item 8) are
constraints, not designs. Acceptance bar: the No Prior Knowledge Test —
an agent with zero repo familiarity plus this pack could plan and execute
without asking Amir anything.

## Runtime workflow (what SKILL.md teaches)

1. **Fit gate.** One-sentence-diff work skips the skill; small-but-real
   work takes the quick lane (brief education, one batched round with
   evidence-backed confirms, quarter-page pack). Full lane for
   conductor-sized work.
2. **Orient.** Restate the ask; ask the 1–3 orienting questions needed to
   aim education (which surfaces, standalone vs part of something bigger).
   No decisions.
3. **Educate.** Parallel clean read-only native children per the shared
   orchestration policy: similar features and reusable patterns; authority
   paths; the user journeys actually touched; git/PR history; docs, prior
   research, settled decisions, facts inventory; test/automation surface;
   what Amir asked for in past similar efforts. Output: `research/` files,
   a "what I found" facts briefing, a **blank Intent Pack template**.
   Explicitly no plan, no pre-filled answers, no decided shape.
4. **Interview — the loop.** Walk the must-always-know list
   breadth-first, but the walk is a loop, not a line:
   - Open questions first, framed with evidence and his history
     ("typically your requirements here are X — what are you thinking?").
     Options with a recommendation are the fallback — when he asks, is
     unsure, or an answer needs sharpening — never the lead for intent,
     requirements, UX, or architecture.
   - **Investigate-and-return** is a first-class move at any point:
     "give me a few minutes to figure out what that means." Findings are
     written into the pack; the return brings questions that could not
     have been asked before looking. Multiple cycles are normal; each
     deepens one area, then the walk advances.
   - Journey maps produced in-flow wherever a journey is touched; visual
     references asked for on any UX work; the full test grid built and
     approved on the spot; standing doctrine and execution policy as
     one-line confirms; discovery facts surface as scope questions, never
     as included work.
   - Plain English only — no code symbols, no invented shorthand;
     requirements referred to by name. Progress restated each turn;
     ~2 follow-ups per topic in the broad pass; checkpoints offer depth
     ("freeze now, or take N more minutes on these areas?"); "good
     enough" always accepted, with assumptions listed.
5. **Proxy mode.** At any point: "have <model> answer as me." A clean
   child (native, or via `$agent-delegate` when a specific model is the
   point) answers under the same open-question rules, armed with the pack,
   his north stars, and the phrasing bank. Proxy answers marked
   `[PROXY-<model>]`; user-visible decisions provisional and flagged
   unless explicitly delegated; skimmable morning summary.
6. **Hardening.** Self-review targeted at this skill's own failure modes:
   any decision with no answer/approval/default behind it (drafting), any
   invented shorthand (jargon), any "coming later" not explicitly parked
   by Amir (deferral), any answer recorded but not understood
   (transcription) — plus placeholders, contradictions, vague adjectives,
   requirements with no proof line, must-know items with no line.
   Optional pre-mortem pass; findings become questions or assumptions,
   never silent scope.
7. **Close — two gates.**
   - **Gate 1, the decision table.** Everything decided as one clean table
     (area → decision, assumptions marked and owned, the approved grid and
     journey maps referenced). "Is this good?" Feedback folds in before
     freeze. Nothing says "later" except items Amir explicitly parked.
   - **Gate 2, the plan step.** "Ready for me to run the plan step?"
     Default: `$arch-mini-plan` against the pack. A bare yes runs it; a
     sentence of steering (full `$arch-step`, adversarial plan review with
     a named model and round cap, straight to `$conductor`) runs exactly
     that. The handoff carries the no-re-asking reminder.

## Integration contract (no downstream edits needed)

- `$arch-mini-plan` / `$arch-step`: pack items 1–8 plus the freeze block
  are the North Star and Scope and Simplicity Contract inputs; education
  evidence seeds research grounding.
- `$conductor`: item 11 answers the consolidated intake question; items
  6–7 make finding-disposition triage mechanical; item 12 answers "what
  are you waiting on me for."
- `$plan-audit`: a recoverable human baseline. Cynical skills: intended UX
  and scope provenance exist in written form.

## Package plan (built with `$skill-authoring` + `$prompt-authoring`)

```
skills/plan-interview/
  SKILL.md                      # runtime contract: fit gate, orient,
                                # educate, interview loop, proxy,
                                # hardening, two-gate close
  references/
    must-know-list.md           # the 13 items, tags, per-item strong/weak
                                # bar, journey-map and visuals rules
    intent-pack-contract.md     # artifact spec, blank template, decision
                                # log, freeze rules, No Prior Knowledge bar
    interview-doctrine.md       # open-question elicitation, framing from
                                # history, investigate-and-return loop,
                                # budgets/checkpoints, jargon + shorthand
                                # ban, grid-up-front, two-gate close,
                                # proxy mode
    education-contract.md       # researcher lenses, facts-not-decisions
                                # rule, blank-template output, recurring
                                # mid-interview education
    standing-doctrine.md        # the 8 core requirements + execution
                                # policy defaults, with compact provenance
    examples.md                 # the six interviews from this doc pack,
                                # rewritten as self-contained examples
                                # with the annotated counter-examples
```

Authoring rules for the build (from `$skill-authoring` + repo red lines):

- `$prompt-authoring` applied to every file — SKILL.md, references, and
  the education/proxy child briefs the doctrine describes.
- **Examples become timeless.** The six transcripts ship in `examples.md`
  stripped of rev history and process backstory (red line: skill doctrine
  never explains its own development). Annotations stay ("note the moves"),
  provenance goes. The counter-examples section ships with them — it is
  the anti-pattern teaching surface.
- No scripts, no runner, no formal parameter interface. The description
  frontmatter is trigger logic written against the visible peer group
  (arch-mini-plan, plan-audit, conductor, fresh-consult) with explicit
  not-for lanes.
- Self-contained: standing doctrine and defaults live in the package, not
  as pointers into this doc pack; the shared
  `_shared/agent-orchestration-policy.md` is referenced for dispatch
  semantics (education researchers, proxy child) as sibling skills do.
- Description under the 1024-char cap; `npx skills check` green.

## Build phases (end to end)

- **Phase 1 — plan approval (this document).** Amir approves this rev or
  corrects it. Exit: his go.
- **Phase 2 — author the package.** Run `$skill-authoring` (with
  `$prompt-authoring` on all prose) to build the six files above. The
  transcripts get their self-contained rewrite here. Exit:
  `npx skills check` passes; every calibration item from
  `00-intent-and-notes.md` traceably lands in a package file (checked
  item-by-item, all eight).
- **Phase 3 — cold-read validation.** `$fresh-consult`: a clean native
  reviewer reads only the package and answers: could you run this
  interview correctly from the package alone, and does anything in it
  contradict the three anti-patterns it names? Fix findings; re-check.
  Exit: pass verdict.
- **Phase 4 — wire and install.** Routing entry in `AGENTS.md` Skill
  Routing, `README.md` inventory, `arch-skills-guide` mention;
  `make install`; verify the skill resolves on this machine. Exit:
  routing text reviewed, install verified, no other skill edited.
- **Phase 5 — live validation.** Run the skill on the next real psmobile
  or psagentspace effort end to end: interview → pack → `$arch-mini-plan`
  → `$conductor`. Measure: questions Amir got asked downstream that the
  pack should have answered (target 0), decisions in the pack he never
  made (target 0), unintended-UX findings in final reviews (target 0),
  reviewer findings triaged mechanically vs debated. Fold lessons into
  `examples.md` first, doctrine second. Exit: one full cycle plus the
  fold-back.

## Risks and mitigations

- **The skill reproduces an anti-pattern in the wild** → the hardening
  step self-checks against all four authoring failures observed in this
  process; Phase 5 measures the outcomes directly.
- **Markdown factory / waterfall** → pack records intent and proof, not
  designs; quick lane; INTENT.md target ≤ ~300 lines.
- **Spec drift** → pack freezes at handoff; post-freeze changes are human
  decisions in the decision log; the downstream plan owns execution truth.
- **Interview fatigue** → breadth-first map, budgets, checkpoints,
  defaults, "good enough" escape, proxy mode.
- **Example rot** → Phase 5 feedback lands in `examples.md` first, by
  design; examples are the doctrine's test suite.

## Open decisions for Amir (with recommendations)

1. **Name**: `plan-interview` (recommended — sits beside plan-audit /
   plan-implement) vs `intent-interview` vs `deep-brief`.
2. **Pack home**: `docs/<SLUG>_INTENT/` directory in the target repo
   (recommended) vs single flat file.
3. **Standing doctrine home**: inside the skill for v1 (recommended);
   per-repo overrides via AGENTS.md later.
4. **Proxy mode and quick lane in v1**: include both (recommended).
