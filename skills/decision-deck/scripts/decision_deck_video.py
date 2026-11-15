"""Decision deck "video" evidence: one to four clips the owner plays on the slide itself, with their sound.

For approving motion, sound or video: an animation, a screen recording, anything that moves or makes a sound is
shown playable on the slide, never as still frames or a description.

Spec: {"kind": "video", "clips": [1 to 4 of {"option": <option id> | "label": <text>, "file", "caption"?}]}
(decision_deck.py --help). A clip is an existing .mp4 (an ftyp box first) or .webm (an EBML header first) file inside
the spec's folder, named by a path relative to it with no "..", no hidden segment and no symlink on the way, not
empty and at most MAX_CLIP_BYTES; a deck's clips together hold at most MAX_DECK_BYTES. Every problem is a spec error
naming the decision and the clip. The tab reads the option's label (or the clip's own label); the caption is the
clip's, else the option's. The recommended option's clip shows first, else the first clip.

Serving (decision_deck_video_serve.py): GET /clip/<sha16>.<ext>, the first 16 hex digits of the clip's SHA-256, from
the bytes snapshot() read once when the server started (through open_clip: one path part at a time from the spec's
folder, never through a symlink, a regular file only), and served from memory with byte ranges, which iPhone Safari
needs. The check stamp records each clip's hash, so a stamp mismatch names the changed clip. The slide, its look and
its script: decision_deck_video_slide.py. Stdlib only.
"""
from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path, PurePosixPath

KIND = "video"
CLIPS_MAX = 4
MAX_CLIP_BYTES = 50 * 1024 * 1024       # one clip, read into memory by serve
MAX_DECK_BYTES = 200 * 1024 * 1024      # every clip of a deck together
CLIP_MIME = {".mp4": "video/mp4", ".webm": "video/webm"}
EBML = b"\x1a\x45\xdf\xa3"              # a WebM (Matroska) file's first four bytes


class ClipTooBig(OSError):
    """A clip, or a deck's clips together, over the caps; serve refuses the deck (exit 2)."""


class ClipPathError(OSError):
    """A clip reached through a symlink, or no longer a regular file, when its bytes are read; serve refuses (exit 2).
    `why` is the refusal without the clip's name, as the spec check words it."""

    def __init__(self, where: str, why: str):
        super().__init__(f"{where} {why}")
        self.why = why


def has_video(spec: dict) -> bool:
    """True when any decision of a loaded spec shows video evidence."""
    return any((d.get("evidence") or {}).get("kind") == KIND for d in spec["decisions"])


# ------------------------------------------------------------------ spec

def _kind_of(head: bytes) -> str:
    """".mp4" when the bytes open with an MP4 ftyp box, ".webm" with an EBML header, else ""."""
    if len(head) >= 8 and head[4:8] == b"ftyp":
        return ".mp4"
    return ".webm" if head[:4] == EBML else ""


def rel_of(file: str) -> str:
    """A clip's key in clip_files() and the snapshot: its path under the spec's folder, posix, as the spec names it
    less any "." part (the spec check has refused "..", absolute paths, hidden parts and symlinks)."""
    return PurePosixPath(*[p for p in PurePosixPath(file.replace("\\", "/")).parts if p != "."]).as_posix()


def clip_path(root: Path, file: str) -> tuple[Path | None, str]:
    """(the clip's resolved path, "") or (None, why it is refused): the path checks that need no reading."""
    if Path(file).is_absolute() or file.startswith(("/", "\\", "~")):
        return None, "must be a path relative to the spec's folder (it is outside it)"
    parts = PurePosixPath(file.replace("\\", "/")).parts
    if ".." in parts:
        return None, "is outside the spec's folder (a '..' in the path)"
    if any(p.startswith(".") and p != "." for p in parts):
        return None, "has a hidden name (a part starting with '.'); name a visible file"
    if Path(file).suffix.lower() not in CLIP_MIME:
        return None, "must end in .mp4 or .webm"
    here = root
    for part in parts:
        if part == ".":
            continue
        here = here / part
        try:
            mode = os.lstat(here).st_mode
        except OSError:
            return None, f"not found under {root}"
        if stat.S_ISLNK(mode):
            return None, f"is reached through a symlink ({here.name}); name the file by its real path"
    path = here.resolve()
    if not path.is_relative_to(root):
        return None, "is outside the spec's folder"
    if not path.is_file():
        return None, "is not a file"
    return path, ""


