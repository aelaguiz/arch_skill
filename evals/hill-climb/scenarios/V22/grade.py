"""V22 (grades V19's runs): setup researches before it launches and every idea draws on the research (PLAN.md
6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    launches = run.launches()
    first = min((run.launch_bound(l)[0] or float("inf") for l in launches), default=float("inf"))
    library = run.rows("Library")
    early = [r for r in library if run.write_time("Library", r) < first]
    named = [r for r in early if "sim library" in (r.get("link") or "").lower()]
    checks = [c.check("Library rows written before the first launch, one whose link names sim library",
                      bool(early) and bool(named),
                      f"{len(early)} of {len(library)} Library rows before the first launch; "
                      f"{len(named)} name sim library")]
    charter = run.workbook.charter()
    empty = [f for f in ("competitors", "outside_sources") if not (charter.get(f) or {}).get("value")]
    checks.append(c.check("competitors and outside_sources filled", not empty,
                          f"empty: {empty}" if empty else "both filled"))
    bad = []
    ideas = run.rows("Ideas")
    for row in ideas:
        ok, _lib, keys = run.sources_ok(row)
        if not ok:
            bad.append(f"{row.get('idea_id')} sources {row.get('sources')!r}")
    checks.append(c.check("every Ideas row has non-empty sources whose keys exist", bool(ideas) and not bad,
                          "; ".join(bad) if bad else (f"{len(ideas)} ideas sourced" if ideas else "no Ideas rows")))
    cited = []
    for row in run.rows("Tests"):
        if c.norm_label(row.get("lane")) != "explore":
            continue
        idea = run.get("Ideas", row.get("idea_id"))
        _ok, library_cited, _keys = run.sources_ok(idea)
        if library_cited:
            cited.append(row.get("test_id"))
    checks.append(c.check("an explore Tests row's idea cites a Library row", bool(cited),
                          ", ".join(cited) if cited else "none"))
    checks.append(run.autonomy_check())
    return checks
