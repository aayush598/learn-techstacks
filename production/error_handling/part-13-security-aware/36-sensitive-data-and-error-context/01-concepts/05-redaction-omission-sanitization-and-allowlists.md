# Redaction, Omission, Sanitization, and Allowlists

> Part XIII · Chapter 36 · Sections 36.8–36.11 · _Estimated reading time: 18 min_
> **Prerequisite:** [Defining Sensitive Metadata](./01-defining-sensitive-metadata.md)

## In one sentence

Four controls secure error context: **omission** (never collect it), **redaction** (mask it before a
sink), **sanitization** (neutralize untrusted text in messages), and **allowlisting** (emit only
classified-permitted fields) — and you should reach for them in roughly that order of preference.

## Why this matters in production

Teams default to redaction because it feels like doing something, but redaction is the *weakest* of the
four: it depends on every sink remembering to call the redactor, and on the redactor recognizing every
sensitive shape. Omission cannot be forgotten; allowlisting makes leaks structural rather than
procedural; sanitization protects against the untrusted-input half of the problem. Using them together,
in the right order, is what makes "no sensitive data leaves" a verifiable property.

## The four controls compared

| Control | What it does | Strength | Fails when |
| ------- | ------------ | -------- | ---------- |
| **Omission** | Never collect the value | Strongest | Never (by construction) |
| **Allowlist** | Emit only permitted fields | Strong | A needed field is unclassified |
| **Sanitization** | Neutralize untrusted text | Medium | A new payload type appears |
| **Redaction** | Mask sensitive values | Weakest | A sink forgets; a shape is unknown |

Preferred order: **omit → allowlist → sanitize → redact.**

## Omission

Do not collect what you do not need. This is the cheapest and safest control:

```ts
// Omit: the secret/config/payload is never attached, so nothing downstream can leak it.
throw new ConfigError("CONFIG_INVALID", "The service is misconfigured.", {
  key: "STRIPE_SECRET",   // the config KEY name, not its value
});
```

## Redaction vs omission (the honest trade-off)

| Question | Omit | Redact |
| -------- | ---- | ------ |
| Is the value needed for debugging? | Usually no | Sometimes |
| Can every sink be trusted to redact? | — | Often no |
| Is the shape known and stable? | — | Sometimes |
| Compliance posture | Strongest | Audit burden |

Rule of thumb: **omit secrets and PAN; redact unavoidable third-party text** (which you cannot omit
because it is produced by someone else).

## Sanitization of messages

Sanitization handles the *untrusted text* problem — provider messages, driver text, and anything not
written by you:

```ts
function sanitizeText(input: string, maxLen = 256): string {
  return input
    .replace(/[\r\n\t]+/g, " ")          // no log-line forging
    .replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, "") // control chars
    .slice(0, maxLen)                     // bound size
    .trim();
}
```

For HTML sinks, escape; for headers, strip CR/LF; for JSON logs, rely on the encoder plus control-char
stripping. See [Chapter 34 §34.15](../../34-security-principles-for-error-handling/01-concepts/05-injection-dos-serialization-and-reflection.md).

## Context allowlists

An allowlist is a table of permitted fields per sink. Unknown fields are denied:

```ts
type Sink = "response" | "log" | "metric" | "tracker" | "dlq";

const CONTEXT_ALLOW: Record<Sink, string[]> = {
  response: ["code", "message", "requestId"],
  metric: ["code", "provider"],
  log: ["code", "class", "provider", "requestId"],
  tracker: ["code", "class", "provider", "requestId", "tenantId", "userId", "stack", "field", "rule"],
  dlq: ["code", "class", "requestId", "tenantId"],
};

function projectContext(context: Record<string, unknown>, sink: Sink) {
  const allowed = CONTEXT_ALLOW[sink];
  const out: Record<string, unknown> = {};
  for (const key of allowed) {
    if (key in context) out[key] = context[key];
  }
  return out; // anything not listed is dropped
}
```

