# Arch Plan Workflow Details

Use this file when `SKILL.md` is not enough to decide which part of the full arch workflow to run.

## Routing by user ask

- "Create a new plan", "start the arch flow", "reformat this doc":
  - create or repair `DOC_PATH`
  - draft the North Star and pause for confirmation if needed
- "Ramp up", "load context", "read the plan before acting":
  - do a read-only ramp-up against `DOC_PATH`
  - write a short context digest only when the user asked for restart or handoff help
- "Do research", "ground this in the repo", "external research":
  - write the research grounding or external research blocks
- "Deep dive", "map current/target architecture", "call-site audit":
  - update current architecture, target architecture, and call-site audit together
- "Phase plan", "tighten the plan", "prevent overbuild", "fold in these specs", "review the plan":
  - do the phase-plan pass and any explicitly requested plan-shaping move
- "Implement the plan", "continue execution", "progress update":
  - implement locally against `DOC_PATH` and keep `WORKLOG_PATH` current
- "Audit implementation", "did we actually finish?", "reopen false-complete phases":
  - run the implementation audit and update the doc truth
- "Render this", "show me the UI/architecture", "make the plan easier to inspect":
  - add UI ASCII or architecture ASCII only when the user explicitly wants the rendering
- "Mock the CLI/devx output":
  - produce the devx artifact only when requested
- "Code review":
  - keep cross-model review explicit-review-only
- "Open the PR":
  - treat PR finalization as a late-stage helper, not part of the default full flow

## Plan-shaping moves

These are part of `arch-plan`, not standalone skills:

- plan enhance:
  - harden contracts, deletes, and consolidation
- fold in:
  - inline external specs/docs so implementation cannot miss them
- overbuild protector:
  - separate ship-blocking work from follow-ups and scope creep
- review gate:
  - run a local idiomatic/completeness review before execution
- gaps audit:
  - capture "gaps and concerns" without turning the audit into implementation
- UI ASCII:
  - add contract-level current/target mockups when UX is in scope
- ramp-up:
  - read the plan doc and the referenced code before acting
- context digest:
  - compress the plan/worklog into a restart-safe brief when explicitly requested
- progress only:
  - update worklog and status without silently replanning
- render / HTML / ASCII:
  - only when the user asks for presentation or visualization help
- devx:
  - only when the user wants CLI-output mocks or related artifacts

## Delegation policy

- If the runtime and user explicitly permit delegation, you may parallelize read-only scans for:
  - internal anchors
  - call-site sweeps
  - reusable patterns
  - smallest-signal checks
  - external-research topic harvesting
- Never delegate implementation.
- Never run multiple doc-writing workers against the same `DOC_PATH`.

## Legacy prompt parity

This skill absorbs the runtime responsibilities that used to live in:

- `arch-new`, `arch-reformat`
- `arch-ramp-up`, `arch-ramp-up-agent`
- `arch-context-load`
- `arch-research`, `arch-research-agent`
- `arch-external-research-agent`
- `arch-deep-dive`, `arch-deep-dive-agent`
- `arch-plan-enhance`
- `arch-phase-plan`, `arch-phase-plan-agent`
- `arch-phase-plan-granularize`, `arch-phase-plan-granularize-agent`
- `arch-fold-in`
- `arch-overbuild-protector`
- `arch-review-gate`
- `arch-implement`
- `arch-progress`
- `arch-audit`
- `arch-audit-implementation`, `arch-audit-implementation-agent`
- `arch-html-full`
- `arch-ascii`, `arch-ui-ascii`
- `arch-devx`, `arch-devx-agent`
