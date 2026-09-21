"""Shared, read-only parsing for the agent-watcher scripts.

Handles the three transcript dialects the watcher reads: Codex rollouts,
Claude Code project JSONL, and Prime Agent session JSONL. Everything here is
stdlib-only and side-effect free. Scripts own stdout shape; this module owns
record classification and text extraction.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Iterator

STATE_ROOT = Path(os.environ.get("AGENT_WATCHER_HOME", Path.home() / ".agent-watcher"))

RUNTIMES = ("codex", "claude", "prime")

# Kinds emitted by classify(). Keep the set small; the watcher reasons over these.
USER_KINDS = {"USER", "USER_INTERRUPT", "USER_QUEUED"}
RESTATEMENT_KINDS = {"GOAL", "HEARTBEAT", "COMPACTION", "SPAWN", "AGENT_MSG"}


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_ts(raw: Any) -> dt.datetime | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        val = float(raw)
        if val > 1e12:
            val /= 1000.0
        try:
            return dt.datetime.fromtimestamp(val).astimezone()
        except (OverflowError, OSError, ValueError):
            return None
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return None
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            parsed = dt.datetime.fromisoformat(s)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone()
    return None


def iso(ts: dt.datetime | None) -> str:
    return ts.strftime("%Y-%m-%dT%H:%M:%S%z") if ts else ""


def age_str(ts: dt.datetime | None, ref: dt.datetime | None = None) -> str:
    if ts is None:
        return "?"
    ref = ref or now()
    secs = int((ref - ts).total_seconds())
    if secs < 0:
        secs = 0
    if secs < 60:
        return f"{secs}s"
    if secs < 3600:
        return f"{secs // 60}m"
    if secs < 86400:
        return f"{secs // 3600}h{(secs % 3600) // 60:02d}m"
    return f"{secs // 86400}d{(secs % 86400) // 3600}h"


def parse_duration(raw: str) -> dt.timedelta:
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([smhd])\s*", raw)
    if not m:
        raise ValueError(f"bad duration: {raw!r} (use e.g. 90m, 6h, 2d)")
    n, unit = float(m.group(1)), m.group(2)
    return dt.timedelta(seconds=n * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit])


def squash(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def short_path(p: str | Path) -> str:
    s = str(p)
    home = str(Path.home())
    return "~" + s[len(home):] if s.startswith(home) else s


def content_text(content: Any) -> str:
    """Flatten Codex/Claude/Prime content blocks to text. Skips tool payloads."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        for key in ("text", "input_text", "output_text", "content"):
            if key in content and isinstance(content[key], (str, list)):
                return content_text(content[key])
        return ""
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type")
                if btype in ("text", "input_text", "output_text"):
                    parts.append(str(block.get("text", "")))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(p for p in parts if p)
    return ""


def iter_lines(path: Path, start: int = 0, max_bytes: int | None = None) -> Iterator[tuple[int, int, str]]:
    """Yield (line_start_offset, next_offset, line) for complete lines from start.

    A trailing line without a newline is treated as incomplete and not yielded,
    so a caller can safely resume from the returned next_offset later.
    """
    with open(path, "rb") as fh:
        fh.seek(start)
        offset = start
        consumed = 0
        while True:
            raw = fh.readline()
            if not raw:
                break
            if not raw.endswith(b"\n"):
                break  # partial trailing line; leave it for the next read
            next_offset = offset + len(raw)
            yield offset, next_offset, raw.decode("utf-8", errors="replace")
            offset = next_offset
            consumed += len(raw)
            if max_bytes is not None and consumed >= max_bytes:
                break


def tail_lines(path: Path, tail_bytes: int) -> list[str]:
    size = path.stat().st_size
    start = max(0, size - tail_bytes)
    with open(path, "rb") as fh:
        fh.seek(start)
        data = fh.read()
    text = data.decode("utf-8", errors="replace")
    lines = text.split("\n")
    if start > 0 and lines:
        lines = lines[1:]  # first line is partial
    return [ln for ln in lines if ln.strip()]


def load_json(line: str) -> dict[str, Any] | None:
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def _event(kind: str, ts: Any, text: str = "", name: str = "", **extra: Any) -> dict[str, Any]:
    ev: dict[str, Any] = {"kind": kind, "ts": iso(parse_ts(ts)), "text": text or ""}
    if name:
        ev["name"] = name
    ev.update({k: v for k, v in extra.items() if v not in (None, "", [], {})})
    return ev


def _args_preview(args: Any, limit: int = 220) -> str:
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return squash(args, limit)
    if isinstance(args, dict):
        for key in ("command", "cmd", "file_path", "path", "description", "prompt", "message", "objective", "pattern", "query", "url"):
            val = args.get(key)
            if isinstance(val, list):
                val = " ".join(str(v) for v in val)
            if isinstance(val, str) and val.strip():
                return squash(f"{key}={val}", limit)
        return squash(json.dumps(args, ensure_ascii=False), limit)
    return squash(str(args), limit)


