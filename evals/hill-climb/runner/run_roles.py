"""Layer 2b: the role tests (PLAN.md 13.2, 13.5).

    python3 evals/hill-climb/runner/run_roles.py --batch R-a                           # every case x 3
    python3 evals/hill-climb/runner/run_roles.py --batch R-b --cases reader-lean --trials 1
    python3 evals/hill-climb/runner/run_roles.py --batch R-a --regrade                 # grade the saved runs again
    python3 evals/hill-climb/runner/run_roles.py --batch R-a --dry-run [--show-briefs] # the plan and the filled briefs

Each trial builds a run folder from its case's fixture (`fixtures.build_scenario`: a scenario's, or the case's own in
`roles/<case>/`), reads the role's brief from `skills/hill-climb/references/roles/<role>.md` at run time (the part after
its `---` line, which the brief tells the main agent to give the role), fills every brace in it with the case's facts,
and starts one clean session through `runner/claude_run.py` (no skill installed, no main agent) whose prompt is the
filled brief. A brief with a brace the lab cannot fill is never sent: that is a lab bug, and the case stops with it.
The trial then grades the row the role wrote. The critic sees its items only under neutral labels in random order,
through `sim preview LABEL`; the label map stays in the hidden folder until the session ends. A role passes when each
of its cases passes 3 of 3. Results go to `results/<batch>/<case>-t<n>/` with `summary.json` and `summary.md`.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402
from runner import batch  # noqa: E402
from runner.claude_run import (  # noqa: E402
    TIMEOUT_S, AccountPool, NoEligibleAccount, build_command, command_line, run_session_with_accounts, session_status,
)

BUDGET_ROLE_USD = 3
LIMITED_RERUNS = 3
BRACE = re.compile(r"\{([a-z_]+)\}")
GOAL = "the cost per conversion of a poker training app's ads, where lower is better"
WHERE = "in their social media feeds on their phones, as a short ad between posts from people they follow"
VISUALS = ("The items differ on purpose in what the ad shows: the app's screen in one, a coach talking to the camera in "
           "the other. Both open with a question and offer a free week")
# The critic's bar when the case's Charter has no `quality_floor` (the fixtures predate the field): neutral, so the
# existing cases keep testing the same judgments (CHANGES.md, 2026-10-15, the intake round).
NEUTRAL_QUALITY_FLOOR = "at least as good as the climb's current best item; nothing named as never to be wrong"
# Who the critic cases' items are aimed at: the people every W1 fixture plan was written for. The Charter no longer has
# an `audience` field (who responds is what a climb finds out; each item's plan says who it is aimed at).
AIMED_AT = "people who play poker in home games and casinos and want to make better decisions at the table"

CASES = (
    {"id": "plan-checker-other-days", "role": "plan-checker", "fixture": "roles/plan-checker-other-days",
     "tests": ["T-0031"], "expect": {"T-0031": "fail"},
     "about": "a plan whose comparison ran on different days from the test (must fail)"},
    {"id": "plan-checker-sound", "role": "plan-checker", "fixture": "roles/plan-checker-sound",
     "tests": ["T-0031"], "expect": {"T-0031": "pass"}, "about": "a sound plan (must pass)"},
    {"id": "build-checker-music", "role": "build-checker", "fixture": "scenarios/V28", "items": {"it_0006": "T-0006"},
     "expect": {"it_0006": "fail"},
     "about": "a W5 variation whose music changed though its plan holds it (must fail)"},
    {"id": "build-checker-clean", "role": "build-checker", "fixture": "roles/build-checker-clean",
     "items": {"it_0006": "T-0006"}, "expect": {"it_0006": "pass"},
     "about": "a clean --from variation with a full recipe (must pass)"},
    {"id": "critic-generic", "role": "critic", "fixture": "scenarios/V06", "items": ["it_0013", "it_0001"],
     "expect": {"it_0013": "fail"}, "intended": VISUALS,
     "about": "a generic item against a well-made one (the generic one must fail)"},
    {"id": "critic-two-well-made", "role": "critic", "fixture": "roles/critic-two-well-made",
     "items": ["it_0032", "it_0001"], "expect": {"it_0032": "pass", "it_0001": "pass"}, "intended": VISUALS,
     "about": "two well-made items (both must pass)"},
    {"id": "reader-lean", "role": "reader", "fixture": "scenarios/V08", "tests": ["T-0004"],
     "expect": {"T-0004": "act"}, "counts": {"T-0004": (31, 420)},
     "about": "a lean of about 0.66 after discounting (call act)"},
)
CASE_IDS = tuple(case["id"] for case in CASES)
TAB_OF = {"plan-checker": "Checks", "build-checker": "Checks", "critic": "Checks", "reader": "Results"}


class LabError(RuntimeError):
    """The lab cannot build a case as specified (a brief brace it cannot fill, a missing brief or fixture)."""


def case_by_id(case_id: str) -> dict:
    for case in CASES:
        if case["id"] == case_id:
            return case
    raise LabError(f"unknown role case {case_id!r}; the cases are {', '.join(CASE_IDS)}")


# ----------------------------------------------------------------------------------------------------------------------
# the brief


def brief_path(repo, role: str) -> Path:
    return Path(repo) / "skills" / "hill-climb" / "references" / "roles" / f"{role}.md"


def read_brief(repo, role: str) -> str:
    """The brief a role is given: the file's text after its `---` line (what comes before tells the main agent how to
    fill it), read at run time so the test always uses the shipped wording."""
    path = brief_path(repo, role)
    if not path.is_file():
        raise LabError(f"no brief for the {role} at {path}")
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^---[ \t]*$", text, maxsplit=1)
    return (parts[1] if len(parts) == 2 else text).strip() + "\n"


def fill(template: str, facts: dict):
    """(the filled brief, the brace names it held). Every brace must have a fact; a leftover brace is a lab bug."""
    names = sorted(set(BRACE.findall(template)))
    missing = [name for name in names if name not in facts]
    if missing:
        raise LabError(f"the brief has braces the lab does not fill: {', '.join(missing)}")
    filled = BRACE.sub(lambda m: str(facts[m.group(1)]), template)
    leftover = sorted(set(BRACE.findall(filled)))
    if leftover:
        raise LabError(f"braces left in the filled brief: {', '.join(leftover)}")
    return filled, names


def label_order(case: dict, trial: int) -> list:
    """The critic's items in a random order that is the same for the same case and trial."""
    items = list(case["items"])
    random.Random(f"{case['id']}:{trial}").shuffle(items)
    return items


