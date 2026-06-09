# Manifest schema: ordered steps plus resolved execution

The manifest is the authoritative plan for a run. Stepwise drafts it in Phase 2
by reading target-repo doctrine, translating the named process into real steps,
and resolving execution preferences against those steps. The manifest is locked
at Phase 3 confirmation and does not change during execution.

## Top-level shape

```json
{
  "schema_version": 2,
  "target_repo_path": "/abs/path/to/target/repo",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "doctrine_paths": [
    "/abs/path/to/target/repo/AGENTS.md",
    "/abs/path/to/target/repo/skills/lessons/SKILL.md"
  ],
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 5,
  "execution_defaults": {
    "step": {
      "runtime": "codex",
      "model": "gpt-5.5",
      "effort": "high",
      "source": "user prompt"
    },
    "critic": {
      "runtime": "codex",
      "model": "gpt-5.5",
      "effort": "xhigh",
      "source": "user prompt"
    }
  },
  "execution_preferences": [],
  "steps": []
}
```

`stop_discipline` is one of `halt_and_ask`, `skip_and_continue`, or
`escalate_to_user`. It applies after known unblocks, diagnostic convergence
failure, or exhausted repair bounces. Upstream traversal is not a stop
discipline; it is part of the normal diagnose-and-repair protocol.

`per_step_retry_cap` is the number of operational repair bounces a broken
session gets. Diagnostic read-only turns do not count.

## Execution object

Resolved execution blocks appear on every step for both worker and critic:

```json
{
  "runtime": "claude",
  "model": "claude-fable-5",
  "effort": "xhigh",
  "source": "execution_preferences[0]",
  "reason": "Matched learner-facing copy artifact."
}
```

Fields:

- `runtime`: `"claude"`, `"codex"`, or `"grok"`.
- `model`: CLI model name to pass to the runtime.
- `effort`: reasoning effort to pass to the runtime.
- `source`: where the value came from.
- `reason`: one sentence explaining why the execution block applies.

If a preference omits effort, inherit the relevant default effort. If a worker
preference says nothing about critics, critic execution stays on critic
defaults.

## StepDescriptor

```json
{
  "n": 1,
  "label": "Draft lesson outline from source material",
  "skill_or_instruction": "$lessons-ops - draft outline",
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
  "step_execution": {
    "runtime": "codex",
    "model": "gpt-5.5",
    "effort": "high",
    "source": "execution_defaults.step",
    "reason": "No step-specific execution preference applied."
  },
  "critic_execution": {
    "runtime": "codex",
    "model": "gpt-5.5",
    "effort": "xhigh",
    "source": "execution_defaults.critic",
    "reason": "No critic-specific execution preference was provided."
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
  "max_retries": 5
}
```

Field notes:

- `n`: 1-indexed position in the ordered sequence.
- `label`: short human-readable description of the step's outcome.
- `skill_or_instruction`: exactly what the worker is supposed to invoke.
- `doctrine_path_for_this_step`: owner runbook entrypoint. If it names
  supporting skills, primitives, configs, commands, or MCP tools, those support
  paths remain in scope.
- `inputs`: prior artifacts or source files the step reads. Use absolute paths
  where possible. Inputs are how Stepwise walks upstream when a diagnostic
  conversation surfaces bad input. If an input is produced by an earlier step,
  record it as the exact earlier `expected_artifact.selector`, or as
  `source: <absolute selector>`, so `upstream-for` can report the relationship
  without fuzzy guessing.
- `expected_artifact`: the artifact the critic verifies.
- `step_execution`: resolved worker runtime/model/effort.
- `critic_execution`: resolved critic runtime/model/effort.
- `critic_contract_ref`: expanded check list.
- `max_retries`: operational repair-bounce limit, usually equal to
  `per_step_retry_cap`.

## Drafting discipline

The manifest is a read-then-think product, not a template.

1. Read `CLAUDE.md` / `AGENTS.md` at the target repo root. Find the named
   process or skill.
2. Read the referenced `SKILL.md`. Identify ordered sub-steps. These become
   candidate steps.
3. For each sub-step, locate the concrete artifact it produces. If no artifact
   is named, look for a natural one. If there is no verifiable artifact, ask
   rather than invent.
4. Record inputs precisely. Inputs are not decoration; they are the upstream
   chain Stepwise uses during diagnosis.
5. Resolve execution for each step using `execution-routing.md`: feasibility,
   hard doctrine, explicit step preference, semantic preference, then defaults.
6. Write the manifest and include a Phase 3 execution table.

## Fail-loud cases

- The named process does not exist in target-repo doctrine.
- A sub-step has no verifiable artifact.
- Doctrine contradicts itself across files.
- A routing preference matches no steps, conflicts with hard doctrine, or is
  too ambiguous to apply responsibly.
- An input cannot be traced and later steps depend on that trace for safe
  upstream diagnosis.

## Worked example

The user said: "Work in ../lessons_studio. Ramp up on track 3 section 3 and
implement lesson 2 strictly according to the skill order, no fabrication.
Default steps on Codex gpt-5.5 high, critic on Codex gpt-5.5 xhigh. Use
Claude Fable 5 for copywriting steps."

After reading target doctrine, Stepwise drafts an abbreviated manifest:

```json
{
  "schema_version": 2,
  "target_repo_path": "/Users/aelaguiz/workspace/lessons_studio",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 5,
  "execution_defaults": {
    "step": {
      "runtime": "codex",
      "model": "gpt-5.5",
      "effort": "high",
      "source": "user prompt"
    },
    "critic": {
      "runtime": "codex",
      "model": "gpt-5.5",
      "effort": "xhigh",
      "source": "user prompt"
    }
  },
  "execution_preferences": [
    {
      "source_quote": "Use Claude Fable 5 for copywriting steps",
      "applies_to": "steps whose primary artifact is learner-facing copy",
      "step_execution": {
        "runtime": "claude",
        "model": "claude-fable-5"
      },
      "resolution_rationale": "Apply only after comparing drafted step label, instruction, and artifact."
    }
  ],
  "steps": [
    {
      "n": 1,
      "label": "Ramp up on track 3 / section 3 context",
      "skill_or_instruction": "$lessons-ops - ramp-up",
      "doctrine_path_for_this_step":
        "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md",
      "inputs": [],
      "expected_artifact": {
        "kind": "file",
        "selector":
          "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/_rampup_notes.md",
        "evidence_required": "file exists AND contains '^## Key concepts'"
      },
      "step_execution": {
        "runtime": "codex",
        "model": "gpt-5.5",
        "effort": "high",
        "source": "execution_defaults.step",
        "reason": "Ramp-up is context gathering, not learner-facing copy."
      },
      "critic_execution": {
        "runtime": "codex",
        "model": "gpt-5.5",
        "effort": "xhigh",
        "source": "execution_defaults.critic",
        "reason": "No critic override was provided."
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
      "max_retries": 5
    }
  ]
}
```
