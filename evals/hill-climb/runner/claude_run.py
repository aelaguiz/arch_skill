"""One isolated headless Claude Code session through aim (PLAN.md 6.10, INTERFACES.md).

`run_session` installs the skill (unless it is a no-skill control), snapshots the hashes of the agent's folder, starts
the workbook watcher, launches

    aim claude run <label> -- -p "<prompt>" --model sonnet --output-format stream-json --verbose \
      --permission-mode bypassPermissions --setting-sources project --strict-mcp-config \
      --settings '{"disableAllHooks":true}' --tools "Bash,Read,Write,Edit,Task,Skill" --disallowedTools 'mcp__*' \
      --no-session-persistence --max-budget-usd <budget>

from `work/` with stdin closed, in its own process group, stamps every stdout line on arrival into `RUN/stream.jsonl`,
kills the whole group on timeout, and writes `RUN/session.json`.

The session's PATH is `work/bin:/usr/bin:/bin:/usr/sbin:/sbin` (a departure from PLAN.md 6.10, which inherited the
runner's PATH): this Mac's real `gws` (signed in to the owner's Google account), an unrelated `sim` and `claude` itself
live in ~/.local/bin and /opt/homebrew/bin, and nothing the agents run may reach them. `work/bin/python3` links to the
runner's own Python. aim finds `claude` on its own PATH, so aim also gets one private folder holding a `claude`
launcher (and `node`, for an aim that is a node script); the launcher drops that folder from PATH before it starts the
real `claude`, so the session and its tools see only the PATH above.

The account comes from `aim claude status --json` (`choose_account`); `run_session_with_accounts` applies the busy rule:
a "busy" refusal is retried after 60 seconds up to three times, then the next account by the same rule is used.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from runner import transcript as transcript_mod  # noqa: E402
from runner.watch import POLL_INTERVAL_S, Watcher  # noqa: E402

MODEL = "sonnet"
TOOLS = "Bash,Read,Write,Edit,Task,Skill"
DISALLOWED_TOOLS = "mcp__*"
SETTINGS_JSON = '{"disableAllHooks":true}'

BUDGET_SCENARIO_USD = 5
BUDGET_SETUP_USD = 8
BUDGET_TICK_USD = 6
TIMEOUT_S = 20 * 60

ISOLATION_ENV = {
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
    "ENABLE_CLAUDEAI_MCP_SERVERS": "false",
    "CLAUDE_CODE_DISABLE_BUNDLED_SKILLS": "1",
    "CLAUDE_CODE_DISABLE_ARTIFACT": "1",
    "CLAUDE_CODE_DISABLE_WORKFLOWS": "1",
    "CLAUDE_CODE_DISABLE_CRON": "1",
}

INSTALLED_SKILLS = ("hill-climb", "prompt-authoring", "_shared", "readable-reports")   # PLAN.md 13.2: reports
SKIP_DIR_NAMES = frozenset({"build", "prompts", "__pycache__"})  # what the repo's Makefile never installs

BUSY_MARKERS = ("is busy", "aimgr_credential_busy")
NO_ELIGIBLE_CODE = "no_eligible_pool_account"

BUSY_WAIT_S = 60
BUSY_RETRIES = 3
MAX_LIMIT_WAIT_S = 6 * 3600     # a pinned account's limit that resets later than this stops the batch
LIMIT_COOLDOWN_S = 600          # when aim does not yet show the limit a session hit


def iso_utc(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_budget(budget_usd) -> str:
    return "%g" % float(budget_usd)


# ----------------------------------------------------------------------------------------------------------------------
# command, environment, skills


def build_command(label: str, prompt: str, budget_usd, aim: str = "aim") -> list:
    """The exact argv of PLAN.md 6.10."""
    return [
        aim, "claude", "run", label, "--",
        "-p", prompt,
        "--model", MODEL,
        "--output-format", "stream-json",
        "--verbose",
        "--permission-mode", "bypassPermissions",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--settings", SETTINGS_JSON,
        "--tools", TOOLS,
        "--disallowedTools", DISALLOWED_TOOLS,
        "--no-session-persistence",
        "--max-budget-usd", format_budget(budget_usd),
    ]


def command_line(argv) -> str:
    """The argv as one shell line (for logs and the dry-run print)."""
    return " ".join(shlex.quote(str(part)) for part in argv)


SYSTEM_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
LAUNCH_DIR_PREFIX = "hcl-aim-"


def session_path(work) -> str:
    """The PATH every session and its tools see: the lab's wrappers and the system's own folders, nothing else."""
    return f"{Path(work).resolve() / 'bin'}:{SYSTEM_PATH}"


def build_env(work, base_env=None, launch_dir=None) -> dict:
    """The session's environment: the runner's, with PATH = work/bin:/usr/bin:/bin:/usr/sbin:/sbin (plus aim's private
    launcher folder, which the launcher removes again before claude starts) and the seven isolation switches."""
    env = dict(os.environ if base_env is None else base_env)
    env["PATH"] = session_path(work) + (f":{launch_dir}" if launch_dir else "")
    env.update(ISOLATION_ENV)
    return env


CLAUDE_LAUNCHER = """#!/bin/sh
# The hill-climb lab's claude launcher (evals/hill-climb/runner/claude_run.py). aim finds claude on its PATH; this
# drops its own folder from PATH before starting the real claude, so nothing the session runs can find claude.
set -f
dir={dir}
new=''
IFS=:
for part in $PATH; do
  [ "$part" = "$dir" ] && continue
  new="${{new:+$new:}}$part"
