import importlib.util
import json
import hashlib
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "skills/cf-share/scripts/share_preview.py"
SPEC = importlib.util.spec_from_file_location("share_preview", SCRIPT)
preview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preview)


class SharePreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "generated"
        self.base = "https://share.fun.country"
        self.slug = "test-slug"

    def args(self, entry, relative, mode, files, title="", description="", image=""):
        direct = preview.object_url(self.base, self.slug, relative)
        url = direct if mode == "html" else f"{self.base}/{self.slug}/__cf_share/index.html"
        return SimpleNamespace(
            entry=str(entry),
            relative=relative,
            mode=mode,
            file=[(str(self.root / name), name) for name in files],
            title=title,
            description=description,
            image=image,
            url=url,
            direct_url=direct,
            base_url=self.base,
            slug=self.slug,
            output_dir=str(self.output),
        )

    def test_html_report_keeps_assets_and_replaces_stale_metadata(self):
        entry = self.root / "index.html"
        source = '''<!doctype html><html><head><meta charset="utf-8">
<title>Research &amp; findings</title>
<meta property="og:title" content="Old title"><meta name="twitter:image" content="old.png">
<link rel="canonical" href="https://old.example.com/"><link rel="stylesheet" href="style.css">
</head><body><h1>Research &amp; findings</h1><p>Results from a representative artifact with concrete findings and linked images.</p><img src="img/chart.png"></body></html>'''
        entry.write_text(source)
        (self.root / "style.css").write_text("body {color: red}")
        args = self.args(entry, "index.html", "html", ["index.html", "style.css"])
        preview.prepare(args)
        result = (self.output / "entry.html").read_text()
        parsed = preview.parse_page(result)
        self.assertEqual(parsed.meta["og:title"], "Research & findings")
        self.assertEqual(parsed.meta["og:url"], args.url)
        info = json.loads((self.output / "info.json").read_text())
        self.assertEqual(parsed.meta["og:image"], info["card_url"])
        self.assertEqual(parsed.meta["twitter:card"], "summary_large_image")
        self.assertEqual(result.count('property="og:title"'), 1)
        self.assertNotIn("old.png", result)
        self.assertIn('href="style.css"', result)
        self.assertIn('src="img/chart.png"', result)
        self.assertEqual(entry.read_text(), source)
        self.assertEqual(len(info["objects"]), 3)
        self.assertEqual(info["objects"][0]["sha256"], preview.file_digest(self.output / "entry.html"))
        with Image.open(self.output / "card.png") as card:
            self.assertEqual(card.size, (1200, 630))

    def test_image_share_page_embeds_file_and_escapes_editorial_text(self):
        entry = self.root / "capture & proof.png"
        Image.new("RGB", (800, 500), "#d1573d").save(entry)
        args = self.args(
            entry,
            entry.name,
            "page",
            [entry.name],
            title='R&D "proof"',
            description="A screenshot of the R&D flow's completed state.",
        )
        preview.prepare(args)
        result = (self.output / "share.html").read_text()
        parsed = preview.parse_page(result)
        self.assertEqual(parsed.meta["og:title"], 'R&D "proof"')
        self.assertEqual(parsed.meta["og:description"], args.description)
        self.assertIn('src="https://share.fun.country/test-slug/capture%20%26%20proof.png"', result)
        self.assertIn('href="https://share.fun.country/test-slug/capture%20%26%20proof.png"', result)
        self.assertNotIn('content="R&D "proof""', result)
        info = json.loads((self.output / "info.json").read_text())
        self.assertEqual(info["url"], args.url)

    def test_pdf_share_page_has_inline_view_and_direct_link(self):
        entry = self.root / "board-review.pdf"
        entry.write_bytes(b"%PDF-1.4\n%%EOF\n")
        args = self.args(entry, entry.name, "page", [entry.name], description="A review of the board decisions.")
        preview.prepare(args)
        result = (self.output / "share.html").read_text()
        self.assertIn('<iframe class="media pdf"', result)
        self.assertIn(f'href="{args.direct_url}"', result)
        self.assertIn("Board Review", result)

    def test_non_html_without_description_fails_before_upload(self):
        entry = self.root / "screenshot.png"
        Image.new("RGB", (500, 300), "#386784").save(entry)
        args = self.args(entry, entry.name, "page", [entry.name])
        with self.assertRaisesRegex(ValueError, "provide --description"):
            preview.prepare(args)

    def test_changed_card_gets_new_path_while_headline_stays_stable(self):
        entry = self.root / "index.html"
        entry.write_text("<h1>Report</h1><p>Concrete findings from the current report revision.</p>")
        args = self.args(entry, entry.name, "html", [entry.name], title="First revision")
        preview.prepare(args)
        first = json.loads((self.output / "info.json").read_text())
        args.title = "Second revision"
        preview.prepare(args)
        second = json.loads((self.output / "info.json").read_text())
        self.assertEqual(first["url"], second["url"])
        self.assertNotEqual(first["card_url"], second["card_url"])
        preview.prepare(args)
        third = json.loads((self.output / "info.json").read_text())
        self.assertEqual(second["card_url"], third["card_url"])

    def test_media_versions_follow_uploaded_bytes_and_preserve_other_urls(self):
        page = "https://share.fun.country/test-slug/reports/index.html"
        url = "https://share.fun.country/test-slug/assets/clip.mp4"
        source = '''<html><head><link rel="canonical" href="reports/index.html"></head><body>
<video src="../assets/clip.mp4?mode=inline#t=1"></video>
<audio><source src='../assets/clip.mp4'></audio>
<video src="https://external.example/clip.mp4"></video>
<a href="../assets/clip.mp4">Download</a>
<script>const text = '<video src="../assets/clip.mp4">';</script>
</body></html>'''
        first = preview.version_media(source, page, {url: "a" * 64})
        self.assertIn('src="../assets/clip.mp4?mode=inline&amp;cf_share_v=' + "a" * 20 + '#t=1"', first)
        self.assertIn('src="https://external.example/clip.mp4"', first)
        self.assertIn('<a href="../assets/clip.mp4">', first)
        self.assertIn("const text = '<video src=\"../assets/clip.mp4\">'", first)
        self.assertEqual(preview.version_media(first, page, {url: "a" * 64}), first)
        second = preview.version_media(first, page, {url: "b" * 64})
        self.assertNotIn("cf_share_v=" + "a" * 20, second)
        self.assertIn("cf_share_v=" + "b" * 20, second)

    def test_pdf_embed_versions_change_without_changing_download_or_headline(self):
        entry = self.root / "review.pdf"
        entry.write_bytes(b"%PDF first revision")
        args = self.args(entry, entry.name, "page", [entry.name], description="A review of the current board decisions.")
        preview.prepare(args)
        first = (self.output / "share.html").read_text()
        first_digest = preview.file_digest(entry)[:20]
        self.assertIn(args.direct_url + "?cf_share_v=" + first_digest, first)
        info = json.loads((self.output / "info.json").read_text())
        self.assertEqual(info["embeds"], [{"url": args.direct_url + "?cf_share_v=" + first_digest, "sha256": preview.file_digest(entry)}])
        self.assertIn('href="' + args.direct_url + '"', first)
        entry.write_bytes(b"%PDF second revision")
        preview.prepare(args)
        second = (self.output / "share.html").read_text()
        self.assertNotIn("cf_share_v=" + first_digest, second)
        self.assertIn(args.direct_url + "?cf_share_v=" + preview.file_digest(entry)[:20], second)
        self.assertEqual(preview.parse_page(first).meta["og:url"], preview.parse_page(second).meta["og:url"])

    def test_nested_document_version_tracks_dependencies_and_verifies_prepared_bytes(self):
        entry = self.root / "index.html"
        entry.write_text('<h1>Report</h1><p>Concrete findings from the report and its embedded document.</p><iframe src="child.html"></iframe>')
        child = self.root / "child.html"
        child.write_text('<video src="assets/movie clip.mp4"></video>')
        (self.root / "assets").mkdir()
        media = self.root / "assets/movie clip.mp4"
        media.write_bytes(b"first media revision")
        args = self.args(entry, entry.name, "html", ["index.html", "child.html", "assets/movie clip.mp4"])
        preview.prepare(args)
        first = json.loads((self.output / "info.json").read_text())
        child_embed = next(item for item in first["embeds"] if "/child.html?" in item["url"])
        self.assertEqual(child_embed["sha256"], preview.file_digest(self.output / "html/child.html"))
        media_embed = next(item for item in first["embeds"] if "movie%20clip.mp4?" in item["url"])
        self.assertEqual(media_embed["sha256"], preview.file_digest(media))
        media.write_bytes(b"second media revision")
        preview.prepare(args)
        second = json.loads((self.output / "info.json").read_text())
        changed_child = next(item for item in second["embeds"] if "/child.html?" in item["url"])
        self.assertNotEqual(child_embed["url"], changed_child["url"])
        self.assertEqual(child.read_text(), '<video src="assets/movie clip.mp4"></video>')


class ShareFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.responses = {}
        self.requests = []
        responses, requests = self.responses, self.requests

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append((self.path, dict(self.headers)))
                body, headers = responses[self.path]
                self.send_response(200)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def object(self, path, body=b"updated bytes", **headers):
        self.responses[path] = (body, {"Content-Type": "application/octet-stream", "Cache-Control": "no-store", **headers})
        return {"url": self.base + path, "sha256": hashlib.sha256(body).hexdigest()}

    def test_normal_gets_verify_binary_bytes_without_cache_bypass(self):
        expected = self.object("/asset.bin", b"\x00\xffcurrent\x00", **{"CF-Cache-Status": "BYPASS"})
        for _ in range(2):
            _, body = preview.fetch_object(expected, keep_body=True)
            self.assertEqual(body, b"\x00\xffcurrent\x00")
        self.assertEqual(len(self.requests), 2)
        for path, headers in self.requests:
            self.assertEqual(path, "/asset.bin")
            self.assertNotIn("Cache-Control", headers)
            self.assertNotIn("Pragma", headers)

    def test_cacheable_response_fails_even_when_bytes_match(self):
        expected = self.object("/style.css", **{"Cache-Control": "public, max-age=86400"})
        with self.assertRaisesRegex(ValueError, "caching still active"):
            preview.fetch_object(expected)

    def test_cached_response_fails_even_with_no_store_and_matching_bytes(self):
        for status in ("HIT", "STALE", "UPDATING", "REVALIDATED"):
            with self.subTest(status=status):
                expected = self.object("/image.png", **{"CF-Cache-Status": status})
                with self.assertRaisesRegex(ValueError, "caching still active"):
                    preview.fetch_object(expected)

    def test_stale_asset_fails_even_when_headers_are_correct(self):
        expected = self.object("/app.js")
        self.responses["/app.js"] = (b"previous bytes", {"Cache-Control": "no-store"})
        with self.assertRaisesRegex(ValueError, "served bytes differ"):
            preview.fetch_object(expected)

    def test_verify_detects_stale_sibling_after_valid_headline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entry = root / "index.html"
            entry.write_text("<h1>Report</h1><p>Concrete findings from a report with sibling assets.</p>")
            style = root / "style.css"
            style.write_text("body {color: blue}")
            args = SimpleNamespace(entry=str(entry), relative="index.html", mode="html",
                file=[(str(entry), "index.html"), (str(style), "style.css")], title="", description="", image="",
                url=self.base + "/report/index.html", direct_url=self.base + "/report/index.html",
                base_url=self.base, slug="report", output_dir=str(root / "generated"))
            preview.prepare(args)
            info = json.loads((root / "generated/info.json").read_text())
            for item, local, ct in zip(info["objects"], [root / "generated/entry.html", style, root / "generated/card.png"], ["text/html", "text/css", "image/png"]):
                path = item["url"].removeprefix(self.base)
                self.object(path, local.read_bytes(), **{"Content-Type": ct})
            preview.verify(SimpleNamespace(info=str(root / "generated/info.json")))
            path = "/report/style.css"
            self.responses[path] = (b"body {color: red}", self.responses[path][1])
            with self.assertRaisesRegex(ValueError, "served bytes differ"):
                preview.verify(SimpleNamespace(info=str(root / "generated/info.json")))

    def test_purge_batches_only_manifest_urls_and_discovers_zone(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "info.json"
            urls = [f"https://share.fun.country/report/file-{index}.css" for index in range(205)]
            path.write_text(json.dumps({"url": urls[0], "objects": [{"url": url} for url in urls]}))
            with patch.object(preview, "api_json", side_effect=[{"zoneId": "share-zone"}, {}, {}, {}]) as api, patch.dict(preview.os.environ, {"CF_SHARE_API_TOKEN": "upload-token", "CF_SHARE_PURGE_API_TOKEN": "purge-token"}):
                preview.purge(SimpleNamespace(info=str(path), account="account", bucket="bucket", zone=""))
            self.assertEqual(api.call_args_list[0].args[0], "accounts/account/r2/buckets/bucket/domains/custom/share.fun.country")
            calls = api.call_args_list[1:]
            self.assertEqual([len(call.args[2]["files"]) for call in calls], [100, 100, 5])
            self.assertEqual([url for call in calls for url in call.args[2]["files"]], urls)
            for call in calls:
                self.assertEqual(call.args[:2], ("zones/share-zone/purge_cache", "purge-token"))


if __name__ == "__main__":
    unittest.main()
