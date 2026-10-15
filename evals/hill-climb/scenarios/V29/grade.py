"""V29: setup of the rich-coded video world from a plain request codes the medium richly: the Charter's `attributes`
codes at least 8 attributes with their values and at least 15 Library rows each carry values for at least 6 of them,
besides every check of V19 (PLAN.md 13.3)."""
import importlib.util
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from graders import common as c  # noqa: E402

# Prose and provenance hold no coding; the rest of a Library row (`coding`, `type`, `notes` and any column the climb
# added) may.
NOT_CODING = {"library_id", "kind", "source", "link", "owner", "content", "signal", "status", "legacy_ref",
              "written_at", "written_by"}


def _v19():
    spec = importlib.util.spec_from_file_location("hill_climb_grade_V19_for_V29", LAB / "scenarios" / "V19" / "grade.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.grade


def grade(run):
    checks = list(_v19()(run))
    coding = (run.workbook.charter().get("attributes") or {}).get("value") or ""
    names = c.coded_attributes(coding, run.world)
    checks.append(c.check("the Charter's attributes codes at least 8 attributes with their values", len(names) >= 8,
                          f"{len(names)} attributes with two or more values: {names}"))
    listed = (getattr(run.world, "config", {}) or {}).get("attributes") or []
    known = set(c.parse_coding(coding)) | {c.normalize_attr(a["name"] if isinstance(a, dict) else a) for a in listed}
    coded = []
    for row in run.rows("Library"):
        pairs = c.coded_pairs(" | ".join(v for k, v in row.items() if k not in NOT_CODING and v))
        values = [k for k, v in pairs.items() if k in known and v.strip().lower() not in c.UNKNOWN_VALUES]
        if len(values) >= 6:
            coded.append(row.get("library_id"))
    library = run.rows("Library")
    checks.append(c.check("at least 15 Library rows each carry values for at least 6 coded attributes",
                          len(coded) >= 15, f"{len(coded)} of {len(library)} Library rows carry 6 or more"))
    return checks
