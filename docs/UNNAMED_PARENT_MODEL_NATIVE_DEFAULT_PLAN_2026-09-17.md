# Plan: Native Default Dispatch For An Unnamed Parent Model

**Date:** 2026-09-17
**Repo:** `arch_skill`
**Status:** revised after Fable 5.1 (high) plan review; ready to implement
**Evidence:** `docs/open-source-model-dispatch-audit-2026-09-17/` and `docs/OPEN_SOURCE_MODEL_DISPATCH_SUPPORT_2026-09-17.md`
**Review record:** Fable's plan feedback, findings 1-11, all accepted. `/tmp/fable-review/plan-feedback.md`

---

## 1. Verdict

Add one global default to the shipped skills: **when nothing names a worker and the parent is a model this repo does not name a worker for, the dispatcher uses a native child of the active host running the parent's own model and thinking level.** The default yields, value by value, to any specific instruction.

The work is four doctrine edits, three skill edits with their metadata, and two doc updates that the repo's Definition Of Done requires. There is no code change: the resolver keeps its current shape, because its only consumers build external command lines and would reject a native value after run state already exists.

## 2. The rule, in the words that will ship

This text is the whole contract. Everything else in this plan serves it.

```markdown
## Default dispatch for a parent model this repo does not name

This repo names a worker for two parents: Astra and Fable. Every other parent —
Sol, Terra, Luna, Opus, DeepSeek, GLM, Fugu, and whatever is added later — takes
the default below, in every host. The Codex model preference below is about
choosing a model for a Codex lane; it does not name a worker for a Codex parent.

When the user names no model and the calling workflow names none, the child is a
native child of the active host that inherits the parent's model and thinking
level. Omit both values so the host supplies them. Do not substitute a vendor
model. If this host cannot start a native child at all, say so, then either do the
work in the parent or take an external lane on the parent's own model; do not open
an external lane merely to have a worker when a native child exists.

Each named value replaces only itself: a named effort runs on the inherited model,
and an explicit level must be one that model supports. A named model, transport,
or reviewer needs no justification.

The default covers every role, including review. A review with no model named is a
native same-model review; ask for a named reviewer when provider diversity is the
point.
```

Four properties this wording holds:

1. **Open-ended and correctly scoped.** The uncovered set is "a parent this repo does not name a worker for." It does not pretend that naming a Codex or Claude family names a worker for a parent in that family.
2. **A default, not a gate.** It fills silence and yields one value at a time.
3. **One owning place.** The rule lives in `skills/_shared/agent-orchestration-policy.md`. One role-local sentence in `delegated-implementation` and one fleet-profile sentence in `conductor` point at it. Nothing else restates it.
4. **Honest about a host with no native child.** It names the fallback instead of leaving the dispatcher to break the rule.

## 3. What changes and what does not

**Changes:**

- Any parent this repo does not name a worker for gets a documented default, including for review. That set includes Sol, Terra, Luna, and Opus parents, which today match no branch at all.
- The executive and worker contract reaches every coordinator instead of only Astra and Fable.
- `conductor` defines its fleet profile when the parent is unnamed, so the inherited child satisfies its own pin rules.
- The capabilities file records the host facts the default depends on, with provenance.
- `README.md` and `docs/arch_skill_usage_guide.md` stop restating the Astra and Fable gate.

**Does not change:**

- Astra to GPT-5.6 Sol at `high`, and Fable to Opus 5. Both sentences stay byte-identical.
- The Codex preference for `gpt-6-astra` at `xhigh` inside a selected Codex lane.
- The conductor's named fleet defaults, the Terra shortcut, `codex-review-yolo`, the Pro lanes, and the alias map.
- Which skills are opt-in. `agent-delegate` stays the only skill the host may reach without being named.
- The install surface, the install commands, `model_resolution.py`, and the `build/` copies.

## 4. Host facts the plan depends on

