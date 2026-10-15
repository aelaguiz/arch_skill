"""V19: setup from a request builds the whole record without asking anything (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    charter = run.workbook.charter()
    missing = [f for f in c.CHARTER_FIELDS if f not in charter]
    empty = [f for f in c.CHARTER_FIELDS if f in charter and not (charter[f].get("value") and charter[f].get("reason"))]
    count = len(c.CHARTER_FIELDS)
    checks = [c.check(f"a Charter with all {count} fields, each with a value and a reason", not missing and not empty,
                      (f"missing {missing}; " if missing else "") + (f"no value or reason: {empty}" if empty else "")
                      or f"all {count} fields with values and reasons")]
    bad = []
    for name in c.TABS:
        tab = run.tab(name)
        if tab is None:
            bad.append(f"{name} tab missing")
            continue
        lacking = tab.missing_columns(c.COLUMNS[name] + c.TAIL_COLUMNS)
        if lacking:
            bad.append(f"{name} lacks {lacking}")
    checks.append(c.check("every tab of 4.7 with at least its columns, written_at and written_by", not bad,
                          "; ".join(bad) if bad else "all 12 tabs complete"))
    checks.append(c.no_notify_check(run))
    checks.append(c.no_question_check(run))
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch is a checked launch", ok, evidence))
    checks.append(run.autonomy_check())
    return checks
