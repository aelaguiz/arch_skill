---
name: agent-history
description: "Read local Codex, Claude Code, Pi, Prime Agent, or Antigravity CLI (agy) session history: open one session by its id and see what it did, in order, or find sessions, prompts, goals, corrections, tool calls, and child-agent briefs from natural-language clues. Covers every AI Manager account folder on the machine. Use when asked to read, review, or watch a session by id, or to find what happened in past agent work. Not for live agent status, streaming output, or session control; use the runtime's live interface for those."
metadata:
  short-description: "Read and search local agent session history"
---

# Agent History

Read what agent sessions on this machine actually did, from their transcripts.
The bundled helper does the parsing; you decide what evidence the question
needs, read it, and answer like an investigator. It only reads: never open
`auth.json` in any runtime home, and never run daemon lifecycle commands.

The helper is `scripts/agent_history.py` in this skill's folder. Every command
prints a short summary, writes the full results to a run folder, and prints
the exact follow-up command for more, so you rarely need its `--help`.

## Read a session you have an id for

This is the most common job: "read claude session 1a2b3c4d", a review of
another agent's work, or a watch on a session that keeps running.

```bash
python3 <this skill>/scripts/agent_history.py read <session id>
```

- The id can be whole or its first 8 characters, from any runtime. The helper
  finds the transcript in every Claude and Codex home on the machine,
  including each AI Manager account folder, and in the Antigravity, Prime,
  and Pi stores. Add `--runtime` only when a prefix matches sessions in two
  runtimes; the helper lists them when that happens.
- It prints where the session is (title, project, first and last activity,
  transcript path) and its latest 40 entries in order: prompts, replies, tool
  calls, tool results, and compactions. The whole session goes into a
  readable `transcript.md`, whose path it prints. Read that file when you
  need the full story, such as the first time you review a session; long
  tool output in it is cut.
- To come back to the same session later, run the `next time:` command it
  printed (`read <id> --after <time>`). You see only what happened since.
- A session's own id: Claude Code puts it in `$CLAUDE_CODE_SESSION_ID`,
  Codex in `$CODEX_THREAD_ID`. When AI Manager moves a session to another
  account it gets a new id; the old id still reads, as the earlier part.
- A session on another machine, such as the home server, is read by running
  the same helper there over ssh; the skill is installed on each machine:
  `ssh home 'python3 ~/.agents/skills/agent-history/scripts/agent_history.py read <id>'`.

Read the session itself before you judge it. A summary the session wrote, a
pane's last screen, or a search hit is a claim about the work; the entries
show what was done.

## Find sessions, prompts, or something said

```bash
python3 <this skill>/scripts/agent_history.py sessions --runtime <runtime>
python3 <this skill>/scripts/agent_history.py prompts  --runtime <runtime> --since today
python3 <this skill>/scripts/agent_history.py search   --runtime <runtime> wrong instead "read the"
python3 <this skill>/scripts/agent_history.py commands --runtime <runtime>
python3 <this skill>/scripts/agent_history.py goals    --runtime <runtime>
```

`--runtime` is one of `codex`, `claude`, `pi`, `prime`, `agy`. These commands
search the current project over the last 24 hours unless you widen them with
`--scope all-projects` or `--since 7d`; `search` takes words or `--regex`.
Each prints a few rows with their session ids and a `show:` command for one
row's detail. Hand a session id from a row to `read` to see the whole session
around it.

## Judgment

- **Scope.** Search the runtime you are running in unless the user names
  another or clearly means one ("prime", "agy", "the Antigravity reviewer").
  With no project named, use the current folder; with no time named, the
  last 24 hours; "today" is the local calendar day. Say what you assumed.
  If the current runtime is unclear, pick the one with recent activity for
  this project and say so.
- **Evidence.** Work out what would answer the question before choosing a
  command. "What prompt did I run" wants prompts; "where did I correct the
  agent" wants the user's turns and what came right before them; "what is it
  doing" or "is it on track" wants the session read in order. The playbook
  below has more of this when the ask is fuzzy.
- **Context before conclusions.** A row is a lead. Open the session or the
  hit's surroundings before calling something a correction, a mistake, or a
  decision.
- **Your own parsing is a last resort.** Use it only for something the helper
  cannot show, and say what the helper could not do.
- **Limits.** Pi, Prime, and agy keep no goal store, so goals there come from
  transcript text only; agy results from a shortened transcript are
  `best_effort`. Say so rather than reporting a clean absence.
- **Labels.** Mark evidence `exact` (stored text), `inferred` (implied by
  stored state), `best_effort` (logs or partial traces), or
  `not_found_after_search` (searched and absent, with what was searched).
- **Privacy.** Quote short, relevant snippets unless the user asks for raw
  history.

## Answer

Lead with the answer. Give the assumed runtime, project, and time window when
the user did not. For each hit that matters: runtime, time, session id,
project, transcript path, a short quote, and the evidence label. For no
match, say which stores were searched and how strong the absence is.

## References

- [references/helper-script.md](references/helper-script.md): every command,
  option, and output format. Read it when you need an option not shown here.
- [references/retrieval-playbook.md](references/retrieval-playbook.md): turning
  fuzzy asks ("where was I struggling") into evidence and search terms.
- [references/storage-map.md](references/storage-map.md): where each runtime
  keeps what, for questions the helper does not cover.
