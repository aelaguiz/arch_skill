---
name: amir-publish
description: "Publish this skills repo to every machine in Amir's cluster by committing the work on main and pushing it; devcluster then pulls, installs and checks it on every machine within minutes, and `devcluster status --all` confirms it. Use when Amir asks to distribute, sync, or publish skill changes to his machines. Not for generic deployments, CI release work, or remote edits outside this repo."
metadata:
  short-description: "Publish skill changes across Amir's machines"
---

# Amir Publish

Use this skill when Amir wants current skill repo changes on all of his machines.

Every machine runs devcluster, which keeps this repo's `main` in sync on its own: every two minutes it pulls `main`, merges and pushes commits made on that machine, and runs `make install` and then `make verify_install` whenever the commit changes. A failed install puts the installed skills back as they were. So publishing means getting the work onto `main` on GitHub. Nothing logs in to the other machines.

## When to use

- Amir asks to publish, sync, distribute, or roll out this skills repo to his machines.
- A skill change should reach every machine, and you want to confirm it did.

## When not to use

- The task is a generic deploy, package release, or CI workflow.
- The task is only to install the current machine: run `make install`.
- The repo is not the skills repo or does not have the expected local install command.

## Workflow

1. Work on `main`. devcluster distributes only `main`; work on another branch reaches the machines once it's merged into `main`.
2. Inspect `git status --short`. Default to committing the full tracked-file diff across the repo, including tracked changes you do not recognize. Unfamiliar tracked changes are not a blocker by themselves.
3. Stage tracked modifications and deletions with `git add -u`. Also stage untracked files that are clearly part of the current repo work; ask only for ambiguous untracked files or concrete safety issues such as secrets.
4. If there are changes to commit, create one concise commit. If there is nothing to commit, say so and continue.
5. Push `main`. If origin moved first, pull with a merge, never a rebase, and push again.
6. If this session needs the change right away, run `make install` here. Otherwise devcluster installs it here too within a few minutes.
7. Confirm it arrived: `devcluster status --all` lists `repo arch_skill` for every machine with its commit. Within about ten minutes each should be at the commit you pushed. A machine under "Needs you" or "Failed" says in its line what stopped it.

## Output

Keep the final response short:

- the commit pushed
- the local install result, if you ran one
- which machines are at that commit, and the status line of any that aren't
