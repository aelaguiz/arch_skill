---
name: fresh-consult
description: "Run one or more clean, independent, read-only reviewers for strict pass/fail second opinions, completion checks, consistency audits, or readability checks. Fresh describes starting context, not a CLI: prefer a clean native child of the active host for same-host review, and use an external Claude, Codex, Cursor Agent, or Grok session when a concrete provider, exact-model/profile, lifecycle, isolation, or receipt benefit justifies it. Resume the exact reviewer for bounded same-line follow-ups; start a new clean child for a new independent gate. Not for implementation, two-participant convergence, Codex `-p yolo` review receipts, or ordered orchestration."
metadata:
  short-description: "Clean independent read-only review"
---

# Fresh Consult

Use this skill for a clean, independent, read-only opinion. `Fresh` means a new
reviewer with clean starting context; it does not inherently mean a Claude,
Codex, Cursor Agent, or Grok CLI subprocess.

Prefer a clean native child of the active host for ordinary same-host review.
Use the external lane when it buys a concrete provider, exact model/profile,
lifecycle, isolation, automation, or structured-receipt benefit that the native
child cannot supply. These are recognition examples, not a closed allowlist or
an approval gate.

The reviewer is a strict yes/no arbiter. If the user's ask is not fully
satisfied, the verdict is `fail` with specific reasons. The second and third
bounded follow-ups in the same consult line resume the exact reviewer by
default. A fourth turn rotates to a new clean reviewer unless the user asks to
continue. A new independent gate always starts a new clean reviewer rather
than resuming convenient history.

The parent dispatches native children or external sessions directly. Do not
add a universal runner, controller, state machine, or harness for this skill.

## When to use

- "Ask Claude for a cold read of this flow."
- "Have a clean Codex reviewer audit whether this plan phase is complete."
- "Run a fresh consult for consistency on these skills."
- "Run three parallel fresh consults on this plan."
- "Resume that reviewer and ask it to re-check the edited section."
- "Get a second opinion on whether this doc is linear and not confusing."
- "Have an independent reviewer check whether implementation matches the
  checklist."
- "Use Cursor Agent Composer 2.5 Fast for a cold read of this artifact."
- "Use Grok Build for an external fresh consult on this implementation claim."
- Another skill needs an independent read before deciding whether to proceed.

## When not to use

- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The child is expected to edit files or fix issues. Use a native implementation
  child for ordinary same-host work or `$agent-delegate` when an external
  editful session provides a concrete benefit.
- The user wants two participants to debate and converge. Use
  `$model-consensus`.
- The work is an ordered workflow with manifests, critics, repair loops, or
  persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The requested activity is a continuation of implementation, repair, debate,
  or another long-running owner role rather than a bounded read-only consult.
- There is no concrete artifact, claim, question, or target path to inspect.

## Non-Negotiables

- Apply `../_shared/agent-orchestration-policy.md`. Keep transport, starting
  context, continuation, capabilities, isolation, topology, and return evidence
  explicit at each dispatch without turning them into a serialized form.
- For a new Codex-native consult, set `fork_turns: "none"`. Do not omit it and
  assume the child is clean. A positive count is bounded recent context and
  `"all"` is a full parent fork; neither is the default for an independent
  review. Resume a bounded same-line follow-up through the exact child handle.
  Start a new child with `fork_turns: "none"` for a later independent gate.
- In Claude Code, use a clean named or custom subagent for a new same-host
  consult. An explicit conversation fork carries the parent conversation and
  is not a clean review. A skill with `context: fork` runs in an isolated clean
  subagent context; it is not shorthand for full conversation inheritance.
  Resume the exact named subagent for a bounded same-line follow-up. Use a
  background agent only when native lifecycle beyond the foreground turn is
  actually needed, and use a team only when direct peer communication is part
  of the requested method.
- Context is separate from permissions and filesystem isolation. Native
  children commonly share the workspace. Prefer an enforced read-only
  capability when the host offers one, always give an explicit no-edit/no-write
  contract, and have the parent inspect status or diff before accepting the
  result.
- Select external transport only for a concrete benefit. On a Codex host,
  another external Codex process adds an operating-system process and may
  contend on shared Codex SQLite/WAL state; that has caused host-wide stalls on
  some systems. This is a real cost, not a ban, approval gate, or fixed
  process-count limit.
- Honor explicit provider, model, profile, durable-session, or receipt requests.
  Do not claim a native child uses an exact model, permission set, worktree, or
  background lifecycle unless the current host exposes and confirms it. Use
  the external lane when a load-bearing requested capability is unavailable
  natively.
- Preserve exact external model resolution. Codex runs GPT/GBT/OpenAI model ids
  and Fugu profiles; Claude Code runs supported Claude models; Cursor Agent
  runs `composer-2.5-fast`; Grok runs `grok-build` or
  `grok-composer-2.5-fast`. An omitted external Codex model defaults to
  `gpt-5.6-sol`. Never silently substitute a nearby model or cross runtimes.
