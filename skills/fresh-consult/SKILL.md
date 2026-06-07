---
name: fresh-consult
description: "Invoke one or more Claude Opus, Codex GPT/GBT, Cursor Composer, or Grok subprocesses for prompt-engineered read-only second opinions with strict pass/fail verdicts. First turns start clean from disk and the consult prompt; second/third same-line follow-ups resume the captured child session by default; turn four starts fresh unless the user asks to continue. Use for cold reads, bounded follow-up consults, parallel consults, flow consistency audits, completion checks, readability/confusion checks, or general second opinions. Ask once if runtime, model, effort, or target is missing; run hook-suppressed where supported and unsandboxed; report mode, evidence, verdict, session id, and directories. Do NOT use for Codex `-p yolo` reviews (`codex-review-yolo`), ordered orchestration (`stepwise`/`arch-epic`), or implementation/fixing (`agent-delegate`)."
metadata:
  short-description: "Fresh Claude, Codex, Cursor, or Grok opinion"
---

# Fresh Consult

Use this skill when the user or another skill needs one or more read-only second
opinions from Claude Opus, Codex GPT/GBT, Cursor Composer, or Grok
subprocesses. The first turn in a consult line starts clean from disk and the
consult prompt, not from the current parent chat history. The second and third
same-line follow-ups resume the captured child session by default so the parent
does not pay full startup cost again. The fourth same-line request starts a new
clean consult by default.

The child is a strict yes/no arbiter. If the user's ask is not fully satisfied,
the verdict is `fail` with specific reasons.

This is a prompt-engineering skill. It ships no scripts, shims, hook
controllers, state machines, parsers, or install-time automation.

## When to use

- "Ask Claude for a cold read of this flow."
- "Use Codex to audit whether this plan phase is actually complete."
- "Run a fresh consult for consistency on these skills."
- "Run three parallel fresh consults on this plan."
- "Resume that consult and ask it to re-check the edited section."
- "Get a second opinion on whether this doc is linear and not confusing."
- "Have a clean model check whether the implementation matches the checklist."
- "Use Cursor Agent Composer 2.5 Fast for a cold read of this artifact."
- "Use Grok Build for a fresh consult on this implementation claim."
- Another skill needs an independent read before it decides whether to proceed.

## When not to use

- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The user asks Cursor Agent to run GPT/GBT or Claude models. Cursor Agent is
  Composer-only; GPT/GBT runs through Codex and Opus runs through Claude Code.
- The user asks Grok to run GPT/GBT, Claude, or Cursor-only model ids. Grok
  uses `grok-build` or `grok-composer-2.5-fast`.
- The work is an ordered subprocess workflow with manifests, critics, repair
  loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The child is expected to edit files or fix issues. Use `$agent-delegate` for
  a one-shot operational subprocess task.
- The child is expected to continue implementation, repair, debate, or a
  long-running workflow beyond bounded read-only consult follow-ups. Use the
  matching workflow skill, `$model-consensus`, or native goal mode instead.
- There is no concrete artifact, claim, question, or target path to inspect.
- The requested runtime CLI is not installed.

## Non-Negotiables

- Resolve each consult objective, exact user-named artifacts or target paths,
  hard constraints, and the work root before launching child processes.
- Runtime, model, and effort must be known. Codex runs GPT/GBT/OpenAI models,
  Claude Code runs Opus, Cursor Agent runs `composer-2.5-fast`, and Grok CLI
  runs `grok-build` or `grok-composer-2.5-fast`. If any value is missing or
  ambiguous, ask one consolidated question before invoking.
- Never run GPT/GBT or Claude models through Cursor Agent or Grok. Do not pass
  Grok model ids to Codex, Claude, or Cursor Agent.
- Treat model text as intent, not a fuzzy alias. Preserve exact family and
  numeric version; never silently substitute a nearby model.
- Run the child fresh, hook-suppressed where the runtime supports it, and
  unsandboxed per this repo's convention on the first turn of a line. The child
  prompt enforces read-only behavior, not a sandbox.
- Use bounded continuity by default: turn 1 is `fresh-resumable`, turns 2 and 3
  are `resume` when the same-line prior chain is healthy and unambiguous, and
  turn 4 is `fresh-rotated` unless the user explicitly asks to continue.
- Strictness is an acceptance bar, not a fresh-start reason. Do not avoid
  resume just because the child must be strict.
- Never use latest-session selection. Resume only with the exact same-runtime
  session id captured from a prior fresh-consult chain.
