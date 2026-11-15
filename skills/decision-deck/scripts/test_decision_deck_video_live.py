"""Live tests for the decision deck's "video" slide in headless Google Chrome, at 1440x900 and 390x844 (a phone).

The round of test_decision_deck_video.py with real clips made in a temp folder by ffmpeg (a two-second H.264 + AAC
MP4 and a VP9 + Opus WebM from its testsrc2 and sine sources). The proof of play: in the installed Google Chrome
(Playwright channel "chrome"; Playwright's own Chromium plays no H.264) play() is called on each clip's shown video
element; within 10 s its readyState must be 3 or more, its error null and its currentTime past where it started (the
#t=0.001 fragment starts it at 1 ms, so the test asks for 0.25 s past the start: the clip really played). The browser
runs with its sound muted and allowed to start a clip from script, as the check's does; the elements themselves are
never muted. Also: Chrome fetches the clips with byte ranges (206); a tab shows its clip, pauses the other and
records nothing; V steps the tabs; leaving the slide pauses a playing clip; the phone shows every clip one per row at
full width; the desktop answer row is whole on screen; decision_deck_check.py is clean on the round and names a clip
Chrome cannot play in a VIDEO line; Playwright's WebKit gets its `bytes=0-1` probe answered and plays both clips.
Each test skips, saying why, without ffmpeg, Python Playwright or the browser it needs.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_check_video import CHANNEL, LAUNCH_ARGS  # noqa: E402
from test_decision_deck_video_serve import LiveVideoCase  # noqa: E402

ADVANCE = 0.25              # seconds past the start that prove the clip played

PLAY = r"""
async (sel) => {
  const v = document.querySelector(sel), t0 = v.currentTime; let refused = null;
  try { await v.play(); } catch (x) { refused = String(x); }
  const end = Date.now() + 10000;
  while (Date.now() < end && !v.error && !(v.readyState >= 3 && v.currentTime > t0 + %s))
    await new Promise((r) => setTimeout(r, 50));
  const out = { readyState: v.readyState, error: v.error ? v.error.code : null, currentTime: v.currentTime,
                start: t0, refused: refused, muted: v.muted, src: v.currentSrc };
  v.pause();
  return out;
}
""" % ADVANCE

FFMPEG = {"today.mp4": ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart"],
          "calm.webm": ["-c:v", "libvpx-vp9", "-b:v", "200k", "-c:a", "libopus"]}


def make_clips(root: Path) -> None:
    """Write today.mp4 and calm.webm into `root` with ffmpeg: two seconds of a test pattern and a tone each."""
    for name, codec in FFMPEG.items():
        tone = "440" if name.endswith(".mp4") else "660"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=15:duration=2",
                        "-f", "lavfi", "-i", f"sine=frequency={tone}:duration=2", *codec, "-shortest",
                        str(root / name)], check=True, stdin=subprocess.DEVNULL, capture_output=True)


@unittest.skipUnless(importlib.util.find_spec("playwright"), "Python Playwright is not installed")
@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is not installed (it makes the test clips)")
class ChromeCase(LiveVideoCase):
    def setUp(self):
        super().setUp()
        make_clips(self.root)
        self.pw = None

    def playwright(self):
        """This test's Playwright, started on first use and stopped after the test."""
        if self.pw is None:
            from playwright.sync_api import sync_playwright
            self.pw = sync_playwright().start()
            self.addCleanup(self.pw.stop)
        return self.pw

    def chrome(self):
        try:
            browser = self.playwright().chromium.launch(channel=CHANNEL, args=list(LAUNCH_ARGS))
        except Exception as exc:    # noqa: BLE001  (no Google Chrome installed)
            self.skipTest(f"no Google Chrome for Playwright channel {CHANNEL!r}: {str(exc).splitlines()[0]}")
        self.addCleanup(browser.close)
        return browser

    def ledger(self) -> str:
        path = self.tmp / "ledger.jsonl"
        return path.read_text() if path.exists() else ""


