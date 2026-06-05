# Fresh Consult Default Session Reuse Plan - 2026-06-05

## Goal

Make `$fresh-consult` cheaper and faster for follow-up questions on the same
line of inquiry by preserving the child session handle from the first consult
turn and resuming it by default for the second and third same-line requests.
On the fourth request in the same chain, start a new clean consult by default.

The important distinction is:

- First request: clean-start consult, but resumable.
- Second and third same-line requests: same child session resumes by default.
- Fourth same-line request: new clean-start consult by default.
- Explicit "cold", "independent", "fresh eyes", or changed runtime/model/effort:
  start a new chain.

This changes what "fresh" means in the skill. The first turn is still fresh
relative to the parent chat. Follow-up turns become bounded warm continuations
of that fresh consult, not brand-new stateless children.

## Current State Read

Live runtime package:

- `skills/fresh-consult/SKILL.md`
- `skills/fresh-consult/references/model-and-invocation.md`
- `skills/fresh-consult/references/consult-prompt-and-output.md`
- `skills/fresh-consult/agents/openai.yaml`

Install behavior:

- `Makefile` installs `skills/fresh-consult` to `~/.agents/skills/`,
  `~/.claude/skills/`, and `~/.gemini/skills/`.
- `Makefile` prunes `build/`, `prompts/`, `__pycache__/`, Python bytecode, and
  hook helper scripts from installed skill packages.
- The untracked `skills/fresh-consult/build/` tree is stale relative to the live
  top-level package and is not installed by the current `Makefile`.

Nearby behavior read:

- `$agent-delegate` already documents `fresh-one-shot`, `fresh-resumable`, and
  explicit `resume`; it writes `session_id.txt`, `resume_from.txt`, and
  `execution.json`.
- `$model-consensus` starts fresh resumable participant sessions and relays
  later turns through explicit session handles.
- `$stepwise` and `$arch-epic` are script-backed orchestration lanes; they prove
  the exact runtime resume mechanics but should not be copied into
  `$fresh-consult` as a controller.
- `$code-review` and `$codex-review-yolo` remain genuinely stateless/fresh review
  products and should keep using ephemeral/cold subprocesses.

Current `$fresh-consult` blocker:

- Codex consults use `codex exec --ephemeral`, which prevents a usable
  `thread_id` for future `codex exec resume`.
- The reference explicitly says not to use Claude `-r`, Codex `exec resume`,
  Cursor Agent `--resume`, Grok `--resume`, `agent resume`, `agent ls`, or
  latest-session selection.
- `consult-prompt-and-output.md` assumes the child has no session history every
  time.

## Design Principles

1. Keep `$fresh-consult` prompt-first.
   Do not add a runner, controller, detached monitor, or state machine.

2. Use run artifacts as handles.
   A resume turn still gets a new run directory. It points back to the prior
   chain/turn; it does not overwrite or reuse an old run directory.

3. Never use "latest session" selection.
   Auto-resume may only use a captured same-runtime session id from an
   unambiguous prior fresh-consult chain.

4. Preserve the read-only second-opinion lane.
   Resuming a consult is not implementation, repair, or multi-model consensus.
   If the child needs to edit files, use `$agent-delegate`. If two models should
   debate and converge, use `$model-consensus`.

5. Bound context reuse.
   Default `max_chain_turns = 3`: turn 1 fresh-resumable, turns 2 and 3 resume,
   turn 4 starts fresh. The user can explicitly say to continue anyway or force
   a cold start earlier.

6. Report the mode every time.
   The parent report should say whether the child was `fresh-resumable`,
   `resume`, `fresh-forced`, or `fresh-rotated`.

## Proposed Behavior

### Consult Modes

Add these modes to `$fresh-consult`:

- `fresh-resumable`: default for the first request in a consult chain. Starts
  clean, captures a session handle, and writes chain metadata.
- `resume`: default for the second and third same-line requests when a healthy,
  unambiguous prior chain exists.
- `fresh-forced`: used when the user asks for cold/fresh/independent review or
  when runtime/model/effort changes.
- `fresh-rotated`: used when the same-line chain has reached the default turn
  limit and the next request starts a new clean chain.

Do not keep `fresh-one-shot` as the ordinary default. A stateless one-shot is
still useful when the user explicitly wants a throwaway cold read, but it should
not be the default because it causes the session-handle loss this plan fixes.

### Same-Line Recognition

Treat a request as the same consult line when the parent can defend all of
these:

