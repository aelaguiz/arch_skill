# Custom Prompt Index (arch_skill)

This file is now an **index only**.

This repo is meant to be used via **installed Codex CLI prompts** (slash commands), not by “importing” it into another repo.
The actual prompt bodies live in `prompts/`.

---

## How to install

```bash
@channel

git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

Restart your Codex instance after updating prompts so it reloads `/prompts:*`.

---

## Prompt index

| Prompt file | Command | Purpose |
| --- | --- | --- |
| `prompts/arch-reformat.md` | `/prompts:arch-reformat` | Convert an existing doc into the canonical arch_skill template (preserve content, infer TL;DR + North Star, then ask for confirmation). |
| `prompts/arch-new.md` | `/prompts:arch-new` | Create a new plan doc and draft the TL;DR + North Star from the blurb, then confirm with user. |
| `prompts/arch-kickoff.md` | `/prompts:arch-kickoff` | Start Phase 1 (Research) and checkpoint before Phase 2 (Architectural planning: current/target architecture + call-site audit). |
| `prompts/arch-phase-plan.md` | `/prompts:arch-phase-plan` | Insert the phased implementation plan block. |
| `prompts/arch-phase-plan-agent.md` | `/prompts:arch-phase-plan-agent` | Agent-assisted phase plan: use parallel read-only subagents for call-site + delete list discovery, then write the phased plan. |
| `prompts/arch-deep-dive.md` | `/prompts:arch-deep-dive` | Fill Current/Target architecture + Call‑Site Audit sections. |
| `prompts/arch-deep-dive-agent.md` | `/prompts:arch-deep-dive-agent` | Agent-assisted deep dive: use parallel read-only subagents for current-arch mapping + call-site sweep + consolidation scan. |
| `prompts/arch-mini-plan-agent.md` | `/prompts:arch-mini-plan-agent` | Mini planning pass: fill Research Grounding + Current/Target Architecture + Call-Site Audit + Phase Plan in one agent-assisted prompt (small tasks). |
| `prompts/arch-plan-audit.md` | `/prompts:arch-plan-audit` | Audit plan readiness across phases (emphasis: fully specified target architecture, fully idiomatic, call sites audited). |
| `prompts/arch-plan-audit-agent.md` | `/prompts:arch-plan-audit-agent` | Agent-assisted plan audit: use parallel read-only subagents to validate call-site completeness, architecture specificity, and idiomatic fit. |
| `prompts/arch-plan-enhance.md` | `/prompts:arch-plan-enhance` | Enhance an existing plan to be best-possible: idiomatic + SSOT + call‑site complete + drift-proof. |
| `prompts/arch-audit-implementation.md` | `/prompts:arch-audit-implementation` | Audit implementation completeness vs the plan, reopen false-complete phases, and get opus+gemini second opinions. |
| `prompts/arch-audit-implementation-agent.md` | `/prompts:arch-audit-implementation-agent` | Agent-assisted implementation audit: parallel read-only subagents prove call-site completeness + cleanup + guardrails, then opus+gemini. |
| `prompts/arch-ui-ascii.md` | `/prompts:arch-ui-ascii` | Add ASCII mockups for current/target UI states. |
| `prompts/arch-ascii.md` | `/prompts:arch-ascii` | Render a simple ASCII chart for the current topic/pipeline. |
| `prompts/arch-research.md` | `/prompts:arch-research` | Populate Research Grounding (external + internal anchors). |
| `prompts/arch-research-agent.md` | `/prompts:arch-research-agent` | Agent-assisted research: parallel read-only subagents gather internal ground truth/patterns and fixtures/tests evidence. |
| `prompts/arch-external-research-agent.md` | `/prompts:arch-external-research-agent` | External web research: parallel subagents search best-in-class practices for plan-adjacent topics and write them into DOC_PATH with sources. |
| `prompts/arch-progress.md` | `/prompts:arch-progress` | Update the worklog with phase progress (plan doc only for decisions). |
| `prompts/arch-implement.md` | `/prompts:arch-implement` | Implement the plan end-to-end: systematic + test-as-you-go + keep doc current + review gate + commit/push after review. |
| `prompts/arch-implement-agent.md` | `/prompts:arch-implement-agent` | Agent-assisted implement: main agent orchestrates phase-by-phase; subagents write code + run checks; main context stays lean. |
| `prompts/arch-qa-autotest.md` | `/prompts:arch-qa-autotest` | Automation QA on existing sims/emulators, then reopen plan issues with evidence. |
| `prompts/arch-ramp-up.md` | `/prompts:arch-ramp-up` | Ramp up on an existing plan doc + code before taking action. |
| `prompts/arch-ramp-up-agent.md` | `/prompts:arch-ramp-up-agent` | Agent-assisted ramp-up: parallel read-only orientation on DOC_PATH + code anchors + repo commands before acting. |
| `prompts/arch-debug.md` | `/prompts:arch-debug` | Debug in context of an existing plan: prove root cause + propose an elegant plan-aligned fix. |
| `prompts/arch-debug-brutal.md` | `/prompts:arch-debug-brutal` | Brutal dev diagnosis: fastest path to prove root cause (temporary hacks allowed). |
| `prompts/arch-devx.md` | `/prompts:arch-devx` | Add Dev Experience targets (CLI/output mocks, artifacts, commands). |
| `prompts/arch-devx-agent.md` | `/prompts:arch-devx-agent` | Agent-assisted DevX: parallel read-only subagents discover existing commands/artifacts; main agent writes DX targets. |
| `prompts/arch-audit.md` | `/prompts:arch-audit` | In‑process audit: code vs plan, add Gaps & Concerns list. |
| `prompts/arch-audit-agent.md` | `/prompts:arch-audit-agent` | Agent-assisted audit: parallel read-only subagents scan for misses/drift/conventions; main agent updates doc. |
| `prompts/arch-review-gate.md` | `/prompts:arch-review-gate` | External review gate for completeness/idiomatic fit. |
| `prompts/arch-html-full.md` | `/prompts:arch-html-full` | Render a full-fidelity HTML doc using the shared template (no omissions). |
| `prompts/arch-ralph-retarget.md` | `/prompts:arch-ralph-retarget` | (Re)seed Ralph in a repo: copy `PROMPT.md`/`@fix_plan.md`/`@AGENT.md` from `~/.ralph/templates`, materialize SSOT in `specs/`, patch PROMPT with a small project context block, and rewrite `@fix_plan.md` into granular phased tasks (manual QA non-blocking). |
| `prompts/arch-ralph-enhance.md` | `/prompts:arch-ralph-enhance` | Second pass for Ralph: re-review DOC_PATH + existing Ralph files, make tasks more granular/complete/idiomatic, and prevent manual-QA proof burdens (update in-place; no code edits). |
| `prompts/maestro-autopilot.md` | `/prompts:maestro-autopilot` | Autonomously run Maestro tests, fix flow issues, re-run. |
| `prompts/maestro-rerun-last.md` | `/prompts:maestro-rerun-last` | Re-run the most recent failed Maestro flow. |
| `prompts/maestro-kill.md` | `/prompts:maestro-kill` | Kill stuck Maestro runs. |
| `prompts/qa-autopilot.md` | `/prompts:qa-autopilot` | Run QA automation (framework-agnostic), fix broken flows idiomatically, and write a QA worklog (plan-aware). |

---

## Suggested usage flows

For a deeper explanation of when to use the **regular flow** vs the **mini flow** (and the conventions that make the prompts compose cleanly), see:
- `docs/arch_skill_usage_guide.md`

### If you already have an existing doc (wrong format)
1) `/prompts:arch-reformat …` (normalize into the canonical template + confirm North Star)
2) Continue with the standard flow below (usually `/prompts:arch-kickoff …`), or use the mini flow (`/prompts:arch-mini-plan-agent …`) if it's a small task.

### Mini flow (small task; fewer prompts; agent-assisted)
1) `/prompts:arch-reformat …` (only if you already have a doc and it needs canonical formatting)
2) `/prompts:arch-mini-plan-agent …` (combined planning pass: research + deep dive + phase plan)
3) `/prompts:arch-implement-agent …` (implement in 1-2 phases; minimal checks; keep doc/worklog current)
4) `/prompts:arch-qa-autotest …` (optional: run automation on an existing sim/emulator; reopen plan issues with evidence)
5) `/prompts:arch-audit-agent …` (recommended: fast audit for drift/missed call sites)
6) `/prompts:arch-audit-implementation-agent …` (optional upgrade: strict completeness audit + second opinions)

### Minimal flow (small change)
1) `/prompts:arch-new …`
2) `/prompts:arch-research …`
3) `/prompts:arch-deep-dive …`
4) `/prompts:arch-plan-enhance …` (optional, recommended: tighten plan + drift-proofing sweep)
5) `/prompts:arch-phase-plan …`
6) `/prompts:arch-implement …` (implement + test systematically; keep doc current; review gate; commit/push after review)
7) `/prompts:arch-qa-autotest …` (optional: run automation on an existing sim/emulator; reopen plan issues with evidence)
8) `/prompts:arch-audit-implementation …` (recommended: prove we didn’t miss anything; reopen false-complete)

### Full flow (large change)
1) `/prompts:arch-new …`
2) `/prompts:arch-kickoff …`
3) `/prompts:arch-research …`
4) `/prompts:arch-deep-dive …`
5) `/prompts:arch-ui-ascii …` (if UI)
6) `/prompts:arch-plan-enhance …`
7) `/prompts:arch-phase-plan …`
8) `/prompts:arch-devx …` (if CLI/output mocks are required)
9) `/prompts:arch-review-gate …`
10) `/prompts:arch-implement …` (implement + test systematically; keep doc current; review gate; commit/push after review)
11) `/prompts:arch-qa-autotest …` (optional: run automation on an existing sim/emulator; reopen plan issues with evidence)
12) `/prompts:arch-progress …` (optional if not covered by implement)
13) `/prompts:arch-audit-implementation …` (recommended: completeness + idiomatic audit vs plan; reopen false-complete)
