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

## Full arch checklist

1. plan doc exists
2. North Star confirmed
3. research grounding
4. deep dive pass 1
5. external research when needed
6. deep dive pass 2 when the external research materially changed the plan
7. phase plan
8. optional plan-shaping moves:
   - plan enhance
   - fold in
   - overbuild protector
   - review gate
   - UI ASCII when UI is in scope
9. implementation + worklog
10. post-checks:
   - gaps audit
   - implementation audit
11. docs cleanup handoff
12. explicit-review-only helpers such as code review or PR finalization

## Mini full-arch checklist

1. plan doc exists
2. North Star confirmed
3. research grounding
4. deep dive
5. phase plan
6. consistency pass
7. implementation + worklog
8. post-checks:
   - implementation audit
   - docs cleanup handoff

## Arch-mini-plan follow-through checklist

1. plan doc exists
2. North Star confirmed
3. one-pass canonical blocks written:
   - research grounding
   - current architecture
   - target architecture
   - call-site audit
   - phase plan
4. implementation + worklog
5. post-checks:
   - implementation audit
   - docs cleanup handoff
   - any explicit follow-up audit

Recommend `miniarch-step` as the governing skill once mini-plan is complete and the next move is execution or auditing, unless the doc clearly outgrew the faster full-arch tier.

## Lilarch checklist

1. plan doc exists
2. North Star confirmed
3. requirements block exists
4. plan audit exists
5. compatible arch blocks exist as needed:
   - research grounding
   - current architecture
   - target architecture
   - call-site audit
   - phase plan
6. finish-mode implementation + worklog
7. implementation audit

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
