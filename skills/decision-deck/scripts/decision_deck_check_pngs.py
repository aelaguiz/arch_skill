"""Which of the checker's PNGs changed since its last run into the same --out folder, so an image review of a fixed
deck views only the slides a fix touched.

decision_deck_check.py --out DIR keeps MANIFEST in DIR (each PNG's file name to the SHA-256 of its bytes), rewritten on
every run, and from the second run on prints one PNGS line before its final line: the PNGs whose bytes changed or are
new, those that existed last run and were not made this time (the deck lost a slide), and a count of the unchanged.
Equal bytes mean an unchanged slide because PNG capture of the same deck is byte-identical between runs. A manifest that cannot be read or has the wrong shape counts as no manifest: the run says so on
stderr and prints no PNGS line, never a claim that something is unchanged.
"""
from __future__ import annotations

import hashlib
import json
import os
import string
import sys
from pathlib import Path

MANIFEST = "png-manifest.json"      # in the --out folder, beside the PNGs
SHA_LEN = 64                        # hex digits in a SHA-256


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _valid(data) -> bool:
    return isinstance(data, dict) and all(
        isinstance(k, str) and isinstance(v, str) and len(v) == SHA_LEN and set(v) <= set(string.hexdigits)
        for k, v in data.items())


def load(folder: Path) -> dict | None:
    """The last run's {name: sha256}; None on a first run, or (said on stderr) when the manifest is unusable."""
    path = folder / MANIFEST
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not _valid(data):
            raise ValueError("not a map of PNG file name to SHA-256")
    except (OSError, ValueError) as exc:     # UnicodeDecodeError and JSONDecodeError are ValueErrors
        sys.stderr.write(f"decision_deck_check: could not read {path} ({exc}); treating this as the first run here\n")
        return None
    return data


def save(folder: Path, shas: dict) -> None:
    """Write the manifest whole (temp file, then rename). If that fails, drop the old one, so the next run cannot
    compare against a run older than this one, and say so on stderr; if the old one cannot be dropped either, say
    that it must be removed by hand."""
    path, tmp = folder / MANIFEST, folder / (MANIFEST + ".tmp")
    try:
        tmp.write_text(json.dumps(shas, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:
        kept = False
        for stale in (tmp, path):
            try:
                stale.unlink(missing_ok=True)
            except OSError:
                kept = kept or stale == path
        after = ("it still holds an older run, so remove it by hand before the next run here" if kept
                 else "the next run here counts as a first run")
        sys.stderr.write(f"decision_deck_check: could not write {path} ({exc.strerror or exc}); {after}\n")


def line(old: dict, new: dict, order: list[str]) -> str:
    """`PNGS <n> changed since the last run here: <names>[; <m> removed: <names>] (<k> unchanged)`; names in
    render order, removed ones sorted."""
    changed = [n for n in order if n in new and old.get(n) != new[n]]
    removed = sorted(n for n in old if n not in new)
    unchanged = sum(1 for n in new if old.get(n) == new[n])
    text = f"PNGS {len(changed)} changed since the last run here"
    text += f": {' '.join(changed)}" if changed else ""
    text += f"; {len(removed)} removed: {' '.join(removed)}" if removed else ""
    return f"{text} ({unchanged} unchanged)"


def report(folder: Path, names: list[str]) -> str | None:
    """Hash this run's PNGs (`names`, in render order), compare with the last run's manifest and rewrite it. The
    PNGS line, or None on a first run (or after an unusable manifest)."""
    new = {n: digest(folder / n) for n in names if (folder / n).is_file()}
    old = load(folder)
    save(folder, new)
    return None if old is None else line(old, new, names)
