# Tiny Substrate Fixture (5 nodes, 6 edges)

Used by `render_dag_d2.py` snapshot test. Mirrors the substrate format from
`../../references/dag-substrate-format.md`.

```mermaid
flowchart TB
    classDef router fill:#FFE4B5,stroke:#B54708,stroke-width:2px
    classDef stage fill:#FFFFFF,stroke:#B54708
    classDef specialist fill:#E6F4FF,stroke:#1E5FA8
    classDef primitive fill:#E8F5E8,stroke:#067647

    R[fixture-router]:::router
    S1[fixture-stage-one]:::stage
    S2[fixture-stage-two]:::stage
    SP[fixture-specialist]:::specialist
    P[fixture-primitive]:::primitive

    R -- "routes_to: stage one for canonical phase A" --> S1
    R -- "routes_to: stage two for canonical phase B" --> S2
    S1 -- "delegates_to: data ops" --> P
    S2 -- "delegates_to: data ops" --> P
    S1 -- "routes_to: specialist for narrow check" --> SP
    SP -- "validates_via: baseline check" --> S1
```

| from | to | edge_kind | relationship_label | evidence (path:line) |
| ---- | -- | --------- | ------------------ | -------------------- |
| fixture-router | fixture-stage-one | routes_to | routes_to stage one for canonical phase A | skills/fixture-router/SKILL.md:10 |
| fixture-router | fixture-stage-two | routes_to | routes_to stage two for canonical phase B | skills/fixture-router/SKILL.md:11 |
| fixture-stage-one | fixture-primitive | delegates_to | delegates data ops to primitive | skills/fixture-stage-one/SKILL.md:20 |
| fixture-stage-one | fixture-specialist | routes_to | routes to specialist for narrow check | skills/fixture-stage-one/SKILL.md:25 |
| fixture-stage-two | fixture-primitive | delegates_to | delegates data ops to primitive | skills/fixture-stage-two/SKILL.md:18 |
| fixture-specialist | fixture-stage-one | validates_via | validates_via baseline check | skills/fixture-specialist/SKILL.md:14 |

## Unresolved references

_None._
