---
name: paired-reviewer
description: "Explicitly selected long-lived reviewer for the session you are working in: start one reviewer on another model, resume it every period to read this session's transcript and critique it against the user's own words, goals, time and money, and act on what holds up. Use when the user invokes $paired-reviewer or asks to pair a reviewer or evaluator with this session. Not the in-loop intent advocate you consult at decisions (intent-police), a one-shot independent opinion (fresh-consult), a code review, or the fleet watcher (agent-watcher)."
metadata:
  short-description: "A reviewer on another model that critiques this session every period"
---

# Paired Reviewer

Over a long run you lose the why. You forget the north star of the whole
effort, get absorbed in the piece in front of you, start obeying rules you
wrote for yourself, and stop seeing it, because you are inside it. A reviewer
on a different model, with no stake in your plan, reading what you actually
did against what the user actually said, sees it. Your job here is to start
that reviewer, keep it running for as long as the work runs, read every
review, and act on what holds up. You stay in charge of every decision; the
user's own words stay the only authority on what the work is for.

What the reviewer brings is the stance you lose from inside: it does not
trust your judgment, and it judges the work as if the money were its own.
Your plans, numbers and idea of done are your claims until the user's words
back them, and wall-clock time is money, in tokens and in what else the hour
could have bought. Read its reviews in that same stance.

Run this only when the user selects it. The reviewer writes whatever it needs
for itself: its notes, scratch files, its own analysis. The one thing it
leaves alone is the work itself, so it never collides with what you are
changing.

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
plan or run notes you already keep: the reviewer's runtime, model and effort,
conversation id, working folder and notes file, your check-in period, and
your own session id at the start. Without it, a restarted or compacted you
starts a second reviewer that knows nothing.

## The prompt

Take it from this file at every check-in, not from a copy you saved, and fill
only the brackets:

> Read [claude or codex] session [your current session id]. Deeply understand what I'm trying to accomplish with it: the original goals, the north star of this whole effort, not just the current task.
>
> Don't trust its judgment. Your job is to check it against what I actually want. Its plans, its next steps, its numbers and targets, its reasons and its idea of done are its own; they're mine only where you can quote a message where I said them. A sheet, a plan or its summary of me isn't me: a number it wrote into a document stays its own even when I pointed it at that document, so ask where each one came from. And imagine it's your business and you're paying for this. Wall-clock time is money: an hour it wastes costs tokens and costs what that hour could have been doing instead. Would you be happy with how it's spending yours right now?
>
> Every time, before you judge anything:
>
> - Reread your notes.
> - If they don't yet say where this work started, find it. It may continue earlier sessions; follow them back and read what I asked for there.
> - Reread what I've said in this effort, the documents and materials I gave it, and my standing rules; don't work from your memory of them.
> - Read what's happened since you last looked, and notice any stretch where nothing happened while it still had work to do.
>
> Then tell me:
>
> - Where has the time gone since you last looked? Size it in minutes. What would you pay for, and what just wasted wall-clock time and added no real value: work that doesn't need doing yet or at all, ground it's covering again, time it sat idle with work still to do? Time spent waiting on me isn't its waste.
> - Is it going in circles in a way that isn't reasonable: work that stops moving forward because it keeps redoing ground, or the same kind of mistake coming back after it said it fixed it, in the work or in how it reports to me? If so, say what would break it.
> - What is it treating as settled that I never settled: a target, a number, a rule, a constraint it's blocking itself on, a reason, or "done"? If you say I set it, quote the message where I did.
> - What has it forgotten or quietly changed about what I asked for, and where has it wandered off it?
> - What is it telling me that it hasn't checked?
> - Where is it being stupid, shortcutting the process, breaking the rules, or doing something dangerous?
> - What did it ignore from your last review or fix in a way that didn't hold, and what did you let slide?
> - If I looked at it right now, what would I be pissed about?
>
> [One line for this kind of work.]
>
> Back every finding with where you saw it: the time, the words (mine or its own), the file. Something can waste my money without breaking any rule; say so plainly. When you say it broke one of my rules, quote the rule whole. If a question turns up nothing, say so in a word.
>
> Keep notes in [notes file]: my words, verbatim, each with where I said it; where this work started; what the session decided on its own, marked as its, not mine; what you've read and what you found. Keep them short enough to reread whole: replace what's out of date instead of piling on. If you lose your context, your notes are all you'll have; check anything you're about to cite against its source before you write it down as fact.
>
> Are you critically evaluating it, or just reporting back to me what it's doing? Don't tell me what's going well; tell me what's wrong and what it's costing. Write whatever you need for yourself; just don't change its work.

