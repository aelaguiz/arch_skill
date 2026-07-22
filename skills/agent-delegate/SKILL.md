---
name: agent-delegate
description: "Run editful Claude, Codex, Cursor Agent, Grok, or Kimi workers as explicit external processes or resumable sessions with exact model/profile resolution and structured receipts. Use when external transport provides a concrete benefit, such as a different provider, a load-bearing exact model/profile, durable exact-session continuation, process isolation, automation, or captured event/final-output artifacts; these are examples, not a closed gate. Route ordinary same-host work directly to the active host's native children when they can satisfy the role. Use exact handles to resume the same external worker. Not for read-only reviews (`fresh-consult`), Codex `-p yolo` reviews, two-model convergence, ordered orchestration, or detached/background delegation."
metadata:
  short-description: "External editful worker sessions and receipts"
---

# Agent Delegate

Use this skill as the explicit external editful worker/session adapter. It runs
Claude Fable/Opus, Codex GPT/GBT models or Fugu profiles, Cursor Composer,
Grok, or Kimi K3 as a separate process, captures a durable receipt, and can resume the
exact external session. It does not own the caller's decomposition, role
choice, context choice, review policy, or final integration.

For ordinary same-host work, use the active host's native child directly when
that child can satisfy the role. Choose this external lane when the provider,
model/profile, lifecycle, process isolation, automation surface, or receipt
provides a concrete benefit worth the extra process and integration cost.
Those are recognition examples, not a finite allowlist or an approval gate.

Fresh-resumable is the external default: the worker starts clean from disk and
the delegation brief, not from the parent chat, and the parent captures an
exact session handle. A resume continues only that worker with a bounded delta.

The child may read files, edit files, run commands, verify its work, and use
installed skills when they fit the task.

This is a prompt-engineering skill. It ships no scripts, shims, hook
controllers, state machines, parsers, detached monitors, or install-time
automation.

## When to use

- "Use an external worker with a durable receipt to implement this."
- "Run two cross-provider workers on these independent fixes."
- "From this Codex host, delegate the refactor to Claude and report back."
- "From this Claude host, use Codex to fix the docs drift and run the checks."
- "Use Cursor Agent Composer to implement this slice and report back."
- "Use Grok Build to investigate and patch this workflow."
- "Use Kimi K3 max to implement this slice and keep its exact session handle."
- "Use the exact Fugu Ultra profile and preserve a resumable receipt."
- "Have an external Claude session use `$skill-authoring` to patch this skill
  package and preserve its exact handle."
- "Resume the same delegated Claude session and continue with higher effort."
- Another skill has already selected an external foreground worker because a
  concrete provider, model, lifecycle, isolation, automation, or receipt
  benefit matters.

## When not to use

- The task is ordinary same-host implementation, investigation, or repair and
  the active host's native child can satisfy the role. Dispatch that child
  directly under `../_shared/agent-orchestration-policy.md` instead of routing
  native work through this adapter.
- The user wants a clean read, second opinion, consistency check, completion
  audit, or readability/confusion check with no file edits. Use
  `$fresh-consult`.
- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The user wants two models to iterate on a plan, architecture, design, or
  concept until they converge. Use `$model-consensus`.
- The work is an ordered subprocess workflow with manifests, critics, repair
  loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The task needs a detached/background worker, a separate git worktree, or
  merge machinery. This skill is foreground and shared-worktree only.
- There is no concrete task, work root, success bar, or write scope for the
  child being launched.
- The requested runtime CLI is not installed.
- The caller wants to resume "the latest" child without an explicit session id
  or prior run directory and ambiguity cannot be resolved safely.

## Non-Negotiables

- Apply `../_shared/agent-orchestration-policy.md` before selecting this lane.
  Apply `$prompt-authoring` to the actual populated worker brief before launch
  and after a material reframe. Connect external transport to a concrete
  benefit, but do not turn that explanation into a permission checklist or ask
  for approval merely because the process is external.
- On a Codex host, account for the real cost of launching another Codex
  process: separate processes can contend on shared Codex SQLite/WAL state and
  have caused host-wide stalls. This is a tradeoff, not a ban, approval gate,
  or fixed process-count limit.
- Derive each delegated task and success bar from the user's request, a
  canonical plan or issue, local doctrine, or verified acceptance evidence.
  Resolve the work root, allowed write scope, constraints, delegation mode,
  and exact user-named inputs before launch. Keep the parent's diagnosis,
  preferred implementation, and selected evidence path advisory unless the
  authoritative source actually chose them.
