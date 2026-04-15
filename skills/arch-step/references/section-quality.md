# Arch Step Section Quality

Execution grades:

- `strong`: downstream commands can trust it directly
- `decent`: downstream can proceed, but should do so carefully
- `weak`: not done for planning purposes
- `missing`: the artifact has not reached this part yet

## `# TL;DR`

Purpose:

- give the highest-signal truth about the plan in a few lines
- constrain the rest of the document rather than merely summarize it

Strong when:

- `Outcome` is falsifiable
- `Problem` is concrete
- `Approach` names the actual architectural move
- `Plan` names real phases or work slices
- `Non-negotiables` materially constrain later decisions
- the section does not leave plan-shaping alternatives unresolved

Weak when:

- it reads like marketing copy
- the plan is generic or empty
- the non-negotiables do not rule anything out
- it disagrees with Section 0 or Section 7
- it contains conditional or branchy plan language that leaves real choices unresolved

Downstream can trust it when:

- it gives one stable sentence for outcome, problem, approach, and plan shape
- later commands do not need to reinterpret what the plan is trying to do

## `# 0) Holistic North Star`

Purpose:

- align the workflow before deeper planning
- lock scope, evidence, invariants, and fallback stance early enough to prevent drift

Strong when:

- the claim is falsifiable
- in-scope and out-of-scope are explicit
- requested behavior scope and allowed convergence scope are distinguishable
- adjacent-surface scope is explicit when the change touches a contract family, source of truth, or migration boundary
- compatibility posture is explicit instead of being left as a hidden safety assumption
- when agent-backed, it is explicit that prompt/native-capability work gets first right of refusal before new tooling
- definition of done is observable
- evidence uses credible proof proportional to the work and risk
- invariants are actionable
- fallback stance is explicit and respected
- later commands can answer ordinary scope and tradeoff questions from it
- no plan-shaping decisions are still waiting for the agent to guess later

Weak when:

- the claim is vague or unmeasurable
- scope boundaries are missing
- convergence work and product scope are blurred together
- adjacent surfaces that would become contradictory are left implicit
- compatibility posture is left to implication instead of being stated
- it assumes the model or agent lacks capability without evidence
- definition of done depends on bespoke ceremony
- invariants are generic platitudes
- it reads like inspiration instead of an execution contract
- it leaves real behavior, scope, owner-path, or evidence decisions unresolved

Downstream can trust it when:

- later commands can answer "is this in scope?", "is this convergence or creep?", and "what evidence is enough?" without guessing
- later commands can answer which sibling surfaces move together and whether the plan preserves the contract or cuts over cleanly without guessing
- there is one clear fallback stance instead of hidden compatibility assumptions

## `# 1) Key Design Considerations (what matters most)`

Purpose:

- record the ranked priorities and constraints that should bias technical choices

Strong when:

- priorities are meaningfully ranked
- constraints are real and grounded
- principles reflect enforceable architecture rules in real code or runtime boundaries, not repo-policing heuristics
- tradeoffs and rejected alternatives are explicit

Weak when:

- priorities are interchangeable
- constraints are boilerplate
- principles do not affect decisions

Downstream can trust it when:

- technical choices can be ranked against it instead of argued from taste

## `# 2) Problem Statement (existing architecture + why change)`

Purpose:

- explain current reality and why change is justified

Strong when:

- current behavior is concrete
- symptoms and root-cause hypotheses are specific
- why-now is explicit
- constraints flow from reality, not taste

Weak when:

- it only restates the desired future
- the current system is not actually described
- root causes are hand-wavy

Downstream can trust it when:

- the reason for change is specific enough to judge whether the target architecture solves it

## `# 3) Research Grounding (external + internal “ground truth”)`

Purpose:

- anchor the plan in repo truth and relevant prior art

Strong when:

- internal anchors cite concrete file paths and explain why they are authoritative
- the canonical owner path is named explicitly
- adjacent surfaces tied to the same contract family or migration boundary are named explicitly
- compatibility posture is grounded explicitly instead of being implied
- when agent-backed, current prompt surfaces, native model capabilities, and existing tool/file/context exposure are anchored explicitly
- reusable patterns are named explicitly
- duplicate or drifting paths are called out when they matter
- capability-first alternatives are visible before new tooling is blessed
- preservation signals are named when refactor risk is real
- external anchors use adopt or reject reasoning instead of cargo cult
- decision gaps are either already resolved in the main artifact or written as explicit blockers that prevent readiness

