# Workflow contract: the five phases in detail

The skill runs five phases in order. Each phase has concrete inputs,
concrete outputs, and concrete failure modes. Judgment lives in model
prose; determinism lives in `scripts/run_stepwise.py`. This file names
which is which at every step.

Across every phase, apply `unblocking.md`: if the current role knows a safe,
bounded repair that preserves the confirmed manifest and role boundaries, do
that repair before asking the user. Stop discipline applies after known
unblocks and retry budgets are exhausted, not before.

## Phase 1 — Intake and interpretation

**Inputs**
- Verbatim user prompt.
- Current working directory (treated as the orchestrator repo root).
- The orchestrator's own session id (used only for run-directory collision
  safety; not for resumption).

**Outputs** (all written into `state.json`)
- `raw_instructions` + `raw_instructions_sha256`.
- `target_repo_path` (absolute, resolved).
- `target_process` — the named process or the explicit intent.
- `profile` — `strict` | `balanced` | `lenient`, per
  `strictness-profiles.md`.
- `forced_checks` — list of check names forced on regardless of profile.
- `stop_discipline` — `halt_and_ask` | `skip_and_continue` |
  `escalate_to_user` | `autonomous_repair`. `autonomous_repair` reopens
  an earlier step when a critic routes a fail upstream via
  `route_to_step_n`; see Phase 4c.
- `per_step_retry_cap` — integer derived from the profile.
- `execution_defaults` — base step and critic runtime/model/effort.
  Asked if missing, per `model-and-effort.md`.
- `execution_preferences` — optional user-specified routing preferences,
  unresolved until Phase 2 drafts real steps.

**Where judgment lives:** the agent's prose reasoning. Read the prompt,
decide profile and forced checks, resolve target repo, parse execution
defaults and routing preferences (ask if required defaults are missing).
Announce the interpretation before Phase 2.

**Where determinism lives:** the run-directory creation and the hash
computation. Both are script concerns.

**Failure modes**
- Target repo cannot be resolved → ask.
- Genuinely contradictory signals (strict + lenient in the same prompt
  with no tie-breaker) → ask.
- Missing execution default values → ask (one consolidated question).
- User's prompt names no process and no default is inferable → ask.

Do not proceed to Phase 2 with unresolved gaps. "I'll figure it out in
the next phase" is how heuristic drift starts.

## Phase 2 — Process grounding and manifest drafting

**Inputs**
- State from Phase 1.

**Outputs**
- `doctrine_paths` — the specific files the step sub-sessions should
  read. Usually `<target>/CLAUDE.md`, `<target>/AGENTS.md` (if present),
  and the SKILL.md for the named process.
- `manifest.json` — the full step manifest per `manifest-schema.md`,
  including resolved `step_execution` and `critic_execution` blocks.

**Where judgment lives:** the agent reads the doctrine and drafts the
manifest. This is the most load-bearing piece of prose in the skill.
The manifest must name real artifacts (no invented files) and real
skills (no hallucinated commands). If the doctrine is ambiguous, the
agent asks rather than guesses. After drafting the steps, resolve execution
preferences using `execution-routing.md`: feasibility, hard doctrine,
explicit step preference, semantic preference, then defaults.

**Where determinism lives:** reading the doctrine files (Read tool) and
writing `manifest.json` to the run directory (script-backed I/O).

**Failure modes**
- Named process does not exist in the target repo's doctrine → ask.
- A sub-step in the doctrine has no verifiable artifact → ask.
- Doctrine contradicts itself across files → surface the contradiction.
- A routing preference matches no steps, conflicts with hard doctrine, or is
  too ambiguous to apply responsibly → surface it before execution.
- A prompt, descriptor, or schema artifact is malformed but the intended
  meaning is clear from the confirmed inputs → repair the run-directory
  artifact, record the repair, and continue.

## Phase 3 — Plan confirmation

**Inputs**
- Interpretation announcement from Phase 1.
- Manifest from Phase 2.

