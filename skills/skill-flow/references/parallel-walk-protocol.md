# Parallel-Walk Protocol

The DAG-grounded audit fans out parallel sub-agents to walk the scoped skill
suite. Each sub-agent reads its assigned skills, returns structured per-skill
evidence, and the parent agent aggregates the evidence into the substrate
document. This file is the SSOT for that contract.

## Scope resolution (parent agent, before fanout)

The parent agent receives a plain-language scope phrase from the user. Resolve
it to a concrete skill list before any sub-agent is spawned. Recognized phrases:

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
  the slugs literally; verify each resolves to a SKILL.md before fanout.
- **Genuinely ambiguous phrases** → exact blocker question. Do not fanout on a
  guess. Example: "the recent skills" — ask which ones.

State the resolved skill list (count + slugs) in the audit's console output
before fanout begins so the user can confirm scope.

## Fanout sizing (parent agent decision)

The parent agent decides the fanout shape based on resolved scope size:

- **Slices ≤ 6 skills**: one sub-agent walks the entire slice. No real
  parallelism benefit at this size.
- **Slices 7-30 skills**: fanout sized so each sub-agent walks 3-6 skills.
  Aim for 3-5 parallel sub-agents.
- **Slices > 30 skills**: cap at 8 parallel sub-agents (host runtime cost
  rises sharply above this); each sub-agent walks 5-8 skills.

These are guidelines. The parent may adjust to keep per-sub-agent context
windows comfortable.

## Per-sub-agent evidence schema

Each sub-agent receives:

- The list of skills it must walk (full file paths).
- The closed edge-kind enum from `dag-substrate-format.md` (so the sub-agent
  uses the same vocabulary as the substrate).
- The reference-extraction rules below (especially the code-block whitelist).
- Whether `inbound_callers` is required for any walked skill (parent decides
  based on which skills look load-bearing or potentially lone-wolf).

Each sub-agent returns, **per assigned skill**, a block in this exact shape:

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
  - <one-sentence honest first-pass impression: is this skill a primitive, a router, a thin wrapper, an over-promoted helper, etc. — sub-agent's read, NOT a verdict>
```

The schema is fixed. Sub-agents do not invent fields, do not omit fields, and
do not aggregate findings — that is the parent's job.

## Reference-extraction rules

The sub-agent extracts `$skill-slug` references from each walked skill's
SKILL.md and `references/*.md` (or `build/SKILL.md` and `build/references/*.md`
for Doctrine packages). Rules:

### Match rule

- Pattern: `\$[a-z][a-z0-9-]*` followed by a non-identifier boundary (whitespace,
  punctuation, end-of-line).
- Match anywhere in regular markdown prose.

### Code-block whitelist (DG-16) — REQUIRED

**Skip** `$WORD` patterns inside:

- Backtick code spans: `` `$RUN_DIR` ``, `` `$FINAL_PATH` ``, `` `$PSMOBILE_REPO_ROOT` ``
- Triple-backtick fenced code blocks (`` ```...``` ``).
- Indented (4-space) code blocks.

These are shell variables, environment variables, or other code-context tokens —
not skill references. Real false-positive examples found in the wild:

- `arch_skill/skills/codex-review-yolo/SKILL.md:5-6` uses `$RUN_DIR` and
  `$FINAL_PATH` as shell variables inside a backtick code span.
- `lessons_studio/skills/studio-distill/build/references/studio-operating-doctrine.md:1`
  uses `$PSMOBILE_REPO_ROOT` as an environment variable in a backtick code span.

If the extractor matches inside any of these contexts, the substrate ends up
with phantom nodes that pollute the audit. Skip them.

### Edge-kind classification rule

After matching a `$peer-slug` reference, the sub-agent classifies the edge-kind
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

## Audit-only / read-only contract for sub-agents

Each sub-agent is read-only against the target skill suite:

- Read SKILL.md and references/ files only. Use Read or grep tools.
- **Do not write to ANY file in the target skill suite.** No edits, no creations.
- Do not invoke any other skill via the Task tool — sub-agents are pure walkers.
- Do not invent edges that the SKILL.md text does not declare.

If the sub-agent encounters an unreadable SKILL.md (file missing, malformed,
permission denied), report the failure in its return value with the file path
and the failure mode. The parent decides whether to abort or proceed with
partial coverage.

## Parent aggregation contract

After all sub-agents return, the parent agent:

1. Validates each sub-agent block against the schema (no missing fields, no
   invented fields, every edge_kind from the closed enum).
2. Collects every distinct skill mentioned in any sub-agent's `outbound_edges`
   that is NOT in the resolved scope list — these become `external` nodes (if
   the slug resolves to a SKILL.md outside the walked scope) or `unresolved`
   nodes (if no SKILL.md exists for the slug anywhere).
3. Writes the substrate document at `<doc-dir>/<doc-slug>_DAG.md` per the format
   in `dag-substrate-format.md` — three surfaces (mermaid graph, edge table,
   unresolved-reference list).
4. Begins audit reasoning by reading the substrate document back and applying
   the recognition tests in `waste-pattern-catalog.md`.

The parent does NOT modify sub-agent evidence. If a sub-agent returned an
edge with `edge_kind: unclassified`, that edge appears in the substrate as
`unclassified` and surfaces as a finding.
