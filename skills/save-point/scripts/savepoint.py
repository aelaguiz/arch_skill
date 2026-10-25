#!/usr/bin/env python3
"""Save, stop and resume every agent session in Herdr on this machine.

  savepoint.py save [--note TEXT]              record every pane, its agent's live resume id, unsent drafts,
                                               live work, ssh panes and detached jobs; nothing is stopped
  savepoint.py stop [SAVE] [--panes S:P,..] [--include-ssh]
                                               exit the saved agents in parallel; any pane with text in its
                                               input box is skipped and left alone
  savepoint.py resume [SAVE] [--panes S:P,..] [--batch N]
                                               bring the saved agents back a few at a time, live work first,
                                               and put unsent drafts back unsent
  savepoint.py tmp-save [SAVE] | tmp-restore [SAVE]
                                               clone /private/tmp into the save point (APFS clones) and back;
                                               only for a machine restart

SAVE defaults to the newest save point under ~/.agent-save-points. Each command prints a short summary and the
path of the JSON it wrote; read the JSON for detail."""
import argparse, concurrent.futures as cf, datetime, json, os, re, subprocess, sys, time

ROOT = os.path.expanduser('~/.agent-save-points')
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')
UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
SHELLS = {'zsh', '-zsh', 'bash', '-bash', 'login', 'sh', 'fish'}


