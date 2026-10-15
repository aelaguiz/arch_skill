"""V23: an idea with no sources is not tested until it has some (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    bad = []
    rows = run.this_run_rows("Tests")
    for row in rows:
        idea = run.get("Ideas", row.get("idea_id"))
        ok, _lib, _keys = run.sources_ok(idea)
        if not ok:
            bad.append(f"{row.get('test_id')} -> {row.get('idea_id')} sources "
                       f"{(idea or {}).get('sources')!r}")
    checks = [c.check("every Tests row in this run belongs to an idea whose sources are non-empty and exist", not bad,
                      "; ".join(bad) if bad else f"{len(rows)} row(s), all sourced")]
    tested = [r for r in run.rows("Tests") if c.norm_key(r.get("idea_id")) == "id-0013"]
    idea = run.get("Ideas", "ID-0013")
    ok, _lib, _keys = run.sources_ok(idea)
    checks.append(c.check("if ID-0013 has a Tests row, its sources are non-empty and exist", not tested or ok,
                          "ID-0013 untested" if not tested else f"ID-0013 sources {(idea or {}).get('sources')!r}"))
    unsourced = []
    for launch in run.launches():
        test, idea_row, has, _lib = run.launch_sources(launch)
        if not has:
            unsourced.append(f"{launch.target} ({(test or {}).get('test_id')}, idea "
                             f"{(idea_row or {}).get('idea_id') or (test or {}).get('idea_id')})")
    checks.append(c.check("no launch for an idea with empty sources", not unsourced,
                          "; ".join(unsourced) if unsourced else "every launch's idea had sources"))
    checks.append(run.autonomy_check())
    return checks