done
unset IFS
PATH=$new
export PATH
exec {claude} "$@"
"""


def prepare_launch_dir(base_env=None) -> Path:
    """A private folder for aim's PATH with a `claude` launcher and `node`, found on the runner's own PATH."""
    path = (base_env or os.environ).get("PATH")
    claude = shutil.which("claude", path=path)
    if not claude:
        raise FileNotFoundError("claude is not on the runner's PATH; aim could not start a session")
    folder = Path(tempfile.mkdtemp(prefix=LAUNCH_DIR_PREFIX))
    launcher = folder / "claude"
    launcher.write_text(CLAUDE_LAUNCHER.format(dir=shlex.quote(str(folder)), claude=shlex.quote(claude)),
                        encoding="utf-8")
    launcher.chmod(0o755)
    node = shutil.which("node", path=path)
    if node:
        (folder / "node").symlink_to(node)
    return folder


def link_python(work, python: str = sys.executable) -> Path:
    """work/bin/python3 -> the runner's own Python, so agents keep a modern python3 on the narrow PATH."""
    target = Path(work) / "bin" / "python3"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or target.exists():
        target.unlink()
    target.symlink_to(python)
    return target


def resolve_aim(aim: str = "aim", base_env=None) -> str:
    """An absolute path for aim, looked up on the runner's own PATH (never the session's narrow one)."""
    if os.sep in aim:
        return os.path.abspath(aim)
    path = (base_env or os.environ).get("PATH")
    found = shutil.which(aim, path=path)
    if not found:
        raise FileNotFoundError(f"{aim} is not on the runner's PATH")
    return found


def _skill_ignore(_directory, names):
    return [n for n in names if n in SKIP_DIR_NAMES or n.endswith(".pyc") or n == ".DS_Store"]


def install_skills(work, repo) -> list:
    """Copy skills/hill-climb, skills/prompt-authoring, skills/_shared and skills/readable-reports into
    work/.claude/skills/."""
    dest = Path(work) / ".claude" / "skills"
    dest.mkdir(parents=True, exist_ok=True)
    installed = []
    for name in INSTALLED_SKILLS:
        source = Path(repo) / "skills" / name
        if not source.is_dir():
            raise FileNotFoundError(f"skill folder missing: {source}")
        target = dest / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=_skill_ignore)
        installed.append(name)
    return installed


