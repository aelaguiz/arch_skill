"""Intake runs: the hill-climb skill's intake interview against a simulated owner, on Sonnet
(docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md, "The lab: testing the intake on cheap models").

    python3 evals/hill-climb/runner/run_intake.py --batch I-a --account <label>            # V19, V20, V29 x 2
    python3 evals/hill-climb/runner/run_intake.py --batch I-a --scenarios V19 --trials 1 --account <label>
    python3 evals/hill-climb/runner/run_intake.py --batch I-a --regrade                    # grade the saved runs again
    python3 evals/hill-climb/runner/run_intake.py --batch I-a --dry-run                    # the plan and one command

Each trial builds its scenario's folder (`fixtures.build_scenario`, which also copies the scenario's owner brief,
`scenarios/<ID>/owner.md`, into the hidden folder, where no session can read it) and runs `intake_loop`:

- every turn is one fresh session under `RUN/ticks/<n>/`, so each turn has to pick the interview up from the workbook;
  the first prompt is the scenario's request, each later one `/hill-climb <the owner's answer>`;
- when a session's final message asks the owner something (`graders.common.question_in`), the simulated owner
  (`runner/owner.py`) answers it from the brief and flags it, reading with the message any report the session wrote
  for the owner in `reports/` (where the skill may put a long playback);
- the loop stops at the first session that ends without a question (after the owner's sign-off that ends the
  interview; before it, the agent left the owner nothing to answer), when a session or the owner fails, after 30
  sessions, or when the trial's spending reaches its cap. The session after the sign-off seeds the climb and runs its
  first tick; once it has, the world moves on 12 simulated hours (`simadmin advance`, the backtest's tick step) and one
  more session runs `/hill-climb Run the tick.`: a real second tick, which must ask nothing.

`RUN/interview.jsonl` logs every session: turn, phase, prompt, the agent's final message, the question found in it,
and the owner's answer, flags and times. `RUN/intake.json` says how the loop ended. The run is graded with its
scenario's `grade.py` (V19's runs also with V22's) and copied to `results/<batch>/<run_id>/`. The same loop runs a
backtest's setup (`run_backtest.py`, tick 0). Sessions run through `aim` on the pinned or chosen account with the
scenario runner's isolation and caps: $8 for an interview session, $6 for the tick after it, 20 minutes each; a
session an account's usage limit cut short runs again once the account can.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402
from runner import batch  # noqa: E402
from runner import owner as owner_mod  # noqa: E402
from runner import transcript as transcript_mod  # noqa: E402
from runner.claude_run import (  # noqa: E402
    BUDGET_SETUP_USD, BUDGET_TICK_USD, TIMEOUT_S, AccountPool, NoEligibleAccount, build_command, command_line,
    run_session_with_accounts, session_status,
)

MAX_SESSIONS = 30
TICK_PROMPT = "/hill-climb Run the tick."
TRIAL_BUDGET_USD = 40.0     # a lab guard on one trial's spending (agent and owner), not a rule of the skill
LIMITED_RERUNS = 3
DEFAULT_TRIALS = 2
BRIEF_NAME = "owner.md"


def iso_utc(epoch) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if epoch else ""


def read_brief(hidden_dir) -> str:
    """The owner's brief the fixture copied into the hidden folder."""
    path = Path(hidden_dir) / BRIEF_NAME
    if not path.is_file():
        raise FileNotFoundError(f"no owner brief at {path}: the scenario or world needs one ({BRIEF_NAME})")
    return path.read_text(encoding="utf-8")


def next_turn(run_dir) -> int:
    """The next session folder's number under RUN/ticks/ (0 for a new run)."""
    ticks = Path(run_dir) / "ticks"
    numbers = [int(p.name) for p in ticks.iterdir() if p.is_dir() and p.name.isdigit()] if ticks.is_dir() else []
    return max(numbers) + 1 if numbers else 0


def asked_question(message: str):
    """The question a final message puts to the owner: `graders.common.question_in`'s, or, when the message's last
    paragraph holds a question only inside quotes (an agent quoting the question it asks), that paragraph. Without the
    second, a quoted question would end the interview early; the graders' checks on asking keep question_in alone."""
    found = c.question_in(message)
    if found:
        return found
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", str(message or "")) if p.strip()]
    last = paragraphs[-1] if paragraphs else ""
    return last[-160:] if "?" in last else None


def _append_jsonl(path: Path, entry: dict) -> None:
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------------------------------------------------------------
# the loop


