# Where The Interview Skill Fits In The Current Suite

Date: 2026-08-02. Grounded in a full read of: `conductor`, `plan-audit`,
`cynical-code-review`, `cynical-architecture-review`, `cynical-cruft-removal`,
`arch-step`, `arch-mini-plan` (+ its artifact contract), `plan-implement`,
`fresh-consult`, `skill-authoring`, `north-star-investigation`,
`_shared/agent-orchestration-policy.md`, `_shared/scope-and-convergence.md`.

## The pipeline today

```
Amir's dictated ask
  → planning skill (arch-mini-plan / arch-step / lilarch) writes DOC_PATH
  → optional plan-audit plan-readiness
  → conductor executes via cheap external fleet (sol ultra default)
  → final gate: whole-plan cynical sweep + 3 cynical reviews + cold verifier
  → delivery worker: pr-authoring + pr-review-followthrough
```

Every stage downstream of the first arrow is already well-doctrined. The weak
link is the first arrow: the "human-authorized outcome" that everything else
treats as the supreme authority is whatever Amir happened to say in one voice
message, plus whatever plan-shaping questions the planning skill fires at him.

## What downstream already demands (the interview's target contract)

The suite has ALREADY defined what a fully specified intake looks like — the
interview skill does not need to invent a schema, it needs to fill an existing
one:

1. **North Star block** (mini-plan artifact contract): claim, in scope, out of
   scope, definition of done, invariants.
2. **Scope and Simplicity Contract** (`_shared/scope-and-convergence.md`):
   - human-authorized outcome **and authorization anchors**
   - smallest sufficient solution
   - initial minimal convergence closure (or explicit `none`)
   - scope-freeze boundary
   - enough proof
   - do-not-build boundary
   - accepted residual risk
3. **Conductor readiness gate**: recoverable requirements, phases, observable
   done-ness, verification obligations — conductor refuses to dispatch without
   them, and stops mid-run to escalate when scope authority is unclear.
4. **Finding dispositions**: cynical reviews classify each finding as
   authorized / frozen-convergence-required / new-scope-needs-human /
   out-of-scope / unauthorized-built-scope. Triage is only mechanical when the
   frozen boundary and do-not-build boundary are explicit and specific.

Insight: **every failure class Amir named maps to a hole in that contract.**

| Amir's failure class | Missing contract element |
|---|---|
| Unintended new UX | intended-UX inventory + "no new user-visible surface" in do-not-build boundary |
| Review-wave scope creep | vague in-scope/out-of-scope → dispositions become judgment calls |
| Away-from-keyboard dumb questions | missing north star / first-principles context + undecided plan-shaping decisions |
| Fuzzy done-ness | weak definition of done + unspecified proof ("enough proof" left generic) |
| Retyped execution boilerplate | no home in any artifact for model assignments, worktree/sim pinning, review-wave policy |

## Gaps no current skill owns

- **Elicitation.** `arch-step` and `arch-mini-plan` ask questions only as a
  last resort ("ask only for true product, UX, external-constraint, access, or
  doc-path gaps") and are optimized to NOT bother the user. Nothing is
  optimized to systematically extract intent while the user is present and
  willing. `plan-audit` finds ambiguity but only after a plan exists, and
  routes gaps back to "the planning owner" — which is currently nobody.
- **Intended-UX capture.** The cynical architecture review treats "intended
  user experience" as the authority for what must continue to exist — but no
  artifact reliably records it. Reviews are anchored to a thing that was never
  written down.
- **Execution policy.** Model/effort per role, worktree pin, simulator pin,
  review-wave sequence, adversarial-review model, delivery model: conductor
  has defaults but Amir overrides them every run by typing. No plan block owns
  these; conductor asks "one consolidated question" for load-bearing values —
  i.e., it stops and waits for him.
- **Proxy interviewee.** `fresh-consult` gives clean read-only second opinions;
  nothing supports "answer as Amir would" delegation of interview questions.

## Boundary decision the plan must settle (duplicate-truth risk)

The interview output must NOT become a second plan. Under
`scope-and-convergence`, two live artifacts defining the same contract is
exactly the split-brain the suite hunts. The clean shape:

- Interview skill owns the **intent pack**: authorized outcome, north stars,
  intended-UX inventory, non-goals/do-not-build, done-definition, proof
  expectations, execution policy, open-decisions-now-closed. These are the
  *authorization anchors* the planning skill cites.
- Planning skill (arch-mini-plan/arch-step) still owns architecture: research
  grounding, current/target architecture, call-site audit, phase plan. It
  consumes the intent pack instead of interrogating Amir.
- Conductor consumes the plan; the intent pack's execution-policy block is the
  standing answer to conductor's intake questions.

## Repo red lines that constrain the build

- Prompt-first; no runner/controller/state machine; scripts only as narrow
  deterministic helpers.
- Skill doctrine self-contained; preserve agent judgment; direct v1 guidance
  without invented refusal paths.
- Any agent dispatch (immersion researchers, proxy interviewee) goes through
  `_shared/agent-orchestration-policy.md`; external transport needs a named
  concrete benefit.
- `$skill-authoring` governs the eventual package; `npx skills check` must
  pass; README/AGENTS.md routing entries update with the new skill.
