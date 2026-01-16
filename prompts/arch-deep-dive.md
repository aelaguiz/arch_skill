---
description: "04) Deep dive: current-target architecture + call-site audit."
argument-hint: DOC_PATH=<path> (optional)
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Populate sections 4–6 in $DOC_PATH:
- Current architecture (on-disk tree, control paths, object model, failure behavior).
- Target architecture (future tree, flows, APIs, invariants).
- Call-site audit table (exhaustive inventory).
Reference ground truth code paths for every claim.
Write the updated sections into $DOC_PATH (replace sections 4–6 in-place). Do not paste the full block to the console.

DOCUMENT INSERT FORMAT (replace sections 4–6 in-place):
# 4) Current Architecture (as-is)

## 4.1 On-disk structure
```text
<tree of relevant dirs/files>
```

## 4.2 Control paths (runtime)

* Flow A:

  * Step 1 → Step 2 → Step 3
* Flow B:

  * ...

## 4.3 Object model + key abstractions

* Key types:
* Ownership boundaries:
* Public APIs:

  * `Foo.doThing(args) -> Result`

## 4.4 Observability + failure behavior today

* Logs:
* Metrics:
* Failure surfaces:
* Common failure modes:

## 4.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for current UI states, if relevant>
```

---

# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

```text
<new/changed tree>
```

## 5.2 Control paths (future)

* Flow A (new):
* Flow B (new):

## 5.3 Object model + abstractions (future)

* New types/modules:
* Explicit contracts:
* Public APIs (new/changed):

  * `Foo.doThingV2(args) -> Result`
  * Migration notes:

## 5.4 Invariants and boundaries

* Fail-loud boundaries:
* Single source of truth:
* Determinism contracts (time/randomness):
* Performance / allocation boundaries:

CONSOLE OUTPUT FORMAT (summary + open questions only):
Summary:
- <bullet>
Open questions:
- <open question>

## 5.5 UI surfaces (ASCII mockups, if UI work)

```ascii
<ASCII mockups for target UI states, if relevant>
```

---

# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

| Area     | File   | Symbol / Call site | Current behavior | Required change | Why         | New API / contract | Tests impacted |
| -------- | ------ | ------------------ | ---------------- | --------------- | ----------- | ------------------ | -------------- |
| <module> | <path> | <fn/cls>           | <today>          | <diff>          | <rationale> | <new usage>        | <tests>        |

## 6.2 Migration notes

* Deprecated APIs:
* Compatibility shims (if any):
* Delete list (what must be removed):

---
