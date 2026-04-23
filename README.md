# arch_skill

This repo ships installable agent skills centered on the arch suite for Codex CLI, Claude Code, and Gemini CLI.

## Community

- License: [MIT](LICENSE)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Support: [SUPPORT.md](SUPPORT.md)

The live arch suite is:

- `arch-step` — the broad full-arch execution surface; owns the full staged workflow, extended helper passes, bounded `auto-plan`, full-frontier `implement-loop`, compact `status`, and guided `advance`
- `miniarch-step` — the trimmed full-arch surface; keeps canonical arch docs, phasing, and real auto controllers without the broader `arch-step` helper surface
- `arch-docs` — standalone docs-audit and cleanup skill; owns topic-first stale-doc cleanup, consolidation onto canonical docs, working-doc retirement, and hook-backed `auto` docs cleanup in Codex and Claude Code
- `arch-mini-plan` — one-pass canonical mini planning that hands follow-through to `miniarch-step` or `arch-step`
- `lilarch` — compact 1-3 phase feature flow
- `bugs-flow` — evidence-first bug analyze/fix/review flow
- `audit-loop` — exhaustive map-first repo audit loop with a root audit ledger, mandatory post-change self-audit, and hook-backed `auto` continuation in Codex and Claude Code
- `comment-loop` — exhaustive map-first repo comment hardening loop with a root comment ledger and hook-backed `auto` continuation in Codex and Claude Code
- `audit-loop-sim` — exhaustive map-first real-app automation audit loop with a root simulator ledger, mandatory post-change self-audit, and hook-backed `auto` continuation in Codex and Claude Code
- `goal-loop` — open-ended goal-seeking loop
- `north-star-investigation` — math-first investigation loop
- `arch-flow` — read-only "what's next?" router for arch docs
- `arch-skills-guide` — explains the suite and recommends the right live subskill

Use `miniarch-step` when the work still needs a real full-arch artifact and auto continuation, but you want the trimmed command surface instead of the broader `arch-step` helper surface. Use `arch-step` when the work is broader, more ambiguous, or needs the full helper surface.

Other shipped skills are:

