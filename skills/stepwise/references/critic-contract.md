# Critic contract: what the critic is for, what it returns

The critic is a separate sub-session that judges one step's output against
the step's declared contract. The critic is the only authority on pass/fail.
The orchestrator does not self-certify and does not second-guess the critic's
verdict — it acts on it.

## What the critic judges

Process adherence, not quality. The critic does not review code style,
suggest refactors, or critique the content of what was produced beyond what
the step descriptor declared. Quality review belongs to `$code-review` or a
sibling skill. This skill's critic asks one question only: did this step
honor its contract?

## The five checks

Each step descriptor in the manifest names which of these checks apply. The
critic runs only the named checks. If a check is not in the descriptor, the
critic does not report on it.

### `skill_order_adherence`
The step invoked the exact skill or instruction the manifest declared, in
the declared position in the sequence. Evidence lives in the transcript
(tool calls, slash-command mentions, or explicit doctrine reads). A step
that used a shortcut or a similar-but-different skill fails this check.

### `no_substep_skipped`
When the target-repo doctrine prescribes sub-steps inside a skill's runbook,
each prescribed sub-step appears as a landmark in the transcript. A step
that collapsed three sub-steps into one "I did it all at once" message
fails this check. Landmarks can be tool invocations, file reads of
doctrine, or explicit announcements of sub-step boundaries.

### `artifact_exists`
The step descriptor's `expected_artifact.selector` resolves and its
`evidence_required` predicate holds. The critic runs the predicate as a
read-only shell operation: `test -f`, `grep -q`, `head -n 1`, etc. If the
artifact is absent or wrong, the step fails this check. This is the
bedrock check.

### `no_fabrication`
Every factual claim the step made about its own work is backed by a real
file change, a real command output, or a real artifact. If the step's
transcript says "I wrote config.toml with three sections" and
`grep -c '^\[' config.toml` returns 0, this check fails. The critic must
check every substantive claim — not just the ones that look wrong.

### `doctrine_quote_fidelity`
If the target-repo doctrine prescribes a specific order of operations, the
step followed it. E.g., doctrine says "read CLAUDE.md first, then run
tests, then edit" — a transcript that edits before reading fails this
check. Evidence is the order of landmarks in the transcript.

## StepVerdict JSON schema

The critic returns a single JSON document conforming to this schema. Both
runtimes enforce it — Claude via `--json-schema`, Codex via `--output-schema`
(schema file must include `"additionalProperties": false` at every object
level).

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["step_n", "verdict", "checks", "summary"],
  "properties": {
    "step_n": {
      "type": "integer",
      "minimum": 1
    },
    "verdict": {
      "enum": ["pass", "fail", "abstain"]
    },
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
    "resume_hint": {
      "type": "object",
      "additionalProperties": false,
      "required": ["headline", "required_fixes", "do_not_redo"],
      "properties": {
        "headline": {"type": "string"},
        "required_fixes": {"type": "array", "items": {"type": "string"}},
        "do_not_redo": {"type": "array", "items": {"type": "string"}}
      }
    },
    "abstain_reason": {"type": "string"},
    "summary": {"type": "string"}
  }
}
```

Field semantics:

- `step_n`: the step's position in the manifest. Sanity-check this matches
  the descriptor — mismatches indicate the critic was briefed on the wrong
  step.
- `verdict`:
  - `pass`: all applicable checks passed. Advance.
  - `fail`: at least one applicable check failed. Resume with `resume_hint`.
  - `abstain`: the critic could not judge (inputs missing, artifact not
    inspectable, transcript corrupted). Fail loud; ask the user.
- `checks`: one entry per check in the descriptor. A check that was not in
  the descriptor but is load-bearing may also appear with `status:
  inapplicable` and an explanation — this is how the critic reports that it
  wanted to check something and could not.
- `resume_hint`: required when `verdict=fail`. The orchestrator renders this
  into the resume prompt verbatim. The critic's phrasing is what the step
  will read.
  - `headline`: one sentence naming what went wrong.
  - `required_fixes`: imperative-form items. The step should execute these.
  - `do_not_redo`: things the step already did correctly. The step should
    not tear down good work to rebuild it.
- `abstain_reason`: required when `verdict=abstain`. Plain English.
- `summary`: 1–3 sentences the orchestrator shows in the Phase 5 report.

## Strictness scoping (which checks run when)

The step descriptor's `critic_contract_ref` names the active profile plus
any forced checks. The orchestrator expands this into a concrete check list
before briefing the critic:

| Profile    | Default checks |
|------------|---------------------------------------------------------------|
| strict     | all five |
| balanced   | artifact_exists, no_fabrication, skill_order_adherence |
| lenient    | artifact_exists, no_fabrication |

Forced checks from intake are unioned into the default set. `no_fabrication`
is always present regardless of profile — lenient means "don't care about
form", not "don't care about truth".

## What the critic never does

- Edit files. The critic is read-only by discipline, not by sandbox flag.
  Its prompt tells it not to write; the schema gives it exactly one
  output. The orchestrator detects writes from the critic by diffing the
  target repo state before and after; any write is a fail-loud condition.
- Re-run the step's work to verify. The critic reads transcripts and
  artifacts. It does not re-execute.
- Soften a fail into a pass because the step "tried hard". Effort is not
  evidence.
- Invent checks not in the descriptor. If the critic wants to report a
  concern outside the contracted checks, it goes in `summary` — not as a
  new `checks` entry.
