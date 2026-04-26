# Epic doc contract

The epic doc is the single on-disk artifact the skill reads and writes.
It is NOT an arch-step plan doc — it does not have Sections 0–10, no
call-site audit, no Section 7 checklist. It is an orchestration
document: an index of sub-plan DOC_PATHs, inter-plan gates, and an
append-only log of decisions and status changes.

Each sub-plan has its own full canonical arch-step DOC_PATH. The epic
doc points at those paths; it does not duplicate their contents.

## Location and naming

Default path: `docs/EPIC_<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`.
Example: `docs/EPIC_ADMIN_DASHBOARD_SSO_2026-04-22.md`.

The skill proposes this at `start` mode. If the user names a different
path in their invocation, use theirs verbatim. Silence means proceed
with the proposed path.

The epic doc lives in the orchestrator repo's `docs/` directory by
convention, alongside arch-step plan docs. Nothing in the shape is
repo-specific; it is just where the user expects architectural docs.

## Frontmatter

```yaml
---
title: Epic — <user's goal in plain English>
date: 2026-04-22
doc_type: epic
status: draft | active | complete | halted
raw_goal: |
  <verbatim user input that created this epic — every word, no edits>
raw_goal_sha256: <hex digest of the raw_goal string>
sub_plans_approved: false
critic_runtime: null | claude | codex
critic_model: null | <resolved CLI model, e.g. claude-opus-4-7>
critic_effort: null | <low | medium | high | xhigh | max>
models_sha256: null | <hex digest of {runtime, model, effort} tuple>
auto_execution: null | <automatic-mode policy block>
---
```

Frontmatter rules:

- `raw_goal` is the literal user invocation. Every word. If you
  normalize whitespace or rewrite, the hash breaks and the skill
  treats the doc as mutated.
- `raw_goal_sha256` is computed over `raw_goal` exactly. Recomputed
  on every `arch-epic` invocation. Mismatch means the user edited
  the goal mid-stream — the skill prints a loud error and asks
  whether to start a new epic or accept the change (clearing the
  decomposition-approved flag).
- `doc_type: epic` is the discriminator that distinguishes this
  artifact from an arch-step plan doc. Other tools may key on this.
- `status` transitions: `draft` → `active` (after decomposition
  approval) → (optionally) `halted` (on scope-change yield) →
  `active` (on user decision) → `complete` (all sub-plans pass).
- `sub_plans_approved` starts `false`. Flips to `true` exactly once:
  when the user approves the decomposition. If the user adjusts the
  decomposition after approval, the skill appends to the log and
  keeps `sub_plans_approved: true`; "approved" means "the user has
  seen and blessed the shape," not "the decomposition is frozen."
- `critic_runtime`, `critic_model`, `critic_effort` are user-supplied
  per `model-and-effort.md` for interactive-mode completion critics.
  They are not defaulted. `critic_model` stores the resolved runnable
  identifier, not raw shorthand. When the user explicitly asked for
  automatic end-to-end execution, these fields may stay `null` until an
  interactive critic is needed; automatic-mode critics use the
  `auto_execution.roles.critic` block instead.
- `models_sha256` is computed over the runtime/model/effort tuple when
  that tuple is present. Changing any of them re-hashes. Past verdicts
  keep their old models recorded in their own artifacts.
- `auto_execution` is `null` until the user explicitly asks for
  automatic execution. Automatic mode fills it after decomposition
  approval and role-table resolution. Interactive mode ignores it.

### `auto_execution`

Automatic mode stores the role-based policy in both the epic doc and
the automatic run directory:

```yaml
auto_execution:
  schema_version: 1
  approval_policy: auto_after_decomposition
  poll_seconds: 180
  quiet_floor_seconds: 900
  stuck_floor_seconds: 1800
  max_runtime_seconds: 7200
  auto_run_dir: .arch_skill/arch-epic/auto/<epic-slug>/run-<ts>
  source_quotes:
    epic_planner: claude opus 4.7 xhigh
    implementation_worker: codex gpt 5.5 xhigh
    repair_worker: same as implementation_worker
    critic: codex gpt 5.5 xhigh
  roles:
    epic_planner:
      runtime: claude
      model: claude-opus-4-7
      effort: xhigh
      source: user_table
    implementation_worker:
      runtime: codex
      model: gpt-5.5
      effort: xhigh
      source: user_table
    repair_worker:
      runtime: codex
      model: gpt-5.5
      effort: xhigh
      source: same_as:implementation_worker
    critic:
      runtime: codex
      model: gpt-5.5
      effort: xhigh
      source: user_table
  execution_sha256: <hex digest of the normalized policy>
```

