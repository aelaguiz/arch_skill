"""Parse a Claude Code stream-json transcript (PLAN.md 6.8, INTERFACES.md).

`claude_run.py` writes `stream.jsonl` with one line per stdout line of the session, stamped on arrival:
`{"t": <epoch>, "e": <event>}`, or `{"t": <epoch>, "raw": "<text>"}` for a line that is not a JSON object. `parse` also
reads an unstamped stream (the raw stream-json lines, as in the 2026-10-14 probes); there an event's time is its own
`timestamp` field when it has one, else the last time seen before it.

`Transcript.calls` holds one dict per tool call, in the order the tool-use events arrived:

    {"id", "name", "input", "parent_id", "t_use", "t_result", "result_text", "depth", "is_error", "agent_id"}

`parent_id` is the event's `parent_tool_use_id` (None for the main agent); `depth` is how many calls sit above it in
that chain (0 for the main agent, 1 for a subagent's call, 2 for a subagent's subagent); `t_use` and `t_result` are the
arrival times of the tool-use and tool-result events (the call's window; `t_result` is None when no result arrived).
A call is a subagent's when its parent chain leads to an Agent (or Task) call of the main agent.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

DISPATCH_TOOLS = frozenset({"Agent", "Task"})


_ISO_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?\s*(Z|[+-]\d{2}:?\d{2})?$"
)


def _iso_epoch(value):
    """Epoch seconds of an event's ISO `timestamp` ("2026-10-15T01:14:02.675Z"), or None."""
    if not isinstance(value, str):
        return None
    match = _ISO_RE.match(value.strip())
    if not match:
        return None
    year, month, day, hour, minute, second = (int(match.group(i)) for i in range(1, 7))
    fraction = float("0." + match.group(7)) if match.group(7) else 0.0
    try:
        stamp = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    except ValueError:
        return None
    offset = match.group(8)
    seconds = stamp.timestamp() + fraction
    if offset and offset != "Z":
        sign = 1 if offset[0] == "+" else -1
        digits = offset[1:].replace(":", "")
        seconds -= sign * (int(digits[:2]) * 3600 + int(digits[2:4]) * 60)
    return seconds


def _result_text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif isinstance(block.get("content"), (str, list)):
                    parts.append(_result_text(block["content"]))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    if isinstance(content, dict):
        return _result_text([content])
    return str(content)


def strings_in(value):
    """Every string inside a JSON value (dict values, list items), depth first."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings_in(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from strings_in(item)
    elif value is not None:
        yield str(value)


class Transcript:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else None
        self.stamped = False
        self.events = []      # [(t, event)] in arrival order
        self.raw_lines = []   # [(t, text)]
        self.calls = []
        self.by_id = {}
        self.texts = []       # [{"t", "parent_id", "text"}] assistant text blocks
        self.results = []     # [(t, result event)]
        self.init = None
        self.t0 = None
        self.t_end = None
        self.final_text = ""
        self.cost_usd = None
        self.orphan_results = 0

    # ----- calls and their chains -----
    @property
    def agent_calls(self):
        """Agent/Task calls of the main agent (the dispatches)."""
        return [c for c in self.calls if c["name"] in DISPATCH_TOOLS and c["parent_id"] is None]

    def parent(self, call):
        pid = call.get("parent_id")
        return self.by_id.get(pid) if pid is not None else None

    def chain(self, call):
        """The calls above `call`, nearest first."""
        out = []
        seen = {call.get("id")}
        cur = call
        while cur.get("parent_id") is not None:
            parent = self.by_id.get(cur["parent_id"])
            if parent is None or parent.get("id") in seen:
                break
            out.append(parent)
            seen.add(parent.get("id"))
            cur = parent
        return out

    def dispatch_of(self, call):
        """The main agent's Agent/Task call that `call` runs under, or None for a main-agent call."""
        for ancestor in self.chain(call):
            if ancestor["name"] in DISPATCH_TOOLS and ancestor.get("parent_id") is None:
                return ancestor
        return None

    def is_subagent(self, call) -> bool:
        return self.dispatch_of(call) is not None

    def window(self, call):
        """(start, end) of a call; an unfinished call runs to the end of the transcript."""
        end = call.get("t_result")
        if end is None:
            end = self.t_end
        return call.get("t_use"), end

    # ----- outcome -----
    @property
    def last_result(self):
        return self.results[-1][1] if self.results else None

    def result_subtypes(self):
        return [ev.get("subtype") for _t, ev in self.results]

    @property
    def budget_hit(self) -> bool:
        return any("budget" in str(ev.get("subtype") or "").lower() for _t, ev in self.results)

    @property
    def ok(self) -> bool:
        """The session ended with a successful result event."""
        last = self.last_result
        return bool(last) and not last.get("is_error") and str(last.get("subtype") or "") == "success"

    def main_texts(self):
        return [item["text"] for item in self.texts if item["parent_id"] is None]


