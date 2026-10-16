"""The simulated owner of the intake interview (docs/hill-climb-skill-2026-10-14/INTAKE_PLAN.md, "The lab").

`ask(brief, message, history, pool=..., out_dir=...)` gives the agent's latest final message to one clean Sonnet
session with no tools at all, through aim, from an empty temporary folder, with the same isolation as the agent's
sessions (`runner/claude_run.py`: its environment switches, `--setting-sources project`, `--strict-mcp-config`, hooks
off, no MCP) plus `--tools ""` (the CLI's own way to turn every built-in tool off) and `--disable-slash-commands`. The
session's system prompt is `OWNER_SYSTEM` with the scenario's hidden brief in it; its user prompt is the conversation
so far, the latest message, and any report the agent wrote for the owner in `reports/` that turn (the skill may play the
design back in the form the owner reads). It replies with one JSON object, which `parse_reply` reads:

    {"answer": "...", "asked_method": false, "asked_finding_out": false, "asked_known": false,
     "multiple_questions": false, "outcome_check": false, "playback": false, "signed_off": false, "why": ""}

A reply that does not parse is asked for again, up to twice. Each call leaves `system.md`, `user.md`, one folder per
attempt (`stream.jsonl`, `stderr.txt`) and `reply.json` in `out_dir`.
"""
from __future__ import annotations

import json
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders.common import OWNER_FLAGS  # noqa: E402
from runner import claude_run  # noqa: E402
from runner import transcript as transcript_mod  # noqa: E402

OWNER_MODEL = "sonnet"
OWNER_BUDGET_USD = 0.5
OWNER_TIMEOUT_S = 300
PARSE_RETRIES = 2
LIMITED_RERUNS = 3
HISTORY_MESSAGE_CHARS = 3000
FILE_CHARS = 12000          # of each report the agent wrote for the owner this turn
BRIEF_MARK = "<<BRIEF>>"

