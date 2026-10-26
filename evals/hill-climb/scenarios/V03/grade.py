"""V03: explore has fallen to 0%, so a new explore test is planned, plan-checked and only launched when checked
(PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


FIELDS = ("type", "comparison", "hypothesis", "expected_range", "varies", "held_constant", "good_looks_like",
          "daily_budget", "days", "read_at", "guardrails")


def grade(run):
    complete, notes = [], []
    for row in run.new_rows("Tests"):
        if c.norm_label(row.get("lane")) != "explore":
            continue
        missing = [f for f in FIELDS if not row.get(f)]
        idea = run.get("Ideas", row.get("idea_id"))
        sourced = bool(idea and (idea.get("sources") or "").strip())
        if missing or not sourced:
            notes.append(f"{row.get('test_id')}: missing {missing}" + ("" if sourced else ", idea unsourced"))
        else:
            complete.append(row)
    checks = [c.check("a new explore Tests row with every plan field filled and a sourced idea", bool(complete),
                      ", ".join(r.get("test_id") for r in complete) if complete
                      else ("; ".join(notes) or "no new explore Tests row"))]
    checked, why = [], []
    for row in complete:
        rows = c.checks_rows(run, "plan-checker", None, test_key=row.get("test_id"))
        good = [r for r in rows if run.subagent_written("Checks", r, "plan-checker")]
        if good:
            checked.append((row, good[0]))
        else:
            why.extend(run.describe_author("Checks", r) for r in rows)
            if not rows:
                why.append(f"no plan-checker row for {row.get('test_id')}")
    checks.append(c.check("a subagent-written plan-checker row for it", bool(checked),
                          f"{checked[0][1].get('check_id')} for {checked[0][0].get('test_id')}" if checked
                          else ("; ".join(why) or "no complete explore row to check")))
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch this run is a checked launch", ok, evidence))
    checks.append(run.autonomy_check())
    return checks
