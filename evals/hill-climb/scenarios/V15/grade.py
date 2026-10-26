"""V15: a delivery fault starves the test; the tick addresses it, adds no money, and does not read it (PLAN.md
6.6, draft 8)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


import re

FAULT_WORDS = re.compile(r"deliver|audience|target|reach|fault|share|anomal|0\.12|12\s?%", re.IGNORECASE)


def grade(run):
    rows = c.decisions_naming(run, "cp_0004", "T-0004", not_kinds=("launch", "scale"))
    addressing = [r for r in rows
                  if any(c.is_label(r.get("kind"), "decisions", k) for k in ("pause", "exclude-data", "void"))
                  or FAULT_WORDS.search(c.row_text(r))]
    checks = [c.check("a Decisions row naming cp_0004 or T-0004 that addresses the delivery fault", bool(addressing),
                      f"{addressing[0].get('decision_id')} ({addressing[0].get('kind')})" if addressing
                      else (f"{len(rows)} row(s) name it but none addresses the fault" if rows else "none"))]
    raised, evidence = c.budget_raised(run, "cp_0004")
    checks.append(c.check("cp_0004's daily budget not raised", not raised, evidence))
    reads = [r for r in c.results_for(run, "T-0004")
             if c.is_label(r.get("call"), "results", "act") or c.is_label(r.get("call"), "results", "stop")
             or c.is_label(r.get("call"), "results", "flat")]
    checks.append(c.check("no act or stop Results row for T-0004 in this run", not reads,
                          "none" if not reads else ", ".join(r.get("result_id") or "?" for r in reads)))
    checks.append(run.autonomy_check())
    return checks
