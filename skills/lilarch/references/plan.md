# Lilarch Plan Mode

## Goal

Write the minimal architecture and delivery plan needed to ship the feature cleanly.

## Required work

1. Read the doc and verify the task still fits 1-3 phases.
2. Gather the smallest useful repo evidence:
   - implementation anchors
   - representative call sites
   - tests or verification surfaces
   - prompt surfaces, native capabilities, and existing tool/file/context exposure when the feature is agent-backed
   - instruction-bearing source content that must keep explicit structure if it is re-homed into the compact doc
3. Write or repair:
   - `research_grounding`
   - `current_architecture`
   - `target_architecture`
   - `call_site_audit`
   - `phase_plan`
   - make the capability-first choice explicit before adding custom tooling for agent-backed behavior
   - inspect the exact changed contract for directly competing owner paths;
     include only their smallest cutover/delete in the initial convergence
     closure and exclude merely similar neighbors
4. Run the internal plan audit and write the result into `lilarch:block:plan_audit`.

The plan audit is not scope authority. It may reject a missing or overbroad
contract, but it cannot add an adjacent surface. Before finish mode, record an
explicit closure or `none`, verify every phase item maps to human scope or that
closure, and freeze the contract.

If preserving instruction-bearing source fidelity cleanly would no longer fit the compact doc, escalate to `miniarch-step reformat` or `arch-step reformat` instead of silently compressing it.

## Plan shape

- Phase 1:
  - core implementation or cutover
- Phase 2:
  - dependent follow-through or validation
- Phase 3:
  - cleanup only if cleanup is real work, not wishful thinking

## Escalation rule

- If the authorized outcome plus minimal pre-freeze closure needs a fourth
  phase, stop and escalate to `miniarch-step reformat`. Do not escalate because
  the audit imagined more work.
- If the work also brings broad rollout logic or heavy plan shaping, stop and escalate to `arch-step reformat`.
