# AGENTS.md

This repo ships installable agent skills. `skills/` is the live runtime
surface. `Makefile` plus `README.md` own the install surface for Codex,
Claude Code, and Gemini.

## Build And Verify

- After skill package changes under `skills/`, run `npx skills check`.
- Use `make verify_install` only when you intentionally changed or want to
  validate the installed skill surface.
- If you change install behavior, also verify the affected paths and commands
  in `README.md` and `Makefile`.
- If you change only doctrine or docs, re-read the edited files and verify any
  commands or paths you added with `rg`. Do not imply that code verification
  ran when it did not.

## Definition Of Done

- The touched surface is internally consistent.
- Required verification for that surface ran, or the final reply says plainly
  why it did not.
- `README.md` or the relevant docs are updated when skill names, routing,
  or install behavior changed.
- New doctrine stays concise, command-first, and points to deeper truth
  instead of copying large reference text into always-on context.

## Red Lines

- Do not use external multi-model consultation workflows unless the user
  explicitly asks for a code review.
- Do not delete user work, untracked files, or repo changes unless the user
  explicitly asks for that exact cleanup. If you are not sure whether a file
  came from your own run, leave it alone and ask.
- Do not make shipped skills depend on archived command files at runtime.
- Do not revive archived command surfaces as part of the live runtime.
- Skill doctrine must be self-contained. Do not explain it with historical
  backstory or the skill development process itself. The only exception is a
  coordinator skill whose job is to explain how other skills fit together.
- Keep changes in the smallest owning surface: reusable workflow doctrine in
  `skills/`, install behavior and stale-surface cleanup in `Makefile`, and
  deeper reference material in `docs/`.

## Skill Routing

- Use `$skill-authoring` for new, edited, refactored, or audited skill
  packages.
- Use `$agents-md-authoring` for `AGENTS.md` authoring or refactors.
- If the user wants to execute one of the shipped workflows, use the matching
  split skill instead of reviving the archived pre-skill surface.
- Use `$arch-step` when the user wants explicit full-arch commands such as
  `new`, `reformat`, `research`, `deep-dive`, `external-research`,
  `phase-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`,
  `consistency-pass`, `review-gate`, `implement`,
  `audit-implementation`, `status`, or `advance`.
- Use `$arch-flow` for read-only checklist and next-step inspection.
- Use `$arch-skills-guide` when the user asks which arch skill to use or how
  the suite is divided.
- Use `$stepwise` when the user wants to run an ordered multi-step process
  (named in another repo's doctrine) with a fresh sub-session per step and a
  per-step critic that resumes the same session on fail.
- Use `$arch-epic` when the user has a goal too big for one `$arch-step` plan
  and wants to decompose it into ordered sub-plans, approve the decomposition
  up front, run each sub-plan through arch-step's `new` → `auto-plan` →
  `implement-loop` → `audit-implementation` arc, and have a fresh critic check
  for scope drift between sub-plans before advancing.

## Writing And Replies

- Write for a human reader first.
- Use plain English. Do not make the reader decode house jargon, compressed
  labels, or pseudo-technical wording.
- Lead with the concrete thing in 1-3 sentences: what changed, what to run,
  what happens next, or what the blocker is.
- If the real answer is a path, command, setting, or skill name, name that
  exact thing first.
- Prefer simple action language over doctrine language. If the rule is simple,
  write the simple rule.
- Say `Only AGENTS.md changed, so I didn't run tests.` when that is the truth.

## Docs Map

- `README.md` for install targets, supported tools, and the current skill
  inventory.
- `CLAUDE.md` as a thin Claude Code shim that imports `AGENTS.md`; do not
  duplicate repo rules there.
- `docs/arch_skill_usage_guide.md` for workflow selection and intended usage.
- `skills/<slug>/SKILL.md` for the runtime contract of a specific shipped
  skill.
