"""Decision deck page script, steady slides: the one-line status band's overlay and the desktop table's column widths.

A fragment of the page script's closure (decision_deck_script.py joins it after HINTS, before TAIL); it runs once when the
page builds and again on a resize, a font load or a switch between the desktop and phone layouts.

The status band (STEADY_CSS in decision_deck_css.py): a status longer than its one line is cut with an ellipsis; then the line
carries the whole text as its title, takes the focus, and a click or Enter opens the whole text in an overlay anchored
above it inside the answer row; Esc, a click elsewhere or another slide closes it. The line itself keeps every word
(aria-live), so a screen reader hears it whole. Watched with a MutationObserver, so each new status is measured
before it is painted.

Table columns. The browser's auto layout can give a short label column most of a wide table, squeeze short values to
the far right and give two compared columns unequal widths. Here the first column is the label column, as wide as its
longest text (capped at STEADY_T.cap of the table), a number column takes its content width, and the other columns
(the compared ones) share the rest equally; when they all fit on one line with room left, every column after the
label shares the rest equally, and with two or more of them, when every column's text fits on one line in an equal
share, every column takes an equal share, unless that leaves a column but the last more than STEADY_T.loose of the
table empty and the label-first layout leaves less (a short "ID" column). Layouts are tried in order and the first
that fits its evidence box without a scroll wins: (a) the label at its full width, then the label wrapped narrower in
up to STEADY_T.steps steps down to (b), its longest word; when none fits but the browser's auto layout does, (near)
the split nearest to equal that fits: from equal columns at the auto layout's label width, STEADY_T.near steps toward
the auto layout's own widths, the first that fits, refined by halving STEADY_T.refine times; when that fails too, the
shortest of them and the auto layout, so a table is never taller than the browser draws it. At most 9 + 11
measurements a table, the same every time for the same table and box. A layout that would squeeze a column under its
longest word is never used. Each is measured before the page is painted (slides not on screen are laid out unseen for
it), so the first paint already shows the chosen widths. A table left in the auto layout because no other layout fits
its box is marked data-fit="kept"; one given the split nearest to equal is marked data-fit="near".
On a phone (STACK) a table that stays a table (not one card per row, `.cards`) gets the same rule with the label
capped at STEADY_T.phoneCap and no box height: the first layout that keeps every word whole. Its longest words are
measured with the phone's break-anywhere wrapping turned off for the reading.
"""

