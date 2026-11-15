"""Tests for the decision_deck.py subcommands, run as a user runs them: help, status, watch, act, reply, text, asks
and serve (the bind rule, the stamp warning, a live round stopped with SIGTERM)."""
import json
import os
import signal
import subprocess
import sys
import threading
import time
import unittest
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_core as core  # noqa: E402
import decision_deck_ledger as lg  # noqa: E402
import decision_deck_server as server  # noqa: E402
import decision_deck_stamp as stamp  # noqa: E402
from test_decision_deck_server import QuietHandler  # noqa: E402
from test_decision_deck_spec import TempDirCase  # noqa: E402

TOOL = Path(__file__).resolve().parent / "decision_deck.py"


def pick(did, oid, ts):
    return {"kind": "pick", "decision_id": did, "option_id": oid, "label": oid, "note": "", "ts": ts}


class CliCase(TempDirCase):
    def setUp(self):
        super().setUp()
        self.ledger = self.spec_path.parent / "ledger.jsonl"

    def run_tool(self, *args, timeout=20):
        return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True,
                              timeout=timeout, cwd=self.tmp)

    def write(self, *records):
        with self.ledger.open("a", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec) + "\n")


class HelpTest(CliCase):
    def test_every_subcommand_has_help(self):
        for args in ([], ["serve"], ["watch"], ["status"], ["act"], ["reply"], ["text"], ["asks"]):
            with self.subTest(args):
                out = self.run_tool(*args, "--help")
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertIn("usage: decision_deck.py", out.stdout)


