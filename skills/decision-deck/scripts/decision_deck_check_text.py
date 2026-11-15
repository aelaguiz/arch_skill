"""Reading checks for decision_deck_check.py: what a reviewer otherwise has to catch by eye on the rendered slides.

READ_PROBE runs in the page after the fit probe, with [slide index, "desktop" | "phone"], and returns
[kind, selector, message] triples; decision_deck_check.HELP describes each kind for the caller:
  MIDWORD  text cut inside a word, by a fold button or by an ellipsis or line clamp
  MARKUP   Markdown markers showing as typed (`**`, a backtick pair, `[text](target)`, a `#` heading line)
  LEGEND   the redline's legend names a mark the redline does not have
  GAP      empty slide between the evidence and the line under it (a desktop picture fills its box: not read)
  SMALL    chart text drawn under SMALL_PX screen px
  KEYS     phone: a keyboard hint showing
  TALL     phone: a slide more than TALL_SCREENS screens tall, so its answers are that far down
  BROKEN   a command flag split after its hyphen at a line end
The header bar is read with the cover (slide 0), once per width. Each kind is one a deterministic check can find, so
a review of the PNGs is left with what only an eye can judge.
"""

GAP_PX = 24                 # CSS px of the unscaled slide
TALL_SCREENS = 2.5
SMALL_PX = 11               # screen px; the deck's own smallest text (a note line) is larger on both sizes
LIMITS = [GAP_PX, TALL_SCREENS, SMALL_PX]

