"""Decision deck spec: validation of every key (options, keys, evidence kinds), loading, and the evidence view.

The spec format is documented once, in decision_deck.py's --help (decision_deck_help.py).
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import ID_RE, MIME, SKIP_ID  # noqa: E402

EVIDENCE_KINDS = ("images", "diff", "chart", "table")
KEY_RE = re.compile(r"^[a-z]$")
RESERVED_KEYS = set("jkcvfbzd")         # next/previous, comment, the picture keys and Done
DEFAULT_REFERENCES_TITLE = "Reference, layout only (not an option)"


class SpecError(ValueError):
    """The spec file is unreadable or breaks the schema; the message lists every problem."""


def _text(obj: dict, key: str, where: str, errors: list, required: bool = True) -> str:
    val = obj.get(key)
    if val is None and not required:
        return ""
    if not isinstance(val, str) or (required and not val.strip()):
        errors.append(f"{where}: '{key}' must be a non-empty string")
        return ""
    return val


def _str_list(obj: dict, key: str, where: str, errors: list) -> list:
    val = obj.get(key, [])
    if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
        errors.append(f"{where}: '{key}' must be a list of strings")
        return []
    return val


def _image(img: str, where: str, root: Path, errors: list) -> None:
    """Append a problem when `img` is not an existing image file inside `root`, named by a relative path."""
    if Path(img).is_absolute() or img.startswith(("/", "\\", "~")):
        errors.append(f"{where}: image '{img}' must be a path relative to the spec's folder")
        return
    if Path(img).suffix.lower() not in MIME:
        errors.append(f"{where}: image '{img}' must end in one of {', '.join(sorted(MIME))}")
    resolved = (root / img).resolve()
    if not resolved.is_relative_to(root):
        errors.append(f"{where}: image '{img}' resolves outside the spec's folder")
    elif not resolved.is_file():
        errors.append(f"{where}: image '{img}' not found under {root}")


def _figures(obj: dict, key: str, where: str, root: Path, errors: list) -> None:
    """Check an optional figure list ("shared" or "references"): [{"image", "caption"?}]."""
    if key not in obj:
        return
    figs = obj[key]
    if not isinstance(figs, list):
        errors.append(f"{where}: '{key}' must be a list of {{\"image\", \"caption\"}}")
        return
    for k, fig in enumerate(figs, 1):
        fw = f"{where} {key} {k}"
        if not isinstance(fig, dict):
            errors.append(f"{fw}: must be an object with 'image' and an optional 'caption'")
            continue
        img = _text(fig, "image", fw, errors)
        _text(fig, "caption", fw, errors, required=False)
        if img:
            _image(img, fw, root, errors)


def _number(val) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(val)


def _chart(ev: dict, ew: str, errors: list) -> None:
    """The chart's keys are checked in decision_deck_chart_spec.py, beside the chart's own drawing."""
    from decision_deck_chart_spec import check_chart      # noqa: PLC0415  (kept beside the chart's own drawing)
    check_chart(ev, ew, errors)


def _table(ev: dict, ew: str, errors: list) -> None:
    cols = ev.get("columns")
    if not isinstance(cols, list) or not cols or not all(isinstance(c, str) for c in cols):
        errors.append(f"{ew}: 'columns' must be a non-empty list of strings")
        return
    rows = ev.get("rows")
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        errors.append(f"{ew}: 'rows' must be a list of rows, each a list of cells")
        return
    for k, row in enumerate(rows, 1):
        if len(row) != len(cols):
            errors.append(f"{ew}: row {k} has {len(row)} cells; there are {len(cols)} columns")
        if not all(isinstance(c, str) or _number(c) for c in row):
            errors.append(f"{ew} row {k}: cells must be text or numbers")


def _evidence(dec: dict, where: str, root: Path, errors: list) -> None:
    """Check the optional `evidence` object: one kind per decision, and images only on a picture decision."""
    pictures = any(isinstance(o, dict) and o.get("images") for o in dec.get("options") or [])
    pictures = pictures or bool(dec.get("shared") or dec.get("references"))
    if "evidence" not in dec:
        return
    ev = dec["evidence"]
    if not isinstance(ev, dict):
        errors.append(f"{where}: 'evidence' must be an object with a 'kind'")
        return
    kind = ev.get("kind")
    if kind not in EVIDENCE_KINDS:
        errors.append(f"{where}: evidence 'kind' must be one of {', '.join(EVIDENCE_KINDS)}")
        return
    ew = f"{where} evidence"
    if kind != "images":
        if pictures:
            errors.append(f"{where}: only a picture decision (evidence kind images) carries images, "
                          "'shared' or 'references'")
        if kind == "diff":
            for key in ("before", "after"):
                if not isinstance(ev.get(key), str):
                    errors.append(f"{ew}: '{key}' must be a string")
            if not (str(ev.get("before") or "").strip() or str(ev.get("after") or "").strip()):
                errors.append(f"{ew}: 'before' and 'after' are both empty")
            _text(ev, "rule_now", ew, errors, required=False)
        elif kind == "chart":
            _chart(ev, ew, errors)
        else:
            _table(ev, ew, errors)
        return
    for key in ("shared", "references", "references_title"):
        if key in ev and key in dec:
            errors.append(f"{where}: give '{key}' in one place, the decision or its evidence")
    for key in ("shared", "references"):
        _figures(ev, key, ew, root, errors)
    if "references_title" in ev:
        _text(ev, "references_title", ew, errors)
    if "views" in ev and (not isinstance(ev["views"], list) or not all(isinstance(v, str) for v in ev["views"])):
        errors.append(f"{ew}: 'views' must be a list of strings, one tab label per picture")
    if "density" in ev and ev["density"] not in (1, 2, 3):
        errors.append(f"{ew}: 'density' must be 1, 2 or 3 (image pixels per screen pixel)")


def _option(opt, where: str, root: Path, errors: list, opt_ids: set, keys: set) -> None:
    oid = opt.get("id")
    if not isinstance(oid, str) or not ID_RE.match(oid):
        errors.append(f"{where}: option id must match {ID_RE.pattern}")
    elif oid == SKIP_ID:
        errors.append(f"{where}: option id '{SKIP_ID}' is reserved for a skip with a note")
    elif oid in opt_ids:
        errors.append(f"{where}: duplicate option id '{oid}'")
    else:
        opt_ids.add(oid)
        where = where.rsplit(" ", 1)[0] + f" {oid}"
    _text(opt, "label", where, errors)
    _text(opt, "caption", where, errors, required=False)
    _str_list(opt, "pros", where, errors)
    _str_list(opt, "cons", where, errors)
    for img in _str_list(opt, "images", where, errors):
        _image(img, where, root, errors)
    if "key" in opt:
        key = opt["key"]
        if not isinstance(key, str) or not KEY_RE.match(key) or key in RESERVED_KEYS:
            errors.append(f"{where}: key {key!r} must be one lowercase letter other than "
                          f"{', '.join(sorted(RESERVED_KEYS))} (digits answer by position already)")
        elif key in keys:
            errors.append(f"{where}: duplicate key '{key}'")
        else:
            keys.add(key)
    if "ask_note" in opt and not isinstance(opt["ask_note"], bool):
        errors.append(f"{where}: 'ask_note' must be true or false")


def validate_spec(data, root: Path) -> list[str]:
    """Every schema problem in `data`, as readable strings; empty means valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["spec: the top level must be a JSON object"]
    _text(data, "title", "spec", errors)
    decisions = data.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        return errors + ["spec: 'decisions' must be a non-empty list"]
    seen: set[str] = set()
    for i, dec in enumerate(decisions, 1):
        where = f"decision {i}"
        if not isinstance(dec, dict):
            errors.append(f"{where}: must be an object")
            continue
        did = dec.get("id")
        if not isinstance(did, str) or not ID_RE.match(did):
            errors.append(f"{where}: decision id must match {ID_RE.pattern}")
        elif did in seen:
            errors.append(f"{where}: duplicate decision id '{did}'")
        else:
            seen.add(did)
            where = f"decision {did}"
        _text(dec, "title", where, errors)
        _text(dec, "question", where, errors)
        _text(dec, "context", where, errors, required=False)
        if "allow_note" in dec and not isinstance(dec["allow_note"], bool):
            errors.append(f"{where}: 'allow_note' must be true or false")
        options = dec.get("options")
        if not isinstance(options, list) or not options:
            errors.append(f"{where}: 'options' must be a non-empty list")
            options = []
        opt_ids: set[str] = set()
        keys: set[str] = set()
        for j, opt in enumerate(options, 1):
            if not isinstance(opt, dict):
                errors.append(f"{where} option {j}: must be an object")
                continue
            _option(opt, f"{where} option {j}", root, errors, opt_ids, keys)
        for key in ("shared", "references"):
            _figures(dec, key, where, root, errors)
        if "references_title" in dec:
            _text(dec, "references_title", where, errors)
        _evidence(dec, where, root, errors)
        rec = dec.get("recommendation")
        if not isinstance(rec, dict):
            errors.append(f"{where}: 'recommendation' must be an object with 'option' (an option id or null) "
                          "and 'why'")
            continue
        if "option" not in rec:
            errors.append(f"{where}: recommendation needs 'option' (an option id, or null for no recommendation)")
        ropt = rec.get("option")
        if ropt is not None and not isinstance(ropt, str):
            errors.append(f"{where}: recommendation 'option' must be an option id string or null")
        elif ropt is not None and ropt not in opt_ids:
            errors.append(f"{where}: recommendation names option '{ropt}', which is not an option here")
        _text(rec, "why", f"{where} recommendation", errors)
    decided = data.get("decided", [])
    if not isinstance(decided, list):
        errors.append("spec: 'decided' must be a list of {\"title\", \"answer\"}")
    else:
        for i, item in enumerate(decided, 1):
            if not isinstance(item, dict):
                errors.append(f"decided {i}: must be an object with 'title' and 'answer'")
                continue
            _text(item, "title", f"decided {i}", errors)
            _text(item, "answer", f"decided {i}", errors)
    return errors


