# Arbiter And Review

`plan-swarm` uses review to hold quality without serializing all implementation
work.

## Arbiter

The arbiter is a delegated observation-only worker. It compares the phase
contract, execution ledger, current diff, worker logs, and proof evidence.
The arbiter prompt must include: "Maximize parallelism with native subagents or
parallel-agent features provided by your current coding harness. Do not
manually spawn separate coding-harness executables, or invoke skills whose main
effect is to shell out to `codex`, `claude`, `agent`, or `grok`, from inside
this child prompt unless the parent explicitly assigns that action."
Run arbiter, consult, and review work through Codex GPT/GBT or Claude
Fable/Opus.
Do not route review through Cursor Agent just because implementation used
Cursor Composer, do not route review through Grok just because implementation
used Grok, and do not pass model ids across runtimes.

Ask it:

- Was the phase implemented exactly as specified?
- Did the work stop at the requested boundary?
- Is the implementation architecturally clean?
- Are owner boundaries, persistence, QA, and cleanup obligations covered?
- Which findings are in-scope blockers versus unrelated old debt?

Ask for an exhaustive phase-scope pass. The goal is a useful batch of findings
for repair routing, not the first defect the reviewer notices.

The arbiter does not edit files.

## Thermonuclear Gate

Run `thermo-nuclear-code-quality-review` before phase closure unless the user
explicitly disables it. Treat findings as input, not automatic scope expansion.
The review should produce enough detail to route repairs: owner surface,
affected files, why the finding is in scope, and what proof would close it.

## Triage

Each finding becomes:

- `accepted`: in-scope and must be repaired.
- `rejected`: incorrect or contradicted by evidence.
- `deferred`: real but outside the requested phase.

Accepted findings route back to implementation workers, usually by resuming the
related healthy session. Group accepted findings into repair or verification
waves before launching follow-up work. The parent may include likely fix paths
or evidence hints in worker prompts, but workers own source edits and assigned
verification. Record the rationale for rejected or deferred findings.