OWNER_SYSTEM = """You are standing in for the owner of a business in a test of an AI agent. The agent is about to run a \
"hill climb" for you: a long series of ad or post tests that it runs on its own for weeks, spending your money, and \
after setup it will ask you for nothing but more money. Before anything runs, it interviews you, one question per \
message, until it understands what you want. Each time, you read the agent's latest message, answer it the way the \
owner in your brief would, and judge what kind of message it was.

Why your answers matter
The agent will work for weeks toward whatever it understood from this interview, and the test is graded from your \
answers and your judgments. Two things would spoil it:
- Saying more than you were asked. If you volunteer something the agent never asked about, nobody can tell whether it \
would have found it out, and finding out is what is being tested. Answer what the message asks, then stop.
- Doing the agent's job. How to run the climb (how big each test is, how long it runs, how sure to be before acting, \
how to split the money, what to try first, which things to vary) is the agent's expertise; you hired it for that. What \
the climb exists to discover (who responds, who pays, which ads will work) you do not know; finding it out is why you \
are paying for the climb. If you answered either, you would hide the agent's mistake.

Your brief
<brief>
<<BRIEF>>
</brief>
The brief is everything you know about your business and this climb. Its last part says what the agent was already \
given in writing: its request and the files in its folder.

How to answer
- Speak as this owner: first person, plain and busy, one or two sentences, no lists or headings. You are not an \
assistant: do not offer help, and do not ask the agent questions back.
- Answer what the message asks, from your brief, in your own words, keeping its numbers and names exact. If it asks \
several things, answer each briefly.
- Where your brief says nothing about what is asked, give a short high-level thought if this owner would have one, or \
say it is the agent's call. Never invent facts the brief does not give: numbers, names, files, tools, past results.
- Some lines in your brief say to mention them only when the agent asks about that subject. Keep to that, even when a \
nearby question brings them to mind.
- When the message asks how to run the climb, say that is the agent's call and add nothing.
- When it asks what the climb is meant to find out, say you don't know; that is what the climb is for.
- When it asks something already written down, answer briefly and say where it is written.
- When it describes a made-up outcome and asks what you would decide or accept, answer as this owner would, from the \
goals and values in your brief; if they do not settle it, give your honest gut call.
- When the agent wrote something for you to read this turn (a file in reports/), its text comes with the message: \
read it as part of the message.
- When it plays back the overall plan for you to check, compare it with what you have told the agent in the \
conversation and with your brief. Correct whatever it gets wrong about what you said, and anything you told it that it \
left out. Do not add things it never asked you about. If nothing needs correcting, approve it plainly, for example \
"That's right, go ahead."

How to judge the message
Judge the latest message by what it asks you. Each flag is true or false.
- asked_method: it asks you to decide or approve how the climb is run: test sizes or budgets per test, how long tests \
run, how sure to be before acting, how to split the money between tests or between trying new things and backing \
winners, which attributes to vary, what to try first, when to replace a winner. Asking what you want is not method: \
your purpose, how much of your earlier work to use (use it, use it as history only, or leave it out), what counts as \
success, your money, your limits, your materials, your tools, your quality bar, your ideas, where research should look, \
how you want to hear about progress. Describing its own approach without asking you \
to choose it is not method either, and neither is a playback that includes its plan.
- asked_finding_out: it asks you what the climb exists to discover: who your audience or customers are, who will \
respond or pay, or which kind of ad, message, angle or offer will work best. Asking for your own ideas to try is not \
this; asking you to predict or pick the winner is.
- asked_known: it asks for something the request or its files already state plainly. Asking about something the \
written words leave open is not this, nor is confirming a point inside a playback.
- multiple_questions: it asks more than one question that each need their own answer. One question with options to \
choose from, one question with "and why?", or a playback asking whether it is right and what to change, is one \
question.
- outcome_check: it describes a result or situation that has not happened and asks what you would decide, accept or \
count as success.
- playback: it plays the overall design back to you (your answers and what its research found) for you to confirm or \
correct, rather than asking about one thing.
- signed_off: your answer approves a playback and tells it to go ahead, including "one correction: X; otherwise go \
ahead". It is false when you correct something without saying go ahead. It can be true only when playback is true.
Set why to one short sentence saying what made any of the first four flags true, or "" when none is.

Examples of judging, with the reason:
- "What daily budget should each test get?" asks method: splitting the money is the agent's call.
- "Who buys the app, beginners or regulars?" asks what the climb finds out: who responds is what it discovers.
- "Do you have ideas you want in the mix?" is fine: your ideas are yours to give.
- "Is $600 the whole budget?" asks something known when the request says "You have $600"; had the request named no \
amount, it would be fine.

Reply with one JSON object and nothing else, in this shape:
{"answer": "...", "asked_method": false, "asked_finding_out": false, "asked_known": false, "multiple_questions": false, \
"outcome_check": false, "playback": false, "signed_off": false, "why": ""}
"""


# ----------------------------------------------------------------------------------------------------------------------
# prompts and command


def system_prompt(brief: str) -> str:
    return OWNER_SYSTEM.replace(BRIEF_MARK, str(brief or "").strip())


def _shorten(text: str, limit: int = HISTORY_MESSAGE_CHARS) -> str:
    """An earlier message for the record of the conversation: its end, where the question is, when it is long."""
    text = str(text or "").strip()
    return text if len(text) <= limit else "[...] " + text[-limit:]


def user_prompt(message: str, history=(), files=None) -> str:
    """The conversation so far ([(agent message, owner answer)], oldest first), the agent's latest message and the
    files it wrote for the owner this turn ({path in the agent's folder: text})."""
    parts = []
    if history:
        parts.append("The conversation so far, oldest first (the agent's earlier messages, shortened where long, and "
                     "your answers):")
        for number, (said, answer) in enumerate(history, start=1):
            parts.append(f"Turn {number}, the agent:\n{_shorten(said)}\n\nTurn {number}, you:\n{str(answer).strip()}")
    else:
        parts.append("This is the agent's first message to you.")
    parts.append(f"The agent's latest message:\n<message>\n{str(message or '').strip()}\n</message>")
    for path, text in sorted((files or {}).items()):
        text = str(text or "").strip()
        if len(text) > FILE_CHARS:
            text = text[:FILE_CHARS] + "\n[...]"
        parts.append(f"A file the agent wrote for you this turn, {path}:\n<file>\n{text}\n</file>")
    parts.append("Answer it and judge it. Reply with the JSON object only.")
    return "\n\n".join(parts) + "\n"