- `arch-loop` — generic hook-backed completion loop for Codex and Claude Code that takes free-form requirements, optional named-skill audit obligations (e.g. `$agent-linter`), and optional runtime/cadence/iteration caps, then drives repeat turns through the installed `Stop` hook until a fresh unsandboxed Codex `gpt-5.4` `xhigh` external evaluator emits a `clean` or `blocked` verdict. Distinct from `delay-poll` (condition-polling only, no work done between checks) and from specialized loops like `audit-loop` (prescribed map-first audit flow).
- `delay-poll` — delay-and-check controller for Codex and Claude Code that waits inside the installed `Stop` hook, re-runs a read-only condition check on a fixed interval, and resumes the same thread when the condition becomes true
- `wait` — one-shot delay-then-resume controller for Codex and Claude Code that sleeps inside the installed `Stop` hook for a parsed duration (`30m`, `1h30m`, `90s`, `2d`) and then injects a literal resume prompt back into the same thread exactly once. Use this for plain "wait N and continue" work. For condition re-checking use `delay-poll`; for recurring or scheduled work use `/loop` or `schedule`.
- `agent-definition-auditor` — cold-reader scoring and findings for `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompts, and other agent-definition markdown
- `agents-md-authoring` — writes, edits, refactors, and audits concise repo-present `AGENTS.md` files
- `prompt-authoring` — writes, edits, refactors, and audits reusable prompt contracts
- `skill-authoring` — writes, edits, refactors, and audits reusable agent skill packages
- `amir-publish` — personal shortcut for publishing this skills repo across Amir's usual machines
- `codex-review-yolo` — external Codex `-p yolo` reviewer for substantial diffs, plans, docs, and completion claims
- `code-review` — deterministic general code-review skill that always shells out to fresh unsandboxed Codex `gpt-5.4` `xhigh` (with parallel `gpt-5.4-mini` `xhigh` review lenses) for diffs, branches, paths, or completion-claim audits; supports direct and hook-backed invocation, and keeps Codex as the reviewer even when Claude hosts the Stop hook
- `stepwise` — thoughtful orchestrator for ordered multi-step processes defined in another repo's doctrine; spawns a fresh Claude or Codex sub-session per step, runs an independent critic sub-session after each step, and resumes the same step's session with the critic's findings on fail (rather than redoing the work itself). Model and effort for step and critic are supplied by the user at invocation; both runtimes run dangerous / skip-permissions / no-sandbox. Distinct from `arch-loop` (requirement-satisfaction, not ordered steps), `arch-step` (plan-doc-backed full-arch), and `code-review` (one-shot review).
- `arch-epic` — multi-plan orchestrator that wraps `arch-step` for goals too big for a single canonical plan. Captures the goal, drafts a plain-English one-sentence-per-sub-plan decomposition with inter-plan gates, gets user approval, then drives each sub-plan through arch-step's `new` → `auto-plan` → `implement-loop` → `audit-implementation` arc. After each sub-plan completes a fresh Claude or Codex critic subprocess inspects the shipped work for scope drift against the approved North Star and flags must-have discoveries or silent scope changes. Progressive lazy planning: sub-plan N+1 is not planned until sub-plan N is complete and passes the critic. Resume is the only mode — any invocation re-reads the epic doc and arch-step state from disk and continues. User involvement is bounded to the goal, decomposition approval, per-sub-plan North Star (arch-step's existing gate), and scope-change decisions.

Examples in this repo use Codex `$skill` notation. In Claude Code, invoke the same skill as `/skill`.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

This installs the live skill surface to `~/.agents/skills/`, writes one arch_skill-managed Codex `Stop` hook in `~/.codex/hooks.json` pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, writes one arch_skill-managed Claude Code `Stop` hook plus one `SessionStart` hook in `~/.claude/settings.json` pointing at the same installed runner with `--runtime claude`, removes older `~/.codex/skills/<skill>` mirrors from previous installs, and also installs the Claude Code and Gemini CLI skill directories. Every loop-skill arm also reruns the same idempotent, flock-guarded `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` so the canonical hook entries cannot drift between runs. Drift is fail-loud at dispatch: any non-canonical group, missing `SessionStart` on Claude, or stale runner path makes the Stop hook exit 2 with the exact repair command rather than silently migrate.

Codex automatic `auto-plan`, `implement-loop`, `auto-implement`, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, `arch-loop`, `delay-poll`, and `wait` also require the Codex feature flag:

```bash
codex features enable codex_hooks
```

Claude Code uses the installed settings-level `Stop` hook and does not depend on the Codex feature flag. Claude controllers that need fresh child review or check passes launch hook-suppressed child runs with `claude -p --settings '{"disableAllHooks":true}'`, so that child path must work with the machine's normal Claude auth.

Hook-backed skills all follow the **arm first, disarm never** controller contract at `skills/_shared/controller-contract.md`. That document owns the state-file paths, the arm-time ensure-install rule, the dispatch-time loud verify, the session-scoped conflict gate, the staleness sweep, and the manual recovery procedure. Do not run the Stop hook yourself — arm the controller, end the turn, and let the installed runner own the rest.

For manual recovery when a controller wedges, see the shared contract's Manual recovery section, or run the shared runner's disarm flags directly:

```bash
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --list-controllers
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm <name> [--session <id>]
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --disarm-all --yes
~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --doctor
```

To skip Gemini:

```bash
make install NO_GEMINI=1
```

Installed skills:

- Default local path:
  - `~/.agents/skills/arch-step/`
  - `~/.agents/skills/miniarch-step/`
  - `~/.agents/skills/arch-docs/`
  - `~/.agents/skills/arch-mini-plan/`
  - `~/.agents/skills/lilarch/`
  - `~/.agents/skills/bugs-flow/`
  - `~/.agents/skills/audit-loop/`
  - `~/.agents/skills/comment-loop/`
  - `~/.agents/skills/audit-loop-sim/`
  - `~/.agents/skills/goal-loop/`
  - `~/.agents/skills/north-star-investigation/`
  - `~/.agents/skills/arch-flow/`
  - `~/.agents/skills/arch-skills-guide/`
  - `~/.agents/skills/arch-loop/`
  - `~/.agents/skills/delay-poll/`
  - `~/.agents/skills/wait/`
  - `~/.agents/skills/agent-definition-auditor/`
  - `~/.agents/skills/agents-md-authoring/`
  - `~/.agents/skills/prompt-authoring/`
  - `~/.agents/skills/skill-authoring/`
  - `~/.agents/skills/amir-publish/`
  - `~/.agents/skills/codex-review-yolo/`
  - `~/.agents/skills/code-review/`
  - `~/.agents/skills/stepwise/`
  - `~/.agents/skills/arch-epic/`
- Claude Code:
  - `~/.claude/skills/arch-step/`
  - `~/.claude/skills/miniarch-step/`
  - `~/.claude/skills/arch-docs/`
  - `~/.claude/skills/arch-mini-plan/`
  - `~/.claude/skills/lilarch/`
  - `~/.claude/skills/bugs-flow/`
  - `~/.claude/skills/audit-loop/`
  - `~/.claude/skills/comment-loop/`
  - `~/.claude/skills/audit-loop-sim/`
  - `~/.claude/skills/goal-loop/`
  - `~/.claude/skills/north-star-investigation/`
  - `~/.claude/skills/arch-flow/`
  - `~/.claude/skills/arch-skills-guide/`
  - `~/.claude/skills/arch-loop/`
  - `~/.claude/skills/delay-poll/`
  - `~/.claude/skills/wait/`
  - `~/.claude/skills/agent-definition-auditor/`
  - `~/.claude/skills/agents-md-authoring/`
  - `~/.claude/skills/prompt-authoring/`
  - `~/.claude/skills/skill-authoring/`
  - `~/.claude/skills/amir-publish/`
  - `~/.claude/skills/codex-review-yolo/`
  - `~/.claude/skills/code-review/`
  - `~/.claude/skills/stepwise/`
  - `~/.claude/skills/arch-epic/`
- Gemini CLI:
  - `~/.gemini/skills/arch-step/`
  - `~/.gemini/skills/miniarch-step/`
  - `~/.gemini/skills/arch-docs/`
  - `~/.gemini/skills/arch-mini-plan/`
  - `~/.gemini/skills/lilarch/`
  - `~/.gemini/skills/bugs-flow/`
  - `~/.gemini/skills/audit-loop/`
  - `~/.gemini/skills/comment-loop/`
  - `~/.gemini/skills/audit-loop-sim/`
  - `~/.gemini/skills/goal-loop/`
  - `~/.gemini/skills/north-star-investigation/`
  - `~/.gemini/skills/arch-flow/`
  - `~/.gemini/skills/arch-skills-guide/`
  - `~/.gemini/skills/agent-definition-auditor/`
  - `~/.gemini/skills/agents-md-authoring/`
  - `~/.gemini/skills/prompt-authoring/`
  - `~/.gemini/skills/skill-authoring/`
  - `~/.gemini/skills/amir-publish/`
  - `~/.gemini/skills/codex-review-yolo/`
  - `~/.gemini/skills/stepwise/`
  - `~/.gemini/skills/arch-epic/`

Codex reads the same installed skill surface from `~/.agents/skills/`. `make install` also removes stale pre-skill command surfaces, removed skill packages, and older `~/.codex/skills/<skill>` mirrors so runtime routing stays unambiguous.

`arch-loop`, `delay-poll`, and `wait` are installed on Codex and Claude Code because both runtimes have a native `Stop` hook surface; all three are omitted from Gemini because Gemini still has no hook-backed auto-controller surface and there is no way for the parsed duration, condition re-check, or evaluator-backed verdict to resume the same thread there. `arch-loop` evaluator turns additionally always shell out to fresh unsandboxed Codex `gpt-5.4` `xhigh` for the external verdict; the Claude host can arm and drive the loop, but the evaluator subprocess itself is always Codex, mirroring the `code-review` exception below. `code-review` is installed on the agents/Codex and Claude Code surfaces only; the Claude host can trigger the skill, but the actual review subprocess always shells out to fresh Codex.

### Remote install

```bash
make remote_install HOST=user@host
```

### Verify

```bash
make verify_install
```

This validates the installed active skill surface in `~/.agents/skills/`, checks that exactly one arch_skill-managed Codex `Stop` hook exists in `~/.codex/hooks.json` and points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`, checks that exactly one arch_skill-managed Claude Code `Stop` hook plus one `SessionStart` hook exist in `~/.claude/settings.json` and point at the same installed runner with `--runtime claude`, confirms the old `~/.codex/skills/<skill>` mirrors are absent, and confirms removed skill packages are absent for the supported runtimes. The Stop hook itself also re-runs the same verify on every dispatch and exits 2 with the exact repair command if it finds drift — there is no silent migration, no legacy fallback, no transitional shim.

