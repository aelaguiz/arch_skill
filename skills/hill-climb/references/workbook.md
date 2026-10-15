# The workbook: tabs, columns, and keeping it honest

Read this at setup, and before you write a kind of row for the first time in a session.

The workbook is the hill climb's memory. Every fresh session, every role agent and the owner read it to learn what
happened, so it is only as useful as it is complete and true. Nothing enforces its shape; it stays right because each
writer understands what each column is for.

Two views are for reading at a glance, so a person never has to chase keys across tabs. The Overview leads the workbook
and answers what its owner opens it for: where the bar stands now and over time, against where it started and the best
known option; what is live and when each reads; each recent test on one line with its checks' verdicts, its read and the
decision; the lessons with how sure each is; what exploring is reaching; the money left and the pace; when the next
report is due. Each Tests row tells one test's whole life on one line: its plan, its checks' verdicts, its read, the
decision taken and how its item was made, each with the key of the row behind it. Both show the roles' own words (a
check's `pass` or `fail`, a read's call), never a paraphrase of them. The other tabs are the record behind those views,
where each independent judgment is written by its own role. In a Google Sheet, put the Overview first and build it from
formulas over the record where you can, so it cannot drift from it, and lay the workbook out with
`$spreadsheet-formatting`, which keeps long notes and history off the reading view.

## Form

A Google Sheet (written with the host's Sheets tool) or, where the host cannot reach Google Sheets, a folder of CSV
files named after the tabs (`Tests.csv` and so on). In CSV, append rows with a CSV library rather than joining strings,
so commas, quotes and line breaks inside a cell survive. Create every tab with its columns at setup, the ones that start
empty too: every later writer appends, and a row appended where no header is has no columns to land in. Append; never
rewrite a whole tab to add a row, because a role writing the same tab at the same moment would lose its row. To change a
row in place, read the whole tab first, write the changed tab to a new file, then move it over the old one: opening a
tab for writing empties it at once, and a mistake before the rows are back loses the record. Two roles change rows in
place: the strategist (the Charter's revisable fields) and the scout (a Library item's status); the main agent
dispatches nothing else that writes the same tab while either runs. After a write, read the rows back: a write that
failed quietly leaves every later session working from a wrong record.

## Rules every row follows

- **Keys** are the tab's prefix and the next number: Library `LB-`, Ideas `ID-`, Tests `T-`, Checks `CK-`, Results `R-`,
  Decisions `D-`, Lessons `L-`, Reviews `RV-`, Money `M-`, Log `LG-`. The Charter's key is its `field`, the Map's its
  `type` and the Overview's its `item`.
- **`written_at`** is the platform's current time; **`written_by`** is `main` or the role's name. Without them, nobody
  can tell what was known when, or whether a check was really independent.
- **Results, Decisions, Checks, Reviews, Money and Log rows are never edited.** A correction is a new row that names the
  row it corrects. The record of what was believed at the time is the point.
- **Charter, Ideas, Map, Library and Lessons rows are updated in place**, as are a Tests row's status, ids, a live
  test's budget and its summary columns (`checks`, `read`, `decision`); each change adds a line to the row's `history`
  (what changed, from what, when, by whom). The Overview is a view: formulas over the record in a Google Sheet,
  otherwise rewritten whole each tick.
- **A revised plan is a new Tests row** with the same `idea_id`; the old one becomes `withdrawn`. A plan that changed
  after it was checked would no longer be the plan that was checked.
- **Labels** in brackets below (statuses, kinds, calls) are the record's usual words. When none fits, write a clearer
  one and say why in the row.
- **A live test's Map cell stays `untested`** until its first read; nothing is known about it yet.
- **Roles get their keys from you.** When you dispatch a role, give it the key its row will use, or a block of keys when
  it writes several rows, so roles working at once never collide.

## The tabs

`type` is a map cell, written as `attr=value` pairs in the Charter's attribute order joined by `|` (for example
`headline=price-first|image=photo`).

| Tab | Columns | What it is for |
|---|---|---|
| Charter | field, value, reason, history | the goal, the owner's limits and the climb's chosen method, each with its reason |
| Overview | item, value, as_of | where the climb stands, for reading at a glance: the bar now and at the start, money left and the pace, what is live and when each reads, the best known option, proven lessons, what comes next |
| Library | library_id, kind, source, link, owner, content, signal, type, coding, status (fresh, stale), notes, legacy_ref | the research ideas draw on, each with where it came from, why it counts and its values on the full coding |
| Ideas | idea_id, source (main, scout, strategist, meta-analyst, legacy), type, description, sources, near_copy_of, status (new, planned, tested, parked, rejected), reason, legacy_ref | what could be tested next, and what each idea draws on |
| Map | type, best_test_id, best_result, tests_count, last_tested, status (best, tested, untested, stale), history | which cells are known, best, stale or untried |
| Tests | test_id, idea_id, lane (confirm, explore, exploit), type, comparison, hypothesis, expected_range, varies, held_constant, good_looks_like, daily_budget, days, read_at, guardrails, rerun_of, lesson_id, item_id, made_from, recipe, coding, platform_id, status (planned, plan-checked, built, ready, live, paused, read, closed, withdrawn), launched_at, checks, read, decision, legacy_ref, history | each test's whole life on one row: the plan written before money moves, how its item was made, its checks' verdicts, its read and the decision, and where it stands |
| Checks | check_id, test_id, item_id, role, verdict (pass, fail), reasons | each independent check and why |
| Results | result_id, test_id, window, metric, k, n, spend, rate_text, versus, chance_beats, method, signals, call (act, hold, stop, legacy), notes, legacy_ref | each read, with the numbers, how the reader got its estimate, the soft signals around the item, and the call |
| Decisions | decision_id, test_id, kind (launch, pause, resume, shift, scale, rerun, retire, exclude-data, void, method-change, money-request, grant), reason, data, legacy_ref | each move, why it was made, and the evidence |
| Lessons | lesson_id, subject, statement, winner, loser, status (unconfirmed, proven, recheck, retired), evidence, recheck_at, legacy_ref, history | what has been learned and how far to trust it |
| Reviews | review_id, role, period, findings, call, changes | each step-back, strategy review, audit and progress report |
| Money | entry_id, kind (allocate, request, grant, refusal), lane, amount, standing, learned, next, note | the money: lanes, requests and answers |
| Log | tick_id, platform_time, read, did, next | each tick in one row, for the next session |

Every tab also has `written_at` and `written_by` as its last two columns. `shift` moves confirm or explore money;
`scale` moves exploit money onto an option.