def run(*a, timeout=30):
    try:
        return subprocess.run(a, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return ''


def hj(session, *a):
    try:
        return json.loads(run('herdr', '--session', session, *a)).get('result', {})
    except Exception:
        return {}


def pane_read(session, pane, lines=40, ansi=False, src='visible'):
    a = ['herdr', '--session', session, 'pane', 'read', pane, '--source', src, '--lines', str(lines)]
    if ansi:
        a += ['--format', 'ansi']
    return run(*a)


def keys(session, pane, *ks):
    for k in ks:
        run('herdr', '--session', session, 'pane', 'send-keys', pane, k)
        time.sleep(0.4)


def fg(session, pane):
    info = hj(session, 'pane', 'process-info', '--pane', pane).get('process_info', {})
    return info.get('foreground_processes', [])


def at_shell(session, pane):
    names = [p.get('name', '') for p in fg(session, pane)]
    return bool(names) and all(n in SHELLS for n in names)


def ps_table():
    rows = {}
    for line in run('ps', '-axo', 'pid=,ppid=,command=').splitlines():
        p = line.split(None, 2)
        if len(p) == 3 and p[0].isdigit():
            rows[int(p[0])] = (int(p[1]), p[2])
    return rows


def descendants(ps, root):
    kids, out, todo = {}, [], [root]
    for pid, (ppid, _) in ps.items():
        kids.setdefault(ppid, []).append(pid)
    while todo:
        for k in kids.get(todo.pop(), []):
            out.append(k)
            todo.append(k)
    return out


def input_box(raw):
    """Text typed into the agent's input box (not a dimmed suggestion or placeholder), or ''."""
    lines = raw.splitlines()
    plain = [ANSI.sub('', l) for l in lines]
    rules = [i for i, l in enumerate(plain) if l.strip().startswith('─') or l.strip().startswith('╭') or l.strip().startswith('╰')]
    box = []
    if len(rules) >= 2:  # Claude Code and Kimi draw the box between two rules
        box = range(rules[-2] + 1, rules[-1])
    else:  # Codex: the prompt line starts with ›
        box = [i for i, l in enumerate(plain) if l.strip().startswith('›')][-1:]
    typed = []
    for i in box:
        if '\x1b[2m' in lines[i] or '\x1b[90m' in lines[i]:
            continue
        t = plain[i].strip().strip('│').strip()
        t = re.sub(r'^[❯›>]\s?', '', t).strip()
        if t:
            typed.append(t)
    return ' '.join(typed)


def live_work(text):
    tail = '\n'.join([l for l in text.splitlines() if l.strip()][-8:])
    work = {}
    if re.search(r'esc to interrupt|… \(\d|· thinking|Working \(|\(\d+s · ', tail):
        work['working'] = True
    m = re.search(r'(\d+) shells?', tail)
    if m:
        work['shells'] = int(m.group(1))
    m = re.search(r'(\d+) monitors?', tail)
    if m:
        work['monitors'] = int(m.group(1))
    return work


def claude_record(cmd, pid):
    m = re.search(r'(/[^ ]*?/\.claude)/', cmd)
    home = m.group(1) if m else os.path.expanduser('~/.claude')
    acct = re.search(r'claude-homes/([^/]+)/', cmd)
    rec = {'kind': 'claude', 'pid': pid, 'account': acct.group(1) if acct else None}
    try:
        s = json.load(open(os.path.join(home, 'sessions', f'{pid}.json')))
        rec.update(session_id=s.get('sessionId'), name=s.get('name'), session_cwd=s.get('cwd'))
    except Exception:
        pass
    return rec


def save(args):
    ps = ps_table()
    stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    out_dir = os.path.join(ROOT, stamp)
    os.makedirs(out_dir, exist_ok=True)
    try:
        sessions = json.loads(run('herdr', 'session', 'list', '--json')).get('sessions', [])
    except Exception:
        sessions = []
    me = (os.environ.get('HERDR_SESSION'), os.environ.get('HERDR_PANE_ID'))
    panes, codex_pids = [], {}
    for s in sessions:
        if not s.get('running'):
            continue
        name = s['name']
        for w in hj(name, 'workspace', 'list').get('workspaces', []):
            wid = w.get('workspace_id')
            for p in hj(name, 'pane', 'list', '--workspace', wid).get('panes', []):
                pid_ = p.get('pane_id')
                rec = {'session': name, 'workspace': wid, 'workspace_label': w.get('label'), 'pane': pid_,
                       'cwd': p.get('cwd'), 'self': (name, pid_) == me}
                procs = fg(name, pid_)
                aimgr = any('aimgr.js' in ps.get(q.get('pid'), (0, ''))[1] for q in procs)
                agent = None
                for q in procs:
                    cmd = ps.get(q.get('pid'), (0, ''))[1]
                    if '/.local/share/claude/versions/' in cmd and 'supervisor' not in cmd:
                        agent = claude_record(cmd, q['pid'])
                        kids = [ps[k][1] for k in descendants(ps, q['pid']) if k in ps]
                        reviewers = sorted({m for c in kids for m in re.findall(r'codex exec resume (' + UUID + ')', c)})
                        helpers = sum(1 for c in kids if '/.local/share/claude/versions/' in c and 'supervisor' not in c)
                        agent['children'] = {'reviewer_threads': reviewers, 'child_agents': helpers}
                        break
                if not agent:
                    for q in procs:
                        cmd = ps.get(q.get('pid'), (0, ''))[1]
                        if re.search(r'(^|/)codex( |$)', cmd) and ' exec ' not in cmd and 'mcp' not in cmd:
                            agent = {'kind': 'codex', 'pid': q['pid']}
                            codex_pids[q['pid']] = agent
                            for k in descendants(ps, q['pid']):
                                codex_pids[k] = agent
                            break
                        if re.search(r'(^|/)kimi( |$)', cmd) or q.get('name') == 'kimi':
                            agent = {'kind': 'kimi', 'pid': q['pid']}
                            break
                        if q.get('name') == 'ssh' or cmd.startswith('ssh ') or cmd.startswith('/usr/bin/ssh '):
                            agent = {'kind': 'ssh', 'pid': q['pid'], 'command': cmd[:200]}
                            break
                if agent is None and procs and not all(q.get('name', '') in SHELLS for q in procs):
                    agent = {'kind': 'other', 'command': '; '.join(ps.get(q.get('pid'), (0, q.get('name', '')))[1][:120]
                                                                   for q in procs if q.get('name', '') not in SHELLS)[:300]}
                if agent:
                    agent['aimgr'] = aimgr
                    raw = pane_read(name, pid_, 14, ansi=True)
                    agent['draft'] = input_box(raw) if agent['kind'] in ('claude', 'codex', 'kimi', 'ssh') else ''
                    agent['live_work'] = live_work(ANSI.sub('', raw))
                rec['agent'] = agent
                panes.append(rec)
    if codex_pids:  # Codex holds its thread's rollout file open; the thread id ends the file name
        for line in run('lsof', '-p', ','.join(map(str, codex_pids)), '-Fpn', timeout=60).splitlines():
            if line.startswith('p'):
                cur = int(line[1:])
            elif line.startswith('n') and 'rollout-' in line:
                m = re.search(r'(' + UUID + r')\.jsonl', line)
                if m and cur in codex_pids:
                    codex_pids[cur]['session_id'] = m.group(1)
    for rec in panes:
        a = rec['agent']
        if not a:
            continue
        sid = a.get('session_id')
        if a['kind'] == 'claude' and sid:
            a['resume'] = f'aim claude resume {sid}' if a.get('aimgr') else f'claude --resume {sid}'
        elif a['kind'] == 'codex' and sid:
            a['resume'] = f'aim codex resume {sid}' if a.get('aimgr') else f'codex resume {sid}'
    # detached jobs: started by a person or an agent, now owned by launchd's pid 1, and gone after a restart
    launchd = set(re.findall(r'^(\d+)\t', run('launchctl', 'list'), re.M))
    jobs = []
    for pid, (ppid, cmd) in ps.items():
        if ppid != 1 or cmd.startswith('-') or re.search(r'^/(System|usr/(libexec|sbin))|/Applications/|/Library/|launchd|herdr server', cmd):
            continue
        if not re.search(r'python|Python|node|\.sh\b|/zsh |/bash |ssh -f|colima|limactl|appium|tail ', cmd):
            continue
        jobs.append({'pid': pid, 'command': re.sub(r'Bearer \S+', 'Bearer [x]', cmd[:400]), 'launchd': str(pid) in launchd})
    if jobs:
        cwd, cur = {}, None
        for line in run('lsof', '-a', '-d', 'cwd', '-p', ','.join(str(j['pid']) for j in jobs), '-Fpn', timeout=60).splitlines():
            if line.startswith('p'):
                cur = int(line[1:])
            elif line.startswith('n'):
                cwd[cur] = line[1:]
        for j in jobs:
            j['cwd'] = cwd.get(j['pid'])
    data = {'saved_at': stamp, 'host': os.uname().nodename, 'note': args.note,
            'not_running_herdr_sessions': [s['name'] for s in sessions if not s.get('running')],
            'panes': panes, 'detached_jobs': jobs}
    path = os.path.join(out_dir, 'save.json')
    json.dump(data, open(path, 'w'), indent=1)
    latest = os.path.join(ROOT, 'latest')
    if os.path.islink(latest):
        os.remove(latest)
    os.symlink(out_dir, latest)
    agents = [p for p in panes if p['agent']]
    kinds = {}
    for p in agents:
        kinds[p['agent']['kind']] = kinds.get(p['agent']['kind'], 0) + 1
    print(f"saved {len(panes)} panes in {len({p['session'] for p in panes})} Herdr sessions: "
          + ', '.join(f'{v} {k}' for k, v in sorted(kinds.items())) + f" -> {path}")
    for p in agents:
        a = p['agent']
        flags = []
        if a.get('draft'):
            flags.append(f"DRAFT \"{a['draft'][:70]}\"")
        if a['kind'] in ('claude', 'codex') and not a.get('session_id'):
            flags.append('NO ID (capture it at stop)')
        if a['kind'] in ('ssh', 'other', 'kimi'):
            flags.append(a['kind'] + (': ' + a.get('command', '')[:70] if a.get('command') else ''))
        if a.get('live_work'):
            flags.append('live work ' + json.dumps(a['live_work']))
        if a.get('children', {}).get('reviewer_threads'):
            flags.append('reviewer ' + ','.join(a['children']['reviewer_threads']))
        if p['self']:
            flags.append('THIS SESSION: resume with ' + a.get('resume', '?'))
        if flags:
            print(f"  {p['session']} {p['pane']} {p['workspace_label']}: " + '; '.join(flags))
    own = [j for j in jobs if not j['launchd']]
    print(f"{len(jobs)} detached jobs ({len(jobs) - len(own)} restart on their own via launchd); "
          f"herdr sessions not running: {', '.join(data['not_running_herdr_sessions']) or 'none'}")


def load(path):
    path = path or os.path.join(ROOT, 'latest', 'save.json')
    if os.path.isdir(path):
        path = os.path.join(path, 'save.json')
    return path, json.load(open(path))


def pick(data, panes_arg, kinds):
    want = set(panes_arg.split(',')) if panes_arg else None
    out = []
    for p in data['panes']:
        a = p.get('agent')
        if not a or p.get('self'):
            continue
        key = f"{p['session']}:{p['pane']}"
        if want is not None:
            if key in want:
                out.append(p)
        elif a['kind'] in kinds:
            out.append(p)
    return out


def stop_one(p):
    s, pane, a = p['session'], p['pane'], p['agent']
    res = {'pane': f'{s}:{pane}', 'kind': a['kind']}
    raw = pane_read(s, pane, 14, ansi=True)
    draft = input_box(raw)
    if draft:
        res.update(result='skipped: text in the input box, left alone', draft=draft)
        return res
    if live_work(ANSI.sub('', raw)).get('working'):
        keys(s, pane, 'esc')
        time.sleep(2)
    run('herdr', '--session', s, 'pane', 'send-text', pane, '/quit' if a['kind'] == 'codex' else '/exit')
    keys(s, pane, 'enter')
    end = time.time() + 40
    while time.time() < end:
        time.sleep(1.5)
        if a['kind'] != 'ssh' and at_shell(s, pane):
            break
        scr = pane_read(s, pane, 25)
        if a['kind'] == 'ssh' and re.search(r'Resume this session with|To continue this session|To resume this session', scr):
            break
        if re.search(r'Feedback drafts|Send feedback|d to discard', scr):
            keys(s, pane, 'esc')  # a feedback draft is never sent
            continue
        if re.search(r'stop tasks|Background work is running', scr):
            for _ in range(4):
                sel = [l for l in pane_read(s, pane, 25).splitlines() if '❯' in l]
                if sel and 'stop' in sel[-1].lower():
                    break
                keys(s, pane, 'down')
            keys(s, pane, 'enter')
    recent = pane_read(s, pane, 60, src='recent-unwrapped')
    ids = re.findall(r'(?:claude resume|claude --resume|codex resume|kimi -r)\s+(' + UUID + r'|session_[0-9a-f-]+)', recent)
    if ids:
        res['printed_id'] = ids[-1]
    res['result'] = 'stopped' if (a['kind'] == 'ssh' and ids) or at_shell(s, pane) else 'check the pane'
    return res


def stop(args):
    path, data = load(args.save)
    kinds = {'claude', 'codex', 'kimi'} | ({'ssh'} if args.include_ssh else set())
    todo = pick(data, args.panes, kinds)
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(stop_one, todo))
    by = {r['pane']: r for r in results}
    for p in data['panes']:
        r = by.get(f"{p['session']}:{p['pane']}")
        if not r:
            continue
        a = p['agent']
        a['stop'] = r
        new = r.get('printed_id')
        if new and new != a.get('session_id'):
            a['session_id'] = new
            if new.startswith('session_'):
                a['resume'] = f'kimi -r {new}'
            elif a['kind'] == 'codex':
                a['resume'] = f"{'aim codex resume' if a.get('aimgr') else 'codex resume'} {new}"
            elif a['kind'] in ('claude', 'ssh'):
                a['resume'] = f"{'aim claude resume' if a.get('aimgr') or a['kind'] == 'ssh' else 'claude --resume'} {new}"
    json.dump(data, open(path, 'w'), indent=1)
    ok = [r for r in results if r['result'] == 'stopped']
    print(f"stopped {len(ok)} of {len(results)} -> {path}")
    for r in results:
        if r['result'] != 'stopped':
            print(f"  {r['pane']}: {r['result']}" + (f" (\"{r.get('draft', '')[:70]}\")" if r.get('draft') else ''))


