"""V09: a rerun that clearly held makes its lesson proven, with a recheck date (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    lesson = run.get("Lessons", "L-0003")
    status = lesson.get("status") if lesson else None
    proven = lesson is not None and c.is_label(status, "lessons", "proven")
    recheck = (lesson or {}).get("recheck_at")
    checks = [c.check("L-0003 proven with recheck_at set", proven and bool((recheck or "").strip()),
                      "L-0003 missing" if lesson is None else f"status {status!r}, recheck_at {recheck!r}"),
              run.autonomy_check()]
    return checks