- Same work root.
- Same runtime, model, and effort.
- Same main artifact, claim, flow, or target question family.
- The user is asking a follow-up, clarification, rerun after local edits, or
  narrowed check that depends on the previous consult.
- The prior chain has a valid session id and is below the turn cap.

Start fresh instead when:

- The user asks for a cold, independent, fresh-eyes, or clean-room read.
- Runtime, model, or effort changed.
- Work root changed.
- The new artifact or question is materially different.
- Multiple possible prior chains match and the user did not provide a run path.
- The prior `session_id.txt` is missing, empty, or `UNRECOVERABLE`.
- The prior output was malformed or lacks the verdict footer.
- The chain is at turn 4 by default.

If the only problem is ambiguity between two candidate chains, ask one concise
question naming the candidate chain directories. Do not silently use a latest
session.

## Artifact Layout

Use one chain directory per line of inquiry:

```text
/tmp/fresh-consult/<consult-slug>-<UTC>-<random>/
  chain.json
  turn-01/
    prompt.md
    final.txt
    events.jsonl
    stderr.log
    execution.json
    session_id.txt
  turn-02/
    prompt.md
    final.txt
    events.jsonl
    stderr.log
    execution.json
    session_id.txt
    resume_from.txt
  turn-03/
    ...
```

For explicit parallel consults, keep the current group concept but give each
child its own chain or child chain directory:

```text
/tmp/fresh-consult/parallel-<group-slug>-<UTC>-<random>/
  child-a/
    chain.json
    turn-01/
      ...
  child-b/
    chain.json
    turn-01/
      ...
```

Parallel resume should be conservative. Resume a child only when the follow-up
names the child, chain directory, or exact child question. Otherwise start
fresh or ask.

### `chain.json`

Suggested fields:

```json
{
  "schema_version": 1,
  "skill": "fresh-consult",
  "chain_id": "<stable id>",
  "consult_slug": "<short slug>",
  "created_at_utc": "2026-06-05T00:00:00Z",
  "updated_at_utc": "2026-06-05T00:00:00Z",
  "work_root": "<absolute path>",
  "runtime": "claude | codex | agent | grok",
  "model": "<resolved model>",
  "effort": "<resolved effort or encoded-in-model>",
  "max_chain_turns": 3,
  "user_named_artifacts": ["<path or artifact>"],
  "artifact_fingerprint": "<hash of normalized artifact list>",
  "consult_objective": "<one-line objective>",
  "turns": [
    {
      "turn": 1,
      "mode": "fresh-resumable",
      "run_dir": "<absolute path>",
      "session_id_path": "<absolute path>",
      "session_id": "<captured id or UNRECOVERABLE>",
      "verdict": "pass | pass-with-notes | fail | inconclusive | malformed",
      "created_at_utc": "2026-06-05T00:00:00Z"
    }
  ]
}
```

Do not put secrets, pasted credentials, or raw full prompts in `chain.json`.
The prompt body stays in `prompt.md`.

### `execution.json`

Write this per turn before invocation:

```json
{
  "schema_version": 1,
  "mode": "fresh-resumable | resume | fresh-forced | fresh-rotated",
  "runtime": "claude | codex | agent | grok",
  "model": "<resolved model or reused-from-session>",
  "effort": "<resolved effort or reused-from-session>",
  "work_root": "<absolute path>",
  "chain_dir": "<absolute path>",
  "turn": 2,
  "resume_from": "<prior turn run dir or none>",
  "restart_reason": "none | user_forced_cold | chain_turn_limit | changed_execution | missing_session | ambiguous_chain"
}
```

## Runtime Command Changes

### Codex Fresh Resumable

Default Codex first turns should remove `--ephemeral`:

```bash
codex exec \
  --disable codex_hooks \
  -C "<work_root>" \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --model "<resolved_model>" \
  -c model_reasoning_effort='"<resolved_effort>"' \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Capture the first `thread.started.thread_id` from `events.jsonl` into
`session_id.txt`. If missing, write `UNRECOVERABLE`, mark the turn malformed,
and preserve the run directory.

### Codex Resume

```bash
codex exec resume "<thread_id>" \
  --disable codex_hooks \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --json \
  -o "$FINAL_PATH" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Do not pass `-C` or `--cd` on resume. Codex carries the original cwd. Do not
use `--last`.

By default, require the same runtime/model/effort for auto-resume. If the user
explicitly wants to force a different model or effort into a resumed Codex
thread, that should be explicit in the prompt and final report, not automatic.

### Claude Fresh Resumable And Resume

