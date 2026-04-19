#!/usr/bin/env python3
"""Deterministic runner for the `code-review` skill.

Resolves a review target, builds per-lens prompts from the canonical references,
launches parallel fresh Codex subprocess reviewers (gpt-5.4-mini xhigh for each
lens, gpt-5.4 xhigh for the final synthesis), validates outputs against the
output contract, and writes all artifacts under a namespaced run directory.

This runner is review-only. It never modifies the reviewed repo and never asks
the caller model to be the reviewer.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as _dt
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = PACKAGE_DIR / "references"
REVIEWER_PROMPT_FILE = REFERENCES_DIR / "reviewer-prompt.md"
REQUIREMENTS_FILE = REFERENCES_DIR / "review-requirements.md"
OUTPUT_CONTRACT_FILE = REFERENCES_DIR / "output-contract.md"

LENS_MODEL = "gpt-5.4-mini"
SYNTHESIS_MODEL = "gpt-5.4"
REASONING_EFFORT = "xhigh"

ALWAYS_REQUIRED_LENSES = ("correctness", "architecture", "proof", "docs-drift", "security")
CONDITIONAL_LENS_AGENT_LINTER = "agent-linter"

AGENT_SURFACE_PATTERNS = (
    re.compile(r"(^|/)skills/"),
    re.compile(r"(^|/)agents/"),
    re.compile(r"(^|/)\.github/claude/"),
    re.compile(r"(^|/)prompts/"),
    re.compile(r"(^|/)(AGENTS\.md|CLAUDE\.md|SKILL\.md|agent\.md|prompt\.md)$"),
    re.compile(r"\.(prompt|skill)\.md$"),
    re.compile(r"(^|/)[^/]*agent[^/]*$", re.IGNORECASE),
    re.compile(r"(^|/)[^/]*prompt[^/]*$", re.IGNORECASE),
    re.compile(r"(^|/)[^/]*skill[^/]*$", re.IGNORECASE),
)

REPO_LOCAL_CANDIDATES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    ".editorconfig",
    ".eslintrc.json",
    ".eslintrc.js",
    ".prettierrc",
    ".prettierrc.json",
    "ruff.toml",
    "pyproject.toml",
    ".flake8",
    ".rubocop.yml",
    "rustfmt.toml",
    "clippy.toml",
    "Cargo.toml",
    "go.mod",
    ".golangci.yml",
    "tsconfig.json",
    ".github/claude",
)


@dataclass
class ReviewTarget:
    mode: str
    base: str | None = None
    head: str | None = None
    paths: list[str] = field(default_factory=list)
    claim_doc: str | None = None
    claim_phase: int | None = None

    def describe(self) -> str:
        if self.mode == "uncommitted-diff":
            return "uncommitted diff (worktree + staged) against HEAD"
        if self.mode == "branch-diff":
            return f"branch diff {self.base}...{self.head}"
        if self.mode == "commit-range":
            return f"commit range {self.base}..{self.head}"
        if self.mode == "paths":
            return f"paths: {', '.join(self.paths)}"
        if self.mode == "completion-claim":
            return (
                f"completion-claim: {self.claim_doc}"
                + (f" phase {self.claim_phase}" if self.claim_phase is not None else "")
            )
        raise RunnerError(f"unsupported target mode: {self.mode}")

    def commands_block(self, repo_root: Path) -> str:
        if self.mode == "uncommitted-diff":
            lines = [
                "git -C {root} status --short".format(root=shlex.quote(str(repo_root))),
                "git -C {root} diff --unified=3 HEAD".format(root=shlex.quote(str(repo_root))),
            ]
        elif self.mode == "branch-diff":
            lines = [
                "git -C {root} diff --unified=3 {base}...{head}".format(
                    root=shlex.quote(str(repo_root)),
                    base=shlex.quote(self.base or ""),
                    head=shlex.quote(self.head or ""),
                ),
                "git -C {root} log --oneline {base}...{head}".format(
                    root=shlex.quote(str(repo_root)),
                    base=shlex.quote(self.base or ""),
                    head=shlex.quote(self.head or ""),
                ),
            ]
        elif self.mode == "commit-range":
            lines = [
                "git -C {root} log -p {base}..{head}".format(
                    root=shlex.quote(str(repo_root)),
                    base=shlex.quote(self.base or ""),
                    head=shlex.quote(self.head or ""),
                ),
            ]
        elif self.mode == "paths":
            quoted = " ".join(shlex.quote(p) for p in self.paths)
            lines = [
                f"ls {quoted}",
                f"cat {quoted}",
            ]
        elif self.mode == "completion-claim":
            lines = [
                f"cat {shlex.quote(self.claim_doc or '')}",
                "git -C {root} log --oneline -n 40".format(root=shlex.quote(str(repo_root))),
                "git -C {root} diff --unified=3 HEAD~10 HEAD".format(root=shlex.quote(str(repo_root))),
            ]
        else:
            raise RunnerError(f"unsupported target mode: {self.mode}")
        return "\n".join(f"  - `{line}`" for line in lines)


class RunnerError(RuntimeError):
    pass


def die(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="run_code_review.py",
        description="Run a fresh unsandboxed Codex code review (see skills/code-review/references/invocation.md).",
    )
    p.add_argument("--repo-root", required=True, help="Absolute path to the repository root.")
    p.add_argument(
        "--target",
        required=True,
        choices=("uncommitted-diff", "branch-diff", "commit-range", "paths", "completion-claim"),
    )
    p.add_argument("--base", default=None)
    p.add_argument("--head", default=None)
    p.add_argument("--paths", nargs="+", default=None)
    p.add_argument("--claim-doc", default=None)
    p.add_argument("--claim-phase", type=int, default=None)
    p.add_argument("--objective", default="")
    p.add_argument("--output-root", default="/tmp/code-review")
    p.add_argument("--run-dir", default=None, help="Explicit run directory; overrides --output-root.")
    p.add_argument("--host-runtime", default=None, choices=(None, "codex", "claude"))
    p.add_argument(
        "--codex-binary",
        default=None,
        help="Override codex binary path (defaults to `codex` on PATH).",
    )
    p.add_argument(
        "--force-agent-linter",
        action="store_true",
        help="Require agent-linter lens regardless of target detection.",
    )
    p.add_argument(
        "--skip-execution",
        action="store_true",
        help="Prepare the run directory and prompts but do not launch Codex subprocesses. Intended for tests.",
    )
    return p.parse_args(argv)


def resolve_target(ns: argparse.Namespace) -> ReviewTarget:
    mode = ns.target
    if mode == "branch-diff":
        if not ns.base or not ns.head:
            die("branch-diff requires --base and --head")
    if mode == "commit-range":
        if not ns.base or not ns.head:
            die("commit-range requires --base and --head")
    if mode == "paths":
        if not ns.paths:
            die("paths requires --paths with at least one entry")
    if mode == "completion-claim":
        if not ns.claim_doc:
            die("completion-claim requires --claim-doc")
    return ReviewTarget(
        mode=mode,
        base=ns.base,
        head=ns.head,
        paths=list(ns.paths or []),
        claim_doc=ns.claim_doc,
        claim_phase=ns.claim_phase,
    )


def resolve_codex_binary(override: str | None) -> str:
    if override:
        if not Path(override).exists():
            die(f"codex binary not found at --codex-binary path: {override}")
        return override
    which = shutil.which("codex")
    if not which:
        die("codex binary not found on PATH")
    return which


def capture_diff(target: ReviewTarget, repo_root: Path) -> str:
    def _run(cmd: list[str]) -> str:
        proc = subprocess.run(
            cmd, cwd=repo_root, capture_output=True, text=True, check=False
        )
        if proc.returncode != 0 and proc.returncode != 1:
            raise RunnerError(
                f"git command failed: {' '.join(shlex.quote(c) for c in cmd)}\n"
                f"stderr: {proc.stderr.strip()}"
            )
        return proc.stdout

    if target.mode == "uncommitted-diff":
        return _run(["git", "diff", "--unified=3", "HEAD"])
    if target.mode == "branch-diff":
        return _run(["git", "diff", "--unified=3", f"{target.base}...{target.head}"])
    if target.mode == "commit-range":
        return _run(["git", "log", "-p", f"{target.base}..{target.head}"])
    if target.mode == "paths":
        parts = []
        for p in target.paths:
            full = repo_root / p
            if not full.exists():
                raise RunnerError(f"path not found: {p}")
            parts.append(f"=== {p} ===\n")
            if full.is_file():
                parts.append(full.read_text(errors="replace"))
            else:
                parts.append(f"(directory; see contents under {p})\n")
        return "".join(parts)
    if target.mode == "completion-claim":
        if not target.claim_doc:
            raise RunnerError("completion-claim missing --claim-doc")
        full = repo_root / target.claim_doc
        if not full.exists():
            raise RunnerError(f"claim doc not found: {target.claim_doc}")
        return full.read_text(errors="replace")
    raise RunnerError(f"unsupported target mode: {target.mode}")


def changed_paths(target: ReviewTarget, repo_root: Path, captured: str) -> list[str]:
    if target.mode == "paths":
        return list(target.paths)
    paths: list[str] = []
    seen: set[str] = set()
    for line in captured.splitlines():
        if line.startswith("+++ b/") or line.startswith("--- a/"):
            path = line[6:].strip()
            if path and path != "/dev/null" and path not in seen:
                seen.add(path)
                paths.append(path)
        elif line.startswith("diff --git "):
            parts = line.split()
            for token in parts[2:]:
                if token.startswith("a/") or token.startswith("b/"):
                    path = token[2:]
                    if path and path not in seen:
                        seen.add(path)
                        paths.append(path)
    return paths


def detect_agent_surface(paths: Iterable[str]) -> bool:
    for raw in paths:
        p = raw.replace("\\", "/")
        for pattern in AGENT_SURFACE_PATTERNS:
            if pattern.search(p):
                return True
    return False


def discover_repo_local_sources(repo_root: Path) -> list[str]:
    found: list[str] = []
    for candidate in REPO_LOCAL_CANDIDATES:
        full = repo_root / candidate
        if full.exists():
            found.append(candidate)
    return found


def make_run_dir(output_root: Path, explicit: Path | None, target: ReviewTarget) -> Path:
    if explicit:
        explicit.mkdir(parents=True, exist_ok=True)
        return explicit
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    hashed = hashlib.sha256(json.dumps(asdict(target), sort_keys=True).encode()).hexdigest()[:8]
    nonce = uuid.uuid4().hex[:8]
    run_dir = output_root / f"{ts}_{hashed}_{nonce}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def copy_references(run_dir: Path) -> dict[str, Path]:
    refs_dir = run_dir / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    copied: dict[str, Path] = {}
    for src in (REVIEWER_PROMPT_FILE, REQUIREMENTS_FILE, OUTPUT_CONTRACT_FILE):
        dst = refs_dir / src.name
        shutil.copy2(src, dst)
        copied[src.name] = dst
    return copied


def write_target_artifacts(run_dir: Path, target: ReviewTarget, captured: str, paths: list[str]) -> None:
    target_dir = run_dir / "target"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "target.json").write_text(json.dumps(asdict(target), indent=2) + "\n")
    (target_dir / "diff.patch").write_text(captured)
    (target_dir / "paths.txt").write_text("\n".join(paths) + ("\n" if paths else ""))


def required_lenses(agent_surface: bool, force_agent_linter: bool) -> list[str]:
    lenses = list(ALWAYS_REQUIRED_LENSES)
    if agent_surface or force_agent_linter:
        lenses.append(CONDITIONAL_LENS_AGENT_LINTER)
    return lenses


def render_lens_prompt(
    lens: str,
    repo_root: Path,
    target: ReviewTarget,
    objective: str,
    repo_local_sources: list[str],
    refs: dict[str, Path],
) -> str:
    sources_block = "\n".join(f"  - `{s}`" for s in repo_local_sources) if repo_local_sources else "  - (none found)"
    objective_block = objective.strip() if objective else "(none)"
    return f"""You are an independent code reviewer owning the `{lens}` lens for a broader code review. You have no memory of any prior session. Read repo truth directly from the filesystem. Return findings only for risks your lens owns.

