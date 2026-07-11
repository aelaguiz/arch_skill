# Plan Conductor Overbuild Root-Cause Analysis

Date: 2026-07-10

Scope: local Codex history for July 10, 2026 (America/Chicago), across all local projects

Primary skill audited: `skills/plan-conductor/`

Verdict confidence: high on the process cause; medium on the independent effect of the Terra model

## Executive verdict

`plan-conductor` is materially contributing to the overbuilding, but it is not
the original source in every case. It is best described as a **scope and
correctness amplifier**:

1. A planner turns a product ask into a broad, highly binding implementation
   plan.
2. `plan-conductor` accepts that whole plan as authoritative if it is
   executable; it does not ask whether the plan is proportionate to the
   original product value.
3. Every worker return begins as `NOT ACCEPTED`, decisive proof must be
   independently reproduced, findings are repaired and re-reviewed, and the
   Terra shortcut adds three fresh cynical reviews plus a cold verifier.
4. A real but low-probability edge case is therefore likely to become a hard
   invariant. If satisfying that invariant needs another table, migration,
   queue, authority owner, state machine, compatibility path, or proof
   harness, the current workflow has no product-value or complexity circuit
   breaker that stops it.
5. The new machinery becomes current repo truth and often gets reflected back
   into the plan or conductor log. Later agents then defend it as required
   scope. Each repair round makes the next round more likely to preserve and
   extend the machinery.

The clearest example is the daily-puzzle reminder. A 1,107-line initial plan
was already too large, but Plan Conductor then ran 21 recorded waves, created
34 findings, and turned same-day push suppression into cross-client,
cross-device, cross-process ordering infrastructure. The resulting checkpoint
was 121 files with 11,646 insertions and 1,830 deletions, before another
uncommitted repair touched 21 files and added four backend files.

The thermal case proves Plan Conductor is not the sole cause. That plan had
already become a platform rewrite before meaningful conductor implementation
began; the active Terra worker was stopped before it produced source changes.
The upstream planner had generalized “fix the thermal regression without
losing animations” into a universal scheduling, frame-work, prewarm, replay,
provider-lifetime, and scene-runtime architecture.

The practical answer is therefore:

> Stop using `plan-conductor terra` as the default implementation path for
> ordinary features until the skill has a binding proportionality gate and a
> review-expansion circuit breaker. Fix plan scope first, then make the
> conductor protect the smallest sufficient solution instead of merely
> enforcing every written requirement and every accepted reviewer finding.

## What I reviewed

I searched the current Codex runtime across all local projects for the local
calendar day, then inspected the relevant parent transcripts, submitted prompt
history, surviving plans, conductor logs, and Git history.

The broad session query returned 1,199 records because Plan Conductor and
`agent-delegate` create many child and resumed sessions. I treated direct
submitted prompts from `~/.codex/history.jsonl` as the user-intent source and
used rollout transcripts for surrounding agent decisions. I did not treat a
search-result preview or a worker summary as sufficient evidence.

Primary parent threads:

| Case | Parent thread | Project | Direct history evidence |
|---|---|---|---|
| iOS exit observability / PR #2774 | `019f4c18-8a22-7bc1-92f9-aac1e5e89b8a` | `psmobile` | `~/.codex/sessions/2026/07/10/rollout-2026-07-10T07-55-04-019f4c18-8a22-7bc1-92f9-aac1e5e89b8a.jsonl` |
| Daily puzzle push | `019f4c63-a700-7863-a7c7-1f275a8eb013` | `psagentspace` plus a psmobile worktree | `~/.codex/sessions/2026/07/10/rollout-2026-07-10T09-17-07-019f4c63-a700-7863-a7c7-1f275a8eb013.jsonl` |
| Lesson feedback determinism | `019f4d3d-5e50-7533-b245-c258342d71b5` | `psmobile` | `~/.codex/sessions/2026/07/10/rollout-2026-07-10T13-14-55-019f4d3d-5e50-7533-b245-c258342d71b5.jsonl` |
| Thermal / continuous motion and prewarm | `019f4d4a-0a39-78c1-9355-14e0602e34aa` | `fix/thermal` | `~/.codex/sessions/2026/07/10/rollout-2026-07-10T13-28-45-019f4d4a-0a39-78c1-9355-14e0602e34aa.jsonl` |
| Thermal restart / narrowed replacement | `019f4efe-4235-7892-b065-d7cedd791ac3` | `fix/thermal` | `~/.codex/sessions/2026/07/10/rollout-2026-07-10T21-25-13-019f4efe-4235-7892-b065-d7cedd791ac3.jsonl` |

