# Canonical Home And New-Doc Judgment

Use this file after profiling the repo so new docs are created only when they are the right canonical outcome, not when they merely feel tidy.

## 1) Resolve repo posture first

- Decide whether the repo is `public OSS` or `private/internal` from repo evidence.
- Strong `public OSS` evidence can include conventional community docs already present, explicit open-source language, or other shipped reader-facing surfaces that clearly invite outside users or contributors.
- Treat those as examples, not a keyword gate. Read the repo as a whole.
- If the evidence is mixed or thin, default to `private/internal`.
- Do not stop only because repo posture is unclear. Use the default and keep going.

## 2) Standard public-repo split points

In `public OSS` repos, these are expected standalone canonical homes:

- `README`
- `LICENSE*`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `SUPPORT.md`

Rules:

- These are standard open-source split points, not optional README subsections.
- If equivalent truth already exists under weaker or nonstandard names, fold it into the conventional home and repair references.
- Do not invent extra baseline docs just because many public repos happen to have them.

## 3) Expand versus create a new doc

Expand the current canonical home when:

- the topic naturally belongs there
- the added truth stays clear and discoverable
- keeping it there preserves one strong reader path instead of splitting attention

Create a focused new canonical doc only when all of these are true:

- the topic is durable and current, not a one-off moment
- readers are likely to seek it out directly as its own topic
- the topic is meaningfully differentiated from the purpose of the current home
- forcing it into the current home would blur that home, overload it, or make the docs worse
- the new home can be made discoverable in the repo's actual nav gravity
- the doc is not merely residue from an implementation pass whose durable truth fits a stronger existing evergreen home

Treat those as recognition tests, not a scorecard.

## 4) What does not justify a new doc

- a cleaner-looking taxonomy by itself
- a topic that is only interesting to the agent
- a one-off plan, rollout note, or worklog that has not been turned into evergreen truth
- a stale implementation-pass doc that contains a few useful paragraphs but whose durable truth can fold into an existing evergreen home
- speculative future reader needs
- a desire to preserve every artifact instead of converging on one canonical home

## 5) Examples are illustrative only

- `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` are ordinary standalone docs in `public OSS` repos because readers specifically look for them.
- A troubleshooting or architecture doc may deserve its own page when users would seek it directly and stuffing it into the README would make both docs worse.
- A narrow implementation note that fits cleanly into an existing module README usually should stay there.
- An old implementation worklog does not earn a top-level evergreen doc just because it once mattered. Fold the durable truth forward unless readers would seek that topic directly now.

The principle is stable: create a new doc when it is the right canonical home for current readers, not when it is merely one possible home.
