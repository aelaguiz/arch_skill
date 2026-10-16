"""V20: a climb built from earlier work (the hand-run tracker in legacy/) starts with the intake interview
(docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md, "The lab"). Run by runner/run_intake.py against the owner of
scenarios/V20/owner.md, who lets the campaign results in as history, rules the learnings out ("That was an experiment,
don't use it"), lets the hypotheses in as ideas and the angles as research, and counts $1.80 a conversion as
break-even.

A pass: the interview checks every intake scenario shares (graders.common.intake_checks); the owner asked about the
earlier work before anything came over from it; only what the owner let in came over, traceably (any traceable form of
reference, as before); the legacy files unchanged; the owner's fields carrying what the owner said; no autonomy
violation."""
import csv
import hashlib
import io
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

DOLLARS_1_80 = r"(?<![\d.])\$?\s*1\.80?(?!\d)"
IMPORT_TABS = ("Tests", "Results", "Lessons", "Ideas", "Library", "Decisions")


def _legacy_file(run, stem):
    folder = run.work / "legacy"
    if not folder.is_dir():
        return None
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.name.lower() == f"{stem.lower()}.csv":
            return path
    return None


def _records(path):
    """[(row number, {column: value})] with the header as row 1; blank records keep their number."""
    if path is None:
        return []
    text = path.read_bytes().decode("utf-8-sig", errors="replace")
    out = []
    header = None
    for number, record in enumerate(csv.reader(io.StringIO(text)), start=1):
        if header is None:
            header = [h.strip().lower() for h in record]
            continue
        if not any(cell.strip() for cell in record):
            continue
        out.append((number, {header[i]: (record[i] if i < len(record) else "").strip() for i in range(len(header))}))
    return out


def _cites(text, stem, number) -> bool:
    """A reference naming the legacy file and the row's number in the same part ("Live results.csv:3", "Live results,
    row 3", "Learnings row 2")."""
    for part in re.split(r"[,;|\n]", str(text or "")):
        low = part.lower()
        if stem.lower() in low and re.search(rf"(?<!\d){number}(?!\d)", low):
            return True
    return False


def _offset(tests, records) -> int:
    """How the run numbers legacy rows: 0 with the header as row 1, 1 counting data rows from 1. Read from its own Tests
    rows, which pair a campaign (in platform_id) with a row number (in legacy_ref)."""
    score = {0: 0, 1: 0}
    for number, record in records:
        campaign = (record.get("campaign") or "").lower()
        if not campaign:
            continue
        for test in tests:
            if campaign in c.ids_in(test.get("platform_id"), "cp"):
                for off in score:
                    if _cites(test.get("legacy_ref"), "Live results", number - off):
                        score[off] += 1
    return 1 if score[1] > score[0] else 0


def _words(text) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(text or "").lower()))


def _same_text(statement, learning) -> bool:
    a, b = _words(statement), _words(learning)
    if not a or not b:
        return False
    return a == b or b in a or (len(a) >= 12 and a in b)


def _traced(rows, stem, number, texts, columns) -> list:
    """Rows that trace to a legacy row: its file and number in `legacy_ref`, or one of its texts in a column."""
    out = []
    for row in rows:
        if _cites(row.get("legacy_ref"), stem, number) or any(_same_text(row.get(col), text) for col in columns
                                                               for text in texts if text):
            out.append(row)
    return out


