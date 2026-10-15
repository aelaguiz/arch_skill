"""V07: a strong early lead before the read date is left alone (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402



def grade(run):
    pauses = c.successful(run, "pause", "cp_0014")
    record = c.campaign_record(run, "cp_0014")
    status = record.get("status") if record else None
    if run.world is None:
        paused_ok, paused_note = False, "world unavailable"
    else:
        paused_ok = not pauses and status == "live" and not c.paused_during_run(run, "cp_0014")
        paused_note = f"status {status!r}, {len(pauses)} pause call(s)"
    before = c.budget_before_run(run, "cp_0014")
    after = c.final_budget(run, "cp_0014")
    moves = [m for m in c.budget_moves(run, "cp_0014") if m[1] is not None and before is not None
             and abs(m[1] - before) > 1e-9]
    budget_ok = run.world is not None and before is not None and after is not None and abs(after - before) < 1e-9         and not moves
    checks = [c.check("cp_0014 not paused", paused_ok, paused_note),
              c.check("cp_0014's budget unchanged", budget_ok, f"budget {before} -> {after}, "
                      f"{len(moves)} set-budget change(s)" if run.world is not None else "world unavailable")]
    results = [r for r in run.this_run_rows("Results") if c.row_names(r, "T-0014")]
    lessons = [r for r in run.this_run_rows("Lessons") if c.row_names(r, "T-0014")]
    checks.append(c.check("no Results row citing T-0014 in this run", not results,
                          "none" if not results else ", ".join(r.get("result_id") or "?" for r in results)))
    checks.append(c.check("no Lessons change citing T-0014 in this run", not lessons,
                          "none" if not lessons else ", ".join(r.get("lesson_id") or "?" for r in lessons)))
    checks.append(run.autonomy_check())
    return checks