Evidence labels used below:

- **Exact:** directly stored user or assistant text, current skill text, plan,
  log, or Git output.
- **Inferred:** a causal conclusion drawn from multiple exact records.
- **Best effort:** a conclusion limited by deleted/uncommitted work or by
  session duplication across restarts.

## Timeline of the overbuild spike

### Before the four failures

Plan Conductor's strict audit loop was not new on July 10. Its whole-plan
default, inverted burden of proof, independent verification, send-backs, cold
verifier, and 25-wave cap originated in the first Plan Conductor version on
July 1.

The important new event was commit `32b415f` at 15:08 local time on July 10:
`Add Terra delivery shortcut to plan conductor`. That shortcut encoded a
frequently typed prompt whose exact submitted text included:

> “making sure its implemented perfectly” and then three cynical reviews,
> fixing anything accepted before PR authoring and PR follow-through.

The shortcut did not invent the behavior. The iOS exit and daily-puzzle runs
had already been launched with the manually typed equivalent before that
commit. The shortcut made the pattern easier and more automatic for later
runs.

### 10:47 local — daily puzzle Plan Conductor starts

The user asked for a daily-puzzle push implementation based on a newly written
plan and requested Terra xhigh plus three cynical reviews. The source ask that
created the plan was a button near the daily puzzle and a push at a daily time,
rooted in existing roadmap work and mocks.

The plan was already 1,107 lines when committed as `7aa95eb`. The conductor
then treated the whole document as binding.

### 11:43 local — iOS exit Plan Conductor starts

The user asked for a full Miniarch plan and Plan Conductor execution with Terra
xhigh, “implemented perfectly,” followed by three cynical reviews and PR
follow-through.

Later in the same parent thread, the user separately demanded a global fix for
invisible simulator windows. The run folded that repository-wide tooling ask
into the same feature PR instead of separating it from MetricKit
observability.

### 15:08 local — Terra shortcut lands

The explicit `plan-conductor terra` preset made the high-rigor stack one
invocation: dedicated worktree, Terra xhigh implementation and repair,
independent verification, conductor sweep, cold verifier, three cynical
reviews, repair and fresh re-review, PR authoring, and PR follow-through.

### 17:40–17:47 local — the broader plan bias is recognized

In thread `019f4e2f-04ec-7a60-8bb0-a476990bfbc4`, the user showed another run
where the agent admitted that a justified release-safety fix had expanded into
too many edge cases, repeated cold verifiers, and custom release-verifier/test
machinery. The session explicitly diagnosed Miniarch as stricter about
underbuilding than overbuilding.

Commit `55d0fed` at 17:47 local then added a Miniarch Simplicity Contract and
overbuild protections. That was a useful repair, but it did not change Plan
Conductor's intake contract. Plan Conductor still does not explicitly validate
or enforce the Simplicity Contract at intake or during finding triage.

### Evening — lesson and thermal plans repeat the pattern

The lesson run created a Miniarch plan after the Miniarch hardening commit, yet
still produced broad generated/profile/readiness/diagnostic architecture. The
thermal planner created a 721-line platform architecture and began a conductor
run, then admitted the scope had become a universal operating system for app
work scheduling.

This matters: the Miniarch patch reduced one known failure mode, but the full
prompt stack still rewarded exhaustive architecture and proof.

## Case study 1: daily puzzle reminder

### Original product ask

The source conversation asked for a daily-puzzle push opt-in near the puzzle
and a daily delivery time. Existing mocks were available. The user asked for a
plan rooted in existing roadmap items, not for a new distributed consistency
platform.

