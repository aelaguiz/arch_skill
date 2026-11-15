"""Decision deck page script, the live link: every action POSTed at once and in order, retried until it lands.

A fragment of the page script's closure (decision_deck_script.py joins HEAD + SYNC + TAIL): a pick shows Recorded only after
its POST returns 200; a network failure, a 5xx or no answer within T.deadline (fetch and body under one
AbortController) marks it "Not saved, retrying" and retries after 1, 2, 4, 8, then every 15 s; a 4xx is shown with its
reason and not retried. Each user action carries one request id (`rid`) on every retry, so a retry of an answer the
server already landed lands nothing new. The comment is sent 1.8 s after typing stops, on leaving the box, and when
the page is left (pagehide: whatever is still unsent goes out in order as one keepalive POST /api/batch, same ids, so
no action can overtake an earlier one); leaving with anything unsent asks first (beforeunload). /api/events streams
each new ledger line {n, gen, line, state}; /api/state?since=<n>&gen=<g> is polled every 2 s while the stream is down,
and once on load. Lines are kept by sequence number, so one delivered by both lands once; a reset (the ledger was
replaced or truncated: a new generation) drops them and rebuilds the page. Every answer names its generation (`gen`;
the server only raises it), so a late one is dropped when it is from an older generation, or is a reset behind the
lines the page already holds in this one; a state from another generation is never applied.
"""