Weak when:

- it is generic or unanchored
- it treats the obvious path as the whole change and leaves sibling surfaces uninspected
- it leaves preservation versus clean cutover implicit
- it jumps to scripts, wrappers, or harnesses without first grounding prompt and capability options
- external references are decorative
- plan-shaping decisions remain unresolved

Downstream can trust it when:

- later commands can point to concrete repo anchors, the canonical owner path, and preservation signals instead of rediscovering them

## `# 4) Current Architecture (as-is)`

Purpose:

- describe the current structure and behavior precisely enough to plan real change

Strong when:

- relevant on-disk structure is grounded in real files
- main control paths are named
- ownership boundaries and failure behavior are explicit
- UI states are captured when UI is in scope

Weak when:

- it is just a restatement of the repo tree
- flows are missing
- ownership and failure behavior are unclear

Downstream can trust it when:

- the current control flow and boundaries are concrete enough to audit planned changes against them

## `# 5) Target Architecture (to-be)`

Purpose:

- specify the future architecture tightly enough to implement without guessing

Strong when:

- future structure is concrete
- the canonical owner path is explicit
- the cutover, preservation, or approved-bridge story is explicit for changed contracts
- when agent-backed, the target architecture clearly says what behavior belongs in prompt/capability usage versus deterministic code
- contracts and boundaries are explicit
- SSOT is clear
- no parallel paths are tolerated without explicit approval
- invariants are enforceable in shipped behavior or boundary code, not through grep- or absence-based hygiene gates
- migration shape is explicit where interfaces change
- there is one chosen architecture, not multiple viable branches left open

Weak when:

- it describes aspirations instead of contracts
- boundaries are mushy
- it relies on hidden compatibility assumptions or leaves multiple migration stories open
- it treats agent-backed behavior as if only deterministic scaffolding can own it
- it leaves multiple plausible architectures open

Downstream can trust it when:

- implementation can proceed without inventing missing contracts or choosing among multiple architectures

## `# 6) Call-Site Audit (exhaustive change inventory)`

Purpose:

- make implementation completeness auditable
- prevent drift and missed migrations

Strong when:

- call sites are concrete and exhaustive enough within approved scope to drive work
- the canonical owner path and required convergence work are explicit
- migration notes and delete list are explicit
- adjacent surfaces such as sibling formats, readers/writers, fixtures, examples, or docs are captured when they move with the same contract family
- compatibility posture and cutover notes are explicit
- touched live docs/comments/instructions to delete or rewrite are explicit when the change would otherwise leave stale truth behind
- tests impacted are called out when relevant
- consolidation sweep names related adopters and default dispositions
- required scope calls are resolved instead of parked as later choices

Weak when:

- it only lists the obvious path
- it ignores non-code sibling surfaces that would drift with the same contract
- it mixes product creep or architecture theater into the required work
- deletes and cleanup are absent
- it cannot be used to verify completeness
- required migrations, owner-path choices, or include-vs-exclude decisions are still unresolved

Downstream can trust it when:

- implementation and later audit can use it to prove completeness rather than merely get started

## `# 7) Depth-First Phased Implementation Plan (authoritative)`

Purpose:

- serve as the one authoritative execution checklist
- convert the rest of the artifact into an implementation order that can actually ship

Strong when:

- the plan is foundational-first
- each phase owns one coherent self-contained unit that later phases clearly build upon
- when two decompositions are both valid, the plan prefers more phases than fewer
- each phase has goal, work, checklist, verification, docs/comments when needed, exit criteria, and rollback
- `Checklist` is exhaustive enough that required work cannot hide behind a vague phase summary
- `Exit criteria` are exhaustive, concrete, and all required
- refactor-heavy phases say how preserved behavior will be proven
- agent-backed phases prefer prompt, grounding, and native-capability changes before new tooling, and any new tooling is explicitly justified
- phases encode the chosen adjacent-surface follow-through and the chosen cutover, preservation, or approved-bridge work directly
- verification is small and credible
- manual QA is deferred to finalization when appropriate
- there is no competing checklist elsewhere
- required deletes, cleanup, touched-doc reality-sync work, and follow-through are visible rather than buried
- phases describe the actual work to do rather than conditional branches the agent must choose between later

