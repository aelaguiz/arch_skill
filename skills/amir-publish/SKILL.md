---
name: amir-publish
description: "Publish this skills repo across Amir's machine cluster by committing and pushing the current local work, installing locally, then SSHing to the known hosts, skipping the current machine, pulling the same branch in the same directory, and running the local install. Use when Amir asks to distribute, sync, or publish skill changes to his machines. Not for generic deployments, CI release work, or remote edits outside this repo."
metadata:
  short-description: "Publish skill changes across Amir's machines"
---

# Amir Publish

Use this skill when Amir wants current skill repo changes distributed across his usual machines.

This is prompt-only shell orchestration. Do not add scripts, harnesses, controller state, or new automation infrastructure.

## When to use

- Amir asks to publish, sync, distribute, or roll out this skills repo to his machines.
- The desired workflow is local commit, push, local install, then remote pull and install.
- The target machines are the fixed cluster listed below.

## When not to use

- The task is a generic deploy, package release, or CI workflow.
- The task is only to install the current machine without pushing or syncing remotes.
- The repo is not the skills repo or does not have the expected local install command.
- The user wants `make remote_install`; this workflow keeps each remote repo on the same branch instead of copying files over SSH.

## Machine List

Publish to these SSH targets, skipping whichever one is the current machine:

- `amirs-m3-max-new`
- `agents@amirs-mac-studio`
- `amir-m5`
- `home`
- `claw`

Treat `agents@amirs-mac-studio` as the host `amirs-mac-studio` when deciding whether to skip the current machine.

## Workflow

1. Resolve the git repo root, current branch, current commit, and same absolute directory path to use on remotes.
2. Identify the current machine with `hostname -s` or the closest available hostname command.
3. Inspect `git status --short`. Default to committing the full tracked-file diff across the repo, including tracked changes you do not recognize. Unfamiliar tracked changes are not a blocker by themselves.
4. Stage tracked modifications and deletions with `git add -u`. Also stage untracked files that are clearly part of the current repo work; ask only for ambiguous untracked files or concrete safety issues such as secrets.
5. If there are changes to commit, create one concise commit. If there is nothing to commit, say so and continue.
6. Push the current branch to its upstream. If no upstream exists, push with `git push -u origin <branch>`.
7. Run the local install command from the repo root:

```bash
make install
```

8. For each non-skipped SSH target, run the remote sync from the same absolute directory:

```bash
cd <same-dir> &&
git fetch origin &&
(git checkout <branch> || git checkout -t origin/<branch>) &&
git pull --ff-only &&
make install
```

9. If one remote fails, continue to the remaining hosts unless the failure means the pushed branch or local install is invalid. Keep the failed host and command visible in the final summary.

## Output

Keep the final response short:

- local branch and commit pushed
- local install result
- each remote host result
- any skipped host
- any failed host and the exact next repair step
