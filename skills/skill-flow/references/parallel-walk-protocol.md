# Native Walk Protocol

The DAG-grounded audit gives independent skill slices to clean native walkers.
Each walker reads its assigned skills, returns structured per-skill evidence,
and the parent agent validates and aggregates that evidence into the substrate
document. This file is the SSOT for that contract.

Read `../../_shared/agent-orchestration-policy.md` before dispatch. The
ordinary same-host lane is native: in Codex set `fork_turns: "none"`; in Claude
use a clean named/custom subagent rather than a full conversation fork or a
skill `context: fork` shorthand. A different provider or external process is
still available when its concrete capability or lifecycle benefit justifies
the added process cost, but ordinary repository walking does not need it.

## Scope resolution (parent agent, before dispatch)

The parent agent receives a plain-language scope phrase from the user. Resolve
it to a concrete skill list before any walker is dispatched. Recognized phrases:

- **`"every skill in this project"`** (or equivalents like "all skills", "the
  whole skill suite") → enumerate `<target>/skills/*/SKILL.md`. If the target
  uses the Doctrine `prompts/SKILL.prompt` → `build/SKILL.md` shape (lessons_studio
  style), enumerate `<target>/skills/*/build/SKILL.md`. The canonical node identity
  is always the SKILL.md, not the `.prompt` source.
- **`"the skills for flow <F>"`** (or "the skills used in flow X") → look up `<F>`
  in any visible `flow-registry.md`, `stage-contracts.md`, or similarly-named
  registry file in the target. Resolve to the named skill set declared there.
  If no such registry file exists in the target, ask the user to enumerate the
  skills explicitly.
- **Explicit slug list** (e.g., "audit `skill-A`, `skill-B`, `skill-C`") → use
  the slugs literally; verify each resolves to a SKILL.md before dispatch.
- **Genuinely ambiguous phrases** → exact blocker question. Do not dispatch on a
  guess. Example: "the recent skills" — ask which ones.

State the resolved skill list (count + slugs) in the audit's progress output
before dispatch so the user can verify scope.

## Fanout judgment (parent agent decision)

Parallelism exists to reduce elapsed time over independent slices, not to
maximize agent count. The parent chooses the smallest useful walker set after
considering:

- available native host slots and the parent's own slot;
- coherent skill families that can be read without overlap;
- enough work per child to justify dispatch and enough context to read the
  assigned package completely;
- the parent's ability to validate every return and reconcile duplicate edges;
- shared workspace state and any current external-process contention.

A small suite may need only one walker. A large suite normally needs several
waves when host slots are scarce. Do not create nested walkers to simulate more
capacity. Record which child owns each slug and do not declare coverage until
every resolved slug has one accepted return.

## Per-walker evidence schema

Each walker receives:

- The list of skills it must walk (full file paths).
- The closed edge-kind enum from `dag-substrate-format.md` (so the walker
  uses the same vocabulary as the substrate).
- The reference-extraction rules below, especially the semantic code-context
  filter.
- Whether `inbound_callers` is required for any walked skill (the parent decides
  based on which skills look load-bearing or potentially lone-wolf).
- A read-only/no-write contract, an instruction not to spawn children or invoke
  delegation/consult skills, and the exact result shape below.

Each walker returns, **per assigned skill**, a block in this exact shape:

```
### <skill-slug>

- declared_job: <one-sentence paraphrase of the SKILL.md frontmatter description, plus the path:line>
- outbound_edges:
  - to: <peer-slug>
    relationship_label: <5-12 word verb phrase describing what THIS skill DOES with the peer>
    evidence: <path:line>
    edge_kind: <one of: delegates_to | validates_via | helper_call | routes_to | gates_on | references_for_truth | consumes_primitive | unclassified>
  - to: <peer-slug>
    relationship_label: ...
    evidence: ...
    edge_kind: ...
- inbound_callers (only when requested by parent prompt):
  - caller-slug, path:line, what the caller appears to use this skill for in 5-10 words
- stage_memberships:
  - <flow-registry / stage-contracts citation with path:line, OR "none">
- smell:
  - <one-sentence honest first-pass impression: is this skill a primitive, a router, a thin wrapper, an over-promoted helper, etc. — walker's read, NOT a verdict>
```

The schema is fixed. Walkers do not invent fields, do not omit fields, and
do not aggregate findings — that is the parent's job.

## Reference-extraction rules

The walker extracts semantically named peer-skill references from each walked
skill's SKILL.md and `references/*.md` (or `build/SKILL.md` and
`build/references/*.md` for Doctrine packages). The repository uses both
`` `$skill-slug` `` and exact backticked `` `skill-slug` `` spans for live
routes, so the contract must preserve both forms without treating arbitrary
code spans as graph edges. Rules:

### Match rule

- Count `\$[a-z][a-z0-9-]*` followed by a non-identifier boundary when it
  appears in regular Markdown prose or a semantically named inline span.
- Also inspect a standalone inline-code span whose entire contents are a
  lowercase exact peer slug such as `` `plan-audit` ``. Count it only when the
  slug resolves to a skill and the surrounding prose identifies a route,
  handoff, helper, validator, dependency, or other real skill relationship.