class PlayTest(ChromeCase):
    def test_both_clips_play_in_chrome_at_both_widths_with_byte_ranges(self):
        browser, srv = self.chrome(), self.start()
        for width, height in ((1440, 900), (390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height})
            statuses = []
            page.on("response", lambda r: statuses.append(r.status) if "/clip/" in r.url else None)
            page.goto(srv.url + "d/1", wait_until="load")
            for k in (0, 1):
                with self.subTest(width=width, clip=k):
                    sel = f'#sl-1 video[data-clip-video="D1|{k}"]'
                    tab = page.locator(f'#sl-1 [data-clip="D1|{k}"]')
                    if tab.is_visible():                    # the desktop: one player, its tab shows the clip
                        tab.click()
                    else:
                        page.locator(sel).scroll_into_view_if_needed()
                    self.assertTrue(page.locator(sel).is_visible())
                    r = page.evaluate(PLAY, sel)
                    self.assertEqual((r["refused"], r["error"], r["muted"]), (None, None, False))
                    self.assertGreaterEqual(r["readyState"], 3)
                    self.assertGreater(r["currentTime"], max(0, r["start"]) + ADVANCE * 0.99)
            self.assertIn(206, statuses)                    # Chrome asked for byte ranges and got them
            page.close()
        self.assertEqual(self.ledger(), "")                 # playing and switching clips never answers

    def test_tabs_switch_pause_and_never_answer_and_leaving_pauses(self):
        browser, srv = self.chrome(), self.start()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(srv.url + "d/1", wait_until="load")
        calm, today = '#sl-1 video[data-clip-video="D1|1"]', '#sl-1 video[data-clip-video="D1|0"]'
        self.assertTrue(page.locator(calm).is_visible())                    # the recommended clip first
        self.assertFalse(page.locator(today).is_visible())
        self.assertTrue(page.locator('#sl-1 [data-clip-cap="D1|1"]').is_visible())
        self.assertTrue(page.evaluate(f"document.querySelector('{calm}').paused"))     # nothing plays by itself
        page.evaluate(f"document.querySelector('{calm}').play()")
        page.wait_for_function(f"document.querySelector('{calm}').currentTime > 0.2")
        page.click('#sl-1 [data-clip="D1|0"]')
        self.assertTrue(page.evaluate(f"document.querySelector('{calm}').paused"))     # hidden: paused
        self.assertTrue(page.locator(today).is_visible())
        self.assertEqual(page.locator('#sl-1 [data-clip="D1|0"]').get_attribute("aria-pressed"), "true")
        self.assertTrue(page.locator('#sl-1 [data-clip-cap="D1|0"]').is_visible())
        page.locator("#sl-1 .title").focus()
        page.keyboard.press("v")                                            # V: the next clip
        self.assertTrue(page.locator(calm).is_visible())
        page.evaluate(f"document.querySelector('{calm}').play()")
        page.wait_for_function(f"document.querySelector('{calm}').currentTime > 0.2")
        page.keyboard.press("ArrowRight")                                   # leaving the slide
        page.wait_for_function("location.pathname === '/d/2'")
        self.assertTrue(page.evaluate(f"document.querySelector('{calm}').paused"))
        page.goto(srv.url + "d/1", wait_until="load")                       # the answer row whole on screen
        for k in range(2):
            b = page.locator("#sl-1 .choices .choice").nth(k).bounding_box()
            self.assertTrue(b and b["y"] >= 0 and b["y"] + b["height"] <= 900 and b["x"] + b["width"] <= 1440, b)
        vb = page.locator("#sl-1 .vclip[data-on] .vbox").bounding_box()    # the player's fixed 16:9 box
        self.assertLess(abs(vb["height"] - vb["width"] * 9 / 16), 1.5)
        self.assertGreater(vb["width"], 600)
        self.assertEqual(self.ledger(), "")

    def test_the_phone_shows_every_clip_one_per_row_at_full_width(self):
        browser, srv = self.chrome(), self.start()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(srv.url + "d/1", wait_until="load")
        boxes = [page.locator(f'#sl-1 .vclip[data-clip-k="{k}"] .vbox').bounding_box() for k in range(2)]
        width = page.locator("#sl-1 .vframe").bounding_box()["width"]
        self.assertTrue(all(b and abs(b["width"] - width) < 1 and b["width"] > 330 for b in boxes), boxes)
        self.assertEqual(boxes[0]["x"], boxes[1]["x"])
        self.assertGreaterEqual(boxes[1]["y"], boxes[0]["y"] + boxes[0]["height"])
        self.assertFalse(page.locator('#sl-1 [data-clip="D1|0"]').is_visible())       # no tabs on a phone
        self.assertEqual(page.locator('#sl-1 .vclip[data-clip-k="0"] .vlab').inner_text(), "Keep today's colours")
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)


class CheckTest(ChromeCase):
    def test_the_checker_is_clean_on_the_round_and_names_a_clip_chrome_cannot_play(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:                # skip here, not inside the check, without Chrome
            try:
                p.chromium.launch(channel=CHANNEL).close()
            except Exception as exc:    # noqa: BLE001  (no Google Chrome installed)
                self.skipTest(f"no Google Chrome for Playwright channel {CHANNEL!r}: {str(exc).splitlines()[0]}")
        import decision_deck_check as check
        self.assertEqual(check.check(self.load(), out=self.tmp / "shots", source="From the test"), [])
        self.assertGreater((self.tmp / "shots" / "desktop-slide1.png").stat().st_size, 10_000)
        (self.root / "broken.mp4").write_bytes((self.root / "today.mp4").read_bytes()[:32] + os.urandom(20_000))
        data = json.loads(self.spec_path.read_text())
        data["decisions"][1]["evidence"]["clips"][0]["file"] = "broken.mp4"
        self.spec_path.write_text(json.dumps(data))
        problems = check.check(self.load(), source="From the test")
        self.assertTrue(problems and all(line.startswith("VIDEO /d/2 ") for line in problems), problems)
        self.assertEqual({line.split()[2] for line in problems}, {"1440", "390"})
        self.assertIn('D2 clip 1 "The animation with its tone" (broken.mp4): the browser could not load it', problems[0])


class WebKitTest(ChromeCase):
    def test_webkit_plays_both_clips_and_gets_its_byte_range_probe_answered(self):
        """Playwright's WebKit stands in for Safari: Safari opens a clip with a `Range: bytes=0-1` probe and plays
        nothing from a server that answers it without a 206."""
        try:
            browser = self.playwright().webkit.launch()
        except Exception as exc:    # noqa: BLE001  (no WebKit installed for Playwright)
            self.skipTest(f"no Playwright WebKit: {str(exc).splitlines()[0]}")
        self.addCleanup(browser.close)
        srv = self.start()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        seen = []
        page.on("response", lambda r: seen.append((r.request.headers.get("range"), r.status)) if "/clip/" in r.url
                else None)
        page.goto(srv.url + "d/1", wait_until="load")
        for k in (0, 1):
            with self.subTest(clip=k):
                r = page.evaluate(PLAY, f'#sl-1 video[data-clip-video="D1|{k}"]')
                self.assertIsNone(r["error"])
                self.assertGreaterEqual(r["readyState"], 3)
                self.assertGreater(r["currentTime"], r["start"] + ADVANCE * 0.99)
        self.assertIn(("bytes=0-1", 206), seen)


if __name__ == "__main__":
    unittest.main()
