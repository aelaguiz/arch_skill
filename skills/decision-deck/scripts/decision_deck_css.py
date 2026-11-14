"""Decision deck CSS: the page's design tokens and every style rule, as one <style> body (page_css).

Stage: 16:9, 720 x 405 pt drawn at 960 x 540 px and scaled to the window; type roles title 20 pt, body 11, note 9,
source 7, cover 28; 36 / 24 / 22 pt margins; a rule under the one-line title; the callout bar carries the why. Accent =
structure; --data-1 = the one emphasised mark; --data-muted = every other mark, always with a direct label. Light only.
Fit rule: the answer row is always fully visible, answers wrap inside their own buttons, and evidence that does not fit
scrolls inside one bounded box with no fade (on the stage the diff's panel and redline share one scroll box; on phones
the page scrolls and the evidence has no inner scroll box). decision_deck_check.py checks a rendered round against it.
The parts, in the order page_css joins them: TOKENS (colours and the type stack), CSS (the desktop stage, kept in
decision_deck_css_stage.py and imported here), PHONE_CSS (phones and portrait screens stack the slides unscaled, and the reduced-motion rule), DIALOG_CSS (Zoom and Keys),
HEADER_CSS (the header's source line and links), STEADY_CSS (nothing moves when an answer lands), CHART_CSS (the
grid bar chart and the line chart of decision_deck_chart.py) and CENTRE_CSS (a chart beside a taller side panel).
"""

from decision_deck_css_stage import CSS  # the desktop stage; page_css joins it second

TOKENS = """:root { --accent: #007439; --accent-text: #007439; --accent-tint: #e6f4ea; --accent-rule: #007439;
  --data-1: #007439; --data-muted: #b7bcc4; --ink: #1f2937; --ink-2: #3d424a; --rule: #e3e5e9; --panel: #f5f6f8;
  --paper: #fff; --ground: #e9ebee; color-scheme: light;
  --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }"""


# ------------------------------------------------------------------ phones and portrait screens

