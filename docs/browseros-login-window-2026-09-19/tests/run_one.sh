#!/bin/zsh
# usage: run_one.sh <codex|claude> <label> <scenario> <runno>
set -u
RT=$1; LABEL=$2; SC=$3; RUN=$4
W=/private/tmp/claude-501/-Users-aelaguiz-workspace-arch-skill/e7e26c09-d590-4d1e-a230-d643740616bd/scratchpad/tests
R=$W/runs/${RT}-${SC}-r${RUN}; mkdir -p $R
if [ "$RT" = "codex" ]; then
  SKILLPATH=/Users/aelaguiz/.agents/skills/browseros/SKILL.md
else
  SKILLPATH=/Users/aelaguiz/.claude/skills/browseros/SKILL.md
fi
sed "s#SKILLPATH#$SKILLPATH#" $W/prompts/$SC.md > $R/prompt.md
echo "$(date -u +%FT%TZ) start $RT $LABEL $SC r$RUN" > $R/meta.txt
cd $W/work
if [ "$RT" = "codex" ]; then
  aim codex run $LABEL -- exec --disable codex_hooks -s read-only --skip-git-repo-check \
    --model gpt-5.6-sol -c 'model_reasoning_effort="high"' -c 'mcp_servers={}' \
    --json -o $R/final.txt < $R/prompt.md > $R/events.jsonl 2> $R/stderr.log
  echo "exit=$?" >> $R/meta.txt
else
  aim claude run $LABEL -- -p --model claude-opus-5 --effort high \
    --output-format stream-json --verbose --settings '{"disableAllHooks":true}' \
    --strict-mcp-config --mcp-config $W/empty-mcp.json --allowedTools "Read,Glob,Grep" \
    < $R/prompt.md > $R/events.jsonl 2> $R/stderr.log
  echo "exit=$?" >> $R/meta.txt
  python3 - "$R" <<'PY'
import json,sys
R=sys.argv[1]; res=None
for l in open(R+'/events.jsonl'):
    try:o=json.loads(l)
    except: continue
    if o.get('type')=='result': res=o
if res: open(R+'/final.txt','w').write(res.get('result') or '')
PY
fi
echo "$(date -u +%FT%TZ) end" >> $R/meta.txt
