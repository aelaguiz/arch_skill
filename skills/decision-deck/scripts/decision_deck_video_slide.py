"""Decision deck "video" evidence, the slide: one player with a tab per clip, its look and its script.

Each clip is one <video controls playsinline preload="metadata"> with no autoplay, loop or muted, so it plays only
when the owner presses play, with its sound. Its src ends in the media fragment #t=0.001, so iPhone Safari draws the
first frame before play (it shows a blank box for preload="metadata" otherwise); other browsers start at 1 ms, which
no one sees.

Desktop: the evidence zone holds the tab row (a tab per clip in spec order when there are two or more, then the shown
clip's caption) over the player, a fixed 16:9 box as tall as the zone (at most its width), the clip drawn whole inside
it on black. The box is sized by the slide, never by the clip, so nothing moves or resizes while a clip loads. The
recommended option's clip shows first. A tab, or V, shows another clip and pauses the one it hides; it never answers.
Leaving the slide pauses its clips, and keys pressed on a focused player stay with the player. Phone: every clip on the page, one per row at full width, each under its label
with its caption under it; the tab row is hidden.

with_video() joins VIDEO_JS and its click, key and slide-change lines into the page script, and deck_page adds
VIDEO_CSS and VIDEO_KEY, only for a deck with a video decision, so every other deck's page stays byte for byte as it
was; each anchor must occur exactly once, so a moved line fails loudly rather than drifting.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_inline import e, linked  # noqa: E402
from decision_deck_video import rel_of, routes_of, snapshot  # noqa: E402

FIRST_FRAME = "#t=0.001"
VIDEO_KEY = ("<kbd>V</kbd>", "Video clips: the next clip")


def clip_urls(spec: dict) -> dict[str, str]:
    """{clip path: /clip/<sha16>.<ext>} read from disk now: for a page rendered without a server (tests); the server
    passes its own, from the bytes it serves."""
    return routes_of(snapshot(spec))[0]


def video_html(did: str, ev: dict, urls: dict) -> str:
    """The evidence zone of a video decision (decision_deck_render.decision_slide): the tab row and shown caption,
    then the frame holding every clip (all but the shown one hidden on the desktop)."""
    shown, many = ev["start"], len(ev["clips"]) > 1
    figs, tabs, caps = [], [], []
    for k, clip in enumerate(ev["clips"]):
        on = k == shown
        src = urls[rel_of(clip["file"])] + FIRST_FRAME
        lab, cap = e(clip["label"]), linked(clip["caption"]) if clip["caption"] else ""
        under = f'<figcaption class="vcap">{cap}</figcaption>' if cap else ""
        figs.append(f'<figure class="vclip" data-clip-k="{k}"{" data-on" if on else ""}><p class="vlab">{lab}</p>'
                    f'<div class="vbox"><video controls playsinline preload="metadata" src="{e(src)}" '
                    f'aria-label="Clip: {lab}" data-clip-video="{e(did)}|{k}"></video></div>'
                    f'{under}</figure>')
        if many:
            tabs.append(f'<button type="button" data-clip="{e(did)}|{k}" aria-pressed="{"true" if on else "false"}" '
                        f'title="{lab}">{lab}</button>')
        caps.append(f'<span data-clip-cap="{e(did)}|{k}"{"" if on else " hidden"}>{cap}</span>')
    seg = (f'<div class="seg" role="group" aria-label="Clips">{"".join(tabs)}</div> <kbd title="Next clip">V</kbd>'
           if many else "")
    row = f'<div class="ev-tools vtools">{seg}{"".join(caps)}</div>' if many or ev["clips"][0]["caption"] else ""
    return f'<div class="ev vid" data-video="{e(did)}">{row}<div class="vframe">{"".join(figs)}</div></div>'


VIDEO_CSS = r"""
.vframe { flex: 1 1 auto; min-height: 0; position: relative; }
.vclip { margin: 0; }
.vbox { position: relative; background: #000; }
.vbox video { position: absolute; inset: 0; display: block; width: 100%; height: 100%; object-fit: contain; background: #000; }
.vlab { margin: 0 0 4px; font-size: var(--t-note); line-height: var(--t-note-lh); font-weight: 700; color: var(--ink); }
.vcap { margin: 6px 0 0; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.ev-tools.vtools > span { white-space: normal; overflow: visible; }
@media (min-width: 900px) and (orientation: landscape) {
  .vclip { position: absolute; inset: 0; }
  .vclip:not([data-on]) { display: none; }
  .vbox { height: 100%; max-width: 100%; aspect-ratio: 16 / 9; }
  .vlab, .vcap { display: none; }
}
@media (max-width: 899px), (orientation: portrait) {
  .vtools { display: none; }
  .vframe { flex: none; }
  .vbox { width: 100%; aspect-ratio: 16 / 9; }
  .vclip + .vclip { margin-top: 14px; }
}
"""

VIDEO_JS = r"""
  // ---------- video: one player, a tab per clip; nothing plays by itself ----------
  function clipTab(spec) {
    const [id, k] = spec.split('|'), zone = $('[data-video="' + id + '"]'); if (!zone) return;
    $$('[data-clip]', zone).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.clip === spec)));
    $$('[data-clip-cap]', zone).forEach((p) => { p.hidden = p.dataset.clipCap !== spec; });
    $$('.vclip', zone).forEach((f) => {
      if (f.dataset.clipK === k) { f.dataset.on = ''; return; }
      delete f.dataset.on; const v = $('video', f); if (v && !v.paused) v.pause();
    });
    const b = $('[data-clip="' + spec + '"]', zone); if (b) live('Showing ' + b.title);
  }
  function clipNext(id) {
    const zone = $('[data-video="' + id + '"]'), tabs = zone ? $$('[data-clip]', zone) : []; if (!tabs.length) return;
    const k = tabs.findIndex((b) => b.getAttribute('aria-pressed') === 'true');
    clipTab(tabs[(k + 1) % tabs.length].dataset.clip);
  }
"""

# Declared as a function so mark() may call it before the events part of the script has run.
QUIET_JS = r"""
  function clipsQuiet(i) { $$('.slide video').forEach((v) => { if (!v.paused && !v.closest('#sl-' + i)) v.pause(); }); }
"""

PATCHES = [
    ("  // ---------- events ----------\n", VIDEO_JS + QUIET_JS + "\n  // ---------- events ----------\n"),
    ("    if (d.zoom) { zoom(d.zoom); return; }\n",
     "    if (d.zoom) { zoom(d.zoom); return; }\n    if (d.clip) { clipTab(d.clip); return; }\n"),
    ("    if (it.kind === 'images') {\n      if (low === 'f')",
     "    if (it.kind === 'video' && low === 'v') { e.preventDefault(); clipNext(it.id); return; }\n"
     "    if (it.kind === 'images') {\n      if (low === 'f')"),
    ("    route(i);\n", "    route(i);\n    clipsQuiet(i);\n"),     # in mark(): every way a slide stops being current
    ("    if (tg.tagName === 'TEXTAREA' || tg.tagName === 'INPUT' ||",       # a focused player keeps its own keys
     "    if (tg.tagName === 'VIDEO') return;\n    if (tg.tagName === 'TEXTAREA' || tg.tagName === 'INPUT' ||"),
]


def with_video(script: str) -> str:
    """The page script with the video script and its click, key and slide-change lines joined in; RuntimeError unless
    each anchor occurs exactly once."""
    for old, new in PATCHES:
        if script.count(old) != 1:
            raise RuntimeError(f"decision_deck_video_slide: expected one {old!r} in the page script, found "
                               f"{script.count(old)}")
        script = script.replace(old, new)
    return script
