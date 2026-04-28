---
name: agent-delegate
description: "Delegate a concrete task to a Claude or Codex subprocess with full local agent capabilities. Use when the user wants another agent to implement, edit, investigate-and-fix, run commands, use installed skills, or resume a previously delegated same-runtime worker session when continuity is explicitly required. Fresh one-shot is the default; ask once if runtime, model, effort, work root, write scope, or resume handle is missing. Run hook-suppressed and unsandboxed in the shared worktree. Do NOT use for read-only second opinions (`fresh-consult`), deterministic reviews (`code-review`/`codex-review-yolo`), two-model plan convergence (`model-consensus`), ordered workflow orchestration (`stepwise`/`arch-epic`), or detached/background delegation."
metadata:
  short-description: "Claude/Codex worker with opt-in resume"
---

# Agent Delegate

Use this skill when the user wants a Claude or Codex subprocess to do a
concrete task with normal local agent capabilities. Fresh one-shot delegation
is the default: the child starts from disk and the delegation prompt, not from
the current chat history. When the caller explicitly requires continuity,
resume the same runtime's previously delegated worker session with a new,
bounded prompt.

The child may read files, edit files, run commands, verify its work, and use
installed skills when they fit the task.

This is a prompt-engineering skill. It ships no scripts, shims, hook
controllers, state machines, parsers, detached monitors, or install-time
automation.

## When to use

- "Have another agent implement this while we keep the main thread clean."
- "Delegate this refactor to Claude and report back."
- "Use Codex to fix the docs drift and run the checks."
- "Spin up a fresh agent to investigate and repair this failing test."
- "Have a child agent use `$skill-authoring` to patch this skill package."
- "Resume the same delegated Claude session and continue with higher effort."
- Another skill needs a foreground operational worker turn, not just an
  independent read.

## When not to use

- The user wants a clean read, second opinion, consistency check, completion
  audit, or readability/confusion check with no file edits. Use
  `$fresh-consult`.
- The user wants deterministic code-review coverage with lens fan-out,
  artifacts, and enforced Codex review policy. Use `$code-review`.
- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The user wants two models to iterate on a plan, architecture, design, or
  concept until they converge. Use `$model-consensus`.
- The work is an ordered subprocess workflow with manifests, critics, repair
  loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The task needs a detached/background worker, a separate git worktree, or
  merge machinery. This skill is foreground and shared-worktree only.
- There is no concrete task, work root, success bar, or write scope.
- The requested runtime CLI is not installed.
- The caller wants to resume "the latest" child without an explicit session id
  or prior run directory and ambiguity cannot be resolved safely.

## Non-Negotiables

- Resolve one delegated task, the success bar, the authoritative artifacts, the
  work root, the allowed write scope, and the delegation mode before launching
  a child process.
- Runtime, model, and effort must be known. If any are missing or ambiguous,
  ask one consolidated question before invoking.
- Delegation mode is one of `fresh-one-shot`, `fresh-resumable`, or `resume`.
  Default to `fresh-one-shot`. Use `fresh-resumable` or `resume` only when the
  caller explicitly requires same-session continuity.
- Resume mode requires an explicit session id or a previous run directory with
  `session_id.txt`. Refuse missing, empty, `UNRECOVERABLE`, cross-runtime, or
  "latest session" resume requests.
- Treat model text as intent, not a fuzzy alias. Preserve exact family and
  numeric version; never silently substitute a nearby model.
- Run the child hook-suppressed, unsandboxed, and in the shared worktree per
  this repo's convention. Prompt boundaries define the task; the sandbox does
  not.
- Fresh one-shot runs may be stateless. Fresh-resumable runs must capture a
  session handle. Resume runs must use the same runtime as the captured handle:
  Claude resumes through Claude, Codex resumes through Codex.
