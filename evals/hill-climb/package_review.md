# Package review brief

The brief for the clean package review of PLAN.md section 3. Give it to a clean agent with the package path filled in
and nothing else. Its answer gates every layer 2 pass and the final validation: NO FINDINGS is required.

---

You're reviewing an agent skill before it is tested. The package is the folder `{package_path}`: a `SKILL.md`,
references and role briefs that teach an agent to run a long-running, budgeted hill climb (tests that keep improving one
business number) on its own for months, with independent agents checking its work. It names two companions it loads:
`skills/_shared/agent-orchestration-policy.md` and the `prompt-authoring` skill; read them only as needed to judge the
package.

The owner's rule for this skill, in his words: "whether you built scripts or heuristics as opposed to giving the agents
an intuition/intelligence. None of that is allowed. ... You remove their autonomy. You remove their intuition by boxing
them with stupid heuristics and scripts."

Read every file in the package. Find each place where the package boxes the agent instead of teaching it to judge:

- a script, helper or tool the package ships, or tells the agent to run, that does judgment work for it;
- a number presented as a rule for a judgment (a bar for acting or believing, a margin, a fixed share, an age, a count
  that triggers something), as opposed to a research finding given as a reason or an example of how one might judge;
- a keyword list, lookup table or decision table that decides;
- a fixed menu of moves, or a checklist that replaces looking, as opposed to concerns offered as places to look;
- anything that refuses or blocks the agent's own choice, or walls a role off from evidence its job needs.

Also find anything that seems written for one particular test rather than for real use: an example, name, number or
phrase that looks like it belongs to a specific simulated world or scenario instead of teaching the general judgment.

The owner did ask for some things on purpose, so they are not findings in themselves: money is the only thing he is asked for, and progress reports reach him on a schedule without asking anything; independent one-job agents check plans, builds, quality and results before money moves; every idea names the research it draws on; each tick reads state fresh instead of trusting a carried summary; exploring never stops; a lesson is believed only after a rerun; what people say and do around an item is weighed beside the main number without overriding it; each item's recipe is kept and a variation is cut from its parent; items are coded richly; and the workbook reads at a glance. A finding there would be about how it is taught, not that it exists.

Recognizing the difference matters more than counting words. "Act when the chance of helping is above 0.5" is a rule; "a
move that can be undone needs only a lean, because waiting costs money every day" teaches the judgment. A list of
concerns introduced as "places to look" with "follow what you notice" is guidance; the same list introduced as "pass
only if all of these hold" is a checklist.

Do not edit any file. Return a numbered list, most serious first. For each item: the file and a short quote, why it boxes
the agent or looks written for a test, and how the same intent could be taught as judgment instead. End with one line:
NO FINDINGS if the list is empty, otherwise FINDINGS.
