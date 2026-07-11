# Scope-Change Discipline: Cuts And Additions Need Authority

Apply `skills/_shared/scope-and-convergence.md`. The raw human goal and
human-approved decomposition are the epic baseline. Each sub-plan inherits that
boundary, may record the smallest evidenced same-contract convergence closure
during its initial architecture pass, and freezes that closure before
implementation.

The epic critic is a read-only detector. It can reject drift; it cannot create
scope. A worklog, Decision Log entry, reviewer recommendation, repeated critic
finding, or already-built path does not authorize an addition.

## What The Critic Checks

The critic compares the raw goal, approved decomposition, current sub-plan
Scope and Simplicity Contract, its freeze anchor, explicit human approvals,
worklog, Decision Log, and shipped code.

Material failures are:

1. **Missing authorized scope.** A raw-goal, decomposition, or frozen sub-plan
   obligation was cut, narrowed, skipped, or left without a named later owner.
2. **Post-freeze proposed expansion.** A newly discovered caller, behavior,
   constraint, mechanism, proof category, or sub-plan is absent from the frozen
   contract. This includes a real same-contract path first found by the critic.
3. **Unauthorized built scope.** Code, tests, schemas, configs, dependencies,
   docs, or operational surfaces were added after freeze without explicit human
   approval.
4. **Scope cycling.** Agent-created work became plan or code truth and later
   reviews used it to demand further expansion.

All four produce `verdict: scope_change_detected`. A missing or non-clean
arch-step implementation audit still produces `incomplete`.

## Discovered Item Shape

Use the existing `discovered_items[]` structure with these meanings:

```json
{
  "what": "one-sentence description with the authority gap",
  "scope_relationship": "new_scope_needs_human",
  "recommendation": "human_decision"
}
```

Allowed relationships and routes are:

- `missing_authorized_scope` → `complete_authorized_scope`;
- `new_scope_needs_human` → `human_decision`;
- `unauthorized_built_scope` → `subtract`.

The critic reports the disposition and evidence, not implementation steps. A
human may explicitly approve a new outcome or sub-plan and re-freeze it. Until
then, the orchestrator may only finish already-authorized work or
subtract/redesign inside the frozen boundary.

## Noise

Ignore implementation choices that stay inside the frozen outcome and do not
create durable new product or operational surface: file renames, local helper
refactors, ordinary style choices, or a library substitution that preserves the
same contract. Also ignore nice-to-have observations that are neither required
by frozen scope nor already built.

Extra tests, utilities, or abstractions are not automatically noise. When they
create durable maintenance surface absent from the contract, classify them as
unauthorized built scope.

## Human Decision Boundary

When scope expansion is proposed, halt and present two classes of choice:

- approve the expansion, choose whether it extends the current sub-plan or
  becomes a new sub-plan, update the canonical contracts, and re-freeze before
  implementation; or
- keep the frozen scope and require subtraction/redesign within it.

Do not phrase critic-derived expansion as already required. A critic may have
found a real architectural relationship; only the human decision owner can
decide that it belongs in this epic now.

Agent-written Decision Log entries are evidence, not approval. The log must
name the human decision owner and visible approval for any post-freeze
expansion.
