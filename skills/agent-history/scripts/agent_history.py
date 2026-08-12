#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Read-only helpers for local Codex, Claude Code, Pi, and Prime Agent history.

The script prints bounded summaries for agents and writes complete result
artifacts to a run directory. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_LIMIT = 20
DEFAULT_PREVIEW_CHARS = 240
DEFAULT_TEXT_CHARS = 10000
# Keeps one broad query from writing a multi-hundred-MB results artifact. The
# newest results are kept; the summary says when the cap bit.
DEFAULT_MAX_RESULTS = 2000

# Pi and Prime Agent write the same `version: 3` session-event schema. Only the
# on-disk layout differs: Prime keeps flat `sessions/<uuid>.jsonl`, Pi keeps
# `sessions/--<encoded-cwd>--/<iso>_<uuid>.jsonl`. Extension debug and state
# files live beside Pi transcripts, so session files are matched by name and
# then confirmed by a `type: session` first line.
SESSION_UUID_NAME = re.compile(r"^[0-9a-fA-F-]{36}\.jsonl$")
PI_SESSION_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}T[0-9:.\-]+Z_[0-9a-fA-F-]{36}\.jsonl$")

# Token/cost accounting for child agents. High volume, never evidence.
SESSION_SKIP_TYPES = {"child_usage_attributed"}


class HistoryError(RuntimeError):
    pass


@dataclass
class TimeWindow:
    since: dt.datetime
    until: dt.datetime


@dataclass
class RunContext:
    command: str
    runtime: str | None
    cwd: Path
    scope: str
    window: TimeWindow | None
    output_root: Path
    codex_home: Path
    claude_home: Path
    pi_home: Path
    prime_home: Path
    limit: int
    page: int
    max_preview_chars: int
    fmt: str
    include_sidechains: bool
    max_results: int = DEFAULT_MAX_RESULTS
    run_dir: Path | None = None
    truncated: bool = False


@dataclass
class SessionCandidate:
    """One Pi/Prime transcript that survived the cwd and time-window prefilter."""

    path: Path
    header: dict[str, Any]
    source: str
    label: str = ""
    parent_session_id: str = ""


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def local_now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_time_value(raw: str | None, *, default: dt.datetime | None = None) -> dt.datetime:
    if raw is None or raw == "":
        if default is None:
            raise HistoryError("missing time value")
        return default

    value = raw.strip()
    now = local_now()
    lowered = value.lower()
    if lowered == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    rel = re.fullmatch(r"(\d+)([smhdw])", lowered)
    if rel:
        amount = int(rel.group(1))
        unit = rel.group(2)
        if unit == "s":
            delta = dt.timedelta(seconds=amount)
        elif unit == "m":
            delta = dt.timedelta(minutes=amount)
        elif unit == "h":
            delta = dt.timedelta(hours=amount)
        elif unit == "d":
            delta = dt.timedelta(days=amount)
        else:
            delta = dt.timedelta(weeks=amount)
        return now - delta

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        parsed_date = dt.date.fromisoformat(value)
        return dt.datetime.combine(parsed_date, dt.time.min).astimezone()

    iso = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = dt.datetime.fromisoformat(iso)
    except ValueError as exc:
        raise HistoryError(f"could not parse time value {raw!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed.astimezone()


def parse_timestamp(raw: Any) -> dt.datetime | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        value = float(raw)
        if value > 10_000_000_000:
            value = value / 1000.0
        try:
            return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc).astimezone()
        except (OSError, OverflowError, ValueError):
            return None
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return None
        if text.isdigit():
            return parse_timestamp(int(text))
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = dt.datetime.fromisoformat(text)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.astimezone()
        return parsed.astimezone()
    return None


