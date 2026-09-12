# Preserve Pro's judgment and verify that the consultation actually reached it

The skills need to preserve two things from beginning to end: the user's reason
for consulting an expert, and the exact evidence and question that expert
received. The parent should give Pro enough context to rethink the approach,
verify delivery, read the resulting assessment, and only then summarize it for
the user.

This plan applies `$skill-authoring` and its required `$prompt-authoring`
discipline to the collected evidence. It precedes the combined revision and
publication. The earlier submission-only edits and installations remain part
of the starting state; this plan does not treat them as an authorized outcome
of the original data-gathering request.

## Evidence and its implications

The primary sources are the [consultation analysis](pro-consultation-prompt-failures-2026-09-11.md),
its [thirteen-episode appendix](pro-consultation-prompt-failures-2026-09-11-evidence.md),
and the [partial-submission investigation](chatgpt-submission-failures-2026-09-11.md).
The retained September 9 BrowserOS survey and Pro-abandonment investigation
were also reviewed for constraints that this revision must preserve: profile
identity, foreground protection, real source access, full instruction reads,
and waiting for the requested response. This is a focused repair of prompting
and delivery, not implementation of the separate filesystem or installation
remediation proposals.

| Evidence | Lesson for the revised skill |
| --- | --- |
| The SNG parent changed a concise report-to-user request into five prescribed Pro bullets and a protected experiment ladder. | Let Pro own interpretation and plan revision; the parent owns concise reporting afterward. |
| Other consultations use “peer” language alongside closed choices, while better examples preserve the original goal and allow alternatives. | Review the actual composer, attachment instructions, and inherited thread assumptions together. A role label does not establish independence. |
| Focused source-repair reviews have a legitimate narrow job. | Do not force every consultation into a broad research exercise or ban lists and precise questions. Infer the judgment needed from the user's task. |
| A multiline fill submitted 64 characters of an 838-character prompt, and draft text was mistaken for conversation content. | Prevent keyboard-driven newline submission and verify full draft and submitted-turn identity separately. |
| Earlier replies and sparse snapshots were accepted in place of a pending review; the existing wait rules were sometimes lost to truncation. | Preserve complete skill loading, the 3–5-minute cadence, response association, and pending decisions until the requested answer arrives. |

These are supported failure modes and useful counterexamples. They do not
establish a fleet-wide failure rate or prove what a differently prompted Pro
would have recommended.

## The intended behavior

Three representative requests define the work:

1. **“We have our first results. Help us interpret them against the original
   goal and decide how the plan should change; summarize the answer for me.”**
   Pro receives the original objective, meaningful prior context, actual
   results, uncertainties, and the current plan as a proposal. It can identify
   the wrong question, reject a diagnosis, reorder experiments, or recommend a
   different approach. Its response structure serves its assessment.
2. **“Review the exact repair in this pushed PR.”** Pro inspects the actual
   source through GitHub and answers the scoped repair question. A concise
   verdict is appropriate; it is not later described as a broader review.
3. **“Send this follow-up with the current evidence and bring back Pro's
   answer.”** The parent verifies the intended draft, the new submitted user
   turn and files, and the corresponding response. A fragment, old reply, or
   unsent editor never counts as completing the consultation.

Ordinary browser form work belongs to BrowserOS. Local prompt drafting alone
belongs to prompt-authoring and does not launch a Pro consultation. These
nearby tasks should remain easy to distinguish.

## Changes in the smallest owning surfaces

| Surface | Planned change | Reason for this location |
| --- | --- | --- |
| `skills/chatgpt-web/SKILL.md` | Put expert collaboration and delivery together at the top. Explain holistic interpretation, actual-brief review, separation of Pro's answer from the parent's summary, faithful retries, and acceptance against the original user purpose. Retain existing browser, Pro, connector, and wait requirements. | Owns the consultation's purpose and end-to-end completion. |
| `skills/chatgpt-web/references/composer-and-attachments.md` | Refine the existing submission details around visible editor state, full new-message readback, attachment placement, and response association. Keep selectors as current examples, not permanent requirements. | Owns ChatGPT-specific mechanics; the main entry retains every mandatory check. |
| `skills/prompt-authoring/SKILL.md` | Make the recipient's required judgment and the parent's final presentation separate authoring decisions. | This error can affect any expert consultation, not only ChatGPT. |
| `skills/browseros/SKILL.md` | Clarify that typing can itself trigger a submission and that field contents and resulting application state both need inspection. | Owns generic input semantics and outcome verification; ChatGPT selectors remain in its site skill. |
| Relevant `agents/openai.yaml` files | Align default prompts with the owning skills without copying their full procedures. | Keeps runtime invocation metadata consistent with the instructions it loads. |

Use direct instructions and short explanations. Do not add a fixed research
questionnaire, mandatory output slots for Pro, a new agent workflow, or a
browser controller. The existing attachment route avoids the demonstrated
newline hazard. A separate BrowserOS text-insertion improvement remains a
possible tool change; this plan does not claim to repair its executable.

## Implementation and verification sequence

1. **Write this combined plan from the evidence.** Separate confirmed behavior
   from inference and preserve successful focused reviews as counterexamples.
