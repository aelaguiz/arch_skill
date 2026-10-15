# Lab interfaces

The contract between the simulator and fixtures (one builder) and the runner, graders and baseline (another builder).
The design and every number live in `docs/hill-climb-skill-2026-10-14/PLAN.md` (section 6); this file fixes the
function names, file formats and paths the two halves share. If a builder must change something here, it adds to this
file and says so in its report; it never changes a part the other builder owns without saying so.

Python 3.9 or later, standard library only. Tests use `unittest` and run with:

```
python3 -m unittest discover -s evals/hill-climb/tests -t evals/hill-climb
```

so modules import as `sim.world`, `sim.cli`, `fixtures`, `runner.transcript`, `graders.common`, `baselines.thompson`.

## Folders of one run

- `<lab_root>` is `~/hill-climb-lab` on the Mac Studio, `~/.cache/hill-climb-lab` when running on this Mac.
- `RUN = <lab_root>/runs/<batch>/<run_id>/` holds `work/` (the agent's folder), `stream.jsonl`, `watch.jsonl`,
  `stderr.txt`, `session.json` and `grade.json`.
- `HIDDEN = <lab_root>/hidden/<run_uuid>/` (outside `RUN`) holds:
  - `state.json`: the simulator's whole state (format owned by `sim/world.py`);
  - `sim_actions.jsonl`: one line per agent-facing `sim`, `notify` or `gws` call:
    `{"wall_time": <epoch float>, "sim_time": "<ISO>", "argv": [...], "exit": <int>, "stdout_head": "<first 500 chars>"}`;
  - `outbox.jsonl`: one line per `notify`: `{"wall_time", "sim_time", "kind", "payload"}` (payload parsed from `--json`,
    or the raw string if it does not parse);
  - `initial_workbook/`: a copy of `work/workbook/` exactly as the fixture left it (may be empty or missing for setup runs);
  - `meta.json`: `{"kind": "scenario" | "world", "scenario": "V08" | null, "world": "W1", "seed": 101,
    "now": "<ISO>", "prompt": "<prompt>", "lab": "<absolute path of evals/hill-climb>"}`.
- `work/` holds `README.md`, `history.csv` (when the world or scenario has one), `legacy/` (V20), `reports/` (V26's
  earlier report), `workbook/<Tab>.csv` (fixture scenarios), and `bin/sim`, `bin/notify`, `bin/gws` (executable `/bin/sh`
  wrappers). The runner adds `.claude/skills/` (`hill-climb`, `prompt-authoring`, `_shared`, `readable-reports`).
- A role test's `HIDDEN/previews.json` maps the critic's labels to items (`{"A": "it_0013", "B": "it_0001"}`), and its
  `RUN/case.json` (written after the session) keeps the case, the labels and the facts its brief was filled with.

Times are ISO 8601 UTC with seconds and `Z` (`2026-11-08T00:00:00Z`) everywhere the lab writes them.

## `sim/world.py` (owned by the simulator builder)

```python
class World:
    @classmethod
    def load(cls, hidden: Path) -> "World": ...
    def save(self) -> None: ...
    now: datetime                      # simulated time, UTC
    config: dict                       # the W*.json contents
    items: dict      # id -> {"requested": {attr: value}, "attrs": {attr: value}, "text": str,
                     #        "quality": "specific" | "neutral" | "generic", "built_at": ISO}
                     #        W5 (`partial_builds`) adds "made_from": parent id | None and "drawn": [attrs drawn]
    campaigns: dict  # id -> {"item": id, "status": "live" | "paused" | "rejected" | "exhausted",
                     #        "budget_events": [[ISO, daily_budget], ...], "launched_at": ISO | None}
    posts: dict      # W3 only: id -> {"item": id, "slot": ISO, "status": "scheduled" | "done"}
    def hourly(self, campaign_or_post: str) -> list:
        """[{"hour": ISO, "clicks": int, "conversions": int, "platform_conversions": int, "spend": float,
             "app_arrivals": [[ISO, int], ...], "target_share": float}] for a campaign; for a W3 post one entry
             with "follows", "reach", "platform_follows", "target_share"."""
    def type_of(self, attrs: dict, names=None) -> str:  # "attr=value|..." over all attributes (or `names`), in order
    def long_run_rate(self, attrs: dict, quality: str) -> float:  # paid worlds: excludes novelty, fatigue, weekday
    def expected_follows(self, attrs: dict, quality: str, slot_multiplier: float = 1.0) -> float:  # W3
    def truth(self) -> dict:
        """{"best_type": str, "best_rate_specific": float (W3: best follows at multiplier 1.0, specific text),
            "type_rates": {type: rate with neutral text} (W3: "type_follows"), "attributes": [...],
            "type_attributes": [...], "cpc": float, "cap": int, "money_received": float}
        Types are written over `type_attributes`: every attribute, except W5's three that move the rate."""
    def faults(self) -> list:  # [{"kind": "build" | "tracking" | "delivery", "target": id, "from": ISO, "to": ISO, ...}]
    def comments(self, campaign_or_post, since=None, until=None) -> list:  # [{"hour", "kind", "text"}]; [] without
                                                                          # a `reception` (W2, W4)
    def saves_hides(self, campaign_or_post, since=None, until=None) -> tuple:  # (saves, hides)
    def balance(self) -> float
```

The grader treats `World` as read-only.

## `sim/cli.py` (owned by the simulator builder)

```
python3 <lab>/sim/cli.py sim --hidden HIDDEN <command> [args]      # what work/bin/sim runs
python3 <lab>/sim/cli.py notify --hidden HIDDEN --kind K --json J  # what work/bin/notify runs
python3 <lab>/sim/cli.py gws [anything]                             # prints the unavailable line, exit 1
python3 <lab>/sim/cli.py simadmin --hidden HIDDEN init --world W --seed S [--no-faults] [--money M] [--start ISO]
python3 <lab>/sim/cli.py simadmin --hidden HIDDEN advance --hours H
python3 <lab>/sim/cli.py simadmin --hidden HIDDEN grant AMOUNT
python3 <lab>/sim/cli.py simadmin --hidden HIDDEN truth            # JSON of World.truth()
python3 <lab>/sim/cli.py simadmin --hidden HIDDEN apply OPS.json
```

The agent-facing commands and their outputs are in PLAN.md section 6.2, with 13.2's additions: `sim comments TARGET
[--from ISO] [--to ISO]` (W1, W3, W5), saves and hides on every `sim report` row in those worlds, and in W5 partial
`--attrs`, `sim build --from ITEM [--attrs JSON] [--text TEXT]` and a manifest that ends with `Made from: ...`. `sim
preview LABEL` exists only where a role test wrote `HIDDEN/previews.json`. Every agent-facing call appends to
`sim_actions.jsonl` (simadmin calls do not).

## `fixtures.py` (owned by the simulator builder)

```python
def build_scenario(scenario: str, run_dir: Path, hidden_dir: Path, lab: Path, python: str = sys.executable,
                   folder=None, kind: str = "scenario") -> dict:
    """Builds RUN/work and HIDDEN for scenario "V01".."V30" from scenarios/<id>/fixture.json (or from `folder`, a role
    test's case, with meta kind "role"); returns the meta dict written to HIDDEN/meta.json."""
def build_world(world: str, seed: int, run_dir: Path, hidden_dir: Path, lab: Path, python: str = sys.executable) -> dict:
    """Builds a backtest's day-0 folder (README.md, history.csv, wrappers, no workbook) for world W1..W5."""
def write_wrappers(work: Path, hidden: Path, lab: Path, python: str) -> None: ...
def reads(test: tuple, comparison: tuple, history: list) -> dict:
    """The three read methods of PLAN.md 6.4 for (k, n) pairs: {"normal": p, "flat": p, "past_prior": p}."""
```

## `runner/` and `graders/` (owned by the runner builder)

```python
# runner/claude_run.py
def run_session(work: Path, prompt: str, label: str, run_dir: Path, budget_usd: float, timeout_s: int,
                install_skill: bool, repo: Path) -> dict:
    """One isolated headless session through aim (PLAN.md 6.10). Writes RUN/stream.jsonl (arrival-stamped),
    RUN/watch.jsonl (via runner/watch.py), RUN/stderr.txt and RUN/session.json
    {"exit", "timed_out", "cost_usd", "label", "started", "ended"}; returns the session.json dict."""

# runner/run_roles.py (layer 2b): CASES, prepare(case, trial, run_dir, hidden_dir, repo) -> {"brief", "braces",
#   "facts", "labels"}, grade_case(run, case, prepared) -> [check]; summary.json and summary.md like run_scenarios.py

# runner/watch.py: polls work/workbook/ every 0.2 s; one line per change in RUN/watch.jsonl (the Overview tab's key
# column is `item`):
#   {"t": <epoch>, "file": "Tests.csv", "added": [{row}], "changed": [{"key": k, "before": {row}, "after": {row}}],
#    "removed": [{row}]}

# runner/transcript.py
def parse(stream_path: Path) -> "Transcript":
    """Transcript.calls: [{"id", "name", "input", "parent_id", "t_use", "t_result", "result_text", "depth",
    "is_error"}]; Transcript.final_text; Transcript.cost_usd; Transcript.agent_calls (Agent/Task calls of the main
    agent)."""

# graders/common.py
# COLUMNS: what every workbook must hold (PLAN.md 4.7); EXTRA_COLUMNS (Library and Tests `coding`, Tests `made_from`,
# `recipe`, `checks`, `read`, `decision`, Results `signals`) and the Overview tab (item, value, as_of) are accepted
# anywhere and needed only by V25 to V30; CHARTER_FIELDS holds 29 fields, `reporting` among setup's.
def load_run(run_dir: Path, hidden_dir: Path) -> "Run": ...
# scenarios/VNN/grade.py
def grade(run) -> list:  # [{"name": str, "pass": bool, "evidence": str}]
```
