"""V10: a rerun that clearly failed leaves its lesson unproven and earns no exploit money (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


CELL = {"hook": "question", "visual": "hand-replay"}


def grade(run):
    lesson = run.get("Lessons", "L-0003")
    status = lesson.get("status") if lesson else None
    checks = [c.check("L-0003 is not proven", lesson is not None and not c.is_label(status, "lessons", "proven"),
                      "L-0003 missing" if lesson is None else f"status {status!r}")]
    exploits = [r for r in run.this_run_rows("Tests") if c.norm_label(r.get("lane")) == "exploit"
                and c.type_covers(r.get("type"), CELL)]
    cell_tests = [r for r in run.rows_ever("Tests") if c.type_covers(r.get("type"), CELL)]
    idents = sorted({r.get("test_id") for r in cell_tests if r.get("test_id")}
                    | {i for r in cell_tests for i in c.ids_in(r.get("platform_id"), "cp")})
    scales = [r for r in c.scale_decisions(run)
              if (idents and c.row_names(r, *idents)) or c.type_covers((r.get("reason") or r.get("rule")) or r.get("data"), CELL)]
    checks.append(c.check("no exploit Tests row or scale decision for hook=question|visual=hand-replay",
                          not exploits and not scales,
                          f"{len(exploits)} exploit row(s), {len(scales)} scale decision(s) on that cell"
                          + (f" (cell tests {idents})" if idents else "")))
    checks.append(run.autonomy_check())
    return checks
