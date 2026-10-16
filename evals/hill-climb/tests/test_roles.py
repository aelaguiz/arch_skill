"""Layer 1: the role tests' runner (PLAN.md 13.2) with a fake `aim`. No model or account is ever used.

The briefs here are stand-ins written into a scratch repo with the braces each real brief holds, so these tests check
the runner's filling, labelling and grading, never the skill's wording; `run_roles.py --dry-run` fills the shipped
briefs.
"""
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from runner import run_roles
from tests.test_runner import PROBE3, install_fake_aim

BRACES = {
    "plan-checker": "{goal} {keys} {now} {other_facts} {platform} {test_ids} {workbook} {write_how}",
    "build-checker": "{built_item_command} {goal} {items} {keys} {now} {other_facts} {workbook} {write_how}",
    "critic": "{aimed_at} {goal} {how_to_see_them} {intended_difference} {items} {keys} {now} {quality_floor} "
              "{where_they_meet_it} {workbook} {write_how}",
    "reader": "{goal} {keys} {now} {other_facts} {platform} {second_source} {test_ids} {workbook} {write_how}",
}


def stand_in_repo(root: Path, extra=None) -> Path:
    repo = root / "repo"
    folder = repo / "skills" / "hill-climb" / "references" / "roles"
    folder.mkdir(parents=True)
    for role, braces in BRACES.items():
        body = braces + (" " + extra if extra and role == "plan-checker" else "")
        (folder / f"{role}.md").write_text(f"# {role} brief\n\nNotes for the main agent {{not_sent}}.\n\n---\n\n"
                                           f"You are the {role}. {body}\n", encoding="utf-8")
    return repo


def append(tab, line):
    return f"printf '%s\\n' '{line}' >> workbook/{tab}.csv"


