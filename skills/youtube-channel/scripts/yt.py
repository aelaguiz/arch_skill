#!/usr/bin/env python3
"""Run a YouTube channel through YouTube's Data, Analytics and Reporting APIs. Standard library only.

    yt.py whoami
    yt.py videos [--limit 20]
    yt.py video <id> [--json-out f.json]
    yt.py upload <file> --title "..." [--description-file d.txt] [--privacy unlisted] [--wait] ...
    yt.py update <id> [--title ...] [--privacy public] [--publish-at 2026-11-01T15:00:00Z] [--dry-run] ...
    yt.py thumbnail <id> <image>
    yt.py captions list|upload|download|delete ...
    yt.py playlists | playlist create|update|delete|items|add|remove|move ...
    yt.py comments [--video <id>] [--status heldForReview] | comment thread|reply|post|edit|delete|moderate ...
    yt.py channel show|update|banner | watermark set|unset ...
    yt.py analytics --metrics views,estimatedMinutesWatched --dimensions day --start 2026-10-01 --end 2026-10-25
    yt.py reporting types|jobs|create-job|delete-job|reports|download ...
    yt.py search "query" | public-videos <ids> | public-channel <@handle or id> | categories | languages
    yt.py delete <id> --confirm-title "exact title"
    yt.py raw GET /channelSections part=snippet mine=true
    yt.py login --url-file <private file>

Every command prints a short summary; --json-out writes the full API response to a file. Run `yt.py <command> -h`.
The grant (Google's authorized_user JSON with a refresh token) is read from $YOUTUBE_OAUTH_FILE, default
~/workspace/secrets/local/services/youtube/pokerskill-channel-oauth.json. Nothing here prints a token or a code.
"""

import argparse
import base64
import hashlib
import http.server
import json
import mimetypes
import os
import secrets
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

HOME = os.path.expanduser("~")
GRANT_FILE = os.environ.get(
    "YOUTUBE_OAUTH_FILE", f"{HOME}/workspace/secrets/local/services/youtube/pokerskill-channel-oauth.json")
CLIENT_FILE = os.environ.get(
    "YOUTUBE_CLIENT_FILE", f"{HOME}/workspace/secrets/local/google/gws-client_secret-poker-skill-a2d33.json")
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
DATA = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2"
REPORTING = "https://youtubereporting.googleapis.com/v1"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
CHUNK = int(os.environ.get("YOUTUBE_UPLOAD_CHUNK_KIB", 16 * 1024)) * 1024  # a multiple of 256 KiB
WRITABLE_STATUS = ("privacyStatus", "publishAt", "license", "embeddable", "publicStatsViewable",
                   "selfDeclaredMadeForKids", "containsSyntheticMedia")

# What a few of YouTube's error reasons mean in practice, said once where the error appears.
HINTS = {
    "quotaExceeded": "the project's daily quota is spent; it resets at midnight Pacific",
    "uploadLimitExceeded": "the channel hit YouTube's own daily upload limit (separate from quota); try again tomorrow",
    "forbidden": "the signed-in account can't do this to this resource (wrong channel, or a feature the channel hasn't unlocked)",
    "insufficientPermissions": "the grant lacks a scope this call needs; redo `yt.py login`",
    "invalid_grant": "the refresh token was revoked or expired; redo `yt.py login`",
    "videoNotFound": "no video with that id on a channel this grant can see",
    "commentsDisabled": "comments are off on that video (private videos and some made-for-kids videos have none)",
    "invalidPublishAt": "publishAt must be in the future and the video must be private and never published",
    "mediaBodyRequired": "the upload sent no file",
    "processingFailure": "for comments: replies only go under a top-level comment, and someone else's comment "
                         "can't be deleted (reject it with `comment moderate --status rejected`)",
    "channelTitleUpdateForbidden": "the channel's name can only be changed in Studio",
}
LONG_UPLOADS = {"allowed": "allowed", "eligible": "not yet (phone verification unlocks videos over 15 minutes)",
                "disallowed": "not allowed"}


# ---------- plumbing ----------

def die(msg):
    sys.exit(f"error: {msg}")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def write_private(path, text):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(text)


def save_json(path, obj):
    if path:
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
        print(f"full response: {path}")


def google_error(code, raw):
    try:
        body = json.loads(raw or b"{}")
    except ValueError:
        return f"HTTP {code}: {raw[:300]!r}"
    err = body.get("error")
    if isinstance(err, str):  # OAuth token endpoint shape
        reason, message = err, body.get("error_description", "")
    else:
        err = err or {}
        reasons = [e.get("reason") for e in err.get("errors", []) if e.get("reason")]
        reason = reasons[0] if reasons else err.get("status", "")
        message = err.get("message", "")
    hint = HINTS.get(reason)
    return f"HTTP {code} {reason}: {message}" + (f" ({hint})" if hint else "")


def http(method, url, params=None, body=None, data=None, headers=None, token=None, raw=False, ok=(200, 201, 204)):
    """One HTTP call with up to 3 tries on 5xx and rate limits. Returns (status, headers, parsed body)."""
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}, doseq=True)
    hdrs = dict(headers or {})
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json; charset=UTF-8"
    if data is None and method in ("POST", "PUT"):
        data = b""  # Google wants a Content-Length even on an empty POST
    for attempt in range(3):
        req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                content = r.read()
                if raw:
                    return r.status, r.headers, content
                return r.status, r.headers, (json.loads(content) if content else {})
        except urllib.error.HTTPError as e:
            content = e.read()
            if e.code in ok:
                return e.code, e.headers, (json.loads(content) if content and not raw else content)
            retryable = e.code >= 500 or (e.code in (403, 429) and b"RateLimitExceeded" in content)
            if retryable and attempt < 2:
                time.sleep(2 ** attempt * 3)
                continue
            die(f"{method} {url.split('?')[0]} -> {google_error(e.code, content)}")
        except urllib.error.URLError as e:
            if attempt < 2:
                time.sleep(2 ** attempt * 3)
                continue
            die(f"{method} {url.split('?')[0]} -> network error: {e.reason}")


_token = None


