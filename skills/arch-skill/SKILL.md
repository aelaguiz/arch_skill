---
name: arch-skill
description: "Router + invariants for the arch_skill prompt suite. Use it to keep a single SSOT plan doc + worklog, enforce strict question policy, and route to the right /prompts:* command for architecture planning and execution."
---

# arch-skill

This skill runs **alongside** the existing `/prompts:*` commands:
- Use it to decide which prompt to run next and to enforce the workflow invariants.
- Then invoke the prompt directly (preferred) or load its markdown procedure on demand.

## When to Use
- User asks for architecture planning, a phased plan, a call-site audit, or "arch_skill flow".
- Work needs a single plan doc + worklog and minimal, credible verification.
- You want to route the user to the correct `/prompts:*` command (and keep the process consistent).

## Non‑Negotiables (Workflow Invariants)
- **Single-document rule (SSOT):** exactly one plan doc under `docs/` is authoritative. Worklog is derived from it.
- **Code is ground truth:** anchor claims in file paths/symbols/commands; do not speculate.
- **Minimal verification:** prefer existing tests/commands; avoid inventing new harnesses by default.
- **No fallbacks:** do not propose or implement runtime fallbacks/shims/placeholder behavior unless explicitly approved in the plan doc (`fallback_policy: approved` + Decision Log entry).
- **Question policy (strict):** only ask questions that cannot be answered by searching the repo/docs/fixtures or running existing tooling.
- **Output format:** when you invoke a prompt, follow that prompt's output format (don't restate style rules here).

## Routing Rule (How to "Load Prompts on Demand")
Prefer invoking prompts:
- Use `/prompts:<name> …` whenever possible (Codex/Claude Code handles placeholder expansion).

If you must **load the markdown procedure directly** (no `/prompts` invocation), then:
- Open the prompt file and follow it as the procedure.
- Apply the placeholder binding contract in `resources/BINDING_CONTRACT.md` (especially `$ARGUMENTS`).

Prompt discovery order:
1) Installed prompts (Claude Code): `~/.claude/commands/prompts/<name>.md`
2) Installed prompts (Codex): `~/.codex/prompts/<name>.md`
3) Repo prompts (when working inside this repo): `prompts/<name>.md`

## Prompt Index
See `resources/PROMPT_INDEX.md` for the canonical mapping from intent → prompt name.

## Full Prompt Catalog

### Setup & orientation

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-new` | Create canonical plan doc + draft North Star from blurb, then confirm. | Freeform blurb |
| `/prompts:arch-reformat` | Convert existing doc into canonical arch_skill format (preserve content). | Input `.md` path; optional `OUT=...` |
| `/prompts:arch-flow` | Detect where you are in the arch flow and recommend/run the next step. | `DOC_PATH` |
| `/prompts:arch-kickoff` | Phase 1 kickoff: research setup + checkpoints. | `DOC_PATH` |
| `/prompts:arch-ramp-up` | Quick ramp-up: read plan doc + referenced code before acting. | `DOC_PATH` or guidance |
| `/prompts:arch-ramp-up-agent` | Agent-assisted ramp-up (parallel read-only scans). | `DOC_PATH` or guidance |
| `/prompts:arch-context-load` | Derive high-signal brief from DOC_PATH for agent handoff. | `DOC_PATH` |

### Mini-arch (lilarch — tiny tasks)

`lilarch` is a compressed 3-prompt flow for small features/improvements that can ship in 1–3 phases.
If the work expands beyond that (or is investigation-heavy), switch back to the full `arch-*` flow or the `bugs-*` flow.

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:lilarch-start` | Create/repair a compact plan doc: North Star + requirements + minimal grounding (optional external best practices). | Freeform request; optional `docs/<...>.md` |
| `/prompts:lilarch-plan` | Deep dive + 1–3 phase plan + internal plan audit + external plan audit (write back to doc). | `DOC_PATH` |
| `/prompts:lilarch-finish` | Implement + self-audit + external code review; update worklog and mark doc complete. | `DOC_PATH`; optional `PAUSE=1` |

### Research grounding

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-research` | Write Research Grounding (internal anchors + patterns). | `DOC_PATH` |
| `/prompts:arch-research-agent` | Agent-assisted research grounding with subagents. | `DOC_PATH` |
| `/prompts:arch-external-research-agent` | Web-based best-practice research, write grounded notes with sources. | `DOC_PATH` |

### Architecture deep dive

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-deep-dive` | Current/Target architecture + call-site audit. | `DOC_PATH` |
| `/prompts:arch-deep-dive-agent` | Agent-assisted deep dive (parallel read-only). | `DOC_PATH` |

