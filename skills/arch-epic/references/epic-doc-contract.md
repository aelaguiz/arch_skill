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
critic_runtime: null | claude | codex | grok  # legacy/external critic only
critic_model: null | <resolved external CLI model, e.g. claude-fable-5>
critic_effort: null | <low | medium | high | xhigh | max>
models_sha256: null | <hex digest of external {runtime, model, effort} tuple>
auto_execution: null | <explicit external-harness policy block>
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
  seen and blessed the shape." The approved decomposition is the epic scope
  baseline. Later agents may reorder execution inside that shape when allowed,
  but adding a sub-plan or outcome requires explicit human approval.
- `critic_runtime`, `critic_model`, and `critic_effort` describe only a
  deliberately selected external completion critic. A capable same-host native
  critic leaves them null and records its clean child handle in the
  Orchestration Log. For an external critic, values are user-supplied per
  `model-and-effort.md`, except an omitted Codex model defaults to
  `gpt-5.6-sol`; store the resolved runnable identifier, not raw shorthand.
  During same-session `auto-plan` these fields may stay null because no critic
  runs. External-harness critics use `auto_execution.roles.critic`.
- `models_sha256` is computed over the runtime/model/effort tuple when
  that tuple is present. Changing any of them re-hashes. Past verdicts
  keep their old models recorded in their own artifacts.
- `auto_execution` is `null` unless the explicit external harness is selected.
  That lane fills it after decomposition approval and external role-table
  resolution. Native role execution uses compact Orchestration Log handle
  receipts rather than pretending this external policy block applies.

### `auto_execution` (external harness only)

External-harness mode stores the role-based policy in both the epic doc and its
run directory:

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
    epic_planner: claude fable 5 high
    implementation_worker: codex gpt-5.6-sol xhigh
    critic: codex gpt-5.6-sol xhigh
  roles:
    epic_planner:
      runtime: claude
      model: claude-fable-5
      effort: xhigh
      source: user_table
    implementation_worker:
      runtime: codex
      model: gpt-5.6-sol
      effort: xhigh
      source: user_table
    critic:
      runtime: codex
      model: gpt-5.6-sol
      effort: xhigh
      source: user_table
  execution_sha256: <hex digest of the normalized policy>
```

Rules:

- The user approves the decomposition before this block is written.
- `poll_seconds` defaults to `180`; do not use short polling loops while
  waiting for external harness processes.
- `quiet_floor_seconds` defaults to `900`. A live child with no stream
  activity before this floor is still running, not failed.
- `stuck_floor_seconds` defaults to `1800`. A live child with no stream
  activity beyond this floor becomes `needs_attention`; this is a diagnostic
  status, not an automatic termination command.
- `max_runtime_seconds` defaults to `7200` for external children unless the
  user pins a different policy.
- `auto_run_dir` is an operational pointer. It is added after the run
  directory exists and is not part of the `execution_sha256` input.
- Raw shorthand belongs in `source_quotes`; executable fields store
  runnable model IDs.
- Model resolution comes from `../../_shared/model_resolution.py` and
  `references/model-and-effort.md`; exact versions are never silently
  substituted.
- New external-harness policies require `epic_planner`, `implementation_worker`, and
  `critic`. Older docs may include a legacy `repair_worker`; keep it readable,
  but ordinary critic failures resume the exact original planner or
  implementation worker session instead of using a separate repair role.
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
> one, or keep the frozen scope and subtract/redesign the surprise.

### Decomposition

A numbered list of sub-plans. Each entry has:

- The sub-plan name in bold and a one-sentence description in plain
  English.
- `DOC_PATH:` the path to the sub-plan's canonical arch-step doc.
  Empty at decomposition time for sub-plans that have not been
  started yet (lazy planning). Filled in when the skill invokes
  `$arch-step new` for that sub-plan or when same-session `auto-plan`
  assigns the grouped path before creating the sub-plan doc.
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
  planned | implementing | complete | scope-changed`.
  In same-session `auto-plan`, `planned` means the exact sub-plan DOC_PATH
  passed `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc
  <DOC_PATH>` after real generated ArcStep auto-plan receipts. A created doc,
  repaired scaffold, consistency-pass marker, copied Section 3-7 content, or
  stored prior Status is not enough.
- `Epic-critic verdict:` empty until the sub-plan reaches
  completion; then the verdict path (relative or absolute) for
  audit.
- `Scope contract:` the Section 0 anchor in the sub-plan DOC_PATH and its
  freeze state (`pending | frozen | human-decision-needed`). This is a pointer,
  not a copy of the sub-plan contract.
- In role-based automatic mode, add `Auto-run status:` when useful. Keep it
  compact: transport, exact role handle or latest worker artifact, latest
  critic verdict, or `not started`. Do not copy child transcripts into the
  epic doc.

The decomposition count follows proof boundaries, not a preferred range.
Each sub-plan should prove a state later sub-plans can rely on. The first
sub-plan should usually make one real piece of the final system work
through the highest-risk owner path; later sub-plans expand along named
axes. If a requirement is intentionally not owned by the current sub-plan,
the decomposition or Epic Requirement Coverage must name the later owner
instead of treating it as dropped or vague future work.

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
- Sub-plan N auto-plan started.
- Sub-plan N auto-plan readiness gate passed:
  `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`.