def token():
    global _token
    if _token:
        return _token
    if not os.path.exists(GRANT_FILE):
        die(f"no grant at {GRANT_FILE}; set YOUTUBE_OAUTH_FILE or run `yt.py login` (see references/setup.md)")
    g = load_json(GRANT_FILE)
    data = urllib.parse.urlencode({"client_id": g["client_id"], "client_secret": g["client_secret"],
                                   "refresh_token": g["refresh_token"], "grant_type": "refresh_token"}).encode()
    _, _, t = http("POST", TOKEN_URI, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    _token = t["access_token"]
    return _token


def api(method, path, params=None, body=None, base=DATA):
    return http(method, base + path, params=params, body=body, token=token())[2]


def pages(path, params, limit, base=DATA):
    """Yield items across pages until `limit` items (None = all)."""
    params = dict(params)
    n = 0
    while True:
        resp = api("GET", path, params, base=base)
        for item in resp.get("items", []):
            yield item
            n += 1
            if limit and n >= limit:
                return
        params["pageToken"] = resp.get("nextPageToken")
        if not params["pageToken"]:
            return


def text_arg(text, path):
    if path:
        with open(path) as f:
            return f.read().rstrip("\n")
    return text


def short(s, n=90):
    s = (s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def table(rows, headers, limit=None):
    shown = rows[:limit] if limit else rows
    widths = [max(len(str(h)), *(len(str(r[i])) for r in shown)) if shown else len(str(h))
              for i, h in enumerate(headers)]
    print("  ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    for r in shown:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    if limit and len(rows) > limit:
        print(f"... {len(rows) - limit} more rows (raise --max-rows or use --csv-out)")


def iso_duration(d):
    """PT1H2M3S -> 1:02:03."""
    if not d or not d.startswith("P"):
        return d or ""
    num, h, m, s = "", 0, 0, 0
    for ch in d.split("T")[-1]:
        if ch.isdigit():
            num += ch
        else:
            v = int(num or 0)
            h, m, s = (v, m, s) if ch == "H" else (h, v, s) if ch == "M" else (h, m, v)
            num = ""
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def mine():
    return api("GET", "/channels", {"part": "snippet,contentDetails,statistics,status,brandingSettings",
                                    "mine": "true"})["items"][0]


# ---------- sign-in ----------

def cmd_login(a):
    c = load_json(CLIENT_FILE)
    c = c.get("installed") or c["web"]
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    redirect = f"http://localhost:{port}/"
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(24)
    url = AUTH_URI + "?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code",
        "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent",
        "code_challenge": challenge, "code_challenge_method": "S256", "state": state})
    write_private(a.url_file, url + "\n")
    print(f"sign-in address written to {a.url_file}; open it in the browser signed in as the channel; "
          f"waiting up to {a.timeout}s", flush=True)
    got = {}

    class Callback(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [None])[0] != state:
                self.send_response(400)
                self.end_headers()
                return
            got["code"], got["error"] = q.get("code", [None])[0], q.get("error", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Signed in. You can close this tab.")

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), Callback)
    server.timeout = 5
    deadline = time.time() + a.timeout
    while not got and time.time() < deadline:
        server.handle_request()
    if not got.get("code"):
        die(f"no sign-in came back ({got.get('error') or 'timed out'})")
    data = urllib.parse.urlencode({"client_id": c["client_id"], "client_secret": c["client_secret"],
                                   "code": got["code"], "code_verifier": verifier, "redirect_uri": redirect,
                                   "grant_type": "authorization_code"}).encode()
    _, _, t = http("POST", TOKEN_URI, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if "refresh_token" not in t:
        die("Google returned no refresh token")
    me = http("GET", f"{DATA}/channels", {"part": "snippet", "mine": "true"}, token=t["access_token"])[2]
    channels = [{"id": i["id"], "title": i["snippet"]["title"]} for i in me.get("items", [])]
    write_private(GRANT_FILE, json.dumps({
        "type": "authorized_user", "client_id": c["client_id"], "client_secret": c["client_secret"],
        "refresh_token": t["refresh_token"], "scopes": t.get("scope", "").split(), "channels": channels},
        indent=2) + "\n")
    print(f"grant saved to {GRANT_FILE}; channel(s): {', '.join(x['id'] + ' ' + x['title'] for x in channels)}")


def cmd_whoami(a):
    ch = mine()
    s, st = ch["statistics"], ch["status"]
    print(f"{ch['id']}  {ch['snippet']['title']} ({ch['snippet'].get('customUrl')})")
    print(f"subscribers {s.get('subscriberCount')}  public videos {s.get('videoCount')}  views {s.get('viewCount')}")
    lu = st.get("longUploadsStatus")
    print(f"videos over 15 minutes: {LONG_UPLOADS.get(lu, lu)}  made for kids {st.get('madeForKids')}  "
          f"privacy {st.get('privacyStatus')}")
    info = http("GET", "https://oauth2.googleapis.com/tokeninfo", {"access_token": token()})[2]
    print("scopes:", " ".join(x.rsplit("/", 1)[-1] for x in info.get("scope", "").split()))
    save_json(a.json_out, ch)


# ---------- videos ----------

def video_row(v):
    sn, st, cd, stats = v["snippet"], v["status"], v.get("contentDetails", {}), v.get("statistics", {})
    when = st.get("publishAt") and f"at {st['publishAt']}" or sn.get("publishedAt", "")[:10]
    return [v["id"], st.get("privacyStatus"), when, iso_duration(cd.get("duration")),
            stats.get("viewCount", ""), short(sn.get("title"), 60)]


def get_videos(ids, parts="snippet,status,contentDetails,statistics"):
    out = []
    for i in range(0, len(ids), 50):
        out += api("GET", "/videos", {"part": parts, "id": ",".join(ids[i:i + 50])}).get("items", [])
    return out


def cmd_videos(a):
    uploads = mine()["contentDetails"]["relatedPlaylists"]["uploads"]
    # The uploads playlist read as the owner can repeat or drop videos (scheduled ones most); dedupe here, and
    # check one video with `yt.py video <id>` when its absence matters.
    ids = list(dict.fromkeys(it["contentDetails"]["videoId"] for it in pages(
        "/playlistItems", {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}, a.limit)))
    vids = get_videos(ids)
    if a.privacy != "all":
        vids = [v for v in vids if v["status"]["privacyStatus"] == a.privacy]
    table([video_row(v) for v in vids], ["id", "privacy", "published", "length", "views", "title"])
    save_json(a.json_out, vids)


def cmd_video(a):
    items = get_videos([a.id], "snippet,status,contentDetails,statistics,processingDetails,fileDetails,"
                                "localizations,recordingDetails,topicDetails,player")
    if not items:
        die(f"no video {a.id} visible to this grant")
    v = items[0]
    sn, st, cd, stats = v["snippet"], v["status"], v["contentDetails"], v.get("statistics", {})
    pd, fd = v.get("processingDetails", {}), v.get("fileDetails", {})
    print(f"{v['id']}  https://youtu.be/{v['id']}")
    print(f"title: {sn['title']}")
    print(f"privacy {st['privacyStatus']}  publishAt {st.get('publishAt', '-')}  published {sn.get('publishedAt')}")
    print(f"upload {st.get('uploadStatus')}  processing {pd.get('processingStatus', '-')}"
          + (f"  failure {st.get('failureReason')}" if st.get("failureReason") else "")
          + (f"  rejected {st.get('rejectionReason')}" if st.get("rejectionReason") else ""))
    print(f"length {iso_duration(cd.get('duration'))}  {cd.get('definition')}  "
          f"captions {cd.get('caption')}  licensed content {cd.get('licensedContent')}")
    vs = (fd.get("videoStreams") or [{}])[0]
    if vs:
        print(f"file {vs.get('widthPixels')}x{vs.get('heightPixels')}  {fd.get('fileName', '')}")
    print(f"views {stats.get('viewCount')}  likes {stats.get('likeCount')}  comments {stats.get('commentCount')}")
    print(f"category {sn.get('categoryId')}  language {sn.get('defaultLanguage')}/"
          f"{sn.get('defaultAudioLanguage')}  tags {len(sn.get('tags', []))}  "
          f"localizations {','.join(sorted(v.get('localizations', {}))) or '-'}")
    print(f"made for kids {st.get('madeForKids')} (self-declared {st.get('selfDeclaredMadeForKids')})  "
          f"synthetic {st.get('containsSyntheticMedia')}  embeddable {st.get('embeddable')}  "
          f"public stats {st.get('publicStatsViewable')}  license {st.get('license')}")
    print(f"description: {short(sn.get('description'), 200)}")
    save_json(a.json_out, v)


def wait_processed(vid, timeout):
    deadline = time.time() + timeout
    last = None
    while True:
        v = get_videos([vid], "status,processingDetails")[0]
        state = (v["status"].get("uploadStatus"), v.get("processingDetails", {}).get("processingStatus"))
        if state != last:
            print(f"  upload {state[0]}, processing {state[1]}", flush=True)
            last = state
        if state[0] in ("processed", "failed", "rejected", "deleted") or state[1] in ("succeeded", "failed",
                                                                                      "terminated"):
            return v
        if time.time() > deadline:
            print(f"  still processing after {timeout}s; check later with `yt.py video {vid}`")
            return v
        time.sleep(15)


def build_status(a, current=None):
    st = {k: v for k, v in (current or {}).items() if k in WRITABLE_STATUS}
    if a.privacy:
        st["privacyStatus"] = a.privacy
    if getattr(a, "clear_publish_at", False) or (a.privacy and a.privacy != "private" and not a.publish_at):
        st.pop("publishAt", None)  # going public or unlisted now cancels any scheduled release
    if a.publish_at:
        st["publishAt"] = a.publish_at
        if st.get("privacyStatus") != "private":
            print("note: a scheduled release must be private until it goes public; privacy set to private")
            st["privacyStatus"] = "private"
    for flag, key in (("made_for_kids", "selfDeclaredMadeForKids"), ("synthetic", "containsSyntheticMedia"),
                      ("embeddable", "embeddable"), ("public_stats", "publicStatsViewable")):
        val = getattr(a, flag, None)
        if val is not None:
            st[key] = val
    if getattr(a, "license", None):
        st["license"] = a.license
    return st


def cmd_upload(a):
    path = a.file
    if not os.path.isfile(path):
        die(f"no file {path}")
    size = os.path.getsize(path)
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    snippet = {"title": a.title, "description": text_arg(a.description, a.description_file) or ""}
    if a.category:
        snippet["categoryId"] = a.category
    if a.tags:
        snippet["tags"] = [t.strip() for t in a.tags.split(",") if t.strip()]
    if a.language:
        snippet["defaultLanguage"] = a.language
    if a.audio_language:
        snippet["defaultAudioLanguage"] = a.audio_language
    if a.made_for_kids is None:
        a.made_for_kids = False
    status = build_status(a)
    status.setdefault("privacyStatus", "private")
    body = {"snippet": snippet, "status": status}
    if len(a.title) > 100 or "<" in a.title or ">" in a.title:
        die("titles are at most 100 characters and can't contain < or >")
    if len(snippet["description"].encode()) > 5000:
        die("descriptions are at most 5,000 bytes")
    print(f"upload {os.path.basename(path)} ({size / 1e6:.1f} MB, {ctype}) as {status['privacyStatus']}"
          + (f", public at {status['publishAt']}" if status.get("publishAt") else "")
          + f", notify subscribers {a.notify}")
    if a.dry_run:
        print(json.dumps(body, indent=2))
        return
    status_code, headers, _ = http(
        "POST", f"{UPLOAD}/videos", params={"uploadType": "resumable", "part": "snippet,status",
                                             "notifySubscribers": str(a.notify).lower()},
        body=body, token=token(),
        headers={"X-Upload-Content-Length": str(size), "X-Upload-Content-Type": ctype})
    session = headers.get("Location")
    if not session:
        die("YouTube returned no upload session")
    video = None
    offset = 0
    with open(path, "rb") as f:
        while offset < size:
            f.seek(offset)
            chunk = f.read(CHUNK)
            end = offset + len(chunk) - 1
            for attempt in range(5):
                try:
                    code, h, resp = http("PUT", session, data=chunk, token=token(), raw=True,
                                         headers={"Content-Length": str(len(chunk)), "Content-Type": ctype,
                                                  "Content-Range": f"bytes {offset}-{end}/{size}"},
                                         ok=(200, 201, 308))
                    break
                except SystemExit:
                    if attempt == 4:
                        raise
                    time.sleep(5 * (attempt + 1))
                    # ask YouTube how much it has, then resume from there
                    code, h, resp = http("PUT", session, data=b"", token=token(), raw=True,
                                         headers={"Content-Range": f"bytes */{size}"}, ok=(200, 201, 308))
                    if code in (200, 201):
                        break
                    rng = h.get("Range")
                    offset = int(rng.split("-")[1]) + 1 if rng else 0
                    f.seek(offset)
                    chunk = f.read(CHUNK)
                    end = offset + len(chunk) - 1
            if code in (200, 201):
                video = json.loads(resp)
                break
            rng = h.get("Range")
            offset = int(rng.split("-")[1]) + 1 if rng else 0
            print(f"  sent {offset / 1e6:.1f} of {size / 1e6:.1f} MB", flush=True)
    if not video:
        die("upload ended without a video resource")
    vid = video["id"]
    print(f"uploaded: {vid}  https://youtu.be/{vid}  ({video['status']['privacyStatus']})")
    if a.thumbnail:
        set_thumbnail(vid, a.thumbnail, soft=True)
    for spec in a.captions or []:
        f, lang, name = (spec.split(":") + [None, None])[:3]
        upload_caption(vid, f, lang or a.language or "en", name or "", draft=False, soft=True)
    if a.playlist:
        add_to_playlist(a.playlist, vid, None)
    if a.wait:
        wait_processed(vid, a.wait_timeout)
    save_json(a.json_out, video)


def cmd_update(a):
    items = get_videos([a.id], "snippet,status,localizations,recordingDetails")
    if not items:
        die(f"no video {a.id} visible to this grant")
    v = items[0]
    sn = {k: v["snippet"][k] for k in ("title", "description", "tags", "categoryId", "defaultLanguage",
                                       "defaultAudioLanguage") if k in v["snippet"]}
    new_sn = dict(sn)
    if a.title is not None:
        new_sn["title"] = a.title
    desc = text_arg(a.description, a.description_file)
    if desc is not None:
        new_sn["description"] = desc
    if a.tags is not None:
        new_sn["tags"] = [t.strip() for t in a.tags.split(",") if t.strip()]
    if a.add_tags:
        new_sn["tags"] = list(dict.fromkeys(new_sn.get("tags", []) + [t.strip() for t in a.add_tags.split(",")]))
    for arg, key in (("category", "categoryId"), ("language", "defaultLanguage"),
                     ("audio_language", "defaultAudioLanguage")):
        if getattr(a, arg):
            new_sn[key] = getattr(a, arg)
    st = {k: v["status"][k] for k in WRITABLE_STATUS if k in v["status"]}
    new_st = build_status(a, v["status"])
    loc = dict(v.get("localizations", {}))
    new_loc = dict(loc)
    for spec in a.localize or []:
        lang, title, dfile = (spec.split(":", 2) + [None, None])[:3]
        entry = dict(new_loc.get(lang, {}))
        if title:
            entry["title"] = title
        if dfile:
            entry["description"] = text_arg(None, dfile)
        new_loc[lang] = entry
    for lang in a.remove_localization or []:
        new_loc.pop(lang, None)
    rec = v.get("recordingDetails", {})
    new_rec = dict(rec)
    if a.recording_date:
        new_rec["recordingDate"] = a.recording_date

    body, parts, changes = {"id": a.id}, [], []
    for part, old, new in (("snippet", sn, new_sn), ("status", st, new_st), ("localizations", loc, new_loc),
                           ("recordingDetails", rec, new_rec)):
        if new != old:
            parts.append(part)
            body[part] = new
            for k in sorted(set(old) | set(new)):
                if old.get(k) != new.get(k):
                    changes.append(f"  {part}.{k}: {short(json.dumps(old.get(k)), 70)} -> "
                                   f"{short(json.dumps(new.get(k)), 70)}")
    if "localizations" in parts and not new_sn.get("defaultLanguage"):
        die("localizations need the video's default language set; add --language")
    if "localizations" in parts and "snippet" not in parts:
        parts.append("snippet")  # the API needs snippet.defaultLanguage alongside localizations
        body["snippet"] = new_sn
    if not changes:
        print("nothing to change")
        return
    print(f"{a.id}: {len(changes)} change(s)")
    print("\n".join(changes))
    if a.dry_run:
        print("dry run: nothing sent")
        return
    resp = api("PUT", "/videos", {"part": ",".join(parts)}, body=body)
    print(f"updated {resp['id']}: privacy {resp.get('status', v['status']).get('privacyStatus')}")
    save_json(a.json_out, resp)


def cmd_delete(a):
    v = get_videos([a.id], "snippet")
    if not v:
        die(f"no video {a.id}")
    title = v[0]["snippet"]["title"]
    if a.confirm_title != title:
        die(f"--confirm-title must equal the video's title exactly: {title!r}")
    http("DELETE", f"{DATA}/videos", {"id": a.id}, token=token())
    print(f"deleted {a.id} ({title})")


def set_thumbnail(vid, image, soft=False):
    ctype = mimetypes.guess_type(image)[0] or "image/jpeg"
    with open(image, "rb") as f:
        data = f.read()
    try:
        resp = http("POST", f"{UPLOAD}/thumbnails/set", {"videoId": vid, "uploadType": "media"}, data=data,
                    headers={"Content-Type": ctype}, token=token())[2]
    except SystemExit as e:
        msg = str(e)
        if "forbidden" in msg and "thumbnails" in msg:
            msg = ("error: YouTube refused custom thumbnails for this channel. They need the channel's one-time "
                   "phone verification (youtube.com/verify), which only the account owner can do; on a verified "
                   "channel this refusal right after an upload clears on a retry a minute later")
        if not soft:
            sys.exit(msg)
        print(f"thumbnail not set: {msg}")
        return
    best = (resp.get("items") or [{}])[0]
    sizes = ",".join(sorted(best)) if best else "?"
    print(f"thumbnail set on {vid} ({sizes})")


def cmd_thumbnail(a):
    set_thumbnail(a.id, a.image)


# ---------- captions ----------

def upload_caption(vid, path, lang, name, draft, soft=False, replace=None):
    meta = {"snippet": {"videoId": vid, "language": lang, "name": name, "isDraft": draft}}
    if replace:
        meta = {"id": replace, "snippet": {"isDraft": draft}}
    boundary = uuid.uuid4().hex
    with open(path, "rb") as f:
        media = f.read()
    body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + media + \
        f"\r\n--{boundary}--\r\n".encode()
    try:
        resp = http("PUT" if replace else "POST", f"{UPLOAD}/captions",
                    {"uploadType": "multipart", "part": "snippet"}, data=body, token=token(),
                    headers={"Content-Type": f"multipart/related; boundary={boundary}"})[2]
    except SystemExit as e:
        if not soft:
            raise
        print(f"captions not added: {e}")
        return None
    sn = resp["snippet"]
    print(f"captions {resp['id']} {'replaced' if replace else 'added'}: {sn.get('language', lang)} "
          f"{sn.get('name', name)!r} draft {sn.get('isDraft')}")
    return resp


def cmd_captions(a):
    if a.action == "list":
        items = api("GET", "/captions", {"part": "snippet", "videoId": a.target}).get("items", [])
        table([[c["id"], c["snippet"]["language"], c["snippet"].get("trackKind"), c["snippet"].get("isDraft"),
                c["snippet"].get("status"), c["snippet"].get("name") or ""] for c in items],
              ["caption id", "lang", "kind", "draft", "status", "name"])
    elif a.action == "upload":
        if not a.file:
            die("captions upload <video id> --file captions.vtt --language en")
        upload_caption(a.target, a.file, a.language, a.name or "", a.draft, replace=a.replace)
    elif a.action == "download":
        if not a.out:
            die("captions download <caption id> --out file.vtt [--format vtt]")
        content = http("GET", f"{DATA}/captions/{a.target}", {"tfmt": a.format, "tlang": a.tlang},
                       token=token(), raw=True)[2]
        with open(a.out, "wb") as f:
            f.write(content)
        print(f"wrote {len(content)} bytes to {a.out}")
    elif a.action == "delete":
        http("DELETE", f"{DATA}/captions", {"id": a.target}, token=token())
        print(f"deleted captions {a.target}")


# ---------- playlists ----------

def add_to_playlist(pl, vid, position):
    body = {"snippet": {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}}
    if position is not None:
        body["snippet"]["position"] = position
    resp = api("POST", "/playlistItems", {"part": "snippet"}, body=body)
    print(f"added {vid} to {pl} at position {resp['snippet'].get('position')} (item {resp['id']})")
    return resp


def cmd_playlists(a):
    items = list(pages("/playlists", {"part": "snippet,status,contentDetails", "mine": "true",
                                      "maxResults": 50}, a.limit))
    table([[p["id"], p["status"]["privacyStatus"], p["contentDetails"]["itemCount"],
            short(p["snippet"]["title"], 60)] for p in items], ["playlist id", "privacy", "videos", "title"])
    save_json(a.json_out, items)


def cmd_playlist(a):
    if a.action == "create":
        body = {"snippet": {"title": a.title, "description": text_arg(a.description, a.description_file) or ""},
                "status": {"privacyStatus": a.privacy or "private"}}
        if a.language:
            body["snippet"]["defaultLanguage"] = a.language
        resp = api("POST", "/playlists", {"part": "snippet,status"}, body=body)
        print(f"created playlist {resp['id']} ({resp['status']['privacyStatus']}): {resp['snippet']['title']}")
    elif a.action == "update":
        cur = api("GET", "/playlists", {"part": "snippet,status,localizations", "id": a.target})["items"][0]
        sn = {k: cur["snippet"][k] for k in ("title", "description", "defaultLanguage") if k in cur["snippet"]}
        if a.title:
            sn["title"] = a.title
        d = text_arg(a.description, a.description_file)
        if d is not None:
            sn["description"] = d
        if a.language:
            sn["defaultLanguage"] = a.language
        st = {"privacyStatus": a.privacy or cur["status"]["privacyStatus"]}
        body, parts = {"id": a.target, "snippet": sn, "status": st}, ["snippet", "status"]
        loc = dict(cur.get("localizations", {}))
        for spec in a.localize or []:
            lang, title, dfile = (spec.split(":", 2) + [None, None])[:3]
            entry = dict(loc.get(lang, {}))
            if title:
                entry["title"] = title
            if dfile:
                entry["description"] = text_arg(None, dfile)
            loc[lang] = entry
        if a.localize:
            if not sn.get("defaultLanguage"):
                die("localizations need the playlist's default language set; add --language")
            body["localizations"], parts = loc, parts + ["localizations"]
        resp = api("PUT", "/playlists", {"part": ",".join(parts)}, body=body)
        print(f"updated playlist {resp['id']} ({resp['status']['privacyStatus']}): {resp['snippet']['title']}"
              + (f"; languages {','.join(sorted(resp.get('localizations', {})))}" if a.localize else ""))
    elif a.action == "delete":
        cur = api("GET", "/playlists", {"part": "snippet", "id": a.target}).get("items", [])
        if not cur:
            die(f"no playlist {a.target}")
        if a.confirm_title != cur[0]["snippet"]["title"]:
            die(f"--confirm-title must equal the playlist's title exactly: {cur[0]['snippet']['title']!r}")
        http("DELETE", f"{DATA}/playlists", {"id": a.target}, token=token())
        print(f"deleted playlist {a.target}")
    elif a.action == "items":
        items = list(pages("/playlistItems", {"part": "snippet,contentDetails,status", "playlistId": a.target,
                                              "maxResults": 50}, a.limit))
        table([[i["id"], i["snippet"]["position"], i["contentDetails"]["videoId"],
                i.get("status", {}).get("privacyStatus", ""), short(i["snippet"]["title"], 60)] for i in items],
              ["item id", "pos", "video", "privacy", "title"])
    elif a.action == "add":
        if not a.video:
            die("playlist add <playlist id> --video <video id> [--position N]")
        add_to_playlist(a.target, a.video, a.position)
    elif a.action == "remove":
        http("DELETE", f"{DATA}/playlistItems", {"id": a.target}, token=token())
        print(f"removed playlist item {a.target}")
    elif a.action == "move":
        cur = api("GET", "/playlistItems", {"part": "snippet", "id": a.target})["items"][0]["snippet"]
        body = {"id": a.target, "snippet": {"playlistId": cur["playlistId"], "resourceId": cur["resourceId"],
                                            "position": a.position}}
        resp = api("PUT", "/playlistItems", {"part": "snippet"}, body=body)
        print(f"moved item {a.target} to position {resp['snippet']['position']}")


# ---------- comments ----------

def comment_row(c, video=None):
    s = c["snippet"]
    return [c["id"], video or s.get("videoId", ""), s.get("publishedAt", "")[:16].replace("T", " "),
            short(s.get("authorDisplayName"), 20), s.get("likeCount", 0), short(s.get("textOriginal")
                                                                             or s.get("textDisplay"), 80)]


def cmd_comments(a):
    params = {"part": "snippet", "maxResults": 100, "order": a.order, "textFormat": "plainText"}
    if a.video:
        params["videoId"] = a.video
    else:
        params["allThreadsRelatedToChannelId"] = mine()["id"]
    if a.status:
        params["moderationStatus"] = a.status
    if a.search:
        params["searchTerms"] = a.search
    rows, threads = [], []
    for t in pages("/commentThreads", params, a.limit):
        if a.since and t["snippet"]["topLevelComment"]["snippet"]["publishedAt"] < a.since:
            continue
        threads.append(t)
        top = t["snippet"]["topLevelComment"]
        r = comment_row(top, t["snippet"].get("videoId"))
        r.insert(5, t["snippet"].get("totalReplyCount", 0))
        rows.append(r)
    table(rows, ["comment id", "video", "posted (UTC)", "author", "likes", "replies", "text"])
    save_json(a.json_out, threads)


def cmd_comment(a):
    if a.action == "thread":
        t = api("GET", "/commentThreads", {"part": "snippet,replies", "id": a.target,
                                           "textFormat": "plainText"}).get("items", [])
        if not t:
            die(f"no thread {a.target}")
        t = t[0]
        rows = [comment_row(t["snippet"]["topLevelComment"], t["snippet"].get("videoId"))]
        replies = list(pages("/comments", {"part": "snippet", "parentId": a.target, "maxResults": 100,
                                           "textFormat": "plainText"}, None))
        rows += [comment_row(r, t["snippet"].get("videoId")) for r in replies]
        table(rows, ["comment id", "video", "posted (UTC)", "author", "likes", "text"])
    elif a.action == "reply":
        text = text_arg(a.text, a.text_file)
        resp = api("POST", "/comments", {"part": "snippet"},
                   body={"snippet": {"parentId": a.target, "textOriginal": text}})
        print(f"replied: comment {resp['id']} under {a.target}")
    elif a.action == "post":
        text = text_arg(a.text, a.text_file)
        resp = api("POST", "/commentThreads", {"part": "snippet"},
                   body={"snippet": {"videoId": a.target, "topLevelComment": {"snippet": {"textOriginal": text}}}})
        print(f"posted: thread {resp['id']} on {a.target}")
    elif a.action == "edit":
        text = text_arg(a.text, a.text_file)
        resp = api("PUT", "/comments", {"part": "snippet"}, body={"id": a.target, "snippet": {"textOriginal": text}})
        print(f"edited comment {resp['id']}")
    elif a.action == "delete":
        http("DELETE", f"{DATA}/comments", {"id": a.target}, token=token())
        print(f"deleted comment {a.target}")
    elif a.action == "moderate":
        if not a.status:
            die("comment moderate <id[,id]> --status published|heldForReview|rejected [--ban]")
        http("POST", f"{DATA}/comments/setModerationStatus",
             {"id": a.target, "moderationStatus": a.status, "banAuthor": str(a.ban).lower()}, token=token())
        print(f"set {a.target} to {a.status}" + (" and banned the author" if a.ban else ""))


# ---------- channel ----------

def cmd_channel(a):
    ch = mine()
    if a.action == "show":
        b = ch.get("brandingSettings", {}).get("channel", {})
        print(f"{ch['id']}  {ch['snippet']['title']} ({ch['snippet'].get('customUrl')})")
        print(f"country {b.get('country') or ch['snippet'].get('country')}  default language "
              f"{b.get('defaultLanguage') or ch['snippet'].get('defaultLanguage')}  "
              f"trailer for non-subscribers {b.get('unsubscribedTrailer', '-')}")
        print(f"keywords: {b.get('keywords', '')}")
        print(f"description: {short(ch['snippet'].get('description'), 300)}")
        save_json(a.json_out, ch)
    elif a.action == "update":
        b = dict(ch.get("brandingSettings", {}).get("channel", {}))
        old = dict(b)
        d = text_arg(a.description, a.description_file)
        if d is not None:
            b["description"] = d
        for arg, key in (("keywords", "keywords"), ("country", "country"), ("language", "defaultLanguage"),
                         ("trailer", "unsubscribedTrailer")):
            if getattr(a, arg) is not None:
                b[key] = getattr(a, arg)
        changes = [f"  {k}: {short(json.dumps(old.get(k)), 60)} -> {short(json.dumps(b.get(k)), 60)}"
                   for k in sorted(set(old) | set(b)) if old.get(k) != b.get(k)]
        if not changes:
            print("nothing to change")
            return
        print("\n".join(changes))
        if a.dry_run:
            print("dry run: nothing sent")
            return
        api("PUT", "/channels", {"part": "brandingSettings"}, body={"id": ch["id"], "brandingSettings": {"channel": b}})
        print(f"updated channel {ch['id']}")
    elif a.action == "banner":
        if not a.image:
            die("channel banner --image banner.png (2048x1152, important content inside the middle 1235x338)")
        with open(a.image, "rb") as f:
            data = f.read()
        ctype = mimetypes.guess_type(a.image)[0] or "image/jpeg"
        resp = http("POST", f"{UPLOAD}/channelBanners/insert", {"uploadType": "media"}, data=data,
                    headers={"Content-Type": ctype}, token=token())[2]
        branding = ch.get("brandingSettings", {})
        branding.setdefault("image", {})["bannerExternalUrl"] = resp["url"]
        api("PUT", "/channels", {"part": "brandingSettings"},
            body={"id": ch["id"], "brandingSettings": {"channel": branding.get("channel", {}),
                                                       "image": branding["image"]}})
        print(f"banner uploaded and set on {ch['id']}")


def cmd_watermark(a):
    cid = mine()["id"]
    if a.action == "unset":
        http("POST", f"{DATA}/watermarks/unset", {"channelId": cid}, token=token())
        print("watermark removed")
        return
    if not a.image:
        die("watermark set --image logo.png [--timing offsetFromEnd --offset-ms 15000 --duration-ms 15000]")
    timing = {"type": a.timing, "offsetMs": a.offset_ms or 0}
    meta = {"timing": timing, "position": {"type": "corner", "cornerPosition": "topRight"}}
    if a.duration_ms:
        timing["durationMs"] = a.duration_ms
    boundary = uuid.uuid4().hex
    with open(a.image, "rb") as f:
        media = f.read()
    ctype = mimetypes.guess_type(a.image)[0] or "image/png"
    body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{boundary}\r\nContent-Type: {ctype}\r\n\r\n").encode() + media + f"\r\n--{boundary}--\r\n".encode()
    http("POST", f"{UPLOAD}/watermarks/set", {"channelId": cid, "uploadType": "multipart"}, data=body,
         headers={"Content-Type": f"multipart/related; boundary={boundary}"}, token=token())
    print(f"watermark set ({a.timing})")


# ---------- analytics and reporting ----------

def cmd_analytics(a):
    params = {"ids": "channel==MINE", "startDate": a.start, "endDate": a.end, "metrics": a.metrics,
              "dimensions": a.dimensions, "filters": a.filters, "sort": a.sort, "maxResults": a.max,
              "currency": a.currency}
    resp = api("GET", "/reports", params, base=ANALYTICS)
    headers = [h["name"] for h in resp.get("columnHeaders", [])]
    rows = resp.get("rows", [])
    if a.csv_out:
        with open(a.csv_out, "w") as f:
            f.write(",".join(headers) + "\n")
            for r in rows:
                f.write(",".join(json.dumps(x) if isinstance(x, str) and "," in x else str(x) for x in r) + "\n")
        print(f"{len(rows)} rows written to {a.csv_out}")
    fmt = [[round(x, 4) if isinstance(x, float) else x for x in r] for r in rows]
    print(f"{len(rows)} row(s), {a.start} to {a.end} (Pacific days)")
    if rows:
        table(fmt, headers, limit=a.max_rows)
    save_json(a.json_out, resp)


def cmd_reporting(a):
    if a.action == "types":
        items = api("GET", "/reportTypes", {}, base=REPORTING).get("reportTypes", [])
        for t in items:
            print(f"{t['id']}  {t.get('name', '')}" + ("  (deprecated)" if t.get("deprecateTime") else ""))
    elif a.action == "jobs":
        items = api("GET", "/jobs", {}, base=REPORTING).get("jobs", [])
        table([[j["id"], j["reportTypeId"], j.get("createTime", "")[:10], j.get("name", "")] for j in items],
              ["job id", "report type", "created", "name"])
    elif a.action == "create-job":
        resp = api("POST", "/jobs", {}, body={"reportTypeId": a.target, "name": a.name or a.target},
                   base=REPORTING)
        print(f"created job {resp['id']} for {resp['reportTypeId']}; first reports appear within about 48 hours")
    elif a.action == "delete-job":
        http("DELETE", f"{REPORTING}/jobs/{a.target}", token=token())
        print(f"deleted job {a.target}")
    elif a.action == "reports":
        params = {"createdAfter": a.since} if a.since else {}
        items = api("GET", f"/jobs/{a.target}/reports", params, base=REPORTING).get("reports", [])
        table([[r["id"], r["startTime"][:10], r["endTime"][:10], r["createTime"][:16]] for r in items],
              ["report id", "from", "to", "created"], limit=a.max_rows)
        save_json(a.json_out, items)
    elif a.action == "download":
        if not (a.job and a.out):
            die("reporting download <report id> --job <job id> --out file.csv")
        r = api("GET", f"/jobs/{a.job}/reports/{a.target}", {}, base=REPORTING)
        content = http("GET", r["downloadUrl"], token=token(), raw=True)[2]
        with open(a.out, "wb") as f:
            f.write(content)
        lines = content.count(b"\n")
        print(f"wrote {a.out}: {lines} lines, {r['startTime'][:10]} to {r['endTime'][:10]}")


# ---------- public lookups ----------

def cmd_search(a):
    params = {"part": "snippet", "q": a.query, "type": a.type, "order": a.order, "maxResults": a.max,
              "publishedAfter": a.published_after, "regionCode": a.region, "channelId": a.channel,
              "relevanceLanguage": a.language}
    if a.type == "video" and a.duration:
        params["videoDuration"] = a.duration
    items = api("GET", "/search", params).get("items", [])
    rows = []
    for i in items:
        rid = i["id"].get("videoId") or i["id"].get("channelId") or i["id"].get("playlistId")
        rows.append([rid, i["snippet"]["publishedAt"][:10], short(i["snippet"]["channelTitle"], 25),
                     short(i["snippet"]["title"], 70)])
    table(rows, ["id", "published", "channel", "title"])
    print("(search.list draws on its own 100-call daily bucket)")
    save_json(a.json_out, items)


def cmd_public_videos(a):
    vids = get_videos(a.ids.split(","), "snippet,contentDetails,statistics,status")
    rows = []
    for v in vids:
        s = v.get("statistics", {})
        rows.append([v["id"], v["snippet"]["publishedAt"][:10], iso_duration(v["contentDetails"].get("duration")),
                     s.get("viewCount", ""), s.get("likeCount", ""), s.get("commentCount", ""),
                     short(v["snippet"]["channelTitle"], 20), short(v["snippet"]["title"], 50)])
    table(rows, ["id", "published", "length", "views", "likes", "comments", "channel", "title"])
    save_json(a.json_out, vids)


def cmd_public_channel(a):
    key = a.channel
    params = {"part": "snippet,statistics,contentDetails"}
    if key.startswith("@"):
        params["forHandle"] = key
    else:
        params["id"] = key
    items = api("GET", "/channels", params).get("items", [])
    for c in items:
        s = c["statistics"]
        print(f"{c['id']}  {c['snippet']['title']} ({c['snippet'].get('customUrl')})  "
              f"subscribers {s.get('subscriberCount')}  videos {s.get('videoCount')}  views {s.get('viewCount')}  "
              f"since {c['snippet']['publishedAt'][:10]}  uploads playlist "
              f"{c['contentDetails']['relatedPlaylists']['uploads']}")
    if not items:
        print("no channel found")
    save_json(a.json_out, items)


def cmd_categories(a):
    items = api("GET", "/videoCategories", {"part": "snippet", "regionCode": a.region}).get("items", [])
    print("  ".join(f"{c['id']}={c['snippet']['title']}" for c in items if c["snippet"].get("assignable")))


def cmd_languages(a):
    items = api("GET", "/i18nLanguages", {"part": "snippet"}).get("items", [])
    print("  ".join(f"{c['snippet']['hl']}={c['snippet']['name']}" for c in items))


def cmd_raw(a):
    params = dict(kv.split("=", 1) for kv in a.params)
    body = load_json(a.body_file) if a.body_file else None
    base = {"data": DATA, "analytics": ANALYTICS, "reporting": REPORTING}[a.api]
    resp = api(a.method.upper(), a.path, params, body=body, base=base)
    text = json.dumps(resp, indent=2)
    if a.json_out:
        save_json(a.json_out, resp)
    print(text if len(text) <= a.max_chars else text[: a.max_chars] + f"\n... ({len(text)} chars; use --json-out)")


# ---------- arguments ----------

def tristate(p, name, dest, help_on, help_off):
    g = p.add_mutually_exclusive_group()
    g.add_argument(f"--{name}", dest=dest, action="store_true", default=None, help=help_on)
    g.add_argument(f"--no-{name}", dest=dest, action="store_false", help=help_off)


def video_meta_args(p, upload):
    p.add_argument("--title", required=upload)
    p.add_argument("--description")
    p.add_argument("--description-file")
    p.add_argument("--tags", help="comma-separated; replaces the tag list")
    p.add_argument("--category", help="category id (`yt.py categories`), e.g. 20 Gaming, 27 Education")
    p.add_argument("--language", help="default language of title and description, e.g. en")
    p.add_argument("--audio-language", help="spoken language, e.g. en")
    p.add_argument("--privacy", choices=["private", "unlisted", "public"])
    p.add_argument("--publish-at", help="RFC 3339 UTC time to go public, e.g. 2026-11-01T15:00:00Z; forces private")
    tristate(p, "made-for-kids", "made_for_kids", "declare made for kids", "declare not made for kids")
    tristate(p, "synthetic", "synthetic", "declare realistic altered or synthetic content",
             "declare no realistic altered or synthetic content")
    tristate(p, "embeddable", "embeddable", "allow embedding", "block embedding")
    tristate(p, "public-stats", "public_stats", "show view counts publicly", "hide view counts")
    p.add_argument("--license", choices=["youtube", "creativeCommon"])
    p.add_argument("--json-out")


def main():
    p = argparse.ArgumentParser(prog="yt.py", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login", help="sign the channel in (writes the grant file)")
    s.add_argument("--url-file", required=True, help="private file the Google sign-in address is written to")
    s.add_argument("--timeout", type=int, default=900)
    s.set_defaults(fn=cmd_login)

    s = sub.add_parser("whoami", help="the signed-in channel and the grant's scopes")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_whoami)

    s = sub.add_parser("videos", help="our channel's videos, newest first, every privacy")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--privacy", default="all", choices=["all", "public", "unlisted", "private"])
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_videos)

    s = sub.add_parser("video", help="one video's state: privacy, processing, file, numbers, settings")
    s.add_argument("id")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_video)

    s = sub.add_parser("upload", help="upload a video (resumable), then optional thumbnail, captions, playlist")
    s.add_argument("file")
    video_meta_args(s, upload=True)
    s.add_argument("--notify", action="store_true", help="notify subscribers (off by default)")
    s.add_argument("--thumbnail")
    s.add_argument("--captions", action="append", help="file[:lang[:name]], repeatable")
    s.add_argument("--playlist", help="playlist id to add the video to")
    s.add_argument("--wait", action="store_true", help="wait until YouTube finishes processing")
    s.add_argument("--wait-timeout", type=int, default=1200)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_upload)

    s = sub.add_parser("update", help="change a video's settings; reads the video first and changes only what you pass")
    s.add_argument("id")
    video_meta_args(s, upload=False)
    s.add_argument("--add-tags", help="comma-separated tags to add")
    s.add_argument("--clear-publish-at", action="store_true", help="cancel a scheduled release")
    s.add_argument("--localize", action="append", help="lang:title[:description-file], repeatable")
    s.add_argument("--remove-localization", action="append")
    s.add_argument("--recording-date", help="RFC 3339, e.g. 2026-10-20T00:00:00Z")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_update)

    s = sub.add_parser("delete", help="delete one of our videos (cannot be undone)")
    s.add_argument("id")
    s.add_argument("--confirm-title", required=True)
    s.set_defaults(fn=cmd_delete)

    s = sub.add_parser("thumbnail", help="set a custom thumbnail")
    s.add_argument("id")
    s.add_argument("image")
    s.set_defaults(fn=cmd_thumbnail)

    s = sub.add_parser("captions", help="list | upload | download | delete caption tracks")
    s.add_argument("action", choices=["list", "upload", "download", "delete"])
    s.add_argument("target", help="video id (list, upload) or caption id (download, delete)")
    s.add_argument("--file")
    s.add_argument("--language", default="en")
    s.add_argument("--name", default="")
    s.add_argument("--draft", action="store_true")
    s.add_argument("--replace", help="caption id to replace with --file")
    s.add_argument("--format", default="vtt", choices=["vtt", "srt", "sbv", "scc", "ttml"])
    s.add_argument("--tlang", help="machine-translate on download into this language")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_captions)

    s = sub.add_parser("playlists", help="our playlists")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_playlists)

    s = sub.add_parser("playlist", help="create | update | delete | items | add | remove | move")
    s.add_argument("action", choices=["create", "update", "delete", "items", "add", "remove", "move"])
    s.add_argument("target", nargs="?", help="playlist id, or playlist item id for remove and move")
    s.add_argument("--title")
    s.add_argument("--description")
    s.add_argument("--description-file")
    s.add_argument("--privacy", choices=["private", "unlisted", "public"])
    s.add_argument("--language")
    s.add_argument("--localize", action="append", help="lang:title[:description-file] (update), repeatable")
    s.add_argument("--video")
    s.add_argument("--position", type=int)
    s.add_argument("--confirm-title")
    s.add_argument("--limit", type=int, default=200)
    s.set_defaults(fn=cmd_playlist)

    s = sub.add_parser("comments", help="comment threads on our channel or one video")
    s.add_argument("--video")
    s.add_argument("--status", choices=["published", "heldForReview", "likelySpam"])
    s.add_argument("--search")
    s.add_argument("--since", help="ISO date; only threads started on or after it")
    s.add_argument("--order", default="time", choices=["time", "relevance"])
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_comments)

    s = sub.add_parser("comment", help="thread | reply | post | edit | delete | moderate")
    s.add_argument("action", choices=["thread", "reply", "post", "edit", "delete", "moderate"])
    s.add_argument("target", help="thread id (thread), parent comment id (reply), video id (post), comment id(s)")
    s.add_argument("--text")
    s.add_argument("--text-file")
    s.add_argument("--status", choices=["published", "heldForReview", "rejected"])
    s.add_argument("--ban", action="store_true")
    s.set_defaults(fn=cmd_comment)

    s = sub.add_parser("channel", help="show | update | banner")
    s.add_argument("action", choices=["show", "update", "banner"])
    s.add_argument("--description")
    s.add_argument("--description-file")
    s.add_argument("--keywords", help="space-separated; quote multi-word keywords")
    s.add_argument("--country")
    s.add_argument("--language")
    s.add_argument("--trailer", help="video id shown to visitors who aren't subscribed")
    s.add_argument("--image", help="banner image (banner)")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_channel)

    s = sub.add_parser("watermark", help="set | unset the branding watermark on our videos")
    s.add_argument("action", choices=["set", "unset"])
    s.add_argument("--image")
    s.add_argument("--timing", default="offsetFromEnd", choices=["offsetFromStart", "offsetFromEnd"])
    s.add_argument("--offset-ms", type=int)
    s.add_argument("--duration-ms", type=int)
    s.set_defaults(fn=cmd_watermark)

    s = sub.add_parser("analytics", help="YouTube Analytics reports.query for our channel")
    s.add_argument("--metrics", required=True)
    s.add_argument("--dimensions")
    s.add_argument("--filters", help="e.g. video==ID or country==US;video==ID")
    s.add_argument("--start", required=True)
    s.add_argument("--end", required=True)
    s.add_argument("--sort", help="write a descending sort with '=': --sort=-views")
    s.add_argument("--max", type=int)
    s.add_argument("--currency")
    s.add_argument("--max-rows", type=int, default=40)
    s.add_argument("--csv-out")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_analytics)

    s = sub.add_parser("reporting", help="types | jobs | create-job | delete-job | reports | download")
    s.add_argument("action", choices=["types", "jobs", "create-job", "delete-job", "reports", "download"])
    s.add_argument("target", nargs="?", help="report type id, job id, or report id")
    s.add_argument("--name")
    s.add_argument("--job")
    s.add_argument("--since", help="RFC 3339; reports created after it")
    s.add_argument("--out")
    s.add_argument("--max-rows", type=int, default=30)
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_reporting)

    s = sub.add_parser("search", help="search public YouTube (100-call daily bucket)")
    s.add_argument("query")
    s.add_argument("--type", default="video", choices=["video", "channel", "playlist"])
    s.add_argument("--order", default="relevance", choices=["relevance", "date", "viewCount", "rating", "title"])
    s.add_argument("--max", type=int, default=10)
    s.add_argument("--published-after", help="RFC 3339")
    s.add_argument("--region", help="two-letter country, e.g. US")
    s.add_argument("--channel", help="only this channel id")
    s.add_argument("--language", help="relevance language, e.g. en")
    s.add_argument("--duration", choices=["short", "medium", "long"])
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("public-videos", help="public numbers for any videos")
    s.add_argument("ids", help="comma-separated video ids")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_public_videos)

    s = sub.add_parser("public-channel", help="any channel by @handle or id")
    s.add_argument("channel")
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_public_channel)

    s = sub.add_parser("categories", help="assignable video categories")
    s.add_argument("--region", default="US")
    s.set_defaults(fn=cmd_categories)

    s = sub.add_parser("languages", help="language codes for localizations and captions")
    s.set_defaults(fn=cmd_languages)

    s = sub.add_parser("raw", help="any other API call: raw GET /channelSections part=snippet mine=true")
    s.add_argument("method")
    s.add_argument("path")
    s.add_argument("params", nargs="*", help="key=value query parameters")
    s.add_argument("--api", default="data", choices=["data", "analytics", "reporting"])
    s.add_argument("--body-file")
    s.add_argument("--max-chars", type=int, default=3000)
    s.add_argument("--json-out")
    s.set_defaults(fn=cmd_raw)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
