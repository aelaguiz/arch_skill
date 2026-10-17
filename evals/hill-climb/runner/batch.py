"""Shared pieces of the batch runners: paths, the session scheduler, grader loading and result copying."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
REPO = LAB.parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from runner.claude_run import NoEligibleAccount, allowed_sessions  # noqa: E402

DEFAULT_LAB_ROOT = Path.home() / ".cache" / "hill-climb-lab"   # this Mac (PLAN.md draft 8); the Studio uses ~/hill-climb-lab
LOCAL_LOAD_LIMIT = 27.0    # 1.5 x this Mac's 18 cores (draft 8)
STUDIO_LOAD_LIMIT = 9.0    # 0.75 x the Studio's 12 cores (6.10)
MEMORY_LIMIT_GB = 16.0
MAX_PARALLEL = 3

SCENARIOS = tuple(f"V{n:02d}" for n in range(1, 32))   # V31: money limits learning (VELOCITY_PLAN.md)
INTAKE_SCENARIOS = ("V19", "V20", "V29")   # the intake interview: run_intake.py, many sessions with a simulated owner
RUN_SCENARIOS = tuple(s for s in SCENARIOS if s != "V22" and s not in INTAKE_SCENARIOS)   # V22 grades V19's runs
SAFETY_SCENARIOS = ("V01", "V02", "V03", "V07", "V16", "V17", "V23", "V28")   # 3 of 3 (PLAN.md 8, 13.5)
CONTROL_SCENARIOS = ("V01", "V02", "V03", "V07", "V16", "V17")
SETUP_SCENARIOS = ("V19", "V20", "V29")   # setup or adoption runs: the $8 cap
EXTRA_GRADERS = {"V19": ("V22",)}

SKILL_PREFIX = "/hill-climb "


def strip_skill_prefix(prompt: str) -> str:
    """The no-skill control's prompt: the same words without `/hill-climb `."""
    text = prompt or ""
    return text[len(SKILL_PREFIX):] if text.startswith(SKILL_PREFIX) else text


def load_grader(scenario: str, lab: Path = LAB):
    """`grade(run)` from scenarios/<ID>/grade.py."""
    path = Path(lab) / "scenarios" / scenario / "grade.py"
    spec = importlib.util.spec_from_file_location(f"hill_climb_grade_{scenario}", path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.grade


def grade_scenario(run, scenario: str, lab: Path = LAB) -> dict:
    """{"checks", "passed"} for a scenario's own grader; a grader that raises fails with its traceback as evidence."""
    try:
        checks = load_grader(scenario, lab)(run)
    except Exception:
        checks = [{"name": "grader ran", "pass": False, "evidence": traceback.format_exc()[-2000:]}]
    return {"checks": checks, "passed": all(item.get("pass") for item in checks)}


def write_json(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=False, default=str) + "\n", encoding="utf-8")


def _copy_ignore(directory, names):
    skip = []
    for name in names:
        if name in ("__pycache__",) or name.endswith(".pyc"):
            skip.append(name)
        elif name == ".claude" and Path(directory).name == "work":
            skip.append(name)   # the installed skill copy; the repo holds the source
    return skip


def copy_results(run_dir: Path, hidden_dir: Path, dest: Path) -> None:
    """Copy a run's folder (without the installed skills) and its hidden folder into dest/run and dest/hidden."""
    dest = Path(dest)
    for source, name in ((run_dir, "run"), (hidden_dir, "hidden")):
        target = dest / name
        if target.exists():
            shutil.rmtree(target)
        if Path(source).exists():
            shutil.copytree(source, target, ignore=_copy_ignore)


def remove_run(run_dir: Path, hidden_dir: Path) -> None:
    for folder in (run_dir, hidden_dir):
        if Path(folder).exists():
            shutil.rmtree(folder, ignore_errors=True)


def run_jobs(jobs, worker, max_parallel: int = MAX_PARALLEL, load_limit: float = LOCAL_LOAD_LIMIT,
             mem_limit_gb: float = MEMORY_LIMIT_GB, poll_s: float = 5.0, stagger_s: float = 3.0, log=None,
             slots_fn=None):
    """Run worker(job) for every job, at most `allowed_sessions(...)` at once (re-checked before each start).
    NoEligibleAccount stops the batch: nothing new starts, running jobs finish, and the error is re-raised."""
    log = log or (lambda message: print(message, file=sys.stderr, flush=True))
    slots_fn = slots_fn or (lambda: allowed_sessions(max_parallel, load_limit, mem_limit_gb))
    pending = list(jobs)
    results = []
    stop = None
    running = {}
    with ThreadPoolExecutor(max_workers=max(1, max_parallel)) as pool:
        while (pending and stop is None) or running:
            while pending and stop is None:
                allowed = slots_fn()
                if len(running) >= allowed:
                    break
                job = pending.pop(0)
                log(f"[batch] start {job.get('run_id') or job} ({len(running) + 1} running, {allowed} allowed)")
                running[pool.submit(worker, job)] = job
                if pending and stagger_s:
                    time.sleep(stagger_s)
            if not running:
                if pending and stop is None:
                    time.sleep(poll_s)
                continue
            done, _ = wait(list(running), timeout=poll_s, return_when=FIRST_COMPLETED)
            for future in done:
                job = running.pop(future)
                try:
                    results.append(future.result())
                except NoEligibleAccount as exc:
                    stop = exc
                    log(f"[batch] stopping: {exc}")
                except Exception:
                    results.append({"run_id": job.get("run_id"), "status": "runner-error", "passed": False,
                                    "error": traceback.format_exc()[-3000:]})
    if stop is not None:
        stop.partial_results = results
        raise stop
    return results
