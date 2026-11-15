"""The check stamp: the record that decision_deck_check.py passed a spec, and serve's reading of it.

A CLEAN check writes `<spec stem>.checked.json` beside the spec: one SHA-256 over the spec's bytes, every picture it
shows and every video clip (with each clip's own hash, so a mismatch names the changed clip), taken when the check loaded them, and read again before the stamp is written; a change during the check
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
from decision_deck_video import manifest as clip_manifest, snapshot as clip_snapshot  # noqa: E402

CHANGED = "the spec, a picture or a clip changed while the check ran; no stamp was written, so run the check again"


class InputsChanged(RuntimeError):
    """The spec, a picture or a clip changed while the check ran; no stamp is written."""


def digest(spec: dict, clips: dict | None = None) -> str:
    """One SHA-256 over the spec's bytes, each shown picture's content hash and each video clip's (`clips`, the
    decision_deck_video.snapshot serve holds; read now when not given). A deck with no video decision hashes exactly as
    before. Raises OSError when one is unreadable."""
    h = hashlib.sha256(Path(spec["path"]).read_bytes())
    for rel, sha in sorted(image_ids(spec).items()):
        h.update(f"\0image\0{rel}\0{sha}".encode("utf-8"))
    for rel, sha in clip_manifest(clip_snapshot(spec) if clips is None else clips).items():
        h.update(f"\0clip\0{rel}\0{sha}".encode("utf-8"))
    return h.hexdigest()


def stamp_path(spec: dict) -> Path:
    path = Path(spec["path"])
    return path.with_name(path.stem + ".checked.json")


def write_stamp(spec: dict, checked: str) -> Path:
    """Write the stamp for a clean check of the inputs whose digest was `checked` when the check loaded them.
    Raises InputsChanged when they differ now."""
    clips = clip_snapshot(spec)
    if digest(spec, clips) != checked:
        raise InputsChanged(CHANGED)
    out = stamp_path(spec)
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"spec_sha256": checked, "checked_at": checked_at}
    if clips:
        record["clips"] = clip_manifest(clips)      # each clip's hash, so a mismatch names the changed clip
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return out


def stamp_problem(spec: dict, clips: dict | None = None) -> str:
    """"" when the stamp names this spec's bytes (with `clips`, the clips snapshot the server will serve), else why
    not; a changed clip is named."""
    try:
        stamp = json.loads(stamp_path(spec).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        stamp = None
    if not isinstance(stamp, dict):
        return f"no check stamp ({stamp_path(spec).name}): decision_deck_check.py has not printed CLEAN for this spec"
    try:
        clips = clip_snapshot(spec) if clips is None else clips
        sha = digest(spec, clips)
    except OSError as exc:
        return f"a deck file cannot be read ({exc})"
    if stamp.get("spec_sha256") != sha:
        old, new = stamp.get("clips") or {}, clip_manifest(clips)
        changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
        if changed:
            return ("a video decision's clip changed (or appeared or went) since decision_deck_check.py last printed "
                    f"CLEAN: {', '.join(str(spec['root'] / k) for k in changed)}")
        return "the spec or a picture changed since decision_deck_check.py last printed CLEAN"
    return ""


def serve_gate(spec: dict, require_checked: bool, clips: dict | None = None) -> bool:
    """True when serve may start. An unchecked spec gets one stderr line: a warning, or with `require_checked` the
    refusal. `clips` is the clips snapshot the server will serve, so the bytes checked here are the bytes served."""
    why = stamp_problem(spec, clips)
    if not why:
        return True
    if require_checked:
        sys.stderr.write(f"decision_deck serve: refused: {why}. Run decision_deck_check.py --spec {spec['path']} "
                         "until it prints CLEAN.\n")
        return False
    sys.stderr.write(f"decision_deck serve: warning: {why}; serving anyway (--require-checked refuses).\n")
    return True