To confirm the Codex feature gate is enabled:

```bash
codex features list | rg '^codex_hooks\\s+.*\\strue$'
```

Restart your Codex, Claude Code, or Gemini CLI session after install so it reloads skills.

## Shipped skills

### `arch-step`

Use `arch-step` for broad or ambiguity-heavy full-arch work. It owns the standalone full-arch workflow, including:

- `new`
- `reformat`
- `research`
- `deep-dive`
- `external-research`
- `phase-plan`
- `auto-plan`
- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `consistency-pass`
- `review-gate`
- `implement`
- `implement-loop`
- `auto-implement`
- `audit-implementation`
- `status`
- `advance`

`consistency-pass` is the optional end-to-end cold-read helper before implementation. In Codex it uses two parallel cold reads; `auto-plan` runs it automatically after `phase-plan`. When it runs, `Decision: proceed to implement? yes` is only legal if the artifact is decision-complete and has no unresolved plan-shaping decisions left.

`auto-plan` is the automatic planning controller in Codex and Claude Code. The user-facing command is still just `$arch-step auto-plan` in Codex or `/arch-step auto-plan` in Claude Code, with an optional `docs/MY_PLAN.md` argument. `DOC_PATH` is always the planning ledger. The armed controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent `auto-plan` pass runs only `research`, then ends its turn. On reruns, the installed Stop hook reads the doc and resumes from the first incomplete stage through `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`, then owns the successful `implement-loop` handoff. That handoff is allowed only when the artifact is decision-complete. If any unresolved plan-shaping decision remains, `auto-plan` must stop and ask the user the exact blocker question; the Stop hook clears controller state. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). If `--ensure-installed` fails loud, repair the named prerequisite and rerun.

