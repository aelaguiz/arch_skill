---
name: "agent-delegate"
description: "Delegate one or more concrete tasks to Claude/Codex subprocesses with full local agent capabilities. Use when the user wants another agent, multiple agents, or parallel agents to implement, edit, investigate-and-fix, run commands, use installed skills, or resume one previously delegated same-runtime worker session when continuity is explicitly required. Fresh one-shot is the default; ask once if runtime, model, effort, work root, write scope, task, or resume handle is missing. Run hook-suppressed and unsandboxed in the shared worktree. Do NOT use for read-only second opinions (`fresh-consult`), deterministic reviews (`code-review`/`codex-review-yolo`), two-model plan convergence (`model-consensus`), ordered workflow orchestration (`stepwise`/`arch-epic`), or detached/background delegation."
version: "1.0.0"
license: "MIT"
---

# Agent Delegate

Use this skill when the user wants one or more Claude or Codex subprocesses to do concrete tasks with normal local agent capabilities. Fresh one-shot delegation is the default: each child starts from disk and the delegation prompt, not from the current chat history. When the caller explicitly requires continuity for one worker, resume the same runtime's previously delegated worker session with a new, bounded prompt.

## When to use

The user wants another agent, multiple agents, or parallel agents to implement, edit, investigate-and-fix, run commands, or use installed skills.
The user wants to delegate a task to a fresh Claude or Codex worker and report back.
The user wants to resume a previously delegated same-runtime worker session when continuity is explicitly required.
Another skill needs a foreground operational worker turn, not just an independent read.

## When not to use

The user wants a clean read, second opinion, consistency check, completion audit, or readability/confusion check with no file edits. Use `$fresh-consult`.
The user wants deterministic code-review coverage with lens fan-out, artifacts, and enforced Codex review policy. Use `$code-review`.
The user specifically asks for the existing Codex `-p yolo` review pattern. Use `$codex-review-yolo`.
The user wants two models to iterate on a plan, architecture, design, or concept until they converge. Use `$model-consensus`.
The work is an ordered subprocess workflow with manifests, critics, repair loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
The task needs a detached/background worker, a separate git worktree, or merge machinery. This skill is foreground and shared-worktree only.
There is no concrete task, work root, success bar, or write scope for the child being launched.
The requested runtime CLI is not installed.
The caller wants to resume `the latest` child without an explicit session id or prior run directory and ambiguity cannot be resolved safely.

## Non-negotiables

Resolve each delegated task, success bar, authoritative artifacts, work root, allowed write scope, and delegation mode before launching child processes.
Runtime, model, and effort must be known. If any are missing or ambiguous, ask one consolidated question before invoking.
Delegation mode is one of `fresh-one-shot`, `fresh-resumable`, or `resume`. Default to `fresh-one-shot`. Use `fresh-resumable` or `resume` only when the caller explicitly requires same-session continuity.
Resume mode requires an explicit session id or a previous run directory with `session_id.txt`. Refuse missing, empty, `UNRECOVERABLE`, cross-runtime, or `latest session` resume requests.
Treat model text as intent, not a fuzzy alias. Preserve exact family and numeric version; never silently substitute a nearby model.
Run the child hook-suppressed, unsandboxed, and in the shared worktree per this repo's convention. Prompt boundaries define the task; the sandbox does not.
Fresh one-shot runs may be stateless. Fresh-resumable runs must capture a session handle. Resume runs must use the same runtime as the captured handle: Claude resumes through Claude, Codex resumes through Codex.
For a single delegation, create one namespaced run directory under `/tmp/agent-delegate/` and keep `prompt.md`, `final.txt`, `events.jsonl`, `stderr.log`, and `execution.json` there. For fresh-resumable and resume runs, also keep `session_id.txt`; for resume runs, also keep `resume_from.txt`.
For explicit parallel delegations, create one group directory under `/tmp/agent-delegate/` and one ordinary child run directory per worker. Do not add a controller, detached monitor, separate worktree, or merge layer.
Brief the child like a capable colleague walking in cold: include the task, paths, success criteria, constraints, allowed write scope, and report contract. For resume prompts, state the new instruction or evidence and what remains unchanged from the original delegation.
Tell the child to read local instructions such as `AGENTS.md` before editing covered files.
In parallel groups, tell each child it is not alone in the codebase, must not revert unfamiliar changes, should make the smallest task-relevant edits, and should report actual conflicts if they happen.
Do not paste secrets into prompts. If a token is needed, source it into the child environment and tell the child which environment variable to read.
Do not ask the child to commit, push, open PRs, rewrite history, stash, or revert unrelated work unless the delegated task explicitly requires that exact operation.
Do not use hook-backed controllers as a continuation strategy. This skill is a foreground subprocess path, not an ordered workflow runner.
If the child changed files or reports a blocker, inspect the repo state before presenting the result as fact.

