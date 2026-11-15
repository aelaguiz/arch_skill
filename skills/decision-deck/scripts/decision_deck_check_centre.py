"""The OFFCENTRE check of decision_deck_check.py: a left pane's drawing stuck to the top beside a taller side panel.

PROBE runs in the page with [slide index, "desktop" | "phone", tolerance] and returns [kind, selector, message]
triples like the fit and reading probes, in screen px. For each evidence `.cx` whose `.side` stands beside its left
pane (to its right and overlapping it from top to bottom; a phone stacks the panel under the pane, so there it reads
nothing unless the two columns stand side by side):
  - the drawing is what the pane draws, never its stretched box: inside an SVG its shapes and text, else each
    displayed child's box (a bar grid, its legend, a picture), joined top to bottom;
  - the panel's height is its own content's (title and list), joined the same way;
  - when the panel is taller than the drawing by more than OFFCENTRE_TOL, the drawing's middle must sit within
    OFFCENTRE_TOL of the middle of its column (the `.cx` row the pane and the panel share). A drawing taller than its
    panel is not read: it sets the row's height, or scales down whole, or scrolls in its box.
"""

OFFCENTRE_TOL = 4           # screen px: rounding and the drawing's own margins (a value label above a line's point)

PROBE = r"""
([i, mode, tol]) => {
  const slide = document.getElementById('sl-' + i);
  if (!slide) return [];
  const out = [], px = (n) => Math.round(n) + 'px';
  const name = (el) => {
    const parts = [];
    for (let n = el; n && n !== slide.parentElement; n = n.parentElement) {
      if (n.id) { parts.unshift('#' + n.id); break; }
      const cls = [...n.classList].filter((c) => c !== 'current').slice(0, 2).map((c) => '.' + c).join('');
      parts.unshift(n.tagName.toLowerCase() + cls);
    }
    return parts.join(' > ');
  };
  const shown = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const span = (els) => { let top = Infinity, bottom = -Infinity;
    for (const el of els) { const r = el.getBoundingClientRect();
      if (r.width > 0 || r.height > 0) { top = Math.min(top, r.top); bottom = Math.max(bottom, r.bottom); } }
    return top < bottom ? { top, bottom, height: bottom - top } : null; };
  const SHAPES = 'rect, text, line, polyline, polygon, path, circle, ellipse, image';
  const drawing = (pane) => span([...pane.children].filter(shown).flatMap((c) =>
    c instanceof SVGSVGElement ? [...c.querySelectorAll(SHAPES)].filter(shown) : [c]));
  for (const cx of slide.querySelectorAll('.cx')) {
    const side = cx.querySelector(':scope > .side'), pane = cx.firstElementChild;
    if (!side || !pane || pane === side || !shown(side) || !shown(pane)) continue;
    const s = side.getBoundingClientRect(), p = pane.getBoundingClientRect();
    if (s.left < p.right - 1 || s.top >= p.bottom || s.bottom <= p.top) continue;    // stacked: not beside it
    const d = drawing(pane), panel = span([...side.children].filter(shown));
    if (!d || !panel || panel.height - d.height <= tol) continue;
    const col = cx.getBoundingClientRect(), off = (d.top + d.bottom) / 2 - (col.top + col.bottom) / 2;
    if (Math.abs(off) > tol) {
      out.push(['OFFCENTRE', name(pane), "the left pane's drawing is " + px(d.height) + ' tall beside a ' +
                px(panel.height) + ' side panel and sits ' + px(Math.abs(off)) + (off < 0 ? ' above' : ' below') +
                ' the middle of its column; centre it vertically']);
    }
  }
  return out;
}
"""