SYNC = r"""
  // ---------- the live link: every action is POSTed at once, in order, and retried until the server answers ----------
  const rid = () => { const a = new Uint8Array(12); crypto.getRandomValues(a); return Array.from(a, (b) => b.toString(16).padStart(2, '0')).join(''); };
  function applyState(st, gen) { if (st && gen === S.gen && st.n >= S.state.n) { S.state = st; refreshAll(); } }
  function take(from, lines, st) {            // by sequence number: a line delivered twice lands in one place
    lines.forEach((x, k) => { S.lines[from + k] = x; });
    S.known = Math.max(S.known, from + lines.length); applyState(st, S.gen);
  }
  // A late answer: from an older generation, or a reset behind the lines already held (a generation never shrinks).
  const current = (x) => x.gen === S.gen ? !(x.reset && x.n < S.known) : !!x.reset && x.gen > S.gen;
  function restart(x) { S.gen = x.gen; S.lines = (x.lines || []).slice(); S.known = x.n; S.state = x.state; refreshAll(); }
  async function timed(url, opts) {           // the request and its body under one deadline: a stall cannot hold the queue
    const ac = new AbortController(), t = setTimeout(() => ac.abort(), T.deadline);
    try {
      const r = await fetch(url, Object.assign({ signal: ac.signal }, opts));
      let out = {}; try { out = await r.json(); } catch (e) { if (ac.signal.aborted) throw e; }
      return [r, out];
    } finally { clearTimeout(t); }
  }
  function send(kind, id, body, mark) { S.queue.push({ url: API[kind], kind: kind, id: id, body: Object.assign({ rid: rid() }, body), mark: mark, tries: 0 }); pump(); }
  function settle(job, err, out) {
    const p = job.id ? S.pend[job.id] : null;
    if (job.kind === 'pick' && p.pick === job.mark) { delete p.pick; if (err) p.pickErr = err; }
    if (job.kind === 'comment' && p.comment === job.mark) { delete p.comment; if (err) p.commentErr = err; }
    if (job.kind === 'done' && S.done === job.mark) S.done = err ? { err: err } : null;
    if (out && out.state) applyState(out.state, out.gen);
    if (job.kind === 'done') renderClosing(); else refresh(job.id);
    if (!err && job.kind === 'pick') live((S.pend[job.id].pick ? 'Saved; your newer answer is on its way.' : 'Recorded.'));
  }
  async function pump() {
    if (S.busy || !S.queue.length) return;
    const job = S.queue[0]; S.busy = true;
    try {
      const [r, out] = await timed(job.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(job.body) });
      if (r.status >= 500 || r.status === 429) throw new Error('HTTP ' + r.status);
      S.queue.shift(); settle(job, r.ok ? null : (out.error || 'HTTP ' + r.status), out);
    } catch (err) {
      job.tries += 1; job.mark.fail = true;
      if (job.kind === 'done') renderClosing(); else refresh(job.id);
      S.busy = false; setTimeout(pump, T.retry[Math.min(job.tries - 1, T.retry.length - 1)]); return;
    }
    S.busy = false; pump();
  }
  function sendComment(id) {
    const it = itemOf(id), b = box(id); if (!it || !b) return;
    if (S.idle[id]) { clearTimeout(S.idle[id]); S.idle[id] = null; }
    const text = b.value.trim(); delete S.draft[id]; delete S.pend[id].commentErr;
    if (text === sentNote(id)) { refresh(id); return; }
    const mark = { note: text }; S.pend[id].comment = mark;
    send('comment', id, { decision_id: id, note: text, ts: now() }, mark);
    refresh(id); live(text ? 'Comment sent to the session.' : 'Comment cleared.');
  }
  function choose(id, optId) {
    const it = itemOf(id), o = opt(it, optId), b = box(id); if (!o) return;
    const note = b ? b.value.trim() : '';
    if (S.idle[id]) { clearTimeout(S.idle[id]); S.idle[id] = null; }
    delete S.draft[id]; delete S.pend[id].pickErr;
    const mark = { option: optId }; S.pend[id].pick = mark;
    send('pick', id, { decision_id: id, option_id: optId, note: note, ts: now() }, mark);
    refresh(id);
    const btn = $('[data-choose="' + id + '|' + optId + '"]'); if (btn) { btn.classList.add('flash'); setTimeout(() => btn.classList.remove('flash'), 900); btn.focus({ preventScroll: true }); }
    if (o.ask_note && !note && b) {
      renderStatus(it, '<span><strong>Say what should change</strong> in the comment; it goes straight to the session.</span>');
      live(o.label + ' sent. Say what should change in the comment.'); b.focus(); return;
    }
    const i = ITEMS.indexOf(it) + 1;
    renderStatus(it, '<span>Next slide <span class="adv" aria-hidden="true"><i style="--d:' + T.advance + 'ms"></i></span></span>');
    S.adv = setTimeout(() => { S.adv = null; show(i + 1, true); }, T.advance);
  }
  function finish() { if (S.state.done && !S.done) return; const mark = {}; S.done = mark; send('done', null, { ts: now() }, mark); renderClosing(); live('Done sent.'); }
  async function poll() {
    try {
      const [r, x] = await timed('/api/state?since=' + S.known + '&gen=' + S.gen, { cache: 'no-store' });
      if (!r.ok || !x.state || !current(x)) return;
      if (x.reset) restart(x); else take(x.since || 0, x.lines || [], x.state);
    } catch (e) { /* the next tick tries again */ }
  }
  function connect() {
    if (!('EventSource' in window)) return;
    const es = new EventSource('/api/events?since=' + S.known + '&gen=' + S.gen);
    es.onopen = () => { S.live = true; };
    es.onerror = () => { S.live = false; };
    es.onmessage = (ev) => {
      let x; try { x = JSON.parse(ev.data); } catch (e) { return; }
      if (!current(x)) { if (x.gen > S.gen) poll(); return; }      // a newer generation's line: ask for its reset
      if (x.reset) restart(x); else if (x.n > S.known + 1) poll(); else take(x.n - 1, [x.line], x.state);
    };
  }
  setInterval(() => { if (!S.live) poll(); }, T.poll);
  // ---------- leaving: nothing typed or clicked is dropped ----------
  const unsent = () => S.queue.length > 0 || ITEMS.some((it) => typed(it.id));
  function flush() {        // one keepalive POST, the queue in order; same ids, so a request also in flight lands once
    ITEMS.forEach((it) => { if (typed(it.id)) sendComment(it.id); });
    if (!S.queue.length) return;
    const body = JSON.stringify({ jobs: S.queue.map((job) => ({ kind: job.kind, body: job.body })) });
    const beacon = () => { try { navigator.sendBeacon('/api/batch', new Blob([body], { type: 'application/json' })); } catch (e) { /* nothing left to try */ } };
    try { fetch('/api/batch', { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' }, body: body }).catch(beacon); }
    catch (e) { beacon(); }
  }
  window.addEventListener('beforeunload', (e) => { if (unsent()) { e.preventDefault(); e.returnValue = ''; } });
  window.addEventListener('pagehide', flush);

"""
