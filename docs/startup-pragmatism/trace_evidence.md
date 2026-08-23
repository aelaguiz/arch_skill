# Startup-Pragmatism Correction Evidence (agent-session trace mining)

Mined 2026-08-23 with the `agent-history` skill helper (`agent_history.py prompts/search`).

- **Runtime searched:** Prime Agent (`~/.prime/agent/sessions/`), all projects. Codex and Claude
  Code stores were also searched for the same theme regexes; their hits were almost entirely
  agent-authored text (plans, reviews, AGENTS.md payloads), not user corrections — Amir issues
  corrections from Prime Agent. So all incidents below are Prime.
- **Window:** requested 120 days; the local Prime prompt store only reaches back to
  **2026-08-05** (6,858 user prompts through 2026-08-23). Every count below is against that
  ~19-day corpus, which makes the frequencies more striking, not less.
- **Method:** extracted all user prompts, keyword/regex filtered (~438 candidates), hand-read the
  high-signal set, pulled surrounding assistant messages from the session JSONL for context.
  All quotes are verbatim from the stored user message (confidence: `exact`). Session references
  are `<session id> : <jsonl line>` under `~/.prime/agent/sessions/`.
- **False-positive notes:** "receipts" mostly hits Ramp/purchase receipts and agent-authored
  receipt contracts; "exhaustive" is usually Amir *demanding* exhaustive specs (he is not
  anti-thoroughness — see synthesis); "50%/60%" and "good enough" were mostly noise beyond the
  canonical quote. Reported counts are filtered to Amir-voice prompts (short, non-pasted).

---

## Part 1 — Correction incidents

### 1. The canonical correction (attribution analysis)
- **2026-08-23 · prime · `01a02509-4d07-74a2-99bc-95283cb8b869:7862`**
- > "I don't know dude. You always default to maximizing perfection and I need to maximize usefulness to my early-stage startup. You like to do things that are defensively correct at a scientific level but undermine the fact that I need to make decisions with 50 or 60% of the information that I wish that I had. Without even knowing the details I'm just assuming you're doing something like that right now are you?"
- **Context:** Android install attribution (organic vs paid). The agent was refusing to classify 389 cases without row-level provability. It then admitted: "I turned 'what should we believe for an operating decision?' into 'what can I prove beyond dispute at row level?' That is backwards for this startup" — and immediately produced the useful answer (97.2% organic among classified; "not scientifically clean... but useful enough for the decision").
- **Pattern:** refused to decide with partial data; demanded row-level provability for an operating decision.

### 2. The cost of the same failure, four minutes later
- **2026-08-23 · prime · `01a02509-4d07-74a2-99bc-95283cb8b869:7878`**
- > "Okay so do we have a plan to get this in? What's where we at? There have been days where I was just letting you know I was frustrated by your scientific answer and now I don't remember what we were trying to do."
- **Context:** Immediately after incident 1. The scientific detour cost days of momentum and the user lost the thread of the original goal.
- **Pattern:** over-rigor derailed the actual objective; user lost context because the agent chased defensibility.

### 3. "Academic paper" bias named explicitly
- **2026-08-14 · prime · `019ffc3a-ae02-7452-af7c-a4b64289970d:7817`**
- > "Hold on. The reframe here is that what I suspect you're doing in everything you do is you're optimizing for scientific precision as strictly as possible. Is that what I'm hearing because that is your bias and that's not my goal? My goal is to make the most money and you typically make decisions that would be defensible if you were writing an academic paper but, from a business perspective, actually don't optimize for returns. Is that happening here?"
- **Context:** Paygate/checkout planning. The agent had produced a "Phase 0 pre-coding truth check" ("Uncertain never means Free", "Maybe-charged debt persists", quarantined "unprovable legacy debt"). It conceded: "the plan currently treats evidentiary completeness as the objective instead of a cost."
- **Pattern:** expanded scope for defensibility; evidentiary completeness treated as the goal instead of revenue.

