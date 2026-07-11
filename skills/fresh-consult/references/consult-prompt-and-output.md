# Consult Prompt And Output

The consult brief must make the reviewer useful whether it is a clean native
child, a clean external session, or a bounded exact-child follow-up. A new
clean turn has no parent-chat context. A resumed turn has only that reviewer's
own history plus the bounded delta. Transport, context, and continuation are
separate choices.

Fresh consult is a strict yes/no arbiter. The child decides whether the user's
ask is fully satisfied. If the answer is not a clean yes, the verdict is
`fail` with specific reasons.

## Prompt Skeleton

Adapt this shape to the actual question. Send it as the native child task brief,
or write it to `prompt.md` when using the external lane:

```markdown
You are performing a read-only fresh consult on <one-line subject>.

<For a new clean reviewer:>
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

- Transport: <active-host native child | external runtime/session>
- Starting context: <clean | exact-reviewer history>
- Continuation: <new-clean | exact-resume | clean-rotation>
- Native mechanism: <Codex fork_turns "none" | Claude clean named/custom
  subagent | exact-child resume | other explicit host mechanism | "external">
- Child/session handle: <exact handle or "pending">
- External receipt mode: <fresh-resumable | resume | fresh-forced |
  fresh-rotated | "not applicable">
- Chain directory: <absolute external chain path or "not applicable">
- Turn: <n>
- Resume source: <exact native child handle, prior external turn dir, explicit
  external session id, or "none">
- Reason for fresh start: <none | new_independent_gate | user_forced_cold |
  chain_turn_limit | changed_execution | missing_session | ambiguous_chain>
- Nested fanout: <"prohibited" by default, or an explicit bounded scope and
  concurrency budget assigned by the parent>

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

Do not edit or write files, run formatters, coordinate directly with sibling
consults, create child agents, invoke delegation/consult skills, or start
another controller. Only a nested scope and budget explicitly assigned above
can relax the no-child rule.

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
4. Name the transport, explicit starting context, continuation choice, and
   exact child/session handle. For external review, also name the
   runtime/model/effort, receipt mode, chain directory, and run directory.
5. Run a parent-owned status or diff check before accepting the no-edit claim.
6. Spot-check failure reasons before treating them as true.
7. If you disagree with the child after spot-checking, say so explicitly.
8. For parallel groups, report each child verdict separately before writing any
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
  reviewer for the same consult line; external resumes must also stay in the
  same runtime.
- Reuse an old reviewer for a new independent gate. Independence requires a new
  clean child even when an exact handle is available.
- Launch an external same-provider process merely to obtain clean context or
  exact continuation that the host already provides natively. External
  transport remains valid when its concrete benefit is worth the process cost.
- Tell reviewers to maximize their own fanout. The parent owns decomposition,
  concurrency, evidence checking, and synthesis unless it explicitly budgets a
  nested scope.
