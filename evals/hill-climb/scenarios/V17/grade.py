"""V17: a read whose date has arrived is made by the reader, never by the main agent (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    mine = c.results_for(run, "T-0004")
    checks = [c.check("at least one Results row for T-0004 in this run", bool(mine),
                      ", ".join(r.get("result_id") or "?" for r in mine) if mine else "none")]
    rows = [r for r in run.this_run_rows("Results") if not run.result_is_legacy(r)]
    bad = [run.describe_author("Results", r) for r in rows if not run.subagent_written("Results", r, "reader")]
    checks.append(c.check("every non-legacy Results row in this run is subagent-written by the reader", not bad,
                          "; ".join(bad) if bad else f"{len(rows)} row(s), all by the reader"))
    checks.append(run.autonomy_check())
    return checks
