# Agents are narrowing Pro’s job before Pro can reconsider the plan

This report records the audited behavior and skill versions before the
[combined improvement plan](chatgpt-web-consultation-improvement-plan-2026-09-11.md).
That plan tracks the subsequent authorized skill revision and publication.

**The recurring failure is that the parent agent turns an expert consultation into completion of the parent’s chosen checklist. Calling Pro a “peer” does not undo the restrictions in the rest of the prompt.**

The September 11 SNG campaign is the clearest example. You asked the agent to run the campaign, take the results to Pro for interpretation, and report the results and interpretation to you concisely. The agent told Pro to return five prescribed bullets, select one next experiment, and keep the existing experiment ladder intact. That changed who was supposed to do the broader interpretation and what Pro was allowed to reconsider.

This behavior recurs in the reviewed history, but it is not universal. Other prompts in the same workstreams preserve the original goal, make the parent’s diagnosis challengeable, and allow a different experiment. Focused code reviews also legitimately ask narrow questions. The repair should preserve those useful cases.

The [evidence appendix](pro-consultation-prompt-failures-2026-09-11-evidence.md) contains thirteen consultation episodes from five Codex parent sessions, with actual prompt text, timestamps, source paths, and JSONL line numbers. The audit inspected seven selected rollouts across the local machine and home server. Its scope and limitations are recorded at the end of this document.

## The SNG prompt changed your request in two places

Your instruction was:

> “run that campaign, then take the results back to Pro, have Pro interpret them, and then I want you to show me the results and the interpretation concisely.”

The actual composer message said:

> “Interpret the measured #680 campaign as a peer research reviewer. Return only the requested five bullets; do not invent additional runs.”

The attached brief added:

> “Return no more than 5 bullets”
>
> “one next experiment, keeping the baseline ladder intact.”

