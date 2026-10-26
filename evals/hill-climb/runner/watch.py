"""Workbook watcher (PLAN.md 6.8, INTERFACES.md).

While a session runs, `Watcher` polls `work/workbook/` every 0.2 s. For each CSV file whose content changed it appends
one line to `RUN/watch.jsonl`:

    {"t": <epoch>, "file": "Tests.csv", "added": [{row}], "changed": [{"key": k, "before": {row}, "after": {row}}],
     "removed": [{row}], "header": [...], "added_keys": [...], "removed_keys": [...], "mtime": <epoch>}

`t` is the wall time at which the poll saw the change (the clock the stream stamps use). The first five fields are the
contract in INTERFACES.md; `header`, `added_keys`, `removed_keys` and `mtime` are extras that let the graders rebuild any
row's values at any moment. Rows are dicts of the file's own header names to cell text.

A row's identity is its key column (Charter `field`, Overview `item`, Map `type`, every other tab its `*_id` column,
else the first column); a repeated key gets `#2`, `#3`; a row with an empty key is identified by its content. The CSV
helpers here are shared with `graders.common`, so the watcher and the graders identify rows the same way.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import threading
import time
from pathlib import Path

POLL_INTERVAL_S = 0.2

TAB_KEYS = {
    "charter": "field",
    "overview": "item",
    "library": "library_id",
    "ideas": "idea_id",
    "map": "type",
    "tests": "test_id",
    "checks": "check_id",
    "results": "result_id",
    "decisions": "decision_id",
    "lessons": "lesson_id",
    "reviews": "review_id",
    "money": "entry_id",
    "log": "tick_id",
    "interview": "interview_id",   # the intake interview (INTAKE_PLAN.md)
}


def normalize_col(name) -> str:
    """Header name as the graders compare it: trimmed, lower case, spaces and hyphens as underscores."""
    text = str(name or "").replace("﻿", "").strip().lower()
    return re.sub(r"[\s\-]+", "_", text)


def tab_name(file_name) -> str:
    """'Tests.csv' -> 'tests' (the lower-case stem)."""
    name = Path(str(file_name)).name
    if name.lower().endswith(".csv"):
        name = name[:-4]
    return name.strip().lower()


def key_column(tab, header) -> str | None:
    """The header name that holds the tab's key, matched tolerantly; the first column when the tab is unknown."""
    header = list(header or [])
    if not header:
        return None
    want = TAB_KEYS.get(tab_name(tab))
    if want:
        for name in header:
            if normalize_col(name) == want:
                return name
    return header[0]


def parse_csv_text(text: str):
    """(header, rows) from CSV text. Blank lines are skipped; cells beyond the header go to `_col<N>` keys; a repeated
    header name gets `#2`."""
    reader = csv.reader(io.StringIO(text))
    try:
        records = list(reader)
    except csv.Error:
        records = [line.split(",") for line in text.splitlines()]
    if not records:
        return [], []
    header = []
    seen = {}
    for name in records[0]:
        clean = name.replace("﻿", "")
        if clean in seen:
            seen[clean] += 1
            clean = f"{clean}#{seen[clean]}"
        else:
            seen[clean] = 1
        header.append(clean)
    rows = []
    for record in records[1:]:
        if not any(cell.strip() for cell in record):
            continue
        row = {}
        for index, name in enumerate(header):
            row[name] = record[index] if index < len(record) else ""
        for index in range(len(header), len(record)):
            row[f"_col{index + 1}"] = record[index]
        rows.append(row)
    return header, rows


def read_csv_file(path):
    """(header, rows) of a CSV file, or ([], []) when it cannot be read."""
    try:
        data = Path(path).read_bytes()
    except OSError:
        return [], []
    return parse_csv_text(data.decode("utf-8-sig", errors="replace"))


def row_identities(rows, key_col):
    """One identity string per row, in order (see the module docstring)."""
    counts = {}
    out = []
    for row in rows:
        key = str(row.get(key_col, "") if key_col else "").strip()
        base = key if key else "\x00" + json.dumps(row, sort_keys=True, ensure_ascii=False)
        counts[base] = counts.get(base, 0) + 1
        out.append(base if counts[base] == 1 else f"{base}#{counts[base]}")
    return out


def diff_rows(before_rows, before_ids, after_rows, after_ids):
    """(added, changed, removed, added_keys, removed_keys) between two snapshots of one file."""
    before = dict(zip(before_ids, before_rows))
    after = dict(zip(after_ids, after_rows))
    added, added_keys, changed = [], [], []
    for ident, row in zip(after_ids, after_rows):
        if ident not in before:
            added.append(row)
            added_keys.append(ident)
        elif before[ident] != row:
            changed.append({"key": ident, "before": before[ident], "after": row})
    removed, removed_keys = [], []
    for ident, row in zip(before_ids, before_rows):
        if ident not in after:
            removed.append(row)
            removed_keys.append(ident)
    return added, changed, removed, added_keys, removed_keys