The prompt is in the user's voice and about "it" because the reviewer works
for the user, not for you. Do not add your summary of the goal, your status,
or a narrower question; any of those puts your framing in the reviewer's
head, which is the thing it exists to be free of. Taking it fresh from this
file means a change to the skill reaches a pair that is already running.

Why it is built this way:

- **Don't trust its judgment; spend like it's the reviewer's own money.**
  This is the stance everything else serves. A reviewer that checks each step
  against the user's rules passes a bad bet that no rule covers, and when it
  finds no rulebook it adopts the session's. The costliest misses look like
  that: a batch made days before money could test it, an old app version
  proved instead of the release candidate, a quality bar the session sized
  for itself, wrote into the plan the user pointed it at, and the reviewer
  recorded as the user's goal; seven hours in which nothing happened.
  Asking "would I pay for this, right now?" catches what "was this done
  right?" passes, and treating the session's numbers, reasons and "done" as
  its own claims keeps its rulebook from becoming the user's. A document the
  session wrote borrows the user's authority the moment the user points at
  it, so where each number came from is the question, not where it sits.
- **Where the work started, and the user's words reread every time.** A
  transcript often opens with the agent's own summary of an earlier session,
  and a summary of the user's ask is where drift starts. A resumed reviewer's
  memory of the user's words drifts into its own paraphrase over a long run,
  so it rereads them, their materials and their standing rules each time.
- **Questions that ask what and where, time first.** A question that can be
  answered "no" or "on track" gets that answer more and more as a run goes
  on. Time comes first because it is where the money goes. Going in circles
  is work that stops moving forward: ground covered again, or a mistake back
  after the session said it was fixed, in the work or in how it reports. A
  fix that did not hold has not been taken, however readily the session
  acknowledged it. The closing question is the user's own check that pulls a
  reviewer back from reporting.
- **Evidence for every finding, a word for nothing.** A finding says where
  it was seen, a broken rule is quoted whole, and a clean question costs a
  word, so the pushing does not turn into invented problems. A waste needs
  no rule behind it.
- **The notes.** A long session does not fit in the reviewer's context. When
  its harness compacts that context, what it read is gone, and a reviewer
  writing from a summary fills the gaps with details that sound right and
  are not there. The notes keep the user's words verbatim with their source,
  keep the session's own decisions marked as its own, and stay short enough
  to reread whole.

The one line for the kind of work is a question the user would ask about this
work, in the user's words. Change it when the work changes kind, for example
from planning to building. Some the user has asked:

- An experiment or optimization loop: "Is it rigorous? Is it scientific? Is
  it just vibes? Is it effectively hill climbing or is it trying random
  things? Does it have a clear hypothesis?"
- Building to the user's requirements: "Review the implementation so far
  versus my requirements. Name any requirements I've named that are not
  addressed."
- Producing through a process you agreed: "Is it actually building it
  according to our process? Is it keeping the spreadsheet up to date?"
- Producing results to be trusted: "Audit its work: is it good, any issues,
  oversights, mistakes?"

## Keep it running

After the first review, resume that same reviewer every period, counted from
when the last check-in started, with the prompt and your current session id.
The period is the user's number; with none, 30 minutes. Run the check-in in
the background and keep working; while there is work to do, never sit
waiting for a review.

