# Deep Dive — Redaction Strategy

> Part XIII · Chapter 34 · Sections 34.5–34.6, 34.13–34.14 (mechanics) · _Estimated reading time: 20 min_
> **Prerequisite:** [Secrets, PII, and Tenant Leakage](../01-concepts/03-secrets-pii-and-tenant-leakage.md)

## In one sentence

A redaction strategy is **classify → redact at the source → allowlist-serialize → audit**: you tag
every field's sensitivity before it can enter an error, strip secrets where they are read, serialize
through an allowlist rather than a blocklist, and verify with automated scans.

## Why this matters in production

Redaction built as "a regex that removes things that look like secrets" fails constantly: it misses
new secret formats, over-matches real data, and runs *after* the value already reached six sinks.
Redaction is fundamentally a **data-classification** problem. If you do not know which fields are
sensitive, no regex will save you; if you do, an allowlist makes leaks structurally impossible rather
than merely unlikely.

## Core concept — a classification lattice

Label every value once, then let the label drive every sink.

| Class | Definition | Sinks allowed | Examples |
| ----- | ---------- | ------------- | -------- |
| **PUBLIC** | Safe for anyone | all | HTTP status, stable error code |
| **INTERNAL** | Safe for operators/engineers | logs, tracker, ops UI | class, retryable, provider name |
| **TENANT-CONFIDENTIAL** | Own-tenant only | tenant-scoped sinks | own resource ids, own quota |
| **SENSITIVE** | Must be redacted at all non-RBAC sinks | tracker (RBAC only) | tenantId, userId, internal errors |
| **SECRET** | Never stored anywhere except the vault | none | tokens, keys, passwords, PAN |
| **PII** | Regulated personal data | minimized; RBAC sinks | email, name, phone, IP |

Two hard rules fall out:

1. **SECRET never enters an error object at all.** It is not "redacted at the sink"; the code never
   reads it into the error.
2. **Allowlist, not blocklist.** For any sink, emit only fields whose classification permits that
   sink. New fields default to denied.

## Redact at the source, not at the sink

The single most effective pattern: **do not put the secret into the error in the first place**.

```ts
// ❌ The token is in the error; every sink must remember to strip it. One forget = breach.
throw new AuthError(`bad token ${token}`);

// ✅ The error never holds the token; sinks have nothing to strip.
throw new AuthError("INVALID_TOKEN", { tokenFingerprint: sha256(token).slice(0, 8) });
```

A fingerprint (a short, non-reversible prefix of a hash) gives operators a way to correlate "which
token" without ever storing the token. This is the difference between redaction and non-collection:
non-collection cannot be forgotten.

## Allowlist serialization

```ts
type Sensitivity = "public" | "internal" | "tenant" | "sensitive" | "secret" | "pii";

const FIELD_CLASS: Record<string, Sensitivity> = {
  code: "public",
  message: "public",
  class: "internal",
  retryable: "internal",
  provider: "internal",
  tenantId: "sensitive",
  userId: "sensitive",
  email: "pii",
  stack: "internal", // internal sinks only
};

const SINK_ALLOWS: Record<Sink, Sensitivity[]> = {
  response: ["public"],
  metric: ["internal"],       // plus bounded-cardinality rule
  log: ["public", "internal"],
  tracker: ["public", "internal", "tenant", "sensitive", "pii"], // RBAC sink, still no secret
};

function serialize(err: Record<string, unknown>, sink: Sink) {
  const allow = SINK_ALLOWS[sink];
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(err)) {
    const cls = FIELD_CLASS[k];
    if (cls && allow.includes(cls) && cls !== "secret") out[k] = v;
    // unknown fields are DENIED by default
  }
  return out;
}
```

Because **unknown fields are denied**, a newly added field cannot leak accidentally — it must be
classified and its class must permit the sink.

## Value-level redaction when non-collection is not possible

Sometimes the value arrives from a third party (a provider error, a webhook body) and cannot be
avoided. Then redact *statically* at the boundary where it is read:

```python
import re, hashlib

PATTERNS = [
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]+"), "Bearer [REDACTED]"),
    (re.compile(r"(?i)(sk|rk)_(live|test)_[A-Za-z0-9]+"), "[REDACTED_KEY]"),
    (re.compile(r"\b\d{13,19}\b"), "[REDACTED_PAN]"),            # card-like (PCI: never store)
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[REDACTED_EMAIL]"),
]

def redact(text: str) -> str:
    for rx, repl in PATTERNS:
        text = rx.sub(repl, text)
    return text
```

