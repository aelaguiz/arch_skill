#!/usr/bin/env python3
from __future__ import annotations

import json
import os
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

    def make_agy_home(self, root: Path, project: Path, other: Path) -> Path:
        home = root / "agy"
        (home / "brain").mkdir(parents=True)
        conn = sqlite3.connect(home / "conversation_summaries.db")
        conn.execute(
            "CREATE TABLE conversation_summaries (conversation_id text, title text, "
            "preview text, last_modified_time datetime, workspace_uris text, "
            "parent_conversation_id text, nesting_depth integer)"
        )
        rows = [
            ("agy-main", "Fix the badge", "", now_iso(), json.dumps([project.as_uri()]), "", 0),
            ("agy-child", "Research helper", "", now_iso(), json.dumps([project.as_uri()]), "agy-main", 1),
            ("agy-other", "Other repo work", "", now_iso(), json.dumps([other.as_uri()]), "", 0),
            ("agy-unset", "Never ran", "", "0001-01-01 00:00:00+00:00", "", "", 0),
        ]
        conn.executemany("INSERT INTO conversation_summaries VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
        conn.commit()
        conn.close()

        def transcript(cid: str, name: str, steps: list[dict]) -> None:
            write_jsonl(home / "brain" / cid / ".system_generated" / "logs" / name, steps)

        transcript(
            "agy-main",
            "transcript_full.jsonl",
            [
                {"step_index": 0, "type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": now_iso(),
                 "content": "<USER_REQUEST>\nFind where the Discount badge comes from.\n</USER_REQUEST>\n<ADDITIONAL_METADATA>\nlocal time\n</ADDITIONAL_METADATA>"},
                {"step_index": 1, "type": "PLANNER_RESPONSE", "source": "MODEL", "created_at": now_iso(),
                 "content": "", "thinking": "I should search the typesense mapping.",
                 "tool_calls": [{"name": "invoke_subagent", "args": {"Subagents": "[{\"Prompt\": \"Trace the badge field\"}]", "toolAction": "\"Launching\""}}]},
                {"step_index": 2, "type": "GENERIC", "source": "SYSTEM", "created_at": now_iso(),
                 "content": "Subagent reply: badge comes from typesense discount_pct"},
                {"step_index": 3, "type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": now_iso(),
                 "content": "<USER_REQUEST>\n/goal ship the badge fix\n</USER_REQUEST>"},
            ],
        )
        transcript(
            "agy-child",
            "transcript.jsonl",
            [
                {"step_index": 0, "type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": now_iso(),
                 "content": "<USER_REQUEST>\nTrace the badge field\n</USER_REQUEST>", "truncated_fields": ["content"]},
            ],
        )
        transcript(
            "agy-other",
            "transcript_full.jsonl",
            [
                {"step_index": 0, "type": "USER_INPUT", "source": "USER_EXPLICIT", "created_at": now_iso(),
                 "content": "<USER_REQUEST>\nUnrelated badge question\n</USER_REQUEST>"},
            ],
        )
        return home

    def test_agy_sessions_prompts_search_and_subagents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            other = root / "other"
            project.mkdir()
            other.mkdir()
            home = self.make_agy_home(root, project, other)
            common = ["--runtime", "agy", "--agy-home", str(home), "--cwd", str(project),
                      "--output-root", str(root / "out"), "--format", "jsonl"]

            proc = self.run_tool("sessions", *common)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Fix the badge", proc.stdout)
            self.assertNotIn("Research helper", proc.stdout)
            self.assertNotIn("Other repo work", proc.stdout)

            proc = self.run_tool("sessions", *common, "--include-sidechains", "--max-preview-chars", "300")
            self.assertIn("Research helper", proc.stdout)
            self.assertIn("subagent of conversation agy-main", proc.stdout)

            proc = self.run_tool("prompts", *common)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Find where the Discount badge comes from.", proc.stdout)
            self.assertNotIn("USER_REQUEST", proc.stdout)
            self.assertNotIn("Unrelated badge question", proc.stdout)

            proc = self.run_tool("goals", *common)
            self.assertIn("/goal ship the badge fix", proc.stdout)

            proc = self.run_tool("search", *common, "typesense")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn('"kind": "thinking"', proc.stdout)
            self.assertIn('"kind": "tool_output"', proc.stdout)

            proc = self.run_tool("search", *common, "Trace the badge field")
            self.assertIn('"kind": "tool_call"', proc.stdout)
            self.assertIn("agy.tool_call.invoke_subagent", proc.stdout)

            proc = self.run_tool("search", *common, "--include-sidechains", "Trace the badge field")
            self.assertIn('"confidence": "best_effort"', proc.stdout)

            proc = self.run_tool("prompts", *common[:-2], "--scope", "all-projects")
            self.assertIn("Unrelated badge question", proc.stdout)


CLAUDE_ID = "1a2b3c4d-0000-4000-8000-00000000c1a0"
CODEX_ID = "01a1beef-1111-7222-8333-444455556666"


def claude_session_rows(session_id: str, project: Path, ask: str) -> list[dict]:
    return [
        {"type": "custom-title", "customTitle": "Hill climb build", "sessionId": session_id, "timestamp": now_iso()},
        {
            "type": "user",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:00:00Z",
            "message": {"role": "user", "content": f"{ask}<system-reminder>project rules</system-reminder>"},
        },
        {
            "type": "assistant",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:00:05Z",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Running the lab now."},
                    {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python3 run_lab.py", "description": "Run the lab"}},
                ],
            },
        },
        {
            "type": "user",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:10:00Z",
            "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t1", "content": "collected 24 items\n" + "." * 5000 + "\n23 of 24 scenarios passed", "is_error": True}]},
        },
        {"type": "system", "subtype": "compact_boundary", "sessionId": session_id, "timestamp": "2026-10-15T11:20:00Z"},
        {
            "type": "user",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:20:01Z",
            "isCompactSummary": True,
            "message": {"role": "user", "content": "Summary: building the hill-climb skill."},
        },
        {
            "type": "user",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:30:00Z",
            "message": {"role": "user", "content": "<system-reminder>only a reminder</system-reminder>"},
        },
        {
            "type": "assistant",
            "sessionId": session_id,
            "cwd": str(project),
            "timestamp": "2026-10-15T11:30:30Z",
            "message": {"role": "assistant", "content": [{"type": "text", "text": "Rerunning only the failing scenario."}]},
        },
    ]