def file_hashes(root, skip_top=(".claude",)) -> dict:
    """{relative path: sha256} of every file under root (the agent's folder before the session)."""
    root = Path(root)
    out = {}
    if not root.is_dir():
        return out
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in skip_top:
            continue
        if path.is_symlink():
            out[rel.as_posix()] = "symlink:" + os.readlink(path)
        elif path.is_file():
            try:
                out[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
    return out


# ----------------------------------------------------------------------------------------------------------------------
# the session


def _pump(stdout, out_fh, counter):
    for raw in iter(stdout.readline, b""):
        t = time.time()
        text = raw.decode("utf-8", errors="replace")
        if text.endswith("\n"):
            text = text[:-1]
        if text.endswith("\r"):
            text = text[:-1]
        try:
            event = json.loads(text) if text.strip() else None
        except ValueError:
            event = None
        if isinstance(event, dict):
            line = {"t": t, "e": event}
            counter["events"] += 1
        else:
            line = {"t": t, "raw": text}
            counter["raw"] += 1
        out_fh.write(json.dumps(line, ensure_ascii=False) + "\n")
        out_fh.flush()


def _signal_group(pgid: int, sig) -> bool:
    try:
        os.killpg(pgid, sig)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def kill_process_group(proc, grace_s: float = 10.0) -> None:
    """SIGTERM the session's process group, wait up to grace_s for the leader, then SIGKILL whatever is left."""
    pgid = proc.pid  # start_new_session=True makes the child its group's leader
    _signal_group(pgid, signal.SIGTERM)
    try:
        proc.wait(timeout=grace_s)
    except subprocess.TimeoutExpired:
        pass
    _signal_group(pgid, signal.SIGKILL)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def detect_busy(tr, stderr_text: str) -> bool:
    """aim refused the account before any session started."""
    if tr.events:
        return False
    text = (stderr_text + "\n" + "\n".join(raw for _t, raw in tr.raw_lines)).lower()
    return any(marker in text for marker in BUSY_MARKERS)


def detect_no_eligible(tr, stderr_text: str) -> bool:
    if tr.events:
        return False
    text = (stderr_text + "\n" + "\n".join(raw for _t, raw in tr.raw_lines)).lower()
    return NO_ELIGIBLE_CODE in text


def detect_limited(tr, stderr_text: str) -> bool:
    """The account hit a usage limit during the session."""
    for _t, ev in tr.events:
        if ev.get("type") == "rate_limit_event":
            status = str((ev.get("rate_limit_info") or {}).get("status") or "").lower()
            if status and not status.startswith("allowed"):
                return True
    last = tr.last_result
    if last is not None and last.get("is_error"):
        text = str(last.get("result") or "").lower()
        if last.get("api_error_status") == 429 or "usage limit" in text or "rate limit" in text:
            return True
    return False


def run_session(work, prompt: str, label: str, run_dir, budget_usd: float, timeout_s: int, install_skill: bool,
                repo, *, aim: str = "aim", base_env=None, poll_interval: float = POLL_INTERVAL_S,
                kill_grace_s: float = 10.0) -> dict:
    """One isolated headless session (PLAN.md 6.10). Writes RUN/stream.jsonl (arrival-stamped), RUN/watch.jsonl,
    RUN/stderr.txt, RUN/pre_session_hashes.json and RUN/session.json; returns the session.json dict."""
    work = Path(work).resolve()
    run_dir = Path(run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    installed = install_skills(work, repo) if install_skill else []
    link_python(work)
    (run_dir / "pre_session_hashes.json").write_text(
        json.dumps(file_hashes(work), indent=1, sort_keys=True) + "\n", encoding="utf-8")

    aim_path = resolve_aim(aim, base_env)       # on the runner's PATH, before the session's narrow one
    argv = build_command(label, prompt, budget_usd, aim=aim_path)
    launch_dir = prepare_launch_dir(base_env)
    env = build_env(work, base_env, launch_dir)
    stream_path = run_dir / "stream.jsonl"
    stderr_path = run_dir / "stderr.txt"
    watcher = Watcher(work / "workbook", run_dir / "watch.jsonl", interval=poll_interval)
    watcher.start()

    counter = {"events": 0, "raw": 0}
    started = time.time()
    timed_out = False
    exit_code = None
    launch_error = None
    with open(stream_path, "w", encoding="utf-8") as out_fh, open(stderr_path, "wb") as err_fh:
        try:
            proc = subprocess.Popen(
                argv, cwd=str(work), env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=err_fh,
                start_new_session=True)
        except OSError as exc:
            proc = None
            launch_error = f"{type(exc).__name__}: {exc}"
        if proc is not None:
            reader = threading.Thread(target=_pump, args=(proc.stdout, out_fh, counter), daemon=True)
            reader.start()
            try:
                exit_code = proc.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                timed_out = True
                kill_process_group(proc, kill_grace_s)
                exit_code = proc.returncode
            reader.join(timeout=5.0)
            # Whatever the session left in its group (tool servers, background shells) is closed here; a straggler
            # that still holds stdout open would otherwise keep the reader waiting.
            if _signal_group(proc.pid, signal.SIGTERM):
                time.sleep(0.2)
                _signal_group(proc.pid, signal.SIGKILL)
            reader.join(timeout=5.0)
            try:
                proc.stdout.close()
            except OSError:
                pass
    ended = time.time()
    watcher.stop()
    shutil.rmtree(launch_dir, ignore_errors=True)

    tr = transcript_mod.parse(stream_path)
    try:
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        stderr_text = ""
    if launch_error:
        stderr_text = (stderr_text + "\n" + launch_error).strip()
        with open(stderr_path, "a", encoding="utf-8") as fh:
            fh.write(launch_error + "\n")
    last = tr.last_result or {}
    info = {
        "exit": exit_code,
        "timed_out": timed_out,
        "cost_usd": tr.cost_usd,
        "label": label,
        "started": iso_utc(started),
        "ended": iso_utc(ended),
        "started_t": started,
        "ended_t": ended,
        "budget_usd": float(budget_usd),
        "timeout_s": timeout_s,
        "budget_hit": tr.budget_hit,
        "busy": detect_busy(tr, stderr_text),
        "no_eligible": detect_no_eligible(tr, stderr_text),
        "limited": detect_limited(tr, stderr_text),
        "result_subtype": last.get("subtype"),
        "result_ok": tr.ok,
        "events": counter["events"],
        "raw_lines": counter["raw"],
        "watch_lines": watcher.lines_written,
        "skills_installed": installed,
        "prompt": prompt,
        "command": argv,
        "launch_error": launch_error,
    }
    (run_dir / "session.json").write_text(json.dumps(info, indent=1) + "\n", encoding="utf-8")
    return info


def session_status(info: dict) -> str:
    """ok, timeout, budget, busy, limited or crashed."""
    if info.get("timed_out"):
        return "timeout"
    if info.get("budget_hit"):
        return "budget"
    if info.get("busy"):
        return "busy"
    if info.get("limited"):
        return "limited"
    if info.get("result_ok"):
        return "ok"
    return "crashed"


# ----------------------------------------------------------------------------------------------------------------------
# accounts

HUMAN_ACTION_STATES = frozenset({
    "reauth_required", "auth_invalid", "scope_blocked", "credential_missing", "credential_candidate",
    "credential_incomplete", "identity_unverified", "identity_mismatch", "credential_generation_invalid",
    "duplicate_account",
})


class NoEligibleAccount(RuntimeError):
    code = NO_ELIGIBLE_CODE

    def __init__(self, detail: str = ""):
        super().__init__(f"{NO_ELIGIBLE_CODE}: {detail}".strip())


def aim_status(aim: str = "aim", timeout_s: int = 120, base_env=None) -> dict:
    """`aim claude status --json` (aim exits 1 when any account is unhealthy, but still prints the JSON)."""
    argv = [resolve_aim(aim, base_env), "claude", "status", "--json"]
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s, stdin=subprocess.DEVNULL,
                          env=dict(os.environ if base_env is None else base_env))
    try:
        return json.loads(proc.stdout)
    except ValueError as exc:
        raise RuntimeError(f"aim claude status --json gave no JSON (exit {proc.returncode}): "
                           f"{proc.stderr.strip()[:300]}") from exc


def _windows(account):
    usage = account.get("usage") or {}
    windows = usage.get("windows") if isinstance(usage, dict) else None
    return [w for w in (windows or []) if isinstance(w, dict)]


def _window_used(account, kinds, labels):
    for window in _windows(account):
        kind = str(window.get("kind") or "")
        label = str(window.get("label") or "").strip().lower()
        if kind in kinds or label in labels:
            try:
                return float(window.get("usedPercent"))
            except (TypeError, ValueError):
                return None
    return None


def account_state(account: dict) -> str:
    """'needs-you', 'limited', 'not-ready' or 'ok' (the plan's three exclusions, then eligible)."""
    auth = str(account.get("authState") or "")
    cred = str(account.get("credentialState") or "")
    if auth in HUMAN_ACTION_STATES or cred in HUMAN_ACTION_STATES:
        return "needs-you"
    if auth == "usage_limited":
        return "limited"
    for window in _windows(account):
        if window.get("active") is False:
            continue
        try:
            used = float(window.get("usedPercent"))
        except (TypeError, ValueError):
            used = None
        if (used is not None and used >= 100) or str(window.get("severity") or "") in ("exceeded", "blocked"):
            return "limited"
    if account.get("credentialReady") is not True:
        return "not-ready"
    return "ok"


def usage_left(account: dict):
    """(five-hour % left, weekly % left); None for a window aim has not read."""
    five = _window_used(account, {"session"}, {"5h", "session"})
    week = _window_used(account, {"weekly_all"}, {"week", "weekly"})
    return (None if five is None else 100.0 - five, None if week is None else 100.0 - week)


def rank_accounts(status: dict, exclude=()) -> list:
    """Eligible labels, best first: the most usage left in both the five-hour and weekly windows (the tighter of the
    two first, then the other); accounts whose usage is unknown come last."""
    excluded = set(exclude)
    known, unknown = [], []
    for account in status.get("accounts") or []:
        if not isinstance(account, dict):
            continue
        label = account.get("label")
        if not label or label in excluded or account_state(account) != "ok":
            continue
        five, week = usage_left(account)
        if five is None or week is None:
            unknown.append(label)
        else:
            known.append((-min(five, week), -max(five, week), label))
    return [label for *_rank, label in sorted(known)] + sorted(unknown)


def choose_account(status: dict, exclude=()) -> str:
    ranked = rank_accounts(status, exclude)
    if not ranked:
        raise NoEligibleAccount("no Claude account is free of needs-you and limits with credentials ready"
                                + (f" (excluded: {', '.join(sorted(exclude))})" if exclude else ""))
    return ranked[0]


class AccountPool:
    """The batch's account. Chosen once by the rule above and replaced by the same rule when it turns busy or limited,
    unless the batch pinned one with `--account`: a pinned account is never swapped for another of the owner's
    accounts. When it hits a usage limit the batch waits for the window to reset (no new session starts meanwhile); when
    another machine holds it, or its limit resets too far away, the batch stops and reports. `--account a,b` pins an
    ordered list: one account at a time, the next taking over only when the current one is limited or busy; the last
    one left behaves as a single pinned account."""

    def __init__(self, aim: str = "aim", fixed: str | None = None, status_fn=None, log=None, base_env=None,
                 sleep=time.sleep, clock=time.time, max_wait_s: float = MAX_LIMIT_WAIT_S):
        self.aim = aim
        listed = [x.strip() for x in fixed.split(",")] if isinstance(fixed, str) else list(fixed or [])
        self.fixed_list = [x for x in listed if x]
        self.fixed = self.fixed_list[0] if self.fixed_list else None
        self.base_env = base_env
        self._status_fn = status_fn or (lambda: aim_status(aim, base_env=base_env))
        self.excluded = set()
        self.current = None
        self.history = []
        self.paused_until = 0.0
        self._sleep = sleep
        self._clock = clock
        self.max_wait_s = max_wait_s
        self._lock = threading.Lock()
        self._log = log or (lambda message: print(message, file=sys.stderr, flush=True))

    def label(self) -> str:
        while True:
            with self._lock:
                wait = self.paused_until - self._clock()
            if wait <= 0:
                break
            self._sleep(min(wait, 60.0))
        with self._lock:
            if self.current is None:
                if self.fixed and self.fixed not in self.excluded:
                    self.current = self.fixed
                elif self.fixed:
                    raise NoEligibleAccount(f"every pinned account ({', '.join(self.fixed_list)}) is excluded")
                else:
                    self.current = choose_account(self._status_fn(), self.excluded)
                self.history.append(self.current)
                self._log(f"[accounts] using {self.current}")
            return self.current

    def _advance(self, label: str, reason: str) -> bool:
        """Move a pinned list past `label` to its next account; False when `label` is the last one left."""
        with self._lock:
            if label != self.fixed or self.fixed_list.index(label) + 1 >= len(self.fixed_list):
                return False
            self.fixed = self.fixed_list[self.fixed_list.index(label) + 1]
            self.excluded.add(label)
            if self.current == label:
                self.current = None
        self._log(f"[accounts] {label} {reason}; moving to the next pinned account, {self.fixed}")
        return True

    def drop(self, label: str, reason: str) -> None:
        if self.fixed and label == self.fixed:
            if self._advance(label, reason):
                return
            raise NoEligibleAccount(f"{label} is pinned and {reason}; the batch stops rather than use another account")
        with self._lock:
            self.excluded.add(label)
            if self.current == label:
                self.current = None
            self._log(f"[accounts] dropping {label}: {reason}")

    def limited(self, label: str) -> None:
        """A session on `label` hit a usage limit: drop it, or for a pinned account pause the batch until it resets."""
        if not (self.fixed and label == self.fixed):
            if not self.fixed:
                self.drop(label, "usage limit reached during a session")
            return                                  # a pinned list already moved past this account
        if self._advance(label, "hit its usage limit"):
            return
        now = self._clock()
        reset = limit_reset(self._status_fn(), label, now)
        if reset is None:
            reset = now + LIMIT_COOLDOWN_S          # aim has not caught up with the limit yet: wait and look again
        if reset - now > self.max_wait_s:
            raise NoEligibleAccount(f"{label} is pinned and its usage limit resets at "
                                    f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(reset))}, too far off to wait")
        with self._lock:
            self.paused_until = max(self.paused_until, reset + 60.0)
            until = self.paused_until
        self._log(f"[accounts] {label} hit its usage limit; pausing the batch until "
                  f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(until))}")


