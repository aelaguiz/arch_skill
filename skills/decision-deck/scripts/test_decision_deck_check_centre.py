"""Tests for the left pane beside a taller side panel (decision_deck_css.CENTRE_CSS) and its check, OFFCENTRE
(decision_deck_check_centre.py). One round holds every chart that can stand beside a side panel (the SVG bars, the
grid bars, the line), each with a tall panel, then the slides that must draw as before: a left pane taller than its
panel, one so tall it scales down whole, and each chart with no panel. The earlier look is the page CSS without
CENTRE_CSS. Only where Playwright and its Chromium are installed."""
import copy
import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_css as css  # noqa: E402
import decision_deck_spec as spec_mod  # noqa: E402
from test_decision_deck_spec import make_spec_dir, spec_dict  # noqa: E402

TALL_SIDE = {"title": "What changes for customers", "items": [
    f"Change {k}: a line long enough to wrap onto a second line inside the side panel" for k in range(1, 9)]}
SHORT_SIDE = {"items": ["Most orders are over $25"]}
BARS = [{"label": "Free over $25", "value": 310, "emphasis": True}, {"label": "Flat fee", "value": 240},
        {"label": "Pickup only", "value": 180}]
WEEKS = [{"label": f"Week {k}", "value": 100 + 15 * k} for k in range(1, 7)]
MORE_WEEKS = [{"label": f"Week {k}", "value": 100 + 15 * k} for k in range(1, 17)]
DAYS = [{"label": d, "value": v} for d, v in (("Mon", 30), ("Tue", 50), ("Wed", 40), ("Thu", 60))]
EVIDENCE = [   # D1 to D3 have a panel taller than their chart; the rest must draw as before
    {"kind": "chart", "unit": "orders", "bars": BARS, "side": TALL_SIDE},
    {"kind": "chart", "prefix": "$", "bars": BARS, "side": TALL_SIDE},
    {"kind": "chart", "type": "line", "bars": DAYS, "side": TALL_SIDE},
    {"kind": "chart", "unit": "orders", "bars": WEEKS, "side": SHORT_SIDE},
    {"kind": "chart", "unit": "orders", "bars": MORE_WEEKS, "side": SHORT_SIDE},
    {"kind": "chart", "prefix": "$", "bars": MORE_WEEKS, "side": SHORT_SIDE},
    {"kind": "chart", "unit": "orders", "bars": BARS},
    {"kind": "chart", "prefix": "$", "bars": BARS},
    {"kind": "chart", "type": "line", "bars": DAYS},
]
LINE = re.compile(r"OFFCENTRE /d/(?P<n>\d) 1440 #sl-\d > div\.ev\.fit > div\.cx > div\.chart[^:]*: the left pane's "
                  r"drawing is (?P<h>\d+)px tall beside a (?P<side>\d+)px side panel and sits (?P<off>\d+)px "
                  r"(?P<way>above|below) the middle of its column; centre it vertically")


def charts_spec(base: Path, count: int = len(EVIDENCE)) -> dict:
    data = spec_dict()
    template = data["decisions"][2]                     # the delivery fee chart
    data["decisions"] = []
    for k, ev in enumerate(EVIDENCE[:count], 1):
        dec = copy.deepcopy(template)
        dec.update(id=f"D{k}", title=f"Delivery fee {k}", evidence=ev)
        data["decisions"].append(dec)
    return spec_mod.load_spec(make_spec_dir(base, data))


@unittest.skipUnless(importlib.util.find_spec("playwright"), "Python Playwright is not installed")
class CentreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import decision_deck_check as check
        from playwright.sync_api import sync_playwright
        try:
            with sync_playwright() as p:
                p.chromium.launch().close()
        except Exception as exc:  # noqa: BLE001
            raise unittest.SkipTest(f"Playwright's Chromium is not installed: {exc}")
        cls.check = staticmethod(check.check)
        cls.desktop, cls.phone = {"desktop": check.SIZES["desktop"]}, {"phone": check.SIZES["phone"]}

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name).resolve()

    @staticmethod
    def offcentre(problems):
        return [p for p in problems if p.startswith("OFFCENTRE ")]

    def test_the_deck_centres_every_left_pane_beside_a_taller_panel(self):
        problems = self.check(charts_spec(self.tmp), sizes=self.desktop)
        self.assertEqual(self.offcentre(problems), [], "\n".join(problems))

    def test_offcentre_catches_a_left_pane_stuck_to_the_top(self):
        with mock.patch.object(css, "CENTRE_CSS", ""):
            lines = self.offcentre(self.check(charts_spec(self.tmp), sizes=self.desktop))
        found = {m["n"]: m for m in map(LINE.fullmatch, lines) if m}
        self.assertEqual((len(lines), sorted(found)), (3, ["1", "2", "3"]), lines)     # D4 to D9 never
        for m in found.values():
            self.assertEqual(m["way"], "above", m[0])
            self.assertGreater(int(m["side"]), int(m["h"]), m[0])
            self.assertGreater(int(m["off"]), 50, m[0])

    def test_the_phone_stacks_the_panel_and_is_not_read(self):
        self.assertEqual(self.offcentre(self.check(charts_spec(self.tmp, 3), sizes=self.phone)), [])

    def test_only_the_slides_with_a_taller_panel_change(self):
        """D4 to D9 draw byte for byte as before at 1440x900, and every slide does on the phone."""
        spec = charts_spec(self.tmp)
        self.check(spec, out=self.tmp / "new")
        with mock.patch.object(css, "CENTRE_CSS", ""):
            self.check(spec, out=self.tmp / "old")
        shots = sorted(p.name for p in (self.tmp / "new").glob("*.png"))
        self.assertEqual(len(shots), 2 * (len(EVIDENCE) + 2), shots)
        changed = [n for n in shots if (self.tmp / "new" / n).read_bytes() != (self.tmp / "old" / n).read_bytes()]
        self.assertEqual(changed, ["desktop-slide1.png", "desktop-slide2.png", "desktop-slide3.png"])


if __name__ == "__main__":
    unittest.main()
