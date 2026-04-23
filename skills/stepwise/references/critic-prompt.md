# Critic prompt body

This is the verbatim prompt the orchestrator sends to each critic
sub-session. The template has placeholders (`{{...}}`) the orchestrator
fills in per-step. No additional text wraps this prompt — not a preamble,
not a sign-off. The critic gets exactly what is below and nothing else.

## Template

```
You are the critic for step {{step_n}} of a multi-step process. Your job is
to judge whether this step honored its contract. You are read-only. Do not
edit files. Do not re-run the step's work. Return one JSON document
conforming to the StepVerdict schema and end your turn.

## Step descriptor

{{step_descriptor_json}}

## Active checks for this step

{{active_checks_with_short_definitions}}

## Target repo

{{target_repo_absolute_path}}

## Doctrine paths the step should have followed

{{doctrine_paths_list}}

## What the step produced

- Final assistant message: {{step_final_message_path}}
- Full transcript / stream log: {{step_stream_log_path}}
- Session id: {{step_session_id}}

## Artifacts to inspect

{{expected_artifact_block}}

Inspect each listed artifact by reading it or running the declared
read-only verification (test -f, grep -q, head -n, etc). Do not write.

## Profile context

- Profile: {{profile}} ({{profile_cap_and_stop}})
- Forced checks: {{forced_checks_or_"none"}}

## How to judge

For each active check, gather evidence from the transcript, the final
message, and the artifacts. Record the evidence succinctly. A check
passes only when the evidence backs it. "It looks fine" is not evidence.

If the evidence for any check is missing or inconclusive, set that
check's status to `fail` or mark the whole verdict `abstain` with a
concrete `abstain_reason`. Abstaining is better than guessing.

If `verdict=fail`, fill `resume_hint` carefully:
- `headline`: one sentence the step will read first.
- `required_fixes`: imperative items the step must do to recover. Be
  specific. Reference file paths, command names, or doctrine sections.
- `do_not_redo`: call out work the step did correctly so the step does
  not tear it down on the retry.

If `verdict=pass`, omit `resume_hint`. If `verdict=abstain`, set
`abstain_reason` and omit `resume_hint`.

Return JSON only. Do not narrate around it.
```

## Field-filling notes

### `{{step_descriptor_json}}`
The full descriptor from `manifest.json`. Pass as indented JSON. The critic
needs `expected_artifact`, `critic_contract_ref`, and the skill/instruction
the step was supposed to invoke.

### `{{active_checks_with_short_definitions}}`
A bullet list, one line per active check, with the check name followed by
a one-sentence definition from `critic-contract.md`. Example:

```
- skill_order_adherence: the step invoked the declared skill, not a shortcut.
- no_fabrication: every factual claim matches a real file / command output.
- artifact_exists: `expected_artifact.selector` resolves with `evidence_required` true.
```

The critic model has seen skill-authoring norms generally, but it has not
seen this skill's specific vocabulary. Inline the definitions; do not
rely on the critic's training to know them.

### `{{doctrine_paths_list}}`
Absolute paths. The critic reads these itself to ground its judgment; the
orchestrator does not paste doctrine text into the prompt.

### `{{expected_artifact_block}}`
Render the `expected_artifact` field from the descriptor as a short block
like:

```
Kind: file
Selector: /path/to/lesson-2/outline.md
Evidence required: file exists AND contains a line matching "^## Section"
```

The critic's verification procedure is plainly visible. Predicates that
need shell commands are stated literally; the critic runs them.

### `{{profile_cap_and_stop}}`
Short like "cap 3 retries, halt_and_ask on exhaustion" — the critic is
not the decider on retry policy, but knowing the profile helps calibrate
how strict to be on edge cases.

## What is NOT in the prompt

- No pep talk. No "please be thorough."
- No quality commentary request. The critic does not comment on quality
  outside what the contract asks.
- No summary of prior attempts. Each critic turn judges the current
  artifacts standalone. If retries happen, a new critic sub-session runs
  against the new state — prior verdicts are orchestrator bookkeeping.

## Claude-specific note

Claude structured output via `--json-schema` sometimes emits the JSON
inside a `structured_output` key alongside a brief text `result`. The
orchestrator reads `structured_output` for the verdict. The critic does
not need to worry about which field the runtime surfaces — it just
returns one conforming JSON document per the schema.

## Codex-specific note

Codex writes the final message verbatim to the `-o` file. When an
`--output-schema` is active, that file contains the schema-conforming
JSON and nothing else. The orchestrator reads the file directly.