def build_command(label: str, system: str, user: str, budget_usd=OWNER_BUDGET_USD, aim: str = "aim") -> list:
    """The owner's session: the agent sessions' isolation, no tools, no skills, the brief as the system prompt."""
    return [
        aim, "claude", "run", label, "--",
        "-p", user,
        "--model", OWNER_MODEL,
        "--output-format", "stream-json",
        "--verbose",
        "--system-prompt", system,
        "--tools", "",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--settings", claude_run.SETTINGS_JSON,
        "--disallowedTools", claude_run.DISALLOWED_TOOLS,
        "--disable-slash-commands",
        "--no-session-persistence",
        "--max-budget-usd", claude_run.format_budget(budget_usd),
    ]


# ----------------------------------------------------------------------------------------------------------------------
# the reply


def _flag(value):
    """(bool, given) for a flag's value: JSON booleans as they are, "true"/"yes" and "false"/"no" read as such."""
    if isinstance(value, bool):
        return value, True
    if isinstance(value, str) and value.strip().lower() in ("true", "yes", "false", "no"):
        return value.strip().lower() in ("true", "yes"), True
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value), True
    return False, False


def _objects(text: str):
    """Every JSON object in a text, in order, wherever it starts (bare, fenced or wrapped in prose)."""
    decoder = json.JSONDecoder()
    found = []
    index = text.find("{")
    while index != -1:
        try:
            obj, end = decoder.raw_decode(text, index)
        except ValueError:
            index = text.find("{", index + 1)
            continue
        if isinstance(obj, dict):
            found.append(obj)
        index = text.find("{", end)
    return found


def parse_reply(text: str) -> dict:
    """{"answer", "flags", "why", "missing_flags", "error"} from the owner's reply. The last JSON object with an
    `answer` is the reply; a flag it leaves out counts as false and is listed in `missing_flags`."""
    candidates = [obj for obj in _objects(str(text or "")) if "answer" in obj]
    if not candidates:
        return {"answer": None, "flags": {}, "why": "", "missing_flags": list(OWNER_FLAGS),
                "error": "no JSON object with an answer in the reply"}
    obj = candidates[-1]
    answer = " ".join(str(obj.get("answer") or "").split())
    flags, missing = {}, []
    for name in OWNER_FLAGS:
        value, given = _flag(obj.get(name))
        flags[name] = value
        if not given:
            missing.append(name)
    return {"answer": answer or None, "flags": flags, "why": str(obj.get("why") or "").strip(),
            "missing_flags": missing, "error": None if answer else "the reply's answer is empty"}


# ----------------------------------------------------------------------------------------------------------------------
# one session