**Outputs**
- User confirmation (`confirmed: true`) or adjustments.

**Where judgment lives:** nowhere new. This phase just prints and waits
(or prints and proceeds, by profile). The printed plan always includes a
step-by-step execution table with worker and critic runtime/model/effort plus
the source of any override.

**Gate behavior by profile**
- `strict`: always pause. Wait for explicit "go".
- `balanced`: print and pause once. Proceed on any affirmative reply.
- `lenient`: print and proceed. User can still interrupt.

**The plan is always printed.** Lenient does not mean invisible.

**Failure modes**
- User rejects → re-enter Phase 1 or Phase 2 with adjusted inputs.
  Do not try to "fix" the manifest in-place without rerunning the
  phase that generated it.

## Phase 4 — Step execution loop

For each step `n` from 1 to N:

### 4a. Spawn step sub-session

**Inputs**
- StepDescriptor for step `n`.
- `step_execution.runtime`, `step_execution.model`, `step_execution.effort`.
- `target_repo_path`.

**Actions (script-backed)**
- Compose the initial step prompt per `step-prompt-contract.md`.
- Build the invocation per `session-resume.md` for the chosen runtime.
- Run the subprocess. Close stdin (`< /dev/null`).
- Capture: exit code, stdout, the final-message file (`-o`), and the
  session id.
- Write all of the above to `steps/<n>/try-1/`.

**Failure modes**
- Subprocess crashes (non-zero exit) → retry policy treats this as
  a FAIL with crash evidence, subject to the same cap logic. If the
  crash is a known prompt/rendering/flag problem in the run machinery,
  repair that orchestration defect before charging the step attempt.
- Session id not captured (unexpected output shape) → the step cannot
  be resumed unless the id can be recovered from the raw stream. Inspect
  the stream for known Claude/Codex id shapes before marking
  `steps/<n>/try-1/session_id.txt` with `UNRECOVERABLE`.

### 4b. Spawn critic sub-session

**Inputs**
- The descriptor, the per-step doctrine paths, the try's artifacts
  and transcript, the `critic_contract_ref`, the profile.
- `critic_execution.runtime`, `critic_execution.model`,
  `critic_execution.effort`.

**Actions (script-backed)**
- Render the critic prompt per `critic-prompt.md`.
- Build the invocation per `session-resume.md` for the critic (Claude
  with `--json-schema`, or Codex with `--output-schema` and
  `--ephemeral`).
- Run the subprocess. Close stdin.
- Parse the StepVerdict from the structured output field (Claude) or
  the `-o` file (Codex).
- Write prompt, invocation, raw output, and parsed verdict into
  `steps/<n>/try-<k>/critic/`.

The critic recovery budget is one repaired retry for each distinct
orchestration defect. Do not spin: if the same repaired defect fails again,
record it as blocked and apply stop discipline.

**Failure modes**
- Critic subprocess crashes because of a known orchestration defect
  (schema shape drift, prompt rendering, command flag drift, missing
  run-directory file) → repair that defect inside the run directory,
  record the repair, and retry within the critic recovery budget.
- Critic subprocess crashes for an unknown runtime reason → retry the
  critic once. If it crashes again, record BLOCKED for the step and
  apply stop_discipline.
- Critic output does not parse against the schema → do not guess at
  the verdict. If the parse failure has a known safe repair, such as
  normalizing required-nullable schema fields for Codex or rerendering
  a malformed prompt, perform that repair and retry. If no bounded
  repair is known, record schema-parse-failure in the critic directory
  and BLOCK.
- Critic output is syntactically valid JSON but fails StepVerdict
  semantic validation → record `verdict.validation_errors.json` and
  retry the critic only if the error is an orchestration artifact. Do
  not coerce an invalid verdict into pass/fail by hand.
- Critic writes to disk (detected by diffing target repo before/after
  the critic call) → fail loud. Critics are read-only by contract.

