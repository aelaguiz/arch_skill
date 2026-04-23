# Manifest schema: the list of steps, grounded in target-repo doctrine

The manifest is the authoritative list of ordered steps for the run. The
orchestrator drafts it in Phase 2 by reading the target repo's doctrine
and translating the named process into a concrete sequence. The manifest
is locked at Phase 3 confirmation — it does not change during execution.

## Top-level shape

```json
{
  "schema_version": 1,
  "target_repo_path": "/abs/path/to/target/repo",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "doctrine_paths": [
    "/abs/path/to/target/repo/CLAUDE.md",
    "/abs/path/to/target/repo/skills/lessons/SKILL.md"
  ],
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 1,
  "models": {
    "step_model": "...",
    "step_effort": "...",
    "critic_model": "...",
    "critic_effort": "..."
  },
  "steps": [ /* StepDescriptor[] */ ]
}
```

## StepDescriptor

```json
{
  "n": 1,
  "label": "Draft lesson outline from source material",
  "skill_or_instruction": "$lessons-ops · ramp-up + draft outline",
  "sub_session_runtime": "claude",
  "doctrine_path_for_this_step":
    "/abs/path/to/target/repo/skills/lessons/SKILL.md",
  "inputs": [
    "source: /abs/path/to/target/repo/tracks/track-3/section-3/lesson-2/brief.md"
  ],
  "expected_artifact": {
    "kind": "file",
    "selector":
      "/abs/path/to/target/repo/tracks/track-3/section-3/lesson-2/outline.md",
    "evidence_required":
      "file exists AND first line matches '^# Lesson 2' AND contains '^## '"
  },
  "critic_contract_ref": {
    "profile": "strict",
    "active_checks": [
      "skill_order_adherence",
      "no_substep_skipped",
      "artifact_exists",
      "no_fabrication",
      "doctrine_quote_fidelity"
    ]
  },
  "max_retries": 1
}
```

Field notes:

- `n`: 1-indexed position in the ordered sequence.
- `label`: short human-readable description of the step's outcome.
- `skill_or_instruction`: exactly what the step session is supposed to
  invoke. A skill reference (`$lessons-ops`) or a free-form instruction
  (`"run tests and record results"`). Specificity here is what
  `skill_order_adherence` keys off — be precise.
- `sub_session_runtime`: `"claude"` or `"codex"`. Inherits the default
  chosen in Phase 1 unless the doctrine calls for a specific runtime for
  this step.
- `doctrine_path_for_this_step`: the single file the step session should
  read to learn how to do this step. If the doctrine is split across
  multiple files, list the entry point; the step session reads onwards
  from there.
- `inputs`: prior artifacts or source files the step needs to read.
  Absolute paths.
- `expected_artifact`: the thing the critic will verify.
  - `kind`: `file` (must exist on disk), `edit` (named file must have a
    new modification), `file-exists` (just existence, no content check),
    `command-success` (a named command exits 0).
  - `selector`: the path, pattern, or command string.
  - `evidence_required`: a plain-English predicate the critic translates
    into a read-only shell check. Use conjunction ("AND") deliberately —
    each condition is checked independently.
- `critic_contract_ref`: the expanded check list for this step. The
  orchestrator computes this from `profile` + `forced_checks` + any
  per-step overrides in the doctrine.
- `max_retries`: per-step cap (usually equals `per_step_retry_cap`).
  Can be smaller for a step known to be binary (either works or not —
  no partial progress to recover from).

## Drafting discipline

The manifest is a read-then-think product, not a template. When drafting
from the target repo's doctrine:

1. Read `CLAUDE.md` / `AGENTS.md` at the repo root. Find the named
   process or skill.
2. Read the referenced SKILL.md. Identify ordered sub-steps. These
   become your candidate steps.
3. For each sub-step, locate the concrete artifact it produces. If no
   artifact is named, look for a natural one (the file it writes, the
   doc it creates, the command it runs). The artifact is what the
   critic verifies — if there is no artifact, the critic has nothing
   to check, and the step needs rethinking before executing.
4. If the doctrine prescribes a runtime for a sub-step, honor it. If
   not, use the run default.
5. Write the manifest. Announce it in Phase 3.

## Fail-loud cases

- The named process does not exist in the target repo's doctrine. Do
  not guess. Ask the user which process they mean.
- A sub-step in the doctrine does not produce a verifiable artifact. Do
  not make one up. Ask the user what evidence of completion looks like,
  or redefine the step boundary so artifacts are natural.
- The doctrine contradicts itself (one file says 3 steps, another says
  4). Do not average. Surface the contradiction to the user and let
  them pick the authoritative source.

## A worked example

The user said: "ramp up on track 3 section 3 and implement lesson 2
strictly according to the skill order, no fabrication."

After reading the target repo's `CLAUDE.md` and
`skills/lessons/SKILL.md`, the orchestrator drafts:

```json
{
  "schema_version": 1,
  "target_repo_path": "/Users/aelaguiz/workspace/lessons_studio",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "doctrine_paths": [
    "/Users/aelaguiz/workspace/lessons_studio/CLAUDE.md",
    "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md"
  ],
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 1,
  "models": {
    "step_model": "opus-4-7",
    "step_effort": "xhigh",
    "critic_model": "sonnet-4-6",
    "critic_effort": "xhigh"
  },
  "steps": [
    {
      "n": 1,
      "label": "Ramp up on track 3 / section 3 context",
      "skill_or_instruction": "$lessons-ops · ramp-up",
      "sub_session_runtime": "claude",
      "doctrine_path_for_this_step":
        "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md",
      "inputs": [],
      "expected_artifact": {
        "kind": "file",
        "selector":
          "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/_rampup_notes.md",
        "evidence_required":
          "file exists AND contains '^## Key concepts'"
      },
      "critic_contract_ref": {
        "profile": "strict",
        "active_checks": [
          "skill_order_adherence", "no_substep_skipped",
          "artifact_exists", "no_fabrication",
          "doctrine_quote_fidelity"
        ]
      },
      "max_retries": 1
    },
    {
      "n": 2,
      "label": "Draft lesson 2 outline",
      "skill_or_instruction": "$lessons-ops · draft outline",
      "sub_session_runtime": "claude",
      "doctrine_path_for_this_step":
        "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md",
      "inputs": [
        "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/_rampup_notes.md"
      ],
      "expected_artifact": {
        "kind": "file",
        "selector":
          "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md",
        "evidence_required":
          "file exists AND first line matches '^# Lesson 2'"
      },
      "critic_contract_ref": {
        "profile": "strict",
        "active_checks": [
          "skill_order_adherence", "no_substep_skipped",
          "artifact_exists", "no_fabrication",
          "doctrine_quote_fidelity"
        ]
      },
      "max_retries": 1
    }
  ]
}
```

The example above is illustrative. Real manifests follow whatever the
target repo's doctrine actually says, not this shape.