PHONE_CSS = r"""@media (max-width: 899px), (orientation: portrait) {
  :root { --t-cover: 28px; --t-cover-lh: 34px; --t-title: 21px; --t-title-lh: 27px; --t-kicker: 12px; --t-lead: 17px; --t-lead-lh: 24px;
    --t-body: 15px; --t-body-lh: 21px; --t-note: 13px; --t-note-lh: 18px; --t-fine: 12px; --t-source: 12px; --t-tag: 11px;
    --m-l: 16px; --m-r: 16px; --m-t: 20px; --m-b: 14px; --bar-h: 84px; }
  html { scroll-snap-type: y proximity; scroll-padding-top: var(--bar-h); }
  body { padding-top: var(--bar-h); }
  .bar { height: auto; min-height: var(--bar-h); flex-wrap: wrap; gap: 6px 10px; padding: 8px 16px; }
  .bar .round { flex: 1; white-space: normal; }
  .ev-tools > span:last-child { white-space: normal; }
  .dots { order: 5; margin-left: 0; width: 100%; flex-wrap: wrap; gap: 2px; padding: 0; position: relative;
    max-height: 82px; overflow-y: auto; }   /* at most two rows; a longer deck scrolls its dots inside the bar */
  .dot { position: relative; width: 36px; height: 40px; border-radius: 0; }   /* a finger-sized target, same icon */
  .dot[aria-current="true"] { box-shadow: none; }
  .dot[aria-current="true"]::after { content: ""; position: absolute; left: 50%; top: 50%; width: 26px; height: 26px; margin: -13px 0 0 -13px;
    border-radius: 50%; box-shadow: 0 0 0 2px var(--ink); pointer-events: none; }   /* the desktop ring, drawn round the icon */
  .bar .help { display: none; }
  .deck { position: static; overflow: visible; }
  .stage { position: static; width: auto; height: auto; transform: none; }
  .nav-arrow { display: none; }
  .slide { position: relative; display: flex; min-height: calc(100svh - var(--bar-h)); margin: 0 0 10px; box-shadow: none; scroll-snap-align: start; }
  .title { white-space: normal; }
  .chart svg.wide { display: none; }
  .chart svg.narrow { display: block; height: auto; }
  .ev { flex: none; }                     /* evidence is as tall as it is; spare slide goes above the answers */
  .grow { flex: 1 1 0; }
  .pair { display: block; }
  .pcol + .pcol { margin-top: 14px; }
  .pbox { position: static; }
  .pic { position: static; height: auto; }
  .pic img { max-height: none; }
  .ev > .tx, .cx { display: block; overflow: visible; padding: 0; border: 0; border-radius: 0; }
  .panel { margin-bottom: 10px; }
  .ev-tools { flex-wrap: wrap; }
  .rec { display: block; }
  .side { margin-top: 16px; }
  .dock { grid-template-columns: 1fr; }
  .choices { display: flex; flex-wrap: wrap; }
  .item .choices { flex-direction: column; flex-wrap: nowrap; }
  .choice { flex: none; width: 100%; min-width: 0; height: auto; min-height: 44px; padding: 6px 10px; white-space: normal; }
  .choice kbd, .seg kbd, .btn kbd, .ev-tools kbd { display: none; }
  .tbl { overflow: visible; }
  .sumtbl th, .sumtbl td { overflow-wrap: break-word; }
  .src, .phead { white-space: normal; }
  .ctx { max-height: calc(3 * var(--t-note-lh)); }
  .ctxrow { align-items: flex-end; }       /* the ellipsis and Read all sit on the third line (same line height) */
  .more { line-height: var(--t-note-lh); }
  .ctx.open { max-height: none; }
  .keyhint { display: none; }             /* a phone has no keys to list */
  .cover h2 { max-width: none; }
  .cover .bar6 { display: none; }
  .cover-s .how, .cover-s .start { margin-left: 0; }
  .cover-s .how { text-wrap: pretty; }     /* no last line of one word */
  .sumtbl td.c { max-width: none; }
}
@media (prefers-reduced-motion: reduce) { .choice.flash, .adv i { animation: none; } .adv i { transform: scaleX(1); } html { scroll-behavior: auto; } }

@media (max-width: 899px), (orientation: portrait) {
  .dtbl.cards, .dtbl.cards tbody, .dtbl.cards tr, .dtbl.cards td { display: block; width: auto; }
  .dtbl.cards thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  .dtbl.cards tr { margin: 0 0 10px; padding: 10px 12px; border: 1px solid var(--rule); border-radius: 4px; }
  .dtbl.cards td { padding: 0; border: 0; text-align: left; }
  .dtbl.cards td:first-child { margin: 0 0 6px; font-weight: 700; }
  .dtbl.cards td + td { margin: 6px 0 0; }
  .dtbl.cards .num + :not(.num) { padding-left: 0; }
  .dtbl:not(.cards) td { overflow-wrap: anywhere; }
  .dtbl:not(.cards) th { overflow-wrap: normal; }      /* a heading wraps between words, never inside one */
  .dtbl:not(.cards) th:last-child, .dtbl:not(.cards) td:last-child { padding-right: 0; }
  .dtbl.cards td + td::before { content: attr(data-label) / ""; display: block; font-size: var(--t-note); line-height: var(--t-note-lh);
    font-weight: 700; color: var(--accent-text); text-transform: uppercase; letter-spacing: .06em; }
  .ev > .tx::after { display: none; }      /* the box does not scroll here; a sticky strip would pin to the screen */
  .closing .dock { grid-template-columns: minmax(0, 1fr); }
  .closing .choices .btn { width: 100%; justify-content: center; }
}
"""


# ------------------------------------------------------------------ the Zoom and Keys dialogs

DIALOG_CSS = r"""
dialog { border: 1px solid var(--rule); border-radius: 8px; padding: 0; color: var(--ink); background: var(--paper);
  box-shadow: 0 20px 60px rgba(17, 19, 24, .22); max-width: calc(100vw - 32px); }
dialog::backdrop { background: rgba(17, 19, 24, .5); }
.dlg-h { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-bottom: 1px solid var(--rule); font-size: 14px; }
.dlg-h h2 { margin: 0; font-size: 15px; line-height: 22px; font-weight: 700; flex: 1; min-width: 0; }
.dlg-b { padding: 14px 16px; max-height: calc(100vh - 140px); overflow: auto; background: var(--panel); font-size: 14px; line-height: 20px; }
#zoom img { display: block; max-width: none; border: 1px solid var(--rule); background: var(--paper); }
#zoom img.close { image-rendering: pixelated; }
#help .dlg-b { background: var(--paper); }
.keys { border-collapse: collapse; }
.keys td { padding: 5px 14px 5px 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
"""


