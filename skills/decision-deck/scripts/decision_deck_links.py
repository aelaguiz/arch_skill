"""Decision deck page script, links and pictures: two fragments of the page script's closure.

decision_deck_script.py joins HEAD + LINKS + PICTURES + SYNC + HINTS + TAIL.
LINKS: `linkify` (escaped text with each http(s) URL a new-tab link; the same pattern and trimming as
decision_deck_deck.linked, which renders the slides), the guard that keeps a link click or Enter on a link from answering
or stepping a slide (registered before the deck's own listeners, so it can stop them), and the phone header's measured
height (--bar-live, read by HEADER_CSS in decision_deck_css.py).
PICTURES: the picture evidence (a caption is linked): columns, views, Flip and Zoom to real size. Flip's "Flip to X"
button keeps one place and one size (flipTo).
"""

LINKS = r"""
  // ---------- links ----------
  const CLOSE = { ')': '(', ']': '[', '}': '{' };
  const count = (s, c) => s.split(c).length - 1;
  const trimUrl = (u) => { for (;;) { const l = u.slice(-1); if (l && ('.,;:!?'.includes(l) || (CLOSE[l] && count(u, l) > count(u, CLOSE[l])))) u = u.slice(0, -1); else return u; } };
  function linkify(t) {
    const s = String(t == null ? '' : t), re = /(^|[^\w/])(https?:\/\/[^\s<>"']+)/gi;
    let out = '', last = 0, m;
    while ((m = re.exec(s))) {
      const at = m.index + m[1].length, u = trimUrl(m[2]);
      if (/:\/\/./.test(u)) { out += esc(s.slice(last, at)) + '<a href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' + esc(u) + '</a>'; last = at + u.length; }
    }
    return out + esc(s.slice(last));
  }
  // A link opens in a new tab and does nothing else: never a pick, a slide step or a fold. Inside a button (an option
  // label) it opens through window.open, since some browsers do not follow a link inside a button on their own.
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    if (a.closest('button')) { e.preventDefault(); window.open(a.href, '_blank', 'noopener,noreferrer'); }
    e.stopImmediatePropagation();
  });
  document.addEventListener('keydown', (e) => {   // Enter or Space on a link follows the link, not a deck key
    if ((e.key === 'Enter' || e.key === ' ') && e.target.closest && e.target.closest('a[href]')) e.stopImmediatePropagation();
  });
  // The phone's fixed bar wraps to its content (title, source line, dots); the page's top padding follows it.
  const barLive = () => document.documentElement.style.setProperty('--bar-live', $('.bar').offsetHeight + 'px');
  barLive();
  if ('ResizeObserver' in window) new ResizeObserver(barLive).observe($('.bar'));
"""

PICTURES = r"""
  // ---------- pictures ----------
  function figOf(it, k) { const c = it.columns[k]; return c.figs[Math.min(S.ui[it.id].view, c.figs.length - 1)]; }
  function pic(it, k) {
    const f = figOf(it, k);
    return '<button type="button" class="pic" data-zoom="' + it.id + '|' + k + '" aria-label="Zoom to real size: ' + esc(f.alt) + '"><img src="' + esc(f.src) + '" alt="' + esc(f.alt) + '" decoding="async"></button>';
  }
  function head(it, k, extra) { const c = it.columns[k], cap = figOf(it, k).caption || c.caption, words = '<b>' + esc(c.tag) + '</b>' + linkify(cap); return '<p class="phead' + (extra ? ' flip' : '') + '" title="' + esc(cap) + '"' + (extra ? ' role="status"' : '') + '>' + (extra ? '<span class="pcap" title="' + esc(cap) + '">' + words + '</span>' + extra : words) + '</p>'; }
  // Flip's "Flip to <next> (F)": at the caption line's right end, as wide as its longest label (every column's label
  // is laid in one cell, the next one shown), so a click neither moves nor resizes it (STEADY_CSS in decision_deck_css.py).
  function flipTo(it, u) {
    const nx = (u.col + 1) % it.columns.length, lab = (c) => 'Flip to ' + esc(c.tag) + ' (F)';
    return '<button type="button" class="more flipto" data-flip="' + it.id + '" title="' + lab(it.columns[nx]) + '">' + it.columns.map((c, k) => '<span' + (k === nx ? '' : ' class="off" aria-hidden="true"') + '>' + lab(c) + '</span>').join('') + '</button>';
  }
  function renderImages(it) {
    const el = $('[data-ev="' + it.id + '"]'); if (!el) return;
    const u = S.ui[it.id], cols = it.columns, nv = Math.max.apply(null, cols.map((c) => c.figs.length));
    const tabs = nv > 1 ? '<div class="seg" role="group" aria-label="View">' + Array.from({ length: nv }, (_, k) => { const l = it.views[k] || 'View ' + (k + 1); return '<button type="button" data-view="' + it.id + '|' + k + '" aria-pressed="' + (k === u.view) + '" title="' + esc(l) + '">' + esc(l) + '</button>'; }).join('') + '</div> <kbd title="Next view">V</kbd>' : '';
    const mode = cols.length > 1 ? '<div class="seg" role="group" aria-label="Compare"><button type="button" data-mode="' + it.id + '|pair" aria-pressed="' + (u.mode === 'pair') + '">' + (STACK.matches ? 'Both' : 'Side by side <kbd>B</kbd>') + '</button><button type="button" data-mode="' + it.id + '|flip" aria-pressed="' + (u.mode === 'flip') + '">Flip <kbd>F</kbd></button></div>' : '';
    let body;
    if (u.mode === 'flip' && cols.length > 1) {
      body = '<div class="pair one"><div class="pcol">' + head(it, u.col, flipTo(it, u)) + '<div class="pbox">' + pic(it, u.col) + '</div></div></div>';
    } else body = '<div class="pair" style="--cols:' + cols.length + '">' + cols.map((c, k) => '<div class="pcol">' + head(it, k) + '<div class="pbox">' + pic(it, k) + '</div></div>').join('') + '</div>';
    el.innerHTML = (tabs || mode ? '<div class="ev-tools">' + tabs + mode + '</div>' : '') + body;
  }
  function setUI(id, patch) { Object.assign(S.ui[id], patch); renderImages(itemOf(id)); }
  function flip(id) { const it = itemOf(id), u = S.ui[id]; if (it.columns.length < 2) return; if (u.mode !== 'flip') setUI(id, { mode: 'flip', col: 0 }); else setUI(id, { col: (u.col + 1) % it.columns.length }); live('Showing ' + it.columns[S.ui[id].col].tag); }
  function zoom(spec) { const [id, k] = spec.split('|'); S.z = { id: id, k: +k, from: document.activeElement }; zoomRender(); $('#zoom').showModal(); $('#zoom-flip').focus(); }
  function zoomRender() {
    const it = itemOf(S.z.id), c = it.columns[S.z.k], f = figOf(it, S.z.k), img = $('#zoom-img'), many = it.columns.length > 1;
    $('#zoom-t').textContent = it.id + ' · ' + c.tag + ': ' + (f.caption || c.caption);
    img.removeAttribute('width'); img.onload = () => { img.width = Math.round(img.naturalWidth / (it.density || 1)); };
    img.src = f.src; img.alt = f.alt;
    $('#zoom-flip').style.display = many ? '' : 'none';
    if (many) $('#zoom-flip').innerHTML = 'Flip to ' + esc(it.columns[(S.z.k + 1) % it.columns.length].tag) + ' <kbd>F</kbd>';
  }

"""
