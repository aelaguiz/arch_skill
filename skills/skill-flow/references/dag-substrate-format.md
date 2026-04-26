# DAG Substrate Format

The substrate is the agent's reasoning surface during a DAG-grounded audit run.
It is one markdown document the parent agent writes from parallel-walk evidence,
then reads back when producing findings. The format below is the SSOT.
Every other reference (parallel-walk-protocol, waste-pattern-catalog,
lessons-studio-worked-example) points here for node-kind and edge-kind vocabulary.

## File naming

`<doc-dir>/<doc-slug>_DAG.md` — the substrate is written alongside the audit
findings doc. Same audit run → one substrate file. Re-extract every run; never
trust a stale substrate.

## Document shape (three surfaces, one file)

The substrate document contains three surfaces in this order:

1. **Surface A: Mermaid `flowchart` graph block.** Topology view with node-kind
   styling via `classDef`. Edge labels in mermaid syntax. Good for at-a-glance
   scanning.
2. **Surface B: Markdown edge table.** Carries the full 5-12 word relationship
   labels and `path:line` evidence that mermaid syntax struggles with at scale.
   This is the surface the agent reads when reasoning about waste patterns.
3. **Surface C: Unresolved-reference list.** Every `$skill-slug` peer reference
   that did not resolve to a node in the walked set. Empty list is rendered
   as `_None._` (do not omit the section).

## Surface A: mermaid graph block

Use `flowchart TB` (top-bottom) or `flowchart LR` (left-right). Choose based on
whether the suite reads better top-down (flow-controllers above stages above
specialists above primitives) or left-right.

### Node-kind closed enum (9 values)

Every node has exactly one node-kind. The closed enum:

