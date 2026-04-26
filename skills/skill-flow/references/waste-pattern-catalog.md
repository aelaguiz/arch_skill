# Waste-Pattern Recognition Catalog

This catalog teaches the audit's parent agent to RECOGNIZE waste patterns in
the DAG substrate. It is NOT a rule engine.

## Not a rule engine

A rule engine would say "if a skill has fan-in > 5, flag it." That produces
false positives (load-bearing primitives have legitimate high fan-in) and false
negatives (over-promotion can happen at fan-in 1 or 2).

The audit's verdict is prompt-driven judgment. The substrate gives the agent
exhaustive grounded evidence. This catalog gives the agent recognition tests —
patterns to look for and false-positive guards. The agent reads the substrate,
applies these tests, and emits findings using the existing 6-field template
(`workflow-and-modes.md` audit-finding template). Each finding is a judgment
call grounded in the substrate's labeled edges, not a score.

If the catalog ever becomes a checklist the agent mechanically applies, it has
turned into a rule engine and the audit has lost its capability-first soul.
Keep the catalog teaching judgment.

## How to apply each test

For each pattern below:

1. **Recognition prompt**: what to look for in the substrate (which edges,
   which node-kinds, which patterns of fan-in or fan-out).
2. **False-positive guard**: a sentence describing what the pattern looks like
   that ISN'T waste. Always check the guard before emitting a finding.
3. **Evidence to cite**: which substrate rows must back the finding.
4. **Smallest credible fix**: a one-line description of the minimum change
   that would resolve the waste. Goes in the `Smallest fix` field of the
   finding.

The audit's finding `Owner` field names affected SKILL.md / reference paths
only. Never invokes another skill at runtime.

---

## Pattern 1 — Over-promotion (helper installed as canonical stage)

**Recognition prompt:** A node X is named as a canonical stage owner by a
router or flow-controller (X has an inbound `routes_to` edge from a `router`
node). But X's own outbound edges to its declared collaborators are mostly
`validates_via` or `helper_call` shape (not `routes_to` or `gates_on` shape).
Meanwhile, the upstream caller(s) of X already route directly to X's
collaborators — bypassing X. The pattern says "X is being treated as a stage
when its own contract is a helper."

**False-positive guard:** X may be a legitimate stage if its own outbound
edges include `routes_to` to multiple specialists AND if upstream callers
route THROUGH X to reach those specialists (not around X). Check both: does X
genuinely own the dispatching, or is X a helper the registry mistakenly
promoted?

**Evidence to cite:** the inbound `routes_to` edge from the router; X's
outbound edges (showing helper-call shape); the upstream caller's direct edges
to X's "downstream" specialists (showing the bypass).

**Smallest credible fix:** Demote X from canonical stage to helper. Update the
flow-registry / stage-contracts file to remove X from the canonical order.
Note that the helper-call relationship from specialists to X can stay — that's
the legitimate use.

**Worked example:** see `lessons-studio-worked-example.md` for the
`psmobile-lesson-playable-layout` case.

---

## Pattern 2 — Duplicate canonical-stage acceptance criteria

**Recognition prompt:** Two skills X and Y are both canonical stages (both
have inbound `routes_to` edges from a router). Their outbound edges overlap
significantly — they share the same set of `delegates_to` and `validates_via`
targets. Their declared jobs (from `declared_job` in the substrate) describe
the same acceptance criteria in different words.

**False-positive guard:** Two stages may share collaborators legitimately if
they own different acceptance criteria. Re-read the `declared_job` text — do
they actually do different things, or are they two phrasings of the same
work? Also check stage_memberships: are they routed in different flows for
genuinely different reasons?

**Evidence to cite:** both skills' `declared_job` text; both skills' overlapping
outbound edges; the router's `routes_to` edges naming both as canonical stages.

**Smallest credible fix:** Merge the two stages into one OR define a clear
boundary between them in their respective SKILL.md descriptors. The merge
direction is a judgment call — usually keep the one with the better-defined
declared_job.

---

## Pattern 3 — Lone-wolf skill

**Recognition prompt:** A node X has no inbound peer edges (no skill in the
walked scope references X) AND no outbound peer edges (X references no peer
skills). X is isolated in the graph.

**False-positive guard:** X may be invoked at the harness layer (CLI runner,
hook system, scheduler) outside the SKILL.md graph. Always note this
possibility in the finding — ask the user to confirm whether X has a known
non-graph invocation path. Diagnostic skills (node-kind `diagnostic`) are
particularly likely to be invoked outside the graph.

**Evidence to cite:** X's node entry in the substrate (showing zero inbound
and zero outbound edges); zero `inbound_callers` if requested.