Weak when:

- phases are generic, unordered, or blend multiple coherent units that could have been phased separately
- work items are too vague to implement
- the checklist is missing, incomplete, or easy to paper over
- a phase could be marked complete without satisfying all of its planned obligations
- product scope creep or architecture theater appears in the authoritative checklist
- agent-backed work jumps to deterministic harnesses or wrappers without a capability-first rationale
- adjacent-surface follow-through or compatibility posture is left implicit
- touched live docs/comments that would go stale are left implicit
- helper blocks compete with the phase plan
- sequencing hides required cleanup or migration work
- the authoritative checklist still contains unresolved alternatives, "if needed" work, or other branchy plan language

Downstream can trust it when:

- `implement` can execute from it directly and `audit-implementation` can reopen work against it concretely without inventing what "done" means for a phase

## `# 8) Verification Strategy (common-sense; non-blocking)`

Purpose:

- explain how the work will be trusted without turning verification into bureaucracy

Strong when:

- it prefers existing checks
- for agent-backed systems, it does not turn capability gaps into bespoke machinery without justification
- unit, integration, or end-to-end signals are used only where they buy confidence
- refactor-heavy work has behavior-preservation checks that survive restructuring
- manual verification is short and purposeful
- it explicitly rejects negative-value tests

Weak when:

- it introduces large new harnesses by default
- it depends on visual constants, doc gates, or deletion proofs
- it conflicts with Section 0 evidence expectations

Downstream can trust it when:

- each phase has a believable required-proof story and final QA expectations are proportionate

## `# 9) Rollout / Ops / Telemetry`

Purpose:

- capture rollout, telemetry, and operational follow-through when relevant

Strong when:

- rollout, rollback, telemetry, and runbook implications are concrete
- it is concise when the change does not need much operational surface

Weak when:

- it is absent for a change that clearly needs rollout or telemetry thought
- it is generic boilerplate with no operational value

Downstream can trust it when:

- rollout or operational follow-through is explicit enough that implementation and finalization will not forget it

## `# 10) Decision Log (append-only)`

Purpose:

- record real decisions, approved exceptions, and plan drift over time

Strong when:

- entries are concrete and append-only
- exceptions such as fallbacks are explicitly time-boxed and justified
- sequencing or scope shifts are recorded when they matter

Weak when:

- decisions disappear into narrative edits
- exceptions are made without a durable record

Downstream can trust it when:

- plan changes, approved exceptions, and fallback decisions are visible without diff archaeology

## Supporting block: `planning_passes`

Purpose:

- track the recommended planning sequence without hard-blocking work

Strong when:

- pass fields are updated additively
- it reflects real planning progress
- it helps `status` and `advance` choose the next move

Weak when:

- it is missing from a canonical doc
- fields are wiped or left misleadingly stale

Downstream can trust it when:

- it reflects what actually happened and does not mislead `status` or `advance`

## Supporting block: `external_research`

Purpose:

- bring in narrowly scoped, plan-adjacent best practice with sources

Strong when:

- topics are narrow and relevant
- sources are authoritative
- findings become adopt or reject guidance for this plan

Weak when:

- it sprawls
- it summarizes without affecting the plan

Downstream can trust it when:

- target architecture or verification choices can cite it without cargo culting

## Helper block: `plan_enhancer`

Purpose:

- harden the main artifact toward the simplest, most idiomatic, most drift-resistant plan

Strong when:

- it sharpens the main plan instead of becoming a parallel plan
- it makes hard architecture rules explicit in real runtime or code terms instead of suggesting repo-policing heuristics
- it identifies must-change call sites, deletes, drift-prone adopters, and the canonical owner path

Weak when:

- it repeats the main plan without improving it
- it acts like a second checklist
- it makes strong claims without grounding them in the actual plan or code

Downstream can trust it when:

- it clearly hardens the main artifact and leaves Section 7 as the one execution checklist

## Helper block: `reference_pack`

Purpose:

- make reference material impossible to miss during planning and implementation without turning it into a shadow checklist

Strong when:

