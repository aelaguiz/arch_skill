# Structure And Scope

Use this file when deciding where `AGENTS.md` guidance should live, how precedence works, and when an override is safer than inheritance.

## Table of contents

- Codex discovery and merge behavior
- Placement strategy
- Monorepo splitting rules
- `AGENTS.override.md` doctrine
- Practical scoping heuristics
- Source notes

## Codex discovery and merge behavior

Codex-style agent runtimes treat `AGENTS.md` as a hierarchical instruction chain.

High-signal behavior to preserve in authored files:

- discovery starts from the repo root and walks toward the current working directory
- at most one `AGENTS.md`-family file is used per directory
- files closer to the current working directory are later in the merged chain and therefore more specific
- `AGENTS.override.md` replaces the normal file for that directory rather than extending it
- all discovered content shares a finite instruction budget

Implications for authors:

- closer files should mostly contain local deviations, not re-state the whole root contract
- if a deeper file contradicts the root, do it intentionally and narrowly
- every additional file consumes budget, so only add a layer when it carries genuinely local truth

## Placement strategy

Use root `AGENTS.md` for repo-wide doctrine:

- install and verification commands
- repo-wide definition of done
- global approval boundaries
- repo-wide plain-English communication rules
- shared doc maps or compressed docs indexes
- cross-cutting required skills or workflows

Use path-local `AGENTS.md` when a subtree has:

- different commands
- different dangerous operations
- different ownership boundaries
- different truth surfaces
- local jargon or shorthand that needs stricter translation rules than root
- a specialized toolchain that would confuse the rest of the repo

Use `AGENTS.override.md` when a directory needs a clean replacement because inheriting the normal local rules would be unsafe or misleading.

Good examples:

- payments or compliance-heavy services
- incident or freeze mode
- generated-code or vendor directories with unusual editing rules
- directories whose commands differ so much that "append local notes" becomes more confusing than replacement

## Monorepo splitting rules

A useful default for large repos is:

- one root file
- one local file per major app, service, or package family
- rare overrides only for genuinely exceptional surfaces

Do not split just because the repo is large. Split when the local truth differs materially.

Signals that a subtree deserves its own file:

- the local verify command differs from the root verify command
- the subtree has its own release process, approval rule, or data risk
- the subtree has a specialized docs set that the rest of the repo does not need
- the local owner would reasonably maintain its own agent rules

Signals that a split is unnecessary:

- the file would only repeat the root rules with different wording
- the subtree has minor style differences but no meaningful workflow differences
- root already owns the communication invariant and the subtree has no special local jargon to ban or translate
- the extra file would exist only to document architecture instead of actionable instructions

## `AGENTS.override.md` doctrine

Treat overrides as a sharp tool.

Use them when:

- the local file must replace, not extend, the normal doctrine
- inheriting nearby instructions would produce the wrong commands or unsafe behavior
- the mode is temporary but materially different, such as freeze mode or incident response

Do not use them when:

- a short path-local file could add one or two local rules safely
- the change is cosmetic rather than semantic
- the directory merely wants to emphasize itself

When authoring an override:

- restate the local verification path completely
- restate the local definition of done completely
- restate the local red lines completely
- assume the reader may not see the replaced local file at all

## Practical scoping heuristics

Ask these questions before adding another file:

1. What would a fresh agent do wrong here if only the root file existed?
2. Is the wrong behavior local to this subtree, or global?
3. Would a short add-on file be enough, or do we need a true replacement?
4. Does the local file introduce new commands, new risks, or new truth surfaces?
5. Can the deeper file stay under control without copying root doctrine?

Good local file shape:

- one short local startup section
- local commands
- local red lines
- local docs pointers

Bad local file shape:

- root doctrine copied again
- long product narratives
- general team values with no operational consequence

## Source notes

Derived from:

- OpenAI Codex project-instruction discovery rules
- the `openai/agents.md` examples and override semantics
- GitHub Copilot repo-instructions guidance
- repo patterns from OpenAI Codex, Apache Airflow, and other hierarchical AGENTS deployments summarized in the research pack
