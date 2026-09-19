# Catalog Slice: Pictures

Applies when the change touches user-visible code and the target carries
screenshots, a mock, or both. Needs the images themselves, opened, the diff,
and the ask. Both checks need a reviewer that can open images; where it cannot,
both return could not evaluate rather than clean. V-12 asks whether the images
exist, render, and show the claimed state; V-13 asks what they show against the
mock, so a missing image set is V-12's alone.

## V-12 Before and after images missing or wrong

Question: Do the images on this change exist, render, and show the states they
claim?

Needs: the PR body and its images, opened; the diff, to know whether
user-visible code changed; the ask, for what the journey is; the worktree where
the screenshots live.

Read: Open the images, not the references. Four comparisons, each against
something different. Rendering: the image markup against what the PR view
actually displays, since a path or an unresolved link leaves the reviewer
seeing nothing. Identity: the before file against the after file, and each
image in the set against the others; an identical pair, or one image repeated,
means nobody opened them. Compare files, never pixels. Recency: an image that
predates the diff cannot be an after. Content: each image against the state it
claims to show, because a loading screen, an empty state or a QA screen is not
the changed screen. The before half must be the prior version stood up and
shot, from the mainline head rather than an interim branch state, never
described from memory.

Block when: a change touching user-visible code carries no embedded images;
images are referenced by path or by a link that does not render; the before and
after are identical files, or the set is one image repeated; an image predates
the change or shows a loading or empty state instead of the claim; or the
before half is prose.

Do not block when: nothing user-visible changed; the repository is a hobby
project or throwaway probe; the images are present and complete and the only
quarrel is pixel-level fidelity, which is de-rated here and everywhere. What
the images show against the mock is V-13's. Screenshots written to a system
temp directory are a location finding, not missing evidence.

Examples:

- **[REQUIRED REPAIR] Every screenshot on the change is the same image.**
  Compared the images against each other, which is what showed that nobody had
  opened them. Repair target: capture each state the body names.
- **[REQUIRED REPAIR] The one screenshot is the loading screen.** The single
  image showed the application loading, not the changed screen. Compared the
  image content against the state being claimed. Repair target: shoot that
  state.
- **[REQUIRED REPAIR] The before half was written from memory.** A set of known
  breakages needed the application stood up at the prior version and again at
  the current one, each place shot in both. Repair target: stand the mainline
  head up and capture it.

## V-13 The built screen not itemized against the mock

Question: Did someone open the built screen and the mock together and write out
the differences?

Needs: screenshots of the built screen, opened; the linked mock or spec; the
diff, for copy strings and component choices; the ask, for what was
commissioned.

Read: Open the screenshot and the linked mock side by side and enumerate the
differences yourself, element by element, with copy strings included. The
deliverable is a difference list somebody wrote; "it matches the mock" is a
claim, and a comparison step whose output is a confirmation has the same shape.
Three comparisons. The built elements against the mock's elements, anchored so
a reader can find each one. The UI copy strings in the diff against the mock's
copy, since changed button and label text shows up only at that granularity and
needs a reason. And the source the screen was built from against the mock
actually linked, since building from an older image set is the same defect.
Where a mock was linked by name, open it: links assembled from names nobody
opened are worth no more than screenshots nobody opened.

Block when: a UI change claims to match the mock with no side-by-side artifact
and no enumerated difference list; copy strings in the diff differ from the
mock's with nothing authorizing the change; the screen was built from an older
image set rather than the linked mock; or a generated or rendered artifact is
delivered with no evidence anyone opened it.

Do not block when: the difference is pixel-level, since mocks explain intent
rather than coordinates and the application's own styles win over the design
file; nothing visual changed; the images are missing altogether, which is
V-12's finding and returns could not evaluate here rather than a second
finding. Never propose a pixel-comparison harness.

Examples:

- **[REQUIRED REPAIR] Built screen contradicts the spec it cites.** A rebuilt
  harness screen showed the player's own cards, disabled, where the spec and
  mocks called for a coach image. Repair target: rebuild to the spec and report
  the differences.
- **[REQUIRED REPAIR] Narrated as done, never diffed against the mocks.** A
  working build was put on the simulator and reported finished with no
  comparison against the approved mocks. Compared nothing, which was the
  finding. Repair target: itemize and save the list.
- **[REQUIRED REPAIR] Button copy changed with no stated reason.** Compared the
  mock's copy strings with the screenshot's, element by element. Repair target:
  restore the mock's copy or name what authorized the change.
