# Run directory layout

One invocation creates one run directory. The directory holds everything needed
to audit the run: raw instructions, confirmed manifest, worker attempts, critic
observations, diagnostic conversations, root-cause records, learning consults,
and the final report.

## Location

```text
<orchestrator_repo_root>/.arch_skill/stepwise/runs/<run-id>/
```

`<run-id>` is `<UTC-iso-timestamp>-<8-char-hash>`, where the hash is the first
8 hex characters of `sha256(raw_instructions + target_repo_path)`.

The orchestrator repo root is the cwd when the skill was invoked. Do not write
run artifacts into the target repo.

On first write, add this marker to the orchestrator repo's `.gitignore` if no
matching marker already exists:

```text
.arch_skill/stepwise/runs/
```

Do not ignore all of `.arch_skill/`; `.arch_skill/stepwise/learnings/` is
intended to be visible and shareable.

## Full layout

```text
.arch_skill/stepwise/runs/<run-id>/
├── state.json
├── manifest.json
├── raw_instructions.txt
├── interpretation.md
├── steps/
│   └── <n>/
│       ├── descriptor.json
│       └── try-<k>/
│           ├── prompt.md
│           ├── origin.json
│           ├── invocation.sh
│           ├── stdout.final.json
│           ├── stream.log
│           ├── session_id.txt
│           ├── start_ts
│           ├── end_ts
│           ├── exit_code
│           ├── critic/
│           │   ├── prompt.md
│           │   ├── schema.codex.json
│           │   ├── invocation.sh
│           │   ├── stdout.final.json
│           │   ├── verdict.json
│           │   ├── verdict.validation_errors.json
│           │   ├── stream.log
│           │   └── exit_code
│           └── diagnostic/
│               ├── intake.md
│               ├── applicable-learnings.md
│               ├── turn-1.with-step-6.prompt.md
│               ├── turn-1.with-step-6.response.md
│               ├── turn-2.with-step-4.prompt.md
│               ├── turn-2.with-step-4.response.md
│               └── root-cause.md
└── report.md
```

Repairs executed against an upstream session as a result of another step's
diagnostic live in the upstream step's own `try-<k>/` directory. The
`origin.json` file records whether the attempt was a fresh spawn, repair
resume, or downstream respawn after upstream repair. Stepwise uses that fact
for repair-bounce accounting and audit truth; it does not infer intent from
the `try-<k>` name alone.

## state.json

```json
{
  "schema_version": 1,
  "run_id": "2026-04-22T18-30-02Z-8ab0c1de",
  "started_at": "2026-04-22T18:30:02Z",
  "ended_at": null,
  "status": "in_progress",
  "raw_instructions": "...",
  "raw_instructions_sha256": "...",
  "target_repo_path": "/abs/path",
  "profile": "strict",
  "forced_checks": ["no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 5,
  "diagnostic_turn_cap": 10,
  "execution": {
    "schema_version": 2,
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
    "execution_preferences": []
  },
  "execution_sha256": "...",
  "progress": []
}
```

Older local invocations may still pass `--models-json` to `init-run`; the
script converts that legacy input into `execution` before writing state. New
run directories should not contain top-level `models` or `models_sha256`.

## Per-step try directory

Every attempt gets its own try directory. `try-1` is the initial attempt;
later tries may be operational repairs or fresh downstream respawns after an
upstream repair. Diagnostic turns are stored under the try they diagnose and do
not create new tries.

`stream.log` is written incrementally while the child is running. Use it for
minutes-scale progress checks during long worker, critic, and diagnostic turns;
do not wait for `stdout.final.json` as the only sign of life.

`origin.json` disambiguates attempt meaning:

```json
{
  "schema_version": 1,
  "created_at": "2026-04-24T00:00:00Z",
  "kind": "repair-resume",
  "session_mode": "same-session",
  "consumes_repair_bounce": true,
  "triggered_by": {
    "diagnostic_path": "steps/6/try-1/diagnostic/root-cause.md"
  },
  "created_by_subcommand": "step-resume",
  "session_id": "...",
  "prompt_path": "/abs/run-dir/steps/6/try-2/prompt.md"
}
```

Valid `kind` values:

- `fresh`: a normal fresh worker session.
- `repair-resume`: an operational repair prompt resumed into the same session.
- `respawn-after-upstream`: a fresh downstream worker session after an
  upstream repair passed.

Only `repair-resume` consumes the repaired step's repair-bounce budget.
Respawning a downstream step after upstream repair is not a repair of the
downstream worker's own failed attempt; it is context hygiene.

`prompt.md` is the exact worker-facing prompt. `invocation.sh` is a
reproducible shell script. `session_id.txt` contains one session id or
`UNRECOVERABLE`.

## Helper subcommands

`latest-session --run-dir <dir> --step-n <n>` prints the latest try, session id,
session path, origin kind, and repair-bounce metadata for one step.

`upstream-for --run-dir <dir> --step-n <n>` reads the confirmed manifest and
prints earlier steps whose `expected_artifact.selector` exactly matches the
step's declared inputs. Inputs shaped as `source: /absolute/path` normalize to
the absolute path before exact matching. Unmatched inputs are returned
explicitly. The helper does not do fuzzy inference; Stepwise can reason about
the result, but the script only reports deterministic manifest facts.

`report-scaffold --run-dir <dir>` prints a report scaffold. Add `--write` to
write `report.md`. The scaffold supplies structure; Stepwise still writes the
judgment and plain-English explanation.

## report.md

Short, human-readable. Include:

- run id, target, process, profile,
- per-step status table,
- notable critic observations,
- diagnostic root cause if halted,
- applied accepted learnings,
- candidate learnings written,
- non-applicable learning near-misses,
- pending work.

Do not auto-delete run directories. If pruning is needed, ship a separate tool.