Rules:

- The user approves the decomposition before this block is written.
- `poll_seconds` defaults to `180`; do not use short polling loops while
  waiting for spawned harnesses.
- `quiet_floor_seconds` defaults to `900`. A live child with no stream
  activity before this floor is still running, not failed.
- `stuck_floor_seconds` defaults to `1800`. A live child with no stream
  activity beyond this floor becomes `needs_attention`; this is a diagnostic
  status, not an automatic termination command.
- `max_runtime_seconds` defaults to `7200` for automatic children unless the
  user pins a different policy.
- `auto_run_dir` is an operational pointer. It is added after the run
  directory exists and is not part of the `execution_sha256` input.
- Raw shorthand belongs in `source_quotes`; executable fields store
  runnable model IDs.
- Model resolution comes from `skills/_shared/model_resolution.py` and
  `references/model-and-effort.md`; exact versions are never silently
  substituted.
- Changing any role updates `execution_sha256`, appends a Decision Log
  entry, and affects only future child runs.

## Body sections

### TL;DR

One paragraph in plain English. The goal, why this decomposition,
what order, what happens if something surprises us. Write for a
reader who has never seen the goal before.

Example:

> Ship a new admin dashboard protected by SSO. Decomposed into three
> sub-plans: SSO support in the auth service, the dashboard itself,
> and user migration. Built in that order because the dashboard can
> only be tested against a live SSO endpoint, and migration is only
> safe once the dashboard works. If implementation reveals a new
> system we did not anticipate (e.g., audit logging), the skill will
> halt and ask whether to extend the current sub-plan or insert a new
> one.

### Decomposition

A numbered list of sub-plans. Each entry has:

- The sub-plan name in bold and a one-sentence description in plain
  English.
- `DOC_PATH:` the path to the sub-plan's canonical arch-step doc.
  Empty at decomposition time for sub-plans that have not been
  started yet (lazy planning). Filled in when the skill invokes
  `$arch-step new` for that sub-plan.
  When arch-epic assigns a path, use
  `docs/epic/<EPIC_SLUG_WITH_DATE>/PHASE_<NN>_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`.
  Derive `<EPIC_SLUG_WITH_DATE>` from the epic doc stem without the
  leading `EPIC_`; derive `<NN>` from the approved Decomposition order
  at assignment time. Preserve already-created DOC_PATHs. If a new
  sub-plan is inserted between existing numbered docs, use a sortable
  fractional slot such as `PHASE_01_5_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`
  instead of renaming existing docs or worklogs.
- `Gate to next:` the assertion that must be true before the next
  sub-plan starts planning. The last sub-plan has no `Gate to next`.
- `Status:` one of `pending | north-star-approved | planning |
  implementing | complete | scope-changed`.
- `Epic-critic verdict:` empty until the sub-plan reaches
  completion; then the verdict path (relative or absolute) for
  audit.
- In automatic mode, add `Auto-run status:` when useful. Keep it
  compact: current role, latest worker artifact, latest critic verdict,
  or `not started`. Do not copy child transcripts into the epic doc.

Example:

```markdown
# Decomposition

1. **Ship SSO in the auth service**: Add SAML/OIDC support to the
   existing email-password auth service.
   - DOC_PATH: docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_01_AUTH_SSO_2026-04-22.md
   - Gate to next: SSO login endpoint live in staging, returns a
     session token compatible with existing dashboard middleware.
   - Status: complete
   - Epic-critic verdict: .arch_skill/arch-epic/critics/auth-sso/
     verdict.json (pass)

2. **Build admin dashboard backed by SSO**: New internal dashboard
   that authenticates via the SSO flow from sub-plan 1.
   - DOC_PATH: docs/epic/ADMIN_DASHBOARD_SSO_2026-04-22/PHASE_02_ADMIN_DASHBOARD_2026-04-23.md
   - Gate to next: Admin dashboard live behind SSO for new users in
     staging.
   - Status: implementing
   - Epic-critic verdict: —

3. **Migrate existing admin users to SSO**: Cut over in-flight
   admins from email-password to SSO without session loss.
   - DOC_PATH: (not yet set)
   - Gate to next: (last sub-plan)
   - Status: pending
   - Epic-critic verdict: —
```

### Orchestration Log (append-only)

One line per significant event, prefixed with the ISO date. Written
by the skill, not the user. Examples of what goes here:

