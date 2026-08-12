---
name: transcribe-audio
description: "Transcribe recorded audio or video speech into a saved plain-text file with the user's OpenAI API access. Use for local M4A, MP3, WAV, MP4, or similar media, especially when the user asks for the latest OpenAI transcription model, long-recording chunking, or explicit parallel processing. Discover the newest eligible model live and adapt to its supported API instead of choosing an older upload model for convenience. Do not use for speech generation, audio editing, summary-only requests, subtitle timing, or live microphone captioning."
metadata:
  short-description: "Transcribe recordings with current OpenAI models"
---

# Transcribe Audio

Turn a recorded media file into a complete, verified plain-text transcript.
Resolve the source, use the OpenAI model the user actually requested, adapt the
transport to that model, and save the result without changing the source file.

## When to use

- "Transcribe this M4A and save it as text."
- "Find the recording in Downloads and transcribe it."
- "Use the latest OpenAI transcription model."
- "Transcribe this long recording in parallel."
- "Make a plain-text transcript of this video."

## When not to use

- The user wants speech generation, voice cloning, or audio editing.
- The deliverable is only a summary, notes, or analysis with no transcript.
- The request is for timed subtitles, caption files, translation, or live
  microphone captioning.
- The user named a provider other than OpenAI.

## Non-negotiables

- Treat model choice and API transport as separate decisions. If the newest
  eligible model is realtime-only, use its supported transcription transport
  for the prerecorded audio instead of silently choosing an older upload model.
- Establish model recency, transcription capability, endpoint support, input
  format, and current limits from official OpenAI sources at execution time.
  Remembered model names are leads, not evidence.
- Never print, echo, paste, commit, or place the OpenAI API key in command
  arguments, logs, transcripts, or user-visible output.
- Preserve complete timeline coverage and source order across every chunk.
  Completion order is never transcript order.
- Keep the source untouched. The final file contains transcript text only,
  with no Markdown wrapper, chunk labels, API events, or agent commentary.

## Model selection contract

- When the user says "latest" or "newest," select by current release recency
  among models officially documented for faithful speech transcription. Do not
  reinterpret this as "newest model accepted by the convenient file endpoint."
- Cross-check the official model documentation with the authenticated model
  catalog available to the user's account. Documentation proves capability;
  the account catalog proves availability.
- Follow the chosen model's current API reference. A realtime-only model means
  streaming the prerecorded audio through a transcription session in the
  documented format, not opening a microphone and not falling back silently.
- If the newest eligible model is unavailable to the account, report that
  exact blocker and ask before using an older model.
- "Best" or "most accurate" is a different request from "latest." For those
  asks, use current documented quality and task fit rather than release date.

## First move

1. Resolve the exact source file and requested output path from the user's
   words and available local files.
2. Inspect media type, duration, size, codec, channels, and sample rate with
   `ffprobe` or an equivalent local probe.
3. Confirm OpenAI credentials are available without revealing their value.
4. Discover and verify the requested model, supported transport, input format,
   and current request or session limits from official OpenAI sources.
5. Choose the smallest execution plan that preserves quality and honors any
   explicit concurrency request.

Only ask a question when multiple source files remain genuinely plausible, the
requested output would overwrite an existing file, or a model fallback needs
approval. A clear request to transcribe with OpenAI already authorizes the
normal API calls required for that recording.

## Workflow

1. **Resolve and inspect**: prefer the named path. If the user points to a
   folder, inspect likely media files and use modification time or wording only
   when it identifies one clear target.
2. **Select model and transport**: verify the live model contract before
   conversion. Choose the API around the model, not the model around the API
   code that is easiest to write.
3. **Prepare audio**: convert only when the chosen transport requires it.
   Preserve intelligible speech, use the documented channel and sample-rate
   format, and put generated audio in a task-specific temporary directory.
4. **Transcribe**: send the whole file when it fits. Otherwise split near
   natural pauses when practical, record each chunk's timeline index, and
   transcribe the independent chunks with bounded concurrency.
5. **Assemble and verify**: join successful chunks by timeline index, resolve
   only obvious duplicated boundary text, write the final file atomically, and
   remove task-created temporary audio after success.

## Parallel recordings

- Treat requested parallelism as a worker limit over independent API work
  units. For chunked recordings, those units are normally chunk requests or
  transcription sessions. For long recordings that need chunking, target a
  12-worker pool by default. A user-specified concurrency replaces that
  default; if provider limits reject it, reduce only enough to finish and
  report the effective concurrency.
- Choose chunk duration with the selected model's current context, output,
  request, and session limits in view. Do not create tiny chunks solely to keep
  every worker busy.
- Keep a numbered manifest with source offsets, chunk paths, attempt status,
  and transcript paths outside the final transcript.
- Retry failed chunks without rerunning successful ones, then assemble only
  when every manifest entry has a final transcript.
- Concatenate by source offset, never by response arrival time. Inspect joins
  for missing speech, repeated phrases, or partial words.

## Output and verification

- If the user gives no output path, save beside the source as `<stem>.txt`. If
  that path exists, choose a clear non-conflicting transcript filename rather
  than overwrite it.
- Save UTF-8 plain text. Preserve wording and readable paragraph breaks; do not
  summarize, polish, censor, or invent speaker labels.
- Verify that the file is nonempty and valid UTF-8, every planned chunk is
  represented exactly once, and the beginning, joins, and ending are coherent.
- Do not publish a partial transcript under the final filename. Keep resumable
  task-created chunk artifacts if an API failure prevents completion.
- Report the final path, exact model id, source duration, chunk count, and
  effective concurrency. Keep API events and raw responses out of the reply
  unless the user asks for debugging details.

## Completion line

The task is complete only when the full recording has a nonempty verified
plain-text transcript at the reported path and the exact OpenAI model used is
known.
