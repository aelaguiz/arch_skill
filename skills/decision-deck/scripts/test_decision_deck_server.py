"""Tests for the decision deck server on loopback: the page, pictures, every API route, the token, resets and the timer."""
import json
import os
import socket
import stat
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_core as core  # noqa: E402
import decision_deck_ledger as lg  # noqa: E402
import decision_deck_routes as routes  # noqa: E402
import decision_deck_server as server  # noqa: E402
from decision_deck_routes import Handler  # noqa: E402
from test_decision_deck_spec import TempDirCase  # noqa: E402


def request(url, payload=None, headers=None, ctype="application/json", method=None):
    """(status, body bytes, headers) for a GET, or a POST when `payload` is given."""
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data is not None else "GET"),
                                 headers={"Content-Type": ctype, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers


def post(url, payload, headers=None, ctype="application/json"):
    code, body, _ = request(url, payload, headers, ctype)
    return code, json.loads(body or b"{}")


class QuietHandler(Handler):
    def log_message(self, fmt, *args):
        pass


class LiveCase(TempDirCase):
    GRACE_S, MAX_S = 60, 60

    def setUp(self):
        super().setUp()
        self.spec = self.load()
        self.ledger = self.tmp / "ledger.jsonl"
        self.srv = server.make_server(self.spec, self.ledger, "127.0.0.1", 0, grace_s=self.GRACE_S, max_s=self.MAX_S)
        self.srv.RequestHandlerClass = QuietHandler
        self.thread = threading.Thread(target=self.srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)

    def stop(self):
        self.srv.finished.set()
        self.srv.shutdown()
        self.srv.server_close()
        server.remove_own_state(self.ledger)

    def kinds(self):
        return [r["kind"] for r in lg.read_records(self.ledger)]


class PageTest(LiveCase):
    def test_the_deck_page_and_its_routes(self):
        code, body, _ = request(self.srv.url)
        html = body.decode()
        self.assertEqual(code, 200)
        self.assertIn("<title>Shop relaunch</title>", html)
        self.assertEqual(html.count('<section class="slide'), 6)       # cover, four decisions, summary
        self.assertEqual(request(self.srv.url + "d/4")[0], 200)
        self.assertEqual(request(self.srv.url + "summary")[0], 200)
        self.assertEqual(request(self.srv.url + "d/5")[0], 404)
        code, body, _ = request(self.srv.url + "healthz")
        self.assertEqual(json.loads(body)["open"], ["D1", "D2", "D3", "D4"])

    def test_pictures_are_served_by_content_hash_and_sandboxed(self):
        sha = self.srv.image_of["img/a.svg"]
        code, body, headers = request(self.srv.url + "img/" + sha)
        self.assertEqual((code, headers["Content-Type"]), (200, "image/svg+xml"))
        self.assertEqual(headers["Content-Security-Policy"], "sandbox")
        self.assertTrue(body.startswith(b"<svg"))
        (self.spec_path.parent / "img" / "a.svg").write_bytes(b"<svg/>")    # changed since start: never served
        self.assertEqual(request(self.srv.url + "img/" + sha)[0], 404)

    def test_nothing_outside_the_routes_is_served(self):
        for path in ("files/spec.json", "img/../spec.json", "..%2fspec.json", "ledger.jsonl", "img/0123456789abcdef"):
            with self.subTest(path):
                self.assertEqual(request(self.srv.url + path)[0], 404)

    def test_the_state_file_is_owner_only_and_names_the_server(self):
        path = core.state_path(self.ledger)
        data = json.loads(path.read_text())
        self.assertEqual((data["url"], data["pid"]), (self.srv.url, os.getpid()))
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertTrue(core.server_running(self.ledger))


class ApiTest(LiveCase):
    def test_pick_comment_and_done_each_append_one_line(self):
        code, body = post(self.srv.url + "api/comment", {"decision_id": "D1", "note": "bigger photo?", "ts": "c1"})
        self.assertEqual((code, body["decision"]["comment"]), (200, "bigger photo?"))
        code, body = post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split", "note": "", "ts": "c2"})
        self.assertEqual((code, body["decision"]["choice"], body["next"]), (200, "split", "/d/2"))
        self.assertFalse(body["all_picked"])
        code, body = post(self.srv.url + "api/done", {"ts": "c3"})
        self.assertEqual((code, body["record"]["open"]), (200, ["D2", "D3", "D4"]))
        self.assertEqual(self.kinds(), ["comment", "pick", "done"])
        self.assertEqual(lg.read_records(self.ledger)[0]["client_ts"], "c1")

    def test_bad_requests_are_refused_and_record_nothing(self):
        self.assertEqual(post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "nope"})[0], 400)
        self.assertEqual(post(self.srv.url + "api/comment", {"decision_id": "D9", "note": "x"})[0], 400)
        self.assertEqual(post(self.srv.url + "api/comment", {"decision_id": "D1", "note": "x"}, ctype="text/plain")[0], 415)
        self.assertEqual(post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split", "rid": "bad id"})[0], 400)
        self.assertEqual(post(self.srv.url + "api/nothing", {})[0], 404)
        self.assertEqual(self.kinds(), [])

    def test_a_retried_rid_lands_once(self):
        payload = {"decision_id": "D1", "option_id": "split", "rid": "p-0000000001"}
        first, second = post(self.srv.url + "api/pick", payload), post(self.srv.url + "api/pick", payload)
        self.assertEqual(first[1]["record"], second[1]["record"])
        self.assertEqual(self.kinds(), ["pick"])
        self.assertEqual(post(self.srv.url + "api/comment",
                              {"decision_id": "D1", "note": "x", "rid": "p-0000000001"})[0], 400)

    def test_the_last_pick_moves_to_the_summary(self):
        for did, oid in (("D1", "split"), ("D2", "yes"), ("D3", "free")):
            post(self.srv.url + "api/pick", {"decision_id": did, "option_id": oid})
        code, body = post(self.srv.url + "api/pick", {"decision_id": "D4", "option_id": "late"})
        self.assertEqual((body["next"], body["all_picked"], body["open"]), ("/summary", True, []))

    def test_batch_lands_in_order_and_skips_a_bad_job(self):
        jobs = [{"kind": "pick", "body": {"decision_id": "D1", "option_id": "split", "rid": "b-0000000001"}},
                {"kind": "comment", "body": {"decision_id": "D9", "note": "x"}},
                {"kind": "comment", "body": {"decision_id": "D2", "note": "tone it down", "rid": "b-0000000002"}},
                {"kind": "done", "body": {"rid": "b-0000000003"}}]
        code, body = post(self.srv.url + "api/batch", {"jobs": jobs})
        self.assertEqual(code, 200)
        self.assertEqual([r["status"] for r in body["results"]], [200, 400, 200, 200])
        self.assertEqual(self.kinds(), ["pick", "comment", "done"])
        post(self.srv.url + "api/batch", {"jobs": jobs})                    # the page retried: nothing new
        self.assertEqual(self.kinds(), ["pick", "comment", "done"])
        self.assertEqual(post(self.srv.url + "api/batch", {"jobs": []})[0], 400)

    def test_status_needs_the_token_from_the_state_file(self):
        post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split"})
        line = {"kind": "status", "decision_id": "D1", "state": "done", "result": "Published"}
        self.assertEqual(post(self.srv.url + "api/status", line)[0], 403)
        self.assertEqual(post(self.srv.url + "api/status", line, {"X-Deck-Token": "wrong"})[0], 403)
        token = core.read_server_state(self.ledger)["token"]
        code, body = post(self.srv.url + "api/status", line, {"X-Deck-Token": token})
        self.assertEqual((code, body["decision"]["status"], body["decision"]["result"]), (200, "done", "Published"))
        self.assertEqual(lg.read_records(self.ledger)[-1]["pick_ts"], lg.read_records(self.ledger)[0]["ts"])
        reply = {"kind": "reply", "decision_id": "D1", "text": "Done."}
        self.assertEqual(post(self.srv.url + "api/status", reply, {"X-Deck-Token": token})[0], 200)
        bad = {"kind": "pick", "decision_id": "D1", "option_id": "banner"}
        self.assertEqual(post(self.srv.url + "api/status", bad, {"X-Deck-Token": token})[0], 400)

    def test_state_since_returns_new_lines_and_a_reset_after_a_replaced_ledger(self):
        post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split"})
        post(self.srv.url + "api/comment", {"decision_id": "D2", "note": "hm"})
        state = json.loads(request(self.srv.url + "api/state?since=1")[1])
        self.assertEqual((state["n"], len(state["lines"]), state["lines"][0]["kind"]), (2, 1, "comment"))
        self.assertEqual(state["picked"]["D1"]["option_id"], "split")
        self.assertNotIn("reset", state)
        gen = state["gen"]
        replacement = self.tmp / "other.jsonl"
        replacement.write_text(json.dumps({"kind": "pick", "decision_id": "D3", "option_id": "free", "ts": "t"}) + "\n")
        os.replace(replacement, self.ledger)                                    # a new file under the same name
        state = json.loads(request(self.srv.url + f"api/state?since=2&gen={gen}")[1])
        self.assertTrue(state["reset"])
        self.assertGreater(state["gen"], gen)
        self.assertEqual([r["decision_id"] for r in state["lines"]], ["D3"])

    def test_events_stream_each_new_line(self):
        post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split"})
        req = urllib.request.Request(self.srv.url + "api/events?since=0")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.headers["Content-Type"], "text/event-stream; charset=utf-8")
            self.assertEqual(resp.readline(), b"retry: 2000\n")
            resp.readline()
            event_id, data = resp.readline().decode(), resp.readline().decode()
        self.assertTrue(event_id.startswith("id: ") and event_id.strip().endswith(":1"))
        self.assertEqual(json.loads(data[len("data: "):])["line"]["option_id"], "split")


