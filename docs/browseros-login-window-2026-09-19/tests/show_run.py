import json,sys,os,re
R=sys.argv[1]
print('=====',os.path.basename(R)); print(open(R+'/meta.txt').read().strip())
reads=[]; tools=[]
for l in open(R+'/events.jsonl',errors='ignore'):
    try:o=json.loads(l)
    except: continue
    # codex
    if o.get('type')=='item.completed':
        it=o.get('item',{})
        if it.get('type') in ('command_execution',):
            c=it.get('command',''); tools.append('sh: '+c[:160])
            for m in re.findall(r'[^\s"\']*browseros[^\s"\']*',c): reads.append(m)
        elif it.get('type')=='mcp_tool_call': tools.append('mcp: '+json.dumps(it.get('arguments'))[:160])
    # claude
    if o.get('type')=='assistant':
        for b in (o.get('message',{}).get('content') or []):
            if isinstance(b,dict) and b.get('type')=='tool_use':
                inp=b.get('input',{}); s=json.dumps(inp)
                tools.append(b.get('name','')+': '+s[:160])
                for m in re.findall(r'[^\s"\']*browseros[^\s"\']*',s): reads.append(m)
print('-- skill files touched:'); 
for r in sorted(set(reads)): print('  ',r)
print('-- tool calls:',len(tools))
for t in tools[:25]: print('  ',t)
print('-- final:'); print(open(R+'/final.txt').read() if os.path.exists(R+'/final.txt') else '(no final.txt)')
