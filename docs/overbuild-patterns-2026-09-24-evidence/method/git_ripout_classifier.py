import json, re, os, sys, random
from collections import Counter, defaultdict
import parse

D = os.path.dirname(os.path.abspath(__file__))
REPOS = parse.REPOS

# Rip-out verbs (subject or first body line)
RIP = re.compile(r"\b(remov\w*|delet\w*|rip(?:ped|s|ping)? out|drop(?:s|ped|ping)?|simplif\w*|revert\w*|retir\w*|collaps\w*|stop(?:s|ped|ping)? |no longer|instead of|get rid|gets rid|strip(?:s|ped|ping)?|prun\w*|kill\w*|eliminat\w*|unwind\w*|back(?:ed)? out|dead code|cruft|purg\w*|excis\w*|de-?scope\w*|tear(?:s)? out|tore out|undo\w*)\b", re.I)

# Noise: lint/compile/format/typo/deps/content-data
NOISE = re.compile(
    r"(unused (import|variable|dependenc|var|mut|parameter|field|lifetime|use)|\bimports?\b.*\bunused\b|clippy|compiler warning|\bwarnings?\b|\btypo\b|rustfmt|\bfmt\b|formatting|whitespace|trailing|lint\b|lints\b"
    r"|^style\b|padding|margin|merge seams?|merge conflict|\bheap alloc|perf:|^perf\b|bump|upgrade|dependabot|\bdeps?\b\(|version bump|merge branch|wip\b"
    r"|drop ?down|dropdown|drag and drop|drag-and-drop|drop[- ]?in|backdrop|drop shadow|airdrop|dropped frames?|droplet"
    r"|kill ?switch|kill-switch"
    r"|\bstrip(?:e|ed)? (?:ansi|whitespace|html|markdown|prefix|suffix|quotes|newline|emoji|tags)"
    r"|\bstop (?:loss|word)|\bstopwatch"
    r"|remove (?:the )?(?:puzzle|lesson|hand|card|image|asset|video|audio|chapter|course)s? (?:from|\d)"
    r"|delete (?:the )?(?:puzzle|lesson|chapter|course)s? \d"
    r")", re.I)

def lead(s):
    s = re.sub(r"^(revert\s+\")", "", s, flags=re.I)
    s = re.sub(r"^[\w\-/]+(\([^)]*\))?!?:\s*", "", s)  # conventional prefix
    return s

LEAD_RIP = re.compile(r"^(remov\w*|delet\w*|rip(?:ped|s|ping)? out|drop(?:s|ped|ping)?|simplif\w*|revert\w*|retir\w*|collaps\w*|stop(?:s|ped|ping)?|strip(?:s|ped|ping)?|prun\w*|kill\w*|eliminat\w*|unwind\w*|back(?:ed)? out|purg\w*|excis\w*|cut|cuts|trim\w*|clean(?:ed|s)? up|cleanup|de-?scope\w*|tear(?:s)? out|tore out|undo\w*|get rid|gets rid|shrink\w*|slim\w*|consolidat\w*|dedupe\w*|deduplicat\w*|unify|unif\w*|replace\w*|no longer|stop)\b", re.I)
ANY_RIP = re.compile(r"(\bno longer\b|\bget(?:s)? rid\b|\brip(?:ped|s|ping)? out\b|\bdead code\b|\bcruft\b|\bteardown of\b|\bdelete-first\b|, (?:remove|delete|drop|retire)\w* |\band (?:remove|delete|drop|retire|strip)\w* |; (?:remove|delete|drop|retire)\w* | — (?:remove|delete|drop|retire)\w* )", re.I)
OVERB = re.compile(r"(fallback|shim|compat|legacy|wrapper|harness|runner|controller|cache|flag|knob|env var|retry|repair|receipt|hash|proof|gate|ledger|registry|sidecar|second|duplicate|parallel|alias|side ?door|script|debug|logging)", re.I)
EXTRA_NOISE = re.compile(r"(compile|compilation|build (error|fix|break)|\bE0\d{3}\b|\btsc\b|type ?error|typecheck|borrow checker|test failure|failing build|\bci\b fix)", re.I)
STOPOBJ = re.compile(r"^stop(?:s|ped|ping)? (writing|emitting|creating|generating|persisting|logging|retrying|shelling|spawning|using|requiring|building|shipping|carrying|maintaining|recording|storing|caching|falling back|duplicating|mirroring|copying|running|launching|calling|re-?\w+ing|auto-?\w+|double|second)", re.I)

