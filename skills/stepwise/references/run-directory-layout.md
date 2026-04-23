# Run directory layout

One invocation of the skill creates one run directory. The directory holds
everything needed to audit the run after the fact: the user's verbatim
instructions, the confirmed manifest, each step's subprocess output, each
critic's verdict, and the final report.

## Location

```
<orchestrator_repo_root>/.arch_skill/stepwise/runs/<run-id>/
```

`<run-id>` is `<UTC-iso-timestamp>-<8-char-hash>`, where the hash is the
first 8 hex characters of `sha256(raw_instructions + target_repo_path)`.
This gives a human-readable sort order and per-user collision safety.

The orchestrator repo root is the cwd when the skill was invoked. Do not
write run artifacts into the target repo — the target repo is where the
steps produce their real outputs; the run directory is orchestration
bookkeeping.

Add `.arch_skill/` to the orchestrator repo's `.gitignore` on first write
if not already present.

## Full layout

```
.arch_skill/stepwise/runs/<run-id>/
├── state.json                    # run state; machine-readable
├── manifest.json                 # confirmed step manifest (see manifest-schema.md)
├── raw_instructions.txt          # verbatim user prompt
├── interpretation.md             # Phase 1 announcement text
├── steps/
│   └── <n>/                      # one directory per step (1-indexed)
│       ├── descriptor.json       # the manifest's StepDescriptor for this step
│       └── try-<k>/              # one per attempt (1-indexed)
│           ├── invocation.sh     # exact command that ran
│           ├── stdout.final.json # claude -p result OR codex -o output
│           ├── stream.log        # claude's lifecycle events or codex JSONL events
│           ├── session_id.txt    # single line with the session id
│           ├── start_ts          # ISO-8601 start
│           ├── end_ts            # ISO-8601 end
│           ├── exit_code         # numeric exit
│           └── critic/
│               ├── prompt.md
│               ├── invocation.sh
│               ├── stdout.final.json  # claude result OR codex schema output
│               ├── verdict.json       # the StepVerdict document
│               ├── stream.log
│               └── exit_code
└── report.md                     # Phase 5 human-readable final report
```

## state.json

```json
{
  "schema_version": 1,
  "run_id": "2026-04-22T18-30-02Z-8ab0c1de",
  "started_at": "2026-04-22T18:30:02Z",
  "ended_at": "2026-04-22T18:41:17Z",
  "status": "completed" | "halted" | "in_progress",
  "raw_instructions": "...",
  "raw_instructions_sha256": "...",
  "target_repo_path": "/abs/path",
  "profile": "strict",
  "forced_checks": ["no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "models": { "step_model": "...", "step_effort": "...",
              "critic_model": "...", "critic_effort": "..." },
  "models_sha256": "...",
  "progress": [
    {
      "n": 1,
      "status": "pass" | "pass-after-retry" | "blocked" | "skipped" | "pending",
      "attempts": 1,
      "final_verdict_path":
        "steps/1/try-1/critic/verdict.json"
    }
  ]
}
```

`raw_instructions_sha256` and `models_sha256` pin the orchestrator's
interpretation. If either changes during the run, the run is aborted and
restarted — no silent rewriting mid-flight. (Same discipline as arch-loop's
`raw_requirements_hash`.)

## Per-step try directory

Every attempt gets its own try directory, even if the prior try was a pass
(which shouldn't happen, but guards against accidental re-runs). Structure
is flat — no nesting beyond what is listed. `try-1` is the initial attempt,
`try-2` is the first resume, and so on.

`invocation.sh` is a reproducible shell script — one line that would
re-run the subprocess exactly. This is what an auditor uses to reproduce a
suspicious run without re-launching the orchestrator.

`session_id.txt` contains one line: the session id (Claude) or thread_id
(Codex). Downstream tries read this file to construct their resume command.

## report.md

Short, human-readable. Example skeleton:

```
# stepwise run report

Run: 2026-04-22T18-30-02Z-8ab0c1de
Target: /Users/aelaguiz/workspace/lessons_studio
Process: Track 3 / Section 3 / Lesson 2
Profile: strict (forced: skill_order_adherence, no_fabrication)

## Steps

| # | Label                                   | Status             | Tries |
|---|------------------------------------------|--------------------|-------|
| 1 | Ramp up on track 3 / section 3 context   | pass               | 1     |
| 2 | Draft lesson 2 outline                   | pass-after-retry   | 2     |
| 3 | Fill lesson 2 body                       | pass               | 1     |

## Notable critic findings

Step 2, try 1: FAIL on `artifact_exists`. The step claimed to write
outline.md but the file was absent. Resumed; try 2 wrote the file and
passed.

## Status

completed
```

If `halted`, the report names the halted step, the final verdict, and
what the user would need to decide to unblock.

## Cleanup

Do not auto-delete run directories. An auditor may come back hours or
days later. If disk pressure becomes real, ship a separate prune tool —
do not entangle pruning with the orchestrator's critical path.
