# Script Output Economy

Read this file when a skill ships a script, command wrapper, or tool whose stdout the agent will read. The decision to add a script at all is upstream in `leverage-and-scope.md` and the "Add a `script` when" rules in `packaging-trigger-and-validation.md`. This file owns the shape of what the script prints once that decision is made.

## Table of contents

- The frame: stdout is the agent's next prompt
- Named failure modes that punish unbounded output
- Good patterns
- Anti-patterns
- Example cases
- Symptom-to-fix map
- Final self-check

## The frame: stdout is the agent's next prompt

When an agent runs a script the skill ships, the script's stdout becomes part of the agent's next turn. Whatever the script prints, the model has to read, paraphrase, hold across follow-up turns, and not be distracted by. A script's output is therefore not a developer console; it is a prompt fragment the skill author is writing on the agent's behalf. Design it the same way you would design any other prompt: smallest set of high-signal tokens that lets the agent decide what to do next, and an explicit way to fetch more if the decision needs more.

This frame is the only durable rule. Every good pattern below is a way of obeying it; every anti-pattern is a way of breaking it.

## Named failure modes that punish unbounded output

These failure modes are not aesthetic preferences. They are degradation curves the literature has named, and skill-shipped scripts trigger them more reliably than almost any other surface, because the same script is invoked many times across many sessions.

- **Lost in the middle.** Long contexts lose the tokens that sit in the middle of the window faster than the ones at the head or tail. A blob the script prints today silently rots out of the agent's effective memory tomorrow. (Liu et al., *Lost in the Middle*, 2023.)
- **Context rot.** Model performance drops as the context window fills, even with tokens the model itself produced. A script that prints its full result by default forces the agent to pay this tax on every invocation. (See the *Context Rot / How Contexts Fail* discussions, e.g. dbreunig 2025-06-22.)
- **Context distraction.** Past tool output starts pulling the model toward repeating historical actions instead of reasoning about the current turn. The bigger the inline tool result, the stronger the pull. (Anthropic, *Effective context engineering for AI agents*.)
- **Context pollution.** Irrelevant or redundant detail in the window degrades reasoning accuracy independently of length. A 500-line JSON dump where 5 lines were the verdict is mostly pollution. (Anthropic and ADK guidance both name this; the handle pattern is the standard remedy.)

If the lesson is reduced to "be short," it has been reduced badly. The lesson is: the script's output shape decides which of these curves the agent walks down.

## Good patterns

Each pattern is a recognition test, not a recipe. A script can satisfy more than one.

### Verdict + handle

- the script prints the decision-grade signal inline (one line: pass / fail / N errors / "ready to advance") and a handle the agent can follow if it needs more (a path on disk, a follow-up command, an identifier)
- the agent can act on the verdict without ever fetching the handle, and can fetch the handle in a separate turn if the verdict is ambiguous
- this is the default shape for any "verify," "check," "status," or "audit" command

### Summary + drill-down

- the script prints a small structured summary (counts, top-K, headlines) and names the exact follow-up command for each kind of detail
- the drill-down commands are spelled out in the script's own output, so the agent does not have to invent them or re-read the SKILL
- this is the default shape for any "list," "search," or "report" command

### Bounded by default, expanded on request

- the default mode caps output (line count, token count, item count, error-only filter) and the cap is documented in the script's `--help`
- a `--full`, `--page N`, `--fields a,b,c`, or `--errors-only` flag opens the cap when the agent specifically wants more
- defaults are treated as a contract with the skill, not a debug convenience

### Large data goes to disk; stdout returns the path

- anything bigger than a small structured summary is written to a deterministic location (workspace tmp, a run directory, an artifact root) and stdout returns only the path and one-line summary
- the layout of that location is documented in a reference (see `skills/stepwise/references/run-directory-layout.md` and `skills/code-review/references/invocation.md` for in-repo examples), so the agent can find sub-artifacts without prose guessing
- this matches the "handle" pattern Anthropic Skills, Google ADK, and Claude Code's own grep/bash discipline already use

## Anti-patterns

Each anti-pattern is a recognition test for the script author. If the script author cannot say which good pattern would replace it, the anti-pattern is real.

### Unbounded JSON blob to stdout

- the script's default invocation prints the entire result tree as JSON, with no cap and no summary line
- the size of the output is a function of the input, not of what the agent needs to decide
- this is the canonical shape that triggers context rot and lost-in-the-middle; it is the shape that motivated this reference

### Pretty-by-default with no compact mode

- the script pretty-prints (indented JSON, ASCII tables, banners, ANSI rules) by default and offers no compact, machine-first mode
- the agent pays for whitespace and decoration on every invocation
- pretty output is a debug convenience for humans; it should be opt-in (`--pretty`), not default

### Inline raw artifact when a path would do

