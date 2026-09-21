#!/bin/zsh
# usage: wave.sh <codex|claude> "<SC> <RUN> <LABEL>" ...
W=/private/tmp/claude-501/-Users-aelaguiz-workspace-arch-skill/e7e26c09-d590-4d1e-a230-d643740616bd/scratchpad/tests
RT=$1; shift
pids=()
for spec in "$@"; do
  parts=(${=spec})
  $W/run_one.sh $RT ${parts[3]} ${parts[1]} ${parts[2]} > /dev/null 2>&1 &
  pids+=($!)
done
wait
for d in $W/runs/${RT}-*; do echo "$(basename $d): $(tail -2 $d/meta.txt | tr '\n' ' ')"; done
