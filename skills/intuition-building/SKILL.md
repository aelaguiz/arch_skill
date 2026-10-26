---
name: intuition-building
description: "Build an intuition instead of a rule when writing anything another agent will learn from: what an intuition is, how to build one, what it is not, and when a plain rule is right, with like-this and not-like-that examples. Use when asked to teach or build an intuition, when turning a request, correction, review finding, failed test or lesson into a skill, prompt, AGENTS.md or CLAUDE.md line, memory, ledger entry or worker brief, or when guidance has hardened into heuristics, thresholds, ban lists or a pile of rules. Not for packaging a skill ($skill-authoring), prompt structure ($prompt-authoring), or writing for a human reader ($readable-reports)."
metadata:
  short-description: "What an intuition is, how to build one, and what it is not"
---

# Intuition Building

You have been asked to build an intuition, or you are about to write something another agent will learn from: a skill, a prompt, an instruction file, a memory, a brief for a worker. That agent will meet situations you can't see from here. What you write decides whether it can handle them, or only the ones you thought of.

## What an intuition is

An intuition is understanding someone can act on: a sense of what matters in a kind of situation, and why, clear enough that they make the right call in a case nobody described to them. Experienced people carry these about their work. A good editor knows a paragraph is too long without counting its words. A good engineer knows which shortcut will cost more later. Neither is following a rule. Each is seeing something.

Building an intuition for another agent means passing on that way of seeing. You describe the situation the way someone who understands it would: what is really at stake, who pays when it goes wrong, what looks important and isn't, what looks harmless and isn't. The agent then works out what to do, and when its case differs from yours, it reaches a different answer.

A rule passes on an answer instead. Someone decided in advance what to do, and the rule repeats that decision wherever it is read. It is right for the cases its author had in mind. In every other case it gives the same answer anyway, and the agent following it has no way to notice it has walked into a case the rule wasn't written for. When that goes wrong, the usual fix is another rule beside the first, and over time the guidance becomes a pile of rules that contradict each other.

A small example. Told that an assistant interrupts its user too often, you could write: "Never message the user more than once an hour." Or you could write: "Every message pulls the user away from what they are doing, so send one when it changes what they would do next, and save the rest for a summary. A production outage is worth interrupting dinner for; a test that passed can wait." The first gets the outage wrong. The second gets both right, and cases you never mentioned.

## How to build one

Start from what the person wants, not the words they used. A request, a correction or a failure shows you something somebody cares about. Work out what they saw that you didn't, and what it costs someone when it goes wrong: a user, a customer, the person paying for the work. Their words are evidence of that, not the thing itself. People talk in examples, rough numbers, questions and quick yeses. An example is one instance of what they want, a number said in passing is a rough feel, and a question is a question. If you can't say why something matters, you don't understand it yet, and anything you write down will come out as a rule.

Then look past the case in front of you. Picture situations that look nothing like it where the same thing would matter. Picture situations where the opposite would be right, because nearly every lesson pushes away from one mistake toward another on the far side: asking too much and deciding too much, spending too little and spending without looking. An intuition knows both edges. One person said it this way after an agent overcorrected: "The intuition is not 'never do it.' The intuition is 'do it the right way first.'"

Write it so a newcomer could use it. Say why, plainly. Name what to pay attention to and what to ignore. Prefer the concrete cost to the abstract instruction: "a recursive search from this folder reads half a terabyte" teaches more than "search narrowly." Give a few examples that look different from each other, including one where the answer goes the other way, so the reader finds the idea between them instead of copying one case. This is not a list of edge cases to cover. One or two examples that show where the answer turns are enough; the reader takes the rest from the reason.

If what you are teaching sharpens or corrects something already written, change that text so it says one thing. A second paragraph beside the old one leaves the next agent two instructions to reconcile.

Then read it as someone who never saw today's case, and picture them in a new one, including a case where the right move is different. If your text would hand them today's answer anyway, you have written a rule; go back and understand more, rather than adding an exception. If you can't picture any case where the right answer would differ, you may be holding a fact, and a plain rule is fine.

## What an intuition is not

It is not a rule with a reason attached. "Don't bring up the price: customers find it pushy" still gives every reader the same answer, including the one who asks what it costs.

It is not a number invented so the call can be checked. "Reply within 48 hours," "at least five items" and "95% of the time" make a judgment gradable, and the agent stops looking at the thing the number stood for.

It is not a ban list or a keyword list. Banning a word stops nobody from doing the thing under another name. Showing what the thing costs does.

It is not a template, a required phrase or a form every lesson fills in. The shape of an intuition, repeated, becomes a rule about wording.

It is not vague. "Use good judgment" and "be careful" give the reader nothing to see by. A good intuition is specific about what matters, and leaves open only what to do about it.

It is not a script or a checker that decides for the agent. Code that applies a fixed test is a rule nobody reads.

It is not one day's behavior of a tool written down as permanent. Tools change; say how to check what the tool does now.

## When a rule is the right tool

Some answers don't depend on the case. A fact (an exact command, a file path, a schema), a role ("you report and analyze; you don't make changes"), or something true in every case ("every pull request needs the approval label") is best written as a plain rule, and a simple rule beats a clever one. What tells them apart is whether the right answer could ever differ. "A working copy older than 48 hours is abandoned" fails that: age doesn't tell you whether anyone still uses it. "Every pull request needs the approval label" passes it, however casually it was said.

## Examples

[references/examples.md](references/examples.md) shows intuitions next to the rules they would replace, across the kinds of guidance agents write: turning a correction or someone's offhand words into guidance, explaining a risk, writing a check, describing a tool or anything that will change, pushing against a bad habit, passing guidance to another agent, and revising guidance that already exists. It ends with cases where a rule was right and "intuitions" that weren't. Most come from real work. Read it before you write, and look for the idea under each pair rather than the case.