# ------------------------------------------------------------------ the header's source line and links

HEADER_CSS = r"""
.bar .who { min-width: 0; display: flex; flex-direction: column; }
.bar .from { min-width: 0; font-size: 12px; line-height: 16px; color: var(--ink-2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
:root { --link: #1f5fa8; }   /* link blue, 6.5:1 on white: a link never looks like added (<ins>) text */
a[href] { color: var(--link); text-decoration: underline; text-underline-offset: 2px; overflow-wrap: anywhere; }
a[href]:hover { text-decoration-thickness: 2px; }
.choice[aria-pressed="true"] a[href] { color: inherit; }
ins a[href], del a[href] { color: inherit; }
@media (max-width: 899px), (orientation: portrait) {
  html { scroll-padding-top: var(--bar-live, var(--bar-h)); }
  body { padding-top: var(--bar-live, var(--bar-h)); }
  .bar .who { flex: 1 1 0; }
  .bar .from { white-space: normal; }
  .slide { min-height: calc(100svh - var(--bar-live, var(--bar-h))); }
}
"""


# ------------------------------------------------------------------ steady answers
# Nothing on a decision slide moves when an answer or a status lands. The status line under the answers is one note
# line from the start (longer text is cut with an ellipsis and opens whole in an overlay, decision_deck_steady_js.py);
# each answer's tick has its slot from the start and is drawn, not typed. On the desktop the band's 22 px come back
# from the chrome around the evidence (BAND_*), not from the evidence. Flip's "Flip to X" button lays every label in
# one grid cell, so a click neither moves nor resizes it.

TICK_W = "13px"         # the tick's slot: the tick's own width
TICK_PULL = "-4px"      # the slot takes this much of the gap after the key cap, so a button widens by 9 px
BAND_GAP = "6px"        # the dock's row gap (decision_deck_css_stage.py .dock), cancelled above the status line
BAND_TOP = "8px"        # off the slide's top margin (--m-t, 32 px)
BAND_DOCK = "2px"       # off the dock's top margin and off its top padding (8 px each)
BAND_FOOT = "4px"       # off the slide's bottom margin (--m-b, 10 px): 6 + 8 + 2 + 2 + 4 = the band's 22 px

STEADY_CSS = r"""
.item .status, .item .status:empty { display: block; height: var(--t-note-lh); min-height: 0; margin: 0; overflow: hidden;
  white-space: nowrap; text-overflow: ellipsis; }
.item .status > * { margin-right: 14px; vertical-align: top; }
.item .status.cut { cursor: pointer; }
.item .dock { position: relative; }
.status-full { position: absolute; z-index: 5; left: 0; right: 0; margin: 0; padding: 8px 10px; background: var(--paper);
  border: 1px solid var(--ink-2); border-radius: 4px; box-shadow: 0 6px 18px rgba(17, 19, 24, .16);
  font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); white-space: normal; overflow-wrap: anywhere;
  max-height: 50vh; overflow-y: auto; }
.status-full[hidden] { display: none; }
.status-full > * { margin-right: 14px; }
.choice .tx { position: relative; padding-left: TICK_W; margin-left: TICK_PULL; }
@media (max-width: 899px), (orientation: portrait) { .choice .tx { margin-left: 0; } }   /* no key cap there */
.choice[aria-pressed="true"] .tx::before { content: "✓" / ""; position: absolute; left: 0; top: 0;
  font-size: var(--t-body); line-height: 18px; font-weight: 700; }
@media (min-width: 900px) and (orientation: landscape) {
  .dtbl.steady th + th, .dtbl.steady td + td { padding-left: 10px; border-left: 1px solid color-mix(in srgb, var(--rule) 60%, var(--paper)); }
}
@media (min-width: 900px) and (orientation: landscape) {
  .slide.item { padding-top: calc(var(--m-t) - BAND_TOP); padding-bottom: calc(var(--m-b) - BAND_FOOT); }
  .slide.item .dock { margin-top: calc(8px - BAND_DOCK); padding-top: calc(8px - BAND_DOCK); }
  .slide.item .dock > .status { margin-top: calc(0px - BAND_GAP); }
}
.phead.flip { display: flex; align-items: flex-start; gap: 0 12px; }
.phead.flip .pcap { flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.flipto { flex: none; display: inline-grid; justify-items: end; white-space: nowrap; }
.flipto > span { grid-area: 1 / 1; }
.flipto > .off { visibility: hidden; }
""".replace("TICK_W", TICK_W).replace("TICK_PULL", TICK_PULL).replace("BAND_GAP", BAND_GAP).replace(
    "BAND_TOP", BAND_TOP).replace("BAND_DOCK", BAND_DOCK).replace("BAND_FOOT", BAND_FOOT)


