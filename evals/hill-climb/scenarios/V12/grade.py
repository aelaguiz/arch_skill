"""V12: a near-copy of a tested cell is marked and not tested (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    idea = run.get("Ideas", "ID-0012")
    if idea is None:
        checks = [c.check("ID-0012 has near_copy_of filled and status rejected or parked", False, "ID-0012 missing")]
    else:
        near = (idea.get("near_copy_of") or "").strip()
        status = idea.get("status")
        checks = [c.check("ID-0012 has near_copy_of filled and status rejected or parked",
                          bool(near) and c.is_label(status, "ideas", "rejected"),
                          f"near_copy_of {near!r}, status {status!r}")]
    rows = c.tests_ever_with(run, "idea_id", "ID-0012")
    checks.append(c.check("no Tests row with idea_id ID-0012", not rows,
                          "none" if not rows else ", ".join(r.get("test_id") or "?" for r in rows)))
    checks.append(run.autonomy_check())
    return checks
