"""Decision deck page script, the scroll hint: a "Scroll for the rest" line under a desktop evidence box that scrolls.

A fragment of the page script's closure (decision_deck_script.py joins HEAD + SYNC + HINTS + TAIL). The line
(decision_deck_deck.SCROLL_HINT) shows while its box can scroll further and hides at the end, when the box fits, and on
phones, where the page scrolls instead; the fit rule allows one bounded scroll box and no fade. It is refreshed on
scroll, resize, font load, and on any change inside the evidence (a MutationObserver: a fold opened) or to the box's
size (a ResizeObserver).
"""

HINTS = r"""
  // "Scroll for the rest" under a desktop evidence box that scrolls, until it is scrolled to the end.
  function hints() {
    $$('[data-scrollhint]').forEach((h) => {
      const box = h.parentElement.querySelector('.tx, .tbl');
      const off = STACK.matches || !box || box.scrollHeight - box.scrollTop - box.clientHeight <= 2;
      if (h.hidden !== off) h.hidden = off;     // only on a change, so the observer below never loops
    });
    // Read all shows only while the context line is cut (a line that fits has nothing more to read).
    $$('.ctxrow').forEach((row) => {
      const p = row.querySelector('.ctx');
      if (!p || !p.clientHeight || p.classList.contains('open')) return;
      const whole = p.scrollHeight <= p.clientHeight + 1;
      if (row.classList.contains('whole') !== whole) row.classList.toggle('whole', whole);
    });
  }
  // The comment box names its key only where there is a keyboard.
  function keyHints() { $$('textarea[data-item]').forEach((t) => { t.placeholder = STACK.matches ? 'Comment' : 'Comment (C)'; }); }
  // A fold opened (its hidden text shown), Read all, a picture loading or a resize changes what the box holds or
  // its size without a scroll; watch the evidence for both.
  const evWatch = 'MutationObserver' in window ? new MutationObserver(hints) : null;
  const evSize = 'ResizeObserver' in window ? new ResizeObserver(hints) : null;
  $$('.ev').forEach((ev) => {
    if (evWatch) evWatch.observe(ev, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['hidden', 'class'] });
    const box = ev.querySelector('.tx, .tbl');
    if (evSize && box) { evSize.observe(box); [...box.children].forEach((c) => evSize.observe(c)); }
  });
  if (evSize) $$('.ctx').forEach((p) => evSize.observe(p));
  document.addEventListener('scroll', (e) => { if (e.target.closest && e.target.closest('.ev')) hints(); }, true);
  window.addEventListener('resize', () => { fit(); hints(); });
  window.addEventListener('load', hints);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(hints);
"""