class StatusAndWatchTest(CliCase):
    def test_status_lists_picks_states_comments_and_open_decisions(self):
        self.write(pick("D1", "split", "t1"),
                   {"kind": "status", "decision_id": "D1", "state": "done", "result": "Shipped", "ts": "t2"},
                   {"kind": "comment", "decision_id": "D2", "note": "tone it down", "ts": "t3"})
        out = self.run_tool("status", "--spec", self.spec_path)
        self.assertEqual(out.returncode, 0, out.stderr)
        lines = out.stdout.splitlines()
        self.assertEqual(lines[0], "Shop relaunch: 1 of 4 picked")
        self.assertTrue(lines[1].startswith("PICK D1=split (Split)"))
        self.assertEqual(lines[2], 'STATE D1 done result="Shipped"')
        self.assertIn("OPEN D2 (Returns)", lines)
        data = json.loads(self.run_tool("status", "--spec", self.spec_path, "--json").stdout)
        self.assertEqual((list(data["picked"]), data["open"], data["all_picked"]), (["D1"], ["D2", "D3", "D4"], False))
        self.assertEqual(data["skipped"]["D2"]["note"], "tone it down")
        self.assertEqual(data["states"], {"D1": {"state": "done", "result": "Shipped"}})   # the STATE lines

    def test_status_refuses_a_bad_spec(self):
        self.spec_path.write_text("{}")
        out = self.run_tool("status", "--spec", self.spec_path)
        self.assertEqual(out.returncode, 2)
        self.assertIn("spec is invalid", out.stderr)

    def test_watch_prints_each_record_and_stops_once_all_are_picked_with_no_server(self):
        self.write(pick("D1", "split", "t1"), pick("D2", "yes", "t2"), pick("D3", "free", "t3"), pick("D4", "late", "t4"))
        out = self.run_tool("watch", "--spec", self.spec_path, "--poll", "0.05")
        self.assertEqual(out.returncode, 0, out.stderr)
        lines = out.stdout.splitlines()
        self.assertEqual([ln.split()[0] for ln in lines], ["PICK"] * 4 + ["ALL_PICKED", "SERVER_STOPPED"])

    def test_watch_stops_with_the_open_ids_once_a_server_it_saw_has_stopped(self):
        self.write(pick("D1", "split", "t1"))
        state = core.state_path(self.ledger)
        state.write_text(json.dumps({"pid": os.getpid()}))     # a live pid: the watch sees a running server
        proc = subprocess.Popen([sys.executable, str(TOOL), "watch", "--spec", self.spec_path, "--poll", "0.05",
                                 "--max-hours", "0.003"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertTrue(proc.stdout.readline().startswith("PICK D1=split"))  # read after it saw the server running
        state.unlink()
        out, err = proc.communicate(timeout=20)
        self.assertEqual((proc.returncode, out.strip()), (0, "SERVER_STOPPED open=D2,D3,D4"), err)

    def test_watch_keeps_waiting_with_decisions_open_and_no_server_ever_seen(self):
        self.write(pick("D1", "split", "t1"))
        out = self.run_tool("watch", "--spec", self.spec_path, "--poll", "0.05", "--max-hours", "0.0001")
        self.assertEqual(out.returncode, 3)
        self.assertEqual(out.stdout.splitlines()[-1], "WATCH_TIMEOUT")

    def test_watch_times_out(self):
        out = self.run_tool("watch", "--spec", self.spec_path, "--poll", "0.05", "--max-hours", "0.00003")
        self.assertEqual((out.returncode, out.stdout.strip()), (3, "WATCH_TIMEOUT"))


class ActAndReplyTest(CliCase):
    def test_act_writes_to_the_ledger_without_a_server_and_names_the_pick(self):
        self.write(pick("D1", "split", "t1"), pick("D3", "free", "t2"))
        out = self.run_tool("act", "D1", "D3", "--spec", self.spec_path, "--state", "done", "--result", "Published")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.splitlines(), ['STATUS D1 done result="Published" via ledger',
                                                   'STATUS D3 done result="Published" via ledger'])
        statuses = [r for r in lg.read_records(self.ledger) if r["kind"] == "status"]
        self.assertEqual([(r["decision_id"], r["pick_ts"]) for r in statuses], [("D1", "t1"), ("D3", "t2")])

    def test_act_writes_nothing_when_one_id_fails(self):
        self.write(pick("D1", "split", "t1"))
        out = self.run_tool("act", "D1", "D9", "--spec", self.spec_path, "--state", "done")
        self.assertEqual(out.returncode, 2)
        self.assertIn("D9: unknown decision", out.stderr)
        self.assertEqual([r["kind"] for r in lg.read_records(self.ledger)], ["pick"])
        out = self.run_tool("act", "D1", "--spec", self.spec_path, "--state", "done", "--pick-ts", "t9")
        self.assertEqual(out.returncode, 2)
        self.assertIn("has no pick at t9", out.stderr)

    def test_act_warns_when_a_newer_pick_exists(self):
        self.write(pick("D1", "split", "t1"), pick("D1", "banner", "t2"))
        out = self.run_tool("act", "D1", "--spec", self.spec_path, "--state", "failed", "--pick", "split",
                            "--result", "Photo too dark")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("a newer pick (banner at t2)", out.stderr)

    def test_reply_binds_to_the_comment_shown(self):
        self.write({"kind": "comment", "decision_id": "D2", "note": "why one day?", "ts": "c1"})
        out = self.run_tool("reply", "D2", "--spec", self.spec_path, "--text", "It keeps refunds rare.")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), 'REPLY D2 text="It keeps refunds rare." via ledger')
        self.assertEqual(lg.read_records(self.ledger)[-1]["comment_ts"], "c1")
        self.assertEqual(self.run_tool("reply", "D9", "--spec", self.spec_path, "--text", "x").returncode, 2)

    def test_act_goes_through_a_running_server(self):
        spec = self.load()
        srv = server.make_server(spec, self.ledger, "127.0.0.1", 0, grace_s=60, max_s=60)
        srv.RequestHandlerClass = QuietHandler
        thread = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        thread.start()
        try:
            srv.record({"decision_id": "D1", "option_id": "split"})
            out = self.run_tool("act", "D1", "--spec", self.spec_path, "--state", "acting")
            self.assertEqual(out.stdout.strip(), 'STATUS D1 acting result="" via server')
            self.assertEqual(lg.deck_state(spec, lg.read_records(self.ledger))["decisions"]["D1"]["status"], "acting")
        finally:
            srv.finished.set()
            srv.shutdown()
            srv.server_close()
            server.remove_own_state(self.ledger)


