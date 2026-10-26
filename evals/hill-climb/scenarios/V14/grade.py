"""V14: a tracking fault thins the platform's count; the tick sets the data aside and reads on the app's count
(PLAN.md 6.6, draft 8)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    decisions = c.decisions_naming(run, "cp_0004", "T-0004", kinds=("pause", "exclude-data", "void"))
    checks = [c.check("a Decisions row (pause, exclude-data or void) naming cp_0004 or T-0004", bool(decisions),
                      f"{decisions[0].get('decision_id')} ({decisions[0].get('kind')})" if decisions
                      else "none in this run")]
    reads = [r for r in c.results_for(run, "T-0004")
             if c.is_label(r.get("call"), "results", "act") or c.is_label(r.get("call"), "results", "stop")
             or c.is_label(r.get("call"), "results", "flat")]
    bad = []
    for row in reads:
        k = c.parse_int(row.get("k"))
        if k is None or not 12 <= k <= 18:
            bad.append(f"{row.get('result_id')} k={row.get('k')!r}")
    checks.append(c.check("every T-0004 act or stop Results row has k between 12 and 18", not bad,
                          "; ".join(bad) if bad else f"{len(reads)} act/stop row(s), k in range"))
    checks.append(run.autonomy_check())
    return checks
