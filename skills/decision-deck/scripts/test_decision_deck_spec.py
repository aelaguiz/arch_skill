"""Tests for the decision deck spec: loading, every validation rule that matters, and the evidence view.

The helpers here (spec_dict, make_spec_dir) build the four-decision spec the other test files share.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_spec as spec_mod  # noqa: E402

SVG = (b'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="30" viewBox="0 0 40 30">'
       b'<rect width="40" height="30" fill="#c98b4e"/></svg>')


def spec_dict() -> dict:
    """One decision per evidence kind: pictures, a diff, a chart and a table."""
    return {
        "title": "Shop relaunch",
        "decided": [{"title": "Ordering", "answer": "Pickup only at launch"}],
        "decisions": [
            {"id": "D1", "title": "Hero", "question": "Which hero layout?", "context": "Same photo in both.",
             "recommendation": {"option": "split", "why": "The headline stays readable."},
             "evidence": {"kind": "images"},
             "options": [
                 {"id": "split", "label": "Split", "images": ["img/a.svg"], "caption": "Side by side"},
                 {"id": "banner", "label": "Banner", "images": ["img/b.svg"], "caption": "Full width"}]},
            {"id": "D2", "title": "Returns", "question": "Use the new returns wording?",
             "context": "Refunds for one day instead of exchanges only.",
             "recommendation": {"option": "yes", "why": "Customers ask for refunds."},
             "evidence": {"kind": "diff", "before": "Exchanges only on the day of purchase.",
                          "after": "Exchanges or refunds within one day of purchase.",
                          "rule_now": "Exchanges or refunds within one day of purchase."},
             "options": [{"id": "yes", "label": "Use it"},
                         {"id": "change", "label": "Needs change", "ask_note": True}]},
            {"id": "D3", "title": "Delivery fee", "question": "Which delivery fee?", "context": "From the survey.",
             "recommendation": {"option": "free", "why": "Most orders."},
             "evidence": {"kind": "chart", "unit": "orders", "source": "Twelve weeks of orders",
                          "bars": [{"label": "Free over $25", "value": 310, "emphasis": True},
                                   {"label": "Flat fee", "value": 240},
                                   {"label": "Pickup only", "value": 180}]},
             "options": [{"id": "free", "label": "Free over $25"}, {"id": "flat", "label": "Flat fee"}]},
            {"id": "D4", "title": "Hours", "question": "Which opening hours?", "allow_note": False,
             "recommendation": {"option": None, "why": "Your call."},
             "evidence": {"kind": "table", "columns": ["Option", "Weekdays", "Staff"],
                          "rows": [["Early", "6:30 to 14:00", 2], ["Late", "9:00 to 17:30", 3]]},
             "options": [{"id": "early", "label": "Early", "key": "e"}, {"id": "late", "label": "Late"}]},
        ],
    }


def make_spec_dir(base: Path, data: dict | None = None) -> Path:
    """A spec folder under `base` with its two pictures; returns the spec.json path."""
    root = Path(base) / "round"
    (root / "img").mkdir(parents=True, exist_ok=True)
    (root / "img" / "a.svg").write_bytes(SVG)
    (root / "img" / "b.svg").write_bytes(SVG.replace(b"#c98b4e", b"#8a4b1f"))
    path = root / "spec.json"
    path.write_text(json.dumps(spec_dict() if data is None else data), encoding="utf-8")
    return path


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        self.spec_path = make_spec_dir(self.tmp)

    def load(self):
        return spec_mod.load_spec(self.spec_path)

    def errors_for(self, mutate) -> list[str]:
        data = spec_dict()
        mutate(data)
        return spec_mod.validate_spec(data, self.spec_path.parent)


class GoodSpecTest(TempDirCase):
    def test_valid_spec_loads_with_its_folder_and_path(self):
        spec = self.load()
        self.assertEqual(spec["root"], self.spec_path.parent)
        self.assertEqual(spec["path"], self.spec_path)
        self.assertEqual([d["id"] for d in spec["decisions"]], ["D1", "D2", "D3", "D4"])

    def test_a_picture_decision_needs_no_evidence_key(self):
        data = spec_dict()
        del data["decisions"][0]["evidence"]
        self.assertEqual(spec_mod.validate_spec(data, self.spec_path.parent), [])

    def test_optional_chart_keys_validate(self):
        def chart(d):
            d["decisions"][2]["evidence"] = {
                "kind": "chart", "type": "line", "prefix": "$", "decimals": 2, "series": ["Today", "New"],
                "side": {"title": "Read", "items": ["Fees cover the courier"]},
                "bars": [{"label": "Jan", "values": [1.5, 2]}, {"label": "Feb", "values": [1.6, 2.4]}]}
        self.assertEqual(self.errors_for(chart), [])


class BadSpecTest(TempDirCase):
    CASES = [
        ("no title", lambda d: d.pop("title"), "'title' must be a non-empty string"),
        ("no decisions", lambda d: d.update(decisions=[]), "'decisions' must be a non-empty list"),
        ("bad id", lambda d: d["decisions"][0].update(id="has space"), "decision id must match"),
        ("duplicate id", lambda d: d["decisions"][1].update(id="D1"), "duplicate decision id 'D1'"),
        ("no question", lambda d: d["decisions"][0].pop("question"), "'question' must be a non-empty string"),
        ("no options", lambda d: d["decisions"][1].update(options=[]), "'options' must be a non-empty list"),
        ("duplicate option", lambda d: d["decisions"][1]["options"][1].update(id="yes"), "duplicate option id 'yes'"),
        ("skip reserved", lambda d: d["decisions"][1]["options"][1].update(id="skip"), "is reserved"),
        ("reserved key", lambda d: d["decisions"][3]["options"][1].update(key="j"), "must be one lowercase letter"),
        ("duplicate key", lambda d: d["decisions"][3]["options"][1].update(key="e"), "duplicate key 'e'"),
        ("ask_note type", lambda d: d["decisions"][1]["options"][1].update(ask_note="yes"), "'ask_note' must be"),
        ("allow_note type", lambda d: d["decisions"][1].update(allow_note="no"), "'allow_note' must be"),
        ("no recommendation", lambda d: d["decisions"][0].pop("recommendation"), "'recommendation' must be"),
        ("unknown recommended option", lambda d: d["decisions"][0]["recommendation"].update(option="nope"),
         "names option 'nope'"),
        ("no why", lambda d: d["decisions"][0]["recommendation"].pop("why"), "'why' must be a non-empty string"),
        ("missing picture", lambda d: d["decisions"][0]["options"][0].update(images=["img/none.svg"]), "not found"),
        ("picture outside", lambda d: d["decisions"][0]["options"][0].update(images=["../x.svg"]),
         "resolves outside the spec's folder"),
        ("absolute picture", lambda d: d["decisions"][0]["options"][0].update(images=["/etc/hosts.png"]),
         "must be a path relative"),
        ("not a picture", lambda d: d["decisions"][0]["options"][0].update(images=["spec.json"]), "must end in"),
        ("unknown kind", lambda d: d["decisions"][1]["evidence"].update(kind="pages"), "evidence 'kind' must be"),
        ("images on a diff", lambda d: d["decisions"][1]["options"][0].update(images=["img/a.svg"]),
         "only a picture decision"),
        ("empty diff", lambda d: d["decisions"][1]["evidence"].update(before="", after=" "), "both empty"),
        ("diff side", lambda d: d["decisions"][1]["evidence"].update(before=3), "'before' must be a string"),
        ("two emphases", lambda d: d["decisions"][2]["evidence"]["bars"][1].update(emphasis=True),
         "at most one bar"),
        ("negative bar", lambda d: d["decisions"][2]["evidence"]["bars"][1].update(value=-1), "'value' must be"),
        ("bad chart type", lambda d: d["decisions"][2]["evidence"].update(type="pie"), "'type' must be one of"),
        ("long prefix", lambda d: d["decisions"][2]["evidence"].update(prefix="USD$"), "'prefix' must be"),
        ("too many decimals", lambda d: d["decisions"][2]["evidence"].update(decimals=5), "'decimals' must be"),
        ("line with a note", lambda d: d["decisions"][2]["evidence"].update(
            type="line", bars=[{"label": "a", "value": 1, "note": "x"}, {"label": "b", "value": 2}]), "carry no note"),
        ("short row", lambda d: d["decisions"][3]["evidence"]["rows"].append(["Only one"]), "has 1 cells"),
        ("bad cell", lambda d: d["decisions"][3]["evidence"]["rows"].append(["x", None, 1]), "text or numbers"),
        ("bad decided", lambda d: d.update(decided=[{"title": "x"}]), "'answer' must be a non-empty string"),
        ("bad density", lambda d: d["decisions"][0]["evidence"].update(density=4), "'density' must be 1, 2 or 3"),
        ("shared twice", lambda d: (d["decisions"][0].update(references=[{"image": "img/a.svg"}]),
                                    d["decisions"][0]["evidence"].update(references=[{"image": "img/b.svg"}])),
         "give 'references' in one place"),
    ]

    def test_each_broken_spec_names_its_problem(self):
        for name, mutate, needle in self.CASES:
            with self.subTest(name):
                errors = self.errors_for(mutate)
                self.assertTrue(any(needle in e for e in errors), f"{needle!r} not in {errors}")

    def test_load_spec_lists_every_problem_at_once(self):
        data = spec_dict()
        data["decisions"][0]["recommendation"]["option"] = "nope"
        data["decisions"][3]["evidence"]["rows"].append(["x"])
        self.spec_path.write_text(json.dumps(data))
        with self.assertRaises(spec_mod.SpecError) as ctx:
            self.load()
        self.assertIn("names option 'nope'", str(ctx.exception))
        self.assertIn("has 1 cells", str(ctx.exception))

    def test_a_file_that_is_not_json_is_refused(self):
        self.spec_path.write_text("{not json")
        with self.assertRaises(spec_mod.SpecError):
            self.load()

    def test_top_level_must_be_an_object(self):
        self.assertEqual(spec_mod.validate_spec([], self.spec_path.parent),
                         ["spec: the top level must be a JSON object"])


class EvidenceViewTest(TempDirCase):
    def test_picture_columns_run_ours_then_options_then_references(self):
        data = copy.deepcopy(spec_dict())
        dec = data["decisions"][0]
        dec["evidence"].update(shared=[{"image": "img/a.svg", "caption": "Today"}],
                               references=[{"image": "img/b.svg"}], views=["Desktop"])
        ev = spec_mod.evidence_of(dec)
        self.assertEqual(ev["kind"], "images")
        self.assertEqual([c["tag"] for c in ev["columns"]],
                         ["Ours", "split", "banner", spec_mod.DEFAULT_REFERENCES_TITLE])
        self.assertEqual(ev["columns"][1]["caption"], "Side by side")
        self.assertEqual(ev["views"], ["Desktop"])
        self.assertEqual(ev["density"], 1)

    def test_text_kinds_pass_through_and_no_pictures_is_kind_none(self):
        spec = self.load()
        self.assertEqual(spec_mod.evidence_of(spec["decisions"][1])["kind"], "diff")
        self.assertEqual(spec_mod.evidence_of(spec["decisions"][2])["bars"][0]["value"], 310)
        bare = {"options": [{"id": "a", "label": "A"}]}
        self.assertEqual(spec_mod.evidence_of(bare), {"kind": "none"})

    def test_option_keys_digits_by_position_and_an_optional_letter(self):
        keys = spec_mod.option_keys(self.load()["decisions"][3])
        self.assertEqual(keys, [{"id": "early", "key": "e", "alt": "1"}, {"id": "late", "key": "2", "alt": "2"}])

    def test_takes_note_unless_allow_note_is_false(self):
        spec = self.load()
        self.assertTrue(spec_mod.takes_note(spec["decisions"][0]))
        self.assertFalse(spec_mod.takes_note(spec["decisions"][3]))


if __name__ == "__main__":
    unittest.main()