def _next_keys(rows, prefix: str, count: int, prefer=None) -> list:
    used = {int(m.group(1)) for r in rows for m in [re.fullmatch(rf"{prefix}-(\d+)", str(next(iter(r.values()), "")))] if m}
    out = []
    for want in prefer or []:
        if want not in used and len(out) < count:
            out.append(want)
            used.add(want)
    number = max([n for n in used if n < 100] or [0]) + 1
    while len(out) < count:
        if number not in used:
            out.append(number)
            used.add(number)
        number += 1
    return [f"{prefix}-{n:04d}" for n in out]


def aimed_at(case: dict, rows: dict, labels: dict) -> str:
    """Who each of the critic's items is aimed at, under its neutral label ("A: ...; B: ..."): the item's own plan when
    its Tests row says (an `aimed_at` column), else the case's own value, else AIMED_AT."""
    plans = {str(r.get("item_id") or "").strip(): r for r in rows.get("Tests", [])}
    default = case.get("aimed_at") or AIMED_AT
    parts = []
    for label in sorted(labels):
        item = labels[label]
        who = str((plans.get(item) or {}).get("aimed_at") or "").strip() or default
        parts.append(f"{label}: {who}")
    return "; ".join(parts)


def facts_for(case: dict, run_dir: Path, now: str, label_map=None) -> dict:
    """The facts the case's brief asks for, from its built run folder, the platform's time and (for the critic) the
    labels its items are shown under."""
    import fixtures

    rows = fixtures.read_workbook(Path(run_dir) / "work" / "workbook")
    charter = {r["field"]: r["value"] for r in rows.get("Charter", [])}
    role = case["role"]
    tab = TAB_OF[role]
    facts = {
        "goal": GOAL,
        "now": now,
        "workbook": "the folder `workbook/` in your working folder, one CSV file per tab, such as `workbook/Tests.csv` "
                    "and `workbook/Checks.csv`",
        "write_how": f"Python's `csv` module, opening `workbook/{tab}.csv` in append mode and writing each row in the order "
                     f"of that file's own header; never rewrite the file",
        "other_facts": case.get("other_facts", ""),
    }
    if role in ("plan-checker", "reader"):
        facts["test_ids"] = ", ".join(case["tests"])
    if role == "plan-checker":
        facts["platform"] = "`sim catalog`, run in your working folder"
        facts["keys"] = ", ".join(_next_keys(rows["Checks"], "CK", len(case["tests"])))
    if role == "reader":
        facts["platform"] = ("`sim report`, run in your working folder, with `--campaign`, `--since` and `--until` to cut "
                             "a window, and `sim comments CAMPAIGN` for what people wrote under an ad")
        facts["second_source"] = ("`sim attribution`, the app's own count of conversions, where a conversion can arrive up "
                                  "to 2 days after its click")
        prefer = [int(t.split("-")[1]) for t in case["tests"]]
        facts["keys"] = ", ".join(_next_keys(rows["Results"], "R", len(case["tests"]), prefer))
    if role == "build-checker":
        first = next(iter(case["items"]))
        facts["items"] = "; ".join(f"{item}, built for test {test}" for item, test in case["items"].items())
        facts["built_item_command"] = f"`sim manifest ITEM`, run in your working folder (for example `sim manifest {first}`)"
        facts["keys"] = ", ".join(_next_keys(rows["Checks"], "CK", len(case["items"])))
    if role == "critic":
        labels = [chr(ord("A") + i) for i in range(len(case["items"]))]
        facts["items"] = "\n".join(f"- {label}: an ad, seen with `sim preview {label}`" for label in labels)
        facts["how_to_see_them"] = "`sim preview A`, `sim preview B` and so on, run in your working folder"
        facts["aimed_at"] = aimed_at(case, rows, label_map or {})
        facts["quality_floor"] = charter.get("quality_floor") or NEUTRAL_QUALITY_FLOOR
        facts["where_they_meet_it"] = WHERE
        facts["intended_difference"] = case["intended"]
        facts["keys"] = ", ".join(_next_keys(rows["Checks"], "CK", len(case["items"])))
    return facts


