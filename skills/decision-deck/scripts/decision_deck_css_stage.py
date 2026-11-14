"""Decision deck CSS, the desktop stage: the 16:9 slide drawn at 960 x 540 px and scaled to the window, the header bar,
and every part of a slide (title, why, evidence, context line, answer row, cover, summary). decision_deck_css.py
describes the stage and its fit rule, and joins this sheet with the tokens and the other parts in page_css.
"""

CSS = r"""
:root { color-scheme: light; }
:root { --bar-h: 52px;
  --t-cover: 37.33px; --t-cover-lh: 44px; --t-title: 26.67px; --t-title-lh: 32px; --t-kicker: 13.33px; --t-lead: 18.67px; --t-lead-lh: 26px;
  --t-body: 14.67px; --t-body-lh: 20px; --t-note: 12px; --t-note-lh: 16px; --t-fine: 10.67px; --t-source: 9.33px; --t-tag: 10.67px;
  --m-l: 48px; --m-r: 48px; --m-t: 32px; --m-b: 10px; --focus: 0 0 0 2px var(--paper), 0 0 0 4px var(--accent); }
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--ground); color: var(--ink); font-family: var(--font-body); font-size: var(--t-body); line-height: var(--t-body-lh);
  font-optical-sizing: auto; -webkit-font-smoothing: antialiased; text-align: left; }
button, textarea { font: inherit; color: inherit; }
button { cursor: pointer; }
:focus-visible { outline: none; box-shadow: var(--focus); border-radius: 4px; }
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
kbd { display: inline-block; min-width: 1.4em; padding: 0 .3em; border: 1px solid color-mix(in srgb, var(--ink-2) 45%, var(--paper)); border-radius: 3px;
  background: var(--panel); color: var(--ink); font: 600 .72em/1.5 var(--font-body); text-align: center; }

.bar { position: fixed; inset: 0 0 auto 0; height: var(--bar-h); z-index: 10; display: flex; align-items: center; gap: 14px; padding: 0 16px;
  background: var(--paper); border-bottom: 1px solid var(--rule); font-size: 14px; line-height: 20px; }
.dots { display: flex; align-items: center; gap: 4px; margin-left: auto; }
.dot { width: 26px; height: 26px; padding: 0; border: 0; background: transparent; display: grid; place-items: center; border-radius: 50%; }
.dot svg { width: 18px; height: 18px; display: block; }
.dot[aria-current="true"] { box-shadow: 0 0 0 2px var(--ink); }
.dot.end svg { width: 12px; height: 12px; }
.btn { display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px; border: 1px solid var(--rule); border-radius: 6px;
  background: var(--paper); font-size: 14px; font-weight: 600; white-space: nowrap; }
.btn:hover { border-color: var(--ink-2); }
.btn.primary { background: var(--accent); border-color: var(--accent); color: var(--paper); }
.btn.primary kbd { background: transparent; color: var(--paper); border-color: color-mix(in srgb, var(--paper) 50%, var(--accent)); }
.btn:disabled { background: var(--panel); border-color: var(--rule); color: var(--ink-2); cursor: default; }
.btn.icon { width: 32px; padding: 0; justify-content: center; }

.deck { position: fixed; inset: var(--bar-h) 0 0 0; overflow: hidden; }
.stage { position: absolute; left: 50%; top: 50%; width: 960px; height: 540px; transform-origin: 0 0;
  transform: translate(var(--tx, -480px), var(--ty, -270px)) scale(var(--s, 1)); }
.slide { position: absolute; inset: 0; display: none; flex-direction: column; background: var(--paper); padding: var(--m-t) var(--m-r) var(--m-b) var(--m-l);
  box-shadow: 0 1px 2px rgba(17, 19, 24, .08), 0 8px 28px rgba(17, 19, 24, .10); }
.slide.current { display: flex; }
.slide > * { flex: none; min-height: 0; }
.nav-arrow { position: absolute; z-index: 2; top: 50%; width: 32px; height: 64px; margin-top: -32px; border: 0; border-radius: 6px; background: transparent;
  color: var(--ink-2); font-size: 28px; line-height: 64px; }
.nav-arrow:hover { background: color-mix(in srgb, var(--paper) 60%, transparent); }
.nav-arrow.prev { left: 4px; } .nav-arrow.next { right: 4px; }

.title { margin: 4px 0 0; font-size: var(--t-title); line-height: var(--t-title-lh); font-weight: 700; letter-spacing: -0.012em; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; }
.title:focus, .title-c:focus { box-shadow: none; }
.trule { height: 0; border-top: 1px solid var(--rule); margin: 10px 0 8px; }

.rec { display: flex; align-items: baseline; gap: 10px; margin: 0 0 8px; padding-left: 12px; border-left: 4px solid var(--data-1);
  font-size: var(--t-body); line-height: var(--t-body-lh); }
.rec .why { color: var(--ink-2); }

.ev { flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; overflow: hidden; }
.ev.fit { flex: 0 1 auto; }                /* text evidence is as tall as it needs: the context line sits under it */
.grow { flex: 0 0 0; }
.ev.fit ~ .grow { flex: 1 1 0; }           /* and the spare room goes above the answer row, which stays put */
.ev-tools { display: flex; align-items: center; flex-wrap: nowrap; gap: 6px 10px; margin: 0 0 6px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.seg { display: inline-flex; border: 1px solid var(--rule); border-radius: 6px; overflow: hidden; }
.seg button { height: 26px; padding: 0 9px; border: 0; background: var(--paper); font-size: var(--t-note); font-weight: 600; color: var(--ink-2);
  display: inline-flex; align-items: center; gap: 6px; }
.seg { flex: 0 1 auto; min-width: 0; max-width: 100%; }   /* long view names wrap inside their tab, never cut */
.seg button { min-width: 0; min-height: 26px; height: auto; line-height: var(--t-note-lh); overflow-wrap: anywhere; text-align: center; }
.seg button + button { border-left: 1px solid var(--rule); }
.ev-tools > span:last-child { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.seg button[aria-pressed="true"] { background: var(--ink); color: var(--paper); }
.seg button[aria-pressed="true"] kbd { background: transparent; color: var(--paper); border-color: color-mix(in srgb, var(--paper) 45%, var(--ink)); }
.pair { flex: 1 1 auto; display: grid; grid-template-columns: repeat(var(--cols, 2), minmax(0, 1fr)); gap: 0 20px; min-height: 0; }
.pair.one { grid-template-columns: 1fr; }
.pcol { display: flex; flex-direction: column; min-height: 0; min-width: 0; }
.phead { margin: 0 0 4px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.phead b { color: var(--ink); font-weight: 700; text-transform: uppercase; letter-spacing: .06em; margin-right: 6px; }
.pbox { flex: 1 1 auto; min-height: 0; position: relative; }
.pic { position: absolute; inset: 0 auto auto 0; height: 100%; max-width: 100%; padding: 0; margin: 0; border: 0; background: transparent; cursor: zoom-in;
  line-height: 0; display: block; text-align: left; }
.pic img { display: block; width: auto; height: auto; max-width: 100%; max-height: 100%; border: 1px solid var(--rule); background: var(--paper); }
.pic.close img { image-rendering: pixelated; }
.pic:hover img { border-color: var(--ink-2); }
.ctxrow { display: flex; gap: 8px; align-items: baseline; margin: 4px 0 0; }
.ctx { flex: 1; margin: 0; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); max-height: var(--t-note-lh); overflow: hidden; }   /* one whole line: it ends on a word, never inside one */
.ctx.open { max-height: none; }
.ctxrow.whole .more { display: none; }     /* nothing is cut (the page script measures it) */
.ctxrow:not(.whole):not(:has(.ctx.open))::after { content: "…"; order: 1; margin: 0 -4px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }   /* the cut shows as one */
.ctxrow .more { order: 2; }
.more { border: 0; background: none; padding: 0; font-size: var(--t-note); color: var(--accent-text); text-decoration: underline; text-underline-offset: 2px; }
.flipnow { font-weight: 700; color: var(--ink); }

.ev > .tx { flex: 0 1 auto; display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); align-items: start; gap: 0 24px;
  min-height: 0; overflow-y: auto; overscroll-behavior: contain; padding: 8px; border: 1px solid var(--rule); border-radius: 4px; }
.ev > .tx { padding-bottom: 0; }
.ev > .tx::after { content: ""; grid-column: 1 / -1; position: sticky; bottom: 0; height: 12px; background: var(--paper); }
.ev > .tx::-webkit-scrollbar, .tbl::-webkit-scrollbar { width: 8px; height: 8px; }
.ev > .tx::-webkit-scrollbar-thumb, .tbl::-webkit-scrollbar-thumb { background: color-mix(in srgb, var(--ink-2) 45%, var(--paper)); border-radius: 4px; }
.ev > .tx::-webkit-scrollbar-track, .tbl::-webkit-scrollbar-track { background: var(--panel); }
@supports not selector(::-webkit-scrollbar) { .ev > .tx, .tbl { scrollbar-width: thin; scrollbar-color: color-mix(in srgb, var(--ink-2) 45%, var(--paper)) var(--panel); } }
.panel { background: var(--panel); padding: 12px 14px; }
.panel .h { margin: 0 0 6px; font-size: var(--t-body); line-height: var(--t-body-lh); font-weight: 700; }
.panel p { margin: 0; font-size: var(--t-body); line-height: var(--t-body-lh); white-space: pre-wrap; overflow-wrap: anywhere; }
.panel p + p { margin-top: 10px; }
.panel .h + p { margin-top: 0; }
.lines { min-height: 0; padding-bottom: 6px; border-top: 1px solid var(--rule); }
.scrollhint { flex: none; margin: 4px 0 0; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.scrollhint[hidden] { display: none; }
.legend { margin: 6px 0 4px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.file h3 { margin: 10px 0 3px; font-size: var(--t-note); line-height: var(--t-note-lh); font-weight: 700; color: var(--ink-2); overflow-wrap: anywhere; }
.line { margin: 0 0 4px; padding: 5px 8px; border: 1px solid var(--rule); font-size: var(--t-note); line-height: calc(var(--t-note-lh) + 6px);
  white-space: pre-wrap; overflow-wrap: anywhere; }
del { color: var(--ink-2); text-decoration: line-through; text-decoration-thickness: 1px; }
ins { color: var(--accent-text); text-decoration: underline; text-decoration-color: var(--accent-rule); text-decoration-thickness: 1px; text-underline-offset: 2px; }
del + ins { margin-left: .25em; }
.newline { font-weight: 700; color: var(--ink-2); }
.fold { border: 0; padding: 0 4px; margin: 0 2px; border-radius: 3px; background: var(--panel); color: var(--ink-2); font-size: var(--t-note); }
.lines code, .panel code { padding: 0 3px; border-radius: 3px; background: color-mix(in srgb, var(--ink-2) 10%, transparent);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .92em; white-space: pre-wrap; }
.lines code .nb, .panel code .nb { white-space: pre; }      /* a command keeps the spaces it was written with */
.lines strong, .panel strong { font-weight: 700; }

.cx { flex: 1 1 auto; display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 0 28px; min-height: 0; }
.cx.one { grid-template-columns: minmax(0, 1fr); }
.side .h { margin: 0 0 6px; font-size: var(--t-body); line-height: var(--t-body-lh); font-weight: 700; }
.side ul { margin: 0; padding-left: 16px; font-size: var(--t-note); line-height: var(--t-note-lh); }
.side li { margin: 0 0 6px; }

.dock { flex: none; display: grid; grid-template-columns: minmax(180px, 1fr) auto; gap: 6px 14px; align-items: center; margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--rule); }
.dock.wide { grid-template-columns: minmax(0, 1fr); }
.dock.wide .choices { justify-content: start; }
.cbox label { display: flex; gap: 8px; margin: 0 0 3px; font-size: var(--t-note); line-height: var(--t-note-lh); font-weight: 700; color: var(--ink-2); }
.cbox label span { font-weight: 400; }
textarea { display: block; width: 100%; height: 42px; min-height: 42px; max-height: 120px; padding: 9px 10px; border: 1px solid var(--ink-2); border-radius: 4px; resize: none;
  font-size: var(--t-body); line-height: var(--t-body-lh); background: var(--paper); }
textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); outline: none; }
.choices { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(min-content, max-content); justify-content: end; gap: 8px; min-width: 0; }
.choice { display: flex; align-items: center; gap: 9px; min-height: 42px; padding: 4px 14px 4px 9px; border: 1px solid var(--ink);
  border-radius: 4px; background: var(--paper); text-align: left; white-space: normal; }
.choice .tx { display: flex; flex-direction: column; justify-content: center; }
.choice .l { font-size: var(--t-body); line-height: 18px; font-weight: 700; text-wrap-style: balance; }
.choice .m { font-size: var(--t-note); line-height: 14px; color: var(--ink-2); }
.choice:hover { background: var(--panel); }
.choice[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--paper); }
.choice[aria-pressed="true"] .m { color: var(--paper); }
.choice[aria-pressed="true"] kbd { background: transparent; color: var(--paper); border-color: color-mix(in srgb, var(--paper) 55%, var(--accent)); }
.choice.flash { animation: flash .8s ease-out; }
@keyframes flash { from { box-shadow: 0 0 0 5px color-mix(in srgb, var(--accent) 35%, transparent); } to { box-shadow: 0 0 0 0 transparent; } }
.status { grid-column: 1 / -1; display: flex; flex-wrap: wrap; align-items: flex-start; align-content: flex-start; gap: 0 14px; min-height: 32px; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.status:empty { display: none; }
.pill { display: inline-flex; align-items: center; gap: 5px; font-weight: 700; color: var(--ink); }
.pill svg { width: 14px; height: 14px; }
.adv { display: inline-block; width: 46px; height: 3px; background: var(--rule); position: relative; overflow: hidden; vertical-align: middle; }
.adv i { position: absolute; inset: 0; background: var(--accent); transform-origin: left; animation: adv var(--d, .9s) linear forwards; }
@keyframes adv { from { transform: scaleX(0); } to { transform: scaleX(1); } }

.src { flex: none; margin: 8px 0 0; font-size: var(--t-source); line-height: 13px; color: var(--ink-2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.cover .bar6 { width: 6px; height: 88px; background: var(--accent); float: left; margin: 4px 16px 0 0; }
.cover h2 { margin: 6px 0 0; font-size: var(--t-cover); line-height: var(--t-cover-lh); font-weight: 700; letter-spacing: -0.015em; text-wrap: balance; }
.nb { white-space: nowrap; }
.how { margin: 6px 0 0; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.start { margin-top: 10px; }
.cover-s { justify-content: center; }
.cover-s .how { margin: 12px 0 0 22px; font-size: var(--t-lead); line-height: var(--t-lead-lh); color: var(--ink-2); max-width: 760px; }
.cover-s .start { margin: 18px 0 0 22px; }
.rec .why { color: var(--ink); }
.sumtbl { width: 100%; border-collapse: collapse; font-size: var(--t-body); line-height: var(--t-body-lh); }
.sumtbl th { text-align: left; font-size: var(--t-note); line-height: var(--t-note-lh); font-weight: 700; color: var(--accent-text); text-transform: uppercase; letter-spacing: .06em;
  padding: 0 10px 6px 0; border-bottom: 1px solid var(--accent-rule); }
.sumtbl td { padding: 7px 10px 7px 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
.sumtbl td.c { color: var(--ink-2); font-size: var(--t-note); line-height: var(--t-note-lh); max-width: 260px; }
.sumtbl .open { color: var(--ink-2); }
.sumtbl button { border: 0; background: none; padding: 0; font-weight: 700; color: var(--ink); text-decoration: underline; text-decoration-color: var(--rule); text-underline-offset: 3px; text-align: left; }
.closing-body { flex: 0 1 auto; overflow-y: auto; min-height: 0; }   /* Done follows the summary, no blank between */
.ledger { margin-top: 12px; font-size: var(--t-note); line-height: var(--t-note-lh); }
.ledger summary { cursor: pointer; font-weight: 700; color: var(--ink-2); }
.ledger pre { margin: 6px 0 0; padding: 8px; background: var(--panel); font-size: 11px; line-height: 15px; white-space: pre-wrap; overflow-wrap: anywhere; }
.closing .dock { grid-template-columns: minmax(0, 1fr) auto; }


.bar .round { min-width: 0; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ev > .tx.one { grid-template-columns: minmax(0, 1fr); }
.cx { grid-template-rows: minmax(0, 1fr); }
.chart { min-height: 0; }                  /* a chart taller than its zone scales down whole (the SVG keeps its ratio) */
.chart svg { display: block; width: 100%; height: 100%; overflow: visible; }
.chart svg.narrow { display: none; }       /* the phone's drawing (labels above the bars) */
.chart text { font-family: var(--font-body); fill: var(--ink); }
.chart .lab { font-size: 14.67px; font-weight: 600; }
.chart .val { font-size: 12px; font-weight: 600; font-variant-numeric: tabular-nums; }
.tbl { flex: 1 1 auto; min-height: 0; overflow: auto; }
.sumtbl td.num { text-align: right; font-variant-numeric: tabular-nums; }
.sumtbl th.num { text-align: right; }                       /* a number column's head sits over its numbers */
.dtbl .num + :not(.num) { padding-left: 14px; }             /* a number never runs into the words after it */
.closing-body:not(:has(.decided, .ledger)) + .dock { border-top: 0; }   /* the table's last rule is the one above Done */
.closing .status { align-items: center; align-content: center; }     /* level with the Done button */
.dock.nonote { grid-template-columns: minmax(0, 1fr); }
.pill.warn { color: var(--ink); }
.pill.warn svg circle { stroke-dasharray: 3 2.5; }
.decided { margin: 12px 0 0; font-size: var(--t-note); line-height: var(--t-note-lh); color: var(--ink-2); }
.decided h3 { margin: 0 0 4px; font-size: var(--t-note); font-weight: 700; }
.decided ul { margin: 0; padding-left: 16px; }
.reply { color: var(--ink); }
"""
