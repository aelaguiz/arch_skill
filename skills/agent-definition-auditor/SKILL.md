---
name: agent-definition-auditor
description: "Audit and score an agent-definition markdown such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, `.cursorrules`, or a system prompt using a cold-reader rubric for clarity, consistency, context independence, and operating-model fit. Use when the user asks to review, score, critique, or audit an agent instruction file. Not for evaluating agent outputs, code quality, or rewriting the file itself."
metadata:
  short-description: "Cold-reader scoring and findings for agent-definition files"
---

# Agent Definition Auditor

Use this skill when the job is auditing one agent-definition file, not rewriting it.

## When to use

- The user wants to audit or score an `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, `.cursorrules`, system prompt, or other agent-definition markdown.
- The user wants a cold-reader review of agent-contract quality.
- The user wants a deploy / revise / do-not-ship judgment with concrete findings and fastest improvements.
- The user wants a reusable rubric-based critique of an agent instruction file rather than an output benchmark.

## When not to use

- The user wants to write, rewrite, or refactor the agent file rather than score it.
- The user wants to evaluate agent outputs, benchmark runtime behavior, or compare model responses rather than audit the instruction artifact itself.
- The job is code review, product-doc review, or general technical writing feedback unrelated to an agent-definition file.
- No target artifact or pasted instruction text is available.

## Non-negotiables

- Default to a single-artifact, read-only cold read.
- Judge the document as an operational contract, not as domain strategy or business policy.
- Distinguish precise layered contracts from phantom context.
- Apply the scoring model, hard caps, and report shape from the reference prompt literally.
- Cite line numbers when available; otherwise cite exact headings or short anchors.
- Do not widen to repo-wide inspection unless the user explicitly asks for multi-file or repo-context evaluation.
- Do not rewrite the file unless the user explicitly asks for fixes after the audit.

## First move

1. Resolve one target artifact path or pasted instruction text.
2. Read `references/agent-definition-judge-prompt.md`.
3. Read the full target artifact once before scoring.
4. If the user also wants revisions, finish the audit first unless they explicitly want authoring instead of judging.

## Workflow

1. Confirm the artifact class and whether the input is a full file or an excerpt.
2. Stay on the single document by default.
3. Inventory the artifact's hard rules:
   - mission and scope
   - output rules
   - tool rules
   - approval and escalation rules
   - failure handling
   - external dependencies
4. Apply the reference prompt's scoring model and hard caps.
5. Return the exact report sections required by the reference prompt.
6. If the user then wants fixes, use the audit as the basis for the follow-up instead of recomputing the diagnosis from scratch.

## Output expectations

- Return the exact top-level sections from the reference prompt.
- Include overall and uncapped score, verdict, confidence, cap logic, findings, strengths, fastest score gains, and limits.
- Keep findings ordered by severity and tied to concrete evidence from the artifact.

## Reference map

- `references/agent-definition-judge-prompt.md` - full judging prompt, scoring model, hard caps, report contract, and examples
