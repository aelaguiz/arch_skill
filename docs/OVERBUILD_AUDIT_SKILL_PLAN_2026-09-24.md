# Overbuild Audit skill plan (2026-09-24)

Evidence: `docs/OVERBUILD_PATTERNS_FROM_AGENT_HISTORY_2026-09-24.md` and its evidence folder.

## Job and leverage

Agents overbuild by default: scope nobody asked for, machinery for hypothetical problems, ceremony, second copies, and old paths kept alive. Amir catches it by hand, and 62% of his overbuild pushback comes after the thing is already planned or built. The skill makes one repeatable pass that measures a plan or an implementation against what was actually asked for, and returns a cut list. Planning, delivery and review skills call it at two moments: before building, and before the final review.

## Canonical asks

- "Where are we overbuilding in this plan?"
- "Is this PR overbuilt relative to what I asked for? What do we rip out?"
- A parent skill (issue-to-pr, milestone-to-pr, epic-to-prs, conductor, arch planners) runs it on its written plan before implementation and on the diff before the final review.

Anti-case: "Review this PR for bugs." That goes to normal review or `cynical-code-review`.

## Mechanism

A prompt-only skill with no scripts. Why it is a skill and not a prompt: the same judgment is needed across a dozen lanes, it depends on the user's intent and a large body of examples the model will not reconstruct, and callers need one owner for it.

## Peer fit

| Peer | Its job | Boundary |
|---|---|---|
| `startup-pragmatism` | Resets the agent's operating frame: decide at partial information, rigor only where wrongness is expensive, team pace | It changes how the agent decides. `overbuild-audit` checks a specific artifact piece by piece against the ask and returns the cut list. Each hands off to the other. |
| `cynical-cruft-removal` | Repo-wide deletion report of low-value artifacts, whatever the current ask | `overbuild-audit` measures one plan or change against its ask. |
| `cynical-code-review` | Is the implementation story true? | Its overbuild/scope lens uses `overbuild-audit`'s types. |
| `plan-audit` | Plan readiness and plan-backed code audit | Its simplicity and subtraction findings use `overbuild-audit`'s types. |
| arch-step `overbuild-protector` | Sorts an arch phase plan into scope buckets A–G | Its judgment of F (scope creep) and G (theatre) uses `overbuild-audit`'s intent and types. |

## Package

- `SKILL.md`, about 200 lines:
  - commander's intent: what the user wants and does not want, the one test, and the boundary;
  - when to use it;
  - the workflow;
  - the 24 types as six compact families of questions;
  - plan versus implementation emphasis;
  - the output contract.
- `references/overbuild-types.md`: every type with what it looks like and many real examples. Each example gives what was built, the user's words, and the simple version.
- `references/casebook.md`: worked audits end to end (plans and implementations), including over-cutting cases where the user wanted more.
- `agents/openai.yaml`: implicit invocation on; a default prompt that matches the contract.

## Wiring

| Skill | Where | What |
|---|---|---|
| issue-to-pr | Delivery contract, workflow steps 1 and 3, goal prompt | Audit the written plan before the final's plan check; audit the diff before publishing; carry the intent into the goal |
| milestone-to-pr | Quality, workflow steps 2 and 5, goal prompt | Same, at milestone scale |
| epic-to-prs | Contract, workflow steps 1 and 4, goal prompt | Same, at epic and stack scale |
| delegated-implementation | Briefs and parent review | Briefs carry the do-not-build line; the parent's own review cuts what workers built beyond the brief (no new gate) |
| conductor | Plan sign-off and final review | Plan audit before dispatch, diff audit before completion |
| arch-step, miniarch-step, arch-mini-plan, lilarch | Plan readiness and implementation audit | Audit before the ready verdict and in the code audit |
| plan-audit | Subtraction lens | Use the types |
| bugs-flow | Fix plan and fix review | Guessed fixes, symptom patches, fallbacks |
| cynical-code-review, cynical-architecture-review, exhaustive-code-review | Overbuild and subtraction lenses | Use the types |
| pr-review-followthrough | Bot and CI findings | Decline findings that add machinery beyond the ask |
| startup-pragmatism | When not to use | Hand artifact audits to overbuild-audit |
| arch-skills-guide, README, usage guide, Makefile | Inventory | List and install the skill |

**Constraint on the wiring:** the audit must not become process overhead. It is one pass that the coordinator runs itself. It adds no review rounds and no approval gates, and a clean result needs no follow-up.
