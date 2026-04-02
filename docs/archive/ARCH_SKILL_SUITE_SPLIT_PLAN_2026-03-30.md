---
title: "arch_skill skill suite split — architecture plan"
date: 2026-03-30
status: draft
owners: [Amir]
reviewers: []
doc_type: phased_refactor
related:
  - README.md
  - docs/arch_skill_usage_guide.md
  - prompts/
  - skills/
---

# TL;DR

- **Outcome:** this repo ships a focused skill suite that covers the real arch workflows without depending on saved prompts at runtime.
- **Problem:** the current `arch-skill` / `arch-flow` pair is a thin router; most of the real workflow still lives in prompt files, so the skill surface loses capability as prompt support disappears.
- **Approach:** split by actual workflow families, move the durable runtime contract into self-contained skills, and keep prompts only as legacy/reference artifacts.
- **Plan:** author the new skills, wire installs/docs to the new suite, and validate trigger quality plus prompt-coverage parity.
- **Non-negotiables:**
  - no new catch-all umbrella skill
  - each shipped skill is self-contained at runtime
  - full arch implementation stays local by default; do not delegate implementation
  - external multi-model review remains explicit-review-only
  - prompts may stay in the repo, but skills must not require them

## 1) Job To Be Done

The repeated user problem is not "install a prompt pack." It is:

> "Given a serious change, small feature, bug, or investigation, load the right workflow automatically, keep the right document as SSOT, and execute that flow end-to-end without me reconstructing the doctrine from saved prompts."

The leverage claim is:

- one skill per real workflow family improves trigger quality
- each skill can carry the exact contract, invariants, and output expectations that the prompt version used to encode
- the suite remains usable when Codex saved prompts go away

## 2) Canonical User Asks

These are the asks the new suite should handle directly:

- "Create a real arch plan, do the research/deep dive/external research, then give me the phased plan."
- "Give me the mini-plan version of arch for this smaller task."
- "This is a small feature; use the little arch flow and ship it."
- "Analyze this bug from Sentry/logs, fix it, and verify it."
- "We know the goal, not the path; run the goal loop."
- "Bootstrap an investigation doc and iterate with brutal tests."

Near-lookalike asks that should *not* load the same skill:

- a tiny 1-3 phase feature should not trigger the full arch flow
- a bug report should not trigger architecture planning
- an open-ended optimization effort should not trigger the bug flow

## 3) Proposed Skill Taxonomy

| Skill | Owns | Use when | Explicitly not for |
| --- | --- | --- | --- |
| `arch-plan` | Full arch workflow | medium/large multi-phase work, deep dives, external research, phase plans, implementation audits | tiny features, one-pass mini plans, bug triage, open-ended loops |
| `arch-mini-plan` | One-pass compressed arch planning | a "mini plan" ask that still needs canonical arch blocks | full arch execution, lilarch, bug fixes |
| `lilarch` | Small-feature 1-3 phase flow | compact feature/improvement work with a short clarification gate | broad migrations, heavy investigation, open-ended planning |
| `bugs-flow` | Analyze/fix/review bug workflow | symptoms, regressions, Sentry issues, logs, crash investigations | planned feature work or architecture planning |
| `goal-loop` | Goal-seeking controller + append-only worklog loop | open-ended optimization/investigation where the path is unknown | fixed-scope implementation plans |
| `north-star-investigation` | Math-first investigation loop | optimization or root-cause hunts that need ranked hypotheses and brutal tests | ordinary bug fixes or planned delivery |
| `arch-flow` | Read-only next-step router | "what's next?", "continue", checklist/flow-status asks for arch docs | doing the work itself |
| `arch-skills-guide` | Suite explainer and selector | "which arch skill should I use?", suite tours, subskill comparisons | doing the workflow itself |

Notes:

- `arch-plan` is the "full arch skill" the user asked for.
- `arch-mini-plan` stays separate from `lilarch` because they solve different asks:
  - `arch-mini-plan` writes the canonical arch blocks in one pass.
  - `lilarch` is the compact start/plan/finish feature flow with its own doc contract.
- `arch-skill` is retained only as a legacy reference artifact and is intentionally removed from the default install surface.

## 4) Prompt Coverage Plan

The new skills should cover the workflows that previously required these prompt families:

| Legacy prompts | New skill |
| --- | --- |
| `arch-new`, `arch-reformat`, `arch-research`, `arch-deep-dive`, `arch-external-research-agent`, `arch-phase-plan`, `arch-implement`, `arch-audit-implementation`, plus plan-shaping helpers | `arch-plan` |
| `arch-mini-plan-agent` | `arch-mini-plan` |
| `lilarch-start`, `lilarch-plan`, `lilarch-finish` | `lilarch` |
| `bugs-analyze`, `bugs-fix`, `bugs-review` | `bugs-flow` |
| `goal-loop-new`, `goal-loop-flow`, `goal-loop-iterate`, `goal-loop-context-load` | `goal-loop` |
| `north-star-investigation-bootstrap`, `north-star-investigation-loop` | `north-star-investigation` |
| `arch-flow` | `arch-flow` |

Intentionally left out of the first split:

- one-shot utility prompts that are better treated as task-local behaviors than as standalone long-lived skills
- review helpers that depend on explicit code-review consent

## 5) Cross-Skill Invariants

These rules should be encoded consistently where relevant:

- single-document SSOT per workflow
- code is ground truth
- strict question policy: only ask what repo/docs/tools cannot answer
- no runtime fallbacks unless explicitly approved and timeboxed in the governing doc
- planning phases are docs-only
- implementation remains local by default
- external cross-model review only happens when the user explicitly asks for review

## 6) Packaging Decisions

- Each skill gets a lean `SKILL.md` plus only the references it truly needs.
- The runtime contract lives in the skill package itself; prompts are not required at runtime.
- The install surface changes from:
  - `arch-skill`, `arch-flow`
  to:
  - `arch-plan`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`
- Prompt files remain in the repo for legacy use, migration review, and non-Codex surfaces, but the skill suite becomes the primary surface.

## 7) Validation Plan

Package integrity:

- every new skill has valid frontmatter
- references exist and are linked from the owning `SKILL.md`
- install/verify targets reference the right skill names

Trigger quality:

- "do the full arch flow" should trigger `arch-plan`
- "give me a mini plan" should trigger `arch-mini-plan`
- "small feature, use lilarch" should trigger `lilarch`
- "analyze this Sentry bug" should trigger `bugs-flow`
- "we have a goal but not the path" should trigger `goal-loop`
- "what's next on this plan doc?" should trigger `arch-flow`
- "which arch skill should I use?" should trigger `arch-skills-guide`

Execution quality:

- each skill must teach the workflow directly instead of routing back to prompts
- full arch implementation must stay local by default
- bug review and any external cross-model review stay opt-in

## 8) Review Focus

The highest-value review questions for this split are:

- are the skill boundaries right, or is any workflow still too broad?
- does `arch-plan` feel like the real full-arch capability, not a prompt index in disguise?
- should any more prompt families become first-class skills now, or are the remaining prompt-only items correctly treated as utilities?