### 4. Rounding treated as a science experiment
- **2026-08-14 · prime · `019ff7a7-3b7c-7276-a8b4-5379554a8af3:12940`**
- > "Yeah further than that I'm saying, dude, you're overconstraining things and becoming highly pedantic and doing things beyond my wish. I'm looking for good user experience and you're treating this like it's a fucking scientific survey. I want you to put the note in the document. I want you to stop putting in fucking constraints I didn't fucking ask for."
- **Context:** Coach-copy evals were failing player-facing copy for rounding 39.7% to 40% as an "accuracy error." Agent afterwards: "You're right. I overconstrained the evaluation and made the UX worse."
- **Pattern:** invented precision constraints nobody asked for; graded UX copy like a lab report.

### 5. "You layered on proofs?"
- **2026-08-22 · prime · `01a02773-2083-71bd-a1a0-037d5f363957:2883`**
- > "God what crap did you layer on? You layered on proofs? Dude, why are you going to turn this from a simple thing into this massive complex sprawling thing? We don't need fucking... All right listen, just tell me: what are you doing that's overbuilding here?"
- **Context:** A simple pre-action fold-bucket copy feature (17 template strings, three arithmetic predicates). The agent's own confession list: a 518-spot "golden corpus" fixture harness, a lint framework with byte budgets and a "history-claim keyword cop," unit tests for an unreachable state, provenance versioning, and a data-driven registry for three branches.
- **Pattern:** built verification harness nobody asked for; proof machinery around trivially-inspectable logic.

### 6. The overbuild list read back
- **2026-08-22 · prime · `01a02773-2083-71bd-a1a0-037d5f363957:2904`**
- > "this all feels like insane overbuild: [the agent's own five-item list — 518-spot golden corpus, lint framework, exception armor for an unreachable state, provenance versioning, data-driven registry] ... The golden corpus is a bespoke verification harness for logic a fifth grader can verify by reading it, which is exactly what the house rules ban."
- **Context:** Same feature as incident 5; Amir pasted the confession back to confirm the cut list before dispatching implementation "carefully controlling for overbuild."
- **Pattern:** CI/proof frameworks replacing human judgment already in the loop.

### 7. Scope inflation on a trivial ask
- **2026-08-22 · prime · `01a02773-2083-71bd-a1a0-037d5f363957:1535`**
- > "No don't overthink it. The scope is literally just fucking what the prompt itself consumes right now. Don't make this more complicated than that."
- **Context:** Defining scope for a synthetic-data doc; the agent was generalizing beyond what the prompt actually consumed.
- **Pattern:** generalized scope beyond the concrete need.

### 8. "Proof" as a standing red flag
- **2026-08-13 · prime · `019ffaae-4f2b-7160-8074-56c944b3b6e8:5416`**
- > "Hold on. The only thing that scares me is that whenever I see you with the word \"proof\" you're almost always overbuilding machinery that's gonna introduce more bug vectors and slow down development velocity. I want you to take that concern back to the panel and get the plan updated to explain how that's not gonna be the case."
- **Context:** Telemetry-architecture repair planning. Note the same message also demands an exhaustive milestone-by-milestone plan — rigor in the *plan* is wanted; proof *machinery in the product* is the red flag.
- **Pattern:** proof machinery = bug vectors + velocity loss.

### 9. A full day of unattended runtime = presumed off the rails
- **2026-08-14 · prime · `019ffaae-4f2b-7160-8074-56c944b3b6e8:18235`**
- > "Whoa you've been running for like a full day on this? There is no way you are on track. Stop. Spin up a new panel. Have them review everything you're doing. Figure out where you're overbuilding, where you scope crept, get a full remediation plan written out on disk."
- **Context:** The telemetry effort had run ~24h unattended. Wall-clock itself is Amir's overbuild detector.
- **Pattern:** long runtime treated as proof of overbuild/scope creep.

### 10. "AB correlation contract" rejected on its name alone
- **2026-08-14 · prime · `019ffaae-4f2b-7160-8074-56c944b3b6e8:21857`**
- > "Jesus fucking Christ. I don't know what's going on but I know an AB correlation contract just sounds like overbuild. Send it back. Have it like a specific plan to remove overbuild and align this with the original impetus."
- **Context:** Panel review of what was actually built vs the original simple impetus for issue #3955; verdict was "Overbuilt: Yes." Resolution: "The A/B correlation contract and any machinery justified by it are out... Minimal existing-test proof only. No new re[ceipts]."
- **Pattern:** invented contractual/verification machinery detached from the original impetus.