# Canonical references (read before emitting output)
- Reviewer prompt contract: `{refs['reviewer-prompt.md']}`
- Review requirements: `{refs['review-requirements.md']}`
- Output contract: `{refs['output-contract.md']}`

Follow the `Lens prompt template` in the reviewer prompt contract for lens `{lens}`. Apply the per-lens scope paragraph for `{lens}`. Obey the output contract's lens output shape — not the synthesis shape.

# Ground truth
- Working directory: `{repo_root}`
- Review target: {target.describe()}
- Objective (if any): {objective_block}
- Commands that show the changed code:
{target.commands_block(repo_root)}
- Repo-local convention sources to consult first:
{sources_block}
- Diff/target artifacts already captured in this run: `{repo_root}/../<run_dir>/target/` (use the commands above to read directly; fall back to `target/diff.patch` only if the commands fail).

# Fail-loud rules
- If the target cannot be resolved (empty diff, missing refs, unreadable paths), emit the coverage-failure shape from the output contract. Do not invent a target.
- If your lens cannot do its job (e.g., `{lens}` is `agent-linter` and `$agent-linter` is not installed), emit the coverage-failure shape. Do not substitute generic code review.
- If required reachability is missing (external source unreachable, required local convention source missing), state that in the coverage notes and do NOT fabricate citations.