| Fact | Status |
|---|---|
| A Prime Agent child inherits the parent model and thinking level when neither is passed | Verified in the runtime source and observed on four children |
| A Prime Agent child can be pinned to another provider when the installation is authenticated for it | Verified live: `openai-codex/gpt-5.6-luna` and `sakana/fugu-max` admitted from a DeepSeek parent |
| An explicitly requested thinking level outside the model's set hard-fails the spawn | Verified live on `openrouter/deepseek/deepseek-v4.1-flash` with `medium` |
| A supported level is not predictable from a registry map alone | Verified: `anthropic/claude-fable-5-1` accepted `high` although its registry map omits `high`. Probe before pinning |
| Codex children inherit the parent model, and a child's provider follows the parent turn | Read from the shared facts file; consistent with 0 of 4,561 September `spawn_agent` calls passing a model |
| A Codex native child requires a catalog entry tagged `multi_agent_version: "v2"` | Read from the installed Codex binary and the local catalogs. **Not spawn-tested under an untagged profile.** Record it with that provenance |
| A Claude Code named subagent carries its own model in frontmatter and is allowlist-checked | Read from installed agent definitions and binary strings |
| A Prime child cannot create children at the default depth | Read from `skills/_shared/agent-orchestration-policy.md:214-216` |

Passing no model and no level is what makes the default work on a host with partial capability. It does not make a native child exist where the host cannot create one; that case has its own sentence in the rule.


---

## 5. Edit plan

Authoring method for every skill edit: `$skill-authoring` in `edit` mode, with `$prompt-authoring` applied to the prose. Read `skills/skill-authoring/references/skill-pattern-contract.md` and `references/packaging-trigger-and-validation.md` before editing. Co-edit each skill's `agents/openai.yaml` when its visible contract changes. Keep every body under the authoring thresholds and every `description` under 1,024 characters. Do not edit anything under `skills/<slug>/build/`.

### 5.1 `skills/_shared/agent-orchestration-policy.md`

**(a) Insert the rule from §2** as a new section immediately before `## Codex model preference`. This is the single owning statement.

**(b) Add a lead-in to the Codex preference.** The existing sentences at `:78-82` stay byte-identical. Add one line before them:

```text
Applies when the child will run under Codex: a Codex lane chosen from any host,
or a native child of a Codex parent. On any other host, resolve a Codex id against
that host's live catalog and do not assume it is present.
```

**(c) Amend the dispatch imperatives so they do not contradict the default.**

- `:93-94`, currently "So state the child's model and thinking level at dispatch the same way you state its starting context, and treat 'cheap worker' as a profile you resolve rather than a transport you pick." Append: ", or state that the child inherits under the default above."
- Replace cost-as-second-test wording with naming as the test: "The cost question has two directions. When a skill or the user names a worker for this parent, state that profile at dispatch or take the external lane. When nothing names one, the default above applies and the inherited child is the stated profile."

### 5.2 `skills/_shared/native-child-capabilities.md`

**(a) Update the provenance line** to record this verification date.

**(b) Add one short section, "Open-source and unnamed parent models,"** carrying: inheritance as the default; the hard failure on an explicitly requested unsupported thinking level; that a supported level is not inferable from a registry map, so probe before pinning; and that reach is per-installation.

**(c) Amend the closing line** "An unpinned native child is not a cheap lane: it runs the parent's model on whatever you gave it." Append: "That is the cost to control when a worker profile is named for the parent, and exactly the default when none is."

**(d) Record the host facts** from §4 with provenance. Write the Codex v2-tag row as read from the binary and catalogs, not spawn-tested. Write the Prime rows from the verified probes.

### 5.3 `skills/delegated-implementation/SKILL.md`

**Keep `:44-47` verbatim**, through "...the general Astra preference does not replace Sol here."

**Replace only `:48-49`**, currently "Honor explicit user model and effort overrides. For another parent model, use the worker choice supplied by the user or calling workflow." New:

