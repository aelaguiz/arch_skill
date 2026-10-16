"""Workbook reader, authorship and the grading definitions of PLAN.md 6.6 and 6.8 (draft 8), and 13.2 to 13.4.

`load_run(run_dir, hidden_dir)` gathers one run's artifacts into a `Run`: the final workbook (`RUN/work/workbook/`),
the fixture's workbook (`HIDDEN/initial_workbook/`), each session's stamped transcript, watcher log and session.json
(one session for a scenario run; `RUN/ticks/<n>/` for a backtest), the simulator's action log and outbox, `meta.json`,
and the simulator's `World` (read-only). Every grade comes from these artifacts, never from an agent's own account.

Scenario graders (`scenarios/VNN/grade.py`) and the backtest grader build their checks from the helpers here; each
check is `{"name", "pass", "evidence"}`.
"""
from __future__ import annotations

import hashlib
import html as html_mod
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from runner import transcript as transcript_mod  # noqa: E402
from runner.transcript import DISPATCH_TOOLS, strings_in  # noqa: E402
from runner.watch import (  # noqa: E402
    TAB_KEYS, key_column, normalize_col, read_csv_file, read_watch_log, row_identities, tab_name,
)

# ----------------------------------------------------------------------------------------------------------------------
# the record (PLAN.md 4.5, 4.7)

TABS = ("Charter", "Library", "Ideas", "Map", "Tests", "Checks", "Results", "Decisions", "Lessons", "Reviews", "Money",
        "Log")
COLUMNS = {
    "Charter": ("field", "value", "reason", "history"),
    "Library": ("library_id", "kind", "source", "link", "owner", "content", "signal", "type", "status", "notes",
                "legacy_ref"),
    "Ideas": ("idea_id", "source", "type", "description", "sources", "near_copy_of", "status", "reason", "legacy_ref"),
    "Map": ("type", "best_test_id", "best_result", "tests_count", "last_tested", "status", "history"),
    "Tests": ("test_id", "idea_id", "lane", "type", "comparison", "hypothesis", "expected_range", "varies",
              "held_constant", "good_looks_like", "daily_budget", "days", "read_at", "guardrails", "rerun_of",
              "lesson_id", "item_id", "platform_id", "status", "launched_at", "legacy_ref", "history"),
    "Checks": ("check_id", "test_id", "item_id", "role", "verdict", "reasons"),
    "Results": ("result_id", "test_id", "window", "metric", "k", "n", "spend", "rate_text", "versus", "chance_beats",
                "method", "call", "notes", "legacy_ref"),
    "Decisions": ("decision_id", "test_id", "kind", "reason", "data", "legacy_ref"),
    "Lessons": ("lesson_id", "subject", "statement", "winner", "loser", "status", "evidence", "recheck_at",
                "legacy_ref", "history"),
    "Reviews": ("review_id", "role", "period", "findings", "call", "changes"),
    "Money": ("entry_id", "kind", "lane", "amount", "standing", "learned", "next", "note"),
    "Log": ("tick_id", "platform_time", "read", "did", "next"),
}
TAIL_COLUMNS = ("written_at", "written_by")
# Added with PLAN.md 13.1 (3) to (5): graders accept them wherever they appear and only V25 to V30 rely on them, so
# COLUMNS stays what every workbook must hold (V19's check) and these stay optional.
EXTRA_COLUMNS = {"Library": ("coding",), "Tests": ("made_from", "recipe", "coding", "checks", "read", "decision"),
                 "Results": ("signals",)}
OVERVIEW_COLUMNS = ("item", "value", "as_of")
VIEW_TABS = ("Overview",)

OWNER_FIELDS = ("goal", "money_total", "off_limits", "money_request_channel")
SETUP_FIELDS = ("bar", "budget_unit", "must_not_waste", "levers", "attributes", "audience", "reporting", "platform",
                "second_source")
METHOD_FIELDS = ("early_read", "map_attributes", "lanes", "exploring", "acting", "believing", "replacing",
                 "lesson_life", "research_freshness", "test_sizing", "pace", "cadence", "trigger", "role_model",
                 "outside_sources", "competitors")
CHARTER_FIELDS = OWNER_FIELDS + SETUP_FIELDS + METHOD_FIELDS  # 29

# The Charter a climb set up through the intake interview writes (docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md,
# references/charter.md): the owner's fields come from the interview and each cites its Interview row; `levers` and
# `reporting` moved to the owner's; `audience` is gone (who responds is what a climb finds out); `tools` is setup's.
# 36 fields. The fixtures' Charters keep the layout above, which CHARTER_FIELDS still describes.
INTAKE_OWNER_FIELDS = ("purpose", "earlier_work", "goal", "success", "money_total", "levers", "off_limits",
                       "making_from", "quality_floor", "tool_rules", "research_direction", "reporting",
                       "money_request_channel")
INTAKE_SETUP_FIELDS = ("bar", "budget_unit", "must_not_waste", "attributes", "tools", "platform", "second_source")
INTAKE_CHARTER_FIELDS = INTAKE_OWNER_FIELDS + INTAKE_SETUP_FIELDS + METHOD_FIELDS  # 36
INTERVIEW_TAB = "Interview"
INTERVIEW_COLUMNS = ("interview_id", "kind", "question", "answer", "asked_at", "answered_at", "about", "research",
                     "status", "history")
# What the simulated owner judges each message for (runner/owner.py); the first four must never be true.
OWNER_FLAGS = ("asked_method", "asked_finding_out", "asked_known", "multiple_questions", "outcome_check", "playback",
               "signed_off")

ROLES = ("plan-checker", "build-checker", "critic", "reader", "meta-analyst", "strategist", "auditor", "scout")

# Tools that cannot write a file are never a row's author (PLAN.md 6.8 leaves out Agent and Task calls; the same
# reasoning leaves out these).
NON_WRITING_TOOLS = frozenset({
    "Read", "Skill", "Glob", "Grep", "LS", "WebFetch", "WebSearch", "TodoWrite", "ToolSearch", "TaskOutput",
    "BashOutput", "KillShell", "TaskStop", "SendMessage", "ExitPlanMode", "EnterPlanMode", "ListMcpResourcesTool",
    "ReadMcpResourceTool",
})

WINDOW_SLACK_S = 1.0
# The watcher notices a write some time after the call that made it ends: its own poll, plus lag on a loaded machine
# (1.4 s seen with the load near 35). A row may follow its call's end by this much more.
WATCH_LAG_S = 3.0

QUESTION_PHRASES = ("let me know", "should i", "do you want", "would you like", "want me to", "shall i",
                    "please confirm", "can you confirm")

WORLD_START = datetime(2026, 11, 2, tzinfo=timezone.utc)
WORLD_DAYS = {"W1": 14, "W2": 10, "W3": 10, "W4": 7, "W5": 14}
W3_SLOTS = ((9, 0.9), (13, 1.0), (19, 1.15))
NEVER_BOUGHT_STARS = ("g31", "g35", "g38")

# ----------------------------------------------------------------------------------------------------------------------
# tolerant reading (PLAN.md 6.6)


def norm_label(value) -> str:
    """Case-insensitive, punctuation-free form used to compare labels."""
    return re.sub(r"[^0-9a-z]+", "", str(value or "").lower())


SYNONYMS = {
    ("checks", "pass"): ("pass", "passed", "ok"),
    ("checks", "fail"): ("fail", "failed"),
    ("results", "act"): ("act",),
    ("results", "stop"): ("stop", "drop"),
    ("results", "hold"): ("hold", "inconclusive"),
    ("decisions", "pause"): ("pause", "stop-spend"),
    ("decisions", "exclude-data"): ("exclude-data", "exclude", "set-aside"),
    ("decisions", "void"): ("void", "cancel", "correction"),
    ("decisions", "scale"): ("scale",),
    ("decisions", "method-change"): ("method-change", "method"),
    ("lessons", "proven"): ("proven", "confirmed"),
    ("lessons", "retired"): ("retired", "dropped", "rejected"),
    ("lessons", "recheck"): ("recheck", "rechecking"),
    ("lessons", "unconfirmed"): ("unconfirmed", "provisional"),
    ("ideas", "rejected"): ("rejected", "parked", "shelved", "duplicate", "near-copy"),
    ("ideas", "parked"): ("rejected", "parked", "shelved", "duplicate", "near-copy"),
    ("tests", "paused"): ("paused", "stopped"),
    ("tests", "withdrawn"): ("withdrawn",),
    ("tests", "closed"): ("closed", "read"),
    # Not in the plan's table; the Money tab's own labels with the obvious spellings (see the runner's report).
    ("money", "request"): ("request", "money-request", "requested"),
    ("money", "grant"): ("grant", "granted"),
}


def is_label(value, tab: str, label: str) -> bool:
    accepted = SYNONYMS.get((tab.lower(), label), (label,))
    return norm_label(value) in {norm_label(word) for word in accepted}


def role_named(written_by, role: str) -> bool:
    """`written_by` names the role (any value containing the role's name, punctuation ignored)."""
    return norm_label(role) in norm_label(written_by)


_TIME_RE = re.compile(
    r"(\d{4})-(\d{1,2})-(\d{1,2})"
    r"(?:[T ]+(\d{1,2})(?:[:h](\d{2})(?::(\d{2})(?:\.\d+)?)?)?)?"
    r"\s*(Z|UTC|GMT|[+-]\d{2}(?::?\d{2})?)?",
    re.IGNORECASE,
)


def parse_time(value):
    """Lenient ISO reader: a date, a date and hour, with or without minutes, seconds, `Z` or an offset. UTC."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    match = _TIME_RE.match(text) or _TIME_RE.search(text)
    if not match:
        return None
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    hour = int(match.group(4) or 0)
    minute = int(match.group(5) or 0)
    second = int(match.group(6) or 0)
    try:
        stamp = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    except ValueError:
        return None
    zone = (match.group(7) or "").upper()
    if zone and zone not in ("Z", "UTC", "GMT"):
        sign = 1 if zone[0] == "+" else -1
        digits = zone[1:].replace(":", "")
        hours = int(digits[:2])
        minutes = int(digits[2:4]) if len(digits) >= 4 else 0
        stamp -= sign * timedelta(hours=hours, minutes=minutes)
    return stamp


def iso(stamp) -> str:
    if stamp is None:
        return ""
    return stamp.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def parse_amount(value):
    """Amounts and budgets: currency signs, commas and units stripped; the first number."""
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = str(value).replace(",", "")
    match = _NUMBER_RE.search(text)
    return float(match.group(0)) if match else None


def parse_int(value):
    amount = parse_amount(value)
    if amount is None or amount != int(amount):
        return None
    return int(amount)


def parse_percent(value):
    """The first number followed by `%` (PLAN.md 6.8). Used only to report a share the charter's `exploring` names;
    no grade depends on it."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", str(value or ""))
    return float(match.group(1)) if match else None


def parse_type(value):
    """'hook=question|visual=app-screen' -> {'hook': 'question', 'visual': 'app-screen'}; None when no pair parses."""
    text = str(value or "").strip()
    if not text:
        return None
    out = {}
    for part in re.split(r"[|,;&+]|\band\b", text):
        if "=" in part:
            name, _, val = part.partition("=")
        elif ":" in part:
            name, _, val = part.partition(":")
        else:
            continue
        name = name.strip().strip("`'\"").lower()
        val = val.strip().strip("`'\"").lower()
        if name and val:
            out[name] = val
    return out or None


def type_covers(candidate, reference) -> bool:
    """Every attr=value of `reference` is in `candidate` (a row of that cell, possibly naming held attributes too)."""
    cand = candidate if isinstance(candidate, dict) else parse_type(candidate)
    ref = reference if isinstance(reference, dict) else parse_type(reference)
    if not cand or not ref:
        return False
    return all(cand.get(name) == val for name, val in ref.items())


def norm_key(value) -> str:
    return str(value or "").strip().lower()


def normalize_field(value) -> str:
    text = str(value or "").strip().strip("`'\"").lower()
    return re.sub(r"[\s\-]+", "_", text)


def _token_re(ident: str):
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(ident) + r"(?![0-9])", re.IGNORECASE)


def text_names(text, *idents) -> bool:
    text = str(text or "")
    return any(ident and _token_re(ident).search(text) for ident in idents)


def row_text(row: dict) -> str:
    return "\n".join(str(v) for v in row.values() if v)


def row_names(row: dict, *idents) -> bool:
    """Some value of the row contains one of the ids as a token."""
    return text_names(row_text(row), *idents)


_KEY_RE = re.compile(r"(?<![A-Za-z0-9])(LB|ID|CK|RV|LG|IV|T|R|D|L|M)-(\d+)(?![0-9])", re.IGNORECASE)   # any digit count: the skill fixes none
_KEY_TABS = {"LB": "Library", "ID": "Ideas", "CK": "Checks", "RV": "Reviews", "LG": "Log", "IV": "Interview",
             "T": "Tests", "R": "Results", "D": "Decisions", "L": "Lessons", "M": "Money"}


def keys_in(text):
    """Workbook keys named in a text: [('LB', 'LB-0001'), ...]."""
    return [(m.group(1).upper(), f"{m.group(1).upper()}-{m.group(2)}") for m in _KEY_RE.finditer(str(text or ""))]


_ID_RANGE_SEP = r"\s*(?:\.\.\.?|\u2013|\u2014|-|\bto\b|\bthrough\b|\bthru\b)\s*"


def ids_in(text, prefix: str):
    """Platform ids with a prefix ('cp', 'po', 'it') in a text, in order. A short ascending range written the way people
    write one ('cp_0001..cp_0004', 'cp_0005-0007', 'it_0002 to it_0004') stands for every id in it."""
    pat = re.compile(rf"(?<![A-Za-z0-9]){prefix}_(\d+)(?:{_ID_RANGE_SEP}({prefix}_)?(\d+)(?![\d.]))?", re.I)
    out = []
    for m in pat.finditer(str(text or "")):
        first, second_prefixed, second = m.group(1), m.group(2), m.group(3)
        low = prefix.lower()
        if second is not None and int(first) < int(second) <= int(first) + 50:
            out.extend(f"{low}_{n:0{len(first)}d}" for n in range(int(first), int(second) + 1))
            continue
        out.append(f"{low}_{first}")
        if second is not None and second_prefixed:
            out.append(f"{low}_{second}")
    return out


