"""Tests for the decision deck's "video" evidence: clips the owner plays on the slide, with their sound.

Without a browser: the spec keys and every file rule (each refused as a spec error naming the decision and the
clip), the slide's markup (one <video> per clip, controls and playsinline, never autoplay, loop or muted; tabs that
never answer; the recommended clip first), a deck without a video decision left as it was, the text and asks
exports and the help. The clip route, the stamp and serve are in test_decision_deck_video_serve.py and the browser
cases in test_decision_deck_video_live.py. The helpers here (video_spec, make_video_dir) build the two-decision video
round both use; its clips are synthetic files whose first bytes are an MP4's or a WebM's, written to a temp folder.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck as dd  # noqa: E402
import decision_deck_check_help as check_help  # noqa: E402
import decision_deck_css as css  # noqa: E402
import decision_deck_render as render  # noqa: E402
import decision_deck_script as script  # noqa: E402
import decision_deck_spec as ps  # noqa: E402
import decision_deck_video as video  # noqa: E402
import decision_deck_video_slide as slide_mod  # noqa: E402
from decision_deck_reply import asks_text  # noqa: E402
from decision_deck_text import deck_text  # noqa: E402
from test_decision_deck_render import slide  # noqa: E402
from test_decision_deck_spec import SVG, TempDirCase  # noqa: E402

MP4 = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom" + bytes(range(256)) * 8
WEBM = video.EBML + b"\x9f\x42\x86\x81\x01" + bytes(range(255, -1, -1)) * 8


def video_spec() -> dict:
    """Two video decisions: two clips tied to options (the recommended one second in spec order), and one clip with a
    label of its own."""
    return {
        "title": "Which opening animation should the app use?",
        "decisions": [
            {"id": "D1", "title": "Opening animation", "question": "Which opening animation should the app use?",
             "context": "Both clips run for two seconds with the same tone; only the colours change.",
             "recommendation": {"option": "calm", "why": "The calm colours match the rest of the app."},
             "evidence": {"kind": "video", "clips": [{"option": "today", "file": "today.mp4"},
                                                     {"option": "calm", "file": "calm.webm"}]},
             "options": [{"id": "calm", "label": "Use the calm colours",
                          "caption": "The new animation in the calm colours, with a higher tone."},
                         {"id": "today", "label": "Keep today's colours",
                          "caption": "The animation the app shows today."}]},
            {"id": "D2", "title": "Opening sound", "question": "Should the opening animation play its tone?",
             "context": "The tone is two seconds long and plays only when the animation does.",
             "recommendation": {"option": "keep", "why": "The tone says the app is ready without looking."},
             "evidence": {"kind": "video", "clips": [{"label": "The animation with its tone", "file": "today.mp4",
                                                      "caption": "Press play to hear the tone."}]},
             "options": [{"id": "keep", "label": "Keep the tone"}, {"id": "drop", "label": "Play it without sound"}]},
        ],
    }


def make_video_dir(base: Path, data: dict | None = None, clips: dict | None = None) -> Path:
    """A spec folder under `base` with its clips (default: the synthetic today.mp4 and calm.webm); the spec path."""
    root = Path(base) / "round"
    root.mkdir(parents=True, exist_ok=True)
    for name, body in (clips or {"today.mp4": MP4, "calm.webm": WEBM}).items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(body)
    path = root / "spec.json"
    path.write_text(json.dumps(video_spec() if data is None else data), encoding="utf-8")
    return path


class VideoCase(TempDirCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)
        self.spec_path = make_video_dir(self.tmp)
        self.root = self.spec_path.parent

    def errors_for(self, mutate) -> list[str]:
        data = video_spec()
        mutate(data)
        return ps.validate_spec(data, self.root)

    def refused(self, mutate, needle: str, where: str = "decision D1 evidence") -> None:
        errors = self.errors_for(mutate)
        self.assertTrue(any(e.startswith(where) and needle in e for e in errors), errors)


def clips(data, k=0):
    return data["decisions"][k]["evidence"]["clips"]


def file_is(name):
    def mutate(data):
        clips(data)[0]["file"] = name
    return mutate


class SpecTest(VideoCase):
    def test_the_round_validates_and_the_recommended_clip_shows_first(self):
        spec = self.load()
        ev = ps.evidence_of(spec["decisions"][0])
        self.assertEqual((ev["kind"], ev["start"]), ("video", 1))
        self.assertEqual([c["label"] for c in ev["clips"]], ["Keep today's colours", "Use the calm colours"])
        self.assertEqual(ev["clips"][0]["caption"], "The animation the app shows today.")    # the option's caption
        one = ps.evidence_of(spec["decisions"][1])
        self.assertEqual((one["clips"][0]["label"], one["start"]), ("The animation with its tone", 0))

    def test_bad_clips_are_spec_errors_naming_the_decision_and_the_clip(self):
        cases = [
            (lambda d: d["decisions"][0]["evidence"].pop("clips"), "'clips' must be a list of 1 to 4"),
            (lambda d: d["decisions"][0]["evidence"].update(clips=[]), "'clips' must be a list of 1 to 4"),
            (lambda d: d["decisions"][0]["evidence"].update(
                clips=[{"label": f"C{k}", "file": "today.mp4"} for k in range(5)]), "'clips' must be a list of 1 to 4"),
            (lambda d: clips(d)[0].update(label="Both"), "clip 1: give 'option' or 'label', not both"),
            (lambda d: clips(d)[0].pop("option"), "clip 1: needs 'option'"),
            (lambda d: clips(d)[0].update(option="nope"), "clip 1: names option 'nope', which is not an option here"),
            (lambda d: clips(d)[1].update(option="today"), "clip 2: option 'today' has two clips"),
            (lambda d: clips(d)[0].update(caption=""), "clip 1: 'caption' must be a non-empty string"),
            (file_is("missing.mp4"), "clip 1: clip 'missing.mp4' not found"),
            (file_is("../today.mp4"), "clip 1: clip '../today.mp4' is outside the spec's folder"),
            (file_is("/tmp/today.mp4"), "clip 1: clip '/tmp/today.mp4' must be a path relative to the spec's folder"),
            (file_is("today.mov"), "clip 1: clip 'today.mov' must end in .mp4 or .webm"),
            (file_is(".hidden.mp4"), "clip 1: clip '.hidden.mp4' has a hidden name"),
            (file_is(".cache/today.mp4"), "clip 1: clip '.cache/today.mp4' has a hidden name"),
        ]
        for mutate, needle in cases:
            with self.subTest(needle):
                self.refused(mutate, needle)

    def test_option_and_label_are_held_by_key_presence_and_type(self):
        cases = [
            (0, {"option": "today", "label": None, "file": "today.mp4"}, "clip 1: give 'option' or 'label', not both"),
            (0, {"option": None, "label": "Preview", "file": "today.mp4"}, "clip 1: give 'option' or 'label', not both"),
            (0, {"file": "today.mp4", "caption": "No key"}, "clip 1: needs 'option' (an option id) or 'label'"),
            (0, {"option": [], "file": "today.mp4"}, "clip 1: 'option' must be an option id (a string), not []"),
            (0, {"option": {}, "file": "today.mp4"}, "clip 1: 'option' must be an option id (a string), not {}"),
            (0, {"option": None, "file": "today.mp4"}, "clip 1: 'option' must be an option id (a string), not None"),
            (0, {"option": True, "file": "today.mp4"}, "clip 1: 'option' must be an option id (a string), not True"),
            (1, {"label": None, "file": "today.mp4"}, "clip 1: 'label' must be a non-empty string"),
            (1, {"label": "  ", "file": "today.mp4"}, "clip 1: 'label' must be a non-empty string"),
            (1, {"label": "Nul", "file": "to\u0000day.mp4"}, "clip 1: 'file' must be a non-empty string"),
        ]
        for k, clip, needle in cases:
            with self.subTest(clip=clip):
                self.refused(lambda d, k=k, clip=clip: clips(d, k).__setitem__(0, copy.deepcopy(clip)), needle,
                             f"decision D{k + 1} evidence ")

    def test_any_json_value_in_any_clip_field_is_a_spec_error_never_a_crash(self):
        odd = [None, 0, 1.5, True, "", [], {}, [[1, [2, {"x": None}]]]]
        for field in ("option", "label", "file", "caption", "clip", "clips"):
            for value in odd:
                with self.subTest(field=field, value=value):
                    data = video_spec()
                    k = 1 if field == "label" else 0       # D2's clip carries a label; D1's carry options
                    ev = data["decisions"][k]["evidence"]
                    if field == "clips":
                        ev["clips"] = copy.deepcopy(value)
                    elif field == "clip":
                        ev["clips"][0] = copy.deepcopy(value)
                    else:
                        ev["clips"][0][field] = copy.deepcopy(value)
                    errors = ps.validate_spec(data, self.root)      # must not raise
                    where = f"decision D{k + 1} evidence" + ("" if field == "clips" else " clip 1")
                    self.assertTrue(errors and all(e.startswith(where) for e in errors), errors)

    def test_a_file_name_no_file_can_have_is_a_spec_error_not_a_crash(self):
        self.refused(file_is("\ud800.mp4"), "clip 1: 'file' '\\ud800.mp4' is not a valid file name")
        data = video_spec()
        file_is("\ud800.mp4")(data)
        self.spec_path.write_text(json.dumps(data))         # JSON escapes the lone surrogate as \ud800
        with self.assertRaises(ps.SpecError):
            self.load()

    def test_a_clip_whose_bytes_are_not_its_kind_is_refused(self):
        for name, body, needle in [("empty.mp4", b"", "is empty"),
                                   ("text.mp4", b"<html>not a clip</html>",
                                    "is not an MP4 (no ftyp box) or WebM (no EBML header) file"),
                                   ("swapped.mp4", WEBM, "holds a WebM file under a .mp4 name; name it .webm"),
                                   ("swapped.webm", MP4, "holds an MP4 file under a .webm name; name it .mp4")]:
            with self.subTest(name):
                (self.root / name).write_bytes(body)
                self.refused(file_is(name), f"clip 1: clip '{name}' {needle}")

    def test_a_clip_reached_through_a_symlink_is_refused(self):
        (self.root / "link.mp4").symlink_to(self.root / "today.mp4")
        (self.root / "sub").symlink_to(self.root)
        for name in ("link.mp4", "sub/today.mp4"):
            with self.subTest(name):
                self.refused(file_is(name), f"clip 1: clip '{name}' is reached through a symlink")

    def test_the_per_clip_and_per_deck_limits(self):
        with mock.patch.object(video, "MAX_CLIP_BYTES", len(MP4) - 1):
            self.refused(lambda d: None, "clip 1: clip 'today.mp4' is ")
            self.refused(lambda d: None, "MB a clip may hold")
        total = len(MP4) + len(WEBM)
        with mock.patch.object(video, "MAX_DECK_BYTES", total - 1):     # both together cross it at the second clip
            self.refused(lambda d: None, "clip 2: clip 'calm.webm' takes the deck's clips over")
        with mock.patch.object(video, "MAX_DECK_BYTES", total):         # D2 reuses today.mp4: counted once
            self.assertEqual(self.errors_for(lambda d: None), [])

    def test_a_video_decision_whose_options_carry_images_is_refused(self):
        (self.root / "shot.svg").write_bytes(SVG)
        self.refused(lambda d: d["decisions"][0]["options"][0].update(images=["shot.svg"]),
                     "only a picture decision (evidence kind images) carries images", "decision D1: ")

    def test_the_limits(self):
        self.assertEqual((video.CLIPS_MAX, video.MAX_CLIP_BYTES, video.MAX_DECK_BYTES), (4, 50 * 2 ** 20, 200 * 2 ** 20))


class SlideTest(VideoCase):
    def setUp(self):
        super().setUp()
        self.spec = self.load()
        self.html = render.deck_page(self.spec, [], source="From the test")

    def test_each_clip_is_one_player_that_plays_only_when_pressed_with_its_sound(self):
        tags = [t.split(">", 1)[0] for t in self.html.split("<video ")[1:]]
        self.assertEqual(len(tags), 3)                      # two clips on D1, one on D2
        for tag in tags:
            for needed in ("controls", "playsinline", 'preload="metadata"', '#t=0.001"'):
                self.assertIn(needed, tag)
            for banned in ("autoplay", "loop", "muted"):
                self.assertNotIn(banned, tag)
        self.assertIn('src="/clip/', tags[0])
        self.assertIn(".mp4#t=0.001", tags[0])
        self.assertIn(".webm#t=0.001", tags[1])

    def test_two_clips_get_a_tab_each_on_the_recommended_clip_and_one_clip_none(self):
        d1, d2 = slide(self.html, 1), slide(self.html, 2)
        self.assertIn('<button type="button" data-clip="D1|0" aria-pressed="false" title="Keep today&#x27;s colours">', d1)
        self.assertIn('<button type="button" data-clip="D1|1" aria-pressed="true" title="Use the calm colours">', d1)
        self.assertIn('<figure class="vclip" data-clip-k="1" data-on>', d1)
        self.assertNotIn('data-clip-k="0" data-on', d1)
        self.assertNotIn("data-choose", d1.split('class="dock')[0])     # the tabs never answer
        self.assertNotIn("data-clip=", d2)
        self.assertIn('<figure class="vclip" data-clip-k="0" data-on>', d2)
        self.assertIn('<span data-clip-cap="D2|0">Press play to hear the tone.</span>', d2)
        # an option's caption sits with its clip, so the context line leaves it out
        self.assertNotIn("The animation the app shows today", d1.split('class="ctxrow"', 1)[1])
        for needle in ("function clipTab", "clipsQuiet(i);", ".vbox", "Video clips: the next clip"):
            self.assertIn(needle, self.html)

    def test_a_deck_without_a_video_decision_keeps_its_page_script_and_look(self):
        with tempfile.TemporaryDirectory() as tmp:
            from test_decision_deck_spec import make_spec_dir
            html = render.deck_page(ps.load_spec(make_spec_dir(Path(tmp))), [])
        self.assertIn(f"<script>{script.SCRIPT}</script>", html)
        self.assertIn(f"<style>{css.page_css()}</style>", html)
        for needle in ("clipTab", ".vbox", "<video", "Video clips", "clipsQuiet"):
            self.assertNotIn(needle, html)

    def test_the_video_script_joins_each_anchor_once_and_fails_loudly_on_a_moved_one(self):
        joined = slide_mod.with_video(script.SCRIPT)
        for needle in ("function clipTab", "if (d.clip) { clipTab(d.clip)", "clipNext(it.id)", "clipsQuiet(i);",
                       "if (tg.tagName === 'VIDEO') return;"):
            self.assertEqual(joined.count(needle), 1, needle)
        with self.assertRaises(RuntimeError):
            slide_mod.with_video(script.SCRIPT.replace("    route(i);\n", "    route(i); \n"))

    def test_text_and_asks_name_each_clip_by_its_tab_and_caption_never_its_file(self):
        for out in (deck_text(self.spec), asks_text(self.spec)):
            self.assertIn("[Evidence: video clips in one player, a tab per clip; each plays on the slide when "
                          "pressed, with its sound]", out)
            self.assertIn('Clip "Use the calm colours" (shown first): The new animation in the calm colours', out)
            self.assertIn('Clip "The animation with its tone": Press play to hear the tone.', out)
            self.assertNotIn("today.mp4", out)
            self.assertNotIn("calm.webm", out)

    def test_help_gives_the_keys_limits_and_the_clip_route(self):
        text = " ".join(dd.build_parser().format_help().split())
        for needle in ('{"kind": "video", "clips": [1 to 4 of {exactly one of "option"', '"caption"?',
                       "at most 50 MB a clip and 200 MB for all of a deck's clips together",
                       "MP4 with H.264 video (yuv420p) and AAC sound",
                       "ffmpeg -i in.mov -c:v libx264 -pix_fmt yuv420p", "GET /clip/<sha16>.<ext>"):
            self.assertIn(needle, text)
        self.assertIn("VIDEO", check_help.HELP)


if __name__ == "__main__":
    unittest.main()