class HostAndOriginTest(LiveCase):
    def setUp(self):
        super().setUp()
        self.port = self.srv.server_address[1]
        self.pick = {"decision_id": "D1", "option_id": "split"}

    def test_a_host_header_naming_anything_else_is_refused_on_every_route(self):
        paths = ("", "d/1", "summary", "healthz", "api/state", "api/events", "img/" + self.srv.image_of["img/a.svg"])
        for host in (f"evil.example:{self.port}", f"127.0.0.1:{self.port + 1}", "127.0.0.1", f"[::1]:{self.port}",
                     f"user@127.0.0.1:{self.port}"):
            for path in paths:
                with self.subTest(host=host, path=path):
                    self.assertEqual(request(self.srv.url + path, headers={"Host": host})[0], 403)
            with self.subTest(host=host, path="api/pick"):
                self.assertEqual(post(self.srv.url + "api/pick", self.pick, {"Host": host})[0], 403)
        self.assertEqual(self.kinds(), [])

    def test_this_servers_own_names_are_accepted(self):
        for host in (f"127.0.0.1:{self.port}", f"localhost:{self.port}", f"LocalHost:{self.port}"):
            with self.subTest(host):
                self.assertEqual(request(self.srv.url, headers={"Host": host})[0], 200)
                self.assertEqual(post(self.srv.url + "api/pick", self.pick, {"Host": host})[0], 200)

    def test_a_post_from_another_site_is_refused_and_one_with_no_origin_is_not(self):
        for origin in ("http://evil.example", f"http://evil.example:{self.port}", "null", f"https://127.0.0.1:{self.port}",
                       f"http://127.0.0.1:{self.port}/path"):
            with self.subTest(origin):
                self.assertEqual(post(self.srv.url + "api/pick", self.pick, {"Origin": origin})[0], 403)
        self.assertEqual(self.kinds(), [])
        for origin in (f"http://127.0.0.1:{self.port}", f"http://localhost:{self.port}", None):
            with self.subTest(origin):
                headers = {"Origin": origin} if origin else {}
                self.assertEqual(post(self.srv.url + "api/pick", self.pick, headers)[0], 200)
        self.assertEqual(post(self.srv.url + "api/batch", {"jobs": [{"kind": "done", "body": {}}]},
                              {"Origin": "http://evil.example"})[0], 403)
        self.assertEqual(self.kinds(), ["pick", "pick", "pick"])

    def test_host_parsing_and_the_ipv6_bracket_form(self):
        self.assertEqual(routes.host_port("[::1]:8080"), ("::1", 8080))
        self.assertEqual(routes.host_port("[0:0:0:0:0:0:0:1]:8080"), ("::1", 8080))
        self.assertEqual(routes.host_port("LOCALHOST"), ("localhost", 80))
        for bad in ("", "127.0.0.1:x", "a@127.0.0.1:1", "127.0.0.1:1/x", "[::1"):
            with self.subTest(bad):
                self.assertIsNone(routes.host_port(bad))
        hosts = routes.allowed_hosts("::1", 8080)
        self.assertEqual(hosts, {("::1", 8080), ("localhost", 8080), ("127.0.0.1", 8080)})
        self.assertTrue(routes.origin_allowed("http://[::1]:8080", hosts))
        self.assertEqual(routes.allowed_hosts("192.168.1.20", 9), {("192.168.1.20", 9)})    # no loopback names

    def test_an_ipv6_loopback_server_accepts_its_bracketed_host(self):
        try:
            srv = server.make_server(self.spec, self.tmp / "v6.jsonl", "::1", 0)
        except OSError:
            self.skipTest("IPv6 loopback is not available")
        srv.RequestHandlerClass = QuietHandler
        threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
        self.addCleanup(lambda: (srv.finished.set(), srv.shutdown(), srv.server_close(),
                                 server.remove_own_state(self.tmp / "v6.jsonl")))
        self.assertTrue(srv.url.startswith("http://[::1]:"))
        self.assertEqual(request(srv.url)[0], 200)
        self.assertEqual(post(srv.url + "api/pick", self.pick, {"Origin": srv.url.rstrip("/")})[0], 200)
        self.assertEqual(request(srv.url, headers={"Host": f"evil.example:{srv.server_address[1]}"})[0], 403)