### What the plan added before conductor execution

The initial committed plan was already 1,107 lines. The parent later identified
these plan-level expansions:

- three opt-in surfaces;
- a Reminders parent-child preference hierarchy;
- permission and reconciliation state machines;
- a 14-day re-ask cadence;
- deterministic holdouts;
- extensive telemetry and feature flags;
- J1 through J4 quiet-window coordination;
- a separate post-puzzle progression bridge;
- warm/cold route proof;
- large visual and behavior matrices.

The first two implementation commits added about 8,462 lines. This proves the
plan was a major cause before later reviewer ratcheting.

### What conductor review added

The conductor log records:

- 21 waves, plus intake;
- 34 `PC-*` findings;
- P1A required six attempts;
- P1B required four attempts;
- P1V required three attempts;
- the exact suppression slice required five attempts;
- the Phase 2 verifier required five attempts;
- three cynical review lanes and a cold verifier were still open.

The critical ratchet began with a plan-level absolute: a player must never
receive the daily-puzzle push after solving that day's puzzle. Customer.io
could not directly express the planned date comparison. Each verifier then
found another consistency edge:

1. The Customer.io limitation produced an expiring suppression attribute.
2. Cross-device monotonicity produced PostgreSQL ownership.
3. Out-of-order Customer.io requests produced row locks and a monotonic
   `_timestamp`.
4. Opt-in before completion sync produced a durable client boundary and pair
   RPC.
5. Old clients, retry ambiguity, and rolling compatibility prompted revisions,
   operation IDs, predecessor chains, and another owner table.

These findings were technically coherent. The failure was treating each one
as worth new production infrastructure. Nothing in Plan Conductor required the
parent to compare the probability and consequence of one redundant push with
the cost of the additional distributed system.

### Measured result

The parent reported this exact Git size before the reset:

```text
121 files changed
11,646 insertions
1,830 deletions
```

The stopped repair then left 21 modified files and four new backend files.
The worktree still showed those same uncommitted paths when inspected for this
report.

The plan and conductor log themselves also ratcheted:

- initial plan: 1,107 lines at `7aa95eb`;
- current plan: 1,118 lines;
- current conductor log: 463 lines;
- plan/log history: more than twenty documentation checkpoints on July 10;
- the plan/log diff since the first committed plan: 430 insertions and 25
  deletions.

### Causal verdict

**Plan was already overbuilt; Plan Conductor then materially amplified it.**

This is the strongest evidence against saying “Plan Conductor merely executed
what it was given.” It did execute an overbuilt plan, but its repeated
verification and repair process also introduced infrastructure that was not in
the original plan. It optimized an absolute correctness statement without a
residual-risk or complexity budget.

Evidence:

- exact overbuild admission and product/system comparison:
  `~/.codex/sessions/2026/07/10/rollout-2026-07-10T09-17-07-019f4c63-a700-7863-a7c7-1f275a8eb013.jsonl:14448-14465`;
- exact historical cause and size summary: same rollout, lines
  `14572-14633`;
- surviving plan and log:
  `/Users/aelaguiz/workspace/psagentspace/plans/drafts/2026-07-10-daily-puzzle-push.md`
  and its `_CONDUCTOR_LOG.md` sidecar.

## Case study 2: iOS exit observability / PR #2774

### Original product ask

The user wanted to determine whether reported iOS watchdog events were real
crashes or OS kills and to add near-perfect observability without introducing
new bug vectors.

The narrow product implementation was reasonable: observe MetricKit's exit
classifications, emit one truthful telemetry event, and avoid claiming more
than Apple reports.

### How it expanded

The run combined the MetricKit feature with a later global request about
invisible simulator windows. It then changed:

- global fail-loud simulator window visibility;
- Make commands and device targeting;
- Android headless behavior;
- screenshots, parity, deep links, multi-client runs, and shutdown commands;
- app-wide telemetry provider lifetime;
- uninitialized RudderStack behavior.