def check(name: str, ok: bool, evidence: str) -> dict:
    return {"name": name, "pass": bool(ok), "evidence": evidence}


def all_pass(checks) -> bool:
    return all(item.get("pass") for item in checks)


# ----------------------------------------------------------------------------------------------------------------------
# questions in the final message


def strip_quoted(text: str) -> str:
    """Remove fenced and inline code, double-quoted and curly-quoted spans, single-quoted spans, blockquote lines and
    Markdown table rows (a table's cells describe things, such as each test's own question; they ask the reader
    nothing)."""
    text = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\"[^\"\n]*\"", " ", text)
    text = re.sub(r"“[^”\n]*”", " ", text)
    text = re.sub(r"‘[^’\n]*’", " ", text)
    text = re.sub(r"(?<![\w'])'[^'\n]+'(?![\w'])", " ", text)
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith((">", "|")))


_QUESTION_END = re.compile(r"\?(?=[\s)\]*_\"'”’]|$)")


def question_in(text: str):
    """The question found in a final message (a sentence ending in `?` or one of the listed phrases), else None.
    Phrases match on word boundaries, so "should include" is not "should i"."""
    plain = strip_quoted(text or "")
    match = _QUESTION_END.search(plain)
    if match:
        start = max(plain.rfind(".", 0, match.start()), plain.rfind("\n", 0, match.start()),
                    plain.rfind("!", 0, match.start()))
        return plain[start + 1:match.end()].strip()[-160:]
    lower = plain.lower()
    for phrase in QUESTION_PHRASES:
        if re.search(r"\b" + re.escape(phrase) + r"\b", lower):
            return phrase
    return None


# ----------------------------------------------------------------------------------------------------------------------
# workbook


def _canonical_tab(name: str) -> str:
    stem = tab_name(name)
    for tab in TABS + VIEW_TABS + (INTERVIEW_TAB,):
        if tab.lower() == stem:
            return tab
    return stem


def norm_row(raw: dict) -> dict:
    out = {}
    for key, value in (raw or {}).items():
        col = normalize_col(key)
        text = "" if value is None else str(value).strip()
        if col in out and not text:
            continue
        out[col] = text
    return out


class Tab:
    def __init__(self, name: str, header, raw_rows):
        self.name = name
        self.raw_header = list(header or [])
        self.header = [normalize_col(h) for h in self.raw_header]
        self.raw_rows = list(raw_rows or [])
        self.rows = [norm_row(r) for r in self.raw_rows]
        want = TAB_KEYS.get(name.lower())
        if want and want in self.header:
            self.key_col = want
        else:
            self.key_col = self.header[0] if self.header else None
        self.raw_key_col = key_column(name, self.raw_header)

    def key(self, row: dict) -> str:
        return str(row.get(self.key_col, "")) if self.key_col else ""

    def get(self, key):
        want = norm_key(key)
        for row in self.rows:
            if norm_key(self.key(row)) == want:
                return row
        return None

    def missing_columns(self, columns):
        return [c for c in columns if c not in self.header]

    def identities(self):
        return row_identities(self.raw_rows, self.raw_key_col)


class Workbook:
    def __init__(self, tabs=None, folder=None):
        self.tabs = dict(tabs or {})
        self.folder = folder

    @classmethod
    def from_dir(cls, folder):
        folder = Path(folder)
        tabs = {}
        if folder.is_dir():
            for path in sorted(folder.iterdir()):
                if not path.is_file() or not path.name.lower().endswith(".csv"):
                    continue
                name = _canonical_tab(path.name)
                if name in tabs:
                    continue
                header, rows = read_csv_file(path)
                tabs[name] = Tab(name, header, rows)
        return cls(tabs, folder)

    def tab(self, name: str):
        return self.tabs.get(_canonical_tab(name))

    def rows(self, name: str):
        tab = self.tab(name)
        return tab.rows if tab is not None else []

    def get(self, name: str, key):
        tab = self.tab(name)
        return tab.get(key) if tab is not None else None

    def charter(self) -> dict:
        """{normalized field: row}"""
        out = {}
        for row in self.rows("Charter"):
            field = normalize_field(row.get("field"))
            if field and field not in out:
                out[field] = row
        return out


def tab_key_col(tab: str, row: dict) -> str | None:
    want = TAB_KEYS.get(tab.lower())
    if want and want in row:
        return want
    return next(iter(row), None)


def row_key(tab: str, row: dict) -> str:
    col = tab_key_col(tab, row)
    return str(row.get(col, "")) if col else ""


# ----------------------------------------------------------------------------------------------------------------------
# sessions, changes, actions


class Change:
    """One row added, changed or removed in a watcher line."""

    __slots__ = ("t", "tab", "kind", "ident", "key", "row", "before", "session", "order")

    def __init__(self, t, tab, kind, ident, row, before, session, order):
        self.t = float(t)
        self.tab = tab
        self.kind = kind
        self.ident = ident
        self.row = row
        self.before = before
        self.session = session
        self.order = order
        self.key = row_key(tab, row)

    def __repr__(self):
        return f"Change({self.tab} {self.kind} {self.key!r} t={self.t:.2f} s={self.session})"


class Session:
    def __init__(self, index, folder, transcript, info, sim_time, prompt, tick):
        self.index = index
        self.dir = folder
        self.transcript = transcript
        self.info = info or {}
        self.sim_time = sim_time
        self.prompt = prompt
        self.tick = tick or {}
        t_start = self.info.get("started_t")
        t_end = self.info.get("ended_t")
        self.t_start = float(t_start) if isinstance(t_start, (int, float)) else transcript.t0
        self.t_end = float(t_end) if isinstance(t_end, (int, float)) else transcript.t_end
        self.setup = False

    @property
    def final_message(self) -> str:
        """The session's last `result` event (PLAN.md 6.8, draft 8)."""
        last = self.transcript.last_result
        if last is not None and isinstance(last.get("result"), str):
            return last["result"]
        return ""

    def contains(self, t, slack: float = 2.0) -> bool:
        if self.t_start is None or self.t_end is None:
            return True
        return self.t_start - slack <= t <= self.t_end + slack


SIM_SUBCOMMANDS = frozenset({"status", "catalog", "library", "build", "manifest", "launch", "resubmit", "pause",
                             "resume", "set-budget", "report", "attribution", "slots", "post"})


def parse_argv(argv):
    """(tool, subcommand, args) of a logged agent-facing call, whatever prefix the log kept."""
    tokens = [str(a) for a in argv or []]
    tool = None
    rest = tokens
    for index, token in enumerate(tokens[:4]):
        base = token.rsplit("/", 1)[-1]
        if base in ("sim", "notify", "gws", "simadmin"):
            tool = base
            rest = tokens[index + 1:]
            break
    if tool is None:
        if tokens and tokens[0] in SIM_SUBCOMMANDS:
            tool, rest = "sim", tokens
        elif "--kind" in tokens:
            tool, rest = "notify", tokens
    if tool != "sim":
        return tool, None, rest
    index = 0
    while index < len(rest):
        token = rest[index]
        if token == "--hidden":
            index += 2
            continue
        if token in SIM_SUBCOMMANDS:
            return tool, token, rest[index + 1:]
        index += 1
    return tool, None, rest


class Action:
    def __init__(self, raw: dict, index: int):
        self.raw = raw
        self.index = index
        try:
            self.wall = float(raw.get("wall_time"))
        except (TypeError, ValueError):
            self.wall = None
        self.sim_time = parse_time(raw.get("sim_time"))
        self.argv = [str(a) for a in raw.get("argv") or []]
        self.exit = raw.get("exit")
        self.out = str(raw.get("stdout_head") or "")
        self.tool, self.sub, self.args = parse_argv(self.argv)

    @property
    def ok(self) -> bool:
        return self.exit == 0

    def positional(self, prefix: str):
        for arg in self.args:
            if re.fullmatch(rf"{prefix}_\d+", arg, re.I):
                return arg.lower()
        return None

    def option(self, name: str):
        for index, arg in enumerate(self.args):
            if arg == name and index + 1 < len(self.args):
                return self.args[index + 1]
            if arg.startswith(name + "="):
                return arg.split("=", 1)[1]
        return None

    def __repr__(self):
        return f"Action({self.tool} {self.sub} {self.args} exit={self.exit})"


class Launch:
    """A `sim launch`, `sim resubmit` or `sim post` (PLAN.md 6.8 "checked launch")."""

    def __init__(self, action: Action, kind: str, target, item):
        self.action = action
        self.kind = kind
        self.target = target
        self.item = item

    @property
    def ok(self) -> bool:
        return self.action.ok

    def __repr__(self):
        return f"Launch({self.kind} {self.target} item={self.item} exit={self.action.exit})"


class Author:
    __slots__ = ("call", "session", "is_subagent", "depth", "dispatch")

    def __init__(self, call=None, session=None, is_subagent=False, depth=0, dispatch=None):
        self.call = call
        self.session = session
        self.is_subagent = is_subagent
        self.depth = depth
        self.dispatch = dispatch

    def describe(self) -> str:
        if self.call is None:
            return "no tool call matched (counted as the main agent)"
        who = "a subagent" if self.is_subagent else "the main agent"
        return f"{who} ({self.call['name']} {self.call['id']})"


def _read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _read_jsonl(path):
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


def load_world(hidden_dir):
    """The simulator's World for a hidden folder, or None when `sim.world` is not importable or the state is absent."""
    try:
        from sim.world import World  # owned by the simulator builder
    except Exception:
        return None
    try:
        return World.load(Path(hidden_dir))
    except Exception:
        return None


# ----------------------------------------------------------------------------------------------------------------------
# the run


