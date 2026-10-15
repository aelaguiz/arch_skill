"""V24: the Library has gone stale and few ideas wait, so the scout researches and brings sourced ideas (PLAN.md
6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    library_rows = run.this_run_rows("Library")
    good, notes = c.subagent_rows(run, "Library", "scout", rows=library_rows)
    checks = [c.check("subagent-written Library rows by the scout", bool(good),
                      ", ".join(r.get("library_id") for r in good) if good else
                      ("; ".join(notes) or "no Library row in this run"))]
    fresh = {c.norm_key(r.get("library_id")) for r in run.new_rows("Library")}
    ideas, why = [], []
    for row in run.this_run_rows("Ideas"):
        if not run.subagent_written("Ideas", row, "scout"):
            why.append(run.describe_author("Ideas", row))
            continue
        cites = [key for prefix, key in c.keys_in(row.get("sources")) if prefix == "LB" and c.norm_key(key) in fresh]
        if cites:
            ideas.append(f"{row.get('idea_id')} cites {cites}")
        else:
            why.append(f"{row.get('idea_id')} cites no Library row written in this run ({row.get('sources')!r})")
    checks.append(c.check("subagent-written Ideas rows by the scout citing a Library row written in this run",
                          bool(ideas), "; ".join(ideas) if ideas else ("; ".join(why) or "no Ideas row in this run")))
    checks.append(run.autonomy_check())
    return checks