def open_clip(root: Path, rel: str) -> int:
    """A read-only descriptor on the clip `rel` (posix, under `root`), reached race-free: each folder is opened
    with O_NOFOLLOW | O_DIRECTORY relative to the one before (dir_fd), then the file with O_NOFOLLOW, and fstat
    must call it a regular file. `root`, the spec's folder, is trusted as given. Raises ClipPathError naming the
    clip and the part when a part is a symlink or the file is not a regular file; every other descriptor is closed
    on every path, and the caller closes the one returned."""
    parts = [p for p in rel.split("/") if p not in ("", ".")]
    where = f"clip {(root / rel).as_posix()}"
    dfd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for k, part in enumerate(parts):
            last = k == len(parts) - 1
            flags = os.O_RDONLY | os.O_NOFOLLOW | (os.O_NONBLOCK if last else os.O_DIRECTORY)
            try:
                fd = os.open(part, flags, dir_fd=dfd)
            except OSError as exc:
                try:
                    mode = os.stat(part, dir_fd=dfd, follow_symlinks=False).st_mode
                except OSError:
                    raise exc from None
                if stat.S_ISLNK(mode):
                    raise ClipPathError(where, f"is reached through a symlink ({'/'.join(parts[:k + 1])}); "
                                               "name the file by its real path") from None
                if not last:
                    raise ClipPathError(where, f"is reached through {'/'.join(parts[:k + 1])}, "
                                               "which is not a folder") from None
                raise
            os.close(dfd)
            dfd = fd
            if last:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    raise ClipPathError(where, "is not a regular file")
                os.set_blocking(fd, True)
                dfd = -1
                return fd
        raise ClipPathError(where, "names no file")
    finally:
        if dfd >= 0:
            os.close(dfd)


def _clip_problem(root: Path, file: str, sizes: dict) -> str:
    """Why the clip `file` cannot be a clip (reached through a symlink, not a regular file, empty, too big,
    unreadable, wrong leading bytes), or "", reading it through open_clip; its size goes in `sizes`."""
    try:
        with os.fdopen(open_clip(root, rel_of(file)), "rb") as fh:
            size = os.fstat(fh.fileno()).st_size
            head = fh.read(16)
    except ClipPathError as exc:
        return exc.why
    except OSError as exc:
        return f"cannot be read ({exc.strerror or exc})"
    sizes[file] = size
    if size == 0:
        return "is empty"
    if size > MAX_CLIP_BYTES:
        return (f"is {size} bytes, over the {MAX_CLIP_BYTES // (1024 * 1024)} MB a clip may hold; send a shorter or "
                "smaller clip")
    kind = _kind_of(head)
    if not kind:
        return "is not an MP4 (no ftyp box) or WebM (no EBML header) file"
    if kind != Path(file).suffix.lower():
        return f"holds {'an MP4' if kind == '.mp4' else 'a WebM'} file under a {Path(file).suffix} name; name it {kind}"
    return ""