def prepare(case: dict, trial: int, run_dir: Path, hidden_dir: Path, repo, python: str = sys.executable) -> dict:
    """Build the case's folder and fill its brief: {"brief", "braces", "facts", "labels"}. Writes the critic's label map
    into the hidden folder only."""
    import fixtures

    kind, _, name = case["fixture"].partition("/")
    folder = LAB / kind / name
    if not (folder / "fixture.json").is_file():
        raise LabError(f"no fixture at {folder}")
    meta = fixtures.build_scenario(name, run_dir, hidden_dir, LAB, python, folder=folder, kind="role")
    labels = {}
    if case["role"] == "critic":
        labels = {chr(ord("A") + i): item for i, item in enumerate(label_order(case, trial))}
        (Path(hidden_dir) / "previews.json").write_text(json.dumps(labels, indent=1) + "\n", encoding="utf-8")
    facts = facts_for(case, run_dir, meta["now"], labels)
    brief, braces = fill(read_brief(repo, case["role"]), facts)
    return {"brief": brief, "braces": braces, "facts": facts, "labels": labels}


# ----------------------------------------------------------------------------------------------------------------------
# grading the role's row


def _verdict(row):
    for word in ("pass", "fail"):
        if c.is_label(row.get("verdict"), "checks", word):
            return word
    return None


def _role_rows(run, case):
    tab = TAB_OF[case["role"]]
    return [r for r in run.new_rows(tab) if c.role_named(r.get("written_by"), case["role"])
            or c.role_named(r.get("role"), case["role"])] if tab == "Checks" else run.new_rows(tab)


def _label_of(row, labels, keys):
    """The critic's label for one of its rows: by `item_id` (the label it saw, or the item's id), else by the order of
    the keys it was given."""
    item = str(row.get("item_id") or "").strip()
    reverse = {v: k for k, v in labels.items()}
    if c.norm_key(item) in reverse:
        return reverse[c.norm_key(item)]
    match = re.fullmatch(r"(?:ad|item|label)?\s*\(?([A-Za-z])\)?\.?", item, re.I)
    if match and match.group(1).upper() in labels:
        return match.group(1).upper()
    key = c.norm_key(row.get("check_id"))
    order = [c.norm_key(k) for k in keys]
    if key in order and order.index(key) < len(labels):
        return sorted(labels)[order.index(key)]
    return None


