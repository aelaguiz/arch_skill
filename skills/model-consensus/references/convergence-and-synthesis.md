# Convergence And Synthesis

Consensus is a quality claim, not a transcript shape. Two models have
converged only when they accept the same small answer for the same reasons and
all hard requirements remain covered.

## Valid Consensus

Call the run converged when:

- both models explicitly sign off on the same candidate answer
- hard user requirements are still present
- repo-dependent claims have file evidence
- new pathways are justified or avoided
- rejected alternatives are named briefly
- remaining risks are residual, not unresolved architecture choices

## Invalid Consensus

Do not call it consensus when:

- one model stops objecting only because the prompt asks for signoff
- the final plan combines every idea from both sides
- the models use the same words but mean different architectures
- a hard requirement disappeared during simplification
- repo evidence is missing for a repo-backed claim
- an unresolved decision is hidden as an implementation detail

## Anti-Kitchen-Sink Rule

When one model proposes A and B, and the other proposes C, the final answer is
not automatically A+B+C. Ask:

- Which idea is necessary for the user goal?
- Which idea can be deferred without violating the quality bar?
- Which idea duplicates an existing repo pathway?
- Which idea creates a new failure mode?
- Can one smaller abstraction satisfy both concerns?

The best result is often a shorter plan after the dialogue than either first
pass produced.

## Parent Synthesis Boundaries

The parent may:

- compress agreed points
- remove repeated transcript material
- organize the plan into clear sections
- call out evidence and rejected alternatives
- ask one more signoff round if the candidate consensus is parent-written

The parent must not:

- add a new architecture that neither model reviewed
- silently choose one side after a material disagreement
- turn unresolved disagreement into an implementation TODO
- claim repo grounding that the children did not actually perform

## No-Consensus Output

If the models do not converge, produce a useful non-consensus result:

```text
Status: no consensus

Resolved:
- <points both models agree on>

Unresolved decision:
- <smallest real decision>

Model A position:
- <position and evidence>

Model B position:
- <position and evidence>

Why it remains unresolved:
- <missing evidence, user preference, or actual tradeoff>

Recommended next user decision:
- <one concrete choice or question>
```

No-consensus is not failure when the disagreement is real. It is better than a
fake compromise.

## Final Response Shape

Use this compact shape unless the user asked for a different artifact:

```text
Participants
- Model A: <runtime/model/effort/role>
- Model B: <runtime/model/effort/role>

Status
- converged | no consensus | blocked

Consensus
<lean agreed result>

Requirement Coverage
<brief mapping from hard requirements to plan elements>

Repo Grounding
<paths and patterns that shaped the result, if applicable>

Rejected Alternatives
<short list with reasons>

Remaining Risks
<only material residual risks>

Artifacts
<run directory>
```

Keep the final result useful. Do not paste long child transcripts unless the
user explicitly asks.
