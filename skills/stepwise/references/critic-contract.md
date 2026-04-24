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

The critic returns a single JSON document conforming to
`step-verdict.schema.json`. Both runtimes enforce it — Claude via
`--json-schema`, Codex via `--output-schema`. Codex requires every property
on every object to appear in `required`, so semantically optional fields are
required-but-nullable. The orchestration script normalizes older schemas to
that shape and then runs semantic validation on the verdict.

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "step_n",
    "verdict",
    "checks",
    "resume_hint",
    "route_to_step_n",
    "abstain_reason",
    "summary"
  ],
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
      "type": ["object", "null"],
      "additionalProperties": false,
      "required": ["headline", "required_fixes", "do_not_redo"],
      "properties": {
        "headline": {"type": "string"},
        "required_fixes": {"type": "array", "items": {"type": "string"}},
        "do_not_redo": {"type": "array", "items": {"type": "string"}}
      }
    },
    "route_to_step_n": {"type": ["integer", "null"], "minimum": 1},
    "abstain_reason": {"type": ["string", "null"]},
    "summary": {"type": "string"}
  }
}
```

Field semantics:

- `step_n`: the step's position in the manifest. Sanity-check this matches
  the descriptor — mismatches indicate the critic was briefed on the wrong
  step.
- `verdict`:
  - `pass`: all applicable checks passed. Advance. Set `resume_hint`,
    `route_to_step_n`, and `abstain_reason` to `null`.
  - `fail`: at least one applicable check failed. Resume with `resume_hint`.
    Set `abstain_reason` to `null`. Set `route_to_step_n` to an earlier
    step number only for upstream-routed fails; otherwise set it to `null`.
  - `abstain`: the critic could not judge (inputs missing, artifact not
    inspectable, transcript corrupted). Set `resume_hint` and
    `route_to_step_n` to `null`, fill `abstain_reason`, and let the
    orchestrator repair any known missing input before asking the user.
- `checks`: one entry per check in the descriptor. A check that was not in
  the descriptor but is load-bearing may also appear with `status:
  inapplicable` and an explanation — this is how the critic reports that it
  wanted to check something and could not.
- `resume_hint`: object when `verdict=fail`; `null` otherwise. The
  orchestrator renders this into the resume prompt verbatim. The critic's
  phrasing is what the step will read.
  - `headline`: one blunt sentence naming the contract breach.
  - `required_fixes`: ordered actions the step must execute. These are not
    suggestions. For repeated failures or failures about process evidence,
    skill loading, owner-path usage, skipped landmarks, or false final claims,
    write a concrete execution checklist with paths, commands, selector
    checks, and explicit stop conditions.
  - `do_not_redo`: things the step already did correctly. The step should
    not tear down good work to rebuild it.
- `route_to_step_n`: nullable. Set on `verdict=fail` when the fix lives in
  an earlier step's artifact and the current step cannot repair it from
  its own scope. Must be `< step_n`. When set, `resume_hint` is addressed
  to that earlier step — its `headline` and `required_fixes` will be read
  by the target step's session when the orchestrator reopens it. Omit for
  self-routed fails by setting it to `null`.
- `abstain_reason`: string when `verdict=abstain`; `null` otherwise. Plain
  English.
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

## Routing a fail

A fail must be actionable. The critic decides where the actual repair
lives and expresses that via `route_to_step_n`.

Self-routed (`route_to_step_n: null`): the current step can repair this
from within its declared scope. A resume with `required_fixes` would be
enough.

Upstream-routed (set `route_to_step_n = M`, with `M < step_n`): the
repair lives in step M's artifact, and the current step cannot reach
it from within its declared scope. Address `resume_hint` to step M — its
`headline` and `required_fixes` are what step M's session will read
when it reopens.

Use upstream routing only when the fix is impossible from the current
step's scope, not when it's merely preferable upstream. "An earlier
step could have done this better" is not a routing reason. When in
doubt, route self.

Example — route self: step 4 produced an artifact missing a field the
step was supposed to produce. The field is derivable from what step 4
was doing. Set `route_to_step_n` to `null`; set `required_fixes` naming the
missing field.

Example — process evidence fail: step 4 produced a copy artifact but used raw
edits while claiming the owner path was unavailable. Omit `route_to_step_n`
by setting it to `null` if step 4 can recover. Set `required_fixes` to the
exact operational sequence: read the owning skill path, read each required
specialist path, use the owner write command or stop with the exact missing
command/help output, remove the false final claim, and finish with the selector
command the critic will use.

Example — route upstream: step 4 produced per-surface copy correctly,
but that copy references step 3's walkthrough stage. Step 3 used the
wrong stage for the pinned Brief. Step 4 cannot rewire step 3's stage
from within copy authoring. Set `route_to_step_n = 3`; address
`resume_hint` to step 3 with a rationale in the headline that cites
the specific structural mismatch.

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
- Invent a routing target. `route_to_step_n` must name an earlier step
  whose artifact the evidence implicates, not a guess.
