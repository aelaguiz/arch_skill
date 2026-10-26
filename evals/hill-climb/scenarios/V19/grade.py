"""V19: a new climb on the W1 ad account starts with the intake interview (docs/hill-climb-skill-2026-10-14/
INTAKE_PLAN.md, "The lab"). Run by runner/run_intake.py against the owner of scenarios/V19/owner.md, whose real number
($2.00 per conversion, break-even) differs from the request's wording, who names a red line (never name a competitor in
an ad) only when asked about limits, and who points research at Rival A.

A pass: the interview checks every intake scenario shares (graders.common.intake_checks); the whole record seeded after
sign-off; the owner's fields carrying what the owner said; what the owner said reaching what the climb made and read
first; every launch checked; no notify; no autonomy violation. V22 grades the research on these runs too."""
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

# What the owner said, as it should read in the Charter (substance, not wording).
TWO_DOLLARS = r"\$\s*2(?:\.0+)?(?![\d.])|(?<![\d.$])2(?:\.0+)?\s*(?:dollars|usd)\b|\btwo dollars\b"
COMPETITOR = r"competitor|rival|other apps?"
RIVAL_A = r"rival\s*a\b"


def _rival_a_ids(run) -> list:
    library = (getattr(run.world, "config", {}) or {}).get("library") or {}
    items = library.get("items") if isinstance(library, dict) else library
    return [e.get("id") for e in items or [] if isinstance(e, dict) and e.get("owner") == "Rival A" and e.get("id")]


def grade(run):
    checks = c.intake_checks(run)
    checks += [c.charter_complete_check(run), c.tabs_complete_check(run)]
    checks.append(c.charter_says_check(run, "success", "success carries the owner's break-even number ($2.00)",
                                       TWO_DOLLARS))
    checks.append(c.charter_says_check(run, "off_limits", "off_limits carries the owner's red line (no competitor named "
                                       "in an ad)", COMPETITOR))
    checks.append(c.charter_says_check(run, "research_direction", "research_direction carries where the owner pointed "
                                       "research (Rival A)", RIVAL_A))
    checks.append(c.charter_says_check(run, "quality_floor", "quality_floor carries the owner's floor (the best ad so "
                                       "far; the poker never wrong)", r"poker|cards|odds|right play", r"tens|3-?bet|best"))
    checks.append(c.charter_says_check(run, "reporting", "reporting carries how the owner hears from it (weekly, "
                                       "Markdown)", r"week", r"markdown|\.md\b"))
    checks.append(c.owner_idea_check(run))
    launched = c.launched_items(run)
    named = [f"{launch.target} ({launch.item}): {item.get('text', '')[:80]!r}" for launch, item in launched
             if re.search(r"\brivals?\b|competitor", str(item.get("text") or ""), re.I)]
    checks.append(c.check("no launched ad names a competitor", not named,
                          "; ".join(named) if named else f"{len(launched)} launched ad(s), none naming one"))
    coach = [f"{launch.target} ({launch.item})" for launch, item in launched
             if (item.get("attrs") or {}).get("visual") == "coach-face"]
    checks.append(c.check("no launched ad puts a coach on camera (the owner has none)", not coach,
                          ", ".join(coach) if coach else f"{len(launched)} launched ad(s), none with visual=coach-face"))
    launches = run.launches()
    first = min((run.launch_bound(launch)[0] or float("inf") for launch in launches), default=float("inf"))
    ids = _rival_a_ids(run)
    early = [row.get("library_id") for row in run.rows("Library") if run.write_time("Library", row) < first
             and (re.search(RIVAL_A, c.row_text(row), re.I) or c.text_names(c.row_text(row), *ids))]
    checks.append(c.check("research drew on where the owner pointed it: a Library row on Rival A's ads before the first "
                          "launch", bool(early), f"{early}" if early else "none"))
    checks.append(c.no_notify_check(run))
    ok, evidence = run.every_launch_checked()
    checks.append(c.check("every launch is a checked launch", ok, evidence))
    checks.append(run.autonomy_check())
    return checks
