---
name: delegated-implementation
description: "Keep the parent responsible for requirements, architecture, integration, and direct review while its subagents implement, test, and repair. Used by issue-to-pr and epic-to-prs for Astra or Fable coordinators, or when the user asks for this executive/worker split on accepted work. Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5. All skill authorship stays with the parent. Owns execution responsibilities, not a delivery lifecycle, agent launcher, read-only review, or conductor's full workflow."
metadata:
  short-description: "Parent judgment and review, worker implementation and tests"
---

# Delegated Implementation

Keep the parent's context available for requirements, architecture, scope,
integration, and first-hand review. Subagents carry the detailed coding and
verification work. The parent owns the result from the initial brief through
the final repair.

Use this execution contract when a calling workflow requires it or the user
asks for this division of work on an accepted plan or outcome. The caller
continues to own planning, external consultations, PR delivery, and completion.
Use `conductor` when the user wants its full plan-or-outcome workflow. A status
read or standalone review does not start implementation.

## Parent and worker responsibilities

The parent defines the smallest coherent assignments, resolves architectural
decisions and dependencies, and judges every deliverable against the accepted
scope. It reads source and artifacts directly, writes worker briefs from the
accepted plan, and records decisions in the existing worklog.

Workers investigate implementation details, reproduce failures, edit code and
tests, run the required checks, and repair accepted findings. This includes
integration fixes, CI failures, and corrections after external review. The
parent sends those jobs back to workers rather than writing the patch or
running the tests itself. Tight requirements describe the outcome and quality
bar; workers choose the implementation within those boundaries.

**Skill authorship stays with the parent.** The parent designs, writes, and
revises the skill package, including `SKILL.md`, references, bundled prompts,
runtime metadata, and any helper code the skill needs. Apply `$skill-authoring`
directly. Workers may run validation and report findings, but must not author
any part of the skill. In mixed work, keep skill authorship with the parent and
delegate the ordinary application code work.

## Worker selection and harness boundary

An Astra parent assigns implementation and verification to GPT-5.6 Sol
(`gpt-5.6-sol`) at `high`. A Fable parent assigns them to Opus 5, using the
user's effort choice or the harness's applicable default. These are deliberate
worker selections; the general Astra preference does not replace Sol here.
Honor explicit user model and effort overrides. For another parent model,
use the worker choice supplied by the user or calling workflow.

Read the installed `../_shared/agent-orchestration-policy.md` before dispatch
and apply `$prompt-authoring` to each populated brief. The active harness
provides the available agents, model identifiers, capabilities, and instructions
for spawning and continuing them. Use that live context for mechanics and
honor the selected worker model; this skill adds no launch procedure.

This contract describes the executive parent's role. An assigned Sol or Opus
worker implements its bounded brief and returns the result to that parent.
Handing it an issue does not make it a replacement executive or require another
layer of delegation. Keep skill authorship out of worker assignments.

## Brief and parallelize

Give each worker the accepted outcome, relevant plan and source paths, owned
scope, dependencies, architectural constraints, acceptance criteria, and
required verification under the repo's instructions. Include inherited review
coverage and the expected handoff when the caller has them. Distinguish binding
decisions from hypotheses the worker should investigate.

Choose coherent assignments large enough for implementation judgment and small
enough for the parent to review completely. Parallelize independent work when
dependencies, shared files, and verification resources allow it. Settle shared
design decisions before splitting the work, and sequence overlapping changes.
Keep enough capacity to review and integrate each return promptly.

Workers return the changed artifacts, checks actually run and their results,
unresolved findings, and any decision the parent needs to make. Keep detailed
logs in artifacts; bring their useful evidence and paths into parent context.

When the parent sends a Fable or Sol reader to review or audit delivered
work, write that brief the way `$chatgpt-web`'s consultation templates write
a PR review (family A): open with what we are building, hand over the plan,
the canonical requirements export, the user's words, and the PR whole, offer
the status as a belief, and say what to look for in the user's words. No
verdict token, answer cap, scope fence, or commit SHA. A native reader has
no `@GitHub`; give it the worktree path and the PR link instead. The parent
watches for the answer and reads all of it.

## Review, repair, and accept

Personally inspect every deliverable and every changed line of code, including
tests and later repair or integration changes. Read surrounding code as needed
to judge behavior, architecture, maintainability, and scope. Open other work
products and assess their substance. Worker summaries, passing tests, bots,
and external reviewers supply evidence; none replaces the parent's own review.

Batch concrete findings into a repair brief for the responsible worker, with
the affected behavior, evidence, and acceptance criteria. Workers repair code
and rerun affected checks; the parent reviews the resulting changes and check
evidence. Skill findings are repaired by the parent under the authorship
exception. Continue until the accepted work is complete and required checks
pass, using the caller's existing escalation and review cadence.

Record acceptance and remaining work in the existing plan or worklog. The
calling workflow determines when the result is merge-ready or complete. This
contract adds no mandatory cynical reviews, independent test reruns, or
separate approval gates.