### Implementation planning

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-plan-enhance` | Harden plan (turn it into best possible architecture). | `DOC_PATH` |
| `/prompts:arch-phase-plan` | Generate depth-first phased implementation plan. | `DOC_PATH` |
| `/prompts:arch-phase-plan-agent` | Agent-assisted phase plan with subagent discovery. | `DOC_PATH` |
| `/prompts:arch-phase-plan-granularize` | Optional: rewrite the Phase Plan into micro-phases + microtasks (single SSOT; no second checklist). | `DOC_PATH` |
| `/prompts:arch-phase-plan-granularize-agent` | Agent-assisted phase plan granularize (parallel read-only: call-site batching, deletes, smallest checks). | `DOC_PATH` |
| `/prompts:arch-review-gate` | External idiomatic + completeness check (recommended for risky changes). | `DOC_PATH` |
| `/prompts:arch-fold-in` | Inline reference docs/links into phases so implementation can't miss them. | `DOC_PATH` |
| `/prompts:arch-plan-audit` | Score plan readiness across phases. | `DOC_PATH` |
| `/prompts:arch-plan-audit-agent` | Agent-assisted plan audit with parallel subagent checks. | `DOC_PATH` |
| `/prompts:arch-mini-plan-agent` | One-pass research + deep dive + phase plan (small tasks). | `DOC_PATH` |

### Execution

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-implement` | Ship the plan end-to-end (systematic, test-as-you-go), update worklog. | `DOC_PATH` |
| `/prompts:arch-implement-agent` | Agent-assisted implement using subagents for code + tests. | `DOC_PATH` |
| `/prompts:arch-progress` | Progress update only (no replanning). | `DOC_PATH` |

### Audits & completion checks

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-audit` | Code vs plan gaps list. | `DOC_PATH` |
| `/prompts:arch-audit-agent` | Agent-assisted audit with subagents. | `DOC_PATH` |
| `/prompts:arch-audit-implementation` | Implementation audit: confirm plan compliance + completeness. | `DOC_PATH` |
| `/prompts:arch-audit-implementation-agent` | Implementation audit (agent-assisted) with subagent scans. | `DOC_PATH` |
| `/prompts:arch-qa-autotest` | Run automation harness on existing sim/emulator. | `DOC_PATH` |

### Bug workflow

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:bugs-analyze` | Create/update bug doc, ingest evidence, form hypotheses. | `DOC_PATH` or evidence |
| `/prompts:bugs-fix` | Plan + implement the bug fix, challenge the plan, verify. | `DOC_PATH` |
| `/prompts:bugs-review` | External audit of bug fix against the bug doc. | `DOC_PATH` |

### Goal-seeking loops

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:goal-loop-new` | Create/repair Goal Loop SSOT doc + append-only running log. | Freeform goal |
| `/prompts:goal-loop-iterate` | Execute ONE bet, append to running log, compound learning. | `DOC_PATH` |
| `/prompts:goal-loop-flow` | Check readiness, recommend single best next step. | `DOC_PATH` |
| `/prompts:goal-loop-context-load` | Write Context Digest from DOC_PATH + log for restarts. | `DOC_PATH` |

### Debug

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-debug` | Plan-aware root cause identification + elegant fix proposal. | `DOC_PATH` or guidance |
| `/prompts:arch-debug-brutal` | Fast root cause (temporary hacks allowed). | `DOC_PATH` or guidance |

### Developer experience

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-devx` | CLI-output mocks + artifacts. | `DOC_PATH` |
| `/prompts:arch-devx-agent` | Agent-assisted DevX with subagent discovery. | `DOC_PATH` |

### Code review & finalization

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-codereview` | Run cross-tool external review (Claude↔Codex), then apply feedback you agree with. | `DOC_PATH` + scope |
| `/prompts:arch-open-pr` | Merge default branch, run preflight, commit/push, open detailed **draft** PR. | Optional title/constraints |

### Rendering

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-html-full` | Render doc with zero omissions (full fidelity HTML). | `DOC_PATH` |
| `/prompts:arch-ascii` | Visualize current topic or pipeline as ASCII chart. | `DOC_PATH` or topic |
| `/prompts:arch-ui-ascii` | Current/target ASCII UI mockups (if plan touches UI). | `DOC_PATH` |

### Ralph

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-ralph-retarget` | Bootstrap-safe: seed from templates, set agent, rewrite fix_plan. | `SPEC_PATH` |
| `/prompts:arch-ralph-enhance` | Re-review spec + existing plan, make tasks more granular + complete. | `SPEC_PATH` |

### Maestro / QA automation

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:maestro-autopilot` | Run tests, fix flow issues, re-run. | `DOC_PATH` or guidance |
| `/prompts:maestro-rerun-last` | Re-run most recent failed flow. | (none) |
| `/prompts:maestro-kill` | Stop stuck maestro runs. | (none) |
| `/prompts:qa-autopilot` | Run QA automation, fix broken flows, document results. | `DOC_PATH` or guidance |

### North Star investigation

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:north-star-investigation-bootstrap` | Bootstrap a North Star investigation doc (Commander's Intent). | Freeform `$ARGUMENTS` |
| `/prompts:north-star-investigation-loop` | Execute investigation loop: iterate + learn + refine. | `DOC_PATH` |

### Misc

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:new-arch-from-docs` | Transform requirements folder into single canonical plan doc. | Folder or paths |
