# Custom Prompt Index (arch_skill)

This file is now an **index only**. The actual prompt bodies live in `arch_skill/prompts/`.
Copy or symlink them into `~/.codex/prompts/` to use as `/prompts:<name>` commands.

---

## How to install

```bash
mkdir -p ~/.codex/prompts
cp arch_skill/prompts/*.md ~/.codex/prompts/
```

Restart Codex after updating prompts.

---

## Prompt index

| Prompt file | Command | Purpose |
| --- | --- | --- |
| `arch_skill/prompts/arch-new.md` | `/prompts:arch-new` | Create a new plan doc and draft the TL;DR + North Star from the blurb, then confirm with user. |
| `arch_skill/prompts/arch-kickoff.md` | `/prompts:arch-kickoff` | Start Phase 1 (Research) and checkpoint before Phase 2 (Architectural planning: current/target architecture + call-site audit). |
| `arch_skill/prompts/arch-phase-plan.md` | `/prompts:arch-phase-plan` | Insert the phased implementation plan block. |
| `arch_skill/prompts/arch-deep-dive.md` | `/prompts:arch-deep-dive` | Fill Current/Target architecture + Call‑Site Audit sections. |
| `arch_skill/prompts/arch-plan-audit.md` | `/prompts:arch-plan-audit` | Audit plan readiness across phases (emphasis: fully specified target architecture, fully idiomatic, call sites audited). |
| `arch_skill/prompts/arch-plan-enhance.md` | `/prompts:arch-plan-enhance` | Enhance an existing plan to be best-possible: idiomatic + SSOT + call‑site complete + drift-proof. |
| `arch_skill/prompts/arch-impl-audit.md` | `/prompts:arch-impl-audit` | Audit implementation completeness vs the plan, reopen false-complete phases, and get opus+gemini second opinions. |
| `arch_skill/prompts/arch-ui-ascii.md` | `/prompts:arch-ui-ascii` | Add ASCII mockups for current/target UI states. |
| `arch_skill/prompts/arch-ascii.md` | `/prompts:arch-ascii` | Render a simple ASCII chart for the current topic/pipeline. |
| `arch_skill/prompts/arch-research.md` | `/prompts:arch-research` | Populate Research Grounding (external + internal anchors). |
| `arch_skill/prompts/arch-progress.md` | `/prompts:arch-progress` | Update the worklog with phase progress (plan doc only for decisions). |
| `arch_skill/prompts/arch-implement.md` | `/prompts:arch-implement` | Implement the plan end-to-end: systematic + test-as-you-go + keep doc current + review gate + commit/push after review. |
| `arch_skill/prompts/arch-ramp-up.md` | `/prompts:arch-ramp-up` | Ramp up on an existing plan doc + code before taking action. |
| `arch_skill/prompts/arch-debug.md` | `/prompts:arch-debug` | Debug in context of an existing plan: prove root cause + propose an elegant plan-aligned fix. |
| `arch_skill/prompts/arch-debug-brutal.md` | `/prompts:arch-debug-brutal` | Brutal dev diagnosis: fastest path to prove root cause (temporary hacks allowed). |
| `arch_skill/prompts/arch-devx.md` | `/prompts:arch-devx` | Add Dev Experience targets (CLI/output mocks, artifacts, commands). |
| `arch_skill/prompts/arch-audit.md` | `/prompts:arch-audit` | In‑process audit: code vs plan, add Gaps & Concerns list. |
| `arch_skill/prompts/arch-audit-subagent.md` | `/prompts:arch-audit-subagent` | Run arch audit in a subagent and insert Gaps & Concerns into the doc. |
| `arch_skill/prompts/arch-review-gate.md` | `/prompts:arch-review-gate` | External review gate for completeness/idiomatic fit. |
| `arch_skill/prompts/arch-html-full.md` | `/prompts:arch-html-full` | Render a full-fidelity HTML doc using the shared template (no omissions). |
| `arch_skill/prompts/arch-ralph-retarget.md` | `/prompts:arch-ralph-retarget` | Retarget an existing Ralph setup by updating `PROMPT.md` + `@fix_plan.md` in-place from a plan doc (manual QA non-blocking); hard-bails if Ralph isn’t set up. |
| `arch_skill/prompts/maestro-autopilot.md` | `/prompts:maestro-autopilot` | Autonomously run Maestro tests, fix flow issues, re-run. |
| `arch_skill/prompts/maestro-rerun-last.md` | `/prompts:maestro-rerun-last` | Re-run the most recent failed Maestro flow. |
| `arch_skill/prompts/maestro-kill.md` | `/prompts:maestro-kill` | Kill stuck Maestro runs. |
| `arch_skill/prompts/qa-autopilot.md` | `/prompts:qa-autopilot` | Run QA automation (framework-agnostic), fix broken flows idiomatically, and write a QA worklog (plan-aware). |

---

## Suggested usage flows

### Minimal flow (small change)
1) `/prompts:arch-new …`
2) `/prompts:arch-research …`
3) `/prompts:arch-deep-dive …`
4) `/prompts:arch-plan-enhance …` (optional, recommended: tighten plan + drift-proofing sweep)
5) `/prompts:arch-phase-plan …`
6) `/prompts:arch-implement …` (implement + test systematically; keep doc current; review gate; commit/push after review)
7) `/prompts:arch-impl-audit …` (recommended: prove we didn’t miss anything; reopen false-complete)

### Full flow (large change)
1) `/prompts:arch-new …`
2) `/prompts:arch-kickoff …`
3) `/prompts:arch-research …`
4) `/prompts:arch-deep-dive …`
5) `/prompts:arch-ui-ascii …` (if UI)
6) `/prompts:arch-plan-enhance …`
7) `/prompts:arch-phase-plan …`
8) `/prompts:arch-devx …` (if CLI/output mocks are required)
9) `/prompts:arch-audit-subagent …` (subagent code vs plan check)
10) `/prompts:arch-review-gate …`
11) `/prompts:arch-implement …` (implement + test systematically; keep doc current; review gate; commit/push after review)
12) `/prompts:arch-progress …` (optional if not covered by implement)
13) `/prompts:arch-impl-audit …` (recommended: completeness + idiomatic audit vs plan; reopen false-complete)
