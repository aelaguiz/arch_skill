---
name: paired-reviewer
description: "Explicitly selected long-lived reviewer for the session you are working in: start one reviewer on another model, resume it every period to read this session's transcript and critique it against the user's goals, and act on what holds up. Use when the user invokes $paired-reviewer or asks to pair a reviewer or evaluator with this session. Not the in-loop intent advocate you consult at decisions (intent-police), a one-shot independent opinion (fresh-consult), a code review, or the fleet watcher (agent-watcher)."
metadata:
  short-description: "A reviewer on another model that critiques this session every period"
---

# Paired Reviewer

Over a long run you lose the why. You forget the north star of the whole
effort, get absorbed in the piece in front of you, start obeying rules you
wrote for yourself, and stop seeing it, because you are inside it. A reviewer
on a different model, with no stake in your plan, reading what you actually
did, sees it. Your job here is to start that reviewer, ask it again on time,
and act on what it finds that holds up. You stay in charge of every decision;
the user's own words stay the only authority on what the work is for.

Run this only when the user selects it. The reviewer only reads and keeps its
own notes; it never edits the work, changes state, or starts other agents.

## Start the reviewer

Use the model or harness the user named. Otherwise pick a different provider
from yours that is installed on this machine: Antigravity (`agy`, Gemini 4
Argon) when it is here; otherwise Codex for a Claude session and Claude for a
Codex session. A different provider is the point: the same model shares your
blind spots.

Read `../_shared/agent-orchestration-policy.md`, then start the reviewer as a
fresh, resumable external session with the command shapes in
`$agent-delegate`'s `references/model-and-invocation.md`: only its "Fresh"
and "Resume" sections for your reviewer's runtime (for Antigravity, "agy
Fresh" and "agy Resume"). Run it from your working folder. Send it the
prompt below with your own session id: in Claude Code it is
`$CLAUDE_CODE_SESSION_ID`, in Codex `$CODEX_THREAD_ID`. Give it a notes file
outside your working tree, somewhere that lasts as long as the work, and send
the same path at every check-in.

Start it as soon as there is something to review, not one period from now.
That is usually right away: a user who asks for a reviewer partway through a
session already has work on the page. If the session has only just begun,
start it once you have a plan or a first result for it to read.

Write one line where you will find it after a compaction or a restart, in the
plan or run notes you already keep: the reviewer's runtime, model,
conversation id, working folder and notes file, your check-in period, and your
own session id at the start. Without it, a compacted you starts a second
reviewer that knows nothing.

## The prompt

Send exactly this, filling only the brackets:

> Read [claude or codex] session [your current session id]. Deeply understand what I'm trying to accomplish with it: the original goals, the north star of this whole effort, not just the current task. Then tell me:
>
> - Does it still remember what it's doing, or has it lost context over time?
> - Is it on track for my ask, or has it lost its way or digressed?
> - Where is it being stupid?
> - What is it doing that just wastes wall-clock time and adds no real value?
> - Where is it shortcutting the process or breaking the rules?
> - Is it artificially blocking itself? Has it invented constraints that never came from me?
> - What's dangerous or moving us in the wrong direction?
>
> [One line for this kind of work.]
>
> Keep notes in [notes file]. Start from them each time: read what they say you haven't read yet and what's happened since. Add to them as you go, not at the end: what you've read, what you couldn't read, what you found and where. If you lose your context, your notes are all you'll have.
>
> Critically evaluate it; don't just report back what it's doing. Give me your full analysis. Only read; don't change anything except your notes.

The prompt is in the user's voice and about "it" because the reviewer works
for the user, not for you. It is short because the reviewer's job is to read
the session: the id is all the briefing it needs. Do not add your summary of
the goal, your status, or a narrower question; any of those puts your framing
in the reviewer's head, which is the thing it exists to be free of.

The notes are there because a long session does not fit in the reviewer's
context. When its harness compacts that context, what it read is gone, and a
reviewer writing from a summary fills the gaps with details that sound right
and are not there. Its notes are what it picks up from after a compaction and
at every check-in.

The one line for the kind of work is a question the user would ask about this
work, in the user's words. Some the user has asked:

- An experiment or optimization loop: "Is it rigorous? Is it scientific? Is
  it just vibes? Is it effectively hill climbing or is it trying random
  things? Does it have a clear hypothesis?"
- Building to the user's requirements: "Review the implementation so far versus my
  requirements. Name any requirements I've named that are not addressed."
- Producing through a process you agreed: "Is it actually building it
  according to our process? Is it keeping the spreadsheet up to date?"
- Producing results to be trusted: "Audit its work: is it good, any issues,
  oversights, mistakes?"

## Check in on time

After the first review, every period while you are working, resume that same
reviewer with the same prompt and your current session id. The period is the
user's number; with none, 30 minutes. Run the check-in in the background and
keep working; while there is work to do, never sit waiting for a review.

- In Claude Code, a background shell command that waits out the period and
  then runs the resume wakes you when it finishes; arm the next one when you
  read the review. Do not look in on the reviewer while it reads: its
  finishing wakes you, and checking its progress spends turns on nothing.
- In Codex, nothing wakes you when a background command finishes. Start the
  resume in the background and look at it between your own steps once the
  period has passed; read the review when it is there.

When your work is done and a review is already running, read it before you
report: it is the last look at the finished work, and catching a problem now
is cheaper than after the user has taken your word that it is done.

Send the prompt in full every time. The questions carry the stance. A
reviewer asked "check again" drifts into reporting what you did, which is no
use to you.

A resume must come back on the same conversation id. `agy` silently starts a
new conversation when it cannot find an id, and a new conversation has
forgotten everything, so check the id in the result before trusting the
review.

When you are stopped, waiting on the user, or done, there is nothing to
review; do not check in. After a compaction, a restart, or a move to another
account, find the reviewer's line in your notes and re-arm the check-in. Your
own session id may have changed; the prompt always carries the current one.

## Act on what holds up

A review is another agent's analysis, not the user's words. Check each claim
against your work and what the user actually said, then act on what holds up,
and act now: if it is right that you have drifted, are wasting hours, or are
blocked on a constraint nobody set, that is the moment the reviewer paid for
itself. Put a point that is about to cost hours first.

Leave the rest. The reviewer can be wrong about facts, about the user's rules,
or about what is in scope. A requirement the user named that you missed
counts; a requirement the reviewer would like does not. Do not argue with it
point by point, and do not take its findings to the user as questions: its
next read shows what you did. When a point would change what the user asked
for, the user's words decide.

## Replace it when it stops helping

A reviewer whose answers turn into summaries of your logs, repeat the last
review, come back garbled, or will not resume has stopped helping. Start a
fresh one with the same prompt and a new notes file, and update your notes.
If you have moved accounts since the work began, a fresh reviewer sees only
what your session carried over, so also give it the session id you started
with; that is where the user's original ask is.

## Finish

When the work is done, stop checking in, and name the reviewer's conversation
id in your final report so the user can read it with `$agent-history`.