class _FileState:
    __slots__ = ("sig", "header", "rows", "ids")

    def __init__(self, sig, header, rows, ids):
        self.sig = sig
        self.header = header
        self.rows = rows
        self.ids = ids


def _signature(stat_result):
    return (stat_result.st_mtime_ns, stat_result.st_size, stat_result.st_ino)


class Watcher:
    """Polls a workbook folder and appends one JSON line per changed CSV file.

    `start()` takes the current files as the baseline (nothing is written for them), then polls in a thread until
    `stop()`, which makes one last poll so a write just before the session ended is not missed.
    """

    def __init__(self, workbook_dir, out_path, interval: float = POLL_INTERVAL_S, clock=time.time):
        self.dir = Path(workbook_dir)
        self.out_path = Path(out_path)
        self.interval = interval
        self.clock = clock
        self._state = {}
        self._stop = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self.lines_written = 0

    def _list_files(self):
        try:
            entries = list(os.scandir(self.dir))
        except OSError:
            return {}
        files = {}
        for entry in entries:
            if not entry.name.lower().endswith(".csv"):
                continue
            try:
                if not entry.is_file():
                    continue
                files[entry.name] = entry.path
            except OSError:
                continue
        return files

    def _read_stable(self, path):
        """(sig, header, rows) when the file did not change while it was read, else None."""
        try:
            first = os.stat(path)
            data = Path(path).read_bytes()
            second = os.stat(path)
        except OSError:
            return None
        if _signature(first) != _signature(second):
            return None
        header, rows = parse_csv_text(data.decode("utf-8-sig", errors="replace"))
        return _signature(second), header, rows, second.st_mtime

    def snapshot(self):
        """Take the current files as the baseline without writing anything."""
        with self._lock:
            self._state = {}
            for name, path in self._list_files().items():
                read = self._read_stable(path)
                if read is None:
                    continue
                sig, header, rows, _mtime = read
                ids = row_identities(rows, key_column(name, header))
                self._state[name] = _FileState(sig, header, rows, ids)

    def poll(self) -> int:
        """Record every change since the last poll; returns the number of lines written."""
        written = 0
        with self._lock:
            now_files = self._list_files()
            lines = []
            for name, path in sorted(now_files.items()):
                try:
                    sig = _signature(os.stat(path))
                except OSError:
                    continue
                old = self._state.get(name)
                if old is not None and old.sig == sig:
                    continue
                read = self._read_stable(path)
                if read is None:
                    continue
                sig, header, rows, mtime = read
                ids = row_identities(rows, key_column(name, header))
                if old is None:
                    old_rows, old_ids = [], []
                else:
                    old_rows, old_ids = old.rows, old.ids
                self._state[name] = _FileState(sig, header, rows, ids)
                added, changed, removed, added_keys, removed_keys = diff_rows(old_rows, old_ids, rows, ids)
                if added or changed or removed:
                    lines.append({
                        "t": self.clock(), "file": name, "added": added, "changed": changed, "removed": removed,
                        "header": header, "added_keys": added_keys, "removed_keys": removed_keys, "mtime": mtime,
                    })
            for name in sorted(set(self._state) - set(now_files)):
                old = self._state.pop(name)
                if old.rows:
                    lines.append({
                        "t": self.clock(), "file": name, "added": [], "changed": [], "removed": old.rows,
                        "header": old.header, "added_keys": [], "removed_keys": old.ids, "mtime": None,
                    })
            if lines:
                self.out_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.out_path, "a", encoding="utf-8") as fh:
                    for line in lines:
                        fh.write(json.dumps(line, ensure_ascii=False) + "\n")
                written = len(lines)
                self.lines_written += written
        return written

    def _loop(self):
        while not self._stop.wait(self.interval):
            try:
                self.poll()
            except Exception:  # a watcher error must never kill the session it watches
                continue

    def start(self):
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        self.out_path.touch()
        self.snapshot()
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="workbook-watcher", daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None
        try:
            self.poll()
        except Exception:
            pass


def read_watch_log(path):
    """The watch.jsonl lines as dicts (unreadable lines skipped)."""
    out = []
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return out
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if isinstance(obj, dict):
                out.append(obj)
    return out


def main(argv=None):
    """`python3 runner/watch.py WORKBOOK_DIR OUT.jsonl [SECONDS]`: watch a folder by hand (for debugging)."""
    import sys

    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 2:
        print("usage: watch.py WORKBOOK_DIR OUT.jsonl [SECONDS]", file=sys.stderr)
        return 2
    seconds = float(args[2]) if len(args) > 2 else 60.0
    watcher = Watcher(args[0], args[1]).start()
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass
    watcher.stop()
    print(f"{watcher.lines_written} lines written to {args[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
