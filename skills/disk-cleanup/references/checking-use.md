# Checking whether anything uses a folder

You want one answer for every large candidate at once: is something running from it, pointing at it or still writing in it? Every command here only reads. Each one is either quick, or one pass you make a single time per run and save. Keep the outputs in a private folder for the run, and put the candidate paths in a file, one per line, rather than on a command line. If they're on a command line, your own shell turns up as "using" every one of them.

```sh
run=<the scheduler's run directory, or a new folder>   # e.g. mkdir -m 700 ~/disk-cleanup-$(date +%F)
printf '%s\n' /path/one /path/two > "$run/candidates.txt"
```

## 1. Sizes and newest file, in one pass

```sh
gdu -x -k --time --time-style=+%s -d 4 ~/workspace > "$run/sizes.txt" 2>/dev/null   # Mac: gdu is GNU du
du  -x -k --time --time-style=+%s -d 4 ~/workspace > "$run/sizes.txt" 2>/dev/null   # Linux
```

Each line holds the size in KB, the newest modification time anywhere inside (epoch seconds) and the path. Measure each tree once. Never run a parent and its children at the same time, because they read the same disk twice. Run it at normal priority: on a Mac, background priority keeps it on the slow cores. Repeat it for the other big roots (the rest of the home folder, a data drive) the same way.

A folder's time is its newest file, so one log line written yesterday makes a dead folder look fresh. To see what was written, run:

```sh
find "$dir" -xdev -type f -mtime -2 -not -path '*/.git/*' 2>/dev/null | head -5
```

On a Mac, many copies of one thing can be APFS clones that share their blocks, and `du` counts each one in full. Before ranking a family of near-identical copies, delete one and watch `df`.

## 2. One snapshot of every process's files

```sh
lsof -nP -F pcfn > "$run/lsof.txt" 2> "$run/lsof.err"; echo "exit $?: $(grep -c '^p' "$run/lsof.txt") processes"
```

This lists every process's working directory, executable and open files. It takes about a second on a Mac and about ten seconds on the home server. On the Mac Studio and the home server, prefix it with `sudo -n`, so the snapshot includes every user's processes. lsof often exits 1 because a process ended mid-scan, and that snapshot is still good. Compare its process count with the processes it should cover: `ps -A -o pid= | wc -l` when you ran it with `sudo -n`, or `ps -U "$(id -un)" -o pid= | wc -l` without. Without sudo it sees only your own user's processes. On the M5, the M3s and Mini 1, that is every agent. A snapshot missing most of what it should cover (permission denied, `sudo` refused) has failed, and nothing it doesn't cover can be called unused.

Never run `lsof +D <folder>`: it walks the whole folder on every call and takes minutes on a big one.

## 3. Match every candidate against it at once

```sh
python3 - "$run/lsof.txt" "$run/candidates.txt" <<'PY'
import os, re, subprocess, sys
snapshot, listfile = sys.argv[1], sys.argv[2]
wanted = {}
for line in open(listfile):
    p = line.strip()
    if p:
        wanted[os.path.realpath(p)] = p
        wanted.setdefault(os.path.abspath(p), p)
def candidates(path):                         # every candidate folder that contains this path
    while path not in ('', '/'):
        if path in wanted:
            yield wanted[path]
        path = os.path.dirname(path)
def ps(*fields):
    r = subprocess.run(['ps', '-A', '-ww'] + [a for f in fields for a in ('-o', f + '=')], capture_output=True, text=True, errors='replace')
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit('ps failed: no answer, so nothing can be called unused')
    return r.stdout.splitlines()
info = {}
for line in ps('pid', 'ppid', 'etime', 'pcpu', 'ucomm'):   # ucomm: the short name, never arguments
    f = line.split(None, 4)
    if len(f) == 5:
        info[f[0]] = f'ppid {f[1]}, up {f[2]}, cpu {f[3]}%, {f[4].strip()}'
uses, pid = {}, None
for line in open(snapshot, errors='replace'):
    tag, val = line[:1], line[1:].rstrip('\n')
    if tag == 'p': pid = val
    elif tag == 'f': fd = val
    elif tag == 'n' and val.startswith('/'):
        for c in candidates(val):
            uses.setdefault(c, {}).setdefault(pid, set()).add('cwd' if fd == 'cwd' else 'program' if fd == 'txt' else 'open file')
named = {real: re.compile(r'(?<![^\s"\'=:;,])' + re.escape(real) + r'(?=$|[/\s"\'=:;,])') for real in wanted}   # the whole path, not part of another
for line in ps('pid', 'args'):                # matched here, never printed
    p, _, args = line.strip().partition(' ')
    for real, c in wanted.items():
        if real in args and named[real].search(args):
            uses.setdefault(c, {}).setdefault(p, set()).add('named in its arguments')
parent = {p: v.split(',')[0].split()[1] for p, v in info.items()}
mine, p = set(), str(os.getpid())
while p in parent and p not in mine:          # this check and the shells that started it
    mine.add(p); p = parent[p]
for c in dict.fromkeys(wanted.values()):
    users = {p: how for p, how in uses.get(c, {}).items() if p not in mine}
    print(c, f'({len(users)} processes)' if users else '')
    for p, how in sorted(users.items())[:12]:
        print(f'   pid {p}: {", ".join(sorted(how))}; {info.get(p, "gone")}')
    if not users:
        print('   nothing')
PY
```

