import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/youtube-channel/scripts/yt.py"
SPEC = importlib.util.spec_from_file_location("yt", SCRIPT)
yt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(yt)


def update_args(**kw):
    base = dict(id="vid1", title=None, description=None, description_file=None, tags=None, add_tags=None,
                category=None, language=None, audio_language=None, privacy=None, publish_at=None,
                clear_publish_at=False, made_for_kids=None, synthetic=None, embeddable=None, public_stats=None,
                license=None, localize=None, remove_localization=None, recording_date=None, dry_run=False,
                json_out=None)
    base.update(kw)
    return SimpleNamespace(**base)


CURRENT = {
    "id": "vid1",
    "snippet": {"title": "Old", "description": "Desc", "tags": ["a", "b"], "categoryId": "27",
                "defaultLanguage": "en", "channelTitle": "Poker Skill", "publishedAt": "2026-10-26T00:00:00Z"},
    "status": {"uploadStatus": "processed", "privacyStatus": "unlisted", "license": "youtube",
               "embeddable": True, "publicStatsViewable": True, "madeForKids": False,
               "selfDeclaredMadeForKids": False},
    "localizations": {"en": {"title": "Old", "description": "Desc"}},
}


class UpdateMergeTests(unittest.TestCase):
    def run_update(self, **kw):
        sent = []

        def fake_api(method, path, params=None, body=None, base=None):
            sent.append((method, path, params, body))
            return {"id": "vid1", "status": body.get("status", CURRENT["status"])}

        with patch.object(yt, "get_videos", return_value=[json.loads(json.dumps(CURRENT))]), \
                patch.object(yt, "api", side_effect=fake_api), redirect_stdout(io.StringIO()) as out:
            yt.cmd_update(update_args(**kw))
        return sent, out.getvalue()

    def test_title_change_keeps_tags_and_sends_only_snippet(self):
        sent, _ = self.run_update(title="New")
        (method, path, params, body), = sent
        self.assertEqual((method, path, params["part"]), ("PUT", "/videos", "snippet"))
        self.assertEqual(body["snippet"]["title"], "New")
        self.assertEqual(body["snippet"]["tags"], ["a", "b"])
        self.assertEqual(body["snippet"]["categoryId"], "27")
        self.assertNotIn("channelTitle", body["snippet"])

    def test_add_tags_appends_without_duplicates(self):
        sent, _ = self.run_update(add_tags="b,c")
        self.assertEqual(sent[0][3]["snippet"]["tags"], ["a", "b", "c"])

    def test_publish_at_forces_private_and_drops_read_only_status(self):
        sent, out = self.run_update(publish_at="2027-01-01T15:00:00Z")
        status = sent[0][3]["status"]
        self.assertEqual(status["privacyStatus"], "private")
        self.assertEqual(status["publishAt"], "2027-01-01T15:00:00Z")
        self.assertNotIn("uploadStatus", status)
        self.assertNotIn("madeForKids", status)
        self.assertIn("privacy set to private", out)

    def test_going_unlisted_cancels_a_schedule(self):
        scheduled = json.loads(json.dumps(CURRENT))
        scheduled["status"].update(privacyStatus="private", publishAt="2027-01-01T15:00:00Z")
        with patch.dict(CURRENT, scheduled):
            sent, _ = self.run_update(privacy="unlisted")
        self.assertEqual(sent[0][3]["status"]["privacyStatus"], "unlisted")
        self.assertNotIn("publishAt", sent[0][3]["status"])

    def test_localization_sends_snippet_with_default_language(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("Descripción\n")
        sent, _ = self.run_update(localize=[f"es:Título:{f.name}"])
        parts = sent[0][2]["part"].split(",")
        self.assertIn("localizations", parts)
        self.assertIn("snippet", parts)
        self.assertEqual(sent[0][3]["localizations"]["es"], {"title": "Título", "description": "Descripción"})
        self.assertEqual(sent[0][3]["snippet"]["defaultLanguage"], "en")

    def test_dry_run_and_no_change_send_nothing(self):
        sent, out = self.run_update(title="New", dry_run=True)
        self.assertEqual(sent, [])
        self.assertIn('"Old" -> "New"', out)
        sent, out = self.run_update(title="Old")
        self.assertEqual(sent, [])
        self.assertIn("nothing to change", out)


class ResumableUploadTests(unittest.TestCase):
    def test_chunks_follow_the_range_youtube_reports(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"x" * (600 * 1024))
        calls = []

        def fake_http(method, url, params=None, body=None, data=None, headers=None, token=None, raw=False,
                      ok=(200, 201, 204)):
            calls.append((method, url, headers or {}, len(data or b"")))
            if method == "POST":
                return 200, {"Location": "https://upload.example/session"}, {}
            rng = headers["Content-Range"]
            end = int(rng.split("-")[1].split("/")[0])
            if end + 1 < 600 * 1024:
                return 308, {"Range": f"bytes=0-{end}"}, b""
            video = {"id": "new1", "status": {"privacyStatus": "unlisted"}}
            return 200, {}, json.dumps(video).encode()

        args = SimpleNamespace(file=f.name, title="T", description=None, description_file=None, tags=None,
                               category=None, language=None, audio_language=None, privacy="unlisted",
                               publish_at=None, made_for_kids=None, synthetic=None, embeddable=None,
                               public_stats=None, license=None, notify=False, thumbnail=None, captions=None,
                               playlist=None, wait=False, wait_timeout=1, dry_run=False, json_out=None)
        with patch.object(yt, "http", side_effect=fake_http), patch.object(yt, "token", return_value="t"), \
                patch.object(yt, "CHUNK", 256 * 1024), redirect_stdout(io.StringIO()) as out:
            yt.cmd_upload(args)
        puts = [c for c in calls if c[0] == "PUT"]
        self.assertEqual([c[2]["Content-Range"] for c in puts],
                         ["bytes 0-262143/614400", "bytes 262144-524287/614400", "bytes 524288-614399/614400"])
        init = calls[0]
        self.assertEqual(init[2]["X-Upload-Content-Length"], str(600 * 1024))
        self.assertIn("uploaded: new1", out.getvalue())


class SmallHelperTests(unittest.TestCase):
    def test_iso_duration(self):
        self.assertEqual(yt.iso_duration("PT14M25S"), "14:25")
        self.assertEqual(yt.iso_duration("PT1H2M3S"), "1:02:03")
        self.assertEqual(yt.iso_duration("PT7S"), "0:07")
        self.assertEqual(yt.iso_duration(None), "")

    def test_google_error_shapes_and_hints(self):
        api_err = json.dumps({"error": {"code": 403, "message": "Quota", "errors": [{"reason": "quotaExceeded"}]}})
        self.assertIn("quotaExceeded", yt.google_error(403, api_err.encode()))
        self.assertIn("midnight Pacific", yt.google_error(403, api_err.encode()))
        oauth_err = json.dumps({"error": "invalid_grant", "error_description": "Token has been expired or revoked."})
        self.assertIn("redo `yt.py login`", yt.google_error(400, oauth_err.encode()))


if __name__ == "__main__":
    unittest.main()