READ_PROBE = r"""
([i, mode, GAP_PX, TALL_SCREENS, SMALL_PX]) => {
  const out = [], slide = document.getElementById('sl-' + i);
  if (!slide) return out;
  const px = (n) => Math.round(n) + 'px';
  const name = (el) => {
    const parts = [];
    for (let n = el; n && n !== document.body; n = n.parentElement) {
      if (n.id) { parts.unshift('#' + n.id); break; }
      const cls = [...n.classList].filter((c) => c !== 'current').slice(0, 2).map((c) => '.' + c).join('');
      parts.unshift(n.tagName.toLowerCase() + cls);
    }
    return parts.join(' > ');
  };
  const shown = (el) => { const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && (el.offsetWidth === undefined || (el.offsetWidth > 1 && el.offsetHeight > 1)) && getComputedStyle(el).visibility !== 'hidden'; };
  const said = (t, n) => { t = String(t).replace(/\s+/g, ' ').trim(); return t.length > (n || 60) ? t.slice(0, n || 60) + '…' : t; };
  const roots = i === 0 ? [document.querySelector('header.bar'), slide].filter(Boolean) : [slide];
  const texts = [];
  for (const root of roots) {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const p = n.parentElement;
      if (p && n.textContent.trim() && !p.closest('script, style, textarea, [hidden]') && shown(p)) texts.push(n);
    }
  }
  const once = new Set();
  const add = (kind, el, msg) => { const key = kind + name(el) + msg; if (!once.has(key)) { once.add(key); out.push([kind, name(el), msg]); } };

  // MIDWORD: a fold button between two halves of one word
  for (const b of slide.querySelectorAll('button.fold')) {
    if (!shown(b)) continue;
    const mid = b.nextElementSibling, before = b.previousSibling ? b.previousSibling.textContent : '',
          after = mid && mid.nextSibling ? mid.nextSibling.textContent : '', hid = mid ? mid.textContent : '';
    if (/[A-Za-z0-9]$/.test(before) && /^[A-Za-z0-9]/.test(hid)) add('MIDWORD', b, 'the fold cuts a word: "' + said(before.slice(-14)) + '" | "' + said(hid.slice(0, 14)) + '"');
    if (/[A-Za-z0-9]$/.test(hid) && /^[A-Za-z0-9]/.test(after)) add('MIDWORD', b, 'the fold cuts a word: "' + said(hid.slice(-14)) + '" | "' + said(after.slice(0, 14)) + '"');
  }
  // MIDWORD: an ellipsis (one line) or a line clamp that ends inside a word; the cut is where the ellipsis starts
  for (const root of roots) for (const el of [root, ...root.querySelectorAll('*')]) {
    if (!shown(el) || !document.caretRangeFromPoint) continue;
    const s = getComputedStyle(el), clamp = s.webkitLineClamp && s.webkitLineClamp !== 'none';
    const cutX = s.textOverflow === 'ellipsis' && /hidden|clip/.test(s.overflowX) && el.scrollWidth > el.clientWidth + 1;
    const cutY = clamp && el.scrollHeight > el.clientHeight + 1;
    if (!cutX && !cutY) continue;
    const r = el.getBoundingClientRect(), k = el.offsetWidth ? r.width / el.offsetWidth : 1;
    const em = parseFloat(s.fontSize) * k, lh = (parseFloat(s.lineHeight) || em * 1.3) * k;
    const c = document.caretRangeFromPoint(r.right - parseFloat(s.paddingRight) * k - em, r.bottom - parseFloat(s.paddingBottom) * k - lh / 2);
    if (!c || c.startContainer.nodeType !== 3 || !el.contains(c.startContainer)) continue;
    const t = c.startContainer.textContent, at = c.startOffset;
    if (/\S\S$/.test(t.slice(0, at)) && /^\S\S/.test(t.slice(at)))
      add('MIDWORD', el, 'the text is cut inside a word: "' + said(t.slice(Math.max(0, at - 16), at)) + '…" (' + (cutY ? 'a line clamp' : 'an ellipsis') + ')');
  }
  // MARKUP: Markdown markers showing as typed (code spans are literal by definition)
  for (const n of texts) {
    const p = n.parentElement, t = n.textContent;
    if (p.closest('code, kbd, pre')) continue;
    // a bold pair or an opener at a word's start (not a footnote's "Revenue**"); a heading line (not a count's "# of users")
    const m = /(^|[\s(\[{"'“‘])\*\*[^\s*\/](?:[^*]*[^\s*])?\*\*(?=$|[\s.,;:!?)\]}"'”’])|(^|\s)\*\*[^\s*\/]/.exec(t) || /`[^`\n]+`/.exec(t) || /\[[^\]\n]+\]\([^)\s]+\)/.exec(t) || /(^|\n)(#{2,6} \S|# [A-Z])/.exec(t);
    if (m) add('MARKUP', p, 'Markdown shows as typed: "' + said(t.slice(Math.max(0, m.index - 10), m.index + 30), 44) + '" (the deck formats it only in a diff\'s text and rule panel: write plain words here, and pair or drop the marker there)');
  }
  // LEGEND: the key names a mark the redline lacks
  for (const lg of slide.querySelectorAll('.legend')) {
    if (!shown(lg)) continue;
    for (const [tag, word] of [['del', 'removed'], ['ins', 'added']])
      if (lg.querySelector(tag) && !lg.parentElement.querySelector('.line ' + tag)) add('LEGEND', lg, 'the legend shows "' + word + '" and the redline has no ' + word + ' text');
  }
  // BROKEN: a command flag split after its hyphen
  for (const n of texts) {
    const re = /(^|[\s(\["'“‘])(--?[A-Za-z0-9][\w=./:-]*)/g;
    for (let m = re.exec(n.textContent); m; m = re.exec(n.textContent)) {
      const from = m.index + m[1].length, rg = document.createRange();
      rg.setStart(n, from); rg.setEnd(n, from + m[2].length);
      const tops = [...rg.getClientRects()].filter((q) => q.width > 0).map((q) => Math.round(q.top));
      if (tops.length > 1 && Math.max(...tops) - Math.min(...tops) > 2) add('BROKEN', n.parentElement, 'the flag "' + said(m[2], 30) + '" breaks across two lines');
    }
  }
  // BROKEN: a table heading split inside a word
  for (const n of texts) {
    if (!n.parentElement.closest('th')) continue;
    for (const m of n.textContent.matchAll(/[A-Za-z0-9]+/g)) {
      const rg = document.createRange();
      rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
      const tops = [...rg.getClientRects()].filter((q) => q.width > 0).map((q) => Math.round(q.top));
      if (tops.length > 1 && Math.max(...tops) - Math.min(...tops) > 2) add('BROKEN', n.parentElement, 'the heading "' + said(n.textContent, 30) + '" breaks inside the word "' + m[0] + '"');
    }
  }
  // GAP: evidence, then empty slide before the line under it (a desktop picture fills its box by design: not read)
  const k = slide.offsetWidth ? slide.getBoundingClientRect().width / slide.offsetWidth : 1;
  for (const ev of slide.querySelectorAll(mode === 'desktop' ? '.ev:not([data-ev])' : '.ev')) {
    const parts = [...ev.querySelectorAll('.tx, .tbl, .chart svg, .side, .scrollhint, .pic img')].filter(shown);
    let next = ev.nextElementSibling;
    while (next && !(shown(next) && next.getBoundingClientRect().height > 1)) next = next.nextElementSibling;
    if (!parts.length || !next) continue;
    const gap = (next.getBoundingClientRect().top - Math.max(...parts.map((p) => p.getBoundingClientRect().bottom))) / k;
    if (gap > GAP_PX) add('GAP', ev, px(gap) + ' of empty slide between the evidence and ' + name(next).split(' > ').pop());
  }
  // SMALL: chart text drawn too small to read (an SVG's text shrinks with its column)
  for (const t of slide.querySelectorAll('.chart svg text')) {
    const svg = t.ownerSVGElement, box = svg.viewBox.baseVal;
    if (!shown(svg) || !box || !box.width) continue;
    const on = svg.getBoundingClientRect(), scale = Math.min(on.width / box.width, on.height / box.height);   // it keeps its ratio
    const size = parseFloat(getComputedStyle(t).fontSize) * scale;
    const words = [...t.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('');   // not its <title>
    if (size < SMALL_PX) { add('SMALL', svg, 'the chart text "' + said(words, 24) + '" is drawn at ' + size.toFixed(1) + 'px'); break; }
  }
  // SMALL: an HTML bar chart's label, value, note and legend text (decision_deck_chart.py), at its size on the screen
  for (const chart of slide.querySelectorAll('.chart')) {
    for (const t of chart.querySelectorAll('.hl, .hv, .hn, .hleg span')) {
      if (!t.textContent.trim() || !shown(t)) continue;
      const size = parseFloat(getComputedStyle(t).fontSize) * (t.offsetWidth ? t.getBoundingClientRect().width / t.offsetWidth : 1);
      if (size < SMALL_PX) { add('SMALL', chart, 'the chart text "' + said(t.textContent, 24) + '" is drawn at ' + size.toFixed(1) + 'px'); break; }
    }
  }
  if (mode !== 'desktop') {
    // KEYS: a keyboard hint on a phone
    for (const root of roots) {
      for (const kb of root.querySelectorAll('kbd')) if (shown(kb)) add('KEYS', kb.parentElement, 'a key hint shows on the phone: "' + said(kb.parentElement.textContent, 40) + '"');
      for (const ta of root.querySelectorAll('textarea')) if (shown(ta) && /\([A-Za-z?]\)\s*$/.test(ta.placeholder || '')) add('KEYS', ta, 'the placeholder names a key on the phone: "' + ta.placeholder + '"');
    }
    // TALL: the answers are more than TALL_SCREENS screens down
    const h = slide.getBoundingClientRect().height;
    if (h > TALL_SCREENS * innerHeight) {
      const big = [...slide.children].filter(shown).sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
      add('TALL', slide, 'the slide is ' + px(h) + ' tall, ' + (h / innerHeight).toFixed(1) + ' screens, so the answers are that far down' + (big ? '; ' + name(big).split(' > ').pop() + ' takes ' + px(big.getBoundingClientRect().height) : ''));
    }
  }
  return out;
}
"""
