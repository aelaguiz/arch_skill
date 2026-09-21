"""Deterministic inventory of what a session did: files, objects, commands, spawns.

Imported by session_events.py for the `work` mode. Stdlib only. This module
extracts facts from tool calls; it decides nothing.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from typing import Any

# Command classes. Each is a recognition of what a shell command does to the
# machine or the repo, derived from the command text alone.
CMD_CLASSES = [
    ("search_broad", re.compile(r"(?:\b(rg|grep|ag|find|fd)\b[^|;&]*?(\s|=)(~|\$HOME|\.\.|~/workspace/?|/Users/[^/\s]+/?(workspace/?)?)(\s|$|-|\"))|(?:\b(find|fd)\s+(?:-\S+\s+)*/(?:\s|$))")),
    ("search_multi_root", re.compile(r"\b(rg|grep|ag|find|fd)\b[^|;&]*?(/Users/[^/\s]+/workspace/[^/\s]+)[^|;&]*?(\s)(/Users/[^/\s]+/workspace/[^/\s]+)")),
    ("search", re.compile(r"\b(rg|grep|ag|find|fd)\b")),
    ("test_run", re.compile(r"\b(flutter test|dart test|pytest|go test|cargo test|npm test|yarn test|pnpm test|jest|vitest|xcodebuild .*test|patrol test|mvn test|gradle test)\b")),
    ("build", re.compile(r"\b(flutter build|flutter run|xcodebuild|cargo build|go build|npm run build|yarn build|pnpm build|make\b|docker build|gradle assemble)")),
    ("install_global", re.compile(r"\b(brew install|npm i(nstall)? -g|npm install --global|pip install|pipx install|cargo install|gem install|curl [^|]*\| *(ba)?sh|install\.sh)\b")),
    ("process_start", re.compile(r"\b(launchctl|nohup|tmux new|screen -dm|pm2|systemctl|open -a|caffeinate)\b|&\s*$")),
    ("vm_or_sim", re.compile(r"\b(tart|utm|multipass|vagrant|xcrun simctl (boot|create)|emulator -avd)\b")),
    ("git_worktree", re.compile(r"\bgit worktree (add|remove)\b")),
    ("git_push", re.compile(r"\bgit push\b")),
    ("git_force", re.compile(r"\bgit push[^|;&]*(--force|-f\b)|\bgit reset --hard|\bgit clean -fd")),
    ("gh_pr_create", re.compile(r"\bgh pr create\b")),
    ("gh_pr_edit", re.compile(r"\bgh pr (edit|close|merge|ready|comment)\b")),
    ("gh_issue_create", re.compile(r"\bgh issue create\b")),
    ("gh_issue_edit", re.compile(r"\bgh issue (edit|close|comment|reopen)\b")),
    ("sheet_write", re.compile(r"\bgws\b[^|;&]*\b(write|update|append|batchUpdate|values\.(update|append)|clear)\b|spreadsheets\.values\.(update|append|batchUpdate)")),
    ("delete", re.compile(r"\brm -rf?\b|\bgit branch -D\b|\bdrop table\b", re.I)),
    ("network_post", re.compile(r"\bcurl\b[^|;&]*-X ?(POST|PUT|PATCH|DELETE)|\bcurl\b[^|;&]*--data")),
    ("sleep_wait", re.compile(r"\bsleep \d+|\bwait_agent\b|write_stdin\(\{[^}]*chars:\"\"")),
]

FIGMA_CREATE = re.compile(r"\bfigma\.(createFrame|createRectangle|createText|createEllipse|createLine|createComponent|createPage)\b")
FIGMA_REUSE = re.compile(r"\b(createInstance|importComponentByKeyAsync|importStyleByKeyAsync|componentKey|getNodeById\([^)]*\)\.clone)\b")

PATCH_ADD = re.compile(r"\*\*\* Add File: ([^\s\\\"']+)")
PATCH_UPDATE = re.compile(r"\*\*\* (Update|Delete|Move to) File: ([^\s\\\"']+)")
SURFACE_FILE = re.compile(r"(/presentation/|/screens?/|/pages?/|/views?/|/ui/|/widgets?/|/components?/|_screen\.|_page\.|_editor\.|_sheet\.|_overlay\.|_dialog\.|_modal\.|_settings\.|_preferences\.|Screen\.|Page\.|View\.|\.tsx$|\.jsx$|\.vue$|\.svelte$|\.storyboard$|\.xib$)")
WRITE_REDIRECT = re.compile(r"(?:>|>>|tee -a?)\s*([~/.\w][^\s;&|]*\.(md|py|ts|tsx|js|dart|go|rs|json|yaml|yml|toml|sh|sql|txt|html|css))")


def _text_of(args: Any) -> str:
    if isinstance(args, str):
        try:
            return _text_of(json.loads(args))
        except json.JSONDecodeError:
            return args
    if isinstance(args, dict):
        return " ".join(str(v) for v in args.values() if isinstance(v, (str, int, float)))
    return str(args)


def classify_command(text: str) -> list[str]:
    out = []
    for name, rx in CMD_CLASSES:
        if rx.search(text):
            out.append(name)
    if ("search_broad" in out or "search_multi_root" in out) and "search" in out:
        out.remove("search")
    if "search_broad" in out and "search_multi_root" in out:
        out.remove("search_multi_root")
    return out


class Inventory:
    def __init__(self) -> None:
        self.files_added: Counter = Counter()
        self.files_changed: Counter = Counter()
        self.commands: Counter = Counter()
        self.command_examples: dict[str, list[str]] = defaultdict(list)
        self.spawns: Counter = Counter()
        self.figma_create: Counter = Counter()
        self.figma_reuse: Counter = Counter()
        self.tool_calls = 0
        self.user_turns = 0
        self.assistant_turns = 0
        self.claims: list[tuple[str, str]] = []  # (ts, sentence) assistant sentences asserting what the work is
        self.first_ts: str = ""
        self.last_ts: str = ""

    def add_event(self, ev: dict[str, Any], raw_args: Any = None) -> None:
        kind = ev.get("kind")
        if kind in ("USER", "USER_INTERRUPT", "USER_QUEUED"):
            self.user_turns += 1
            return
        if kind == "ASSISTANT":
            self.assistant_turns += 1
            for sent in re.split(r"(?<=[.!?])\s+", ev.get("text", "")):
                if re.search(r"\b(uses|reuses|reused|using|based on|built on|existing|canonical|no new|nothing new|only|just)\b", sent, re.I) and len(sent) < 300:
                    self.claims.append((ev.get("ts", ""), sent.strip()))
            return
        if kind == "SPAWN":
            self.spawns[ev.get("name") or "spawn"] += 1
            return
        if kind not in ("TOOL", "GOAL", "ASK"):
            return
        self.tool_calls += 1
        if ev.get("ts"):
            self.first_ts = self.first_ts or ev["ts"]
            self.last_ts = ev["ts"]
        text = _text_of(raw_args if raw_args is not None else ev.get("text", ""))
        for m in PATCH_ADD.finditer(text):
            self.files_added[m.group(1)] += 1
        for m in PATCH_UPDATE.finditer(text):
            self.files_changed[m.group(2)] += 1
        for m in WRITE_REDIRECT.finditer(text):
            self.files_changed[m.group(1)] += 1
        if isinstance(raw_args, dict):
            fp = raw_args.get("file_path") or raw_args.get("path")
            if isinstance(fp, str) and ev.get("name") in ("Write", "Edit", "MultiEdit", "NotebookEdit", "write_file", "edit_file"):
                (self.files_added if ev.get("name") == "Write" else self.files_changed)[fp] += 1
        flat = re.sub(r"\s+", " ", text)
        for cls in classify_command(text):
            self.commands[cls] += 1
            cap = 5 if cls.startswith("search_") else 3
            if len(self.command_examples[cls]) < cap:
                if cls.startswith("search_"):
                    m = next((rx.search(flat) for name, rx in CMD_CLASSES if name == cls), None)
                    start = max(0, m.start() - 20) if m else 0
                    self.command_examples[cls].append(("..." if start else "") + flat[start:start + 200])
                else:
                    self.command_examples[cls].append(flat[:200])
        for m in FIGMA_CREATE.finditer(text):
            self.figma_create[m.group(1)] += 1
        for m in FIGMA_REUSE.finditer(text):
            self.figma_reuse[m.group(1)] += 1

    def summary_lines(self, limit: int = 12) -> list[str]:
        lines = []
        span = ""
        try:
            import datetime as _dt
            a = _dt.datetime.fromisoformat(self.first_ts); b = _dt.datetime.fromisoformat(self.last_ts)
            mins = max(1, int((b - a).total_seconds() // 60))
            broad = self.commands.get("search_broad", 0) + self.commands.get("search_multi_root", 0)
            searches = self.commands.get("search", 0) + broad
            broad_note = f", {broad} rooted at ~, ~/workspace, .., or several repos" if broad else ""
            span = f"; span {mins} min; searches {searches} ({searches/mins:.1f}/min{broad_note}), tests {self.commands.get('test_run', 0)}, builds {self.commands.get('build', 0)}"
        except Exception:
            pass
        lines.append(f"turns: user {self.user_turns}, assistant {self.assistant_turns}, tool calls {self.tool_calls}, spawns {sum(self.spawns.values())}{span}")
        if self.files_added:
            lines.append("files added: " + ", ".join(f"{p}" for p, _ in self.files_added.most_common(limit)) + (f" (+{len(self.files_added)-limit} more)" if len(self.files_added) > limit else ""))
        if self.files_changed:
            lines.append("files changed: " + ", ".join(f"{p}" for p, _ in self.files_changed.most_common(limit)) + (f" (+{len(self.files_changed)-limit} more)" if len(self.files_changed) > limit else ""))
        surfaces = [p for p in list(self.files_added) + list(self.files_changed) if SURFACE_FILE.search(p) and not re.search(r"(/test/|/tests/|_test\.|\.test\.|\.spec\.)", p)]
        if surfaces:
            seen = []
            for p in surfaces:
                if p not in seen:
                    seen.append(p)
            lines.append("user-facing surfaces touched (by path; he sees these): " + ", ".join(p.rsplit("/", 1)[-1] + (" (new)" if p in self.files_added else "") for p in seen[:limit]) + (f" (+{len(seen)-limit} more)" if len(seen) > limit else ""))
        if self.commands:
            lines.append("commands by class: " + ", ".join(f"{k} x{v}" for k, v in self.commands.most_common()))
            for cls in ("search_broad", "search_multi_root", "test_run", "build", "install_global", "process_start", "vm_or_sim", "git_force", "delete", "gh_pr_create", "gh_issue_create", "sheet_write"):
                for ex in self.command_examples.get(cls, [])[: (5 if cls.startswith("search_") else 1)]:
                    lines.append(f"  {cls}: {ex}")
        if self.figma_create or self.figma_reuse:
            lines.append(f"figma: created from primitives {dict(self.figma_create)} | reused components/styles {dict(self.figma_reuse) or 'none'}")
        if self.spawns:
            lines.append("spawns: " + ", ".join(f"{k} x{v}" for k, v in self.spawns.most_common()))
        if self.claims:
            lines.append(f"assistant claims about the work ({len(self.claims)}), latest:")
            for ts, c in self.claims[-4:]:
                lines.append(f"  {ts[11:19] if ts else '--:--:--'} \"{c[:180]}\"")
        return lines

    def to_dict(self) -> dict[str, Any]:
        return {
            "turns": {"user": self.user_turns, "assistant": self.assistant_turns, "tool_calls": self.tool_calls},
            "files_added": dict(self.files_added),
            "files_changed": dict(self.files_changed),
            "commands": dict(self.commands),
            "command_examples": dict(self.command_examples),
            "spawns": dict(self.spawns),
            "figma_create": dict(self.figma_create),
            "figma_reuse": dict(self.figma_reuse),
            "claims": self.claims[-40:],
        }
