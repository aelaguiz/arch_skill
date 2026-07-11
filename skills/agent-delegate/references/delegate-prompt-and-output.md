# Delegate Prompt And Output

The external delegation prompt must make the worker useful without relying on
the parent chat. Fresh prompts have no session history. Resume prompts do have
that exact worker's session history, but still need a bounded instruction,
unchanged constraints, and explicit new evidence. The parent owns fanout,
scope assignment, and integration.

## Prompt Skeleton

Write a prompt like this to `prompt.md` and adapt the sections to the actual
task:

```markdown
You are an externally delegated worker for <one-line subject>.
You do not have the parent chat context. Read the repo and artifacts directly
from disk.
Your job is to complete the delegated task in the shared worktree, verify it,
and report exactly what changed.

# Delegation Mode

- Transport: external process/session
- External benefit: <provider, exact model/profile, lifecycle, process
  isolation, automation, structured receipt, or another concrete reason>
- Starting context: <clean prompt-and-disk context | existing exact session context>
- Continuation: <new one-shot | new resumable session | exact-session resume>
- Mode: fresh-one-shot | fresh-resumable | resume
- Resume source: <previous run directory, session id, or "none">

# Parallel Group

- Group: <group objective, or "none">
- Child id: <stable child id, or "single">
- Sibling tasks: <short names of sibling tasks, or "none">
- Nested fanout: <"prohibited" by default, or an explicit bounded scope and
  concurrency budget assigned by the parent>

<For resume mode only: Continue the same delegated task using your existing
session history. Apply the new instruction or evidence below. The original
success bar, work root, allowed write scope, constraints, and report contract
still apply unless this prompt explicitly changes them.>

<For parallel groups only: You are not alone in this codebase. Other delegated
workers may be editing the same repo at the same time. Do not revert unfamiliar
changes. Make the smallest task-relevant edits you can. If you hit an actual
conflict with another worker's changes, stop and report the files and evidence
instead of guessing.>

# Delegated Task

- Task: <the exact work to do>
- Success bar: <what makes the task complete>
- Work root: <absolute path>
- Allowed write scope: <paths, file families, or "repo-wide if needed for this task">
- Constraints: <commands, style rules, no-go areas, deadlines, or "none">
- User-named inputs: <paths, failing command, repro steps, doc section, issue, or "none">

# Required Local Instructions

Before editing, read the applicable local instructions, including any
`AGENTS.md` files that cover files you will touch. Follow the deepest applicable
instructions. If a local instruction conflicts with this prompt, report the
conflict before proceeding unless the conflict can be resolved by using the more
specific repo instruction.

# Capabilities And Boundaries

You may:

1. Read and search files.
2. Edit files inside the allowed write scope.
3. Run commands needed to inspect, implement, format, lint, test, or verify.
4. Use installed skills when their trigger and contract fit the delegated task.
5. Make pragmatic implementation decisions that are implied by repo evidence.
6. Make local implementation choices inside the assigned scope.

You must not:

1. Commit, push, create pull requests, rewrite history, or stash changes unless
   the task explicitly asks for that exact operation.
2. Revert unrelated work or user changes.
3. Start external continuation controllers, detached background workers, or nested
   orchestration workflows as a continuation strategy.
4. Create child agents or invoke delegation/consult skills unless the parent
   explicitly assigned a bounded nested scope and concurrency budget above.
5. Expand beyond the allowed write scope unless the task is impossible without
   it; if that happens, stop and report the blocker.
6. Paste or expose secrets. Use environment variables when the task requires a
   secret that is already available in the environment.

# Process

Please do all of the following:

1. Read the local instructions and user-named inputs, then inspect whatever repo
   evidence is needed to complete the task.
2. Inspect the current repo state before editing.
3. Implement the smallest change that satisfies the success bar.
4. Use installed skills only when they directly improve the delegated work and
   do not violate the parent-owned fanout boundary.
5. Run verification proportional to the changed surface.
6. Re-read changed files or inspect the diff before finalizing.
7. If blocked, stop with a precise blocker instead of inventing a workaround.

# Report Contract

End with this exact footer:

STATUS: done | partial | blocked | failed
CHANGED FILES: <paths or "none">
SKILLS USED: <skills or "none">
VERIFICATION: <commands/results or "not run: reason">
BLOCKERS: <bullets or "none">
FOLLOW-UP NEEDED: <bullets or "none">
SUMMARY FOR PARENT: <one concise paragraph>
```

## Status Semantics

- `done` - the delegated task satisfies the success bar and verification is
  adequate for the changed surface.
- `partial` - useful work landed, but some in-scope work remains.
- `blocked` - the child could not proceed because of a missing prerequisite,
  unclear requirement, unsafe write scope, unavailable tool, failing dependency,
  or conflict with local instructions.
- `failed` - the child attempted the task but ended with a broken state,
  unrepaired error, or verification failure.

`CHANGED FILES` must name every file the child intentionally changed. If the
child changed generated or lock files, include those too.

`VERIFICATION` must say exactly what ran and whether it passed. If verification
did not run, the reason must be concrete.

## Parent Report

When reporting the result upstream:

1. Lead with `STATUS` verbatim.
2. Include changed files, skills used, verification, blockers, and follow-up.
3. Name the runtime/model/effort and the run directory.
4. Name the external transport, concrete benefit, starting context, delegation
   mode, and session id when the run is resumable.
5. Check repo status before reporting changed files as final truth.
6. Spot-check blockers and changed-file claims before treating them as true.
7. If you disagree with the child after spot-checking, say so explicitly.
8. For parallel groups, report each child status separately before writing the
   combined outcome, then include the parent-side repo-state check.

A `partial` child result is progress, not closure. It must never close the
parent user goal by itself. Before reporting the combined outcome as complete,
the parent must name the unresolved in-scope work, decide whether the next move
is continue, repair, ask, or stop at an explicit boundary, and name the owner
file, phase, worker scope, or review finding for that continuation.

## Good Delegated Tasks

- "Implement the missing parser tests in `pkg/parser` and run the package
  tests."
- "Use `$skill-authoring` to tighten this one skill package's trigger boundary."
- "Investigate why this CLI test fails, fix the root cause, and verify it."
- "Update README and Makefile for this new install surface."
- "Refactor this prompt with `$prompt-authoring`, preserving the intended
  behavior."

## Anti-Patterns

Do not:

- Delegate vague work without naming the success bar or write scope.
- Use this skill for a read-only cold read. Use `$fresh-consult`.
- Launch an external same-provider process merely to get clean context,
  parallelism, or continuation that the active host's native children already
  provide. Account for the external-process cost described in the owning skill
  and shared policy without treating it as a ban.
- Ask the child to keep working asynchronously after the parent returns.
- Hide missing context behind parent summaries. Point at ground truth.
- Ask the child to use external continuation controllers or ordered subprocess workflows
  as part of this foreground delegation path.
- Ignore known shared-owner collisions when planning fanout. Sequence colliding
  work or assign non-overlapping write scopes; do not treat mere file proximity
  as proof of a collision.
- Resume an ambiguous "latest" session instead of an explicit session id or
  prior run directory.
- Change runtime when resuming a session. Resume through the same runtime that
  created the session.
- Treat the child as final authority. It is a capable worker whose output still
  needs parent-side sanity checks.
- Tell workers to maximize their own fanout. The parent owns decomposition and
  concurrency unless it explicitly assigns a bounded nested scope and budget.
- Reuse old run directories for new turns. A resume turn still gets a new run
  directory that points back to the previous session source.