`arch-step` does not have authority to silently cut approved behavior, acceptance criteria, or required implementation work because the agent wants to narrow scope on its own. If repo evidence cannot settle a plan-shaping choice, the skill must ask the user instead of guessing.

Before Section 7 is allowed to harden, `arch-step` should inspect adjacent surfaces tied to the same contract family, source of truth, migration boundary, or parity story, such as sibling formats, readers/writers, examples, fixtures, mirrored config, generated artifacts, or live docs. It should either include those surfaces now, explicitly defer or exclude them, or ask one exact blocker question instead of silently leaving them contradictory.

Compatibility posture is separate from `fallback_policy`. The plan should say whether it preserves the existing contract, performs a clean cutover, or uses an explicitly approved timeboxed bridge. `arch-step` should not assume backward compatibility by default just because it feels safer.

Section 7 phase plans should split work into one coherent self-contained unit per phase, with the most fundamental units first and later phases clearly building on earlier ones. When two decompositions are both valid, prefer more, smaller phases than fewer blended phases. New phase plans should use an explicit `Checklist (must all be done)` plus `Exit criteria (all required)` so a phase cannot be called complete while planned obligations are still implicit.

`implement-loop` is the automatic full-frontier delivery controller in Codex and Claude Code. `auto-implement` is an exact user-facing synonym for the same controller. The user-facing command is `$arch-step implement-loop docs/MY_PLAN.md` or `$arch-step auto-implement docs/MY_PLAN.md` in Codex, and the same `/arch-step ...` command in Claude Code. It arms loop state before implementation work, then runs the full approved Section 7 frontier in order from the earliest incomplete or reopened phase through later reachable phases before handing control to fresh audit. The controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). Claude fresh-audit cycles additionally require working hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'`.

