# Arch Flow Checklist Rules

Use this file when `arch-flow` needs to decide what is done vs pending from `DOC_PATH` and `WORKLOG_PATH`.

## DOC_PATH and WORKLOG_PATH

- Prefer an explicit `docs/<...>.md` path.
- Derive `WORKLOG_PATH` as:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`

## Shared evidence signals

- North Star confirmed:
  - `status: active` or `status: complete` in frontmatter
- Research grounding:
  - `arch_skill:block:research_grounding`
- External research:
  - `arch_skill:block:external_research`
  - or planning-passes evidence that `external_research_grounding` is done
- Deep dive:
  - `arch_skill:block:current_architecture`
  - `arch_skill:block:target_architecture`
  - `arch_skill:block:call_site_audit`
- Phase plan:
  - `arch_skill:block:phase_plan`
- Review gate:
  - `arch_skill:block:review_gate`
- Gaps audit:
  - `arch_skill:block:gaps_concerns`
- Implementation audit:
  - `arch_skill:block:implementation_audit`
- Worklog exists:
  - `WORKLOG_PATH` exists on disk
- Scope and Simplicity Contract:
  - human authorization anchors are present
  - initial minimal convergence closure is present or explicit `none`
  - scope freeze is present before implementation
  - required phase work does not exceed the frozen contract

## Full arch checklist

1. plan doc exists
2. North Star confirmed
3. Scope and Simplicity Contract complete and frozen
4. research grounding
5. deep dive pass 1
6. external research when needed
7. deep dive pass 2 when the external research materially changed the plan
8. phase plan
9. optional plan-shaping moves:
   - plan enhance
   - fold in
   - overbuild protector
   - review gate
   - UI ASCII when UI is in scope
10. implementation + worklog
11. post-checks:
   - gaps audit
   - implementation audit
12. docs cleanup handoff
13. explicit-review-only helpers such as code review or PR finalization

## Mini full-arch checklist

1. plan doc exists
2. North Star confirmed
3. Scope and Simplicity Contract complete and frozen
4. research grounding
5. deep dive
6. phase plan
7. implementation + worklog
8. post-checks:
   - implementation audit
   - docs cleanup handoff

## Arch-mini-plan follow-through checklist

1. plan doc exists
2. North Star confirmed
3. Compact Scope and Simplicity Contract complete and frozen
4. one-pass canonical blocks written:
   - research grounding
   - current architecture
   - target architecture
   - call-site audit
   - phase plan
5. implementation + worklog
6. post-checks:
   - implementation audit
   - docs cleanup handoff
   - any explicit follow-up audit

Recommend `miniarch-step` as the governing skill once mini-plan is complete and the next move is execution or auditing, unless the doc clearly outgrew the faster full-arch tier.

## Lilarch checklist

1. plan doc exists
2. North Star confirmed
3. Compact Scope and Simplicity Contract complete and frozen
4. requirements block exists
5. plan audit exists
6. compatible arch blocks exist as needed:
   - research grounding
   - current architecture
   - target architecture
   - call-site audit
   - phase plan
7. finish-mode implementation + worklog
8. implementation audit

## Output rule

- Every checklist line should be marked `DONE`, `PENDING`, `OPTIONAL`, or `UNKNOWN`.
- Every line should include a short evidence note, for example:
  - marker present
  - marker missing
  - file missing
  - `status: draft`

## Governing-skill recommendation

- For full-arch docs, recommend `arch-step` until the code audit is clean, then recommend `arch-docs`.
- For mini full-arch docs, recommend `miniarch-step` until the code audit is clean, then recommend `arch-docs`.
- For arch-mini-plan follow-through into implementation or audits, recommend `miniarch-step` until the code audit is clean, then recommend `arch-docs`, unless the doc clearly outgrew the faster full-arch tier.
- For lilarch docs that still fit lilarch, recommend `lilarch`.
