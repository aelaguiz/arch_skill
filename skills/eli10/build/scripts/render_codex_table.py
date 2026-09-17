# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "rich>=13.7,<15",
# ]
# ///
"""Render Codex-safe Unicode tables for the eli10 skill.

This script is intentionally self-contained. Direct `python3` invocation
re-execs through `uv --quiet run --script` when Rich is not already importable.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import unicodedata
from io import StringIO
from pathlib import Path
from typing import Any


BOOTSTRAP_ENV = "ELI10_RENDER_CODEX_TABLE_BOOTSTRAPPED"


def _ensure_rich() -> None:
    try:
        import rich  # noqa: F401
    except ModuleNotFoundError as exc:
        if exc.name != "rich":
            raise
        if os.environ.get(BOOTSTRAP_ENV) == "1":
            print(
                "ERROR: rich is still unavailable after uv bootstrap.",
                file=sys.stderr,
            )
            raise SystemExit(2) from exc
        uv = shutil.which("uv")
        if uv is None:
            print(
                "ERROR: rich is required and uv is not on PATH. "
                "Install uv, then rerun this script.",
                file=sys.stderr,
            )
            raise SystemExit(2) from exc
        env = os.environ.copy()
        env[BOOTSTRAP_ENV] = "1"
        os.execvpe(
            uv,
            [
                uv,
                "--quiet",
                "run",
                "--script",
                str(Path(__file__).resolve()),
                *sys.argv[1:],
            ],
            env,
        )


_ensure_rich()

from rich import box  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402


DEFAULT_WIDTH = 88
MAX_COLUMNS = 5
MIN_ESTIMATED_COLUMN_WIDTH = 14
MAX_ROWS_PER_TABLE = 12
MAX_CELL_WIDTH = 72
MAX_PATH_OR_CODE_CELL_WIDTH = 96
MAX_ESTIMATED_WRAP_LINES = 2
MAX_WORDS_PER_CELL = 14


class TableRejected(ValueError):
    """Raised when a requested table would be less readable than prose."""


def display_width(value: str) -> int:
    total = 0
    for char in value:
        if unicodedata.combining(char):
            continue
        total += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return total


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def normalize_columns(raw_columns: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_columns, list) or not raw_columns:
        raise TableRejected("missing columns")

    columns: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_columns):
        if isinstance(raw, str):
            key = raw
            label = raw
            justify = "left"
            kind = "text"
        elif isinstance(raw, dict):
            key = raw.get("key") or raw.get("label")
            label = raw.get("label") or key
            justify = raw.get("justify", "left")
            kind = raw.get("kind", "text")
        else:
            raise TableRejected(f"column {index + 1} is not a string or object")

        if not key or not label:
            raise TableRejected(f"column {index + 1} is missing key/label")
        if justify not in {"left", "center", "right"}:
            raise TableRejected(f"column {label!r} has unsupported justify")
        if kind not in {"text", "path", "code", "number"}:
            raise TableRejected(f"column {label!r} has unsupported kind")

        columns.append(
            {
                "key": str(key),
                "label": str(label),
                "justify": justify,
                "kind": kind,
            }
        )

    if len(columns) > MAX_COLUMNS:
        raise TableRejected(
            f"{len(columns)} columns is too wide; split into smaller grouped tables"
        )
    return columns


def normalize_rows(raw_rows: Any, columns: list[dict[str, Any]]) -> list[list[str]]:
    if not isinstance(raw_rows, list):
        raise TableRejected("rows must be a list")
    if len(raw_rows) > MAX_ROWS_PER_TABLE:
        raise TableRejected(
            f"{len(raw_rows)} rows is too many for one table; split into grouped tables"
        )

    rows: list[list[str]] = []
    keys = [column["key"] for column in columns]
    for row_index, raw_row in enumerate(raw_rows):
        if isinstance(raw_row, dict):
            row = [normalize_cell(raw_row.get(key, "")) for key in keys]
        elif isinstance(raw_row, list):
            if len(raw_row) != len(columns):
                raise TableRejected(
                    f"row {row_index + 1} has {len(raw_row)} cells; "
                    f"expected {len(columns)}"
                )
            row = [normalize_cell(cell) for cell in raw_row]
        else:
            raise TableRejected(f"row {row_index + 1} is not an object or list")
        rows.append(row)
    return rows


def is_markdown_table_like(payload: Any) -> bool:
    if isinstance(payload, str):
        lines = [line.strip() for line in payload.splitlines() if line.strip()]
        return any(line.startswith("|") and line.endswith("|") for line in lines)
    if isinstance(payload, dict):
        return any(is_markdown_table_like(value) for value in payload.values())
    if isinstance(payload, list):
        return any(is_markdown_table_like(value) for value in payload)
    return False


def estimated_content_width(total_width: int, column_count: int) -> int:
    # Rich adds borders and horizontal padding. This conservative estimate
    # prevents tables that technically render but become thin wrapped columns.
    return total_width - (column_count + 1) - (2 * column_count)


def validate_cell(
    cell: str,
    column: dict[str, Any],
    estimated_column_width: int,
    row_number: int | None = None,
) -> None:
    label = column["label"]
    cell_name = f"{label}"
    if row_number is not None:
        cell_name = f"row {row_number}, {label}"

    if "\n" in cell or "\r" in cell:
        raise TableRejected(f"{cell_name} contains a newline; use a block instead")

    width = display_width(cell)
    max_width = (
        MAX_PATH_OR_CODE_CELL_WIDTH
        if column["kind"] in {"path", "code"}
        else MAX_CELL_WIDTH
    )
    if width > max_width:
        raise TableRejected(
            f"{cell_name} is {width} columns wide; use bullets or a proof block"
        )

    words = [word for word in cell.split() if word]
    if column["kind"] == "text" and len(words) > MAX_WORDS_PER_CELL:
        raise TableRejected(
            f"{cell_name} has {len(words)} words; table cells should stay short"
        )

    if estimated_column_width <= 0:
        raise TableRejected("computed table width is invalid")
    estimated_lines = max(1, math.ceil(width / estimated_column_width))
    if estimated_lines > MAX_ESTIMATED_WRAP_LINES:
        raise TableRejected(
            f"{cell_name} would wrap to about {estimated_lines} lines; "
            "use grouped prose instead"
        )


def validate_table_spec(table_spec: dict[str, Any], width: int) -> tuple[str | None, list[dict[str, Any]], list[list[str]]]:
    columns = normalize_columns(table_spec.get("columns"))
    rows = normalize_rows(table_spec.get("rows", []), columns)

    content_width = estimated_content_width(width, len(columns))
    estimated_column_width = content_width // len(columns)
    if estimated_column_width < MIN_ESTIMATED_COLUMN_WIDTH:
        raise TableRejected(
            f"{len(columns)} columns leaves only about {estimated_column_width} "
            "columns per cell; split the table"
        )

    for column in columns:
        validate_cell(column["label"], column, estimated_column_width)

    for row_number, row in enumerate(rows, start=1):
        row_width_sum = sum(display_width(cell) for cell in row)
        long_cell_count = sum(1 for cell in row if display_width(cell) > 40)
        if len(columns) >= 5 and (long_cell_count >= 2 or row_width_sum > width):
            raise TableRejected(
                "wide audit-matrix shape detected; group by decision/status instead"
            )
        for column, cell in zip(columns, row, strict=True):
            validate_cell(cell, column, estimated_column_width, row_number)

    title = table_spec.get("title")
    if title is not None:
        title = str(title)
        if display_width(title) > width - 4:
            raise TableRejected("title is wider than the table")
    return title, columns, rows


def render_one_table(table_spec: dict[str, Any], width: int) -> str:
    title, columns, rows = validate_table_spec(table_spec, width)
    table = Table(
        title=title,
        box=getattr(box, "ROUNDED", box.SIMPLE),
        show_header=True,
        header_style="",
        expand=False,
    )

    for column in columns:
        table.add_column(
            column["label"],
            justify=column["justify"],
            no_wrap=False,
            overflow="fold",
        )
    for row in rows:
        table.add_row(*row)

    output = StringIO()
    console = Console(
        file=output,
        width=width,
        force_terminal=False,
        color_system=None,
        no_color=True,
        highlight=False,
        soft_wrap=False,
    )
    console.print(table)
    rendered = output.getvalue().rstrip()

    too_wide = [line for line in rendered.splitlines() if display_width(line) > width]
    if too_wide:
        raise TableRejected("rendered output exceeded configured width")
    return rendered


def normalize_payload(raw: Any) -> list[dict[str, Any]]:
    if is_markdown_table_like(raw):
        raise TableRejected("Markdown pipe tables are not Codex-safe input")
    if not isinstance(raw, dict):
        raise TableRejected("input must be a JSON object")
    if "tables" in raw:
        tables = raw["tables"]
        if not isinstance(tables, list) or not tables:
            raise TableRejected("tables must be a non-empty list")
        if len(tables) > 6:
            raise TableRejected("too many grouped tables; use sections instead")
        if not all(isinstance(table, dict) for table in tables):
            raise TableRejected("each grouped table must be an object")
        return tables
    return [raw]


def render_payload(raw: Any, width: int) -> str:
    rendered_tables = [render_one_table(table, width) for table in normalize_payload(raw)]
    return "\n\n".join(rendered_tables)


def load_json(args: argparse.Namespace) -> Any:
    if args.input:
        return json.loads(Path(args.input).read_text(encoding="utf-8"))
    text = sys.stdin.read()
    if not text.strip():
        raise TableRejected("no JSON input provided")
    return json.loads(text)


def run_self_test(width: int) -> None:
    good = {
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
    rendered = render_payload(good, width)
    if "\x1b[" in rendered:
        raise AssertionError("ANSI escape sequence found")
    if any(display_width(line) > width for line in rendered.splitlines()):
        raise AssertionError("rendered line exceeded width")

    bad = {
        "columns": ["Area", "File / Symbol", "Pattern to adopt", "Why", "Scope"],
        "rows": [
            [
                "Shared per-kind doctrine",
                "shared/prompts/playable_kind_selection_contract/AGENTS.prompt",
                "One shared contract emitted into every kind skill",
                "Prevents 32 packages from drifting on evidence posture and label-shim language",
                "include",
            ]
        ],
    }
    try:
        render_payload(bad, width)
    except TableRejected:
        pass
    else:
        raise AssertionError("wide audit matrix was not rejected")
    print("OK render_codex_table self-test")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render short Unicode tables that stay readable inside Codex.",
    )
    parser.add_argument("--input", help="Read table JSON from this path instead of stdin.")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.width < 48:
        print("NO_TABLE: width is too narrow for readable tables", file=sys.stderr)
        return 1

    try:
        if args.self_test:
            run_self_test(args.width)
            return 0
        payload = load_json(args)
        print(render_payload(payload, args.width))
        return 0
    except json.JSONDecodeError as exc:
        print(f"NO_TABLE: invalid JSON: {exc}", file=sys.stderr)
        return 1
    except TableRejected as exc:
        print(f"NO_TABLE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