class ReadAndHomeDiscoveryTests(unittest.TestCase):
    """`read` opens one session by id; Claude and Codex searches read every home on the machine."""

    run_tool = AgentHistoryScriptTests.run_tool
    make_agy_home = AgentHistoryScriptTests.make_agy_home

    def fake_home_env(self, home: Path) -> dict[str, str]:
        env = {k: v for k, v in os.environ.items() if k not in {"CLAUDE_CONFIG_DIR", "CODEX_HOME"}}
        env["HOME"] = str(home)
        return env

    def run_in_home(self, home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            env=self.fake_home_env(home),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def account_transcript(self, home: Path, account: str, session_id: str, project: Path, ask: str) -> Path:
        path = home / ".aimgr" / "claude-homes" / account / ".claude" / "projects" / "-tmp-project" / f"{session_id}.jsonl"
        write_jsonl(path, claude_session_rows(session_id, project, ask))
        return path

    def test_read_claude_session_by_prefix_in_an_account_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            self.account_transcript(home, "pro16", CLAUDE_ID, project, "Build the hill climb skill.")
            proc = self.run_in_home(home, "read", CLAUDE_ID[:8], "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            out = proc.stdout
            self.assertIn(f"session: claude {CLAUDE_ID}", out)
            self.assertIn("title: Hill climb build", out)
            self.assertIn("claude-homes/pro16", out)
            self.assertIn("| user | Build the hill climb skill.", out)
            self.assertNotIn("project rules", out)
            self.assertNotIn("only a reminder", out)
            self.assertIn("| tool call | Bash: python3 run_lab.py | Run the lab", out)
            # Long tool output keeps its end, where the result is.
            self.assertRegex(out, r"\| tool result \| error: collected 24 items .*characters cut.*23 of 24 scenarios passed")
            self.assertIn("| compaction | Summary: building the hill-climb skill.", out)
            self.assertIn(f"read {CLAUDE_ID} --after ", out)
            transcript = Path(re.search(r"readable copy: (\S+)", out).group(1)).read_text()
            self.assertIn("Rerunning only the failing scenario.", transcript)
            self.assertIn("23 of 24 scenarios passed", transcript)

            later = self.run_in_home(home, "read", CLAUDE_ID, "--after", "2026-10-15T11:20:00Z", "--output-root", str(home / "runs"))
            self.assertEqual(later.returncode, 0, later.stdout + later.stderr)
            self.assertIn("2 entries after", later.stdout)
            self.assertNotIn("Running the lab now.", later.stdout)
            self.assertIn("Rerunning only the failing scenario.", later.stdout)

    def test_read_follows_a_continued_session_back_and_lists_what_the_user_wrote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work" / "repo"
            project.mkdir(parents=True)
            (project / "AGENTS.md").write_text("repo rules\n")
            first_id = "0a1b2c3d-0000-4000-8000-0000000000a1"
            later_id = "0a1b2c3d-0000-4000-8000-0000000000b2"
            first = home / ".aimgr" / "claude-homes" / "pro1" / ".claude" / "projects" / "-tmp-project" / f"{first_id}.jsonl"
            write_jsonl(first, [
                {"type": "user", "sessionId": first_id, "cwd": str(project), "timestamp": "2026-10-15T09:00:00Z",
                 "message": {"role": "user", "content": "Test it on the version we're about to ship."}},
                {"type": "assistant", "sessionId": first_id, "cwd": str(project), "timestamp": "2026-10-15T09:00:05Z",
                 "message": {"role": "assistant", "content": [{"type": "text", "text": "Planning the release test."}]}},
            ])
            later = home / ".aimgr" / "claude-homes" / "pro2" / ".claude" / "projects" / "-tmp-project" / f"{later_id}.jsonl"
            summary = ("This session is being continued from a previous conversation that ran out of context.\n\n"
                       "Summary: prove it on the oldest app.\n\nIf you need specific details from before compaction, "
                       f"read the full transcript at: {first}")
            write_jsonl(later, [
                {"type": "user", "sessionId": later_id, "cwd": str(project), "timestamp": "2026-10-15T12:00:00Z",
                 "isCompactSummary": True, "message": {"role": "user", "content": summary}},
                {"type": "user", "sessionId": later_id, "cwd": str(project), "timestamp": "2026-10-15T12:05:00Z",
                 "message": {"role": "user", "content": "Now run the phone test.<system-reminder>rules</system-reminder>"}},
                {"type": "assistant", "sessionId": later_id, "cwd": str(project), "timestamp": "2026-10-15T12:05:10Z",
                 "message": {"role": "assistant", "content": [{"type": "text", "text": "Building the oldest app."}]}},
                {"type": "user", "sessionId": later_id, "cwd": str(project), "timestamp": "2026-10-15T12:20:00Z",
                 "message": {"role": "user", "content": "<task-notification> <status>completed</status> </task-notification>"}},
                {"type": "user", "sessionId": later_id, "cwd": str(project), "timestamp": "2026-10-15T12:30:00Z",
                 "message": {"role": "user", "content": "<command-message>paired-reviewer</command-message>\n<command-name>/paired-reviewer</command-name>\n<command-args>use flash</command-args>"}},
            ])
            memory = home / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(project)) / "memory"
            memory.mkdir(parents=True)
            (memory / "MEMORY.md").write_text("- Device QA tests head, never production\n")
            runs = str(home / "runs")

            proc = self.run_in_home(home, "read", later_id, "--output-root", runs)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn(f"continues: {first_id} {first}", proc.stdout)
            self.assertIn(f"memory: {memory}", proc.stdout)
            self.assertIn(str(project / "AGENTS.md"), proc.stdout)
            self.assertIn(f"read {later_id} --yours", proc.stdout)

            yours = self.run_in_home(home, "read", later_id, "--yours", "--output-root", runs)
            self.assertEqual(yours.returncode, 0, yours.stdout + yours.stderr)
            out = yours.stdout
            self.assertIn("3 messages from the user", out)
            ask, phone, command = (out.index(text) for text in (
                "Test it on the version we're about to ship.", "Now run the phone test.", "/paired-reviewer use flash"))
            self.assertLess(ask, phone)
            self.assertLess(phone, command)
            self.assertIn(f"| {first_id[:8]} | user |", out)
            for text in ("prove it on the oldest app", "Planning the release test.", "Building the oldest app.", "task-notification", "rules"):
                self.assertNotIn(text, out.split("readable copy:")[1])
            self.assertIn(f"read {later_id} --yours --after ", out)

            newer = self.run_in_home(home, "read", later_id, "--yours", "--after", "2026-10-15T12:10:00Z", "--output-root", runs)
            self.assertIn("1 messages from the user", newer.stdout)
            self.assertNotIn("about to ship", newer.stdout.split("readable copy:")[1])

    def test_read_includes_messages_sent_while_a_turn_was_running(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            path = home / ".claude" / "projects" / "-tmp-project" / f"{CLAUDE_ID}.jsonl"
            mid_turn = "From Amir: stop making new ones for now."
            note = "<task-notification> <status>completed</status> </task-notification>"
            write_jsonl(path, [
                {"type": "user", "sessionId": CLAUDE_ID, "cwd": str(project), "timestamp": "2026-10-18T10:00:00Z",
                 "message": {"role": "user", "content": "Run the climb."}},
                {"type": "queue-operation", "operation": "enqueue", "sessionId": CLAUDE_ID, "timestamp": "2026-10-18T10:04:00Z", "content": mid_turn},
                {"type": "queue-operation", "operation": "remove", "reason": "absorbed_mid_turn", "sessionId": CLAUDE_ID, "timestamp": "2026-10-18T10:04:05Z", "content": mid_turn},
                {"type": "queue-operation", "operation": "remove", "reason": "absorbed_mid_turn", "sessionId": CLAUDE_ID, "timestamp": "2026-10-18T10:05:00Z", "content": note},
                {"type": "queue-operation", "operation": "enqueue", "sessionId": CLAUDE_ID, "timestamp": "2026-10-18T10:06:00Z", "content": "Next turn's message."},
                {"type": "queue-operation", "operation": "dequeue", "sessionId": CLAUDE_ID, "timestamp": "2026-10-18T10:07:00Z"},
                {"type": "user", "sessionId": CLAUDE_ID, "cwd": str(project), "timestamp": "2026-10-18T10:07:00Z",
                 "message": {"role": "user", "content": "Next turn's message."}},
            ])
            yours = self.run_in_home(home, "read", CLAUDE_ID, "--yours", "--output-root", str(home / "runs"))
            self.assertEqual(yours.returncode, 0, yours.stdout + yours.stderr)
            shown = yours.stdout.split("readable copy:")[1]
            self.assertIn("3 messages from the user", yours.stdout)
            self.assertIn(mid_turn, shown)
            self.assertEqual(shown.count("Next turn's message."), 1)
            self.assertNotIn("task-notification", shown)
            full = self.run_in_home(home, "read", CLAUDE_ID, "--output-root", str(home / "runs"))
            self.assertIn(f"| user | {mid_turn}", full.stdout)
            self.assertIn("| context | <task-notification>", full.stdout)

    def test_read_names_an_earlier_session_that_is_not_on_this_machine(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            gone = "/elsewhere/projects/-tmp-project/9f8e7d6c-0000-4000-8000-0000000000c3.jsonl"
            path = home / ".claude" / "projects" / "-tmp-project" / f"{CLAUDE_ID}.jsonl"
            write_jsonl(path, [
                {"type": "user", "sessionId": CLAUDE_ID, "cwd": str(project), "timestamp": "2026-10-15T12:00:00Z",
                 "isCompactSummary": True, "message": {"role": "user", "content": f"Summary.\nread the full transcript at: {gone}"}},
                {"type": "user", "sessionId": CLAUDE_ID, "cwd": str(project), "timestamp": "2026-10-15T12:01:00Z",
                 "message": {"role": "user", "content": "Keep going."}},
            ])
            proc = self.run_in_home(home, "read", CLAUDE_ID, "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn(f"continues: 9f8e7d6c-0000-4000-8000-0000000000c3 (not on this machine: {gone})", proc.stdout)

    def test_read_picks_the_newest_copy_and_names_the_others(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            old = self.account_transcript(home, "pro1", CLAUDE_ID, project, "Old copy ask.")
            self.account_transcript(home, "pro9", CLAUDE_ID, project, "Live copy ask.")
            os.utime(old, (1_700_000_000, 1_700_000_000))
            proc = self.run_in_home(home, "read", CLAUDE_ID, "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Live copy ask.", proc.stdout)
            self.assertRegex(proc.stdout, r"transcript: \S+claude-homes/pro9/")
            self.assertRegex(proc.stdout, r"older copies: \S+claude-homes/pro1/")

    def test_read_ambiguous_prefix_lists_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            self.account_transcript(home, "pro1", CLAUDE_ID, project, "First.")
            self.account_transcript(home, "pro2", CLAUDE_ID[:8] + "-9999-4000-8000-000000000002", project, "Second.")
            proc = self.run_in_home(home, "read", CLAUDE_ID[:8], "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("2 sessions start with", proc.stdout)

            missing = self.run_in_home(home, "read", "ffffffff", "--output-root", str(home / "runs"))
            self.assertEqual(missing.returncode, 1, missing.stdout)
            self.assertIn("NO_MATCH agent-history read", missing.stdout)

    def test_read_codex_session_and_linked_codex_homes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            rollout = home / ".codex" / "sessions" / "2026" / "10" / "15" / f"rollout-2026-10-15T07-00-00-{CODEX_ID}.jsonl"
            write_jsonl(
                rollout,
                [
                    {"timestamp": now_iso(), "type": "session_meta", "payload": {"id": CODEX_ID, "cwd": str(project)}},
                    {"timestamp": now_iso(), "type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "<environment_context>cwd</environment_context>"}]}},
                    {"timestamp": now_iso(), "type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "Fix the flaky test."}]}},
                    {"timestamp": now_iso(), "type": "response_item", "payload": {"type": "function_call", "name": "exec_command", "call_id": "c1", "arguments": json.dumps({"cmd": "pytest -k flaky"})}},
                    {"timestamp": now_iso(), "type": "response_item", "payload": {"type": "function_call_output", "call_id": "c1", "output": json.dumps({"output": "1 failed"})}},
                    {"timestamp": now_iso(), "type": "response_item", "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "The test races the clock."}]}},
                ],
            )
            # AI Manager's Codex home links its sessions back to ~/.codex.
            aim = home / ".aimgr" / "codex-cli"
            aim.mkdir(parents=True)
            (aim / "sessions").symlink_to(home / ".codex" / "sessions")
            proc = self.run_in_home(home, "read", CODEX_ID[:8], "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn(f"session: codex {CODEX_ID}", proc.stdout)
            self.assertIn("| context | <environment_context>", proc.stdout)
            self.assertIn("| user | Fix the flaky test.", proc.stdout)
            self.assertIn("| tool call | exec_command: pytest -k flaky", proc.stdout)
            self.assertIn("| tool result | 1 failed", proc.stdout)
            self.assertNotIn("older copies", proc.stdout)

    def test_read_agy_conversation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, other = root / "project", root / "other"
            project.mkdir()
            other.mkdir()
            agy_home = self.make_agy_home(root, project, other)
            target = agy_home / "brain" / "agy-main-0000-4000-8000-000000000000"
            (agy_home / "brain" / "agy-main").rename(target)
            proc = self.run_tool("read", "agy-main-0000", "--runtime", "agy", "--agy-home", str(agy_home), "--output-root", str(root / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("| user | Find where the Discount badge comes from.", proc.stdout)
            self.assertIn("| tool call | invoke_subagent", proc.stdout)
            self.assertIn("| tool result | Subagent reply", proc.stdout)

    def test_claude_searches_read_every_account_home_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home, project = Path(tmp), Path(tmp) / "project"
            project.mkdir()
            recent = [dict(row, timestamp=now_iso()) for row in claude_session_rows(CLAUDE_ID, project, "Ask from pro3.")]
            write_jsonl(home / ".aimgr" / "claude-homes" / "pro3" / ".claude" / "projects" / "-tmp-project" / f"{CLAUDE_ID}.jsonl", recent)
            other_id = "2b3c4d5e-0000-4000-8000-00000000c1a0"
            recent2 = [dict(row, timestamp=now_iso()) for row in claude_session_rows(other_id, project, "Ask from boss.")]
            write_jsonl(home / ".aimgr" / "claude-homes" / "boss" / ".claude" / "projects" / "-tmp-project" / f"{other_id}.jsonl", recent2)
            stale = home / ".claude" / "projects" / "-tmp-project" / "3c4d5e6f-0000-4000-8000-00000000c1a0.jsonl"
            write_jsonl(stale, [dict(row, timestamp=now_iso()) for row in claude_session_rows("3c4d5e6f-0000-4000-8000-00000000c1a0", project, "Ask from an untouched file.")])
            os.utime(stale, (1_700_000_000, 1_700_000_000))

            proc = self.run_in_home(home, "prompts", "--runtime", "claude", "--cwd", str(project), "--output-root", str(home / "runs"))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Ask from pro3.", proc.stdout)
            self.assertIn("Ask from boss.", proc.stdout)
            # A file last written before the window opened is not read at all.
            self.assertNotIn("untouched file", proc.stdout)

            narrowed = self.run_in_home(
                home, "prompts", "--runtime", "claude", "--cwd", str(project),
                "--claude-home", str(home / ".aimgr" / "claude-homes" / "boss" / ".claude"),
                "--output-root", str(home / "runs"),
            )
            self.assertIn("Ask from boss.", narrowed.stdout)
            self.assertNotIn("Ask from pro3.", narrowed.stdout)


if __name__ == "__main__":
    unittest.main()
