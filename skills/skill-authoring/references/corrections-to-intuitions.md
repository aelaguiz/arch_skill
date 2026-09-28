# Corrections To Intuitions

Read this when a user corrects an agent's work and the correction should change
how future agents work: an entry in a corrections ledger, a skill or prompt
edit, an `AGENTS.md` rule, a memory, or the brief for the next worker.

## What a correction is

A correction is the user showing you something they see that you did not. The
goal is not to stop this one incident from happening again. The goal is for the
next agent to see what the user saw, including in cases that look nothing like
this one.

That takes understanding before writing. You understand a correction when you
can say why it is wrong: what it costs the person on the other end (the learner,
reader, customer or reviewer). "The lesson defined the river" says what went
wrong. "We talked down to a player four tracks in, so they tuned out right where
the new idea was" says why, and the why is what the next agent can use.

## Why rules shaped like the incident fail

A rule named after the incident teaches the next agent to recognize that
incident. A case in different clothes passes every rule and ships, and the user
has to correct the same thing again.

A real sequence from a lesson-authoring system shows how it goes:
1. **Graded questions.** The user said lessons deep in the curriculum were
   re-teaching which poker hand wins. The fix became a rule about graded
   questions.
2. **Walkthroughs.** The same problem came back in walkthroughs, and the rule
   was patched to "walkthroughs too".
3. **Terminology.** It came back again as a Track 5 lesson telling the player,
   seven times, that the river is the last card.

The idea under all three was never written down: write for the learner who has
reached this point, not for someone opening the app for the first time. Each
rule was a correct description of one incident. None of them taught anyone to
see the problem.

Incident rules also pile up. Each one adds an item to the list a reviewer runs,
the reviewer checks items instead of looking, and passing the list starts to
mean passing. Invented thresholds, such as a 70% bar or "1 point to spare",
make a judgment checkable for one case and then get copied as precedent for
cases they do not fit.

## The practice

1. **Understand what they saw.** Restate the correction as what the user
   perceived and what it costs the person on the other end. If you cannot say
   why it is wrong, ask the user one question rather than guessing.
2. **Find how far it reaches.** Ask what else the user would object to for the
   same reason, and look for two or three real cases that look different from
   the incident: other surfaces, other artifacts, other repos. Most corrections
   reach well past their case, some reach less far than a first guess, and a
   few turn out to be facts. Keep the user's repair scope (what to fix now)
   separate from reach (how far the lesson goes). "Only fix the new section"
   limits today's work, not the lesson.
3. **Fold it into what is already taught.** Most corrections sharpen an
   intuition you already teach, or reveal that several existing rules were
   instances of one idea. Strengthen that intuition with the new case as a
   different-looking example and, if needed, a clearer reason. When several
   rules share one reason, replace them with the intuition and keep them as
   examples. Name a new intuition only when nothing already covers it.
4. **Teach it where the judgment is made.** Put it once, in the doctrine an
   agent reads while making that call, and let other surfaces point to it.
   Write the intuition in plain words, then why it matters (the cost to the
   person), then two to four examples that differ from each other, the incident
   being one. Then give the question a good practitioner asks while looking.
   That question is a way of seeing, not a pass/fail gate.
5. **Check that it carried.** Give a clean agent, one that has not seen the
   incident, a case that looks different from it, with no hint. If it catches
   the case, the teaching transferred. Replaying the incident only proves
   recall. If the clean agent misses, the intuition is unclear or sits where the
   judgment is not made. Fix the teaching instead of adding a rule.

## When a rule is right

Use a rule or a mechanical check for facts, not judgment: a schema, a shipped
surface, a committed file, a required approval, an exact command. One way to
tell them apart: could two careful experts disagree about a given case? If they
could, it is judgment, and you teach the intuition. If the answer can be looked
up, it is a fact, and you check it.

An explicit preference the user states as a rule (a banned word, a required
format) is a fact about what they want. Record it as they said it, without
dressing it up as an intuition.

## Signs you wrote a rule instead

- It names the surface where the incident happened ("in graded questions", "in
  two-player headlines") when the reason applies more widely.
- It would catch the next case only if that case looks like this one.
- It contains a number you picked so the call could be checked.
- It adds one more item to a list that reviewers run.
- Its reason is missing, or is "because the user said so".
- Its only test replays the incident.

## Worked examples

**A lesson that talks down.** The user objects that a Track 5 lesson keeps
telling the player "the river is the last card".
- **Incident rule:** "Don't define terms taught in earlier tracks", plus a
  reviewer check for redefined street names. A later lesson that re-explains a
  value bet passes, because a value bet is not a street name.
- **Intuition:** the learner has a history. By this lesson they have done
  everything before it, so build on what they know and what they have just
  seen, and spend the words on the one new thing. It reaches vocabulary,
  re-explained skills, walkthroughs, a reason restated on every row, and a
  situation re-established that the learner already holds. It folds into the
  same idea as earlier corrections about replaying a hand the learner just
  watched and re-teaching a skill an earlier track taught.
- **Transfer check:** a clean reviewer, never told about the river, flags a
  different case, such as a later lesson re-explaining something an earlier
  track taught.

**A claim nobody opened.** The user finds a worker's "screenshots verified"
next to screenshots of a blank page.
- **Incident rule:** "Open screenshots before accepting them."
- **Intuition:** you only know what you have looked at. A claim about an
  artifact is not evidence until you open the artifact and check its substance.
  It reaches spreadsheets whose math nobody checked, reports summarized without
  reading them, "tests pass" without output, and a deploy called done without
  checking the live system.
- **Transfer check:** a clean agent handed a worker's report that says "the
  sheet totals match" opens the sheet before relaying it.

## Recording a correction

When a correction goes into a ledger or memory, lead with what the user saw and
the intuition. Then record how far it reaches, the examples (the incident is
one), what was repaired now, where the intuition is taught, and the transfer
check. Keep the user's words verbatim as evidence.