def is_candidate(c):
    subj = c["subject"]
    if NOISE.search(subj) or EXTRA_NOISE.search(subj):
        return False
    if re.match(r"^revert\s+\"?(chore|style)?:?\s*(rustfmt|fmt|format)", subj, re.I):
        return False
    if re.match(r"^revert\b", subj, re.I):
        return True
    L = lead(subj)
    m = LEAD_RIP.match(L)
    if m:
        w = m.group(1).lower()
        if w.startswith("stop"):
            return bool(STOPOBJ.match(L))
        if w.startswith("prun") and not re.match(r"^prun\w* (dead|unused|stale|old|obsolete|legacy|redundant|the |orphan|docs?|plans?|scripts?|tests?)", L, re.I):
            return False
        if w.startswith("replac") and not OVERB.search(subj):
            return False
        if w in ("unify","consolidate","consolidates","consolidated","dedupe","deduplicate","cleanup","clean up","cleaned up","cleans up") and not (OVERB.search(subj) or re.search(r"remov|delet|drop|retir", subj, re.I)):
            return False
        return True
    if ANY_RIP.search(subj):
        return True
    if re.search(r"\binstead of\b", subj, re.I) and OVERB.search(subj):
        return True
    return False

CATS = [
    ("outside-task change", r"(unrelated|out[- ]of[- ]scope|outside (the )?(task|scope)|not (part of|requested)|accidental(ly)?|stray|unintended|wasn'?t asked|scope creep|unauthori[sz]ed|without (approval|being asked)|another (agent|session)'?s)"),
    ("test sprawl", r"(\btests?\b|test[- ]?files?|test suite|\bfixtures?\b|\bspecs?\b|\be2e\b|smoke|snapshot tests?|contract tests?|test[- ]?cases?|test helpers?|test scenario|testing)"),
    ("proof ceremony", r"(sha-?256|\bexact[- ]hash|hash (gate|check|pin|receipt|manifest|verification|ceremony)|\bhashes\b(?! ?map)|checksum|receipts?|attest|\bproofs?\b|provenance|verif(y|ier|ication)|\baudit (gate|trail|step|harness|pass|stamp|artifact)s?\b|\bgates?\b|\bgated\b|gating|golden|manifest|fingerprint|signature|\bseal|evidence|certif|preflight|guard ?rails?|guardrail|parity|sentinel|ceremony|invariant|validator|validation|attestation|exact[- ]match|freshness check|stamp)"),
    ("fallback/compat path", r"(fallback|fall back|fall-back|compat|shim|legacy|backward|back-compat|migration|dual[- ]?(path|write|source|route|read)|second (path|route|source|owner|authority|copy|implementation|average)|parallel (path|route|implementation|system|copy|stack)|\balias(es)?\b|old (path|route|api|format|schema|name)|deprecated|polyfill|workaround|bridge|adapter|side ?doors?|two (paths|sources|owners|routes)|redundant (path|route|source|copy|implementation|write|read|call|lookup|fetch|guard|check)s?|\bduplicate\b|duplicated|mirror|double[- ]?write|alternate (path|route)|escape hatch|bypass)"),
    ("retry/repair machinery", r"(retr(y|ies|ying)|repair|self[- ]heal|auto[- ]?fix|recover(y|ies)?|reconcil|backoff|re-?attempt|watchdog|respawn|restart loop|\bheal|auto[- ]?resume|auto[- ]?restart|reclaim)"),
    ("diagnostics residue", r"(debug|logging|\blogs?\b|print(s|ln)?\b|\btrac(e|ing)\b|telemetry|instrument|diagnostic|console\.log|verbose|temp(orary)? (script|file|code|hack)|scratch|\bprobes?\b|breadcrumb|\bdumps?\b|eprintln|dbg!|timing output|tracer|\bspam\b|noisy|noise)"),
    ("flags/knobs/env", r"(\bflags?\b|feature[- ]flag|toggle|\bknobs?\b|env(ironment)?[- ]var|\benv\b|config(uration)? (option|key|field|surface)|\boptions?\b|--[a-z]|\bcli (arg|option|flag)s?|\bparameters?\b|\bparams?\b|opt[- ]?in|opt[- ]?out|\bmodes?\b|\bsettings?\b|tuning surface|\bswitch(es)?\b)"),
    ("extra state", r"(\bcache[sd]?\b|caching|persist|state file|registry|ledger|sidecar|database|\btables?\b|columns?|index file|\bstore\b|storage|\bqueue\b|lock ?file|marker|metadata|journal|checkpoint|memo(ize)?|snapshot|\bstate\b|stateful|history file|bookkeeping)"),
    ("abstraction/wrapper/controller", r"(wrapper|abstraction layer|controller|harness|runner|orchestrat|framework|\blayer\b|indirection|facade|manager\b|factory|helper|plugin|daemon|supervisor|dispatcher|router|pipeline|coordinator|scaffold|boilerplate|generic|interface|\btraits?\b|middleware|\bservice\b|\bextension\b|\bscripts?\b|tooling|\bcli\b|\bcommand\b|subcommand|\bmcp\b|\bskill\b|workflow|\bloop\b|automation|agent)"),
    ("unrequested feature", r"(unrequested|not needed|unneeded|unnecessary|speculative|premature|over-?engineer|overbuil|nobody (uses|asked)|yagni|gold[- ]plat|nice-to-have|not asked)"),
]
CATS_C = [(n, re.compile(p, re.I)) for n, p in CATS]
OTHER_SUB = [
    ("other: dead/stale/unused code", re.compile(r"(unused|dead|unreachable|orphan|stale|obsolete|superseded|no longer (used|needed)|cruft|leftover|old\b|outdated|vestigial)", re.I)),
    ("other: docs/plans", re.compile(r"(\bdocs?\b|readme|plan(s|\.md)?\b|writeup|write-up|\.md\b|notes?\b|documentation|runbook|report)", re.I)),
    ("other: revert", re.compile(r"^revert", re.I)),
]

