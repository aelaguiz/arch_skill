from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("render_codex_table.py")


class RenderCodexTableTests(unittest.TestCase):
    def run_renderer(
        self,
        payload: object | None = None,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        input_text = None if payload is None else json.dumps(payload)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
        if check and proc.returncode != 0:
            self.fail(
                f"renderer failed with {proc.returncode}\n"
                f"stdout:\n{proc.stdout}\n"
                f"stderr:\n{proc.stderr}"
            )
        return proc

    def test_direct_python_self_test_bootstraps_dependencies(self) -> None:
        proc = self.run_renderer(None, "--self-test")
        self.assertIn("OK render_codex_table self-test", proc.stdout)

    @unittest.skipUnless(shutil.which("uv"), "uv is required for explicit script mode")
    def test_uv_script_self_test(self) -> None:
        proc = subprocess.run(
            ["uv", "--quiet", "run", "--script", str(SCRIPT), "--self-test"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("OK render_codex_table self-test", proc.stdout)

    def test_short_metric_table_renders_without_ansi_or_width_overflow(self) -> None:
        payload = {
            "title": "Metric Snapshot",
            "columns": [
                {"key": "metric", "label": "Metric"},
                {"key": "value", "label": "Value", "justify": "right", "kind": "number"},
                {"key": "meaning", "label": "Meaning"},
            ],
            "rows": [
                {
                    "metric": "AIVAT lift",
                    "value": "+3.2",
                    "meaning": "RTS won after noise reduction",
                },
                {
                    "metric": "CI width",
                    "value": "8.4",
                    "meaning": "Evidence is still noisy",
                },
            ],
        }
        proc = self.run_renderer(payload, "--width", "88")
        self.assertIn("Metric Snapshot", proc.stdout)
        self.assertIn("AIVAT lift", proc.stdout)
        self.assertNotIn("\x1b[", proc.stdout)
        for line in proc.stdout.splitlines():
            self.assertLessEqual(len(line), 88, line)

    def test_grouped_tables_render_as_separate_tables(self) -> None:
        payload = {
            "tables": [
                {
                    "title": "Keep",
                    "columns": ["Case", "Why"],
                    "rows": [["Metrics", "Short repeated values"]],
                },
                {
                    "title": "Avoid",
                    "columns": ["Case", "Why"],
                    "rows": [["Long prose", "Wraps into unreadable blocks"]],
                },
            ]
        }
        proc = self.run_renderer(payload)
        self.assertIn("Keep", proc.stdout)
        self.assertIn("Avoid", proc.stdout)
        self.assertIn("\n\n", proc.stdout)

    def test_rejects_too_many_columns(self) -> None:
        payload = {
            "columns": ["A", "B", "C", "D", "E", "F"],
            "rows": [["1", "2", "3", "4", "5", "6"]],
        }
        proc = self.run_renderer(payload, check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("NO_TABLE:", proc.stderr)
        self.assertIn("too wide", proc.stderr)

    def test_rejects_long_paragraph_cell(self) -> None:
        payload = {
            "columns": ["Area", "Meaning"],
            "rows": [
                [
                    "Runtime",
                    "This cell is a long explanatory paragraph that will wrap repeatedly and make the user reconstruct the row instead of understanding the point.",
                ]
            ],
        }
        proc = self.run_renderer(payload, check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("NO_TABLE:", proc.stderr)

    def test_rejects_multiline_cell(self) -> None:
        payload = {
            "columns": ["Area", "Meaning"],
            "rows": [["Runtime", "first line\nsecond line"]],
        }
        proc = self.run_renderer(payload, check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("contains a newline", proc.stderr)

    def test_rejects_markdown_pipe_table_input(self) -> None:
        proc = self.run_renderer("| A | B |\n|---|---|", check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Markdown pipe tables", proc.stderr)

    def test_rejects_pattern_consolidation_sweep_shape(self) -> None:
        payload = {
            "columns": [
                "Area",
                "File / Symbol",
                "Pattern to adopt",
                "Why (drift prevented)",
                "Proposed scope (include/defer/exclude/blocker question)",
            ],
            "rows": [
                [
                    "Shared per-kind doctrine",
                    "shared/prompts/playable_kind_selection_contract/AGENTS.prompt",
                    "One shared contract emitted into every kind skill",
                    "Prevents 32 packages from drifting on evidence posture, label-shim language, and not-good-for semantics",
                    "include",
                ]
            ],
        }
        proc = self.run_renderer(payload, check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("NO_TABLE:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
