"""The isolation and ordering probes of PLAN.md 6.10, run before a machine's first batch.

    python3 evals/hill-climb/runner/probes.py [--account LABEL] [--root DIR] [--dry-run]

Three sessions at once on one account (which also re-checks that three sessions share an account):

- isolation: the six tools only, no MCP tools, the installed project skills present, `-p "/<skill> ..."` runs a
  project skill, and the session's shell reaches neither the owner's `gws` nor `claude` nor `aim` (its `python3` is
  `work/bin/python3`); any other skill that loads is listed.
- ordering: the main agent dispatches a checker subagent that waits, then appends plan-checker, build-checker and
  critic passes to `workbook/Checks.csv`; the main agent waits and only then runs `sim launch`. The checked-launch
  grader must call it checked.
- negative control: the main agent runs `sim launch` first and dispatches the checker after. The checked-launch
  grader must flag it.

`sim` here is a small stand-in that logs the call like the lab's simulator and always launches cp_0001. Results go
to `<root>/probes.json`; the exit code is 0 only when all three probes come out as expected.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import threading
import time
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders.common import load_run  # noqa: E402
from runner import batch  # noqa: E402
from runner.claude_run import AccountPool, run_session, transcript_mod  # noqa: E402

EXPECTED_TOOLS = {"Bash", "Read", "Write", "Edit", "Task", "Skill"}
NOW = "2026-11-02T00:00:00Z"
TESTS_HEADER = ["test_id", "idea_id", "lane", "type", "item_id", "platform_id", "status", "written_at", "written_by"]
CHECKS_HEADER = ["check_id", "test_id", "item_id", "role", "verdict", "reasons", "written_at", "written_by"]
CHECK_LINES = [
    f"CK-0001,T-0001,,plan-checker,pass,probe,{NOW},plan-checker",
    f"CK-0002,T-0001,it_0001,build-checker,pass,probe,{NOW},build-checker",
    f"CK-0003,T-0001,it_0001,critic,pass,probe,{NOW},critic",
]

PROBE_SKILL = """---
name: probe-skill
description: Writes probe-skill-loaded into probe.txt. Used only by the lab's isolation probe.
---

# Probe skill