class HandlerTimeoutTest(unittest.TestCase):
    def test_the_real_handler_has_a_finite_timeout(self):
        self.assertEqual(routes.Handler.__dict__["timeout"], routes.REQUEST_TIMEOUT_S)
        self.assertTrue(0 < routes.REQUEST_TIMEOUT_S <= 60)


class StalledConnectionTest(LiveCase):
    SHORT_S = 0.3       # a test-only handler timeout, so nothing here waits the real one

    def setUp(self):
        patcher = mock.patch.object(Handler, "timeout", self.SHORT_S)
        patcher.start()
        self.addCleanup(patcher.stop)
        super().setUp()

    def stalled(self, data: bytes) -> tuple:
        """(what the server sent back, seconds until it closed) for a connection that sends `data` and then nothing."""
        with socket.create_connection(("127.0.0.1", self.srv.server_address[1]), timeout=3) as sock:
            sock.sendall(data)
            start = time.monotonic()
            got = sock.recv(4096)       # b"" once the server drops the connection; socket.timeout if it never does
            return got, time.monotonic() - start

    def test_a_request_line_never_finished_is_dropped(self):
        got, took = self.stalled(b"GET / HT")
        self.assertEqual(got, b"")
        self.assertLess(took, 2.5)

    def test_headers_with_no_body_are_dropped_and_record_nothing(self):
        head = (f"POST /api/pick HTTP/1.1\r\nHost: 127.0.0.1:{self.srv.server_address[1]}\r\n"
                "Content-Type: application/json\r\nContent-Length: 60\r\n\r\n")
        got, took = self.stalled(head.encode())
        self.assertEqual(got, b"")
        self.assertLess(took, 2.5)
        self.assertEqual(self.kinds(), [])
        self.assertEqual(request(self.srv.url)[0], 200)          # the server still answers

    def test_the_event_stream_stays_open_past_the_timeout(self):
        with urllib.request.urlopen(self.srv.url + "api/events?since=0", timeout=5) as resp:
            self.assertEqual(resp.readline(), b"retry: 2000\n")
            resp.readline()
            time.sleep(self.SHORT_S * 3)                         # idle for three timeouts
            self.assertEqual(post(self.srv.url + "api/pick", {"decision_id": "D1", "option_id": "split"})[0], 200)
            event_id, data = resp.readline().decode(), resp.readline().decode()
        self.assertTrue(event_id.strip().endswith(":1"))
        self.assertEqual(json.loads(data[len("data: "):])["line"]["option_id"], "split")


