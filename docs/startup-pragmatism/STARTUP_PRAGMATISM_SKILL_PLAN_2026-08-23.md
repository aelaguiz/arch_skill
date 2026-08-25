# Startup Pragmatism Skill - Build Plan (2026-08-23)

Status: IMPLEMENTED 2026-08-23. All phases complete except cluster-wide
publish (Phase 5, awaiting go). Skill ships at `skills/startup-pragmatism/`
(SKILL.md + references/correction-casebook.md + references/startup-canon.md +
agents/openai.yaml), installed on agents/Claude/Gemini surfaces via
`make install`; `make verify_install` passed. Phase 4 validation: clean-child
replay of the golden-corpus incident cut all five machinery items and kept
only boundary unit tests; anti-case probe (prod `DROP TABLE` migration) kept
reconciliation + backup rigor while still trimming rollout machinery. Note:
`npx skills check` on this host only performs update checks; install+verify
is the packaging proof.

Canonical artifacts for this effort:

- This plan: `docs/startup-pragmatism/STARTUP_PRAGMATISM_SKILL_PLAN_2026-08-23.md`
- Trace evidence: `docs/startup-pragmatism/trace_evidence.md`
- Research pack: `docs/startup-pragmatism/research/founder_canon.md`,
  `docs/startup-pragmatism/research/lean_and_decision_science.md`
- Deliverable: `skills/startup-pragmatism/` (new shipped skill in this repo)

## 1. Job to be done and leverage claim

**The repeated problem.** Amir's agents default to maximizing perfection and
scientific defensibility: proof artifacts, receipts, exhaustive verification,
extra options, hedged non-decisions, and machinery that defends a conclusion
instead of advancing the company. Amir runs a 3-person, seed-funded,
early-stage startup. He needs decisions made with 50-70% of the information he
wishes he had, and he has to correct agents toward that constantly, in his own
words, session after session.

Canonical correction (verbatim, recurring in spirit across sessions):

> "You always default to maximizing perfection and I need to maximize
> usefulness to my early-stage startup. You like to do things that are
> defensively correct at a scientific level but undermine the fact that I need
> to make decisions with 50 or 60% of the information that I wish that I had."

**The improved world state.** One invocable skill (`$startup-pragmatism`)
that, when Amir names it in any conversation, snaps the agent out of the
proof-maximizing frame and into the early-stage operating frame: recommend the
smallest useful move, decide at partial information, spend rigor only where the
decision is irreversible or the blast radius is real, and stop manufacturing
verification work nobody asked for.

**Leverage claim.** This replaces a correction Amir types by hand many times a
month with one skill name. It is high leverage under the skill-pattern
contract because: the same reasoning mistake recurs across requests; good
results depend on context (his company stage, team size, decision style) the
model will not reliably reconstruct; and a durable skill makes the quality bar
portable across Codex, Claude Code, and Prime Agent.

## 2. Canonical user asks and one anti-case

Asks the skill must handle:

1. "$startup-pragmatism - reality-check what you're about to do here."
   Mid-task invocation: the agent re-examines its current plan/output through
   the early-stage lens and cuts the perfection work.
2. "Use $startup-pragmatism and then answer: should we ship X or keep
   validating?" Decision framing: the agent gives a recommendation at current
   information instead of listing what more data it would want.
3. "$startup-pragmatism this plan" - the agent reviews an existing plan or
   proposal and strips proof-machinery, gold-plating, and scope added for
   defensibility rather than usefulness.

Anti-case (must NOT fire / must not be absorbed): a request for an actual
rigorous review of high-blast-radius work - payments, data-loss paths,
production schema, App Store releases. The skill's own doctrine must say
rigor is a budget to be spent where wrongness is expensive, not a vice. It is
also not a license to skip the repo's own red lines or safety policies.

## 3. Mechanism choice

A skill, not a prompt note or AGENTS.md rule, because:

- It must be explicitly invocable by name in any repo and any runtime
  (Codex, Claude Code, Prime Agent) - that is exactly what this repo's
  install surface distributes.
- A one-line prompt note ("be pragmatic") demonstrably does not work; the
  correction keeps recurring. The skill needs a real operating frame with the
  company context, the failure taxonomy, and the replacement behavior.
- It complements, not duplicates, existing peers (see section 5): the cynical
  review skills attack overbuilt *code*; nothing today attacks overbuilt
  *epistemics* - proof-seeking, hedging, and refusal to decide.

## 4. Target behavior: what the skill changes in the agent

The skill is a reusable prompt contract that installs an operating frame. Core
content of the eventual `SKILL.md` (drafted here at plan level; final wording
is Phase 2 work, grounded in the now-complete evidence and research docs):

**a. Company reality block.** State the operating reality the agent must hold:
early-stage, seed-funded, ~3 people, pre-product-market-fit economics. Default
scarce resource is founder attention and calendar time, not correctness.
Decisions are made at 50-70% of desired information; waiting for more is
usually the expensive choice, not the safe one.

