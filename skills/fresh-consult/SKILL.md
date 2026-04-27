---
name: fresh-consult
description: "Invoke a fresh Claude or Codex subprocess for a prompt-engineered second opinion with clean context. Use when the user or another skill asks for a cold read, external consult, flow consistency audit, completion-claim check, readability/confusion check, or general second opinion from Claude/Codex. Ask once if runtime, model, or effort is missing; run hook-suppressed and unsandboxed; report the child result back. Do NOT use for deterministic full code-review coverage (`code-review`), Codex `-p yolo` reviews (`codex-review-yolo`), ordered subprocess orchestration (`stepwise`/`arch-epic`), or implementation/fixing by the child (`agent-delegate`)."
metadata:
  short-description: "Fresh Claude/Codex second opinion with clean context"
---

# Fresh Consult

Use this skill when the user or another skill needs a clean second opinion from
a fresh Claude or Codex subprocess. The child model starts from disk and the
consult prompt, not from the current chat history, so it can catch confusion,
drift, missing completion, or weak reasoning the parent may have normalized.

This is a prompt-engineering skill. It ships no scripts, shims, hook
controllers, state machines, parsers, or install-time automation.

## When to use

- "Ask Claude for a cold read of this flow."
- "Use Codex to audit whether this plan phase is actually complete."
- "Run a fresh consult for consistency on these skills."
- "Get a second opinion on whether this doc is linear and not confusing."
- "Have a clean model check whether the implementation matches the checklist."
- Another skill needs an independent read before it decides whether to proceed.

## When not to use

- The user wants deterministic code-review coverage with lens fan-out, artifacts,
  and enforced Codex `gpt-5.4` `xhigh` synthesis. Use `$code-review`.
- The user specifically asks for the existing Codex `-p yolo` review pattern.
  Use `$codex-review-yolo`.
- The work is an ordered subprocess workflow with manifests, critics, repair
  loops, or persistent orchestration. Use `$stepwise` or `$arch-epic`.
- The child is expected to edit files or fix issues. Use `$agent-delegate` for
  a one-shot operational subprocess task.
- The child is expected to arm hooks or continue a controller. Use the matching
  hook-backed workflow skill instead.
- There is no concrete artifact, claim, question, or target path to inspect.
- The requested runtime CLI is not installed.

## Non-Negotiables

- Resolve one consult objective, the authoritative artifacts, and the work root
  before launching a child process.
- Runtime, model, and effort must be known. If any are missing or ambiguous,
  ask one consolidated question before invoking.
- Treat model text as intent, not a fuzzy alias. Preserve exact family and
  numeric version; never silently substitute a nearby model.
- Run the child fresh, hook-suppressed, and unsandboxed per this repo's
  convention. The child prompt enforces read-only behavior, not a sandbox.
- Create one namespaced run directory under `/tmp/fresh-consult/` and keep
  `prompt.md`, `final.txt`, `events.jsonl`, and `stderr.log` there.
- Brief the child like a colleague walking in cold: include objective, paths,
  claims, what to inspect, and the report contract.
- Do not paste secrets into prompts. If a token is needed, source it into the
  child environment and tell the child which environment variable to read.
- Do not ask the child to fix the issues it finds. Report back to the parent;
  fixes are a separate step.
- If the child reports a blocking finding, spot-check the cited evidence before
  acting on it or presenting it as verified truth.

## First Move

1. Read `references/model-and-invocation.md`.
2. Read `references/consult-prompt-and-output.md`.
3. Identify the consult objective, work root, artifacts, explicit claims, and
   requested runtime/model/effort from the user's words.
4. If runtime/model/effort is incomplete, ask one question that names exactly
   what is missing and what it controls.
5. Confirm the selected CLI exists with `command -v codex` or
   `command -v claude`.
6. Create the run directory and write the consult prompt to `prompt.md`.
7. Invoke the child with the exact command shape from the invocation reference.

## Workflow

1. **Shape the consult.** State the decision or question the child must answer,
   the bar for success, and the authoritative files, commits, docs, or claims.
2. **Resolve execution.** Map the raw model phrase to
   `runtime=<claude|codex>`, `model=<runnable id>`, and `effort=<level>`.
   Announce the mapping before execution.
3. **Run the child.** Use a fresh subprocess, no inherited session, disabled
   hooks, no sandbox, a namespaced run directory, and live event capture.
4. **Monitor patiently.** Normal consults often take 5+ minutes; broad repo
   reads, `xhigh`, or `max` can reasonably take 20-40 minutes. Poll live
   `events.jsonl` and `stderr.log` every few minutes, not every few seconds.
5. **Consume the result.** Read `final.txt`, locate the verdict footer, and
   inspect `events.jsonl`/`stderr.log` when the final output is missing or
   malformed.
6. **Report upstream.** Lead with the verdict, blocking findings, confidence,
   and any disagreement after spot-checking. Include the run directory path.

## Output Expectations

- A concise parent-facing report:
  - runtime/model/effort used
  - consult verdict
  - blocking findings or `none`
  - non-blocking findings or `none`
  - evidence the child says it read
  - confidence and limits
  - run directory path
- If the child output is missing or malformed, say that plainly and preserve the
  run directory for debugging. Do not invent a verdict.
- If the child is wrong on a blocking point, say so explicitly and cite the
  evidence that contradicts it.

## Reference Map

- `references/model-and-invocation.md` - runtime/model/effort resolution and
  exact Claude/Codex command shapes
- `references/consult-prompt-and-output.md` - consult prompt skeleton, verdict
  footer, report rules, and anti-patterns
