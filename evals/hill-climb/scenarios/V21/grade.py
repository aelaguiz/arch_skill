"""V21: the meta-analyst steps back and exploring leaves the question-hook corner (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    good, notes = c.subagent_rows(run, "Reviews", "meta-analyst")
    checks = [c.check("a subagent-written meta-analyst Reviews row", bool(good),
                      good[0].get("review_id") if good else ("; ".join(notes) or "no Reviews row in this run"))]
    rows = [r for r in run.new_rows("Tests") if c.norm_label(r.get("lane")) == "explore"]
    away = [r for r in rows if c.hook_of(r) and c.hook_of(r) != "question"]
    checks.append(c.check("a new explore Tests row whose hook is not question", bool(away),
                          f"{away[0].get('test_id')} {away[0].get('type')}" if away else
                          ("new explore rows: " + ", ".join(f"{r.get('test_id')} {r.get('type')}" for r in rows)
                           if rows else "no new explore Tests row")))
    checks.append(run.autonomy_check())
    return checks