```text
Caveat: regexes are a *backstop* for unavoidable third-party text, never the primary control.
They will miss novel formats and can corrupt legitimate data. Prefer non-collection + allowlist.
```

## Handling nested causes and chains

Causes are where redaction is most often forgotten. When serializing a cause chain, apply the same
sink rules at every depth and **bound the depth**:

```ts
function serializeChain(err: unknown, sink: Sink, depth = 0, max = 6): unknown {
  if (depth > max) return "[cause chain truncated]";
  if (!(err instanceof AppError)) return "[non-app error ignored]";
  return {
    ...serialize(err as any, sink),
    cause: err.cause ? serializeChain(err.cause, sink, depth + 1, max) : undefined,
  };
}
```

Two rules: never serialize a raw `Error` (only sanitized app errors), and never walk unbounded (both
for leakage control and to avoid cycles).

## Auditing the strategy

Redaction is only as good as its verification.

1. **Static scan**: flag `err.stack`, `JSON.stringify(err`, request/header logging, and template
   strings containing variables in log calls.
2. **Canary test**: inject a synthetic secret and a synthetic PII value through every failure path in
   a test suite; assert neither appears in any sink output.
3. **Log sampling review**: periodically inspect a sample of production logs for values matching
   secret/PII patterns.

## Key data / numbers

- **PCI DSS v4.0 Req 3.3**: do not store sensitive authentication data after authorization; PAN must
  be rendered unreadable. Req 10 governs log access. Card-like numbers must never be logged.
- **GDPR Article 32**: appropriate technical measures (including pseudonymization) for personal data;
  Article 33 requires breach notification within **72 hours** if PII leaks.
- **CWE-532** (sensitive info in logs), **CWE-312** (cleartext storage of sensitive information),
  **CWE-359** (exposure of private personal information).
- **Fingerprint length**: a short hash prefix (commonly 8 hex chars) is enough to correlate without
  enabling reversal; document that it is not a secret.
- **Cause depth bound**: 5–10 levels is commonly enough to reach the root cause.

## Real-world use case — Acme SaaS

Acme's `Checkout` wrapped Stripe errors and stored the raw provider error object on the internal
`PaymentError`. The tracker showed everything — including the customer's `last4` and the idempotency
key — in a UI that support could read. A support agent shared a screenshot in a customer thread and
the key leaked. Fix: (1) the Stripe adapter now builds `PaymentError` from an **allowlist** of provider
fields (`statusCode`, `requestId`, `code`) and never stores the raw object; (2) the idempotency key is
replaced by a fingerprint; (3) `last4` is classified PII and permitted only in a tenant-scoped support
view; (4) a canary test injects a fake PAN and a fake email through the Checkout failure path and fails
the build if either reaches logs or the tracker. Result: the payment error path now carries zero
secret/PII-by-default fields.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Non-collection (never read the secret) | Cannot be forgotten | Requires discipline at source | Secrets, tokens, PAN |
| Allowlist serialization | New fields denied by default | Must classify each field | All sinks |
| Value-level regex redaction | Catches third-party text | Misses novel formats | Backstop only |
| Fingerprint instead of value | Correlatable, non-reversible | Slightly less direct debugging | Secrets you must correlate |

## Common mistakes

- **Blocklist thinking.** "Remove known-bad strings" always lags reality.
- **Redacting after the fact.** The value already hit the sinks.
- **Redacting the response only.** Logs, DLQ, tracker, and metrics leak too.
- **Forgetting causes.** Nested causes carry the raw detail.
- **Trusting regex alone.** It is a backstop, not the control.
- **Leaving no audit.** Without a canary test, you never know it works.

## Checklist

- [ ] Does every error field have a classification?
- [ ] Are secrets never read into the error object (non-collection)?
- [ ] Do sinks emit via allowlist with unknown-field denial?
- [ ] Are causes serialized with the same rules and a depth bound?
- [ ] Is there a canary test for secrets and PII on failure paths?
- [ ] Is there a static scan for `err.stack` and raw `JSON.stringify(err)`?

## Related

- [Errors as a Disclosure Channel](../01-concepts/01-errors-as-a-disclosure-channel.md)
- [Injection, DoS, Serialization, and Reflection](../01-concepts/05-injection-dos-serialization-and-reflection.md)
- [Information Disclosure Channels](./01-information-disclosure-channels.md)
- [Chapter 36 — Sensitive Data and Error Context](../../36-sensitive-data-and-error-context/README.md)
- [Glossary](../../../GLOSSARY.md)