- For a single consult line, create one chain directory under
  `/tmp/fresh-consult/` with `chain.json` and one `turn-XX/` run directory per
  request. Keep each turn's `prompt.md`, `final.txt`, `events.jsonl`,
  `stderr.log`, `execution.json`, and `session_id.txt` there; resume turns also
  get `resume_from.txt`.
- For explicit parallel consults, create one group directory under
  `/tmp/fresh-consult/` and one ordinary child chain per consult. Do not add a
  controller, detached monitor, or new runner surface.
- Brief the child with enough context to reason independently: include the raw
  consult ask, consult mode, work root, exact user-named artifacts or target
  paths, hard constraints, and the report contract. The child chooses what
  evidence to inspect beyond those inputs.
- Do not paste secrets into prompts. If a token is needed, source it into the
  child environment and tell the child which environment variable to read.
- Do not ask the child to fix the issues it finds. Report back to the parent;
  fixes are a separate step.
- The child verdict is `pass` or `fail` only. If the answer is not a clean yes,
  including missing evidence or uncertainty, the child must fail and explain why.
- If the child reports a failure reason, spot-check the cited evidence before
  acting on it or presenting it as verified truth.

## First Move

1. Read `references/model-and-invocation.md`.
2. Read `references/consult-prompt-and-output.md`.
3. Identify the consult objective or parallel consult objectives, work root,
   exact user-named artifacts or target paths, hard constraints, and requested
   runtime/model/effort from the user's words.
4. If runtime/model/effort or consult target is incomplete, ask one question
   that names exactly what is missing and what it controls.
5. Confirm the selected CLI exists with `command -v codex`, `command -v
   claude`, `command -v agent`, or `command -v grok`.
6. Select continuity: reuse an unambiguous healthy same-line chain for turns 2
   and 3, even for strict checks. Start fresh only when forced or rotated, and
   ask only if multiple candidate chains plausibly match.
7. Create the chain, turn, or group directories and write each consult prompt
   to its own `prompt.md`.
8. Invoke each child with the exact command shape from the invocation reference.

## Workflow

1. **Shape the consult.** State the user's question, the bar for a useful
   answer, the work root, and the exact artifacts or target paths the user
   named.
2. **Resolve execution.** Map the raw model phrase to
   `runtime=<claude|codex|agent|grok>`, `model=<runnable id>`, and
   `effort=<level-or-encoded-in-model>`.
   Announce the mapping before execution.
3. **Select continuity.** Use `fresh-resumable`, `resume`, `fresh-forced`, or
   `fresh-rotated` according to the chain rules in the invocation reference.
   Never use latest-session selection.
4. **Select single or parallel.** Use the single-child path by default. Use a
   parallel group only when the user asks for parallel consults or gives
   multiple consult questions.
5. **Run the child or children.** Use fresh-resumable or exact-session resume
   subprocesses, disabled hooks where supported, no sandbox, namespaced
   chain/turn directories, and live event capture.
6. **Monitor patiently.** Normal consults often take 5+ minutes; broad repo
   reads, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live
   `events.jsonl` and `stderr.log` every few minutes, not every few seconds.
7. **Consume the result.** Read `final.txt`, locate the verdict footer, update
   `chain.json` and `session_id.txt`, and inspect `events.jsonl`/`stderr.log`
   when the final output is missing or malformed.
8. **Report upstream.** For one child, lead with the verdict, failure reasons,
   confidence, mode, chain directory, run directory, and session id after
   spot-checking. For a parallel group, report one compact child-by-child table
   plus a short synthesis of agreement and disagreement. Include all chain and
   run directory paths.

## Output Expectations

- A concise parent-facing report:
  - runtime/model/effort used
  - consult mode: `fresh-resumable`, `resume`, `fresh-forced`, or
    `fresh-rotated`
  - strict `pass` or `fail` verdict, or one verdict per child for parallel
    groups
  - failure reasons or `none`
  - evidence the child says it read
  - confidence and limits
  - chain directory, run directory, and session id when captured or reused
  - group directory plus child chain/run directories for parallel groups
- If the child output is missing or malformed, say that plainly and preserve the
  run directory for debugging. Do not invent a verdict.
- If the child is wrong on a failure reason, say so explicitly and cite the
  evidence that contradicts it.

## Reference Map

- `references/model-and-invocation.md` - runtime/model/effort resolution and
  exact child-runtime command shapes
- `references/consult-prompt-and-output.md` - consult prompt skeleton, verdict
  footer, report rules, and anti-patterns
