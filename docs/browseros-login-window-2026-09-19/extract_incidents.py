import json,re,sys,os,collections
S=os.path.dirname(os.path.abspath(__file__))
WIN=re.compile(r"wrong (browser )?window|wrong profile|other window|another window|different window|popped (up|open)|pops? (up|open) in|opened in the wrong|focused window|whatever window|window (that )?has focus|wrong tab|wrong browser",re.I)
BLOCK=re.compile(r"can'?t log ?in|cannot log ?in|not logged in|login wall|login gate|log in first|sign in first|need you to log ?in|please log ?in|log in manually|sign in manually|requires (you to )?log ?in|login required|asks? (me )?to (log|sign) ?in|logged out|sign[- ]in page|login page|login screen|sign-in screen|blocked (by|on) (a )?(login|sign)",re.I)
AUTHLINK=re.compile(r"oauth|\bsso\b|login link|sign.?in link|device.?code|sign in with google|continue with google|auth login|gh auth|gcloud auth|vercel login|firebase login|supabase login|wrangler login|open (this|the) (url|link)|open the following|visit (this|the) (url|link)|xdg-open|\bopen https?://",re.I)
INJECT=re.compile(r"^\s*(<skill>|# AGENTS\.md|<INSTRUCTIONS>|<environment_context>|<permissions|<system-reminder|<command-name|<local-command)")
def texts_codex(o):
    if o.get('type')!='response_item': return
    p=o.get('payload',{})
    if p.get('type')=='message':
        role=p.get('role'); t='\n'.join(c.get('text','') for c in (p.get('content') or []) if isinstance(c,dict))
        yield role,t
def texts_claude(o):
    t=o.get('type')
    if t not in ('user','assistant'): return
    m=o.get('message') or {}
    c=m.get('content')
    if isinstance(c,str): yield t,c
    elif isinstance(c,list):
        for b in c:
            if isinstance(b,dict) and b.get('type')=='text': yield t,b.get('text','')
def texts_prime(o):
    if o.get('type')!='message': return
    m=o.get('message') or o
    role=m.get('role') or o.get('role')
    c=m.get('content')
    if isinstance(c,str): yield role,c
    elif isinstance(c,list):
        for b in c:
            if isinstance(b,dict) and b.get('type')=='text': yield role,b.get('text','')
def scan(files,runtime,parser,out):
    n=0
    for F in files:
        F=F.strip()
        if not F or not F.endswith('.jsonl'): continue
        try: fh=open(F,errors='ignore')
        except Exception: continue
        for i,line in enumerate(fh):
            if not (WIN.search(line) or BLOCK.search(line) or AUTHLINK.search(line)): continue
            try:o=json.loads(line)
            except: continue
            ts=o.get('timestamp','')
            for role,t in parser(o) or []:
                if not t or INJECT.match(t): continue
                if len(t)>20000: continue  # injected docs
                kinds=[]
                if WIN.search(t): kinds.append('window')
                if BLOCK.search(t): kinds.append('block')
                if AUTHLINK.search(t): kinds.append('authlink')
                if not kinds: continue
                # user messages: any kind; assistant: only block/window/authlink with short text (claims), skip huge
                if role not in ('user','assistant'): continue
                if role=='assistant' and len(t)>6000: continue
                m=(WIN.search(t) or BLOCK.search(t) or AUTHLINK.search(t))
                a=max(0,m.start()-400); b=min(len(t),m.end()+400)
                out.write(json.dumps({'runtime':runtime,'file':F,'line':i,'ts':ts,'role':role,'kinds':kinds,'snippet':t[a:b]})+'\n'); n+=1
    return n
def main():
    codex=set(open(S+'/codex_files_win.txt').read().split('\n'))|set(open(S+'/codex_files_block.txt').read().split('\n'))
    claude=set(open(S+'/claude_files_win.txt').read().split('\n'))|set(open(S+'/claude_files_block.txt').read().split('\n'))
    prime=[l for l in open(S+'/prime_pi_files.txt').read().split('\n') if '/sessions/' in l]
    with open(S+'/incidents.jsonl','w') as out:
        print('codex',scan(sorted(codex),'codex',texts_codex,out),flush=True)
        print('claude',scan(sorted(claude),'claude',texts_claude,out),flush=True)
        print('prime',scan(sorted(prime),'prime',texts_prime,out),flush=True)
main()