# Output
Produce ONLY the lens output shape defined in the output contract, starting with the `## Lens: {lens}` heading. No extra sections. No narrative preamble. No `suggested patch` block.
"""


def render_synthesis_prompt(
    repo_root: Path,
    target: ReviewTarget,
    objective: str,
    repo_local_sources: list[str],
    refs: dict[str, Path],
    lens_outputs: dict[str, str],
) -> str:
    sources_block = "\n".join(f"  - `{s}`" for s in repo_local_sources) if repo_local_sources else "  - (none found)"
    objective_block = objective.strip() if objective else "(none)"
    lens_block_parts = []
    for lens, output in lens_outputs.items():
        lens_block_parts.append(f"---- LENS: {lens} ----\n{output.strip()}\n")
    lens_block = "\n".join(lens_block_parts)
    return f"""You are the synthesis reviewer for a general code review. You have no memory of any prior session. Read repo truth directly; do not rely on the summaries below as the final verdict. Your job is to produce the final `ReviewVerdict` defined by the output contract.

# Canonical references (read before emitting output)
- Reviewer prompt contract: `{refs['reviewer-prompt.md']}`
- Review requirements: `{refs['review-requirements.md']}`
- Output contract: `{refs['output-contract.md']}`

# Ground truth
- Working directory: `{repo_root}`
- Review target: {target.describe()}
- Objective (if any): {objective_block}
- Commands that show the changed code:
{target.commands_block(repo_root)}
- Repo-local convention sources to consult:
{sources_block}

