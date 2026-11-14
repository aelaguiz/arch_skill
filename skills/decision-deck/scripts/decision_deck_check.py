#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""Check a decision deck: render every slide at desktop and phone width and report what does not fit or does not
read; probe its links, and refuse a diff slide that dumps many changes under one approval (decision_deck_check_spec.py).

Run it on a round's spec before the deck goes in front of the owner. It serves the deck itself on 127.0.0.1 with a
throwaway ledger in a temp folder (the round's own ledger is never read or written), opens the cover, each decision
slide and the summary in headless Chromium (Python Playwright) at 1440x900 and 390x844, and prints one line per
problem. Playwright is an optional import here; decision_deck.py itself stays stdlib only. The --help text is
decision_deck_check_help.py.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_check_pngs as pngs  # noqa: E402
import decision_deck_stamp as stamp  # noqa: E402
from decision_deck_check_fit import PROBE  # noqa: E402
from decision_deck_check_help import HELP  # noqa: E402
from decision_deck_check_spec import spec_lines  # noqa: E402
from decision_deck_check_text import LIMITS, READ_PROBE  # noqa: E402
from decision_deck_spec import SpecError, load_spec  # noqa: E402

SIZES = {"desktop": {"width": 1440, "height": 900, "scale": 1}, "phone": {"width": 390, "height": 844, "scale": 2}}
# Added only for the phone PNG, after the probes: a phone draws the page's own scrollbar while a finger moves it,
# never on a still screen, and headless Chromium would paint it over the slide's right edge.
PHONE_SHOT_CSS = "html::-webkit-scrollbar { display: none; }"

SETTLE = r"""
async ([i, phone]) => {
  await document.fonts.ready;
  const slide = document.getElementById('sl-' + i);
  await Promise.all([...document.images].map((im) => im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; })));
  await Promise.all([...document.images].map((im) => im.decode ? im.decode().catch(() => 0) : 0));   // loaded is not yet drawn
  if (phone && slide) slide.scrollIntoView({ block: 'start' });
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  return !!slide;
}
"""


# The slide's box on the whole page. An element shot of a slide taller than the screen below the header bar, yet
# shorter than the screen, is taken as it sits in the window, with its foot cut and the page behind it showing.
SLIDE_BOX = """(i) => { const r = document.getElementById('sl-' + i).getBoundingClientRect();
  return { x: r.left + scrollX, y: r.top + scrollY, width: r.width, height: r.height }; }"""


def routes(spec: dict) -> list[tuple[str, str, int]]:
    """(name, path, slide index) for the cover, each decision slide and the summary."""
    n = len(spec["decisions"])
    names = [f"slide{k}" for k in range(1, n + 1)]
    return ([("cover", "/", 0)] + [(name, f"/d/{k}", k) for k, name in enumerate(names, 1)]
            + [("summary", "/summary", n + 1)])


def shot_name(mode: str, route: str) -> str:
    return f"{mode}-{route}.png"


def shot_names(spec: dict, sizes: dict | None = None) -> list[str]:
    """The PNG file names --out gets, in the order check() renders them."""
    return [shot_name(mode, name) for mode in (sizes or SIZES) for name, _, _ in routes(spec)]


class _Served:
    """The deck served in this process on 127.0.0.1, with its ledger in a temp folder that goes on exit."""

    def __init__(self, spec: dict, source: str = ""):
        self.spec, self.source = spec, source

    def __enter__(self):
        from decision_deck_routes import Handler
        from decision_deck_server import make_server

        class Quiet(Handler):
            def log_message(self, fmt, *args):
                pass

        self.tmp = tempfile.TemporaryDirectory(prefix="decision-deck-check-")
        self.srv = make_server(self.spec, Path(self.tmp.name) / "ledger.jsonl", "127.0.0.1", 0, source=self.source)
        self.srv.RequestHandlerClass = Quiet
        self.thread = threading.Thread(target=self.srv.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
        self.thread.start()
        return self.srv.url.rstrip("/")

    def __exit__(self, *exc):
        self.srv.finished.set()
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()


def check(spec: dict, out: Path | None = None, sizes: dict | None = None, source: str = "") -> list[str]:
    """Every problem as one line, `<KIND> <route> <width> <selector>: <what>`; raises ImportError without Playwright.
    `source` is the header's source line, as serve --source would set it."""
    from playwright.sync_api import sync_playwright

    sizes = sizes or SIZES
    problems = []
    if out:
        out.mkdir(parents=True, exist_ok=True)
    with _Served(spec, source) as base, sync_playwright() as p:
        browser = p.chromium.launch(ignore_default_args=["--hide-scrollbars"])    # draw them, as a reader sees
        try:
            for mode, s in sizes.items():
                ctx = browser.new_context(viewport={"width": s["width"], "height": s["height"]},
                                          device_scale_factor=s["scale"], color_scheme="light",
                                          reduced_motion="reduce")
                page = ctx.new_page()
                for name, path, i in routes(spec):
                    page.goto(base + path, wait_until="load")
                    page.evaluate(SETTLE, [i, mode == "phone"])
                    found = page.evaluate(PROBE, [i, mode]) + page.evaluate(READ_PROBE, [i, mode, *LIMITS])
                    for kind, sel, msg in found:
                        problems.append(f"{kind} {path} {s['width']} {sel}: {msg}")
                    if out:
                        shot = out / shot_name(mode, name)
                        if mode == "phone":
                            page.add_style_tag(content=PHONE_SHOT_CSS)
                            page.screenshot(path=str(shot), full_page=True, clip=page.evaluate(SLIDE_BOX, i))
                        else:
                            page.screenshot(path=str(shot))
                ctx.close()
        finally:
            browser.close()
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="decision_deck_check.py", description=HELP,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True, help="the round's spec JSON (the file decision_deck.py serve takes)")
    ap.add_argument("--out", help="folder for one PNG per route and width (made if missing), with its PNG manifest; "
                                  "a later run into it prints the PNGS line")
    ap.add_argument("--no-link-probe", action="store_true", help="do not fetch the spec's URLs (offline runs)")
    ap.add_argument("--source", metavar="TEXT", default="",
                    help="the header's source line to render with, as serve --source would set it (default: none)")
    args = ap.parse_args(argv)
    try:
        before = stamp.digest(load_spec(args.spec))     # the inputs just before the load the checks use
        spec = load_spec(args.spec)
        checked = stamp.digest(spec)                    # and right after it; the stamp is only for these bytes
    except SpecError as exc:
        sys.stderr.write(f"decision_deck_check: {exc}\n")
        return 2
    except OSError as exc:
        sys.stderr.write(f"decision_deck_check: {exc.strerror or exc}: {exc.filename or ''}\n")
        return 2
    if before != checked:               # an edit around the load: the loaded bytes may not be the hashed ones
        sys.stderr.write(f"decision_deck_check: {stamp.CHANGED}\n")
        return 2
    try:
        from playwright.sync_api import Error as PlaywrightError
    except ImportError:
        sys.stderr.write("decision_deck_check: Python Playwright is not installed. Install it with\n"
                         "  python3 -m pip install playwright\n"
                         "  python3 -m playwright install chromium\n")
        return 2
    found, warnings = spec_lines(spec, links=not args.no_link_probe)
    out = Path(args.out).expanduser() if args.out else None
    try:
        problems = found + check(spec, out, source=args.source)
        changed = pngs.report(out, shot_names(spec)) if out else None     # never a problem; None on a first run
    except PlaywrightError as exc:      # no Chromium, a launch or page failure: say so, not a traceback
        first = (str(exc).strip().splitlines() or [type(exc).__name__])[0]
        sys.stderr.write(f"decision_deck_check: the headless Chromium run failed: {first}\n"
                         "  (no browser? python3 -m playwright install chromium)\n")
        return 2
    except OSError as exc:              # an --out path that is a file or unwritable, a socket that will not bind
        sys.stderr.write(f"decision_deck_check: {exc.strerror or exc}: {exc.filename or args.out or ''}\n")
        return 2
    try:
        if not problems:                # the stamp serve reads (decision_deck_stamp.py); it prints nothing
            stamp.write_stamp(spec, checked)
    except stamp.InputsChanged as exc:
        sys.stderr.write(f"decision_deck_check: {exc}\n")
        return 2
    except OSError as exc:              # the stamp could not be written
        sys.stderr.write(f"decision_deck_check: {exc.strerror or exc}: {exc.filename or ''}\n")
        return 2
    for line in warnings + problems:
        print(line)
    if changed:
        print(changed)
    n, where = len(routes(spec)), " and ".join(f"{s['width']}x{s['height']}" for s in SIZES.values())
    if problems:
        print(f"PROBLEMS {len(problems)} in {n} routes at {where}")
        return 1
    print(f"CLEAN {n} routes at {where}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
