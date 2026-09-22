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

The account pool contains only the consultation profiles configured on this
machine: the BrowserOS profiles labeled, for example, `pro1`, `pro2`, and
`pro3`.
Names and count vary; these examples are not a fixed inventory or rotation
order. The label is how you find the profile and which login it holds. It is
not the model: choosing the profile and choosing the model are two separate
steps with two separate proofs.
Discover the existing windows through BrowserOS; never activate a window
to infer its profile or create windows for this task. The user's `Work` profile
is excluded: do not use it for ChatGPT or test its Pro availability. Preserve
its rate-limit capacity for the user, even if every consultation profile is
unavailable.

Start with an explicitly requested consultation profile, or the one whose
account contains the needed conversation, if its picker offers Pro. A prior
thread in `Work` does not make that profile eligible. Restore the needed
context from already-available task artifacts into a conversation in a
consultation profile instead.
Otherwise prefer a recently observed working account and verify its current
state. Keep brief availability notes in the
existing run context: safe profile label, window, whether the picker offered
the `Pro` option, required connector status, observed condition, and check
time. Record the
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

For continuing work, look for a recent thread in that project that ran on Pro and read enough
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
The page snapshot lists both radios without marking the selected one; read
each radio's `aria-checked` value from the page.
The BrowserOS profile named `Work` does not select this surface.

The model is chosen and proven here, on the page, in every conversation you
send into. The consultation profile does not choose it: a page in `pro1`
sends to whatever model its composer holds. The composer returns to ChatGPT's
default on a new chat or a project page, so a thread that showed `6 Pro` does
not carry Pro into the new chat opened from it.

Observed composer shape: the model pill beside the composer shows the current
setting. It reads `6 Pro` with Pro selected and a power word such as `Medium`,
`High`, `Extra High`, or `Instant` otherwise. While its menu is open the same
button reads `Thinking effort`, so read the pill with the menu closed. The
menu has `Select model`, whose radios are `Latest`, `GPT-6 Sol`, and
`GPT-5.5`, and `Power`, a slider.

Pro is the top `Power` position of `Latest`. With Pro available the slider has
five positions: `Extra High` is `4 of 5` and Pro reads `Pro, 5 of 5`. Pro is
not an entry in the model list. Do not look for it there, and never report Pro
missing, disabled, or rate limited because the list shows only `Latest`,
`GPT-6 Sol`, and `GPT-5.5`.

When a composer cannot select Pro, the slider ends at `Extra High, 4 of 4` and
a disabled `Pro` entry appears below the model list. Hover the disabled entry
and read its tooltip: `Limit reached. Try again after 9:48 AM tomorrow.` is the
account's rate limit with its reset time, which goes in the availability notes
and the report to the user. This is a reading of this composer. Another chat
in the same profile can still read `6 Pro`, so check an existing Pro thread in
the project before leaving the profile. Do not send from the disabled composer
on whatever it does offer; the entry file's no-send rule applies.
Other layouts appear, such as
`Configure...` / `Intelligence` or a separate `Extended` thinking control; use
whatever is offered to the same end. The default is GPT-6 Astra, `Pro`, and
`Extended` thinking where separately offered.

Select the model and option, close the picker, and read the pill back from the
page. Write the read-back text and the time in the task notes before Send.
After Send, read the model slug on the response turn that answers your message,
`data-message-model-slug` on its assistant message, which is `gpt-6-pro` for
Pro; the scoped DOM read in
[generation-progress-and-recovery.md](generation-progress-and-recovery.md)
returns it. Note that too. Take both readings again after a new chat, reload,
project change, or account switch.

None of these is a reading of this conversation's model: the profile label;
the account button, whose text such as `Pro 1 Pro, open profile menu` is the
account's display name and plan badge; a `Used GPT-6 Pro` footer, model tag,
`Pro feedback`, or `Switch model` button on an earlier turn; a `Pro thinking`
label; a numeric power level alone; the project or thread title; the user's
request; the plan; the word Pro in your own prompt; or the setting an earlier
conversation had. A search of the page for "Pro" matches these and is not a
reading.
Respect an explicitly different user choice without silent upgrading or
substitution.

A Work-surface thread, often labeled `Work` in the sidebar, cannot serve as the
required Chat-surface Pro consultation. Open the appropriate Chat conversation
in the project and restore its needed context before submission.

## Switch accounts

A `Power` slider that cannot reach Pro (it ends at `Extra High, 4 of 4`, with
a disabled `Pro` entry under the model list) suggests a temporary account
limit; the entry's hover tooltip or an explicit usage-cap message confirms it.
Pro absent from the model list is normal and is not this signal. Switching
accounts is the only response to a composer without Pro; running the
consultation on another model is never one. Before telling the user that no
account offers Pro, read the pill or slider in each consultation profile and
report what each one read, with any reset time shown.
Failed connector access requires a suitable account too, but does not itself
prove a Pro rate limit.

1. Record the current account's observed condition and time. Prefer another
   recently verified working account; otherwise check the next consultation
   profile not yet examined. Never include `Work` in this search.
   Do not repeatedly retry the capped account.
2. Under BrowserOS, select or open one eligible page in that account's existing
   window and prove the profile/window/page. Verify login, then select the
   requested literal configuration in that page's picker and read it back; the
   previous account's setting does not carry over, and arriving in another
   profile labeled `Pro` proves nothing about its model. If unavailable,
   record it and continue the search.
3. Once an account works, use it; there is no need to test every remaining
   account. Verify the same-named project and restore necessary context in the
   destination thread. Reattach files and required connector mentions, including
   the exact PR URL for a code review. Verify every required connector works.
4. Continue in that page alone. Clean up task-created pages no longer needed
   under BrowserOS and record the successful account and destination thread.
5. If no consultation profile's account works, report the profiles and observed conditions.
   Keep the required consultation pending, continue independent work, and wait
   for user notice that Pro is available again. Do not select a substitute tier
   or fall back to `Work`.