def _note_time(tr, t):
    if t is None:
        return
    if tr.t0 is None or t < tr.t0:
        tr.t0 = t
    if tr.t_end is None or t > tr.t_end:
        tr.t_end = t


def _ingest(tr, t, ev):
    tr.events.append((t, ev))
    etype = ev.get("type")
    if etype == "system":
        if ev.get("subtype") == "init" and tr.init is None:
            tr.init = ev
    elif etype == "assistant":
        message = ev.get("message") or {}
        parent = ev.get("parent_tool_use_id")
        content = message.get("content") or []
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                cid = block.get("id")
                if cid is None or cid in tr.by_id:
                    continue
                call = {
                    "id": cid,
                    "name": block.get("name") or "",
                    "input": block.get("input") if block.get("input") is not None else {},
                    "parent_id": parent,
                    "t_use": t,
                    "t_result": None,
                    "result_text": None,
                    "depth": None,
                    "is_error": False,
                    "agent_id": ev.get("agent_id"),
                }
                tr.calls.append(call)
                tr.by_id[cid] = call
            elif block.get("type") == "text":
                tr.texts.append({"t": t, "parent_id": parent, "text": block.get("text") or ""})
    elif etype == "user":
        message = ev.get("message") or {}
        content = message.get("content")
        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                call = tr.by_id.get(block.get("tool_use_id"))
                if call is None:
                    tr.orphan_results += 1
                    continue
                if call["t_result"] is None and call["result_text"] is None:
                    call["t_result"] = t
                    call["result_text"] = _result_text(block.get("content"))
                    call["is_error"] = bool(block.get("is_error"))
    elif etype == "result":
        tr.results.append((t, ev))


def _finish(tr):
    for call in tr.calls:
        call["depth"] = len(tr.chain(call)) if call.get("parent_id") is not None else 0
        if call.get("parent_id") is not None and call["depth"] == 0:
            call["depth"] = 1  # parent not in the stream: still not the main agent
    last = tr.last_result
    if last is not None and isinstance(last.get("result"), str):
        tr.final_text = last["result"]
    else:
        texts = tr.main_texts()
        tr.final_text = texts[-1] if texts else ""
    costs = []
    for _t, ev in tr.results:
        value = ev.get("total_cost_usd")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            costs.append(float(value))
    tr.cost_usd = max(costs) if costs else None  # total_cost_usd is cumulative across a session's turns


def parse(stream_path) -> Transcript:
    """Parse a stamped (or raw) stream-json file into a Transcript; a missing file gives an empty one."""
    tr = Transcript(stream_path)
    path = Path(stream_path)
    if not path.exists():
        return tr
    last_t = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n").rstrip("\r")
            try:
                obj = json.loads(line) if line.strip() else None
            except ValueError:
                obj = None
            if isinstance(obj, dict) and "t" in obj and set(obj) <= {"t", "e", "raw"} and ("e" in obj or "raw" in obj):
                tr.stamped = True
                try:
                    t = float(obj["t"])
                except (TypeError, ValueError):
                    t = last_t
                _note_time(tr, t)
                last_t = t if t is not None else last_t
                if "raw" in obj:
                    tr.raw_lines.append((t, str(obj["raw"])))
                    continue
                event = obj.get("e")
                if isinstance(event, dict):
                    _ingest(tr, t, event)
                else:
                    tr.raw_lines.append((t, json.dumps(event)))
                continue
            if isinstance(obj, dict):
                t = _iso_epoch(obj.get("timestamp"))
                if t is None:
                    t = last_t
                else:
                    last_t = t
                _note_time(tr, t)
                _ingest(tr, t, obj)
            else:
                tr.raw_lines.append((last_t, line))
    _finish(tr)
    return tr


def main(argv=None):
    """`python3 runner/transcript.py STREAM.jsonl`: print the calls, final text and cost (for debugging)."""
    import sys

    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: transcript.py STREAM.jsonl", file=sys.stderr)
        return 2
    tr = parse(args[0])
    t0 = tr.t0 or 0.0
    for call in tr.calls:
        start, end = tr.window(call)
        span = f"{(start or t0) - t0:8.2f}s..{(end or t0) - t0:8.2f}s"
        who = "main" if call["depth"] == 0 else f"sub{call['depth']}"
        summary = json.dumps(call["input"], ensure_ascii=False)[:100]
        print(f"{span} {who:5} {call['name']:6} {call['id']} {summary}")
    print("final:", tr.final_text[:300])
    print("cost_usd:", tr.cost_usd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
