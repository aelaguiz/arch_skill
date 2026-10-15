"""Run a batch on the Mac Studio over SSH (PLAN.md 6.1). Not the default path in draft 8: model batches run on this
Mac, because the Studio's aim refuses accounts that other machines hold. Kept for when the Studio has an account.

    python3 evals/hill-climb/runner/remote.py --batch L2-a scenarios [run_scenarios.py arguments ...]
    python3 evals/hill-climb/runner/remote.py --batch L3-a backtest [run_backtest.py arguments ...]
    python3 evals/hill-climb/runner/remote.py --batch L2-a --dry-run scenarios      # print the commands only

Steps: rsync -a --delete `evals/hill-climb/` (without results/), `skills/hill-climb/`, `skills/prompt-authoring/`,
`skills/_shared/` and `skills/readable-reports/` to `~/hill-climb-lab/src/`; run the batch there with `/opt/homebrew/bin/python3` and the Studio's load
limit (9); copy `~/hill-climb-lab/results/<batch>/` back into `evals/hill-climb/results/<batch>/`; then remove
`~/hill-climb-lab/runs/` and `~/hill-climb-lab/hidden/`.
"""
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
REPO = LAB.parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from runner.batch import STUDIO_LOAD_LIMIT  # noqa: E402

HOST = "agents@amirs-mac-studio"
REMOTE_ROOT = "~/hill-climb-lab"
REMOTE_PYTHON = "/opt/homebrew/bin/python3"
RUNNERS = {"scenarios": "run_scenarios.py", "backtest": "run_backtest.py", "roles": "run_roles.py"}
SYNC_DIRS = ("evals/hill-climb", "skills/hill-climb", "skills/prompt-authoring", "skills/_shared",
             "skills/readable-reports")


def sync_commands(repo: Path = REPO, host: str = HOST, root: str = REMOTE_ROOT) -> list:
    commands = [["ssh", host, f"mkdir -p {root}/src/evals {root}/src/skills"]]
    for rel in SYNC_DIRS:
        argv = ["rsync", "-a", "--delete", "--exclude", "__pycache__", "--exclude", "*.pyc"]
        if rel == "evals/hill-climb":
            argv += ["--exclude", "/results/"]
        argv += [f"{Path(repo) / rel}/", f"{host}:{root}/src/{rel}/"]
        commands.append(argv)
    return commands


def run_command(kind: str, batch_name: str, extra=(), host: str = HOST, root: str = REMOTE_ROOT) -> list:
    runner = RUNNERS[kind]
    remote = (f"cd {root}/src && {REMOTE_PYTHON} evals/hill-climb/runner/{runner} --batch {shlex.quote(batch_name)} "
              f"--lab-root {root} --results-dir {root}/results/{shlex.quote(batch_name)} "
              f"--load-limit {STUDIO_LOAD_LIMIT:g}")
    if extra:
        remote += " " + " ".join(shlex.quote(str(a)) for a in extra)
    return ["ssh", host, remote]


def fetch_command(batch_name: str, repo: Path = REPO, host: str = HOST, root: str = REMOTE_ROOT) -> list:
    dest = Path(repo) / "evals" / "hill-climb" / "results" / batch_name
    return ["rsync", "-a", f"{host}:{root}/results/{batch_name}/", f"{dest}/"]


def cleanup_command(host: str = HOST, root: str = REMOTE_ROOT) -> list:
    return ["ssh", host, f"rm -rf {root}/runs {root}/hidden"]


def plan(kind: str, batch_name: str, extra=(), repo: Path = REPO, host: str = HOST) -> list:
    return (sync_commands(repo, host) + [run_command(kind, batch_name, extra, host)]
            + [fetch_command(batch_name, repo, host), cleanup_command(host)])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("kind", choices=sorted(RUNNERS))
    parser.add_argument("extra", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    commands = plan(args.kind, args.batch, args.extra, REPO, args.host)
    for argv_ in commands:
        print(" ".join(shlex.quote(part) for part in argv_), flush=True)
        if args.dry_run:
            continue
        code = subprocess.run(argv_).returncode
        if code != 0 and argv_ is not commands[-1]:
            # results are still copied back and the remote run folders removed when the batch itself fails
            if argv_ in commands[:len(SYNC_DIRS) + 1]:
                print(f"sync failed with exit {code}; nothing ran", file=sys.stderr)
                return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