class TimerTest(LiveCase):
    GRACE_S = 0.3

    def test_it_stops_once_every_decision_is_picked_and_the_grace_passes(self):
        for did, oid in (("D1", "split"), ("D2", "yes"), ("D3", "free"), ("D4", "early")):
            self.assertEqual(post(self.srv.url + "api/pick", {"decision_id": did, "option_id": oid})[0], 200)
        # Wait on the stop itself with a wide ceiling (it costs nothing when the stop comes on time), then check it
        # against the clock the timer used: never before the grace, whatever the scheduler did in between.
        self.assertTrue(self.srv.finished.wait(timeout=30), "the server never stopped")
        stopped = time.monotonic()
        self.thread.join(timeout=30)
        self.assertFalse(self.thread.is_alive())
        self.assertGreaterEqual(stopped - self.srv.all_picked_at, self.GRACE_S)
        self.assertEqual(self.srv.reason, "every decision picked; grace period over")
        self.assertFalse(core.state_path(self.ledger).exists())
        with self.assertRaises(server.PageClosed):
            self.srv.record({"decision_id": "D1", "option_id": "banner"})


class MaxLifetimeTest(LiveCase):
    MAX_S = 0.2

    def test_it_stops_at_its_maximum_lifetime(self):
        self.assertTrue(self.srv.finished.wait(timeout=30), "the server never stopped")
        self.thread.join(timeout=30)
        self.assertGreaterEqual(time.monotonic() - self.srv.started, self.MAX_S)
        self.assertEqual(self.srv.reason, "maximum lifetime reached")


