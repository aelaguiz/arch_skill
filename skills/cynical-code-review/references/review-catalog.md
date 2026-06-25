# Cynical Review Catalog

Use this catalog after the target and suspicion map are clear. It is review
doctrine, not a rule system. Apply judgment, read real code, and cite evidence
you actually inspected.

The central question is:

```text
What did the implementation make look true without making it true in current code?
```

For every pattern:

- name the implementation claim being tested
- identify the current code authority, or say there is no clear owner yet
- search for old and alternate paths that can still express the same concept
- trace the actual runtime path instead of trusting names, comments, status, or
  tests
- decide whether the change converges the system or leaves two ways to be right
- flag only current-code or requested-scope risks with concrete evidence

## Completion Story Authority Drift

Flag when the review target says or implies the work is complete, but completion
is grounded in a proxy: status block, plan checkbox, worklog, reviewer launch,
green test, branch name, local frontier, or summary.

Common lies:

- "complete for the current frontier" narrows the user's done state
- a plan status says `COMPLETE` while manual proof, review, or code paths are
  still open
- a reviewer was launched, so the parent treats the work as reviewed
- tests passed for a narrower behavior than the requested one
- a branch or PR title matches the goal, so the code is assumed aligned

Read:

- the user request or completion claim
- controlling plan or source truth when supplied
- changed code and affected owners
- review logs or status docs only as claims
- old authority paths and unfinished review findings

Block when the claim is still false in current code, old behavior remains
reachable, requested review findings are untriaged, or the completion boundary
was narrowed without the user's consent.

Do not block merely because the wording is imperfect if code reality is correct
and no future agent would be misled.

Example:

```markdown
### [REQUIRED REPAIR] Completion claim says lane identity is unified but puzzle still derives a local key

- File: src/puzzle/PuzzleRoute.ts
- Symbol / line: `buildVisibleLaneKey`
- Claim being tested: "Phase 2 unified prewarm and visible puzzle lane identity."
- Risk: The visible route still derives `table_scene_*` locally while prewarm
  reads from `SceneLaneRegistry`. The same handoff has two authorities.
- Evidence: `PuzzleRoute.ts` calls `buildVisibleLaneKey`; `PrewarmRoute.ts`
  calls `SceneLaneRegistry.keyFor`.
- Repair target: Route the visible puzzle path through the registry or delete
  the old local derivation.
- Cynical review pattern: completion story authority drift
```

## Name-Only Completion Or False Unification

Flag when a new name, wrapper, class, comment, route, phase label, or status
uses the right words but the behavior underneath is still old, split, partial,
or narrower than the claim.

Common lies:

- a new `Unified*`, `Canonical*`, or `SingleSource*` object exists but only one
  caller uses it
- a wrapper forwards to the old behavior unchanged
- a "deleted" path remains registered behind an alias or fallback
- tests assert the new label rather than the intended outcome
- docs say centralized while code keeps direct writers

Read:

- the new named owner and old owner
- all public entrypoints for the concept
- representative callers, readers, writers, tests, fixtures, prompts, examples,
  generated artifacts, and configs
- deletion or migration notes when present

Block when the old behavior remains live, callers can choose between old and
new owners, the wrapper owns no invariant, or the new path covers only a happy
path while siblings stay split.

Do not block when the old path is unreachable, the wrapper now owns a real
invariant, or a short explicit compatibility shim delegates immediately to the
new owner and has a deletion point.

## Old Authority Path Still Live

Flag when an implementation claims migration, deletion, centralization, or
simplification while old authority can still affect behavior.

Common lies:

- old command or route still registered
- direct writer still imported by one sibling
- fallback reader silently accepts the old shape
- generated artifact still contains old contract
- fixture or example still makes the old path look supported
- compatibility flag keeps both systems selectable after convergence is claimed

Read:

- old API, route, command, store, adapter, schema, prompt, generated file, and
  config names
- import graph and public registries
- tests/fixtures that instantiate old models
- docs/examples only when they keep the old path alive or teach future use

Block when user-visible or externally observable behavior can still enter
through the old path, when both data shapes are accepted without one adapter
boundary, or when the old owner can mutate the same concept.

