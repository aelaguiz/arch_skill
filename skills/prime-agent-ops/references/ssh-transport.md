# SSH Transport

SSH carries bytes to the same public host-local Prime/AIM owner commands. It is
not a daemon federation, authorization layer, socket proxy, or generic remote
administration lane.

Remote v1 is noninteractive only. Do not attach, allocate a PTY, launch a TUI,
answer extension UI, create tmux ownership, forward a socket, or fall back to a
local command.

## Approve and verify the destination

Require the user to approve the exact SSH host/alias before connecting. Pass it
as one local `ssh` argv item. Reject a destination containing leading `-`, NUL,
control/newline, whitespace, or shell metacharacters. Do not discover targets
from AIM, Tailscale, SSH config, prior sessions, or a network scan.

Inspect effective SSH configuration first:

```bash
ssh -G -- operator@prime-lab.example
```

Present the effective user, hostname, proxy/jump, identity file, and configured
remote-command behavior. SSH config is evidence, not self-authenticating user
intent. If it changes the approved destination materially, stop and clarify.

Use fixed, value-free preflight commands to verify hostname, OS user, HOME, OS,
and the approved absolute launcher. For example:

```bash
ssh -T -- operator@prime-lab.example '/bin/hostname'
ssh -T -- operator@prime-lab.example '/usr/bin/id -un'
ssh -T -- operator@prime-lab.example '/usr/bin/printenv HOME'
ssh -T -- operator@prime-lab.example '/usr/bin/uname -a'
ssh -T -- operator@prime-lab.example '/opt/prime/bin/prime-agent --help'
```

Run fixed `prime-agent status --json` only when the user authorized
**full-machine** Prime discovery. Omit it for an explicit-socket request; use
the fixed structured per-socket list owner form instead.

Treat paths above as synthetic. Use only an operator-approved, owner-safe
absolute launcher path with no shell metacharacters, and verify its help,
version, lane, and capability surface. Noninteractive SSH can have a different
PATH; never source arbitrary profiles or silently choose another build.

Preflight writable agent/session/runtime directories only through a fixed
product-owned owner surface when available. Do not run arbitrary repair or
permission commands.

## Fixed structured-stdin rule

For every remote verb with dynamic values, the remote command string contains
only the approved absolute launcher, one allowlisted verb, and fixed
`--request-json -` tokens. Put socket, identities, cwd, name, model/provider,
account expectation, mode, and payload only in the validated bounded JSON
stdin document.

Capability-gated examples:

```bash
ssh -T -- operator@prime-lab.example   '/opt/prime/bin/prime-agent list --request-json -'   < validated-list-request.json

ssh -T -- operator@prime-lab.example   '/opt/prime/bin/prime-agent input --request-json -'   < validated-input-request.json

ssh -T -- operator@prime-lab.example   '/opt/prime/bin/prime-agent create --request-json -'   < validated-create-request.json

ssh -T -- operator@prime-lab.example   '/opt/aim/bin/aim prime create --request-json -'   < validated-aim-create-request.json
```

The same rule applies to public `commands`, `send`, `rename`, and `stop` forms.
Use the installed verb's exact published request schema; unknown keys, wrong
types, control characters, and oversize values must fail before dispatch. Do
not guess schema keys or invent a generic operation envelope.

Build the request with a typed JSON facility or a reviewed local file. Do not
hand-concatenate values into a remote shell string, inline a dynamic here-doc,
interpolate a payload into an SSH command, or depend on nested quoting.
Potentially hostile text—leading dashes, quotes, dollar/command substitutions,
backticks, Unicode, and newlines—must arrive only as JSON stdin bytes.

If the installed owner verb lacks `--request-json -`, remote operation for that
verb is unsupported. A local argv command, raw list, raw protocol call, copied
script, or attached UI is not a remote fallback.

## Read and write boundaries

Ordinary remote inventory uses only:

- static `prime-agent status --json` for an explicitly authorized
  `full_machine` inventory, never an `explicit_sockets` request;
- product-owned Prime `list --request-json -` requesting the brief view for
  each in-scope exact socket;
- product-owned AIM brief status when account context is explicitly needed.

Never send raw list/transcript output across the remote lane by default. A
remote sensitive-content workflow requires a separately designed and
explicitly authorized owner surface; this skill does not emulate it.

For mutation, the JSON request must carry the exact expected build/generation
and lifecycle-appropriate active/durable precondition. Re-resolve immediately
before dispatch. The remote shell never receives dynamic locators or payload
as command text.

## Capture and interpret the receipt

Require one typed JSON response on stdout and fixed value-free errors on stderr.
Record:

- approved and effective destination;
- verified hostname/user/HOME;
- exact fixed remote command identity;
- local SSH exit status;
- parsed owner response/action/operation ID;
- whether dispatch could have reached the owner;
- fresh post-state evidence.

Do not echo the request or payload in logs. Keep stdout/stderr separate. Treat
any value-bearing or malformed stderr as an owner-contract problem and avoid
relaying it wholesale.

A connection failure before dispatch is rejected/unreached. A drop after bytes
may have reached the owner is `uncertain`. Re-run read-only inventory or the
same operation-status lookup; never replay the mutation blindly. No remote
failure may cause local execution.

## Never weaken host security

Do not disable host-key checking, accept a changed key automatically, use sudo
implicitly, copy/chmod/forward the Prime socket, expose it over TCP, or relax
owner permissions. Stop on host-key, effective-user, HOME, path-ownership,
launcher-lane, build, schema, or descriptor conflict.