- Runtime must be known. Effort must also be known except that GPT-5.6 Sol
  defaults an omitted effort to `ultra` and Kimi K3 defaults it to `max`.
  Model or profile must be known except that a Codex lane with no named model
  defaults to `gpt-5.6-sol` and a Kimi lane defaults to `kimi-code/k3`. Codex runs
  GPT/GBT/OpenAI model ids and Fugu profiles, Claude Code runs supported
  Claude models, Cursor Agent runs `composer-2.5-fast`, Grok CLI naturally
  resolves to `grok-4.5`, and Kimi Code runs `kimi-code/k3`. Explicit legacy
  Grok ids remain exact and discovery-gated. If any other required value is
  missing or ambiguous, ask one consolidated question before invoking.
- Never run GPT/GBT model ids, Fugu profiles, or Claude models through Cursor
  Agent, Grok, or Kimi. Do not pass Grok or Kimi model ids through another
  runtime.
- Delegation mode is one of `fresh-one-shot`, `fresh-resumable`, or `resume`.
  Default to `fresh-resumable`. Use `fresh-one-shot` only when the caller
  explicitly asks for a stateless, ephemeral, no-resume, or throwaway worker.
  Kimi always persists sessions, so it cannot satisfy a load-bearing
  stateless/no-persist requirement even when the receipt would be ignored.
- Resume mode requires an explicit session id or a previous run directory with
  `session_id.txt`. Refuse missing, empty, `UNRECOVERABLE`, cross-runtime, or
  "latest session" resume requests.
- Treat model text as intent, not a fuzzy alias. Preserve exact family and
  numeric version; never silently substitute a nearby model.
- Run the child hook-suppressed where the runtime supports it, unsandboxed, and
  in the shared worktree per this repo's convention. Prompt boundaries define
  the task; the sandbox does not. A clean external session is a context choice,
  not filesystem, permission, or worktree isolation.
- Fresh one-shot runs may be stateless. Fresh-resumable runs must capture a
  session handle. Resume runs must use the same runtime as the captured handle:
  Claude resumes through Claude, Codex resumes through Codex, Cursor Agent
  resumes through Cursor Agent, Grok resumes through Grok, and Kimi resumes
  through Kimi with the exact captured id.
- For a single delegation, create one namespaced run directory under
  `/tmp/agent-delegate/` and keep `prompt.md`, `final.txt`, `events.jsonl`,
  `stderr.log`, and `execution.json` there. For fresh-resumable and resume
  runs, also keep `session_id.txt`; for resume runs, also keep
  `resume_from.txt`.
- For explicit parallel delegations, create one group directory under
  `/tmp/agent-delegate/` and one ordinary child run directory per worker. Do
  not add a controller, detached monitor, separate worktree, or merge layer.
  The parent owns the fanout, concurrency budget, scope separation, and final
  integration.
- Brief the child like a capable colleague walking in cold: include the
  authoritative outcome and success criteria, source evidence, work root,
  allowed write scope, real constraints, exact user-named inputs, the
  parent-owned topology and nested-fanout boundary, and report contract. Let
  the child choose the evidence and implementation path inside that contract
  and report when the brief's premise conflicts with repo truth. For resume
  prompts, state the new instruction or evidence and what remains unchanged
  from the original delegation.
- Tell the child to read local instructions such as `AGENTS.md` before editing
  covered files.
- In parallel groups, tell each child it is not alone in the codebase, must not
  revert unfamiliar changes, should make the smallest task-relevant edits, and
  should report actual conflicts if they happen.
- Tell every worker not to create children or invoke delegation/consult skills.
  Nested fanout is allowed only when the parent explicitly assigns a bounded
  nested scope and concurrency budget in that worker's prompt.
- Do not paste secrets into prompts. If a token is needed, source it into the
  child environment and tell the child which environment variable to read.
- Do not ask the child to commit, push, open PRs, rewrite history, stash, or
  revert unrelated work unless the delegated task explicitly requires that
  exact operation.
- Do not use external continuation controllers as a strategy. This skill is
  a foreground subprocess path, not an ordered workflow runner.
- If the child changed files or reports a blocker, inspect the repo state before
  presenting the result as fact. If the child claims a work-product artifact —
  a screenshot, report, generated file, export — open the artifact itself and
  confirm its content matches the claim before relaying it; existence is not
  evidence, and a screenshot that exists but shows a blank page, error, or
  wrong screen is a failed claim, not a delivered result.

## First Move

1. Read `../_shared/agent-orchestration-policy.md`.
2. Read `references/model-and-invocation.md`.
3. Read `references/delegate-prompt-and-output.md`.
4. Inspect the active host's native-child surface. If an ordinary same-host
   native child can satisfy the role, dispatch it directly instead of using
   this skill. Make that native context choice explicit: Codex uses
   `fork_turns: "none"`, a positive bounded count, or `"all"`; Claude uses a
   clean named/custom subagent, an explicit full-conversation fork, or a
   `context: fork` isolated clean skill context as appropriate. Resume the
   exact subagent only when the same role continues; use a background agent
   only when work must outlive the foreground turn, and a team only when direct
   peer communication genuinely helps.
   Context inheritance remains separate from permissions and worktree sharing.
   Otherwise state the concrete benefit of the external lane.