STEADY = r"""
  // ---------- steady slides: the status band's overlay, and table columns that use the width ----------
  // loose: the most of the table's width an equal share may leave empty in a column but the last (the content width
  // read here includes the cell's padding)
  const STEADY_T = { cap: 0.36, phoneCap: 0.5, steps: 8, near: 8, refine: 3, minStep: 6, gap: 4, edge: 8, loose: 0.25 };
  function fullOf(st, make) {
    let f = st.parentElement.querySelector('.status-full');
    if (!f && make) { f = document.createElement('div'); f.className = 'status-full'; f.hidden = true; st.parentElement.appendChild(f); }
    return f;
  }
  function closeFull(st) { const f = fullOf(st); if (f && !f.hidden) f.hidden = true; }
  function closeAllFull() { $$('.status-full').forEach((f) => { if (!f.hidden) closeFull(f.parentElement.querySelector('.status')); }); }
  function topIn(el, root) { let y = 0; for (let n = el; n && n !== root; n = n.offsetParent) y += n.offsetTop; return y; }
  function openFull(st) {
    const f = fullOf(st, true), dock = st.parentElement, slide = st.closest('.slide');
    f.innerHTML = st.innerHTML;
    f.style.bottom = (dock.clientHeight - st.offsetTop + STEADY_T.gap) + 'px';
    f.style.maxHeight = Math.max(0, topIn(st, slide) - STEADY_T.gap - STEADY_T.edge) + 'px';
    f.hidden = false;
  }
  function cutCheck(st) {
    const cut = st.clientWidth > 0 && st.scrollWidth > st.clientWidth + 1;
    if (cut) {
      const text = st.textContent.replace(/\s+/g, ' ').trim();
      if (st.title !== text) st.title = text;
      st.tabIndex = 0;
    } else {
      closeFull(st);
      st.removeAttribute('title'); st.removeAttribute('tabindex');
    }
    st.classList.toggle('cut', cut);
    const f = fullOf(st); if (f && !f.hidden) f.innerHTML = st.innerHTML;
  }
  const bands = () => $$('.slide.item .status');
  const statusWatch = 'MutationObserver' in window ? new MutationObserver((recs) => {
    new Set(recs.map((r) => (r.target.nodeType === 1 ? r.target : r.target.parentElement).closest('.status'))).forEach((st) => { if (st) cutCheck(st); });
  }) : null;
  const slideWatch = 'MutationObserver' in window ? new MutationObserver((recs) => recs.forEach((r) => {
    const st = r.target.querySelector('.status'); if (!st) return;
    closeFull(st); if (r.target.classList.contains('current')) cutCheck(st);
  })) : null;
  bands().forEach((st) => {
    if (statusWatch) statusWatch.observe(st, { childList: true, subtree: true, characterData: true });
    if (slideWatch) slideWatch.observe(st.closest('.slide'), { attributes: true, attributeFilter: ['class'] });
  });
  document.addEventListener('click', (e) => {
    const st = e.target.closest && e.target.closest('.slide.item .status.cut');
    if (st && !e.target.closest('a')) { const f = fullOf(st); if (f && !f.hidden) closeFull(st); else openFull(st); return; }
    if (!(e.target.closest && e.target.closest('.status-full'))) closeAllFull();
  }, true);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && $$('.status-full').some((f) => !f.hidden)) { e.preventDefault(); e.stopPropagation(); closeAllFull(); return; }
    const st = e.target.closest && e.target.closest('.slide.item .status.cut');
    if (st && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); e.stopPropagation(); const f = fullOf(st); if (f && !f.hidden) closeFull(st); else openFull(st); }
  }, true);

  // Lay a table out unseen when its slide is not on screen or it sits in a hidden box, so it can be measured; put
  // each box back after.
  function unseen(t, fn) {
    const slide = t.closest('.slide'), put = [];
    const show = (el) => { put.push([el, el.style.display, el.style.visibility]); el.style.display = 'flex'; el.style.visibility = 'hidden'; };
    if (!slide.classList.contains('current')) show(slide);
    for (let n = t.parentElement; n && n !== slide; n = n.parentElement) if (n.hidden) show(n);
    try { return fn(); } finally { put.reverse().forEach(([el, d, v]) => { el.style.display = d; el.style.visibility = v; }); }
  }
  function plainTable(t) {
    t.classList.remove('steady'); t.style.width = ''; t.style.tableLayout = '';
    const cg = t.querySelector('colgroup.steady'); if (cg) cg.remove();
  }
  function colWidths(t, how) {
    // A phone cell may break anywhere (PHONE_CSS in decision_deck_css.py); its longest word is still its narrowest.
    const cells = STACK.matches && how === 'min-content' ? Array.from(t.querySelectorAll('td')) : [];
    cells.forEach((c) => { c.style.overflowWrap = 'normal'; });
    t.style.tableLayout = 'auto'; t.style.width = how;
    const out = Array.from(t.rows[0].cells).map((c) => c.offsetWidth);
    t.style.width = ''; t.style.tableLayout = '';
    cells.forEach((c) => { c.style.overflowWrap = ''; });
    return out;
  }
  // Column widths for a label column `lab` px wide, or null when a column would be squeezed under its longest word.
  function plan(W, lab, mx, mn, nums) {
    const vals = mx.map((_, k) => k).filter((k) => k > 0), text = vals.filter((k) => !nums[k]), num = vals.filter((k) => nums[k]);
    const out = mx.map(() => 0); out[0] = lab;
    const even = (W - lab) / vals.length, slack = !text.length || vals.every((k) => mx[k] <= even);
    const share = (W - lab - num.reduce((a, k) => a + mx[k], 0)) / Math.max(1, text.length);
    vals.forEach((k) => { out[k] = slack ? even : nums[k] ? mx[k] : share; });
    const ok = out.every((w, k) => w >= mn[k] - 0.5);
    const share1 = W / mx.length;            // one equal share each, when every column's text fits in one on one line
    const empty = (ws) => Math.max(...ws.slice(0, -1).map((w, k) => w - mx[k]));   // the most room left in one column but the last
    if (slack && vals.length > 1 && mx.every((m) => m <= share1)) {
      const eq = mx.map(() => share1);
      if (!ok || empty(eq) <= STEADY_T.loose * W || empty(eq) <= empty(out)) return eq;
    }
    return ok ? out : null;
  }
  function apply(t, ws) {
    plainTable(t);
    const cg = document.createElement('colgroup'); cg.className = 'steady';
    ws.forEach((w) => { const c = document.createElement('col'); c.style.width = w.toFixed(2) + 'px'; cg.appendChild(c); });
    t.insertBefore(cg, t.firstChild); t.classList.add('steady'); t.style.tableLayout = 'fixed';
  }
  function layTable(t) {
    const box = t.closest('.tbl, .tx'), hint = box && box.parentElement.querySelector('[data-scrollhint]');
    plainTable(t); delete t.dataset.fit; delete t.dataset.layout;
    const phone = STACK.matches;
    if (!box || !t.rows.length || t.rows[0].cells.length < 2 || (phone && t.classList.contains('cards'))) return;
    const nums = Array.from(t.rows[0].cells).map((c) => c.classList.contains('num'));
    if (nums[0]) return;                   // no label column: the auto layout
    if (hint && !phone) hint.hidden = true;  // measured without the hint line; hints() puts it back
    const fits = () => phone || (box.scrollHeight <= box.clientHeight + 1 && box.scrollWidth <= box.clientWidth + 1);
    const W = box.clientWidth, main = Array.from(t.rows[0].cells).map((c) => c.offsetWidth);
    const auto = { ws: null, h: t.offsetHeight, fit: fits(), name: 'auto' };
    t.classList.add('steady');
    const mx = colWidths(t, 'max-content'), mn = colWidths(t, 'min-content');
    plainTable(t);
    const measure = (ws, name) => { apply(t, ws); const r = { ws: ws, h: t.offsetHeight, fit: fits(), name: name }; plainTable(t); return r; };
    const tryOut = (lab, name) => { const ws = plan(W, lab, mx, mn, nums); return ws ? measure(ws, name) : null; };
    // (a) the label at its full width (capped); then narrower labels down to (b), its longest word: the first that
    // fits wins (on a phone, with no box height, the first that keeps every word whole).
    const cap = phone ? STEADY_T.phoneCap : STEADY_T.cap;
    const full = Math.max(mn[0], Math.min(mx[0], cap * W)), step = (full - mn[0]) / STEADY_T.steps;
    const tries = [tryOut(full, 'a')];
    for (let k = 1; k < STEADY_T.steps && step >= STEADY_T.minStep; k++) tries.push(tryOut(full - k * step, 'b'));
    if (full > mn[0]) tries.push(tryOut(mn[0], 'b'));
    const ok = tries.filter(Boolean);
    // (near) none fits but the auto layout does: the split nearest to equal that fits; failing that, the shortest
    // of them all and the auto layout.
    let pick = ok.find((x) => x.fit);
    if (!pick && auto.fit) pick = nearest(W, Math.min(full, Math.max(mn[0], main[0])), main, mx, mn, nums, measure);
    pick = pick || ok.concat([auto]).reduce((x, y) => (y.h < x.h - 0.5 ? y : x));
    if (pick.ws) apply(t, pick.ws);
    if (!pick.ws || pick.name === 'near') t.dataset.fit = pick.ws ? 'near' : 'kept';   // kept: the auto layout, no other fits its box
    t.dataset.layout = pick.name;
  }
  // Equal columns at the auto layout's label width `lab` (within the label's bounds), then STEADY_T.near steps of the straight
  // path toward the auto layout's own widths (its other columns scaled to the room the label leaves): the first step that fits,
  // its distance from the step before halved STEADY_T.refine times while it still fits. A step never squeezes a
  // column under its longest word and keeps its compared columns more equal than the auto layout's.
  function nearest(W, lab, main, mx, mn, nums, measure) {
    const base = plan(W, lab, mx, mn, nums); if (!base) return null;
    const rest = main.reduce((a, w, k) => a + (k ? w : 0), 0), to = main.map((w, k) => (k ? w * (W - lab) / rest : lab));
    const gap = (ws) => { const c = ws.filter((_, k) => k && !nums[k]); return c.length > 1 ? Math.max(...c) - Math.min(...c) : 0; };
    const at = (f) => {
      const ws = base.map((w, k) => w + f * (to[k] - w));
      if (!ws.every((w, k) => w >= mn[k] - 0.5) || (f > 0 && gap(ws) >= gap(main) - 0.5)) return null;
      const r = measure(ws, f > 0 ? 'near' : 'b'); return r.fit ? r : null;
    };
    let lo = 0, hi = -1, got = null;
    for (let k = 0; k < STEADY_T.near && !got; k++) { got = at(k / STEADY_T.near); if (got) hi = k / STEADY_T.near; else lo = k / STEADY_T.near; }
    for (let n = 0; got && hi > 0 && n < STEADY_T.refine; n++) {
      const f = (lo + hi) / 2, r = at(f); if (r) { got = r; hi = f; } else lo = f;
    }
    return got;
  }
  function layTables() { $$('.slide .dtbl').forEach((t) => unseen(t, () => layTable(t))); }
  function steady() { layTables(); bands().forEach((st) => cutCheck(st)); if (typeof hints === 'function') hints(); }
  steady();
  STACK.addEventListener('change', steady);
  window.addEventListener('resize', steady);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(steady);
"""
