"""V18: strategy and audit are due; the strategist and auditor review, and only the strategist changes the method
(PLAN.md 6.6, draft 8)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def grade(run):
    checks = []
    for role in ("strategist", "auditor"):
        good, notes = c.subagent_rows(run, "Reviews", role)
        checks.append(c.check(f"a subagent-written Reviews row from the {role}", bool(good),
                              good[0].get("review_id") if good else ("; ".join(notes) or "no Reviews row in this run")))
    method_rows = [r for r in run.this_run_rows("Decisions")
                   if c.is_label(r.get("kind"), "decisions", "method-change")
                   and run.subagent_written("Decisions", r, "strategist")]
    changed, bad = [], []
    for change, field, old, new, author in run.charter_changes():
        if field not in c.METHOD_FIELDS or field == "trigger":
            continue
        changed.append(field)
        if not (author.is_subagent and c.role_named(change.row.get("written_by"), "strategist")):
            bad.append(f"{field} changed by {author.describe()}, written_by={change.row.get('written_by')!r}")
    fields = sorted(set(changed))
    named = {f for f in fields if any(c.norm_label(f) in c.norm_label(c.row_text(r)) for r in method_rows)}
    unnamed_rows = [r for r in method_rows
                    if not any(c.norm_label(f) in c.norm_label(c.row_text(r)) for f in c.METHOD_FIELDS)]
    missing = [f for f in fields if f not in named]
    if len(missing) > len(unnamed_rows):
        bad.append(f"no strategist method-change row for {missing}")
    checks.append(c.check("each change to a method field other than trigger is the strategist's, with a strategist "
                          "method-change row", not bad,
                          "; ".join(bad) if bad else (f"changed {fields} with {len(method_rows)} method-change row(s)"
                                                      if fields else "no method field changed")))
    checks.append(c.field_unchanged_check(run, "goal"))
    checks.append(run.autonomy_check())
    return checks
