# arch_skill Usage Guide

This guide describes the live workflow surface for the repo.

The current skill suite is:

- `arch-step`
- `arch-docs`
- `arch-mini-plan`
- `lilarch`
- `bugs-flow`
- `goal-loop`
- `north-star-investigation`
- `arch-flow`
- `arch-skills-guide`

`arch-step` is the only live full-arch execution surface.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

For Codex automatic `auto-plan`, `implement-loop`, and `arch-docs auto`, also enable the Codex feature once:

```bash
codex features enable codex_hooks
```

Default local path:

- `~/.agents/skills/arch-step/`
- `~/.agents/skills/arch-docs/`
- `~/.agents/skills/arch-mini-plan/`
- `~/.agents/skills/lilarch/`
- `~/.agents/skills/bugs-flow/`
- `~/.agents/skills/goal-loop/`
- `~/.agents/skills/north-star-investigation/`
- `~/.agents/skills/arch-flow/`
- `~/.agents/skills/arch-skills-guide/`
- `~/.agents/skills/codemagic-builds/`

Codex reads the same installed skills from `~/.agents/skills/`. `make install` also wires the Codex runtime support for `auto-plan`, `implement-loop`, and `arch-docs auto` through `~/.codex/hooks.json` and removes older `~/.codex/skills/<skill>` mirrors from previous installs.

Installed skills:

- Codex:
  - `arch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
  - `codemagic-builds`
- Claude Code:
  - `arch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`
- Gemini:
  - `arch-step`
  - `arch-docs`
  - `arch-mini-plan`
  - `lilarch`
  - `bugs-flow`
  - `goal-loop`
  - `north-star-investigation`
  - `arch-flow`
  - `arch-skills-guide`

Install removes stale pre-skill command surfaces, removed competing skill packages, and older Codex skill mirrors. For Codex, it installs the runtime support for `auto-plan`, `implement-loop`, and `arch-docs auto` in `~/.codex/hooks.json` pointing at the installed runner under `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.

## Shared conventions

### One planning artifact

- Full-arch and mini-plan work keep one canonical `DOC_PATH`.
- Implementation work derives `WORKLOG_PATH` from `DOC_PATH`.
- Do not create sidecar planning docs or competing checklists.

### Code is ground truth

- Anchor claims in files, symbols, tests, logs, or explicit sources.
- Ask only when repo evidence cannot answer the question.

### No hidden fallbacks

- Default to fail-loud behavior, hard cutover, and explicit deletes.
- Runtime shims, compatibility paths, and silent alternate behavior require explicit approval in the governing doc.

### Converge on canonical paths

- When full-arch work touches duplicated or drifting logic, converge onto the canonical existing path or extract one clean shared path.
- Internal convergence work may widen beyond the directly touched file set when needed to remove duplicate truth or prevent a new parallel path.
- Convergence work must not be used as an excuse to invent new product functionality, modes, or speculative infrastructure.

### Preserve behavior during refactor

- Any refactor, consolidation, or shared-path extraction needs a credible behavior-preservation check.
- Prefer existing tests, typecheck, build, instrumentation, or stable behavior-level checks before adding new tests.
- Do not write negative-value tests that only assert implementation details, deletions, or visual constants.

### Capability-first for agent-backed systems

- Understand current prompt surfaces, native model capabilities, and existing tool/file/context exposure before designing.
- Lean into prompt engineering, grounding, and native capabilities before inventing custom harnesses, wrappers, parsers, OCR layers, fuzzy matchers, or scripts.
- If custom tooling is still needed, the plan should say why prompt-first and capability-first options were insufficient and keep the tool narrow.
- When the real lever is prompt repair, call that out plainly and use `prompt-authoring` instead of building deterministic scaffolding around the model.

### Preserve instruction fidelity when porting

- When moving prompts, agent instructions, or other instruction-bearing doctrine, preserve explicit process structure by default.
- Do not silently condense ordered steps, conditions, hard negatives, or escalation logic into vague summary bullets.
- If condensation is truly appropriate, record why it is safe and keep the original text recoverable in the artifact.

### Delete dead truth

- Git is the history for retired code paths, docs, comments, and instructions.
- Do not keep dead competing truth surfaces around for legacy or archaeology.
- If a touched live doc, comment, or instruction still matters after the change, rewrite it to present reality in the same run. If it no longer matters, delete it.