def resume_one(p):
    s, pane, a = p['session'], p['pane'], p['agent']
    res = {'pane': f'{s}:{pane}'}
    if not at_shell(s, pane):
        res['result'] = 'pane is not at a shell (already running, or a program in the way)'
        return res
    run('herdr', '--session', s, 'pane', 'run', pane, f"cd {p.get('cwd') or '~'} && {a['resume']}")
    end, state = time.time() + 180, 'no prompt after 3 minutes'
    while time.time() < end:
        time.sleep(3)
        tail = '\n'.join([l for l in pane_read(s, pane, 30).splitlines() if l.strip()][-6:])
        if 'trust this folder' in tail.lower():
            state = 'waiting at the folder-trust prompt'
            break
        m = re.search(r'is busy|no other unlocked|hit your|limit reached|Not logged in|rror', tail)
        if m:
            state = 'blocked: ' + m.group(0)
            break
        if re.search(r'bypass permissions|Ask Codex|context: \d', tail):
            state = 'up'
            break
        if time.time() > end - 170 and at_shell(s, pane):  # the resume command already ended: say why
            last = [l for l in pane_read(s, pane, 12, src='recent-unwrapped').splitlines() if l.strip()]
            state = 'resume command exited: ' + (last[-2].strip()[:160] if len(last) >= 2 else '?')
            break
    if state == 'up' and a.get('draft'):
        run('herdr', '--session', s, 'pane', 'send-text', pane, a['draft'])  # back in the box, never sent
        res['draft_restored'] = True
    res['result'] = state
    return res


