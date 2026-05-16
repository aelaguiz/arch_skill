#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow>=10"]
# ///
"""Build compact PNG contact sheets from local image files.

The default stdout is intentionally small because agents read it as context.
Full details are written to a manifest beside the generated sheet.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import json
import math
import os
import re
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    from PIL import __version__ as PILLOW_VERSION
except ImportError as exc:  # pragma: no cover - depends on host env
    print("ERROR missing_dependency Pillow is required: python3 -m pip install Pillow", file=sys.stderr)
    raise SystemExit(4) from exc


IMAGE_SUFFIXES = {
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}
DEFAULT_PAGE_WIDTH = 2048
DEFAULT_PAGE_HEIGHT = 2560
DEFAULT_LABEL_MAX = 32
DEFAULT_MAX_THUMB_WIDTH = 2048
DEFAULT_MAX_THUMB_HEIGHT = 2048
DEFAULT_MAX_PAGE_HEIGHT = 12000
DEFAULT_DYNAMIC_MARGIN = 0
DEFAULT_DYNAMIC_GUTTER = 2
DEFAULT_DYNAMIC_LABEL_HEIGHT = 44
DEFAULT_FIXED_MARGIN = 32
DEFAULT_FIXED_GUTTER = 16
DEFAULT_FIXED_LABEL_HEIGHT = 68
DEFAULT_ROOT = Path("/tmp") / "contact-sheet-builder"
WARNING_STDOUT_LIMIT = 10


class ContactSheetError(RuntimeError):
    def __init__(self, message: str, exit_code: int = 4) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(f"ERROR invalid_options {message}", file=sys.stderr)
        raise SystemExit(4)


@dataclass
class SkippedInput:
    path: str
    reason: str


@dataclass
class ImageRecord:
    path: Path
    width: int
    height: int
    mode: str
    has_alpha: bool
    label: str = ""
    page: int = 0
    index: int = 0

    def to_manifest(self) -> dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass
class Layout:
    mode: str
    page_width: int
    page_height: int
    page_heights: list[int]
    page_row_ranges: list[tuple[int, int]]
    row_image_heights: list[int]
    columns: int
    rows_per_page: int
    images_per_page: int
    margin: int
    gutter: int
    cell_width: int
    image_height: int
    label_height: int
    title_height: int


@dataclass
class OutputPlan:
    output_dir: Path
    output_paths: list[Path]
    manifest_path: Path


@dataclass
class OpenResult:
    requested: bool
    status: str
    app: str | None = None
    reason: str | None = None


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def natural_key(value: str | Path) -> list[Any]:
    text = str(value).lower()
    parts = re.split(r"(\d+)", text)
    return [int(part) if part.isdigit() else part for part in parts]


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts if part not in {".", ".."})


def has_glob_magic(value: str) -> bool:
    return any(char in value for char in "*?[")


def normalize_path_arg(raw: str) -> str:
    return os.path.expandvars(os.path.expanduser(raw))


def iter_folder_images(folder: Path, *, recursive: bool, include_hidden: bool) -> Iterable[Path]:
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    for item in sorted(iterator, key=natural_key):
        if item.is_dir():
            continue
        if not include_hidden and is_hidden(item.relative_to(folder)):
            continue
        yield item


def resolve_inputs(raw_paths: list[str], *, recursive: bool, include_hidden: bool) -> tuple[list[Path], list[SkippedInput]]:
    candidates: list[Path] = []
    skipped: list[SkippedInput] = []

    for raw in raw_paths:
        expanded = normalize_path_arg(raw)
        matches: list[Path]
        if has_glob_magic(expanded):
            matches = [Path(match) for match in glob.glob(expanded, recursive=recursive or "**" in expanded)]
            if not matches:
                skipped.append(SkippedInput(raw, "no matches"))
                continue
        else:
            matches = [Path(expanded)]

        for match in sorted(matches, key=natural_key):
            path = match.expanduser()
            if not path.exists():
                skipped.append(SkippedInput(str(path), "not found"))
                continue
            if not include_hidden and is_hidden(path):
                skipped.append(SkippedInput(str(path), "hidden file"))
                continue
            if path.is_dir():
                for child in iter_folder_images(path, recursive=recursive, include_hidden=include_hidden):
                    if child.suffix.lower() in IMAGE_SUFFIXES:
                        candidates.append(child)
                    else:
                        skipped.append(SkippedInput(str(child), "unsupported file type"))
                continue
            if path.is_file():
                candidates.append(path)
                continue
            skipped.append(SkippedInput(str(path), "not a regular file"))

    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        try:
            key = path.resolve()
        except OSError:
            key = path.absolute()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)
    return deduped, skipped


def inspect_image(path: Path) -> ImageRecord | None:
    with Image.open(path) as image:
        width, height = image.size
        mode = image.mode
        has_alpha = image_has_alpha(image)
    if width <= 0 or height <= 0:
        return None
    return ImageRecord(path=path, width=width, height=height, mode=mode, has_alpha=has_alpha)


def image_has_alpha(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return True
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def load_usable_images(paths: list[Path], skipped: list[SkippedInput]) -> list[ImageRecord]:
    usable: list[ImageRecord] = []
    for path in paths:
        try:
            record = inspect_image(path)
        except Exception as exc:  # noqa: BLE001 - Pillow raises several decode errors.
            skipped.append(SkippedInput(str(path), f"not a valid image: {exc}"))
            continue
        if record is None:
            skipped.append(SkippedInput(str(path), "not a valid image"))
            continue
        usable.append(record)
    return usable


def parse_columns(raw: str, image_count: int) -> int:
    if raw == "auto":
        if image_count <= 1:
            return 1
        if image_count == 2:
            return 2
        if image_count <= 4:
            return 2
        if image_count <= 6:
            return 3
        return 4
    try:
        value = int(raw)
    except ValueError as exc:
        raise ContactSheetError("--columns must be auto or a positive integer", 4) from exc
    if value < 1:
        raise ContactSheetError("--columns must be at least 1", 4)
    return value


def parse_bg(raw: str) -> tuple[int, int, int] | str:
    value = raw.strip().lower()
    named = {
        "neutral": (244, 244, 241),
        "white": (255, 255, 255),
        "black": (18, 18, 18),
        "checker": "checker",
    }
    if value in named:
        return named[value]
    if re.fullmatch(r"#[0-9a-fA-F]{6}", raw):
        return tuple(int(raw[i : i + 2], 16) for i in (1, 3, 5))  # type: ignore[return-value]
    raise ContactSheetError("--bg must be neutral, white, black, checker, or #RRGGBB", 4)


def calculate_layout(
    *,
    records: list[ImageRecord],
    page_width: int,
    page_height: int,
    columns: int,
    labels_on: bool,
    title: str | None,
    mode: str,
    margin: int | None,
    gutter: int | None,
    max_thumb_width: int,
    max_thumb_height: int,
    max_page_height: int,
) -> Layout:
    if mode == "dynamic":
        return calculate_dynamic_layout(
            records=records,
            columns=columns,
            labels_on=labels_on,
            title=title,
            margin=margin,
            gutter=gutter,
            max_thumb_width=max_thumb_width,
            max_thumb_height=max_thumb_height,
            max_page_height=max_page_height,
        )
    return calculate_fixed_layout(
        records=records,
        page_width=page_width,
        page_height=page_height,
        columns=columns,
        labels_on=labels_on,
        title=title,
        margin=margin,
        gutter=gutter,
    )


def calculate_fixed_layout(
    *,
    records: list[ImageRecord],
    page_width: int,
    page_height: int,
    columns: int,
    labels_on: bool,
    title: str | None,
    margin: int | None,
    gutter: int | None,
) -> Layout:
    if page_width < 360 or page_height < 360:
        raise ContactSheetError("--page-width and --page-height must be at least 360", 4)
    margin = DEFAULT_FIXED_MARGIN if margin is None else margin
    gutter = DEFAULT_FIXED_GUTTER if gutter is None else gutter
    validate_spacing(margin=margin, gutter=gutter)
    title_height = 78 if title else 0
    label_height = DEFAULT_FIXED_LABEL_HEIGHT if labels_on else 0
    usable_width = page_width - (2 * margin) - (gutter * (columns - 1))
    if usable_width < columns * 120:
        raise ContactSheetError("too many columns for page width", 4)
    cell_width = usable_width // columns
    available_height = page_height - (2 * margin) - title_height
    if available_height < 180:
        raise ContactSheetError("page height leaves no room for images", 4)
    image_height = int(cell_width * 0.85)
    max_image_height = max(96, available_height - label_height)
    image_height = min(image_height, max_image_height)
    row_height = image_height + label_height
    rows_per_page = max(1, int((available_height + gutter) // (row_height + gutter)))
    images_per_page = max(1, rows_per_page * columns)
    total_rows = max(1, math.ceil(len(records) / columns))
    page_row_ranges = [
        (start_row, min(start_row + rows_per_page, total_rows))
        for start_row in range(0, total_rows, rows_per_page)
    ]
    return Layout(
        mode="fixed",
        page_width=page_width,
        page_height=page_height,
        page_heights=[page_height for _ in page_row_ranges],
        page_row_ranges=page_row_ranges,
        row_image_heights=[image_height for _ in range(total_rows)],
        columns=columns,
        rows_per_page=rows_per_page,
        images_per_page=images_per_page,
        margin=margin,
        gutter=gutter,
        cell_width=cell_width,
        image_height=image_height,
        label_height=label_height,
        title_height=title_height,
    )


def calculate_dynamic_layout(
    *,
    records: list[ImageRecord],
    columns: int,
    labels_on: bool,
    title: str | None,
    margin: int | None,
    gutter: int | None,
    max_thumb_width: int,
    max_thumb_height: int,
    max_page_height: int,
) -> Layout:
    if max_thumb_width < 120 or max_thumb_height < 120:
        raise ContactSheetError("--max-thumb-width and --max-thumb-height must be at least 120", 4)
    if max_page_height < 720:
        raise ContactSheetError("--max-page-height must be at least 720", 4)

    scaled_sizes: list[tuple[int, int]] = []
    for record in records:
        scale = min(1.0, max_thumb_width / record.width, max_thumb_height / record.height)
        scaled_sizes.append((max(1, round(record.width * scale)), max(1, round(record.height * scale))))

    cell_width = max(width for width, _height in scaled_sizes)
    content_width = columns * cell_width
    margin = DEFAULT_DYNAMIC_MARGIN if margin is None else margin
    gutter = DEFAULT_DYNAMIC_GUTTER if gutter is None else gutter
    validate_spacing(margin=margin, gutter=gutter)
    title_height = 78 if title else 0
    label_height = DEFAULT_DYNAMIC_LABEL_HEIGHT if labels_on else 0
    page_width = (2 * margin) + content_width + (gutter * (columns - 1))
    total_rows = max(1, math.ceil(len(records) / columns))
    row_image_heights: list[int] = []
    for row in range(total_rows):
        row_sizes = scaled_sizes[row * columns : (row + 1) * columns]
        row_image_heights.append(max(height for _width, height in row_sizes))

    page_row_ranges: list[tuple[int, int]] = []
    page_heights: list[int] = []
    row = 0
    while row < total_rows:
        start_row = row
        page_body_height = title_height
        rows_in_page = 0
        while row < total_rows:
            next_row_height = row_image_heights[row] + label_height
            extra_gutter = gutter if rows_in_page > 0 else 0
            projected = (2 * margin) + page_body_height + extra_gutter + next_row_height
            if rows_in_page > 0 and projected > max_page_height:
                break
            page_body_height += extra_gutter + next_row_height
            row += 1
            rows_in_page += 1
        end_row = row
        page_row_ranges.append((start_row, end_row))
        page_heights.append((2 * margin) + page_body_height)

    max_rows_per_page = max(end - start for start, end in page_row_ranges)
    return Layout(
        mode="dynamic",
        page_width=page_width,
        page_height=page_heights[0],
        page_heights=page_heights,
        page_row_ranges=page_row_ranges,
        row_image_heights=row_image_heights,
        columns=columns,
        rows_per_page=max_rows_per_page,
        images_per_page=max_rows_per_page * columns,
        margin=margin,
        gutter=gutter,
        cell_width=cell_width,
        image_height=max(row_image_heights),
        label_height=label_height,
        title_height=title_height,
    )


def validate_spacing(*, margin: int, gutter: int) -> None:
    if margin < 0:
        raise ContactSheetError("--margin must be zero or positive", 4)
    if gutter < 0:
        raise ContactSheetError("--gutter must be zero or positive", 4)


def unique_run_dir(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    base = root / utc_stamp()
    candidate = base
    suffix = 1
    while candidate.exists():
        candidate = Path(f"{base}-{suffix:02d}")
        suffix += 1
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def resolve_output_plan(out_arg: str | None, page_count: int, *, force: bool) -> OutputPlan:
    if page_count < 1:
        page_count = 1
    if out_arg is None:
        output_dir = unique_run_dir(DEFAULT_ROOT)
        output_paths = default_page_paths(output_dir, page_count)
        return OutputPlan(output_dir=output_dir, output_paths=output_paths, manifest_path=output_dir / "manifest.json")

    out_path = Path(normalize_path_arg(out_arg))
    looks_like_file = out_path.suffix.lower() == ".png"
    if looks_like_file:
        output_dir = out_path.parent if out_path.parent != Path("") else Path(".")
        output_dir.mkdir(parents=True, exist_ok=True)
        if page_count == 1:
            output_paths = [out_path]
        else:
            output_paths = [
                output_dir / f"{out_path.stem}_page_{page_number:03d}{out_path.suffix}"
                for page_number in range(1, page_count + 1)
            ]
        manifest_path = output_dir / f"{out_path.stem}.manifest.json"
    else:
        output_dir = out_path
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = default_page_paths(output_dir, page_count)
        manifest_path = output_dir / "manifest.json"

    collisions = [path for path in [*output_paths, manifest_path] if path.exists()]
    if collisions and not force:
        first = collisions[0]
        raise ContactSheetError(f"BLOCKED output_exists path={first} use --force to overwrite", 3)
    return OutputPlan(output_dir=output_dir, output_paths=output_paths, manifest_path=manifest_path)


def resolve_error_output_plan(out_arg: str | None, *, force: bool) -> OutputPlan:
    if out_arg is None:
        output_dir = unique_run_dir(DEFAULT_ROOT)
        return OutputPlan(output_dir=output_dir, output_paths=[], manifest_path=output_dir / "manifest.json")

    out_path = Path(normalize_path_arg(out_arg))
    if out_path.suffix.lower() == ".png":
        output_dir = out_path.parent if out_path.parent != Path("") else Path(".")
        manifest_path = output_dir / f"{out_path.stem}.manifest.json"
    else:
        output_dir = out_path
        manifest_path = output_dir / "manifest.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    if manifest_path.exists() and not force:
        raise ContactSheetError(f"BLOCKED output_exists path={manifest_path} use --force to overwrite", 3)
    return OutputPlan(output_dir=output_dir, output_paths=[], manifest_path=manifest_path)


def default_page_paths(output_dir: Path, page_count: int) -> list[Path]:
    if page_count == 1:
        return [output_dir / "contact_sheet.png"]
    return [output_dir / f"contact_sheet_page_{page_number:03d}.png" for page_number in range(1, page_count + 1)]


def read_labels(args: argparse.Namespace, image_count: int) -> list[str] | None:
    labels: list[str] | None = None
    if args.labels and args.labels_file:
        raise ContactSheetError("use --labels or --labels-file, not both", 4)
    if args.labels:
        labels = next(csv.reader([args.labels]))
    elif args.labels_file:
        path = Path(normalize_path_arg(args.labels_file))
        try:
            labels = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise ContactSheetError(f"could not read labels file: {exc}", 4) from exc
    if labels is None:
        return None
    labels = [label.strip() for label in labels]
    if len(labels) != image_count:
        raise ContactSheetError(f"explicit label count {len(labels)} does not match usable image count {image_count}", 4)
    return labels


def derive_labels(records: list[ImageRecord], source: str, explicit: list[str] | None, label_max: int) -> None:
    if explicit is not None:
        for record, label in zip(records, explicit, strict=True):
            record.label = clamp_label(label, label_max)
        return

    raw_labels: list[str] = []
    for index, record in enumerate(records, start=1):
        if source == "stem":
            label = readable_stem(record.path.stem)
        elif source == "filename":
            label = record.path.name
        elif source == "parent":
            label = record.path.parent.name or record.path.name
        elif source == "index":
            label = str(index)
        else:
            raise ContactSheetError("--labels-from must be stem, filename, parent, or index", 4)
        raw_labels.append(label)

    counts: dict[str, int] = {}
    for label in raw_labels:
        counts[label] = counts.get(label, 0) + 1

    seen: dict[str, int] = {}
    for record, label in zip(records, raw_labels, strict=True):
        final = label
        if counts[label] > 1:
            final = f"{record.path.parent.name} / {label}"
        seen[final] = seen.get(final, 0) + 1
        if seen[final] > 1:
            final = f"{final} {seen[final]}"
        record.label = clamp_label(final, label_max)


def readable_stem(stem: str) -> str:
    value = re.sub(r"[_-]+", " ", stem)
    value = re.sub(r"\s+", " ", value).strip()
    return value or stem


def clamp_label(label: str, label_max: int) -> str:
    text = re.sub(r"\s+", " ", label).strip()
    if label_max < 4:
        raise ContactSheetError("--label-max must be at least 4", 4)
    if len(text) <= label_max:
        return text
    return text[: label_max - 3].rstrip() + "..."


def load_font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_word(draw: ImageDraw.ImageDraw, word: str, font: ImageFont.ImageFont, max_width: int) -> str:
    if measure_text(draw, word, font)[0] <= max_width:
        return word
    if len(word) <= 3:
        return word
    result = word
    while len(result) > 3 and measure_text(draw, result + "...", font)[0] > max_width:
        result = result[:-1]
    return result.rstrip() + "..."


def wrap_label(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int, max_lines: int = 2) -> list[str]:
    words = [fit_word(draw, word, font, max_width) for word in text.split()]
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if measure_text(draw, candidate, font)[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    tail = " ".join([kept[-1], *lines[max_lines:]])
    kept[-1] = fit_word(draw, tail, font, max_width)
    return kept


def make_checker(width: int, height: int, square: int = 18) -> Image.Image:
    image = Image.new("RGB", (width, height), (238, 238, 238))
    draw = ImageDraw.Draw(image)
    for y in range(0, height, square):
        for x in range(0, width, square):
            if (x // square + y // square) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill=(205, 205, 205))
    return image


def page_background(width: int, height: int, bg: tuple[int, int, int] | str) -> Image.Image:
    if bg == "checker":
        return make_checker(width, height, square=24)
    return Image.new("RGB", (width, height), bg)


def render_image_into_box(page: Image.Image, record: ImageRecord, box: tuple[int, int, int, int], *, fallback_bg: tuple[int, int, int]) -> None:
    x, y, width, height = box
    with Image.open(record.path) as raw:
        image = ImageOps.exif_transpose(raw)
        has_alpha = image_has_alpha(image)
        image = image.convert("RGBA" if has_alpha else "RGB")
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        thumb_x = x + (width - image.width) // 2
        thumb_y = y + (height - image.height) // 2
        if has_alpha:
            base = make_checker(width, height)
            page.paste(base, (x, y))
            region = page.crop((thumb_x, thumb_y, thumb_x + image.width, thumb_y + image.height)).convert("RGBA")
            region.alpha_composite(image)
            page.paste(region.convert("RGB"), (thumb_x, thumb_y))
        else:
            ImageDraw.Draw(page).rectangle((x, y, x + width, y + height), fill=fallback_bg)
            page.paste(image, (thumb_x, thumb_y))


def render_pages(
    records: list[ImageRecord],
    output_plan: OutputPlan,
    layout: Layout,
    *,
    labels_on: bool,
    title: str | None,
    bg: tuple[int, int, int] | str,
) -> None:
    label_font = load_font(20 if layout.mode == "dynamic" else 26)
    title_font = load_font(44, bold=True)
    page_count = len(output_plan.output_paths)
    cell_fill = bg if isinstance(bg, tuple) else (246, 246, 246)
    image_fill = cell_fill if isinstance(cell_fill, tuple) else (244, 244, 241)
    border = (210, 210, 205)
    text_fill = (25, 25, 25) if bg != (18, 18, 18) else (235, 235, 235)

    for page_index, output_path in enumerate(output_plan.output_paths):
        start_row, end_row = layout.page_row_ranges[page_index]
        start = start_row * layout.columns
        end = min(end_row * layout.columns, len(records))
        page_records = records[start:end]
        page = page_background(layout.page_width, layout.page_heights[page_index], bg)
        draw = ImageDraw.Draw(page)
        top = layout.margin

        if title:
            title_text = title if page_count == 1 else f"{title} ({page_index + 1}/{page_count})"
            title_width, title_height = measure_text(draw, title_text, title_font)
            draw.text(((layout.page_width - title_width) // 2, top), title_text, font=title_font, fill=text_fill)
            top += max(layout.title_height, title_height + 26)

        for item_index, record in enumerate(page_records):
            page_row = item_index // layout.columns
            row = start_row + page_row
            col = item_index % layout.columns
            x = layout.margin + col * (layout.cell_width + layout.gutter)
            y = top
            for prior_row in range(start_row, row):
                y += layout.row_image_heights[prior_row] + layout.label_height + layout.gutter
            row_image_height = layout.row_image_heights[row]
            row_height = row_image_height + layout.label_height
            cell_bottom = y + row_height
            if layout.mode == "fixed":
                draw.rectangle((x, y, x + layout.cell_width, cell_bottom), fill=cell_fill, outline=border, width=2)
                image_box = (x + 1, y + 1, layout.cell_width - 2, row_image_height - 2)
            else:
                image_box = (x, y, layout.cell_width, row_image_height)
            render_image_into_box(page, record, image_box, fallback_bg=image_fill)
            if labels_on:
                label_gap = 3 if layout.mode == "dynamic" else 8
                label_pad = 8 if layout.mode == "dynamic" else 22
                label_top = y + row_image_height + label_gap
                lines = wrap_label(draw, record.label, label_font, max(24, layout.cell_width - label_pad), max_lines=2)
                line_heights = [measure_text(draw, line, label_font)[1] for line in lines]
                total_height = sum(line_heights) + max(0, len(lines) - 1) * 4
                cursor_y = label_top + max(0, (layout.label_height - label_gap - total_height) // 2)
                for line, line_height in zip(lines, line_heights, strict=True):
                    line_width, _ = measure_text(draw, line, label_font)
                    draw.text((x + (layout.cell_width - line_width) // 2, cursor_y), line, font=label_font, fill=(35, 35, 35))
                    cursor_y += line_height + 4
            global_index = start + item_index
            record.page = page_index + 1
            record.index = global_index + 1

        output_path.parent.mkdir(parents=True, exist_ok=True)
        page.save(output_path, "PNG")


def write_manifest(
    path: Path,
    *,
    args: argparse.Namespace,
    records: list[ImageRecord],
    skipped: list[SkippedInput],
    output_plan: OutputPlan,
    layout: Layout | None,
    open_result: OpenResult,
    status: str,
) -> None:
    manifest = {
        "version": 1,
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": status,
        "command": " ".join(shlex.quote(arg) for arg in sys.argv),
        "pillow_version": PILLOW_VERSION,
        "args": {
            "columns": args.columns,
            "labels": not args.no_labels,
            "labels_from": args.labels_from,
            "label_max": args.label_max,
            "margin": args.margin,
            "gutter": args.gutter,
            "page_width": args.page_width,
            "page_height": args.page_height,
            "fixed_page": args.page_width is not None or args.page_height is not None,
            "max_thumb_width": args.max_thumb_width,
            "max_thumb_height": args.max_thumb_height,
            "max_page_height": args.max_page_height,
            "bg": args.bg,
            "recursive": args.recursive,
            "include_hidden": args.include_hidden,
            "open_preview": not args.no_open,
            "force": args.force,
        },
        "summary": {
            "images": len(records),
            "skipped": len(skipped),
            "pages": len(output_plan.output_paths),
            "output_dir": str(output_plan.output_dir),
            "manifest": str(output_plan.manifest_path),
        },
        "layout": asdict(layout) if layout else None,
        "preview": asdict(open_result),
        "outputs": [str(output_path) for output_path in output_plan.output_paths],
        "images": [record.to_manifest() for record in records],
        "skipped": [asdict(item) for item in skipped],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def warning_lines(skipped: list[SkippedInput]) -> list[str]:
    lines = [f"warning: skipped {item.path} ({item.reason})" for item in skipped[:WARNING_STDOUT_LIMIT]]
    remaining = len(skipped) - WARNING_STDOUT_LIMIT
    if remaining > 0:
        lines.append(f"warning: {remaining} more skipped inputs; see manifest")
    return lines


def open_in_preview(paths: list[Path], *, enabled: bool) -> OpenResult:
    if not enabled:
        return OpenResult(requested=False, status="disabled", app="Preview")
    if not paths:
        return OpenResult(requested=False, status="skipped", app="Preview", reason="no outputs")
    if sys.platform != "darwin":
        return OpenResult(requested=True, status="skipped", app="Preview", reason="not macOS")
    command = ["open", "-a", "Preview", *[str(path) for path in paths]]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=10)
    except FileNotFoundError:
        return OpenResult(requested=True, status="failed", app="Preview", reason="open command not found")
    except subprocess.TimeoutExpired:
        return OpenResult(requested=True, status="failed", app="Preview", reason="open command timed out")
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        reason = stderr or stdout or f"open exited {exc.returncode}"
        return OpenResult(requested=True, status="failed", app="Preview", reason=reason)
    return OpenResult(requested=True, status="opened", app="Preview")


def build_parser() -> Parser:
    parser = Parser(description="Build a PNG contact sheet from local images.")
    parser.add_argument("paths", nargs="+", help="Image files, folders, or globs.")
    parser.add_argument("--out", help="Output PNG path or directory. Defaults to /tmp/contact-sheet-builder/<UTC-timestamp>/")
    parser.add_argument("--columns", default="auto", help="auto or a positive integer. Default: auto.")
    parser.add_argument("--no-labels", action="store_true", help="Turn labels off.")
    parser.add_argument(
        "--labels-from",
        choices=["stem", "filename", "parent", "index"],
        default="stem",
        help="Label source when labels are on. Default: stem.",
    )
    parser.add_argument("--labels", help="CSV labels, one per usable image.")
    parser.add_argument("--labels-file", help="Text file with one label per usable image.")
    parser.add_argument("--label-max", type=int, default=DEFAULT_LABEL_MAX, help="Maximum label characters. Default: 32.")
    parser.add_argument("--margin", type=int, help="Outer margin in pixels. Defaults: dynamic 0, fixed 32.")
    parser.add_argument("--gutter", type=int, help="Gap between cells in pixels. Defaults: dynamic 2, fixed 16.")
    parser.add_argument("--title", help="Optional sheet title.")
    parser.add_argument("--page-width", type=int, help="Use a fixed page width in pixels. Default: dynamic native-ish sheet width.")
    parser.add_argument("--page-height", type=int, help="Use a fixed page height in pixels. Default: dynamic native-ish sheet height.")
    parser.add_argument("--max-thumb-width", type=int, default=DEFAULT_MAX_THUMB_WIDTH, help="Largest thumbnail width in dynamic mode. Default: 2048.")
    parser.add_argument("--max-thumb-height", type=int, default=DEFAULT_MAX_THUMB_HEIGHT, help="Largest thumbnail height in dynamic mode. Default: 2048.")
    parser.add_argument("--max-page-height", type=int, default=DEFAULT_MAX_PAGE_HEIGHT, help="Maximum dynamic page height before pagination. Default: 12000.")
    parser.add_argument("--bg", default="neutral", help="neutral, white, black, checker, or #RRGGBB. Default: neutral.")
    parser.add_argument("--recursive", action="store_true", help="Read folder inputs recursively.")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files.")
    parser.add_argument("--no-open", action="store_true", help="Do not open generated sheets in Preview.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        bg = parse_bg(args.bg)
        candidates, skipped = resolve_inputs(args.paths, recursive=args.recursive, include_hidden=args.include_hidden)
        records = load_usable_images(candidates, skipped)
        if not records:
            output_plan = resolve_error_output_plan(args.out, force=args.force)
            open_result = open_in_preview([], enabled=not args.no_open)
            write_manifest(output_plan.manifest_path, args=args, records=[], skipped=skipped, output_plan=output_plan, layout=None, open_result=open_result, status="no_usable_images")
            print(f"ERROR no_usable_images skipped={len(skipped)} manifest={output_plan.manifest_path}")
            for line in warning_lines(skipped):
                print(line)
            return 2

        labels = read_labels(args, len(records)) if not args.no_labels else None
        if not args.no_labels:
            derive_labels(records, args.labels_from, labels, args.label_max)

        columns = parse_columns(args.columns, len(records))
        fixed_page = args.page_width is not None or args.page_height is not None
        layout = calculate_layout(
            records=records,
            page_width=args.page_width or DEFAULT_PAGE_WIDTH,
            page_height=args.page_height or DEFAULT_PAGE_HEIGHT,
            columns=columns,
            labels_on=not args.no_labels,
            title=args.title,
            mode="fixed" if fixed_page else "dynamic",
            margin=args.margin,
            gutter=args.gutter,
            max_thumb_width=args.max_thumb_width,
            max_thumb_height=args.max_thumb_height,
            max_page_height=args.max_page_height,
        )
        page_count = len(layout.page_row_ranges)
        output_plan = resolve_output_plan(args.out, page_count, force=args.force)
        render_pages(records, output_plan, layout, labels_on=not args.no_labels, title=args.title, bg=bg)
        open_result = open_in_preview(output_plan.output_paths, enabled=not args.no_open)
        write_manifest(output_plan.manifest_path, args=args, records=records, skipped=skipped, output_plan=output_plan, layout=layout, open_result=open_result, status="ok")
        label_state = "off" if args.no_labels else "on"
        first_output = output_plan.output_paths[0] if output_plan.output_paths else output_plan.output_dir
        print(
            "OK contact_sheet "
            f"pages={len(output_plan.output_paths)} images={len(records)} skipped={len(skipped)} "
            f"labels={label_state} columns={columns} preview={open_result.status} "
            f"out={first_output} manifest={output_plan.manifest_path}"
        )
        if open_result.status == "failed":
            print(f"warning: preview open failed ({open_result.reason})")
        elif open_result.status == "skipped" and open_result.requested:
            print(f"warning: preview open skipped ({open_result.reason})")
        for line in warning_lines(skipped):
            print(line)
        return 0
    except ContactSheetError as exc:
        print(str(exc))
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
