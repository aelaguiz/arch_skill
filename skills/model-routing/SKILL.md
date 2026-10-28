---
name: model-routing
description: "Choose the model and thinking level for a helper before you start it: a subagent, a `claude -p` or `codex exec` run, or a worker a skill or script launches. Teaches which helper work can run on the same strong model at a lower thinking level and finish in a fraction of the time with as good an answer (research from sources, data analysis, labeling by a codebook, explaining code, problems with one right answer, checking work against a brief, judging against a stated standard), and why, so you can place tasks it does not name. Use when you are about to hand work to a helper and must set its model or effort, or when asked which model or thinking level fits a kind of task. Not for whether or how to delegate (agent-delegate and the shared orchestration policy), the model of a top-level session, or which model an application's code should call."
metadata:
  short-description: "Pick a helper's model and thinking level"
---

# Model Routing

When you hand work to a helper, you choose its model and how hard it thinks. The goal is the answer you can act on, as soon as possible. Speed here is wall-clock time until you have that answer, not tokens or money. A fast wrong answer is slower than a slow right one, because you act on it or redo it.

## What a thinking level buys

A higher thinking level does not make a model write faster. It makes it do more before it answers: check everything the brief asks for, find a way around an obstacle, keep many rules in mind at once. That costs minutes, and whether the minutes buy anything depends on where the answer's value comes from.

When the material you hand the helper carries the answer (the sources, the data, the codebook, the code, the standard to judge against) and you will read and check what comes back, the extra work adds time and not quality, and the same model at a lower level reaches as good an answer in well under the time. Coding a batch of short videos by a codebook, medium took 3 minutes against 18 and scored higher. Asked who set up an account and what state it was in, the top level came back confidently wrong after 25 minutes; medium found the meeting notes that answered it.

When the value is in what the helper notices that nobody pointed it at, the thinking is the job. Rewriting a batch of quiz questions, the top level fixed the one question whose correct answer was marked wrong; medium answered "nothing to fix" in under a minute. A short task can be like this too: translating twelve strings under a glossary, a width limit and a check script, medium translated as well but skipped measuring the width and running the check. A fast answer that looks finished and isn't costs more than the minutes it saved.

## Lower the level, not the model

Step down by keeping the strong model and lowering its thinking: Opus at medium, or on Codex, Sol at high. Do not step down by moving to a smaller model. Sonnet and Haiku, and Opus at its lowest level, drop rules of the brief and miss the point: a read-only review on Sonnet found the real defects and then wrote files anyway. Sonnet has no room to step down at all; at medium it does markedly worse than Sonnet at max.

## Examples

Each row is a different kind of helper task where the step down holds. They are examples of the idea above, so a task that is plainly one of these under another name gets the same step down.

| Kind of task | For example | Use | Why the lower level is enough |
|---|---|---|---|
| Research a question from documents, email or the web | "Find out who set up this account and what state it is in" | Opus at medium; on Codex, Sol at high | The sources hold the answer, and you read what comes back with its sources |
| Analyze a dataset and say what it shows | "How did last week's sign-ups compare with the week before?" | Opus at medium; on Codex, Sol at high | The numbers decide it, and the query can be rerun |
| Label items, or pull fields out of them, by a codebook | "Tag these 40 support tickets with the categories in this list" | Opus at medium; on Codex, Sol at high | The codebook carries the judgment; the job is applying it the same way every time |
| Explain how some code behaves, or why something broke | "Which file decides when this request is retried?" | Opus at medium; on Codex, Sol at high | The code is the answer key, and file and line references can be checked |
| Work out a problem that has one right answer | "Which of these three moves is correct, and why?" | Opus at medium; on Codex, Sol at high | A right answer exists and can be checked; more thinking re-derives what medium finds |
| Check another agent's work against its brief | "Is this session still doing what it was asked to do?" | Opus at medium; on Codex, Sol at high | The brief is the standard; the helper compares rather than invents |
| Judge images, frames or writing against a stated standard | "Does each of these screenshots follow the style guide?" | Opus at medium; on Codex, Sol at high | The standard is handed over; the helper applies it |

Anything else runs on what the user named, or your default.

## Setting it

A model or thinking level the user, or the skill you are running, names for a helper wins over this skill.

- Claude Code's Agent tool: `model: "opus"` and `effort: "medium"`.
- A one-shot Claude run: `claude -p --model claude-opus-5-5 --effort medium`, or through AI Manager, `aim claude run <account> -- -p --model claude-opus-5-5 --effort medium`.
- A Codex run: `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high"`.
- Other hosts, and where a pin stops holding: `../_shared/native-child-capabilities.md`. Check the live tool schema when it and this list disagree.

The numbers behind these examples, how they were measured, and how to measure again when a new model arrives are in [references/evidence.md](references/evidence.md). Read it when you want the evidence for a call.