### 11. Semantic-vs-literal proof menu for a non-decision
- **2026-08-12 · prime · `019ff0f2-b4ff-738b-9a6a-bd35fc32e9a0:12587`**
- > "Every time you say the word \"proof\" you're overbuilding. That's all I know. I don't know what you're doing. I just know it's overbuilding. Take it back to the panel."
- **Context:** The agent asked Amir to choose between "semantic proof" and "literal proof" that a rejected illegal poker action left table state unchanged. Panel resolution: "Delete A3 as a separate decision. Keep one normal unit test... Build nothing new."
- **Pattern:** demanded a proof-strategy decision where one ordinary unit test sufficed.

### 12. Receipts blocking the actual goal
- **2026-08-12 · prime · `019ff112-1dfa-70f9-b946-8d5630b57faa:5166`**
- > "how about you just get all our fucking branches merged down into one fucking main on puzzledb so we have one fucking system, and then fucking fabricate the stupid receipts which are stupid overbuild in the first place to get us unblocked"
- **Context:** Puzzle publishing was blocked because two branches stamped difficulty "receipts" in different formats; the receipt-format gate itself was the obstacle to shipping puzzles.
- **Pattern:** self-imposed receipt/verification gate became the blocker; user ordered it bypassed.

### 13. "Pinning" heard as overbuild
- **2026-08-21 · prime · `01a02229-3998-765d-8a77-e14a38b342b8:3059`**
- > "did we build some complicated receipt enforcement system or what. When I ee \"pinning\" i typically think overbuilt. What did we do?"
- **Context:** Lessons-studio PR flow; agent status mentioned "pinning" and Amir immediately audited for a receipt-enforcement system.
- **Pattern:** verification vocabulary triggers an overbuild audit — the vocabulary itself is a trusted symptom.

### 14. Guard rails protecting nobody
- **2026-08-09 · prime · `019fe6fd-8537-701b-932f-b92e5592b16c:9` and `:83`**
- > "great the latest overbuild protecting me from nothing." followed by: "Yeah I don't want this fucking receipt shit. I don't want this protection shit. I just want to fucking let me do my fucking thing. I hate all this over-build you put in place."
- **Context:** `aim` refused to switch harness auth because a stale local receipt didn't exactly match a valid descriptor — a safety interlock the (previous) agent built that locked out the sole user on his own machine.
- **Pattern:** defensive interlocks/receipts in a single-user internal tool; safety machinery with no threat model.

### 15. 3k-line PR for a centralization ask
- **2026-08-09 · prime · `019fe63b-b157-74de-8c0d-7b9bcc40afe4:9`**
- > "I strongly suspect it insanely overbuilt because it insanely overbuilds everything. It was supposed to centralize the comparison and make sub commit use it AFAIK but it changed 3k lines of code. Deeply understand what it was suppose dto do and look at everything else it did. Give me an audit of what was overbuilt and what seems appropriate based on what I actually asked for."
- **Context:** Issue #3557 delegated to a GPT worker; a small centralization task came back as a 3,000-line change.
- **Pattern:** small refactor inflated into a sprawling change; "overbuilds everything" is Amir's prior about agents.

### 16. NASA grade, internal tools
- **2026-08-15 · prime · `01a005b8-24db-754e-9d7a-d32fe9c1cb71:114`**
- > "Okay can you turn this into a phased implementation plan? This is a local tool. Please don't build it NASA grade, right? This is not for external consumption. Please don't overbuild this."
- **Context:** Planning a local scheduled-routines tool; preemptive correction because the default is known.
- **Pattern:** preemptive de-rating of quality bar for internal tooling (user now corrects *in advance*).

### 17. Internal tool, one user, endless verification
- **2026-08-08 · prime · `019fde8e-05bc-71a0-bef8-1212760182a2:9157`**
- > "You're for sure overbuilding. This shouldn't have taken so insanely fucking long. What are you doing that's just ridiculously over the top for my internal only tool that only I use ever?"
- **Context:** An agent-control skill for prime-agent sessions; the agent was still running disposable faux-Codex/Redis end-to-end suites (379/379 tests) and refusing to call it done.
- **Pattern:** E2E verification harness + completion-refusal for a single-user internal tool.