If the user says "do the full arch flow," "continue this architecture doc," or "audit implementation against the plan," the right live skill is `arch-step`.

### `miniarch-step`

Use `miniarch-step` when the work still needs a canonical full-arch doc, phased execution, and real auto controllers in Codex or Claude Code, but does not need `arch-step`'s broader staged helper surface. It keeps the trimmed command surface without changing the full-work posture.

It keeps the same full-arch artifact shape and the same clean-audit handoff to `arch-docs`, but with a shorter command surface:

- `new`
- `reformat`
- `research`
- `deep-dive`
- `phase-plan`
- `auto-plan`
- `implement`
- `implement-loop`
- `auto-implement`
- `audit-implementation`
- `status`
- `advance`

`miniarch-step auto-plan` is the planning controller for the trimmed full-arch surface in Codex and Claude Code. `DOC_PATH` is the planning ledger and the armed controller state lives under `.codex/` in Codex and under `.claude/arch_skill/` in Claude Code. On a fresh doc, the parent pass runs only `research`, then ends its turn. On reruns, the installed Stop hook resumes from the first incomplete stage through `deep-dive` and `phase-plan`, then owns the successful `implement-loop` handoff.

`miniarch-step implement-loop` and `miniarch-step auto-implement` share the same full-frontier delivery controller. They arm runtime-local controller state under `.codex/` in Codex or `.claude/arch_skill/` in Claude Code, implement the full approved remaining frontier, and let fresh `audit-implementation` decide whether the loop is clean or more work remains. In Codex, that fresh miniarch audit child runs with `gpt-5.4-mini` at `xhigh` reasoning effort.

Use `miniarch-step` when the work needs full-arch execution but does not need `arch-step`'s broader helper surface.

### `arch-docs`

Use when the job is leaving repo docs healthier: cleaning up stale, overlapping, misleading, or obviously dated docs, updating stale survivors, clarifying confusing docs, and promoting grounded missing truth into evergreen docs. It works in any repo and, after full-arch work, uses the plan/worklog as narrowing context instead of as the whole scope.

With no extra mode, `arch-docs` runs one grounded DGTFO docs-health pass: orient to the repo's doc system, inventory doc-shaped surfaces, group them by topic, ground those topics against code, use git history when staleness or datedness matters, consolidate each topic to one canonical home, update stale surviving docs, clarify confusing docs, and add grounded missing docs when the canonical result is either a standard public-repo doc or a differentiated evergreen doc that deserves its own home. Repo posture is evidence-based: default to `private/internal` when unclear, but in `public OSS` repos treat `README`, `LICENSE*`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `SUPPORT.md` as expected standalone docs. Then delete stale, duplicate, or dated one-off truth and repair links or nav for the surviving docs.

`arch-docs auto` is the hook-backed controller for repeated docs-cleanup passes in Codex and Claude Code. The user-facing command is still just `$arch-docs auto` in Codex or `/arch-docs auto` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude).

For any of these supported auto controllers, do not run the Stop hook yourself. After the controller is armed, just end the turn and let the installed Stop hook run.

### `arch-mini-plan`

Use when the task still needs canonical arch blocks, but the planning should be done in one pass and follow-through should happen later via `miniarch-step` or `arch-step`, then `arch-docs` for later docs cleanup.

### `lilarch`

Use for contained features or improvements that should fit in 1-3 phases.

### `bugs-flow`

Use for Sentry/log-driven bug analysis, narrow fixes, and explicit-review-only follow-up.

### `audit-loop`

Use for repo-wide audit passes where the agent should exhaustively map the codebase and current proof surface before editing, then rank and attack the biggest real unresolved risks by consequence instead of picking something convenient. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

### `comment-loop`

