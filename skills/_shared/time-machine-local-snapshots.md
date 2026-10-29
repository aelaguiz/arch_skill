# Time Machine's local snapshots and free space

Read this before measuring free space on a Mac with Time Machine on (`tmutil destinationinfo` names a drive). As of
October 28, 2026 that is the Mac Studio (drive T7), the M3 Max and Amir's laptop (each a drive named Elements). The
M3 36 GB has none.

## What they are

Each backup (hourly when backups keep up; every three hours or so on a disk that churns faster than the drive copies) starts with a snapshot of the internal disk: a frozen picture of every file at that moment, which
copies nothing when taken. Time Machine copies what changed from that snapshot to the backup drive, then keeps the
snapshot on the internal disk for 24 hours, so a laptop away from its drive can still restore the last day.

A snapshot costs space only as files change after it. A deleted or overwritten file's old data stays on the disk until
the last snapshot holding it is gone. So the internal disk carries, beyond its live files, everything deleted or
rewritten in the last 24 hours. Where agents and CI churn builds, checkouts and app installs all day, that is a lot,
and it never goes away, because each new hour's snapshot fills with that hour's churn. On October 28, deleting the
snapshots the backup drive already had freed 187 GB on the Studio (from 26 GB free to 214 GB) and 104 GB on the M3
Max, whose disk had been 100% full.

## What it means for a cleanup

- **Deleting doesn't raise free space for up to a day.** On October 26 an agent deleted 101 GB of videos on the
  Studio and free space went from 19.23 GB to 19.20 GB. The deletion worked; the snapshots were holding the data. Don't
  read an unmoved number as a failed deletion, and don't go looking for something else to delete to make it move.
- **The free space that counts is what tools see:** `df -k /System/Volumes/Data`. Xcode, Gradle, Docker, CI and
  agents fail against it. Finder and About This Mac show a bigger number (macOS's "available for important usage"),
  which adds other space macOS calls purgeable. It is not a measure of the snapshots: on October 28 it stayed exactly
  164 GB above `df` on the Studio before and after 187 GB of snapshots were deleted. macOS reports no size for local
  snapshots; what deleting them frees is the only measure.

- **Deleting a cache that comes straight back makes things worse for a day.** CI rebuilds a cleared Go or Gradle cache
  on its next job while the snapshots still hold the old one, so the disk carries both. Space comes from what is done,
  not from what is in use.
- **macOS deletes snapshots itself only when the disk is nearly out of room**, and not soon enough to help: the Studio
  ran a week at 14 to 46 GB free with every snapshot kept.
- **Leaving folders out of Time Machine doesn't change this.** An exclusion only stops a folder being copied to the
  drive; the snapshot is of the whole volume and holds it anyway. A separate APFS volume that Time Machine skips gets
  no snapshots at all (`tmutil localsnapshot` snapshots only the volumes it backs up; the Studio's policy drive is
  skipped and has none).

## Deleting snapshots the drive already has

A local snapshot older than the drive's newest completed backup is a second copy of a point the drive already holds,
except the hours the drive skipped while a long backup ran. Amir, October 28, 2026, asked whether cleanups should
delete those once the drive has the same hour: "sure". So a cleanup on a Mac with Time Machine does it:

1. Read the drive's newest completed backup: `tmutil latestbackup` (its folder name is the local time, for example
   `2026-10-28-183814.backup`).
2. List the local snapshots: `tmutil listlocalsnapshots /`.
3. Keep the two newest local snapshots, whatever their dates: a running or next backup works from them. Delete each
   other one dated before the newest completed backup, by its date: `tmutil deletelocalsnapshots 2026-10-28-142153`.
   It needs no password on the M3 Max; on the Studio it also runs under `sudo -n`.
4. Measure `df` before and after, and report both and how many snapshots went.

If the drive's newest completed backup is old (a laptop away from its drive, or backups failing), nothing qualifies,
and the local snapshots are the only copy of the hours since: leave them, and report the backup's state.

## A backup also changes what a wrong deletion costs

With a healthy backup, a folder deleted by mistake comes back from the drive: from any hour of the last day, and from
any day of roughly the last month while the drive has room. Check that the drive's newest backup completed recently
before relying on it (`tmutil latestbackup`, or `diskutil apfs listSnapshots <drive mount point>`). A backup that has
been failing is the first thing to report, and until it is fixed every deletion is final.
