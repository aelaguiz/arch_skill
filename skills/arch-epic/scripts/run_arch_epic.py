#!/usr/bin/env python3
"""arch-epic orchestration plumbing.

This script is deterministic infrastructure for the arch-epic skill.
It does NOT make judgments about decomposition, scope changes,
verdicts, or routing. Those decisions live in the orchestrator's
prose reasoning.

Current subcommand:

  critic-spawn   Spawn a fresh ephemeral critic sub-session (claude
                 or codex), capture the EpicVerdict JSON, and write
                 run-directory artifacts.

The script exits non-zero with a plain-English message whenever its
expected output shape does not appear. It never swallows errors.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _die(msg: str, code: int = 2) -> None:
    print(f"run_arch_epic: {msg}", file=sys.stderr)
    sys.exit(code)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _write_invocation_sh(path: Path, argv: list[str], cwd: str | None) -> None:
    def quote(s: str) -> str:
        return "'" + s.replace("'", "'\\''") + "'"

    line = " ".join(quote(a) for a in argv)
    prefix = f"cd {quote(cwd)} && " if cwd else ""
    _write_text(
        path, "#!/bin/sh\n" + prefix + "exec " + line + " < /dev/null\n"
    )
    path.chmod(0o755)


def _run_subprocess(
    argv: list[str],
    stdout_stream_path: Path,
    out_dir: Path,
    cwd: str | None = None,
) -> tuple[int, str]:
    """Run a subprocess with stdin closed. Combined stdout+stderr
    is captured both to memory and to `stdout_stream_path`.
    """
    _write_text(out_dir / "start_ts", _utc_now_iso())
    with open(os.devnull, "rb") as devnull, open(stdout_stream_path, "wb") as out:
        proc = subprocess.run(
            argv,
            stdin=devnull,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            check=False,
        )
        out.write(proc.stdout)
    _write_text(out_dir / "end_ts", _utc_now_iso())
    _write_text(out_dir / "exit_code", str(proc.returncode) + "\n")
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def _parse_claude_final_json(stdout_text: str) -> dict | None:
    """Claude -p --output-format json prints a single JSON object
    at the end of stdout.
    """
    try:
        return json.loads(stdout_text.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return None


def _extract_claude_structured_verdict(final: dict) -> dict | None:
    """Return the critic's structured verdict from a Claude `-p --output-format
    json --json-schema ...` response.

    Claude populates `structured_output` reliably when the model answers
    in one shot. When the critic uses tools (reading files) before
    answering, Claude sometimes returns the conforming JSON as text in
    `result` (often wrapped in ```json fences). Accept either path.
    """
    so = final.get("structured_output")
    if isinstance(so, dict):
        return so
    result = final.get("result")
    if not isinstance(result, str):
        return None
    text = result.strip()
    if text.startswith("```"):
        # strip opening fence (with optional language tag) and closing fence
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        obj = json.loads(text.strip())
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _slugify(name: str) -> str:
    out = []
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in ("_", "-", " "):
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "sub-plan"


def cmd_critic_spawn(args: argparse.Namespace) -> int:
    epic_doc = Path(args.epic_doc).resolve()
    if not epic_doc.is_file():
        _die(f"epic doc not found: {epic_doc}")

    sub_plan_doc_path = Path(args.sub_plan_doc_path).resolve()
    if not sub_plan_doc_path.is_file():
        _die(f"sub-plan doc not found: {sub_plan_doc_path}")

    schema_path = Path(args.schema_file).resolve()
    if not schema_path.is_file():
        _die(f"critic schema file not found: {schema_path}")

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    orch_root = Path(args.orchestrator_root).resolve() if args.orchestrator_root else Path.cwd()
    if not orch_root.is_dir():
        _die(f"orchestrator root is not a directory: {orch_root}")

    slug = _slugify(args.sub_plan_name)
    run_id = _utc_now_stamp()
    run_dir = orch_root / ".arch_skill" / "arch-epic" / "critics" / slug / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=False)

    # ensure .arch_skill/ is gitignored in the orchestrator repo
    gi = orch_root / ".gitignore"
    marker = ".arch_skill/"
    if gi.exists():
        lines = gi.read_text(encoding="utf-8").splitlines()
        if marker not in lines:
            with gi.open("a", encoding="utf-8") as f:
                f.write(f"\n{marker}\n")
    else:
        gi.write_text(f"{marker}\n", encoding="utf-8")

    _write_text(run_dir / "prompt.md", prompt)

    final_path = run_dir / "stdout.final.json"
    stream_path = run_dir / "stream.log"
    verdict_path = run_dir / "verdict.json"

    if args.runtime == "claude":
        # Claude's --json-schema is flaky on multi-line pretty-printed
        # JSON (model may emit prose-wrapped JSON in `result` instead of
        # populating `structured_output`). Minify the schema.
        schema_inline = json.dumps(
            json.loads(schema_path.read_text(encoding="utf-8")),
            separators=(",", ":"),
        )
        argv = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--settings",
            '{"disableAllHooks":true}',
            "--model",
            args.model,
            "--effort",
            args.effort,
            "--json-schema",
            schema_inline,
            prompt,
        ]
        subprocess_cwd = str(orch_root)
    elif args.runtime == "codex":
        argv = [
            "codex",
            "exec",
            "--cd",
            str(orch_root),
            "--ephemeral",
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "--model",
            args.model,
            "-c",
            f'model_reasoning_effort="{args.effort}"',
            "--output-schema",
            str(schema_path),
            "--json",
            "-o",
            str(final_path),
            prompt,
        ]
        subprocess_cwd = None
    else:
        _die(f"unknown runtime: {args.runtime}")

    _write_invocation_sh(run_dir / "invocation.sh", argv, subprocess_cwd)
    code, stdout_text = _run_subprocess(
        argv, stream_path, run_dir, cwd=subprocess_cwd
    )

    if args.runtime == "claude":
        final = _parse_claude_final_json(stdout_text)
        if final is None:
            _die(
                "claude stdout did not parse as JSON; see stream.log",
                code=3,
            )
        _write_json(final_path, final)
        verdict = _extract_claude_structured_verdict(final)
        if verdict is None:
            _die(
                "claude critic produced no schema-conforming JSON in structured_output or result; see stdout.final.json",
                code=5,
            )
        _write_json(verdict_path, verdict)
    else:
        if not final_path.is_file():
            _die(
                f"codex critic did not write -o file: {final_path}",
                code=5,
            )
        try:
            verdict = json.loads(final_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            _die(f"codex critic output is not valid JSON: {e}", code=5)
        _write_json(verdict_path, verdict)

    print(str(verdict_path))
    return 0 if code == 0 else code


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_arch_epic")
    sub = p.add_subparsers(dest="cmd", required=True)

    critic = sub.add_parser(
        "critic-spawn",
        help="Spawn a fresh ephemeral critic sub-session",
    )
    for a in [
        "--epic-doc",
        "--sub-plan-name",
        "--sub-plan-doc-path",
        "--prompt-file",
        "--schema-file",
        "--model",
        "--effort",
    ]:
        critic.add_argument(a, required=True)
    critic.add_argument(
        "--runtime", required=True, choices=["claude", "codex"]
    )
    critic.add_argument(
        "--orchestrator-root",
        required=False,
        default=None,
        help="Root where .arch_skill/arch-epic/critics/<slug>/run-<ts>/ lives. Defaults to cwd.",
    )
    critic.set_defaults(func=cmd_critic_spawn)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
