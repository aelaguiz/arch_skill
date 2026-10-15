"""V30: after a read and a launch in one tick (V08's situation), the Tests rows the tick touched each show their checks'
verdicts, T-0004's row shows its read's call, and the Overview written this tick names the money left and the best
known option (PLAN.md 13.3)."""
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

TEST = "T-0004"


def _shows_call(text, call) -> bool:
    for label in ("act", "stop", "hold"):
        if c.is_label(call, "results", label):
            words = c.SYNONYMS.get(("results", label), (label,))
            return any(re.search(rf"\b{re.escape(w)}\b", text, re.I) for w in words)
    return bool(str(call or "").strip()) and str(call).strip().lower() in text.lower()


def _money_left(world):
    balance = getattr(world, "balance", None)
    return balance() if callable(balance) else None


def grade(run):
    missing = []
    touched = run.this_run_rows("Tests")
    for row in touched:
        text = c.row_text(row)
        for check_row in c.checks_of_test(run, row):
            if not c.shows_check(text, check_row):
                missing.append(f"{row.get('test_id')} does not show {check_row.get('check_id')} "
                               f"({check_row.get('role')} {check_row.get('verdict')})")
    checks = [c.check("the Tests rows touched this run show their checks' verdicts", not missing,
                      "; ".join(missing) if missing else f"{len(touched)} touched row(s), each showing its checks")]
    reads = [r for r in c.results_for(run, TEST) if not run.result_is_legacy(r)]
    row = run.get("Tests", TEST) or {}
    if not reads:
        checks.append(c.check("T-0004 was read this run and its Tests row shows the call", False,
                              "no Results row for T-0004 in this run"))
    else:
        call = reads[-1].get("call")
        shown = _shows_call(c.row_text(row), call)
        checks.append(c.check("T-0004 was read this run and its Tests row shows the call", shown,
                              f"{reads[-1].get('result_id')} call {call!r}; the Tests row "
                              + ("shows it" if shown else "does not")))
    written = run.this_run_rows("Overview")
    text = "\n".join(c.row_text(r) for r in run.rows("Overview"))
    checks.append(c.check("an Overview tab written this run", bool(written),
                          f"{len(written)} Overview row(s) written or changed this run" if written else
                          ("the Overview tab is missing" if run.tab("Overview") is None else
                           "no Overview row changed this run")))
    left = _money_left(run.world)
    named = c.names_a_number(text, [left], rel=0.0, floor=1.0) if left is not None and written else None
    checks.append(c.check("the Overview names the money left", named is not None,
                          f"names {named:g} (the platform's balance is {left:.2f})" if named is not None else
                          f"no amount within $1 of the balance {left!r}" + ("" if written else " in an Overview written "
                                                                                                 "this run")))
    best = [r for r in run.initial.rows("Tests") if c.norm_label(r.get("lane")) == "exploit"
            and c.norm_label(r.get("status")) == "live"]
    idents = [x for r in best for x in [r.get("test_id")] + c.ids_in(r.get("platform_id"), "cp")
              + c.ids_in(r.get("item_id"), "it") if x]
    worded = any(all(any(re.search(rf"\b{re.escape(w)}\b", text, re.I) for w in c.value_words([v]))
                     for v in (c.parse_type(r.get("type")) or {}).values()) for r in best)
    named_best = bool(written) and (c.text_names(text, *idents) or worded)
    checks.append(c.check("the Overview names the best known option", named_best,
                          f"names {', '.join(idents)}" if named_best else f"no mention of {', '.join(idents)} or its "
                                                                          f"cell"))
    checks.append(run.autonomy_check())
    return checks
