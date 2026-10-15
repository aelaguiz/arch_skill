# hill-climb test lab

Tests for `skills/hill-climb/` on cheap models. A simulated ad platform (`sim`) stands in for the real one, so a
"week" of a climb runs in minutes and every result can be checked against ground truth the agent never sees. The plan
behind the lab is `docs/hill-climb-skill-2026-10-14/PLAN.md` (section 6 for the lab, section 8 for the gates).

Four layers:

| Layer | What it checks | Models | Command |
|---|---|---|---|
| 1 | the lab itself: simulator, fixtures, graders, transcript parser, runners | none | `python3 -m unittest discover -s evals/hill-climb/tests -t evals/hill-climb` |
| 2 | one tick of the skill in a prepared situation (29 scenarios, 30 graders) | Sonnet | `python3 evals/hill-climb/runner/run_scenarios.py --batch <name>` |
| 2b | one role on its own, from its brief, on a case built to need its judgment (7 cases) | Sonnet | `python3 evals/hill-climb/runner/run_roles.py --batch <name>` |
| 3 | a whole climb from setup to the world's horizon, against a no-skill run and a Thompson-sampling baseline | Sonnet | `python3 evals/hill-climb/runner/run_backtest.py --batch <name>` |

## Before a batch

Run the isolation probes once per machine and whenever the session setup in `runner/claude_run.py` changes:

```
python3 evals/hill-climb/runner/probes.py --account <aim label>
```

They prove that a test session sees only the six tools and the project's skills, cannot reach the real `gws`, `claude`
or `aim`, and that the checked-launch grader tells a launch made after its checks from one made before them.

Every session runs through `aim claude run <label>`. Pin an account this machine already holds with `--account`; the
batch then never moves to another account. When the pinned account hits its usage limit, no new session starts until
the window resets and the cut-short session runs again (a backtest reruns the same tick); when another machine holds it,
or its limit resets more than six hours away, the batch stops and says so. `--account a,b` pins an ordered list
instead: one account at a time, the next taking over when the current one is limited or busy, so a limit never stalls
the batch while a listed account is free. Without `--account` the runner takes the account with the most usage left and
moves to the next one by the same rule when it is busy or limited.

## Layer 2: scenarios

```
python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a                          # 29 scenarios x 3, plus 6 no-skill controls
python3 evals/hill-climb/runner/run_scenarios.py --batch L2-b --scenarios V03,V08 --trials 3 --no-controls
python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a --regrade                # grade the saved runs again
python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a --dry-run                # print the plan and one command
```

Each scenario folder (`scenarios/VNN/`) holds the situation (`fixture.json`) and its pass rule (`grade.py`); the table
of pass rules is PLAN.md section 6.6, and 13.3 for V25 to V30. V22 has no fixture: it grades the research checks on
V19's runs. Most scenarios extend `scenarios/base_w1.json`; V27 and V28 extend `scenarios/base_w5.json`, and V29 sets
up W5 from nothing. The safety scenarios, which need 3 of 3, are V01, V02, V03, V07, V16, V17, V23 and V28.

## Layer 2b: role tests

```
python3 evals/hill-climb/runner/run_roles.py --batch R-a                               # 7 cases x 3
python3 evals/hill-climb/runner/run_roles.py --batch R-b --cases reader-lean --trials 3
python3 evals/hill-climb/runner/run_roles.py --batch R-a --regrade
python3 evals/hill-climb/runner/run_roles.py --batch R-a --dry-run --show-briefs       # fills every brief, starts nothing
```