def limit_reset(status: dict, label: str, now: float):
    """Epoch seconds when `label`'s exhausted usage window resets, or None when aim shows it usable."""
    for account in status.get("accounts") or []:
        if not isinstance(account, dict) or account.get("label") != label:
            continue
        if account_state(account) == "ok":
            return None
        resets = []
        for window in _windows(account):
            try:
                used = float(window.get("usedPercent"))
            except (TypeError, ValueError):
                used = None
            exhausted = (used is not None and used >= 100) or str(window.get("severity") or "") in ("exceeded",
                                                                                                    "blocked")
            if exhausted and window.get("resetAt"):
                try:
                    resets.append(float(window["resetAt"]) / 1000.0)
                except (TypeError, ValueError):
                    pass
        future = [t for t in resets if t > now]
        return max(future) if future else now + LIMIT_COOLDOWN_S
    return None


def run_session_with_accounts(pool: AccountPool, *, sleep=time.sleep, busy_wait_s: float = BUSY_WAIT_S,
                              busy_retries: int = BUSY_RETRIES, runner=None, **session_kwargs) -> dict:
    """run_session (or `runner`, a function with the same account contract, such as the simulated owner's session) on
    the pool's account. A busy refusal is retried after busy_wait_s up to busy_retries times, then the next account is
    used; `no_eligible_pool_account` raises NoEligibleAccount."""
    runner = runner or run_session
    tries = 0
    while True:
        label = pool.label()
        info = runner(label=label, **session_kwargs)
        if info.get("no_eligible"):
            raise NoEligibleAccount(f"aim refused {label}")
        if info.get("busy"):
            if tries < busy_retries:
                tries += 1
                sleep(busy_wait_s)
                continue
            pool.drop(label, f"busy after {busy_retries} retries")
            tries = 0
            continue
        info["account_history"] = list(pool.history)
        return info


