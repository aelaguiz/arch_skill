# Running a Round

Read this before serving a deck to another device, or when something in a
round surprises you. Every output line and flag is in the tool's `--help`.

## Contents

- Requirements
- Where the owner looks: the bind address
- Files a round leaves
- Reading `watch` and `status`
- Reporting back
- An answer given in chat
- Ending a round

## Requirements

`decision_deck.py` needs only `python3` (3.10 or later). The layout checker,
`decision_deck_check.py`, renders the deck in headless Chromium through Python
Playwright. Without it the checker exits 2 and says so; install it once with:

```bash
python3 -m pip install playwright && python3 -m playwright install chromium
```

## Where the owner looks: the bind address

`serve` binds `127.0.0.1` by default, so the deck opens only on the machine
running it. When the owner looks from a phone or another computer, pass this
machine's address on a private network you share with that device:

```bash
nohup python3 <this skill>/scripts/decision_deck.py serve --spec <dir>/spec.json --require-checked --host <private address> > <dir>/server.log 2>&1 &
```

`serve --help` lists the address ranges it accepts (home and work networks,
and the range private mesh VPNs commonly use); it refuses `0.0.0.0` and
public addresses. Anyone who can reach that address can open the deck and
answer it, so serve only on a network you trust. `--port` fixes the port
instead of taking a free one, and `--source "<text>"` puts a line under the
title saying who is asking.

Links work the same way. The checker fetches every `http(s)` link in the spec
and refuses one that does not answer (`DEADLINK`); a link to `localhost` only
warns, because it opens only on a machine where that server runs. Link to an
address the owner's device can reach.

## Files a round leaves

Beside the spec:

- `spec.checked.json`: the check stamp, written by a `CLEAN` check. It covers
  the spec and every picture, so any edit needs a new check before
  `serve --require-checked` accepts it.
- `ledger.jsonl`: every pick, comment, Done press, status and reply, one JSON
  line each. It is the record of the round; keep it. `--ledger` puts it
  elsewhere, and every subcommand then takes the same `--ledger`.
- `ledger.server.json`: the running server's URL, process id and token, kept
  private to your user. It goes away when the server stops.

In the `--out` folder of the checker: one PNG per slide and width
(`desktop-slide1.png`, `phone-slide1.png`, and so on) and `png-manifest.json`,
which lets a rerun name the PNGs that changed. The tool writes nothing else.
Your own `server.log` and `deck-text.txt` are whatever you redirect.

## Reading `watch` and `status`

`watch --spec <dir>/spec.json` prints what is already in the ledger, then one
line per new event:

```text
PICK D1=split (Split: photo left, text right) note="" at <local time> pick=<ts>
COMMENT D2 note="Can we say two days instead?" at <local time>
ALL_PICKED
SERVER_STOPPED
```

The `pick=` value names that exact pick for `act --pick-ts`. `ALL_PICKED`
prints once, the first time every decision has an answer; `SERVER_STOPPED`
prints and `watch` exits once the server has stopped. When you restart a watch
after handling the earlier lines, add `--from-end`. Your own `act` and `reply`
lines are not echoed.

`status` prints the current answer per decision (`PICK`), what you reported
about it (`STATE D1 done result="..."`), any newer comment (`COMMENT`) and the
decisions still open (`OPEN`); `--json` gives the same for a script. Use it
rather than reading the ledger file yourself.

## Reporting back

Several decisions with the same outcome share one `act`, with one `--pick-ts`
per decision in the same order:

```bash
python3 <this skill>/scripts/decision_deck.py act D3 D4 --spec <dir>/spec.json --state done --result "Set on the live site" --pick-ts <ts of D3> --pick-ts <ts of D4>
```

Always pass `--pick-ts`. Without it, a `done` line attaches to the pick your
last `acting` line named; if the owner changed the answer in between, your
result lands on the old answer, the slide shows the new one with no status,
and only a stderr note says so. `act` and `reply` go through the running server
and appear on the page within two seconds; once it has stopped they go
straight to the ledger.

## An answer given in chat

The `asks` text letters each decision's options in spec order: `D1a` is the
first option of D1, `D1b` the second. When the owner answers in chat, map the
letter to the option's id in the spec. While the deck is served, record the
answer through the page's own pick route, so the slide, `watch` and `status`
all show it:

```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"decision_id": "D1", "option_id": "split", "note": "Answered in chat"}' <url>api/pick
```

`<url>` is the `URL` line from the server log, which ends in `/`. The pick then
arrives as a `PICK` line like any other, with the `pick=` value to act on. Once
the server has stopped, append one pick record to the ledger instead (its
fields are under Ledger records in `--help`) if `status` should show it.

## Ending a round

The server stops itself once every decision is picked and its grace period
(`--grace-min`, 15 minutes by default) has passed with nothing new, or at its
maximum lifetime (`--max-hours`, 24 by default). To stop it sooner, send
SIGINT or SIGTERM to the process id the log prints on its second line.
`serve` and `watch` read the spec once at start, so after editing a spec,
check it again and restart both.