The parent ultimately described the result as approximately 75 files and 30
commits for a narrow observability feature. It also recorded that the global
window gate had already blocked a valid boot attempt.

### Causal verdict

**Mixed cause: mid-run scope mixing plus Plan Conductor's whole-plan/perfection
posture.**

The global simulator request was genuinely user-authorized, so the additional
work was not invented from nothing. The conductor failure was allowing it to
share the same feature plan and PR instead of escalating it as a separate
scope boundary. The skill says scope changes escalate, but this execution did
not preserve that separation.

This case also shows why “all tests green and heavily reviewed” is not a
proportionality verdict. The code could be correct while the PR was still the
wrong unit of change.

Evidence:

- user challenge and exact agent admission:
  `~/.codex/sessions/2026/07/10/rollout-2026-07-10T07-55-04-019f4c18-8a22-7bc1-92f9-aac1e5e89b8a.jsonl:11162-11190`;
- submitted prompts show the manual high-rigor path and the later separate
  global simulator demand in `~/.codex/history.jsonl`, thread
  `019f4c18-8a22-7bc1-92f9-aac1e5e89b8a`.

## Case study 3: lesson sounds and haptics

### Original product ask

The user observed that lessons sometimes produced sounds and haptics and
sometimes did not. The requested job was to audit current main, establish
parity/common sense, turn the result into a Miniarch plan, and implement it.

### What the build accumulated

Before the user intervened, the branch had added or attempted:

- a six-type `LessonFeedbackMoment` wrapper hierarchy;
- duplicate answer-identity ownership and fallback plumbing;
- generated SFX profiles and profile derivation;
- retained-core metadata and route-readiness type hierarchies;
- new interaction-class schema/validator fields;
- per-event requested/resolved/played diagnostics;
- QA JSON evidence;
- facade terminal-settlement machinery;
- broad catalog metadata and caller-contract validation;
- large restatement test matrices;
- a final-gate split of a pre-existing 1,240-line render file even though the
  feature added only 17 net lines there.

The conductor stopped the unrelated render split only after the user asked
whether the branch was also overbuilt.

### Cleanup evidence

The first subtraction pass removed 595 net lines of production/catalog
ceremony. The second removed another 199 net lines of proof surface. After
those 794 lines were removed, the branch still touched 87 files:

- production: +629 net lines across 38 files;
- tests and automation: +1,233 net lines across 26 files;
- catalog/tooling/generated code: -998 net lines;
- plan, audit, and SSOT docs: +2,117 net lines.

A later minimal analysis concluded the user-visible repair could be made by
editing roughly 11 existing production files with no new production
abstractions, schemas, generated profile systems, readiness framework, or
diagnostic pipeline.

### Causal verdict

**Plan and implementation both overgeneralized; conductor caught some bloat
late but did not prevent it.**

This case is especially important because Plan Conductor already contains
subtraction-first architecture and cruft lenses. Those lenses worked after the
user forced an explicit scope audit. They were not an effective pre-build
constraint. The workflow allowed expensive machinery to be built, verified,
and normalized before applying the same doctrine as cleanup.

The unrelated render split also shows a final-gate failure mode: a reviewer
can convert a pre-existing repo quality rule into mandatory feature work even
when it has almost no relationship to the product outcome.

Evidence:

- user intervention, render-split stop, three-lane subtraction, and cleanup
  metrics:
  `~/.codex/sessions/2026/07/10/rollout-2026-07-10T22-07-26-019f4f24-e717-72a2-a71b-fdea940e9c61.jsonl:2738-3111`;
- minimal replacement analysis: same rollout, lines `3348-3364`;
- submitted prompt history: `~/.codex/history.jsonl`, thread
  `019f4d3d-5e50-7533-b245-c258342d71b5`.

## Case study 4: thermal / continuous motion and scene prewarm

### Original product ask

The user had a real staging regression: physical devices felt hot, CPU had
exceeded budget, animations were implicated, and scene prewarm might be
contributing. The requested architecture should prevent recurrence while
preserving and enabling more animation and seamless scene transitions.

