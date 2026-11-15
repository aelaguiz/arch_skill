"""The check's VIDEO rule: every clip of a video decision loads and plays in the browser, at both widths.

A deck with a video decision is checked in the installed Google Chrome (Playwright channel "chrome"), not
Playwright's own Chromium, which plays no H.264 or AAC: the check then sees the clips as the owner's browser does, and
its PNGs show each clip's first frame. The browser starts with its sound muted (--mute-audio, so a check never plays a
sound on the machine) and allowed to start a clip from script (--autoplay-policy=no-user-gesture-required: the page
itself never starts one; the check presses play as the owner would). On each video slide, after the other rules have
read it and its PNG is taken, each clip in turn is shown (its tab clicked, on the desktop) and play() called on it:
within PLAY_S seconds its readyState must reach 3 (HAVE_FUTURE_DATA) or more with no error and currentTime past where
it started (the src starts at the #t=0.001 first-frame fragment, so 0 alone proves nothing). A clip that fails is one
`VIDEO <route> <width> <decision> clip <n> "<label>" (<file>): ...` line naming the reason; then the clip is paused,
put back where it started and the slide's first tab shown again.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_spec import evidence_of  # noqa: E402
from decision_deck_video import has_video  # noqa: E402

CHANNEL = "chrome"
LAUNCH_ARGS = ["--autoplay-policy=no-user-gesture-required", "--mute-audio"]
PLAY_S = 10
ADVANCE_S = 0.05            # currentTime must pass its start by this much: the clip really played
NO_CHROME = ("a deck with a video decision is checked in the installed Google Chrome (Playwright's own Chromium "
             "plays no H.264 or AAC): install Google Chrome, then run the check again")

HELP = """  VIDEO     (a deck with a video decision) a clip that does not play: shown and played in the installed Google
            Chrome at each width, its readyState must reach 3 with no error and its time move past where it
            started within 10 s. The line names the decision, the clip's number, label and file, and the reason
"""

# The SETTLE step's wait for a video slide's shown clips: their first frame is in (or they failed), or 5 s have passed.
SETTLE_CLIPS = r"""
async (i) => {
  const slide = document.getElementById('sl-' + i);
  const clips = slide ? [...slide.querySelectorAll('video')].filter((v) => v.offsetWidth > 0) : [];
  await Promise.all(clips.map((v) => new Promise((r) => { const t0 = Date.now(); (function wait() {
    if (v.readyState >= 2 || v.error || Date.now() - t0 > 5000) r(); else setTimeout(wait, 50); })(); })));
}
"""

# [slide index, wait ms, advance s] -> one result per clip on the slide, in clip order.
PROBE = r"""
async ([i, waitMs, advance]) => {
  const slide = document.getElementById('sl-' + i); if (!slide) return [];
  const first = slide.querySelector('[data-clip][aria-pressed="true"]'), out = [];
  for (const v of slide.querySelectorAll('video[data-clip-video]')) {
    const spec = v.dataset.clipVideo, tab = slide.querySelector('[data-clip="' + spec + '"]');
    if (tab && tab.getBoundingClientRect().width > 0) tab.click();
    const t0 = v.currentTime, end = Date.now() + waitMs; let refused = null, settled = false;
    // the deadline covers play() itself: a clip whose play() never settles must not hold the check
    const playing = (async () => { try { await v.play(); } catch (x) { refused = (x && x.name) || String(x); }
                                   settled = true; })();
    await Promise.race([playing, new Promise((r) => setTimeout(r, waitMs))]);
    while (Date.now() < end && !v.error && !refused && !(v.readyState >= 3 && v.currentTime > t0 + advance))
      await new Promise((r) => setTimeout(r, 50));
    out.push({ spec: spec, readyState: v.readyState, currentTime: v.currentTime, start: t0, refused: refused,
               settled: settled, error: v.error ? v.error.code + (v.error.message ? ' ' + v.error.message : '') : null });
    try { v.pause(); } catch (x) { /* nothing to stop */ }
    try { v.currentTime = t0; } catch (x) { /* a clip that never loaded has no time to set */ }
  }
  if (first) first.click();
  return out;
}
"""


def launch_options(spec: dict) -> dict:
    """The browser launch options for this deck: Chrome with its sound muted for a video deck, else none."""
    return {"channel": CHANNEL, "args": list(LAUNCH_ARGS)} if has_video(spec) else {}


def why_not(r: dict) -> str:
    """'' when the clip played, else why not, in words."""
    if r["error"]:
        return f"the browser could not load it (media error {r['error']})"
    if r["refused"]:
        return f"play() was refused ({r['refused']})"
    if not r.get("settled", True):
        return f"play() did not settle within {PLAY_S} s"
    if r["readyState"] < 3:
        return f"it never had enough data to play (readyState {r['readyState']} after {PLAY_S} s)"
    if r["currentTime"] <= r["start"] + ADVANCE_S:
        return f"its time did not move after play() ({r['currentTime']:.3f} s after {PLAY_S} s)"
    return ""


def settle(page, spec: dict, i: int) -> None:
    """Wait for slide i's shown clips to draw their first frame, when it is a video decision's slide."""
    if 1 <= i <= len(spec["decisions"]) and evidence_of(spec["decisions"][i - 1])["kind"] == "video":
        page.evaluate(SETTLE_CLIPS, i)


def lines(page, spec: dict, i: int, path: str, width: int) -> list[str]:
    """VIDEO lines for slide i (decision i of the spec) at this width; none for a slide that is no video decision."""
    if not 1 <= i <= len(spec["decisions"]):
        return []
    dec = spec["decisions"][i - 1]
    ev = evidence_of(dec)
    if ev["kind"] != "video":
        return []
    out = []
    for r in page.evaluate(PROBE, [i, PLAY_S * 1000, ADVANCE_S]):
        k = int(r["spec"].rsplit("|", 1)[1])
        why = why_not(r)
        if why:
            clip = ev["clips"][k]
            out.append(f'VIDEO {path} {width} {dec["id"]} clip {k + 1} "{clip["label"]}" ({clip["file"]}): {why}')
    return out