def load_spec(path) -> dict:
    """Read and validate a spec; returns it with `root` (the resolved spec folder) added. Raises SpecError."""
    path = Path(path).expanduser()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SpecError(f"spec {path}: {exc}") from exc
    root = path.resolve().parent
    errors = validate_spec(data, root)
    if errors:
        raise SpecError("spec is invalid:\n  " + "\n  ".join(errors))
    data["root"] = root
    data["path"] = path.resolve()
    return data


# ------------------------------------------------------------------ views of a valid decision

def takes_note(dec: dict) -> bool:
    """True unless the decision sets "allow_note": false; the deck gives every other slide a comment box."""
    return dec.get("allow_note", True) is not False


def option_keys(dec: dict) -> list[dict]:
    """[{"id", "key", "alt"}] per option: digits 1 to 9 by position always answer; "key" adds a letter."""
    out = []
    for i, opt in enumerate(dec["options"]):
        alt = str(i + 1) if i < 9 else ""
        out.append({"id": opt["id"], "key": opt.get("key") or alt, "alt": alt})
    return out


def _fig(fig: dict) -> dict:
    return {"image": fig["image"], "caption": fig.get("caption") or ""}


def evidence_of(dec: dict) -> dict:
    """The decision's evidence, normalized: diff, chart and table as given; pictures as columns; else kind none.

    Picture columns, left to right: "Ours" (the shared images), each option with images of its own (tagged with its
    id, captioned with its caption or label), then the references under their title. View k shows each column's
    k-th picture (its last one when it has fewer).
    """
    ev = dec.get("evidence") or {}
    if ev.get("kind") in ("diff", "chart", "table"):
        return dict(ev)
    shared = ev.get("shared", dec.get("shared")) or []
    refs = ev.get("references", dec.get("references")) or []
    title = ev.get("references_title") or dec.get("references_title") or DEFAULT_REFERENCES_TITLE
    cols = []
    if shared:
        cols.append({"tag": "Ours", "caption": "", "option": None, "figs": [_fig(f) for f in shared]})
    for opt in dec["options"]:
        if opt.get("images"):
            cols.append({"tag": opt["id"], "caption": opt.get("caption") or opt["label"], "option": opt["id"],
                         "figs": [{"image": rel, "caption": ""} for rel in opt["images"]]})
    if refs:
        cols.append({"tag": title, "caption": "", "option": None, "figs": [_fig(f) for f in refs]})
    if not cols:
        return {"kind": "none"}
    return {"kind": "images", "columns": cols, "views": list(ev.get("views") or []), "density": ev.get("density", 1)}
