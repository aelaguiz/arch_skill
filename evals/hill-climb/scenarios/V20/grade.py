"""V20: adoption imports an old tracker into a new workbook and leaves the old files untouched (PLAN.md 6.6, draft 8:
any traceable form of reference)."""
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402
import csv
import hashlib
import io
import re


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


def grade(run):
    checks = []
    tests, results, lessons = run.rows("Tests"), run.rows("Results"), run.rows("Lessons")
    live_file = _legacy_file(run, "Live results")
    if live_file is None:
        for name in ("each Live results.csv row has a Tests row traceable to it",
                     "paused rows have a traceable legacy Results row and live rows none"):
            checks.append(c.check(name, False, "legacy/Live results.csv missing"))
    else:
        records = _records(live_file)
        offset = _offset(tests, records)
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
            elif status == "live" and refs:
                wrong.append(f"live row {number} ({campaign}) has Results row(s) {[r.get('result_id') for r in refs]}")
        checks.append(c.check("each Live results.csv row has a Tests row traceable to it", not no_test,
                              f"rows without a Tests row: {no_test}" if no_test else f"{len(records)} rows imported"))
        checks.append(c.check("paused rows have a traceable legacy Results row and live rows none", not wrong,
                              "; ".join(wrong) if wrong else "results match the old statuses"))
    offset = _offset(tests, _records(live_file)) if live_file is not None else 0
    learn_file = _legacy_file(run, "Learnings")
    if learn_file is None:
        checks.append(c.check("each Learnings.csv row has a Lessons row traceable to it that is not proven", False,
                              "legacy/Learnings.csv missing"))
    else:
        bad = []
        for number, record in _records(learn_file):
            text = record.get("learning") or next(iter(record.values()), "")
            rows = [r for r in lessons if _cites(r.get("legacy_ref"), "Learnings", number - offset)
                    or _same_text(r.get("statement"), text)]
            # Not believed is what matters: unconfirmed, or retired once its own cited data failed to show it
            # (CHANGES.md, 2026-10-15). Proven, with no rerun in the old tracker, fails.
            if not any(c.is_label(r.get("status"), "lessons", "unconfirmed")
                       or c.is_label(r.get("status"), "lessons", "retired")
                       or c.is_label(r.get("status"), "lessons", "recheck") for r in rows):
                bad.append(f"row {number}: " + (", ".join(f"{r.get('lesson_id')} {r.get('status')!r}" for r in rows)
                                                 or "no Lessons row traceable to it"))
        checks.append(c.check("each Learnings.csv row has a Lessons row traceable to it that is not proven", not bad,
                              "; ".join(bad) if bad else "all learnings imported without being believed"))
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
    charter = run.workbook.charter()
    unfilled = [f for f in c.CHARTER_FIELDS if not (charter.get(f) or {}).get("value")]
    checks.append(c.check(f"all {len(c.CHARTER_FIELDS)} Charter fields filled", not unfilled,
                          f"unfilled: {unfilled}" if unfilled else f"all {len(c.CHARTER_FIELDS)} filled"))
    checks.append(c.no_question_check(run))
    checks.append(run.autonomy_check())
    return checks
