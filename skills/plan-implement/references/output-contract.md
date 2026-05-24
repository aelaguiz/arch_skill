# Output Contract

Keep chat output short. The implementation log carries detail; the chat should
name the current state, evidence, and next move.

## Progress Update Shape

Use this during active implementation:

```markdown
Plan scope: <phase/section/checklist item>
Current state: <one sentence>
Changed: <paths or behavior summary>
Proof: <run | reused | stale | not yet needed>
Review: <clean | findings opened | findings repaired | not yet run>
Artifacts: <plan/audit log/implementation log updates>
Next: <one useful move>
```

Do not include filler sections.

## Final Scope Report Shape

Use this at the requested stop boundary:

```markdown
Plan scope: <phase/section/checklist item>
Result: complete | partially complete | blocked | stopped at boundary
Implementation log: <path or not applicable>
Audit log: <path or not applicable>

Changed:
- <high-signal behavior or files>

Plan State:
- <items completed, not completed, or changed>

Proof:
- <checks run, supplied proof accepted, reused proof, stale proof, or proof not run with reason>

Review:
- <IMP findings opened/repaired/rejected/open>

Still Open:
- <real remaining gap or none>

Next:
- <one exact next move>
```

## Rules

- Name the implementation log path when one exists.
- Name the audit log path when one exists.
- Be explicit about proof reuse and stale triggers.
- Do not claim completion from logs alone.
- Do not imply tests or checks ran when they did not.
- Do not bury blockers behind progress language.
- Do not turn the final answer into a copied worklog.
- If the stop boundary was honored with unfinished adjacent work, say so.

## Completion Words

Use `complete` only when:

- the in-scope plan outcome is true in code
- old paths and side doors in scope are deleted, migrated, or explicitly
  classified
- relevant review findings are resolved, rejected with rationale, or out of
  scope
- proof is run, supplied, or reused with a freshness rationale
- source-truth decisions are carried into the plan
- the implementation log names code, proof, and review anchors

Use `partially complete` when useful code landed but any in-scope plan outcome
remains false or unreviewed.

Use `blocked` when a decision, unread required code surface, failing proof, or
unresolved blocking review finding prevents completion.
