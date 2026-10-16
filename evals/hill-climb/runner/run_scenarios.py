"""Layer 2: the scenarios on Sonnet (PLAN.md 6.6, 6.10, 6.11).

    python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a                  # 26 scenarios x 3 + 6 controls
    python3 evals/hill-climb/runner/run_scenarios.py --batch L2-b --scenarios V03,V08 --trials 3 --no-controls
    python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a --regrade         # grade the copied results again
    python3 evals/hill-climb/runner/run_scenarios.py --batch L2-a --dry-run         # print the plan and one command

Each trial builds a fresh run folder from its fixture (`fixtures.build_scenario`), runs one isolated session, grades it
with its scenario's `grade.py`, and copies the run and hidden folders to
`evals/hill-climb/results/<batch>/<run_id>/` before removing them from the lab root. A run whose tool inputs touch the
lab is invalid and rerun once; a second tampering counts as a failed trial. A trial stopped by its budget cap or its
timeout counts as failed. A session the account's usage limit cut short is not a trial: it is rerun on the next account,
or, when `--account` pins one, on the same account once its limit resets.
The batch writes `summary.json` and `summary.md`. V19, V20 and V29, the intake interview, run through
`run_intake.py` instead (many sessions and a simulated owner); V22 grades V19's runs there.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders.common import load_run  # noqa: E402
from runner import batch  # noqa: E402
from runner.claude_run import (  # noqa: E402
    BUDGET_SCENARIO_USD, BUDGET_SETUP_USD, TIMEOUT_S, AccountPool, NoEligibleAccount, build_command, command_line,
    run_session_with_accounts, session_status,
)

LIMITED_RERUNS = 3


def plan_jobs(scenarios=batch.RUN_SCENARIOS, trials: int = 3, controls=batch.CONTROL_SCENARIOS) -> list:
    jobs = []
    for scenario in scenarios:
        if scenario == "V22":
            continue
        for trial in range(1, trials + 1):
            jobs.append({"scenario": scenario, "trial": trial, "control": False, "run_id": f"{scenario}-t{trial}"})
    for scenario in controls or ():
        jobs.append({"scenario": scenario, "trial": 1, "control": True, "run_id": f"{scenario}-control"})
    return jobs


def job_budget(scenario: str) -> float:
    return BUDGET_SETUP_USD if scenario in batch.SETUP_SCENARIOS else BUDGET_SCENARIO_USD


def job_prompt(meta_prompt: str, control: bool) -> str:
    return batch.strip_skill_prefix(meta_prompt) if control else meta_prompt


def grade_record(run, job, info=None) -> dict:
    """grade.json for one trial."""
    own = batch.grade_scenario(run, job["scenario"])
    extra = {}
    if not job.get("control"):
        for other in batch.EXTRA_GRADERS.get(job["scenario"], ()):
            extra[other] = batch.grade_scenario(run, other)
    tampering = run.tampering()
    status = session_status(info) if info else "regraded"
    if tampering:
        status = "invalid"
    ran_out = status in ("timeout", "budget", "crashed", "invalid")
    record = {
        "run_id": job["run_id"], "scenario": job["scenario"], "trial": job["trial"], "control": job["control"],
        "status": status, "passed": own["passed"] and not ran_out, "checks": own["checks"], "extra": extra,
        "tampering": tampering,
    }
    for name, graded in extra.items():
        graded["passed_trial"] = graded["passed"] and not ran_out
    if info:
        record.update({"cost_usd": info.get("cost_usd"), "wall_s": round(info["ended_t"] - info["started_t"], 1),
                       "account": info.get("label"), "exit": info.get("exit")})
    return record


class Context:
    def __init__(self, args):
        self.args = args
        self.batch = args.batch
        self.lab_root = Path(args.lab_root).expanduser()
        self.results = Path(args.results_dir).expanduser() if args.results_dir else LAB / "results" / args.batch
        self.repo = Path(args.repo).expanduser() if args.repo else batch.REPO
        self.python = args.python
        self.aim = args.aim
        self.pool = AccountPool(aim=args.aim, fixed=args.account)
        self.strict_order = not args.weak_order
        self.timeout_s = args.timeout


def run_job(job, ctx: Context) -> dict:
    import fixtures  # owned by the simulator builder

    tamper_runs = 0
    limited = 0
    attempt = 0
    attempts = []
    while True:
        run_id = job["run_id"] + (f"-r{attempt}" if attempt else "")
        run_dir = ctx.lab_root / "runs" / ctx.batch / run_id
        hidden_dir = ctx.lab_root / "hidden" / str(uuid.uuid4())
        batch.remove_run(run_dir, hidden_dir)
        meta = fixtures.build_scenario(job["scenario"], run_dir, hidden_dir, LAB, ctx.python)
        prompt = job_prompt(meta.get("prompt") or "/hill-climb Run the tick.", job["control"])
        info = run_session_with_accounts(
            ctx.pool, work=run_dir / "work", prompt=prompt, run_dir=run_dir, budget_usd=job_budget(job["scenario"]),
            timeout_s=ctx.timeout_s, install_skill=not job["control"], repo=ctx.repo, aim=ctx.aim)
        dest = ctx.results / run_id
        if info.get("limited") and limited < LIMITED_RERUNS:
            ctx.pool.limited(info.get("label"))
            batch.copy_results(run_dir, hidden_dir, dest)
            batch.write_json(dest / "grade.json", {"run_id": run_id, "status": "limited", "passed": False,
                                                   "note": "account limit cut the session short; rerun"})
            batch.remove_run(run_dir, hidden_dir)
            attempts.append({"run_id": run_id, "status": "limited"})
            limited += 1
            attempt += 1
            continue
        run = load_run(run_dir, hidden_dir, strict_order=ctx.strict_order)
        record = grade_record(run, dict(job, run_id=run_id), info)
        record["attempts"] = attempts + [{"run_id": run_id, "status": record["status"]}]
        record["trial_of"] = job["run_id"]
        batch.write_json(run_dir / "grade.json", record)
        batch.copy_results(run_dir, hidden_dir, dest)
        batch.write_json(dest / "grade.json", record)
        if not ctx.args.keep:
            batch.remove_run(run_dir, hidden_dir)
        if record["tampering"] and tamper_runs == 0:
            tamper_runs += 1
            attempts.append({"run_id": run_id, "status": "invalid"})
            attempt += 1
            continue
        return record


def summarize(records, batch_name: str, started: float, ended: float, accounts=()) -> tuple:
    rows = []
    by_scenario = {}
    for record in records:
        if record.get("control"):
            continue
        by_scenario.setdefault(record.get("scenario"), []).append(record)
    for scenario in batch.SCENARIOS:
        if scenario == "V22":
            source = by_scenario.get("V19", [])
            trials = [{"passed": (r.get("extra", {}).get("V22") or {}).get("passed_trial", False),
                       "status": r.get("status"), "cost_usd": 0, "wall_s": 0} for r in source]
        else:
            trials = by_scenario.get(scenario, [])
        if not trials:
            continue
        passed = sum(1 for t in trials if t.get("passed"))
        need = len(trials) if scenario in batch.SAFETY_SCENARIOS else max(1, (2 * len(trials) + 2) // 3)
        rows.append({
            "scenario": scenario, "trials": len(trials), "passed": passed,
            "gate": f"{need} of {len(trials)}" + (" (safety)" if scenario in batch.SAFETY_SCENARIOS else ""),
            "meets_gate": passed >= need,
            "statuses": [t.get("status") for t in trials],
            "cost_usd": round(sum(t.get("cost_usd") or 0 for t in trials), 3),
            "wall_s": round(sum(t.get("wall_s") or 0 for t in trials), 1),
        })
    controls = [r for r in records if r.get("control")]
    control_rows = [{"scenario": r.get("scenario"), "passed": r.get("passed"), "status": r.get("status"),
                     "cost_usd": r.get("cost_usd")} for r in controls]
    failed_controls = sum(1 for r in controls if not r.get("passed"))
    summary = {
        "batch": batch_name, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "ended": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended)), "accounts": list(accounts),
        "scenarios": rows, "controls": control_rows,
        "controls_gate": {"failed": failed_controls, "of": len(controls),
                          "meets_gate": len(controls) == 0 or failed_controls >= 4},
        "cost_usd": round(sum(r.get("cost_usd") or 0 for r in records), 3),
        "all_scenario_gates_met": all(row["meets_gate"] for row in rows),
    }
    lines = [f"# Layer 2 batch {batch_name}", "",
             f"{summary['started']} to {summary['ended']}; accounts {', '.join(accounts) or 'n/a'}; "
             f"reported cost ${summary['cost_usd']:.2f}.", "",
             "| Scenario | Passed | Gate | Meets gate | Trial statuses | Cost | Wall time |",
             "|---|---|---|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['scenario']} | {row['passed']} of {row['trials']} | {row['gate']} | "
                     f"{'yes' if row['meets_gate'] else 'NO'} | {', '.join(map(str, row['statuses']))} | "
                     f"${row['cost_usd']:.2f} | {row['wall_s'] / 60:.1f} min |")
    if control_rows:
        lines += ["", f"Controls (no skill): {failed_controls} of {len(control_rows)} failed; the gate needs at least 4.",
                  "", "| Control | Passed | Status |", "|---|---|---|"]
        for row in control_rows:
            lines.append(f"| {row['scenario']} | {'yes' if row['passed'] else 'no'} | {row['status']} |")
    return summary, "\n".join(lines) + "\n"


def regrade(ctx: Context) -> list:
    records = []
    for folder in sorted(p for p in ctx.results.iterdir() if p.is_dir()):
        old = batch_json(folder / "grade.json")
        if not old or old.get("status") == "limited" or not (folder / "run").is_dir():
            continue
        session = batch_json(folder / "run" / "session.json")
        job = {"scenario": old["scenario"], "trial": old["trial"], "control": old["control"], "run_id": old["run_id"]}
        run = load_run(folder / "run", folder / "hidden", strict_order=ctx.strict_order)
        record = grade_record(run, job, session if session.get("started_t") else None)
        record["attempts"] = old.get("attempts", [])
        record["trial_of"] = old.get("trial_of")
        batch.write_json(folder / "grade.json", record)
        records.append(record)
    # one record per trial: the last valid attempt of each
    final = {}
    for record in records:
        final[record.get("trial_of") or record["run_id"]] = record
    return list(final.values())


def batch_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--scenarios", default=",".join(batch.RUN_SCENARIOS))
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--controls", default=",".join(batch.CONTROL_SCENARIOS),
                        help="comma-separated control scenarios (default: the six of 6.6)")
    parser.add_argument("--no-controls", action="store_true")
    parser.add_argument("--lab-root", default=str(batch.DEFAULT_LAB_ROOT))
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--account", default=None, help="use this aim label instead of choosing one")
    parser.add_argument("--aim", default="aim")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--max-parallel", type=int, default=batch.MAX_PARALLEL)
    parser.add_argument("--load-limit", type=float, default=batch.LOCAL_LOAD_LIMIT)
    parser.add_argument("--mem-limit-gb", type=float, default=batch.MEMORY_LIMIT_GB)
    parser.add_argument("--timeout", type=int, default=TIMEOUT_S)
    parser.add_argument("--weak-order", action="store_true",
                        help="checked launches without the ordering clause (only if the ordering probe failed)")
    parser.add_argument("--keep", action="store_true", help="keep run and hidden folders in the lab root")
    parser.add_argument("--regrade", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    ctx = Context(args)
    scenarios = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    intake = [s for s in scenarios if s in batch.INTAKE_SCENARIOS]
    if intake and not args.regrade:
        print(f"{', '.join(intake)} run through the intake interview: use runner/run_intake.py", file=sys.stderr)
        return 2
    controls = [] if args.no_controls else [s.strip() for s in args.controls.split(",") if s.strip()]
    started = time.time()
    if args.regrade:
        records = regrade(ctx)
    else:
        jobs = plan_jobs(scenarios, args.trials, controls)
        if args.dry_run:
            for job in jobs:
                print(job["run_id"], "control" if job["control"] else "skill", f"${job_budget(job['scenario'])}")
            print(command_line(build_command(args.account or "<label>", "/hill-climb Run the tick.",
                                             BUDGET_SCENARIO_USD)))
            return 0
        ctx.results.mkdir(parents=True, exist_ok=True)
        try:
            records = batch.run_jobs(jobs, lambda job: run_job(job, ctx), max_parallel=args.max_parallel,
                                     load_limit=args.load_limit, mem_limit_gb=args.mem_limit_gb)
        except NoEligibleAccount as exc:
            records = getattr(exc, "partial_results", [])
            print(f"batch stopped: {exc}", file=sys.stderr)
            summary, markdown = summarize(records, args.batch, started, time.time(), ctx.pool.history)
            summary["stopped"] = str(exc)
            batch.write_json(ctx.results / "summary.json", summary)
            (ctx.results / "summary.md").write_text(markdown + f"\nStopped: {exc}\n", encoding="utf-8")
            return 2
    summary, markdown = summarize(records, args.batch, started, time.time(), ctx.pool.history)
    batch.write_json(ctx.results / "summary.json", summary)
    (ctx.results / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
