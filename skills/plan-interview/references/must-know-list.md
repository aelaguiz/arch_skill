# The Must-Always-Know List

Every Intent Pack has a written line for each item below, even when the line
is "none" or "standard." Complexity scales how much discovery an item gets —
never whether it exists. A pack with a missing line is not ready to sign off.

Tags say how each item gets answered:

- **[elicited]** — an open question to the user; their thinking leads.
- **[default]** — a standing answer from `standing-doctrine.md`, confirmed
  in one line; only deviations get discussion.
- **[derived]** — the agent works it out from evidence and the user
  approves or edits it on the spot.

Tags may be compounded or annotated where an item mixes modes (for
example `[elicited; agent structures]`, or item 9's bar-then-grid
procedure, which is a derivation the user approves in-flow).

## Intent

1. **What are we doing** — the outcome in the user's own words, one
   paragraph. [elicited]
   - Strong: quotes the user's framing; a stranger could repeat the goal.
   - Weak: a restated feature title, or the agent's interpretation standing
     in for the user's words.
2. **Why / why now** — the problem it solves, first principles. [elicited]
   - Strong: names the pain and what changes when it's gone.
   - Weak: "improve X" with no observable pain behind it.
3. **Success signals** — how anyone would observe it worked. [elicited]
   - Strong: observable, checkable, ideally measurable.
   - Weak: adjectives ("faster", "cleaner") with no way to check.

## Shape

4. **Project type** — feature / centralization+deletion / repair /
   investigation. Decides which standing rules bite hardest: in a
   non-feature project any new user-facing noun is auto-rejected. [derived]
5. **UX delta** — exactly what users see change; everything else unchanged.
   Includes: new-UX-or-not declared; a stay-dead list (intentionally
   removed things no parity pass may resurrect); an agreed vocabulary (no
   code-internal label may surface as a product concept); **a user journey
   map wherever the work touches a journey** — in a mature product usually
   the existing journey confirmed unchanged or the tweak marked on it,
   while bigger features map every journey they create, sometimes several;
   and **visual references** — do mocks, target images, or reference apps
   exist, and where? New UX with no visuals gets an offered mock-approval
   gate before implementation. [elicited]
6. **Requirements** — a plain numbered list, hard/soft marked, each stated
   in words and referred to by name afterward, never by invented code.
   Acceptance criteria in testable form (given/when/then shape) where
   testability matters. [elicited; agent structures]
7. **Non-goals and scope boundary** — what is explicitly out; the line
   reviewer findings get triaged against; the deferral ledger (anything
   planned-then-parked must surface at completion, never be discovered
   later). [elicited; agent proposes candidates from discovery]

## Build

8. **Architecture requirements** — the user's constraints, not a design:
   one owner, no duplicate patterns, what gets deleted,
   cutover-versus-compatibility posture. Asked with framing: "typically
   your requirements here are X and Y — what are you thinking?" [elicited]
9. **Test grid and proof** — the full grid with edge cases; the right
   altitude per requirement (simulator/device automation vs widget vs
   unit — widget-only has historically been insufficient for journey-level
   claims); where proof must be seen (simulator, device, production);
   required artifacts (before/after journey screenshots, live data — never
   placeholder content). **Built and approved inside the interview, before
   sign-off. It is part of the approval, never a follow-up.** [user sets the
   bar; agent builds the grid on the spot; user approves or edits it there]

## Finish

10. **Definition of done** — the observable finish line: what is visibly
    working, where, with what artifact — and who signs off (an adversarial
    reviewer disinclined to accept a surrender). Done includes
    verified-live when a deploy is involved. [elicited]

## Run

11. **Execution policy** — models per role, worktree pin, simulator pin,
    review waves and caps, PR contract, usage-limit rotation. All standing
    defaults; one consolidated confirm. [default]
12. **Autonomy contract** — will the user be present; which decision
    classes the agent must settle itself from first principles; the
    question protocol (batched, on-screen, plain English, each with a
    stated default so silence equals the default); what counts as a real
    blocker (proven external, not a decision the agent could make), stated
    as one plain sentence while unblocked work continues. [default + one
    question]

## Residue

13. **Open decisions and assumptions** — every remaining unknown, each
    with an owner (user or agent) and a default. Nothing unwritten;
    nothing silently decided. [derived; listed in full at sign-off]

## Using the list

The list is the interview's map, not its script. Walk it breadth-first;
items 1–3 and 5–8 and 10 are the conversation, items 4, 9, and 13 are
derivations brought back for approval, items 11–12 are confirms. When the
user's answer to one item resolves another, write both lines and say so —
never re-ask what an earlier answer already settled.