- Create one namespaced run directory under `/tmp/agent-delegate/` and keep
  `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, and
  `execution.json` there. For fresh-resumable and resume runs, also keep
  `session_id.txt`; for resume runs, also keep `resume_from.txt`.
- Brief the child like a capable colleague walking in cold: include the task,
  paths, success criteria, constraints, allowed write scope, and report
  contract. For resume prompts, state the new instruction or evidence and what
  remains unchanged from the original delegation.
- Tell the child to read local instructions such as `AGENTS.md` before editing
  covered files.
- Do not paste secrets into prompts. If a token is needed, source it into the
  child environment and tell the child which environment variable to read.
- Do not ask the child to commit, push, open PRs, rewrite history, stash, or
  revert unrelated work unless the delegated task explicitly requires that
  exact operation.
- Do not use hook-backed controllers as a continuation strategy. This skill is
  a foreground subprocess path, not an ordered workflow runner.
- If the child changed files or reports a blocker, inspect the repo state before
  presenting the result as fact.

## First Move

1. Read `references/model-and-invocation.md`.
2. Read `references/delegate-prompt-and-output.md`.
3. Identify the delegated task, success bar, work root, authoritative
   artifacts, allowed write scope, constraints, and requested
   runtime/model/effort from the user's words.
4. Identify the delegation mode. Use `fresh-one-shot` unless the caller
   explicitly asks for a resumable worker or to resume a previous delegate.
5. If runtime/model/effort, write scope, or a required resume handle is
   incomplete, ask one question that names exactly what is missing and what it
   controls.
6. Confirm the selected CLI exists with `command -v codex` or
   `command -v claude`.
7. Create the run directory and write the delegation prompt to `prompt.md`.
8. Invoke the child with the exact command shape from the invocation reference.

## Workflow

1. **Shape the delegation.** State the concrete work, allowed write scope,
   success bar, constraints, and authoritative files, commits, docs, or claims.
2. **Resolve execution.** Map the raw model phrase to
   `runtime=<claude|codex>`, `model=<runnable id>`, and `effort=<level>`.
   Announce the mapping before execution.
3. **Select continuity.** Use `fresh-one-shot` by default. Use
   `fresh-resumable` when the caller says this worker may need later resume.
   Use `resume` only with an explicit same-runtime session id or prior run
   directory.
4. **Run the child.** Use disabled hooks, no sandbox, a shared worktree, a
   namespaced run directory, and live event capture. Fresh one-shot runs start
   cold; fresh-resumable runs start a persistent child session; resume runs
   continue the captured session.
5. **Monitor patiently.** Normal delegated work often takes 5+ minutes; broad
   repo edits, verification, `xhigh`, or `max` can reasonably take 20-40
   minutes. Poll live `events.jsonl` and `stderr.log` every few minutes, not
   every few seconds.
6. **Consume the result.** Read `final.txt`, locate the status footer, and
   inspect `events.jsonl`/`stderr.log` when the final output is missing or
   malformed. For fresh-resumable and resume runs, preserve the session handle
   for the next explicit resume.
7. **Inspect local truth.** Check git status and any changed files named by the
   child before reporting upstream.
8. **Report upstream.** Lead with status, changed files, verification, blockers,
   confidence limits, and the run directory.

## Output Expectations

- A concise parent-facing report:
  - delegation mode
  - runtime/model/effort used
  - delegated task status
  - changed files or `none`
  - skills the child says it used or `none`
  - verification run or `not run: <reason>`
  - blockers or `none`
  - follow-up needed or `none`
  - run directory path
  - session id or `none` when not resumable
- If the child output is missing or malformed, say that plainly and preserve the
  run directory for debugging. Do not invent a status.
- If the child is wrong about a changed file, blocker, or verification result,
  say so explicitly and cite the evidence that contradicts it.

## Reference Map

- `references/model-and-invocation.md` - runtime/model/effort resolution and
  exact Claude/Codex command shapes
- `references/delegate-prompt-and-output.md` - delegated-worker prompt skeleton,
  status footer, report rules, and anti-patterns