def mem_free():
    m = re.search(r'(\d+)%', run('memory_pressure', '-Q'))
    return int(m.group(1)) if m else None


def resume(args):
    path, data = load(args.save)
    todo = [p for p in pick(data, args.panes, {'claude', 'codex', 'kimi'}) if p['agent'].get('resume')]
    running = {s['name'] for s in json.loads(run('herdr', 'session', 'list', '--json') or '{}').get('sessions', []) if s.get('running')}
    waiting = sorted({p['session'] for p in todo if p['session'] not in running})
    todo = [p for p in todo if p['session'] in running]
    todo.sort(key=lambda p: not (p['agent'].get('live_work') or p['agent'].get('children', {}).get('reviewer_threads')))
    results = []
    for i in range(0, len(todo), args.batch):
        with cf.ThreadPoolExecutor(max_workers=args.batch) as ex:
            results += list(ex.map(resume_one, todo[i:i + args.batch]))
    up = [r for r in results if r['result'] == 'up']
    print(f"resumed {len(up)} of {len(results)}; memory {mem_free()}% free -> {path}")
    for r in results:
        if r['result'] != 'up':
            print(f"  {r['pane']}: {r['result']}")
    if waiting:
        print(f"  not resumed, Herdr session not running (needs `herdr session attach <name>`): {', '.join(waiting)}")
    notes = [p for p in todo if p['agent'].get('live_work') or p['agent'].get('children', {}).get('reviewer_threads')
             or p['agent'].get('children', {}).get('child_agents')]
    if notes:
        print('  had live work when saved (tell each what stopped):')
        for p in notes:
            a = p['agent']
            print(f"    {p['session']}:{p['pane']} {p['workspace_label']}: {json.dumps(a.get('live_work', {}))}"
                  + (f" reviewer {','.join(a['children']['reviewer_threads'])}" if a.get('children', {}).get('reviewer_threads') else '')
                  + (f" child agents {a['children']['child_agents']}" if a.get('children', {}).get('child_agents') else ''))
    ssh = [p for p in data['panes'] if p.get('agent') and p['agent']['kind'] == 'ssh']
    for p in ssh:
        print(f"  ssh pane {p['session']}:{p['pane']}: {p['agent'].get('command', '')[:90]}")