def iso_or_empty(value: dt.datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone().isoformat(timespec="seconds")


def in_window(timestamp: dt.datetime | None, window: TimeWindow | None) -> bool:
    if window is None or timestamp is None:
        return True
    return window.since <= timestamp <= window.until


def resolve_path(path: str | Path | None) -> Path | None:
    if not path:
        return None
    try:
        return Path(path).expanduser().resolve()
    except OSError:
        return Path(path).expanduser()


def same_project(record_cwd: str | None, target_cwd: Path, scope: str) -> bool:
    if scope == "all-projects":
        return True
    if not record_cwd:
        return True
    record_path = resolve_path(record_cwd)
    target_path = resolve_path(target_cwd)
    if record_path is None or target_path is None:
        return True
    if record_path == target_path:
        return True
    return record_path in target_path.parents or target_path in record_path.parents


def ensure_run_dir(ctx: RunContext) -> Path:
    if ctx.run_dir is not None:
        return ctx.run_dir
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug_source = f"{ctx.command}-{ctx.runtime}-{ctx.cwd}"
    slug = hashlib.sha256(slug_source.encode("utf-8")).hexdigest()[:8]
    run_dir = ctx.output_root / f"{stamp}-{ctx.command}-{slug}"
    run_dir.mkdir(parents=True, exist_ok=False)
    ctx.run_dir = run_dir
    return run_dir


def read_jsonl(path: Path, errors: list[dict[str, Any]]) -> Iterable[tuple[int, dict[str, Any]]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(
                        {
                            "path": str(path),
                            "line": line_no,
                            "error": f"invalid JSONL: {exc}",
                        }
                    )
                    continue
                if isinstance(value, dict):
                    yield line_no, value
    except FileNotFoundError:
        return
    except OSError as exc:
        errors.append({"path": str(path), "error": str(exc)})


def cap_text(text: str, max_chars: int = DEFAULT_TEXT_CHARS) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[: max_chars - 20] + "\n[...truncated...]", True


def preview_text(text: str, max_chars: int) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    if len(collapsed) <= max_chars:
        return collapsed
    return collapsed[: max_chars - 3].rstrip() + "..."


def content_to_text(content: Any) -> str:
    parts: list[str] = []
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                block_type = block.get("type")
                if block_type in {"text", "thinking"} and isinstance(block.get(block_type), str):
                    parts.append(block[block_type])
                elif block_type == "tool_use":
                    name = block.get("name", "")
                    payload = block.get("input")
                    parts.append(f"tool_use {name} {json.dumps(payload, sort_keys=True, default=str)}")
                elif block_type == "tool_result":
                    parts.append(content_to_text(block.get("content")))
                elif isinstance(block.get("text"), str):
                    parts.append(block["text"])
    elif isinstance(content, dict):
        for key in ("text", "content", "thinking"):
            if isinstance(content.get(key), str):
                parts.append(content[key])
    return "\n".join(part for part in parts if part)


def recursively_collect_strings(value: Any, limit: int = 30) -> list[str]:
    found: list[str] = []

    def walk(item: Any) -> None:
        if len(found) >= limit:
            return
        if isinstance(item, str):
            if item.strip():
                found.append(item)
        elif isinstance(item, dict):
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return found


def make_result(
    *,
    ctx: RunContext,
    kind: str,
    source: str,
    confidence: str,
    timestamp: dt.datetime | None,
    path: Path | None,
    text: str,
    session_id: str | None = None,
    thread_id: str | None = None,
    cwd: str | None = None,
    line: int | None = None,
    role: str | None = None,
    context: str | None = None,
) -> dict[str, Any]:
    text_body, text_capped = cap_text(text)
    return {
        "runtime": ctx.runtime,
        "kind": kind,
        "source": source,
        "confidence": confidence,
        "timestamp": iso_or_empty(timestamp),
        "session_id": session_id or "",
        "thread_id": thread_id or "",
        "cwd": cwd or "",
        "path": str(path) if path else "",
        "line": line,
        "role": role or "",
        "preview": preview_text(text_body, ctx.max_preview_chars),
        "text": text_body,
        "text_capped": text_capped,
        "context": context or "",
    }


def sort_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(item: dict[str, Any]) -> str:
        return item.get("timestamp") or ""

    return sorted(results, key=key, reverse=True)


def paginate(results: list[dict[str, Any]], limit: int, page: int) -> list[dict[str, Any]]:
    start = max(page - 1, 0) * limit
    return results[start : start + limit]


def write_artifacts(
    ctx: RunContext,
    results: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> Path:
    run_dir = ensure_run_dir(ctx)
    for index, result in enumerate(results, 1):
        result["id"] = result.get("id") or f"r{index:04d}"
    manifest = {
        "command": ctx.command,
        "runtime": ctx.runtime,
        "cwd": str(ctx.cwd),
        "scope": ctx.scope,
        "since": iso_or_empty(ctx.window.since) if ctx.window else "",
        "until": iso_or_empty(ctx.window.until) if ctx.window else "",
        "result_count": len(results),
        "source_count": len(sources),
        "error_count": len(errors),
        "max_results": ctx.max_results,
        "truncated": ctx.truncated,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    write_jsonl(run_dir / "results.jsonl", results)
    write_jsonl(run_dir / "sources.jsonl", sources)
    write_jsonl(run_dir / "errors.jsonl", errors)
    return run_dir


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def print_summary(
    ctx: RunContext,
    results: list[dict[str, Any]],
    visible: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    run_dir: Path,
    extra_args: list[str],
) -> None:
    if ctx.fmt == "jsonl":
        for result in visible:
            print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return

    searched_names = list(dict.fromkeys(source.get("name", "unknown") for source in sources))
    searched = ",".join(searched_names) or "none"
    if len(sources) > len(searched_names):
        searched = f"{searched} ({len(sources)} stores)"
    if results:
        capped = (
            f" (capped at {ctx.max_results}; narrow --since or add terms)" if ctx.truncated else ""
        )
        print(
            f"OK agent-history {ctx.command}: {len(results)} matches{capped}; "
            f"showing {len(visible)}; run={run_dir}"
        )
    else:
        print(f"NO_MATCH agent-history {ctx.command}: searched {searched}; run={run_dir}")

    for result in visible:
        timestamp = result.get("timestamp") or "unknown-time"
        session = result.get("session_id") or result.get("thread_id") or "unknown-session"
        path = result.get("path") or "unknown-path"
        line = f":{result['line']}" if result.get("line") else ""
        print(
            f"{result['id']} | {timestamp} | {result.get('runtime')} | "
            f"{result.get('kind')} | {result.get('confidence')} | {session} | "
            f"{path}{line} | {result.get('preview')}"
        )

    script_path = Path(__file__).resolve()
    if visible:
        first_id = visible[0]["id"]
        print(f"show: python3 {script_path} show --run {run_dir} --id {first_id} --context 3")
    if len(results) > ctx.page * ctx.limit:
        print(
            "next page: "
            f"python3 {script_path} {ctx.command} {' '.join(extra_args)} --page {ctx.page + 1}"
        )


def sqlite_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    try:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    except sqlite3.Error:
        return set()
    return {str(row[1]) for row in rows}


def codex_thread_rows(home: Path, errors: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    db = home / "state_5.sqlite"
    if not db.exists():
        return {}
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        errors.append({"path": str(db), "error": str(exc)})
        return {}
    try:
        cols = sqlite_columns(conn, "threads")
        if not cols:
            return {}
        wanted = [
            "id",
            "rollout_path",
            "cwd",
            "title",
            "created_at",
            "updated_at",
            "created_at_ms",
            "updated_at_ms",
            "first_user_message",
            "model",
        ]
        selected = [col for col in wanted if col in cols]
        rows = conn.execute(f"SELECT {', '.join(selected)} FROM threads").fetchall()
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            item = dict(zip(selected, row))
            if item.get("id"):
                result[str(item["id"])] = item
        return result
    except sqlite3.Error as exc:
        errors.append({"path": str(db), "error": str(exc)})
        return {}
    finally:
        conn.close()


def codex_thread_timestamp(row: dict[str, Any]) -> dt.datetime | None:
    return (
        parse_timestamp(row.get("updated_at_ms"))
        or parse_timestamp(row.get("updated_at"))
        or parse_timestamp(row.get("created_at_ms"))
        or parse_timestamp(row.get("created_at"))
    )


def codex_rollout_paths(
    home: Path,
    threads: dict[str, dict[str, Any]],
    ctx: RunContext,
) -> list[Path]:
    paths: list[Path] = []
    for row in threads.values():
        if not same_project(row.get("cwd"), ctx.cwd, ctx.scope):
            continue
        if not in_window(codex_thread_timestamp(row), ctx.window):
            continue
        rollout_path = row.get("rollout_path")
        if rollout_path:
            path = Path(str(rollout_path)).expanduser()
            if path.exists():
                paths.append(path)
    if paths:
        return sorted(set(paths))

    discovered: list[Path] = []
    for root_name in ("sessions", "archived_sessions"):
        root = home / root_name
        if root.exists():
            discovered.extend(root.rglob("rollout-*.jsonl"))
    return sorted(set(discovered))


def collect_codex_sessions(ctx: RunContext) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    sources = [{"name": "codex_state", "path": str(ctx.codex_home / "state_5.sqlite")}]
    threads = codex_thread_rows(ctx.codex_home, errors)
    results: list[dict[str, Any]] = []
    for thread_id, row in threads.items():
        ts = codex_thread_timestamp(row)
        if not same_project(row.get("cwd"), ctx.cwd, ctx.scope) or not in_window(ts, ctx.window):
            continue
        text = row.get("title") or row.get("first_user_message") or thread_id
        results.append(
            make_result(
                ctx=ctx,
                kind="session",
                source="codex_state.threads",
                confidence="exact",
                timestamp=ts,
                path=ctx.codex_home / "state_5.sqlite",
                text=str(text),
                thread_id=thread_id,
                cwd=row.get("cwd"),
            )
        )
    return sort_results(results), sources, errors


def collect_codex_history_prompts(
    ctx: RunContext,
    threads: dict[str, dict[str, Any]],
    errors: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    path = ctx.codex_home / "history.jsonl"
    sources = [{"name": "codex_history", "path": str(path)}]
    results: list[dict[str, Any]] = []
    for line_no, row in read_jsonl(path, errors):
        thread_id = str(row.get("session_id") or row.get("conversation_id") or "")
        thread = threads.get(thread_id, {})
        ts = parse_timestamp(row.get("ts"))
        if not in_window(ts, ctx.window):
            continue
        if not same_project(thread.get("cwd"), ctx.cwd, ctx.scope):
            continue
        text = str(row.get("text") or "")
        if not text:
            continue
        results.append(
            make_result(
                ctx=ctx,
                kind="prompt",
                source="codex_history",
                confidence="exact",
                timestamp=ts,
                path=path,
                line=line_no,
                text=text,
                thread_id=thread_id,
                cwd=thread.get("cwd"),
                role="user",
            )
        )
    return results, sources


def extract_codex_rollout_records(
    ctx: RunContext,
    threads: dict[str, dict[str, Any]],
    errors: list[dict[str, Any]],
    *,
    mode: str,
    matcher: Any | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    paths = codex_rollout_paths(ctx.codex_home, threads, ctx)
    sources = [{"name": "codex_rollouts", "path": str(path)} for path in paths]
    results: list[dict[str, Any]] = []
    for path in paths:
        thread_id = ""
        cwd = ""
        for line_no, row in read_jsonl(path, errors):
            ts = parse_timestamp(row.get("timestamp"))
            row_type = row.get("type")
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            if row_type == "session_meta":
                thread_id = str(payload.get("id") or thread_id)
                cwd = str(payload.get("cwd") or cwd)
                continue
            if not in_window(ts, ctx.window):
                continue
            if cwd and not same_project(cwd, ctx.cwd, ctx.scope):
                continue

            if row_type == "response_item":
                payload_type = payload.get("type")
                if payload_type == "message":
                    role = str(payload.get("role") or "")
                    text = content_to_text(payload.get("content"))
                    if mode == "prompts" and role == "user" and text:
                        results.append(
                            make_result(
                                ctx=ctx,
                                kind="prompt",
                                source="codex_rollout.message",
                                confidence="exact",
                                timestamp=ts,
                                path=path,
                                line=line_no,
                                text=text,
                                thread_id=thread_id,
                                cwd=cwd,
                                role=role,
                            )
                        )
                    elif mode == "commands" and role == "user" and text.strip().startswith("/"):
                        results.append(
                            make_result(
                                ctx=ctx,
                                kind="command",
                                source="codex_rollout.message",
                                confidence="exact",
                                timestamp=ts,
                                path=path,
                                line=line_no,
                                text=text,
                                thread_id=thread_id,
                                cwd=cwd,
                                role=role,
                            )
                        )
                    elif mode == "search" and text and matcher(text):
                        results.append(
                            make_result(
                                ctx=ctx,
                                kind="message",
                                source="codex_rollout.message",
                                confidence="exact",
                                timestamp=ts,
                                path=path,
                                line=line_no,
                                text=text,
                                thread_id=thread_id,
                                cwd=cwd,
                                role=role,
                            )
                        )
                elif payload_type == "function_call":
                    name = str(payload.get("name") or "")
                    args = payload.get("arguments")
                    text = f"{name} {args if isinstance(args, str) else json.dumps(args, sort_keys=True, default=str)}"
                    if mode == "goals" and name in {"create_goal", "update_goal"}:
                        results.append(
                            make_result(
                                ctx=ctx,
                                kind="goal",
                                source="codex_rollout.function_call",
                                confidence="exact",
                                timestamp=ts,
                                path=path,
                                line=line_no,
                                text=text,
                                thread_id=thread_id,
                                cwd=cwd,
                                role="tool_call",
                            )
                        )
                    elif mode == "search" and matcher(text):
                        results.append(
                            make_result(
                                ctx=ctx,
                                kind="tool_call",
                                source="codex_rollout.function_call",
                                confidence="exact",
                                timestamp=ts,
                                path=path,
                                line=line_no,
                                text=text,
                                thread_id=thread_id,
                                cwd=cwd,
                                role="tool_call",
                            )
                        )
            elif row_type == "event_msg" and mode == "search":
                text = "\n".join(recursively_collect_strings(payload))
                if text and matcher(text):
                    results.append(
                        make_result(
                            ctx=ctx,
                            kind="event",
                            source="codex_rollout.event_msg",
                            confidence="exact",
                            timestamp=ts,
                            path=path,
                            line=line_no,
                            text=text,
                            thread_id=thread_id,
                            cwd=cwd,
                        )
                    )
    return results, sources


def collect_codex_goals(ctx: RunContext) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    sources = [{"name": "codex_thread_goals", "path": str(ctx.codex_home / "state_5.sqlite")}]
    results: list[dict[str, Any]] = []
    threads = codex_thread_rows(ctx.codex_home, errors)
    db = ctx.codex_home / "state_5.sqlite"
    if db.exists():
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            cols = sqlite_columns(conn, "thread_goals")
            if cols:
                selected = [col for col in ("thread_id", "goal_id", "objective", "status", "token_budget", "tokens_used", "time_used_seconds", "created_at_ms", "updated_at_ms") if col in cols]
                for row in conn.execute(f"SELECT {', '.join(selected)} FROM thread_goals").fetchall():
                    item = dict(zip(selected, row))
                    thread_id = str(item.get("thread_id") or "")
                    thread = threads.get(thread_id, {})
                    ts = parse_timestamp(item.get("updated_at_ms")) or parse_timestamp(item.get("created_at_ms"))
                    if not in_window(ts, ctx.window):
                        continue
                    if not same_project(thread.get("cwd"), ctx.cwd, ctx.scope):
                        continue
                    objective = str(item.get("objective") or "")
                    status = str(item.get("status") or "")
                    text = f"/goal current state: {objective} [{status}]"
                    results.append(
                        make_result(
                            ctx=ctx,
                            kind="goal",
                            source="codex_state.thread_goals",
                            confidence="inferred",
                            timestamp=ts,
                            path=db,
                            text=text,
                            thread_id=thread_id,
                            cwd=thread.get("cwd"),
                        )
                    )
            conn.close()
        except sqlite3.Error as exc:
            errors.append({"path": str(db), "error": str(exc)})
    rollout_results, rollout_sources = extract_codex_rollout_records(ctx, threads, errors, mode="goals")
    results.extend(rollout_results)
    sources.extend(rollout_sources)
    return sort_results(results), sources, errors


def collect_codex(ctx: RunContext, mode: str, matcher: Any | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if mode == "sessions":
        return collect_codex_sessions(ctx)
    if mode == "goals":
        return collect_codex_goals(ctx)

    errors: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    threads = codex_thread_rows(ctx.codex_home, errors)
    results: list[dict[str, Any]] = []
    if mode in {"prompts", "commands", "search"}:
        history_results, history_sources = collect_codex_history_prompts(ctx, threads, errors)
        sources.extend(history_sources)
        if mode == "prompts":
            results.extend(history_results)
        elif mode == "commands":
            results.extend(
                [
                    dict(result, kind="command")
                    for result in history_results
                    if result.get("text", "").lstrip().startswith("/")
                ]
            )
        elif mode == "search":
            results.extend([result for result in history_results if matcher(result.get("text", ""))])
    rollout_results, rollout_sources = extract_codex_rollout_records(
        ctx,
        threads,
        errors,
        mode=mode,
        matcher=matcher,
    )
    results.extend(rollout_results)
    sources.extend(rollout_sources)
    if mode == "commands":
        goal_results, goal_sources, goal_errors = collect_codex_goals(ctx)
        results.extend([dict(result, kind="command") for result in goal_results if result.get("source") == "codex_state.thread_goals"])
        sources.extend(goal_sources)
        errors.extend(goal_errors)
    return sort_results(results), sources, errors


def claude_project_files(home: Path, include_sidechains: bool) -> list[Path]:
    root = home / "projects"
    if not root.exists():
        return []
    files = sorted(root.glob("*/*.jsonl"))
    if include_sidechains:
        files.extend(sorted(root.glob("*/*/subagents/*.jsonl")))
    return files


def collect_claude_history(
    ctx: RunContext,
    errors: list[dict[str, Any]],
    *,
    mode: str,
    matcher: Any | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    path = ctx.claude_home / "history.jsonl"
    sources = [{"name": "claude_history", "path": str(path)}]
    results: list[dict[str, Any]] = []
    for line_no, row in read_jsonl(path, errors):
        ts = parse_timestamp(row.get("timestamp"))
        if not in_window(ts, ctx.window):
            continue
        project = str(row.get("project") or "")
        if not same_project(project, ctx.cwd, ctx.scope):
            continue
        text = str(row.get("display") or "")
        if not text:
            continue
        is_command = text.lstrip().startswith("/")
        if mode == "prompts" or (mode == "commands" and is_command) or (mode == "goals" and text.lstrip().startswith("/goal")) or (mode == "search" and matcher(text)):
            results.append(
                make_result(
                    ctx=ctx,
                    kind="command" if is_command and mode in {"commands", "goals"} else "prompt",
                    source="claude_history",
                    confidence="exact",
                    timestamp=ts,
                    path=path,
                    line=line_no,
                    text=text,
                    session_id=str(row.get("sessionId") or ""),
                    cwd=project,
                    role="user",
                )
            )
    return results, sources


def collect_claude_project_records(
    ctx: RunContext,
    errors: list[dict[str, Any]],
    *,
    mode: str,
    matcher: Any | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    files = claude_project_files(ctx.claude_home, ctx.include_sidechains)
    sources = [{"name": "claude_project_jsonl", "path": str(path)} for path in files]
    results: list[dict[str, Any]] = []
    sessions: dict[str, dict[str, Any]] = {}
    for path in files:
        for line_no, row in read_jsonl(path, errors):
            record_type = str(row.get("type") or "")
            session_id = str(row.get("sessionId") or "")
            cwd = str(row.get("cwd") or "")
            ts = parse_timestamp(row.get("timestamp"))
            if session_id:
                session = sessions.setdefault(
                    session_id,
                    {
                        "session_id": session_id,
                        "cwd": cwd,
                        "path": path,
                        "first_ts": ts,
                        "last_ts": ts,
                        "title": "",
                        "messages": 0,
                    },
                )
                if cwd and not session.get("cwd"):
                    session["cwd"] = cwd
                if ts and (session.get("first_ts") is None or ts < session["first_ts"]):
                    session["first_ts"] = ts
                if ts and (session.get("last_ts") is None or ts > session["last_ts"]):
                    session["last_ts"] = ts
                if record_type in {"user", "assistant"}:
                    session["messages"] += 1
                if record_type in {"custom-title", "ai-title"}:
                    session["title"] = row.get("customTitle") or row.get("aiTitle") or session.get("title") or ""

            if mode == "sessions":
                continue
            if not in_window(ts, ctx.window):
                continue
            if not same_project(cwd, ctx.cwd, ctx.scope):
                continue
            if record_type == "queue-operation":
                text = str(row.get("content") or "")
                if not text:
                    continue
                is_command = text.lstrip().startswith("/")
                if (mode == "commands" and is_command) or (mode == "goals" and text.lstrip().startswith("/goal")) or (mode == "search" and matcher(text)):
                    results.append(
                        make_result(
                            ctx=ctx,
                            kind="command",
                            source="claude_project.queue-operation",
                            confidence="exact",
                            timestamp=ts,
                            path=path,
                            line=line_no,
                            text=text,
                            session_id=session_id,
                            cwd=cwd,
                            role="user",
                        )
                    )
            elif record_type in {"user", "assistant"}:
                message = row.get("message") if isinstance(row.get("message"), dict) else {}
                role = str(message.get("role") or record_type)
                text = content_to_text(message.get("content"))
                if not text:
                    continue
                if mode == "prompts" and record_type == "user" and "tool_result" not in text[:80]:
                    results.append(
                        make_result(
                            ctx=ctx,
                            kind="prompt",
                            source="claude_project.user",
                            confidence="exact",
                            timestamp=ts,
                            path=path,
                            line=line_no,
                            text=text,
                            session_id=session_id,
                            cwd=cwd,
                            role=role,
                        )
                    )
                elif mode == "search" and matcher(text):
                    results.append(
                        make_result(
                            ctx=ctx,
                            kind="message",
                            source=f"claude_project.{record_type}",
                            confidence="exact",
                            timestamp=ts,
                            path=path,
                            line=line_no,
                            text=text,
                            session_id=session_id,
                            cwd=cwd,
                            role=role,
                        )
                    )

    if mode == "sessions":
        for session in sessions.values():
            ts = session.get("last_ts")
            if not in_window(ts, ctx.window):
                continue
            if not same_project(session.get("cwd"), ctx.cwd, ctx.scope):
                continue
            text = session.get("title") or f"{session['session_id']} ({session.get('messages', 0)} messages)"
            results.append(
                make_result(
                    ctx=ctx,
                    kind="session",
                    source="claude_project.session",
                    confidence="exact",
                    timestamp=ts,
                    path=session.get("path"),
                    text=str(text),
                    session_id=session["session_id"],
                    cwd=session.get("cwd"),
                )
            )
    return results, sources


def collect_claude(ctx: RunContext, mode: str, matcher: Any | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    if mode in {"prompts", "commands", "goals", "search"}:
        history_results, history_sources = collect_claude_history(ctx, errors, mode=mode, matcher=matcher)
        results.extend(history_results)
        sources.extend(history_sources)
    project_results, project_sources = collect_claude_project_records(ctx, errors, mode=mode, matcher=matcher)
    results.extend(project_results)
    sources.extend(project_sources)
    return sort_results(results), sources, errors


def session_home(ctx: RunContext) -> Path:
    base = ctx.pi_home if ctx.runtime == "pi" else ctx.prime_home
    return base / "agent"


def session_message_text(content: Any, *, text_only: bool = False) -> str:
    """Flatten Pi/Prime message content blocks: text, thinking, toolCall, image."""
    if isinstance(content, str):
        return content
    parts: list[str] = []
    if not isinstance(content, list):
        return ""
    for block in content:
        if isinstance(block, str):
            parts.append(block)
            continue
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")
        if block_type == "text" and isinstance(block.get("text"), str):
            parts.append(block["text"])
        elif text_only:
            continue
        elif block_type == "thinking" and isinstance(block.get("thinking"), str):
            parts.append(block["thinking"])
        elif block_type == "toolCall":
            name = str(block.get("name") or "")
            arguments = block.get("arguments")
            rendered = (
                arguments
                if isinstance(arguments, str)
                else json.dumps(arguments, sort_keys=True, default=str)
            )
            parts.append(f"toolCall {name} {rendered}")
        elif block_type == "image":
            parts.append("[image]")
        elif isinstance(block.get("text"), str):
            parts.append(block["text"])
    return "\n".join(part for part in parts if part)


def read_session_header(path: Path, errors: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the `type: session` first line, or None when this is not a transcript."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            first_line = handle.readline()
    except OSError as exc:
        errors.append({"path": str(path), "error": str(exc)})
        return None
    if not first_line.strip():
        return None
    try:
        header = json.loads(first_line)
    except json.JSONDecodeError:
        return None
    if not isinstance(header, dict) or header.get("type") != "session":
        return None
    return header


def file_mtime(path: Path) -> dt.datetime | None:
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    except OSError:
        return None


def session_overlaps_window(header: dict[str, Any], path: Path, window: TimeWindow | None) -> bool:
    """A session spans [header timestamp, file mtime]; keep it when that overlaps."""
    if window is None:
        return True
    start = parse_timestamp(header.get("timestamp"))
    end = file_mtime(path)
    if start is not None and start > window.until:
        return False
    if end is not None and end < window.since:
        return False
    return True


def pi_session_files(home: Path) -> list[Path]:
    root = home / "sessions"
    if not root.exists():
        return []
    return sorted(path for path in root.glob("*/*.jsonl") if PI_SESSION_NAME.match(path.name))


def prime_session_files(home: Path) -> list[Path]:
    root = home / "sessions"
    if not root.exists():
        return []
    return sorted(path for path in root.glob("*.jsonl") if SESSION_UUID_NAME.match(path.name))


def prime_subagent_files(
    home: Path,
    root_session_id: str,
    errors: list[dict[str, Any]],
) -> list[tuple[Path, str]]:
    """Child transcripts for one Prime root, labelled from `rlm-subagents.jsonl`."""
    artifacts = home / "session-artifacts" / root_session_id
    if not artifacts.is_dir():
        return []
    labels: dict[str, str] = {}
    index = artifacts / "rlm-subagents.jsonl"
    if index.exists():
        for _, row in read_jsonl(index, errors):
            child_id = str(row.get("childId") or "")
            if child_id:
                labels[child_id] = str(row.get("sessionName") or child_id)
    found: list[tuple[Path, str]] = []
    for child_dir in sorted(artifacts.glob("sub-*")):
        for path in sorted(child_dir.glob("*.jsonl")):
            if SESSION_UUID_NAME.match(path.name):
                found.append((path, labels.get(child_dir.name, child_dir.name)))
    return found


def pi_prime_candidates(ctx: RunContext, errors: list[dict[str, Any]]) -> list[SessionCandidate]:
    home = session_home(ctx)
    files = pi_session_files(home) if ctx.runtime == "pi" else prime_session_files(home)
    candidates: list[SessionCandidate] = []
    for path in files:
        header = read_session_header(path, errors)
        if header is None:
            continue
        if not same_project(str(header.get("cwd") or ""), ctx.cwd, ctx.scope):
            continue
        if not session_overlaps_window(header, path, ctx.window):
            continue
        candidates.append(SessionCandidate(path=path, header=header, source=f"{ctx.runtime}_sessions"))

    if ctx.runtime != "prime" or not ctx.include_sidechains:
        return candidates

    children: list[SessionCandidate] = []
    for root in candidates:
        root_id = str(root.header.get("id") or "")
        if not root_id:
            continue
        for path, label in prime_subagent_files(home, root_id, errors):
            header = read_session_header(path, errors)
            if header is None:
                continue
            if not session_overlaps_window(header, path, ctx.window):
                continue
            children.append(
                SessionCandidate(
                    path=path,
                    header=header,
                    source="prime_subagents",
                    label=label,
                    parent_session_id=root_id,
                )
            )
    return candidates + children


def collect_pi_prime_records(
    ctx: RunContext,
    candidate: SessionCandidate,
    errors: list[dict[str, Any]],
    *,
    mode: str,
    matcher: Any | None = None,
    max_results: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    header = candidate.header
    session_id = str(header.get("id") or "")
    cwd = str(header.get("cwd") or "")
    path = candidate.path
    prefix = f"{ctx.runtime}_session"

    results: list[dict[str, Any]] = []
    name = candidate.label
    model = ""
    binding = ""
    messages = 0
    compactions = 0
    last_ts = parse_timestamp(header.get("timestamp"))

    def emit(**kwargs: Any) -> None:
        results.append(
            make_result(
                ctx=ctx,
                session_id=session_id,
                cwd=cwd,
                path=path,
                **kwargs,
            )
        )

    truncated = False
    for line_no, row in read_jsonl(path, errors):
        if max_results is not None and len(results) >= max_results:
            truncated = True
            break
        row_type = str(row.get("type") or "")
        if row_type in SESSION_SKIP_TYPES:
            continue
        ts = parse_timestamp(row.get("timestamp"))
        if ts is not None and (last_ts is None or ts > last_ts):
            last_ts = ts

        if row_type == "session_info":
            name = str(row.get("name") or name)
        elif row_type == "model_change":
            model = str(row.get("modelId") or model)
        elif row_type == "message":
            messages += 1
        elif row_type == "compaction":
            compactions += 1
        elif row_type == "custom" and row.get("customType") == "aimgr_credential_binding_v1":
            data = row.get("data") if isinstance(row.get("data"), dict) else {}
            binding = str(data.get("binding") or binding)

        if mode == "sessions" or not in_window(ts, ctx.window):
            continue

        if row_type == "message":
            message = row.get("message") if isinstance(row.get("message"), dict) else {}
            role = str(message.get("role") or "")
            if mode == "prompts":
                if role != "user":
                    continue
                text = session_message_text(message.get("content"), text_only=True)
                if not text.strip():
                    continue
                emit(
                    kind="prompt",
                    source=f"{prefix}.user",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=text,
                    role=role,
                )
            elif mode in {"commands", "goals"}:
                if role != "user":
                    continue
                text = session_message_text(message.get("content"), text_only=True)
                if not text.strip().startswith("/goal" if mode == "goals" else "/"):
                    continue
                emit(
                    kind="goal" if mode == "goals" else "command",
                    source=f"{prefix}.user",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=text,
                    role=role,
                )
            elif mode == "search":
                text = session_message_text(message.get("content"))
                if not text or not matcher(text):
                    continue
                emit(
                    kind="message",
                    source=f"{prefix}.{role or 'message'}",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=text,
                    role=role,
                )
        elif row_type == "custom_message":
            custom_type = str(row.get("customType") or "")
            text = str(row.get("content") or "")
            if not text:
                continue
            if mode in {"commands", "goals"} and custom_type == "session_slash_command":
                details = row.get("details") if isinstance(row.get("details"), dict) else {}
                command = details.get("command") if isinstance(details.get("command"), dict) else {}
                command_text = str(command.get("text") or text)
                if mode == "goals" and not command_text.strip().startswith("/goal"):
                    continue
                emit(
                    kind="goal" if mode == "goals" else "command",
                    source=f"{prefix}.session_slash_command",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=command_text,
                    role="user",
                )
            elif mode == "search" and matcher(text):
                emit(
                    kind="agent_message" if custom_type == "agent_message" else "custom",
                    source=f"{prefix}.{custom_type or 'custom_message'}",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=text,
                )
        elif row_type == "compaction" and mode == "search":
            summary = str(row.get("summary") or "")
            if summary and matcher(summary):
                emit(
                    kind="compaction",
                    source=f"{prefix}.compaction",
                    confidence="best_effort",
                    timestamp=ts,
                    line=line_no,
                    text=summary,
                    context="compaction summary; the replaced turns are no longer in this transcript",
                )
        elif row_type == "agent_status" and mode == "search":
            status = row.get("status") if isinstance(row.get("status"), dict) else {}
            summary = str(status.get("summary") or "")
            if summary and matcher(summary):
                emit(
                    kind="status",
                    source=f"{prefix}.agent_status",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=summary,
                )
        elif row_type == "custom" and mode == "search":
            text = "\n".join(recursively_collect_strings(row.get("data")))
            if text and matcher(text):
                emit(
                    kind="custom",
                    source=f"{prefix}.{row.get('customType') or 'custom'}",
                    confidence="exact",
                    timestamp=ts,
                    line=line_no,
                    text=text,
                )

    if mode == "sessions":
        detail = [f"{messages} messages"]
        if model:
            detail.append(model)
        if binding:
            detail.append(f"account {binding}")
        if compactions:
            detail.append(f"{compactions} compactions")
        if candidate.parent_session_id:
            detail.append(f"child of {candidate.parent_session_id}")
        emit(
            kind="session",
            source=f"{prefix}.session",
            confidence="exact",
            timestamp=last_ts,
            text=f"{name or session_id} ({', '.join(detail)})",
        )

    stats: dict[str, Any] = {
        "session_id": session_id,
        "messages": messages,
        "compactions": compactions,
    }
    if candidate.label:
        stats["child"] = candidate.label
    if truncated:
        stats["truncated"] = True
    return results, stats


def collect_pi_prime(
    ctx: RunContext,
    mode: str,
    matcher: Any | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    home = session_home(ctx)
    store_root = home / "sessions"

    candidates = pi_prime_candidates(ctx, errors)
    if not candidates:
        return [], [{"name": f"{ctx.runtime}_sessions", "path": str(store_root)}], errors

    results: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    if mode == "goals":
        # There is no durable goal store in either runtime; `/goal` command text
        # inside transcripts is the only evidence, so say that in the receipt.
        sources.append(
            {
                "name": f"{ctx.runtime}_sessions",
                "path": str(store_root),
                "note": "no goal store in this runtime; /goal command text only",
            }
        )
    # Newest session first, so a capped scan keeps the most recent evidence.
    def recency(candidate: SessionCandidate) -> str:
        started = parse_timestamp(candidate.header.get("timestamp")) or file_mtime(candidate.path)
        return iso_or_empty(started)

    ordered = sorted(candidates, key=recency, reverse=True)
    remaining = max(ctx.max_results, 0) if ctx.max_results else None
    skipped = 0
    for candidate in ordered:
        if remaining is not None and remaining <= 0:
            ctx.truncated = True
            skipped += 1
            continue
        candidate_results, stats = collect_pi_prime_records(
            ctx,
            candidate,
            errors,
            mode=mode,
            matcher=matcher,
            max_results=remaining,
        )
        results.extend(candidate_results)
        sources.append({"name": candidate.source, "path": str(candidate.path), **stats})
        if stats.get("truncated"):
            ctx.truncated = True
        if remaining is not None:
            remaining -= len(candidate_results)
    if skipped:
        sources.append(
            {
                "name": f"{ctx.runtime}_sessions_unscanned",
                "path": str(store_root),
                "note": f"{skipped} older sessions not scanned after the result cap",
            }
        )
    return sort_results(results), sources, errors


def build_matcher(args: argparse.Namespace) -> Any:
    terms = list(args.query or [])
    if args.regex:
        pattern = re.compile(args.regex, re.IGNORECASE | re.MULTILINE)
        return lambda text: bool(pattern.search(text or ""))
    lowered = [term.lower() for term in terms if term.strip()]
    if not lowered:
        raise HistoryError("search requires query terms or --regex")
    return lambda text: any(term in (text or "").lower() for term in lowered)


def execute_search_command(args: argparse.Namespace) -> int:
    ctx = context_from_args(args, command=args.command)
    matcher = build_matcher(args) if args.command == "search" else None
    if ctx.runtime == "codex":
        results, sources, errors = collect_codex(ctx, args.command, matcher=matcher)
    elif ctx.runtime == "claude":
        results, sources, errors = collect_claude(ctx, args.command, matcher=matcher)
    elif ctx.runtime in {"pi", "prime"}:
        results, sources, errors = collect_pi_prime(ctx, args.command, matcher=matcher)
    else:
        raise HistoryError("--runtime must be codex, claude, pi, or prime")

    if ctx.max_results and len(results) > ctx.max_results:
        results = results[: ctx.max_results]
        ctx.truncated = True

    visible = paginate(results, ctx.limit, ctx.page)
    run_dir = write_artifacts(ctx, results, sources, errors)
    extra_args = rebuild_args_for_next_page(args)
    print_summary(ctx, results, visible, sources, run_dir, extra_args)
    return 0


def rebuild_args_for_next_page(args: argparse.Namespace) -> list[str]:
    pieces = ["--runtime", args.runtime, "--cwd", str(args.cwd), "--scope", args.scope, "--since", args.since]
    if args.until:
        pieces.extend(["--until", args.until])
    if args.include_sidechains:
        pieces.append("--include-sidechains")
    for flag, value, default in (
        ("--codex-home", args.codex_home, Path.home() / ".codex"),
        ("--claude-home", args.claude_home, Path.home() / ".claude"),
        ("--pi-home", args.pi_home, Path.home() / ".pi"),
        ("--prime-home", args.prime_home, Path.home() / ".prime"),
    ):
        if str(value) != str(default):
            pieces.extend([flag, str(value)])
    if args.command == "search":
        if args.regex:
            pieces.extend(["--regex", args.regex])
        pieces.extend(args.query or [])
    return pieces


def context_from_args(args: argparse.Namespace, *, command: str) -> RunContext:
    now = local_now()
    since = parse_time_value(args.since, default=now - dt.timedelta(hours=24))
    until = parse_time_value(args.until, default=now)
    return RunContext(
        command=command,
        runtime=args.runtime,
        cwd=Path(args.cwd).expanduser().resolve(),
        scope=args.scope,
        window=TimeWindow(since=since, until=until),
        output_root=Path(args.output_root).expanduser(),
        codex_home=Path(args.codex_home).expanduser(),
        claude_home=Path(args.claude_home).expanduser(),
        pi_home=Path(args.pi_home).expanduser(),
        prime_home=Path(args.prime_home).expanduser(),
        limit=args.limit,
        max_results=args.max_results,
        page=args.page,
        max_preview_chars=args.max_preview_chars,
        fmt=args.format,
        include_sidechains=args.include_sidechains,
    )


def cmd_show(args: argparse.Namespace) -> int:
    run_dir = Path(args.run).expanduser()
    results_path = run_dir / "results.jsonl"
    errors: list[dict[str, Any]] = []
    results = [row for _, row in read_jsonl(results_path, errors)]
    target_index = next((idx for idx, row in enumerate(results) if row.get("id") == args.id), None)
    target = results[target_index] if target_index is not None else None
    if target is None:
        print(f"ERROR agent-history show: result id {args.id!r} not found in {results_path}")
        return 2
    print(f"OK agent-history show: {args.id}; run={run_dir}")
    print(
        f"{target.get('timestamp') or 'unknown-time'} | {target.get('runtime')} | "
        f"{target.get('kind')} | {target.get('confidence')} | "
        f"{target.get('session_id') or target.get('thread_id')}"
    )
    print(f"path: {target.get('path')}{':' + str(target.get('line')) if target.get('line') else ''}")
    print(f"cwd: {target.get('cwd')}")
    text = target.get("text") or target.get("preview") or ""
    if not args.raw and len(text) > args.max_chars:
        text = text[: args.max_chars - 20] + "\n[...truncated...]"
    print("")
    print(text)
    if target.get("context"):
        print("")
        print("context:")
        print(target["context"])
    if args.context > 0 and target_index is not None:
        start = max(0, target_index - args.context)
        end = min(len(results), target_index + args.context + 1)
        nearby = [row for idx, row in enumerate(results[start:end], start) if idx != target_index]
        if nearby:
            print("")
            print("nearby results:")
            for row in nearby:
                print(
                    f"{row.get('id')} | {row.get('timestamp') or 'unknown-time'} | "
                    f"{row.get('kind')} | {row.get('preview')}"
                )
    return 0


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--runtime", required=True, choices=("codex", "claude", "pi", "prime"))
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--scope", default="current-project", choices=("current-project", "all-projects"))
    parser.add_argument("--since", default="24h")
    parser.add_argument("--until", default=None)
    parser.add_argument("--include-sidechains", action="store_true")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--format", default="summary", choices=("summary", "jsonl"))
    parser.add_argument("--max-preview-chars", type=int, default=DEFAULT_PREVIEW_CHARS)
    parser.add_argument("--output-root", default=str(Path(tempfile.gettempdir()) / "agent-history"))
    parser.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--pi-home", default=str(Path.home() / ".pi"))
    parser.add_argument("--prime-home", default=str(Path.home() / ".prime"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent_history.py")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("sessions", "prompts", "commands", "goals"):
        child = sub.add_parser(name)
        add_common_options(child)
        child.set_defaults(func=execute_search_command)
    search = sub.add_parser("search")
    add_common_options(search)
    search.add_argument("query", nargs="*")
    search.add_argument("--regex", default=None)
    search.set_defaults(func=execute_search_command)

    show = sub.add_parser("show")
    show.add_argument("--run", required=True)
    show.add_argument("--id", required=True)
    show.add_argument("--context", type=int, default=3)
    show.add_argument("--raw", action="store_true")
    show.add_argument("--max-chars", type=int, default=2000)
    show.set_defaults(func=cmd_show)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except HistoryError as exc:
        print(f"ERROR agent-history {getattr(args, 'command', 'unknown')}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