## First move

Read `references/model-and-invocation.md`.
Read `references/delegate-invocation.md`.
Read `references/delegate-prompt-and-output.md`.
Identify the delegated task or parallel delegated tasks, success bar, work root, authoritative artifacts, allowed write scope, constraints, and requested runtime/model/effort from the user's words.
Identify the delegation mode. Use `fresh-one-shot` unless the caller explicitly asks for a resumable worker or to resume a previous delegate.
If runtime/model/effort, write scope, or a required resume handle is incomplete, ask one question that names exactly what is missing and what it controls.
Confirm the selected CLI exists with `command -v codex` or `command -v claude`.
Create the run directory or group directory and write each delegation prompt to its own `prompt.md`.
Invoke each child with the exact command shape from the invocation reference.

## Workflow

Shape the delegation: state the concrete work, allowed write scope, success bar, constraints, and authoritative files, commits, docs, or claims.
Resolve execution: map the raw model phrase to `runtime=<claude|codex>`, `model=<runnable id>`, and `effort=<level>`. Announce the mapping before execution.
Select single or parallel: use one child by default. Use a parallel group only when the user asks for parallel workers or gives multiple delegated tasks.
Select continuity: use `fresh-one-shot` by default. Use `fresh-resumable` when the caller says this worker may need later resume. Use `resume` only with an explicit same-runtime session id or prior run directory. Keep resume on the single-worker path.
Run the child or children: use disabled hooks, no sandbox, a shared worktree, namespaced run directories, and live event capture. Fresh one-shot runs start cold; fresh-resumable runs start persistent child sessions; resume runs continue the captured session.
Monitor patiently: normal delegated work often takes 5+ minutes; broad repo edits, verification, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live `events.jsonl` and `stderr.log` every few minutes, not every few seconds.
Consume the result: read `final.txt`, locate the status footer, and inspect `events.jsonl`/`stderr.log` when the final output is missing or malformed. For fresh-resumable and resume runs, preserve the session handle for the next explicit resume.
Inspect local truth: check git status and any changed files named by the child or children before reporting upstream.
Report upstream: for one child, lead with status, changed files, verification, blockers, confidence limits, and the run directory. For a parallel group, report one compact child-by-child table plus the parent repo state check and combined outcome.

## Output expectations

A concise parent-facing report:

- delegation mode
- runtime/model/effort used
- delegated task status, or one status per child for parallel groups
- changed files or `none`
- skills the child says it used or `none`
- verification run or `not run: <reason>`
- blockers or `none`
- follow-up needed or `none`
- run directory path, or group directory plus child run directories
- session id or `none` when not resumable

If the child output is missing or malformed, say that plainly and preserve the run directory for debugging. Do not invent a status.
If the child is wrong about a changed file, blocker, or verification result, say so explicitly and cite the evidence that contradicts it.

## Reference map

`references/model-and-invocation.md` - shared runtime/model/effort resolution and fail-loud substitution rules
`references/delegate-invocation.md` - agent-delegate specific invocation: delegation modes, run directories, command shapes, parallel groups, monitoring, and failure behavior
`references/delegate-prompt-and-output.md` - delegated-worker prompt skeleton, status footer, report rules, and anti-patterns