def tmp_copy(args, restore):
    path, data = load(args.save)
    dest = os.path.join(os.path.dirname(path), 'tmp')
    src, dst = ('/private/tmp/', dest) if not restore else (dest + '/', '/private/tmp')
    if os.stat(os.path.dirname(path)).st_dev != os.stat('/private/tmp').st_dev:
        print('the save point is on another volume, so clones would be full copies; pick a save root on the /tmp volume')
        sys.exit(1)
    os.makedirs(dest, exist_ok=True)
    log = os.path.join(os.path.dirname(path), 'tmp-restore.log' if restore else 'tmp-save.log')
    t0 = time.time()
    with open(log, 'w') as f:
        rc = subprocess.run(['cp', '-cRp', '.', dst], cwd=src, stderr=f).returncode
    errs = [l for l in open(log) if not re.search(r'socket|not supported|fifo|utimensat|Permission denied|extended attributes', l)]
    print(f"{'restored /tmp from' if restore else 'cloned /tmp into'} {dest} in {int(time.time() - t0)}s "
          f"(cp exit {rc}; {len(errs)} errors worth a look in {log})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('save'); a.add_argument('--note')
    a = sub.add_parser('stop'); a.add_argument('save', nargs='?'); a.add_argument('--panes'); a.add_argument('--include-ssh', action='store_true')
    a = sub.add_parser('resume'); a.add_argument('save', nargs='?'); a.add_argument('--panes'); a.add_argument('--batch', type=int, default=3)
    a = sub.add_parser('tmp-save'); a.add_argument('save', nargs='?')
    a = sub.add_parser('tmp-restore'); a.add_argument('save', nargs='?')
    args = ap.parse_args()
    {'save': save, 'stop': stop, 'resume': resume,
     'tmp-save': lambda x: tmp_copy(x, False), 'tmp-restore': lambda x: tmp_copy(x, True)}[args.cmd](args)


if __name__ == '__main__':
    main()