CODEX_INJECTED_PREFIXES = ("# AGENTS.md instructions", "<INSTRUCTIONS>", "<skills_instructions>", "<environment_context>")
CODEX_SPAWN_TOOLS = {"spawn_agent", "send_message", "followup_task", "wait_agent", "close_agent"}
CODEX_GOAL_TOOLS = {"create_goal", "update_goal"}


def classify_codex(obj: dict[str, Any]) -> list[dict[str, Any]]:
    t = obj.get("type")
    ts = obj.get("timestamp")
    pl = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
    out: list[dict[str, Any]] = []
    if t == "session_meta":
        out.append(_event("META", ts, name="session", cwd=pl.get("cwd"), session_id=pl.get("id") or pl.get("session_id"),
                          model=pl.get("model"), source=pl.get("thread_source")))
    elif t == "turn_context":
        sandbox = pl.get("sandbox_policy")
        out.append(_event("META", ts, name="turn_context", cwd=pl.get("cwd"), model=pl.get("model"),
                          approval=pl.get("approval_policy"),
                          sandbox=sandbox.get("type") if isinstance(sandbox, dict) else sandbox))
    elif t == "compacted":
        out.append(_event("COMPACTION", ts, "codex compaction"))
    elif t == "event_msg":
        pt = pl.get("type")
        if pt == "item_completed":
            item = pl.get("item") or {}
            if item.get("type") == "UserMessage":
                out.append(_event("USER", ts, content_text(item.get("content"))))
        elif pt == "task_complete":
            out.append(_event("TASK_COMPLETE", ts, str(pl.get("last_agent_message") or "")))
        elif pt == "turn_aborted":
            out.append(_event("ABORTED", ts, str(pl.get("reason") or "")))
    elif t == "response_item":
        pt = pl.get("type")
        if pt == "message":
            role = pl.get("role")
            text = content_text(pl.get("content"))
            if role == "assistant":
                out.append(_event("ASSISTANT", ts, text, phase=pl.get("phase")))
            elif role == "user":
                stripped = text.lstrip()
                if "<codex_internal_context" in stripped and 'source="goal"' in stripped:
                    out.append(_event("GOAL", ts, text))
                elif stripped.startswith(CODEX_INJECTED_PREFIXES) or "<codex_internal_context" in stripped:
                    pass  # injected instructions, not the human
                elif text.strip():
                    out.append(_event("USER", ts, text, source="response_item"))
        elif pt in ("function_call", "custom_tool_call"):
            name = str(pl.get("name") or "")
            args = pl.get("arguments") if pt == "function_call" else pl.get("input")
            if name in CODEX_GOAL_TOOLS:
                out.append(_event("GOAL", ts, _args_preview(args, 800), name=name))
            elif name in CODEX_SPAWN_TOOLS:
                out.append(_event("SPAWN", ts, "payload encrypted in rollout; read the parent's narration", name=name))
            else:
                ev = _event("TOOL", ts, _args_preview(args), name=name)
                ev["_raw"] = args
                out.append(ev)
    return out


def classify_claude(obj: dict[str, Any]) -> list[dict[str, Any]]:
    t = obj.get("type")
    ts = obj.get("timestamp")
    out: list[dict[str, Any]] = []
    if t == "user":
        if obj.get("isMeta"):
            return out
        msg = obj.get("message") or {}
        content = msg.get("content")
        if isinstance(content, str):
            text = content
            if text.strip():
                out.append(_event("USER", ts, text, cwd=obj.get("cwd")))
        elif isinstance(content, list):
            texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                    out.append(_event("TOOL_ERROR", ts, squash(content_text(b.get("content")), 300)))
            text = "\n".join(x for x in texts if x)
            if text.strip():
                s = text.lstrip()
                if s.startswith("[Request interrupted"):
                    out.append(_event("USER_INTERRUPT", ts, text, cwd=obj.get("cwd")))
                elif s.startswith("<task-notification>"):
                    out.append(_event("CHILD_NOTICE", ts, text))
                elif s.startswith("<system-reminder>") or s.startswith("<local-command"):
                    pass
                else:
                    out.append(_event("USER", ts, text, cwd=obj.get("cwd")))
    elif t == "assistant":
        msg = obj.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            text = "\n".join(x for x in texts if x)
            if text.strip():
                out.append(_event("ASSISTANT", ts, text, model=msg.get("model")))
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    name = str(b.get("name") or "")
                    inp = b.get("input") or {}
                    if name in ("Agent", "Task"):
                        prompt = inp.get("prompt") if isinstance(inp, dict) else ""
                        out.append(_event("SPAWN", ts, squash(str(prompt or ""), 600), name=name,
                                          model=inp.get("model") if isinstance(inp, dict) else None,
                                          description=inp.get("description") if isinstance(inp, dict) else None))
                    elif name == "AskUserQuestion":
                        out.append(_event("ASK", ts, _args_preview(inp, 400), name=name))
                    else:
                        ev = _event("TOOL", ts, _args_preview(inp), name=name)
                        ev["_raw"] = inp
                        out.append(ev)
    elif t == "queue-operation":
        out.append(_event("USER_QUEUED", ts, str(obj.get("content") or ""), reason=obj.get("reason")))
    elif t == "system":
        st = obj.get("subtype")
        if st == "away_summary":
            out.append(_event("AWAY_SUMMARY", ts, str(obj.get("content") or "")))
        elif st == "compact_boundary":
            out.append(_event("COMPACTION", ts, "claude compaction"))
    elif t == "permission-mode":
        out.append(_event("META", ts, name="permission-mode", mode=obj.get("permissionMode")))
    return out


