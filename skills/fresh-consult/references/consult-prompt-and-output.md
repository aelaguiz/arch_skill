# Consult Prompt And Output

The consult prompt must make the child useful whether the turn is a clean-start
consult or a bounded same-session follow-up. A fresh-start turn has no parent
chat context. A resume turn has its own child-session history, but still has no
unstated parent context beyond the new prompt.

Fresh consult is a strict yes/no arbiter. The child decides whether the user's
ask is fully satisfied. If the answer is not a clean yes, the verdict is
`fail` with specific reasons.

## Prompt Skeleton

Write a prompt like this to `prompt.md` and adapt the sections to the actual
question:

```markdown
You are performing a read-only fresh consult on <one-line subject>.

<For fresh-resumable, fresh-forced, or fresh-rotated:>
You are starting clean from disk and this prompt. You have no prior parent chat
context. Read the artifacts directly from disk. Your job is to answer the
user's ask for the parent agent, not to fix files.

<For resume:>
You are resuming the same fresh-consult child session for <one-line subject>.
Use your existing child-session history plus the new ask below. You still do
not have the parent chat context beyond what is in this prompt. Re-read files
when the answer depends on current repo state. Do not assume old file contents
are still current.

# Consult Mode

- Mode: fresh-resumable | resume | fresh-forced | fresh-rotated
- Chain directory: <absolute chain path>
- Turn: <n>
- Resume source: <prior turn dir, explicit session id, or "none">
- Reason for fresh start: <none | user_forced_cold | chain_turn_limit | changed_execution | missing_session | ambiguous_chain>

# User Ask

<quote the user's ask when practical; otherwise give a faithful one-paragraph
restatement without adding the caller's own framing>

# Working Context

- Work root: <absolute path>
- User-named artifacts or target paths:
  - <path, commit, branch, doc, or "none">
- Hard constraints: <read-only limits, runtime constraints, or "none">

# Your Job

Read the user-named artifacts or target paths directly. Then inspect whatever
nearby repo, docs, research, tests, command output, or local evidence you judge
necessary to answer the user's ask. Report what you read and what answer the
evidence supports.

Maximize parallelism by using parallel agents. Do not invoke skills that spawn subagents.

Do not edit files, run formatters, coordinate with sibling consults, or start
another controller.

# Report Contract

End with this exact footer:

VERDICT: pass | fail
FAILURE REASONS: <specific bullets or "none">
EVIDENCE READ: <paths, commands, or anchors actually inspected>
CONFIDENCE: high | medium | low
SUMMARY FOR PARENT: <one concise paragraph>
```

## Verdict Semantics

- `pass` - the artifacts fully satisfy the consult question and are good enough
  with no material caveats.
- `fail` - anything short of a clean yes. This includes incomplete work,
  unresolved notes, missing proof, uncertainty, confusing quality, malformed
  evidence, or not enough inspected evidence to answer.

`FAILURE REASONS` must name the file, heading, command, artifact, claim, or
decision that fails. For code or repo-backed consults, cite line numbers when
practical. A `pass` must use `FAILURE REASONS: none`.

`CONFIDENCE: low` must pair with `VERDICT: fail`. Low confidence means the
child cannot cleanly say yes.

`EVIDENCE READ` is required. A consult that does not say what it inspected is
not actionable.

## Parent Report

When reporting the result upstream:

1. Lead with `VERDICT` verbatim.
2. Quote failure reasons exactly when there are only a few; summarize only when
   the list is long.
3. Include confidence and evidence read.
4. Name the runtime/model/effort, consult mode, chain directory, run directory,
   and session id when captured or reused.
5. Spot-check failure reasons before treating them as true.
6. If you disagree with the child after spot-checking, say so explicitly.
7. For parallel groups, report each child verdict separately before writing any
   synthesis. Treat disagreement between children as useful signal, not a
   majority vote.

## Good Consult Questions

- "Is this flow linear and not confusing to a cold reader?"
- "Did the implementation actually complete Phase 3 in `docs/MY_PLAN.md`?"
- "Is the skill boundary between these packages clear enough?"
- "Are there contradictions between the README install surface and Makefile?"
- "Does this prompt preserve the source intent without heuristic shortcuts?"
- "Resume the same consult and ask whether the edited plan fixed its concern."

## Anti-Patterns

Do not:

- Ask "review this" without naming the actual decision or artifact.
- Paste huge diffs inline when the child can run `git diff` or read files.
- Hide missing context behind parent summaries. Point at ground truth.
- Ask the child to fix, refactor, or implement as part of the consult.
- Return `pass` with caveats, notes to triage, or unresolved uncertainty. If it
  is not a clean yes, return `fail`.
- Treat the child as final authority. It is an independent read, not a judge
  that overrides repo evidence.
- Overwrite old turn directories. A resume turn gets a new run directory that
  points back to the previous turn.
- Resume a latest session by convenience. Resume only the exact captured
  same-runtime session for the same consult line.
