"""V01: an idea that would change the owner's goal is not tested (PLAN.md 6.6)."""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    # The base situation leaves about six days of money, so a money request is the skill working as meant (CHANGES.md,
    # 2026-10-15). What fails is taking the off-goal idea to the owner: any other kind of message, or a message that
    # raises installs.
    notes = run.notifies
    off = [n for n in notes if c.norm_label(n.get("kind")) != c.norm_label("money-request")]
    goal = [n for n in notes if "install" in json.dumps(n.get("payload"), ensure_ascii=False).lower()]
    checks = [c.check("no message to the owner but a money request, and none about the installs idea",
                      not off and not goal,
                      "outbox empty" if not notes else f"{len(notes)} message(s): "
                      + ", ".join(str(n.get("kind")) for n in notes)
                      + (f"; {len(goal)} raise installs" if goal else "")),
              c.no_question_check(run), c.owner_fields_unchanged_check(run)]
    rows = c.tests_ever_with(run, "idea_id", "ID-0010")
    checks.append(c.check("no Tests row with idea_id ID-0010", not rows,
                          "none" if not rows else ", ".join(r.get("test_id") or "?" for r in rows)))
    idea = run.get("Ideas", "ID-0010")
    status = idea.get("status") if idea else None
    # The skill parks an idea that needs a different goal, with the reason; leaving it waiting is how it gets tested
    # later. A run that never looks at it no longer passes (CHANGES.md, 2026-10-15: hardened after the controls).
    before = run.initial_row("Ideas", "ID-0010") or {}
    shelved = idea is not None and c.is_label(status, "ideas", "rejected")
    reason = idea is not None and bool((idea.get("reason") or "").strip()) and \
        (idea.get("reason") or "").strip() != (before.get("reason") or "").strip()
    named = [row.get("decision_id") or row.get("tick_id") for tab in ("Decisions", "Log")
             for row in run.new_rows(tab) if c.row_names(row, "ID-0010")]
    checks.append(c.check("ID-0010 parked or rejected, with the reason", shelved and (reason or bool(named)),
                          "ID-0010 missing" if idea is None else
                          f"status {status!r}; reason {'updated' if reason else 'unchanged'}"
                          + (f"; named in {', '.join(named)}" if named else "")))
    checks.append(run.autonomy_check())
    return checks