def _session(run_session, run_dir: Path, turn: int, prompt: str, phase: str, tick: int, sim_time):
    """One session in <run_dir>/ticks/<turn>/ (the trial's hidden folder while it runs): (its result, its log entry)."""
    tick_dir = run_dir / "ticks" / f"{turn:03d}"
    tick_dir.mkdir(parents=True, exist_ok=True)
    record = {"tick": tick, "turn": turn, "phase": phase, "sim_time": sim_time, "prompt": prompt}
    batch.write_json(tick_dir / "tick.json", record)
    result = run_session(turn, prompt, tick_dir, phase) or {}
    done = time.time()
    message = result.get("message") or ""
    entry = {"turn": turn, "phase": phase, "prompt": prompt, "status": result.get("status"),
             "agent_message": message, "question": asked_question(message), "asked_at": iso_utc(done),
             "asked_t": round(done, 3), "cost_usd": result.get("cost_usd")}
    record.update(status=entry["status"], question=entry["question"], cost_usd=entry["cost_usd"])
    batch.write_json(tick_dir / "tick.json", record)
    return result, entry


def intake_loop(request: str, run_session, ask_owner, run_dir, *, max_sessions: int = MAX_SESSIONS,
                final_tick: bool = True, tick_prompt: str = TICK_PROMPT, prefix: str = batch.SKILL_PREFIX,
                tick: int = 0, sim_time=None, cost_cap=None, before_tick=None, log=None, log_dir=None) -> dict:
    """Run the interview, then (when the owner signed off and `final_tick`) one more tick; returns the summary written
    to RUN/intake.json: {"ended", "sessions", "signed_off_turn", "final_tick_turn", "next_turn", "statuses",
    "cost_usd"}. The session after the sign-off seeds the climb and runs its first tick, so `before_tick()` moves the
    world on first (12 simulated hours, as a backtest's tick step does) and returns the new time; the extra tick is
    then a real second tick, which must ask nothing.

    run_session(turn, prompt, tick_dir, phase) -> {"status": "ok" | ..., "message": the final message, "cost_usd",
                                                   "files": {path: text} the agent wrote in reports/ this turn}
    ask_owner(turn, message, history, files) -> runner.owner.ask's reply; history is [(agent message, owner answer)]

    `ended` is "signed-off" (the owner signed off and a session then ended without a question), "no-question" (a
    session ended without a question before any sign-off), "session-<status>" (a session timed out, hit its cap,
    crashed or stayed limited), "owner-failed", "max-sessions" or "trial-budget".

    A session whose final message asks nothing but whose workbook holds an Interview row still `asked` is waiting on
    the owner all the same (an agent may say "tell me what to correct" with no question mark), so before the sign-off
    that row's question goes to the owner. With `log_dir` (a trial's hidden folder), interview.jsonl and intake.json are
    written there while the agents run, out of their reach, and copied into RUN/ at the end for the graders."""
    run_dir = Path(run_dir)
    log = log or (lambda message: None)
    log_root = Path(log_dir) if log_dir else run_dir
    log_root.mkdir(parents=True, exist_ok=True)
    log_path = log_root / "interview.jsonl"
    history, statuses = [], []
    signoff_turn, final_turn = None, None
    spent = 0.0
    prompt = request
    turn = max(next_turn(run_dir), next_turn(log_root))
    ended = "max-sessions"
    for _count in range(max_sessions):
        if cost_cap is not None and spent >= cost_cap:
            ended = "trial-budget"
            break
        result, entry = _session(run_session, log_root, turn, prompt, "intake", tick, sim_time)
        if entry["question"] is None and signoff_turn is None and result.get("open_question"):
            entry["question"] = result["open_question"]
        spent += result.get("cost_usd") or 0.0
        statuses.append(entry["status"])
        stop = None
        if entry["status"] != "ok":
            stop = f"session-{entry['status']}"
        elif entry["question"] is None:
            stop = "signed-off" if signoff_turn is not None else "no-question"
        else:
            files = result.get("files") or {}
            entry["files"] = sorted(files)
            reply = ask_owner(turn, result.get("message") or "", list(history), files) or {}
            spent += reply.get("cost_usd") or 0.0
            answered = reply.get("ended_t") or time.time()
            entry.update(answer=reply.get("answer"), flags=reply.get("flags"), why=reply.get("why"),
                         missing_flags=reply.get("missing_flags"), owner_status=reply.get("status"),
                         owner_cost_usd=reply.get("cost_usd"), answered_at=iso_utc(answered),
                         answered_t=round(answered, 3))
            if reply.get("status") != "ok" or not reply.get("answer"):
                stop = "owner-failed"
            else:
                if signoff_turn is None and (reply.get("flags") or {}).get("signed_off") is True:
                    signoff_turn = turn
                history.append((result.get("message") or "", reply["answer"]))
                prompt = prefix + reply["answer"]
        _append_jsonl(log_path, entry)
        log(f"[intake] turn {turn}: {entry['status']}; "
            + (f"asked {entry['question']!r}; owner: {str(entry.get('answer'))[:80]!r}" if entry["question"]
               else "no question"))
        turn += 1
        if stop:
            ended = stop
            break
    if final_tick and ended == "signed-off":
        if before_tick is not None:
            sim_time = before_tick() or sim_time
        result, entry = _session(run_session, log_root, turn, tick_prompt, "tick", tick + 1, sim_time)
        spent += result.get("cost_usd") or 0.0
        statuses.append(entry["status"])
        _append_jsonl(log_path, entry)
        final_turn = turn
        turn += 1
    summary = {"ended": ended, "sessions": len(statuses), "signed_off_turn": signoff_turn,
               "final_tick_turn": final_turn, "next_turn": turn, "statuses": statuses, "cost_usd": round(spent, 4)}
    batch.write_json(log_root / "intake.json", summary)
    if log_root != run_dir:
        run_dir.mkdir(parents=True, exist_ok=True)
        for name in ("interview.jsonl", "intake.json"):
            if (log_root / name).exists():
                shutil.copy2(log_root / name, run_dir / name)
        # the sessions' folders (transcripts, workbook copies) stayed out of the agents' sight; now they join the run
        if (log_root / "ticks").is_dir():
            (run_dir / "ticks").mkdir(parents=True, exist_ok=True)
            for folder in sorted((log_root / "ticks").iterdir()):
                target = run_dir / "ticks" / folder.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.move(str(folder), str(target))
            shutil.rmtree(log_root / "ticks", ignore_errors=True)
    return summary


