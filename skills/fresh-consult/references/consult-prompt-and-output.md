# Consult Prompt And Output

The consult prompt must make the child useful from a cold start. It has no
session history and should not be trusted to infer the parent skill's unstated
context.

## Prompt Skeleton

Write a prompt like this to `prompt.md` and adapt the sections to the actual
question:

```markdown
You are performing an independent fresh consult on <one-line subject>.
You have no prior chat context. Read the artifacts directly from disk. Your job
is to answer the user's ask for the parent agent, not to fix files.

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

Do not edit files, run formatters, arm hooks, coordinate with sibling consults,
or start another controller.

# Report Contract

End with this exact footer:

VERDICT: pass | pass-with-notes | fail | inconclusive
BLOCKING: <bullets or "none">
NON-BLOCKING: <bullets or "none">
EVIDENCE READ: <paths, commands, or anchors actually inspected>
CONFIDENCE: high | medium | low
SUMMARY FOR PARENT: <one concise paragraph>
```

## Verdict Semantics

- `pass` - the artifacts satisfy the consult question with no material caveats.
- `pass-with-notes` - the core answer is acceptable, but the notes should be
  triaged.
- `fail` - at least one blocking issue prevents approval or confidence.
- `inconclusive` - the child could not inspect enough evidence to answer.

`BLOCKING` issues must name the file, heading, command, artifact, or decision
that fails. For code or repo-backed consults, cite line numbers when practical.

`EVIDENCE READ` is required. A consult that does not say what it inspected is
not actionable.

## Parent Report

When reporting the result upstream:

1. Lead with `VERDICT` verbatim.
2. Quote blocking findings exactly when there are only a few; summarize only
   when the list is long.
3. Include non-blocking notes, confidence, and evidence read.
4. Name the runtime/model/effort and the run directory.
5. Spot-check blocking findings before treating them as true.
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

## Anti-Patterns

Do not:

- Ask "review this" without naming the actual decision or artifact.
- Paste huge diffs inline when the child can run `git diff` or read files.
- Hide missing context behind parent summaries. Point at ground truth.
- Ask the child to fix, refactor, or implement as part of the consult.
- Treat the child as final authority. It is an independent read, not a judge
  that overrides repo evidence.
- Reuse old run directories across consults.
