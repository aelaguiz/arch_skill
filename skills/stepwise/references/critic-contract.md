# Critic contract: observation only

The critic is a new clean child that judges one worker attempt against the
step's declared contract. Prefer a same-host native child; use the external
adapter only when its concrete provider, model, lifecycle, isolation,
automation, or receipt benefit warrants the additional process. The critic
answers one question:

Did this attempt honor its contract, and what evidence proves that answer?

The critic does not prescribe repairs. It does not write future worker
commands. It does not decide whether root cause is local or upstream. Stepwise
owns diagnosis and repair authorship after reading the critic's observation.

## What the critic judges

The critic judges process adherence and artifact truth, not general quality.
It does not review code style, suggest refactors, or critique content beyond
what the step descriptor declared.

## The five checks

Each step descriptor names which checks apply. The critic runs only the named
checks, plus any forced checks already expanded into the descriptor.

### `skill_order_adherence`

The worker followed the owner skill or instruction declared by the manifest.
Evidence lives in the transcript: doctrine reads, tool calls, support-skill
invocations, owner-declared primitives, and explicit step landmarks.

Owner-declared supporting skills, primitives, configs, commands, and MCP tools
are in scope and count as adherence. Switching to a different stage owner,
restarting the process, invoking an unrelated workflow/loop skill, or replacing
owner authority with repo-wide guessing fails this check.

### `no_substep_skipped`

When owner doctrine prescribes sub-steps, each prescribed sub-step appears as a
landmark in the transcript. Landmarks can be tool invocations, doctrine reads,
or explicit boundaries with evidence. Collapsing prescribed sub-steps into "I
did it all" fails this check.

### `artifact_exists`

The expected artifact selector resolves and `evidence_required` holds. The
critic checks this with read-only file inspection or read-only commands named
by the descriptor.

### `no_fabrication`

Every substantive claim the worker made about its work is backed by a real file
change, command output, transcript event, or artifact. Effort is not evidence.

### `doctrine_quote_fidelity`

If owner doctrine prescribes order, the worker followed that order. Evidence is
the sequence of transcript landmarks.

## StepVerdict JSON schema

The critic returns one JSON document conforming to
`step-verdict.schema.json`. Claude enforces it with `--json-schema`, Codex
enforces it with `--output-schema`, and Grok receives the schema inline before
the script post-validates the returned JSON. Codex may require
required-but-nullable fields; the orchestration script normalizes schema shape
while preserving semantics.

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "step_n",
    "verdict",
    "checks",
    "observed_breach",
    "evidence_pointers",
    "contract_clauses_implicated",
    "summary",
    "abstain_reason"
  ],
  "properties": {
    "step_n": {"type": "integer", "minimum": 1},
    "verdict": {"enum": ["pass", "fail", "abstain"]},
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "status", "evidence"],
        "properties": {
          "name": {
            "enum": [
              "skill_order_adherence",
              "no_substep_skipped",
              "artifact_exists",
              "no_fabrication",
              "doctrine_quote_fidelity"
            ]
          },
          "status": {"enum": ["pass", "fail", "inapplicable"]},
          "evidence": {"type": "string"}
        }
      }
    },
    "observed_breach": {"type": ["string", "null"]},
    "evidence_pointers": {"type": "array", "items": {"type": "string"}},
    "contract_clauses_implicated": {
      "type": "array",
      "items": {"type": "string"}
    },
    "summary": {"type": "string"},
    "abstain_reason": {"type": ["string", "null"]}
  }
}
```

Field semantics:

- `step_n`: the step position. Mismatches indicate the critic was briefed on
  the wrong step.
- `verdict`:
  - `pass`: all applicable checks passed. `observed_breach` and
    `abstain_reason` must be `null`; `evidence_pointers` may cite decisive
    pass evidence or be empty.
  - `fail`: at least one applicable check failed. Fill `observed_breach`,
    `evidence_pointers`, and `contract_clauses_implicated`. Do not prescribe a
    fix.
  - `abstain`: the critic could not judge because required evidence was
    unavailable or corrupted. Fill `abstain_reason`; do not guess the
    underlying verdict.
- `checks`: one entry per active check.
- `observed_breach`: one sentence naming what the attempt failed to honor, or
  `null` when not failing.
- `evidence_pointers`: concrete transcript/artifact/command-output pointers.
- `contract_clauses_implicated`: manifest, owner-runbook, or support-doctrine
  clauses implicated by the observation.
- `summary`: 1-3 sentences for the run report.
- `abstain_reason`: plain English when abstaining, otherwise `null`.

## Strictness scoping

The step descriptor's `critic_contract_ref` names the active profile plus any
forced checks. The orchestrator expands this into a concrete check list before
briefing the critic:

| Profile | Default checks |
| --- | --- |
| strict | all five |
| balanced | artifact_exists, no_fabrication, skill_order_adherence |
| lenient | artifact_exists, no_fabrication |

Forced checks are unioned into the default set. `no_fabrication` is always
present regardless of profile.

## What the critic never does

- Edit files.
- Create or coordinate other model agents or invoke delegation/consult skills.
- Re-run the worker's work.
- Suggest repair steps.
- Recommend paths or commands to the worker.
- Decide root-cause location.
- Route to an upstream step.
- Add candidate directions, timeline-sensitivity analysis, overconstraint
  warnings, or future-process recommendations.
- Soften a fail into a pass because the worker tried.
- Invent checks not in the descriptor.

Any critic output that reads like a worker instruction is invalid for this
skill. The critic produces observation, evidence, and contract citation only.
Use enforced read-only capability when available, retain the no-edit prompt in
all transports, and have the parent compare target-repo state before and after
the critic. Clean context does not itself enforce filesystem isolation.