class Run:
    def __init__(self, run_dir, hidden_dir, world=None, strict_order: bool = True):
        self.run_dir = Path(run_dir)
        self.hidden_dir = Path(hidden_dir)
        self.strict_order = strict_order
        self.meta = _read_json(self.hidden_dir / "meta.json", {}) or {}
        self.kind = self.meta.get("kind") or "scenario"
        self.scenario = self.meta.get("scenario")
        self.world_name = self.meta.get("world")
        self.now = parse_time(self.meta.get("now"))
        self.work = self.run_dir / "work"
        self.workbook = Workbook.from_dir(self.work / "workbook")
        self.initial = Workbook.from_dir(self.hidden_dir / "initial_workbook")
        self.world = world if world is not None else load_world(self.hidden_dir)
        self.sim_actions = [Action(raw, i) for i, raw in enumerate(_read_jsonl(self.hidden_dir / "sim_actions.jsonl"))]
        self.outbox = _read_jsonl(self.hidden_dir / "outbox.jsonl")
        # the intake interview, as runner/run_intake.py logged it: one entry per session, with the owner's answer and
        # flags when the session asked something; empty for a run without an interview
        self.interview = _read_jsonl(self.run_dir / "interview.jsonl")
        self.intake = _read_json(self.run_dir / "intake.json", {}) or {}
        self.sessions = self._load_sessions()
        self.changes = self._load_changes()
        self._mark_setup_sessions()
        self.pre_hashes = self._load_pre_hashes()
        self._author_cache = {}
        self._launches = None

    # ----- loading -----
    def _load_sessions(self):
        ticks = self.run_dir / "ticks"
        sessions = []
        if ticks.is_dir():
            folders = [p for p in ticks.iterdir() if p.is_dir()]
            folders.sort(key=lambda p: (int(p.name) if p.name.isdigit() else 10 ** 9, p.name))
            for index, folder in enumerate(folders):
                tick = _read_json(folder / "tick.json", {}) or {}
                info = _read_json(folder / "session.json", {}) or {}
                sim_time = parse_time(tick.get("sim_time"))
                if sim_time is None and self.now is not None:
                    sim_time = self.now + timedelta(hours=12 * index)
                sessions.append(Session(index, folder, transcript_mod.parse(folder / "stream.jsonl"), info, sim_time,
                                        tick.get("prompt") or info.get("prompt"), tick))
        else:
            info = _read_json(self.run_dir / "session.json", {}) or {}
            sessions.append(Session(0, self.run_dir, transcript_mod.parse(self.run_dir / "stream.jsonl"), info,
                                    self.now, self.meta.get("prompt") or info.get("prompt"), {}))
        return sessions

    def _load_changes(self):
        changes = []
        order = 0
        for session in self.sessions:
            for line in read_watch_log(session.dir / "watch.jsonl"):
                tab = _canonical_tab(line.get("file") or "")
                t = line.get("t")
                if not isinstance(t, (int, float)):
                    continue
                header = line.get("header") or []
                added = line.get("added") or []
                kcol = key_column(tab, header or (list(added[0]) if added else []))
                added_keys = line.get("added_keys") or [str(r.get(kcol, "")).strip() if kcol else "" for r in added]
                for row, ident in zip(added, added_keys):
                    changes.append(Change(t, tab, "added", ident, norm_row(row), None, session.index, order))
                    order += 1
                for item in line.get("changed") or []:
                    changes.append(Change(t, tab, "changed", item.get("key"), norm_row(item.get("after")),
                                          norm_row(item.get("before")), session.index, order))
                    order += 1
                removed = line.get("removed") or []
                removed_keys = line.get("removed_keys") or [str(r.get(kcol, "")).strip() if kcol else ""
                                                            for r in removed]
                for row, ident in zip(removed, removed_keys):
                    changes.append(Change(t, tab, "removed", ident, norm_row(row), None, session.index, order))
                    order += 1
        changes.sort(key=lambda c: (c.t, c.order))
        return changes

    def _mark_setup_sessions(self):
        """A session is a setup or adoption session when the Charter had no rows when it started."""
        for session in self.sessions:
            cut = session.t_start
            if cut is None:
                session.setup = not self.initial.rows("Charter") and session.index == 0
                continue
            session.setup = not self.rows_at("Charter", cut - 1e-6)

    def _load_pre_hashes(self):
        """{work-relative path: sha256} of the agent's folder before the run: the fixture builder's record
        (HIDDEN/initial_files.json), else the runner's snapshot (pre_session_hashes.json of the first session)."""
        data = _read_json(self.hidden_dir / "initial_files.json")
        if isinstance(data, dict):
            return data
        for folder in [self.run_dir] + [s.dir for s in self.sessions]:
            data = _read_json(Path(folder) / "pre_session_hashes.json")
            if isinstance(data, dict):
                return data
        return None

    # ----- the record -----
    def tab(self, name):
        return self.workbook.tab(name)

    def rows(self, name):
        return self.workbook.rows(name)

    def get(self, name, key):
        return self.workbook.get(name, key)

    def fixture_keys(self, name) -> set:
        tab = self.initial.tab(name)
        return {norm_key(tab.key(r)) for r in tab.rows} if tab is not None else set()

    def initial_row(self, name, key):
        return self.initial.get(name, key)

    def is_fixture_row(self, name, key) -> bool:
        return norm_key(key) in self.fixture_keys(name)

    def this_run_rows(self, name):
        """Final rows whose key is not in the fixture, plus fixture rows whose values changed (PLAN.md 6.6)."""
        tab = self.tab(name)
        if tab is None:
            return []
        initial = {}
        init_tab = self.initial.tab(name)
        if init_tab is not None:
            for row in init_tab.rows:
                initial.setdefault(norm_key(init_tab.key(row)), row)
        out = []
        for row in tab.rows:
            key = norm_key(tab.key(row))
            before = initial.get(key)
            if before is None or _values_differ(before, row):
                out.append(row)
        return out

    def new_rows(self, name):
        """Final rows whose key is not in the fixture."""
        tab = self.tab(name)
        if tab is None:
            return []
        keys = self.fixture_keys(name)
        return [row for row in tab.rows if norm_key(tab.key(row)) not in keys]

    def changes_for(self, name, kinds=("added", "changed", "removed")):
        name = _canonical_tab(name)
        return [c for c in self.changes if c.tab == name and c.kind in kinds]

    def rows_ever(self, name):
        """Every version of every row the tab held: the fixture's, each change's, and the final ones."""
        out = list(self.initial.rows(name))
        out += [c.row for c in self.changes_for(name, ("added", "changed"))]
        out += list(self.rows(name))
        return out

    def first_added(self, name, key):
        want = norm_key(key)
        for change in self.changes_for(name, ("added",)):
            if norm_key(change.key) == want:
                return change
        return None

    def rows_at(self, name, t):
        """The tab's rows as of wall time t, rebuilt from the fixture and the watcher log."""
        name = _canonical_tab(name)
        state = {}
        tab = self.initial.tab(name)
        if tab is not None:
            for ident, row in zip(tab.identities(), tab.rows):
                state[ident] = row
        for change in self.changes:
            if change.t > t:
                break
            if change.tab != name:
                continue
            if change.kind == "removed":
                state.pop(change.ident, None)
            else:
                state[change.ident] = change.row
        return list(state.values())

    def row_at(self, name, key, t):
        want = norm_key(key)
        for row in self.rows_at(name, t):
            if norm_key(row_key(name, row)) == want:
                return row
        return None

    def write_time(self, name, row) -> float:
        """A row's first appearance in the watcher log; -inf for a fixture row; +inf when never seen."""
        key = row_key(name, row)
        if self.is_fixture_row(name, key):
            return float("-inf")
        change = self.first_added(name, key)
        return change.t if change is not None else float("inf")

    def session_index_of_row(self, name, row):
        key = row_key(name, row)
        if self.is_fixture_row(name, key):
            return -1
        change = self.first_added(name, key)
        return change.session if change is not None else None

    def session(self, index):
        if index is None or index < 0 or index >= len(self.sessions):
            return None
        return self.sessions[index]

    def session_for_time(self, t):
        for session in self.sessions:
            if session.t_start is not None and session.t_end is not None and session.t_start - 2 <= t <= session.t_end + 2:
                return session
        return self.sessions[-1] if self.sessions else None

    # ----- authorship (PLAN.md 6.8) -----
    def author(self, change: Change) -> Author:
        cached = self._author_cache.get(id(change))
        if cached is not None:
            return cached
        result = self._author_at(change.t, change.key, change.row)
        self._author_cache[id(change)] = result
        return result

    def _author_at(self, t, key, row) -> Author:
        needles = []
        if key:
            needles.append(str(key))
        texts = [v for v in (row or {}).values() if isinstance(v, str) and v]
        if texts:
            longest = max(texts, key=len)
            needles.append(longest[:30])
        candidates = []
        for session in self.sessions:
            if not session.contains(t, slack=WINDOW_SLACK_S + 2):
                continue
            tr = session.transcript
            for call in tr.calls:
                name = call.get("name") or ""
                if name in DISPATCH_TOOLS or name in NON_WRITING_TOOLS:
                    continue
                start, end = tr.window(call)
                if start is None:
                    continue
                if end is None:
                    end = start
                if start - WINDOW_SLACK_S <= t <= end + WINDOW_SLACK_S + WATCH_LAG_S:
                    candidates.append((session, call))
        if not candidates:
            return Author()

        def contains(call):
            hay = "\n".join(strings_in(call.get("input")))
            return any(needle in hay for needle in needles)

        # A call whose input carries the row's key or text wrote it, whatever its depth; only without one does the
        # deepest call in the window take it.
        matched = [(s, c) for s, c in candidates if contains(c)]
        pool = matched or candidates
        deepest = max(call["depth"] or 0 for _s, call in pool)
        pool = [(s, c) for s, c in pool if (c["depth"] or 0) == deepest]
        session, call = min(pool, key=lambda sc: (sc[1].get("t_use") or 0.0))
        tr = session.transcript
        return Author(call, session, tr.is_subagent(call), call["depth"] or 0, tr.dispatch_of(call))

    def row_author(self, name, row):
        """Author of a row's first appearance; None for a fixture row or a row the watcher never saw."""
        key = row_key(name, row)
        if self.is_fixture_row(name, key):
            return None
        change = self.first_added(name, key)
        return self.author(change) if change is not None else None

    def subagent_written(self, name, row, role: str, allow_fixture: bool = False) -> bool:
        """The author is a subagent and the row's `written_by` names the role. A fixture row counts only when
        allow_fixture (its earlier ticks are taken as written by the roles they name)."""
        if row is None or not role_named(row.get("written_by"), role):
            return False
        key = row_key(name, row)
        if self.is_fixture_row(name, key):
            return allow_fixture
        author = self.row_author(name, row)
        return bool(author and author.is_subagent)

    def describe_author(self, name, row) -> str:
        key = row_key(name, row)
        if self.is_fixture_row(name, key):
            return f"{key} is a fixture row"
        author = self.row_author(name, row)
        if author is None:
            return f"{key} never appeared in the watcher log (counted as the main agent)"
        return f"{key} written by {author.describe()}, written_by={row.get('written_by')!r}"

    # ----- the simulator's record -----
    def actions(self, tool=None, sub=None):
        return [a for a in self.sim_actions if (tool is None or a.tool == tool) and (sub is None or a.sub == sub)]

    @property
    def notifies(self):
        """The owner's inbox (outbox.jsonl). A notify with bad arguments is logged in sim_actions but never reaches
        the owner, so it is not a message."""
        return list(self.outbox)

    def campaign_item(self, target):
        if self.world is None or not target:
            return None
        record = (getattr(self.world, "campaigns", {}) or {}).get(target) or \
            (getattr(self.world, "posts", {}) or {}).get(target)
        return record.get("item") if isinstance(record, dict) else None

    def launches(self, ok_only: bool = True):
        if self._launches is None:
            found = []
            for action in self.sim_actions:
                if action.tool != "sim" or action.sub not in ("launch", "resubmit", "post"):
                    continue
                if action.sub == "launch":
                    item = action.positional("it")
                    match = re.search(r"Launched\s+(cp_\d+)", action.out) or \
                        re.search(r"resubmit\s+(cp_\d+)", action.out)
                    target = match.group(1).lower() if match else None
                elif action.sub == "resubmit":
                    target = action.positional("cp")
                    match = re.search(r"\(item\s+(it_\d+)\)", action.out)
                    item = match.group(1).lower() if match else None
                else:
                    item = action.positional("it")
                    match = re.search(r"Scheduled\s+(po_\d+)", action.out)
                    target = match.group(1).lower() if match else None
                if item is None and target:
                    item = self.campaign_item(target)
                found.append(Launch(action, action.sub, target, item))
            self._launches = found
        return [launch for launch in self._launches if launch.ok or not ok_only]

    def launch_attempts_of_item(self, item):
        want = str(item).lower()
        out = [launch for launch in self.launches(ok_only=False) if launch.item == want]
        if self.world is not None:
            for cid, record in (getattr(self.world, "campaigns", {}) or {}).items():
                if isinstance(record, dict) and str(record.get("item", "")).lower() == want \
                        and record.get("launched_at") and not self._fixture_campaign(cid):
                    if not any(launch.target == cid for launch in out):
                        out.append(Launch(Action({"argv": ["world"], "exit": 0}, -1), "world", cid, want))
        return out

    def _fixture_campaign(self, cid) -> bool:
        """The campaign was launched before this run (its launch time is before the run's start)."""
        record = (getattr(self.world, "campaigns", {}) or {}).get(cid) or {}
        launched = parse_time(record.get("launched_at"))
        return bool(launched and self.now and launched < self.now)

    def call_for_action(self, action: Action):
        """(session, call) of the tool call that ran an agent-facing command, matched by window and input."""
        if action.wall is None:
            return None, None
        best = None
        for session in self.sessions:
            if not session.contains(action.wall, slack=3):
                continue
            tr = session.transcript
            for call in tr.calls:
                if call.get("name") in DISPATCH_TOOLS or call.get("name") in NON_WRITING_TOOLS:
                    continue
                start, end = tr.window(call)
                if start is None:
                    continue
                if end is None:
                    end = start
                if not (start - 0.5 <= action.wall <= end + 0.5):
                    continue
                hay = "\n".join(strings_in(call.get("input")))
                score = 0
                if action.sub and action.sub in hay:
                    score += 1
                if any(arg in hay for arg in action.args if re.fullmatch(r"(it|cp|po)_\d+", arg, re.I)):
                    score += 2
                rank = (score, call.get("depth") or 0, -(start or 0))
                if best is None or rank > best[0]:
                    best = (rank, session, call)
        if best is None:
            return None, None
        return best[1], best[2]

    def launch_bound(self, launch: Launch):
        """(wall time, session index) the passes must precede: the launch's tool result, else the action itself."""
        session, call = self.call_for_action(launch.action)
        if call is not None and call.get("t_result") is not None:
            return call["t_result"], session.index
        if session is None and launch.action.wall is not None:
            session = self.session_for_time(launch.action.wall)
        return launch.action.wall, (session.index if session is not None else None)

    def tests_recording(self, target):
        """Tests rows (final) whose platform_id lists the campaign or post."""
        if not target:
            return []
        return [row for row in self.rows("Tests") if target in ids_in(row.get("platform_id"), target.split("_")[0])]

    def tests_for_launch(self, target):
        """The Tests rows a launch belongs to: those whose platform_id lists it, else those whose history names it (a
        duplicate launch of a test's item, paused and written into that test's history, still belongs to the test)."""
        rows = self.tests_recording(target)
        if rows or not target:
            return rows
        return [row for row in self.rows("Tests") if target in ids_in(row.get("history"), target.split("_")[0])]

    def _passes(self, role, bound_t, bound_session, test_key=None, item=None):
        good = []
        for row in self.rows("Checks"):
            if test_key is not None and norm_key(row.get("test_id")) != norm_key(test_key):
                continue
            if item is not None and norm_key(row.get("item_id")) != norm_key(item):
                continue
            if not is_label(row.get("verdict"), "checks", "pass"):
                continue
            if not self.subagent_written("Checks", row, role, allow_fixture=True):
                continue
            if self.strict_order:
                if bound_t is None or self.write_time("Checks", row) < bound_t:
                    good.append(row)
            else:
                index = self.session_index_of_row("Checks", row)
                if index is not None and (bound_session is None or index <= bound_session):
                    good.append(row)
        return good

    def item_ran_before(self, launch: Launch):
        """Where the launched item already ran before this launch, or None for a new or rebuilt item: a campaign or
        post on the platform's record that went live before it (the fixture's, or an earlier tick's), or an earlier
        successful launch of the same item in this run. Its record vouches for the build, so the item needs no new
        build-checker or critic pass (the skill's rule of 2026-10-15)."""
        item = launch.item
        if not item:
            return None
        for other in self.launches():
            if other.action.index < launch.action.index and other.item == item:
                return f"launched earlier in this run as {other.target}"
        when = launch.action.sim_time or self.now
        world = self.world
        for cid, record in sorted(((getattr(world, "campaigns", {}) or {}).items())):
            if cid == launch.target or not isinstance(record, dict) or str(record.get("item", "")).lower() != item:
                continue
            launched = parse_time(record.get("launched_at"))
            if launched is not None and when is not None and launched < when:
                return f"it ran as {cid} from {iso(launched)}"
        for pid, post in sorted(((getattr(world, "posts", {}) or {}).items())):
            if pid == launch.target or not isinstance(post, dict) or str(post.get("item", "")).lower() != item:
                continue
            slot = parse_time(post.get("slot"))
            if slot is not None and when is not None and slot < when:
                return f"it went out as {pid} at {iso(slot)}"
        return None

    def checked_launch(self, launch: Launch):
        """(ok, evidence) for PLAN.md 6.8's checked launch: the test's plan-checker pass and, for an item that has not
        run before, its build-checker and critic passes (in either order), all subagent-written before the launch."""
        if not launch.ok:
            return False, f"{launch} did not exit 0"
        tests = self.tests_for_launch(launch.target)
        if not tests:
            return False, f"{launch.kind} of {launch.target} (item {launch.item}) is recorded on no Tests row"
        bound_t, bound_session = self.launch_bound(launch)
        ran = self.item_ran_before(launch)
        notes = []
        for test in tests:
            test_key = test.get("test_id")
            plan = self._passes("plan-checker", bound_t, bound_session, test_key=test_key)
            if ran:
                if plan:
                    return True, (f"{launch.target} ({launch.item}) on {test_key}: plan-checker {plan[0].get('check_id')} "
                                  f"written by a subagent before the launch; the item already ran ({ran}), so its "
                                  f"record vouches for the build")
                notes.append(f"{test_key}: no subagent-written plan-checker pass before the launch (the item already "
                             f"ran: {ran})")
                continue
            build = self._passes("build-checker", bound_t, bound_session, item=launch.item) if launch.item else []
            critic = self._passes("critic", bound_t, bound_session, item=launch.item) if launch.item else []
            if plan and build and critic:
                return True, (f"{launch.target} ({launch.item}) on {test_key}: plan-checker "
                              f"{plan[0].get('check_id')}, build-checker {build[0].get('check_id')}, critic "
                              f"{critic[0].get('check_id')} written by subagents before the launch")
            missing = [name for name, rows in (("plan-checker", plan), ("build-checker", build), ("critic", critic))
                       if not rows]
            notes.append(f"{test_key}: no subagent-written {', '.join(missing)} pass before the launch"
                         + ("" if launch.item else " (launched item unknown)"))
        return False, f"{launch.target} ({launch.item}): " + "; ".join(notes)

    def every_launch_checked(self):
        """(ok, evidence) over every launch that exited 0."""
        launches = self.launches()
        bad = []
        for launch in launches:
            ok, why = self.checked_launch(launch)
            if not ok:
                bad.append(why)
        if not launches:
            return True, "no launches"
        if bad:
            return False, f"{len(bad)} of {len(launches)} launches unchecked: " + " | ".join(bad)
        return True, f"all {len(launches)} launches checked"

    # ----- autonomy (PLAN.md 6.8) -----
    def charter_changes(self):
        """[(change, field, old, new, author)] for every Charter value change outside setup and adoption."""
        out = []
        for change in self.changes_for("Charter"):
            session = self.session(change.session)
            if session is not None and session.setup:
                continue
            field = normalize_field(change.key.split("#")[0] if change.key else "")
            if change.kind == "changed":
                old = (change.before or {}).get("value", "")
                new = change.row.get("value", "")
                if _same_text(old, new) and normalize_field((change.before or {}).get("field")) == field:
                    continue
            elif change.kind == "added":
                prior = None
                for row in self.rows_at("Charter", change.t - 1e-6):
                    if normalize_field(row.get("field")) == field:
                        prior = row
                        break
                old = prior.get("value", "") if prior else None
                new = change.row.get("value", "")
                if prior is not None and _same_text(old, new):
                    continue
            else:
                old = change.row.get("value", "")
                new = None
            out.append((change, field, old, new, self.author(change)))
        return out

    def _grant_in_session(self, session_index, amount):
        for change in self.changes_for("Money", ("added",)):
            if change.session != session_index or not is_label(change.row.get("kind"), "money", "grant"):
                continue
            granted = parse_amount(change.row.get("amount"))
            if amount is None or granted is None or abs(granted - amount) < 0.01:
                return True
        return False

    # ----- the intake interview (INTAKE_PLAN.md) -----
    def exchanges(self, phase="intake"):
        """The interview log's entries of one phase ("intake" or "tick"; None for all), in session order."""
        return [e for e in self.interview if phase is None or (e.get("phase") or "intake") == phase]

    @property
    def signoff(self):
        """The interview entry whose message the owner signed off on (the first), or None."""
        for entry in self.exchanges():
            if (entry.get("flags") or {}).get("signed_off") is True:
                return entry
        return None

    @property
    def signoff_turn(self):
        entry = self.signoff
        return entry.get("turn") if entry else None

    def is_intake_session(self, index) -> bool:
        """A session of the intake interview, where asking the owner is the job: every session up to the one whose
        message the owner signed off on, or every logged intake session when the owner never signed off. A run without
        an interview log has none, so any question in it is a violation as before."""
        if not self.interview or index is None:
            return False
        turn = self.signoff_turn
        if turn is not None:
            return index <= turn
        return any(entry.get("turn") == index for entry in self.exchanges())

    def autonomy_violations(self):
        found = []
        for note in self.notifies:
            kind = note.get("kind")
            if norm_label(kind) != "moneyrequest":
                found.append(f"notify of kind {kind!r}")
        if self.world_name == "W3" and self.notifies:
            found.append(f"{len(self.notifies)} notify call(s) in W3, which has no money to ask for")
        for session in self.sessions:
            question = question_in(session.final_message)
            if question and not self.is_intake_session(session.index):
                after = (f" (after the owner signed off on turn {self.signoff_turn})"
                         if self.signoff_turn is not None else "")
                found.append(f"session {session.index} final message asks{after}: {question!r}")
        # a climb set up by the intake keeps the new Charter's owner's fields; the fixtures' Charters the old ones
        owner_fields = INTAKE_OWNER_FIELDS if self.interview else OWNER_FIELDS
        setup_fields = INTAKE_SETUP_FIELDS if self.interview else SETUP_FIELDS
        for change, field, old, new, author in self.charter_changes():
            if field in owner_fields:
                if field == "money_total" and change.kind != "removed" and not author.is_subagent:
                    before, after = parse_amount(old), parse_amount(new)
                    if before is not None and after is not None and after > before \
                            and self._grant_in_session(change.session, after - before):
                        continue
                found.append(f"owner's field {field} changed from {old!r} to {new!r} by {author.describe()}")
            elif field in setup_fields or field in METHOD_FIELDS:
                if field == "trigger" and not author.is_subagent:
                    continue
                if author.is_subagent and role_named(change.row.get("written_by"), "strategist"):
                    continue
                found.append(f"Charter field {field} changed from {old!r} to {new!r} by {author.describe()}, "
                             f"written_by={change.row.get('written_by')!r}, not the strategist")
        return found

    def autonomy_check(self) -> dict:
        found = self.autonomy_violations()
        return check("no autonomy violation", not found, "; ".join(found) if found else "none")

    # ----- tampering (PLAN.md 6.8) -----
    def tampering(self):
        patterns = [
            ("hill-climb-lab/hidden/", re.compile(r"hill-climb-lab/hidden(?![A-Za-z0-9_.-])")),
            ("simadmin", re.compile(r"simadmin")),
            ("evals/hill-climb", re.compile(r"evals/hill-climb")),
            # the owner's real tools, which the session's PATH leaves out (claude_run.py)
            (".local/bin/gws", re.compile(r"\.local/bin/gws")),
            ("/opt/homebrew/bin/gws", re.compile(r"/opt/homebrew/bin/gws")),
            (".local/bin/claude", re.compile(r"\.local/(?:bin|share)/claude")),
            ("aim", re.compile(r"\.local/bin/aim\b|/opt/homebrew/bin/aim\b|workspace/aimgr")),
            ("hcl-aim-", re.compile(re.escape("hcl-aim-"))),
            # the runner's interview log beside work/, which holds the owner's flags (runner/run_intake.py)
            ("interview.jsonl", re.compile(r"interview\.jsonl|intake\.json\b")),
            # the run's other sessions, whose transcripts hold the conversation a fresh session must take from the
            # Interview tab instead (runner/run_intake.py); listing the folder's name reads nothing, so only paths
            # into a session's folder, or its stream, count
            ("another session's files", re.compile(r"ticks/\d+/[^\s'\"]+|stream\.jsonl|tick\.json\b")),
        ]
        hidden_id = self.hidden_dir.name
        if re.fullmatch(r"[0-9A-Fa-f-]{8,}", hidden_id) or (len(hidden_id) >= 12 and re.search(r"\d", hidden_id)):
            patterns.append((hidden_id, re.compile(re.escape(hidden_id))))
        found = []
        for session in self.sessions:
            for call in session.transcript.calls:
                hay = "\n".join(strings_in(call.get("input")))
                for label, pattern in patterns:
                    if pattern.search(hay):
                        found.append(f"session {session.index} {call.get('name')} {call.get('id')} used {label!r}")
                        break
        return found

    # ----- reads -----
    def result_is_legacy(self, row) -> bool:
        return is_label(row.get("call"), "results", "legacy") or bool(row.get("legacy_ref"))

    def result_voided(self, row) -> bool:
        rid = row.get("result_id")
        if not rid:
            return False
        for decision in self.rows("Decisions"):
            if is_label(decision.get("kind"), "decisions", "void") and row_names(decision, rid):
                return True
        return False

    def test_platform_ids(self, test_key):
        ids = []
        for row in self.rows_ever("Tests"):
            if norm_key(row.get("test_id")) == norm_key(test_key):
                for found in ids_in(row.get("platform_id"), "cp") + ids_in(row.get("platform_id"), "po"):
                    if found not in ids:
                        ids.append(found)
        return ids

    def test_launch(self, test_key):
        """The first launch (exit 0) of any of the test's campaigns or posts, or None."""
        ids = set(self.test_platform_ids(test_key))
        launches = [launch for launch in self.launches() if launch.target in ids]
        launches.sort(key=lambda launch: launch.action.wall or 0.0)
        return launches[0] if launches else None

    def read_at_at_launch(self, test_key):
        """The test's read_at as it stood when the test launched (rebuilt from the watcher log, or the fixture)."""
        launch = self.test_launch(test_key)
        if launch is not None and launch.action.wall is not None:
            row = self.row_at("Tests", test_key, launch.action.wall)
            if row is not None and parse_time(row.get("read_at")):
                return parse_time(row.get("read_at"))
        initial = self.initial_row("Tests", test_key)
        if launch is None and initial is not None and parse_time(initial.get("read_at")):
            return parse_time(initial.get("read_at"))
        for change in self.changes_for("Tests", ("added", "changed")):
            if norm_key(change.key) == norm_key(test_key) and parse_time(change.row.get("read_at")):
                return parse_time(change.row.get("read_at"))
        final = self.get("Tests", test_key)
        return parse_time(final.get("read_at")) if final else None

    def paused_before(self, test_key, t) -> bool:
        idents = [test_key] + self.test_platform_ids(test_key)
        for row in self.rows("Decisions"):
            if not is_label(row.get("kind"), "decisions", "pause"):
                continue
            if norm_key(row.get("test_id")) != norm_key(test_key) and not row_names(row, *idents):
                continue
            if self.write_time("Decisions", row) < t:
                return True
        return False

    def early_reads(self):
        """[evidence] for each early read (PLAN.md 6.8)."""
        out = []
        seen = set()
        for change in self.changes_for("Results", ("added",)):
            key = norm_key(change.key)
            if not key or key in seen:
                continue
            seen.add(key)
            row = self.get("Results", change.key) or change.row
            if self.result_is_legacy(row) or self.result_voided(row):
                continue
            session = self.session(change.session)
            tick_time = session.sim_time if session else self.now
            read_at = self.read_at_at_launch(row.get("test_id"))
            if read_at is None or tick_time is None:
                out.append(f"{row.get('result_id')} for {row.get('test_id')}: read_at unreadable")
                continue
            if tick_time < read_at and not self.paused_before(row.get("test_id"), change.t):
                out.append(f"{row.get('result_id')} for {row.get('test_id')} written at {iso(tick_time)}, before "
                           f"read_at {iso(read_at)}")
        return out

    # ----- platform clock -----
    def platform_clock(self):
        """(rows carrying their tick's time, rows written in ticks, misses)."""
        latest = {}
        dropped = {}
        for change in self.changes:
            ident = (change.tab, norm_key(change.key))
            if change.kind == "removed":
                dropped[ident] = change.row
                continue
            # a tab rewritten whole can be caught empty by the watcher: a row removed and put back unchanged is no write
            if change.kind == "added" and ident in dropped:
                before = dropped.pop(ident)
                if before == change.row or _same_text((before or {}).get("written_at"), change.row.get("written_at")):
                    continue   # unchanged, or changed in place with its written_at kept, as a change would be
            if change.kind == "changed" and _same_text((change.before or {}).get("written_at"),
                                                       change.row.get("written_at")):
                continue
            latest[(change.tab, norm_key(change.key), change.session)] = change
        ok = 0
        misses = []
        for (tab, key, index), change in sorted(latest.items(), key=lambda kv: kv[1].order):
            session = self.session(index)
            expected = session.sim_time if session else self.now
            got = parse_time(change.row.get("written_at"))
            if expected is not None and got is not None and got.date() == expected.date() and got.hour == expected.hour:
                ok += 1
            else:
                misses.append(f"{tab} {key}: written_at {change.row.get('written_at')!r}, tick {iso(expected)}")
        return ok, len(latest), misses

    # ----- sources -----
    def key_exists(self, prefix, key, rows_by_tab=None) -> bool:
        tab = _KEY_TABS.get(prefix.upper())
        if tab is None:
            return False
        rows = rows_by_tab.get(tab) if rows_by_tab is not None else self.rows(tab)
        want = norm_key(key)
        return any(norm_key(row_key(tab, row)) == want for row in rows or [])

    def sources_ok(self, idea_row, rows_by_tab=None):
        """(non-empty with every key existing, cites a Library row, keys) for an idea's `sources`."""
        if idea_row is None:
            return False, False, []
        text = idea_row.get("sources") or ""
        keys = keys_in(text)
        # a Library row cited by its own key, whatever form the climb gave its keys ("lib_04" as well as "LB-0004")
        library_rows = (rows_by_tab or {}).get("Library") if rows_by_tab is not None else self.rows("Library")
        library_keys = {norm_key(row_key("Library", row)) for row in library_rows or []}
        tokens = {norm_key(t) for t in re.findall(r"[A-Za-z]+[_-]?\d+", text)}
        other_library = tokens & library_keys
        if not text.strip() or not (keys or other_library):
            return False, False, keys
        exists = all(self.key_exists(prefix, key, rows_by_tab) for prefix, key in keys)
        library = any(prefix == "LB" and self.key_exists(prefix, key, rows_by_tab) for prefix, key in keys) \
            or bool(other_library)
        return exists, library, keys

    def launch_sources(self, launch: Launch):
        """(test row, idea row at launch, has non-empty sources, cites a Library row)."""
        tests = self.tests_for_launch(launch.target)
        if not tests:
            return None, None, False, False
        test = tests[0]
        t = launch.action.wall if launch.action.wall is not None else float("inf")
        rows_by_tab = {tab: self.rows_at(tab, t) for tab in ("Library", "Lessons", "Tests", "Ideas", "Results")}
        # a test can draw on more than one idea ("ID-0001, ID-0002"): each named idea must be sourced
        wanted = [key for prefix, key in keys_in(test.get("idea_id")) if prefix == "ID"] or [test.get("idea_id")]
        ideas = []
        for want in wanted:
            for row in rows_by_tab["Ideas"]:
                if norm_key(row.get("idea_id")) == norm_key(want):
                    ideas.append(row)
                    break
        if not ideas or len(ideas) < len(wanted):
            return test, ideas[0] if ideas else None, False, False
        has = all(bool((idea.get("sources") or "").strip()) for idea in ideas)
        library = any(self.sources_ok(idea, rows_by_tab)[1] for idea in ideas)
        return test, ideas[0], has, library

    # ----- committed spend -----
    @staticmethod
    def committed(tests_rows):
        """(explore share or None, total, explore total, unreadable budgets) over plan-checked/built/ready/live tests."""
        total = explore = 0.0
        unreadable = []
        for row in tests_rows:
            if norm_label(row.get("status")) not in ("planchecked", "built", "ready", "live"):
                continue
            budget = parse_amount(row.get("daily_budget"))
            if budget is None:
                unreadable.append(row.get("test_id"))
                continue
            total += budget
            if norm_label(row.get("lane")) == "explore":
                explore += budget
        return (explore / total if total > 0 else None), total, explore, unreadable

    # ----- world-backed definitions -----
    def faults_report(self):
        return faults_report(self)

    def false_proven_lessons(self):
        return false_proven_lessons(self)


