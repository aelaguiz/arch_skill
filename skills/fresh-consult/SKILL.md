---
name: fresh-consult
description: "Invoke one or more fresh Claude Opus, Codex GPT/GBT, or Cursor Composer subprocesses for prompt-engineered read-only second opinions with clean context. Use when the user or another skill asks for a cold read, parallel consults, external consult, flow consistency audit, completion check, readability/confusion check, or general second opinion. Ask once if runtime, model, effort, or consult target is missing; run hook-suppressed where supported and unsandboxed; report each child result back. Do NOT use for deterministic code-review coverage (`code-review`), Codex `-p yolo` reviews (`codex-review-yolo`), ordered subprocess orchestration (`stepwise`/`arch-epic`), or implementation/fixing (`agent-delegate`)."
metadata:
  short-description: "Fresh Claude, Codex, or Composer second opinion"
---

# Fresh Consult

Use this skill when the user or another skill needs one or more clean second
opinions from fresh Claude Opus, Codex GPT/GBT, or Cursor Composer
subprocesses. Each child model starts from disk and the consult prompt, not from
the current chat history, so it can catch confusion, drift, missing completion,
or weak reasoning the parent may have normalized.

This is a prompt-engineering skill. It ships no scripts, shims, hook
controllers, state machines, parsers, or install-time automation.

## When to use

- "Ask Claude for a cold read of this flow."
- "Use Codex to audit whether this plan phase is actually complete."
- "Run a fresh consult for consistency on these skills."
- "Run three parallel fresh consults on this plan."
- "Get a second opinion on whether this doc is linear and not confusing."
- "Have a clean model check whether the implementation matches the checklist."
- "Use Cursor Agent Composer 2.5 Fast for a cold read of this artifact."
- Another skill needs an independent read before it decides whether to proceed.

## When not to use

- The user wants deterministic code-review coverage with lens fan-out, artifacts,
  and enforced Codex `gpt-5.4` `xhigh` synthesis. Use `$code-review`.
- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The user asks Cursor Agent to run GPT/GBT or Claude models. Cursor Agent is
  Composer-only; GPT/GBT runs through Codex and Opus runs through Claude Code.
- The work is an ordered subprocess workflow with manifests, critics, repair
  loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The child is expected to edit files or fix issues. Use `$agent-delegate` for
  a one-shot operational subprocess task.
- The child is expected to continue a long-running workflow. Use the matching
  workflow skill or native goal mode instead.
- There is no concrete artifact, claim, question, or target path to inspect.
- The requested runtime CLI is not installed.

## Non-Negotiables

- Resolve each consult objective, exact user-named artifacts or target paths,
  hard constraints, and the work root before launching child processes.
- Runtime, model, and effort must be known. Codex runs GPT/GBT/OpenAI models,
  Claude Code runs Opus, and Cursor Agent runs `composer-2.5-fast`. If any
  value is missing or ambiguous, ask one consolidated question before invoking.
- Never run GPT/GBT or Claude models through Cursor Agent. Do not pass GPT/GBT
  or Claude model ids to Cursor Agent.
- Treat model text as intent, not a fuzzy alias. Preserve exact family and
  numeric version; never silently substitute a nearby model.
- Run the child fresh, hook-suppressed where the runtime supports it, and
  unsandboxed per this repo's convention. The child prompt enforces read-only
  behavior, not a sandbox.
- For a single consult, create one namespaced run directory under
  `/tmp/fresh-consult/` and keep `prompt.md`, `final.txt`, `events.jsonl`, and
  `stderr.log` there.
- For explicit parallel consults, create one group directory under
  `/tmp/fresh-consult/` and one ordinary child run directory per consult. Do not
  add a controller, detached monitor, or new runner surface.
- Brief the child like a colleague walking in cold: include the raw consult ask,
  work root, exact user-named artifacts or target paths, hard constraints, and
  the report contract. The child chooses what evidence to inspect beyond those
  inputs.
- Do not paste secrets into prompts. If a token is needed, source it into the
  child environment and tell the child which environment variable to read.
- Do not ask the child to fix the issues it finds. Report back to the parent;
  fixes are a separate step.
- If the child reports a blocking finding, spot-check the cited evidence before
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
   claude`, or `command -v agent`.
6. Create the run directory or group directory and write each consult prompt to
   its own `prompt.md`.
7. Invoke each child with the exact command shape from the invocation reference.

## Workflow

1. **Shape the consult.** State the user's question, the bar for a useful
   answer, the work root, and the exact artifacts or target paths the user
   named.
2. **Resolve execution.** Map the raw model phrase to
   `runtime=<claude|codex|agent>`, `model=<runnable id>`, and
   `effort=<level-or-encoded-in-model>`.
   Announce the mapping before execution.
3. **Select single or parallel.** Use the single-child path by default. Use a
   parallel group only when the user asks for parallel consults or gives
   multiple consult questions.
4. **Run the child or children.** Use fresh subprocesses, no inherited sessions,
   disabled hooks where supported, no sandbox, namespaced run directories, and
   live event capture.
5. **Monitor patiently.** Normal consults often take 5+ minutes; broad repo
   reads, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live
   `events.jsonl` and `stderr.log` every few minutes, not every few seconds.
6. **Consume the result.** Read `final.txt`, locate the verdict footer, and
   inspect `events.jsonl`/`stderr.log` when the final output is missing or
   malformed.
7. **Report upstream.** For one child, lead with the verdict, blocking findings,
   confidence, and any disagreement after spot-checking. For a parallel group,
   report one compact child-by-child table plus a short synthesis of agreement
   and disagreement. Include all run directory paths.

## Output Expectations

- A concise parent-facing report:
  - runtime/model/effort used
  - consult verdict, or one verdict per child for parallel groups
  - blocking findings or `none`
  - non-blocking findings or `none`
  - evidence the child says it read
  - confidence and limits
  - run directory path, or group directory plus child run directories
- If the child output is missing or malformed, say that plainly and preserve the
  run directory for debugging. Do not invent a verdict.
- If the child is wrong on a blocking point, say so explicitly and cite the
  evidence that contradicts it.

## Reference Map

- `references/model-and-invocation.md` - runtime/model/effort resolution and
  exact Claude/Codex command shapes
- `references/consult-prompt-and-output.md` - consult prompt skeleton, verdict
  footer, report rules, and anti-patterns