def grade_case(run, case: dict, prepared: dict) -> list:
    """[check] for the row the role wrote."""
    rows = _role_rows(run, case)
    role = case["role"]
    checks = []
    if role in ("plan-checker", "build-checker"):
        targets = case["tests"] if role == "plan-checker" else list(case["items"])
        for target in targets:
            if role == "plan-checker":
                mine = [r for r in rows if c.text_names(r.get("test_id"), target)]
            else:
                test = case["items"][target]
                mine = [r for r in rows if c.norm_key(r.get("item_id")) == target
                        or (not str(r.get("item_id") or "").strip() and c.text_names(r.get("test_id"), test))]
            want = case["expect"][target]
            got = [_verdict(r) for r in mine]
            checks.append(c.check(f"the {role}'s row for {target} says {want}", bool(mine) and set(got) == {want},
                                  "; ".join(f"{r.get('check_id')}: {r.get('verdict')!r} ({str(r.get('reasons'))[:160]})"
                                            for r in mine) or f"no {role} row for {target}"))
    elif role == "critic":
        labels = prepared["labels"]
        keys = [k.strip() for k in prepared["facts"]["keys"].split(",")]
        by_item = {}
        for row in rows:
            label = _label_of(row, labels, keys)
            if label:
                by_item.setdefault(labels[label], []).append(row)
        unread = [labels[label] for label in sorted(labels) if labels[label] not in by_item]
        checks.append(c.check("the critic wrote a row for each item", not unread,
                              f"no row for {unread}" if unread else
                              "; ".join(f"{label}={labels[label]}" for label in sorted(labels))))
        for item, want in case["expect"].items():
            mine = by_item.get(item, [])
            got = [_verdict(r) for r in mine]
            checks.append(c.check(f"the critic's verdict on {item} is {want}", bool(mine) and set(got) == {want},
                                  "; ".join(f"{r.get('check_id')}: {r.get('verdict')!r} ({str(r.get('reasons'))[:160]})"
                                            for r in mine) or f"no critic row for {item}"))
        for item in case["items"]:
            if item not in case["expect"] and by_item.get(item):
                checks.append(c.check(f"(reported) the critic's verdict on {item}", True,
                                      ", ".join(str(r.get("verdict")) for r in by_item[item])))
    else:
        for test in case["tests"]:
            mine = [r for r in rows if c.text_names(r.get("test_id"), test)]
            calls = [str(r.get("call") or "") for r in mine]
            want = case["expect"][test]
            ok = bool(mine) and all(_leans(call) == want for call in calls)
            checks.append(c.check(f"the reader's row for {test} calls {want}", ok,
                                  "; ".join(f"{r.get('result_id')}: call {r.get('call')!r}, chance {r.get('chance_beats')!r}"
                                            for r in mine) or f"no Results row for {test}"))
            k, n = case["counts"][test]
            counted = [(c.parse_int(r.get("k")), c.parse_int(r.get("n"))) for r in mine]
            checks.append(c.check(f"the reader's row for {test} counts the plan's window ({k} of {n})",
                                  bool(mine) and all(pair == (k, n) for pair in counted),
                                  f"counts {counted}" if mine else f"no Results row for {test}"))
    return checks


def _leans(call: str):
    """act, stop or hold for a call, reading `act` as the record's word for a favored lean ("act (lean)" too)."""
    words = set(re.findall(r"[a-z]+", call.lower()))
    if words & {"stop", "drop", "hold", "inconclusive"}:
        return "stop" if words & {"stop", "drop"} else "hold"
    if words & {"act", "lean", "leans", "favored", "favoured", "favor", "favour"}:
        return "act"
    return None


# ----------------------------------------------------------------------------------------------------------------------
# trials


def plan_jobs(cases, trials: int = 3) -> list:
    return [{"case": case_id, "trial": t, "run_id": f"{case_id}-t{t}"} for case_id in cases for t in range(1, trials + 1)]


def record_for(run, case: dict, prepared: dict, info=None, run_id=None, trial=None) -> dict:
    checks = grade_case(run, case, prepared)
    tampering = run.tampering()
    status = session_status(info) if info else "regraded"
    if tampering:
        status = "invalid"
    ran_out = status in ("timeout", "budget", "crashed", "invalid")
    record = {"run_id": run_id, "case": case["id"], "role": case["role"], "trial": trial, "status": status,
              "passed": c.all_pass(checks) and not ran_out, "checks": checks, "tampering": tampering,
              "labels": prepared.get("labels") or {}, "braces": prepared.get("braces"),
              "keys": prepared.get("facts", {}).get("keys"), "brief_chars": len(prepared.get("brief") or "")}
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
        self.timeout_s = args.timeout


