"""V08: a favored first read is read by the reader, its lesson is a lean rather than strong, and the lean steers what
comes next without moving everything onto it (VELOCITY_PLAN.md)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402



def grade(run):
    rows = [r for r in c.results_for(run, "T-0004") if c.is_label(r.get("call"), "results", "act")]
    good = [r for r in rows if run.subagent_written("Results", r, "reader")]
    checks = [c.check("a subagent-written reader Results row for T-0004 with call act", bool(good),
                      run.describe_author("Results", good[0]) if good else
                      ("; ".join(run.describe_author("Results", r) for r in rows) or
                       "no act Results row for T-0004 in this run"))]
    lessons = [r for r in run.rows("Lessons") if c.row_names(r, "T-0004")]
    bad = [r for r in lessons if not c.is_label(r.get("status"), "lessons", "unconfirmed")]
    checks.append(c.check("any lesson citing T-0004 is a lean, not strong", not bad,
                          "; ".join(f"{r.get('lesson_id')} {r.get('status')!r}" for r in bad) if bad
                          else f"{len(lessons)} lesson(s) cite T-0004, all leans"))
    # A lean steers now: money toward it, a test or idea built on it, or a decision about it (VELOCITY_PLAN.md).
    acted = c.built_on(run, "T-0004", "cp_0004", "it_0004")
    reasons = [r for r in c.decisions_naming(run, "T-0004", not_kinds=("pause",))
               if ((r.get("reason") or r.get("rule")) or "").strip()]
    checks.append(c.check("the lean steers something this run, or a Decisions row says why not",
                          bool(acted or reasons),
                          "; ".join(acted) if acted else
                          (f"{reasons[0].get('decision_id')} ({reasons[0].get('kind')})" if reasons
                           else "nothing built on the lean and no reason row")))
    # Money may follow the lean in steps; moving everything onto it may not.
    checks.append(c.not_all_in_check(run, "cp_0001"))
    checks.append(run.autonomy_check())
    return checks
