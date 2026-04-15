# Arch Mini Plan Fit And Escalation

## Good fits

- "Give me the mini plan version for this feature flag cleanup."
- "I want one pass that grounds the repo, maps current and target architecture, and gives me a tight plan."
- "This is bigger than lilarch but still small enough that I do not want staged research and deep-dive commands."

## Bad fits

- "Do the full arch flow and implement it."
- "We need several checkpoints, external research, and multiple rounds of plan shaping."
- "This is mostly a regression investigation."
- "The path is unknown and we need to iterate on bets."

## Escalate out of mini mode when

- the plan needs 4 or more real phases
- the task spans several subsystems and wants staged checkpoints
- external research becomes a first-class deliverable instead of a narrow helper
- implementation or audit work is now part of the ask
- the existing doc is too non-canonical to trust

## Escalation targets

- Escalate to `lilarch` when the task is actually a small 1-3 phase feature flow.
- Escalate to `miniarch-step` when the work now needs faster full-arch execution against the same canonical doc.
- Escalate to `arch-step reformat <DOC_PATH>` when the work is now broader or more ambiguous real full-arch work.
- Escalate to `bugs-flow` when investigation dominates.
- Escalate to `goal-loop` or `north-star-investigation` when the path is intentionally open-ended.

## Boundary examples

- Event handler rename across two call sites with one follow-up delete:
  - still mini mode
- Storage-layer migration plus rollout concerns plus compatibility decisions:
  - escalate to `miniarch-step` or `arch-step`
- Tiny UX tweak with one implementation pass:
  - use `lilarch`
