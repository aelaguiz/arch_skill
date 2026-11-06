# Setting up and running the reruns

These are the working facts from the first run, on October 27, 2026. Tools change, so check each one against what the tool does today before you rely on it. When a fact here has stopped being true, fix this file.

## What the last run left

Everything is in psbrain under `projects/agent-watcher/efficiency-profile/task-routing/`:

- `PLAN.md` holds the method and the run's log, including every problem it hit and how it was fixed. Read the log before starting: most of the setup below came out of it.
- `GUIDE.md` holds what the run concluded, and `backtest/scores.md` and `backtest/cases.md` hold every score, with both judges' reasons for each case.
- `catalog/` holds the kinds of helper work (`kinds.md`, with the labelling rubric in `rubric.md`) and the extracted tasks (`tasks.jsonl.gz`, `tasks-classified.jsonl.gz`). The task files hold whole briefs and results, so they are git-ignored and live only on the machine that made them.
- `backtest/tasks.jsonl` holds the tasks screened as safe to rerun, with their briefs, rerun folders and original results. `backtest/excluded.json` and `backtest/harness-mismatch.json` list what was left out and why.
- The tooling: `extract_tasks.py` reads every Claude Code and Codex transcript on a machine into tasks, `prep_catalog.py` groups repeated briefs and draws a sample, `classify.py` labels kinds, `select_backtest.py` and `screen.py` pick and screen tasks, `runner.py` runs one rerun on Claude or Codex and can stop everything working in a folder, `backtest.py` drives the reruns, `judge.py` scores them, and `analyze_scores.py` makes the tables.

For a small question, start from the newest round's `harness/` folder rather than October's tooling: the rounds of November 5 ran in minutes to a couple of hours with a written cap. Copy into the new run's dated folder what the next run builds on, and change it there, so the last run stays intact as a record. The scripts read their inputs relative to their own folder, so take the scripts together with `catalog/`, `backtest/tasks.jsonl`, `backtest/excluded.json`, `backtest/harness-mismatch.json`, `backtest/legacy-tids.json` and `backtest/sandbox-settings.json`.

Take `backtest/runs/` too: it holds every setting's stored answer to every task (one record per setting in `runs/<task>/<setting>.json`, about 260 MB, git-ignored, so it exists only on the M5). The driver skips any setting that already has a record, so with the stored records in place it runs only the new model's settings, which is what you want. Leave out any stored record you have decided to rerun, such as the reference on a task whose inputs have moved; the driver then runs that one again.

Leave behind `backtest/judgments/`, the scores, the logs, the pid files and `backtest/accounts.txt`. The judge skips a task it has already judged, so old judgments would keep the new answers from being scored beside the stored ones. Judging is cheap next to rerunning: every task is judged again, with all its answers, old and new, in one pass.

What to change in the copy:

- The model ids are constants at the top of `backtest.py`, and the settings to run are the list in `settings_for`: list the new model's settings there. That function also makes the reference each task's own original model and level. For a fresh task, change it so the reference is the strong model at its top level, as `SKILL.md` explains.
- `backtest/legacy-tids.json` lists 20 tasks whose stored answers ran without the project context mirrored in. Run the new model on them the same way, or leave them out.
- The judges are written into `judge.py`, near the end.
- The driver's limits are numbers chosen for October 27's disk and accounts: when an account rests (88% of its five-hour window, 60% of its week), how much free disk a rerun needs before it starts (80 GB for one that copies a repository, 50 GB otherwise), and how big a rerun's folder may grow (8 GB, or 2 GB for one that copies nothing). At 15:12 that day every worker sat idle on the 80 GB floor while the back-test itself held only 9 GB. Set them from today's disk and accounts.

## Where reruns work

Reruns worked in `/Users/Shared/taskroute-backtest/runs/`. That folder sits outside the home folder and `/tmp`, because the sandbox denies writes in both. It also sits outside Claude Code's own temp area (`/private/tmp/claude-501/`), where Write calls land in a per-session redirect folder. Delete each rerun's folder once its record is saved; the record keeps the result, the files written and the diff.

Reruns ran on the M5 Mac. Most tasks read files at that Mac's paths, so they cannot run elsewhere as they ran. They are network-bound agent processes, so `nice -n 10` and a cap on how many run at once was enough.

## Containing a rerun

A Claude rerun:

```bash
nice -n 10 aim claude run <account> -- -p --model <model-id> --effort <level> \
  --output-format json --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --permission-mode bypassPermissions --settings <sandbox-settings.json> < prompt.txt
```

run with the rerun's folder as its working directory. The settings file (`backtest/sandbox-settings.json`) did this:

- turned the sandbox on, with `allowUnsandboxedCommands: false`, network open (`allowedDomains: ["*"]`) and `enableWeakerNetworkIsolation: true`, without which `gh` fails on a certificate error inside the sandbox;
- denied Write and Edit under the home folder, `/Users/agents`, `/Volumes`, `/tmp`, `/private/tmp` and `/home`;
- denied every command that acts on the world: `git push`, `gh` commands that write, `gws`, `approvals`, `aim`, `herdr`, `ssh`, `scp`, `rsync`, `adb`, `xcrun`, `slack`, `open`, `osascript`, and `kill`;
- denied searches that start at the disk root, the home folder or the workspace root.

The first run tested it before using it: writes inside the folder worked, writes elsewhere were refused, reading anywhere and `curl` worked, and the denied commands never ran. Test it the same way after any Claude Code upgrade. Inside the sandbox each shell command also prints `operation not permitted: /tmp/claude-501/cwd-…` and exits 1. The command itself runs and its output is intact, so don't read that exit as a failure; it touches every setting alike.

A Codex rerun:

```bash
nice -n 10 aim codex run -- exec --sandbox workspace-write --skip-git-repo-check \
  -C <rerun-folder> -m <model-id> -c model_reasoning_effort=<level> --json \
  -c sandbox_workspace_write.exclude_slash_tmp=true - < prompt.txt
```

Codex reads anywhere and writes only inside its folder. Its network is off unless the task needs it (`-c sandbox_workspace_write.network_access=true`).

For another harness, such as the Antigravity CLI for Gemini, take its exact invocation from `$agent-delegate`'s references. Then test its containment the same way before any real rerun: a write outside the folder must fail.

## What each rerun is told

A preamble goes in front of the original brief. It says this is a test rerun of a task first done on a given date, and that nothing it does is used for real. It says which folder the rerun works in. It says not to send, post, publish, push, deploy, comment, message, buy or start other agents; when the task needs one of those, the rerun goes as far as it can and says what it would have done. Reading anything and making read-only web or GitHub requests is fine. It says to write only the files the task changes, never to copy a repository or content tree, and to search only where the thing lives. Its final answer is the deliverable the brief asks for. The first run's wording is `PREAMBLE` in `backtest.py`.

## Giving a rerun the original's context

The original agent loaded its project's instruction files and project skills; a rerun in a scratch folder does not. Copy the text of every `CLAUDE.md` and `AGENTS.md` from the repo root down to the original working folder into the rerun's folder, and link every project skill (`.claude/skills`, `.agents/skills`) into it. An `@import` that points outside the folder is not expanded without a person's approval. The first run's version is `mirror_context` in `backtest.py`. Don't change this setup partway through a task: a task compares its settings under one setup.

## Code-writing tasks

A task that wrote code reruns in a `git clone --shared` of its repo, made inside the rerun's folder, at the commit the task started from. A `git worktree` won't do, because it keeps its git data in the original repo, which the sandbox won't let it write. Take the diff against that starting commit, not against the clone's latest commit, which is empty once the agent commits. When the starting commit is gone, leave the task out: a nearby commit changes the task.

These are the reruns that eat disk. A psmobile clone with its build output and Flutter's package cache passed 8 GB, and lesson builds that copied a 2.8 GB content tree into each rerun had to be left out. Run few of them at once, and stop any rerun whose folder grows past what the task could need.

## Accounts

Claude reruns and Opus judging go through AI Manager on pooled accounts that `aim claude status` shows with room in both their five-hour window and their week. Never use this session's own account. Rest an account before its window fills, so the sessions that live on it keep room, and send each rerun to whichever account has the most room. When an account hits a limit, move its queue to another; don't wait for the reset. Codex reruns and Sol judging go to the Codex pool through `aim codex run`.

As a rough measure: one Opus rerun at xhigh, about ten minutes long, used about 3% of an account's five-hour window. The first run's roughly 340 Opus reruns came to about ten five-hour windows, about one account's week.

## Watching the run

- **Disk.** Check free space all through the run. The first run fell 25 GB an hour at its worst, from repository copies, until the agent watcher caught it. Hold back reruns that copy a repository when space is low, and stop any rerun whose folder passes its cap.
- **Wide searches.** A rerun hunting for a file ran `bfs /` across the whole disk. The sandbox now refuses that, and a driver check stopped any search a rerun started from the disk root, the home folder or a workspace root.
- **Stopping.** Stop a rerun by its working directory: list processes with `lsof -a -d cwd` and stop those inside the folder (`stop_folder` in `runner.py`). Matching command lines finds nothing, because agents work inside their folder without naming it. When the driver stops, stop its reruns too, and don't save records from reruns killed by the shutdown; they look like failures and would be judged as the model's.
- **Restarts.** Each rerun's record is saved as it finishes, and the driver skips what is saved, so a restart loses only the reruns in flight. Queue changes to the setup until a batch finishes, rather than restarting for each one.

## What a rerun's record keeps

The result text, the files written (with the diff for code tasks), wall-clock time, model time, turns, tokens, errors, and whether it hit an account limit. A rerun that hit a limit is run again, not scored.