- Decomposition drafted and surfaced to user.
- User approved decomposition with adjustments: `<what changed>`.
- Sub-plan N invoked: `$arch-step new <DOC_PATH>`.
- Sub-plan N North Star approved by user.
- Sub-plan N auto-plan armed.
- Sub-plan N auto-plan completed (consistency-pass clean).
- Sub-plan N implement-loop armed.
- Sub-plan N implement-loop completed (arch-step audit COMPLETE).
- Epic critic run on sub-plan N: verdict=`<pass|scope_change|incomplete>`.
- Scope-change detected on sub-plan N: `<headline>`. Halted.
- User resolution on sub-plan N scope change: `<decision>`.
- Sub-plan N marked complete.
- Epic marked complete.

Never rewrite past entries. If an earlier entry was wrong, append a
correction; do not redact.

### Decision Log (append-only)

User-visible decisions about scope changes, punted items, renamed
sub-plans, reordered sub-plans. One entry per decision. Example:

```markdown
# Decision Log

- 2026-04-22 During sub-plan 1 (Ship SSO in the auth service)
  implementation, worklog surfaced that session token rotation needs
  a background job. Options presented: extend current sub-plan, new
  sub-plan. User chose: new sub-plan. Inserted as
  sub-plan 1.5 "Token rotation background job" between sub-plans 1
  and 2. Gate 1 → 1.5: rotation endpoint live. Gate 1.5 → 2: unchanged
  from original 1 → 2.
```

The Decision Log is the user-facing record of why the decomposition
looks the way it does after the fact. It should read like a
conversation history a month from now, not a machine log.

### Epic Requirement Coverage

Automatic-mode sub-plan DOC_PATHs must include an Epic Requirement
Coverage section, usually in Section 0 or immediately after it. The
coverage map classifies every meaningful raw-goal/decomposition
requirement as one of:

- owned by this sub-plan
- satisfied by a prior sub-plan
- assigned to a named later sub-plan

The epic doc does not duplicate the full coverage map. It points to the
sub-plan DOC_PATH and records only material coverage decisions in the
Decision Log.

Coverage is a scope-preservation map, not a scope-reduction tool. A
requirement from the raw goal, approved Decomposition, North Star, Section 7,
acceptance criteria, or verification obligations must never be classified as
out of scope by an automatic child. If it is not owned here, satisfied already,
or assigned to a named later sub-plan, the sub-plan is not ready.

## Mutation rules

The skill mutates the epic doc under these conditions only:

- `start` mode: creates the doc with initial frontmatter, TL;DR, and
  the drafted Decomposition. Orchestration Log gets one entry.
- `approve-decomposition` mode: applies adjustments, flips
  `sub_plans_approved: true`, sets `status: active`, appends to log.
- `run` mode: updates sub-plan Status fields, fills in DOC_PATH when
  `$arch-step new` runs, appends to log, writes critic verdict
  pointer under the sub-plan entry.
- `resume-scope-change` mode: inserts a new sub-plan or extends an
  existing one's scope to preserve approved requirements; always
  appends a Decision Log entry.
- `auto-run` mode: writes or updates `auto_execution`, writes compact
  Auto-run status fields, records role-policy changes, critic-gated
  repairs, and auto-inserted sub-plans. Full child artifacts stay in the
  automatic run directory.

The skill never edits `raw_goal` or `raw_goal_sha256` except at
`start`. If the user wants to edit the goal, they start a new epic;
the skill does not rewrite history in place.

## Validation on load

Every time the skill reads the epic doc, it validates:

1. Frontmatter parses as YAML with all required fields.
2. `raw_goal_sha256` matches a fresh hash of `raw_goal`.
3. If the interactive critic tuple is present, `models_sha256` matches
   a fresh hash of the runtime/model/effort tuple. If the tuple is
   pending/null, `models_sha256` is also null and the skill must ask
   before running an interactive completion critic.
4. If `auto_execution` is present, its role blocks contain
   `runtime`, `model`, `effort`, `source_quote` or source metadata, positive
   monitor fields (`poll_seconds`, `quiet_floor_seconds`,
   `stuck_floor_seconds`, `max_runtime_seconds`), and a matching
   `execution_sha256` computed over the normalized execution policy excluding
   `auto_run_dir`.
5. The Decomposition section is present and non-empty if
   `sub_plans_approved: true`.
6. Every sub-plan entry has a Status; Status is one of the allowed
   values; sub-plans whose Status is beyond `pending` have a
   DOC_PATH set.
7. Orchestration Log and Decision Log are present (may be empty at
   `start`, always present after).

Validation failure is a loud error. The skill tells the user exactly
what is wrong and asks them to fix it manually — the skill does not
auto-repair the artifact.
