# AGENTS.md

This repo ships installable agent skills. `skills/` is the main live runtime
surface. `Makefile` may also install explicitly listed vendored skills from
`vendor/`; `Makefile` plus `README.md` own the install surface for Codex,
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
  helper scripts, and runtime output instead; use `npx skills check` plus
  review for doctrine quality.
- Keep changes in the smallest owning surface: reusable workflow doctrine in
  `skills/`, install behavior and stale-surface cleanup in `Makefile`, and
  deeper reference material in `docs/`.

## Skill Routing

- For any skill that creates or resumes model agents, apply
  `skills/_shared/agent-orchestration-policy.md`: prefer the active host's
  native child for ordinary same-host work, choose starting context and
  continuation explicitly, and use an external process when its concrete
  provider, model, lifecycle, isolation, automation, or receipt benefit is
  worth the added cost. This is a reasoned preference, not a ban or threshold.
- Use `$skill-authoring` for new, edited, refactored, or audited skill
  packages.
- Use `$agents-md-authoring` for `AGENTS.md` authoring or refactors.
- Use `$figma-best-practices` when the user wants Figma file-craft,
  component-library, variables/token, Dev Mode, Code Connect, Make, Sites,
  Buzz, Slides, or MCP-readiness guidance.
- Use `$fal-ai-tools` when the user wants to use fal.ai tools, models, MCP,
  SDK/API calls, background removal, media generation or editing, model
  discovery, schema lookup, pricing, upload, inference, or result polling.
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
  (named in another repo's doctrine) with a new clean worker per step, a new
  clean critic, and exact-worker resume on fail. Same-host roles normally use
  native children; deliberate external roles use the external adapter lane.
- Use `$arch-epic` when the user has a goal too big for one `$arch-step` plan
  and wants to decompose it into ordered sub-plans, approve the decomposition
  up front, run each sub-plan through arch-step's `new` → `auto-plan` →
  `implement-loop` → `audit-implementation` arc, and have a new clean critic check
  for scope drift between sub-plans before advancing. Resolve each role under
  the shared agent policy rather than assuming every role is a subprocess.
- Use `$skill-flow` when the user wants to design, repair, or audit an ordered
  flow of multiple agent skills with distinct jobs, concrete handoffs, and
  clear peer boundaries. For 30+ skill suites or any multi-skill audit driven
  by a scope phrase (e.g. "audit every skill in this project", "audit the
  skills for flow F1"), the DAG-grounded audit sub-mode walks the suite in
  clean native subagents with parent-owned fanout, builds a labeled-edge substrate at
  `<doc-dir>/<doc-slug>_DAG.md`, and surfaces wasted-energy patterns
  (over-promotion, redundancy, dead skills, broken refs) with `path:line`
  evidence.
- Use `$fresh-consult` when the user or another skill wants one or more
  clean independent second opinions on a concrete artifact, completion claim,
  flow consistency question, or readability/confusion check. Use a clean
  same-host native child when capable; use its external lane for another
  provider, an unavailable exact model/profile, or another concrete benefit.
- Use `$commit-history-authoring` when the user wants the current branch's
  local-only commit messages rewritten into informative history while
  preserving patches and commit boundaries by default.
- Use `$agent-delegate` when the user explicitly wants an external Claude,
  Codex, Cursor Agent, or Grok worker/session, or when an external provider,
  exact model/profile, durable session, isolation, automation, or receipt is
  the concrete benefit. Ordinary same-host delegated work should use native
  children directly under the shared policy.
- Use `$codex-babysit` when the user wants to monitor, babysit, or keep alive
  an already-running Codex goal-mode tmux session across real usage limits,
  account rotations, restarts, and same-session resumes. It is not for
  launching a new worker or doing delegated work.
- Use `$codex-review-yolo` only for the exact external Codex `-p yolo` profile
  and captured receipt contract. Use a clean native child for an ordinary
  same-host Codex review.
- Use `$pr-review-followthrough` when the user explicitly wants an already-open
  GitHub PR polled, review comments handled and replied to, same-branch fixes
  pushed, and the loop continued until merge-ready; use `$pr-authoring` for
  drafting, opening, or publishing a PR.
- Use `$plan-audit` when the user wants an existing planning artifact in any
  format audited before work starts for plan quality, outcome clarity, real
  ambiguity, constraints, repo/code truth, depth-first risk, side doors,
  required deletes, drift-proofing, or proof gaps; or when they want code
  already written for a plan reviewed against that plan's architecture and
  code-quality bar. Its `implementation-audit` mode is plan-backed code review
  only: it does not run tests, ask for logs, prove CI, investigate honesty, or
  replace ordinary diff or PR review.
- Use `$cynical-code-review` when the user wants a skeptical,
  implementation-integrity audit of implemented code, a diff, branch, path set,
  completion claim, or optional plan-backed implementation and explicitly
  wants the review to assume the completion story may be misleading. It hunts
  for name-only completion, split-brain owners, side doors, partial
  unification, stale authority paths, stopped-short user workflows, overbuilt
  machinery, scope contamination, fake proof receipts, and docs/status/tests
  that mask broken code. Use `$exhaustive-code-review` instead when coverage
  itself is the deliverable.
- Use `$cynical-architecture-review` when the user wants a skeptical,
  subtraction-first architecture review of a branch, diff, subsystem,
  plan-backed implementation, or code area and explicitly wants the review to
  assume the architecture may have emerged accidentally through iteration. It
  hunts sprawl, invalid split ownership, duplicate truth, accidental
  abstractions, compatibility shims, flags-as-architecture, registries,
  adapters, state spread, wrong decomposition, and complexity not forced by the
  intended UX or hard experiment requirements. It is not for QA/test/doc review
  unless those surfaces expose architecture truth or the user asks.
- Use `$cynical-cruft-removal` when the user wants a skeptical cleanup review
  of a repo, branch, diff, subsystem, test suite, dependency set, generated
  artifacts, or docs/examples/prompt surface and wants a deep report of
  low-value items that should go away. It assumes references are not proof of
  value and hunts dead code, self-referential islands, retired V1/V2 paths,
  stale feature flags, worthless tests, fake coverage, unused dependencies,
  obsolete configs/scripts, stale generated artifacts, and point-in-time docs
  or examples that no longer serve a live purpose. It is not for ordinary code
  review, architecture review, docs-only cleanup, QA/test coverage review,
  implementation, automated deletion, or proof harnesses.
- Use `$plan-implement` when the user wants to implement an existing plan,
  phase, section, checklist, issue-body plan, or design doc while keeping the
  plan, plan-audit log, implementation log, proof freshness, and warm
  plan-backed review aligned. It is the lightweight implementation lane: use
  native subagents when helpful, and do not manually spawn `codex`, `claude`,
  `agent`, or `grok` executables for ordinary acceleration. Route a deliberate
  external worker or conductor through `$agent-delegate` or
  `$plan-conductor` under the shared policy.
- Use `$plan-conductor` when the user wants an entire existing plan document
  (or an explicit phase range) driven to verified completion by delegated
  workers while the parent agent stays the
  architect and cynical reviewer: it extracts the plan into a conductor log,
  gives phase-sized slices to clean same-host native children when capable or
  to deliberate external sessions through `$agent-delegate`, parallelizes only
  naturally independent slices, audits every diff assuming workers cut
  corners, resumes the exact worker with batched findings until exit criteria
  are true in code, and closes with a new clean whole-plan audit plus optional
  cold verifier. The explicit Terra preset remains an external exact-model
  lane. The parent never writes plans or implements code.
- Use `$model-consensus` when the user wants two selected Claude, Codex,
  Cursor Agent, or Grok models to iterate on a plan, architecture, design, or
  concept until they converge or expose the smallest unresolved decision, including
  adversarial simplification. Resolve transport separately for each participant,
  keep each participant's exact continuation, and let the parent relay; do not
  introduce a deterministic runner, script, controller, or harness layer.
- Use `$thermo-nuclear-code-quality-review` only when the user explicitly wants
  a thermonuclear, code-judo, or especially harsh maintainability review.
  Handle ordinary code review requests with the normal review response unless
  the user names a specific review skill.

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