```text
Honor a worker the user or the calling workflow named. For any other parent —
Sol, Terra, Luna, Opus, DeepSeek, GLM, Fugu, and whatever is added later — the
worker is a native child of the active host that inherits the parent's model and
thinking level; read the default in
`../_shared/agent-orchestration-policy.md`.
```

**Two small corrections in the same file:** `:57` "An assigned Sol or Opus worker implements its bounded brief" becomes "An assigned worker implements its bounded brief"; `:80` "When the parent sends a Fable or Sol reader to review or audit delivered work" becomes "When the parent sends a reader to review or audit delivered work", so the family-A brief rule still applies to a same-model reader.

**`description`**, currently containing "Used by issue-to-pr and epic-to-prs for Astra or Fable coordinators, or when the user asks for this executive/worker split on accepted work. Astra delegates to GPT-5.6 Sol high; Fable delegates to Opus 5." Replace that span with:

```text
Used by issue-to-pr and epic-to-prs for every coordinator, or when the user asks
for this executive/worker split on accepted work. Astra delegates to GPT-5.6 Sol
high; Fable delegates to Opus 5; any other parent delegates to a native child on
its own model.
```

### 5.4 `skills/issue-to-pr/SKILL.md`

**(a) Drop the gate** at `:18-22`. New opening:

```text
Apply `$delegated-implementation` throughout the work: delegate code,
reproduction, tests, and repairs; personally review every deliverable and changed
code line. All skill authorship stays with the parent. An assigned implementation
worker keeps its bounded role and reports to the originating coordinator under
that contract.
```

**(b) Replace the Delegation section** at `:205-209`. It already points at `$delegated-implementation`, so it carries no restatement of the rule:

```text
`$delegated-implementation` owns the worker selection, brief, direct review, and
repair contract, including parent-owned skill authorship. Read the installed
`../_shared/agent-orchestration-policy.md` before dispatch and apply
`$prompt-authoring` to the populated brief. Leave spawning mechanics to the active
harness. Carry the scope, inherited review coverage and cadence, unblocker
contact, and handoff into each brief.
```

**(c) `description`:** replace "Astra and Fable coordinators use delegated-implementation: workers code, test, and repair; the parent owns decisions, every deliverable's direct review, and all skill authorship." with:

```text
Every coordinator uses delegated-implementation: workers code, test, and repair;
the parent owns decisions, every deliverable's direct review, and all skill
authorship.
```

### 5.5 `skills/epic-to-prs/SKILL.md`

**(a) Drop the gate** at `:20-23`, with the same wording as 5.4(a) plus the epic's shared scope.

**(b) Replace the Delegation section** at `:200-205` with the same text as 5.4(b), adding "the coordinator owns Pro submissions and the submission count" as it does today.

**(c) `description`:** replace "Astra and Fable coordinators use delegated-implementation: workers code, test, and repair; the parent owns direct review of every deliverable and all skill authorship." with the same span as 5.4(c).

### 5.6 `skills/conductor/SKILL.md` and `references/delegation-and-monitoring.md`

The rule is already in `_shared`, and this skill's ten "unpinned native child" sentences are correct for a named parent. Do not rewrite them. Make the inherited child satisfy them by definition.

**(a) Define the fleet profile twice.** Add one sentence in `SKILL.md` at the fleet resolution (`:294-296`) and again in `references/delegation-and-monitoring.md:102-108`:

```text
When the parent is a model this repo does not name and the user names no provider,
the fleet profile is the parent's own model and thinking level.
```

**(b) Add the pinning equivalence once.** In `references/delegation-and-monitoring.md:10-13`, after "never route bulk work to an unpinned native child", add:

```text
When the fleet profile is the parent's own, the inherited native child already
carries it and counts as pinned for every rule in this skill.
```

**(c) `SKILL.md:36-39`** gets that same equivalence sentence and nothing else. The existing "Pin the profile or take the external lane" text stays.

**(d) No change** to `audit-and-send-back.md:247-251`, the named defaults, the alias map, the Terra shortcut, `fork_turns` doctrine, or the log contract.