- Do not match an unprefixed slug merely because the same word appears as bare
  prose. The exact standalone inline span plus resolving target makes the
  candidate visible; the surrounding sentence decides whether it is an edge.

### Code-context filter (DG-16) — REQUIRED

**Skip all candidates** inside:

- Triple-backtick fenced code blocks (`` ```...``` ``).
- Indented (4-space) code blocks.

Inspect inline backtick spans semantically instead of excluding them wholesale.
This repository writes live peer routes as spans such as
`` `$agent-delegate` ``, `` `$arch-step` ``, `` `plan-audit` ``, and
`` `plan-conductor` ``. Count a standalone lowercase `$skill-slug` span when
the target resolves to a skill or the surrounding prose clearly identifies it
as a named skill route, handoff, helper, validator, or dependency. Preserve a
clearly named but non-resolving dollar-prefixed peer as an unresolved edge.
For an unprefixed inline span, require an exact resolving peer slug as well as
relationship-bearing prose; do not manufacture unresolved nodes from ordinary
command names, modes, or filenames that happen to be lowercase and hyphenated.

Do not assign an edge to the containing skill when a token appears only inside
a quoted sample, template, anti-example, or example of text that some other
artifact might contain. For example, an authoring guide that shows a sample
`AGENTS.md` sentence such as “call `$example-skill`” is teaching a writing
pattern; it does not mean the authoring skill itself calls that peer. Count an
example only when the surrounding source also asserts that the current skill
really owns that route or dependency.

Skip an inline span when it is code rather than a skill name: shell/environment
variables, assignments, paths, substitutions, placeholders, or command
expressions. Signals include uppercase or underscore variable names, braces,
slashes, equals signs, surrounding shell syntax, or prose that describes a
value/path instead of a skill. Real code-variable examples include:

- `arch_skill/skills/codex-review-yolo/SKILL.md` uses `$RUN_DIR` and
  `$FINAL_PATH` as shell variables inside backtick code spans.
- `lessons_studio/skills/studio-distill/build/references/studio-operating-doctrine.md:1`
  uses `$PSMOBILE_REPO_ROOT` as an environment variable in a backtick code span.

The token's case, exact target resolution, and syntax are useful signals, but
the surrounding sentence decides ambiguous cases. The goal is to keep real
backticked peer edges without turning shell variables, commands, modes,
filenames, or incidental code words into phantom nodes.

### Edge-kind classification rule

After matching a peer-skill reference, the walker classifies the edge-kind
by reading the surrounding 1-3 sentences of context:

- Look for verbs like "delegates", "hands off to", "routes to", "uses as helper",
  "validates against", "gates on", "references", "consumes" — these map directly
  to the closed enum.
- If no clear verb context exists, classify as `unclassified` honestly and let
  the audit surface it as a finding. Do NOT guess to make the substrate look
  cleaner.

### Relationship label rule

Write the relationship label as a 5-12 word verb phrase that says what the
calling skill DOES with the peer. Examples:

- "delegates manifest building to" (delegates_to)
- "validates output of" (validates_via)
- "is helper called inside stage X" (helper_call)
- "routes to as specialist when Z" (routes_to)
- "gates on completion of" (gates_on)
- "references for X contract" (references_for_truth)

If the relationship is unclear from the text, use the literal label
"unclear-relationship" and set `edge_kind: unclassified`. Do NOT invent a verb
phrase that the SKILL.md does not support.

## Audit-only / read-only contract for walkers

Each walker is read-only against the target skill suite:

- Read `SKILL.md` and `references/` files only. Use exact file reads and `rg`.
- **Do not write to ANY file in the target skill suite.** No edits, no creations.
- Do not spawn children or invoke delegation, consultation, or review skills.
- Do not invent edges that the SKILL.md text does not declare.

If a walker encounters an unreadable SKILL.md (file missing, malformed,
permission denied), report the failure in its return value with the file path
and the failure mode. The parent decides whether to abort or proceed with
partial coverage.

## Parent aggregation contract

After all walkers return, the parent agent:

1. Confirms the target git/diff state did not change during the read-only walk.
2. Validates each walker block against the schema (no missing fields, no
   invented fields, every edge_kind from the closed enum).
3. Checks the accounting ledger: every resolved slug has exactly one accepted
   owner return; missing, duplicated, or failed slices remain explicit.
4. Collects every distinct skill mentioned in any walker's `outbound_edges`
   that is NOT in the resolved scope list — these become `external` nodes (if
   the slug resolves to a SKILL.md outside the walked scope) or `unresolved`
   nodes (if no SKILL.md exists for the slug anywhere).
5. Writes the substrate document at `<doc-dir>/<doc-slug>_DAG.md` per the format
   in `dag-substrate-format.md` — three surfaces (mermaid graph, edge table,
   unresolved-reference list).
6. Begins audit reasoning by reading the substrate document back and applying
   the recognition tests in `waste-pattern-catalog.md`.

The parent does NOT silently improve walker evidence. If a walker returned an
edge with `edge_kind: unclassified`, that edge appears in the substrate as
`unclassified` and surfaces as a finding.
