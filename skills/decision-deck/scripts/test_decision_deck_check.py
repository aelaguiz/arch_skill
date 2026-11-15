"""Tests for decision_deck_check.py: the spec checks, the PNG manifest, the exit codes, and (only where Playwright and
its Chromium are installed) one rendered run."""
import contextlib
import copy
import importlib.util
import io
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_check_pngs as pngs  # noqa: E402
import decision_deck_check_spec as checks  # noqa: E402
import decision_deck_stamp as stamp  # noqa: E402
from test_decision_deck_spec import TempDirCase, spec_dict  # noqa: E402

CHECK = Path(__file__).resolve().parent / "decision_deck_check.py"


def diff_spec(*diffs) -> dict:
    """A spec whose decisions are diffs: each (id, before, after, context)."""
    data = spec_dict()
    template = data["decisions"][1]
    data["decisions"] = []
    for did, before, after, context in diffs:
        dec = copy.deepcopy(template)
        dec.update(id=did, context=context)
        dec["evidence"].update(before=before, after=after)
        data["decisions"].append(dec)
    return data


class SpecChecksTest(unittest.TestCase):
    RECAP = "Refunds for one day instead of exchanges only."

    def test_a_clean_spec_has_no_problems(self):
        problems, warnings = checks.spec_lines(spec_dict(), links=False)
        self.assertEqual((problems, warnings), ([], []))

    def test_too_many_changes_on_one_slide(self):
        before = "\n\n".join(f"Rule {k}: the oven opens at six." for k in range(9))
        after = before.replace("six", "seven")
        lines = checks.size_lines(diff_spec(("D1", before, after, self.RECAP)))
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("TOOBIG D1: 9 changes on one slide"))

    def test_a_diff_needs_a_recap(self):
        lines = checks.size_lines(diff_spec(("D1", "Open at six.", "Open at seven.", "short")))
        self.assertEqual(lines, ["NORECAP D1: add a recap of what changed in context"])

    def test_the_same_change_on_two_slides_is_a_repeat(self):
        same = ("Bread is sold until it runs out.", "Bread is sold until four in the afternoon.")
        data = diff_spec(("D1", *same, self.RECAP), ("D2", "Shop: " + same[0], "Shop: " + same[1], self.RECAP),
                         ("D3", "Yes.", "No.", self.RECAP), ("D4", "Yes.", "No.", self.RECAP))
        lines = checks.repeat_lines(data)
        self.assertEqual(len(lines), 1)                     # the short Yes/No pair is too generic to count
        self.assertTrue(lines[0].startswith("REPEAT D1, D2: the same change shows more than once"))

    def test_dead_links_are_problems_and_local_links_only_warnings(self):
        data = spec_dict()
        data["decisions"][0]["context"] = "See https://example.com/dead and http://127.0.0.1:9/local."
        data["decisions"][2]["evidence"]["source"] = "https://example.com/ok"
        answers = {"https://example.com/dead": "HTTP 404", "http://127.0.0.1:9/local": "no answer: refused",
                   "https://example.com/ok": ""}
        problems, warnings = checks.link_lines(data, probe_fn=answers.get)
        self.assertEqual(problems, ["DEADLINK D1: https://example.com/dead (HTTP 404)"])
        self.assertEqual(len(warnings), 1)
        self.assertTrue(warnings[0].startswith("WARNING D1: http://127.0.0.1:9/local opens only where"))

    def test_is_local(self):
        for url, local in (("http://localhost:8/x", True), ("http://[::1]/", True), ("https://example.com", False),
                           ("http://[bad", False)):
            with self.subTest(url):
                self.assertEqual(checks.is_local(url), local)


class PngManifestTest(TempDirCase):
    def test_the_first_run_prints_nothing_and_later_runs_name_changed_pngs(self):
        out = self.tmp / "pngs"
        out.mkdir()
        for name in ("desktop-cover.png", "desktop-slide1.png", "desktop-slide2.png"):
            (out / name).write_bytes(name.encode())
        names = ["desktop-cover.png", "desktop-slide1.png", "desktop-slide2.png"]
        self.assertIsNone(pngs.report(out, names))
        (out / "desktop-slide1.png").write_bytes(b"changed")
        (out / "desktop-slide2.png").unlink()
        self.assertEqual(pngs.report(out, names[:2]),
                         "PNGS 1 changed since the last run here: desktop-slide1.png; 1 removed: desktop-slide2.png "
                         "(1 unchanged)")

    def test_a_malformed_manifest_counts_as_a_first_run(self):
        out = self.tmp / "pngs"
        out.mkdir()
        (out / pngs.MANIFEST).write_text("{not json")
        (out / "a.png").write_bytes(b"x")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertIsNone(pngs.report(out, ["a.png"]))
        self.assertIn("treating this as the first run here", err.getvalue())


class CheckCliTest(TempDirCase):
    def run_check(self, *args):
        return subprocess.run([sys.executable, str(CHECK), *map(str, args)], capture_output=True, text=True,
                              timeout=180, cwd=self.tmp)

    def test_help_and_a_bad_spec(self):
        self.assertEqual(self.run_check("--help").returncode, 0)
        self.spec_path.write_text("{}")
        out = self.run_check("--spec", self.spec_path, "--no-link-probe")
        self.assertEqual(out.returncode, 2)
        self.assertIn("spec is invalid", out.stderr)

    @unittest.skipUnless(importlib.util.find_spec("playwright"), "Python Playwright is not installed")
    def test_a_clean_round_renders_and_writes_the_stamp(self):
        out_dir = self.tmp / "pngs"
        out = self.run_check("--spec", self.spec_path, "--no-link-probe", "--out", out_dir)
        if out.returncode == 2 and "Chromium" in out.stderr:
            self.skipTest("Playwright's Chromium is not installed")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(out.stdout.strip().splitlines()[-1], "CLEAN 6 routes at 1440x900 and 390x844")
        self.assertEqual(len(list(out_dir.glob("*.png"))), 12)
        self.assertEqual(stamp.stamp_problem(self.load()), "")


if __name__ == "__main__":
    unittest.main()
