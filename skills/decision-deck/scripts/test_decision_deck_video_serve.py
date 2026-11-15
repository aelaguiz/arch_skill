"""Tests for the decision deck's "video" clip route, how serve reaches a clip's bytes, the check stamp and serve.

The route: byte ranges (206 with exactly the bytes asked for and their Content-Range, for first-byte, open-ended and
suffix ranges; 416 with `Content-Range: bytes */<size>` past the end; 200 and the whole clip with no Range or one
the route does not read), HEAD, the content types, only the spec's clips by content hash (never the ledger, its
state file or the spec), the bytes read at start and never the disk, and a client dropping mid-clip leaving no
traceback and the server serving. Reaching the bytes: one path part at a time from the spec's folder, so a folder or
the clip swapped for a symlink, a file, a folder or a FIFO after the spec loaded is refused by name, with no
descriptor left open. The stamp records each clip's hash and names a changed clip; serve --require-checked refuses
it, and serve on the command line serves a checked video deck with ranges. Helpers: test_decision_deck_video.py.
"""
import contextlib
import io
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import threading
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck as dd  # noqa: E402
import decision_deck_server as server  # noqa: E402
import decision_deck_spec as ps  # noqa: E402
import decision_deck_stamp as stamp  # noqa: E402
import decision_deck_video as video  # noqa: E402
from decision_deck_video_serve import UNSATISFIABLE, byte_range  # noqa: E402
from test_decision_deck_server import QuietHandler, request  # noqa: E402
from test_decision_deck_spec import make_spec_dir  # noqa: E402
from test_decision_deck_video import MP4, WEBM, VideoCase, file_is, make_video_dir, video_spec  # noqa: E402

TOOL = Path(__file__).resolve().parent / "decision_deck.py"


def serve(spec, ledger):
    srv = server.make_server(spec, ledger, "127.0.0.1", 0, grace_s=60, max_s=60)
    srv.RequestHandlerClass = QuietHandler
    threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
    return srv


def stop(srv):
    srv.finished.set()
    srv.shutdown()
    srv.server_close()
    server.remove_own_state(srv.ledger)


class LiveVideoCase(VideoCase):
    def start(self, spec=None):
        self.srv = serve(spec or self.load(), self.tmp / "ledger.jsonl")
        self.addCleanup(stop, self.srv)
        return self.srv

    def clip_url(self, rel):
        return self.srv.url.rstrip("/") + self.srv.clip_urls[rel]


class RouteTest(LiveVideoCase):
    def setUp(self):
        super().setUp()
        self.start()

    def test_the_clip_route_answers_byte_ranges(self):
        body = (self.root / "today.mp4").read_bytes()
        size = len(body)
        for header, status, first, last in [
                (None, 200, 0, None), ("bytes=0-", 206, 0, None), ("bytes=100-199", 206, 100, 199),
                ("bytes=-500", 206, -500, None), ("bytes=100-99999999", 206, 100, None), ("bytes=0-0", 206, 0, 0),
                ("bytes=abc", 200, 0, None), ("bytes=0-1,5-6", 200, 0, None), ("items=0-10", 200, 0, None),
                ("bytes=200-100", 200, 0, None)]:
            with self.subTest(header):
                code, data, head = request(self.clip_url("today.mp4"), headers={"Range": header} if header else {})
                self.assertEqual(code, status)
                self.assertEqual((head["Content-Type"], head["Accept-Ranges"]), ("video/mp4", "bytes"))
                start = size + first if first < 0 else first
                end = size - 1 if last is None else last
                self.assertEqual(data, body[start:end + 1])
                self.assertEqual(head["Content-Length"], str(end + 1 - start))
                self.assertEqual(head.get("Content-Range"), f"bytes {start}-{end}/{size}" if status == 206 else None)

    def test_a_range_past_the_end_is_416_with_the_size(self):
        size = (self.root / "today.mp4").stat().st_size
        for header in ("bytes=999999999-", "bytes=-0"):
            with self.subTest(header):
                code, data, head = request(self.clip_url("today.mp4"), headers={"Range": header})
                self.assertEqual((code, head["Content-Range"], data), (416, f"bytes */{size}", b""))

    def test_webm_head_and_unknown_names(self):
        code, data, head = request(self.clip_url("calm.webm"), method="HEAD")
        self.assertEqual((code, head["Content-Type"], data), (200, "video/webm", b""))
        self.assertEqual(head["Content-Length"], str((self.root / "calm.webm").stat().st_size))
        code, data, head = request(self.clip_url("calm.webm"), headers={"Range": "bytes=10-19"}, method="HEAD")
        self.assertEqual((code, data), (206, b""))
        self.assertTrue(head["Content-Range"].startswith("bytes 10-19/"))
        name = self.srv.clip_urls["today.mp4"].rsplit("/", 1)[1]
        for path in ("/clip/0123456789abcdef.mp4", "/clip/" + name.replace(".mp4", ".webm"), "/clip/ledger.jsonl",
                     "/clip/ledger.server.json", "/clip/spec.json", "/clip/../spec.json", "/clip/today.mp4"):
            with self.subTest(path):
                self.assertEqual(request(self.srv.url.rstrip("/") + path)[0], 404)

    def test_the_route_serves_the_bytes_read_at_start_never_the_disk(self):
        before = (self.root / "today.mp4").read_bytes()
        (self.root / "today.mp4").write_bytes(before[:100] + b"\0" * (len(before) - 100))
        self.assertEqual(request(self.clip_url("today.mp4"))[1], before)


