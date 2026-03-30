# Arch Mini Plan Fit And Contract

## Use mini-plan when

- the user wants a compact plan in one pass
- the task still benefits from canonical arch blocks
- you can keep the plan to roughly 1-2 main phases plus optional cleanup

## Escalate to full arch when

- the work becomes clearly multi-checkpoint or cross-cutting
- external research dominates the planning effort
- the plan wants 4+ phases or a broad migration/cutover
- there is too much ambiguity to responsibly compress into one pass

## Required blocks

Write or update these blocks in `DOC_PATH`:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`

Use the same marker shapes as the full arch flow so the doc remains compatible with `arch-plan` and `arch-flow`.

## Output contract

- planning only
- no code changes
- one-pass writeback into `DOC_PATH`
- explicit verdict on whether the next move should be:
  - local implementation against the same doc
  - escalation to `arch-plan`
