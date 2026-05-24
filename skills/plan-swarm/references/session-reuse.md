# Session Reuse

Resume workers when continuity helps and the session is healthy.

## Resume By Default When

- The repair is directly related to the worker's previous slice.
- The worker understood the owning surface.
- The worker reported `SESSION HEALTH: healthy`.
- The session id was captured for the same runtime.

## Spawn Fresh When

- The worker is stuck, repeatedly wrong, or causing bugs.
- The repair crosses into a different owner boundary.
- The session id is missing, empty, or `UNRECOVERABLE`.
- The parent needs a cold implementation view.

## Quiet Workers And Stall Judgment

Quiet is not the same as stuck. Big implementation slices, high-thinking
models, long-running tests, sleeps, simulators, generators, installs, and
scarce-resource waits can naturally produce little or no visible event stream
for meaningful time.

After roughly five minutes with no event stream, report, log movement, or other
visible progress, the parent may start evaluating the worker. That is an
inspection threshold, not an abandonment threshold. Short silence, including a
couple of minutes, is normal and should not trigger replacement by itself.

Before labeling a worker stuck or spawning fresh, consider:

- the complexity and expected duration of the assigned slice
- whether the worker may be thinking, waiting on a command, sleeping, or holding
  an assigned verification resource
- the last observed event, command, stderr/log movement, file changes, or
  worklog update
- whether the worker is actually blocked, repeating bad fixes, causing bugs, or
  operating in the wrong owner boundary

If silence is the only signal, keep the worker in a `quiet/observing` state,
record why waiting is reasonable, and check again later. Replace or abandon the
worker only when evidence shows it is stuck, harmful, or unable to continue.

## Hard Rules

- Never cross-resume between runtimes.
- Never use latest-session selection.
- Cursor Agent resumes only through `--resume <session_id>`.
- Codex resumes only through `codex exec resume <thread_id>`.
- Claude resumes only through `-r <session_id>`.
