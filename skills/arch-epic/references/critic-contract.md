# Critic contract: EpicVerdict schema and the four scope-drift checks

The epic critic runs once per sub-plan, after `$arch-step
implement-loop` finishes and the audit block reports
`Verdict (code): COMPLETE`. Its job is narrow: detect scope drift
between what the user approved and what shipped. It does NOT
re-audit code completeness — arch-step already did that and the
epic critic trusts the verdict.

The critic is a fresh subprocess (Claude or Codex, per the epic
doc's `critic_runtime`). It has no memory of the orchestrator's
prose. It reads the sub-plan's DOC_PATH, worklog, and the arch-step
audit block directly, returns one JSON document, and exits.

## The four checks

Each check runs on every critic invocation. There are no
strictness profiles at the epic level; scope drift is always
important.

### 1. `north_star_preserved`

Compare the sub-plan's approved North Star (Section 0 of the
DOC_PATH) against what shipped. The North Star was approved by
the user; anything missing, downgraded, or silently reinterpreted
is a fail.

Evidence source: Section 0 of the sub-plan's DOC_PATH (the
North Star), versus the worklog and phase status lines.

Fail pattern: the North Star says "the dashboard shows the last 30
days of audit events"; the worklog says "shipped with 7-day window
because of performance concerns"; the Decision Log has no entry
authorizing the change. Fail.

Pass pattern: the North Star's claims are fully represented in the
shipped behavior, or narrowed with an explicit Decision Log entry.

### 2. `scope_not_cut`

Check the sub-plan's Section 7 (phase plan) checklist items and
Exit Criteria against the worklog. Any item that was dropped,
marked "skipped," or never referenced in the worklog is a suspect
silent scope cut.

Evidence source: Section 7 of the DOC_PATH (phase plan and exit
criteria), the WORKLOG_PATH, and the Decision Log inside the
sub-plan doc.

Fail pattern: phase 2 had an exit criterion "migration script
tested against staging data"; worklog never mentions the test; no
Decision Log entry. Fail.

Pass pattern: every phase's checklist items and exit criteria are
either visibly completed in the worklog or explicitly deferred with
a Decision Log note the user can inspect.

### 3. `no_orphaned_discoveries`

Read the worklog and Decision Log looking for language that signals
an unplanned discovery: "we also needed to", "turns out we had to
add", "this was blocked until we did X", "surprised by", "had to
work around". Every such mention is a candidate. Classify each:

- If the discovery was added to the phase plan and implemented, and
  the Decision Log records the change: fine. Not orphaned.
- If the discovery was added and implemented silently (no Decision
  Log entry): this is a fail — silent scope expansion. The
  implementation exists but the decomposition does not reflect it.
- If the discovery was called out but left unresolved ("we'll need
  X eventually, punting for now"): this is a `discovered_items[]`
  entry. Classify `must_have_or_nice` by reading the North Star —
  if the sub-plan's claim cannot be met without the discovery, it
  is must-have.

Evidence source: worklog text, Decision Log text, North Star.

### 4. `audit_clean`

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

- `pass`: all four checks passed.
- `scope_change_detected`: at least one of checks 1–3 failed, OR
  the critic found at least one `discovered_items[]` entry that
  needs a user decision.
- `incomplete`: check 4 (`audit_clean`) failed. This should never
  happen in normal flow; the orchestrator surfaces it to the user
  as an arch-step audit issue.
- No verdict is `abstain`. If the critic cannot read the sub-plan
  doc at all, it fails loud rather than abstaining.

## EpicVerdict JSON schema

Lives at `references/epic-verdict-schema.json`. Inlined here for
reference. Both Claude (`--json-schema`) and Codex
(`--output-schema`) expect `additionalProperties: false` at every
object level.

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
              "north_star_preserved",
              "scope_not_cut",
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
        "required": ["what", "must_have_or_nice", "recommendation"],
        "properties": {
          "what": {"type": "string"},
          "must_have_or_nice": {"enum": ["must_have", "nice_to_have"]},
          "recommendation": {
            "enum": ["extend_current", "new_sub_plan", "defer", "drop"]
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
  "no items" signal. Each item, when present, is actionable —
  the orchestrator or the user picks a recommendation.
- `summary`: 1–3 sentences the orchestrator prints to the user at
  the halt or pass boundary. Plain English.

## Critic posture

The critic reads. It does not write files. It does not run arch-step
commands. It does not attempt to fix anything it finds. Read-only
discipline is enforced in the critic prompt (see `critic-prompt.md`),
not by sandbox — per repo convention, both runtimes run dangerous /
skip-permissions / no-sandbox.

If the critic discovers that the sub-plan doc is malformed (missing
required sections, corrupt frontmatter), it fails `audit_clean` and
reports the malformation in `summary`. It does not try to repair it.

The critic does not have authority to downgrade a discovery from
must-have to nice-to-have as a "compromise." Its classification is
based on whether the sub-plan's North Star is met, not on what would
make the epic proceed smoothly.

## What this critic is NOT

- Not a code reviewer. Use `$code-review` for that.
- Not a re-audit of arch-step's implementation. That is
  `$arch-step audit-implementation`'s job.
- Not a gate on the next sub-plan's North Star (that is the user's
  job at the next `$arch-step new` invocation).
- Not a general quality checker for the epic. The epic doc
  maintains quality by being approved up-front; the critic watches
  for drift from that approval.