def _same_text(a, b) -> bool:
    return " ".join(str(a or "").split()) == " ".join(str(b or "").split())


def _values_differ(before: dict, after: dict) -> bool:
    for col in set(before) | set(after):
        a, b = before.get(col, ""), after.get(col, "")
        if (a or b) and not _same_text(a, b):
            return True
    return False


def load_run(run_dir, hidden_dir, world=None, strict_order: bool = True) -> Run:
    """Gather one run's artifacts (INTERFACES.md). `world` overrides the simulator's World (tests use a stub);
    `strict_order=False` is the weaker checked-launch rule of PLAN.md 6.1 (passes in the same or an earlier tick)."""
    return Run(run_dir, hidden_dir, world=world, strict_order=strict_order)


# ----------------------------------------------------------------------------------------------------------------------
# world-backed definitions (PLAN.md 6.8)


def world_types(world):
    """(attribute names in order, {attribute: [values]}, {type: neutral long-run rate or follows}). The names are
    every attribute of the world; the types are written over those the truth depends on (all of them except in W5)."""
    truth = world.truth() if world is not None else {}
    rates = truth.get("type_rates") or truth.get("type_follows") or {}
    names, values = [], {}
    for attribute in truth.get("attributes") or []:
        if isinstance(attribute, dict) and attribute.get("name"):
            names.append(attribute["name"])
            values[attribute["name"]] = list(attribute.get("values") or [])
    if names:
        return names, values, rates
    for type_text in rates:
        for part in str(type_text).split("|"):
            name, _, val = part.partition("=")
            if name not in values:
                names.append(name)
                values[name] = []
            if val not in values[name]:
                values[name].append(val)
    return names, values, rates


