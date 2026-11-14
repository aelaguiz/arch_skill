"""`decision_deck.py act`: the agent tells one or more slides what it did about their decisions.

`act D1 [D2 ...] --spec S --state acting|done|failed [--result "..."]` writes one status record per decision
(decision_deck_ledger.make_status). Every decision is checked first (it exists, its pick resolves, the state and texts
are valid) and nothing is written unless all pass; with several ids the error names each failing id.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_core import decision_by_id  # noqa: E402
from decision_deck_ledger import current_comment, decision_picks, make_status, read_records, status_pick  # noqa: E402


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def build(args, spec: dict, records: list[dict]) -> tuple[list[dict], list[str]]:
    """(the status records to write, in id order; the error lines). Records only when there are no errors."""
    ids = args.decision
    named = args.pick_ts if args.pick_ts is not None else [None] * len(ids)
    if len(named) != len(ids):
        return [], [f"decision_deck act: {_plural(len(ids), 'decision')} but {len(named)} --pick-ts; "
                    f"give one per decision, in the same order"]
    built, errors = [], []
    for did, ts in zip(ids, named):
        try:
            if decision_by_id(spec, did)[1] is None:
                raise ValueError(f"unknown decision {did!r}")
            pick_ts = status_pick(spec, records, did, args.state, args.pick, ts)
            built.append(make_status(spec, did, args.state, args.result or "", args.reply, pick_ts,
                                     current_comment(spec, records, did)))
        except ValueError as exc:       # several ids name the failing id first
            errors.append(f"decision_deck act: {did}: {exc}" if len(ids) > 1 else f"decision_deck act: {exc}")
    return ([] if errors else built), errors


def cmd_act(args, load_or_exit, ledger_for, send) -> int:
    """load_or_exit, ledger_for and send are decision_deck's spec loader, ledger path and server-or-ledger writer."""
    spec = load_or_exit(args.spec)
    records = read_records(ledger_for(args))
    built, errors = build(args, spec, records)
    if errors:
        sys.stderr.write("".join(line + "\n" for line in errors))
        return 2
    for rec in built:
        pick_ts = rec.get("pick_ts")
        picks = decision_picks(spec, records, rec["decision_id"])
        at = [i for i, r in enumerate(picks) if r.get("ts") == pick_ts]
        later = picks[at[-1] + 1:] if at else []
        if later:       # the line is about older work; the slide keeps showing the newer answer as it is
            sys.stderr.write(f"decision_deck act: this line is about the pick at {pick_ts}; the slide shows a newer "
                             f"pick ({later[-1]['option_id']} at {later[-1].get('ts')}). Name another with "
                             f"--pick-ts.\n")
        payload = {k: rec.get(k) for k in ("decision_id", "state", "result", "reply", "pick_ts", "comment_ts")}
        via = send(args, "status", payload, rec)
        print(f"STATUS {rec['decision_id']} {rec['state']} result={json.dumps(rec['result'], ensure_ascii=False)} "
              f"via {via}", flush=True)
    return 0


def add_act_parser(sub, load_or_exit, ledger_for, send) -> None:
    """Register the `act` subcommand on decision_deck.py's subparsers (its helpers passed in, so no import cycle)."""
    a = sub.add_parser("act", help="the agent reports what it did about one or more decisions",
                       description="Append a status line for each decision named: acting, done with its one-line "
                                   "result, or failed with the reason. Several ids share one --state, --result and "
                                   "--reply and get one line each, the line a single act writes; every id is checked "
                                   "first and nothing is written unless all pass. The line names the pick it is "
                                   "about, so a result for an answer the owner has since changed never marks the new "
                                   "one: --pick-ts <ts> names it exactly (the pick=<ts> ending its PICK line), given "
                                   "once per decision in the same order; --pick <option> names that option's latest pick "
                                   "on each; without either, acting takes the latest pick, and done or failed the "
                                   "pick the decision's most recent acting line named (also after a done or failed "
                                   "for it, so a corrected result stays with that work), else the latest pick. A "
                                   "note on stderr says when a newer pick exists than the one named. A --reply binds "
                                   "to the comment shown now. Goes through the running server (POST /api/status "
                                   "with the state file's token), else straight to the ledger. Prints one 'STATUS "
                                   "<decision> <state> result=\"...\" via server|ledger' per decision. Exit 2 for a "
                                   "bad spec, decision, state, --pick or --pick-ts, or a --pick-ts count that does "
                                   "not match the ids; the error names each failing id.")
    a.add_argument("decision", nargs="+", help="decision id; several share the one state and result")
    a.add_argument("--spec", required=True, help="spec JSON")
    a.add_argument("--ledger", help="JSONL ledger (default: ledger.jsonl beside the spec)")
    a.add_argument("--state", required=True, help="acting, done or failed")
    a.add_argument("--result", default="", help='one line: what was done ("Published the new hours") or why it failed')
    a.add_argument("--reply", help="optional answer to the owner's comment, shown under it")
    which = a.add_mutually_exclusive_group()
    which.add_argument("--pick-ts", metavar="TS", action="append",      # one value per flag: never swallows an id
                       help="the exact pick acted on: the pick=<ts> at the end of its PICK line; give the flag once "
                            "per decision, in the same order")
    which.add_argument("--pick", metavar="OPTION",
                       help="the option id of the answer acted on (its latest pick); default: see above")
    a.set_defaults(func=lambda args: cmd_act(args, load_or_exit, ledger_for, send))