- the script reads a file, processes it, and prints the result inline when the result is large and the script could have written to disk and returned a path
- the agent ends up with the artifact paraphrased into its context, which is strictly worse than a path it can read on demand
- if the result is structured, large, or reused later in the session, it belongs on disk

### Token-blind defaults

- the script has no `--summary` / `--full` split, no pagination, no error-only mode, no field selection
- there is no way for the agent to ask for less without parsing and discarding what it already paid for
- the absence of opt-in narrowing is itself the bug, even if the script's full output is sometimes the right answer

## Example cases

Adapted from real and representative scripts. Use them to teach the principle, not to copy the wording.

### Case 1: a verify command that returns the entire check tree

Real failure pattern:
- a `verify` script returns the full check tree (every check name, status, error array) as JSON by default, even when nothing failed

Bad shape:
- "Print `{ ok, lesson_uid, check_count, error_count, warning_count, checks: [ {...}, ... 19 entries ... ] }` on every invocation."

Better shape:
- "Print one line: `OK <lesson_uid> 19 checks (0 errors, 0 warnings) - details: <run_dir>/verify.json`. Write the full check tree to `<run_dir>/verify.json`. Add `--full` to print the tree inline and `--errors-only` to print only failed checks inline."

Why the better shape works:
- the success case costs the agent one line and one path
- the failure case is opt-in and bounded to what the agent actually needs
- the agent can still get every byte of the original output by reading the path or passing `--full`

Transferable principle:
- a verify-style script's default output should be the verdict, not the evidence

### Case 2: a list command that returns every match inline

Real failure pattern:
- a `list` or `search` command returns every matching record as a JSON array, with no cap, no top-K, and no follow-up command

Bad shape:
- "Print all 412 matching records as a JSON array, sorted by name, with full fields per record."

Better shape:
- "Print a header: `412 matches; showing top 10 by recency`. Print 10 compact rows. End with: `more: <command> --page 2` and `details for one: <command> show <id>`. Default `--fields` to a small set; allow `--fields all` and `--page N` to expand."

Why the better shape works:
- the agent gets a calibrated picture in a few lines
- the next move is named, so the agent does not have to invent a follow-up
- the full data is reachable but not pre-loaded

Transferable principle:
- a list-style script's default output is a calibrated sample plus the follow-up commands, not the entire result set

### Case 3: a script that processes a file and prints the processed file

Real failure pattern:
- a transform script reads `input.json`, computes a derived artifact, and prints the derived artifact inline

Bad shape:
- "Read `input.json`, compute `output.json`, print `output.json` to stdout."

Better shape:
- "Read `input.json`, compute `output.json`, write it to `<run_dir>/output.json`, and print one line: `wrote <run_dir>/output.json (N items, M warnings)`."

Why the better shape works:
- the artifact lives where artifacts live; the agent reads it on demand
- the agent's context records the action and the location, not the contents
- subsequent turns can refer to the path instead of paraphrasing the contents

Transferable principle:
- if the script's job is to produce an artifact, the script's output is the artifact's location, not its body

## Symptom-to-fix map

If the problem is:

- the agent paraphrases the script's output every turn and the paraphrase keeps drifting: the script is inlining what should be a handle. Move the body to disk and return the path.
- the agent loses track of what the script said two turns later: lost-in-the-middle. Cut default verbosity and add `--full` for the rare case it is needed.
- the script's output is longer than the user's question: the default has no verdict line. Add a one-line verdict at the top and demote the rest behind a flag or a path.
- the agent re-reads the same large tool result on multiple turns: tool-result clearing is not enough by itself. Move the data to disk so subsequent turns reference a path, not a re-pasted blob.
- the script offers no way to ask for less: token-blind defaults. Add a `--summary` mode (or make summary the default and add `--full`) before adding more features.
- the script pretty-prints by default and the agent pays for whitespace: invert the default. Compact and minimal becomes default; `--pretty` becomes opt-in.
- the agent has to invent a follow-up command to drill down: the summary failed to name its own drill-downs. Print the exact follow-up commands in the summary itself.
- the script's output looks fine in isolation but the multi-turn workflow degrades: that is the named failure modes (context rot, distraction, pollution). The fix is one of the four good patterns, not "be careful."

## Final self-check

These are principle tests, not a runtime checklist. If a script's output cannot pass them, the failure is in the output shape, not in the agent.

- If a downstream agent replayed this script's stdout into its prompt for ten turns, would the work degrade or stay sharp?
- Could the agent decide its next move from the first line alone, and only fetch the rest if the decision is ambiguous?
- Does the script give the agent an explicit way to ask for less, and an explicit way to ask for more?
- If the result is large or structured, is the canonical copy on disk and the stdout a handle to it?
- Would a reviewer reading only the script's `--help` and one example invocation know the default cap, the drill-down commands, and where artifacts land?