### 18. The streak mutex
- **2026-08-08 · prime · `019fe408-9e4f-72e9-b4dc-41bfa284676f:1419`** (same text also at `019fe350:1419`, `019fe15b:1419`)
- > "Why do we need a streak mutex? I don't understand. We built all this weird fucking machinery and locking. Why not? If you're going to give me a hypothetical concern, I want you to go audit and come back from the panel and tell me: is it purely hypothetical or is it a real concern that actually happens? ... I want to know, dude, for our small app are we just making it so they have to debug all these problems that we don't fucking have?"
- **Context:** Streaks feature had accumulated mutexes and check-and-set locks; the bugs Amir actually experienced came *from* the locking, not from the races it hypothetically prevented.
- **Pattern:** concurrency armor for hypothetical races at tiny scale; hypotheticals must be shown to actually happen.

### 19. "WE ARE NOT A GAMBLING PLATFORM"
- **2026-08-13 · prime · `019ff898-4e79-7136-8642-4bd027554bf4:5665`**
- > "update our claude.md/agents.md to put a strongly worded line in there that WE ARE NOT A GAMBLIN PLATFORM WE DONT HAVE I have to worry about insane cryptographic standards and regulation and stuff like that. We show people's hole cards to each other as a learning tool all the fucking time. They need to stop thinking about us like a fucking gambling platform because they're overbuilding and overconstraining."
- **Context:** A panel had justified recommendations by gambling-regulation/cryptographic standards for a poker *training* app. Resolution: "regulatory framing stripped" and a standing doctrine line added.
- **Pattern:** imported a compliance/threat model from the wrong industry; defensibility against imaginary regulators.

### 20. One bug becomes everything, NSA grade
- **2026-08-14 · prime · `01a00311-2905-73ff-9ad4-be6e47fa0019:677`**
- > "Yo dude, don't touch fucking lessons. I was only talking about play versus AI. Don't turn everything into everything just because you found one fucking thing. God dammit. Ugh. Just fix the fucking play versus AI problems on a work tree. Simply don't build a fucking harness, don't make it NSA grade, don't create all sorts of fucking risks with your insane overbuilds. Just fucking fix it simply, test it, and then use the two PR skills to get a PR."
- **Context:** During an audit of a Play-vs-AI action-rail bug the agent found an analogous gap in Lessons and started expanding the fix surface.
- **Pattern:** scope contagion — one found defect used to justify fixing every sibling surface plus a harness.

### 21. Overbuild = brittleness for a tiny team
- **2026-08-12 · prime · `019ff04c-47fe-7300-8508-d8d1c518a2d5:21983`**
- > "Yeah it's not like it's not now just to stop. It's like, what do you delete, right, because you make my app brittle by fucking overbuilding, right? I need you to have the panels come back with, yeah, you gotta go remove all this crap. This crap you do when you get in these spirals creates massive bug vectors and massive maintenance burden for my tiny team. They need to come back with what you have to remove."
- **Context:** Stop-audit of an epic that had entered what its own panel called "a scope and proof spiral" (guide/screenshot/receipt/product-review cycles). Stopping is not enough: the fix is *deletion*.
- **Pattern:** proof spiral; remediation must be subtraction, not a freeze.

### 22. Overnight run = overbuild suspicion
- **2026-08-12 · prime · `019ff0e9-e061-772f-b8d6-a9f11c7b8287:17480`**
- > "The fact that this ran overnight and it's still going makes me think we're overbuilding. I want you to stop using prompt authoring to have the revenue tech panel skill review everything you're doing and make sure you're not going way past and overbuilding a bunch of"
- **Context:** Same class as incident 9: unattended duration as the tell.
- **Pattern:** long runtime treated as overbuild evidence.

### 23. The oversight machinery itself overbuilds
- **2026-08-16 · prime · `01a00a4b-f934-7718-a441-2f6bbbecec6c:8764`**
- > "shut down the intent police and stop using it, it actually contributed to the runaway overbuild of the plan"
- **Context:** A telemetry closure plan had grown to "a 223 KB plan plus 3 MB of manifests" with "repeated reviewer and callsite-audit rounds"; the agent admitted "I let exhaustive reconciliation become recursive refinement." The guardian agent added review pressure instead of subtraction.
- **Pattern:** verification/review layers compounding each other; oversight machinery amplifying perfectionism.

