#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).with_name("agent_history.py")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


class AgentHistoryScriptTests(unittest.TestCase):
    def run_tool(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def extract_run_dir(self, stdout: str) -> Path:
        match = re.search(r"run=([^\s]+)", stdout)
        self.assertIsNotNone(match, stdout)
        return Path(match.group(1))

    def make_codex_home(self, root: Path, project: Path) -> Path:
        home = root / "codex"
        home.mkdir()
        rollout = home / "sessions" / "2026" / "05" / "02" / "rollout-2026-05-02T10-00-00-codex-thread.jsonl"
        write_jsonl(
            rollout,
            [
                {
                    "timestamp": now_iso(),
                    "type": "session_meta",
                    "payload": {"id": "codex-thread", "cwd": str(project)},
                },
                {
                    "timestamp": now_iso(),
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "text", "text": "Actually use helper scripts instead."}],
                    },
                },
                {
                    "timestamp": now_iso(),
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "create_goal",
                        "arguments": "{\"objective\":\"ship agent-history\"}",
                    },
                },
            ],
        )
        write_jsonl(
            home / "history.jsonl",
            [
                {
                    "session_id": "codex-thread",
                    "ts": int(datetime.now(timezone.utc).timestamp()),
                    "text": "What prompt did I run here?",
                }
            ],
        )
        conn = sqlite3.connect(home / "state_5.sqlite")
        conn.execute(
            """
            CREATE TABLE threads (
                id TEXT,
                rollout_path TEXT,
                cwd TEXT,
                title TEXT,
                created_at_ms INTEGER,
                updated_at_ms INTEGER,
                first_user_message TEXT,
                model TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE thread_goals (
                thread_id TEXT PRIMARY KEY,
                goal_id TEXT,
                objective TEXT,
                status TEXT,
                token_budget INTEGER,
                tokens_used INTEGER,
                time_used_seconds INTEGER,
                created_at_ms INTEGER,
                updated_at_ms INTEGER
            )
            """
        )
        conn.execute(
            "INSERT INTO threads VALUES (?,?,?,?,?,?,?,?)",
            (
                "codex-thread",
                str(rollout),
                str(project),
                "Agent history work",
                now_ms(),
                now_ms(),
                "What prompt did I run here?",
                "gpt-test",
            ),
        )
        conn.execute(
            "INSERT INTO thread_goals VALUES (?,?,?,?,?,?,?,?,?)",
            (
                "codex-thread",
                "goal-1",
                "ship agent-history",
                "active",
                None,
                10,
                0,
                now_ms(),
                now_ms(),
            ),
        )
        conn.commit()
        conn.close()
        return home

    def make_claude_home(self, root: Path, project: Path) -> Path:
        home = root / "claude"
        home.mkdir()
        write_jsonl(
            home / "history.jsonl",
            [
                {
                    "display": "/arch-step status",
                    "project": str(project),
                    "sessionId": "claude-session",
                    "timestamp": now_ms(),
                },
                {
                    "display": "Find all the places I corrected the agent",
                    "project": str(project),
                    "sessionId": "claude-session",
                    "timestamp": now_ms(),
                },
            ],
        )
        project_file = home / "projects" / "-tmp-project" / "claude-session.jsonl"
        write_jsonl(
            project_file,
            [
                {
                    "type": "custom-title",
                    "customTitle": "Claude history work",
                    "sessionId": "claude-session",
                    "timestamp": now_iso(),
                },
                {
                    "type": "user",
                    "sessionId": "claude-session",
                    "cwd": str(project),
                    "timestamp": now_iso(),
                    "message": {
                        "role": "user",
                        "content": "No, that is wrong; use the bundled helper.",
                    },
                },
                {
                    "type": "queue-operation",
                    "sessionId": "claude-session",
                    "cwd": str(project),
                    "timestamp": now_iso(),
                    "operation": "enqueue",
                    "content": "/goal improve history lookup",
                },
            ],
        )
        return home

    def prime_session_lines(self, project: Path, session_id: str) -> list[dict]:
        return [
            {
                "type": "session",
                "version": 3,
                "id": session_id,
                "timestamp": now_iso(),
                "cwd": str(project),
                "rlmDepth": 0,
            },
            {"type": "model_change", "timestamp": now_iso(), "provider": "anthropic", "modelId": "claude-fable-5-1"},
            {"type": "session_info", "timestamp": now_iso(), "name": "prime root session"},
            {
                "type": "custom",
                "customType": "aimgr_credential_binding_v1",
                "timestamp": now_iso(),
                "data": {"provider": "anthropic", "binding": "cfo"},
            },
            {
                "type": "message",
                "timestamp": now_iso(),
                "message": {
                    "role": "user",
                    "content": [{"type": "text", "text": "Why did the prime worker stall?"}],
                },
            },
            {
                "type": "message",
                "timestamp": now_iso(),
                "message": {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "thinking": "checking the daemon"},
                        {"type": "toolCall", "name": "ipython", "arguments": "{\"code\": \"print('stall probe')\"}"},
                    ],
                },
            },
            {
                "type": "custom_message",
                "customType": "session_slash_command",
                "timestamp": now_iso(),
                "content": "/compact",
                "details": {"command": {"name": "compact", "args": "", "text": "/compact"}},
            },
            {
                "type": "custom_message",
                "customType": "session_slash_command",
                "timestamp": now_iso(),
                "content": "/goal finish the prime lane",
                "details": {"command": {"name": "goal", "args": "finish the prime lane", "text": "/goal finish the prime lane"}},
            },
            {
                "type": "custom_message",
                "customType": "agent_message",
                "timestamp": now_iso(),
                "content": "[from child:impl-worker] the worktree rebase is clean",
            },
            {
                "type": "child_usage_attributed",
                "timestamp": now_iso(),
                "usage": {"inputTokens": 991, "note": "accounting noise marker"},
            },
            {"type": "compaction", "timestamp": now_iso(), "summary": "earlier turns replaced by summary"},
        ]

    def make_prime_home(self, root: Path, project: Path) -> Path:
        home = root / "prime"
        session_id = "019ff047-07a1-713e-b276-6267b0e671f3"
        child_id = "019ff08a-b620-73dd-ab62-d1b7d97b4082"
        write_jsonl(
            home / "agent" / "sessions" / f"{session_id}.jsonl",
            self.prime_session_lines(project, session_id),
        )
        artifacts = home / "agent" / "session-artifacts" / session_id
        child_dir = artifacts / "sub-39fd0823"
        write_jsonl(
            artifacts / "rlm-subagents.jsonl",
            [
                {
                    "type": "rlm_subagent",
                    "childId": "sub-39fd0823",
                    "sessionName": "impl-worker",
                    "sessionFile": str(child_dir / f"{child_id}.jsonl"),
                    "parentSessionId": session_id,
                    "rlmDepth": 1,
                    "prompt": "Role: implement the branch",
                }
            ],
        )
        write_jsonl(
            child_dir / f"{child_id}.jsonl",
            [
                {
                    "type": "session",
                    "version": 3,
                    "id": child_id,
                    "timestamp": now_iso(),
                    "cwd": str(project),
                    "rlmDepth": 1,
                },
                {
                    "type": "message",
                    "timestamp": now_iso(),
                    "message": {
                        "role": "user",
                        "content": [{"type": "text", "text": "child transcript marker"}],
                    },
                },
            ],
        )
        return home

    def make_pi_home(self, root: Path, project: Path) -> Path:
        home = root / "pi"
        session_dir = home / "agent" / "sessions" / "--decoy-encoded-path--"
        write_jsonl(
            session_dir / "2026-06-12T20-46-27-706Z_019ebd96-0b79-74a1-a46f-b2ce2ec9e674.jsonl",
            [
                {
                    "type": "session",
                    "version": 3,
                    "id": "019ebd96-0b79-74a1-a46f-b2ce2ec9e674",
                    "timestamp": now_iso(),
                    "cwd": str(project),
                },
                {
                    "type": "message",
                    "timestamp": now_iso(),
                    "message": {
                        "role": "user",
                        "content": [{"type": "text", "text": "pi prompt in the real project"}],
                    },
                },
            ],
        )
        # Extension diagnostics live beside transcripts and are keyed `event`.
        write_jsonl(
            session_dir / "authoring-panel-debug.jsonl",
            [
                {"event": "extension_module_registered", "at": now_iso(), "cwd": str(project)},
                {"event": "panel_state", "at": now_iso(), "note": "extension noise marker"},
            ],
        )
        (session_dir / "authoring-panel-state.json").write_text('{"activeKind": "lesson"}\n')
        return home

    def test_prime_prompts_and_show(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            proc = self.run_tool(
                "prompts",
                "--runtime",
                "prime",
                "--prime-home",
                str(prime_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Why did the prime worker stall?", proc.stdout)
            self.assertNotIn("checking the daemon", proc.stdout)

            run_dir = self.extract_run_dir(proc.stdout)
            show = self.run_tool("show", "--run", str(run_dir), "--id", "r0001")
            self.assertEqual(show.returncode, 0, show.stderr)
            self.assertIn("Why did the prime worker stall?", show.stdout)

    def test_prime_sessions_report_name_model_and_account(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            proc = self.run_tool(
                "sessions",
                "--runtime",
                "prime",
                "--prime-home",
                str(prime_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("prime root session", proc.stdout)
            self.assertIn("claude-fable-5-1", proc.stdout)
            self.assertIn("account cfo", proc.stdout)
            self.assertIn("1 compactions", proc.stdout)

    def test_prime_sidechains_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            base = [
                "search",
                "--runtime",
                "prime",
                "--prime-home",
                str(prime_home),
                "--cwd",
                str(project),
            ]
            without = self.run_tool(*base, "--output-root", str(root / "runs1"), "child transcript marker")
            self.assertEqual(without.returncode, 0, without.stderr)
            self.assertIn("NO_MATCH", without.stdout)

            with_children = self.run_tool(
                *base,
                "--include-sidechains",
                "--output-root",
                str(root / "runs2"),
                "child transcript marker",
            )
            self.assertEqual(with_children.returncode, 0, with_children.stderr)
            self.assertIn("child transcript marker", with_children.stdout)

            listing = self.run_tool(
                "sessions",
                "--runtime",
                "prime",
                "--prime-home",
                str(prime_home),
                "--cwd",
                str(project),
                "--include-sidechains",
                "--output-root",
                str(root / "runs3"),
            )
            self.assertEqual(listing.returncode, 0, listing.stderr)
            self.assertIn("impl-worker", listing.stdout)

    def test_prime_commands_goals_and_agent_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            base = ["--runtime", "prime", "--prime-home", str(prime_home), "--cwd", str(project)]

            commands = self.run_tool("commands", *base, "--output-root", str(root / "runs1"))
            self.assertEqual(commands.returncode, 0, commands.stderr)
            self.assertIn("/compact", commands.stdout)
            self.assertIn("/goal finish the prime lane", commands.stdout)

            goals = self.run_tool("goals", *base, "--output-root", str(root / "runs2"))
            self.assertEqual(goals.returncode, 0, goals.stderr)
            self.assertIn("/goal finish the prime lane", goals.stdout)
            self.assertNotIn("/compact", goals.stdout)

            agent_messages = self.run_tool(
                "search", *base, "--output-root", str(root / "runs3"), "worktree rebase"
            )
            self.assertEqual(agent_messages.returncode, 0, agent_messages.stderr)
            self.assertIn("agent_message", agent_messages.stdout)

    def test_prime_skips_usage_records_and_caps_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            base = ["--runtime", "prime", "--prime-home", str(prime_home), "--cwd", str(project)]

            usage = self.run_tool("search", *base, "--output-root", str(root / "runs1"), "accounting noise marker")
            self.assertEqual(usage.returncode, 0, usage.stderr)
            self.assertIn("NO_MATCH", usage.stdout)

            capped = self.run_tool(
                "search",
                *base,
                "--max-results",
                "1",
                "--output-root",
                str(root / "runs2"),
                "prime",
            )
            self.assertEqual(capped.returncode, 0, capped.stderr)
            self.assertIn("capped at 1", capped.stdout)

    def test_pi_uses_header_cwd_and_ignores_extension_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            pi_home = self.make_pi_home(root, project)
            base = ["--runtime", "pi", "--pi-home", str(pi_home), "--cwd", str(project)]

            # The directory name encodes a decoy path; the header cwd is truth.
            prompts = self.run_tool("prompts", *base, "--output-root", str(root / "runs1"))
            self.assertEqual(prompts.returncode, 0, prompts.stderr)
            self.assertIn("pi prompt in the real project", prompts.stdout)

            noise = self.run_tool("search", *base, "--output-root", str(root / "runs2"), "extension noise marker")
            self.assertEqual(noise.returncode, 0, noise.stderr)
            self.assertIn("NO_MATCH", noise.stdout)
            run_dir = self.extract_run_dir(noise.stdout)
            errors = (run_dir / "errors.jsonl").read_text().strip()
            self.assertEqual(errors, "", errors)

    def test_pi_scope_filters_other_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            other = root / "other"
            project.mkdir()
            other.mkdir()
            pi_home = self.make_pi_home(root, project)
            write_jsonl(
                pi_home / "agent" / "sessions" / "--other--" / "2026-06-13T10-00-00-000Z_019ebd96-0b79-74a1-a46f-b2ce2ec9e675.jsonl",
                [
                    {
                        "type": "session",
                        "version": 3,
                        "id": "019ebd96-0b79-74a1-a46f-b2ce2ec9e675",
                        "timestamp": now_iso(),
                        "cwd": str(other),
                    },
                    {
                        "type": "message",
                        "timestamp": now_iso(),
                        "message": {
                            "role": "user",
                            "content": [{"type": "text", "text": "wrong project marker"}],
                        },
                    },
                ],
            )
            scoped = self.run_tool(
                "prompts",
                "--runtime",
                "pi",
                "--pi-home",
                str(pi_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs1"),
            )
            self.assertEqual(scoped.returncode, 0, scoped.stderr)
            self.assertNotIn("wrong project marker", scoped.stdout)

            everywhere = self.run_tool(
                "prompts",
                "--runtime",
                "pi",
                "--pi-home",
                str(pi_home),
                "--cwd",
                str(project),
                "--scope",
                "all-projects",
                "--output-root",
                str(root / "runs2"),
            )
            self.assertEqual(everywhere.returncode, 0, everywhere.stderr)
            self.assertIn("wrong project marker", everywhere.stdout)

    def test_malformed_session_lines_are_recoverable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            prime_home = self.make_prime_home(root, project)
            session = prime_home / "agent" / "sessions" / "019ff047-07a1-713e-b276-6267b0e671f3.jsonl"
            with session.open("a", encoding="utf-8") as handle:
                handle.write("{not json at all}\n")
            proc = self.run_tool(
                "prompts",
                "--runtime",
                "prime",
                "--prime-home",
                str(prime_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Why did the prime worker stall?", proc.stdout)
            run_dir = self.extract_run_dir(proc.stdout)
            errors = [json.loads(line) for line in (run_dir / "errors.jsonl").read_text().splitlines() if line]
            self.assertTrue(any("invalid JSONL" in error.get("error", "") for error in errors), errors)

    def test_codex_prompts_and_show(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            codex_home = self.make_codex_home(root, project)
            out_root = root / "runs"
            proc = self.run_tool(
                "prompts",
                "--runtime",
                "codex",
                "--codex-home",
                str(codex_home),
                "--cwd",
                str(project),
                "--output-root",
                str(out_root),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("OK agent-history prompts", proc.stdout)
            self.assertIn("What prompt did I run here?", proc.stdout)
            run_dir = self.extract_run_dir(proc.stdout)
            self.assertTrue((run_dir / "results.jsonl").exists())

            show = self.run_tool("show", "--run", str(run_dir), "--id", "r0001")
            self.assertEqual(show.returncode, 0, show.stderr)
            self.assertIn("What prompt did I run here?", show.stdout)

    def test_codex_goals_include_state_and_tool_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            codex_home = self.make_codex_home(root, project)
            proc = self.run_tool(
                "goals",
                "--runtime",
                "codex",
                "--codex-home",
                str(codex_home),
                "--cwd",
                str(project),
                "--since",
                "today",
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("ship agent-history", proc.stdout)
            self.assertIn("create_goal", proc.stdout)

    def test_claude_commands_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            claude_home = self.make_claude_home(root, project)
            commands = self.run_tool(
                "commands",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
            )
            self.assertEqual(commands.returncode, 0, commands.stderr)
            self.assertIn("/arch-step status", commands.stdout)
            self.assertIn("/goal improve history lookup", commands.stdout)

            search = self.run_tool(
                "search",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs2"),
                "wrong",
            )
            self.assertEqual(search.returncode, 0, search.stderr)
            self.assertIn("No, that is wrong", search.stdout)

    def test_current_project_scope_filters_other_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            other = root / "other"
            project.mkdir()
            other.mkdir()
            claude_home = self.make_claude_home(root, project)
            write_jsonl(
                claude_home / "projects" / "-other" / "other-session.jsonl",
                [
                    {
                        "type": "user",
                        "sessionId": "other-session",
                        "cwd": str(other),
                        "timestamp": now_iso(),
                        "message": {"role": "user", "content": "wrong project marker"},
                    }
                ],
            )
            proc = self.run_tool(
                "search",
                "--runtime",
                "claude",
                "--claude-home",
                str(claude_home),
                "--cwd",
                str(project),
                "--output-root",
                str(root / "runs"),
                "wrong",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn("wrong project marker", proc.stdout)
            self.assertIn("No, that is wrong", proc.stdout)


if __name__ == "__main__":
    unittest.main()
