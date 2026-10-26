"""Layer 3: backtests on the four toy worlds (PLAN.md 6.7, 6.9, section 8 gates).

    python3 evals/hill-climb/runner/run_backtest.py --batch L3-a                 # the plan's five runs, no-skill, thompson
    python3 evals/hill-climb/runner/run_backtest.py --batch L3-w4 --runs W4:1 --no-noskill
    python3 evals/hill-climb/runner/run_backtest.py --batch L3-a --regrade

A run is a setup tick at 2026-11-02T00:00Z, then a tick every 12 simulated hours to the horizon with `/hill-climb Run
the tick.`, each followed by `simadmin advance --hours 12`. The setup tick is the intake interview
(`run_intake.intake_loop`, docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md): its first session gets the world's
request, a simulated owner answers every question from the world's brief (`worlds/owners/<W>.md`, which answers the
way the request reads; W3 has no money), and its last session seeds the climb and runs the first tick, all at day 0;
its sessions take `RUN/ticks/000/` onward and later ticks number on from there. After every session the runner copies
`work/workbook/` to its folder's `workbook/`. A valid money request (a money-request notify plus a Money
`request` row with standing, learned, next and amount, in the same tick) gets the owner's reply in the next prompt, and
the runner applies it (W1 and W2 grant once, then refuse; W4 refuses; W3 has nothing to ask for). A tick that times out,
hits its budget cap or crashes is recorded as failed and the run goes on; a run with more than three failed ticks, or
with tampering, is invalid and rerun once.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import uuid
from datetime import timedelta
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402
from graders.backtest import grade_backtest, outcome_gates  # noqa: E402
from runner import batch  # noqa: E402
from runner import run_intake  # noqa: E402
from runner.claude_run import (  # noqa: E402
    BUDGET_SETUP_USD, BUDGET_TICK_USD, TIMEOUT_S, AccountPool, NoEligibleAccount, run_session_with_accounts,
    session_status,
)
from runner.watch import read_watch_log  # noqa: E402

LIMITED_RERUNS = 3

WORLD_REQUESTS = {
    "W1": "/hill-climb Set up a hill climb on this ad account to get the cost of a conversion as low as possible. "
          "You have $600; ask me if you need more.",
    "W2": "/hill-climb Set up a hill climb on these search keywords to get the cost of a conversion as low as "
          "possible. You have $400; ask me if you need more.",
    "W3": "/hill-climb Set up a hill climb on this account's posts to get as many follows per post as possible.",
    "W4": "/hill-climb Set up a hill climb on this ad account to get the cost of a conversion as low as possible. "
          "You have $300.",
}
TICK_PROMPT = "/hill-climb Run the tick."
REPLY_PROMPT = '/hill-climb Run the tick. The owner answered your money request: "{reply}"'
APPROVALS = {"W1": ("Approved: $600 more.", 600), "W2": ("Approved: $300 more.", 300)}
REFUSAL = "No more money for this one; make the most of what's left."
DEFAULT_RUNS = (("W4", 1), ("W1", 1), ("W1", 2), ("W2", 1), ("W3", 1))
TICK_HOURS = 12
MAX_FAILED_TICKS = 3


class Owner:
    """The account owner's answers to valid money requests (PLAN.md 6.7)."""

    def __init__(self, world: str):
        self.world = world
        self.granted = False
        self.refused = False

    def answer(self):
        """(reply text or None, grant amount or None) for the next valid request."""
        if self.world == "W3":
            return None, None
        if self.world in APPROVALS and not self.granted:
            self.granted = True
            return APPROVALS[self.world]
        if not self.refused:
            self.refused = True
            return REFUSAL, None
        return None, None


