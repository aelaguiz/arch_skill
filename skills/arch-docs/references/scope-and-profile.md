# Scope And Repo Doc Profile

Use this file first so the cleanup adapts to the repo's actual doc system and resolves scope from evidence instead of from habit.

## Scope resolution order

- Resolve working context in this order:
  - explicit user context such as paths, modules, topics, or stop conditions
  - active arch artifacts when they clearly exist, such as the current plan doc, worklog, related docs, or a clean implementation audit
  - otherwise the repo docs surface itself
- Standalone `arch-docs` must work even when there is no plan doc at all.
- If arch artifacts exist, treat them as narrowing context, not as the whole scope by default.
- In any mode, inventory broadly enough to find all docs that touch the chosen topics.

## Scope defaults

- If the user gave explicit context:
  - start there
  - widen only enough to capture all overlapping docs for the same topics
- If active arch context exists:
  - use the plan/worklog and related repo evidence to identify the feature topics
  - then inspect every doc-shaped surface that touches those topics
- If neither exists:
  - profile the repo docs surface
  - inventory doc-shaped surfaces across the repo
  - group them by topic
  - choose the strongest grounded cleanup slice for the current pass
- In repo-scope `auto`, later passes may widen across the repo docs surface when the first slice exposed more grounded stale, overlapping, or misleading docs elsewhere.
- Do not silently turn a pass into an aesthetic or taxonomy rewrite.

## Repo doc profile

Before changing docs, answer these with repo evidence:

- Where do docs live?
- What folder or naming scheme already exists?
- What formats are used?
- Is there a docs build or nav system?
- Who are the likely readers for the scoped docs?

Write the answers at the top of `.doc-audit-ledger.md`.

## Topic-first grouping

- Group inventory items by topic, not by folder.
- A topic is a thing a reader needs to know, for example:
  - setup for this feature
  - how the subsystem works now
  - how to operate or debug it
  - what changed in a migration
- One topic may span several files. Several files may partially overlap on the same topic.

## Canonical-home rule

- Each in-scope topic ends with one canonical evergreen home.
- Prefer the repo's existing gravity:
  - root `README.md`
  - docs index or usage guide
  - focused doc under `docs/`
  - module README when that is the established local pattern
- Do not create a new doc home just because a cleanup pass wants a tidier taxonomy.

## Stop and route back

Do not proceed with docs cleanup when:

- current code truth is still changing materially in the same run
- the cleanup needs external doc sources that are inaccessible from the repo and current context
- active arch context exists but its implementation truth is still too unstable to trust
- the only way to keep going would be a speculative repo-wide reorganization that is no longer grounded in the current topics
