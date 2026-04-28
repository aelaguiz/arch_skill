# Consult Prompt And Output

The consult prompt must make the child useful from a cold start. It has no
session history and should not be trusted to infer the parent skill's unstated
context.

## Prompt Skeleton

Write a prompt like this to `prompt.md` and adapt the sections to the actual
question:

```markdown
You are performing an independent fresh consult on <one-line subject>.
You have no prior chat context. Read the artifacts directly from disk and be
skeptical. Your job is to answer the consult question for the parent agent, not
to fix files.

# Consult Question

- Question: <the exact thing to decide>
- Success bar: <what would make the answer pass/approve/ready>
- Work root: <absolute path>

# Parallel Group

- Group: <group objective, or "none">
- Child id: <stable child id, or "single">
- Sibling consults: <short names of sibling questions, or "none">

<For parallel groups only: Answer only this child's consult question. Sibling
consults may inspect related artifacts, but you should not coordinate with them
or wait for them.>

# Authoritative Artifacts

- <path, commit, branch, or doc section> - <why it matters>
- <path, commit, branch, or doc section> - <why it matters>

# Claims Or Completion Targets

If explicit claims, checklist items, or completion targets exist, audit them:

1. <claim or target>
2. <claim or target>

If there are no explicit claims, say so and inspect the artifact directly.

# What To Check

Please do all of the following:

1. Read the authoritative artifacts directly.
2. Check whether the consult question is answered by the artifacts.
3. Identify contradictions, missing steps, unclear ordering, stale claims, or
   completion gaps relevant to the consult.
4. Separate blocking issues from non-blocking notes.
5. Do not edit files, run formatters, arm hooks, coordinate with sibling
   consults, or start another controller.

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

`BLOCKING` issues must name the file, heading, command, claim, or checklist item
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
