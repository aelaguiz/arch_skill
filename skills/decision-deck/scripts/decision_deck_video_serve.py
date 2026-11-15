"""Decision deck "video" evidence, the clip route: GET /clip/<sha16>.<ext> with byte ranges, from memory.

iPhone Safari plays a video only from a server that answers byte ranges, so every clip response says
Accept-Ranges: bytes, and a single range (bytes=a-b, bytes=a-, bytes=-n) gets 206 with exactly those bytes and their
Content-Range; a range starting past the end (or bytes=-0) gets 416 with `Content-Range: bytes */<size>`; no Range,
or one this route does not read (malformed, several ranges, another unit), gets 200 and the whole clip, as RFC 9110
allows. HEAD gets the same headers and no body. A browser drops a clip's connection whenever it seeks, so a client
gone mid-body ends that response quietly: no traceback, the server carries on.
Only the clips the spec names are served (decision_deck_video.routes_of: the bytes serve read once at start); any
other name is the deck's 404.
"""
from __future__ import annotations

import re

RANGE_RE = re.compile(r"bytes=(\d{0,18})-(\d{0,18})")     # longer numbers are not read: the whole clip, 200
UNSATISFIABLE = "unsatisfiable"
CHUNK = 256 * 1024
# a client gone mid-body: a broken pipe or reset, and on macOS also EPROTOTYPE from a socket the peer is closing
GONE = OSError
NAME_RE = re.compile(r"/clip/([0-9a-f]{16}\.(?:mp4|webm))")


def byte_range(header: str | None, size: int):
    """None (send the whole clip), UNSATISFIABLE, or (first, last) inclusive for the Range header `header`."""
    if not header:
        return None
    m = RANGE_RE.fullmatch(header.strip())
    if not m or not (m.group(1) or m.group(2)):
        return None                     # malformed, several ranges or another unit: the whole clip, 200
    first, last = m.groups()
    if not first:                       # bytes=-n: the last n bytes
        n = int(last)
        return UNSATISFIABLE if n == 0 or size == 0 else (max(0, size - n), size - 1)
    a = int(first)
    if last and int(last) < a:
        return None                     # an invalid range is ignored, as RFC 9110 says
    return UNSATISFIABLE if a >= size else (a, min(int(last) if last else size - 1, size - 1))


def send_clip(handler, body: bytes, ctype: str) -> None:
    """Answer GET or HEAD for one clip on `handler` (decision_deck_routes.Handler), honouring its Range header."""
    size = len(body)
    rng = byte_range(handler.headers.get("Range"), size)
    if rng == UNSATISFIABLE:
        status, part, extra = 416, b"", {"Content-Range": f"bytes */{size}"}
    elif rng:
        a, b = rng
        status, part, extra = 206, memoryview(body)[a:b + 1], {"Content-Range": f"bytes {a}-{b}/{size}"}
    else:
        status, part, extra = 200, memoryview(body), {}
    try:
        handler.send_response(status)
        for name, value in extra.items():
            handler.send_header(name, value)
        handler.send_header("Accept-Ranges", "bytes")
        handler.send_header("Content-Type", ctype if status != 416 else "text/plain; charset=utf-8")
        handler.send_header("Content-Length", str(len(part)))
        handler.send_header("Cache-Control", "private, max-age=31536000, immutable")   # named by content hash
        handler.send_header("X-Content-Type-Options", "nosniff")
        handler.send_header("Referrer-Policy", "no-referrer")
        handler.end_headers()
        if handler.command != "HEAD":
            for k in range(0, len(part), CHUNK):
                handler.wfile.write(part[k:k + CHUNK])
    except GONE:                        # the browser seeked or left: nothing to report, nothing more to send
        handler.close_connection = True