Do not block when old code is dead, historical, clearly out of scope, or
normalizes immediately through the new owner.

## Duplicate Truth Or Split-Brain Owner

Flag when current code has two live ways to express, mutate, validate, render,
serialize, route, prompt, configure, or prove the same concept.

Common lies:

- "we centralized it" but UI reads local state while a job reads a service
- two schemas describe one API contract
- one path validates in a form and another validates at the server
- one prompt says use the new flow while another live prompt names the old flow
- two generated artifacts can drift

Read:

- all owners that can read or write the concept
- caller and lifecycle boundaries
- generated artifacts and schemas
- prompts/docs/examples that guide future callers
- tests that instantiate either truth

Block when both truths remain reachable, callers must know which one to use,
bridging is implicit, or future work can update one truth and leave the other
stale.

Do not block when contracts are genuinely different and the review can name the
difference, or when one adapter owns the bridge.

## Partial Migration Or Stopped-Short Implementation

Flag when one route, caller, product surface, command, or phase moved to the new
model while adjacent same-contract paths stayed old.

Common lies:

- one button uses the new service while a sibling button calls the old writer
- one route accepts the new schema while another route still accepts old shape
- one plan phase says "done" while later in-scope obligations still depend on
  old behavior
- a "unified" path handles only initial load, not refresh, edit, retry, or
  failure states

Read:

- adjacent routes, jobs, commands, UI actions, API methods, prompts, scripts,
  old aliases, compatibility flags, fallbacks, docs, examples, and migration
  notes
- success, failure, refresh, retry, persistence, and cleanup paths

Block when the user can still reach the old behavior, when same-contract
siblings diverge, or when the implementation stops before the behavior that
made the plan matter.

Do not block when scope explicitly moved one isolated caller, no shared
invariant is broken, and the leftover path is named as out of scope.

## User Job Missed From The Starting State

Flag when code implements a real surface or command, but it does not let the
user complete the actual job from the starting state that matters.

Common lies:

- an editor can choose among existing options but cannot create or assign the
  missing thing
- a tool works only after synthetic state setup no user can reach
- an automation path advances through hidden state instead of user-facing
  controls
- a UI supports the happy path but not the initial empty, silent, missing,
  legacy, or errored state named by the user

Read:

- the user's intended job in plain English
- UI/CLI/API entrypoints from the relevant starting state
- state creation, editing, persistence, and failure paths
- tests or docs only when they reveal a narrower job assumption

Block when the code supports an internal interpretation but not the user's
workflow, or when proof depends on synthetic shortcuts the user did not
authorize.

Do not block when the user job was genuinely narrower and code supports that
starting state.

## Historical Split Rationalized As Architecture

Flag when the review or implementation explains existing divergence by labels,
class names, roles, route names, lanes, or comments without proving a real
contract difference.

Common lies:

- current names are treated as product truth
- old wiring is explained as architecture after the fact
- multiple modes exist because they emerged over time, then are defended as
  intentional
- "this one is table, that one is ambient" replaces a first-principles contract
  comparison

Read:

- product behavior each path must support
- runtime/platform constraints
- shared renderer/owner contracts
- call flow and data flow for both paths
- history only if available and useful, never as a substitute for current code

Block when no product, runtime, or compatibility reason justifies the split and
the split keeps duplicate truth, extra roles, special cases, or divergent
behavior alive.

Do not block when the review can name a real contract difference and show where
code enforces it.

## Proxy Proof, Receipt Theater, Or Status Laundering

Flag when proof-like artifacts make incomplete code look done.

Common lies:

- checkboxes, audit blocks, or readiness labels are formatted but not earned
- "verified" means a command ran, not that the right behavior exists
- "all phases" were supposedly covered in an implausible time window
- logs, tests, or internal proof match the model while user-visible behavior
  or externally observable behavior still contradicts the target
- a child review is launched but not finished or triaged

Read:

- the claimed proof surface
- the code path the proof claims to validate
- generated artifacts or test fixtures involved in proof
- child-agent outputs if native agents were used