- Sub-plan N marked planned after ArcStep readiness proof.
- Sub-plan N stored status was planned but readiness gate failed; reset to
  planning and resumed auto-plan.
- Sub-plan N implement-loop started.
- Sub-plan N auto-implement continued; ArcStep audit is not COMPLETE yet.
- Sub-plan N implement-loop completed (arch-step audit COMPLETE).
- Role dispatch/resume: role, transport, clean/bounded/full starting context,
  exact child/session handle, capabilities/worktree posture, and receipt path.
- Epic critic run on sub-plan N: verdict=`<pass|scope_change|incomplete>`.
- Epic critic incomplete on sub-plan N; status kept implementing and ArcStep
  auto-implement resumed.
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

Same-session `auto-plan` and role-based automatic sub-plan DOC_PATHs
must include an Epic Requirement Coverage section, usually in Section 0 or
immediately after it. The coverage map classifies every meaningful
raw-goal/decomposition requirement as one of:

- owned by this sub-plan
- satisfied by a prior sub-plan
- assigned to a named later sub-plan

The epic doc does not duplicate the full coverage map. It points to the
sub-plan DOC_PATH and records only material coverage decisions in the
Decision Log.

Coverage is a scope-preservation map, not a scope-reduction tool. A
requirement from the raw goal, approved Decomposition, North Star, Section 7,
acceptance criteria, or verification obligations must never be classified as
out of scope by the orchestrator or a role child. If it is not owned here,
satisfied already, or assigned to a named later sub-plan, the sub-plan is not
ready.

Coverage is also not expansion authority. Each sub-plan's Section 0 Scope and
Simplicity Contract must identify the inherited raw-goal/decomposition anchors,
its own initial minimal convergence closure or `none`, and its scope freeze.
Initial sub-plan architecture may add the smallest evidenced same-contract
closure before freeze. After freeze, a critic, worklog, Decision Log, or later
plan edit cannot add another path or sub-plan without human approval.

## Mutation rules

The skill mutates the epic doc under these conditions only:

- `start` mode: creates the doc with initial frontmatter, TL;DR, and
  the drafted Decomposition. Orchestration Log gets one entry.
- `approve-decomposition` mode: applies adjustments, flips
  `sub_plans_approved: true`, sets `status: active`, appends to log.
- `run` mode: updates sub-plan Status fields, fills in DOC_PATH when
  `$arch-step new` runs, appends to log, writes critic verdict
  pointer under the sub-plan entry.
- `auto-plan` mode: assigns missing DOC_PATHs, creates or repairs only the
  `arch-step new` scaffold directly, runs or continues the real `$arch-step
  auto-plan <DOC_PATH>` flow, sets sub-plan Status to `planned` only after
  `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
  exits 0 for that exact DOC_PATH, and appends compact log entries. It never
  treats scaffold setup, marker-looking text, copied planning sections, or a
  prior stored Status as readiness proof.
- `auto-implement` mode: requires every non-complete sub-plan to be `planned`,
  verifies the exact DOC_PATH still passes the ArcStep readiness gate, runs or
  continues the real `$arch-step auto-implement <DOC_PATH>` implement/prove/audit
  loop until `arch_skill:block:implementation_audit` says `Verdict (code):
  COMPLETE` or a true blocker stops progress, runs the epic critic only after
  that clean audit, updates Status to `complete` only after critic `pass`, and
  appends compact log entries. It never treats one invocation, local proof,
  worklog optimism, stored Status, or ArcStep audit alone as epic completion.
- `resume-scope-change` mode: inserts a new sub-plan or extends an
  existing one's scope only after explicit human approval, or records the
  human choice to keep scope and subtract/redesign unauthorized work; always
  appends the human decision anchor to the Decision Log.
- `auto-run` mode: records compact transport/context/handle receipts,
  exact-role worker resumes after critic failures, and auto-inserted sub-plans.
  When the external harness is selected it also writes or updates
  `auto_execution`; full external child artifacts stay in its run directory,
  and `state.json` keeps compact `latest_worker_attempts` pointers to the
  sessions that may be resumed.

The skill never edits `raw_goal` or `raw_goal_sha256` except at
`start`. If the user wants to edit the goal, they start a new epic;
the skill does not rewrite history in place.

## Validation on load

Every time the skill reads the epic doc, it validates:

1. Frontmatter parses as YAML with all required fields.
2. `raw_goal_sha256` matches a fresh hash of `raw_goal`.
3. If the external interactive-critic tuple is present, `models_sha256`
   matches a fresh hash of the runtime/model/effort tuple. If the tuple is
   null, `models_sha256` is also null; use a clean native critic unless an
   external critic was deliberately selected, in which case ask before it runs.
4. If `auto_execution` is present, required role blocks
   (`epic_planner`, `implementation_worker`, `critic`) contain `runtime`,
   `model`, `effort`, `source_quote` or source metadata, positive monitor
   fields (`poll_seconds`, `quiet_floor_seconds`, `stuck_floor_seconds`,
   `max_runtime_seconds`), and a matching `execution_sha256` computed over the
   normalized execution policy excluding `auto_run_dir`. A legacy
   `repair_worker` role is optional and must not be required in new docs.
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
