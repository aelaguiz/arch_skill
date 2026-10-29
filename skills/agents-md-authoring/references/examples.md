# Rule piles and the intuitions under them

Each example shows lines from a real instruction file, the understanding they were reaching for, and what changes when the file says that instead. Look for the move from the lines to the understanding, not for the case.

## Five bans that were one idea

A website repo's file grew a numbered list of "explicitly outlawed behaviors" after one bad day, each a paragraph: running the copy checks after publishing instead of before; calling a skill "passed" without running it; checking three hand-picked claims and reporting the page as checked; calling copy "pre-approved" without showing where it was approved; naming a skill in a report as though naming it ran it. The next variation would have been number six.

Under all five: a check counts only if it happened, and saying it did tells everyone else they can stop looking. An agent holding that won't write "reviewed" over a review it skimmed, which none of the five named.

## A section that was already an intuition

A mobile app's bug-fix section ran about 600 words: reproduce before fixing; name the cause at file and line; label a retry or a filter as a mitigation, not a repair; never mute an alert before finding what produces it; show which build a device verdict ran on; don't close an issue while it still fires. Every bullet protects one thing: a fix is real when it changes what caused the bug, shown on the build users will run, and anything else hides the symptom.

The file needs that sentence and the facts an agent can't work out: where the reproduction note goes in the pull request, and the command that proves which build is installed. An agent holding the sentence also refuses the fix nobody listed, such as raising a rate limit until an error stops appearing.

## A paragraph said in a breath

The same file explained, in about 200 words, how to verify faster: shrink a 15-minute timeout to 30 seconds in config, seed state so the run starts at the failure point, re-enter a long journey at the failing step instead of step 1, except when real elapsed time is the mechanism, as with suspension, cron cadence or store propagation.

In a breath: "Proof attaches to the mechanism, not the clock." An agent that understands it shrinks the timeout, and also leaves the store-propagation wait alone, because there the clock is the mechanism.

## A ban list and the reason it came from

Before: "Do not propose or design 'second pair of eyes,' 'dual sign-off,' 'staged review,' 'RFC process,' 'committee approval,' or other enterprise-shaped process gates." The next agent invents a gate with a sixth name.

The same file already said why: "This is a two-person startup… The default outcome for a startup is running out of time and money." An agent holding that asks of any process whether it prevents a real failure for less than it costs, and drops the gate whatever it is called. It also keeps the one check that does pay for itself, which a ban list can't tell apart from the rest.

A sibling repo's file turned the same sentence into a list of things not to build: adjacent refactors, helpers, wrappers, defensive branches, edge-case handling the request doesn't need. The sentence already produces that list, and the next item on it too, so the list isn't a fact to keep.

## Pointers, not reading lists

OpenAI's guidance for GPT-6 contrasts "Before every edit, read architecture.md, database.md, and deployment.md" with "Use architecture.md for service boundaries, database.md for schema changes…". The first makes every edit pay for three documents. The second says which question each document answers, so the agent opens the right one when that question comes up.

## A correction phrased as a rule

The website file said: "A check counts only if it happened, and saying it did tells everyone else they can stop looking." Then an agent reported a page as fact-checked after checking three of its claims, and the owner said: "Never report a gate as passed on a subset."

- Not this: a new paragraph beside it, "Never report a check as passed when you checked only some of the claims, because readers assume every claim was checked."
- Like this: the existing sentence reaches the case once its words do: "A check counts only if it happened, to everything it claims to cover, and saying it did tells everyone else they can stop looking."

The owner's words named one way of faking a check. The file already had the idea; it needed to reach a little further, not a second instruction next to it.

## A correction that needed no new line

A file said "Proof attaches to the mechanism, not the clock." An agent then re-ran a 40-minute end-to-end journey from the start to check a one-line fix in its last step, and was corrected.

- Not this: a new line, "Re-enter long journeys at the failing step."
- Like this: no new line. The intuition already covered it; the agent hadn't seen a long setup before the step that matters as "the clock". If the file changes at all, the intuition reaches further: "…not the clock, whether that is a timer or a long setup before the step that matters."

Most corrections land this way when a file is built from intuitions: the agent missed or misread one, and the fix is to make that one clearer, not to add a line that only this case will ever match.

## What a revised file looks like

A mobile app's file had grown to about 4,900 words under twenty headings. Read whole, it kept returning to a few concerns, and the rewrite is those plus the facts:

```md
# AGENTS.md

This file is a few intuitions about working here; a new lesson deepens the one it belongs to.

We are a two-person startup, and running out of time and money is the real risk: build what was asked, as the smallest change that does it.
A fix is real when it changes what caused the bug, shown on the build users will run; anything else hides the symptom.
Proof attaches to the mechanism, not the clock.
A fresh worktree has none of the local configs, and every build in it fails until they are there.

## Facts
- Hydrate a new worktree with `zsh -ic 'cd <worktree> && gwtc'` (`gwtc staging` for staging).
- Setup: `make setup && make flutter-setup`; run: `make flutter-dev FLUTTER_PLATFORM=ios`.
- Check: `make flutter-lint`, then the tests that cover the change.
- `make flutter-sync` owns the generated asset block in `apps/flutter/pubspec.yaml`.
- Deeper guides, each linked with when to read it: device QA, releases, the content pipeline.
```

The intuitions sit at the top, each a sentence. Most of the old headings had no line of their own left, because one of these sentences produced everything under them.
