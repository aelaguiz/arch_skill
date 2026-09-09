# ChatGPT Accounts and Conversations

Read before selecting an account, project, thread, or model, and when switching
accounts. Apply the BrowserOS profile-targeting reference before browser calls.

## Contents

- Choose a working account
- Verify login without exposing session data
- Choose the project and conversation
- Select the literal model and mode
- Switch accounts

## Choose a working account

The pool is one `Work` profile and however many Pro profiles are configured on
this machine. `Pro One`, `Pro1`, `Pro2`, and `Pro3` are examples, not a fixed
inventory or required order. Discover the existing windows through BrowserOS;
never activate a window to infer its profile or create windows for this task.

Start with an explicitly requested profile or the account containing the needed
conversation if it offers Pro. Otherwise prefer a recently observed working
account and verify its current state. Keep brief availability notes in the
existing run context: safe profile label, window, Pro available or unavailable,
required connector status, observed condition, and check time. Record the
working account as well as failures. Recheck stale observations on resume;
these limits are temporary.

All accounts should have the same projects. Verify the actual project after
switching; project-name similarity is not proof of account identity. Threads
are per account. Carry the required goal, decisions, evidence, and prior context
into a destination conversation rather than assuming that account has the thread.

## Verify login without exposing session data

On the verified `https://chatgpt.com/` page, use BrowserOS page-context JavaScript
for the following boolean-only check:

```javascript
async () => {
  const response = await fetch('/api/auth/session', {credentials: 'include'});
  if (!response.ok) throw new Error('ChatGPT login check failed');
  const session = await response.json();
  return Boolean(session.user);
}
```

Use the live `evaluate` schema's accepted function or expression shape. Only
return the boolean; never return, print, persist, or inspect the user object,
account details, token fields, cookies, or raw payload. If the check fails or
returns false, identify the verified profile/window and ask the user to log in
manually there. Do not automate login or infer it solely from visible controls.

## Choose the project and conversation

Read the project list and select the one matching the repository, product, or
workstream. Project context matters; a root chat lacks the project's supplied
files and instructions. Use a root conversation only when no project plausibly
fits and disclose that choice.

For continuing work, look for a recent Pro thread in that project and read enough
to confirm the workstream rather than trusting a similar title. The normal
starting point is a thread from the last 24–48 hours. Around six or more
prompt/response turns, consider whether a new conversation with the needed
context would be clearer; use the thread's actual content to judge saturation.

Continue a suitable `Chat` thread for follow-ups. Start a new conversation in
the project when no thread fits, the work is independent, or the prior thread
is overloaded. An explicit requested project, exact thread, or fresh chat wins.
If an exact requested thread cannot be identified, ask for the missing choice.
Do not send into whichever history happens to be open.

## Select the literal model and mode

The composer's `Select chat surface` radio chooses between ChatGPT `Chat` and
`Work`. Verify `Chat` before opening the model pill and again before sending.
The BrowserOS profile named `Work` does not select this surface.

Use the model pill and, when offered, `Configure...` / `Intelligence` to inspect
nested model and reasoning controls. Verify the selected model name and actual
literal mode. The default is GPT-6 Astra, `Pro`, and separate `Extended` thinking
where offered. A numeric power level or a profile called Pro is not mode proof.
Respect an explicitly different user choice without silent upgrading or
substitution.

A Work-surface thread, often labeled `Work` in the sidebar, cannot serve as the
required Chat-surface Pro consultation. Open the appropriate Chat conversation
in the project and restore its needed context before submission.

## Switch accounts

A missing/disabled literal Pro option after checking the live nested picker
suggests a temporary account limit; an explicit usage-cap message confirms it.
Failed connector access requires a suitable account too, but does not itself
prove a Pro rate limit.

1. Record the current account's observed condition and time. Prefer another
   recently verified working account; otherwise check the next configured
   account not yet examined. Do not repeatedly retry the capped account.
2. Under BrowserOS, select or open one eligible page in that account's existing
   window and prove the profile/window/page. Verify login and the requested
   literal configuration. If unavailable, record it and continue the search.
3. Once an account works, use it; there is no need to test every remaining
   account. Verify the same-named project and restore necessary context in the
   destination thread. Reattach files and required connector mentions, including
   the exact PR URL for a code review. Verify every required connector works.
4. Continue in that page alone. Clean up task-created pages no longer needed
   under BrowserOS and record the successful account and destination thread.
5. If no available account works, report the profiles and observed conditions.
   Keep the required consultation pending, continue independent work, and wait
   for user notice that Pro is available again. Do not select a substitute tier.