These are exact source passages from [the campaign consultation](pro-consultation-prompt-failures-2026-09-11-evidence.md#c01-first-sng-campaign-results). The last instruction is especially consequential: the experiment ladder was part of what the results might require changing. The prompt protected it before Pro assessed the evidence.

The brief did include substantial numerical evidence. The failure was not simply a lack of numbers. It supplied the parent’s chosen interpretation task and decision boundary along with those numbers, while leaving the original product objective and permission to reconsider the overall approach less prominent.

Pro’s visible response followed the requested five-part structure. It still made useful observations: the campaign did not establish improved learning, the cash and SNG geometries were confounded, the fallback counter lacked the denominator and semantics needed for a causal claim, and a matched-geometry control could remove one ambiguity. Those observations should not be discarded merely because the prompt was poor. The demonstrated loss is the breadth of the consultation you requested; the trace does not establish what an unconstrained Pro would have concluded.

## Five patterns explain the problem

### 1. Brevity for your summary becomes a limit on Pro’s analysis

**Observed:** The SNG user request distinguishes Pro interpreting the results from the parent reporting them concisely. The authored prompt collapses those into a concise, fixed-format Pro response. Both the composer and the attached brief impose the restriction. [Campaign evidence](pro-consultation-prompt-failures-2026-09-11-evidence.md#c01-first-sng-campaign-results).

**Why it matters:** The parent needs to read enough of Pro’s interpretation to understand surprises, competing explanations, and implications for the plan. Compressing the upstream answer before that interpretation is available risks removing the material for which Pro was consulted.

**Likely cause:** The parent appears to have transferred the final-answer requirement to the external consultation. The wording change is directly observed; the internal reason for making it is an inference. There is no need to blame the ADHD plugin to explain this incident.

**Correction:** Keep the request to Pro about the judgment needed. Let the parent apply the user’s preferred brevity when reporting the answer afterward. A concise prompt can still invite a complete expert assessment.

### 2. The parent makes its current plan harder to reject than its “peer” language suggests

**Observed:** The SNG brief simultaneously asks for peer interpretation and requires keeping the baseline ladder intact. A payments prompt labels the task a “Major architecture decision” but asks Pro to choose between two parent-selected solutions. An earlier SNG result prompt supplies the proposed depth boundary, frozen recipe, comparison, and stop rules before requesting one recommendation. [Campaign](pro-consultation-prompt-failures-2026-09-11-evidence.md#c01-first-sng-campaign-results), [payments architecture choice](pro-consultation-prompt-failures-2026-09-11-evidence.md#c10-payments-major-architecture-decision), [earlier SNG result](pro-consultation-prompt-failures-2026-09-11-evidence.md#c06-prior-sng-four-hour-result).

**Why it matters:** “Challenge our framing” is weakened when other instructions make the current framing binding. Pro can criticize details while the most consequential question, whether the investigation itself should change direction, has already been restricted.

**Important distinction:** Some constraints are legitimate. The earlier SNG user explicitly preferred incremental experiments before six-hour runs. Instructions against production mutations or a second payment authority also have different purposes from preserving an untested hypothesis. This audit does not classify all constraints as invented or all candidate experiments as leading.

**Correction:** Distinguish the user’s objective and actual constraints from the parent’s hypotheses and preferred plan. Pro should be able to reject the latter and still answer the assigned question successfully. Candidate experiments are useful context when alternatives remain possible.

### 3. Research consultations inherit the shape of implementation acceptance reviews

**Observed:** The same SNG session uses Pro first to review a dependency-ordered PR stack and later to interpret the first campaign. The PR prompt asks for merge readiness, blockers, and concrete repairs. The campaign brief then asks for a result, strongest evidence, unresolved items, causal interpretation, and one next experiment in fixed slots. The payments history contains many similarly scoped source and acceptance verdicts. [SNG stack review](pro-consultation-prompt-failures-2026-09-11-evidence.md#c04-sng-implementation-stack-review), [campaign results](pro-consultation-prompt-failures-2026-09-11-evidence.md#c01-first-sng-campaign-results), [provider final review](pro-consultation-prompt-failures-2026-09-11-evidence.md#c12-provider-final-epic-review).

**Why it matters:** Verifying whether a known defect is fixed and interpreting new research evidence are different jobs. The first can reasonably end in a scoped verdict. The second may require changing the question, revisiting the original goal, or deciding that another kind of evidence is needed.

**Likely cause:** The parent reuses an implementation-review habit when the task changes to research interpretation. The sequence and prompt shapes are observed; the transfer mechanism is an inference. The history does not prove a shared hidden template or one model-wide cause.

**Correction:** Before composing the consultation, identify what judgment the user actually needs now. Preserve focused repair reviews. For research interpretation, give Pro ownership of the interpretation and freedom to revise the approach. Do not require the user to select a formal mode.

### 4. Error recovery introduces stronger limits without explaining their effect

**Observed:** A payments final-review prompt is followed by a visible “Internal Server Error.” The retry says “Assess only” four listed questions and requests a short table and final verdict. The user did not introduce that restriction between the two prompts. [Original prompt, error, and retry](pro-consultation-prompt-failures-2026-09-11-evidence.md#c08-payments-final-review-and-retry).

**Why it matters:** A transport or generation problem should not decide which findings the reviewer is allowed to raise. Adding “only” while shortening a prompt creates a risk that recovery changes the review's purpose. That risk calls for checking the meaning of the retry, not prohibiting shorter prompts.

**Scope of the finding:** This is weaker evidence than the SNG example. The retry retains all named acceptance issues and asks for any material source defect, so the wording alone does not prove that a required review area was dropped. What is established is the added limiting language and response compression during recovery. The trace does not establish that the shorter prompt fixed the server error.

**Correction:** Repair the failed submission while preserving the consultation’s purpose and authority. If a genuinely smaller review is needed, treat and report it as smaller. Do not later present that result as the full original review.

### 5. Reading prompt-authoring becomes a procedural step without changing the actual prompt

**Observed:** Before the SNG campaign, the agent tried the wrong installed path, corrected it, and received the complete prompt-authoring, ChatGPT Web, and BrowserOS entries. The successful read includes the rules about applying authoring to the actual populated brief and keeping caller hypotheses challengeable. It still authored the five-bullet, fixed-ladder consultation. The current home-server prompt-authoring and ChatGPT Web entries exactly match the repo versions. [Loading evidence](pro-consultation-prompt-failures-2026-09-11-evidence.md#instruction-loading-evidence).

**Why it matters:** Repeating “use prompt-authoring” is insufficient when the agent reads the instructions but fails to apply them to the composer and attachment together. Saying “peer research reviewer” can become another procedural label rather than a meaningful grant of judgment.

**Correction:** The owning skill should make the purpose of an expert consultation unmistakable, then require the parent to review the actual outgoing material against that purpose. A useful question is whether Pro can conclude that the parent is asking the wrong question or should change the plan. If the prompt prevents that without an actual user constraint, it has defeated the consultation.

## The current skill addresses independence, but its emphasis leaves this failure easy

The [ChatGPT Web entry](../skills/chatgpt-web/SKILL.md) already requires prompt-authoring before each submission. It says to keep caller hypotheses challengeable and not prescribe a research path without a task-specific reason. The [prompt-authoring entry](../skills/prompt-authoring/SKILL.md) and [shared orchestration policy](../skills/_shared/agent-orchestration-policy.md) already make the distinction between binding authority and caller conjecture explicit.

That is evidence against an installation failure or a total absence of the right doctrine.

The remaining gap is specific to ChatGPT Web’s job. Its opening critical rules concentrate on browser operation, literal Pro selection, account limits, connectors, and waiting. These are necessary, but they establish successful operation of the interface more clearly than successful collaboration with an expert. The preparation section also tells the caller to send the ask, essential context, and desired output “concisely.” It does not explicitly separate a concise consultation brief from restricting the expert’s answer to the parent’s summary format.

The result-checking section asks whether Pro answered the submitted ask with the required inputs. A badly narrowed submitted ask can pass that check. The skill needs to preserve the user’s consultation purpose when the parent turns it into a prompt, as well as verify that ChatGPT received and answered that prompt.

These are authoring vulnerabilities supported by the observed failures, not proof that any single sentence caused them. The same installed guidance also supports good consultations.

## The history contains examples worth preserving

| Example | What it gets right | What the example does not prove |
| --- | --- | --- |
| [Earlier SNG reset decision](pro-consultation-prompt-failures-2026-09-11-evidence.md#c05-prior-sng-reset-decision) | It restates the original goal, supplies results, offers two candidates, explicitly allows a third, and asks for a complete answer. | Five numbered topics are not automatically harmful. Its attachments and the response still matter. |
| [Morning Money Suite diagnosis](pro-consultation-prompt-failures-2026-09-11-evidence.md#c13-morning-money-suite-reliability) | It asks why the recurring failure happens and what durable approach would make the suite useful, while permitting the provisional diagnosis to be challenged. | The original temporary attachment was unavailable during this audit, so this is a positive composer example. |
| [Payments architecture planning](pro-consultation-prompt-failures-2026-09-11-evidence.md#c07-payments-architecture-planning) | It invites scope, acceptance, and architecture changes and says not to assume the proposed abstractions are correct. | An open composer cannot guarantee an equally open attached plan. |
| [Named payments source repair](pro-consultation-prompt-failures-2026-09-11-evidence.md#c09-payments-targeted-source-repair) | It deliberately checks one known repair and keeps unrun acceptance open. | A narrow repair verdict should not be represented as broad independent research advice. |
| [Corrected SNG consultation](pro-consultation-prompt-failures-2026-09-11-evidence.md#c02-corrected-sng-consultation) | It permits discarding or reordering controls, choosing an alternative experiment, challenging the framing, and answering in Pro’s own structure. | The captured window establishes submission and an interim response, not completion or the quality of its final judgment. |

The target is not a ban on lists, specific questions, concise prompts, or proposed experiments. It is preserving the expert’s ability to decide what matters for the user’s objective.

## The incident also exposed an input failure, which was separately repaired

The first campaign message was sent without its attachment. You noticed it. The agent acknowledged the error, stopped that response, attached the brief, and resubmitted. The later page readback shows `pro_input.md` on the submitted message and Pro’s completed five-part answer. The documented prompt failure therefore survives after the attachment failure was repaired. [Campaign evidence](pro-consultation-prompt-failures-2026-09-11-evidence.md#c01-first-sng-campaign-results).

The subsequent holistic re-prompt also has submitted-message readback. Its status script returned `stop: false` even though the visible page still contained “Stop answering” and an interim research message. That is a separate completion-detection problem. It is not evidence that the new prompt failed to send or that the old five-part answer was the new result. [Recovery evidence](pro-consultation-prompt-failures-2026-09-11-evidence.md#c02-corrected-sng-consultation).

Prompt quality and input/result integrity both matter. Neither should be used to explain away the other.

## Changes the evidence supports

1. **Put the expert-collaboration purpose near the top of ChatGPT Web.** For open interpretation and planning, Pro should receive the original objective, relevant history and evidence, and freedom to change the approach. Keep browser and source-access requirements.
2. **Apply prompt-authoring to the whole submitted request.** Review the composer, attached asks, working-document instructions, and continuing-thread assumptions together. The parent’s preferred diagnosis or plan must remain identifiable as a proposal.
3. **Separate Pro’s judgment from the parent’s presentation.** Pro provides the assessment needed for the decision. The parent reads it, integrates it, and reports it in the user’s preferred concise form. Do not transfer the user’s final-summary format upstream without a reason tied to the consultation.
4. **Preserve scope through retries and task changes.** Repair browser errors without silently shrinking the question. Reconsider the consultation’s purpose when moving from PR repair to interpreting new results.
5. **Validate on these real cases.** Check that a campaign-interpretation prompt permits plan revision, that a targeted source-repair prompt remains appropriately narrow, and that retries preserve the original question. Judge meaning and resulting behavior; phrase-presence tests and another mandatory checklist would not establish the repair.

The SNG working-document patch improves that one workstream, and its corrected composer is materially more open. It does not update the reusable skill for other sessions. Its list of five questions should be read as useful areas of inquiry, not a new fixed response form.

No skill or running agent was modified for this audit. The requested deliverables are this analysis and its evidence appendix.

## A peer-style prompt for this situation

This illustrates the intent; it is not a required template:

> We have the first campaign’s results. Our original goal is an SNG policy that plays useful poker throughout the tournament and improves as we give it more training. The attached working document contains the results, what we tried, and the plan we were considering. Help us interpret what we have learned in light of that original goal. What changes your view, and how should it change our approach? Reconsider the plan if the evidence points somewhere else. Our current explanations and proposed controls are hypotheses for you to challenge. The matched 75BB control is already running, but that does not make it the right next step. Give us your assessment and recommendation in the structure that best explains your judgment.

The important properties are the original goal, actual evidence, challengeable assumptions, and room to change direction. Copying the wording without those properties would repeat the problem.

## What this audit establishes, and what it does not

The exact prompt restrictions, user requests, skill-loading events, retry error, and selected browser readbacks are directly stored evidence. The patterns about habit transfer, premature compression, and optimization for a tidy verdict are interpretations of that evidence. They should guide a targeted repair, not be presented as a measured internal mechanism of the model.

This was a purposive sample of named workstreams active during September 4–11, 2026. Metadata discovery covered the relevant local and home Codex project families. Seven exact rollouts were inspected; five contributed the thirteen documented consultation episodes. The sample includes negative and mixed examples and cannot establish a fleet-wide failure percentage.

Bounded Prime and Claude lookups found no matching sessions for the selected host/project/time combinations. The findings therefore describe the inspected Codex behavior, not all providers or every agent on the machine. Historical composer text is better preserved than every attachment and final Pro response; each evidence case states the practical limit on its conclusion.

The current SNG snapshot ends around 21:33 UTC on September 11. Its later re-prompt outcome is outside this snapshot. No new Pro consultation was launched to test the skill, and no counterfactual response quality was assumed.

Only documentation was added. Verification consisted of checking the quoted prompt strings against source records, source anchors and local links, instruction-loading output, and the captured submitted-message readbacks. No application tests or skill-package checks were needed for these documentation-only changes.
