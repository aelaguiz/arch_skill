---
name: agents-md-authoring
description: "Write, revise or audit always-on instruction files (AGENTS.md, CLAUDE.md, GEMINI.md, AGENTS.override.md, global instruction files) as a few intuitions about the project rather than a pile of rules: land each new lesson or correction by deepening the intuition it belongs to, collapse rules into the understanding under them, and keep the docs the file points to teaching the same thing. Use when creating one of these files, adding a lesson, correction or rule to one, or when one has grown long, rule-heavy or contradictory. Builds each intuition with $intuition-building. Not for skills ($skill-authoring) or prompts ($prompt-authoring)."
---

# AGENTS.md Authoring

An always-on file is how a project passes its understanding to every agent that works in it. Each session reads it first, then meets situations its authors never pictured. A list of what to do helps only in the cases on the list. What carries into the rest is a sense of what matters here and why: what is at stake, who pays when it goes wrong, what looks important and isn't. That is an intuition, and a good file is mostly a handful of them. Build each one with `$intuition-building`. Current models act well on an understood reason and get worse with every special case they have to steer around.

## Find the intuition under the rules

Most long files are rules that one intuition would have produced. Five numbered bans on faking a review (gating copy after it shipped, calling a skill "passed" without running it, checking three claims and calling the page checked) are one idea: a check counts only if it happened, and saying it did tells everyone else to stop looking. "Proof attaches to the mechanism, not the clock" covers shrinking a timeout to test it, entering a long journey at the failing step, and, read the other way, waiting out a delay that is itself the thing being tested. When a group of lines keeps circling one concern, say the concern, and the lines it produces can go.

An intuition someone understands fits in a breath. If it takes a paragraph, the incident it came from is still in it: the date, the story, the quote. Those belong in the commit message; the file keeps what the incident taught.

## When a lesson arrives

A correction or a mistake shows that an agent couldn't see something. It usually arrives already phrased as a rule ("never X", "always Y", a date, a quote), because that is how a person states a fix in the middle of work. The wording tells you what they saw; it is not the line to add, and attaching a reason to it doesn't change that. Find the intuition in the file that should have let the agent see, and work out why it didn't: it was missing, too vague, or read too literally. Rewrite that intuition's own words so it would have caught this case and still handles the old ones. Add a new intuition only when nothing in the file is about this. A line shaped like the incident helps only if the next case looks the same, and it won't.

A lesson that landed well usually leaves the file about as long as it found it, and a reader meets it inside an idea that was already there. If your edit gives the lesson a paragraph of its own beside the guidance it belongs to, you have added a rule with a reason; go back and change the guidance instead.

Then reread the whole file and the docs it points to. A deepened intuition usually makes other lines unnecessary; take them out. Where a linked doc says something different about the same thing, each usually holds a rule from a different incident. Find the understanding both were reaching for and make them say it, or have one point to the other.

## Is it an intuition?

Take it to a case it never mentions, then to one where the obvious move is wrong. An intuition gets both right; a rule gives the same answer to both. "Set long timers to 30 seconds when verifying a fix" is a rule, and it fakes the proof when the delay is the bug, as with a cache that must expire. "Proof attaches to the mechanism, not the clock" shrinks the timer when the mechanism stays the same and waits it out when the wait is the mechanism.

Not everything is judgment. A command, a path, a name, or a choice the owner made that no understanding would produce, such as a standing exception, is a fact and sits as a plain line beside the intuition it serves. A list the intuition already produces is not a fact: keep only the items it wouldn't.

## Revising, starting or auditing a file

Revising a file that has grown starts from the whole of it. Read it end to end and say what it keeps worrying about: usually a handful of concerns, scattered under headings that grew one incident at a time. Those concerns, each said in a breath, are the file. Every existing line is then something one of them produces, which goes; a fact an agent couldn't work out, which stays as a plain line under the intuition it serves; or something no longer true, which goes. Trimming each section in place leaves the same pile, smaller.

For a new file, read the repo and whatever shows what its people correct agents for: review comments, the README's warnings, the history of the code that keeps breaking. Write the few things an agent new here would get wrong, as intuitions, and the facts it can't find by looking, such as how to check its work. A short file that teaches what matters beats a complete one.

An audit looks for the same things a revision fixes: groups of lines circling one concern, places where the file and its docs disagree, lines the repo or the models have outgrown, and situations an agent would still get wrong. Name the intuition each group was reaching for, not just the lines to cut.

## Where things go

An intuition goes in the narrowest file that covers everywhere it applies. Worked cases, procedures and reference go in a doc the file points to, with when to read it. Leave out what an agent sees by looking: layout, frameworks, what the linter already enforces. A file that tells agents how to start other agents points to `../_shared/agent-orchestration-policy.md` instead of restating it. Codex reads one file per folder from the repo root down, an `AGENTS.override.md` replaces its folder's file, and everything past 32 KiB combined is dropped.

Agents often write a lesson into the file in the middle of other work, without this skill. A line at the top saying how the file is kept, such as "This file is a few intuitions about working here; a new lesson deepens the one it belongs to", lets them do it well.

## Check the file

Give a fresh agent the file and a few situations it never mentions, including one where the obvious move is wrong, and watch what it does. Taking a line out is a guess until an agent shows the case still comes out right.

[references/examples.md](references/examples.md) shows real rule piles next to the intuitions under them, a long paragraph said in a breath, a correction phrased as a rule landing inside the idea it belonged to, and what a revised file looks like. Read it before your first revision of a file.