| node-kind | meaning | mermaid `classDef` color |
| --------- | ------- | ------------------------ |
| `router` | Skill whose primary job is selecting and dispatching to other skills (e.g., `studio-authoring-flow-controller`). High fan-out is normal. | `fill:#FFE4B5,stroke:#B54708,stroke-width:2px` (amber) |
| `orchestrator` | Skill that coordinates a multi-step process owning judgment but delegating execution to specialists or primitives. | `fill:#FFF4D6,stroke:#B54708` (light amber) |
| `stage` | Skill that owns one canonical authoring stage in a flow. | `fill:#FFFFFF,stroke:#B54708` (white) |
| `specialist` | Skill that owns a narrow technical or domain check, called by a stage or orchestrator. | `fill:#E6F4FF,stroke:#1E5FA8` (light blue) |
| `primitive` | Skill that owns deterministic data operations (CRUD, validation, schema). High fan-in is normal. | `fill:#E8F5E8,stroke:#067647` (light green) |
| `presentation` | Skill that owns rendering, formatting, or display surfaces. | `fill:#F4E6FF,stroke:#6B2FB3` (light purple) |
| `diagnostic` | Skill whose primary job is retrospective analysis or session inspection (e.g., session-distill style). | `fill:#F0F0F0,stroke:#666,stroke-dasharray:4 2` (gray, dashed) |
| `external` | Node referenced by a walked skill but outside the walked scope (the skill exists in a different repo or was excluded from this run's scope). | `fill:#F8F8F8,stroke:#999,stroke-dasharray:2 2` (light gray, dashed) |
| `unresolved` | Node referenced by a walked skill that does NOT resolve to any skill in the walked set. Surfaces as a finding via the unresolved-reference list. | `fill:#FFE4E1,stroke:#B54708,stroke-dasharray:2 2` (pink, dashed) |

Copy-paste palette block for the substrate's mermaid block:

```mermaid
flowchart TB
    classDef router fill:#FFE4B5,stroke:#B54708,stroke-width:2px
    classDef orchestrator fill:#FFF4D6,stroke:#B54708
    classDef stage fill:#FFFFFF,stroke:#B54708
    classDef specialist fill:#E6F4FF,stroke:#1E5FA8
    classDef primitive fill:#E8F5E8,stroke:#067647
    classDef presentation fill:#F4E6FF,stroke:#6B2FB3
    classDef diagnostic fill:#F0F0F0,stroke:#666,stroke-dasharray:4 2
    classDef external fill:#F8F8F8,stroke:#999,stroke-dasharray:2 2
    classDef unresolved fill:#FFE4E1,stroke:#B54708,stroke-dasharray:2 2
```

### Edge-kind closed enum (8 values)

Every edge has exactly one edge-kind:

| edge-kind | meaning |
| --------- | ------- |
| `delegates_to` | A delegates ownership of an operation to B. A keeps judgment; B does the work. |
| `validates_via` | A uses B as a precondition validator before doing its own work. B's output gates A's progression. |
| `helper_call` | A invokes B as a stateless helper inside A's own work. No ownership transfer. |
| `routes_to` | A selects B as the canonical next stage / specialist owner for a downstream task. |
| `gates_on` | A waits for B to reach a stable state before A proceeds. |
| `references_for_truth` | A treats B as the authoritative source for a contract or definition. |
| `consumes_primitive` | A reads or invokes B as a deterministic data primitive (CRUD, schema validation). |
| `unclassified` | The walked sub-agent could not pick a clean edge-kind from the closed set. **MUST surface as a finding** via the unresolved-reference list or as a separate audit finding — never silently swallowed. |

### Edge label vocabulary

Every edge in the mermaid block carries a 5-12 word relationship label using
verb phrases drawn from this vocabulary. These are illustrative templates, not
a closed enum — pick the verb phrase that most accurately describes what the
calling skill DOES with the peer:

- `delegates_to`: "delegates X to", "hands ownership of Y to"
- `validates_via`: "validates X against", "uses as baseline validation before X"
- `helper_call`: "uses as helper for X", "calls inline for X"
- `routes_to`: "routes to as specialist when X", "names as canonical stage owner of X"
- `gates_on`: "gates on X completing", "waits for X to stabilize before"
- `references_for_truth`: "references for X contract", "treats as authority on X"
- `consumes_primitive`: "consumes for X", "reads X via"

Bare adjacency (`A --> B` with no label) is a substrate-writer bug.

### Mermaid edge syntax

Use `A -- "<label>" --> B` for labeled edges. Multi-word labels work fine:

```
MAT[studio-playable-materializer]:::orchestrator
GW[psmobile-lesson-layout-guided-walkthrough]:::specialist
MAT -- "routes_to: visible-state and beat proof for guided steps" --> GW
```

The label inside quotes carries the full relationship phrase. Apply node-kind
class via `:::class-name`.

## Surface B: markdown edge table

Beneath the mermaid block, the substrate carries a markdown table that holds
the full label and evidence anchor for every edge. Required column shape:

```
| from | to | edge_kind | relationship_label | evidence (path:line) |
| ---- | -- | --------- | ------------------ | -------------------- |
| skill-A | skill-B | delegates_to | delegates manifest building to | skills/skill-A/build/SKILL.md:42 |
```

- `from`: the calling skill's slug.
- `to`: the called peer skill's slug.
- `edge_kind`: one value from the closed enum.
- `relationship_label`: 5-12 word verb phrase, same vocabulary as the mermaid label.
- `evidence (path:line)`: at least one `path:line` anchor showing where the
  reference appears in the calling skill's SKILL.md or its references.

## Surface C: unresolved-reference list

```
## Unresolved references

| from | unresolved-target | evidence (path:line) |
| ---- | ----------------- | -------------------- |
| skill-A | $imaginary-peer | skills/skill-A/build/SKILL.md:88 |
```

If every reference resolved, render the section heading with body `_None._`
— do not omit the section. The audit reads this list when checking for
broken-edge waste patterns.

## Determinism contract

Same `skills/` input → same substrate output. Re-running on an unchanged tree
must produce a substrate that is functionally equivalent (node ordering by
slug ascending; edge table sorted by `from` ascending then `to` ascending).
Mermaid block layout may have minor visual variation due to mermaid's own
layout engine, but the underlying node and edge declarations must be stable.

The parent agent achieves determinism by:

- Sorting walked skills alphabetically by slug before declaring nodes.
- Sorting outbound edges per skill alphabetically by target slug.
- Aggregating the edge table in `from`-then-`to` lexicographic order.
- Emitting mermaid node IDs as short uppercase abbreviations of slugs (e.g.
  `studio-playable-materializer` → `MAT`) — abbreviations are derived
  deterministically from the slug, not invented per-run.

## Audit-only contract

The substrate document is a read-only artifact for the agent's reasoning. It
is written once per audit run from sub-agent evidence and is NOT edited by
the audit reasoning step. Findings are emitted in the audit's text output
using the existing 6-field template; the substrate is the grounding, not the
finding store.
