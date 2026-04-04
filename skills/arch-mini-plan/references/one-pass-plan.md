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
   - prompt surfaces, native capabilities, and existing tool/file/context exposure when the work is agent-backed
3. Write `research_grounding`:
   - what you inspected
   - what matters
   - what constraints the code already imposes
   - what can be solved by prompt, grounding, or native-capability changes before new tooling
   - what instruction-bearing source content must keep explicit structure instead of being summarized
4. Write `current_architecture` and `target_architecture` together.
5. Write the `call_site_audit`:
   - changed files
   - representative call sites
   - deletions or consolidation work
   - capability-replacing side paths to delete or justify when agent-backed
6. Write the `phase_plan`:
   - phase goal
   - concrete work
   - smallest credible verification
   - capability-first work before custom tooling when agent-backed
   - explicit deletes and follow-ups
7. End with a readiness verdict:
   - ready for `arch-step implement`
   - or too large / too weak, use `arch-step reformat`
   - if preserving instruction-bearing source fidelity cleanly would need appendices or a fuller import surface, use `arch-step reformat`

## External guidance rule

- Pull in external guidance only when it changes correctness or idiomatic design.
- Keep it short and fold its implications directly into the plan.
- Do not turn mini mode into a bibliography.

## Output rule

- Write back to `DOC_PATH`.
- Do not create second notes or scratch plans.
- Keep the console summary short and name the exact next command.
