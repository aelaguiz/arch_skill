"""The --help text for decision_deck.py, the video evidence kind (decision_deck_video.py): keys, limits, what plays on an
iPhone. decision_deck_help.HELP joins it after the table kind; the limits are read from decision_deck_video.py, so the
text and the checks cannot disagree."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_deck_video import CLIPS_MAX, MAX_CLIP_BYTES, MAX_DECK_BYTES  # noqa: E402

MB = 1024 * 1024

VIDEO_HELP = f"""    {{"kind": "video", "clips": [1 to {CLIPS_MAX} of {{exactly one of "option" (an option id, a string; its tab
     reads the option's label) or "label" (a non-empty string: a clip that is no option), "file" (an .mp4 or .webm
     file, a path relative to the spec's folder), "caption"? (default: the option's caption)}}]}}: clips the owner
     plays on the slide itself. Motion, sound or video to approve (an animation, a screen recording, anything that
     moves or makes a sound) goes here, playable on the slide, never as still frames or a description. Each clip
     is one player with its controls; nothing plays until the owner presses play, it plays with its sound, and it
     never loops. One clip shows alone. With two or more, the desktop shows one player (a fixed 16:9 box as tall
     as the evidence zone, whatever the clip's shape, the clip drawn whole inside it on black) under a tab per
     clip in spec order (V steps to the next) and the shown clip's caption; the recommended option's clip shows
     first, and a tab never answers (the answer buttons do). Showing another clip or leaving the slide pauses the
     one playing. On a phone every clip is on the page, one per row at full width, its label above it and its
     caption under it. An option gives at most one clip, and its caption sits with its clip, not in the context
     line. Example, two clips tied to options:
       "evidence": {{"kind": "video", "clips": [{{"option": "today", "file": "today.mp4"}},
                    {{"option": "new", "file": "new.mp4", "caption": "The new intro, with its chime."}}]}}
     The file rules, each refused as a spec error naming the decision and the clip: inside the spec's folder
     (no absolute path, no "..", no symlink anywhere on the way, no part of the path starting with "."); ending in
     .mp4 or .webm; not empty; its first bytes an MP4 file's ftyp box (.mp4) or a WebM file's EBML header (.webm);
     at most {MAX_CLIP_BYTES // MB} MB a clip and {MAX_DECK_BYTES // MB} MB for all of a deck's clips together.
     What plays everywhere, iPhone Safari included: MP4 with H.264 video (yuv420p) and AAC sound. WebM (VP9 or VP8
     with Opus or Vorbis) plays in Chrome and Firefox but not on every iPhone, so give MP4 for anything the owner
     may open on a phone. Make one from any recording with ffmpeg:
       ffmpeg -i in.mov -c:v libx264 -pix_fmt yuv420p -crf 23 -vf "scale=-2:720" -c:a aac -b:a 128k \\
         -movflags +faststart out.mp4
     (-movflags +faststart puts the index first so the clip starts before it has all loaded; scale=-2:720 makes it
     720 px tall with an even width; drop -vf to keep its size; a clip with no sound needs no -c:a.) Check it with
     `ffprobe -v error -show_entries stream=codec_name,pix_fmt -of csv=p=0 out.mp4`: "h264,yuv420p" then "aac".
     Served at /clip/<sha16>.<ext> (the first 16 hex digits of its SHA-256), with byte ranges (iPhone Safari plays
     nothing from a server without them). serve reads each clip once at start and serves only those bytes from
     memory; it refuses a clip that is now reached through a symlink at any folder on the way, is no longer a
     regular file or is over the limits, naming it, and the check stamp names a clip changed since the check.
     decision_deck_check.py checks a deck with a video decision in the installed Google Chrome (Playwright's own
     Chromium plays no H.264 or AAC) and plays each clip there: a clip that does not play is a VIDEO problem. A
     sound with no picture is not a clip: record it over a still picture.
"""