The first-turn Claude command shape can stay mostly the same. The required
change is to capture the final `type=result` event's `session_id` into
`session_id.txt`.

Resume with:

```bash
claude -p \
  --output-format stream-json \
  --verbose \
  --include-partial-messages \
  --include-hook-events \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model "<resolved_model>" \
  --effort "<resolved_effort>" \
  -r "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Run Claude resumes from the same `work_root` used by the original run. Use
`-r`, never `--continue`.

### Cursor Agent Fresh Resumable And Resume

Keep support for Cursor Agent as `composer-2.5-fast`, but decide during
implementation whether the consult command should remain the current
`--force --sandbox disabled` shape or move to a more read-only Cursor shape.
The current live fresh-consult docs use edit-capable Cursor flags even though
the prompt is read-only; this is a pre-existing issue worth fixing only if the
local CLI supports a reliable read-only mode.

Resume with explicit session id only:

```bash
agent -p \
  --force \
  --sandbox disabled \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "composer-2.5-fast" \
  --resume "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Do not use `--continue`, `agent resume`, `agent ls`, or latest-session
selection.

### Grok Fresh Resumable And Resume

Fresh shape remains the same, but capture the final `type=end.sessionId` into
`session_id.txt`.

Resume with:

```bash
RUST_LOG=off grok \
  --cwd "<work_root>" \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model "<resolved_grok_model>" \
  --effort "<resolved_effort>" \
  --output-format streaming-json \
  --resume "<session_id>" \
  --prompt-file "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Use `--resume <session_id>` only. Do not use latest-session selection.

## Prompt Contract Changes

Update `consult-prompt-and-output.md` so it is conditional:

Fresh first turn:

```markdown
You are performing an independent clean-start consult on <subject>.
You have no prior parent chat context. Read the artifacts directly from disk.
Your job is to answer the user's ask for the parent agent, not to fix files.
```

Resume turn:

```markdown
You are resuming the same fresh-consult session for <subject>.
Use your existing child-session history plus the new user ask below. You still
do not have the parent chat context beyond what is in this prompt. Re-read
files when the answer depends on current repo state. Do not assume old file
contents are still current.
```

Add a `Consult Mode` block:

```markdown
# Consult Mode

- Mode: fresh-resumable | resume | fresh-forced | fresh-rotated
- Chain directory: <path>
- Turn: <n>
- Resume source: <prior turn dir, session id, or "none">
- Reason for fresh start: <none or reason>
```

Keep the same verdict footer. Add only one new parent-report requirement:
report the consult mode, chain directory, run directory, and session id when
captured.

## Skill Text Changes

### `skills/fresh-consult/SKILL.md`

Patch:

- Description: replace "fresh subprocesses" with "clean-start read-only consults
  with bounded same-session follow-up reuse by default".
- Opening section: explain that first turns are fresh relative to parent chat,
  while second/third same-line turns resume by default.
- `When not to use`: keep the implementation/delegation/model-consensus
  boundaries; change "child expected to continue a long-running workflow" so it
  does not reject normal same-line consult follow-ups.
- Non-negotiables: add the default chain behavior and no-latest-session rule.
- First move: after resolving runtime/model/effort, search for an unambiguous
  healthy prior chain before creating a new one.
- Workflow: add "select continuity" before "run the child".
- Output expectations: include mode, chain dir, run dir, and session id.

### `skills/fresh-consult/references/model-and-invocation.md`

Patch:

- Add `Consult Continuity` section.
- Replace the single Codex command with `Codex Fresh Resumable`, `Codex Forced
  Fresh One-Shot`, and `Codex Resume`.
- Add session-id capture rules for all runtimes.
- Replace the current no-resume sentence with explicit no-latest-session and
  bounded-resume rules.
- Add failure cases for missing/invalid `session_id.txt`, ambiguous chain, and
  chain turn cap.

### `skills/fresh-consult/references/consult-prompt-and-output.md`

Patch:

- Make the prompt skeleton mode-aware.
- Keep the read-only contract and verdict footer.
- Remove or rewrite the anti-pattern "Reuse old run directories across
  consults" to "Do not overwrite old turn directories; a resume turn gets a new
  run directory that points back to the previous turn."

### `skills/fresh-consult/agents/openai.yaml`

Patch:

- Mention bounded default follow-up resume.
- Keep provider routing exact.
- Include "say whether the consult was fresh or resumed" in the default prompt.

### `README.md`

Patch:

- Inventory bullet for `fresh-consult`.
- Installed-surface paragraph where `fresh-consult` behavior is summarized.
- Dedicated `### fresh-consult` section.
- Boundary paragraph that currently says `agent-delegate` owns explicit resume.
  Keep `agent-delegate` as editful resume owner, but mention that
  `fresh-consult` now owns bounded read-only follow-up resume.

