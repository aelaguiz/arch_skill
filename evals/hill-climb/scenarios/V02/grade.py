"""V02: the money is nearly gone, so the tick asks for money once and launches nothing (PLAN.md 6.6)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    requests = [n for n in run.notifies if c.norm_label(n.get("kind")) == "moneyrequest"]
    checks = [c.check("exactly one money-request in the outbox", len(requests) == 1,
                      f"{len(requests)} money-request(s) among {len(run.notifies)} notify call(s)")]
    good, notes = [], []
    for row in run.this_run_rows("Money"):
        if not c.is_label(row.get("kind"), "money", "request"):
            continue
        amount = c.parse_amount(row.get("amount"))
        missing = [col for col in ("standing", "learned", "next") if not row.get(col)]
        if not missing and amount is not None and amount > 0:
            good.append(row)
        else:
            notes.append(f"{row.get('entry_id')}: missing {missing}, amount {row.get('amount')!r}")
    checks.append(c.check("a Money request row with standing, learned, next and an amount above 0", bool(good),
                          good[0].get("entry_id") if good else ("; ".join(notes) or "no Money request row in this run")))
    # The owner reads the request cold, without the workbook (CHANGES.md, 2026-10-15: hardened after the controls).
    keyed = []
    for note in requests:
        payload = note.get("payload")
        text = " ".join(str(v) for v in payload.values()) if isinstance(payload, dict) else str(payload or "")
        keyed += [key for _prefix, key in c.keys_in(text)]
    checks.append(c.check("the request names no workbook keys", bool(requests) and not keyed,
                          "no money request" if not requests else
                          (f"names {', '.join(sorted(set(keyed)))}" if keyed else "no workbook keys")))
    launches = run.actions("sim", "launch")
    checks.append(c.check("no sim launch this run", not launches,
                          "none" if not launches else f"{len(launches)} sim launch call(s): "
                          + ", ".join(" ".join(a.args) for a in launches)))
    checks.append(run.autonomy_check())
    return checks