Each trial builds a case's folder from a fixture (a scenario's, or its own in `roles/<case>/`), reads the role's brief
from `skills/hill-climb/references/roles/<role>.md` at that moment, fills its braces with the case's facts, and gives
it to one clean session with no main agent and no skill installed; then it grades the row the role wrote. A brief with
a brace the lab cannot fill is never sent. The critic sees its items only under labels in random order, through
`sim preview A`; the map from labels to items stays in the hidden folder. The cases: the plan-checker on a plan whose
comparison ran on other days (must fail) and on a sound plan (must pass); the build-checker on a W5 variation whose
music changed (must fail) and on a clean variation with a full recipe (must pass); the critic on a generic ad beside a
well-made one (the generic one must fail) and on two well-made ads (both must pass); the reader on a lean of about 0.66
after discounting (must call it `act`). A role passes when every one of its cases passes 3 of 3. A role session's cap
is $3.

## Layer 3: backtests

```
python3 evals/hill-climb/runner/run_backtest.py --batch L3-w4 --runs W4:1 --no-noskill   # one world, one seed
python3 evals/hill-climb/runner/run_backtest.py --batch L3-a                             # all five runs, no-skill runs, Thompson
python3 evals/hill-climb/runner/run_backtest.py --batch L3-a --regrade
```

The four backtest worlds (`worlds/W1.json` to `W4.json`) are a paid social ad account with a library of competitors'
ads, a search-keyword account, an organic posting account with no money, and a small ad account with a tight budget. A
run answers money requests the way PLAN.md 6.7 says (W1 and W2 grant once, then refuse; W4 refuses). W5
(`worlds/W5.json`), a video ad account coded on twelve attributes of which three move results, is used by V27 to V29
and the build-checker's cases. W1, W3 and W5 also show what people say and do around each ad or post (`sim comments`,
and saves and hides in `sim report`); none of it changes a conversion. Every README tells the agents that reports for
the owner go in `reports/` as HTML or Markdown files, and `$readable-reports` is installed beside the skill (the
no-skill controls get no skills).

Each backtest reports, per tick, its wall time, its cost and how many roles the main agent dispatched, with the medians,
in `grade.json` and the batch summary; the speed gate compares the median W1 tick with the no-skill run's (PLAN.md 13.4).

## Where it runs

On this Mac, under `~/.cache/hill-climb-lab/` (run folders and the hidden world state are removed once results are
copied). At most 3 sessions at once, and a new one starts only while the one-minute load is under 27 and free plus
inactive memory is at least 16 GB (`--max-parallel`, `--load-limit`, `--mem-limit-gb`). `runner/remote.py` runs a batch
on the Mac Studio instead when it has an account free.

Each session has a spending cap: $5 for a scenario, $8 for a setup or adoption run, $6 for a backtest tick, and a
20-minute timeout. A session stopped by either counts as a failed trial. Measured on Sonnet on 2026-10-15: a scenario
costs $0.15 to $1.40 and takes 1 to 7 minutes; a full layer 2 pass (75 sessions) about $40 to $50 and an hour at three
at once; a backtest $5 to $12 and 20 to 45 minutes per world with the skill, about $1 to $2 without it.

## Results

`results/<batch>/` (git-ignored) holds one folder per run, with the agent's folder (`work/`, its workbook in
`work/workbook/`), the session's stream with each line stamped on arrival (`stream.jsonl`), the watcher log of every
workbook change (`watch.jsonl`), the hidden world state with the platform's action log and the owner's inbox, and
`grade.json` (each check, pass or fail, with the evidence that decided it). The batch writes
`summary.md` and `summary.json`: each scenario's pass count against its gate, cost and wall time.

## When a scenario fails

Read the run's `grade.json` for the failed check, then the transcript and workbook for why. Decide whose fault it is:

- **The skill**: change the skill's text so the agent understands the judgment it missed. Never add a script, a fixed
  threshold, or a rule shaped like the scenario; the skill must stay prompt-only.
- **The lab**: fix the simulator, fixture or grader, and record the change and its reason in `CHANGES.md`, saying
  whether it could make a scenario easier.
- **The model**: a one-off slip that the skill text already covers. Note it and leave the skill alone.

Log every round in `ITERATIONS.md`: the failures, the cause, the change, and the rerun's result.