class TextAndAsksTest(CliCase):
    def test_text_writes_every_slide_in_order(self):
        out = self.run_tool("text", "--spec", self.spec_path)
        self.assertEqual(out.returncode, 0, out.stderr)
        text = out.stdout
        for needle in ("[Cover]\nShop relaunch", "[Slide 1 of 4: decision D1", "Column split: Side by side (1 picture)",
                       "Was: Exchanges only on the day of purchase.", "Free over $25: 310 orders (highlighted)",
                       "Option | Weekdays | Staff", "Early | 6:30 to 14:00 | 2", "1. Split (Recommended)",
                       "[Decided in earlier rounds]\nOrdering: Pickup only at launch"):
            self.assertIn(needle, text)
        self.assertLess(text.index("decision D1"), text.index("decision D4"))
        target = self.tmp / "deck.txt"
        out = self.run_tool("text", "--spec", self.spec_path, "--out", target)
        self.assertTrue(out.stdout.startswith("TEXT "))
        self.assertEqual(target.read_text(), text)

    def test_asks_writes_each_ask_with_lettered_options(self):
        out = self.run_tool("asks", "--spec", self.spec_path, "--url", "http://127.0.0.1:9/")
        self.assertEqual(out.returncode, 0, out.stderr)
        blocks = out.stdout.strip().split("\n\n")
        self.assertEqual(blocks[0], "Deck: http://127.0.0.1:9/")
        d1 = blocks[1].splitlines()
        self.assertEqual(d1[0], "D1 (Hero): Which hero layout?")
        self.assertEqual(d1[1], "Recommendation: D1a (Split). The headline stays readable.")
        self.assertEqual(d1[-2:], ["D1a. Split", "D1b. Banner"])
        self.assertIn("No recommendation. Your call.", blocks[4])
        self.assertIn("Source: Twelve weeks of orders", blocks[3])
        self.assertNotIn("Ordering", out.stdout)                        # the decided list is no ask
        self.assertNotIn("**", out.stdout)


class ServeTest(CliCase):
    def test_serve_refuses_every_interface_and_public_addresses(self):
        for host in ("0.0.0.0", "::", "8.8.8.8"):
            with self.subTest(host):
                out = self.run_tool("serve", "--spec", self.spec_path, "--host", host)
                self.assertEqual(out.returncode, 2)
                self.assertIn("refusing to bind", out.stderr)
        self.assertFalse(self.ledger.exists())

    def test_require_checked_refuses_an_unchecked_spec(self):
        out = self.run_tool("serve", "--spec", self.spec_path, "--require-checked")
        self.assertEqual(out.returncode, 2)
        self.assertIn("refused: no check stamp", out.stderr)

    def test_a_live_round_warns_once_records_and_stops_on_sigterm(self):
        proc = subprocess.Popen([sys.executable, str(TOOL), "serve", "--spec", str(self.spec_path), "--port", "0"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.tmp)
        try:
            url = proc.stdout.readline().split()[1]
            self.assertTrue(url.startswith("http://127.0.0.1:"))
            with urllib.request.urlopen(url, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
            req = urllib.request.Request(url + "api/pick", method="POST", headers={"Content-Type": "application/json"},
                                         data=json.dumps({"decision_id": "D1", "option_id": "split"}).encode())
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
            self.assertTrue(core.server_running(self.ledger))
            proc.send_signal(signal.SIGTERM)
            out, err = proc.communicate(timeout=10)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.communicate()
        self.assertEqual(proc.returncode, 0)
        self.assertIn("STOPPED terminated", out)
        self.assertEqual(err.count("warning: no check stamp"), 1)
        self.assertFalse(core.state_path(self.ledger).exists())
        self.assertEqual(lg.current_picks(self.load(), lg.read_records(self.ledger))["D1"]["option_id"], "split")


class StampTest(CliCase):
    def test_a_stamp_matches_until_the_spec_or_a_picture_changes(self):
        spec = self.load()
        self.assertIn("no check stamp", stamp.stamp_problem(spec))
        stamp.write_stamp(spec, stamp.digest(spec))
        self.assertEqual(stamp.stamp_problem(spec), "")
        self.assertTrue(stamp.serve_gate(spec, require_checked=True))
        (self.spec_path.parent / "img" / "b.svg").write_bytes(b"<svg/>")
        self.assertIn("changed since", stamp.stamp_problem(self.load()))

    def test_a_change_during_the_check_writes_no_stamp(self):
        spec = self.load()
        checked = stamp.digest(spec)
        time.sleep(0.01)
        self.spec_path.write_text(self.spec_path.read_text().replace("Shop relaunch", "Shop relaunch, again"))
        with self.assertRaises(stamp.InputsChanged):
            stamp.write_stamp(spec, checked)
        self.assertFalse(stamp.stamp_path(spec).exists())


if __name__ == "__main__":
    unittest.main()