class DroppedClientTest(LiveVideoCase):
    def test_a_client_dropping_mid_clip_leaves_no_traceback_and_the_server_serving(self):
        big = MP4[:64] + os.urandom(6 * 1024 * 1024)        # big enough that the dropped client meets a broken pipe
        (self.root / "big.mp4").write_bytes(big)
        data = video_spec()
        file_is("big.mp4")(data)
        self.spec_path.write_text(json.dumps(data))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            srv = self.start()
            host, port = srv.server_address[:2]
            for rng in ("", "Range: bytes=0-\r\n", "Range: bytes=1000-\r\n"):
                sock = socket.create_connection((host, port), timeout=5)
                sock.sendall(f"GET {srv.clip_urls['big.mp4']} HTTP/1.1\r\nHost: {host}:{port}\r\n{rng}\r\n".encode())
                self.assertTrue(sock.recv(4096))            # the headers and some of the body, then gone
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))   # close with a reset
                sock.close()
            code, body, _ = request(self.clip_url("big.mp4"), headers={"Range": "bytes=0-9"})
            self.assertEqual((code, body), (206, big[:10]))
            self.assertEqual(request(srv.url + "healthz")[0], 200)
        self.assertNotIn("Traceback", err.getvalue())


class PathTest(VideoCase):
    """Clips in subfolders, swapped after the spec loaded."""

    TODAY, CALM = "assets/today.mp4", "a/b/calm.webm"

    def setUp(self):
        super().setUp()
        data = video_spec()
        for dec in data["decisions"]:
            for clip in dec["evidence"]["clips"]:
                clip["file"] = self.TODAY if clip["file"] == "today.mp4" else self.CALM
        self.spec_path = make_video_dir(self.tmp, data, {self.TODAY: MP4, self.CALM: WEBM})
        self.spec = self.load()
        self.outside = self.tmp / "outside"
        for rel in ("today.mp4", "b/calm.webm"):
            (self.outside / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.outside / rel).write_bytes(MP4 if rel.endswith(".mp4") else WEBM)

    def swap_for_link(self, rel, target):
        (self.root / rel).rename(self.root / (rel + "-was"))
        (self.root / rel).symlink_to(target, target_is_directory=True)

    def test_a_folder_swapped_for_a_symlink_is_refused_by_name_at_any_depth(self):
        self.swap_for_link("assets", self.outside)
        with self.assertRaises(video.ClipPathError) as exc:
            video.snapshot(self.spec)
        self.assertEqual(str(exc.exception), f"clip {self.root.as_posix()}/{self.TODAY} is reached through a symlink "
                                             "(assets); name the file by its real path")
        (self.root / "assets").unlink()
        (self.root / "assets-was").rename(self.root / "assets")
        self.swap_for_link("a/b", self.outside / "b")
        with self.assertRaisesRegex(video.ClipPathError, r"calm\.webm is reached through a symlink \(a/b\)"):
            video.snapshot(self.spec)

    def test_serve_refuses_a_folder_swapped_after_the_load_by_name_and_serves_nothing(self):
        real = dd.load_spec

        def load_then_swap(path):
            spec = real(path)
            self.swap_for_link("a", self.outside)
            return spec
        err = io.StringIO()
        with mock.patch.object(dd, "load_spec", load_then_swap), \
                mock.patch.object(dd, "make_server", side_effect=AssertionError("served a refused deck")), \
                contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()) as out:
            code = dd.main(["serve", "--spec", str(self.spec_path), "--host", "127.0.0.1"])
        self.assertEqual(code, 2)
        self.assertIn("decision_deck serve: refused: clip ", err.getvalue())
        self.assertIn("is reached through a symlink (a)", err.getvalue())
        self.assertNotIn("URL ", out.getvalue())

    def test_a_folder_swapped_for_a_file_or_the_clip_for_a_folder_or_fifo_is_refused(self):
        shutil.move(str(self.root / "a"), str(self.root / "a-was"))
        (self.root / "a").write_bytes(b"not a folder")
        with self.assertRaisesRegex(video.ClipPathError, r"is reached through a, which is not a folder"):
            video.snapshot(self.spec)
        (self.root / "a").unlink()
        shutil.move(str(self.root / "a-was"), str(self.root / "a"))
        (self.root / self.TODAY).rename(self.root / "assets" / "was.mp4")
        (self.root / self.TODAY).mkdir()
        with self.assertRaises(video.ClipPathError) as exc:
            video.snapshot(self.spec)
        self.assertEqual(str(exc.exception), f"clip {self.root.as_posix()}/{self.TODAY} is not a regular file")
        if hasattr(os, "mkfifo"):           # O_NONBLOCK: a FIFO with no writer opens at once, then fstat refuses it
            (self.root / self.TODAY).rmdir()
            os.mkfifo(self.root / self.TODAY)
            with self.assertRaisesRegex(video.ClipPathError, "is not a regular file"):
                video.snapshot(self.spec)
            self.assertIn("clip 1: clip 'assets/today.mp4' is not a file",
                          "\n".join(ps.validate_spec(json.loads(self.spec_path.read_text()), self.root)))

    def test_open_clip_leaves_no_descriptor_open_on_any_refusal(self):
        before = len(os.listdir("/dev/fd"))
        self.swap_for_link("a", self.outside)
        (self.root / self.TODAY).rename(self.root / "assets" / "was.mp4")
        (self.root / self.TODAY).mkdir()
        for rel in (self.CALM, self.TODAY, "assets/missing.mp4"):
            with self.subTest(rel), self.assertRaises(OSError):
                video.open_clip(self.root, rel)
        self.assertEqual(len(os.listdir("/dev/fd")), before)

    def test_clips_in_subfolders_are_served_by_their_routes_with_ranges(self):
        srv = serve(self.spec, self.tmp / "ledger.jsonl")
        self.addCleanup(stop, srv)
        self.assertEqual(set(srv.clip_urls), {self.TODAY, self.CALM})
        for rel in (self.TODAY, self.CALM):
            with self.subTest(rel):
                code, data, head = request(srv.url.rstrip("/") + srv.clip_urls[rel], headers={"Range": "bytes=0-99"})
                self.assertEqual((code, data), (206, (self.root / rel).read_bytes()[:100]))
                self.assertEqual(head["Content-Range"], f"bytes 0-99/{(self.root / rel).stat().st_size}")