This was broader than the daily-puzzle ask, and some architectural work was
appropriate.

### Where the plan crossed the line

The planner generalized the goal into:

- a universal `FrameWorkLedger` for finite animations and domain timers;
- multiple new owned ticker, frame request, frame observer, UI task, and
  domain task abstractions;
- a semantic deadline framework spanning puzzles, lessons, and Play vs AI;
- provider-container lifetime changes;
- scene-transition state-machine changes;
- a custom app-owned cross-platform PostHog transport;
- combined thermal, prewarm, image-retention, memory-pressure, and scene
  runtime redesign;
- thousands of lines of phase gates and architecture bookkeeping.

The agent later stated the scope explosion began after a defensible first
phase and that the active Terra worker had produced no source changes when
stopped. The overbuilt material was primarily in the plan edits.

### Causal verdict

**Predominantly an upstream planning failure, not a Plan Conductor-generated
implementation failure.**

The user did ask for a permanent architectural pattern across all similar
places, so the planner had legitimate room to generalize. It failed to find
the smallest shared boundary and instead treated “systemic” as permission for
a new platform.

This is the counterexample that prevents over-attributing the day's failures
to Plan Conductor. The plan was already the problem. Plan Conductor was ready
to execute it faithfully, which would have amplified the damage, but the user
stopped it early.

The restarted, narrowed conductor run is also a useful control. Its surviving
log has four waves, one finding, a minimal Phase 1 diff, and independent clean
verification. The same conductor machinery behaved much better once the plan
boundary was explicitly reduced.

Evidence:

- plan-overbuild admission and exact cut categories:
  `~/.codex/sessions/2026/07/10/rollout-2026-07-10T13-28-45-019f4d4a-0a39-78c1-9355-14e0602e34aa.jsonl:8951-8975`;
- restart complaint:
  `~/.codex/sessions/2026/07/10/rollout-2026-07-10T21-25-13-019f4efe-4235-7892-b065-d7cedd791ac3.jsonl:10-11`;
- surviving replacement plan and log:
  `/Users/aelaguiz/workspace/fix/thermal/docs/APP/CONTINUOUS_MOTION_AND_SCENE_PREWARM_ARCHITECTURE_2026-07-10.md`
  and its `_CONDUCTOR_LOG.md` sidecar.

## Root cause in the Plan Conductor contract

### 1. Intake checks observability, not proportionality

The readiness gate stops only when a plan has no observable done-ness. A
detailed 1,107-line plan with explicit checks passes easily, even if it is
wildly disproportionate to the product ask.

Relevant contract:

- `skills/plan-conductor/SKILL.md:83-90`;
- `skills/plan-conductor/references/plan-intake-and-readiness.md:26-39`.

The intake reference extracts requirements, phases, verification, cleanup,
and delete obligations. It does not require:

- a one-sentence original product outcome;
- a smallest sufficient fix;
- an explicit residual-risk budget;
- a proof ceiling;
- a list of tempting machinery not to build;
- a comparison between expected diff size and product value;
- a check that every phase directly serves the original ask.

An overbuilt plan is therefore a perfect input to the conductor: detailed,
auditable, and wrong-sized.

### 2. The whole plan is binding by default

The skill says the whole plan is the default boundary and that requirements,
checklists, and exit criteria cannot be rewritten during execution.

Relevant contract:

- `skills/plan-conductor/SKILL.md:71-90`;
- `skills/plan-conductor/SKILL.md:161-180`.

That is good anti-drift discipline only if the plan is already proportionate.
With an overbuilt plan, it turns scope mistakes into non-negotiable work.

### 3. The review loop is asymmetric

The workflow is extremely strong against underbuilding and false completion:

- every return starts `NOT ACCEPTED`;
- the conductor must trace beyond the diff;
- decisive proof must be independently reproduced;
- all accepted findings must be fixed;
- a repair is re-audited from scratch;
- a slice may take five worker attempts;
- the run may take 25 waves;
- final closure requires no open accepted findings.

Relevant contract:

- `skills/plan-conductor/SKILL.md:117-150`;
- `skills/plan-conductor/references/audit-and-send-back.md:9-18`;
- `skills/plan-conductor/references/audit-and-send-back.md:65-80`;
- `skills/plan-conductor/references/audit-and-send-back.md:86-137`.

The equivalent anti-overbuild rule is much weaker. The audit does say every
new abstraction must be forced and that subtraction-first is the standard.
That is good doctrine. But if the plan or an accepted reviewer finding creates
the forcing requirement, there is no higher product-value test to reject the
requirement itself.

### 4. Real findings become mandatory without a value test

Finding triage supports `accepted`, `rejected`, and `deferred`. In practice,
the gate strongly biases toward accepting and repairing a technically valid
finding:

- `accepted` means must fix;
- `rejected` requires contradicting evidence;
- `deferred` must be allowed by plan/user and remains visible;
- final review verdicts do not pass with open required repairs.

There is no first-class status for:

> Real edge case, correctly identified, but not worth a new subsystem for
> this product consequence.

That missing category explains the daily-puzzle ratchet. The reviewers were
not necessarily wrong. The orchestration treated “real” as synonymous with
“must eliminate now.”

### 5. The Terra preset stacks multiple independent vetoes

The Terra path runs:

1. normal conductor implementation and independent verification;
2. parent cynical audit;
3. whole-plan sweep;
4. cold verifier;
5. fresh cynical code review;
6. fresh cynical architecture review;
7. fresh cynical cruft review;
8. repairs;
9. fresh re-review of affected lanes;
10. PR review follow-through with more same-branch fixes.

Relevant contract:

- `skills/plan-conductor/SKILL.md:199-210`;
- `skills/plan-conductor/references/terra-delivery-shortcut.md:27-38`;
- `skills/plan-conductor/references/terra-delivery-shortcut.md:47-80`;
- `skills/plan-conductor/references/terra-delivery-shortcut.md:84-91`.

Independent review is valuable, but repeated skeptical reviewers will keep
finding edges. Without a shared proportionality contract, more intelligence
and more review rounds increase the chance of sophisticated overbuilding.

### 6. The standard kickoff language asks for an unbounded world state

The exact prompt used to create the Terra shortcut asked the conductor to
ensure the implementation was “perfect,” run three cynical reviews, fix
everything it agreed with, and then continue through PR review.

“Perfect” has no stopping rule. In a software system with old clients,
multiple devices, async networks, external SaaS APIs, lifecycle races, and
large existing owners, a capable reviewer can always find another way the
world might violate an absolute.

The shortcut faithfully encoded the user's frequently typed path, but it did
not translate “perfect” into an outcome with a bounded risk and proof budget.

### 7. Miniarch's new Simplicity Contract is not connected to conductor

Commit `55d0fed` added:

- smallest sufficient fix;
- enough proof;
- tempting machinery not to build;
- a hard stop on unapproved machinery or new test categories.

Plan Conductor's intake and review references do not explicitly read or
enforce those fields. A Miniarch plan can carry a Simplicity Contract, but the
conductor still extracts ordinary requirements/checklists and runs its own
review loop without making that contract the highest-order acceptance rule.

This is a broken handoff between the planning and implementation skills.

### 8. Scope changes are prohibited in doctrine but not robustly isolated

The skill says scope changes escalate. The iOS session nevertheless combined
a separate global simulator-tooling demand with MetricKit observability. The
skill needs a stronger operational recognition test:

> If a new request changes repository-wide tooling, unrelated platforms, or
> a different production owner than the plan, stop and either amend the plan
> with explicit user approval or create a separate plan/PR.

Without that test, the parent can rationalize a newly authorized ask as part
of “finishing perfectly.”

## Factors outside Plan Conductor

### Upstream plan authoring

This is a co-primary cause. Daily puzzle was already a 1,107-line plan. Thermal
was already a platform rewrite. Lesson's plan and architecture choices had
already turned a behavior defect into generated/profile/readiness machinery.

