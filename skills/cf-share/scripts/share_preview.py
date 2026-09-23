#!/usr/bin/env python3
"""Build and verify crawler-readable previews for cf-share uploads."""

import argparse
import html
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


CARD_SIZE = (1200, 630)
RESERVED = "__cf_share"


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def shorten(value, limit):
    value = clean(value)
    if len(value) <= limit:
        return value
    return value[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"


class PageText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.title = ""
        self.heading = ""
        self.paragraphs = []
        self._capture = None
        self._pieces = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = (attrs.get("property") or attrs.get("name") or "").lower()
            if key and key not in self.meta:
                self.meta[key] = attrs.get("content") or ""
        if tag in ("title", "h1", "p") and self._capture is None:
            self._capture = tag
            self._pieces = []

    def handle_data(self, data):
        if self._capture:
            self._pieces.append(data)

    def handle_endtag(self, tag):
        if tag != self._capture:
            return
        value = clean(" ".join(self._pieces))
        if tag == "title" and not self.title:
            self.title = value
        elif tag == "h1" and not self.heading:
            self.heading = value
        elif tag == "p" and value:
            self.paragraphs.append(value)
        self._capture = None
        self._pieces = []


def parse_page(source):
    page = PageText()
    page.feed(source)
    return page


def tag_attr(raw, key):
    match = re.search(
        rf"\b{re.escape(key)}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
        raw,
        flags=re.I,
    )
    return html.unescape(next((value for value in match.groups() if value is not None), "")) if match else ""


def meta_tags(title, description, url, card_url):
    esc = lambda value: html.escape(value, quote=True)
    return "\n".join(
        [
            f'<meta name="description" content="{esc(description)}">',
            f'<link rel="canonical" href="{esc(url)}">',
            f'<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="Fun Country Shares">',
            f'<meta property="og:title" content="{esc(title)}">',
            f'<meta property="og:description" content="{esc(description)}">',
            f'<meta property="og:url" content="{esc(url)}">',
            f'<meta property="og:image" content="{esc(card_url)}">',
            f'<meta property="og:image:secure_url" content="{esc(card_url)}">',
            f'<meta property="og:image:type" content="image/png">',
            f'<meta property="og:image:width" content="1200">',
            f'<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{esc('Preview card for ' + title)}">',
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{esc(title)}">',
            f'<meta name="twitter:description" content="{esc(description)}">',
            f'<meta name="twitter:image" content="{esc(card_url)}">',
        ]
    )


def add_metadata(source, title, description, url, card_url):
    head_open = re.search(r"<head\b[^>]*>", source, flags=re.I)
    if not head_open:
        head = f"<head><meta charset=\"utf-8\"><title>{html.escape(title)}</title>\n{meta_tags(title, description, url, card_url)}\n</head>"
        document = re.sub(r"(<html\b[^>]*>)", lambda match: match.group(1) + "\n" + head, source, count=1, flags=re.I)
        return document if document != source else head + "\n" + source

    head_close = re.search(r"</head\s*>", source[head_open.end() :], flags=re.I)
    if not head_close:
        raise ValueError("HTML has a <head> with no closing </head>")
    end = head_open.end() + head_close.start()
    old_head = source[head_open.end() : end]

    def keep_meta(match):
        raw = match.group(0)
        key = (tag_attr(raw, "property") or tag_attr(raw, "name")).lower()
        return "" if key == "description" or key.startswith(("og:", "twitter:")) else raw

    old_head = re.sub(r"<meta\b[^>]*>", keep_meta, old_head, flags=re.I)
    old_head = re.sub(
        r"<link\b[^>]*>",
        lambda match: "" if "canonical" in tag_attr(match.group(0), "rel").lower().split() else match.group(0),
        old_head,
        flags=re.I,
    )
    if re.search(r"<title\b[^>]*>.*?</title\s*>", old_head, flags=re.I | re.S):
        old_head = re.sub(
            r"<title\b[^>]*>.*?</title\s*>",
            lambda match: f"<title>{html.escape(title)}</title>",
            old_head,
            count=1,
            flags=re.I | re.S,
        )
    else:
        old_head = f"<title>{html.escape(title)}</title>\n" + old_head
    return source[: head_open.end()] + "\n" + meta_tags(title, description, url, card_url) + "\n" + old_head + source[end:]


def font(size, bold=False):
    names = (
        ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold
        else ["/System/Library/Fonts/Supplemental/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for name in names:
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default(size=size)


def wrap(draw, value, chosen_font, max_width, max_lines):
    words = value.split()
    lines = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=chosen_font) <= max_width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while draw.textlength(lines[-1] + "…", font=chosen_font) > max_width and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return lines


def render_card(title, description, image_path, output):
    canvas = Image.new("RGB", CARD_SIZE, "#0b1426")
    draw = ImageDraw.Draw(canvas)
    for y in range(CARD_SIZE[1]):
        shade = int(14 + y * 13 / CARD_SIZE[1])
        draw.line((0, y, 1199, y), fill=(shade, shade + 7, shade + 24))
    draw.rounded_rectangle((54, 52, 1146, 578), radius=28, outline="#33506a", width=2)
    draw.rounded_rectangle((76, 78, 94, 96), radius=5, fill="#44d6c8")
    draw.text((112, 76), "FUN COUNTRY  /  SHARE", font=font(23, True), fill="#a6c8cf")

    text_width = 620 if image_path else 990
    title_font = font(72, True)
    title_lines = wrap(draw, title, title_font, text_width, 4)
    while len(title_lines) > 3 and title_font.size > 48:
        title_font = font(title_font.size - 4, True)
        title_lines = wrap(draw, title, title_font, text_width, 4)
    line_height = title_font.size + 11
    y = 156
    for line in title_lines:
        draw.text((76, y), line, font=title_font, fill="#f6fbff")
        y += line_height

    y = max(y + 16, 375)
    desc_font = font(27)
    for line in wrap(draw, description, desc_font, text_width, 2):
        draw.text((78, y), line, font=desc_font, fill="#bfd0dc")
        y += 38
    draw.line((78, 532, 390, 532), fill="#44d6c8", width=4)
    draw.text((78, 545), "share.fun.country", font=font(20), fill="#8eacbd")

    if image_path:
        with Image.open(image_path) as source:
            source = ImageOps.exif_transpose(source).convert("RGB")
            size = (380, 378)
            fitted = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS)
            mask = Image.new("L", size)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=22, fill=255)
            canvas.paste(fitted, (740, 132), mask)
            draw.rounded_rectangle((739, 131, 1121, 511), radius=23, outline="#668597", width=2)
    else:
        draw.rounded_rectangle((830, 213, 1093, 441), radius=24, outline="#3b6470", width=3)
        draw.rounded_rectangle((856, 240, 1067, 272), radius=8, fill="#2c6670")
        for offset, width in ((0, 165), (47, 125), (94, 180)):
            draw.rounded_rectangle((856, 306 + offset, 856 + width, 320 + offset), radius=7, fill="#33536b")
        draw.ellipse((1032, 451, 1095, 514), fill="#44d6c8")

    canvas.save(output, format="PNG", optimize=True)


