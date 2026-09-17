# Goal Loop Context Digest

Write or refresh a short restart-safe digest only when the user explicitly asks for it. Core doctrine and lifecycle live in references/controller-lifecycle.md. This document documents only the context-digest-mode additions.

## Goal

Write or refresh a short restart-safe digest only when the user explicitly asks for it.

## Digest contents

- North Star
- current best belief
- biggest uncertainty
- last completed bet
- next recommended bet
- any constraints the next operator must not forget

## Rules

Derive it from the controller and latest worklog entries.
Keep it compact.
Do not let the digest replace the controller or worklog.