2. **Revise the three owning skills and applicable metadata.** Preserve the
   expert's freedom, the user's real constraints, exact relays, required
   connectors, full-input checks, profile identity, foreground protection, and
   waiting semantics. Remove repetition as material is moved toward the top.
3. **Exercise the revised guidance on the recorded cases.** Produce an
   illustrative campaign consultation without protected conclusions, preserve
   a focused PR review, and judge the captured fragment/draft/full-send states
   separately. Check retries preserve the substantive question. These are
   document and recorded-state exercises, not new Pro submissions or an
   independent model evaluation.
4. **Check package shape and reading cost.** Review complete changed files,
   frontmatter, metadata and links; measure entry bodies and required reading;
   run `npx skills check` and appropriate installation verification. The CLI
   update check does not validate the meaning of the prose.
5. **Publish through `$amir-publish`.** Commit the reviewed skill changes and
   their plan/evidence docs, push the current branch, run the standard local
   install, and sync/install on each reachable configured host. Preserve
   unrelated untracked material. Record unreachable hosts or install failures
   precisely; do not hide incomplete distribution.

Completion requires both the consultation and delivery improvements to be
present in the published package, with validation and host results recorded.
Installing a file cannot guarantee that an already-running agent has reread
it; existing sessions need the new instructions before their next consultation.

## Execution record

The plan was written before the combined revision. The three skills and their
invocation metadata now carry the planned changes. The ChatGPT composer
reference remains the owner of DOM details, with its mandatory checks retained
in the entry file.

### Recorded-case exercises

| Exercise | Result |
| --- | --- |
| First-campaign consultation | Replaced the attached brief's five-bullet/fixed-ladder instructions with an open interpretation request grounded in the original goal. Preserved the complete campaign evidence section. The composer is a short single paragraph; concise reporting remains the parent's job. |
| Focused payments repair | Preserved the actual C09 source-repair prompt and its limited verdict. The new guidance does not require reopening the entire architecture for this task. |
| Partial submission and later recovery | Compared the retained DOM messages with the intended prompt. The 64-character fragment fails full-text delivery; the later 832-character body matches after removal of six line breaks. This establishes text coverage only; attachment freshness remains a separate question. |
| Retry and nearby tasks | Reviewed C08 as a meaning-preservation exercise: shortening a retry must retain the original substantive review. Local prompt drafting does not launch ChatGPT, and ordinary browser fields use BrowserOS without the ChatGPT-specific message selectors. |

For example, the revised campaign composer is:

> Read the attached campaign evidence in light of our original goal. What do you think we have learned, and how should it change our approach? Reconsider our proposed plan where warranted.

The attachment also had to change: an open composer above a fixed-ladder,
five-bullet brief would still fail. The revised attachment preserves the
measured data and makes the plan and causal explanations proposals for expert
assessment. This example illustrates the principle; it is not a required
template or an experimentally validated prediction of Pro's answer.

Temporary exercise artifacts are in
`/tmp/chatgpt-web-skill-revision-20260911`. No Pro submission, browser mutation,
or independent model evaluation was performed for these exercises.

### Package checks

All six entry/metadata YAML files parsed successfully; names and descriptions
were valid and within the 1,024-character description limit. Package and plan
links resolved, and `git diff --check` passed. The required `npx skills check`
completed with exit code 0; it reported the same unrelated Impeccable upstream
path warnings and did not delete those skills. That command checks upstream
updates, not the semantics of this revision.

| Entry body | Lines | Estimated tokens |
| --- | ---: | ---: |
| ChatGPT Web | 200 | 3,036 |
| BrowserOS | 143 | 2,084 |
| Prompt Authoring | 125 | 2,848 |

Token estimates use UTF-8 bytes divided by four because a tokenizer was not
installed. The full consultation reading path, including existing required
companions and applicable references, is approximately 19,814 tokens. It must
be read in suitably sized calls and reused within the session. A short entry
does not make that combined reading free, and a successful file read does not
make truncated tool output complete. This revision adds no new mandatory
reference or controller.

### Publication

The combined revision and evidence docs were committed as `cecc89d`
(`Preserve expert judgment and verify complete ChatGPT submissions`) and
pushed to `origin/main` through `$amir-publish`.

| Host | Result |
| --- | --- |
| Amir-M5, current machine | `make install` and `make verify_install` passed. Skipped a duplicate SSH install to the `amir-m5` alias. |
| `amirs-m3-max-new` | Fast-forwarded `main`; installation and verification passed. |
| `amir-m3-36gb` | Fast-forwarded `main`; installation and verification passed. |
| `agents@amirs-mac-studio` | Fast-forwarded `main`; installation and verification passed. |
| `home` | Fast-forwarded `main`; installation and verification passed. |

The standard local installer also refreshed the pre-existing Hermes skill
mirror. That was not needed for this task. Subsequent remote installs and
verification used the existing `NO_HERMES=1` option, consistent with the user's
stated preference. No reactive deletion was performed.

Local logs are under `/tmp/chatgpt-web-skill-revision-20260911`; each remote's
installation log is `/tmp/chatgpt-web-publish-20260911.log`. All four remote
installs verified the implementation commit. This execution-record update is
documentation only and is distributed afterward without repeating installs.

The plan, combined skill revision, checks, and publication are complete.
Running sessions still need to read the updated instructions before their
next consultation; installation does not prove future model compliance.