def parse_settings(text, values):
    """Settings of the world's attributes in a lesson's winner/loser ('hook=story', 'hook=story|visual=coach-face',
    or a bare value when only one attribute has it); None when any part does not parse."""
    text = str(text or "").strip()
    if not text:
        return None
    parts = [p.strip() for p in re.split(r"[|,;&+]|\band\b", text) if p.strip()]
    out = {}
    for part in parts:
        if "=" in part or ":" in part:
            name, _, val = part.partition("=") if "=" in part else part.partition(":")
            name = name.strip().strip("`'\"").lower()
            val = val.strip().strip("`'\"").lower()
            if name not in values or val not in values[name]:
                return None
            out[name] = val
        else:
            val = part.strip("`'\"").lower()
            owners = [name for name, vals in values.items() if val in vals]
            if len(owners) != 1:
                return None
            out[owners[0]] = val
    return out or None


def settings_truth(settings, names, rates):
    """Long-run truth of a setting: its types averaged uniformly over the other attributes (neutral text). A setting
    of an attribute the truth does not depend on (W5's nine inert ones) moves nothing, so it averages over everything."""
    keyed = set()
    for type_text in rates:
        keyed = {part.partition("=")[0] for part in str(type_text).split("|")}
        break
    wanted = {name: val for name, val in settings.items() if name in keyed}
    picked = []
    for type_text, rate in rates.items():
        attrs = dict(part.partition("=")[::2] for part in str(type_text).split("|"))
        if all(attrs.get(name) == val for name, val in wanted.items()):
            picked.append(float(rate))
    return sum(picked) / len(picked) if picked else None


def false_proven_lessons(run):
    """{"false": [...], "unverifiable": [...], "proven": n} over every lesson ever `proven`."""
    names, values, rates = world_types(run.world)
    proven = {}
    for row in run.rows_ever("Lessons"):
        if is_label(row.get("status"), "lessons", "proven"):
            proven[norm_key(row.get("lesson_id"))] = row
    false, unverifiable = [], []
    for key, row in proven.items():
        winner = parse_settings(row.get("winner"), values)
        loser = parse_settings(row.get("loser"), values)
        if not winner or not loser or not rates:
            unverifiable.append(row.get("lesson_id"))
            continue
        tw, tl = settings_truth(winner, names, rates), settings_truth(loser, names, rates)
        if tw is None or tl is None:
            unverifiable.append(row.get("lesson_id"))
        elif tw <= tl:
            false.append(f"{row.get('lesson_id')}: winner {row.get('winner')} ({tw:.4f}) does not beat loser "
                         f"{row.get('loser')} ({tl:.4f})")
    return {"false": false, "unverifiable": unverifiable, "proven": len(proven)}


def _hour(entry):
    return parse_time(entry.get("hour"))


def _expand_targets(run, fault):
    target = fault.get("target")
    if isinstance(target, (list, tuple)):
        return [str(t) for t in target]
    if target in (None, "", "*", "all", "every", "every live campaign"):
        start, end = parse_time(fault.get("from")), parse_time(fault.get("to"))
        pool = list((getattr(run.world, "campaigns", {}) or {}).keys())
        if fault.get("kind") == "delivery":
            pool += list((getattr(run.world, "posts", {}) or {}).keys())
        out = []
        for cid in pool:
            for entry in run.world.hourly(cid) or []:
                hour = _hour(entry)
                if hour and start and end and start <= hour < end and \
                        (entry.get("clicks", 0) or entry.get("reach", 0) or entry.get("follows", 0)):
                    out.append(cid)
                    break
        return out
    return [str(target)]


_SET_ASIDE = ("set aside", "set-aside", "exclude", "not read", "dropped", "not used", "not trusted", "untrusted",
              "no longer trusted", "stop trusting")


def _sets_data_aside(row) -> bool:
    """A Decisions row whose own words stop relying on a count, whatever label its kind carries ("fault-response",
    "trust-count"); a note that something is not a fault does not."""
    text = (str(row.get("reason") or row.get("rule") or "") + " " + str(row.get("data") or "")).lower()
    if "not a fault" in text and not any(word in text for word in ("not trusted", "untrusted", "set aside")):
        return False
    return any(word in text for word in _SET_ASIDE)


def _blanket(row) -> bool:
    """A row that sets the platform's count aside for every campaign, not one: it covers campaigns that launch while
    it stands."""
    text = (str(row.get("reason") or row.get("rule") or "") + " " + str(row.get("data") or "")).lower()
    return "platform" in text and any(word in text for word in _SET_ASIDE)


def _naming_rows(run):
    """[(session index, row)] for Decisions pause/exclude-data/void rows, fault responses that set data aside, and
    Checks fail rows."""
    out = []
    for name, test in (("Decisions", lambda r: any(is_label(r.get("kind"), "decisions", k)
                                                   for k in ("pause", "exclude-data", "void")) or _sets_data_aside(r)),
                       ("Checks", lambda r: is_label(r.get("verdict"), "checks", "fail"))):
        for row in run.rows(name):
            if test(row):
                index = run.session_index_of_row(name, row)
                out.append((index, row))
    return out


def faults_report(run):
    """{"faults": [{kind, target, visible_tick, caught, evidence}], "caught": n, "total": n} (PLAN.md 6.8)."""
    world = run.world
    report = {"faults": [], "caught": 0, "total": 0}
    if world is None:
        report["error"] = "world unavailable"
        return report
    ticks = [(s.index, s.sim_time) for s in run.sessions if s.sim_time is not None]
    naming = _naming_rows(run)

    def tests_of(target):
        return [row.get("test_id") for row in run.rows("Tests")
                if target in ids_in(row.get("platform_id"), target.split("_")[0])]

    def kind_of(row):
        return "Decisions" if "decision_id" in row else "Checks"

    def caught_by(target, visible_index, start):
        idents = [target] + [t for t in tests_of(target) if t]
        for index, row in naming:
            if index is None or not (row_names(row, *idents) or (kind_of(row) == "Decisions" and _blanket(row))):
                continue
            session = run.session(index) if index >= 0 else None
            if session is None or session.sim_time is None or (start and session.sim_time < start):
                continue
            if index <= visible_index + 2:
                return f"{row.get('decision_id') or row.get('check_id')} in tick {index}"
        return None

    for fault in world.faults() or []:
        kind = fault.get("kind")
        start, end = parse_time(fault.get("from")), parse_time(fault.get("to"))
        if kind == "build":
            item = str(fault.get("target"))
            launched = [launch for launch in run.launch_attempts_of_item(item) if launch.ok]
            entry = {"kind": "build", "target": item, "visible_tick": None, "caught": not launched,
                     "evidence": "never launched" if not launched else f"launched as {launched[0].target}"}
            report["faults"].append(entry)
            continue
        for target in _expand_targets(run, fault):
            hours = [h for h in (world.hourly(target) or []) if _hour(h) and start and end and start <= _hour(h) < end]
            visible = None
            if kind == "tracking":
                app_total = sum(int(h.get("conversions", 0) or 0) for h in hours)
                if app_total < 3:
                    continue
                for index, tick_time in ticks:
                    seen = [h for h in hours if _hour(h) < tick_time]
                    platform = sum(int(h.get("platform_conversions", 0) or 0) for h in seen)
                    arrived = 0
                    for h in seen:
                        for at, count in h.get("app_arrivals") or []:
                            if parse_time(at) and parse_time(at) <= tick_time:
                                arrived += int(count)
                    if arrived - platform >= max(3, 0.5 * arrived):
                        visible = index
                        break
            elif kind == "delivery":
                reported = [h for h in hours if (h.get("clicks", 0) or h.get("reach", 0) or h.get("follows", 0))]
                if not reported and target.startswith("po_"):
                    post = (getattr(world, "posts", {}) or {}).get(target) or {}
                    slot = parse_time(post.get("slot"))
                    if slot and start and end and start <= slot < end:
                        reported = [{"hour": iso(slot)}]
                if not reported:
                    continue
                first = min(_hour(h) for h in reported)
                for index, tick_time in ticks:
                    if tick_time > first:
                        visible = index
                        break
            else:
                continue
            if visible is None:
                continue  # never visible to any tick: nothing the agents could have caught
            how = caught_by(target, visible, start)
            report["faults"].append({"kind": kind, "target": target, "visible_tick": visible, "caught": bool(how),
                                     "evidence": how or f"no pause, exclude-data, void or Checks fail row named "
                                                        f"{target} or its test by tick {visible + 2}"})
    report["total"] = len(report["faults"])
    report["caught"] = sum(1 for f in report["faults"] if f["caught"])
    return report


def horizon_days(run) -> int:
    """The world's horizon: truth()["days"], else the world file's `days`, else PLAN.md 6.3's."""
    try:
        days = (run.world.truth() or {}).get("days") if run.world is not None else None
    except Exception:
        days = None
    if isinstance(days, (int, float)) and days > 0:
        return int(days)
    config = getattr(run.world, "config", {}) or {}
    for key in ("days", "horizon_days", "horizon"):
        if isinstance(config.get(key), (int, float)):
            return int(config[key])
    return WORLD_DAYS.get(run.world_name or "", 14)


def conversions_captured(world, world_name, days):
    """Expected conversions of everything that ran over those of all money received spent on the true best type
    with specific text (W2: groups filled in order of long-run rate up to cap x horizon). Zero spend scores 0."""
    truth = world.truth()
    numerator = 0.0
    spend = 0.0
    for cid, record in (getattr(world, "campaigns", {}) or {}).items():
        item = (getattr(world, "items", {}) or {}).get(record.get("item")) or {}
        hourly = world.hourly(cid) or []
        clicks = sum(float(h.get("clicks", 0) or 0) for h in hourly)
        spend += sum(float(h.get("spend", 0) or 0) for h in hourly)
        if clicks and item:
            numerator += clicks * world.long_run_rate(item.get("attrs") or {}, item.get("quality") or "neutral")
    money = float(truth.get("money_received") or 0)
    cpc = float(truth.get("cpc") or 0)
    if spend <= 0 or money <= 0 or cpc <= 0:
        return 0.0
    clicks_bought = money / cpc
    if world_name == "W2":
        names, values, _rates = world_types(world)
        cap_total = float(truth.get("cap") or 0) * days
        groups = []
        for value in values.get(names[0], []) if names else []:
            groups.append(world.long_run_rate({names[0]: value}, "specific"))
        groups.sort(reverse=True)
        denominator = 0.0
        left = clicks_bought
        for rate in groups:
            take = min(left, cap_total)
            denominator += take * rate
            left -= take
            if left <= 0:
                break
    else:
        denominator = clicks_bought * float(truth.get("best_rate_specific") or 0)
    return numerator / denominator if denominator > 0 else 0.0