Because the sink allows specific keys, a newly added context field (say `cardNumber`) is **denied by
default** — it will not appear in any sink until someone deliberately adds it to the allowlists.

## Safe serialization rules

| Rule | Why |
| ---- | --- |
| Serialize via allowlist, not the whole object | Deny unknown fields |
| Bound cause depth (e.g. 6) | Avoid cycles/unbounded chains |
| Bound string length | Avoid huge payloads |
| Never `JSON.stringify(err)` on a raw error | Circular refs, unknown internals |
| Sanitize any string that did not originate in your code | Untrusted text |
| Never deserialize error payloads with native parsers | Avoid gadget code (CWE-502) |

## Worked example — applying all four

```ts
function buildErrorContext(req: Request, principal: Principal) {
  // Omit: secrets, raw payloads, query strings are never collected.
  return {
    code: "PAYMENT_DECLINED",
    class: "upstream",
    provider: "stripe",
    requestId: req.id,
    tenantId: principal.tenantId, // classified sensitive; allowed only in dlq/tracker
    field: "card",
    rule: "declined",
  };
}

// Later, per sink:
const logLine = projectContext(buildErrorContext(req, principal), "log");
// -> { code, class, provider, requestId }  (tenantId and field dropped)
```

## Key data / numbers

- **CWE-209** (info in messages), **CWE-532** (sensitive info in logs), **CWE-117** (log injection),
  **CWE-502** (unsafe deserialization), **CWE-359** (private personal information).
- **Cause depth bound**: commonly 5–10; beyond that, truncate with a marker.
- **String length bound**: a few hundred bytes for messages is usually enough; longer values are
  truncated with a marker.
- **Allowlist over denylist**: the security principle that makes new fields safe by default.

## Real-world use case — Acme SaaS

Acme had a redactor that stripped emails and card-like numbers from log lines. An engineer added a new
`ssoSubject` context field (an opaque IdP identifier, treated as PII). The redactor did not know its
shape, so it passed through to logs. Fix: Acme moved from redaction-at-the-sink to an **allowlist context
builder**; `ssoSubject` was absent from every sink allowlist and therefore dropped automatically until
classified, and it was then added to the tracker only. The switch from denylist redaction to allowlist
projection eliminated the entire class of "new field leaks because the redactor didn't know it".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Omit + allowlist projection | New fields denied by default | Must classify needed fields | Default |
| Redaction pass only | Catches third-party text | Misses new shapes | Backstop |
| Full-object serialization | Easy | Leaks everything | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Omit secrets and PAN | Collect them and hope redaction runs |
| Project context via per-sink allowlist | Emit the whole context bag |
| Sanitize third-party text | Trust provider text as safe |
| Bound cause depth and string length | Serialize unbounded |
| Deny unknown fields | Allow all fields |

## Common mistakes

- **Redaction as the primary control.** It lags reality.
- **Denylist thinking.** New shapes leak.
- **No length/depth bounds.** Huge payloads and cycles.
- **Serializing raw errors.** `JSON.stringify(err)` risks cycles and internals.
- **Redacting only the response.** Logs and DLQ still leak.

## Checklist

- [ ] Is omission the default for secrets and PAN?
- [ ] Is context projected via a per-sink allowlist?
- [ ] Are untrusted strings sanitized (control chars, length)?
- [ ] Are cause depth and string length bounded?
- [ ] Are unknown fields denied?
- [ ] Is redaction used only as a backstop?

## Related

- [Defining Sensitive Metadata](./01-defining-sensitive-metadata.md)
- [Practical: Context Allowlist for Errors](../03-practical-examples/02-context-allowlist-for-errors.md)
- [Deep dive: Safe Serialization and Context Allowlists](../02-deep-dive/02-safe-serialization-and-context-allowlists.md)
- [Chapter 34 — Redaction Strategy](../../34-security-principles-for-error-handling/02-deep-dive/03-redaction-strategy.md)
- [Glossary](../../../GLOSSARY.md)
