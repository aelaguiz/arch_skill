import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

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
            file=files,
            title=title,
            description=description,
            image=image,
            url=url,
            card_url=f"{self.base}/{self.slug}/__cf_share/card.png",
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
        args = self.args(entry, "index.html", "html", ["index.html", "style.css"])
        preview.prepare(args)
        result = (self.output / "entry.html").read_text()
        parsed = preview.parse_page(result)
        self.assertEqual(parsed.meta["og:title"], "Research & findings")
        self.assertEqual(parsed.meta["og:url"], args.url)
        self.assertEqual(parsed.meta["og:image"], args.card_url)
        self.assertEqual(parsed.meta["twitter:card"], "summary_large_image")
        self.assertEqual(result.count('property="og:title"'), 1)
        self.assertNotIn("old.png", result)
        self.assertIn('href="style.css"', result)
        self.assertIn('src="img/chart.png"', result)
        self.assertEqual(entry.read_text(), source)
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


if __name__ == "__main__":
    unittest.main()