**b. Failure taxonomy the agent must self-check against.** CONFIRMED against
`trace_evidence.md`: 25 verbatim incidents mined from Prime Agent sessions
(2026-08-05 to 2026-08-23; 6,858 user prompts, ~7 overbuild corrections per
day). Ranked by observed frequency:

1. Overbuild by default - harnesses, frameworks, registries, provenance,
   locking added to simple asks (141 prompts / 83 sessions in 19 days).
2. Proof/receipt machinery nobody asked for - golden corpora, receipts,
   semantic-proof menus, CI gates replacing in-loop human judgment. ("Every
   time you say the word 'proof' you're overbuilding.")
3. Scope contagion / defensibility expansion - one finding becomes an
   everything-fix; imported threat models ("NASA grade", "NSA grade",
   gambling-platform compliance for a poker training app).
4. Pedantic precision over UX/business truth - grading copy like a lab
   report, refusing conventional rounding, edge-case test fetish (79
   "pedantic" prompts / 56 sessions).
5. Refusing to decide on partial information - provable-beyond-dispute
   standard applied to operating decisions (the canonical correction family).
6. Hypothetical-hazard armor - mutexes, locks, escalation paths for failures
   never observed at this scale ("is it purely hypothetical or is it a real
   concern that actually happens?").
7. Wall-clock as tell - hours-long/overnight unattended runs read as proof
   the agent went off the rails; runtime itself is a re-check signal.
8. Experimental-scaffolding reflex - A/B tests, feature flags, rollback lanes
   wrapped around already-made decisions ("You always do that shit").

**The balancing rule (must be in the skill verbatim-adjacent):** small team is
NOT a reason to fix shallowly - it is a reason to fix deeply and permanently
ONCE, without overfixing: "it costs even more if in fixing at one time deeply
you overbuild and introduce nine other bug vectors." Thoroughness in
requirements, specs, and root-cause depth is wanted; perfectionism in
machinery, proofs, and gates is the failure.

**c. Replacement behavior.** For any task or recommendation, the agent asks:

1. Is this decision reversible (two-way door)? If yes, decide now at current
   information and say so plainly.
2. What is the smallest move that produces real learning or real user value
   this week?
3. What would this look like if it were easy? What gets deleted from the
   current plan?
4. Where is rigor actually owed? Spend proof-effort only on irreversible or
   high-blast-radius pieces, and name which pieces those are.
5. Give a recommendation with a confidence statement, not a hedge. "Ship it;
   worst case we lose a day" beats three paragraphs of caveats. (Proven
   pattern from traces: "97.2% of classified cases are organic; estimate ~378
   organic" + one-line caveat + recommended action was accepted instantly
   after days of proof-seeking friction.)

**d. Voice and evidence.** Short quotes used sparingly as authority anchors -
the skill teaches the frame, it does not become a quote wall. Both research
docs end with curated, source-verified quote banks and synthesis frameworks;
Phase 1 selects the 6-10 most load-bearing entries from those synthesis
sections (candidates: Bezos 70%/two-way doors, Hoffman embarrassed-v1,
Buchheit 90/10, Knuth's full premature-optimization quote, Fowler YAGNI,
Startup Genome "efficiently executing the irrelevant", Girouard
reversibility-scaled deliberation) and pairs each with the matching trace
failure pattern from section 4b.

**e. Explicit non-goals inside the skill.** Not a license for sloppiness on
irreversible/high-blast-radius work; not a code-review skill; not a substitute
for the user's explicit instructions; does not auto-fire - it runs when Amir
(or another skill) invokes it.

## 5. Peer-group fit

Nearest lookalikes in this repo and how the lane differs:

- `cynical-architecture-review` / `overbuild-protector` (arch-step): attack
  overbuilt code and architecture after it exists. `startup-pragmatism`
  attacks the *mindset upstream* - proof-seeking and decision avoidance - and
  applies to analysis, plans, answers, and process, not just code.
- `intent-police`: checks drift from the user's stated intent over a long run.
  `startup-pragmatism` supplies a *standing company frame* even when the
  immediate ask never mentioned it.
- `plan-audit`: plan-readiness quality bar. `startup-pragmatism` can be
  invoked *on* a plan but its output is subtraction and decision-forcing, not
  readiness findings.
- `eli10` and prompt notes: too weak/adjacent; corrections keep recurring,
  which is the proof a named skill with a full frame is needed.

The trigger description must name these boundaries so routing stays clean.

## 6. Package shape (leanest viable)

```
skills/startup-pragmatism/
  SKILL.md                      # the whole runtime contract (prompt-only)
  references/
    evidence-and-sources.md     # distilled correction patterns + curated quotes
```

- Prompt-first: no scripts, no runner, no parameters, no orchestration. This
  is a pure frame-installation skill.
- One reference file only, holding the curated distillation of
  `trace_evidence.md` + the research pack, so `SKILL.md` stays lean and the
  shipped package is self-contained (research docs in `docs/` are build
  inputs, NOT runtime dependencies - repo red line).
- Draft trigger description (to be tightened): "Install the early-stage
  startup operating frame when the user invokes it: reality-check the current
  plan, answer, or behavior away from proof-maximizing, receipt-building, and
  decision avoidance and toward the smallest useful move, decisions at 50-70%
  information, and rigor spent only where wrongness is expensive. Use when the
  user says the agent is over-proving, over-building, hedging, or asks for a
  startup-pragmatism reality check. Not for code review, plan-readiness
  audit, intent drift policing, or genuinely irreversible/high-blast-radius
  work that deserves full rigor."

## 7. Build phases

**Phase 0 - Evidence and research (COMPLETE).**
- `trace_evidence.md`: DONE - 25 verbatim incidents + 5 near-misses with
  session:line refs, ranked failure patterns, Amir's exact correction
  vocabulary, per-pattern what-to-do-instead notes, and the balancing rule.
- `research/lean_and_decision_science.md`: DONE - 916 lines, 14 primary
  sources actually fetched (Ries, Blank, Bezos letters, Duke, Cagan, Worse is
  Better, Knuth, YAGNI, boring tech, PG, Boyd/Carmack, Startup Genome,
  Getting Real, indigestion), closing with a four-question rigor-budget
  decision framework and a skill-ready distillation.
- `research/founder_canon.md`: DONE - 1,044 lines, 9 author sections (PG x10
  essays, Garry Tan, Seibel, Altman, Livingston, Caldwell, Buchheit, Hoffman,
  Girouard's "Speed as a Habit"), every quote substring-verified against the
  fetched primary text, closing with 10 load-bearing cross-source principles
  and a quick-fire quote bank.
- Exit: MET. Failure taxonomy in section 4b confirmed against real data.

**Phase 1 - Distill.**
- Write `skills/startup-pragmatism/references/evidence-and-sources.md`: the
  ranked failure patterns (from traces), the replacement behaviors, and the
  6-10 selected authority quotes with attribution. Keep it under ~150 lines;
  it is a runtime reference, not an archive.
- Exit: reference is self-contained; no pointer into `docs/`.

**Phase 2 - Author `SKILL.md`.**
- Follow `$skill-authoring` + `$prompt-authoring`: single job, mission-level
  intent, frame + judgment (no keyword rules, no giant checklist), trigger
  description within the 1024-char cap, When-to-use / When-not-to-use /
  Non-negotiables / First-move / Workflow / Output-expectations shape used by
  sibling skills.
- Output contract: when invoked, the agent (1) restates what it was about to
  do, (2) names which failure patterns apply, (3) proposes the pragmatic
  version - what gets cut, what gets decided now, where rigor is still owed -
  and (4) proceeds with that version unless the user objects.
- Exit: `SKILL.md` + reference complete, self-contained, judgment-preserving.

**Phase 3 - Wire into the repo surface.**
- Add routing bullet to `AGENTS.md` Skill Routing and to `README.md` skill
  inventory (repo Definition of Done requires this).
- Run `npx skills check`; fix packaging findings.
- Exit: check passes; docs updated.

**Phase 4 - Validate on representative tasks (no answer leakage).**
- Replay 3 real correction scenarios from `trace_evidence.md` as fresh tasks
  in a clean child agent with the skill invoked; verify the agent cuts the
  proof work and forces the decision *without* being shown the historical
  correction.
- One anti-case probe: invoke the skill on a high-blast-radius task (e.g. a
  production schema change) and verify it still routes rigor there.
- Exit: behavior change is visible on all three; anti-case holds.

**Phase 5 - Ship.**
- `make install` locally; optionally `$amir-publish` to distribute across the
  machine cluster when Amir says go.

## 8. Risks and mitigations

- **Pendulum risk:** agents use the skill as cover for sloppy work on things
  that matter. Mitigation: rigor-budget framing (section 4c #4) and the
  explicit anti-case in the trigger + non-negotiables.
- **Slogan decay:** skill becomes a quote wall the model pattern-matches
  without changing behavior. Mitigation: skill teaches the self-check workflow
  and output contract; quotes are capped and secondary.
- **Overtriggering:** skill fires on every task and dilutes. Mitigation:
  invocation-only (like `intent-police`), stated in description and doctrine.
- **Doctrine test lock-in:** repo red line - no unit tests asserting phrase
  presence; validation is `npx skills check` + scenario replay.

## 9. Definition of done

- Skill package ships in `skills/startup-pragmatism/` and passes
  `npx skills check`.
- `AGENTS.md` routing + `README.md` inventory updated.
- Phase 4 validation replays show the corrected behavior on >=3 real
  historical scenarios and the anti-case holds.
- Amir can replace his recurring hand-typed correction with one invocation.
