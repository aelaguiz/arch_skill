# Review Prompt Template

Use this skeleton when drafting a namespaced prompt file such as `$PROMPT_PATH`.
Fill every `<...>` placeholder.

## Skeleton

```markdown
You are performing an independent review of <one-line subject>. The requester
wants a skeptical external audit before <next step>. Read the artifacts
directly. If the work is not approved, say so plainly.

# Review Goal

- Requested decision: <what approval means here>
- Standard for approval: <the bar codex should apply>
- Working directory: <absolute path>

# User-Named Artifacts Or Target Paths

- <path | commit | branch | doc | command to inspect current state>
- <path | commit | branch | doc | command to inspect current state>

# Hard Constraints

- <review-only, token/env handling, local boundary, or "none">

# How To Work

Read the named artifacts directly. Then inspect whatever nearby repo, docs,
tests, command output, or local evidence you judge necessary to decide whether
the review goal is met. Report evidence-backed findings only.

# How To Report

End with a final verdict block:

    VERDICT: approve / not-approved / inconclusive
    REQUIRED REPAIRS: <list required repairs, or "none">
    OBSERVATIONS: <list informational observations, or "none">
    ASSESSMENT: <one paragraph on whether the artifact meets the review goal>

Be direct. I want the real assessment, not reassurance.
```

## Example adaptations

These are examples, not a mandatory menu. Adapt the skeleton to the actual review goal.

### Example: diff-only review

If the artifact is a single uncommitted diff rather than commits:

- In "User-Named Artifacts Or Target Paths", list "Uncommitted diff in
  <branch>; run `git diff HEAD` from the working directory."

### Example: implementation completion audit

If the user wants an external audit of whether a plan phase or implementation
checklist was actually completed:

- In "Review goal", define the approval bar in terms of completion, not shipping.
- In "User-Named Artifacts Or Target Paths", list the user-named plan,
  checklist, branch, commit, or diff that defines the completion target.

### Example: plan / design doc review

If the artifact is a plan doc (not code):

- In "User-Named Artifacts Or Target Paths", list the doc path and any
  user-named sections in scope.
- In "Review Goal", state the approval decision the doc needs to earn.
- Keep the generic verdict block unchanged.

### Example: cross-repo / submodule review

When both a super-repo commit and a submodule commit need to be audited together:

- In "User-Named Artifacts Or Target Paths", list both. Explicitly note which
  commits belong to which repo.
- Tell codex: "The submodule lives at `services/<name>`; `git -C services/<name> log` is how you read its history."

## Anti-patterns

Don't:

- Send a terse prompt like "review my work" — codex has no context and will hallucinate.
- Omit the verdict block — you'll get a narrative that's hard to act on.
- Treat one example above like a hardcoded prompt shape — adapt the sections to the real review objective.
- Paste the diff inline instead of pointing at commits or files — it inflates the prompt and codex can't cross-reference with the rest of the tree.
- List secrets inline. Point at `.env` and source it into the codex env before invocation.
- Ask codex to "also fix the issues it finds". This skill is review-only; fixing is a separate turn after you've read the verdict.

## Sizing

Keep the prompt under ~400 lines. If it's growing beyond that, you're probably trying to audit too much in one pass — split into two audits (e.g. "code correctness" and "drift-proofing strength") and run them in parallel.