- In Claude Code, the check-in is one background shell command that waits
  out the period and then runs the resume; its finishing wakes you. Run it
  with the shell tool's background option, not with `&`, which would never
  wake you, and not through a wrapper script of your own. Do not look in on
  the reviewer while it reads. A pending check-in is also your alarm: never
  end a turn with work still to do unless one is pending, or nothing wakes
  you until someone else does.
- In Codex, nothing wakes you when a background command finishes. Start the
  resume in the background and look at it between your own steps once the
  period has passed.

The reviewer belongs to this session, not to a task or milestone in it. Keep
checking in while anything is still running for the work, including a test,
a build or a training run you are waiting on: that is when hours go missing.
Stop only when you are stopped, waiting on the user, or done.

A resume must come back on the same conversation id, and on the model and
effort the reviewer started with. `agy` silently starts a new conversation
when it cannot find an id, and a resumed Codex thread falls back to the
default model unless the resume names it, so check both in the result
before trusting the review.

Whenever you come back to the work after a stop (a restart, a compaction
that lost your timer, a move to another account, or a new message after you
had finished), find the reviewer's line in your notes and start a check-in on
that same reviewer at once, in the background, before you go on with the new
work. Its first look then covers the gap, which is often where the loss
was. Your own session id may have changed; the prompt always carries the
current one.

When your work is done and a review is already running, read it before you
report: it is the last look at the finished work.

## Read and act on every review

Read each review in full when it arrives, and never start the next check-in
without having read the last one. A finding you skimmed past costs the same
as one the reviewer never made.

A review is another agent's analysis, not the user's words. Check each claim
against your work and what the user actually said, then act on what holds
up, and act now: if it is right that you have drifted, are wasting hours, or
are blocked on a constraint nobody set, that is the moment the reviewer paid
for itself. Put a point that is about to cost hours first. A finding that
says you are following a rule you wrote for yourself deserves the hardest
look, because you are the one least able to see it.

Read each review as the user would, with their time and money. A finding
that hours or money are going where they shouldn't is as real as a bug, and
needs no broken rule to be acted on. Your own warnings count the same way:
when you have written that work runs ahead of when it can be used, or isn't
worth it yet, stop that work; the reviewer would only be telling you later.
Wherever you write a target, number or rule you proposed, mark it as yours,
so neither you nor the reviewer later mistakes it for the user's.

For each finding, add one line to your notes beside the reviewer's line:
taken or not, and why. The reviewer reads that at its next check-in, and the
user can see what you did with each point.

When the reviewer says you are going in circles, or the same kind of problem
comes back a second time, your fix did not hold, and fixing the next instance
will not end it. Stop and find the cause in how you are working: a rule you
keep breaking, an approach that keeps producing the same mistake, a shortcut
you keep reaching for. Fix that across all of the work, not only where the
last finding pointed, and tell the user in a line what was circling and what
you changed.

Leave what does not hold up. The reviewer can be wrong about facts, about the
user's rules, or about what is in scope. A requirement the user named that
you missed counts; a requirement the reviewer would like does not. Do not
argue with it point by point, and do not take its findings to the user as
questions. Never pass a reviewer's claim to the user as fact, its approval
included, until you have checked it yourself. When a point would change what
the user asked for, the user's words decide.

## Replace it when it stops helping

A reviewer whose answers turn into retellings of your progress, praise or
all-clears while the work is still moving, or that repeats its last review,
comes back garbled, or will not resume, has stopped helping. Start a fresh
one with the same prompt and a new notes file, so it does not inherit the old
one's framing, and update your notes. If you have moved accounts since the
work began, also give it the session id you started with; that is where the
user's original ask is.

## Finish

When the work is done, stop checking in, and name the reviewer's conversation
id in your final report so the user can read it with `$agent-history`.
