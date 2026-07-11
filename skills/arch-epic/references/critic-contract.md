# Critic contract: EpicVerdict schema and scope-drift checks

In interactive mode, the epic critic runs once per sub-plan after
`$arch-step implement-loop` finishes and the audit block reports
`Verdict (code): COMPLETE`. Its job is narrow: detect scope drift
between what the user approved and what shipped.

In spawned-harness automatic mode, the same critic role also runs earlier gates:
North Star / Epic Requirement Coverage, plan readiness, and
completion/scope. Spawned-harness automatic mode uses spawned critics instead of
per-sub-plan user approval, so those critics must check that the raw
epic goal and approved decomposition are still represented.

The critic is a fresh subprocess (Claude, Codex, or Grok, per the epic
doc's `critic_runtime`). It has no memory of the orchestrator's
prose. It reads the sub-plan's DOC_PATH, worklog, and the arch-step
audit block directly, returns one JSON document, and exits. It reports
observation and evidence only; it does not prescribe repair steps for
the worker.

## The checks

Completion critics run all checks. Earlier spawned-harness gates run the
checks that apply to that gate and mark completion-only checks
`inapplicable`.

### 0. `epic_requirement_coverage`

Spawned-harness sub-plan docs must include an Epic Requirement Coverage
section. Verify that every meaningful raw-goal/decomposition requirement
is classified as:

- owned by this sub-plan
- satisfied by a prior sub-plan
- assigned to a named later sub-plan

Fail if the worker only restates the one-sentence decomposition and
loses a raw-goal obligation, if a future sub-plan depends on an unstated
handoff from the current sub-plan, if a requirement is assigned onward
without a named later owner, or if an approved requirement is called out
of scope.

Evidence source: epic doc raw goal and Decomposition, current sub-plan
Section 0 / coverage map, prior sub-plan verdicts when relevant.

### 1. `north_star_preserved`

Compare the sub-plan's approved North Star (Section 0 of the
DOC_PATH) against what shipped. The North Star was approved by
the user; anything missing, downgraded, or silently reinterpreted
is a fail.

Evidence source: Section 0 of the sub-plan's DOC_PATH (the
North Star), versus the worklog and phase status lines.

Fail pattern: the North Star says "the dashboard shows the last 30
days of audit events"; the worklog says "shipped with 7-day window
because of performance concerns." Fail even if an agent wrote a Decision
Log note, because agents cannot approve scope reduction.

Pass pattern: the North Star's claims are fully represented in the
shipped behavior.

### 2. `scope_not_cut`

Check the sub-plan's Section 7 (phase plan) checklist items and
Exit Criteria against the worklog. Any item that was dropped,
marked "skipped," silently removed, or never referenced in the worklog
is a suspect scope cut. A requirement explicitly assigned to a named
later sub-plan is preserved epic scope, not a current-sub-plan failure.

Evidence source: Section 7 of the DOC_PATH (phase plan and exit
criteria), the WORKLOG_PATH, and the Decision Log inside the
sub-plan doc.

Fail pattern: phase 2 had an exit criterion "migration script
tested against staging data"; worklog never mentions the test. Fail.

Pass pattern: every current phase's checklist items and exit criteria are
visibly completed in the worklog, and every approved requirement not due
in this sub-plan has a named later owner. If an item cannot be completed
and has no named later owner, the verdict must be `scope_change_detected`
or `incomplete`, not pass.

### 3. `scope_provenance_and_no_cycling`

Recover the raw human goal, approved decomposition, sub-plan Scope and
Simplicity Contract, initial convergence closure and freeze anchor, and any
explicit later human approvals. Compare those anchors with the worklog,
Decision Log, and shipped code.

Fail when an obligation or durable concept appeared only after freeze, when an
agent-authored Decision Log entry is the only claimed authority, when code was
built and the plan was edited later to match it, or when repeated critic waves
used prior agent-created work to demand further expansion. A newly discovered
same-contract path is still new scope after freeze.

### 4. `no_orphaned_discoveries`

Read the worklog and Decision Log against the approved sub-plan. A
discovery candidate is any fact showing that implementation encountered a
required surface, dependency, behavior, constraint, or handoff that was not
represented in the approved sub-plan when work began. Do not rely on a
phrase list. Infer the discovery from the relationship between approved
scope, what implementation says became necessary, and what is now recorded
in Section 7, Epic Requirement Coverage, or the Decision Log. Classify each
candidate:

- If the discovery was present in the frozen initial closure or has an explicit
  later human-approval anchor: fine. Not orphaned.
- If it was added to the phase plan or implemented after freeze without human
  approval: fail, even when the Decision Log records it.
