"""Fit checks for decision_deck_check.py: the probe that holds a rendered slide to the deck's fit rule.

PROBE runs in the page with [slide index, "desktop" | "phone"] and returns [kind, selector, message] triples;
decision_deck_check.HELP describes each kind for the caller:
  CLIPPED  content hidden by overflow, or running past the bottom of the desktop slide, with no way to read it
  FADED    a mask image fading evidence out
  OFFCARD  an answer button or the comment box that does not show whole without scrolling something but the page
  WIDE     phone: an element wider than the viewport (or the page scrolling sideways)
  NESTED   phone: a scroll box inside the evidence zone
  SCROLLS  desktop: more than one scroll box in one evidence zone
READ_PROBE (decision_deck_check_text.py) runs after it on the same slide.
"""

# Runs in the page with [slide index, "desktop" | "phone"]; returns [kind, selector, message] triples.
PROBE = r"""
([i, mode]) => {
  const out = [], slide = document.getElementById('sl-' + i), vw = innerWidth, vh = innerHeight;
  if (!slide) return [['MISSING', '#sl-' + i, 'the page has no slide ' + i]];
  const px = (n) => Math.round(n) + 'px';
  const name = (el) => {
    const parts = [];
    for (let n = el; n && n !== slide.parentElement; n = n.parentElement) {
      if (n.id) { parts.unshift('#' + n.id); break; }
      const cls = [...n.classList].filter((c) => c !== 'current').slice(0, 2).map((c) => '.' + c).join('');
      parts.unshift(n.tagName.toLowerCase() + cls);
    }
    return parts.join(' > ');
  };
  const els = [slide, ...slide.querySelectorAll('*')];
  const shown = (el) => { const r = el.getBoundingClientRect();   // offset sizes are unscaled, so a 1px screen-reader-only label is skipped at any stage scale
    return r.width > 0 && r.height > 0 && (el.offsetWidth === undefined || (el.offsetWidth > 1 && el.offsetHeight > 1)) && getComputedStyle(el).visibility !== 'hidden'; };
  const opener = (el) => el.id && document.querySelector('[aria-controls="' + el.id + '"]');   // a Read all that opens it
  const reachable = (el) => el.hasAttribute('title') || opener(el);
  const scroller = (el) => {
    const s = getComputedStyle(el), y = /auto|scroll/.test(s.overflowY) && el.scrollHeight > el.clientHeight + 1,
          x = /auto|scroll/.test(s.overflowX) && el.scrollWidth > el.clientWidth + 1;
    return (x || y) ? (y ? 'scrolls ' + px(el.scrollHeight - el.clientHeight) + ' (content ' + px(el.scrollHeight) + ', box ' + px(el.clientHeight) + ')'
                         : 'scrolls sideways ' + px(el.scrollWidth - el.clientWidth) + ' (content ' + px(el.scrollWidth) + ', box ' + px(el.clientWidth) + ')') : '';
  };
  // an answer control must show without scrolling anything but the page: every box between it and the page that
  // clips or scrolls (overflow other than visible, the slide itself included) must hold it whole where it stands now
  const boxed = (el) => {
    const r = el.getBoundingClientRect(), miss = [];
    for (let n = el.parentElement; n && n !== document.body && n !== document.documentElement; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.overflowX === 'visible' && s.overflowY === 'visible') continue;
      const b = n.getBoundingClientRect();      // client sizes are unscaled; the desktop stage is scaled to the window
      const sy = n.offsetHeight ? b.height / n.offsetHeight : 1, sx = n.offsetWidth ? b.width / n.offsetWidth : 1;
      const top = b.top + n.clientTop * sy, left = b.left + n.clientLeft * sx;
      const cut = [['below', r.bottom - (top + n.clientHeight * sy)], ['above', top - r.top],
                   ['past the right of', r.right - (left + n.clientWidth * sx)], ['past the left of', left - r.left]]
        .filter(([, d]) => d > 0.5);
      const how = /auto|scroll/.test(s.overflowY + s.overflowX) ? 'scroll box that must be scrolled to reach it'
                                                                  : 'box that hides it';
      for (const [side, d] of cut)
        miss.push(side + ' ' + name(n).split(' > ').pop() + ' by ' + px(d) + ' (overflow ' + (s.overflowX === s.overflowY ? s.overflowY : s.overflowX + ' ' + s.overflowY) + ': a ' + how + ')');
    }
    return miss;
  };
  for (const el of els) {
    if (!shown(el)) continue;
    const s = getComputedStyle(el);
    if (/hidden|clip/.test(s.overflowY) && el.scrollHeight > el.clientHeight + 1 && !opener(el))
      out.push(['CLIPPED', name(el), 'overflow-y ' + s.overflowY + ' hides ' + px(el.scrollHeight - el.clientHeight) + ' (content ' + px(el.scrollHeight) + ', box ' + px(el.clientHeight) + ')']);
    if (/hidden|clip/.test(s.overflowX) && el.scrollWidth > el.clientWidth + 1 && !(s.textOverflow === 'ellipsis' && reachable(el)))
      out.push(['CLIPPED', name(el), 'overflow-x ' + s.overflowX + ' hides ' + px(el.scrollWidth - el.clientWidth) + ' (content ' + px(el.scrollWidth) + ', box ' + px(el.clientWidth) + ')' + (s.textOverflow === 'ellipsis' ? ', cut with an ellipsis and no way to read it' : '')]);
  }
  const zones = [...slide.querySelectorAll('.ev, .closing-body')];
  for (const z of zones) {
    const inside = [z, ...z.querySelectorAll('*')].filter(shown);
    for (const el of inside) {
      const m = getComputedStyle(el).maskImage || getComputedStyle(el).webkitMaskImage;
      if (m && m !== 'none') out.push(['FADED', name(el), 'mask-image fades the evidence (' + m.slice(0, 60) + ')']);
    }
    const boxes = inside.map((el) => [el, scroller(el)]).filter(([, w]) => w);
    if (mode === 'phone') boxes.forEach(([el, w]) => out.push(['NESTED', name(el), 'a scroll box inside the page scroll: ' + w]));
    else if (boxes.length > 1) out.push(['SCROLLS', name(z), boxes.length + ' scroll boxes in one evidence zone: ' + boxes.map(([el, w]) => name(el).split(' > ').pop() + ' ' + w).join('; ')]);
  }
  if (mode === 'desktop') {
    const card = slide.getBoundingClientRect(), controls = [];
    if (slide.scrollHeight > slide.clientHeight + 1)
      out.push(['CLIPPED', name(slide), 'content runs ' + px(slide.scrollHeight - slide.clientHeight) + ' past the bottom of the card']);
    for (const el of slide.querySelectorAll('.choices button, .choices .choice, .cbox textarea')) {
      if (!shown(el)) continue;
      const r = el.getBoundingClientRect(), miss = [];
      const edge = (label, a, b) => { if (a > b + 0.5) miss.push(label + ' ' + px(a - b)); };
      edge('past the right of the card by', r.right, card.right); edge('past the left of the card by', card.left, r.left);
      edge('below the card by', r.bottom, card.bottom); edge('above the card by', card.top, r.top);
      edge('past the right of the viewport by', r.right, vw); edge('below the viewport by', r.bottom, vh);
      edge('past the left of the viewport by', 0, r.left); edge('above the viewport by', 0, r.top);
      if (el.scrollWidth > el.clientWidth + 1) miss.push('its own text overflows it by ' + px(el.scrollWidth - el.clientWidth));
      miss.push(...boxed(el));
      for (const c of el.querySelectorAll('.l, .m')) {
        const q = c.getBoundingClientRect();
        if (q.right > r.right + 0.5) miss.push('its label runs ' + px(q.right - r.right) + ' past its edge');
      }
      for (const [other, q] of controls) {
        const w = Math.min(r.right, q.right) - Math.max(r.left, q.left), h = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
        if (w > 0.5 && h > 0.5) miss.push('overlaps ' + name(other).split(' > ').pop() + ' by ' + px(w) + ' x ' + px(h));
      }
      controls.push([el, r]);
      if (miss.length) out.push(['OFFCARD', name(el), [...new Set(miss)].join(', ')]);
    }
  } else {
    const wide = (el) => { const r = el.getBoundingClientRect(); return r.right > vw + 0.5 || r.left < -0.5; };
    for (const el of els) {
      if (!shown(el) || !wide(el) || (el !== slide && wide(el.parentElement))) continue;   // the outermost one only
      const r = el.getBoundingClientRect();
      out.push(['WIDE', name(el), 'spans ' + px(r.left) + ' to ' + px(r.right) + ' on a ' + vw + 'px screen (' + px(Math.max(r.right - vw, -r.left)) + ' off screen)']);
    }
    const card = slide.getBoundingClientRect();
    for (const el of slide.querySelectorAll('.choices button, .choices .choice, .cbox textarea')) {
      if (!shown(el)) continue;
      const r = el.getBoundingClientRect(), miss = boxed(el);
      if (!miss.length && r.bottom > card.bottom + 0.5) miss.push('below the card by ' + px(r.bottom - card.bottom));
      if (miss.length) out.push(['OFFCARD', name(el), [...new Set(miss)].join(', ')]);
    }
    if (i === 0 && document.documentElement.scrollWidth > vw + 1)
      out.push(['WIDE', 'html', 'the page scrolls sideways ' + px(document.documentElement.scrollWidth - vw)]);
  }
  return out;
}
"""