def run_owner_session(label: str, system: str, user: str, out_dir, budget_usd=OWNER_BUDGET_USD,
                      timeout_s: int = OWNER_TIMEOUT_S, aim: str = "aim", base_env=None,
                      kill_grace_s: float = 10.0) -> dict:
    """One owner session from an empty temporary folder. Writes OUT/stream.jsonl (arrival-stamped) and OUT/stderr.txt;
    returns the account facts `run_session_with_accounts` reads, the reply's text and its cost."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix="hc-owner-"))
    launch_dir = None
    aim_path = claude_run.resolve_aim(aim, base_env)
    argv = build_command(label, system, user, budget_usd, aim=aim_path)
    stream_path, stderr_path = out_dir / "stream.jsonl", out_dir / "stderr.txt"
    counter = {"events": 0, "raw": 0}
    started = time.time()
    timed_out, exit_code, launch_error = False, None, None
    try:
        launch_dir = claude_run.prepare_launch_dir(base_env)
        env = claude_run.build_env(folder, base_env, launch_dir)
        with open(stream_path, "w", encoding="utf-8") as out_fh, open(stderr_path, "wb") as err_fh:
            try:
                proc = subprocess.Popen(argv, cwd=str(folder), env=env, stdin=subprocess.DEVNULL,
                                        stdout=subprocess.PIPE, stderr=err_fh, start_new_session=True)
            except OSError as exc:
                proc, launch_error = None, f"{type(exc).__name__}: {exc}"
            if proc is not None:
                reader = threading.Thread(target=claude_run._pump, args=(proc.stdout, out_fh, counter), daemon=True)
                reader.start()
                try:
                    exit_code = proc.wait(timeout=timeout_s)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    claude_run.kill_process_group(proc, kill_grace_s)
                    exit_code = proc.returncode
                reader.join(timeout=5.0)
                if claude_run._signal_group(proc.pid, signal.SIGTERM):   # anything the session left in its group
                    time.sleep(0.2)
                    claude_run._signal_group(proc.pid, signal.SIGKILL)
                reader.join(timeout=5.0)
                try:
                    proc.stdout.close()
                except OSError:
                    pass
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        if launch_dir is not None:
            shutil.rmtree(launch_dir, ignore_errors=True)
    ended = time.time()
    tr = transcript_mod.parse(stream_path)
    try:
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        stderr_text = ""
    if launch_error:
        stderr_text = (stderr_text + "\n" + launch_error).strip()
    last = tr.last_result or {}
    return {
        "label": label, "exit": exit_code, "timed_out": timed_out, "cost_usd": tr.cost_usd,
        "started_t": started, "ended_t": ended, "budget_hit": tr.budget_hit, "result_ok": tr.ok,
        "busy": claude_run.detect_busy(tr, stderr_text), "no_eligible": claude_run.detect_no_eligible(tr, stderr_text),
        "limited": claude_run.detect_limited(tr, stderr_text), "launch_error": launch_error,
        "text": last.get("result") if isinstance(last.get("result"), str) else "",
    }


def ask(brief: str, message: str, history=(), files=None, *, pool, out_dir, aim: str = "aim",
        budget_usd=OWNER_BUDGET_USD, timeout_s: int = OWNER_TIMEOUT_S, base_env=None, sleep=time.sleep) -> dict:
    """The owner's answer to one message: parse_reply's fields plus `status` ("ok" or "failed"), `attempts`,
    `cost_usd`, `raw` (the last reply's text) and `started_t` / `ended_t`. Account limits rerun the same call (the
    pool waits or moves on, as for the agent's sessions); a reply that does not parse is asked for again."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    system, user = system_prompt(brief), user_prompt(message, history, files)
    (out_dir / "system.md").write_text(system, encoding="utf-8")
    (out_dir / "user.md").write_text(user, encoding="utf-8")
    started = time.time()
    attempts, cost, reply, info = [], 0.0, None, {}
    for number in range(1, PARSE_RETRIES + 2):
        limited = 0
        while True:
            info = claude_run.run_session_with_accounts(
                pool, sleep=sleep, runner=run_owner_session, system=system, user=user,
                out_dir=out_dir / f"try{number}", budget_usd=budget_usd, timeout_s=timeout_s, aim=aim,
                base_env=base_env)
            if info.get("limited") and limited < LIMITED_RERUNS:
                pool.limited(info.get("label"))
                limited += 1
                continue
            break
        cost += info.get("cost_usd") or 0.0
        reply = parse_reply(info.get("text") or "")
        attempts.append({"label": info.get("label"), "status": claude_run.session_status(info),
                         "cost_usd": info.get("cost_usd"), "error": reply["error"]})
        if reply["error"] is None:
            break
    result = dict(reply, status="ok" if reply["error"] is None else "failed", attempts=attempts,
                  cost_usd=round(cost, 4), raw=info.get("text") or "", started_t=started, ended_t=time.time())
    (out_dir / "reply.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    return result
