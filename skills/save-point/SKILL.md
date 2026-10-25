---
name: save-point
description: "Save every agent session running in Herdr on this machine to a save point in seconds (each Claude Code, Codex and Kimi session's live resume id, unsent drafts, live work, ssh panes, detached jobs), optionally stop them all, and later resume them from the save point. Use when the user says to save, checkpoint or stop everything, is about to restart or shut down the computer, or says to restore, resume or get everything going again after a restart or a stop. Not for moving one workspace between Herdr sessions ($herdr-helper) or moving one stalled session to an account with room ($agent-watcher)."
---

# Save Point

Amir runs dozens of agent sessions at once across Herdr sessions, and some of them reach into other machines over ssh. When he restarts the computer, or just wants everything stopped for a while, every session's place has to be kept so it comes back exactly where it was: the same conversation, the same folder and pane, nothing he typed lost, nothing on another machine killed, and the work that lived only inside a running session brought back. He wants this fast. The first time it was done by hand it took about half an hour, sent one of his half-written messages, and almost killed two remote sessions. The script below does the mechanics in seconds. Your part is the judgment around it.

`scripts/savepoint.py` (run with `python3`; `--help` lists every command) has five commands:

- `save` records every running Herdr session's panes: each agent's live resume id, read from the agent's own records, plus any text in its input box, signs of live work, ssh panes and detached jobs. It stops nothing and takes about two seconds. The record goes to `~/.agent-save-points/<time>/save.json`, with `~/.agent-save-points/latest` pointing at it.
- `stop` exits the saved agents in parallel.
- `resume` brings them back a few at a time, the ones with live work first.
- `tmp-save` and `tmp-restore` are for a computer restart only.

Each command prints a short summary. Read `save.json` when you need the detail.

## The usual path

1. Run `save` and read its summary. Save is cheap and safe, so when he only wants a save point, this is the whole job.
2. Before anything stops, look at what the summary flagged: input boxes with text in them, ssh panes, sessions with live work, and your own session. The sections below say why each matters.
3. If he asked to stop everything, or is restarting, run `stop`. For a restart, also run `tmp-save` in the background as soon as you know, because it takes minutes on a large /tmp. Then read [references/restart.md](references/restart.md) for what else a restart takes away.
4. Tell him in a few lines what is saved, what you left alone and why, the one command that resumes you, and when it is safe to restart.
5. To bring things back: after a restart, `tmp-restore` first, then `resume`. Then send a note to each session that had live work, and restart the detached jobs that need it.

## What to keep in mind

**Text in an input box belongs to whoever typed it.** A session's input box can hold a message Amir is halfway through, sometimes over several lines. Any keystroke you send to that pane lands in his message. On October 25 the stop typed `/exit` into the Chief morning session while his long message sat in the box: his message went out with `/exit` on the end, and the agent acted on it. `stop` re-reads the box just before touching a pane and leaves alone any pane with typed text in it. The greyed-out suggestion Claude Code shows on its own is not typing. When a pane is skipped, tell him which one and what the text says, and he will send it or clear it. A draft recorded by `save` is put back in the box by `resume`, unsent.

**Where a session runs decides what a restart does to it.** A restart ends everything running on this computer, and the resume id brings it back. A session on another machine keeps running only if it doesn't depend on this computer's connection to it. Inside tmux or screen on that machine, it survives the disconnect. Started straight from the ssh login, it dies the moment the connection closes. That happened on October 25: 5p and subgame on the home server were running directly under sshd. So for each ssh pane, check on the remote machine whether the agent's process sits under a tmux server or under sshd. If it's tied to the connection, the way to keep it alive is to exit it cleanly, resume it inside tmux on that machine, and reattach the pane later. The exact commands are in the restart reference. When the computer isn't restarting and the connection will stay up, leave remote sessions alone.

**A stop ends more than the conversation.** Background shells, monitors, helper agents, a paired reviewer's run and any headless child sessions die with the session that started them. A cloud machine or remote job it was watching keeps running, and keeps costing money, with nobody watching it. Scheduled jobs (`CronCreate`) came back with their sessions on October 25, but check with `CronList` rather than assuming. `save` records the signs of live work for each session: the spinner, shell and monitor counts on its status line, and any reviewer threads and child agents under it. After `resume`, give each of those sessions one line, labeled as from Chief: it was stopped for the restart, here is what stopped with it, re-arm what it needs. Name what the save shows, such as the reviewer's conversation, an ask of Amir's it was carrying out, or a machine it was watching. A session that was stopped mid-turn should be told so. A session that was idle comes back without a note, since a note would only start a turn that finds nothing to do.

**A session's id comes from its own record, never from the screen.** Claude Code writes `<home>/.claude/sessions/<pid>.json` for each running process, and Codex holds its thread's rollout file open. That is how `save` gets ids without stopping anything. AI Manager can fork a session onto a new id when it moves accounts, so the id printed at exit is the newest, and `stop` keeps it. Resuming an older id wakes a session in the past: on October 25 a backstop resumed the watcher from an old copy, and it lost forty minutes of work until it read its newer copy.

**Bringing sessions back costs the machine.** Each AI Manager resume reads every transcript on the machine for up to a minute and holds several gigabytes while it does. Thirty resumes started together right after a boot stack that thirty times. `resume` brings back three at a time by default, sessions with live work first, and reports free memory after each batch. If memory falls between batches, slow down.

**Herdr keeps its layouts across a restart.** Session names, pane ids and folders come back the same, so the save's pane keys still work. A Herdr session that isn't running after a boot comes back when someone attaches to it with `herdr session attach <name>` from a terminal window. Until then, any command against it fails with `server_not_running`. `resume` lists those sessions. Tell Amir which ones to open, then resume them.

**You are one of the sessions.** `save` marks your own pane and `stop` never touches it. Before a restart, give Amir your own resume command, the line `save` prints for this session, and ask him to say "restore" once he has resumed you. Then run `resume` against the save point.

## When something doesn't fit

The script knows Claude Code, Codex, Kimi and ssh panes. Anything else in a pane (a dev server, a script, another agent's interface) shows up as `other` with its command. Decide case by case whether it needs a clean stop and a restart command, and record what you did in the save point folder. When `stop` reports "check the pane", read the pane before doing anything else. A dialog it didn't recognize may be waiting. Never answer a dialog by sending something you haven't read, and never send a feedback draft. If `resume` says a command exited, the line it quotes usually says why. For example, a session that never got a message has no transcript to resume.
