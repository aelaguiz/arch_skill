"""The check stamp: the record that decision_deck_check.py passed a spec, and serve's reading of it.

A CLEAN check writes `<spec stem>.checked.json` beside the spec: one SHA-256 over the spec's bytes and every picture
it shows, taken when the check loaded them, and read again before the stamp is written; a change during the check
writes no stamp (InputsChanged). `serve` reads the stamp: with no matching stamp it prints one warning line on stderr
and serves anyway, unless --require-checked, which makes it refuse.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import image_ids  # noqa: E402

CHANGED = "the spec or a picture changed while the check ran; no stamp was written, so run the check again"


class InputsChanged(RuntimeError):
    """The spec or a picture changed while the check ran; no stamp is written."""


def digest(spec: dict) -> str:
    """One SHA-256 over the spec's bytes and each shown picture's content hash. Raises OSError when one is unreadable."""
    h = hashlib.sha256(Path(spec["path"]).read_bytes())
    for rel, sha in sorted(image_ids(spec).items()):
        h.update(f"\0image\0{rel}\0{sha}".encode("utf-8"))
    return h.hexdigest()


def stamp_path(spec: dict) -> Path:
    path = Path(spec["path"])
    return path.with_name(path.stem + ".checked.json")


def write_stamp(spec: dict, checked: str) -> Path:
    """Write the stamp for a clean check of the inputs whose digest was `checked` when the check loaded them.
    Raises InputsChanged when they differ now."""
    if digest(spec) != checked:
        raise InputsChanged(CHANGED)
    out = stamp_path(spec)
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out.write_text(json.dumps({"spec_sha256": checked, "checked_at": checked_at}, indent=2) + "\n", encoding="utf-8")
    return out


def stamp_problem(spec: dict) -> str:
    """"" when the stamp names this spec's bytes, else why not."""
    try:
        stamp = json.loads(stamp_path(spec).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        stamp = None
    if not isinstance(stamp, dict):
        return f"no check stamp ({stamp_path(spec).name}): decision_deck_check.py has not printed CLEAN for this spec"
    try:
        sha = digest(spec)
    except OSError as exc:
        return f"a deck file cannot be read ({exc})"
    if stamp.get("spec_sha256") != sha:
        return "the spec or a picture changed since decision_deck_check.py last printed CLEAN"
    return ""


def serve_gate(spec: dict, require_checked: bool) -> bool:
    """True when serve may start. An unchecked spec gets one stderr line: a warning, or with `require_checked` the
    refusal."""
    why = stamp_problem(spec)
    if not why:
        return True
    if require_checked:
        sys.stderr.write(f"decision_deck serve: refused: {why}. Run decision_deck_check.py --spec {spec['path']} "
                         "until it prints CLEAN.\n")
        return False
    sys.stderr.write(f"decision_deck serve: warning: {why}; serving anyway (--require-checked refuses).\n")
    return True
