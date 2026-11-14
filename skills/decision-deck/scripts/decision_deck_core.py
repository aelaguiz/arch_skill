"""Decision deck core: shared constants, the file guard, spec lookups, ledger appends, server liveness and the bind guard.

Used by decision_deck.py (CLI), decision_deck_spec.py, decision_deck_ledger.py and decision_deck_server.py; `decision_deck.py
--help` documents the spec and ledger formats.
"""
from __future__ import annotations

import fcntl
import hashlib
import ipaddress
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
NOTE_MAX = 500
SKIP_ID = "skip"                        # reserved option id: "left this page without picking, here is my note"
SKIP_LABEL = "Skipped"
BODY_MAX = 16 * 1024
DEFAULT_GRACE_MIN = 15.0
DEFAULT_MAX_HOURS = 24.0
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".gif": "image/gif", ".svg": "image/svg+xml", ".avif": "image/avif"}


# ------------------------------------------------------------------ paths

def safe_file(root: Path, rel: str, decode: bool = True) -> Path | None:
    """The file at `rel` under `root`, or None when it is absent, a directory, or resolves outside root.

    `rel` is URL-decoded once more here (unless `decode` is false, for a path that is already a file name), so an
    encoded `..` cannot slip past; the containment check runs either way; symlinks are followed before the
    containment check, so a link pointing out of the folder is refused too.
    """
    rel = urllib.parse.unquote(rel or "") if decode else (rel or "")
    if not rel or rel.startswith(("/", "\\")) or "\x00" in rel:
        return None
    try:
        target = (root / rel).resolve()
    except (OSError, RuntimeError):
        return None
    if not target.is_relative_to(root) or not target.is_file():
        return None
    return target


# ------------------------------------------------------------------ spec lookups

def decision_by_id(spec: dict, did: str) -> tuple[int, dict] | tuple[None, None]:
    for n, dec in enumerate(spec["decisions"], 1):
        if dec["id"] == did:
            return n, dec
    return None, None


def option_by_id(dec: dict, oid: str) -> dict | None:
    return next((o for o in dec["options"] if o["id"] == oid), None)


def open_decisions(spec: dict, latest: dict) -> list[str]:
    return [d["id"] for d in spec["decisions"] if d["id"] not in latest]


def next_open(spec: dict, latest: dict, after: int) -> int | None:
    """1-based page number of the first open decision after page `after`, wrapping; None when none is open."""
    n = len(spec["decisions"])
    for k in range(1, n + 1):
        i = (after + k - 1) % n + 1
        if spec["decisions"][i - 1]["id"] not in latest:
            return i
    return None


def image_ids(spec: dict) -> dict[str, str]:
    """Each image path in the spec -> the first 16 hex digits of its SHA-256, the page's `/img/<sha16>` name."""
    out: dict[str, str] = {}
    for dec in spec["decisions"]:
        ev = dec.get("evidence") if isinstance(dec.get("evidence"), dict) else {}
        rels = [img for o in dec["options"] for img in o.get("images", [])]
        rels += [f["image"] for src in (dec, ev) for key in ("shared", "references") for f in src.get(key) or []]
        for rel in rels:
            if rel not in out:
                out[rel] = hashlib.sha256((spec["root"] / rel).read_bytes()).hexdigest()[:16]
    return out


# ------------------------------------------------------------------ ledger appends and times

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def local_time(ts: str | None) -> str:
    """'9:05 AM CET' from a UTC ISO stamp, in this machine's time zone; the raw value when it cannot be parsed."""
    try:
        when = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return str(ts)
    local = when.astimezone()
    return f"{local.strftime('%I:%M %p').lstrip('0')} {local.tzname() or ''}".rstrip()


def append_pick(ledger: Path, record: dict) -> None:
    """Append one JSON line (any record kind) under an exclusive lock, flushed to disk before returning."""
    ledger = Path(ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with ledger.open("a", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


# ------------------------------------------------------------------ server liveness

def state_path(ledger: Path) -> Path:
    """`<ledger stem>.server.json` beside the ledger: the running server's url and pid."""
    ledger = Path(ledger)
    return ledger.with_name(ledger.stem + ".server.json")


def read_server_state(ledger: Path) -> dict:
    """The running server's state file (url, pid, token), or {} when it is absent or unreadable."""
    try:
        data = json.loads(state_path(ledger).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def server_running(ledger: Path) -> bool:
    """True while the ledger's state file exists and names a live pid (`os.kill(pid, 0)`)."""
    try:
        pid = json.loads(state_path(ledger).read_text(encoding="utf-8")).get("pid")
    except (OSError, ValueError, AttributeError):
        return False
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:             # alive, owned by another user
        return True
    return True


# ------------------------------------------------------------------ bind host

LOCAL_NETS = [ipaddress.ip_network(n) for n in (
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",   # RFC 1918 private ranges
    "100.64.0.0/10",                                   # shared address space (carrier-grade NAT, overlay VPNs)
    "fc00::/7")]                                       # IPv6 unique-local
DEFAULT_HOST = "127.0.0.1"


def validate_bind_host(host: str) -> str:
    """Accept loopback ("localhost" reads as 127.0.0.1) or a private-network address; refuse every-interface and
    public addresses, and any other name, with ValueError. Names other than localhost are refused rather than
    resolved, so the address checked is the address bound."""
    text = str(host).strip()
    if text.lower() == "localhost":
        text = DEFAULT_HOST
    try:
        addr = ipaddress.ip_address(text)
    except ValueError as exc:
        raise ValueError(f"bind host {host!r} is not an IP address; pass one, such as 127.0.0.1 or "
                         "192.168.1.20") from exc
    if addr.is_unspecified:
        raise ValueError(f"refusing to bind {host}: that listens on every interface; pass loopback or a "
                         "private-network address")
    if addr.is_loopback or any(addr.version == net.version and addr in net for net in LOCAL_NETS):
        return str(addr)
    raise ValueError(f"refusing to bind {host}: a public address would expose the deck to the internet; pass "
                     "loopback (the default) or a private-network address (10/8, 172.16/12, 192.168/16, "
                     "100.64/10, fc00::/7)")
