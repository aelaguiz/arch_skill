import json, glob, collections, sys, re
S = sys.argv[1]
A = json.load(open(f"{S}/tierA.json")); A.sort(key=lambda d: (d["ts"] or ""))
meta = {f"p{i:05d}": d for i, d in enumerate(A)}
for l in open(f"{S}/batches/batch9.jsonl"):
    r = json.loads(l); meta[r["id"]] = {"machine": r["m"], "runtime": r["rt"], "ts": r["date"], "cwd": r["cwd"], "session": None}
MAP = {
 "new-speculative-fix-residue":"guess-fix-hack","new-speculative-fix":"guess-fix-hack","new-symptom-patching":"guess-fix-hack",
 "new-hack-not-rootfix":"guess-fix-hack","new-eval-gaming":"guess-fix-hack",
 "new-dead-cruft":"dead-code-kept","new-dead-code":"dead-code-kept","new-archive-instead-of-delete":"dead-code-kept",
 "new-delete-not-contain":"dead-code-kept","new-comment-residue":"dead-code-kept",
 "new-avoid-interface-change":"compat-dual-path",
 "new-rewrite-over-reuse":"reinvent-existing","new-reinvent-existing":"reinvent-existing","new-reinvent-native":"reinvent-existing",
 "new-code-over-agent-judgment":"code-over-judgment",
 "new-off-spec-additions":"invented-rules","new-invented-rules":"invented-rules",
 "new-premature-action":"unrequested-scope","new-forced-determinism":"proof-ceremony",
 "new-heavyweight-entry-point":"process-overhead","new-test-hooks-in-prod":"test-sprawl",
 "new-overprescriptive":"doc-prompt-bloat","new-jargon-coinage":"doc-prompt-bloat",
}
labels=[]
for f in sorted(glob.glob(f"{S}/labels/*.labels.jsonl")):
    for l in open(f):
        l=l.strip()
        if l:
            d=json.loads(l); d["_b"]=f.split("/")[-1].split(".")[0]; labels.append(d)
flag=[d for d in labels if d.get("verdict") in ("yes","partial")]
# dedupe re-sent prompts by normalized quote
seenq=set(); ded=[]
for d in flag:
    q=re.sub(r"\W+"," ",(d.get("quote") or "").lower()).strip()
    if q and q in seenq: continue
    seenq.add(q); ded.append(d)
def cats(d):
    c=d.get("cats") or []
    c=[c] if isinstance(c,str) else c
    out=[]
    for x in c:
        x=MAP.get(x,x)
        if x.startswith("new-") and x!="new-abstraction": x="other"
        if x not in out: out.append(x)
    return out
unk=collections.Counter(x for d in flag for x in (d.get("cats") or []) if x.startswith("new-") and x not in MAP and x!="new-abstraction")
print("unmapped new-:",dict(unk))
print("flagged",len(flag),"deduped",len(ded), "yes", sum(d["verdict"]=="yes" for d in ded))
cc=collections.Counter(); cy=collections.Counter(); ct=collections.defaultdict(collections.Counter); cm=collections.defaultdict(collections.Counter)
sess=collections.defaultdict(set); half=collections.defaultdict(collections.Counter)
for d in ded:
    m=meta.get(d["id"],{})
    ym=(m.get("ts") or "")[:7]
    h="H1 (to 2026-01)" if ym<"2026-02" else "H2 (2026-02 on)"
    for c in cats(d):
        cc[c]+=1; cy[c]+= d["verdict"]=="yes"; ct[c][d.get("target","unclear")]+=1; cm[c][d.get("mode")]+=1
        if m.get("session"): sess[c].add(m["session"])
        half[c][h]+=1
N=len(ded)
print(f"\n{'category':24s} {'n':>5s} {'%':>5s} {'yes':>4s} {'sess':>4s} | plan impl prompt proc | react preempt audit | early late")
for c,n in cc.most_common():
    t=ct[c]; mo=cm[c]
    print(f"{c:24s} {n:5d} {100*n/N:5.1f} {cy[c]:4d} {len(sess[c]):4d} | {t['plan']:4d} {t['impl']:4d} {t['prompt']:6d} {t['process']:4d} | {mo['reactive']:5d} {mo['preemptive']:7d} {mo['audit-request']:5d} | {half[c]['H1 (to 2026-01)']:5d} {half[c]['H2 (2026-02 on)']:4d}")
tg=collections.Counter(d.get("target") for d in ded); md=collections.Counter(d.get("mode") for d in ded)
print("\ntarget",dict(tg)); print("mode",dict(md))
mon=collections.Counter((meta.get(d["id"],{}).get("ts") or "")[:7] for d in ded)
print("month",sorted(mon.items()))
mach=collections.Counter(f'{meta.get(d["id"],{}).get("machine")}/{meta.get(d["id"],{}).get("runtime")}' for d in ded); print("machine",dict(mach))
repo=collections.Counter((meta.get(d["id"],{}).get("cwd") or "").split("/")[-1] or "(no cwd)" for d in ded); print("repo",repo.most_common(15))
# multi-category co-occurrence
co=collections.Counter()
for d in ded:
    cs=sorted(cats(d))
    for i in range(len(cs)):
        for j in range(i+1,len(cs)): co[(cs[i],cs[j])]+=1
print("cooccur",co.most_common(10))
json.dump([dict(d,cats2=cats(d),date=(meta.get(d["id"],{}).get("ts") or "")[:10],machine=meta.get(d["id"],{}).get("machine"),runtime=meta.get(d["id"],{}).get("runtime"),session=meta.get(d["id"],{}).get("session"),repo=(meta.get(d["id"],{}).get("cwd") or "").split("/")[-1]) for d in ded],open(f"{S}/flagged_dedup.json","w"))
