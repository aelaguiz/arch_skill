import json, re, collections, sys
S=sys.argv[1]
strong = re.compile(r"(overbuil|over-buil|over ?-?engineer|overkill|over-?complicat|bloat|cruft|ceremony|machinery|scope creep|gold.?plat|yagni|unnecessary|not needed|(?:we|you) don'?t need|do we (?:even |actually |really )?need|(?:didn'?t|did not|never) ask|nobody asked|no one asked|rip(?:ping)? (?:it |this |that |all |them |these |)out|tear (?:it |this |)out|get rid of|strip (?:out|it|this)|delete (?:it|that|this|all|every)|simplif|simpler|simplest|keep it simple|speculative|hypothetical|dual path|parallel (?:path|implementation|system)|second (?:path|copy|owner|system)|shim|fallback|fall back|backward.?compat|back-?compat|why (?:the fuck |the hell )?(?:are|did|would|do) you|why (?:is|are) there|what (?:the fuck )?is (?:all )?this|what'?s all this|too (?:complex|complicated|much)|moving parts|less code|fewer (?:lines|files)|just in case|future.?proof|defensive|self.?heal|retr(?:y|ies)|feature flag|knob|toggle|state machine|wrapper|indirection|layer of)", re.I)
template = re.compile(r"^(# /prompts:|Execution rule:|You are an externally delegated|You own |You are a |<|\$?arch-|/prompts:)", re.I)
A=[];T=[]
for l in open(f"{S}/candidates.jsonl"):
    d=json.loads(l); t=d["text"]
    hits=sorted(set(m.lower() for m in strong.findall(t)))
    if not hits: continue
    d["strong"]=hits
    (T if template.match(t.strip()) else A).append(d)
print("strong typed", len(A), "templated", len(T))
b=collections.Counter()
for d in A:
    n=len(d["text"]); b["<300" if n<300 else "<1000" if n<1000 else "<3000" if n<3000 else ">=3000"]+=1
print(b)
print(collections.Counter(d["machine"]+"/"+d["runtime"] for d in A))
json.dump(A, open(f"{S}/tierA.json","w")); json.dump(T, open(f"{S}/templated.json","w"))
