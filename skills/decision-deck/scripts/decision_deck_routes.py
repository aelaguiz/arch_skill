"""Decision deck routes: the request handler for decision_deck_server.DeckServer (the deck, pictures, the API, events)."""
from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_render as render  # noqa: E402
from decision_deck_core import BODY_MAX, MIME, safe_file  # noqa: E402
from decision_deck_ledger import deck_state, read_records  # noqa: E402

EVENT_POLL_S = 0.25         # how often an event stream looks for new ledger lines
KEEPALIVE_S = 15.0          # a comment line on an idle stream, so proxies and the browser keep it open
PAGE_KINDS = {"/api/comment": "comment", "/api/done": "done"}
# A picture opened as a document (an SVG can carry script) runs sandboxed in an opaque origin, never as the deck;
# an <img> ignores the header, so pictures on slides are unchanged.
PICTURE_HEADERS = {"Content-Security-Policy": "sandbox"}
BATCH_MAX = 64 * 1024       # POST /api/batch: what a page leaves with, inside the browser's keepalive allowance
# Seconds any one read or write on a connection may wait. A client that stops sending part-way through its request
# line, headers or body is dropped after this. The event stream only writes, and each write finishes at once while
# the browser reads, so the stream stays open past this; a browser that stops reading is dropped like a stalled one.
REQUEST_TIMEOUT_S = 30.0


def host_port(value: str):
    """(host, port) from a Host header or the authority part of an Origin, the host lowercased and an IP address in
    its canonical form (brackets dropped from IPv6); port 80 when none is given. None when it cannot be parsed or
    carries anything besides host and port."""
    value = (value or "").strip()
    if not value or any(c in value for c in "@/?#\\ "):
        return None
    try:
        parts = urllib.parse.urlsplit("//" + value)
        host, port = parts.hostname, parts.port
    except ValueError:
        return None
    if not host:
        return None
    try:
        host = str(ipaddress.ip_address(host))
    except ValueError:
        pass
    return host, 80 if port is None else port


def allowed_hosts(bound: str, port: int) -> set:
    """The (host, port) pairs a request may name in its Host header: the bound address and port, plus localhost and
    127.0.0.1 on that port when the server is bound to loopback. Any other name (a DNS name that a page elsewhere
    pointed at this address) is refused, which is what stops a DNS-rebinding page from reading or writing the deck."""
    addr = ipaddress.ip_address(bound)
    hosts = {(str(addr), port)}
    if addr.is_loopback:
        hosts |= {("localhost", port), ("127.0.0.1", port)}
    return hosts


def origin_allowed(origin: str, hosts: set) -> bool:
    """True when an Origin header names this server: http, with an allowed host and port and nothing after them."""
    if not origin.lower().startswith("http://"):
        return False
    return host_port(origin[len("http://"):]) in hosts


def _int(text, default=0):
    try:
        return max(0, int(text))
    except (TypeError, ValueError):
        return default


def _cursor(last_id, query) -> tuple:
    """(since, gen) for a stream or poll: the browser's Last-Event-ID `<gen>:<n>` on a reconnect, else the query's
    `since` and `gen` (gen None when the caller holds none)."""
    if last_id and ":" in last_id:
        gen, n = last_id.split(":", 1)
        return _int(n), _int(gen, None)
    first = lambda key: (query.get(key) or [None])[0]       # noqa: E731
    return _int(last_id, _int(first("since"))), _int(first("gen"), None)