def run_job(job, ctx: Context) -> dict:
    case = case_by_id(job["case"])
    attempt, limited, tampered, attempts = 0, 0, 0, []
    while True:
        run_id = job["run_id"] + (f"-r{attempt}" if attempt else "")
        run_dir = ctx.lab_root / "runs" / ctx.batch / run_id
        hidden_dir = ctx.lab_root / "hidden" / str(uuid.uuid4())
        batch.remove_run(run_dir, hidden_dir)
        prepared = prepare(case, job["trial"], run_dir, hidden_dir, ctx.repo, ctx.python)
        info = run_session_with_accounts(
            ctx.pool, work=run_dir / "work", prompt=prepared["brief"], run_dir=run_dir, budget_usd=BUDGET_ROLE_USD,
            timeout_s=ctx.timeout_s, install_skill=False, repo=ctx.repo, aim=ctx.aim)
        dest = ctx.results / run_id
        if info.get("limited") and limited < LIMITED_RERUNS:
            ctx.pool.limited(info.get("label"))
            batch.copy_results(run_dir, hidden_dir, dest)
            batch.write_json(dest / "grade.json", {"run_id": run_id, "case": case["id"], "status": "limited",
                                                   "passed": False, "note": "account limit cut the session short; rerun"})
            batch.remove_run(run_dir, hidden_dir)
            attempts.append({"run_id": run_id, "status": "limited"})
            limited += 1
            attempt += 1
            continue
        run = c.load_run(run_dir, hidden_dir)
        record = record_for(run, case, prepared, info, run_id, job["trial"])
        record["attempts"] = attempts + [{"run_id": run_id, "status": record["status"]}]
        record["trial_of"] = job["run_id"]
        case_record = {"case": case["id"], "trial": job["trial"], "labels": prepared["labels"],
                       "facts": prepared["facts"], "braces": prepared["braces"]}
        batch.write_json(run_dir / "case.json", case_record)
        (run_dir / "brief.md").write_text(prepared["brief"], encoding="utf-8")
        batch.write_json(run_dir / "grade.json", record)
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


def regrade(ctx: Context) -> list:
    records = []
    for folder in sorted(p for p in ctx.results.iterdir() if p.is_dir()):
        old = _json(folder / "grade.json")
        saved = _json(folder / "run" / "case.json")
        if not old or old.get("status") == "limited" or not saved or not (folder / "run").is_dir():
            continue
        case = case_by_id(saved["case"])
        prepared = {"labels": saved.get("labels") or {}, "facts": saved.get("facts") or {},
                    "braces": saved.get("braces"), "brief": _text(folder / "run" / "brief.md")}
        session = _json(folder / "run" / "session.json")
        run = c.load_run(folder / "run", folder / "hidden")
        record = record_for(run, case, prepared, session if session.get("started_t") else None, old.get("run_id"),
                            saved.get("trial"))
        record["attempts"] = old.get("attempts", [])
        record["trial_of"] = old.get("trial_of")
        batch.write_json(folder / "grade.json", record)
        records.append(record)
    final = {}
    for record in records:
        final[record.get("trial_of") or record["run_id"]] = record
    return list(final.values())


def _json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def summarize(records, batch_name: str, started: float, ended: float, accounts=()) -> tuple:
    by_case = {}
    for record in records:
        by_case.setdefault(record.get("case"), []).append(record)
    rows = []
    for case in CASES:
        trials = by_case.get(case["id"], [])
        if not trials:
            continue
        passed = sum(1 for t in trials if t.get("passed"))
        rows.append({"case": case["id"], "role": case["role"], "about": case["about"], "trials": len(trials),
                     "passed": passed, "gate": f"{len(trials)} of {len(trials)}", "meets_gate": passed == len(trials),
                     "statuses": [t.get("status") for t in trials],
                     "failing": sorted({ch["name"] for t in trials for ch in t.get("checks", []) if not ch["pass"]}),
                     "cost_usd": round(sum(t.get("cost_usd") or 0 for t in trials), 3),
                     "wall_s": round(sum(t.get("wall_s") or 0 for t in trials), 1)})
    roles = {}
    for row in rows:
        roles.setdefault(row["role"], []).append(row["meets_gate"])
    summary = {"batch": batch_name, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
               "ended": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended)), "accounts": list(accounts),
               "cases": rows, "roles": {role: all(meets) for role, meets in roles.items()},
               "cost_usd": round(sum(r.get("cost_usd") or 0 for r in records), 3),
               "all_role_gates_met": bool(rows) and all(row["meets_gate"] for row in rows)}
    lines = [f"# Role tests {batch_name}", "",
             f"{summary['started']} to {summary['ended']}; accounts {', '.join(accounts) or 'n/a'}; reported cost "
             f"${summary['cost_usd']:.2f}. A role passes when each of its cases passes every trial.", "",
             "| Case | Role | What it shows the role | Passed | Meets gate | Trial statuses | Failing checks | Cost | "
             "Wall time |", "|---|---|---|---|---|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['case']} | {row['role']} | {row['about']} | {row['passed']} of {row['trials']} | "
                     f"{'yes' if row['meets_gate'] else 'NO'} | {', '.join(map(str, row['statuses']))} | "
                     f"{'; '.join(row['failing']) or '-'} | ${row['cost_usd']:.2f} | {row['wall_s'] / 60:.1f} min |")
    lines += ["", "| Role | All cases 3 of 3 |", "|---|---|"]
    for role, ok in summary["roles"].items():
        lines.append(f"| {role} | {'yes' if ok else 'NO'} |")
    return summary, "\n".join(lines) + "\n"