Plan Conductor is deliberately not a plan-audit skill. That boundary is
reasonable in isolation but unsafe in the common real workflow: create a plan
and immediately conduct it in the same long parent session. No independent
proportionality gate occurs between those steps.

### The user's high-rigor shortcut wording

The repeated user wording contributes to the result:

- “implemented perfectly”;
- three cynical reviews;
- fix everything accepted;
- review again until clean;
- continue through PR follow-through.

This is not blame. The skill's job is to turn that desired quality bar into a
bounded engineering contract. It currently interprets the wording literally
and procedurally.

### Terra xhigh

Every highlighted implementation/review loop used `gpt-5.6-terra` at `xhigh`.
That is a plausible amplifier: a high-reasoning skeptical agent is good at
finding cross-device, old-client, timeout, and concurrency edges and at
designing machinery to eliminate them.

It is **not proven as an independent root cause**. There is no same-plan A/B
comparison in today's history against Sol, Luna, Claude, or another effort
level. The exact transcripts already explain the growth through plan scope and
review findings. A different capable model could follow the same contract into
the same failure.

### Same-session normalization

The parent stayed in long, context-heavy sessions while plans, logs, worker
claims, reviews, and repairs accumulated. Even though child reviewers were
fresh, the parent deciding which findings to accept had normalized the
existing architecture. Plan Conductor's own final-gate rationale acknowledges
this risk, but it uses more refutation as the remedy. It does not use a cold
return to the original product ask and expected complexity.

## Why the existing anti-overbuild text did not save the runs

Plan Conductor already says:

- recovered facts never expand approved scope;
- every abstraction needs a forcing requirement;
- subtraction-first is the standard;
- cruft and compatibility ghosts are findings;
- scope changes escalate.

Those are good local rules. They failed for three structural reasons:

1. **The plan itself supplied the forcing requirement.** The conductor audits
   plan fidelity, not whether the requirement should exist.
2. **A reviewer finding supplied the next forcing requirement.** A real race
   or edge was accepted, making infrastructure to eliminate it look necessary.
3. **The anti-overbuild review arrived after construction.** Lesson feedback
   shows the lenses can remove hundreds of lines, but prevention would have
   been much cheaper than constructing, testing, reviewing, and then deleting
   the machinery.

## Recommended changes

### Immediate operating change

Until the skill is repaired:

1. Do not use `plan-conductor terra` as the default for a small or medium
   product feature.
2. Use `$plan-implement` or ordinary implementation for a bounded plan when a
   delegated whole-plan conductor is unnecessary.
3. Before any conductor run, require an independent plan proportionality pass,
   not merely Fable feedback or plan completeness review.
4. Name an explicit phase range instead of accepting whole-plan default when
   only one outcome is needed.
5. Set a low initial wave cap, such as 4–6. Crossing it should require a fresh
   user-visible scope review, not an automatic increase.
6. Select one review lane based on actual risk. Do not automatically run all
   three cynical reviews plus a cold verifier for ordinary work.
7. Record accepted residual risks. A rare duplicate notification, stale old
   client, or ambiguous timeout is allowed to remain when eliminating it costs
   more than its product harm.

### Skill change 1: add a binding proportionality gate at intake

Before creating the execution map, the conductor should extract or require:

- original product outcome in one sentence;
- smallest sufficient implementation;
- explicit non-goals;
- acceptable residual risks;
- enough proof;
- tempting machinery not to build;
- expected owner surfaces and rough change shape;
- any new abstraction, table, migration, queue, service, protocol, or
  operational surface the plan explicitly authorizes.

If the plan lacks these or contradicts them, stop and route to `$plan-audit`
or the owning planning skill. A plan being detailed is not readiness.

### Skill change 2: make the Simplicity Contract outrank all lower layers

For Miniarch/Arch plans with a Simplicity Contract:

- extract it into the conductor log;
- make it the first line of every worker prompt;
- require every slice and finding repair to state how it serves the smallest
  fix or enough proof;
- prohibit a reviewer from widening it;
- require explicit user approval for any complexity expansion;
- prevent plan/log rewrites from retroactively authorizing implementation
  growth.

