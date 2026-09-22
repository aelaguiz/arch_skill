# Nightly disk cleanup

Each job runs one AIM-managed Codex session. **Studio: GPT-5.6 Terra, high.**
**Home and both M3 Macs: GPT-5.6 Sol, medium.**
This is routine filesystem housekeeping with host-specific instructions. There
is no child-agent fan-out or automatic switch to Astra. Computer-use is disabled
for these shell maintenance jobs to prevent an unrelated desktop helper from
surviving a run. Each run has a 20-minute
deadline and records the real process exit status plus measured free bytes.

| SSH target | Time, America/Chicago | Skill | Volumes and maintenance target |
| --- | --- | --- | --- |
| `agents@amirs-mac-studio` | 01:15 | `mac-studio-disk-cleanup` | Data volume, 150 GB available |
| `home` | 01:45 | `home-disk-cleanup` | Root, 150 GB; each mounted data drive, 10% available |
| `amirs-m3-max-new` | 02:15 | `disk-cleanup` | Data volume, 150 GB available |
| `amirs-m3-36gb` | 02:45 | `disk-cleanup` | Data volume, 150 GB available |

Targets guide cleanup; they do not authorize deleting unique work to force a
number. Recurring retention runs even above target. Expired AIM snapshots and
rotated diagnostic logs have seven-day retention; large eligible text logs keep
a recent tail; completed cleanup reports have fourteen-day retention. Source,
active builds/training, useful models, current credentials, persistent service
data and current device work remain protected. The home skill uses policy
catalogs and run metadata to distinguish throwaway training/test output from
retained policies, without loading policy payloads. Missing data mounts are
skipped, so cleanup cannot accidentally operate on the directory underneath.

## Source and installed files

Mac Studio reuses the existing `com.funcountry.agents_host.nightly_disk_cleanup`
LaunchAgent and the launcher/mission in
`~/workspace/agents/deploy/mac/host_runner/`. Its operations and original
incident records are in that repository's `docs/MAC_STUDIO_DISK_CLEANUP*.md`.
Do not install a second timer there.

The other three hosts use [nightly_disk_cleanup.sh](../scripts/nightly_disk_cleanup.sh),
installed as `~/.local/bin/nightly-disk-cleanup`. Their saved missions and native
scheduler definitions are in [scripts/nightly_disk_cleanup](../scripts/nightly_disk_cleanup/).
The installed mission is `~/.config/disk-cleanup/mission.md`.

On `home`, the timer and service are under `~/.config/systemd/user/`. Lingering
is enabled, the timer is persistent, and the service owns its process group.
On each M3, the LaunchAgent is
`~/Library/LaunchAgents/com.amir.nightly-disk-cleanup.plist` in `gui/501`.
Mac Studio uses `gui/502`. Mac timers follow the host's Chicago timezone and
require that user's LaunchAgent session; a sleeping/offline machine cannot
perform cleanup until it is available. Native schedulers prevent overlap.

## Inspect or run

On `home`:

```sh
systemctl --user list-timers nightly-disk-cleanup.timer
systemctl --user start --no-block nightly-disk-cleanup.service
systemctl --user show nightly-disk-cleanup.service -p Result -p ExecMainStatus -p MainPID
```

On either M3:

```sh
launchctl print gui/501/com.amir.nightly-disk-cleanup
launchctl kickstart gui/501/com.amir.nightly-disk-cleanup
```

For the Studio, substitute `gui/502/com.funcountry.agents_host.nightly_disk_cleanup`.
Do not use `kickstart -k` to interrupt an in-progress cleanup.

Latest reports on home/M3 are `~/.local/state/disk-cleanup/latest/`; Studio uses
`~/.local/state/mac-studio-disk-cleanup/latest/`. Read `final.md`, `summary.json`
and `exit-code`. The action manifest records individual removals. No `exit-code`
means unfinished; nonzero means failure even if cleanup already wrote a report.
`error.log` and `events.jsonl` explain the failure. These files are private and
should not be copied wholesale into public reports.

Stop only this job with `systemctl --user stop nightly-disk-cleanup.service`
on home, or `launchctl kill SIGTERM <domain/label>` on a Mac. Verify task-owned
descendants exited. To disable the timer, use `systemctl --user disable --now
nightly-disk-cleanup.timer` or `launchctl bootout <domain/label>` respectively.
The installed sources remain available for reinstallation.

## September 22 deployment evidence

The complete fleet validation, configurations and account-selection repair
patch are saved in Amir's `psagentspace` checkout at
`_artifacts/2026-09-22-fleet-disk-cleanup/`. The original Studio incident and
first validation are in `_artifacts/2026-09-21-mac-studio-disk-cleanup/`.
The first Studio validation used Astra xhigh. After Amir requested an appropriate
routine model, all jobs were configured for Sol medium. Two Studio Sol runs
ended with model-capacity errors. A Terra medium check proposed removing a
live Camofox runtime after an inconclusive activity probe and was stopped
before that deletion. Its known live owner is now explicit in the host map,
incomplete probes must defer deletion, and the Studio uses Terra high for this
more complex service host. These are explicit deployment choices, not automatic
fallbacks. Other hosts remain on Sol medium.

Stopping the original Studio launcher exposed a cancellation gap: its timeout
child could outlive the shell. Both launchers now forward termination to that
owned process and record interruption. A real signal test verified exit 143,
a finished record, and no remaining fixture children. The initial M3 Max scan
freed 51.5 GB but exceeded its 20-minute limit while finishing the report; its
recurring brief now reuses the saved inventory, targets 150 GB of headroom,
and reserves three minutes for verification/reporting.

The M3 36 GB initially could not start because AIM tried to project a newer but
still expired current credential before choosing a healthy account. A small
local repair in `~/workspace/aimgr/src/targets/codex-cli.js` skips that expired
projection and permits normal pool selection. No credentials were revoked or
reauthenticated. Its regression test failed before the fix and passed after it;
the saved patch includes both source and test. This host-local repair is not
yet an upstream AIM commit, so preserve it during an AIM checkout update.