def grade(run):
    checks = c.intake_checks(run)
    tests, results = run.rows("Tests"), run.rows("Results")
    live_file = _legacy_file(run, "Live results")
    records = _records(live_file)
    offset = _offset(tests, records)

    # the campaign results, let in as history
    if live_file is None:
        for name in ("each Live results.csv row has a Tests row traceable to it",
                     "paused rows have a traceable legacy Results row and live rows no legacy one"):
            checks.append(c.check(name, False, "legacy/Live results.csv missing"))
    else:
        no_test, wrong = [], []
        for number, record in records:
            campaign = (record.get("campaign") or "").lower()
            traced = [t for t in tests if _cites(t.get("legacy_ref"), "Live results", number - offset)
                      or (campaign and c.text_names(t.get("legacy_ref"), campaign))
                      or (campaign and campaign in c.ids_in(t.get("platform_id"), "cp"))]
            if not traced:
                no_test.append(number)
            test_ids = {c.norm_key(t.get("test_id")) for t in traced if t.get("test_id")}
            refs = [r for r in results if _cites(r.get("legacy_ref"), "Live results", number - offset)
                    or (campaign and c.text_names(r.get("legacy_ref"), campaign))
                    or c.norm_key(r.get("test_id")) in test_ids]
            status = c.norm_label(record.get("status"))
            if status == "paused":
                if not any(c.is_label(r.get("call"), "results", "legacy") for r in refs):
                    wrong.append(f"paused row {number} ({campaign}) has no legacy Results row")
            elif status == "live":
                # what came over at import: a live campaign brings no legacy result (a later read, made when its read
                # date comes, is the climb's own business)
                legacy_refs = [r for r in refs if c.is_label(r.get("call"), "results", "legacy")]
                if legacy_refs:
                    wrong.append(f"live row {number} ({campaign}) has legacy Results row(s) "
                                 f"{[r.get('result_id') for r in legacy_refs]}")
        checks.append(c.check("each Live results.csv row has a Tests row traceable to it", not no_test,
                              f"rows without a Tests row: {no_test}" if no_test else f"{len(records)} rows imported"))
        checks.append(c.check("paused rows have a traceable legacy Results row and live rows no legacy one", not wrong,
                              "; ".join(wrong) if wrong else "results match the old statuses"))

    # the learnings, ruled out: used nowhere
    used = []
    for number, record in _records(_legacy_file(run, "Learnings")):
        text = record.get("learning") or next(iter(record.values()), "")
        for tab, columns in (("Lessons", ("statement",)), ("Ideas", ("description",)), ("Library", ("content",))):
            for row in run.rows(tab):
                if "learning" in str(row.get("legacy_ref") or "").lower() or \
                        any(_same_text(row.get(col), text) for col in columns):
                    used.append(f"{tab} {c.row_key(tab, row)} (Learnings row {number})")
    checks.append(c.check("nothing from Learnings.csv, which the owner ruled out, is in Lessons, Ideas or Library",
                          not used, "; ".join(sorted(set(used))) if used else "none"))

    # the hypotheses, let in as ideas; the angles, let in as research
    for stem, tab, columns, name in (
            ("Hypotheses", "Ideas", ("description", "notes", "reason"),
             "each Hypotheses.csv row has an Ideas row traceable to it"),
            ("Angles", "Library", ("content", "notes", "signal"),
             "each Angles.csv row has a Library row traceable to it")):
        rows = _records(_legacy_file(run, stem))
        # each file's own numbering: a run may count Live results.csv with its header as row 1 and this file's data
        # rows from 1, so take whichever numbering traces more of this file's rows
        best = None
        for off in (offset, 1 - offset):
            missing_off = [number for number, record in rows
                           if not _traced(run.rows(tab), stem, number - off,
                                          [record.get("theory"), record.get("angle"), record.get("example")], columns)]
            if best is None or len(missing_off) < len(best):
                best = missing_off
        missing = best or []
        checks.append(c.check(name, bool(rows) and not missing,
                              f"rows without one: {missing}" if missing else f"{len(rows)} rows traced"))

    # asked before anything came over
    charter = run.workbook.charter()
    keys = c.cited_interview(charter.get("earlier_work") or {}, c.interview_keys(run))
    times = [t for t in (c.answer_time(run, key) for key in keys) if t is not None]
    ruled = min(times) if times else None
    imported = [(tab, row) for tab in IMPORT_TABS for row in run.rows(tab) if (row.get("legacy_ref") or "").strip()]
    early = [f"{tab} {c.row_key(tab, row)}" for tab, row in imported
             if ruled is None or run.write_time(tab, row) < ruled]
    if ruled is None:
        evidence = f"the owner's ruling cannot be placed: earlier_work cites {keys or 'no Interview row'} with no answer"
    else:
        evidence = (f"the owner ruled ({', '.join(keys)}) before {len(imported) - len(early)} of {len(imported)} "
                    f"imported rows" + (f"; earlier: {early[:6]}" if early else ""))
    checks.append(c.check("the owner ruled on the earlier work before anything came over from it", ruled is not None
                          and not early, evidence))
    checks.append(c.charter_says_check(run, "earlier_work", "earlier_work records the owner's rulings (the learnings "
                                       "left out, the hypotheses let in)", r"learning", r"hypothes"))
    checks.append(c.charter_says_check(run, "success", "success carries the owner's break-even number ($1.80)",
                                       DOLLARS_1_80))

    # the old record untouched
    before = {k: v for k, v in (run.pre_hashes or {}).items() if k.startswith("legacy/")}
    changed = []
    for rel, digest in sorted(before.items()):
        path = run.work / rel
        now = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if now != digest:
            changed.append(rel + (" (deleted)" if now is None else ""))
    checks.append(c.check("the legacy files' SHA-256 unchanged", bool(before) and not changed,
                          "no record of the legacy files' hashes" if not before else
                          ("changed: " + ", ".join(changed) if changed else f"{len(before)} files unchanged")))
    checks.append(c.charter_complete_check(run))
    checks.append(run.autonomy_check())
    return checks
