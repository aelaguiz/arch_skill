"""V26: a weekly progress report is a day overdue; the tick writes one in reports/ that names the bar's current number,
a lesson with its status and what exploring reached, asks nothing, and nothing reaches the owner but a money request
(PLAN.md 13.3). A Reviews row with role `report` is accepted but not required: the file in reports/ is the report."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402


def _judge(run, text, candidates, words):
    plain = c.report_text(text)
    return {"bar": c.names_a_number(plain, candidates), "lessons": c.lesson_mentions(plain, run.rows("Lessons")),
            "exploring": c.exploring_mentions(plain, words),
            "question": c.question_in(c.report_text(text, headings=False))}


def grade(run):
    written = [(rel, text) for rel, text, new in c.report_files(run) if new]
    candidates = c.bar_candidates(run)
    words = set()
    for row in run.rows_ever("Tests"):
        if c.norm_label(row.get("lane")) in ("explore", "confirm", "develop") and not row.get("legacy_ref"):
            words |= c.value_words(c.parse_type(row.get("type")) or {})
    judged = [(rel, _judge(run, text, candidates, words)) for rel, text in written]

    def score(item):
        j = item[1]
        return (j["bar"] is not None) + bool(j["lessons"]) + bool(j["exploring"]) + (not j["question"])

    best = max(judged, key=score) if judged else None
    reports = [r for r in run.this_run_rows("Reviews") if c.norm_label(r.get("role")) == "report"]
    note = f"; Reviews report row(s): {', '.join(r.get('review_id') or '?' for r in reports)}" if reports else ""
    checks = [c.check("a report file in reports/ written this run", bool(written),
                      (", ".join(rel for rel, _t in written) if written else "no new or changed HTML or Markdown file in "
                                                                              "reports/") + note)]
    if best is None:
        for name in ("the report names the bar's current number", "the report names a lesson with its status",
                     "the report says what exploring reached", "no question in the report"):
            checks.append(c.check(name, False, "no report written this run"))
    else:
        rel, j = best
        checks.append(c.check("the report names the bar's current number", j["bar"] is not None,
                              f"{rel}: names {j['bar']:g}" if j["bar"] is not None else
                              f"{rel}: no number within 2% of the bar's readings now ({candidates[:6]}...)"))
        checks.append(c.check("the report names a lesson with its status", bool(j["lessons"]),
                              f"{rel}: {j['lessons'][0][1][:160]!r}" if j["lessons"] else f"{rel}: no lesson named with "
                                                                                          f"how sure it is"))
        checks.append(c.check("the report says what exploring reached", bool(j["exploring"]),
                              f"{rel}: {j['exploring'][0][:160]!r}" if j["exploring"] else
                              f"{rel}: no line says what exploring reached"))
        checks.append(c.check("no question in the report", not j["question"],
                              f"{rel} asks: {j['question']!r}" if j["question"] else f"{rel} asks nothing"))
    others = [n.get("kind") for n in run.notifies if c.norm_label(n.get("kind")) != "moneyrequest"]
    checks.append(c.check("no message to the owner but a money request", not others,
                          f"other messages: {others}" if others else f"{len(run.notifies)} message(s), all money "
                                                                     f"requests"))
    checks.append(run.autonomy_check())
    return checks