DOCS_FIRST = re.compile(r"(\bnotes\b|^docs?(\(|:)|\.md\b|\bdocs?\b|readme|\bplans?\b|writeup|write-up|runbook|documentation|agents\.md|claude\.md|skill\.md)", re.I)
def classify(c):
    subj = c["subject"]
    if DOCS_FIRST.search(subj) and not re.search(r"(fallback|shim|harness|receipt|hash|flag|retry|cache)", subj, re.I):
        return "other: docs/plans"
    for name, rx in CATS_C:
        if rx.search(subj):
            return name
    for name, rx in OTHER_SUB:
        if rx.search(subj):
            return name
    body = "\n".join(c["body"].splitlines()[:4])
    for name, rx in CATS_C:
        if name in ("abstraction/wrapper/controller", "test sprawl"):
            continue
        if rx.search(body):
            return name
    return "other: product/behavior"

def dedupe(cs):
    seen = set(); out = []
    for c in cs:
        k = (c["repo"], c["subject"], c["ins"], c["dele"])
        if k in seen:
            continue
        seen.add(k); out.append(c)
    return out

def load():
    allc = []
    for r in REPOS:
        cs = parse.parse(r)
        allc.extend(cs)
    return allc


def authors():
    A = {}
    for r in REPOS:
        for line in open(os.path.join(D, r + ".authors"), encoding="utf-8", errors="replace"):
            sha, _, a = line.rstrip("\n").partition("\t")
            A[sha] = a
    return A

def is_amir_or_agent(a):
    if re.search(r"(dependabot|github-actions|sentry\[bot\]|copilot|justin|natasha|blake|nickfang|mario|zechner|seth|kevin|kt <|sebastian|markus|andrew|joey|release-bot)", a, re.I):
        return False
    return bool(re.search(r"(elaguiz|amir|agent|claude|codex|coder|bot|lane|aider|@local|fun\.country|funcountry|mw-|metaopt|astra)", a, re.I))

if __name__ == "__main__":
    A = authors()
    allc = load()
    shas = set(); u = []
    for c in allc:
        if c["sha"] in shas: continue
        shas.add(c["sha"]); c["author"] = A.get(c["sha"], "?"); u.append(c)
    # repo totals (Amir/agent authored) from author maps
    tot = Counter()
    for r in REPOS:
        for line in open(os.path.join(D, r + ".authors"), encoding="utf-8", errors="replace"):
            if is_amir_or_agent(line.split("\t",1)[1]): tot[r] += 1
    u = [c for c in u if is_amir_or_agent(c["author"])]
    dd = dedupe(u)
    cand = [c for c in dd if is_candidate(c)]
    for c in cand:
        c["cat"] = classify(c)
        c["net"] = c["dele"] - c["ins"]
    print("Amir/agent commits by repo:", dict(tot), sum(tot.values()))
    print("candidates:", len(cand), dict(Counter(c["repo"] for c in cand)))
    print(Counter(c["cat"] for c in cand).most_common())
    json.dump(cand, open(os.path.join(D, "cand.json"), "w"))
