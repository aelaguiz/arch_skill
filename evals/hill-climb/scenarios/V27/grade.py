"""V27: a variation of the proven winner is cut from the winner's own materials and recipe, so the item launched for it
differs from the winner only in `presenter`, and its Tests row records how it was made (PLAN.md 13.3)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

WINNER = "it_0002"
WINNER_TESTS = ("T-0002", "T-0004", "T-0005")
IDEA = "ID-0006"
CHANGES = ("presenter",)


def variation_rows(run, rows):
    """Tests rows for the variation: its idea's, or any whose `made_from` names the winner or the winner's tests."""
    return [r for r in rows if c.norm_key(r.get("item_id")) != WINNER
            and (c.text_names(r.get("idea_id"), IDEA) or c.text_names(r.get("made_from"), WINNER, *WINNER_TESTS))]


def grade(run):
    world = run.world
    bad, seen = [], []
    for launch in run.launches():
        if not variation_rows(run, run.tests_recording(launch.target)):
            continue
        diffs, same_text = c.item_differences(world, launch.item, WINNER)
        seen.append(f"{launch.target} ({launch.item})")
        extra = [d for d in diffs if d not in CHANGES]
        if extra or not same_text or not set(CHANGES) <= set(diffs):
            bad.append(f"{launch.item} differs from {WINNER} in {diffs or 'nothing'}"
                       + ("" if same_text else " and its text"))
    checks = [c.check("every item launched this run for the variation differs from it_0002 only in presenter, with "
                      "the same text", not bad,
                      "; ".join(bad) if bad else (f"launched {', '.join(seen)}" if seen else "no launch for the "
                                                                                            "variation"))]
    fixture_items = {c.norm_key(r.get("item_id")) for r in run.initial.rows("Tests") if r.get("item_id")}
    made = [r for r in variation_rows(run, run.rows("Tests"))
            if any(i not in fixture_items for i in c.ids_in(r.get("item_id"), "it"))]
    thin = [r.get("test_id") for r in made if not (r.get("recipe") or "").strip() or not (r.get("made_from") or "").strip()]
    checks.append(c.check("the variation's Tests row has its built item, recipe and made_from", bool(made) and not thin,
                          ("no Tests row for the variation records an item built this run" if not made else
                           f"no recipe or made_from on {thin}" if thin else
                           "; ".join(f"{r.get('test_id')}: {r.get('item_id')} made from {r.get('made_from')}"
                                     for r in made))))
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch this run is a checked launch", ok, evidence))
    checks.append(run.autonomy_check())
    return checks
