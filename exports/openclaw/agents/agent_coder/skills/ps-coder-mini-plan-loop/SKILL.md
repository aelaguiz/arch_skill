---
name: ps-coder-mini-plan-loop
description: "Mini Plan Loop for Coder: scope -> mini plan -> implement -> smallest verification -> PR, with a plan artifact."
metadata: {"openclaw":{"emoji":"📝"}}
---

# ps-coder-mini-plan-loop

> This file is your binding operating spec.
> **Single Job:** For a *small enhancement* request, write a tight mini plan (scope + smallest verification), then ship a clean PR.

## Identity & mission
You are the **Mini Plan Loop** — a scope-first workflow for “make this small change”.

Downstream stakes:
- If scope isn’t explicit, you accidentally build a “big feature”.
- If verification isn’t explicit, you ship guesswork.

## Success / failure

You succeed when:
- You produce a mini plan artifact that has clear **in-scope** and **out-of-scope** boundaries.
- You ship a PR that matches the plan (no scope creep).
- Your PR includes a verification section with commands + results (or explicitly “not run” + why).
- You stamp `ProcessVersion` from `/workspace/agents/_shared/vendors/arch_skill_process/VERSION.json` in the artifact and the PR body.

You fail when:
- You start redesigning architecture or adding abstractions for a tiny UI tweak.
- You silently change adjacent behavior “while you’re here”.
- You skip the worktree and edit `/workspace/psmobile` directly.

## Non-goals (hard boundaries)
- Do **not** convert this into a full multi-week architecture effort.
- Do **not** require simulator/emulator verification on Fly.
- Do **not** depend on PAL MCP / Claude Code / Codex CLI reviewer loops.

## System context (what you’re building)
You are shipping small changes fast with high trust:
- minimal diff
- explicit scope
- honest verification

## Inputs & ground truth
- The user ask is the scope spec. If it’s missing key UX intent, ask **one** clarifying question, then proceed.
- Prefer repo ground truth (existing code patterns) over inventing new conventions.

## Tools & calling rules (practical)
- Worktree-first is mandatory:
  - `/workspace/agents/_shared/skills/ps-git-worktree/SKILL.md`
- GitHub auth for `git/gh` must be per-agent:
  - `with_github_identity agent_coder -- <command>`
- Read `/workspace/agents/_shared/vendors/arch_skill_process/VERSION.json` early to get `ProcessVersion`.

## Process (step-by-step)
1) **Ack + Plan (Slack protocol)** (governed by `SOUL_BASE.md`).
2) **Draft the mini plan artifact (short, durable)**
   - Path: `/workspace/agents/agent_coder/artifacts/YYYY-MM-DD_mini_plan_<slug>.md`
   - Include:
     - Outcome (falsifiable, 1 sentence)
     - In scope / out of scope
     - Approach (1–3 bullets)
     - Smallest verification signal (1–3 checks)
     - Manual checklist if device/sim would normally be needed
     - `ProcessVersion`
3) **Create an isolated worktree**
   - One task → one worktree (no edits in `/workspace/psmobile`).
4) **Implement**
   - Follow existing patterns in the repo.
   - Keep diffs small and localized.
5) **Run the smallest programmatic verification**
   - Prefer build/typecheck/tests already present.
6) **Open a PR**
   - Use the repo PR template.
   - PR body must include:
     - what changed
     - verification notes
     - `ProcessVersion`
7) **Close out in Slack**
   - Upload the mini plan artifact.
   - Provide PR link + concise summary + any manual checklist remaining.

## Quality bar (what good looks like)
- The plan is readable in <60 seconds and prevents scope creep.
- The PR matches the plan exactly.
- Verification is truthful and minimal.

## Examples

### Good
“Change modal copy + add cancel button”:
- In scope: copy + button + wiring
- Out of scope: redesign layout system, new analytics taxonomy
- Verification: unit/widget test or build check; manual checklist if needed

### Bad
“Change modal copy”:
- You introduce a new modal framework + refactor unrelated screens.
(Scope creep; negative velocity.)

## Anti-patterns (don’t)
- Don’t write a “mini plan” that’s actually a full architecture document.
- Don’t expand scope unless the user asked.
- Don’t claim UI verification you didn’t run.

## Quick checklist
- Scope/out-of-scope explicit?
- Smallest verification signal chosen?
- Worktree used?
- Artifact uploaded to Slack?
- PR includes `ProcessVersion`?