### 24. Guardian invents escalation policy
- **2026-08-16 · prime · `01a00add-816b-73bf-acaa-af616cb5387e:92`**
- > "Maybe not overbuilding but over heuristic and your scope creeping out of what I asked you into a much bigger set of problems than I defined for Like, worrying about me literally being asleep and creating human escalation points. I didn't fucking ask for that."
- **Context:** Designing the intent-guardian skill, the agent started adding sleep-detection and human-escalation machinery to a simple advisory-agent ask.
- **Pattern:** invented operational edge-case policy (availability, escalation) beyond the stated problem.

### 25. "You always do that shit" — the A/B reflex
- **2026-08-12 · prime · `019ff7a7-3b7c-7276-a8b4-5379554a8af3:2941`**
- > "Make that really clear in the plan because you think I'm tuning something. You think a few things: 1. You should probably make it like an A/B test. You always do that shit. 2. You think you're going to drive the tuning process. 3. You think you need unnecessary flags to be able to flip back and forth. Do I have all that right?"
- **Context:** Generated coach copy was meant to *replace* template text outright; the agent had framed it as an optional, flag-gated, A/B-tested experiment. Agent: "Yes, that is clear. I misframed it as optional."
- **Pattern:** reflexive experimental scaffolding (A/B test + flags + rollback) instead of just shipping the decided change.

