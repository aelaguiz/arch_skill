# AIM Account Context

Use this reference only when the user asks for safe AIM account context or an
account-aware new Prime root. AIM does not own Prime session inventory or task
status.

Every command here is capability-gated. If the selected installed AIM/Prime
build does not advertise the brief status, journaled create/status, descriptor
preconditions, or root-captured labels, report the limitation. Do not recreate
the transaction in skill prose or scripts.

## Keep the authority planes separate

| State | Owner | Safe interpretation |
|---|---|---|
| account record | AIM | credential authority; never read directly for session control |
| current configured projection | AIM target | candidate descriptor for future roots, not a root fact |
| last selected label | AIM journal/receipt | historical selection, possibly stale |
| root-captured configured label | Prime admission record | label actually captured before first provider use |
| root bound label | Prime durable session | account actually resolved and pinned after provider use |
| child binding | Prime root tree | inherited from root, not independently selected |

Labels are not credentials or stable proof of underlying identity. Public output
may show bounded provider/source/label fields only. Never return provider IDs,
identity fingerprints, versions, tokens, raw Redis records, `auth.json`,
descriptor/backup paths, helper output, environment, or credential files.

## Read-only account context

When advertised, use only the product-owned fixed view:

```bash
aim prime status --brief-json
```

Report these separately:

- coordination/managed/installed/owned/conflict readiness;
- `pathConflict` or ownership conflict;
- validated current `configuredBinding` for future roots;
- persisted `lastSelectedBinding` with its historical provenance;
- Prime root-captured configured labels and actually bound labels from the
  explicitly authorized Prime list variant.

Do not call AIM status “session status.” Do not join mutable current AIM state
onto a root and present it as that root's configuration.

## Exact account-aware create

Use only the journaled owner transaction:

```bash
aim prime create --request-json - < validated-aim-create-request.json
```

The verb-specific typed request follows installed help and must include a
caller-stable operation ID, exact owned target path, provider, exact label or
`auto`, preserve-other-provider policy (true by default), and the Prime
socket/cwd/session configuration. The model prompt is not part of the AIM
transaction.

Before dispatch, disclose that a committed create intentionally leaves the
selected global future-root projection in place. Require exact account intent,
preserve-other-provider intent, target path, Prime create target, and
root-captured descriptor precondition. A path/ownership/capability/source-dist
conflict must fail before writes or launch.

The owner command, not this skill, must hold its transaction mutex, journal the
transition, project the descriptor, invoke Prime create with the same stable
operation identity, obtain the root's captured labels and active/durable
identity, and commit or roll back. Never compose `aim prime use` followed by
`prime-agent create`.

After a committed root receipt, send the brief separately with Prime `input`.
The create receipt can prove root-captured configured labels; only later
provider use can create actually bound labels.

## Recover an uncertain create

If the response is lost or a connection drops, query the same operation ID:

```bash
aim prime create status --request-json - < validated-aim-create-status-request.json
```

Interpret owner outcomes without replay:

- `aborted_no_effect`: no descriptor/root effect;
- `rolled_back_no_root`: descriptor restored and no root admitted;
- committed: observe the stored root and projection receipt;
- `partial_effect`: remaining global projection effect is named; separate
  human-authorized repair is required;
- `conflict_uncertain`: evidence conflicts; no retry, rollback, prompt, or
  cleanup is automatic.

Never replace a lost operation ID with a new create attempt.

## Resume and excluded AIM mutations

Exact noninteractive resume is Prime-owned. Use Prime's exact durable resume
contract so the root preserves its admission-time configuration and persisted
binding. Do not use AIM resume as the machine-control lane.

Do not use these as hidden prerequisites or substitutes:

- `aim prime use` or fixed-flavor `run` for exact creation;
- plain or rotating AIM resume;
- automatic account rotation/rebinding;
- identity-extension install/update;
- login, reauthentication, account repair, uninstall, native-auth replacement,
  Redis mutation, or credential inspection.

Those are separate account/extension mutations requiring their own explicit
request and owner receipt. In particular, rotation is outside v1: a fork with
selective credential reset is not same-session resume.

## Identity stability

A safe Prime owner stores a private admission-time expected identity for each
managed provider and restores it across exact resume. Same-label replacement
must either preserve that identity or fail `identity_conflict`; public output
remains labels-only. If the selected build lacks this fail-closed behavior, do
not claim identity-stable account-aware resume.
