import json, re, sys, glob, hashlib, collections
S = sys.argv[1]
pat = re.compile(r"""(overbuil|over-buil|over ?engineer|over-?complicat|overcomplicat|overkill|too (?:complex|complicated|much (?:code|machinery|stuff|ceremony))|simplif|simpler|simplest|bloat|cruft|ceremony|machinery|gold.?plat|yagni|scope creep|rip (?:it |this |that |all |)out|rip out|tear (?:it |this |)out|delete (?:all|every|the|this|that|it)|get rid of|strip (?:out|it|this)|(?:didn'?t|did not|never) ask(?:ed)? (?:for|you)|nobody asked|no one asked|who asked|why (?:the fuck |the hell )?(?:do|did|would|are|is) (?:we|you|there|it|this)|why (?:is|are) (?:there|this|these)|what is (?:all )?this|do we (?:even |actually |really )?need|we don'?t need|you don'?t need|not needed|unnecessary|fallback|fall back|shim|backward.?compat|back-?compat|legacy path|dual path|two paths|second (?:path|copy|owner|system)|parallel (?:path|system|implementation)|wrapper|abstraction|indirection|framework|harness|controller|state machine|registry|heuristic|defensive|guard(?:s|rail)|retr(?:y|ies)|backoff|self-?heal|repair (?:pass|loop|job)|config(?:urable|uration) (?:knob|option|flag)|knob|feature flag|toggle|minimal|smallest|just (?:do|use|make|call|read)|keep it simple|less code|fewer (?:lines|files|moving)|moving parts|speculative|future-?proof|hypothetical|edge case|in case|just in case|ripping|cleanup|clean up|delete-first|deletion)""", re.I)
seen = set(); out = []; counts = collections.Counter()
for f in sorted(glob.glob(f"{S}/corpus/*.jsonl")):
    for l in open(f):
        d = json.loads(l)
        t = d["text"] or ""
        if len(t) < 15: continue
        k = hashlib.sha1(t[:2000].encode()).hexdigest()
        if k in seen: continue
        seen.add(k)
        counts["unique"] += 1
        m = pat.findall(t)
        if m:
            d["hits"] = sorted(set(x.lower() for x in m))
            out.append(d)
print(counts, "candidates", len(out), file=sys.stderr)
with open(f"{S}/candidates.jsonl", "w") as w:
    for d in out: w.write(json.dumps(d) + "\n")
c = collections.Counter(h for d in out for h in d["hits"])
for k, v in c.most_common(80): print(v, k)
