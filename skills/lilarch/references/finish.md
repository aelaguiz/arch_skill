# Lilarch Finish Mode

## Goal

Implement under active-host ownership against the compact doc, keep the worklog
current, and audit without inventing a new plan.

## Required behavior

- Re-read `DOC_PATH` before changing code.
- Create or repair `WORKLOG_PATH`.
- Implement phase by phase.
- Before the first edit, verify the contract is frozen and every active item is
  `authorized` or `frozen-convergence-required`.
- For agent-backed behavior, prefer the planned prompt, grounding, or native-capability edits before adding new tooling.
- Run the smallest credible checks after meaningful work.
- Update `arch_skill:block:implementation_audit` before declaring completion.
- Classify new findings with the shared scope dispositions. A newly discovered
  same-contract path is still `new-scope-needs-human` after freeze; do not add
  it automatically. Subtract `unauthorized-built-scope`.

## Optional clean child use

The parent may assign a clean same-host native implementation child a
low-collision slice only when its owner paths do not overlap another writer.
Give it `DOC_PATH`, the exact slice, allowed write paths, required checks, the
frozen scope boundary, and a return contract covering files changed, checks
and results, unresolved findings, collision risks, and its durable handle. The
parent retains ownership of `DOC_PATH`, `WORKLOG_PATH`, scope decisions, and
final integration. Children do not create children unless the parent
explicitly assigned a bounded nested scope and budget.

If that slice needs repair, resume the exact implementer handle with the
accepted findings and current delta. If confidence needs an independent
completion recheck, start a new clean same-host native reviewer. In Codex use
`fork_turns: "none"`; in Claude Code use a clean named or custom subagent.
Give the reviewer read-only capability when available plus explicit no-edit and
no-write guidance. Record repo state before dispatch, verify it after the
return, and let the parent integrate the evidence and write the authoritative
audit block.

An external implementation or review session is still valid when its concrete
provider, exact-model/profile, lifecycle, isolation, automation, or receipt
benefit is worth the added process and integration cost. Name that benefit in
the dispatch rather than externalizing ordinary same-host work by habit.

## Completion rule

Mark the doc complete only when:

- the intended code changes exist
- obvious call sites are updated
- required deletes happened or are assigned to an explicit named follow-up in the doc
- any new tooling for agent-backed behavior is explicitly justified by the doc rather than invented during finish mode
- verification evidence is recorded

## Escalation during finish mode

- If the change stops fitting the compact plan, stop and escalate to `miniarch-step reformat <DOC_PATH>` or `arch-step reformat <DOC_PATH>`, depending on how broad the work became.
- Do not quietly grow lilarch into a second full-arch workflow.
- Do not use escalation or a plan rewrite to normalize agent-created scope.
