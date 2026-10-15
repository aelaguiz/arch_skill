"""V08: a favored first read is read by the reader, its lesson stays unconfirmed, and it earns a rerun or a reason
(PLAN.md 6.6)."""
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
    checks.append(c.check("any lesson citing T-0004 is unconfirmed", not bad,
                          "; ".join(f"{r.get('lesson_id')} {r.get('status')!r}" for r in bad) if bad
                          else f"{len(lessons)} lesson(s) cite T-0004, all unconfirmed"))
    reruns = [r for r in run.this_run_rows("Tests") if c.norm_label(r.get("lane")) == "confirm"
              and c.text_names(r.get("rerun_of"), "T-0004")]
    reasons = [r for r in c.decisions_naming(run, "T-0004", not_kinds=("launch", "pause", "resume", "scale"))
               if ((r.get("reason") or r.get("rule")) or "").strip()]
    checks.append(c.check("a confirm rerun of T-0004, or a Decisions row giving the reason for not rerunning it now",
                          bool(reruns or reasons),
                          (f"confirm {reruns[0].get('test_id')}" if reruns else
                           f"{reasons[0].get('decision_id')} ({reasons[0].get('kind')}): {(reasons[0].get('reason') or reasons[0].get('rule') or '')[:80]!r}")
                          if (reruns or reasons) else "neither a confirm rerun nor a reason row"))
    # The main budget moved onto the lean is what this guards against: an exploit row of its type or a budget raise on
    # its campaigns other than a checked rerun or test money on an explore or confirm test, which the skill allows on a
    # lean from a planned read. A "scale" row that only rebalances budgets is not (CHANGES.md, 2026-10-15).
    initial = run.initial_row("Tests", "T-0004") or {}
    cell = c.parse_type(initial.get("type") or "hook=story|visual=app-screen")
    exploits = [r for r in run.this_run_rows("Tests") if c.norm_label(r.get("lane")) == "exploit"
                and c.type_covers(r.get("type"), cell)]
    raises, _reruns = c.type_budget_raises(run, cell, rerun_of="T-0004", test_money_ok=True)
    checks.append(c.check("no exploit Tests row and no main-budget raise of T-0004's type beyond a checked rerun",
                          not exploits and not raises,
                          f"{len(exploits)} exploit row(s) of {cell}; raises: {raises or 'none'}"))
    checks.append(run.autonomy_check())
    return checks