Use for repo-wide code comment hardening passes where the agent should exhaustively map the repo, current proof surface, and current explanatory coverage before editing, then rank and attack the biggest shared explanation gaps around contracts, conventions, gotchas, and subtle behavior instead of writing narration wherever it feels helpful.

### `audit-loop-sim`

Use for repo-wide real-app automation passes where the agent should exhaustively map the app, journeys, and current automation surface before editing, then rank and attack the biggest unresolved automation risks by consequence instead of cashing out on tiny safe test tweaks. Every editful pass must then audit its own diff for safety, downstream consequences, elegance, and duplication before it can count as done.

### `arch-loop`

Use when the user wants Codex or Claude Code to drive a generic hook-backed completion loop: free-form requirements go in, optional named-skill audit obligations (e.g. `$agent-linter`, `$code-review`) and optional runtime/cadence/iteration caps, and the loop runs repeat parent turns through the installed `Stop` hook until an external Codex evaluator returns `clean` or `blocked`. Every evaluator turn always shells out to a fresh unsandboxed Codex `gpt-5.4` `xhigh` subprocess — even when Claude hosts the Stop hook — and the evaluator's structured verdict is the only thing that can stop the loop. Continue verdicts choose between `parent_work` (run another implementation turn now) and `wait_recheck` (sleep `cadence_seconds` inside the hook, then re-run the evaluator without spending a parent turn). Controller state lives under `.codex/arch-loop-state.<SESSION_ID>.json` in Codex and under `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json` in Claude Code. Every arm runs `arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>` first; the installer is idempotent and flock-guarded and writes the canonical `Stop` entry (and the `SessionStart` entry on Claude). Distinct from `delay-poll` (condition-polling only, no work done between checks) and from specialized loops like `audit-loop` / `comment-loop` / `audit-loop-sim` (prescribed map-first flows with their own artifact contracts).

### `delay-poll`

Use when the user wants Codex or Claude Code to wait on some external condition, re-check it every 30 minutes, every hour, or similar, and continue the same visible thread only after that condition becomes true.

### `wait`

Use when the user wants Codex or Claude Code to sleep a specific parsed duration (`30m`, `1h30m`, `90s`, `2d`) and then continue the same visible thread with a literal follow-up prompt exactly once. No polling, no re-checking, no fresh child run during the wait. For condition re-checking use `delay-poll`; for recurring or scheduled work use `/loop` or `schedule`.

### `goal-loop`

Use when the goal is clear but the path is not, and you want a controller doc plus append-only iteration log.

### `north-star-investigation`

Use for quantified investigations where ranked hypotheses and brutal tests are the main job.

### `arch-flow`

Use when the question is "what's next?" on an arch-style doc and you want the single best read-only recommendation.

### `arch-skills-guide`

Use when the question is "which arch skill should I use?" or "what is the difference between these live subskills?"

### `agent-definition-auditor`

Use when the user wants a cold-read score, rationale, and prioritized improvements for an `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SOUL.md`, system prompt, or other agent-definition markdown.

### `agents-md-authoring`

Use when the user wants to write, edit, refactor, or audit a repo-root or path-local `AGENTS.md` so it stays command-first, scope-aware, and about current repo truth only.

### `prompt-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable prompt contract so it stays intent-driven, section-correct, and anti-heuristic.

### `skill-authoring`

Use when the user wants to write, edit, refactor, or audit a reusable agent skill package with precise triggers, lean packaging, and self-contained references.

### `amir-publish`

Use when Amir wants to publish this skills repo across his usual machines: commit and push the current local work, install locally, then SSH to the fixed host list, skip the current host, pull the same branch from the same directory, and install remotely.

### `code-review`

Use when the user wants a real, deterministic code review against a diff, branch, path set, or "is this plan phase actually complete?" completion-claim. The skill does not review with the caller model. Every review subprocess is a fresh unsandboxed Codex process at `gpt-5.4` `xhigh` for the final synthesis, with parallel `gpt-5.4-mini` `xhigh` Codex subprocesses for per-lens review coverage (`correctness`, `architecture`, `proof`, `docs-drift`, `security`, and a conditional `agent-linter` lens when the change touches agent-building or instruction-bearing surfaces). The runner writes a namespaced artifact tree under `/tmp/code-review/...` (or a caller-supplied `--output-root`) that includes per-lens prompts, stream logs, final outputs, and a single synthesized `ReviewVerdict`.