def check_video(dec: dict, ev: dict, ew: str, root: Path, errors: list, deck: dict) -> None:
    """Append every problem with a video evidence object; never raises on any JSON value. `deck` carries the bytes
    counted so far across the spec's video decisions ({"bytes": n, "seen": set of paths}), so the deck cap names the
    clip that crosses it."""
    clips = ev.get("clips")
    if not isinstance(clips, list) or not 1 <= len(clips) <= CLIPS_MAX:
        errors.append(f"{ew}: 'clips' must be a list of 1 to {CLIPS_MAX} clips, each {{\"option\" or \"label\", "
                      "\"file\", \"caption\"?}")
        return
    opt_ids = {o.get("id") for o in dec.get("options") or [] if isinstance(o, dict) and isinstance(o.get("id"), str)}
    clipped: set = set()
    for k, clip in enumerate(clips, 1):
        cw = f"{ew} clip {k}"
        if not isinstance(clip, dict):
            errors.append(f"{cw}: must be an object with 'option' or 'label', 'file' and an optional 'caption'")
            continue
        given = [key for key in ("option", "label") if key in clip]     # by key presence, whatever the value
        if len(given) == 2:
            errors.append(f"{cw}: give 'option' or 'label', not both (an option's clip reads its label)")
        elif not given:
            errors.append(f"{cw}: needs 'option' (an option id) or 'label' (a clip that is no option)")
        elif given == ["option"]:
            oid = clip["option"]
            if not isinstance(oid, str):
                errors.append(f"{cw}: 'option' must be an option id (a string), not {oid!r}")
            elif oid not in opt_ids:
                errors.append(f"{cw}: names option {oid!r}, which is not an option here")
            elif oid in clipped:
                errors.append(f"{cw}: option {oid!r} has two clips; give each option one")
            else:
                clipped.add(oid)
        elif not isinstance(clip["label"], str) or not clip["label"].strip():
            errors.append(f"{cw}: 'label' must be a non-empty string")
        if "caption" in clip and (not isinstance(clip["caption"], str) or not clip["caption"].strip()):
            errors.append(f"{cw}: 'caption' must be a non-empty string")
        file = clip.get("file")
        if not isinstance(file, str) or not file.strip() or "\x00" in file:
            errors.append(f"{cw}: 'file' must be a non-empty string, the clip's path relative to the spec's folder")
            continue
        try:
            file.encode("utf-8")
        except UnicodeEncodeError:            # a JSON-escaped lone surrogate: no file can have this name
            errors.append(f"{cw}: 'file' {file!r} is not a valid file name (it holds a character no file name can)")
            continue
        path, why = clip_path(root, file)
        sizes: dict = {}
        why = why or _clip_problem(root, file, sizes)
        if why:
            errors.append(f"{cw}: clip '{file}' {why}")
            continue
        if path not in deck["seen"]:
            deck["seen"].add(path)
            deck["bytes"] += sizes[file]
            if deck["bytes"] > MAX_DECK_BYTES:
                errors.append(f"{cw}: clip '{file}' takes the deck's clips over {MAX_DECK_BYTES // (1024 * 1024)} MB "
                              "in all; send fewer or smaller clips")


def clips_of(dec: dict, ev: dict) -> dict:
    """The normalized evidence: {"kind": "video", "clips": [{label, caption, file, option}], "start": index}."""
    opts = {o["id"]: o for o in dec["options"]}
    out = []
    for clip in ev["clips"]:
        opt = opts[clip["option"]] if "option" in clip else None     # validated: a string id of this decision
        out.append({"label": opt["label"] if opt else clip["label"],
                    "caption": clip.get("caption") or (opt.get("caption") or "" if opt else ""),
                    "file": clip["file"], "option": opt["id"] if opt else None})
    rec = (dec.get("recommendation") or {}).get("option")
    start = next((k for k, c in enumerate(out) if rec and c["option"] == rec), 0)
    return {"kind": KIND, "clips": out, "start": start}


def clipped_options(dec: dict) -> set:
    """The ids of the options a video decision shows a clip for (their captions sit with their clips)."""
    ev = dec.get("evidence") if isinstance(dec.get("evidence"), dict) else {}
    if ev.get("kind") != KIND:
        return set()
    return {c["option"] for c in ev.get("clips") or [] if isinstance(c, dict) and isinstance(c.get("option"), str)}