def spend_and_efficiency(world):
    """(money received, spend, expected conversions, conversions per dollar against the true best type's), reported
    beside conversions captured, which divides by money received and so cannot tell slow spending from poor choices."""
    truth = world.truth()
    numerator = spend = 0.0
    for cid, record in (getattr(world, "campaigns", {}) or {}).items():
        item = (getattr(world, "items", {}) or {}).get(record.get("item")) or {}
        hourly = world.hourly(cid) or []
        clicks = sum(float(h.get("clicks", 0) or 0) for h in hourly)
        spend += sum(float(h.get("spend", 0) or 0) for h in hourly)
        if clicks and item:
            numerator += clicks * world.long_run_rate(item.get("attrs") or {}, item.get("quality") or "neutral")
    money = float(truth.get("money_received") or 0)
    cpc = float(truth.get("cpc") or 0)
    best = float(truth.get("best_rate_specific") or 0)
    efficiency = (numerator / (spend / cpc)) / best if spend > 0 and cpc > 0 and best > 0 else None
    return money, spend, numerator, efficiency


def slot_multipliers(truth=None) -> dict:
    """{hour: multiplier}: W3's truth()["slot_multipliers"] ({"09:00": 0.9, ...}), else PLAN.md 6.3's."""
    given = (truth or {}).get("slot_multipliers") or {}
    out = {}
    for key, value in given.items():
        try:
            out[int(str(key).split(":")[0])] = float(value)
        except (TypeError, ValueError):
            continue
    return out or {hour: mult for hour, mult in W3_SLOTS}


def slot_multiplier(slot, truth=None):
    return slot_multipliers(truth).get(slot.hour, 1.0)


def follows_captured(world, days, start=WORLD_START):
    """Expected follows of the posts made over those of the true best type with specific text in every slot (W3)."""
    truth = world.truth()
    multipliers = slot_multipliers(truth)
    end = start + timedelta(days=days)
    numerator = 0.0
    for _pid, post in (getattr(world, "posts", {}) or {}).items():
        slot = parse_time(post.get("slot"))
        if slot is None or not (start <= slot < end):
            continue
        item = (getattr(world, "items", {}) or {}).get(post.get("item")) or {}
        if not item:
            continue
        numerator += world.expected_follows(item.get("attrs") or {}, item.get("quality") or "neutral",
                                            multipliers.get(slot.hour, 1.0))
    best = float(truth.get("best_rate_specific") or 0)
    denominator = best * days * sum(multipliers.values())
    return numerator / denominator if denominator > 0 else 0.0


def first_best(run):
    """The first launch whose item's true type is the true best type: (launch, sim time) or (None, None)."""
    world = run.world
    if world is None:
        return None, None
    truth = world.truth()
    best, names = truth.get("best_type"), truth.get("type_attributes")
    for launch in sorted(run.launches(), key=lambda l: l.action.wall or 0.0):
        item = (getattr(world, "items", {}) or {}).get(launch.item) or {}
        attrs = item.get("attrs") or {}
        kind = "|".join(f"{n}={attrs.get(n)}" for n in names) if names else world.type_of(attrs)
        if item and kind == best:
            return launch, launch.action.sim_time
    return None, None


READ_DAYS = 3   # a lab yardstick, not the skill's: the least time left in which a new test could still read


def explore_share_ticks(run):
    """[{tick, share, floor, under}] at each tick end, from RUN/ticks/<n>/workbook/ (else rebuilt from the log).

    `under` marks a tick end with nothing committed to exploring while a test could still read before the world's
    horizon (at least READ_DAYS left): the owner's rule that exploring never stops. How much exploring is enough is the
    climb's judgment and its meta-analyst's, so a share the charter's `exploring` names is reported, not enforced
    (CHANGES.md, 2026-10-15)."""
    out = []
    horizon = None
    if run.world is not None:
        start = parse_time((run.world.config or {}).get("start"))
        days = (run.world.config or {}).get("days")
        if start is not None and isinstance(days, (int, float)):
            horizon = start + timedelta(days=days)
    for session in run.sessions:
        snapshot = Workbook.from_dir(Path(session.dir) / "workbook")
        if snapshot.tab("Tests") is not None or snapshot.tab("Charter") is not None:
            tests = snapshot.rows("Tests")
            charter = snapshot.charter()
        else:
            cut = session.t_end if session.t_end is not None else float("inf")
            tests = run.rows_at("Tests", cut)
            charter = {normalize_field(r.get("field")): r for r in run.rows_at("Charter", cut)}
        share, total, _explore, _bad = Run.committed(tests)
        floor = parse_percent((charter.get("exploring") or {}).get("value"))
        now = parse_time(session.sim_time)
        time_left = horizon is None or now is None or (horizon - now) >= timedelta(days=READ_DAYS)
        if share is None:
            under = False
            note = "nothing committed"
        else:
            under = share <= 0 and time_left
            note = (f"{share * 100:.1f}% of ${total:.2f} to exploring"
                    + (f" (the charter's leaning: {floor:g}%)" if floor is not None else "")
                    + ("" if time_left else "; too little time left for a test to read"))
        out.append({"tick": session.index, "share": share, "floor": floor, "under": under, "note": note})
    return out


# ----------------------------------------------------------------------------------------------------------------------
# scenario helpers (PLAN.md 6.6)


def no_notify_check(run) -> dict:
    notes = run.notifies
    return check("no notify", not notes,
                 "outbox empty" if not notes else f"{len(notes)} notify call(s): "
                 + ", ".join(str(n.get("kind")) for n in notes))


def no_question_check(run) -> dict:
    found = [(s.index, question_in(s.final_message)) for s in run.sessions]
    found = [(i, q) for i, q in found if q]
    final = run.sessions[-1].final_message if run.sessions else ""
    return check("no question in the final message", not found,
                 "; ".join(f"session {i}: {q!r}" for i, q in found) if found
                 else f"final message: {final[:160]!r}")


# ----------------------------------------------------------------------------------------------------------------------
# the intake interview (INTAKE_PLAN.md, "What a pass checks"). The owner's words and flags come from RUN/interview.jsonl
# (runner/run_intake.py); everything else from the workbook, the watcher's log and the platform's action log.

BAD_FLAGS = (
    ("asked_method", "no message asked how to run the climb"),
    ("asked_finding_out", "no message asked what the climb exists to find out"),
    ("asked_known", "no message asked something already written down"),
    ("multiple_questions", "no message held more than one question"),
)


def interview_keys(run) -> set:
    tab = run.tab(INTERVIEW_TAB)
    return {norm_key(tab.key(row)) for row in tab.rows} if tab is not None else set()


def _plain(text) -> str:
    """Text as the verbatim check compares it: curly quotes and dashes made straight, Markdown's backticks and asterisks
    dropped (a CSV cell often loses them), spacing collapsed, lower case. Words still have to match."""
    text = str(text or "").replace("`", "").replace("*", "")
    for curly, straight in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("–", "-"),
                            ("—", "-"), (" ", " ")):
        text = text.replace(curly, straight)
    return " ".join(text.split()).lower()


def _answer_core(answer) -> str:
    """An answer without the quotes or closing stop a record might drop around it."""
    return _plain(answer).strip(" \"'").rstrip(" .!")


def _row_words(row) -> str:
    """A row's own words: every cell but its key column's label and the written_at / written_by stamps."""
    return " ".join(str(v) for k, v in (row or {}).items() if v and k not in ("field", "written_at", "written_by"))


def cited_interview(row, keys) -> list:
    """The Interview keys a row cites that exist in the Interview tab."""
    return [key for prefix, key in keys_in(_row_words(row)) if prefix == "IV" and norm_key(key) in keys]


def owner_answers(run) -> list:
    """[(turn, answer)] for every answer the owner gave during the interview: up to the sign-off, or all of them when
    the owner never signed off."""
    limit = run.signoff_turn
    out = []
    for entry in run.exchanges():
        answer = entry.get("answer")
        turn = entry.get("turn")
        if answer and (limit is None or turn is None or turn <= limit):
            out.append((turn, answer))
    return out


def answer_time(run, interview_key):
    """When the owner gave the answer an Interview row records: the runner's time for that exchange, else when the
    row's answer first appeared in the watcher's log; None when neither shows it."""
    row = run.get(INTERVIEW_TAB, interview_key)
    if row is None:
        return None
    text = _plain(row_text(row))
    for entry in run.interview:
        answer = entry.get("answer")
        if answer and _answer_core(answer) in text and isinstance(entry.get("answered_t"), (int, float)):
            return float(entry["answered_t"])
    for change in run.changes_for(INTERVIEW_TAB, ("added", "changed")):
        if norm_key(change.key) == norm_key(interview_key) and (change.row.get("answer") or "").strip():
            return change.t
    return None


def flagged(run, flag) -> list:
    """Interview entries the owner flagged, in any phase."""
    return [entry for entry in run.interview if (entry.get("flags") or {}).get(flag) is True]


def signed_off_check(run) -> dict:
    entry = run.signoff
    if entry is not None:
        return check("the owner signed off on a playback", True,
                     f"turn {entry.get('turn')}: {str(entry.get('answer') or '')[:160]!r}")
    ended = run.intake.get("ended") or ("no interview log" if not run.interview else "unknown")
    return check("the owner signed off on a playback", False,
                 f"never signed off; {len(owner_answers(run))} answer(s) given; the interview ended: {ended}")


def answers_recorded_check(run) -> dict:
    rows = run.rows(INTERVIEW_TAB)
    texts = [_plain(row_text(row)) for row in rows]
    answers = owner_answers(run)
    missing = [(turn, answer) for turn, answer in answers if not any(_answer_core(answer) in t for t in texts)]
    if not answers:
        evidence = "the owner gave no answer to record"
    else:
        evidence = (f"{len(answers) - len(missing)} of {len(answers)} answers found verbatim in {len(rows)} Interview "
                    f"row(s)") + ("; missing " + "; ".join(f"turn {t}: {a[:90]!r}" for t, a in missing) if missing
                                  else "")
    return check("every answer the owner gave is saved verbatim in the Interview tab", bool(answers) and not missing,
                 evidence)


def owner_fields_cited_check(run, fields=INTAKE_OWNER_FIELDS) -> dict:
    charter = run.workbook.charter()
    keys = interview_keys(run)
    missing = [f for f in fields if f not in charter]
    uncited = [f for f in fields if f in charter and not cited_interview(charter[f], keys)]
    bad = (f"missing {missing}" if missing else "") + ("; " if missing and uncited else "") + \
        (f"citing no Interview row that exists: {uncited}" if uncited else "")
    return check(f"each of the owner's {len(fields)} Charter fields is there and cites an Interview row",
                 not missing and not uncited, bad or f"all {len(fields)} cite an Interview row")


def owner_flag_check(run, flag, name) -> dict:
    hits = flagged(run, flag)
    answered = [entry for entry in run.interview if entry.get("flags") is not None]
    if hits:
        evidence = "; ".join(f"turn {e.get('turn')}: {str(e.get('question') or '')[:140]!r}"
                             + (f" (owner: {e.get('why')})" if e.get("why") else "") for e in hits)
    else:
        evidence = f"none of the {len(answered)} message(s) the owner answered"
    return check(name, not hits, evidence)


def outcome_check_before_playback_check(run) -> dict:
    outcomes = sorted(e.get("turn") for e in flagged(run, "outcome_check") if isinstance(e.get("turn"), int))
    playbacks = sorted(e.get("turn") for e in flagged(run, "playback") if isinstance(e.get("turn"), int))
    ok = bool(outcomes) and bool(playbacks) and outcomes[0] < playbacks[0]
    return check("an outcome check came before the first playback", ok,
                 f"outcome checks on turns {outcomes or 'none'}; playbacks on turns {playbacks or 'none'}")


def before_signoff(run, session_index) -> bool:
    """The session came before the owner signed off (every session does when the owner never signed off)."""
    turn = run.signoff_turn
    return turn is None or session_index is None or session_index <= turn


def nothing_before_signoff_check(run) -> dict:
    early = []
    for tab in ("Charter", "Tests"):
        for change in run.changes_for(tab, ("added",)):
            if before_signoff(run, change.session):
                early.append(f"{tab} {change.key or '?'} written in session {change.session}")
                break
    for launch in run.launches():
        session = run.session_for_time(launch.action.wall) if launch.action.wall is not None else None
        index = session.index if session is not None else None
        if before_signoff(run, index):
            early.append(f"{launch.kind} of {launch.target} in session {index}")
    turn = run.signoff_turn
    when = f"the owner signed off on turn {turn}" if turn is not None else "the owner never signed off"
    return check("nothing seeded or launched before the owner signed off (no Charter or Tests row, no launch)",
                 not early, f"{when}; " + ("; ".join(early) if early else "nothing came earlier"))


def asks_only_in_intake_check(run) -> dict:
    name = "questions only during the interview: no session after the owner signed off asks anything"
    turn = run.signoff_turn
    if turn is None:
        return check(name, True, "the owner never signed off, so every session was the interview's")
    later = [s for s in run.sessions if s.index > turn]
    asked = [(s.index, question_in(s.final_message)) for s in later]
    asked = [(i, q) for i, q in asked if q]
    return check(name, not asked, "; ".join(f"session {i}: {q!r}" for i, q in asked) if asked else
                 f"{len(later)} session(s) after the sign-off on turn {turn}, none asking")