Direct invocation runs the runner as a one-shot command. The skill also wires into the shared `arch-step` Stop-hook dispatcher so Codex and Claude Code can trigger the same runner via `.codex/code-review-state.<SESSION_ID>.json` or `.claude/arch_skill/code-review-state.<SESSION_ID>.json`. The Claude-host path is an intentional exception to the broader native-auto-loop direction: the Stop hook runs under Claude, but the review subprocess itself must always be Codex. Generic Claude auto-controllers stay Claude-native; `code-review` does not. `code-review` is review-only — it never edits the reviewed repo and never writes a "suggested patch" block.

Use `code-review` when the user wants an automated finding-set with explicit coverage guarantees. Use `codex-review-yolo` when the user wants a narrower, more interactive `-p yolo` fresh-eyes consult on a specific artifact.

## Usage

- Primary surface: ask the agent to use `arch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `arch-loop`, `delay-poll`, `wait`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `skill-authoring`, `amir-publish`, `code-review`, or `codex-review-yolo`.
- Full-arch execution defaults to `miniarch-step` when the trimmed command surface is enough and `arch-step` when the broader or helper-heavy surface is needed.
- Docs cleanup loops default to `arch-docs`.
- Read-only checklist and next-step inspection uses `arch-flow`.

Examples:

- `Use $arch-step "do the full arch flow for this change"`
- `Use $arch-step new "build this"`
- `Use $arch-step advance docs/MY_PLAN.md`
- `Use $arch-step advance docs/MY_PLAN.md RUN=1`
- `Use $arch-step auto-plan`
- `Use $arch-step consistency-pass docs/MY_PLAN.md`
- `Use $arch-step implement-loop docs/MY_PLAN.md`
- `Use $arch-step auto-implement docs/MY_PLAN.md`
- `Use $miniarch-step for this feature`
- `Use $miniarch-step auto-plan`
- `Use $miniarch-step implement-loop docs/MY_PLAN.md`
- `Use $miniarch-step auto-implement docs/MY_PLAN.md`
- `Use $arch-docs`
- `Use $arch-docs auto`
- `Use $arch-mini-plan docs/MY_PLAN.md`
- `Use $lilarch for this small feature`
- `Use $bugs-flow on this Sentry issue`
- `Use $audit-loop`
- `Use $audit-loop review`
- `Use $audit-loop auto`
- `Use $comment-loop`
- `Use $comment-loop review`
- `Use $comment-loop auto`
- `Use $audit-loop-sim`
- `Use $audit-loop-sim review`
- `Use $audit-loop-sim auto`
- `Use $arch-loop tighten the onboarding copy across the marketing site until it reads cleanly on mobile`
- `Use $arch-loop rewrite this AGENTS.md file with $agent-linter as a required clean audit`
- `Use $arch-loop every 30 minutes check whether staging.api.internal is reachable and keep fixing infra until it is, max 8 hours`
- `Use $delay-poll every 30 minutes check whether branch blah has been fully pushed; when it is, pull it and integrate it in`
- `Use $wait 1h30m then continue investigating the flaky test`
- `Use $goal-loop for this metric problem`
- `Use $north-star-investigation for this quantified performance hunt`
- `Use $arch-flow docs/MY_PLAN.md`
- `Use $arch-skills-guide for this request`
- `Use $agent-definition-auditor to audit this AGENTS.md`
- `Use $agents-md-authoring to tighten this AGENTS.md`
- `Use $prompt-authoring to refactor this prompt`
- `Use $skill-authoring to audit this skill package`
- `Use $amir-publish`
- `Use $code-review on the uncommitted diff`
- `Use $code-review branch-diff --base main --head feature/ingest-fix`
- `Use $code-review paths src/ingest/pipeline.py src/ingest/schema.py`
- `Use $code-review completion-claim docs/MY_PLAN.md 3`