def object_url(base, slug, relative):
    path = "/".join(urllib.parse.quote(piece, safe="") for piece in relative.split("/"))
    return f"{base.rstrip('/')}/{urllib.parse.quote(slug, safe='')}/{path}"


def share_page(title, description, url, card_url, direct_url, relative, files, base, slug):
    esc = lambda value: html.escape(value, quote=True)
    ext = Path(relative).suffix.lower()
    media = ""
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        media = f'<img class="media" src="{esc(direct_url)}" alt="{esc(title)}">'
    elif ext == ".pdf":
        media = f'<iframe class="media pdf" src="{esc(direct_url)}" title="{esc(title)}"></iframe>'
    elif ext in (".mp4", ".webm", ".mov"):
        media = f'<video class="media" controls src="{esc(direct_url)}"></video>'
    elif ext in (".mp3", ".wav"):
        media = f'<audio class="media" controls src="{esc(direct_url)}"></audio>'
    file_links = "\n".join(
        f'<li><a href="{esc(object_url(base, slug, item))}">{esc(item)}</a></li>' for item in files
    )
    file_section = f'<section><h2>Files in this share</h2><ul>{file_links}</ul></section>' if len(files) > 1 else ""
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{esc(title)}</title>
{meta_tags(title, description, url, card_url)}
<style>
:root {{ color-scheme: dark; font-family: system-ui, -apple-system, Segoe UI, sans-serif; background: #0b1426; color: #f6fbff; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; }} main {{ max-width: 1100px; margin: auto; padding: 48px 24px 80px; }}
.eyebrow {{ color: #65dacc; font-size: 13px; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; }}
h1 {{ font-size: clamp(34px, 5vw, 62px); line-height: 1.09; margin: 18px 0; }} p {{ color: #c4d1dc; font-size: 19px; line-height: 1.55; max-width: 780px; }}
.button {{ display: inline-block; background: #44d6c8; color: #082328; text-decoration: none; border-radius: 10px; padding: 15px 21px; font-weight: 700; margin: 20px 0 28px; }}
.button:hover {{ background: #75eee2; }} .media {{ display: block; max-width: 100%; max-height: 75vh; border: 1px solid #365269; border-radius: 12px; background: #13243a; }}
.pdf {{ width: 100%; height: 75vh; }} h2 {{ font-size: 20px; margin-top: 48px; }} ul {{ padding-left: 20px; }} li {{ margin: 8px 0; overflow-wrap: anywhere; }} a {{ color: #75eee2; }}
</style></head><body><main><div class="eyebrow">Fun Country / Shared artifact</div>
<h1>{esc(title)}</h1><p>{esc(description)}</p>
<a class="button" href="{esc(direct_url)}">Open {esc(Path(relative).name)}</a>
{media}{file_section}</main></body></html>'''


def prepare(args):
    source_path = Path(args.entry)
    source = source_path.read_text(encoding="utf-8", errors="replace") if args.mode == "html" else ""
    parsed = parse_page(source) if source else PageText()
    filename = source_path.name
    fallback = re.sub(r"[_-]+", " ", Path(filename).stem).strip().title()
    if fallback.lower() in ("index", "report", "share"):
        fallback = re.sub(r"[_-]+", " ", source_path.parent.name).strip().title() or "Shared artifact"
    title = shorten(args.title or parsed.title or parsed.heading or parsed.meta.get("og:title") or fallback, 115)
    first_paragraph = next((p for p in parsed.paragraphs if len(p) >= 35), "")
    description_source = args.description or parsed.meta.get("description") or parsed.meta.get("og:description") or first_paragraph
    if not clean(description_source):
        raise ValueError("provide --description; the artifact has no descriptive page text")
    description = shorten(description_source, 220)
    if not title or not description:
        raise ValueError("could not determine a useful preview title and description")

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    image_path = Path(args.image) if args.image else None
    if image_path and not image_path.is_file():
        raise ValueError(f"preview image does not exist: {image_path}")
    if image_path is None and source_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        image_path = source_path
    render_card(title, description, image_path, output / "card.png")

    if args.mode == "html":
        transformed = add_metadata(source, title, description, args.url, args.card_url)
        (output / "entry.html").write_text(transformed, encoding="utf-8")
    else:
        page = share_page(title, description, args.url, args.card_url, args.direct_url, args.relative, args.file, args.base_url, args.slug)
        (output / "share.html").write_text(page, encoding="utf-8")
    (output / "info.json").write_text(
        json.dumps({"title": title, "description": description, "url": args.url, "card_url": args.card_url, "direct_url": args.direct_url}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"preview: {title}")
    print(f"summary: {description}")


def fetch(url, method="GET", limit=None):
    request = urllib.request.Request(url, method=method, headers={"User-Agent": "cf-share-preview-check/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read(limit) if method == "GET" else b""
        return response.status, response.headers.get_content_type(), data


def verify(args):
    info = json.loads(Path(args.info).read_text(encoding="utf-8"))
    status, content_type, body = fetch(info["url"], limit=512 * 1024)
    if status != 200 or content_type != "text/html":
        raise ValueError(f"share page: HTTP {status}, {content_type}")
    parsed = parse_page(body.decode("utf-8", errors="replace"))
    required = {
        "og:title": info["title"],
        "og:description": info["description"],
        "og:url": info["url"],
        "og:image": info["card_url"],
        "twitter:card": "summary_large_image",
        "twitter:title": info["title"],
        "twitter:image": info["card_url"],
    }
    for key, expected in required.items():
        if parsed.meta.get(key) != expected:
            raise ValueError(f"share page {key}: expected {expected!r}, got {parsed.meta.get(key)!r}")
    status, content_type, card = fetch(info["card_url"])
    if status != 200 or content_type != "image/png":
        raise ValueError(f"preview card: HTTP {status}, {content_type}")
    with Image.open(io.BytesIO(card)) as image:
        if image.size != CARD_SIZE:
            raise ValueError(f"preview card size: {image.size}, expected {CARD_SIZE}")
    status, _, _ = fetch(info["direct_url"], method="HEAD")
    if status != 200:
        raise ValueError(f"artifact: HTTP {status}")
    print("verified HTTP 200: share page, Open Graph, X Card, 1200x630 PNG, artifact")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    for name in ("entry", "relative", "url", "card-url", "direct-url", "base-url", "slug", "output-dir", "mode"):
        prep.add_argument("--" + name, required=True)
    prep.add_argument("--title", default="")
    prep.add_argument("--description", default="")
    prep.add_argument("--image", default="")
    prep.add_argument("--file", action="append", default=[])
    check = commands.add_parser("verify")
    check.add_argument("--info", required=True)
    args = parser.parse_args()
    try:
        prepare(args) if args.command == "prepare" else verify(args)
    except Exception as exc:
        print(f"cf-share preview error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