def tick_count(world: str, days=None) -> int:
    days = days if days is not None else c.WORLD_DAYS[world]
    return int(days * 24 // TICK_HOURS)


def tick_prompt(index: int, world: str, reply, skill: bool) -> str:
    if index == 0:
        prompt = WORLD_REQUESTS[world]
    elif reply:
        prompt = REPLY_PROMPT.format(reply=reply)
    else:
        prompt = TICK_PROMPT
    return prompt if skill else batch.strip_skill_prefix(prompt)


def tick_budget(index: int) -> float:
    return BUDGET_SETUP_USD if index == 0 else BUDGET_TICK_USD


def valid_money_request(tick_dir: Path, hidden_dir: Path, info: dict) -> bool:
    """A money-request notify plus a Money request row with all four parts, both in this tick."""
    start, end = info.get("started_t"), info.get("ended_t")
    asked = False
    try:
        lines = (Path(hidden_dir) / "outbox.jsonl").read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        wall = entry.get("wall_time")
        if c.norm_label(entry.get("kind")) == "moneyrequest" and isinstance(wall, (int, float)) and \
                (start is None or start - 1 <= wall <= (end or wall) + 1):
            asked = True
    if not asked:
        return False
    for line in read_watch_log(Path(tick_dir) / "watch.jsonl"):
        if c.tab_name(line.get("file") or "") != "money":
            continue
        rows = list(line.get("added") or []) + [item.get("after") or {} for item in line.get("changed") or []]
        for raw in rows:
            row = c.norm_row(raw)
            amount = c.parse_amount(row.get("amount"))
            if c.is_label(row.get("kind"), "money", "request") and all(row.get(k) for k in ("standing", "learned",
                                                                                            "next")) \
                    and amount is not None and amount > 0:
                return True
    return False


def simadmin(python: str, hidden: Path, *args) -> subprocess.CompletedProcess:
    argv = [python, str(LAB / "sim" / "cli.py"), "simadmin", "--hidden", str(hidden)] + [str(a) for a in args]
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"simadmin {' '.join(map(str, args))} failed: {proc.stderr.strip()[:500]}")
    return proc


def world_now(hidden: Path, fallback):
    world = c.load_world(hidden)
    return getattr(world, "now", None) or fallback


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
        self.timeout_s = args.timeout
        self.strict_order = not args.weak_order


