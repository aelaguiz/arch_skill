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
| `arch_skill/prompts/arch-new.md` | `/prompts:arch-new` | Create a new architecture doc from the canonical template (single‑doc rule). |
| `arch_skill/prompts/arch-kickoff.md` | `/prompts:arch-kickoff` | Start Phase 1 research and checkpoint before Phase 2. |
| `arch_skill/prompts/arch-phase-plan.md` | `/prompts:arch-phase-plan` | Insert the phased implementation plan block. |
| `arch_skill/prompts/arch-deep-dive.md` | `/prompts:arch-deep-dive` | Fill Current/Target architecture + Call‑Site Audit sections. |
| `arch_skill/prompts/arch-ui-ascii.md` | `/prompts:arch-ui-ascii` | Add ASCII mockups for current/target UI states. |
| `arch_skill/prompts/arch-ascii.md` | `/prompts:arch-ascii` | Render a simple ASCII chart for the current topic/pipeline. |
| `arch_skill/prompts/arch-research.md` | `/prompts:arch-research` | Populate Research Grounding (external + internal anchors). |
| `arch_skill/prompts/arch-progress.md` | `/prompts:arch-progress` | Update the canonical doc with phase progress + Decision Log. |
| `arch_skill/prompts/arch-implement.md` | `/prompts:arch-implement` | Execute the next phase and update the doc + tests/review. |
| `arch_skill/prompts/arch-ramp-up.md` | `/prompts:arch-ramp-up` | Ramp up on an existing plan doc + code before taking action. |
| `arch_skill/prompts/arch-devx.md` | `/prompts:arch-devx` | Add Dev Experience targets (CLI/output mocks, artifacts, commands). |
| `arch_skill/prompts/arch-audit.md` | `/prompts:arch-audit` | In‑process audit: code vs plan, add Gaps & Concerns list. |
| `arch_skill/prompts/arch-audit-subagent.md` | `/prompts:arch-audit-subagent` | Run arch audit in a subagent and insert Gaps & Concerns into the doc. |
| `arch_skill/prompts/arch-review-gate.md` | `/prompts:arch-review-gate` | External review gate for completeness/idiomatic fit. |
| `arch_skill/prompts/arch-html-full.md` | `/prompts:arch-html-full` | Render a full-fidelity HTML doc using the shared template (no omissions). |
| `arch_skill/prompts/maestro-autopilot.md` | `/prompts:maestro-autopilot` | Autonomously run Maestro tests, fix flow issues, re-run. |
| `arch_skill/prompts/maestro-rerun-last.md` | `/prompts:maestro-rerun-last` | Re-run the most recent failed Maestro flow. |
| `arch_skill/prompts/maestro-kill.md` | `/prompts:maestro-kill` | Kill stuck Maestro runs. |

---

## Suggested usage flows

### Minimal flow (small change)
1) `/prompts:arch-new …`
2) `/prompts:arch-research …`
3) `/prompts:arch-deep-dive …`
4) `/prompts:arch-phase-plan …`
5) `/prompts:arch-implement …` (execute phase; updates doc/tests/review)

### Full flow (large change)
1) `/prompts:arch-new …`
2) `/prompts:arch-kickoff …`
3) `/prompts:arch-research …`
4) `/prompts:arch-deep-dive …`
5) `/prompts:arch-ui-ascii …` (if UI)
6) `/prompts:arch-phase-plan …`
7) `/prompts:arch-devx …` (if CLI/output mocks are required)
8) `/prompts:arch-audit-subagent …` (subagent code vs plan check)
9) `/prompts:arch-review-gate …`
10) `/prompts:arch-implement …` (execute each phase; updates doc/tests/review)
11) `/prompts:arch-progress …` (optional if not covered by implement)