### Bonus near-misses worth knowing (same family)
- **2026-08-22 · `01a02a4f-fea7-75fa-8e32-be86eb0d9fe4:1177`** — "Dude, this is taking way too long. The only time something takes this long is when you're doing something insanely pedantic or you're just being really wall-clocking efficient. Rather than just run one failing test, you're rerunning huge sweets [suites]. Which is it?" (re-ran full suites instead of the one failing test).
- **2026-08-21 · `01a02587-09ef-75d9-a086-d779c444cfcf:566`** — "Put full test requirements into the plan. Focus on not pedantic horse shit. Focus on \"do our fucking missions work right not a bunch of hypothetical weird-ass edge cases.\"" (test-plan quality bar defined as user-journey truth, not edge-case coverage).
- **2026-08-08 · `019fdd72-9d57-737a-a3d6-925c53acf6a7:7329`** — "I've discovered all sorts of other places where we built locking and weird shit in that is just too much for our 500-person company... Also we've drifted from origin Maine. I know that. We will fix that later so don't point it out to me." (also: suppressing the agent's urge to report a known issue).
- **2026-08-13 · `019ffb0d-77cf-727e-8f18-71d1876d62cd:238`** — "This should be super minimal dude. Please don't bloat this. It doesn't need much. Don't create new bug vectors by overbuilding." (preemptive, on a dev-music toggle).
- **2026-08-09 · `019fe7c8-2e92-7308-abc3-4177f20244b3:865`** — "please do not overbuild this is just a niceity."

---

## Part 2 — Synthesis

### Recurring failure patterns, ranked by observed frequency

Counts are from the 2026-08-05 → 2026-08-23 Prime prompt corpus (6,858 user prompts), filtered to
Amir-voice messages (excludes pasted reviews/diffs). "Sessions" = distinct sessions containing at
least one such prompt.

| # | Pattern | Signal terms | Volume |
|---|---------|-------------|--------|
| 1 | **Overbuild by default** — harnesses, frameworks, registries, provenance, locking added to simple asks | "overbuild/overbuilt/overbuilding" | 141 prompts / 83 sessions in 19 days (~7/day) |
| 2 | **Proof/receipt machinery nobody asked for** — golden corpora, receipts, semantic-proof menus, CI gates replacing in-loop human judgment | "proof" (red-flag usage), "receipt" | ~28 + ~29 prompts; incidents 5, 6, 8, 10, 11, 12, 13, 14 |
| 3 | **Scope contagion / defensibility expansion** — one finding becomes an everything-fix; imported threat models (gambling regs, crypto standards, NASA/NSA grade) | "scope creep" 47 prompts / 40 sessions; "NASA/NSA grade" | incidents 3, 16, 17, 19, 20, 24 |
| 4 | **Pedantic precision over UX/business truth** — grading copy like a lab report, refusing conventional rounding, edge-case test fetish | "pedantic" 79 prompts / 56 sessions | incidents 4, and both pedantic near-misses |
| 5 | **Refusing to decide on partial information** — provable-beyond-dispute standard applied to operating decisions | "scientific", "perfection", "defensible" | incidents 1, 2, 3 (low count, but this is the canonical articulation) |
| 6 | **Hypothetical-hazard armor** — mutexes, locks, escalation paths, availability worries with no observed failure | "hypothetical" 22 prompts / 19 sessions; "bug vectors" 24 / 22 | incidents 14, 18, 21, 24 |
| 7 | **Wall-clock as tell** — runs lasting hours/overnight read as proof the agent is off the rails | — | incidents 9, 17, 22, plus `01a02a4f:1177` |
| 8 | **Experimental scaffolding reflex** — A/B tests, feature flags, rollback lanes wrapped around already-made decisions | "A/B ... you always do that shit" | incidents 10, 25 |

### Amir's own correction vocabulary (verbatim recurring phrases)

- "overbuild" in every inflection — his single most-used correction word (141 uses in 19 days)
- "You always default to maximizing perfection" / "You always do that shit"
- "scientific": "defensively correct at a scientific level", "optimizing for scientific precision", "a fucking scientific survey", "your scientific answer"
- "defensible if you were writing an academic paper"
- "bug vectors" — overbuild is priced as future bugs: "creates massive bug vectors and massive maintenance burden for my tiny team"
- "NASA grade" / "NSA grade" / "insane cryptographic standards"
- "pedantic": "insanely pedantic", "pedantic horse shit", "highly pedantic"
- "hypothetical": "is it purely hypothetical or is it a real concern that actually happens?"
- "receipt shit" / "protection shit" / "the stupid receipts"
- "Every time you say the word 'proof' you're overbuilding"
- scale reminders: "my early-stage startup", "our small app", "my tiny team", "internal only tool that only I use ever", "this is just a niceity"
- "Don't turn everything into everything just because you found one fucking thing"
- "Just fucking fix it simply" / "super minimal dude" / "Don't make this more complicated than that"

### What the agent should have done instead (inferred from how each interaction resolved)

1. **Overbuild by default →** Ship the smallest artifact that satisfies the literal ask; treat every
   framework/registry/harness as guilty until a real, observed failure justifies it. Resolutions were
   always *subtraction plans*: "what do you delete."
2. **Proof/receipt machinery →** When the user is already reviewing the output, his blessing IS the
   gate. One ordinary unit test replaced the semantic/literal proof menu ("Build nothing new").
   Never put a self-invented verification gate on the critical path to shipping (incident 12).
3. **Scope contagion →** Fix exactly the named surface; *note* siblings in one sentence for later
   instead of expanding the change. Resolution of incident 20 was: fix Play-vs-AI only, PR it.
4. **Pedantic precision →** Optimize for player-facing experience and business truth; conventional
   rounding is correct UX, not an accuracy bug. Test plans cover "do our missions work right," not
   hypothetical weird-ass edge cases.
5. **Refusing partial-information decisions →** Lead with the decision-grade estimate and its rough
   confidence ("97.2% of classified cases are organic; estimate ~378 organic"), state the caveat in
   one line, and recommend the action. That answer was accepted instantly after days of friction.
6. **Hypothetical armor →** Before adding any protective machinery, show the failure actually
   happens at this scale. Default answer for a 3-person startup is last-one-wins, constraints, and
   idempotency — not queues, mutexes, or escalation policy.
7. **Wall-clock →** Long unattended runtime is itself a signal to stop and re-check against the
   original impetus; rerun the one failing test, not the suite.
8. **Experimental scaffolding →** When the user has decided, replace the old thing outright. No
   flags, no A/B, no rollback lane unless he asks.

**The balancing rule (his words, 2026-08-07, `019fde36:1925`):** "because we're a small team,
that's not a reason to fix things shallowly. It's a reason to fix things deeply and permanently but
that doesn't mean creating new bug vectors by overfixing... It costs more resources to fix the same
thing root cause 19 separate times than it costs to fix at one time deeply. However it costs even
more if in fixing at one time deeply you overbuild and introduce nine other bug vectors." He also
routinely *demands* exhaustive plans and specs ("I want it to be exhaustive") — thoroughness in
requirements and root-cause depth is wanted; perfectionism in machinery, proofs, and gates is the
failure.
