"""Tests for the decision deck ledger: record kinds, the reducer behind every slide, status binding and the watcher."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_core as core  # noqa: E402
import decision_deck_ledger as lg  # noqa: E402
from test_decision_deck_spec import TempDirCase  # noqa: E402


def pick(did, oid, ts, note="", **extra):
    return {"kind": "pick", "decision_id": did, "option_id": oid, "label": oid, "note": note, "ts": ts, **extra}


def comment(did, note, ts, **extra):
    return {"kind": "comment", "decision_id": did, "note": note, "ts": ts, **extra}


def status(did, state, ts, result="", **extra):
    return {"kind": "status", "decision_id": did, "state": state, "result": result, "ts": ts, **extra}


class LedgerCase(TempDirCase):
    def setUp(self):
        super().setUp()
        self.spec = self.load()
        self.ledger = self.tmp / "ledger.jsonl"

    def write(self, *records, raw=()):
        with self.ledger.open("a", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec) + "\n")
            for line in raw:
                fh.write(line + "\n")


class RecordKindsTest(LedgerCase):
    def test_a_line_without_kind_reads_as_a_pick_and_option_skip_as_a_comment(self):
        self.assertEqual(lg.normalize({"decision_id": "D1", "option_id": "split"})["kind"], "pick")
        self.assertEqual(lg.normalize({"decision_id": "D1", "option_id": "skip", "note": "later"})["kind"], "comment")

    def test_malformed_records_are_dropped_and_file_order_is_kept(self):
        self.write(pick("D1", "split", "t1"), {"kind": "status", "decision_id": "D1", "state": "sleeping"},
                   {"kind": "reply", "decision_id": "D1", "text": "  "}, {"kind": "done", "open": "D1"},
                   comment("D2", "hm", "t2"), raw=["not json", "[1, 2]"])
        self.assertEqual([(r["kind"], r["ts"]) for r in lg.read_records(self.ledger)],
                         [("pick", "t1"), ("comment", "t2")])

    def test_a_missing_ledger_reads_as_empty(self):
        self.assertEqual(lg.read_records(self.tmp / "nothing.jsonl"), [])

    def test_a_repeated_rid_is_read_once(self):
        self.write(pick("D1", "split", "t1", rid="r-12345678"), pick("D1", "banner", "t2", rid="r-12345678"))
        records = lg.read_records(self.ledger)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["option_id"], "split")

    def test_append_pick_writes_one_json_line(self):
        core.append_pick(self.ledger, pick("D1", "split", "t1"))
        core.append_pick(self.ledger, comment("D1", "ok", "t2"))
        lines = self.ledger.read_text().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[1])["note"], "ok")


class ReducerTest(LedgerCase):
    def test_the_latest_pick_wins_and_a_comment_never_replaces_it(self):
        records = [pick("D1", "split", "t1"), pick("D1", "banner", "t2"), comment("D1", "why not both?", "t3")]
        self.assertEqual(lg.current_picks(self.spec, records)["D1"]["option_id"], "banner")
        self.assertEqual(lg.current_skips(self.spec, records)["D1"]["note"], "why not both?")
        self.assertEqual(core.open_decisions(self.spec, lg.current_picks(self.spec, records)), ["D2", "D3", "D4"])

    def test_a_later_pick_or_an_empty_comment_clears_the_note(self):
        base = [comment("D1", "hm", "t1")]
        self.assertNotIn("D1", lg.current_skips(self.spec, base + [pick("D1", "split", "t2")]))
        self.assertNotIn("D1", lg.current_skips(self.spec, base + [comment("D1", "", "t2")]))

    def test_records_outside_the_spec_count_nowhere(self):
        records = [pick("D9", "x", "t1"), pick("D1", "gone", "t2"), pick("D1", "split", "t3")]
        self.assertEqual(list(lg.current_picks(self.spec, records)), ["D1"])
        self.assertTrue(lg.in_spec(self.spec, {"kind": "done", "open": []}))

    def test_deck_state_walks_acting_done_and_a_new_pick_starts_over(self):
        records = [pick("D1", "split", "t1"), status("D1", "acting", "t2", pick_ts="t1")]
        self.assertEqual(lg.deck_state(self.spec, records)["decisions"]["D1"]["status"], "acting")
        records.append(status("D1", "done", "t3", result="Published", pick_ts="t1"))
        d = lg.deck_state(self.spec, records)["decisions"]["D1"]
        self.assertEqual((d["status"], d["result"], d["choice"]), ("done", "Published", "split"))
        records.append(pick("D1", "banner", "t4"))
        d = lg.deck_state(self.spec, records)["decisions"]["D1"]
        self.assertEqual((d["status"], d["result"], d["choice"]), (None, "", "banner"))

    def test_a_status_about_a_replaced_pick_changes_nothing(self):
        records = [pick("D1", "split", "t1"), pick("D1", "banner", "t2"),
                   status("D1", "done", "t3", result="late", pick_ts="t1")]
        self.assertIsNone(lg.deck_state(self.spec, records)["decisions"]["D1"]["status"])

    def test_a_reply_shows_until_its_comment_changes(self):
        records = [comment("D1", "bigger photo?", "t1"),
                   {"kind": "reply", "decision_id": "D1", "text": "Yes, 20% larger.", "comment_ts": "t1", "ts": "t2"}]
        self.assertEqual(lg.deck_state(self.spec, records)["decisions"]["D1"]["reply"], "Yes, 20% larger.")
        records.append(comment("D1", "and darker?", "t3"))
        d = lg.deck_state(self.spec, records)["decisions"]["D1"]
        self.assertEqual((d["comment"], d["reply"]), ("and darker?", ""))

    def test_a_pick_carries_the_comment_box(self):
        records = [comment("D1", "hm", "t1"), pick("D1", "split", "t2", note="fine, with a darker photo")]
        self.assertEqual(lg.deck_state(self.spec, records)["decisions"]["D1"]["comment"], "fine, with a darker photo")

    def test_done_and_the_record_count(self):
        records = [pick("D1", "split", "t1"), {"kind": "done", "open": ["D2"], "ts": "t2"}]
        state = lg.deck_state(self.spec, records)
        self.assertEqual(state["done"], {"open": ["D2"], "ts": "t2"})
        self.assertEqual(state["n"], 2)


class BuildersTest(LedgerCase):
    def test_make_record_validates_against_the_spec(self):
        rec = lg.make_record(self.spec, "D1", "split", "  looks good  ", "c1")
        self.assertEqual((rec["kind"], rec["label"], rec["note"], rec["client_ts"]), ("pick", "Split", "looks good", "c1"))
        for did, oid, note in (("D9", "split", ""), ("D1", "nope", ""), ("D1", "split", "x" * 501)):
            with self.subTest(did=did, oid=oid), self.assertRaises(ValueError):
                lg.make_record(self.spec, did, oid, note, None)

    def test_a_note_is_dropped_where_the_decision_takes_none(self):
        self.assertEqual(lg.make_record(self.spec, "D4", "early", "a note", None)["note"], "")
        with self.assertRaises(ValueError):
            lg.make_comment(self.spec, "D4", "a note", None)

    def test_a_skip_line_needs_its_note_and_keeps_the_kindless_shape(self):
        rec = lg.make_record(self.spec, "D1", "skip", "decide later", None)
        self.assertNotIn("kind", rec)
        self.assertEqual(rec["label"], core.SKIP_LABEL)
        with self.assertRaises(ValueError):
            lg.make_record(self.spec, "D1", "skip", "", None)

    def test_make_status_and_make_reply(self):
        rec = lg.make_status(self.spec, "D1", "done", "Published", reply="Thanks", pick_ts="t1", comment_ts="t0")
        self.assertEqual({k: rec[k] for k in ("state", "result", "reply", "pick_ts", "comment_ts")},
                         {"state": "done", "result": "Published", "reply": "Thanks", "pick_ts": "t1", "comment_ts": "t0"})
        with self.assertRaises(ValueError):
            lg.make_status(self.spec, "D1", "sleeping")
        with self.assertRaises(ValueError):
            lg.make_reply(self.spec, "D1", "   ")

    def test_make_done_lists_the_open_decisions(self):
        rec = lg.make_done(self.spec, [pick("D1", "split", "t1"), pick("D3", "free", "t2")], "c1")
        self.assertEqual(rec["open"], ["D2", "D4"])


class StatusPickTest(LedgerCase):
    def test_which_pick_a_status_names(self):
        records = [pick("D1", "split", "t1"), pick("D1", "banner", "t2")]
        self.assertEqual(lg.status_pick(self.spec, records, "D1", "acting"), "t2")
        self.assertEqual(lg.status_pick(self.spec, records, "D1", "done", option="split"), "t1")
        self.assertEqual(lg.status_pick(self.spec, records, "D1", "done", pick_ts="t1"), "t1")
        with self.assertRaises(ValueError):
            lg.status_pick(self.spec, records, "D1", "done", pick_ts="t9")
        with self.assertRaises(ValueError):
            lg.status_pick(self.spec, records, "D1", "done", option="nope")

    def test_done_follows_the_pick_the_last_acting_line_named(self):
        records = [pick("D1", "split", "t1"), status("D1", "acting", "t2", pick_ts="t1"), pick("D1", "banner", "t3")]
        self.assertEqual(lg.status_pick(self.spec, records, "D1", "done"), "t1")
        self.assertEqual(lg.status_pick(self.spec, records, "D1", "acting"), "t3")
        self.assertIsNone(lg.status_pick(self.spec, [], "D2", "acting"))


class WatcherTest(LedgerCase):
    def test_lines_for_each_kind_and_all_picked_once(self):
        w = lg.Watcher(self.ledger, self.spec)
        self.assertEqual(w.poll(), [])                              # no ledger yet
        self.write(pick("D1", "split", "2026-01-02T03:04:05.000000Z", note="ok"), comment("D2", "hm", "t2"),
                   status("D1", "done", "t3"), {"kind": "done", "open": ["D3", "D4"], "ts": "t4"})
        out = w.poll()
        self.assertEqual(len(out), 3)                               # the agent's status line is not echoed
        self.assertTrue(out[0].startswith('PICK D1=split (Split) note="ok" at '))
        self.assertTrue(out[0].endswith(" pick=2026-01-02T03:04:05.000000Z"))
        self.assertTrue(out[1].startswith('COMMENT D2 note="hm" at '))
        self.assertTrue(out[2].startswith("DONE open=D3,D4 at "))
        self.write(pick("D2", "yes", "t5"), pick("D3", "free", "t6"), pick("D4", "early", "t7"))
        self.assertEqual(w.poll()[-1], "ALL_PICKED")
        self.write(pick("D4", "late", "t8"))
        self.assertNotIn("ALL_PICKED", w.poll())

    def test_a_partial_line_waits_and_a_truncated_ledger_starts_over(self):
        w = lg.Watcher(self.ledger, self.spec)
        with self.ledger.open("w") as fh:
            fh.write(json.dumps(pick("D1", "split", "t1"))[:20])
        self.assertEqual(w.poll(), [])
        self.ledger.write_text(json.dumps(pick("D1", "split", "t1")) + "\n")
        self.assertEqual(len(w.poll()), 1)
        self.ledger.write_text("")
        self.assertEqual(w.poll(), [])                              # smaller than what was read: start over
        self.write(pick("D1", "banner", "t2"))
        self.assertTrue(w.poll()[0].startswith("PICK D1=banner"))

    def test_without_a_spec_no_all_picked(self):
        self.write(*(pick(d, o, f"t{i}") for i, (d, o) in enumerate(
            [("D1", "split"), ("D2", "yes"), ("D3", "free"), ("D4", "early")])))
        self.assertNotIn("ALL_PICKED", lg.Watcher(self.ledger, None).poll())

    def test_local_time_falls_back_to_the_raw_value(self):
        self.assertEqual(core.local_time("not a stamp"), "not a stamp")
        self.assertRegex(core.local_time("2026-01-02T03:04:05.000000Z"), r"^\d{1,2}:\d\d [AP]M")


if __name__ == "__main__":
    unittest.main()
