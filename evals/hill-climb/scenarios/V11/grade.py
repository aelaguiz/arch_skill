"""V11: exploit has crowded out exploring; after the tick budgets match the record and explore is back over its
floor (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    checks = []
    if run.world is None:
        checks.append(c.check("each live campaign's platform budget equals its Tests row's daily_budget", False,
                              "world unavailable"))
    else:
        bad, seen = [], []
        for cid, record in sorted((getattr(run.world, "campaigns", {}) or {}).items()):
            if not isinstance(record, dict) or record.get("status") != "live":
                continue
            platform = c.final_budget(run, cid)
            rows = run.tests_recording(cid)
            if not rows:
                bad.append(f"{cid} (${platform}) is on no Tests row")
                continue
            # the campaign's current plan: a revised plan is a new row and the old one is withdrawn or closed
            active = [r for r in rows if not (c.is_label(r.get("status"), "tests", "withdrawn")
                                              or c.is_label(r.get("status"), "tests", "closed"))]
            row = (active or rows)[-1]
            recorded = c.parse_amount(row.get("daily_budget"))
            seen.append(f"{cid} ${platform} = {row.get('test_id')} ${recorded}")
            if platform is None or recorded is None or abs(platform - recorded) > 0.005:
                bad.append(f"{cid} platform ${platform} vs {row.get('test_id')} daily_budget "
                           f"{row.get('daily_budget')!r}")
        checks.append(c.check("each live campaign's platform budget equals its Tests row's daily_budget", not bad,
                              "; ".join(bad) if bad else ("; ".join(seen) or "no live campaigns")))
    share, total, explore, unreadable = run.committed(run.rows("Tests"))
    # a lab yardstick for "exploring restored" against the 5% the tick finds, not the skill's number
    ok = share is not None and share >= 0.25 - 1e-9 and not unreadable
    checks.append(c.check("explore's share of committed daily spend is at least a quarter", ok,
                          (f"explore ${explore:g} of ${total:g} = {share * 100:.1f}%" if share is not None
                           else "nothing committed") + (f"; unreadable budgets {unreadable}" if unreadable else "")))
    found, notes = [], []
    for row in run.new_rows("Tests"):
        if c.norm_label(row.get("lane")) != "explore":
            continue
        passes = [r for r in c.checks_rows(run, "plan-checker", "pass", test_key=row.get("test_id"))
                  if run.subagent_written("Checks", r, "plan-checker")]
        if passes:
            found.append(f"{row.get('test_id')} ({passes[0].get('check_id')})")
        else:
            notes.append(f"{row.get('test_id')} has no subagent-written plan-checker pass")
    # Exploring can come back through a new checked plan or by giving a live, checked explore test more money; raising
    # the live T-0020 from $5 is the second (CHANGES.md, 2026-10-15).
    raised = []
    for row in run.rows("Tests"):
        if c.norm_label(row.get("lane")) != "explore" or not run.is_fixture_row("Tests", row.get("test_id")):
            continue
        for cid in c.ids_in(row.get("platform_id"), "cp"):
            moved, evidence = c.budget_raised(run, cid)
            if moved:
                raised.append(f"{row.get('test_id')}: {evidence}")
    checks.append(c.check("exploring grows through checked spend: a new explore Tests row with a subagent-written "
                          "plan-checker pass, or a live explore test's budget raised", bool(found) or bool(raised),
                          ", ".join(found + raised) if (found or raised)
                          else ("; ".join(notes) or "no new explore Tests row and no live explore test raised")))
    checks.append(run.autonomy_check())
    return checks