### 4c. Act on the verdict

- `verdict=pass` → mark step `pass` (or `pass-after-retry` if `k>1`).
  Advance to step `n+1`.
- `verdict=fail` + `route_to_step_n = M` + `stop_discipline =
  autonomous_repair` → reopen step M:
  - If step M's retries are exhausted, halt with M's last verdict.
    Containment on `autonomous_repair` is M's own `max_retries`; a
    target that has been reopened up to its cap is treated like any
    other exhausted step.
  - Otherwise, `step-resume` step M with the critic's `resume_hint`
    (addressed to M, not to the current step). The critic's phrasing
    is what M reads. This counts as another try on M.
  - Run M's critic against the new try. On M fail, fall back into the
    normal fail handling for M (including another upstream route if
    the critic emits one).
- On M pass, mark M `repaired`. Then fresh `step-spawn` for each
    step from M+1 through the current step n (downstream sessions
    were built on the broken M artifact; resume would compound). Run
    each critic as usual using the confirmed manifest's resolved execution
    blocks. A fresh pass on a re-run step is `pass-after-repair`; a fresh
    fail re-enters the normal fail handling for that step.
- `verdict=fail` + non-null `route_to_step_n` but `stop_discipline` is
  anything other than `autonomous_repair` → treat like a retries-
  remaining fail (resume the current step with the same
  `resume_hint`) or, if retries are exhausted, apply `stop_discipline`
  as below. The routing field is a hint only; the orchestrator does
  not reopen upstream unless the discipline says so.
- `verdict=fail` + `route_to_step_n: null` + retries remaining → compose
  the resume prompt per `step-prompt-contract.md`. Build the resume
  invocation per `session-resume.md` (`claude -r <id>` or `codex exec
  resume <id>`). Run. Repeat 4b on the new attempt.
- `verdict=fail` + retries exhausted → apply `stop_discipline`:
  - `halt_and_ask`: mark step `blocked`. Stop the loop. Jump to
    Phase 5 with remaining steps marked `pending`.
  - `skip_and_continue`: mark step `skipped`. Advance.
  - `escalate_to_user`: print the verdict, ask the user how to
    proceed. Their decision selects `halt_and_ask` or
    `skip_and_continue` semantics for this step only.
  - `autonomous_repair`: with no routing hint and retries exhausted,
    fall back to `halt_and_ask` semantics — autonomous repair has
    nothing to repair with.
- `verdict=abstain` → first inspect whether the abstain reason names
  a known unblock. If the critic lacked a transcript path, artifact
  path, schema file, or read-only predicate that the orchestrator can
  reconstruct from the run directory, repair that and rerun the critic.
  Ask the user only when the evidence is genuinely unavailable or the
  required decision is outside the manifest.

**Where judgment lives:** step 4c's decision is mechanical (cap
arithmetic) once the verdict is in hand. The critic's verdict is the
authority. The orchestrator does not overrule it.

## Phase 5 — Report

**Inputs**
- `state.json`, `manifest.json`, per-step verdicts.

**Outputs**
- `report.md` in the run directory.
- A short console summary to the user: run-id, per-step status table,
  one notable critic finding (the most instructive failure, if any),
  what is pending if halted.

**Where judgment lives:** picking "the most instructive critic finding"
from the set of fails. Short prose, based on the verdict summaries.

**Where determinism lives:** the status table and the file I/O.

**No certification language.** The report states what happened. It
does not claim the work is "complete" or "approved"; that is for the
user to decide after reading it.

## What spans all phases

- The run directory is created at the start of Phase 1 and appended to
  throughout.
- `raw_instructions_sha256` and `execution_sha256` are checked at the start
  of each subprocess. A mismatch means the user mutated critical state
  mid-run; abort with a loud error and let them re-invoke.
- The orchestrator never edits target-repo files directly. If it finds
  itself tempted ("the step almost worked, I'll just fix this one
  thing"), it stops and writes a new step instead.
