# `check` Mode

`check` is the suite-only read-only checker used by the installed Stop hook. Do not advertise it as a public mode.

## Goal

Look at the current truth for the literal waited-on condition and say whether it is satisfied yet.

## Hard rules

- Stay read-only.
- Use the literal `check_prompt` from the invocation. Do not swap in a canned checker or service-specific shortcut.
- Keep the answer grounded in concrete current evidence.
- Return structured JSON only.

## Output contract

Return exactly:

```json
{
  "ready": false,
  "summary": "The waited-on condition is still false.",
  "evidence": [
    "Concrete fact 1",
    "Concrete fact 2"
  ]
}
```

Requirements:

- `ready` is `true` only when the waited-on condition is actually satisfied now.
- `summary` is one short grounded punchline and must not be blank.
- `evidence` is a short list of concrete facts that justify the decision.
- Do not return markdown, prose framing, or extra keys.
