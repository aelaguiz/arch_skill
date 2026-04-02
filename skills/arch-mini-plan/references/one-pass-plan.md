# Arch Mini Plan One-Pass Workflow

## Goal

Write the canonical planning blocks in one pass without pretending the work was simpler than it is.

## Order of work

1. Repair the artifact if needed:
   - frontmatter
   - TL;DR
   - North Star
   - required block markers
2. Gather internal anchors:
   - files
   - symbols
   - tests
   - reusable patterns
3. Write `research_grounding`:
   - what you inspected
   - what matters
   - what constraints the code already imposes
4. Write `current_architecture` and `target_architecture` together.
5. Write the `call_site_audit`:
   - changed files
   - representative call sites
   - deletions or consolidation work
6. Write the `phase_plan`:
   - phase goal
   - concrete work
   - smallest credible verification
   - explicit deletes and follow-ups
7. End with a readiness verdict:
   - ready for `arch-step implement`
   - or too large / too weak, use `arch-step reformat`

## External guidance rule

- Pull in external guidance only when it changes correctness or idiomatic design.
- Keep it short and fold its implications directly into the plan.
- Do not turn mini mode into a bibliography.

## Output rule

- Write back to `DOC_PATH`.
- Do not create second notes or scratch plans.
- Keep the console summary short and name the exact next command.
