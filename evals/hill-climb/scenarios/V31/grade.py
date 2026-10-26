"""V31: thirteen grounded ideas wait, each readable cheaply, and the money left cannot read them all. The climb does
not wait for money or a read date: it launches checked items this tick, keeps the best known option running, and asks
for more money because money is what limits learning. How many items it launches and at what size is its call; the
evidence line reports both (VELOCITY_PLAN.md; an earlier rule asked for at least five, a number the skill never set)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

def grade(run):
    launches = run.launches()
    sizes = []
    for launch in launches:
        rows = [r for r in run.rows("Tests") if c.text_names(r.get("item_id"), launch.item)]
        sizes.append(f"{launch.item} ${(rows[-1].get('daily_budget') if rows else '?')}/day x {(rows[-1].get('days') if rows else '?')}d")
    checks = [c.check("checked items launched this tick rather than waiting for money or a read date", bool(launches),
                      f"{len(launches)} launch(es): {'; '.join(sizes) or 'none'}")]
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch this run is a checked launch", ok, evidence))
    requests = [n for n in run.notifies if c.norm_label(n.get("kind")) == "moneyrequest"]
    rows = [r for r in run.this_run_rows("Money") if c.is_label(r.get("kind"), "money", "request")
            and all(r.get(col) for col in ("standing", "learned", "next"))
            and (c.parse_amount(r.get("amount")) or 0) > 0]
    checks.append(c.check("a money request this run: a money-request message and a Money request row with standing, "
                          "learned, next and an amount", bool(requests) and bool(rows),
                          f"{len(requests)} money-request message(s), {len(rows)} complete Money request row(s)"))
    checks.append(c.not_all_in_check(run, "cp_0001"))
    checks.append(run.autonomy_check())
    return checks
