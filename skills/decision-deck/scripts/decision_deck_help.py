"""The --help text for decision_deck.py: subcommands, the spec format with every key, the ledger records and the routes."""

HELP = """Decision deck: an agent that needs a person's approvals (the owner's) writes one JSON spec; this serves it as one
interactive presentation, one decision per slide, with the exact thing being decided shown as evidence and the options
as one-click buttons. Each click and comment lands in an append-only JSONL ledger at once; the asking agent watches
the ledger, acts on each answer and reports what it did back onto the slide.

Subcommands:
  serve   Serve the spec as one deck page: a cover, one slide per decision, a summary with Done. Binds 127.0.0.1
          unless --host names another loopback or private-network address. Prints `URL <url>` first. Each click
          and comment POSTs at once; the server appends one JSON line to the ledger (append-only; the latest pick
          per decision wins; a comment never replaces a pick). It stops itself once every decision is picked and a
          grace period (default 15 min) has passed since the last pick, status or reply made while no decision was
          open (however it reached the ledger: the server or a direct append; a decision open again, as after a
          replaced ledger, stops that clock until all are picked again), at its maximum lifetime (default 24 h),
          or on SIGINT/SIGTERM; its state file (url, pid, token; mode 0600) goes with it. The header bar shows the
          title and, under it, the --source line when given. A spec with no matching check stamp (below) gets one
          stderr warning and is served; --require-checked refuses it.
  watch   Tail the ledger, one line per record as it lands (the records already there first, unless --from-end),
          for an agent's background watcher: `PICK <decision>=<option> (<label>) note="..." at <time> pick=<ts>`
          (<time> in this machine's time zone; <ts> names that pick exactly, for act --pick-ts),
          `COMMENT <decision> note="..." at <time>` (an empty note clears the comment; the decision stays open),
          `DONE open=<ids or none> at <time>` (the owner pressed Done; it gates nothing), and for a skip line
          `SKIP <decision> note="..." at <time>`. A change of answer after the agent reported done is a new PICK
          line: reverse or redo the action. With --spec: ALL_PICKED once, the first time every decision has a
          pick. SERVER_STOPPED and exit 0 once a server this watch saw running has stopped, or (with --spec) once
          every decision is picked and no server is running; with --spec, any decisions still open are named on
          that line: `SERVER_STOPPED open=<ids>` (the owner left with answers missing; ask in the chat). With no
          server ever seen and decisions open it keeps waiting. Exit 3 with WATCH_TIMEOUT at --max-hours. The agent's own status and reply lines are not echoed.
  status  The latest pick per decision (PICK), the agent's status for it (STATE <decision> acting|done|failed
          result="..."), any note newer than the pick (COMMENT, or SKIP for a skip line) and the decisions still
          open (OPEN). --json for machines: "picked", "skipped" (the newer notes), "open", "all_picked", and
          "states" ({<decision>: {"state", "result"}} for each decision with a STATE line).
  act     `act <decision> [<decision> ...] --spec S --state acting|done|failed [--result "..."] [--reply "..."]
          [--pick-ts <ts> [--pick-ts <ts> ...] | --pick <option>]`: the agent tells the slide what it did ("Published
          the new hours", or the reason it failed). Several ids share the state, result and reply and get one
          status line each; all are checked first and nothing is written unless every one passes (the error names
          each failing id). The line names the pick it is about, so a late result for an answer the owner has
          since changed never marks the new one: --pick-ts names it exactly (the pick=<ts> ending its PICK line;
          the flag once per decision, in the same order), --pick that option's latest pick. Without either,
          acting takes the latest pick, and done or failed the pick the decision's most recent acting line named
          (also after a done or failed for it, so a corrected result stays with that work), else the latest pick;
          stderr notes when a newer pick exists than the one named. Prints `STATUS <decision> <state>
          result="..." via server|ledger` per decision.
  reply   `reply <decision> --spec S --text "..."`: the agent answers a comment; it shows under the comment it
          answers (the one shown when reply runs) until that comment changes.
          act and reply go through the running server (POST /api/status with the state file's token), else
          straight to the ledger; the page shows them within 2 s either way while it is served.
  text    `text --spec S [--out FILE]`: every word the spec puts on a slide, as plain text in slide order (the
          cover title; per decision the slide title, the recommendation's why, the evidence as text: table rows,
          the diff paragraph by paragraph, chart bars and values, pictures by column and caption; the context line
          with each option's caption, pros and cons; the answer buttons with the Recommended mark; the summary
          rows and earlier rounds). Lines in [square brackets] say where the text sits. Hand it to a reader who
          has not seen the work to find slides that do not make sense on their own; nothing is served or rendered.
  asks    `asks --spec S [--url URL] [--out FILE]`: the full text ask of every decision, in spec order, to paste
          into the chat message that goes with the deck, so the owner can answer from chat too. With --url the
          first line is `Deck: <url>`. Per decision: `<id> (<title>): <question>`; `Recommendation: <id><letter>
          (<label>). <why>` or `No recommendation. <why>`; the exact thing as `text` writes it; `Context: ...`;
          `Source: ...` when the chart has one; one line per option, `<id>a. <label>`, lettered in spec order.
          The spec's decided list is left out. Plain text: no Markdown, no HTML.

Spec (JSON; "?" marks an optional key, every other key is required):
  {"title" (the cover), "decided"?: [{"title", "answer"}] (earlier rounds, listed read-only on the summary),
   "decisions": [{"id" (the label the reply uses, such as D1, D2), "title" (the dot and summary name), "question"
    (the slide title when it fits one line, 62 characters; else the title, with the question under the evidence),
    "context"?, "allow_note"? (default true: a comment box; false hides it and drops notes),
    "recommendation": {"option": <option id or null>, "why"} (the callout carries the why; the button its mark),
    "evidence"?: one kind, below; without it, options with images make a picture decision,
    "shared"?: [{"image", "caption"?}] (pictures that apply to every option, shown as the "Ours" column),
    "references"?: [{"image", "caption"?}] (screenshots to compare against, never an option),
    "references_title"? (default "Reference, layout only (not an option)"),
    "options": [{"id", "label", "images"?: [paths relative to the spec's folder], "caption"?,
                 "pros"?: [strings], "cons"?: [strings], "key"?: one letter that also answers it (digits 1-9
                 answer by position; j k c v f b z d are taken), "ask_note"?: true (picking it asks for a comment
                 when none is typed, such as "Needs change")}]}]}
  Evidence kinds (one per decision, drawn in the slide's evidence zone):
    {"kind": "images", "views"?: [tab label per picture index], "density"?: 1|2|3 (image pixels per screen pixel,
     so Zoom shows real size), "shared"?, "references"?, "references_title"? (here or on the decision, not both)}:
     columns side by side (Ours, then each option with images, then the references); Flip (F) shows one column
     at a time, V steps the views, Z zooms to real size.
    {"kind": "diff", "before", "after", "rule_now"?}: the text change as a redline (removed struck through, added
     underlined), beside a "The rule now reads" panel when rule_now is given. Paragraphs (split on blank lines) are
     paired in order; a pair sharing half its words or more is marked word by word, a rewrite shows the whole old
     paragraph struck and then the whole new one underlined, and an unpaired paragraph is wholly removed or added.
     A blank line in rule_now starts a new panel paragraph; a single line break is kept. On the desktop the panel
     and the change share one scroll box. Paste rule text as it is written: Markdown in before, after and rule_now
     shows formatted (`**bold**`, `` `code` ``, a `# heading` line, the text of `[text](target)`), never as typed
     markers; a code span up to 60 characters and a double-quoted phrase up to 8 words are struck or underlined
     whole; an added or removed sentence is marked from its first word, and words added or removed beside
     punctuation ("script." to "script or a tool.") are marked on their own; the legend names only the marks the
     redline has. Markdown anywhere else on a slide shows as typed (the checker's MARKUP): write plain words there.
    {"kind": "chart", "bars": [{"label", "value" (a number, 0 or more), "emphasis"? (true on at most one bar),
     "note"? (what this bar tells us)}], "unit"? (after each value), "prefix"? (before it, 1 to 3 characters, such
     as "$"), "decimals"? (0 to 4: 2 writes 1.6 as 1.60), "series"? (two names, such as ["Today", "New"]: each bar
     then gives "values": [a, b] instead of "value", and no emphasis), "type"? ("bar", the default, or "line"),
     "source"? (the slide's source line), "side"?: {"title"?, "items": [strings]}}: a horizontal bar chart, the
     emphasised bar in the accent, the rest grey, each labelled directly (on a phone each label sits above its
     bar, so the text keeps its size). A chart with a note, prefix, decimals, series or type, or a label over 25
     characters, reads one row per bar: the label (as wide as the longest, up to 45% of the chart; a longer one
     wraps, never cut), the bar, the value (all values in one right-aligned column) and the note; with "series"
     two bars per label, the first grey and the second in the accent, each with its value, under a legend. Too
     tall for the slide, it scrolls in its box. "type": "line" draws the bars as the points of an ordered series
     (at least 2, in order; any number, a note is refused), joined by a line, with the x labels under the axis
     (as many as fit) and every value written up to 8 points, past that the first, last and highest; with
     "series" two lines. A line whose first and last labels and longest value (with prefix and unit) leave the
     phone's drawing under 160 px of plot is refused: keep each end label to about 20 characters.
    {"kind": "table", "columns": [strings], "rows": [[text or number per column]]}: a simple table; a column
     whose cells are all numbers is right-aligned under its head. On the desktop the first column is the label
     column, as wide as its longest text up to about a third of the table; a number column takes its content
     width; the other columns are equal and share the rest; when equal columns would make the table scroll where
     the browser's own layout fits, they take the split nearest to equal that fits, and only when none does, the
     browser's own; a table is never taller than the browser's own layout draws it; with three columns or more
     whose cells all fit on one line, each column takes an equal share when every column's text fits in one,
     unless that leaves a column but the last more than a quarter of the table empty and the label-first layout
     leaves less. On a phone a table of up to 4 columns of short cells stays a table, laid out the same way with
     the label column up to half the width; a wider one shows one card per row.
  Images and the other evidence kinds do not mix: a diff, chart or table decision carries no images.
  Links: an http:// or https:// URL in any text the deck shows (question, context, why, option labels, captions,
  pros and cons, table cells, the diff and rule_now, chart source, side items and notes, decided answers, and the
  agent's results and replies) becomes a link that opens in a new tab; no other scheme is ever linked, and
  punctuation after the URL (and a closing bracket it never opened) stays outside it. In the diff a URL is marked
  inside its <del> or <ins>; a fold never cuts one. A click on a link never answers or changes the slide.
  The answer row holds still: the line under the answers (Recorded, the agent's status, result and reply) has
  one line of room from the start, and longer text is cut with an ellipsis, whole in its title and in a box that a
  click or Enter on the line opens above it (Esc or a click elsewhere closes it); a chosen answer's tick has its
  room in every button, so no button, comment box or evidence moves or changes size when an answer lands.
  Text values are non-empty strings ("context" and "caption" may be empty); ids match
  [A-Za-z0-9][A-Za-z0-9_.-]{0,63} and are unique within their list (option id "skip" is reserved for skip
  lines); "decisions" and "options" are non-empty; an image is an existing file inside the spec's folder ending in
  .png .jpg .jpeg .webp .gif .svg or .avif.
Ledger records (one JSON line each; `<ledger>` default ledger.jsonl beside the spec):
  pick {kind, decision_id, option_id, label, note, client_ts, ts}; comment {kind, decision_id, note, client_ts,
  ts}; status {kind, decision_id, state, result, reply?, pick_ts?, comment_ts?, ts}; reply {kind, decision_id,
  text, comment_ts?, ts}; done {kind, open, client_ts, ts}. A line without "kind" reads as a pick; option_id "skip"
  reads as a comment. Any record may carry "rid", the page's id for one user action, the same on every retry: the
  server lands it once (it reads the ids back from the ledger on a restart) and readers drop a repeat. "pick_ts"
  is the ts of the pick a status is about and "comment_ts" that of the comment a reply answers; a status or reply
  about a pick or comment since replaced changes nothing on the page. A pick carries the comment box, so like a
  comment it sets the comment (an empty one clears it), and a changed comment drops the reply to the old one.
Routes: GET / (the deck; /d/<n> opens slide n, /summary the summary; the address follows the slide shown),
  GET /img/<sha16> (pictures by content hash; 404 once the file no longer hashes to that name; sent with a bare
  CSP sandbox, so an SVG opened on its own runs no script), POST /api/pick, /api/comment, /api/done (each appends
  one line and returns the decision's state and "gen"; optional "rid"), POST /api/batch {"jobs": [{"kind":
  pick|comment|done, "body"}]} (what a page leaves with: all land in order under one lock, each as its own route
  would, a bad one skipped with its error in "results"), POST /api/status (from this machine only, with header
  X-Deck-Token from the state file), GET /api/events (server-sent events, one per new ledger line, id <gen>:<n>),
  GET /api/state?since=<n>&gen=<g> (the polling fallback, every 2 s), GET /healthz. "gen" is the ledger's
  generation; it goes up when the ledger is replaced or truncated (or a caller holds more lines than it has), and a
  caller holding another one gets {"reset": true} with every line. The page drops a late answer from an older
  generation, and a reset behind the lines it already holds. Every route answers 403 when the Host header names
  anything but the address in the URL with its port (or localhost:<port> and 127.0.0.1:<port> on a loopback
  bind), and every POST answers 403 when it carries an Origin header for another site; a POST with no Origin, as
  from curl, is accepted. So open the deck by the printed URL (or localhost on a loopback bind), not by a DNS
  name. A connection that sends nothing for 30 s in the middle of a request is dropped.
Files: the ledger and the `<ledger stem>.server.json` state file live beside the ledger (default: the spec's folder)
  and the check stamp `<spec stem>.checked.json` beside the spec; the tool keeps no state anywhere else.
Layout: every slide keeps its answer row fully visible; evidence that does not fit scrolls in one bounded box with
  no fade on the desktop, and on a phone the page scrolls with no inner scroll box. Text evidence is as tall as it
  needs, the context line sits under it and the answer row stays at the slide's foot; the context line shows one
  whole line (three on a phone) ending on a word, with Read all only when it is cut. Check a round before showing
  it: `decision_deck_check.py --spec S` (headless Chromium at 1440x900 and 390x844 through Python Playwright; exit
  1 on any problem; a CLEAN run writes the check stamp). It also fetches every http(s) URL in the spec and refuses
  a diff slide with no recap, more than 8 changes, or a change another slide shows.
Stdlib only.
"""
