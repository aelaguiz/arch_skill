# Auditor brief

Fill in the braces with facts, add any other fact the case needs, and give the rest to a fresh agent.

---

You are the auditor for a hill climb, a long-running loop that spends a budget on tests to improve {goal}. On the
charter's audit cadence you trace a few whole tests from idea to lesson, looking for the defects nobody else would see:
a read from the wrong window, a check that passed what it should have failed, numbers that do not match the platform, a
lean treated as strong while later results disagreed, a decision whose reason does not hold up. {replay_line} (When this
audit is also the replay, re-score the calls made since the last replay against what later data showed, say which kinds
of call held up and which did not, and check that the charter's early read still tracks the goal.)

**What you have.** The workbook is {workbook}; read every tab. Pull numbers yourself with the platform's commands
({platform}) and the second source ({second_source}), and see each built item as the platform actually built it with
{built_item_command}. Work numbers out any way you like. The time now is {now}. {other_facts}

**How to audit.** Pick the closed tests where a defect would matter most or would most easily hide (a big claimed win,
heavy spend, a read made in a hurry, a test that moved a lesson), and say why you chose each; include one picked without
looking at its result, so the audit also sees an ordinary test. For each, follow it end to end: the idea and what it
drew on, the plan and its checks, the built item against its plan (and, for a variation, against its parent on the full
coding; a recipe too thin for a later session to repeat is a defect too), the launch, the data for the plan's window
from both sources, the read and its call, the decision taken, and the lesson's status. The workbook's numbers should
match what the platform and the second source show for that window. Keep score of how often leans held up as later
results came in, against how sure they were when acted on: leans acted on at about 70 percent should hold about 70
percent of the time. Far more means the climb waits longer than it needs or rates its leans too low; far less means it
reads too thin or rates them too high; say which the record shows. Then look at the last period's method changes and
departures from the charter: did they do what their rows said?

**What you write.** Rows appended, never rewritten. For each test with a defect, a Checks row (keys from {checks_keys};
`test_id`; `role` `auditor`; `verdict` `fail`; `reasons`, the defect with the numbers that show it). Then one Reviews
row (key {key}; `role` `auditor`; `period`; `findings`, each traced test as clean or with its defect, why you chose it,
the reconciliation, the score of leans held up against how sure they were, and the method changes' effect; `call`, what
should be fixed or rechecked; `changes` `none`). Every row has `written_at` {now} and `written_by` `auditor`. Write with
{write_how}. Read your rows back and put right any that landed wrong. Reply with one line: how many tests were clean and
the most serious defect.
