---
name: agent-history
description: "Search and interpret local Codex or Claude Code session history from natural-language asks about prior prompts, goals, commands, corrections, tool use, timelines, or agent behavior. Use the current runtime, current project, and last 24h by default unless the user says otherwise. Run the bundled helpers for JSONL/SQLite extraction, then synthesize evidence with confidence notes. Do not require rigid syntax, replace Git commit history tools, launch subprocesses, or dump raw transcripts by default."
metadata:
  short-description: "Search local agent session history"
---

# Agent History

Use this skill when the user wants to find, explain, or summarize past local
agent-session evidence. The user may speak casually: "what prompt did I run
here", "what goal commands did I run today", "where did I have to correct the
agent", or "find where I was struggling with the agent last night".

This skill is a retrieval and evidence skill. It ships helper scripts so agents
do not hand-roll fragile JSONL and SQLite parsing, but the scripts are not a
query language for the user. Interpret the user's words, run the helper to get
candidates, inspect the evidence, and answer like an investigator.

If a neighboring request actually needs another model agent, apply
`../_shared/agent-orchestration-policy.md` before routing it. This history
skill remains read-only and does not dispatch that agent itself.

## When To Use

- The user asks about prior Codex or Claude Code prompts, turns, commands,
  goals, tool calls, corrections, confusion, or session timelines.
- The user asks what happened in the current project during recent agent work.
- The user wants to search local session history by natural-language clues.
- Another skill needs grounded history evidence before deciding what happened.

## When Not To Use

- The user wants Git commit history rewritten. Use `$commit-history-authoring`.
- The user wants a fresh second opinion from another model. Use
  `$fresh-consult`.
- The user wants another agent to do work. Use the active host's native child
  for ordinary same-host work; use `$agent-delegate` only when a deliberate
  external worker/session provides the needed benefit.
- The user wants to search current repo files rather than past agent-session
  evidence. Use normal repo search.
- The user asks for history from a runtime whose local store is absent and no
  exported history is provided.

## Non-Negotiables

- Use the current agent runtime by default. In Codex, search Codex history. In
  Claude Code, search Claude history. Search another runtime only when the user
  asks for it or clearly implies it.
- If the user does not name a project, default to the current working
  directory. If they do not name a time range, default to the last 24 hours.
  If they say "today", use the local calendar day.
- Interpret natural language with judgment. Do not force flags, templates, or
  a canned command vocabulary onto the user.
- Run `scripts/agent_history.py` before inventing ad hoc parsers for common
  Codex or Claude history stores.
- Treat helper output as evidence, not the final answer. Drill down when the
  summary is ambiguous or when the user's question needs surrounding context.
- Preserve privacy. Quote only short, relevant snippets unless the user asks
  for raw history.
- Label evidence quality. Use `exact` for directly stored text, `inferred` for
  durable effects, `best_effort` for logs or partial traces, and
  `not_found_after_search` when the searched stores did not contain a match.

## First Move

1. Read `references/retrieval-playbook.md`.
2. Read `references/helper-script.md`.
3. Read `references/storage-map.md` only as needed for the runtime and evidence
   type in the user's request.
4. Convert the user's ask into a search intent: runtime, project scope, time
   window, evidence target, and answer shape.
5. Run the bundled helper with the current runtime and the smallest useful
   scope. Use follow-up helper calls for drill-down instead of dumping raw logs.

## Workflow

1. **Resolve defaults.** Use the current runtime, current cwd, and last 24h
   unless the user supplied a different runtime, project, or time range.
2. **Choose evidence.** Start with metadata and indexes, then transcripts, then
   logs only when logs are the right or only source.
3. **Run helpers.** Use `agent_history.py sessions`, `prompts`, `commands`,
   `goals`, or `search` to get bounded candidates and artifact handles.
4. **Inspect context.** Use `agent_history.py show` or targeted file reads for
   the few hits that matter. Do not summarize a whole transcript from a search
   result row alone.
5. **Synthesize.** Answer the user's real question, not the helper command.
   Include assumptions, evidence paths, confidence, and any storage limitation.
6. **Stop cleanly.** Stop when the answer is supported enough for the user's
   question. If the store cannot answer exactly, say what was searched and why
   the remaining uncertainty exists.

## Output Expectations

- Lead with the direct answer.
- State assumed runtime, project, and time window when they were not explicit.
- For each meaningful hit, include runtime, timestamp, session/thread id, cwd
  or project, source path, short evidence, and confidence.
- Keep snippets short. Prefer path/session handles over raw transcript dumps.
- If no match is found, say which stores were searched and whether the absence
  is strong evidence or only best-effort.

## Reference Map

- `references/retrieval-playbook.md` - natural-language interpretation,
  evidence selection, examples, and answer shape
- `references/storage-map.md` - Codex and Claude local stores, formats, and
  command/goal persistence limits
- `references/helper-script.md` - helper commands, output contract, artifact
  layout, and drill-down behavior
- `scripts/agent_history.py` - self-contained read-only history parser