### Full-arch finish handoff

- `arch-step` owns planning, implementation, and code-completeness audit.
- `arch-docs` owns the docs-audit cleanup pass after a clean full-arch code audit and can also run standalone in any repo.
- A clean `implement-loop` or `audit-implementation` means the next required move is docs cleanup, not another generic full-arch command.

## Choosing a skill

### `arch-step`

Use for full-arch planning, continuation, implementation, bounded implement/audit delivery, or implementation audit.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step auto-plan`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step implement docs/MY_PLAN.md`
- `Use $arch-step implement-loop docs/MY_PLAN.md`
- `Use $arch-step audit-implementation docs/MY_PLAN.md`

Practical rule:

- If the ask is generic full arch, the live answer is `arch-step`.
- If the ask names a full-arch command, the live answer is also `arch-step`.
- `arch-step` may widen internal refactor scope to converge on one tested path and remove duplicate truth, but it must not invent extra product functionality while doing it.
- If capability-first analysis shows the main lever is prompt repair, `arch-step` should say so plainly and point to `prompt-authoring`.
- `arch-step status` is the concise readout.
- `arch-step advance` owns the full checklist and exact next-command selection.
- `arch-step auto-plan` is the explicit bounded planning controller after North Star approval. It runs `research`, `deep-dive`, `deep-dive`, and `phase-plan`, then stops and says the doc is ready for `implement-loop`.
- `arch-step implement-loop` is the explicit bounded controller when the user wants repeated implement then audit passes until the audit is clean or a real blocker stops the run.
- After a clean full-arch code audit, `arch-step` hands off to `arch-docs` for docs cleanup using the finished artifact as context.
- In Codex, the user still invokes only `auto-plan` or `implement-loop`; each requires the installed runtime support in `~/.codex/hooks.json` and enabled `codex_hooks`.
- If that hook path is absent or disabled, those commands should fail loud with the remediation commands instead of pretending a prompt-only loop exists.

### `arch-docs`

Use when the code is clean enough to trust and the job is cleaning up stale, overlapping, or misleading docs.

Examples:

- `Use $arch-docs`
- `Use $arch-docs auto`

Practical rule:

- With no extra mode, `arch-docs` runs the normal one-pass DGTFO cleanup and should resolve scope from explicit user context, active arch context, or the repo docs surface.
- Use `arch-docs auto` only in Codex when you want hook-backed repeated cleanup passes with fresh external evaluation.
- If a clean arch plan/worklog exists, `arch-docs` should use it as narrowing context rather than as the whole scope.

### `arch-flow`

Use for read-only checklist and next-step inspection on an arch-style doc.

Examples:

- `Use $arch-flow docs/MY_PLAN.md`
- "What’s next on this doc?"

### `arch-mini-plan`

Use when the task still needs canonical architecture blocks, but the planning should happen in one pass and follow-through should later happen in `arch-step`, then `arch-docs` for later docs cleanup.

Examples:

- `Use $arch-mini-plan docs/MY_PLAN.md`
- "Give me the mini plan version"

### `lilarch`

Use for contained feature work that should fit in 1-3 phases.

Examples:

- `Use $lilarch for this small feature`
- "Use little arch for this improvement"

If lilarch stops fitting, escalate to `arch-step reformat`.

### `bugs-flow`

Use for regressions, crashes, incidents, or Sentry/log-driven fixes.

### `goal-loop`

Use when the goal is clear but the path is unknown and you want a controller doc plus append-only iteration log.

### `north-star-investigation`

Use when the work is a quantified investigation with ranked hypotheses and brutal tests.

### `arch-skills-guide`

Use when the question is which live arch skill should handle the task.

## Full-arch doc conventions

`arch-step` and `arch-mini-plan` both work against a canonical full-arch doc shape. The main stable markers are:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:reference_pack`
- `arch_skill:block:plan_enhancer`
- `arch_skill:block:overbuild_protector`
- `arch_skill:block:review_gate`
- `arch_skill:block:gaps_concerns`
- `arch_skill:block:implementation_audit`

Practical rule:

- Do not delete or rename these markers once the doc is live.

Historical pre-skill materials live under `archive/` and `docs/archive/`. They are not part of the runtime surface.