def dry_run(args, cases, ctx) -> int:
    """Print the plan, check that every case's brief fills (building each fixture in a scratch folder), and print one
    session's command. No session starts."""
    jobs = plan_jobs(cases, args.trials)
    for job in jobs:
        case = case_by_id(job["case"])
        print(job["run_id"], case["role"], f"${BUDGET_ROLE_USD}", f"expect {case['expect']}")
    scratch = Path(tempfile.mkdtemp(prefix="hc-roles-dry-"))
    problems = 0
    try:
        print("\nBriefs (read now from the repo, filled from each case's fixture):")
        for case_id in cases:
            case = case_by_id(case_id)
            try:
                prepared = prepare(case, 1, scratch / case_id / "run", scratch / case_id / "hidden", ctx.repo,
                                   ctx.python)
            except LabError as exc:
                problems += 1
                print(f"  {case_id}: LAB BUG: {exc}")
                continue
            print(f"  {case_id}: {brief_path(ctx.repo, case['role']).relative_to(ctx.repo)}, {len(prepared['brief'])} "
                  f"characters; braces filled: {', '.join(prepared['braces'])}; leftover braces: none"
                  + (f"; labels (hidden from the critic): {prepared['labels']}" if prepared["labels"] else ""))
            for name in prepared["braces"]:
                value = " ".join(str(prepared["facts"][name]).split())
                print(f"      {{{name}}} = {value[:110]}{'...' if len(value) > 110 else ''}")
            if args.show_briefs:
                print("\n" + prepared["brief"])
        argv = build_command(args.account or "<label>", "<the filled brief>", BUDGET_ROLE_USD)
        print("\nOne session (run from the case's work/ folder, no skill installed):")
        print(command_line(argv))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return 1 if problems else 0


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True)
    parser.add_argument("--cases", default=",".join(CASE_IDS))
    parser.add_argument("--trials", type=int, default=3)
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
    parser.add_argument("--keep", action="store_true", help="keep run and hidden folders in the lab root")
    parser.add_argument("--regrade", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-briefs", action="store_true", help="with --dry-run, print each filled brief")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    ctx = Context(args)
    cases = [s.strip() for s in args.cases.split(",") if s.strip()]
    for case_id in cases:
        case_by_id(case_id)
    started = time.time()
    if args.dry_run:
        return dry_run(args, cases, ctx)
    if args.regrade:
        records = regrade(ctx)
    else:
        ctx.results.mkdir(parents=True, exist_ok=True)
        try:
            records = batch.run_jobs(plan_jobs(cases, args.trials), lambda job: run_job(job, ctx),
                                     max_parallel=args.max_parallel, load_limit=args.load_limit,
                                     mem_limit_gb=args.mem_limit_gb)
        except NoEligibleAccount as exc:
            records = getattr(exc, "partial_results", [])
            summary, markdown = summarize(records, args.batch, started, time.time(), ctx.pool.history)
            summary["stopped"] = str(exc)
            batch.write_json(ctx.results / "summary.json", summary)
            (ctx.results / "summary.md").write_text(markdown + f"\nStopped: {exc}\n", encoding="utf-8")
            print(f"batch stopped: {exc}", file=sys.stderr)
            return 2
    records = [r for r in records if r.get("case")]
    summary, markdown = summarize(records, args.batch, started, time.time(), ctx.pool.history)
    batch.write_json(ctx.results / "summary.json", summary)
    (ctx.results / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