class BindRuleTest(unittest.TestCase):
    def test_loopback_and_private_networks_are_accepted(self):
        for host in ("127.0.0.1", "::1", "10.1.2.3", "172.16.0.9", "192.168.1.20", "100.64.0.1", "fd12:3456::1"):
            with self.subTest(host):
                self.assertEqual(core.validate_bind_host(host), host)
        self.assertEqual(core.validate_bind_host("localhost"), "127.0.0.1")

    def test_every_interface_public_addresses_and_other_names_are_refused(self):
        for host in ("0.0.0.0", "::", "8.8.8.8", "172.32.0.1", "2001:4860::8888", "deck.example", "", "100.128.0.1"):
            with self.subTest(host), self.assertRaises(ValueError):
                core.validate_bind_host(host)

    def test_the_default_is_loopback(self):
        self.assertEqual(core.DEFAULT_HOST, "127.0.0.1")


class SafeFileTest(TempDirCase):
    def test_safe_file_stays_inside_the_folder(self):
        root = self.spec_path.parent
        (self.tmp / "outside.txt").write_text("secret")
        (root / "link.svg").symlink_to(self.tmp / "outside.txt")
        self.assertEqual(core.safe_file(root, "img/a.svg"), root / "img" / "a.svg")
        for rel in ("../outside.txt", "%2e%2e/outside.txt", "/etc/hosts", "link.svg", "img", "", "a\x00b"):
            with self.subTest(rel):
                self.assertIsNone(core.safe_file(root, rel))


if __name__ == "__main__":
    unittest.main()