For each candidate it prints "nothing", or each process using it with how (working directory, program, open file, named in its arguments), its parent, how long it has run, its CPU and its name. It never prints a command line, because command lines can carry credentials. On the home server, 300 candidates against a 1.4-million-line snapshot take about two seconds.

Reading the result is the judgment:

- An agent session (`claude`, `codex`, a `node` running either) working in the folder, a server, a trainer, a build or a test runner means someone is using it.
- Some processes are leftovers that look like use: `tail` or `less` on a finished job's log, a `zsh` or `bash` whose parent is gone (a parent pid of 1) with no children and no CPU, or a language server or tool server whose editor or agent has left. Stop the exact process by pid and check the folder again.
- For "named in its arguments", look at the process by pid (`ps -o pid=,ppid=,etime=,ucomm= -p <pid>`). Use `ucomm` rather than `comm`: on a Mac, `comm` shows a process's title, and some tools put their arguments there., not at its arguments.
- A server can read a file only when a request needs it, so an idle server isn't proof its data is unused. When a live server sits next to a candidate, look in that server's config and launch scripts for the candidate's path.

## 4. What points at it without running

```sh
grep -rlF -f "$run/candidates.txt" ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons 2>/dev/null   # Mac services (file names only)
grep -rlF -f "$run/candidates.txt" ~/.config/systemd/user /etc/systemd/system 2>/dev/null                            # Linux services
crontab -l 2>/dev/null | grep -o -F -f "$run/candidates.txt" | sort -u                                              # schedules (prints only the path)
docker ps -aq | xargs docker inspect --format '{{.Name}} {{.State.Status}} {{range .Mounts}}{{.Source}} {{end}}' 2>/dev/null \
  | grep -F -f "$run/candidates.txt"                                                                                   # containers, stopped ones too
```

Links from the live projects' checkouts into a candidate. They sit near the top of a checkout (`policies`, `artifacts/cardabs`), so three levels is enough:

```sh
for live in <each live checkout>; do
  find "$live" -maxdepth 3 \( -name node_modules -o -name .git \) -prune -o -type l -exec realpath {} \; 2>/dev/null
done | grep -F -f "$run/candidates.txt"
```

On a Mac with Colima, `docker` talks to the current context only. `docker context ls` lists the others, and a stopped VM has no running containers to report.

## 5. The state of every checkout

Find every checkout under a root in one pass. It skips build trees and takes a second or two:

```sh
find ~/workspace -maxdepth 4 \( -name node_modules -o -name target -o -name build -o -name .dart_tool -o -name Pods -o -name .venv \) -prune \
  -o -name .git -print 2>/dev/null | sed 's#/\.git$##' > "$run/checkouts.txt"
```

Then read each one with commands that change nothing. `GIT_OPTIONAL_LOCKS=0` stops `git status` from rewriting the index:

```sh
while read -r wt; do
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$wt" \
    "$(git -C "$wt" remote get-url origin 2>/dev/null | sed -E 's#://[^@/]*@#://#')" \
    "$(git -C "$wt" symbolic-ref -q --short HEAD 2>/dev/null)" \
    "$(git -C "$wt" log -1 --format=%ct 2>/dev/null)" \
    "$(st=$(GIT_OPTIONAL_LOCKS=0 git -C "$wt" status --porcelain=v1 --untracked-files=normal 2>/dev/null) && { printf '%s' "$st" | grep -c . || true; } || echo '?')" \
    "$(git -C "$wt" rev-list --count HEAD --not --remotes 2>/dev/null)"
done < "$run/checkouts.txt" > "$run/git.tsv"
```

The columns are path, origin (with any credentials stripped), branch, last commit time, changed files and commits not on any remote. A `?` or an empty column means that check failed (a broken worktree link, a repository with no commits). Treat it as unknown, never as zero. Remote-tracking branches go stale: a branch deleted on GitHub still counts as "on the remote" until a fetch prunes it. Before you trust a zero in a repository you're about to clean, run `git -C <primary> fetch --prune --quiet origin` once for that repository. This is the one step here that changes anything: it downloads objects and updates remote-tracking refs and `FETCH_HEAD`. Leave it out of a preview.

Get PR state once per repository, then match each checkout's branch against it:

```sh
gh pr list --repo funcountry/psmobile --state all --limit 1000 --json headRefName,state,mergedAt > "$run/prs-psmobile.json"
```

A merged or closed PR means the task is finished. A detached checkout has no branch to match, so its commit time and the use checks decide.

## 6. Right before deleting

A snapshot from ten minutes ago can miss an agent that has just started. Run steps 2 and 3 again for the batch you're about to delete. Skip any path that turns up in use and carry on with the rest.