Block when the proof surface hides a current-code gap, proves the wrong layer,
or lets old behavior remain reachable.

Do not block merely because no proof was run unless the review target requires
that proof and the absence masks a current-code risk.

## Docs, Tests, Prompts, Or Comments As Misdirection

Flag when instruction or proof surfaces contradict code reality, preserve old
paths, or would mislead the next developer or agent into reintroducing the bug.

Common lies:

- docs say central owner while examples import direct writer
- tests duplicate production rules and pass when the owner is wrong
- comments say "single source" over code that reads a local copy
- prompt doctrine names archived or old runtime behavior as live
- status says deleted while package metadata or command aliases still expose it

Read:

- touched docs/tests/prompts/comments and nearby live truth surfaces that name
  changed symbols, commands, APIs, env vars, install surfaces, schemas, routes,
  stable IDs, or generated artifacts
- production owners and callers they claim to describe

Block when the surface masks a current-code gap, teaches a live old path,
contradicts generated/runtime behavior, or makes future agents trust a false
source.

Do not emit doc hygiene or test-coverage findings. The blocker is the code
truth being hidden or distorted.

## Harness, Policy, Or Machinery Overbuild

Flag when the implementation adds a framework, harness, policy layer, flag
matrix, controller, abstraction, or proof system that does not make the target
code behavior true.

Common lies:

- the machinery feels robust, so the root code problem is treated as solved
- a tiny fix becomes a new policy with more roles and lanes
- diagnostic work becomes a permanent harness
- a wrapper hides a direct bug without deleting the old path
- a script owns workflow judgment instead of narrow deterministic mechanics

Read:

- the root behavior the user asked to change
- new layers, flags, wrappers, scripts, controllers, and policies
- old code paths that the machinery should have deleted or routed through one
  owner
- caller burden before and after

Block when the machinery adds live concepts, hides the same old problem, makes
debugging harder, or replaces direct root-cause work with ceremony.

Do not block narrow deterministic helpers that genuinely remove repeated
mechanics while leaving judgment in code or the agent.

## Scope Contamination Or Adjacent Drift

Flag when a targeted implementation changes adjacent behavior that was not part
of the request.

Common lies:

- shared styles or render paths change neighboring UI
- a cleanup touches a sibling workflow
- a broad abstraction changes semantics for callers outside the target
- a "centralized" helper changes old behavior that should have stayed stable

Read:

- diff hunks around adjacent surfaces
- shared owners used by the changed code
- sibling components, routes, commands, and user-visible states
- git history only when exact restoration is needed

Block when unrelated in-scope behavior changed or adjacent user-visible
contracts drifted without an explicit requirement.

Do not block expected shared behavior changes that the user requested and the
code carries through consistently.

## Environment Or Target Confusion

Flag when the review cannot honestly bind the code under review to the branch,
checkout, running app, log source, generated artifact, or target path.

Common lies:

- cwd and live process come from different checkouts
- branch name matches the theme but diff is from another branch
- logs or artifacts were produced by a different build
- generated files belong to an old source state

Read:

- current working directory
- git status, branch, baseline, and target diff
- named live process, log, build, generated output, or artifact source when the
  review depends on it

Block with `coverage-incomplete` when target confusion prevents an honest code
verdict.

Do not block when the review is purely static and no live/process claim is part
of the target.

## Agent, Prompt, Or Skill Surface Regression

Flag instruction-bearing code or docs that make future agents easier to fool,
less capable, or more likely to bypass judgment.

Common lies:

- a skill depends on hidden history instead of self-contained runtime doctrine
- examples become a hidden rulebook
- a runner owns judgment that belongs to the agent
- several skills claim the same review lane with no boundary
- source, generated, install, and runtime surfaces disagree

Read:

- changed `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, prompt files, `agents/*.yaml`,
  references, generated outputs, install docs, Makefile targets, and sibling
  skills with overlapping descriptions

Block when the shipped surface creates duplicate runtime truth, revives
archived behavior, makes routing ambiguous, or moves reasoning into unjustified
scaffolding.

Do not block examples that teach reasoning while the principle lives in the
main contract and the agent still owns synthesis.
