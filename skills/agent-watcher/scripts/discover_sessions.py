#!/usr/bin/env python3
"""List active human-root coding-agent sessions across Codex, Claude Code, and Prime.

Read-only. Prints a compact roster; writes the full record set to
~/.agent-watcher/discovery.json (or --json PATH). The master uses this every
tick to decide which sessions moved and which are idle after an assistant turn.

Default window: sessions whose transcript changed in the last 6h.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sqlite3
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep installed skill dirs free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watcher_lib as W  # noqa: E402

TAIL_BYTES = 200_000
HEAD_LINES = 120


def codex_sessions(home: Path, since, include_children: bool, errors: list[str]) -> list[dict]:
    db = home / "state_5.sqlite"
    if not db.exists():
        return []
    rows: list[dict] = []
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cols = {r[1] for r in conn.execute("PRAGMA table_info(threads)")}
        children: set[str] = set()
        try:
            ecols = [r[1] for r in conn.execute("PRAGMA table_info(thread_spawn_edges)")]
            ccol = next((c for c in ecols if "child" in c), None)
            if ccol:
                children = {r[0] for r in conn.execute(f"SELECT {ccol} FROM thread_spawn_edges")}
        except sqlite3.Error:
            pass
        since_ms = int(since.timestamp() * 1000)
        recency = "recency_at_ms" if "recency_at_ms" in cols else "updated_at_ms"
        q = f"SELECT * FROM threads WHERE COALESCE({recency}, updated_at*1000) >= ? AND archived = 0"
        for r in conn.execute(q, (since_ms,)):
            r = dict(r)
            sid = r["id"]
            first = (r.get("first_user_message") or "").strip()
            is_child = sid in children or first in ("", sid)
            if is_child and not include_children:
                continue
            path = Path(r["rollout_path"]) if r.get("rollout_path") else None
            if path and not path.is_absolute():
                path = home / path
            if not path or not path.exists():
                continue
            rows.append(build_record("codex", sid, path, cwd=r.get("cwd"), first_ask=first or r.get("title") or "",
                                     title=r.get("title") or r.get("name") or "", model=r.get("model"),
                                     approval=r.get("approval_mode"), is_child=is_child, label="codex"))
        conn.close()
    except sqlite3.Error as exc:
        errors.append(f"codex sqlite: {exc}")
    return rows


def claude_homes(extra: list[str]) -> list[tuple[str, Path]]:
    homes: list[tuple[str, Path]] = [("default", Path.home() / ".claude")]
    for p in sorted(glob.glob(str(Path.home() / ".aimgr" / "claude-homes" / "*" / ".claude"))):
        homes.append((Path(p).parent.name, Path(p)))
    for e in extra:
        homes.append((Path(e).parent.name or "extra", Path(e)))
    return [(label, h) for label, h in homes if (h / "projects").is_dir()]


def claude_sessions(homes, since, include_workers: bool, errors: list[str]) -> list[dict]:
    rows: list[dict] = []
    since_epoch = since.timestamp()
    for label, home in homes:
        for path in (home / "projects").glob("*/*.jsonl"):
            try:
                st = path.stat()
            except OSError:
                continue
            if st.st_mtime < since_epoch or st.st_size == 0:
                continue
            sid = path.stem
            cwd = None
            first_ask = ""
            mode = None
            try:
                with open(path, "r", errors="replace") as fh:
                    for i, line in enumerate(fh):
                        if i > HEAD_LINES and first_ask:
                            break
                        obj = W.load_json(line)
                        if not obj:
                            continue
                        if obj.get("type") == "permission-mode":
                            mode = obj.get("permissionMode")
                        if cwd is None and obj.get("cwd"):
                            cwd = obj.get("cwd")
                        if not first_ask and obj.get("type") == "user":
                            for ev in W.classify_claude(obj):
                                if ev["kind"] == "USER":
                                    first_ask = ev["text"]
                                    break
                        if i > 2000:
                            break
            except OSError as exc:
                errors.append(f"claude read {path}: {exc}")
                continue
            is_worker = first_ask.lstrip().startswith("You are an externally delegated worker") or "no parent chat context" in first_ask[:400]
            if is_worker and not include_workers:
                continue
            rows.append(build_record("claude", sid, path, cwd=cwd, first_ask=first_ask, title="", model=None,
                                     approval=mode or "unrecorded", is_child=is_worker, label=label))
    return rows


def prime_sessions(home: Path, since, errors: list[str]) -> list[dict]:
    rows: list[dict] = []
    sess = home / "sessions"
    if not sess.is_dir():
        return rows
    since_epoch = since.timestamp()
    for path in sess.glob("*.jsonl"):
        try:
            st = path.stat()
        except OSError:
            continue
        if st.st_mtime < since_epoch or st.st_size == 0:
            continue
        cwd = None
        sid = path.stem
        first_ask = ""
        model = None
        try:
            with open(path, "r", errors="replace") as fh:
                for i, line in enumerate(fh):
                    obj = W.load_json(line)
                    if not obj:
                        continue
                    if obj.get("type") == "session":
                        cwd = obj.get("cwd")
                        sid = obj.get("id") or sid
                    elif obj.get("type") == "model_change":
                        model = obj.get("modelId")
                    elif obj.get("type") == "message" and (obj.get("message") or {}).get("role") == "user":
                        first_ask = W.content_text((obj.get("message") or {}).get("content"))
                        break
                    if i > 400:
                        break
        except OSError as exc:
            errors.append(f"prime read {path}: {exc}")
            continue
        rows.append(build_record("prime", sid, path, cwd=cwd, first_ask=first_ask, title="", model=model,
                                 approval=None, is_child=False, label="prime"))
    return rows


def list_children(home: Path, parent_id: str, active_within=None) -> int:
    db = home / "state_5.sqlite"
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True); conn.row_factory = sqlite3.Row
    ecols = [r[1] for r in conn.execute("PRAGMA table_info(thread_spawn_edges)")]
    pcol = next((c for c in ecols if "parent" in c), None); ccol = next((c for c in ecols if "child" in c), None)
    if not (pcol and ccol):
        print("ERROR discover: thread_spawn_edges has no parent/child columns"); return 2
    kids = [r[0] for r in conn.execute(f"SELECT {ccol} FROM thread_spawn_edges WHERE {pcol} = ?", (parent_id,))]
    rows = []
    for k in kids:
        r = conn.execute("SELECT id, rollout_path, first_user_message, created_at FROM threads WHERE id = ?", (k,)).fetchone()
        if not r: continue
        path = Path(r["rollout_path"]); path = path if path.is_absolute() else home / path
        if not path.exists(): continue
        mtime = W.parse_ts(path.stat().st_mtime)
        if active_within is not None and mtime and (W.now() - mtime) > active_within:
            continue
        rows.append((mtime, str(path), W.squash(r["first_user_message"] or "", 110), path.stat().st_size))
    rows.sort(key=lambda x: x[0] or W.now(), reverse=True)
    total = conn.execute(f"SELECT COUNT(*) FROM thread_spawn_edges WHERE {pcol} = ?", (parent_id,)).fetchone()[0]
    print(f"OK discover children of codex-{parent_id}: {len(rows)} active" + (f" within {active_within}" if active_within else "") + f" of {total} total; newest first")
    for ts, pth, first, sz in rows:
        print(f"last {W.age_str(ts)} ago | {sz//1024}KB | {pth} | {first}")
    return 0


def find_session(codex_home: Path, prime_home: Path, ident: str) -> int:
    """Resolve a session id (or key, or unique prefix) to its transcript path across the known stores."""
    ident = ident.split("-", 1)[-1] if ident.split("-", 1)[0] in ("codex", "claude", "prime") and "-" in ident else ident
    hits: list[tuple[str, str, str, str]] = []
    db = codex_home / "state_5.sqlite"
    if db.exists():
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        for sid, rp, first in conn.execute("SELECT id, rollout_path, first_user_message FROM threads WHERE id LIKE ?", (ident + "%",)):
            p = Path(rp); p = p if p.is_absolute() else codex_home / p
            if p.exists():
                parent = conn.execute("SELECT parent_thread_id FROM thread_spawn_edges WHERE child_thread_id = ?", (sid,)).fetchone()
                hits.append(("codex", str(p), f"child of {parent[0]}" if parent else "root", W.squash(first or "", 100)))
    for base in [Path.home() / ".claude"] + [Path(p) for p in glob.glob(str(Path.home() / ".aimgr" / "claude-homes" / "*" / ".claude"))]:
        for p in glob.glob(str(base / "projects" / "*" / f"{ident}*.jsonl")):
            hits.append(("claude", p, "root", ""))
    for p in glob.glob(str(prime_home / "sessions" / f"{ident}*.jsonl")):
        hits.append(("prime", p, "root", ""))
    if not hits:
        print(f"NONE discover find {ident}: no transcript in the Codex, Claude, or Prime stores"); return 1
    print(f"OK discover find {ident}: {len(hits)} match(es)")
    for rt, p, rel, first in hits:
        print(f"{rt} | {rel} | {p} | {first}")
    return 0


def build_record(runtime, sid, path: Path, *, cwd, first_ask, title, model, approval, is_child, label) -> dict:
    st = path.stat()
    mtime = W.parse_ts(st.st_mtime)
    last = W.last_meaningful(runtime, W.tail_lines(path, TAIL_BYTES))
    last_kind = last["kind"] if last else "?"
    last_ts = W.parse_ts(last["ts"]) if last and last.get("ts") else None
    return {
        "key": W.session_key(runtime, sid),
        "runtime": runtime,
        "session_id": sid,
        "label": label,
        "path": str(path),
        "cwd": cwd,
        "title": W.squash(title or "", 120),
        "first_ask": W.squash(first_ask or "", 600),
        "model": model,
        "approval": approval,
        "is_child": bool(is_child),
        "size_bytes": st.st_size,
        "mtime": W.iso(mtime),
        "last_kind": last_kind,
        "last_event_ts": W.iso(last_ts),
        "last_text": W.squash(last.get("text", ""), 240) if last else "",
        "last_name": last.get("name", "") if last else "",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", default="6h", help="activity window, e.g. 90m, 6h, 2d (default 6h)")
    ap.add_argument("--limit", type=int, default=40, help="rows to print (default 40)")
    ap.add_argument("--runtime", choices=W.RUNTIMES, action="append", help="restrict to runtime(s)")
    ap.add_argument("--include-children", action="store_true", help="include spawned Codex children and delegated Claude workers")
    ap.add_argument("--json", default=None, help="write full records here (default ~/.agent-watcher/discovery.json)")
    ap.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    ap.add_argument("--prime-home", default=str(Path.home() / ".prime" / "agent"))
    ap.add_argument("--claude-home", action="append", default=[], help="extra Claude home(s) beyond ~/.claude and ~/.aimgr/claude-homes/*")
    ap.add_argument("--children-of", default=None, help="Codex session key or id: list its spawned child rollouts (path, last activity, size) and exit")
    ap.add_argument("--active-within", default="90m", help="with --children-of: only children whose rollout changed within this window (default 90m; use 0 for all)")
    ap.add_argument("--find", default=None, help="session id, key, or unique id prefix: print its runtime, lineage, and transcript path, then exit")
    args = ap.parse_args(argv)

    if args.find:
        return find_session(Path(args.codex_home), Path(args.prime_home), args.find)

    if args.children_of:
        win = None if args.active_within in ("0", "all") else W.parse_duration(args.active_within)
        return list_children(Path(args.codex_home), args.children_of.split("-", 1)[-1] if args.children_of.startswith("codex-") else args.children_of, win)

    since = W.now() - W.parse_duration(args.since)
    runtimes = set(args.runtime or W.RUNTIMES)
    errors: list[str] = []
    rows: list[dict] = []
    if "codex" in runtimes:
        rows += codex_sessions(Path(args.codex_home), since, args.include_children, errors)
    if "claude" in runtimes:
        rows += claude_sessions(claude_homes(args.claude_home), since, args.include_children, errors)
    if "prime" in runtimes:
        rows += prime_sessions(Path(args.prime_home), since, errors)

    rows.sort(key=lambda r: r["mtime"], reverse=True)
    out = Path(args.json) if args.json else W.STATE_ROOT / "discovery.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"generated": W.iso(W.now()), "since": args.since, "sessions": rows, "errors": errors}, indent=1))

    counts = {rt: sum(1 for r in rows if r["runtime"] == rt) for rt in W.RUNTIMES}
    print(f"OK discover: {len(rows)} active sessions (codex {counts['codex']}, claude {counts['claude']}, prime {counts['prime']}); "
          f"since {args.since}; full: {W.short_path(out)}" + (f"; errors {len(errors)}" if errors else ""))
    print("key | age | last | cwd | ask")
    for r in rows[: args.limit]:
        age = W.age_str(W.parse_ts(r["mtime"]))
        cwd = W.short_path(r["cwd"] or "?")
        lab = f"[{r['label']}] " if r["runtime"] == "claude" else ""
        print(f"{r['key']} | {age} | {r['last_kind']} | {cwd} | {lab}{W.squash(r['first_ask'], 90)}")
    if len(rows) > args.limit:
        print(f"… {len(rows) - args.limit} more in {W.short_path(out)}")
    for e in errors[:3]:
        print(f"warn: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