**Smallest credible fix:** EITHER add explicit peer references in callers OR
document the harness-layer invocation in X's SKILL.md OR retire X if truly
unused. The audit names options; the user decides.

---

## Pattern 4 — High-fan-in primitive vs. hand-coded loop dressed as a primitive

**Recognition prompt:** A node X has very high fan-in (e.g., 10+ inbound
edges, mostly `delegates_to` or `consumes_primitive`). X looks load-bearing.
The question is whether X is a legitimate primitive (deterministic data
operation, schema validation, CRUD) or whether X is actually a hand-coded
loop where the same boilerplate is repeated across many callers.

**False-positive guard:** X is a legitimate primitive if its `declared_job`
describes a single deterministic operation that callers genuinely need, AND
its node-kind is `primitive`. Do not flag legitimate primitives — high fan-in
is the WHOLE POINT of a primitive.

X is a hand-coded loop if the callers all do nearly-identical work that could
be lifted into X's contract, OR if X's `declared_job` reads more like a
"how-to do this thing" than a deterministic operation.

**Evidence to cite:** X's fan-in count; X's `declared_job`; 2-3 representative
caller edges showing the work being duplicated.

**Smallest credible fix:** If hand-coded loop: lift the duplicated work into
X's owned contract. If legitimate primitive: no change; note as informational.

---

## Pattern 5 — Broken edge (peer reference to non-existent skill)

**Recognition prompt:** Surface C of the substrate (the unresolved-reference
list) contains entries.

**False-positive guard:** A reference may be unresolved because the target
skill is in a different repo or was excluded from this run's scope. Check
whether the reference points at a slug that EXISTS as a SKILL.md somewhere
in `<target>` but was not in the resolved scope. If so, the entry should be
classified as `external` rather than `unresolved`. (The aggregation step
should already handle this — but verify in case the aggregation logic
missed.)

**Evidence to cite:** the unresolved-reference list row(s); confirmation that
no SKILL.md exists at the expected path in `<target>` or any sibling repo
named in the reference.

**Smallest credible fix:** Update the calling skill's SKILL.md to remove the
broken reference, OR install the missing peer skill, OR rename the reference
to the correct slug if it's a typo.

---

## Pattern 6 — Flow-registry stage names a skill whose own SKILL.md never mentions the stage

**Recognition prompt:** The substrate's edge table shows `routes_to` edges from
a router to a node X with `relationship_label` like "named as canonical stage
owner of stage_Y". Cross-check X's own `declared_job` and outbound edges:
does X mention `stage_Y` anywhere? If X has no awareness of being a stage
owner, the registry is making a claim X's own contract does not back.

**False-positive guard:** X may legitimately not name the stage in its
`declared_job` if the stage name is purely a registry-side organizational
label. Check whether X's outbound edges OR X's reference docs mention the
stage's expected behavior. If yes, the stage assignment is real even if the
SKILL.md doesn't cite the stage name. If no, the registry is over-promoting
X.

**Evidence to cite:** the router's `routes_to` edge with the stage name in
its label; X's `declared_job` text; X's outbound edges.

**Smallest credible fix:** EITHER update X's SKILL.md to acknowledge the stage
ownership and the expected behavior OR remove X from the registry as the
stage owner OR find the correct stage owner. Usually this is a sign of stale
registry, not stale skill.

---

## Pattern 7 — Two skills owning the same fan-out edges to the same downstream specialists

**Recognition prompt:** Two nodes X and Y both have `routes_to` edges to the
same set of downstream specialists Z1, Z2, Z3. X and Y are not the same
node-kind as each other (e.g., X is a `router` and Y is a `stage` — they
should be at different layers).

**False-positive guard:** A router routing to a stage that itself routes to
specialists is normal layered architecture (router → stage → specialists).
The pattern is only waste if X and Y are at the SAME architectural layer
(both routers, or both stages) and route to the same set of specialists —
that means one of them is redundant routing.

**Evidence to cite:** X's outbound `routes_to` edges; Y's outbound `routes_to`
edges; their overlapping set Z1, Z2, Z3; the node-kinds of X and Y.

**Smallest credible fix:** Choose which of X or Y owns the routing. The other
either delegates to the chosen one or is removed.

---

## Authority and limits

This catalog has 7 seed patterns. The audit may notice patterns this catalog
does not name — that is fine, name them in findings using the substrate as
evidence. Do NOT extend this catalog mid-audit; that would turn it into a rule
engine. Future additions to the catalog go through `$skill-authoring` /
`$prompt-authoring`, not through the audit run.

If the agent is unsure whether a pattern is waste, write the finding with
`Severity: low` and explicitly note the uncertainty in the `Why it matters`
field. False positives reduce trust — be honest about confidence.