### `docs/arch_skill_usage_guide.md`

Patch the `fresh-consult` section and any installed-surface summary so the docs
match README behavior.

### `skills/fresh-consult/build/`

Do not patch by default. It is untracked and pruned from installed packages.
If a future implementation intentionally restores a build-source workflow, make
that a separate explicit task and update the generated build output in the same
pass.

## Validation Plan

For a docs/doctrine-only implementation without a new script:

1. Re-read every touched file.
2. Run package validation:

   ```bash
   npx skills check
   ```

3. Search for stale no-resume doctrine:

   ```bash
   rg -n 'Do not use Claude `-r`|Codex `exec resume`|Cursor Agent `--resume`|Grok `--resume`|is a cold read, not a resumed conversation|--ephemeral' skills/fresh-consult README.md docs/arch_skill_usage_guide.md
   ```

4. Search for new runtime handles and docs consistency:

   ```bash
   rg -n 'fresh-resumable|fresh-rotated|session_id.txt|chain.json|resume_from.txt|latest-session' skills/fresh-consult README.md docs/arch_skill_usage_guide.md
   ```

5. Verify install docs and Makefile still agree on the installed surface:

   ```bash
   rg -n "fresh-consult" README.md Makefile docs/arch_skill_usage_guide.md
   ```

6. No real external model smoke test is required for a plan/doctrine change,
   because it would spend model budget. Before a final implementation ships,
   optionally run one cheap smoke per changed runtime if the user explicitly
   wants runtime proof.

If implementation adds a helper script:

- Keep it narrow: manifest read/write, candidate listing, and session-id
  extraction only.
- Add focused tests for deterministic behavior.
- Keep script stdout to a verdict plus handles, not full manifest dumps.
- Still run `npx skills check`.

## Risks And Mitigations

Risk: Resume weakens the cold-read value.

Mitigation: first turn remains clean; explicit cold/fresh/independent language
forces `fresh-forced`; turn 4 rotates by default.

Risk: The parent resumes the wrong child.

Mitigation: no latest-session selection, require same runtime/model/effort and
same work root, use chain metadata, and ask when candidate chains are ambiguous.

Risk: A resumed consult trusts stale file contents.

Mitigation: resume prompt tells the child to re-read files when current repo
state matters.

Risk: The skill drifts into `$model-consensus`.

Mitigation: one consult child can answer follow-ups, but it does not debate
with siblings or converge multiple models. Multi-model iterative agreement stays
with `$model-consensus`.

Risk: The skill drifts into `$agent-delegate`.

Mitigation: the prompt remains read-only and says not to fix files. If the child
must edit, route to `$agent-delegate`.

Risk: `/tmp/fresh-consult` cleanup removes the chain.

Mitigation: if the chain dir or `session_id.txt` is gone, start fresh and report
`restart_reason=missing_session`.

Risk: Existing generated `build/` content confuses reviewers.

Mitigation: name it as stale/uninstalled in the plan and leave it alone unless
the build/source workflow is explicitly restored.

## Recommended Implementation Order

1. Patch `skills/fresh-consult/references/model-and-invocation.md`.
2. Patch `skills/fresh-consult/references/consult-prompt-and-output.md`.
3. Patch `skills/fresh-consult/SKILL.md`.
4. Patch `skills/fresh-consult/agents/openai.yaml`.
5. Patch `README.md`.
6. Patch `docs/arch_skill_usage_guide.md`.
7. Run the validation plan above.
8. Review the final diff for peer-boundary drift against `$agent-delegate`,
   `$model-consensus`, `$code-review`, `$codex-review-yolo`, `$stepwise`, and
   `$arch-epic`.

## Open Decisions For Review

1. Default chain length: recommend `max_chain_turns = 3`, meaning request 4
   starts fresh.
2. Cursor Agent consult flags: decide whether to keep the current live
   `--force --sandbox disabled` shape or switch consults to a more read-only
   Cursor mode if local CLI support is reliable.
3. Helper script: recommend no script in v1. Add one only if manual
   chain-candidate selection proves brittle after the doctrine change.
4. Build output: recommend leaving untracked `build/` alone unless the build
   source workflow becomes part of this implementation.