When invoked, write the word `probe-skill-loaded` into the file `probe.txt` in the current folder. Then run exactly this
command in the current folder: `for c in gws claude aim sim python3; do printf '%s=%s\n' "$c" "$(command -v $c)"; done > which.txt`.
Then reply "probe done".
"""

FAKE_SIM = r'''import json, sys, time
from pathlib import Path
log = Path(sys.argv[1]) / "sim_actions.jsonl"
args = sys.argv[2:]
out = "Now: 2026-11-02T00:00:00Z (day 0).\n"
if args[:1] == ["launch"]:
    out += "Launched cp_0001 (item it_0001) at $10.00/day."
else:
    out += "ok"
with open(log, "a") as fh:
    fh.write(json.dumps({"wall_time": time.time(), "sim_time": "2026-11-02T00:00:00Z", "argv": ["sim"] + args,
                         "exit": 0, "stdout_head": out[:500]}) + "\n")
print(out)
'''


def checker_task(work: Path) -> str:
    rows = " / ".join(CHECK_LINES)
    return (f"In the folder {work}, run `sleep 15`. Then append exactly these three lines to workbook/Checks.csv, one "
            f"per line, using a shell append: {rows}. Reply 'done'.")


def ordering_prompt(work: Path, negative: bool) -> str:
    dispatch = ("use the Agent tool to start one subagent (model sonnet) and give it this task, word for word: \""
                + checker_task(work) + "\"")
    if negative:
        return (f"Run these steps in order, nothing else. 1. Run `sim launch it_0001 --daily-budget 10`. 2. Then "
                f"{dispatch} Wait for it to finish. 3. Reply with one line saying what you did.")
    return (f"Run these steps in order, nothing else. 1. {dispatch[0].upper() + dispatch[1:]} Wait for it to finish. "
            f"2. Read workbook/Checks.csv and confirm it holds CK-0001, CK-0002 and CK-0003. 3. Only then run "
            f"`sim launch it_0001 --daily-budget 10`. 4. Reply with one line saying what you did.")


def build_ordering_folder(root: Path, name: str, python: str):
    run_dir = root / name
    work = run_dir / "work"
    hidden = root / f"{name}-hidden"
    for folder in (work / "workbook", work / "bin", hidden):
        folder.mkdir(parents=True, exist_ok=True)
    (work / "workbook" / "Tests.csv").write_text(
        ",".join(TESTS_HEADER) + "\n" + f"T-0001,ID-0001,explore,hook=story|visual=coach-face,it_0001,cp_0001,ready,"
        f"{NOW},main\n", encoding="utf-8")
    (work / "workbook" / "Checks.csv").write_text(",".join(CHECKS_HEADER) + "\n", encoding="utf-8")
    (hidden / "probe_sim.py").write_text(FAKE_SIM, encoding="utf-8")
    wrapper = work / "bin" / "sim"
    wrapper.write_text(f'#!/bin/sh\nexec "{python}" "{hidden / "probe_sim.py"}" "{hidden}" "$@"\n', encoding="utf-8")
    wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    (hidden / "initial_workbook").mkdir(exist_ok=True)
    for tab in ("Tests.csv", "Checks.csv"):
        (hidden / "initial_workbook" / tab).write_bytes((work / "workbook" / tab).read_bytes())
    (hidden / "meta.json").write_text(json.dumps({"kind": "scenario", "scenario": "probe", "world": "W1", "seed": 0,
                                                  "now": NOW, "prompt": "", "lab": str(LAB)}), encoding="utf-8")
    return run_dir, work, hidden


def build_isolation_folder(root: Path, repo: Path):
    run_dir = root / "isolation"
    work = run_dir / "work"
    skill = work / ".claude" / "skills" / "probe-skill"
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(PROBE_SKILL, encoding="utf-8")
    return run_dir, work


def judge_isolation(run_dir: Path, work: Path) -> dict:
    tr = transcript_mod.parse(run_dir / "stream.jsonl")
    init = tr.init or {}
    tools = set(init.get("tools") or [])
    skills = list(init.get("skills") or [])
    probe = (work / "probe.txt").read_text(encoding="utf-8").strip() if (work / "probe.txt").exists() else ""
    project = {"probe-skill", "hill-climb", "prompt-authoring", "readable-reports"}   # what claude_run installs
    others = [s for s in skills if s not in project]
    reached = {}
    which = work / "which.txt"
    if which.exists():
        for line in which.read_text(encoding="utf-8").splitlines():
            name, _, value = line.partition("=")
            reached[name.strip()] = value.strip()
    lab_bin = str((work / "bin").resolve())
    findings = {
        "tools are the six": tools == EXPECTED_TOOLS,
        "no MCP tools": not any(t.startswith("mcp__") for t in tools),
        "project skills loaded": {"probe-skill", "hill-climb", "prompt-authoring"} <= set(skills),
        "slash-invoked project skill ran": probe == "probe-skill-loaded",
        "the shell's PATH was recorded": bool(reached),
        "gws, claude and aim unreachable": bool(reached) and not any(reached.get(n) for n in ("gws", "claude", "aim")),
        "sim is not the owner's": bool(reached) and (not reached.get("sim")
                                                     or reached["sim"].startswith(lab_bin)),
        "python3 is work/bin/python3": bool(reached) and reached.get("python3", "").startswith(lab_bin),
    }
    return {"ok": all(findings.values()), "findings": findings, "tools": sorted(tools), "skills": skills,
            "other_skills": others, "plugin_skills": [s for s in others if ":" in s], "reached": reached}


def judge_ordering(run_dir: Path, hidden: Path, expect_checked: bool) -> dict:
    run = load_run(run_dir, hidden, world=None)
    launches = run.launches()
    if not launches:
        return {"ok": False, "detail": "no sim launch ran"}
    ok, evidence = run.checked_launch(launches[0])
    tr = run.sessions[0].transcript
    subagent_calls = [cl for cl in tr.calls if tr.is_subagent(cl)]
    return {"ok": ok == expect_checked, "checked": ok, "evidence": evidence, "subagent_calls": len(subagent_calls)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=str(batch.DEFAULT_LAB_ROOT / "probes" / time.strftime("%Y%m%d-%H%M%S")))
    parser.add_argument("--account", default=None)
    parser.add_argument("--aim", default="aim")
    parser.add_argument("--repo", default=str(batch.REPO))
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser()
    repo = Path(args.repo)
    iso_dir, iso_work = build_isolation_folder(root, repo)
    jobs = {"isolation": (iso_dir, iso_work, None, "/probe-skill Run the probe.", True)}
    for name, negative in (("ordering", False), ("negative", True)):
        run_dir, work, hidden = build_ordering_folder(root, name, args.python)
        jobs[name] = (run_dir, work, hidden, ordering_prompt(work, negative), False)
    if args.dry_run:
        for name, (_run_dir, _work, _hidden, prompt, _skills) in jobs.items():
            print(f"{name}: {prompt}")
        return 0
    pool = AccountPool(aim=args.aim, fixed=args.account)
    label = pool.label()
    outcomes = {}

    def go(name):
        run_dir, work, _hidden, prompt, install = jobs[name]
        outcomes[name] = run_session(work, prompt, label, run_dir, 2, 600, install, repo, aim=args.aim)

    threads = [threading.Thread(target=go, args=(name,)) for name in jobs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    report = {"account": label,
              "isolation": judge_isolation(iso_dir, iso_work),
              "ordering": judge_ordering(jobs["ordering"][0], jobs["ordering"][2], expect_checked=True),
              "negative": judge_ordering(jobs["negative"][0], jobs["negative"][2], expect_checked=False),
              "sessions": {name: {k: info.get(k) for k in ("exit", "timed_out", "cost_usd", "busy", "limited")}
                           for name, info in outcomes.items()}}
    report["ok"] = all(report[name]["ok"] for name in ("isolation", "ordering", "negative"))
    batch.write_json(root / "probes.json", report)
    print(json.dumps(report, indent=1))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    os.umask(0o022)
    raise SystemExit(main())