class Handler(BaseHTTPRequestHandler):
    server_version = "decision-deck/1"
    timeout = REQUEST_TIMEOUT_S     # set on the connection in setup(); a timed-out request is logged and dropped

    def _refused(self, post: bool) -> bool:
        """Answer 403 and return True when the Host header does not name this server, or (POST only) when an Origin
        header names another site. A request with no Origin (curl, the agent's act and reply) is not refused for
        that; browsers send Origin on every POST, so a page on another site always is."""
        hosts = self.server.allowed_hosts
        if host_port(self.headers.get("Host", "")) not in hosts:
            why = "the Host header does not name this server"
        elif post and self.headers.get("Origin") is not None and not origin_allowed(self.headers["Origin"], hosts):
            why = "the request comes from another site"
        else:
            return False
        self._json(403, {"ok": False, "error": why})
        return True

    def log_message(self, fmt, *args):  # one line per request on stderr, timestamped in local time
        sys.stderr.write(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {self.address_string()} {fmt % args}\n")

    def _send(self, status: int, body: bytes, ctype: str, cache: str = "no-store", extra: dict | None = None) -> None:
        self.send_response(status)
        for name, value in (extra or {}).items():
            self.send_header(name, value)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _html(self, status: int, html: str) -> None:
        self._send(status, html.encode("utf-8"), "text/html; charset=utf-8")

    def _json(self, status: int, data) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json")

    def _deck(self, start: int) -> None:
        srv = self.server
        gen = srv.ledger_gen()
        self._html(200, render.deck_page(srv.spec, read_records(srv.ledger), start=start, image_of=srv.image_of,
                                         gen=gen, source=srv.source))

    def do_HEAD(self):  # noqa: N802
        self.do_GET()

    def do_GET(self):  # noqa: N802
        srv = self.server
        if self._refused(post=False):
            return None
        url = urllib.parse.urlsplit(self.path)
        path, query = url.path, urllib.parse.parse_qs(url.query)
        total = len(srv.spec["decisions"])      # slides between the cover and the summary
        if path == "/":
            return self._deck(0)
        if path == "/summary":
            return self._deck(total + 1)
        m = re.fullmatch(r"/d/(\d{1,4})", path)
        if m:
            n = int(m.group(1))
            return self._deck(n) if 1 <= n <= total else self._html(404, render.not_found(srv.spec))
        if path == "/healthz":
            return self._json(200, {"ok": True, "open": srv.snapshot()["open"]})
        if path == "/api/state":
            return self._json(200, srv.snapshot(*_cursor(None, query)))
        if path == "/api/events":
            return self._events(*_cursor(self.headers.get("Last-Event-ID"), query))
        m = re.fullmatch(r"/img/([0-9a-f]{16})", path)
        if m and m.group(1) in srv.images:
            target = safe_file(srv.spec["root"], srv.images[m.group(1)])
            body = target.read_bytes() if target is not None else b""
            # Content-addressed and cached for a year, so only the bytes that still hash to the name are served:
            # a picture regenerated since the server started is a 404, never other evidence under the same URL.
            if target is not None and hashlib.sha256(body).hexdigest()[:16] == m.group(1):
                return self._send(200, body, MIME[target.suffix.lower()], cache="private, max-age=31536000, immutable",
                                  extra=PICTURE_HEADERS)
        return self._html(404, render.not_found(srv.spec))

    def _events(self, since: int, gen) -> None:
        """Server-sent events, until shutdown: one `data:` line per new ledger line {n, gen, line, state}, with event
        id `<gen>:<n>`. When the ledger was replaced or truncated (a new generation, or fewer records than the
        caller holds) one {reset: true, gen, n, lines, state} instead, and the page starts over from it; fewer
        records in the same generation make a new one (DeckServer.regen), so a reset never goes back in a
        generation."""
        srv = self.server
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        self.close_connection = True
        sent, seen, beat = since, None, time.monotonic()
        try:
            self.wfile.write(b"retry: 2000\n\n")
            self.wfile.flush()
            while not srv.finished.is_set():
                now = srv.ledger_gen()
                try:
                    st = srv.ledger.stat()
                    mark = (now, st.st_size, st.st_mtime_ns, st.st_ino)
                except FileNotFoundError:
                    mark = (now, None)
                if mark != seen:
                    seen = mark
                    records = read_records(srv.ledger)
                    gen = now if gen is None else gen
                    if gen == now and len(records) < sent:      # rewritten in place without shrinking
                        now = srv.regen(now)
                    if gen != now:                              # a replaced ledger: the page starts over
                        data = json.dumps({"reset": True, "gen": now, "n": len(records), "lines": records,
                                           "state": deck_state(srv.spec, records)}, ensure_ascii=False)
                        self.wfile.write(f"id: {now}:{len(records)}\ndata: {data}\n\n".encode("utf-8"))
                        gen, sent, beat = now, len(records), time.monotonic()
                        self.wfile.flush()
                    elif len(records) > sent:
                        state = deck_state(srv.spec, records)
                        for i in range(sent, len(records)):
                            data = json.dumps({"n": i + 1, "gen": now, "line": records[i], "state": state},
                                              ensure_ascii=False)
                            self.wfile.write(f"id: {now}:{i + 1}\ndata: {data}\n\n".encode("utf-8"))
                        sent = len(records)
                        beat = time.monotonic()
                        self.wfile.flush()
                if time.monotonic() - beat > KEEPALIVE_S:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
                    beat = time.monotonic()
                time.sleep(EVENT_POLL_S)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    def _local(self) -> bool:
        """True for a request from this machine: loopback, or this server's own bind address."""
        try:
            addr = ipaddress.ip_address(self.client_address[0])
            own = ipaddress.ip_address(self.server.host)
        except ValueError:
            return False
        mapped = getattr(addr, "ipv4_mapped", None)
        return addr.is_loopback or addr == own or (mapped is not None and (mapped.is_loopback or mapped == own))

    def do_POST(self):  # noqa: N802
        srv = self.server
        if self._refused(post=True):
            return None
        path = urllib.parse.urlsplit(self.path).path
        if path not in ("/api/pick", "/api/status", "/api/batch", *PAGE_KINDS):
            return self._json(404, {"ok": False, "error": "not found"})
        if path == "/api/status":
            token = self.headers.get("X-Deck-Token", "")
            if not self._local() or not hmac.compare_digest(token.encode(), srv.token.encode()):
                return self._json(403, {"ok": False, "error": "status lines come from this machine with the token"})
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            return self._json(415, {"ok": False, "error": "send application/json"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if not 0 < length <= (BATCH_MAX if path == "/api/batch" else BODY_MAX):
            return self._json(400, {"ok": False, "error": "bad body length"})
        from decision_deck_server import PageClosed
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("body must be a JSON object")
            if path == "/api/pick":
                result = srv.record(payload)
            elif path == "/api/batch":
                result = srv.batch(payload.get("jobs"))
            elif path == "/api/status":
                kind = payload.get("kind", "status")
                if kind not in ("status", "reply"):
                    raise ValueError("kind must be status or reply")
                result = srv.append(kind, payload)
            else:
                result = srv.append(PAGE_KINDS[path], payload)
        except PageClosed as exc:
            return self._json(410, {"ok": False, "error": str(exc)})
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"ok": False, "error": str(exc)})
        return self._json(200, result)