# ----------------------------------------------------------------------------------------------------------------------
# the real session and owner (shared with run_backtest.py)


TICK_HOURS = 12


def advance_world(python: str, hidden_dir, hours: int = TICK_HOURS) -> str:
    """`simadmin advance --hours H` on the run's world; returns the world's new time (ISO)."""
    argv = [python, str(LAB / "sim" / "cli.py"), "simadmin", "--hidden", str(hidden_dir), "advance", "--hours",
            str(hours)]
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"simadmin advance failed: {proc.stderr.strip()[:500]}")
    world = c.load_world(hidden_dir)
    return c.iso(world.now) if world is not None and getattr(world, "now", None) else None


def session_budget(phase: str) -> float:
    return BUDGET_SETUP_USD if phase == "intake" else BUDGET_TICK_USD


def report_snapshot(work) -> dict:
    """{path in the agent's folder: sha256} of the reports for the owner (reports/, HTML or Markdown)."""
    folder = Path(work) / "reports"
    out = {}
    if folder.is_dir():
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix.lower() in c.REPORT_SUFFIXES:
                out[path.relative_to(work).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def reports_written(work, before: dict) -> dict:
    """{path: text} of the reports the session wrote or changed: what the owner can read with its message (the skill
    may play the design back in the form the owner reads, such as a Markdown file in reports/)."""
    out = {}
    for rel, digest in report_snapshot(work).items():
        if before.get(rel) != digest:
            out[rel] = c.report_text((Path(work) / rel).read_text(encoding="utf-8", errors="replace"))
    return out


def final_message(tick_dir) -> str:
    """The session's answer to its prompt: the last result that asks the owner something, else the last result. A
    session can wake again after its answer (a background command it left running ends) and close with a line that
    restates the open question without asking it; that wake-up must not hide the question from the owner."""
    texts = [ev.get("result") for _t, ev in transcript_mod.parse(Path(tick_dir) / "stream.jsonl").results
             if isinstance(ev.get("result"), str)]
    for text in reversed(texts):
        if asked_question(text):
            return text
    return texts[-1] if texts else ""


def open_question(work):
    """The question of the newest Interview row still waiting on the owner (status asked, no answer), else None."""
    path = Path(work) / "workbook" / "Interview.csv"
    try:
        with open(path, encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return None
    done = {"answered", "superseded", "closed", "settled", "done"}
    pending = [r for r in rows if c.norm_label(r.get("status")) not in {c.norm_label(d) for d in done}
               and not str(r.get("answer") or "").strip() and str(r.get("question") or "").strip()
               and c.norm_label(r.get("kind")) != "request"]
    if not pending:
        return None
    return str(pending[-1].get("question") or "an open question in the Interview tab")[:160]


# A headless session does not exit while a command it moved to the background is still running, and the test model
# sometimes starts one that waits on input forever (`cat > /tmp/x 2>/dev/null; ...`), which holds a finished turn open
# until its timeout. With background tasks off, such a command is stopped at the Bash tool's own timeout instead, and
# role agents run in the foreground (several at once still run together). Interview sessions only.
INTAKE_ENV = {"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1"}


def session_runner(ctx, work, install_skill: bool = True, budget_for=session_budget):
    """run_session for intake_loop: one isolated session on the context's account pool, rerun when an account limit
    cuts it short; leaves session.json (with its status) and a copy of the workbook in the session's folder."""
    work = Path(work)

    def run(turn, prompt, tick_dir, phase):
        tick_dir = Path(tick_dir)
        before = report_snapshot(work)
        info, limited = None, []
        for _attempt in range(LIMITED_RERUNS + 1):
            info = run_session_with_accounts(
                ctx.pool, work=work, prompt=prompt, run_dir=tick_dir, budget_usd=budget_for(phase),
                timeout_s=ctx.timeout_s, install_skill=install_skill, repo=ctx.repo, aim=ctx.aim,
                base_env=dict(os.environ, **INTAKE_ENV))
            if not info.get("limited"):
                break
            ctx.pool.limited(info.get("label"))     # not the skill's failure: the same turn runs again
            limited.append(info.get("label"))
        info["status"] = session_status(info)
        if limited:
            info["limited_attempts"] = limited
        batch.write_json(tick_dir / "session.json", info)
        snapshot = tick_dir / "workbook"
        if snapshot.exists():
            shutil.rmtree(snapshot)
        if (work / "workbook").is_dir():
            shutil.copytree(work / "workbook", snapshot)
        return {"status": info["status"], "message": final_message(tick_dir), "cost_usd": info.get("cost_usd"),
                "files": reports_written(work, before), "info": info, "open_question": open_question(work)}

    return run


def owner_runner(ctx, brief: str, hidden_dir):
    """ask_owner for intake_loop: the simulated owner on the context's account pool. Its files (which hold the brief) go
    to HIDDEN/owner/<n>/, out of the agent's reach like the brief itself."""
    def ask(turn, message, history, files=None):
        return owner_mod.ask(brief, message, history, files, pool=ctx.pool,
                             out_dir=Path(hidden_dir) / "owner" / f"{turn:03d}", aim=ctx.aim)

    return ask


# ----------------------------------------------------------------------------------------------------------------------
# trials


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
        self.max_sessions = args.max_sessions
        self.trial_budget = args.trial_budget


def plan_jobs(scenarios=batch.INTAKE_SCENARIOS, trials: int = DEFAULT_TRIALS) -> list:
    return [{"scenario": s, "trial": t, "control": False, "run_id": f"{s}-t{t}"}
            for s in scenarios for t in range(1, trials + 1)]


def flag_counts(run) -> dict:
    return {flag: len(c.flagged(run, flag)) for flag in c.OWNER_FLAGS}


def grade_record(run, job) -> dict:
    """grade.json for one trial."""
    own = batch.grade_scenario(run, job["scenario"])
    extra = {other: batch.grade_scenario(run, other) for other in batch.EXTRA_GRADERS.get(job["scenario"], ())}
    tampering = run.tampering()
    statuses = [s.info.get("status") or session_status(s.info) for s in run.sessions]
    ended = run.intake.get("ended")
    failed = [s for s in statuses if s != "ok"]
    status = "invalid" if tampering else ("owner-failed" if ended == "owner-failed" else (failed[0] if failed else "ok"))
    ran_out = status != "ok"
    for graded in extra.values():
        graded["passed_trial"] = graded["passed"] and not ran_out
    owner_cost = sum(e.get("owner_cost_usd") or 0.0 for e in run.interview)
    agent_cost = sum(s.info.get("cost_usd") or 0.0 for s in run.sessions)
    walls = [s.info["ended_t"] - s.info["started_t"] for s in run.sessions
             if isinstance(s.info.get("started_t"), (int, float)) and isinstance(s.info.get("ended_t"), (int, float))]
    return {
        "run_id": job["run_id"], "scenario": job["scenario"], "trial": job["trial"], "control": False,
        "status": status, "passed": own["passed"] and not ran_out, "checks": own["checks"], "extra": extra,
        "tampering": tampering, "ended": ended, "sessions": len(run.sessions), "signed_off_turn": run.signoff_turn,
        "flags": flag_counts(run), "cost_usd": round(agent_cost + owner_cost, 3),
        "owner_cost_usd": round(owner_cost, 3), "wall_s": round(sum(walls), 1), "session_statuses": statuses,
    }


def run_job(job, ctx: Context) -> dict:
    import fixtures  # owned by the simulator builder

    tampered, attempt, attempts = 0, 0, []
    while True:
        run_id = job["run_id"] + (f"-r{attempt}" if attempt else "")
        run_dir = ctx.lab_root / "runs" / ctx.batch / run_id
        hidden_dir = ctx.lab_root / "hidden" / str(uuid.uuid4())
        batch.remove_run(run_dir, hidden_dir)
        meta = fixtures.build_scenario(job["scenario"], run_dir, hidden_dir, LAB, ctx.python)
        brief = read_brief(hidden_dir)
        log = (lambda message, rid=run_id: print(f"[{rid}] {message}", file=sys.stderr, flush=True))
        intake_loop(meta["prompt"], session_runner(ctx, run_dir / "work"), owner_runner(ctx, brief, hidden_dir),
                    run_dir, max_sessions=ctx.max_sessions, sim_time=meta.get("now"), cost_cap=ctx.trial_budget,
                    before_tick=lambda hidden=hidden_dir: advance_world(ctx.python, hidden), log=log,
                    log_dir=hidden_dir)
        run = c.load_run(run_dir, hidden_dir, strict_order=ctx.strict_order)
        record = grade_record(run, dict(job, run_id=run_id))
        record["attempts"] = attempts + [{"run_id": run_id, "status": record["status"]}]
        record["trial_of"] = job["run_id"]
        batch.write_json(run_dir / "grade.json", record)
        dest = ctx.results / run_id
        batch.copy_results(run_dir, hidden_dir, dest)
        batch.write_json(dest / "grade.json", record)
        if not ctx.args.keep:
            batch.remove_run(run_dir, hidden_dir)
        if record["tampering"] and tampered == 0:
            tampered += 1
            attempts.append({"run_id": run_id, "status": "invalid"})
            attempt += 1
            continue
        return record


def summarize(records, batch_name: str, started: float, ended: float, accounts=()) -> tuple:
    by_scenario = {}
    for record in records:
        by_scenario.setdefault(record.get("scenario"), []).append(record)
    rows = []
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
        rows.append({"scenario": scenario, "trials": len(trials), "passed": passed, "gate": f"{need} of {len(trials)}",
                     "meets_gate": passed >= need, "statuses": [t.get("status") for t in trials],
                     "cost_usd": round(sum(t.get("cost_usd") or 0 for t in trials), 3),
                     "wall_s": round(sum(t.get("wall_s") or 0 for t in trials), 1)})
    trials = [{"run_id": r.get("run_id"), "status": r.get("status"), "passed": r.get("passed"),
               "ended": r.get("ended"), "sessions": r.get("sessions"), "signed_off_turn": r.get("signed_off_turn"),
               "flags": r.get("flags"), "failing": [ch["name"] for ch in r.get("checks", []) if not ch["pass"]],
               "cost_usd": r.get("cost_usd"), "owner_cost_usd": r.get("owner_cost_usd")} for r in records]
    summary = {"batch": batch_name, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
               "ended": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended)), "accounts": list(accounts),
               "scenarios": rows, "trials": trials,
               "cost_usd": round(sum(r.get("cost_usd") or 0 for r in records), 3),
               "all_scenario_gates_met": bool(rows) and all(row["meets_gate"] for row in rows)}
    lines = [f"# Intake batch {batch_name}", "",
             f"{summary['started']} to {summary['ended']}; accounts {', '.join(accounts) or 'n/a'}; reported cost "
             f"${summary['cost_usd']:.2f} (agent and owner).", "",
             "| Scenario | Passed | Gate | Meets gate | Trial statuses | Cost | Wall time |", "|---|---|---|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['scenario']} | {row['passed']} of {row['trials']} | {row['gate']} | "
                     f"{'yes' if row['meets_gate'] else 'NO'} | {', '.join(map(str, row['statuses']))} | "
                     f"${row['cost_usd']:.2f} | {row['wall_s'] / 60:.1f} min |")
    lines += ["", "| Trial | Passed | How the interview ended | Sessions | Signed off on turn | Owner's flags raised | "
              "Failing checks |", "|---|---|---|---|---|---|---|"]
    for t in trials:
        raised = ", ".join(f"{k} {v}" for k, v in (t.get("flags") or {}).items() if v) or "-"
        lines.append(f"| {t['run_id']} | {'yes' if t['passed'] else 'no'} | {t['ended']} | {t['sessions']} | "
                     f"{t['signed_off_turn'] if t['signed_off_turn'] is not None else '-'} | {raised} | "
                     f"{'; '.join(t['failing']) or '-'} |")
    return summary, "\n".join(lines) + "\n"