### Skill change 3: add a finding-value decision before `accepted`

Every technically valid finding should be triaged through four questions:

1. What user-visible or operational harm occurs?
2. How likely is it in the supported world?
3. What is the cheapest acceptable response: fix, simplify the requirement,
   document residual risk, or defer?
4. Does the fix introduce a new owner, authority, state machine, persistence
   layer, migration, protocol, compatibility path, or proof category?

If question 4 is yes and that machinery was not explicitly authorized, the
finding cannot be auto-accepted. It becomes a user decision with the tradeoff
stated plainly.

Add a first-class triage status such as `accepted-risk` or
`real-not-worth-fixing-now`. A finding does not need to be factually wrong to
be rejected as current product scope.

### Skill change 4: add a complexity ratchet breaker per wave

At every wave boundary, compare current reality with intake:

- changed production owners;
- new concepts/types/abstractions;
- new persistence or operational surfaces;
- new test categories or harnesses;
- file/line shape as a diagnostic, not a hard universal quota;
- residual risk eliminated versus complexity introduced.

Stop when a repair causes an order-of-magnitude increase, adds an unplanned
production authority, or expands into an adjacent subsystem. Do not let a new
checkpoint normalize the expansion.

### Skill change 5: narrow the Terra final gate

The Terra shortcut should not mean “every reviewer veto must be eliminated.”
Recommended behavior:

- conductor sweep checks plan fidelity and proportionality;
- choose the review lanes that match the change;
- reviewers must include the smallest acceptable response and product harm;
- one material repair round by default;
- further rounds require a concrete plan-blocking defect, not merely another
  real edge;
- the cold verifier checks the desired product world and forbidden
  overbuild, not every imaginable missing guarantee;
- PR follow-through cannot widen product or architecture scope.

### Skill change 6: replace “perfect” with a bounded quality statement

The shortcut's human intent should become:

> Deliver the smallest sufficient implementation, prove the demonstrated
> behavior and material regressions, preserve explicit non-goals, and stop
> when remaining risks cost more to eliminate than their likely harm.

That preserves the user's desire for quality without defining done as the
absence of any objection a fresh xhigh reviewer can formulate.

### Skill change 7: separate mid-run requests by default

When a new user request touches an unrelated repository-wide owner or adds a
new product outcome, the conductor should:

1. finish or pause the current bounded plan;
2. state that the new request is separate scope;
3. create or request a separate plan/branch/PR unless the user explicitly
   approves combining them after seeing the tradeoff.

This would have kept the simulator visibility overhaul out of the MetricKit
observability PR.

## Suggested routing policy after repair

| Work shape | Recommended path |
|---|---|
| Small feature or narrow bug with an obvious owner | ordinary implementation or `$plan-implement` |
| Existing bounded multi-phase plan with clear simplicity contract | normal `$plan-conductor`, targeted review only |
| High-risk migration, security boundary, money movement, irreversible data change | `$plan-conductor terra` with full review stack |
| Plan is broad, architecture-heavy, or has absolute language such as “never”/“perfect” | `$plan-audit` proportionality pass before implementation |
| Reviewer repair would add a table, migration, protocol, queue, compatibility system, or new authority | stop for explicit user tradeoff approval |

## Bottom line

The overbuilds were not random, and they were not simply four workers making
the same bad aesthetic choice. The workflow consistently rewarded the same
behavior:

- broaden the ask during planning;
- bind the whole plan;
- define every edge as a correctness obligation;
- use multiple skeptical xhigh agents to find more edges;
- repair until no accepted finding remains;
- let each repair create the authority that justifies the next repair;
- never return to the product value and ask whether the risk was worth the
  machinery.

Plan Conductor is therefore part of the root cause. It is the component that
made the scope mistakes durable, executable, repeatedly audited, and expensive.
But the fix cannot be limited to removing one review pass. The plan handoff,
finding triage, residual-risk policy, and Terra shortcut all need the same
binding rule: **the smallest sufficient product outcome outranks exhaustive
correctness machinery.**