PRIME_SKIP = {"child_usage_attributed", "agent_status", "token_usage", "git_state", "model_change",
              "thinking_level_change", "service_tier_change", "session_state", "session_info"}


def _prime_goal_block(summary: str) -> str:
    m = re.search(r"## Goal\s*(.*?)(?:\n## |\Z)", summary or "", re.S)
    return (m.group(1).strip() if m else squash(summary or "", 400))


def classify_prime(obj: dict[str, Any]) -> list[dict[str, Any]]:
    t = obj.get("type")
    ts = obj.get("timestamp")
    out: list[dict[str, Any]] = []
    if t in PRIME_SKIP:
        return out
    if t == "session":
        out.append(_event("META", ts, name="session", cwd=obj.get("cwd"), session_id=obj.get("id"),
                          depth=obj.get("rlmDepth")))
    elif t == "message":
        msg = obj.get("message") or {}
        role = msg.get("role")
        content = msg.get("content")
        if role == "user":
            text = content_text(content)
            if text.strip():
                out.append(_event("USER", ts, text))
        elif role == "assistant":
            text = content_text(content)
            if text.strip():
                out.append(_event("ASSISTANT", ts, text))
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "toolCall":
                        ev = _event("TOOL", ts, _args_preview(b.get("arguments")), name=str(b.get("name") or ""))
                        ev["_raw"] = b.get("arguments")
                        out.append(ev)
        elif role == "toolResult" and msg.get("isError"):
            out.append(_event("TOOL_ERROR", ts, squash(content_text(content), 300)))
    elif t == "custom_message":
        ct = obj.get("customType")
        content = str(obj.get("content") or "")
        if ct == "heartbeat_prompt":
            out.append(_event("HEARTBEAT", ts, content))
        elif ct == "agent_message":
            out.append(_event("AGENT_MSG", ts, content))
        elif ct == "rlm_child_terminal_notice":
            out.append(_event("CHILD_NOTICE", ts, content))
        elif ct == "session_slash_command":
            details = obj.get("details") or {}
            cmd = (details.get("command") or {}).get("text") if isinstance(details, dict) else None
            out.append(_event("USER", ts, cmd or content, source="slash"))
    elif t == "compaction":
        out.append(_event("COMPACTION", ts, _prime_goal_block(str(obj.get("summary") or "")), name="goal"))
    return out


def classify(runtime: str, obj: dict[str, Any]) -> list[dict[str, Any]]:
    if runtime == "codex":
        return classify_codex(obj)
    if runtime == "claude":
        return classify_claude(obj)
    if runtime == "prime":
        return classify_prime(obj)
    raise ValueError(f"unknown runtime {runtime}")


# Substrings that a line must contain to possibly yield one of the anchor kinds.
ANCHOR_HINTS = {
    "codex": ('"UserMessage"', '"role": "user"', '"role":"user"', '"session_meta"', '"turn_context"',
              '"compacted"', "create_goal", "update_goal", "spawn_agent"),
    "claude": ('"type": "user"', '"type":"user"', "queue-operation", "permission-mode", "compact_boundary", '"Agent"', '"Task"'),
    "prime": ('"role": "user"', '"role":"user"', '"type": "session"', '"type":"session"', "heartbeat_prompt",
              '"compaction"', "agent_message", "session_slash_command"),
}


def line_may_anchor(runtime: str, line: str) -> bool:
    return any(h in line for h in ANCHOR_HINTS[runtime])


def last_meaningful(runtime: str, lines: list[str]) -> dict[str, Any] | None:
    """Classify from the end and return the last event that says who acted last."""
    for line in reversed(lines):
        obj = load_json(line)
        if not obj:
            continue
        evs = classify(runtime, obj)
        for ev in reversed(evs):
            if ev["kind"] in ("META", "COMPACTION", "CHILD_NOTICE"):
                continue
            return ev
    return None


def session_key(runtime: str, session_id: str) -> str:
    return f"{runtime}-{session_id}"


def session_dir(key: str) -> Path:
    return STATE_ROOT / "sessions" / key


def user_kind(ev: dict[str, Any]) -> bool:
    return ev.get("kind") in USER_KINDS