# Lens outputs
The following lens outputs were produced by parallel reviewers. Treat them as evidence, not as the final verdict. Dedupe findings. Escalate or demote them based on your own read of the repo. Drop findings whose evidence does not hold up. You MAY add findings the lenses missed, with evidence.

{lens_block}

# Synthesis rules
- Dedupe findings across lenses. The same file/symbol issue reported by two lenses is one finding.
- Keep findings sparse. Sparse, evidence-backed findings are more valuable than long lists.
- If the changed code is clean within the scope the lenses covered, say so plainly and set `VERDICT: approve`.
- If one or more lenses reported a coverage failure, reflect that in the coverage notes. If the failure prevents a trustworthy review (e.g., required agent-linter unavailable on an agent-surface target), set `VERDICT: not-approved` and cite the coverage failure as the top blocking finding.

# Fail-loud rules
- If the target cannot be resolved from the commands above, emit the coverage-failure shape from the output contract instead of a verdict.
- Do not claim agent-linter coverage unless the agent-linter lens output shows it was invoked.
- Do not include a `suggested patch` block anywhere.

# Output
Produce ONLY the final `ReviewVerdict` shape defined in the output contract. No other sections. Start with the `# ReviewVerdict` heading.
"""


def validate_lens_output(lens: str, text: str) -> list[str]:
    errors: list[str] = []
    stripped = text.strip()
    if not stripped:
        errors.append("lens output was empty")
        return errors
    if f"## Lens: {lens}" not in stripped:
        errors.append(f"missing required heading `## Lens: {lens}`")
    has_findings = "## Findings" in stripped
    has_coverage_failure = "## Coverage failure" in stripped
    if not has_findings and not has_coverage_failure:
        errors.append("missing `## Findings` or `## Coverage failure` section")
    if has_findings and has_coverage_failure:
        errors.append("both `## Findings` and `## Coverage failure` present (mutually exclusive)")
    if has_findings and "## Coverage notes" not in stripped:
        errors.append("missing `## Coverage notes` section")
    if "suggested patch" in stripped.lower():
        errors.append("output contains a `suggested patch` block (review-only contract)")
    return errors


def validate_synthesis_output(text: str) -> list[str]:
    errors: list[str] = []
    stripped = text.strip()
    if not stripped:
        errors.append("synthesis output was empty")
        return errors
    if not stripped.startswith("# ReviewVerdict"):
        errors.append("must start with `# ReviewVerdict` heading")
    if not re.search(r"^VERDICT:\s*(approve|approve-with-notes|not-approved)\s*$", stripped, re.MULTILINE):
        errors.append("missing required `VERDICT:` line with a valid value")
    for required in ("## Blocking findings", "## Non-blocking findings", "## Coverage notes"):
        if required not in stripped:
            errors.append(f"missing required section `{required}`")
    if "suggested patch" in stripped.lower():
        errors.append("output contains a `suggested patch` block (review-only contract)")
    return errors


def run_codex_subprocess(
    codex: str,
    repo_root: Path,
    model: str,
    prompt_path: Path,
    final_path: Path,
    stream_path: Path,
) -> int:
    cmd = [
        codex,
        "exec",
        "--ephemeral",
        "--disable",
        "codex_hooks",
        "--cd",
        str(repo_root),
        "--dangerously-bypass-approvals-and-sandbox",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{REASONING_EFFORT}"',
        "-o",
        str(final_path),
    ]
    with prompt_path.open("r") as stdin, stream_path.open("w") as stream:
        stream.write(f"+ {' '.join(shlex.quote(c) for c in cmd)}\n")
        stream.flush()
        proc = subprocess.run(
            cmd, stdin=stdin, stdout=stream, stderr=subprocess.STDOUT, check=False
        )
    return proc.returncode


def run_lens(
    lens: str,
    codex: str,
    repo_root: Path,
    target: ReviewTarget,
    objective: str,
    repo_local_sources: list[str],
    refs: dict[str, Path],
    lenses_dir: Path,
) -> tuple[str, dict]:
    prompt_path = lenses_dir / f"{lens}.prompt.md"
    final_path = lenses_dir / f"{lens}.final.txt"
    stream_path = lenses_dir / f"{lens}.stream.log"
    prompt_path.write_text(render_lens_prompt(lens, repo_root, target, objective, repo_local_sources, refs))
    rc = run_codex_subprocess(codex, repo_root, LENS_MODEL, prompt_path, final_path, stream_path)
    if rc != 0 or not final_path.exists():
        return lens, {
            "status": "failed",
            "returncode": rc,
            "output_path": str(final_path) if final_path.exists() else None,
            "errors": [f"codex lens subprocess exited {rc}"],
        }
    text = final_path.read_text(errors="replace")
    errors = validate_lens_output(lens, text)
    return lens, {
        "status": "ok" if not errors else "malformed",
        "returncode": rc,
        "output_path": str(final_path),
        "errors": errors,
        "is_coverage_failure": "## Coverage failure" in text,
    }


def main(argv: list[str]) -> int:
    ns = parse_args(argv)

    repo_root = Path(ns.repo_root).resolve()
    if not (repo_root / ".git").exists() and ns.target != "paths":
        # paths mode is the only one that's git-independent
        die(f"repo-root is not a git repository: {repo_root}")

    target = resolve_target(ns)
    codex = resolve_codex_binary(ns.codex_binary) if not ns.skip_execution else (ns.codex_binary or "codex")

    try:
        captured = capture_diff(target, repo_root)
    except RunnerError as exc:
        die(str(exc))

    paths = changed_paths(target, repo_root, captured)
    if target.mode != "completion-claim" and not captured.strip() and not paths:
        die("review target produced an empty diff and no paths; refusing to spin up a vapor review")

    agent_surface = detect_agent_surface(paths)
    repo_local_sources = discover_repo_local_sources(repo_root)
    lenses = required_lenses(agent_surface, ns.force_agent_linter)

    output_root = Path(ns.output_root).resolve()
    explicit = Path(ns.run_dir).resolve() if ns.run_dir else None
    output_root.mkdir(parents=True, exist_ok=True)
    run_dir = make_run_dir(output_root, explicit, target)
    lenses_dir = run_dir / "lenses"
    lenses_dir.mkdir(parents=True, exist_ok=True)

    refs = copy_references(run_dir)
    write_target_artifacts(run_dir, target, captured, paths)

    manifest = {
        "version": 1,
        "target": asdict(target),
        "target_description": target.describe(),
        "objective": ns.objective,
        "repo_root": str(repo_root),
        "host_runtime": ns.host_runtime,
        "lens_model": LENS_MODEL,
        "synthesis_model": SYNTHESIS_MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "lenses": lenses,
        "agent_surface_detected": agent_surface,
        "repo_local_sources": repo_local_sources,
        "run_dir": str(run_dir),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    errors_log = run_dir / "errors.log"

    if ns.skip_execution:
        # Prepare-only mode: render lens prompts so artifacts exist, but do not launch Codex.
        for lens in lenses:
            (lenses_dir / f"{lens}.prompt.md").write_text(
                render_lens_prompt(lens, repo_root, target, ns.objective, repo_local_sources, refs)
            )
        (run_dir / "coverage.json").write_text(
            json.dumps(
                {"skipped_execution": True, "lenses": lenses, "agent_surface": agent_surface},
                indent=2,
            )
            + "\n"
        )
        print(str(run_dir))
        return 0

    lens_results: dict[str, dict] = {}
    lens_outputs: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(lenses)) as pool:
        futures = {
            pool.submit(
                run_lens,
                lens,
                codex,
                repo_root,
                target,
                ns.objective,
                repo_local_sources,
                refs,
                lenses_dir,
            ): lens
            for lens in lenses
        }
        for fut in concurrent.futures.as_completed(futures):
            lens_name, result = fut.result()
            lens_results[lens_name] = result
            if result.get("output_path"):
                try:
                    lens_outputs[lens_name] = Path(result["output_path"]).read_text(errors="replace")
                except OSError:
                    pass

    # Fail loud if any required lens has no usable output.
    lens_failures: list[str] = []
    for lens in lenses:
        r = lens_results.get(lens, {})
        if r.get("status") != "ok":
            lens_failures.append(f"{lens}: {r.get('status', 'missing')} ({', '.join(r.get('errors', []))})")

    if lens_failures:
        errors_log.write_text("Lens failures:\n" + "\n".join(lens_failures) + "\n")

    synthesis_prompt_path = run_dir / "synthesis.prompt.md"
    synthesis_final_path = run_dir / "synthesis.final.txt"
    synthesis_stream_path = run_dir / "synthesis.stream.log"

    synthesis_prompt = render_synthesis_prompt(
        repo_root, target, ns.objective, repo_local_sources, refs, lens_outputs
    )
    synthesis_prompt_path.write_text(synthesis_prompt)

    synthesis_rc = run_codex_subprocess(
        codex, repo_root, SYNTHESIS_MODEL, synthesis_prompt_path, synthesis_final_path, synthesis_stream_path
    )
    synthesis_errors: list[str] = []
    if synthesis_rc != 0 or not synthesis_final_path.exists():
        synthesis_errors.append(f"codex synthesis subprocess exited {synthesis_rc}")
    else:
        synthesis_text = synthesis_final_path.read_text(errors="replace")
        synthesis_errors.extend(validate_synthesis_output(synthesis_text))

    coverage = {
        "lenses_run": [l for l, r in lens_results.items() if r.get("status") == "ok"],
        "lens_failures": lens_failures,
        "agent_surface": agent_surface,
        "repo_local_sources": repo_local_sources,
        "synthesis_status": "ok" if synthesis_rc == 0 and not synthesis_errors else "failed",
        "synthesis_errors": synthesis_errors,
        "run_dir": str(run_dir),
    }
    (run_dir / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")

    if lens_failures or synthesis_errors:
        with errors_log.open("a") as fh:
            if synthesis_errors:
                fh.write("Synthesis failures:\n" + "\n".join(synthesis_errors) + "\n")
        print(str(run_dir))
        return 1

    print(str(run_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