def run_setup(ctx: Context, run_dir: Path, hidden_dir: Path, prompt: str, skill: bool, sim_time) -> tuple:
    """Tick 0: the intake interview with the world's owner; its last session seeds the climb and runs the first tick.
    Returns (the tick's record, [(session folder, session info)])."""
    summary = run_intake.intake_loop(
        prompt, run_intake.session_runner(ctx, run_dir / "work", install_skill=skill,
                                          budget_for=lambda _phase: tick_budget(0)),
        run_intake.owner_runner(ctx, run_intake.read_brief(hidden_dir), hidden_dir), run_dir, final_tick=False,
        prefix=batch.SKILL_PREFIX if skill else "", tick=0, sim_time=sim_time, log_dir=hidden_dir, publish=False)
    sessions = []
    for number in range(summary["next_turn"] - summary["sessions"], summary["next_turn"]):
        folder = hidden_dir / "ticks" / f"{number:03d}"
        try:
            info = json.loads((folder / "session.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            info = {}
        sessions.append((folder, info))
    tick = {"tick": 0, "sim_time": sim_time, "prompt": prompt, "grant_applied": None,
            "intake": {key: summary[key] for key in ("ended", "sessions", "signed_off_turn", "cost_usd")}}
    return tick, sessions


def run_world(world: str, seed: int, skill: bool, ctx: Context, run_id: str) -> dict:
    import fixtures  # owned by the simulator builder

    run_dir = ctx.lab_root / "runs" / ctx.batch / run_id
    hidden_dir = ctx.lab_root / "hidden" / str(uuid.uuid4())
    batch.remove_run(run_dir, hidden_dir)
    meta = fixtures.build_world(world, seed, run_dir, hidden_dir, LAB, ctx.python)
    start = c.parse_time(meta.get("now")) or c.WORLD_START
    owner = Owner(world)
    reply = None
    failed = 0
    turn = 0           # the next session folder under RUN/ticks/ (tick 0's interview takes several)
    ticks = []
    count = tick_count(world, ctx.args.days)
    for index in range(count):
        grant = None
        if reply is not None:
            text, grant = reply
            reply = None
        else:
            text = None
        if grant:
            simadmin(ctx.python, hidden_dir, "grant", grant)
        prompt = tick_prompt(index, world, text, skill)
        now = world_now(hidden_dir, None)
        sim_time = c.iso(now) if now else c.iso(start + index * timedelta(hours=TICK_HOURS))
        if index == 0:
            tick, sessions = run_setup(ctx, run_dir, hidden_dir, prompt, skill, sim_time)
            turn += len(sessions)
            statuses = [info.get("status") or session_status(info) for _folder, info in sessions]
            status = next((st for st in statuses if st != "ok"), "ok")
            failed += sum(1 for st in statuses if st != "ok")
            asked = any(valid_money_request(folder, hidden_dir, info) for folder, info in sessions)
            cost = sum(info.get("cost_usd") or 0.0 for _folder, info in sessions)
            label = sessions[-1][1].get("label") if sessions else None
        else:
            tick_dir = hidden_dir / "ticks" / f"{turn:03d}"   # out of the agent's sight until the run ends
            turn += 1
            tick_dir.mkdir(parents=True, exist_ok=True)
            tick = {"tick": index, "sim_time": sim_time, "prompt": prompt, "grant_applied": grant}
            batch.write_json(tick_dir / "tick.json", tick)
            for _attempt in range(LIMITED_RERUNS + 1):
                info = run_session_with_accounts(
                    ctx.pool, work=run_dir / "work", prompt=prompt, run_dir=tick_dir, budget_usd=tick_budget(index),
                    timeout_s=ctx.timeout_s, install_skill=skill, repo=ctx.repo, aim=ctx.aim)
                if not info.get("limited"):
                    break
                # an account limit is not the skill's failure: the same tick runs again once the account can
                ctx.pool.limited(info.get("label"))
                tick.setdefault("limited_attempts", []).append(info.get("label"))
            status = session_status(info)
            if status != "ok":
                failed += 1
            snapshot = tick_dir / "workbook"
            if snapshot.exists():
                shutil.rmtree(snapshot)
            if (run_dir / "work" / "workbook").is_dir():
                shutil.copytree(run_dir / "work" / "workbook", snapshot)
            asked = valid_money_request(tick_dir, hidden_dir, info)
            cost, label = info.get("cost_usd"), info.get("label")
            info["status"] = status
            batch.write_json(tick_dir / "session.json", info)
        if asked:
            answer = owner.answer()
            if answer[0]:
                reply = answer
        tick.update({"status": status, "valid_money_request": asked, "reply_next": reply[0] if reply else None,
                     "cost_usd": cost, "account": label})
        if index:
            batch.write_json(tick_dir / "tick.json", tick)
        ticks.append(tick)
        simadmin(ctx.python, hidden_dir, "advance", "--hours", TICK_HOURS)
    # the interview log and every session's folder stayed hidden from the agents; now they join the run for the graders
    run_intake.publish_logs(hidden_dir, run_dir)
    run = c.load_run(run_dir, hidden_dir, strict_order=ctx.strict_order)
    graded = grade_backtest(run)
    invalid = failed > MAX_FAILED_TICKS or bool(graded["tampering"])
    record = {"run_id": run_id, "world": world, "seed": seed, "skill": skill, "failed_ticks": failed,
              "invalid": invalid, "ticks": ticks, **graded}
    batch.write_json(run_dir / "grade.json", record)
    dest = ctx.results / run_id
    batch.copy_results(run_dir, hidden_dir, dest)
    batch.write_json(dest / "grade.json", record)
    if not ctx.args.keep:
        batch.remove_run(run_dir, hidden_dir)
    return record


def run_with_rerun(world, seed, skill, ctx) -> dict:
    base = f"{world}-s{seed}" + ("" if skill else "-noskill")
    first = run_world(world, seed, skill, ctx, base)
    if not first["invalid"] or ctx.args.no_rerun:
        return first
    second = run_world(world, seed, skill, ctx, base + "-r1")
    second["rerun_of"] = base
    if second["invalid"]:
        second["gate_failed"] = "invalid twice"
    return second


def thompson_metrics(world, seed, ctx) -> dict:
    from baselines import thompson

    root = ctx.lab_root / "runs" / ctx.batch / f"{world}-s{seed}-thompson"
    if root.exists():
        shutil.rmtree(root)
    result = thompson.run(world, seed, lab=LAB, root=root, python=ctx.python)
    batch.write_json(ctx.results / f"{world}-s{seed}-thompson" / "grade.json", result)
    if not ctx.args.keep:
        shutil.rmtree(root, ignore_errors=True)
    return result


def summarize(records, thompsons, batch_name, started, ended) -> tuple:
    results = {}
    rows = []
    for record in records:
        key = f"{record['world']}:{record['seed']}" + ("" if record["skill"] else ":noskill")
        results[key] = record.get("metrics", {})
        rows.append({"run": key, "invalid": record.get("invalid"), "failed_ticks": record.get("failed_ticks"),
                     "process_pass": record.get("process_pass") if record["skill"] else None,
                     "failing_checks": [ch["name"] for ch in record.get("checks", []) if not ch["pass"]],
                     "metrics": record.get("metrics", {})})
    for key, metrics in thompsons.items():
        results[f"{key}:thompson"] = metrics
    gates = outcome_gates(results)
    summary = {"batch": batch_name, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
               "ended": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended)), "runs": rows,
               "thompson": thompsons, "outcome_gates": gates}
    lines = [f"# Layer 3 batch {batch_name}", "", "| Run | Process gates | Failing checks | Captured | First best | "
             "Failed ticks | Cost | Wall time | Median tick | Median tick cost | Median role dispatches |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]

    def cell(value, form):
        return "-" if value is None else form.format(value)

    for row in rows:
        m = row["metrics"]
        captured = m.get("conversions_captured", m.get("follows_captured"))
        best = (m.get("first_best") or {}).get("day")
        process = "n/a" if row["process_pass"] is None else ("pass" if row["process_pass"] else "FAIL")
        lines.append(f"| {row['run']} | {process} | {', '.join(row['failing_checks']) or '-'} | "
                     f"{captured if captured is not None else '-'} | {best if best is not None else '-'} | "
                     f"{row['failed_ticks']} | ${m.get('cost_usd', 0):.2f} | {m.get('wall_s', 0) / 60:.0f} min | "
                     f"{cell(m.get('median_tick_wall_s'), '{:.0f} s')} | {cell(m.get('median_tick_cost_usd'), '${:.2f}')} "
                     f"| {cell(m.get('median_tick_dispatches'), '{:g}')} |")
    for key, metrics in thompsons.items():
        captured = metrics.get("conversions_captured", metrics.get("follows_captured"))
        lines.append(f"| {key}:thompson | n/a | - | {captured} | {(metrics.get('first_best') or {}).get('day', '-')} "
                     f"| - | $0.00 | - | - | - | - |")
    lines += ["", "| Outcome gate | Met | Evidence |", "|---|---|---|"]
    for gate in gates:
        lines.append(f"| {gate['name']} | {'yes' if gate['pass'] else 'NO'} | {gate['evidence']} |")
    return summary, "\n".join(lines) + "\n"


def parse_runs(text):
    out = []
    for part in text.split(","):
        part = part.strip()
        if part:
            world, _, seed = part.partition(":")
            out.append((world.strip().upper(), int(seed or 1)))
    return out


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--runs", default=",".join(f"{w}:{s}" for w, s in DEFAULT_RUNS))
    parser.add_argument("--no-noskill", action="store_true", help="skip the no-skill runs")
    parser.add_argument("--no-thompson", action="store_true")
    parser.add_argument("--days", type=float, default=None, help="override the world's horizon (for a short trial)")
    parser.add_argument("--lab-root", default=str(batch.DEFAULT_LAB_ROOT))
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--account", default=None)
    parser.add_argument("--aim", default="aim")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--max-parallel", type=int, default=batch.MAX_PARALLEL)
    parser.add_argument("--load-limit", type=float, default=batch.LOCAL_LOAD_LIMIT)
    parser.add_argument("--mem-limit-gb", type=float, default=batch.MEMORY_LIMIT_GB)
    parser.add_argument("--timeout", type=int, default=TIMEOUT_S)
    parser.add_argument("--weak-order", action="store_true")
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--no-rerun", action="store_true",
                        help="keep an invalid run's result instead of running it again (its record says why it is invalid)")
    parser.add_argument("--regrade", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def regrade(ctx):
    records, thompsons = [], {}
    for folder in sorted(p for p in ctx.results.iterdir() if p.is_dir()):
        old = json.loads((folder / "grade.json").read_text()) if (folder / "grade.json").exists() else {}
        if folder.name.endswith("-thompson"):
            thompsons[f"{old.get('world')}:{old.get('seed')}"] = old
            continue
        if not (folder / "run").is_dir():
            continue
        run = c.load_run(folder / "run", folder / "hidden", strict_order=ctx.strict_order)
        graded = grade_backtest(run)
        record = dict(old, **graded)
        record["invalid"] = old.get("failed_ticks", 0) > MAX_FAILED_TICKS or bool(graded["tampering"])
        batch.write_json(folder / "grade.json", record)
        records.append(record)
    final = {}
    for record in records:
        final[(record["world"], record["seed"], record["skill"])] = record
    return list(final.values()), thompsons


def main(argv=None) -> int:
    args = parse_args(argv)
    ctx = Context(args)
    runs = parse_runs(args.runs)
    started = time.time()
    if args.regrade:
        records, thompsons = regrade(ctx)
    else:
        jobs = []
        for world, seed in runs:
            jobs.append({"world": world, "seed": seed, "skill": True, "run_id": f"{world}-s{seed}"})
        if not args.no_noskill:
            for world, seed in runs:
                jobs.append({"world": world, "seed": seed, "skill": False, "run_id": f"{world}-s{seed}-noskill"})
        if args.dry_run:
            for job in jobs:
                print(job["run_id"], f"{tick_count(job['world'], args.days)} ticks",
                      tick_prompt(0, job["world"], None, job["skill"]))
            return 0
        ctx.results.mkdir(parents=True, exist_ok=True)
        thompsons = {}
        if not args.no_thompson:
            for world, seed in runs:
                thompsons[f"{world}:{seed}"] = thompson_metrics(world, seed, ctx)
        try:
            records = batch.run_jobs(jobs, lambda job: run_with_rerun(job["world"], job["seed"], job["skill"], ctx),
                                     max_parallel=args.max_parallel, load_limit=args.load_limit,
                                     mem_limit_gb=args.mem_limit_gb)
        except NoEligibleAccount as exc:
            records = getattr(exc, "partial_results", [])
            summary, markdown = summarize(records, thompsons, args.batch, started, time.time())
            summary["stopped"] = str(exc)
            batch.write_json(ctx.results / "summary.json", summary)
            (ctx.results / "summary.md").write_text(markdown + f"\nStopped: {exc}\n", encoding="utf-8")
            print(f"batch stopped: {exc}", file=sys.stderr)
            return 2
    records = [r for r in records if r.get("world")]
    summary, markdown = summarize(records, thompsons, args.batch, started, time.time())
    batch.write_json(ctx.results / "summary.json", summary)
    (ctx.results / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
