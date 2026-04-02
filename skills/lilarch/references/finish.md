# Lilarch Finish Mode

## Goal

Implement locally against the compact doc, keep the worklog current, and self-audit without inventing a new plan.

## Required behavior

- Re-read `DOC_PATH` before changing code.
- Create or repair `WORKLOG_PATH`.
- Implement phase by phase.
- Run the smallest credible checks after meaningful work.
- Update `arch_skill:block:implementation_audit` before declaring completion.

## Completion rule

Mark the doc complete only when:

- the intended code changes exist
- obvious call sites are updated
- required deletes happened or are explicitly deferred in the doc
- verification evidence is recorded

## Escalation during finish mode

- If the change stops fitting the compact plan, stop and escalate to `arch-step reformat <DOC_PATH>`.
- Do not quietly grow lilarch into a second full-arch workflow.
