import json,re,sys
from collections import Counter,defaultdict
d=json.load(open('templated.json'))
R=[
("R01 No runtime fallbacks/shims; work correctly or fail loud",
 r"no (?:silent |runtime )?fallbacks|NO fallbacks or runtime shims|No fallbacks ?/ ?runtime shims|fallback_policy|do NOT add runtime fallbacks|no-fallback policy|fallbacks?/(?:runtime )?shims"),
("R02 Fallback only with explicit approval (fallback_policy: approved + timebox + removal plan)",
 r"fallback_policy: approved"),
("R03 No 'make it feel unbroken' paths: swallowed errors, stale-cache defaults, try-old-API, placeholder behavior",
 r"feel unbroken|swallowing errors|best effort.{0,3} paths|try old API|placeholder behavior|placeholder values"),
("R04 Single source of truth; no parallel paths/implementations/writers",
 r"no (?:competing|dual|parallel) (?:sources? of truth|paths?|implementations?|writers)|avoid parallel (?:implementations|paths)|anti-parallel-paths|delete/avoid parallel|no parallel paths|remove parallel solutions|SSOT is real|prevent parallel truth|parallel sources of truth|danger: parallel path"),
("R05 Delete old/legacy paths (delete list; hard cutover, no compat shims)",
 r"Delete list|delete old path|hard cutover|Old paths are deleted|legacy shims|what must be deleted|delete legacy paths|Deletes / cleanup"),
("R06 No new bespoke harnesses/frameworks/scripts/DSLs; prefer existing checks",
 r"bespoke (?:screenshot )?harness|invent new harnesses|harnesses/DSLs|drift scripts|avoid adding new harnesses|no harness|do not waste time building permanent gates or frameworks"),
("R07 Smallest credible signal; 1-3 checks; no verification bureaucracy/proof ladders",
 r"verification bureaucracy|proof ladders?|smallest (?:credible|existing|relevant) (?:acceptance )?(?:signal|check)|1[-–]3 checks|keep it minimal; prefer existing"),
("R08 No negative-value 'proof' tests (deleted-code refs, visual constants/goldens, doc-inventory gates, mock-only, timing hacks)",
 r"negative-value|\"proof\" tests|“proof” tests|deleted code not referenced|deleted code isn.t referenced|visual[- ]constant|doc-driven (?:inventory )?gates|mock-only"),
("R09 Default: add no new tests if typecheck/lint + existing checks suffice",
 r"do NOT add new tests|Write tests only when they buy|tests optional|add only minimal tests"),
("R10 Manual QA/screenshots/sim are non-blocking follow-ups, never gates",
 r"don.t gate implementation|do not gate mid-implementation|Manual QA \(non-blocking\)|non-blocking follow-ups|Do NOT require screenshots|not a gating criterion|Do not block the entire plan on flaky|screenshot proof burdens|Defer manual verification"),
("R11 Do not expand scope; out-of-scope ideas become deferred follow-ups",
 r"do not scope creep|do NOT expand scope|expands scope: default to defer|does not silently expand|avoid scope creep|Do not introduce new scope|out-of-scope for this PR|default to follow-up/ignore|meaningfully expands work"),
("R12 Reuse repo patterns; no unnecessary new abstractions/frameworks",
 r"no unnecessary new abstractions|avoids? inventing new frameworks|do not add new abstractions|Reuses existing repo patterns|inventing new frameworks|new generators/frameworks"),
("R13 No second plan/checklist/ledger; keep tracking out of ceremony",
 r"second plan doc|second execution checklist|do not turn this into ceremony|not ceremony|no ceremony"),
("R14 Keep phase plan short (1-2 phases); no sprawling proof ladders",
 r"default 1-2 phases|sprawling proof ladders"),
("R15 Run only the smallest relevant tests, not the full suite/CI matrix",
 r"avoid the full suite|full CI matrix|don.t run the full suite|relevant only\)|avoid re-running suites|avoid building everything"),
("R16 Flags/gradual rollout only if needed; avoid long-lived dual paths; rollback over runtime shims",
 r"avoid long-lived dual paths|preferred over runtime shims"),
("R17 No dev gates/flags/config/env vars during debugging; remove diagnostics after",
 r"Avoid adding dev gates|remove diagnostics|revert temporary cuts|Avoid hot-loop logs"),
("R18 Delete or rewrite a blocking negative-value test instead of bending code to it",
 r"prefer deleting (?:it|or rewriting)|instead of .fixing. code to satisf"),
("R19 Stage/touch only your own files; ignore unrelated dirty files (no collateral edits)",
 r"stage only (?:files you touched|what you touched|what you touched)|Do not revert unfamiliar changes|avoid collateral damage|write only the assigned"),
("R20 Avoid research sprawl / cargo-cult best practice",
 r"research sprawl|cargo-cult"),
("R21 Keep fixes minimal and localized",
 r"keep changes minimal/targeted|minimal and localized|Proposed fix \(minimal\)|minimal fix that removes the cause|minimal, surgical edits"),
("R22 Reject bug vectors: coverage gates, remote runners, generators (overbuild-protector)",
 r"Coverage gates|remote runner"),
("R23 Shared env: avoid commands that generate/overwrite artifacts in read-only passes",
 r"avoid commands that generate/overwrite"),
]
cnt=Counter(); ex={}; tmpl=defaultdict(Counter); dates=defaultdict(list)
for x in d:
    t=x['text']
    name=t.split()[1].split('—')[0] if t.startswith('# /prompts:') else 'other'
    for rid,pat in R:
        m=re.search(pat,t,re.I)
        if m:
            cnt[rid]+=1; tmpl[rid][name]+=1; dates[rid].append(x['ts'][:10])
            if rid not in ex:
                # line containing match
                s=t.rfind('\n',0,m.start())+1; e=t.find('\n',m.end()); e=len(t) if e<0 else e
                ex[rid]=t[s:e].strip()[:300]
for rid,_ in R:
    ds=sorted(dates[rid])
    print(f"{cnt[rid]:4d} {rid}  [{ds[0] if ds else ''}..{ds[-1] if ds else ''}]")
    print("     tmpl:",dict(tmpl[rid].most_common(4)))
    print("     ex:",ex.get(rid))

print("\n\n=== matched-line variants ===")
for rid,pat in R:
    lc=Counter()
    for x in d:
        t=x['text']; seen=set()
        for m in re.finditer(pat,t,re.I):
            s=t.rfind('\n',0,m.start())+1; e=t.find('\n',m.end()); e=len(t) if e<0 else e
            ln=re.sub(r'\s+',' ',t[s:e].strip())[:200]
            if ln not in seen: seen.add(ln); lc[ln]+=1
    print(rid)
    for k,v in lc.most_common(4): print('   ',v,'|',k)
