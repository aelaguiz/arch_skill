# What a computer restart takes away

Read this when the computer itself is restarting or shutting down, not for a plain stop. Everything here comes from the October 25 restart of Amir's Mac.

## /tmp is emptied at boot

macOS empties `/private/tmp` when it starts. Agents keep real work there: every Claude Code session's scratchpad lives under `/private/tmp/claude-<uid>/`, and builds keep their scripts and stacks there too. On October 25 that included the lessons build's runners and play stack, 27 GB in `/tmp/lessons_studio`, and the playtest runners. A session resumed after the restart without its scratchpad loses whatever it kept there.

`savepoint.py tmp-save` copies all of /tmp into the save point folder with APFS clones (`cp -cRp`). Clones share disk blocks, so this costs almost no space, but it still walks every file. On October 25, 94 GB took about eight minutes. Start it in the background as soon as a restart is likely, and tell Amir to restart only after it finishes. After the boot, run `tmp-restore` before resuming sessions. Sockets and a few system folders can't be copied, and the log ignores those errors. Once everything is running again, the clone in the save point can be deleted. While it exists, its blocks stay shared rather than freed.

## Detached jobs die and only some come back

`save.json` lists the processes nobody's terminal owns any more (`detached_jobs`), each with its command and folder, and whether launchd owns it. It can't tell which session started a job, because the job outlived its parent. The folder and command usually say: workers in a build's worktrees belong to that build's session, and a script under a session's scratchpad belongs to that session. Your own helpers are on the list too. launchd's jobs (MCP servers, listeners, scheduled routines) come back on their own. The others need someone to start them again:

- **A job a session started for itself**, such as a dev server, a tunnel or a build's workers, is that session's to restart. In its resume note, say which of its jobs died, rather than starting them yourself and racing it.
- **A standalone job that keeps something on schedule** is yours to restart, the same way it was started. Read its first lines or its docstring for the command. The Apple Ads on/off timer was one: it keeps a paid test switching campaigns on the right days. Check its log after the restart to confirm it ran.
- **ssh port forwards** (`ssh -f -N -L ...`) come back with the same command, which the save records.
- **Docker VMs under colima** come back with `colima start <profile>`. After a shutdown that wasn't clean, a start can fail with `failed to run attach disk "<name>", in use by instance "<name>"`. That is a stale lock, the link `~/.colima/_lima/_disks/<name>/in_use_by`. When no `limactl hostagent` is running for that instance, remove that one named link and start again.

## Remote sessions tied to an ssh connection

Before disconnecting, check on the remote machine whether the agent runs under a tmux server or straight under sshd: walk up its process tree, or run `tmux ls`. A session tied to the connection dies with it. To keep it alive:

1. Run `stop` on that pane (`--panes S:P --include-ssh`). The remote agent exits, the pane prints its resume id, and the pane drops back to the remote shell.
2. Start it again inside tmux on that machine: `ssh <host> "tmux new-session -d -s <name> -c <folder>; tmux send-keys -t <name> 'aim claude resume <id>' Enter"`. On a machine where AI Manager says the session already belongs to an account, use a plain resume without `--account`.
3. If it had live work, send its note inside tmux: `tmux send-keys -t <name> -l '<note>'`, then `tmux send-keys -t <name> Enter`, as two separate sends.
4. Close the pane's ssh (`exit`). After the restart, reattach it with `ssh <host> -t tmux attach -t <name>`.

A session already inside tmux needs none of this: closing the ssh only detaches it.

## Order after the boot

1. `tmp-restore`.
2. Ask Amir to open any Herdr session that `resume` reports isn't running.
3. `resume`.
4. Send a note to each session that had live work.
5. Restart the detached jobs that are yours.
6. Reattach the ssh panes to their tmux sessions.
