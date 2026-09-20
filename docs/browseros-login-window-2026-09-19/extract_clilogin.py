import json,re,os,sys
S=os.path.dirname(os.path.abspath(__file__))
CLI=re.compile(r'gh auth login|gcloud auth (application-default )?login|vercel login|firebase login|supabase login|wrangler login|stripe login|az login|aws sso login|--no-launch-browser|--no-browser|--device-code|[Dd]evice code',re.I)
CTX=re.compile(r'browser|window|profile|opened|open the|open this|visit|paste|code|log ?in|sign ?in|BrowserOS|newPage|default browser',re.I)
def codex_iter(F):
    for i,line in enumerate(open(F,errors='ignore')):
        try:o=json.loads(line)
        except: continue
        if o.get('type')!='response_item': continue
        p=o.get('payload',{}); pt=p.get('type'); ts=o.get('timestamp','')
        if pt in ('function_call','custom_tool_call'):
            args=p.get('arguments') or p.get('input') or ''
            if isinstance(args,dict): args=json.dumps(args)
            yield i,ts,'call',p.get('name'),str(args)
        elif pt=='message':
            yield i,ts,'msg',p.get('role'),'\n'.join(c.get('text','') for c in (p.get('content') or []) if isinstance(c,dict))
        elif pt in ('function_call_output','custom_tool_call_output'):
            out=p.get('output'); 
            if isinstance(out,dict): out=json.dumps(out)
            yield i,ts,'out','', str(out)
def claude_iter(F):
    for i,line in enumerate(open(F,errors='ignore')):
        try:o=json.loads(line)
        except: continue
        t=o.get('type'); ts=o.get('timestamp','')
        if t=='message' and isinstance(o.get('message'),dict):  # prime
            m=o['message']; role=m.get('role'); c=m.get('content')
            if isinstance(c,str): yield i,ts,'msg',role,c
            elif isinstance(c,list):
                for b in c:
                    if not isinstance(b,dict): continue
                    if b.get('type')=='text': yield i,ts,'msg',role,b.get('text','')
                    elif b.get('type')=='toolCall': yield i,ts,'call',b.get('name'),json.dumps(b.get('arguments'))
                    elif b.get('type')=='tool_result' or role=='toolResult': yield i,ts,'out','',json.dumps(b)[:5000]
        elif t in ('user','assistant'):
            m=o.get('message') or {}; c=m.get('content')
            if isinstance(c,str): yield i,ts,'msg',t,c
            elif isinstance(c,list):
                for b in c:
                    if not isinstance(b,dict): continue
                    if b.get('type')=='text': yield i,ts,'msg',t,b.get('text','')
                    elif b.get('type')=='tool_use': yield i,ts,'call',b.get('name'),json.dumps(b.get('input'))
                    elif b.get('type')=='tool_result':
                        cc=b.get('content'); 
                        if isinstance(cc,list): cc=' '.join(x.get('text','') for x in cc if isinstance(x,dict))
                        yield i,ts,'out','',str(cc)[:5000]
def scan(files,runtime,it,out):
    n=0
    for F in files:
        F=F.strip()
        if not F.endswith('.jsonl') or '/sessions/' not in F and 'projects' not in F: continue
        recs=list(it(F)) if os.path.getsize(F)<400_000_000 else []
        hits=[k for k,(i,ts,kind,who,txt) in enumerate(recs) if kind=='call' and CLI.search(txt) and len(txt)<20000]
        if not hits: continue
        for k in hits[:5]:
            i,ts,kind,who,txt=recs[k]
            m=CLI.search(txt); a=max(0,m.start()-300)
            ctx=[]
            for j in range(max(0,k-1),min(len(recs),k+12)):
                ii,tts,kk,ww,tt=recs[j]
                if kk=='msg' and CTX.search(tt) and not tt.startswith('<'): ctx.append((ii,ww,tt[:500]))
                if kk=='out' and re.search(r'https?://[^\s"\\]*(auth|login|oauth|device|verify)[^\s"\\]*',tt): 
                    mm=re.search(r'https?://[^\s"\\]*(auth|login|oauth|device|verify)[^\s"\\]*',tt); ctx.append((ii,'OUT-URL',mm.group(0)[:160]))
            out.write(json.dumps({'runtime':runtime,'file':F,'line':i,'ts':ts,'tool':who,'cmd':txt[a:m.end()+200],'context':ctx[:8]})+'\n'); n+=1
    return n
codex=open(S+'/codex_files_clilogin.txt').read().split('\n')
cp=open(S+'/claude_prime_files_clilogin.txt').read().split('\n')
with open(S+'/clilogin.jsonl','w') as out:
    print('codex',scan(codex,'codex',codex_iter,out),flush=True)
    print('claude/prime',scan(cp,'claude',claude_iter,out),flush=True)