### 5.7 Metadata co-edits

- `skills/issue-to-pr/agents/openai.yaml:4`: replace "Astra and Fable coordinators apply $delegated-implementation, personally review every deliverable and changed code line, and retain all skill authorship" with "Every coordinator applies $delegated-implementation, personally reviews every deliverable and changed code line, and retains all skill authorship".
- `skills/epic-to-prs/agents/openai.yaml:4`: replace "Astra and Fable coordinators apply $delegated-implementation: workers code, test, and repair; the originating parent personally reviews every deliverable and changed code line and authors all skill content." with "Every coordinator applies $delegated-implementation: workers code, test, and repair; the originating parent personally reviews every deliverable and changed code line and authors all skill content."
- `skills/delegated-implementation/agents/openai.yaml:4`: replace "Use Astra to GPT-5.6 Sol high or Fable to Opus 5, honoring explicit user choices and the active harness's agent mechanics." with "Use Astra to GPT-5.6 Sol high or Fable to Opus 5; any other parent uses a native child on its own model. Honor explicit user choices and the active harness's agent mechanics."
- `skills/conductor/agents/openai.yaml`: no change. It already defers to the shared policy, and "pinned worker fleet" stays accurate under 5.6.

### 5.8 Docs required by the Definition Of Done

These are required, not optional, because they restate the gate the plan removes.

- `README.md:579-582`: "Use this execution contract when an Astra or Fable coordinator runs `issue-to-pr` or `epic-to-prs`" becomes "Use this execution contract when a coordinator runs `issue-to-pr` or `epic-to-prs`", and after "Fable uses Opus 5" add "; any other parent uses a native child on its own model".
- `docs/arch_skill_usage_guide.md:467-468`: the same two changes in its own wording.
- Optional, one line: `AGENTS.md` Skill Routing, scope "Default Codex to `gpt-6-astra` at `xhigh`" to a selected Codex lane. If that line changes, `README.md:865` must change with it.

---

## 6. Out of scope, and deferred on purpose

| Item | Why it is not in this plan |
|---|---|
| A `native` value in `model_resolution.py` | Every consumer switches on the runtime to build an external command line, and `run_arch_epic.py:994-997` and `:1464-1503` would reject a model-less role after `auto-init` already wrote run state. The host's own child is expressed by absence, which is what the arch-epic contract already does. A real feature for `arch-epic` and `stepwise`; separate issue |
| Stepwise's runner accepting a native runtime | Confirmed correct to defer: `skills/stepwise/SKILL.md:12-14` and `:103-104` already have the native lane, and it reads `_shared`, so the default reaches it. The runner is only the external adapter |
| Rewriting the 36 `fork_turns` host-pair lines | No host is blocked today, and it touches ten skills |
| The resolver learning the local Codex profiles | Unrelated to the default, which passes no model |
| Codex catalog tagging, Prime `settings.json`, host config | Local configuration, explicitly outside the ask |
| The `sonnet`/`haiku` contradiction, the 4-versus-5 runtime list, `gpt-5.4-mini` beside a blocked `gpt-5.4` | Real inconsistencies, unrelated to this default |
| Deleting the stale `skills/<slug>/build/` copies | Housekeeping; do not touch them here |
| `make install` | A separate act that writes to every skill root |

## 7. Execution order and effort

| Step | Work | Estimate |
|---|---|---|
| 1 | `_shared/agent-orchestration-policy.md`: new rule, Codex lead-in, two imperative amendments | 25 min |
| 2 | `_shared/native-child-capabilities.md`: provenance, new section, host facts, closing line | 25 min |
| 3 | `delegated-implementation`: paragraph, two small corrections, description, metadata | 20 min |
| 4 | `issue-to-pr` and `epic-to-prs`: gates, delegation sections, descriptions, metadata | 30 min |
| 5 | `conductor` and `delegation-and-monitoring.md`: two definitional sentences, one equivalence | 20 min |
| 6 | `README.md` and `docs/arch_skill_usage_guide.md` | 15 min |
| 7 | Verification, size and description checks, `npx skills check` | 20 min |

