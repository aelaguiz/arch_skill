"""Decision deck page script: slides, keys, pictures, and the live link (each action POSTed at once, retried; events).

The page talks to the server: a pick shows Recorded only after its POST returns 200, else "Not saved, retrying" with backoff; a comment is sent
1.8 s after typing stops or on leaving the box; /api/events streams every new ledger line with the state after it,
and /api/state?since=<n> is polled every 2 s whenever the stream is down. Status lines from the agent flip a slide
to Acting on it, Done with its result, or Failed with its reason; the dots and the summary read the same state.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_hints import HINTS  # noqa: E402
from decision_deck_links import LINKS, PICTURES  # noqa: E402
from decision_deck_steady_js import STEADY  # noqa: E402
from decision_deck_sync import SYNC  # noqa: E402

HEAD = r"""
(function () {
  'use strict';
  const D = JSON.parse(document.getElementById('data').textContent);
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
  const esc = (t) => String(t == null ? '' : t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const STACK = window.matchMedia('(max-width: 899px), (orientation: portrait)');
  const T = Object.assign({ advance: 900, idle: 1800, poll: 2000, deadline: 10000, retry: [1000, 2000, 4000, 8000, 15000] }, window.__deckT || {});
  const API = { pick: '/api/pick', comment: '/api/comment', done: '/api/done' };
  const ITEMS = D.items, N = ITEMS.length, LAST = N + 1;
  const S = { cur: D.start, state: D.state, known: D.n, gen: D.gen || 0, lines: D.lines.slice(), ui: {}, pend: {}, draft: {},
    idle: {}, adv: null, queue: [], busy: false, live: false, done: null };
  ITEMS.forEach((it) => { S.ui[it.id] = { mode: 'pair', col: 0, view: 0 }; S.pend[it.id] = {}; });
  const itemOf = (id) => ITEMS.find((i) => i.id === id);
  const opt = (it, id) => it.options.find((o) => o.id === id);
  const dec = (id) => S.state.decisions[id] || {};
  const now = () => new Date().toISOString();
  const live = (t) => { const el = $('#live'); el.textContent = ''; setTimeout(() => { el.textContent = t; }, 30); };
  const ring = (stroke, dash) => '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7" fill="var(--paper)" stroke="' + stroke + '" stroke-width="1.6"' + (dash ? ' stroke-dasharray="3 2.5"' : '') + '/></svg>';
  const ICON = {
    open: ring('var(--ink-2)'), unsaved: ring('var(--ink)', true),
    commented: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 4.5h12a1.5 1.5 0 0 1 1.5 1.5v7a1.5 1.5 0 0 1-1.5 1.5H9.2L5.5 17.3V14.5H4A1.5 1.5 0 0 1 2.5 13V6A1.5 1.5 0 0 1 4 4.5z" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    recorded: '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7.25" fill="var(--paper)" stroke="var(--accent)" stroke-width="1.8"/><path d="M6.6 10.2l2.3 2.3 4.6-4.8" fill="none" stroke="var(--accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    acting: '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="var(--accent)"/><circle cx="6.5" cy="10" r="1.4" fill="var(--paper)"/><circle cx="10" cy="10" r="1.4" fill="var(--paper)"/><circle cx="13.5" cy="10" r="1.4" fill="var(--paper)"/></svg>',
    done: '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8.5" fill="var(--accent)"/><path d="M5.8 10.4l2.8 2.8 5.6-5.9" fill="none" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    failed: '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8.5" fill="var(--ink)"/><path d="M7 7l6 6M13 7l-6 6" stroke="var(--paper)" stroke-width="2.2" stroke-linecap="round"/></svg>',
    end: '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="1" y="1" width="10" height="10" fill="none" stroke="var(--ink-2)" stroke-width="1.5"/></svg>'
  };
  const WORD = { open: 'open', commented: 'commented, still open', unsaved: 'not saved yet', recorded: 'answer recorded',
    acting: 'session acting on it', done: 'done', failed: 'failed' };
  const SAY = { recorded: 'Recorded', acting: 'Acting on it', done: 'Done', failed: 'Failed' };
  const pill = (k, text, cls) => '<span class="pill' + (cls ? ' ' + cls : '') + '">' + ICON[k] + esc(text) + '</span>';
  const box = (id) => document.getElementById('c-' + id);
  const typed = (id) => S.draft[id] !== undefined && S.draft[id].trim() !== sentNote(id);
  function sentNote(id) { const p = S.pend[id]; return p.comment ? p.comment.note : (dec(id).comment || ''); }
  function stateOf(id) {
    const p = S.pend[id], d = dec(id);
    if (p.pick) return 'unsaved';
    if (d.status) return d.status;
    if (d.choice) return 'recorded';
    return (typed(id) || p.comment || (d.comment || '').trim()) ? 'commented' : 'open';
  }

  // ---------- drawing ----------
  function renderBar() {
    $('#dots').innerHTML = Array.from({ length: N + 2 }, (_, i) => {
      const cur = i === S.cur ? ' aria-current="true"' : '';
      if (i === 0 || i === LAST) return '<button type="button" class="dot end" data-goto="' + i + '"' + cur + ' aria-label="' + (i ? 'Summary slide' : 'Opening slide') + '">' + ICON.end + '</button>';
      const it = ITEMS[i - 1], k = stateOf(it.id);
      return '<button type="button" class="dot" data-goto="' + i + '"' + cur + ' aria-label="' + esc(it.id + ', ' + it.name + ': ' + WORD[k]) + '" title="' + esc(it.id + ': ' + WORD[k]) + '">' + ICON[k] + '</button>';
    }).join('');
  }
  function renderChoices(it) {
    const p = S.pend[it.id], chosen = p.pick ? p.pick.option : dec(it.id).choice;
    $$('[data-choices="' + it.id + '"] .choice').forEach((b) => {   // in place: re-creating them would swallow a click
      const id = b.dataset.choose.split('|')[1], on = chosen === id;
      b.setAttribute('aria-pressed', String(on)); b.querySelector('.l').innerHTML = linkify(opt(it, id).label);   // its tick is drawn (STEADY_CSS in decision_deck_css.py)
    });
  }
  function renderStatus(it, extra) {
    const el = $('[data-status="' + it.id + '"]'); if (!el) return;
    const d = dec(it.id), p = S.pend[it.id], parts = [];
    if (p.pick) parts.push(p.pick.fail ? pill('unsaved', 'Not saved, retrying', 'warn') : '<span>Saving…</span>');
    else if (p.pickErr) parts.push(pill('failed', 'Not saved') + '<span>' + esc(p.pickErr) + '</span>');
    else if (d.choice || d.status) {
      const k = d.status || 'recorded';
      parts.push(pill(k, SAY[k]));
      if (k !== 'recorded' && d.result) parts.push('<span>' + linkify(d.result) + '</span>');
    }
    if (typed(it.id)) parts.push('<span>Comment sends when you pause</span>');
    else if (p.comment) parts.push(p.comment.fail ? pill('unsaved', 'Comment not saved, retrying', 'warn') : '<span>Sending comment…</span>');
    else if (p.commentErr) parts.push(pill('failed', 'Comment not saved') + '<span>' + esc(p.commentErr) + '</span>');
    else if ((d.comment || '').trim()) parts.push(pill('commented', 'Comment sent'));
    if (d.reply && !typed(it.id) && !p.comment) parts.push('<span class="reply">' + linkify(d.reply) + '</span>');
    el.innerHTML = parts.join('') + (extra || '');
  }
  function renderClosing() {
    let d = 0, c = 0;
    ITEMS.forEach((it) => { const k = stateOf(it.id); if (k === 'commented') c++; else if (k !== 'open') d++; });
    $('[data-closing-title]').textContent = d + ' of ' + N + ' decided' + (c ? ', ' + c + ' commented and open' : '') + (N - d - c ? ', ' + (N - d - c) + ' not yet answered' : '');
    // The Session and Comment columns show only when some decision has a value there, and the ledger only once it has lines.
    const rows = ITEMS.map((it, k) => {
      const x = dec(it.id), p = S.pend[it.id], o = p.pick ? opt(it, p.pick.option) : (x.choice ? opt(it, x.choice) : null), sk = stateOf(it.id);
      const ses = sk === 'unsaved' ? 'Not saved yet' : sk === 'done' ? (x.result || 'Done') : sk === 'failed' ? 'Failed' + (x.result ? ': ' + x.result : '') : sk === 'acting' ? 'Acting on it' : o ? 'Recorded' : '';
      const note = (S.draft[it.id] !== undefined ? S.draft[it.id] : sentNote(it.id)).trim();
      return { k: k, it: it, o: o, ses: ses, note: note, reply: x.reply || '' };
    });
    const hasSes = rows.some((r) => r.ses), hasNote = rows.some((r) => r.note || r.reply);
    $('[data-closing]').innerHTML = '<table class="sumtbl"><thead><tr><th>Decision</th><th>Answer</th>' + (hasSes ? '<th>Session</th>' : '') + (hasNote ? '<th>Comment</th>' : '') + '</tr></thead><tbody>' +
      rows.map((r) => '<tr><td><button type="button" data-goto="' + (r.k + 1) + '">' + esc(r.it.id + ' ' + r.it.name) + '</button></td><td>' + (r.o ? linkify(r.o.label) : '<span class="open">Open</span>') + '</td>' +
        (hasSes ? '<td>' + linkify(r.ses) + '</td>' : '') +
        (hasNote ? '<td class="c">' + linkify(r.note) + (r.reply ? '<br><span class="reply">' + linkify(r.reply) + '</span>' : '') + '</td>' : '') + '</tr>').join('') + '</tbody></table>' +
      (S.lines.length ? '<details class="ledger"><summary>Ledger lines so far (' + S.lines.length + ')</summary><pre>' + esc(S.lines.map((x) => JSON.stringify(x)).join('\n')) + '</pre></details>' : '');
    const btn = $('#done-btn'), st = $('[data-status="closing"]'), left = N - d;
    btn.disabled = !!S.state.done && !S.done;
    btn.innerHTML = S.state.done ? '✓ Done recorded' : 'Done <kbd>D</kbd>';
    if (S.done) st.innerHTML = S.done.fail ? pill('unsaved', 'Not saved, retrying', 'warn') : S.done.err ? pill('failed', 'Not saved') + '<span>' + esc(S.done.err) + '</span>' : '<span>Saving…</span>';
    else st.innerHTML = S.state.done ? pill('done', 'Done recorded') + '<span>' + (S.state.done.open.length ? S.state.done.open.length + ' left open' : 'nothing left open') + '</span>'
      : 'Done is optional: it tells the session the round is finished' + (left ? ', with ' + left + ' left open' : '') + '.';
  }
  function refreshAll() {
    ITEMS.forEach((it) => {
      renderChoices(it); renderStatus(it);
      const b = box(it.id);
      if (b && document.activeElement !== b && S.draft[it.id] === undefined && !S.pend[it.id].comment) b.value = dec(it.id).comment || '';
    });
    renderClosing(); renderBar();
  }
  function refresh(id) { const it = itemOf(id); if (it) { renderChoices(it); renderStatus(it); } renderClosing(); renderBar(); }

  // ---------- navigation ----------
  // The address follows the slide, replaced rather than pushed so Back still leaves the deck: a reload or a copied
  // link opens the slide on screen. The server serves the deck from its root (/, /d/<n>, /summary).
  function route(i) {
    const p = i === 0 ? '/' : i === LAST ? '/summary' : '/d/' + i;
    if (p !== location.pathname) try { history.replaceState(history.state, '', p + location.search); } catch (e) { /* no history here */ }
  }
  let land = 0;     // a deep-linked phone slide to land on again once pictures load; any other move clears it
  let aim = null, still = 0;   // the slide a phone scroll is heading for, held until it arrives or the scroll stops
  // Which slide is current, everywhere it shows (its class, the arrows, the address, the dots), without scrolling.
  function mark(i) {
    S.cur = i;
    $$('.slide').forEach((s) => s.classList.toggle('current', +s.dataset.i === i));
    $('.nav-arrow.prev').hidden = i === 0; $('.nav-arrow.next').hidden = i === LAST;
    route(i);
    renderBar();
    const box = $('#dots'), d = box && box.querySelector('[aria-current="true"]');      // keep the current dot in view
    if (d && box.scrollHeight > box.clientHeight + 1) box.scrollTop = d.offsetTop - (box.clientHeight - d.offsetHeight) / 2;
  }
  // how: left out glides there on a phone, 'jump' moves there at once (opening on a deep link), true leaves the scroll alone.
  function show(i, focus, how) {
    i = Math.max(0, Math.min(LAST, i));
    if (how !== 'jump') land = 0;
    if (S.adv) { clearTimeout(S.adv); S.adv = null; }
    mark(i);
    if (STACK.matches && how !== true) {
      const sl = $('#sl-' + i);
      if (sl) { aim = i; waitSettle(); sl.scrollIntoView({ behavior: how === 'jump' || matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
    }
    if (focus) { const h = $('#sl-' + i + ' .title, #sl-' + i + ' .title-c'); if (h) h.focus({ preventScroll: true }); }
  }
  function fit() {
    if (STACK.matches) return;
    const w = window.innerWidth, h = window.innerHeight - $('.bar').offsetHeight;
    const s = Math.min((w - 96) / 960, (h - 32) / 540), st = $('#stage').style;
    st.setProperty('--s', s.toFixed(4)); st.setProperty('--tx', (-480 * s).toFixed(1) + 'px'); st.setProperty('--ty', (-270 * s).toFixed(1) + 'px');
  }
  // On a phone the current slide is the last one whose top has passed a line 40% down the screen under the bar, so a
  // slide taller than two screens still becomes current (an intersection ratio over half never reaches it).
  // While a glide is moving the target stays current; once the page has been still for 400 ms (or never moved, as
  // for the slide already on screen), what is on screen is current.
  let ticking = false;
  function track() {
    if (!STACK.matches) return;
    const bar = $('.bar').offsetHeight, line = bar + (window.innerHeight - bar) * 0.4;
    let i = 0;
    $$('.slide').forEach((s) => { if (s.getBoundingClientRect().top <= line) i = +s.dataset.i; });
    if (aim !== null && i !== aim) return;
    aim = null;
    if (i !== S.cur) mark(i);
  }
  function waitSettle() { clearTimeout(still); still = setTimeout(() => { aim = null; track(); }, 400); }
  function onScroll() {
    waitSettle();
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; track(); });
  }
  ['touchstart', 'wheel'].forEach((t) => window.addEventListener(t, () => { aim = null; }, { passive: true }));   // the reader took over
  function watchStack() {
    window.removeEventListener('scroll', onScroll);
    if (STACK.matches) window.addEventListener('scroll', onScroll, { passive: true });
  }
"""

TAIL = r"""
  // ---------- events ----------
  document.addEventListener('click', (e) => {
    const t = e.target.closest('button'); if (!t) return;
    const d = t.dataset;
    if (d.goto != null) { show(+d.goto, true); return; }
    if (d.step) { show(S.cur + +d.step, true); return; }
    if (d.choose) { const [id, o] = d.choose.split('|'); choose(id, o); return; }
    if (d.view) { const [id, k] = d.view.split('|'); setUI(id, { view: +k }); return; }
    if (d.mode) { const [id, m] = d.mode.split('|'); setUI(id, { mode: m, col: 0 }); return; }
    if (d.flip) { flip(d.flip); return; }
    if (d.zoom) { zoom(d.zoom); return; }
    if (d.ctx) { const p = $('#ctx-' + d.ctx), o = !p.classList.contains('open'); p.classList.toggle('open', o); t.textContent = o ? 'Show less' : 'Read all'; t.setAttribute('aria-expanded', String(o)); return; }
    if (t.classList.contains('fold')) { t.nextElementSibling.hidden = false; t.hidden = true; return; }
    if (t.id === 'zoom-flip') { S.z.k = (S.z.k + 1) % itemOf(S.z.id).columns.length; zoomRender(); return; }
    if (t.id === 'done-btn') { finish(); return; }
    if (t.id === 'help-btn') { $('#help').showModal(); return; }
    if (d.close) { t.closest('dialog').close(); return; }
  });
  $('#zoom').addEventListener('close', () => { if (S.z && S.z.from) S.z.from.focus({ preventScroll: true }); });
  document.addEventListener('input', (e) => {
    const id = e.target.dataset && e.target.dataset.item; if (!id || !S.pend[id]) return;
    S.draft[id] = e.target.value;
    if (S.adv) { clearTimeout(S.adv); S.adv = null; }
    if (S.idle[id]) clearTimeout(S.idle[id]);
    S.idle[id] = setTimeout(() => sendComment(id), T.idle);
    renderStatus(itemOf(id)); renderBar();
  });
  document.addEventListener('focusout', (e) => { const id = e.target.dataset && e.target.dataset.item; if (id && S.pend[id] && S.draft[id] !== undefined) sendComment(id); });
  STACK.addEventListener('change', () => { fit(); hints(); keyHints(); watchStack(); show(S.cur); ITEMS.forEach((it) => { if (it.kind === 'images') renderImages(it); }); });
  document.addEventListener('keydown', (e) => {
    const tg = e.target, k = e.key, low = k.toLowerCase();
    if ($('#zoom').open) { if (low === 'f') { e.preventDefault(); $('#zoom-flip').click(); } return; }
    if ($('#help').open) return;
    if (tg.dataset && tg.dataset.item) {
      if (k === 'Escape') { e.preventDefault(); tg.blur(); const h = tg.closest('.slide').querySelector('.title'); if (h) h.focus({ preventScroll: true }); }
      else if (k === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); sendComment(tg.dataset.item); }
      return;
    }
    if (tg.tagName === 'TEXTAREA' || tg.tagName === 'INPUT' || e.metaKey || e.ctrlKey || e.altKey) return;
    const i = S.cur, it = ITEMS[i - 1];
    if (k === 'ArrowRight' || low === 'j' || k === 'PageDown' || (k === 'ArrowDown' && !STACK.matches)) { e.preventDefault(); show(i + 1, true); return; }
    if (k === 'ArrowLeft' || low === 'k' || k === 'PageUp' || (k === 'ArrowUp' && !STACK.matches)) { e.preventDefault(); show(i - 1, true); return; }
    if (k === 'Home') { e.preventDefault(); show(0, true); return; }
    if (k === 'End') { e.preventDefault(); show(LAST, true); return; }
    if (k === '?') { e.preventDefault(); $('#help').showModal(); return; }
    if (i === 0 && k === 'Enter' && !tg.closest('button')) { e.preventDefault(); show(1, true); return; }
    if (i === LAST && low === 'd') { e.preventDefault(); finish(); return; }
    if (!it) return;
    const o = it.options.find((x) => x.key === low || x.alt === low);
    if (o) { e.preventDefault(); choose(it.id, o.id); return; }
    if (low === 'c' && box(it.id)) { e.preventDefault(); if (S.adv) { clearTimeout(S.adv); S.adv = null; } box(it.id).focus(); return; }
    if (it.kind === 'images') {
      if (low === 'f') { e.preventDefault(); flip(it.id); return; }
      if (low === 'b') { e.preventDefault(); setUI(it.id, { mode: 'pair', col: 0 }); return; }
      if (low === 'v') { e.preventDefault(); setUI(it.id, { view: (S.ui[it.id].view + 1) % Math.max.apply(null, it.columns.map((c) => c.figs.length)) }); return; }
      if (low === 'z') { e.preventDefault(); const u = S.ui[it.id]; zoom(it.id + '|' + (u.mode === 'flip' ? u.col : 0)); return; }
    }
  });

  ITEMS.forEach((it) => { if (it.kind === 'images') renderImages(it); });
  refreshAll(); fit(); hints(); keyHints(); watchStack(); show(S.cur, false, S.cur === 0 || 'jump');
  // Pictures above a deep-linked phone slide load after that jump and push it down: land on it again once they have,
  // unless the reader did anything first (a tap, click, key, wheel or typing, or any move to another slide).
  if (STACK.matches && S.cur && document.readyState !== 'complete') {
    land = S.cur;
    ['touchstart', 'wheel', 'keydown', 'pointerdown', 'click', 'input'].forEach((t) => window.addEventListener(t, () => { land = 0; }, { once: true, passive: true, capture: true }));
    window.addEventListener('load', () => { if (land) show(land, false, 'jump'); land = 0; }, { once: true });
  }
  connect(); poll();
})();
"""

SCRIPT = HEAD + LINKS + PICTURES + SYNC + HINTS + STEADY + TAIL