class StampTest(VideoCase):
    def test_the_stamp_records_each_clip_and_names_a_changed_one(self):
        spec = self.load()
        stamp.write_stamp(spec, stamp.digest(spec))
        self.assertEqual(set(json.loads(stamp.stamp_path(spec).read_text())["clips"]), {"today.mp4", "calm.webm"})
        self.assertEqual(stamp.stamp_problem(spec), "")
        body = (self.root / "calm.webm").read_bytes()
        (self.root / "calm.webm").write_bytes(body[:-1] + bytes([body[-1] ^ 1]))
        why = stamp.stamp_problem(self.load())
        self.assertTrue(why.startswith("a video decision's clip changed"), why)
        self.assertTrue(why.endswith(str(self.root / "calm.webm")), why)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = dd.main(["serve", "--spec", str(self.spec_path), "--require-checked"])
        self.assertEqual(code, 2)
        self.assertIn("refused", err.getvalue())
        self.assertIn("calm.webm", err.getvalue())

    def test_a_deck_without_clips_stamps_and_hashes_as_before(self):
        spec = ps.load_spec(make_spec_dir(self.tmp / "plain"))
        stamp.write_stamp(spec, stamp.digest(spec))
        self.assertNotIn("clips", json.loads(stamp.stamp_path(spec).read_text()))
        self.assertEqual(stamp.digest(spec), stamp.digest(spec, clips={}))

    def test_an_unreadable_clip_is_refused_naming_it(self):
        spec = self.load()
        os.chmod(self.root / "calm.webm", 0)
        try:
            err = io.StringIO()
            with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as exc:
                dd.main(["serve", "--spec", str(self.spec_path)])       # at the load: a spec error, exit 2
            with self.assertRaises(PermissionError) as late:            # after the load: the snapshot refuses it
                video.snapshot(spec)
        finally:
            os.chmod(self.root / "calm.webm", 0o644)
        self.assertEqual(exc.exception.code, 2)
        self.assertIn("decision D1 evidence clip 2: clip 'calm.webm' cannot be read", err.getvalue())
        self.assertIn("calm.webm", str(late.exception))

    def test_a_clip_swapped_for_a_symlink_after_the_load_is_never_read(self):
        spec = self.load()
        (self.root / "calm.webm").unlink()
        (self.root / "calm.webm").symlink_to(self.root / "today.mp4")
        with self.assertRaises(OSError):
            video.snapshot(spec)

    def test_serve_on_the_command_line_serves_a_checked_video_deck_with_ranges(self):
        spec = self.load()
        stamp.write_stamp(spec, stamp.digest(spec))
        proc = subprocess.Popen([sys.executable, str(TOOL), "serve", "--spec", str(self.spec_path),
                                 "--require-checked", "--source", "From the test"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            line = proc.stdout.readline()
            self.assertTrue(line.startswith("URL "), proc.stderr.read() if proc.poll() is not None else line)
            url = line.split()[1]
            code, page, _ = request(url + "d/1")
            self.assertEqual(code, 200)
            self.assertIn(b"<video controls playsinline", page)
            src = page.decode().split('<video controls playsinline preload="metadata" src="', 1)[1].split("#", 1)[0]
            code, data, head = request(url.rstrip("/") + src, headers={"Range": "bytes=100-199"})
            self.assertEqual((code, len(data)), (206, 100))
            self.assertTrue(head["Content-Range"].startswith("bytes 100-199/"))
        finally:
            proc.terminate()
            proc.wait(timeout=10)
            proc.stderr.close()
        self.assertIn("STOPPED", proc.stdout.read())
        proc.stdout.close()


class ByteRangeTest(unittest.TestCase):
    def test_byte_range(self):
        self.assertIsNone(byte_range(None, 10))
        self.assertEqual(byte_range("bytes=2-", 10), (2, 9))
        self.assertEqual((byte_range("bytes=-3", 10), byte_range("bytes=-30", 10)), ((7, 9), (0, 9)))
        self.assertEqual((byte_range("bytes=10-", 10), byte_range("bytes=-0", 10)), (UNSATISFIABLE, UNSATISFIABLE))
        self.assertEqual(byte_range(" bytes=1-2 ", 10), (1, 2))
        self.assertIsNone(byte_range("bytes=1-2, 4-5", 10))
        self.assertIsNone(byte_range("bytes=" + "9" * 5000 + "-", 10))     # no int() of a huge number


if __name__ == "__main__":
    unittest.main()