# ----------------------------------------------------------------------------------------------------------------------
# machine load


def load_1m() -> float:
    try:
        return os.getloadavg()[0]
    except OSError:
        return 0.0


def free_inactive_gb() -> float:
    """Free plus inactive memory in GB (vm_stat on macOS, MemAvailable on Linux)."""
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        out = ""
    if out:
        page = 4096
        match = re.search(r"page size of (\d+) bytes", out)
        if match:
            page = int(match.group(1))
        pages = 0
        for name in ("Pages free", "Pages inactive"):
            found = re.search(rf"{name}:\s+(\d+)", out)
            if found:
                pages += int(found.group(1))
        return pages * page / 1e9
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024 / 1e9
    except OSError:
        pass
    return 0.0


def allowed_sessions(max_parallel: int = 3, load_limit: float = 27.0, mem_limit_gb: float = 16.0,
                     load=None, mem_gb=None) -> int:
    """Up to max_parallel sessions while the one-minute load is under load_limit and free plus inactive memory is at
    least mem_limit_gb, else 1 (PLAN.md 6.10, draft 8: 27 on this Mac, 9 on the Studio)."""
    load = load_1m() if load is None else load
    mem_gb = free_inactive_gb() if mem_gb is None else mem_gb
    return max_parallel if (load < load_limit and mem_gb >= mem_limit_gb) else 1