class Filling(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_the_brief_is_the_part_after_its_rule_and_every_brace_is_filled(self):
        repo = stand_in_repo(self.root)
        text = run_roles.read_brief(repo, "plan-checker")
        self.assertTrue(text.startswith("You are the plan-checker."))
        self.assertNotIn("not_sent", text)
        facts = {name: f"<{name}>" for name in run_roles.BRACE.findall(BRACES["plan-checker"])}
        filled, names = run_roles.fill(text, facts)
        self.assertEqual(names, sorted(facts))
        self.assertNotRegex(filled, r"\{[a-z_]+\}")
        with self.assertRaises(run_roles.LabError):
            run_roles.fill(text + "{surprise}", facts)
        with self.assertRaises(run_roles.LabError):
            run_roles.fill(text, dict(facts, goal="{now}"))

    def test_every_case_fills_from_its_fixture(self):
        repo = stand_in_repo(self.root)
        for case in run_roles.CASES:
            with self.subTest(case=case["id"]):
                prepared = run_roles.prepare(case, 1, self.root / case["id"] / "run", self.root / case["id"] / "hidden",
                                             repo)
                self.assertEqual(sorted(prepared["braces"]), sorted(run_roles.BRACE.findall(BRACES[case["role"]])))
                self.assertNotRegex(prepared["brief"], r"\{[a-z_]+\}")
                hidden = self.root / case["id"] / "hidden"
                if case["role"] == "critic":
                    labels = json.loads((hidden / "previews.json").read_text())
                    self.assertEqual(sorted(labels.values()), sorted(case["items"]))
                    self.assertEqual(labels, prepared["labels"])
                    for item in case["items"]:
                        self.assertNotIn(item, prepared["brief"])      # the critic sees labels only
                    # who each item is aimed at, under the same labels; the bar is neutral without a quality_floor
                    self.assertEqual([part.split(":")[0] for part in prepared["facts"]["aimed_at"].split("; ")],
                                     sorted(labels))
                    self.assertIn("people who play poker", prepared["facts"]["aimed_at"])
                    self.assertEqual(prepared["facts"]["quality_floor"], run_roles.NEUTRAL_QUALITY_FLOOR)
                    self.assertFalse(list((self.root / case["id"] / "run").glob("*.json")))
                else:
                    self.assertFalse((hidden / "previews.json").exists())
                meta = json.loads((hidden / "meta.json").read_text())
                self.assertEqual((meta["kind"], meta["now"] in prepared["brief"]), ("role", True))

    def test_label_order_is_random_but_repeatable(self):
        case = run_roles.case_by_id("critic-generic")
        orders = {tuple(run_roles.label_order(case, t)) for t in range(1, 9)}
        self.assertEqual(orders, {("it_0013", "it_0001"), ("it_0001", "it_0013")})
        self.assertEqual(run_roles.label_order(case, 3), run_roles.label_order(case, 3))

    def test_a_critics_row_is_tied_to_its_item_by_label_id_or_key_order(self):
        labels = {"A": "it_0001", "B": "it_0013"}
        keys = ["CK-0011", "CK-0012"]
        for item_id, want in (("A", "A"), ("item b", "B"), ("Ad A", "A"), ("it_0013", "B"), ("(B)", "B")):
            self.assertEqual(run_roles._label_of({"item_id": item_id, "check_id": "CK-0099"}, labels, keys), want)
        self.assertEqual(run_roles._label_of({"item_id": "", "check_id": "CK-0012"}, labels, keys), "B")
        self.assertIsNone(run_roles._label_of({"item_id": "the second one", "check_id": "CK-0099"}, labels, keys))

    def test_a_lean_is_read_as_act(self):
        for call, want in (("act", "act"), ("Act (lean)", "act"), ("lean", "act"), ("hold", "hold"),
                           ("stop", "stop"), ("act, then hold", "hold"), ("", None)):
            self.assertEqual(run_roles._leans(call), want, call)

    def test_dry_run_reports_a_brace_the_lab_cannot_fill(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = run_roles.main(["--batch", "dry", "--dry-run", "--repo", str(stand_in_repo(self.root)),
                                   "--cases", "plan-checker-sound,critic-generic", "--trials", "2"])
        self.assertEqual(code, 0, out.getvalue())
        text = out.getvalue()
        for line in ("plan-checker-sound-t1 plan-checker", "critic-generic-t2 critic", "leftover braces: none",
                     "aim claude run '<label>' -- -p '<the filled brief>' --model sonnet"):
            self.assertIn(line, text)
        bad = self.root / "bad"
        bad.mkdir()
        out = io.StringIO()
        with redirect_stdout(out):
            code = run_roles.main(["--batch", "dry", "--dry-run", "--repo", str(stand_in_repo(bad, "{tests_due}")),
                                   "--cases", "plan-checker-sound"])
        self.assertEqual(code, 1)
        self.assertIn("LAB BUG: the brief has braces the lab does not fill: tests_due", out.getvalue())


class TrialsOnAFakeAim(unittest.TestCase):
    """run_roles end to end: a fixture's folder, the filled brief as the prompt, the fake aim writing the role's row,
    grading, results, the summary and a regrade."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        self.fake = install_fake_aim(self.root)
        self.log = self.root / "aim_log.jsonl"
        self.repo = stand_in_repo(self.root)
        self.saved = {k: os.environ.get(k) for k in ("FAKE_AIM_LOG", "FAKE_AIM_REPLAY", "FAKE_AIM_RUN",
                                                      "FAKE_AIM_RUN_IF")}
        os.environ.update(FAKE_AIM_LOG=str(self.log), FAKE_AIM_REPLAY=str(PROBE3))

    def tearDown(self):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def context(self, *extra):
        args = run_roles.parse_args(["--batch", "t", "--lab-root", str(self.root / "lab"), "--results-dir",
                                     str(self.root / "results"), "--aim", str(self.fake), "--account", "fake-label",
                                     "--repo", str(self.repo), "--timeout", "60"] + list(extra))
        ctx = run_roles.Context(args)
        ctx.pool._log = lambda message: None
        ctx.results.mkdir(parents=True, exist_ok=True)
        return ctx

    def trial(self, case_id, command, trial=1):
        os.environ.update(FAKE_AIM_RUN=command, FAKE_AIM_RUN_IF="You are the")
        return run_roles.run_job({"case": case_id, "trial": trial, "run_id": f"{case_id}-t{trial}"}, self.context())

    def prompts(self):
        return [call["argv"][call["argv"].index("-p") + 1] for call in
                (json.loads(line) for line in self.log.read_text().splitlines()) if "label" in call]

    def test_a_plan_checker_that_fails_the_other_days_plan_passes_the_case(self):
        line = "CK-0010,T-0031,,plan-checker,fail,the comparison ran on other days,2026-11-08T00:00:00Z,plan-checker"
        record = self.trial("plan-checker-other-days", append("Checks", line))
        self.assertEqual(record["status"], "ok")
        self.assertTrue(record["passed"], record["checks"])
        prompt = self.prompts()[-1]
        self.assertTrue(prompt.startswith("You are the plan-checker."))
        self.assertNotRegex(prompt, r"\{[a-z_]+\}")
        for fact in ("T-0031", "CK-0010", "2026-11-08T00:00:00Z", "`sim catalog`"):
            self.assertIn(fact, prompt)
        dest = self.root / "results" / "plan-checker-other-days-t1"
        for rel in ("grade.json", "run/case.json", "run/brief.md", "run/stream.jsonl", "hidden/meta.json"):
            self.assertTrue((dest / rel).exists(), rel)
        self.assertFalse((self.root / "lab" / "runs" / "t" / "plan-checker-other-days-t1").exists())
        passing = line.replace(",fail,", ",pass,")
        record = self.trial("plan-checker-other-days", append("Checks", passing), trial=2)
        self.assertFalse(record["passed"])
        self.assertEqual([ch["name"] for ch in record["checks"] if not ch["pass"]],
                         ["the plan-checker's row for T-0031 says fail"])

    def test_no_row_fails_the_case(self):
        record = self.trial("build-checker-clean", "true")
        self.assertFalse(record["passed"])
        self.assertIn("no build-checker row for it_0006", record["checks"][0]["evidence"])

    def test_the_critic_case_reads_rows_through_the_hidden_labels(self):
        case = run_roles.case_by_id("critic-generic")
        order = run_roles.label_order(case, 1)
        rows = []
        for i, item in enumerate(order):
            label = chr(ord("A") + i)
            verdict = "fail" if item == "it_0013" else "pass"
            rows.append(append("Checks", f"CK-00{11 + i},,{label},critic,{verdict},judged {label},"
                                         f"2026-11-08T00:00:00Z,critic"))
        record = self.trial("critic-generic", " && ".join(rows))
        self.assertTrue(record["passed"], record["checks"])
        self.assertEqual(record["labels"], {chr(ord("A") + i): item for i, item in enumerate(order)})
        names = [ch["name"] for ch in record["checks"]]
        self.assertIn("(reported) the critic's verdict on it_0001", names)
        self.assertNotIn("it_0013", self.prompts()[-1])
        both_pass = " && ".join(r.replace(",fail,", ",pass,") for r in rows)
        record = self.trial("critic-generic", both_pass, trial=2)
        self.assertFalse(record["passed"])

    def test_the_reader_case_needs_act_on_the_plans_window(self):
        line = "R-0004,T-0004,w,platform conversions,31,420,42.00,7.4%,54 of 870,0.67,flat prior,a few,act,n,," \
               "2026-11-08T00:00:00Z,reader"
        header = "result_id,test_id,window,metric,k,n,spend,rate_text,versus,chance_beats,method,signals,call,notes"
        record = self.trial("reader-lean", append("Results", line))
        self.assertTrue(record["passed"], record["checks"])
        self.assertIn(header, (self.root / "results" / "reader-lean-t1" / "run" / "work" / "workbook" /
                               "Results.csv").read_text())
        held = line.replace(",act,", ",hold,")
        self.assertFalse(self.trial("reader-lean", append("Results", held), trial=2)["passed"])
        wrong = line.replace(",31,420,", ",31,560,")
        record = self.trial("reader-lean", append("Results", wrong), trial=3)
        self.assertEqual([ch["name"] for ch in record["checks"] if not ch["pass"]],
                         ["the reader's row for T-0004 counts the plan's window (31 of 420)"])

    def test_summary_gates_and_regrade(self):
        line = "CK-0010,T-0031,,plan-checker,fail,other days,2026-11-08T00:00:00Z,plan-checker"
        records = [self.trial("plan-checker-other-days", append("Checks", line), trial=t) for t in (1, 2, 3)]
        records.append(self.trial("plan-checker-sound", append("Checks", line), trial=1))
        summary, markdown = run_roles.summarize(records, "t", 0, 60, ["fake-label"])
        rows = {row["case"]: row for row in summary["cases"]}
        self.assertTrue(rows["plan-checker-other-days"]["meets_gate"])
        self.assertFalse(rows["plan-checker-sound"]["meets_gate"])
        self.assertEqual(summary["roles"], {"plan-checker": False})
        self.assertIn("| plan-checker-other-days | plan-checker |", markdown)
        regraded = run_roles.regrade(self.context("--regrade"))
        self.assertEqual(sorted(r["run_id"] for r in regraded), ["plan-checker-other-days-t1",
                                                                 "plan-checker-other-days-t2",
                                                                 "plan-checker-other-days-t3", "plan-checker-sound-t1"])
        self.assertEqual({r["run_id"]: r["passed"] for r in regraded},
                         {r["run_id"]: r["passed"] for r in records})


if __name__ == "__main__":
    unittest.main()