- Use bounded continuity by default: turn 1 is a new clean reviewer, turns 2
  and 3 resume the exact healthy same-line reviewer, and turn 4 starts clean
  unless the user explicitly asks to continue. Strictness is an acceptance bar,
  not a reason to discard useful same-line history.
- Never use latest-session selection. Resume only an exact native child handle
  or exact same-runtime external session captured for the same consult line.
- A new independent gate, cold check, or second verifier is a new clean child,
  even when an older reviewer handle is convenient.
- The parent owns fanout, the concurrency budget, evidence spot-checking, and
  synthesis. Every reviewer prompt prohibits child-created fanout and
  delegation/consult skills unless the parent explicitly assigns a bounded
  nested scope and budget.
- For external consults, preserve the existing namespaced chain directories,
  per-turn receipts, event streams, final output, execution metadata, and exact
  session handles described in the invocation reference.
- Brief the reviewer with the raw ask, work root, exact user-named artifacts or
  target paths, hard constraints, and report contract. Let it choose the
  evidence needed beyond those inputs.
- Do not ask the reviewer to fix what it finds. The verdict is `pass` or `fail`
  only; missing evidence or material uncertainty is `fail` with reasons.
- Do not paste secrets into prompts. If a token is needed, expose only the
  authorized environment variable and name it in the brief.

## First Move

1. Read `../_shared/agent-orchestration-policy.md`.
2. Read `references/consult-prompt-and-output.md`.
3. Identify the consult objective, work root, user-named artifacts or target
   paths, hard constraints, and whether this is a new independent gate or a
   bounded follow-up in an existing consult line.
4. Inspect the active host's native child surface. Choose a new clean native
   child for ordinary same-host review when it can satisfy the role. Record the
   explicit native context mechanism: Codex `fork_turns: "none"`, or a clean
   Claude named/custom subagent.
5. If the same consult line is continuing, resume its exact healthy child for
   turns 2 and 3. If independence is the point, start a new clean child. Never
   resume by "latest" or convenience.
6. If a provider, exact-model/profile, lifecycle, isolation, automation, or
   receipt benefit requires the external lane, read
   `references/model-and-invocation.md`, resolve the model and effort exactly,
   confirm the CLI, and use its receipt mechanics. Ask one consolidated
   question only when a load-bearing external execution value is missing.
7. Dispatch the reviewer with the prompt contract and explicit no-edit/no-child
   rules.

## Workflow

1. **Shape the consult.** State the user's question, strict acceptance bar,
   work root, exact user-named artifacts, and hard constraints without adding
   the parent's diagnosis.
2. **Choose continuity.** Start a new clean reviewer for a new line or
   independent gate. Resume the exact reviewer only for a bounded same-line
   follow-up. Rotate after the third turn unless the user asks to continue.
3. **Choose transport per reviewer.** Prefer the active host's clean native
   child for same-host work. Use an external session when its concrete benefit
   outweighs the additional process and integration cost. Explicit parallel
   consults may resolve independently; the parent owns every launch and result.
4. **Dispatch explicitly.** For Codex native, use `fork_turns: "none"` for new
   reviewers and exact-child follow-up for continuation. For Claude native, use
   a clean named/custom subagent and exact-subagent resume. For external, use
   the exact command and chain/turn receipt shape in the invocation reference.
5. **Protect read-only scope.** Use enforced read-only capability where
   available, include the no-edit/no-write prompt contract, and prohibit nested
   fanout unless explicitly budgeted.
6. **Consume the result.** Require the verdict footer and evidence actually
   read. Spot-check failure reasons and inspect parent-owned status/diff for
   unexpected writes before treating the result as fact.
7. **Report upstream.** Lead with the verdict, reasons, evidence, confidence,
   transport, starting context, continuation choice, and exact child/session
   handle. Include external chain/run paths only when the external lane was
   used. For multiple reviewers, report each result before synthesizing
   agreement or disagreement; do not majority-vote.

## Output Expectations

- A concise parent-facing report containing:
  - transport and active-host mechanism
  - starting context: clean prompt-and-disk context, or the existing exact
    reviewer context
  - continuation: new child, exact resume, or clean rotation
  - confirmed native model capability, or external runtime/model/effort
  - strict `pass` or `fail` verdict for each reviewer
  - failure reasons or `none`
  - evidence actually read
  - confidence and limits
  - exact native child handle or external session id when continuation matters
  - external chain, run, and group paths when applicable
  - parent read-only/status check
- If output is missing or malformed, say so and preserve any external receipt
  directory. Do not invent a verdict.
- If spot-checking contradicts a reviewer, say so explicitly and cite the
  parent-owned evidence.

## Reference Map

- `references/consult-prompt-and-output.md` - transport-neutral clean-review
  brief, strict verdict footer, parent report, and anti-patterns
- `references/model-and-invocation.md` - native host context/continuation
  semantics plus exact external model resolution, command shapes, chain
  receipts, and session resume