- it distills binding obligations
- it folds reference material into the main artifact
- instruction-bearing references preserve explicit structure or keep the exact source text recoverable
- it makes phase alignment explicit while staying advisory
- it does not silently promote reference content into authoritative execution work

Weak when:

- it is just an inventory dump
- obligations are vague or not phase-aligned
- folded content is missing the parts implementation actually needs
- instruction-bearing source was condensed into generalities without explicit rationale and recoverable source text
- it behaves like a shadow checklist or silently expands Section 7

Downstream can trust it when:

- implementation and review can see the real non-negotiables without chasing external docs, while core planning commands still own what becomes ship-blocking work

## Helper block: `overbuild_protector`

Purpose:

- mechanically separate ship-blocking work from optional work, follow-ups, product scope creep, and architecture theater

Strong when:

- classifications are explicit
- evidence anchors are cited
- convergence work is clearly separated from product creep
- Section 7 remains the single execution checklist

Weak when:

- it classifies work without evidence
- it creates a shadow execution surface
- it leaves scope calls ambiguous

Downstream can trust it when:

- execution agents can tell what is ship-blocking convergence work versus optional, deferred, or rejected work without guessing

## Helper block: `consistency_pass`

Purpose:

- run one explicit end-to-end cold-read consistency check before implementation starts

Strong when:

- it checks the full artifact instead of only one local block
- it repairs real cross-section contradictions in the main plan
- it makes remaining inconsistencies explicit
- it says plainly whether the doc should proceed to implementation
- in Codex, it reflects two real cold-reader passes rather than one same-voice reread
- it makes unresolved decisions and unauthorized scope cuts explicit

Weak when:

- it becomes copy editing instead of truth repair
- it leaves contradictions parked in the helper block instead of fixing the plan
- it says `yes` while major scope, owner-path, or phase-plan disagreements remain
- it says `yes` while unresolved decisions or unauthorized scope cuts remain
- it becomes a second execution checklist

Downstream can trust it when:

- the artifact has been reread end to end and the proceed or stop decision is explicit and credible

## Helper block: `review_gate`

Purpose:

- record local idiomatic and completeness review before moving on

Strong when:

- it asks the right question
- it records integrated changes and remaining risks
- it improves the main plan rather than merely commenting on it
- it catches needless new code paths, unjustified scaffolding around agent-backed behavior, and missing preservation evidence
- it catches silent compression of instruction-bearing content during re-homing or folding

Weak when:

- it is generic or ceremonial
- it records feedback without integrating it
- it duplicates the plan instead of sharpening it

Downstream can trust it when:

- the artifact is more idiomatic and complete after the review than before it

## `WORKLOG_PATH`

Purpose:

- record short execution evidence and progress truth

Strong when:

- it links to the plan
- it records real progress at phase boundaries
- entries name work completed, checks run, issues or deviations, and next steps
- phase-boundary updates match the current phase status in Section 7
- touched live docs/comments cleanup is reflected when that work was part of the phase
- it does not become a second planning document

Weak when:

- it claims progress without evidence
- it diverges from the plan
- phase-boundary truth is missing or stale
- it turns into a second checklist or backlog

Downstream can trust it when:

- implementation truth can be reconstructed quickly without rereading the whole diff

## `implementation_audit`

Purpose:

- stop false-complete claims and force evidence-anchored completeness

Strong when:

- verdict is explicit and honest
- code blockers are concrete
- reopened phases are updated in place
- missing items cite evidence anchors
- each missing item says what the plan expects, what code reality is, and what fix remains
- false-complete phases are reopened
- it catches execution-side plan drift instead of accepting a narrowed after-the-fact story
- it checks explicit details and sub-obligations, not just broad feature impressions
- stale touched live docs/comments are treated as implementation gaps when the plan required cleanup
- unjustified scaffolding around agent-backed behavior is treated as an implementation gap when the plan required prompt-first or capability-first handling
- manual QA is tracked as non-blocking follow-up instead of missing code

Weak when:

- it claims completeness without evidence
- missing items are vague
- code gaps and manual QA are mixed together
- phases stay marked complete despite real code gaps
- it accepts broad "done" language while explicit plan details are still missing
- execution-side plan rewrites are allowed to stand as truth

Downstream can trust it when:

- the repo can be judged code-complete or not without hand-waving
