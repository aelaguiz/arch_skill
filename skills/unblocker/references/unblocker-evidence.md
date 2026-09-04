# Unblocker evidence

Current escalation rule (2026-09-04): the unblocker resolves ordinary
uncertainty locally and reserves Pro for major consequential problems it
cannot resolve through reasonable investigation and reasoning. The run's
review cadence applies. Historical wording below does not require a Pro
consultation for every uncertain decision; `SKILL.md` owns the live rule.

Historical owner ruling (2026-09-01):

> "My thinking is we just spawn an unblocker or authorization agent whose
> job is to handle when it thinks it got blocked or it needs an
> authorization. Based on my high-level intent, it fucking figures it out.
> Its job is to unblock and to authorize. Its only boundaries are: don't
> mess with the fucking production apps. Other than that, sure fucking go
> for it. It can escalate to pro if it doesn't know what to do."

> "We need to make this less random: deciding it needs approval, which
> these agents all fucking do, or deciding it's blocked on shit that it's
> actually not blocked on and could just work through with pro from first
> principles and from the plan intent itself."

> "It's just a long-lived agent who's there to be the end blocker and it
> becomes a part of the goal prompt. We should suggest goal prompts for
> these two [epic-to-prs, issue-to-pr] using the goal prompt authoring...
> Agents that can arm their own goal prompt can do that. Otherwise it can
> tell me what to do and I'll arm it."

The observed failure (epic #497 run, session archived
2026-09-01T10:07:49Z): three hours in, with two issues merge-ready and a
third implemented and passing in a preserved worktree, the agent invented
the literal gate "respond authorize both" before (1) stacking the finished
work onto the newer PR head and repairing three call sites, and (2) fixing
incorrect multiplayer strategy averaging before training. Neither touched
production. It reported WAITING FOR USER repeatedly until the session died
at compaction overflow. Every gated step was ordinary in-scope engineering
it could have decided from the plan, or settled with one Pro consult.
