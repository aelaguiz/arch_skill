# Classify Amir's prompts for overbuild pushback

## Purpose

Amir wants to build an "overbuild audit" skill that checks a plan or an implementation for overbuilding. Before writing it, he needs evidence: every kind of overbuilding he has caught his coding agents doing, and how often. Your batch holds prompts he typed to Codex, Claude Code, and Prime Agent sessions. A regex pre-filter selected them, so many are false positives: poker "card abstraction", a test "harness" he actually wants, a "fallback" he asks for, "cleanup" of disk space, "minimal" as a neutral word. Your job is to read each one and judge it.

## Input

A JSONL file. Each line: `id`, `m` (machine), `rt` (runtime), `date`, `cwd` (last path segment, may be empty), `len` (original length), `text`. Long prompts were cut to the windows around keyword hits, joined with ` … `.

Read the whole file in pieces (for example 120 lines at a time with the Read tool's offset and limit). Do not skip lines. Do not sample.

## Judgment per prompt

`verdict`:
- `yes`: Amir is pushing back on something built, planned, or proposed that is more than needed. This includes: asking "why do we need X", "where are we overbuilding", ordering X ripped out, demanding the simplest shape, forbidding a pattern in advance because agents keep doing it, complaining about unrequested work, or asking an agent to audit for overbuild.
- `partial`: the prompt mixes a real overbuild concern with other intent, or the concern is implied but plain.
- `no`: anything else. Most false positives are domain vocabulary or neutral requests.

Only emit lines for `yes` and `partial`. Count the `no` lines.

For each `yes`/`partial`, record:
- `cats`: one or more category keys from the seed list below. If none fits, invent a short kebab-case key prefixed `new-` and define it in your final report.
- `target`: what he is auditing: `plan` (plan, spec, design doc, proposal), `impl` (code, diff, PR, running system), `prompt` (skill, agent instructions, goal prompt, doc prose), `process` (how the agent works: worktrees, subagents, tests it runs, steps it takes), or `unclear`.
- `mode`: `reactive` (he caught it after the fact), `preemptive` (he forbids it before it happens, standing rule in a goal or dispatch prompt), or `audit-request` (he asks an agent to hunt for overbuild).
- `quote`: his own words, 30 words or fewer, verbatim (fix nothing, keep profanity).
- `check`: one line naming the question or test he is effectively applying, phrased as a reusable check (for example "Is there a second path that stays live after the new one lands?").

## Seed categories

Use these keys. A prompt can carry several.

- `unrequested-scope`: work, features, files, or side quests nobody asked for.
- `outside-diff`: changes to files or subsystems outside the task (unrelated analytics, iOS runner, other screens).
- `speculative-generality`: building for hypothetical futures, presuming needs before first use, configurability nobody needs yet.
- `proof-ceremony`: guarantees, certificates, receipts, hashes, golden sets, output schemas, verification layers heavier than the risk.
- `test-sprawl`: test harnesses, fixtures, rehearsals, extra test tiers, tests for things that do not need them.
- `fallback-masking`: fallbacks or silent degradation that hide failure where a hard fail is wanted.
- `compat-dual-path`: backward compatibility, shims, legacy path kept beside new path, parallel implementations, two baselines, migration layers.
- `retry-repair-machinery`: retries, background repair passes, recovery loops, self-healing, reconciliation jobs.
- `knobs-flags-env`: config options, feature flags, env vars, toggles, CLI flags, optional modes.
- `extra-state`: history windows, lineage, revisions, tracking tables, caches, stored bookkeeping that could be derived.
- `new-abstraction`: wrappers, frameworks, registries, controllers, state machines, runners, helper layers, indirection.
- `defensive-guards`: caps, validation, protection, guard clauses, gates beyond what the contract needs.
- `diagnostics-residue`: temporary logging, instrumentation, debug output left behind.
- `process-overhead`: extra worktrees, subagents, plans, ledgers, phases, steps, approvals in how the agent works.
- `doc-prompt-bloat`: long or padded docs, plans, prompts, skills, agent instructions; asking for the two-sentence version.
- `heuristic-over-signal`: inferred heuristics where stated data or a direct signal exists.
- `authority-plumbing`: permission, authority, approval, or gate plumbing.
- `duplicate-owner`: a second copy or second owner of the same truth or behavior.
- `generic-simplify`: a plain "make it simpler / smallest shape / rip it out" with no finer category.

## Output

1. Write your labels to the output path you were given, one JSON object per line: `{"id","verdict","cats","target","mode","quote","check"}`. Write with the Write tool once at the end, or in a few appends via Bash heredoc. Keep JSON valid.
2. Final reply (under 700 words):
   - totals: lines read, yes, partial, no;
   - count per category (yes + partial);
   - count per target and per mode;
   - any `new-` categories with one-line definitions and counts;
   - for the five biggest categories, the two best verbatim quotes each with id and date;
   - recurring phrasings he uses to ask the question (for example "where are we overbuilding", "rip it out"), with rough counts.

Do not modify any file other than your output file. Do not contact any other machine.