5. Identify the delegated task or parallel delegated tasks, success bar, work
   root, exact user-named inputs, allowed write scope, constraints, and
   requested runtime/model/effort from the user's words. Apply
   `$prompt-authoring` to the populated brief: preserve source-backed authority,
   mark useful parent conjecture as advisory, and leave the worker free to
   reject it from repo evidence.
6. Identify the delegation mode. Use `fresh-resumable` unless the caller
   explicitly asks for a stateless one-shot worker or to resume a previous
   delegate.
7. When an external Codex lane omits its model, apply `gpt-5.6-sol`; when that
   Sol lane also omits effort, apply the preference default `ultra`. For Kimi,
   apply `kimi-code/k3` and the model-default `max` effort when omitted. If
   another required execution value, write scope, or resume handle is
   incomplete, ask one question that names exactly what is missing and what it
   controls.
8. Confirm the selected CLI exists with `command -v codex`, `command -v
   claude`, `command -v agent`, `command -v grok`, or `command -v kimi`.
9. Create the run directory or group directory and write each delegation prompt
   to its own `prompt.md`.
10. Invoke each worker with the exact command shape from the invocation reference.

## Workflow

1. **Confirm the external dispatch.** Keep role and decomposition with the
   caller. Record why this worker is external, whether it is a new clean
   session or an exact resume, its capabilities, its write scope, and the
   parent-owned return contract.
2. **Shape the delegation.** State the source-backed outcome, allowed write
   scope, observable success bar, real constraints, verified evidence, and
   exact user-named inputs such as paths, failing commands, repro steps, or
   docs. Do not assume parent-chat inheritance or promote a parent diagnosis,
   preferred fix, or selected file list into task authority.
3. **Resolve execution.** Map the raw model phrase to
   `runtime=<claude|codex|agent|grok|kimi>`, `model=<runnable id>`, and
   `effort=<level-or-encoded-in-model>`.
   Announce the mapping before execution.
4. **Select single or parallel.** Use one worker by default. Use a parallel group
   only when the user asks for parallel workers or gives multiple delegated
   tasks and the parent can own every scope and result.
5. **Select continuity.** Use `fresh-resumable` by default. Use
   `fresh-one-shot` only for explicit stateless, ephemeral, no-resume, or
   throwaway delegation. Use `resume` only with an explicit same-runtime
   session id or prior run directory. Keep resume on the single-worker path.
6. **Run the worker or workers.** Use disabled hooks, no sandbox, a shared
   worktree, namespaced run directories, and live event capture. Fresh one-shot
   runs start cold; fresh-resumable runs start persistent child sessions; resume
   runs continue the captured session.
7. **Monitor patiently.** Normal delegated work often takes 5+ minutes; broad
   repo edits, verification, `xhigh`, or `max` can reasonably take 20-40
   minutes. Poll live `events.jsonl` and `stderr.log` every few minutes, not
   every few seconds.
8. **Consume the result.** Read `final.txt`, locate the status footer, and
   inspect `events.jsonl`/`stderr.log` when the final output is missing or
   malformed. For fresh-resumable and resume runs, preserve the session handle
   for the next explicit resume.
9. **Inspect local truth.** Check git status and any changed files named by the
   child or children before reporting upstream. Open any claimed work-product
   artifact (screenshot, report, generated file) and verify its content shows
   the claimed result, not merely that the file exists.
10. **Report upstream.** For one worker, lead with status, changed files,
   verification, blockers, confidence limits, and the run directory. For a
   parallel group, report one compact child-by-child table plus the parent repo
   state check and combined outcome.

## Output Expectations

- A concise parent-facing report:
  - transport: `external`
  - concrete external benefit
  - starting context: clean prompt-and-disk context or the existing exact
    session context
  - continuation: new one-shot, new resumable session, or exact-session resume
  - delegation mode
  - runtime/model/effort used
  - delegated task status, or one status per child for parallel groups
  - changed files or `none`
  - skills the child says it used or `none`
  - verification run or `not run: <reason>`
  - blockers or `none`
  - follow-up needed or `none`
  - run directory path, or group directory plus child run directories
  - session id, or `none` only for explicit `fresh-one-shot` or failed capture
- If the child output is missing or malformed, say that plainly and preserve the
  run directory for debugging. Do not invent a status.
- If the child is wrong about a changed file, blocker, or verification result,
  say so explicitly and cite the evidence that contradicts it.

## Reference Map

- `references/model-and-invocation.md` - exact external runtime/model/effort
  resolution, command shapes, session capture/resume, and receipts
- `references/delegate-prompt-and-output.md` - external-worker brief, status
  footer, parent integration report, and anti-patterns