def clip_files(spec: dict) -> dict[str, Path]:
    """{the clip's path under the spec's folder, posix: its file} for every clip of a video decision, in spec order."""
    out: dict[str, Path] = {}
    for dec in spec["decisions"]:
        ev = dec.get("evidence") if isinstance(dec.get("evidence"), dict) else {}
        if ev.get("kind") != KIND:
            continue
        for clip in ev["clips"]:
            rel = rel_of(clip["file"])
            out.setdefault(rel, spec["root"] / rel)    # not resolved: a symlink put in its place is refused on read
    return out


# ------------------------------------------------------------------ the snapshot serve holds

def _read(root: Path, rel: str, room: int) -> bytes:
    """The clip's bytes, reached through open_clip (no symlink at any part since the spec was loaded, a regular
    file), reading at most one byte past the caps (MAX_CLIP_BYTES, and `room` left of MAX_DECK_BYTES)."""
    path = root / rel
    with os.fdopen(open_clip(root, rel), "rb") as fh:
        body = fh.read(min(MAX_CLIP_BYTES, room) + 1)
    if len(body) > MAX_CLIP_BYTES:
        raise ClipTooBig(f"clip {path} is over {MAX_CLIP_BYTES} bytes, the most one clip may hold")
    if len(body) > room:
        raise ClipTooBig(f"the deck's clips are over {MAX_DECK_BYTES} bytes in all (at {path})")
    if not body or _kind_of(body[:16]) != path.suffix.lower():
        raise OSError(f"clip {path} is no longer a {path.suffix} file (empty or other bytes since the spec loaded)")
    return body


def snapshot(spec: dict) -> dict[str, tuple[bytes, str]]:
    """{the clip's path under the spec's folder: (bytes, content type)} for every clip, each read once now through
    open_clip. The server takes it at start and serves only these bytes for its life; the stamp's digest reads clips
    only through it. Raises OSError when a clip cannot be read: ClipPathError (a symlink at any part, not a regular
    file), ClipTooBig past the caps."""
    out, used = {}, 0
    for rel, path in clip_files(spec).items():
        body = _read(spec["root"], rel, MAX_DECK_BYTES - used)
        used += len(body)
        out[rel] = (body, CLIP_MIME[path.suffix.lower()])
    return out


def manifest(snap: dict) -> dict[str, str]:
    """{clip path: SHA-256 of its bytes}: what the stamp records, so a stamp mismatch names the changed clip."""
    return {rel: hashlib.sha256(body).hexdigest() for rel, (body, _) in snap.items()}


def routes_of(snap: dict) -> tuple[dict[str, str], dict[str, tuple[bytes, str]]]:
    """({clip path: its URL, /clip/<sha16>.<ext>}, {"<sha16>.<ext>": (bytes, content type)}) from the snapshot."""
    urls, by_name = {}, {}
    for rel, (body, ctype) in snap.items():
        name = hashlib.sha256(body).hexdigest()[:16] + Path(rel).suffix.lower()
        urls[rel] = "/clip/" + name
        by_name[name] = (body, ctype)
    return urls, by_name


# ------------------------------------------------------------------ text (decision_deck.py text and asks)

def video_lines(ev: dict, flat) -> list[str]:
    """The clips as `decision_deck.py text` writes them: by tab label and caption, the one shown first marked; never a
    file name (the reader's words only)."""
    one = len(ev["clips"]) == 1
    out = ["[Evidence: a video clip that plays on the slide when pressed, with its sound]" if one else
           "[Evidence: video clips in one player, a tab per clip; each plays on the slide when pressed, with its sound]"]
    for k, clip in enumerate(ev["clips"]):
        first = " (shown first)" if k == ev["start"] and not one else ""
        cap = f": {flat(clip['caption'])}" if clip["caption"] else ""
        out.append(f'Clip "{flat(clip["label"])}"{first}{cap}')
    return out
