# Catalog Slice: Agent And Prompt Surfaces

Applies when the diff touches prompts, skills, agent instructions, or workflow
configuration: a skill package, a prompt or agent definition file, a
repository-level instruction file, a reviewer or generator prompt, and the
scripts, metadata, and generated copies that ship beside them. These files are
live product surface and get the same reading as application code.

Needs the diff, the changed files at head, the version of the text before the
change, the request that asked for it, and the surfaces around it: peer skills
or prompts with overlapping triggers, the commands and files the text names, and
the install steps and runtime metadata that ship with the package.

Both checks read the changed text as the agent will meet it at runtime, with
none of the conversation that produced it. C-41 asks what the change takes away
from the agent's judgment. C-44 asks whether the surface still matches what
actually runs. Report each defect once, under the check whose comparison found
it.

## C-41 Judgment replaced by a rule, a script, or a gate

Question: Does this change take a decision away from the agent that the agent
should be making?

Needs: the diff of the changed instruction-bearing files and of any script,
runner, or controller the change adds; the text before the change; the request;
the pipeline the surface sits in, to see what already reviews the output.

Read: For every rule the change adds, ask what the agent decided at that point
before and what it now has to obey. The shapes are a quality decision reduced to
a threshold, a score, a count, or a keyword list; a checklist that has to be
satisfied in order; a template whose slots get filled; a script, runner, or
controller that owns the sequence of work and can refuse it; and an extra gate
appended to a pipeline that already reviews the same output. Separate mechanics
from judgment: parsing, counting, formatting, checking syntax, calling an API,
and assembling a command are deterministic and belong in a script, while
deciding whether work is good, which option fits, or whether something is done
is not. Then read every added absolute sentence as a cold reader who has none of
the history behind it — a short imperative of the "smallest change", "always ask
first", "never touch that" kind will be applied literally where it does the most
damage, either as a licence for a hack or as a reason to stop. Read the
deliverables the surface produces too: many items sharing templated prose mean
the template did the work instead of the agent.

Block when: the change converts a decision that needs judgment into a threshold,
a rule or keyword table, a scored gate, or a runner that owns the workflow; or
it adds an absolute phrase a literal reader would apply as a gate where the text
used to teach what good looks like.

Do not block when: the mechanics really are deterministic and the helper stays
inside them while the agent keeps the decision; the user asked for the gate, the
script, or the threshold; the artifact is a plan, specification, inventory, or
runbook, where being exhaustive and impossible to misread is the point; the
checklist is offered as an aid and the agent still owns the synthesis and may
depart from it with a reason. A surface that no longer matches what runs is
C-44. Where the new machinery is also most of the change for a small ask, its
size is C-08 and added verification machinery is C-36.

Examples:

- **[REQUIRED REPAIR] A qualitative selection replaced by a scoring gate.** The
  generator used to have the agent choose candidates on quality against
  described examples; the change scores counted features and rejects anything
  under a threshold, so the outputs converge on one shape. Compared what the
  agent decided before with what the threshold now decides. Repair target: teach
  what a good candidate looks like and let the agent choose, keeping the count
  as something it reads rather than something that refuses.
- **[REQUIRED REPAIR] A helper script became the owner of the workflow.** A
  script that existed to run a simulator now sequences the steps, refuses work
  taken out of order, and stops the run when a document is missing, so two
  agents can no longer work the same repository in parallel. Compared what the
  script does with the narrow mechanic it was written for. Repair target: return
  it to running the simulator and leave the sequence to the agent.
- **[REQUIRED REPAIR] A doctrine line a literal reader will apply as a gate.**
  The added rule tells the agent to make the smallest possible fix and to act
  only on things the user names; the first invites a hack over a real repair and
  the second leaves the agent stuck whenever nobody named anything. Compared the
  sentence a cold reader would obey with the lesson it meant to teach. Repair
  target: state the lesson with the reasoning behind it, so the agent can apply
  it to a case nobody anticipated.
- **[OBSERVATION] A counting helper is not a gate.** The added script counts
  items and prints them for the agent to read; nothing refuses work on the
  count, and the decision the count informs is still the agent's.

## C-44 An agent-facing surface that no longer matches what runs

Question: Would an agent that has only this changed surface and the repository
do the right thing?

Needs: the changed skill, prompt, agent definition, or instruction file; the
runtime it names — commands, files, skills, models, paths, helpers; its sibling
surfaces, including peers whose triggers describe similar work; the generated
copies, install steps, and runtime metadata that ship with it.

Read: Read the changed text the way the runtime agent meets it: with no memory
of this conversation and no access to anything the text does not name. Take each
thing it points at — a command, a file, a skill name, a model, a path, a helper
script — and check against the repository whether that thing is live, archived,
renamed, or gone. Then compare the surface with its siblings: two live surfaces
whose triggers describe the same job with no handoff between them leave routing
to chance, and a generated copy that can be edited apart from its source gives
one instruction two owners. Compare the runtime metadata, the install steps, and
the documentation with each other and with what the package actually contains.
Read the doctrine itself for what it assumes the reader knows: text that
explains a rule through the history of how it came about, a past incident, or a
conversation the agent cannot see gives the reader nothing it can act on.

Block when: a shipped surface depends at runtime on a file, command, or skill
that is archived or absent; two live surfaces claim the same work with no
boundary between them; a generated artifact and its source can disagree; the
runtime metadata, install steps, and documentation name different things; or the
instruction can only be followed by someone who was there when it was written.

Do not block when: the overlap is a documented handoff and each surface names
when it yields; the generated artifact is produced during the build from the
source and cannot be edited separately; the historical note sits in a document
whose job is to record history rather than in the text the agent runs on; the
named thing is live and you read it. Residue of a removed feature elsewhere in
code, configuration, or documentation is C-01; prose claiming more than the code
establishes is C-26; a second implementation of one job is C-04. Judgment taken
away from the agent is C-41.

Examples:

- **[REQUIRED REPAIR] Two skills claim one lane.** The changed description says
  this skill reviews any branch or a plan-backed implementation, while a peer
  skill already owns plan-backed implementation review and says nothing about
  yielding. Compared the two trigger descriptions against the work each package
  actually does. Repair target: narrow this trigger to the lane it owns and name
  the handoff to the peer.
- **[REQUIRED REPAIR] A shipped workflow calls an archived command.** The
  skill's steps invoke a command file that the same change moved into an archive
  directory, so a fresh install has a workflow whose second step cannot run.
  Compared each command the text names with what the package installs. Repair
  target: carry the step into the skill, or keep the command as a live part of
  the package.
- **[REQUIRED REPAIR] The installed copy and the source can drift.** The change
  edits the generated copy of a prompt that the install step also writes from
  its source, so the next install silently reverts it. Compared the generated
  file with the source it is produced from. Repair target: edit the source and
  regenerate.
- **[OBSERVATION] An overlap the two surfaces resolve themselves.** Two skills
  touch at one shape of request, and each description names the other and says
  which one takes it. Routing is decidable from the text alone.
