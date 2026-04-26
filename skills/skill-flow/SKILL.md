---
name: skill-flow
description: "Design, repair, or audit an ordered flow of multiple agent skills so each skill has a distinct job, clear handoff artifact, and lean prompt contract. Use when building a new skill suite, reviewing a skill-to-skill workflow, or deciding how skill-authoring, prompt-authoring, doctrine-learn, and agent-linter should fit together. Not for writing one isolated skill, generic prompt repair, arch-epic execution plans, arch suite selection, or deterministic step execution."
metadata:
  short-description: "Design and audit multi-skill flows"
---

# Skill Flow

Use this skill when the work is the architecture of a multi-skill flow, not a single skill package.

A flow is ordered when the default handoff from one skill to the next is easy to explain.
It may still have audits, repair loops, optional branches, or specialist calls.
The test is whether a new reader can see the normal path without decoding a routing table.

## When to use

- The user wants to design a new group of skills that work together.
- An existing skill suite has blurry roles, unclear handoffs, or too much shared process copied across skills.
- The user wants a flow-level audit before or after individual skills are written.
- The user wants to decide where `skill-authoring`, `prompt-authoring`, `doctrine-learn`, and `agent-linter` fit in a skill authoring flow.
- The target skills may be pure Markdown packages, Doctrine-authored packages, or a mix of both.
- The user wants to audit a 30+ skill suite (or any suite too large for one-pass reasoning) for wasted-energy patterns: redundancy, repeated work, over-promotion, dead skills, or broken peer references. Use the DAG-grounded audit sub-mode in `references/workflow-and-modes.md`.
- The user says things like "audit every skill in this project", "audit the skills for flow X", or names a suite by slug list with audit intent.

## When not to use

- The job is one isolated skill package. Use `skill-authoring`.
- The job is one prompt contract or prompt repair. Use `prompt-authoring`.
- The job is learning which Doctrine construct to write. Use `doctrine-learn` when available.
- The job is a Doctrine authoring audit with a concrete package or flow already supplied. Use `agent-linter` when available.
- The job is decomposing one execution goal into ordered `arch-step` sub-plans. Use `arch-epic`.
- The job is choosing among the arch suite. Use `arch-skills-guide`.
- The job is deterministic step execution with worker sessions and critics. Use `stepwise`.
- The job is auditing one agent-definition file, such as one `SKILL.md`, `AGENTS.md`, or system prompt. Use `agent-definition-auditor`.

## Non-negotiables

- Start from 2-3 concrete user asks, one nearby anti-case, and the leverage claim for the whole flow.
- Each skill must have a distinct job and a concrete output, blocker, or question it leaves for the next skill.
- Keep judgment in skills and exact truth in typed, declared, or deterministic surfaces when the target stack provides them.
- Use examples, rationale, and recognition tests to teach judgment. Do not replace judgment with keyword routers, canned menus, or giant gates.
- Keep the shipped flow self-contained. Named peer skills are preferred levers when installed, not hidden dependencies.
- Do not encode Amir's private workflows, project-specific habits, or current repo accidents as universal flow law.
- Add scripts only for narrow utility work that natural-language execution handles poorly.

## First move

1. Classify the job as `design`, `audit`, or `repair`.
2. Read `references/flow-design-principles.md`.
3. Read `references/workflow-and-modes.md` for the selected mode.
4. Read `references/examples-and-anti-examples.md` only when the boundary or failure mode is still fuzzy.
5. Map the visible flow frontier: candidate skills, their jobs, their inputs, their handoff artifacts, and the nearest peer each one could be confused with.

## Workflow

1. Lock the flow's intent spine: the repeated user problem, the improved world state, and the canonical use cases.
2. List the candidate stages in plain English. For each stage, write one job sentence, one required input, and one output or blocker.
3. Test separability. Merge stages that only rename the same job. Split stages that own different artifacts, proof burdens, or reader moments.
4. Shape each handoff so the next skill can start without hidden state. If the user asked to audit a multi-skill suite by scope phrase, switch to the DAG-grounded audit sub-mode procedure in `references/workflow-and-modes.md` instead of the in-memory flow-map approach — the substrate-grounded path is required for suites too large for one-pass reasoning.
5. Define peer boundaries against the closest wrong choice.
   Pay special attention to `skill-authoring`, `prompt-authoring`, `agent-linter`, `doctrine-learn`, `arch-epic`, `arch-skills-guide`, and `stepwise`.
6. Use specialist skills only when their active question is present.
   Common active questions are individual skill quality, prompt contract quality, Doctrine construct choice, and Doctrine audit.
7. Validate the flow with one representative use case and one nearby anti-case. Check that a reader can see the next move without a routing table.
8. Return either a flow plan, a findings-first audit, or the smallest credible repair.

## Output expectations

- `design`: return a concise flow brief with the intent spine, proposed skills, handoff artifacts, peer boundaries, validation checks, and open questions.
- `audit`: return findings first.
  For each finding, name the affected skill or handoff, show exact evidence, explain why it hurts the flow, and give the smallest credible fix.
- `repair`: patch the smallest owning surface or return exact edits when writing is not appropriate.
- If the necessary skill surfaces are missing, report the coverage gap instead of inventing the flow.

## Reference map

- `references/flow-design-principles.md` - the core principles for separable jobs, handoffs, peer boundaries, and minimal complexity
- `references/workflow-and-modes.md` - how to run design, audit, and repair modes (including the DAG-grounded audit sub-mode) without turning the skill into a prompt runner
- `references/examples-and-anti-examples.md` - small examples and failure patterns that teach the judgment behind the principles
- `references/dag-substrate-format.md` - SSOT for the DAG substrate document the agent writes during a DAG-grounded audit (mermaid graph + edge table + unresolved-reference list, plus the closed node-kind and edge-kind enums)
- `references/parallel-walk-protocol.md` - per-sub-agent evidence schema, fanout sizing, scope resolution rules, and the code-block whitelist that prevents shell-variable false positives during reference extraction
- `references/waste-pattern-catalog.md` - 7 seed recognition tests for the audit reasoning step (over-promotion, duplicate canonical-stage criteria, lone-wolf, primitive vs hand-coded loop, broken edge, registry-stage mismatch, duplicate fan-out); explicitly NOT a rule engine
- `references/lessons-studio-worked-example.md` - evidence-anchored worked example calibrating over-promotion recognition; never named in the audit prompt itself