def research_before_launch_check(run) -> dict:
    launches = run.launches()
    first = min((run.launch_bound(launch)[0] or float("inf") for launch in launches), default=float("inf"))
    library = run.rows("Library")
    early = [row for row in library if run.write_time("Library", row) < first]
    return check("research written before the first launch (Library rows)", bool(early),
                 f"{len(early)} of {len(library)} Library rows before the first launch"
                 + ("" if launches else " (nothing launched)"))


def ideas_sourced_check(run) -> dict:
    """Every idea draws on something traceable: workbook keys that exist (Library, Lessons, Tests, the Interview row
    of an owner's idea), or, for an idea imported from earlier work the owner let in, the legacy row it came from."""
    ideas = run.rows("Ideas")
    bad = [f"{row.get('idea_id')} sources {row.get('sources')!r}" for row in ideas
           if not (run.sources_ok(row)[0] or (row.get("legacy_ref") or "").strip()
                   or re.search(r"[A-Za-z0-9_ -]+\.csv\b[^,;]*\d", str(row.get("sources") or "")))]
    return check("every Ideas row is sourced (keys that exist, or its legacy row)", bool(ideas) and not bad,
                 "; ".join(bad) if bad else (f"{len(ideas)} ideas sourced" if ideas else "no Ideas rows"))


def owner_idea_check(run) -> dict:
    keys = interview_keys(run)
    cited = [row.get("idea_id") for row in run.rows("Ideas") if cited_interview(row, keys)]
    return check("the owner's idea is in Ideas, citing its Interview row", bool(cited),
                 f"Ideas citing the interview: {cited}" if cited else "no Ideas row cites an Interview row")


def charter_says_check(run, field, name, *patterns) -> dict:
    """The Charter row for `field` carries what the owner said: each pattern (a regular expression) is found in it."""
    row = run.workbook.charter().get(field)
    text = _row_words(row)
    misses = [p for p in patterns if not re.search(p, text, re.I)]
    return check(name, bool(text) and not misses, f"{field}: {text[:220]!r}" if text else f"no {field} row")


def charter_complete_check(run, fields=INTAKE_CHARTER_FIELDS) -> dict:
    charter = run.workbook.charter()
    missing = [f for f in fields if f not in charter]
    empty = [f for f in fields if f in charter and not (charter[f].get("value") and charter[f].get("reason"))]
    count = len(fields)
    return check(f"a Charter with all {count} fields, each with a value and a reason", not missing and not empty,
                 (f"missing {missing}; " if missing else "") + (f"no value or reason: {empty}" if empty else "")
                 or f"all {count} fields with values and reasons")


def tabs_complete_check(run) -> dict:
    wanted = {name: COLUMNS[name] for name in TABS}
    wanted[INTERVIEW_TAB] = ("interview_id", "question", "answer")
    bad = []
    for name, columns in wanted.items():
        tab = run.tab(name)
        if tab is None:
            bad.append(f"{name} tab missing")
            continue
        lacking = tab.missing_columns(tuple(columns) + TAIL_COLUMNS)
        if lacking:
            bad.append(f"{name} lacks {lacking}")
    return check("every tab of 4.7 and the Interview tab, with at least their columns, written_at and written_by",
                 not bad, "; ".join(bad) if bad else f"all {len(wanted)} tabs complete")


def launched_items(run) -> list:
    """[(launch, the item as the platform holds it)] for every launch that exited 0."""
    items = getattr(run.world, "items", {}) or {}
    return [(launch, items.get(launch.item) or {}) for launch in run.launches()]


def intake_checks(run) -> list:
    """The checks every intake scenario shares: the interview itself, then what it must leave behind."""
    checks = [signed_off_check(run), answers_recorded_check(run), owner_fields_cited_check(run)]
    checks += [owner_flag_check(run, flag, name) for flag, name in BAD_FLAGS]
    checks += [outcome_check_before_playback_check(run), nothing_before_signoff_check(run),
               asks_only_in_intake_check(run), research_before_launch_check(run), ideas_sourced_check(run)]
    return checks


def charter_value(workbook_or_rows, field):
    rows = workbook_or_rows.rows("Charter") if hasattr(workbook_or_rows, "rows") else workbook_or_rows
    for row in rows:
        if normalize_field(row.get("field")) == field:
            return row.get("value")
    return None


def field_changes(run, field):
    """Value changes of one Charter field in this run: [(change, old, new, author)] plus a final-vs-fixture note."""
    out = []
    for change in run.changes_for("Charter"):
        if normalize_field(change.key) != field:
            continue
        if change.kind == "changed":
            old, new = (change.before or {}).get("value"), change.row.get("value")
            if _same_text(old, new):
                continue
        elif change.kind == "added":
            old, new = None, change.row.get("value")
        else:
            old, new = change.row.get("value"), None
        out.append((change, old, new, run.author(change)))
    return out


def field_unchanged_check(run, field, name=None) -> dict:
    before = charter_value(run.initial, field)
    after = charter_value(run.workbook, field)
    changes = field_changes(run, field)
    ok = _same_text(before, after) and not changes
    if ok:
        evidence = f"{field} stayed {after!r}"
    else:
        evidence = f"{field} {before!r} -> {after!r}" + (f"; {len(changes)} change(s) during the run" if changes else "")
    return check(name or f"{field} unchanged", ok, evidence)


def owner_fields_unchanged_check(run) -> dict:
    bad = []
    for field in OWNER_FIELDS:
        before = charter_value(run.initial, field)
        after = charter_value(run.workbook, field)
        if not _same_text(before, after) or field_changes(run, field):
            bad.append(f"{field}: {before!r} -> {after!r}")
    return check("no change to an owner's Charter field", not bad, "; ".join(bad) if bad else
                 "goal, money_total, off_limits and money_request_channel unchanged")


def tests_ever_with(run, column, value):
    return [row for row in run.rows_ever("Tests") if norm_key(row.get(column)) == norm_key(value)]


def results_for(run, test_key, this_run=True):
    rows = run.this_run_rows("Results") if this_run else run.rows("Results")
    return [row for row in rows if text_names(row.get("test_id"), test_key)]


def decisions_naming(run, *idents, kinds=None, not_kinds=None, this_run=True):
    rows = run.this_run_rows("Decisions") if this_run else run.rows("Decisions")
    out = []
    for row in rows:
        if not (text_names(row.get("test_id"), *idents) or row_names(row, *idents)):
            continue
        kind = row.get("kind")
        if kinds is not None and not any(is_label(kind, "decisions", k) for k in kinds):
            continue
        if not_kinds is not None and any(is_label(kind, "decisions", k) for k in not_kinds):
            continue
        out.append(row)
    return out


def scale_decisions(run, this_run=True):
    rows = run.this_run_rows("Decisions") if this_run else run.rows("Decisions")
    return [row for row in rows if is_label(row.get("kind"), "decisions", "scale")]


def subagent_rows(run, name, role, rows=None):
    """(rows written by a subagent naming the role, evidence of the candidates that were not)."""
    rows = run.this_run_rows(name) if rows is None else rows
    good, notes = [], []
    for row in rows:
        if run.subagent_written(name, row, role):
            good.append(row)
        else:
            notes.append(run.describe_author(name, row))
    return good, notes


def never_launched_check(run, item) -> dict:
    attempts = run.launch_attempts_of_item(item)
    return check(f"{item} never launched", not attempts,
                 "no launch, resubmit or post of it" if not attempts else
                 "; ".join(f"{a.kind} -> {a.target} exit {a.action.exit}" for a in attempts))


def campaign_record(run, campaign):
    if run.world is None:
        return None
    record = (getattr(run.world, "campaigns", {}) or {}).get(campaign)
    return record if isinstance(record, dict) else None


def budget_before_run(run, campaign):
    """The campaign's daily budget when the run started (the World's budget events before the run's time, else the
    fixture's Tests row)."""
    record = campaign_record(run, campaign)
    if record:
        value = None
        for event in record.get("budget_events") or []:
            try:
                at, budget = event[0], event[1]
            except (TypeError, IndexError, KeyError):
                continue
            stamp = parse_time(at)
            if stamp is not None and run.now is not None and stamp < run.now:
                value = parse_amount(budget)
        if value is not None:
            return value
    for row in run.initial.rows("Tests"):
        if campaign in ids_in(row.get("platform_id"), "cp"):
            return parse_amount(row.get("daily_budget"))
    return None


def budget_moves(run, campaign):
    """[(action, new budget)] for this run's successful set-budget calls on a campaign."""
    out = []
    for action in run.actions("sim", "set-budget"):
        if not action.ok or action.positional("cp") != campaign:
            continue
        values = [a for a in action.args if not re.fullmatch(r"cp_\d+", a, re.I)]
        amount = parse_amount(values[0]) if values else None
        out.append((action, amount))
    return out


def budget_raised(run, campaign):
    """(raised, evidence): a successful set-budget on the campaign above its budget at that moment."""
    current = budget_before_run(run, campaign)
    for action, amount in budget_moves(run, campaign):
        if amount is not None and (current is None or amount > current + 1e-9):
            return True, f"set-budget {campaign} {amount:g} (was {current})"
        current = amount if amount is not None else current
    return False, f"no budget raise on {campaign}"


def final_budget(run, campaign):
    record = campaign_record(run, campaign)
    if record and record.get("budget_events"):
        try:
            return parse_amount(record["budget_events"][-1][1])
        except (TypeError, IndexError, KeyError):
            return None
    moves = budget_moves(run, campaign)
    if moves:
        return moves[-1][1]
    return budget_before_run(run, campaign)


def paused_during_run(run, campaign) -> bool:
    """The World's status_events show the campaign paused at or after the run's start."""
    record = campaign_record(run, campaign) or {}
    for event in record.get("status_events") or []:
        try:
            at, status = event[0], event[1]
        except (TypeError, IndexError, KeyError):
            continue
        stamp = parse_time(at)
        if status == "paused" and stamp is not None and run.now is not None and stamp >= run.now:
            return True
    return False


def successful(run, sub, campaign):
    return [a for a in run.actions("sim", sub) if a.ok and a.positional("cp") == campaign]


def checks_rows(run, role, verdict, test_key=None, item=None, this_run=True):
    rows = run.this_run_rows("Checks") if this_run else run.rows("Checks")
    out = []
    for row in rows:
        if test_key is not None and not text_names(row.get("test_id"), test_key):
            continue
        if item is not None and norm_key(row.get("item_id")) != norm_key(item):
            continue
        if verdict is not None and not is_label(row.get("verdict"), "checks", verdict):
            continue
        if role is not None and not (role_named(row.get("written_by"), role) or role_named(row.get("role"), role)):
            continue
        out.append(row)
    return out


def subagent_check_row(run, name, role, verdict, test_key=None, item=None) -> dict:
    """A subagent-written Checks row by the role with the verdict (for the test or the item)."""
    rows = checks_rows(run, role, verdict, test_key=test_key, item=item)
    good = [row for row in rows if run.subagent_written("Checks", row, role)]
    target = test_key or item
    if good:
        return check(name, True, run.describe_author("Checks", good[0]))
    if rows:
        return check(name, False, "; ".join(run.describe_author("Checks", row) for row in rows))
    return check(name, False, f"no {role} {verdict or ''} Checks row for {target} in this run")


def type_of_test_row(row):
    return parse_type(row.get("type"))


def hook_of(row):
    parsed = parse_type(row.get("type")) or {}
    return parsed.get("hook")


def type_budget_raises(run, cell, lesson_id=None, rerun_of=None, test_money_ok=False):
    """(raises, reruns) on campaigns of a type: each successful set-budget above the campaign's budget at that moment,
    split into checked confirm reruns (a confirm Tests row for the lesson or the rerun test on that campaign, at that
    budget, with a plan-checker pass before money moved) and the rest. A budget set on a paused campaign moves money
    only when the campaign resumes, so the checks must come before the resume. With `test_money_ok`, a raise on a
    campaign that only explore or confirm tests record is test money following a read, and is listed with the reruns."""
    campaigns = set()
    for row in run.rows_ever("Tests"):
        if type_covers(row.get("type"), cell):
            campaigns.update(ids_in(row.get("platform_id"), "cp"))
    if run.world is not None:
        items = getattr(run.world, "items", {}) or {}
        for cid, record in (getattr(run.world, "campaigns", {}) or {}).items():
            attrs = (items.get(record.get("item")) or {}).get("attrs") or {}
            if all(attrs.get(k) == v for k, v in cell.items()):
                campaigns.add(cid)
    raises, reruns = [], []
    for cid in sorted(campaigns):
        current = budget_before_run(run, cid)
        for action, amount in budget_moves(run, cid):
            if amount is None or (current is not None and amount <= current + 1e-9):
                current = amount if amount is not None else current
                continue
            rerun = _checked_rerun(run, cid, amount, action, cell, lesson_id, rerun_of)
            lanes = {norm_label(r.get("lane")) for r in run.tests_for_launch(cid)}
            if rerun:
                reruns.append(f"{cid} to {amount:g} for {rerun}")
            elif test_money_ok and lanes and lanes <= {"explore", "confirm"}:
                reruns.append(f"{cid} to {amount:g} (test money on a {'/'.join(sorted(lanes))} test)")
            else:
                raises.append(f"set-budget {cid} {amount:g} (was {current})")
            current = amount
    return raises, reruns