- If the discovery was called out but left unresolved ("we'll need
  X eventually, punting for now"): this is a `discovered_items[]`
  entry only if X is required for approved scope and has no named later
  owner. If X is assigned to a named later sub-plan, treat it as
  preserved scope. If X is a harmless observation that is not required
  for the approved North Star, ignore it.

Evidence source: worklog text, Decision Log text, North Star.

### 5. `audit_clean`

Confirm `arch_skill:block:implementation_audit` exists in the
sub-plan's DOC_PATH and reports `Verdict (code): COMPLETE` with
no reopened phases listed.

This is a sanity check — the orchestrator only runs the epic
critic after arch-step's audit passed, so this check should almost
always `pass`. It is here as a guard against someone running the
critic out-of-order or against a doc whose audit is stale.

Evidence source: the `arch_skill:block:implementation_audit` block
in the DOC_PATH.

## Verdict logic

The critic computes each check's status (`pass` / `fail` /
`inapplicable`), then picks the overall verdict:

- `pass`: all applicable checks passed.
- `scope_change_detected`: at least one of checks 0–4 failed, OR
  the critic found at least one `discovered_items[]` entry that
  needs a user decision.
- `incomplete`: check 5 (`audit_clean`) failed. This should never
  happen in normal flow; the orchestrator surfaces it to the user
  as an arch-step audit issue.
- No verdict is `abstain`. If the critic cannot read the sub-plan
  doc at all, it fails loud rather than abstaining.

## EpicVerdict JSON schema

Lives at `references/epic-verdict-schema.json`. Inlined here for
reference. Claude (`--json-schema`) and Codex (`--output-schema`) expect
`additionalProperties: false` at every object level; Grok receives the schema
inline and the script post-validates the returned JSON.

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["sub_plan_name", "verdict", "checks", "discovered_items", "summary"],
  "properties": {
    "sub_plan_name": {"type": "string"},
    "verdict": {"enum": ["pass", "scope_change_detected", "incomplete"]},
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "status", "evidence"],
        "properties": {
          "name": {
            "enum": [
              "epic_requirement_coverage",
              "north_star_preserved",
              "scope_not_cut",
              "scope_provenance_and_no_cycling",
              "no_orphaned_discoveries",
              "audit_clean"
            ]
          },
          "status": {"enum": ["pass", "fail", "inapplicable"]},
          "evidence": {"type": "string"}
        }
      }
    },
    "discovered_items": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["what", "scope_relationship", "recommendation"],
        "properties": {
          "what": {"type": "string"},
          "scope_relationship": {
            "enum": [
              "missing_authorized_scope",
              "new_scope_needs_human",
              "unauthorized_built_scope"
            ]
          },
          "recommendation": {
            "enum": ["complete_authorized_scope", "human_decision", "subtract"]
          }
        }
      }
    },
    "summary": {"type": "string"}
  }
}
```

## Field semantics

- `sub_plan_name`: string identifying which sub-plan this verdict
  is for. The orchestrator cross-checks this against the sub-plan
  named in the critic invocation.
- `verdict`: overall verdict per the logic above.
- `checks`: one entry per check. The critic reports every check
  it ran; it does not omit inapplicable ones.
- `discovered_items`: always present. Empty array `[]` when
  `verdict: pass` or `verdict: incomplete`; non-empty when
  `verdict: scope_change_detected`. Codex's `--output-schema`
  requires every `properties` key to appear in `required`, so
  this field is always emitted — the empty-array form is the
  "no items" signal. Each item names whether authorized scope is missing, new
  scope needs a human decision, or unauthorized built scope must be subtracted.
- `summary`: 1–3 sentences the orchestrator prints to the user at
  the halt or pass boundary. Plain English.

Existing schema consumers may see older verdicts without
`epic_requirement_coverage`; those historical verdicts stand. New
spawned-harness critics must include it.

## Critic posture

The critic reads. It does not write files. It does not run arch-step
commands. It does not attempt to fix anything it finds, and it does
not tell the planner or implementation worker how to fix the finding.
Read-only discipline is enforced in the critic prompt (see
`critic-prompt.md`), not by sandbox — per repo convention, both
runtimes run dangerous / skip-permissions / no-sandbox.

If the critic discovers that the sub-plan doc is malformed (missing
required sections, corrupt frontmatter), it fails `audit_clean` and
reports the malformation in `summary`. It does not try to repair it.

The critic does not have authority to downgrade approved scope as a
"compromise." Its classification is based on whether the sub-plan's North Star
and epic requirements are met, not on what would make the epic proceed
smoothly.
It also has no authority to expand scope. Its finding can halt the epic, but
only a human approval can add a new path or sub-plan after freeze.

## What this critic is NOT

- Not a code reviewer. Use the host agent's normal review response for that.
- Not a re-audit of arch-step's implementation. That is
  `$arch-step audit-implementation`'s job.
- Not a repair author. In spawned-harness automatic mode, the parent resumes the
  planner or implementation worker with the critic verdict as evidence.
- Not a gate on the next sub-plan's North Star (that is the user's
  job at the next `$arch-step new` invocation in interactive mode).
- Not a general quality checker for the epic. The epic doc
  maintains quality by being approved up-front; the critic watches
  for drift from that approval.
