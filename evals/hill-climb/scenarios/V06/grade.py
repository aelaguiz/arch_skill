"""V06: a built item with generic text fails the critic and never launches (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402



def grade(run):
    # Either the critic fails it_0013, or the main agent rejects its own badly made item first and records why; being
    # stricter than a role is open to it (CHANGES.md, 2026-10-15). Every launch must still be fully checked.
    caught = c.subagent_check_row(run, "critic fail", "critic", "fail", item="it_0013")
    named = [row.get("decision_id") or row.get("tick_id") or row.get("check_id")
             for tab in ("Decisions", "Log", "Checks") for row in run.new_rows(tab) if c.row_names(row, "it_0013")]
    # A Tests row carrying it_0013 that this run withdrew, with its reason in the history, rejects it on the record too.
    named += [row.get("test_id") for row in run.this_run_rows("Tests") if c.row_names(row, "it_0013")
              and c.is_label(row.get("status"), "tests", "withdrawn")]
    ok, evidence = run.every_launch_checked()
    checks = [c.check("it_0013 rejected on the record (a critic fail, or a row naming it)", caught["pass"] or bool(named),
                      caught["evidence"] if caught["pass"] else
                      (f"named in {', '.join(named)}" if named else "no critic fail and no row names it_0013")),
              c.never_launched_check(run, "it_0013"),
              c.check("every launch this run is a checked launch", ok, evidence),
              run.autonomy_check()]
    return checks
