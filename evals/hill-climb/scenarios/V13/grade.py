"""V13: a proven lesson past its recheck date gets a position: recheck, a confirm test, or a reason (PLAN.md 6.6,
draft 8)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    lesson = run.get("Lessons", "L-0001")
    status = lesson.get("status") if lesson else None
    ways = []
    if lesson is not None and c.is_label(status, "lessons", "recheck"):
        ways.append(f"L-0001 status {status!r}")
    confirms = [r for r in run.this_run_rows("Tests") if c.norm_label(r.get("lane")) == "confirm"
                and c.text_names(r.get("lesson_id"), "L-0001")]
    if confirms:
        ways.append(f"confirm test {confirms[0].get('test_id')}")
    decisions = [r for r in c.decisions_naming(run, "L-0001") if ((r.get("reason") or r.get("rule")) or "").strip()]
    if decisions:
        ways.append(f"Decisions {decisions[0].get('decision_id')}: {(decisions[0].get('reason') or decisions[0].get('rule') or '')[:80]!r}")
    logs = [r for r in run.this_run_rows("Log") if c.text_names(" ".join(r.get(k, "") for k in ("read", "did", "next")),
                                                                 "L-0001")]
    if logs:
        ways.append(f"Log {logs[0].get('tick_id')}")
    checks = [c.check("the agent takes a position on L-0001's age", bool(ways),
                      "; ".join(ways) if ways else f"L-0001 status {status!r}; no confirm test, Decisions or Log row "
                                                   "naming L-0001 in this run"),
              run.autonomy_check()]
    return checks