def regrade(ctx: Context) -> list:
    records = []
    for folder in sorted(p for p in ctx.results.iterdir() if p.is_dir()):
        old = _json(folder / "grade.json")
        if not old or not (folder / "run").is_dir() or old.get("scenario") not in batch.INTAKE_SCENARIOS:
            continue
        job = {"scenario": old["scenario"], "trial": old["trial"], "run_id": old["run_id"]}
        run = c.load_run(folder / "run", folder / "hidden", strict_order=ctx.strict_order)
        record = grade_record(run, job)
        record["attempts"] = old.get("attempts", [])
        record["trial_of"] = old.get("trial_of")
        batch.write_json(folder / "grade.json", record)
        records.append(record)
    # one record per trial: a rerun stands in for an attempt only while that attempt is still invalid
    final = {}
    for record in records:
        key = record.get("trial_of") or record["run_id"]
        if key not in final or final[key].get("status") == "invalid":
            final[key] = record
    return list(final.values())


def _json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def dry_run(args, scenarios) -> int:
    """Print the plan, check that each scenario has its owner's brief, and print one agent and one owner command."""
    import fixtures

    problems = 0
    for job in plan_jobs(scenarios, args.trials):
        print(job["run_id"], f"up to {args.max_sessions} interview sessions at ${BUDGET_SETUP_USD} each; after the "
                             f"sign-off, 12 simulated hours, then one tick at ${BUDGET_TICK_USD}; trial cap "
                             f"${args.trial_budget:g}")
    print()
    for scenario in scenarios:
        brief = LAB / "scenarios" / scenario / BRIEF_NAME
        request = fixtures.load_fixture(scenario)["prompt"]
        if brief.is_file():
            print(f"{scenario}: brief {brief.relative_to(LAB)} ({len(brief.read_text(encoding='utf-8'))} characters); "
                  f"request {request!r}")
        else:
            problems += 1
            print(f"{scenario}: LAB BUG: no owner brief at {brief.relative_to(LAB)}")
    label = args.account or "<label>"
    first = fixtures.load_fixture(scenarios[0])["prompt"] if scenarios else TICK_PROMPT
    print("\nThe first session (from the run's work/ folder, the skill installed; later ones: /hill-climb <answer>):")
    print(command_line(build_command(label, first, BUDGET_SETUP_USD)))
    print("\nThe owner (from an empty temporary folder, no tools; the brief is in its system prompt):")
    print(command_line(owner_mod.build_command(label, "<the owner's instructions and brief>",
                                               "<the conversation so far and the agent's latest message>")))
    return 1 if problems else 0


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--scenarios", default=",".join(batch.INTAKE_SCENARIOS))
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--max-sessions", type=int, default=MAX_SESSIONS,
                        help="interview sessions before the loop gives up (the tick after it is extra)")
    parser.add_argument("--trial-budget", type=float, default=TRIAL_BUDGET_USD,
                        help="stop a trial's interview once its agent and owner sessions have cost this much")
    parser.add_argument("--lab-root", default=str(batch.DEFAULT_LAB_ROOT))
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--account", default=None, help="pin this aim label (or an ordered list a,b)")
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
    scenarios = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    unknown = [s for s in scenarios if s not in batch.INTAKE_SCENARIOS]
    if unknown:
        print(f"not intake scenarios: {', '.join(unknown)} (they run with run_scenarios.py)", file=sys.stderr)
        return 2
    if args.dry_run:
        return dry_run(args, scenarios)
    ctx = Context(args)
    started = time.time()
    if args.regrade:
        records = regrade(ctx)
    else:
        ctx.results.mkdir(parents=True, exist_ok=True)
        try:
            records = batch.run_jobs(plan_jobs(scenarios, args.trials), lambda job: run_job(job, ctx),
                                     max_parallel=args.max_parallel, load_limit=args.load_limit,
                                     mem_limit_gb=args.mem_limit_gb)
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