About two and a half hours, plus the review round.

## 8. Verification

| Check | How |
|---|---|
| Rule present once | `rg -n 'does not name' skills/` and confirm exactly three sites: `_shared` as owner, one role-local sentence in `delegated-implementation`, one fleet-profile sentence in `conductor` |
| Named text byte-identical | `git diff` and confirm the Astra, Fable, Codex-lane, Terra, Pro, alias-map, and `yolo` sentences are unchanged, except where §5 names them |
| Descriptions within cap | Measure each changed `description`; fail over 1,024 characters |
| Bodies within authoring thresholds | Measure line count and approximate tokens for each changed `SKILL.md` |
| Metadata matches the visible contract | Read each changed `agents/openai.yaml` against its `SKILL.md` |
| Conductor rules stay true | Read the ten "unpinned native child" sentences and confirm each is still literally true for a named parent, and true for an unnamed one under the new definition |
| No code change | `git diff --stat` shows no change under `skills/_shared/model_resolution.py` or any `scripts/` |
| Inheritance still works | Spawn one Prime child with no model and confirm it reports the parent's model and level |
| Package integrity | `npx skills check` |
| Installed surface | Do not run `make verify_install` unless the user asks for the install. Report that `~/.agents/skills` is stale until `make install` |

Do not add tests that assert doctrine wording.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Scope creep into named behavior | The do-not-change list in §3 plus the byte-identical diff check in §8 |
| The rule drifts into near-copies | One owning statement plus three named sites, verified by `rg` |
| Weakening the conductor's protection for named parents | Do not rewrite its ten sentences; add one definition and one equivalence sentence and check that every sentence stays true |
| A dispatcher reads the rule as forbidding the only available lane | The rule's own fallback sentence covers a host with no native child |
| Reviewers read a stale installed copy | Report the install state; do not install as part of this change |

## 10. Decisions taken

1. **The uncovered set is written open-ended**: a parent this repo does not name a worker for. Sol, Terra, Luna, and Opus parents are inside it, because no file names a worker for them today and the alternative is the dead end this plan removes. **Flagged for the user in one sentence.**
2. **Inheritance means model and thinking level.** Passing neither is what makes the default work on a host with partial capability.
3. **The default covers review.** A review with no named reviewer is a native same-model review.
4. **The rule lives in `_shared`.** Exactly two role-local sentences point at it.
5. **No resolver change.** The enum stays external-only; the host's own child is expressed by absence.
6. **Cost is not a second test.** Naming decides; cost explains why the named-parent rule exists.
7. **Reviewers for this plan:** one native Prime child on `anthropic/claude-fable-5-1` at `high`.

## 11. Reviewer questions from the plan review — status

All five were answered in the plan review and are folded in: the parent set (finding 1), the conductor protection (finding 3), the Stepwise deferral (confirmed correct, and applied to `arch-epic` as well), the resolver enum (do not add `native`), and the Codex-preference scoping (safe as a lead-in, rewritten to avoid baking a per-installation fact).

## Appendix — evidence

- `docs/OPEN_SOURCE_MODEL_DISPATCH_SUPPORT_2026-09-17.md` — the analysis this plan implements
- `docs/open-source-model-dispatch-audit-2026-09-17/A-container-skills.md` — container-skill inventory, 9 findings
- `docs/open-source-model-dispatch-audit-2026-09-17/B-review-consult-skills.md` — review and consult inventory, 12 findings
- `docs/open-source-model-dispatch-audit-2026-09-17/C-arch-family-and-shared.md` — arch family and shared doctrine, 16 findings
- `docs/open-source-model-dispatch-audit-2026-09-17/D-runtime-reality.md` — host reach, inheritance, and pinning probes
- `docs/open-source-model-dispatch-audit-2026-09-17/00-core-facts.md` — the verified fact set