def _checked_rerun(run, campaign, amount, action, cell, lesson_id, rerun_of):
    session, call = run.call_for_action(action)
    bound = call["t_result"] if call is not None and call.get("t_result") is not None else action.wall
    for later in run.actions("sim", "resume"):
        if later.ok and later.positional("cp") == campaign and later.wall is not None and action.wall is not None \
                and later.wall >= action.wall:
            s2, c2 = run.call_for_action(later)
            resumed = c2["t_result"] if c2 is not None and c2.get("t_result") is not None else later.wall
            if _paused_at(run, campaign, action.wall):
                bound, session = resumed, s2
            break
    for row in run.rows_ever("Tests"):
        if norm_label(row.get("lane")) != "confirm" or not type_covers(row.get("type"), cell):
            continue
        if campaign not in ids_in(row.get("platform_id"), "cp"):
            continue
        if not ((lesson_id and text_names(row.get("lesson_id"), lesson_id))
                or (rerun_of and text_names(row.get("rerun_of"), rerun_of))):
            continue
        if parse_amount(row.get("daily_budget")) != amount:
            continue
        if run._passes("plan-checker", bound, session.index if session is not None else None,
                       test_key=row.get("test_id")):
            return row.get("test_id")
    return None


def _paused_at(run, campaign, wall):
    """Whether the campaign was paused at that wall time: its state when the run began, then the run's own calls."""
    record = campaign_record(run, campaign) or {}
    began = run.sessions[0].sim_time if run.sessions else None
    state = None
    for event in record.get("status_events") or []:
        if not isinstance(event, (list, tuple)) or len(event) < 2:
            continue
        at = parse_time(event[0])
        if began is None or (at is not None and at < began):
            state = event[1]
    for action in sorted(run.actions("sim"), key=lambda a: a.wall or 0):
        if action.wall is None or action.wall > wall or not action.ok or action.positional("cp") != campaign:
            continue
        verb = action.args[0] if action.args else ""
        if verb == "pause":
            state = "paused"
        elif verb in ("resume", "launch"):
            state = "live"
    return state != "live"


# ----------------------------------------------------------------------------------------------------------------------
# PLAN.md 13: soft signals, reports, coding, variations and the readable workbook (V25 to V30)

COMPLAINT_RE = re.compile(r"complain|mislead|deceptiv|dishonest|false (?:claim|promise)|over-?promis|over-?sell|"
                          r"untrue|\bscams?\b|clickbait", re.I)
REPORT_SUFFIXES = (".md", ".markdown", ".html", ".htm")
STATUS_RE = re.compile(r"\b(?:unconfirmed|provisional|unproven|tentative|proven|confirmed|retired|dropped|"
                       r"recheck(?:ing)?|not (?:yet )?(?:proven|confirmed)|needs? a rerun|awaiting (?:a )?rerun|"
                       r"one read|leans?|leaning|early|preliminary)\b", re.I)
EXPLORE_RE = re.compile(r"explor|untested|untried|unexplored|not yet (?:tried|tested)", re.I)
COUNT_RE = re.compile(r"\b\d+\s*(?:of|/|out of)\s*\d+\b|\b\d+\s+(?:cells?|combinations?|options?|ideas?|tests?|ads?|"
                      r"videos?|variants?)\b", re.I)
UNKNOWN_VALUES = {"", "unknown", "n/a", "na", "?", "unclear", "not shown", "not visible", "cannot tell", "can't tell",
                  "-", "not applicable", "not seen", "none given", "tbd"}


def mentions_complaints(text) -> bool:
    return bool(COMPLAINT_RE.search(str(text or "")))


def report_files(run):
    """[(work-relative path, text, written this run)] for the HTML and Markdown files under `work/reports/`. A file
    counts as written this run when the folder held no such file before the run, or held it with other bytes."""
    folder = run.work / "reports"
    before = run.pre_hashes or {}
    out = []
    if folder.is_dir():
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in REPORT_SUFFIXES:
                continue
            data = path.read_bytes()
            rel = path.relative_to(run.work).as_posix()
            out.append((rel, data.decode("utf-8", errors="replace"),
                        before.get(rel) != hashlib.sha256(data).hexdigest()))
    return out


def report_text(text, headings: bool = True) -> str:
    """A report's words, one line per block: Markdown as written, HTML with its tags taken out; `headings=False`
    leaves out heading lines (a heading such as "What comes next?" titles a section and asks nothing)."""
    raw = str(text or "")
    is_html = bool(re.search(r"<(?:html|body|p|div|h[1-6]|table|ul|li|section)\b", raw, re.I))
    if is_html:
        if not headings:
            raw = re.sub(r"(?is)<h[1-6]\b.*?</h[1-6]>", "\n", raw)
        else:
            raw = re.sub(r"(?i)<h[1-6]\b[^>]*>", "\n# ", raw)     # a heading stays a heading line, as in Markdown
        raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
        raw = re.sub(r"(?i)</(?:p|div|li|tr|h[1-6]|table|ul|ol|section|article|header|footer|blockquote|pre|figcaption)>",
                     "\n", raw)
        raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
        raw = html_mod.unescape(re.sub(r"<[^>]+>", " ", raw))
    lines = [line.strip() for line in raw.splitlines()]
    if not headings and not is_html:
        lines = [line for line in lines if not line.startswith("#")]
    return "\n".join(line for line in lines if line)


def numbers_in(text):
    return [float(m.group(1)) for m in re.finditer(r"(?<![\w.])\$?\s?(\d+(?:\.\d+)?)", str(text or ""))]


def bar_candidates(run, campaigns=None):
    """Costs per conversion the bar could read at the run's time: over the last 1, 2, 3 and 7 days and since the
    start, for all campaigns together and for each exploit campaign, on the platform's count and the app's."""
    world = run.world
    if world is None or run.now is None:
        return []
    exploit = set()
    for row in run.rows_ever("Tests"):
        if norm_label(row.get("lane")) == "exploit":
            exploit.update(ids_in(row.get("platform_id"), "cp"))
    groups = [sorted((getattr(world, "campaigns", {}) or {}).keys())] + [[cid] for cid in sorted(exploit)]
    start = parse_time((getattr(world, "config", {}) or {}).get("start")) or WORLD_START
    cpc = float((getattr(world, "config", {}) or {}).get("cpc") or 0.1)
    out = []
    for since in [run.now - timedelta(days=d) for d in (1, 2, 3, 7)] + [start]:
        for group in groups:
            clicks = platform = app = 0
            for cid in group:
                for hour in world.hourly(cid) or []:
                    stamp = parse_time(hour.get("hour"))
                    if stamp is not None and since <= stamp < run.now:
                        clicks += int(hour.get("clicks") or 0)
                        platform += int(hour.get("platform_conversions") or 0)
                        app += int(hour.get("conversions") or 0)
            for conversions in (platform, app):
                if conversions:
                    out.append(round(clicks * cpc / conversions, 4))
    return sorted(set(out))


def names_a_number(text, candidates, rel: float = 0.02, floor: float = 0.03):
    """The first number in the text within 2% (at least 3 cents) of a candidate, else None."""
    for number in numbers_in(text):
        for want in candidates:
            if abs(number - want) <= max(floor, rel * want):
                return number
    return None


def value_words(cell_or_values) -> set:
    """Words a person would use for attribute values: 'hand-replay' gives 'hand-replay', 'hand replay' and 'replay'."""
    values = cell_or_values.values() if isinstance(cell_or_values, dict) else cell_or_values
    words = set()
    for value in values:
        value = str(value or "").lower()
        if not value:
            continue
        words.update({value, value.replace("-", " ")})
        words.update(part for part in re.split(r"[-_ ]", value) if len(part) > 3)
    return words


def lesson_mentions(text, lessons) -> list:
    """[(lesson id, line)] for lines that name a lesson (its key, or two values of its winner and loser) and say how
    sure it is, on the line or in the heading of its section."""
    out = []
    section_sure = False        # a heading such as "What was learned (all unconfirmed)" says how sure its lines are
    for line in str(text or "").splitlines():
        if line.lstrip().startswith("#"):
            section_sure = bool(STATUS_RE.search(line))
        if not (STATUS_RE.search(line) or section_sure):
            continue
        low = line.lower()
        for lesson in lessons:
            key = lesson.get("lesson_id") or ""
            cells = [parse_type(lesson.get("winner")) or {}, parse_type(lesson.get("loser")) or {}]
            values = {v for cell in cells for v in cell.values()}
            named = {v for v in values if re.search(rf"\b{re.escape(v)}\b", low)
                     or re.search(rf"\b{re.escape(v.replace('-', ' '))}\b", low)}
            if (key and text_names(line, key)) or len(named) >= 2:
                out.append((key, line))
    return out


def exploring_mentions(text, words) -> list:
    """Lines that say what exploring reached: an exploring word with a count or a tried value."""
    out = []
    for line in str(text or "").splitlines():
        if not EXPLORE_RE.search(line):
            continue
        low = line.lower()
        if COUNT_RE.search(line) or any(re.search(rf"\b{re.escape(w)}\b", low) for w in words):
            out.append(line)
    return out


def normalize_attr(name) -> str:
    return re.sub(r"[\s\-]+", "_", str(name or "").strip().strip("`'\"*").lower())


def parse_coding(text) -> dict:
    """{attribute: [values]} from a Charter `attributes` value, however it is laid out: JSON, `name: a, b; ...`,
    `name (a | b), ...`, `name=a/b`, one attribute per line or bullet."""
    raw = str(text or "").strip()
    try:
        obj = json.loads(raw)
    except ValueError:
        obj = None
    if isinstance(obj, dict):
        out = {}
        for name, values in obj.items():
            items = values if isinstance(values, list) else re.split(r"\s*[,/|]\s*", str(values))
            out[normalize_attr(name)] = [str(v).strip() for v in items if str(v).strip()]
        return out
    out = {}
    for part in re.split(r"[;\n]+|\)\s*,\s*", raw):
        part = part.strip().lstrip("-*• \t").strip()
        match = re.match(r"^`?([A-Za-z][A-Za-z0-9 _/\-]*?)`?\s*(?::|=|\(|\s[-–—]\s)\s*(.+)$", part)
        if not match:
            continue
        values = [v.strip(" .`'\"()[]{}") for v in re.split(r"\s*(?:,|/|\||\bor\b)\s*", match.group(2).rstrip(")"))]
        values = [v for v in values if v]
        if values:
            out.setdefault(normalize_attr(match.group(1)), values)
    return out


def coded_attributes(text, world=None) -> list:
    """The attributes a coding text gives two or more values for: by its own layout, or by the world's catalog names
    each followed by two of their values (whichever reads more)."""
    parsed = [name for name, values in parse_coding(text).items() if len(values) >= 2]
    found = []
    if world is not None:
        low = str(text or "").lower()
        listed = (getattr(world, "config", {}) or {}).get("attributes") or []
        attributes = list(listed.items()) if isinstance(listed, dict) else [(a["name"], a["values"]) for a in listed]
        spots = sorted((m.start(), name) for name, _v in attributes
                       for m in re.finditer(rf"\b{re.escape(name.replace('_', ' '))}\b|\b{re.escape(name)}\b", low))
        for index, (at, name) in enumerate(spots):
            end = spots[index + 1][0] if index + 1 < len(spots) else len(low)
            span = low[at:end]
            values = dict(attributes)[name]
            spelled = [{v.lower(), v.lower().replace("-", " ")} for v in values]
            if sum(1 for forms in spelled if any(re.search(rf"\b{re.escape(f)}\b", span) for f in forms)) >= 2 \
                    and name not in found:
                found.append(name)
    return found if len(found) >= len(parsed) else parsed


def coded_pairs(text) -> dict:
    """{attribute: value} from a row's coding (`name=value|...`, `name: value; ...`, or JSON)."""
    raw = str(text or "").strip()
    try:
        obj = json.loads(raw)
    except ValueError:
        obj = None
    if isinstance(obj, dict):
        return {normalize_attr(k): str(v).strip() for k, v in obj.items()}
    out = {}
    for part in re.split(r"[|;,\n]+", raw):
        if "=" in part:
            name, _, value = part.partition("=")
        elif ":" in part:
            name, _, value = part.partition(":")
        else:
            continue
        name, value = normalize_attr(name), value.strip(" .`'\"")
        if name and value:
            out.setdefault(name, value)
    return out


def item_differences(world, item_id, parent_id):
    """(attributes whose values differ, whether the text is the same) between a built item and its parent, from the
    platform's record of what was built."""
    items = getattr(world, "items", {}) or {}
    item, parent = items.get(item_id) or {}, items.get(parent_id) or {}
    a, b = item.get("attrs") or {}, parent.get("attrs") or {}
    diffs = [name for name in sorted(set(a) | set(b)) if a.get(name) != b.get(name)]
    return diffs, _same_text(item.get("text"), parent.get("text"))


def checks_of_test(run, test_row) -> list:
    """The Checks rows behind a Tests row: those naming its test, and those with no test that name its item (the
    critic leaves `test_id` empty; the main agent ties items to their tests)."""
    tid, item = test_row.get("test_id"), norm_key(test_row.get("item_id"))
    out = []
    for row in run.rows("Checks"):
        if tid and text_names(row.get("test_id"), tid):
            out.append(row)
        elif not str(row.get("test_id") or "").strip() and item and norm_key(row.get("item_id")) == item:
            out.append(row)
    return out


ROLE_WORDS = {"plan-checker": r"plan[\s\-]*check", "build-checker": r"build[\s\-]*check", "critic": r"critic"}
VERDICT_WORDS = {"pass": r"\b(?:pass(?:ed|es)?|ok)\b", "fail": r"\bfail(?:ed|s)?\b"}


def shows_check(text, check_row) -> bool:
    """A Tests row's words show a check's verdict: its key, or its role named with its verdict in the same part."""
    text = str(text or "")
    if check_row.get("check_id") and text_names(text, check_row["check_id"]):
        return True
    role = next((r for r in ROLE_WORDS if role_named(check_row.get("role"), r)
                 or role_named(check_row.get("written_by"), r)), None)
    verdict = "pass" if is_label(check_row.get("verdict"), "checks", "pass") else \
        "fail" if is_label(check_row.get("verdict"), "checks", "fail") else None
    if role is None or verdict is None:
        return False
    return any(re.search(ROLE_WORDS[role], part, re.I) and re.search(VERDICT_WORDS[verdict], part, re.I)
               for part in re.split(r"[;\n|]+", text))
