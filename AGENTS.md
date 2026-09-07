# AGENTS.md

This repo ships installable agent skills. `skills/` is the main live runtime
surface. `Makefile` may also install explicitly listed vendored skills from
`vendor/`; `Makefile` plus `README.md` own the install surface for Codex,
Claude Code, and Gemini.

## Build And Verify

- After skill package changes under `skills/`, run `npx skills add . --list`.
- Use `make verify_install` only when you intentionally changed or want to
  validate the installed skill surface.
- If you change install behavior, also verify the affected paths and commands
  in `README.md` and `Makefile`.
- If you change only doctrine or docs, re-read the edited files and verify any
  commands or paths you added with `rg`. Do not imply that code verification
  ran when it did not.

## Code Review Graph

- `make crg-setup` installs the `code-review-graph` CLI and builds this repo's
  local structural graph. Normal skill installation does not rebuild it.
- Use the graph for unfamiliar-area orientation, multi-hop change impact, and
  duplicate-pattern searches. Use `rg` for one exact identifier.
- Each Git worktree owns its own graph. Never copy or share
  `.code-review-graph/` between worktrees.
- Project hooks start a complete build in the background when a checkout lacks
  `.code-review-graph/.baseline-v1.complete`. They run incremental updates only
  after that baseline exists. Run `make crg-setup` for a foreground repair.
- If CRG is unavailable, say so and continue with normal repository search.

## Definition Of Done

- The touched surface is internally consistent.
- Required verification for that surface ran, or the final reply says plainly
  why it did not.
- `README.md` or the relevant docs are updated when skill names, routing,
  or install behavior changed.
- New doctrine stays concise, command-first, and points to deeper truth
  instead of copying large reference text into always-on context.

## Red Lines

- Do not make external model consultation or delegation the automatic way to
  get parallelism or fresh context. Apply
  `skills/_shared/agent-orchestration-policy.md`: ordinarily use native
  same-host agents, and use an external process when its concrete
  model/profile/session/automation benefit is worth its lifecycle,
  integration, and shared-state cost.
- Do not delete user work, untracked files, or repo changes unless the user
  explicitly asks for that exact cleanup. If you are not sure whether a file
  came from your own run, leave it alone and ask.
- Treat changes outside your intentional edit scope as user-owned, even if they
  appear while you are working. Do not reverse-apply, restore, checkout, or
  "clean up" those files to tidy your diff. If a command rewrites unrelated
  tracked files, report the exact paths and ask before undoing them.
- Do not make shipped skills depend on archived command files at runtime.
- Do not revive archived command surfaces as part of the live runtime.
- Do not edit vendored plugin packages unless the task is explicitly updating
  that vendor source; route repo-specific install behavior through `Makefile`
  and docs instead.
- Skill doctrine must be self-contained. Do not explain it with historical
  backstory or the skill development process itself. The only exception is a
  coordinator skill whose job is to explain how other skills fit together.
- Skill authoring must preserve agent judgment. `skills/<slug>/SKILL.md` is
  the runtime contract and should tell the agent how to inspect context, choose
  actions, execute thoughtfully, and verify the result.
- Skills that create, resume, replace, or coordinate model agents must apply
  `skills/_shared/agent-orchestration-policy.md`. Keep the role-specific
  workflow in the owning skill; do not duplicate or contradict the shared
  native/external, context, continuation, isolation, topology, and return
  contract.
- Scripts in a skill may only be narrow helpers for deterministic mechanics
  such as command syntax, parsing, templating, validation, or API calls. Do not
  make a skill a thin wrapper around a script, runner, controller, or harness
  that owns the workflow or removes the agent's reasoning.
- Author skills as direct v1 agent guidance. Include only the requested
  workflow: the job, key context to inspect, expected output, and verification
  to run. Leave out invented checks, conditions, refusal paths, cross-checks,
  edge-case policy, and exception lists.
- Do not write unit tests that lock skill doctrine to exact wording. Avoid
  tests that read `skills/<slug>/SKILL.md`, skill reference docs, prompt
  doctrine, or usage docs only to assert phrase or regex presence/absence.
  Test deterministic behavior, schemas, package shape, install inventory,
  helper scripts, and runtime output instead; use `npx skills add . --list` plus
  review for doctrine quality.
- Keep changes in the smallest owning surface: reusable workflow doctrine in
  `skills/`, install behavior and stale-surface cleanup in `Makefile`, and
  deeper reference material in `docs/`.

## Skill Routing

- Default Codex to `gpt-6-astra` at `xhigh`. Redirect casual Sol references
  to that default; honor deliberate exact model and effort choices.
- Elective lifecycles, persistent loops, and specialist reviews run only when
  explicitly selected or required by binding task instructions. Ordinary bug
  fixes, features, plan implementation, and code review stay ordinary. Do not
  replace a declined skill with another elective workflow or pause to ask.
- A selected parent may load its necessary documented helpers within the
  user's scope. A handoff never overrides read-only or no-delegation limits.
  See `docs/arch_skill_usage_guide.md` for the available choices.
- Apply `skills/_shared/agent-orchestration-policy.md` before agent dispatch;
  it owns native/Prime/external behavior and task-resource cleanup.
- Use `$skill-authoring` for skill packages, `$agents-md-authoring` for
  AGENTS files, and `$prompt-authoring` for actual model-facing prompts.
- Use `$browseros` before BrowserOS calls; Codex CLI browser work uses only
  BrowserOS, existing windows, and background pages. Foreground changes need
  the user's explicit request.
- Use `$herdr` for requested live Herdr control and `$herdr-helper` for
  cross-session migration. Use `$agent-history` for past session evidence,
  never as the default for live status or streaming.
- Use `$figma-best-practices` for requested Figma file/library guidance and
  `$fal-ai-tools` for fal.ai model/API operations. Use `$cf-share` for
  authorized static artifact sharing, not product deployment.
- Use `$spreadsheet-formatting` for spreadsheet readability, layout, or
  formatting, not ordinary Markdown tables.
- Use `$readable-reports` when a report, status update, morning or weekly
  report, audit summary, delivery report, deck, sheet note, or status answer
  must be written or rewritten so a smart, busy expert can read it in one
  pass, or when the user says an artifact is confusing, dense, jargon-heavy,
  or a wall of text but must not be dumbed down. It owns the words, not the
  HTML theme, the spreadsheet grid, or the public-copy voice gate.

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
- `vendor/cursor/plugins/cursor-team-kit/` for the vendored MIT Cursor Team Kit
  package that supplies `thermo-nuclear-code-quality-review`.