# ------------------------------------------------------------------ the grid bar chart and the line chart
# Bars as an HTML grid, one row per bar (label up to 45% wide and wrapping past it, the bar's track, values right-
# aligned in one column, a note column when any bar has a note); its text is the deck's own size, never under 11
# screen px. On a phone each label and note take a full line. A line chart is an SVG drawn at its column's width.

CHART_CSS = r"""
.chart.tbl { overscroll-behavior: contain; }
.hleg { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 6px; margin: 0 0 8px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.hleg .k { display: inline-block; width: 12px; height: 12px; }
.hleg span + .k { margin-left: 10px; }
.hleg .k.s0 { background: var(--data-muted); } .hleg .k.s1 { background: var(--data-1); }
.hb { display: grid; grid-template-columns: fit-content(45%) minmax(80px, 1fr) max-content; gap: 8px 12px; align-items: center; }
.hb.notes { grid-template-columns: fit-content(45%) minmax(80px, 1fr) max-content minmax(0, 1.6fr); }
.hb .r { display: grid; grid-column: 1 / -1; grid-template-columns: subgrid; align-items: center; }
.hb .hl { font-size: var(--t-body); line-height: 18px; font-weight: 600; overflow-wrap: break-word; min-width: 0; }
.hb .track { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.hb .b { display: block; height: 16px; background: var(--data-muted); }
.hb .b.em, .hb .b.s1 { background: var(--data-1); }
.hb.two .b { height: 14px; }
.hb .hv { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; font-size: var(--t-note); line-height: 16px; font-weight: 600;
  font-variant-numeric: tabular-nums; white-space: nowrap; }
.hb.two .hv { line-height: 14px; }       /* each value level with its own bar */
.hb .hn { font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); min-width: 0; }
.chart.lc svg { height: auto; }
.chart.lc text { font-size: 12px; font-variant-numeric: tabular-nums; }
.chart.lc .pv, .chart.lc .lg { font-weight: 600; }
.chart.lc .xl { fill: var(--ink-2); }
.chart.lc .ax { stroke: var(--rule); stroke-width: 1; }
.chart.lc .ln { fill: none; stroke-width: 2.5; stroke-linejoin: round; stroke-linecap: round; }
.chart.lc .ln.s0 { stroke: var(--data-muted); } .chart.lc .ln.s1 { stroke: var(--data-1); }
.chart.lc .pt.s0, .chart.lc .k.s0 { fill: var(--data-muted); } .chart.lc .pt.s1, .chart.lc .k.s1 { fill: var(--data-1); }
@media (max-width: 899px), (orientation: portrait) {
  .hb, .hb.notes { grid-template-columns: minmax(0, 1fr) max-content; row-gap: 12px; }
  .hb .r { row-gap: 4px; }
  .hb .hl, .hb .hn { grid-column: 1 / -1; }
}
"""

# ------------------------------------------------------------------ a chart beside a taller side panel
# On the stage the chart's drawing sits in the middle of its column, level with the panel, not at the column's top.
# The chart becomes a column flexbox centring its drawing (`safe`, so a drawing taller than its box starts at the top
# and scrolls as before); the SVG bars take their own height, capped at the chart's, so a chart taller than its zone
# still scales down whole. A chart as tall as the row, a slide with no panel (.cx.one) and a phone draw as before.
# decision_deck_check_centre.py (OFFCENTRE) checks it.

CENTRE_CSS = r"""
@media (min-width: 900px) and (orientation: landscape) {
  .cx:not(.one) > .chart { display: flex; flex-direction: column; justify-content: safe center; }
  .cx:not(.one) > .chart > * { flex: none; }
  .cx:not(.one) > .chart:not(.tbl) > svg { height: auto; max-height: 100%; }
}
"""


def page_css() -> str:
    """The whole <style> body for a deck page."""
    return "\n".join((TOKENS, CSS, PHONE_CSS, DIALOG_CSS, HEADER_CSS, STEADY_CSS, CHART_CSS, CENTRE_CSS))
