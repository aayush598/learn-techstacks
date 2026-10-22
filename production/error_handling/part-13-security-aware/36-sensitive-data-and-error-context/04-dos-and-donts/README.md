# Chapter 36 — Do's and Don'ts

> Part XIII · Chapter 36 · all sections · _Estimated reading time: 9 min_

## In one sentence

Error context is safe when every field is **classified before collection**, secrets are **never
collected**, unavoidable sensitive text is **redacted as a backstop**, and all output is **allowlisted,
bounded, and fail-safe**.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | Classify every context field at the source | Attach a `req.body` blob |
| 2 | Deny unclassified fields by default | Assume a field is "probably fine" |
| 3 | Never collect secrets/tokens | `throw new Error(\`bad key ${key}\`)` |
| 4 | Fingerprint when correlation is needed | Store the raw token |
| 5 | Reference field name + rule, not the value | Echo the validated value |
| 6 | Pseudonymize PII with a salted hash | Store raw emails for correlation |
| 7 | Never store PAN/CVC anywhere | Log payment method details |
| 8 | Allowlist provider fields | `JSON.stringify(providerError)` |
| 9 | Log route + presence flags, not query strings | Log `req.originalUrl` |
| 10 | Sanitize untrusted text (control chars, length) | Store raw provider text |
| 11 | Project context via a per-sink allowlist | Emit the whole context bag |
| 12 | Sanitize every node in the cause chain | Trust the outer error only |
| 13 | Bound depth, chain size, and string length | Serialize unbounded |
| 14 | Detect cycles in chains | Risk infinite loops |
| 15 | Make the serializer fail-safe | Let it throw |
| 16 | Treat logs as personal data | Exempt logs from privacy rules |
| 17 | Set retention per sink | Keep logs forever |
| 18 | Run a canary corpus in CI | Assume redaction works |
| 19 | Omit first, then allowlist, redact last | Make redaction the primary control |
| 20 | Audit third-party sinks | Ignore metrics/tracker exports |

## Anti-patterns with symptoms

### ❌ `JSON.stringify(providerError)`

```ts
throw new PaymentError(JSON.stringify(stripeErr));
```

**Symptom:** card details and API keys in logs; a PCI finding.
**Fix:** allowlist provider `code`/`statusCode`/`requestId` only.

### ❌ Echoing the input

```ts
throw new ValidationError(`invalid email: ${email}`);
```

**Symptom:** PII in responses/logs plus injection risk.
**Fix:** return `{ field, rule }`, never the value.

### ❌ Secret in the message

```python
raise AuthError(f"invalid token {token}")
```

**Symptom:** a live credential in logs and tickets.
**Fix:** non-collection; attach a fingerprint if needed.

### ❌ Unbounded cause walk

```ts
function dump(e) { return { msg: e.message, cause: e.cause ? dump(e.cause) : null }; }
```

**Symptom:** raw innermost errors (SQL, headers) leak; cycles crash the process.
**Fix:** bounded, per-node-sanitized `serializeChain`.

### ❌ Whole-context logging

```ts
log.error({ err, ctx: req.body }, "failed");
```

**Symptom:** bulk PII/secrets in logs.
**Fix:** `buildContext` with classified fields only.

### ❌ Logging `originalUrl`

```ts
log.info({ url: req.originalUrl }, "reset");
```

**Symptom:** `?token=` and `?email=` in access logs.
**Fix:** log the route + presence flags.

### ❌ Raw email in metrics

```ts
metrics.increment("signup_failed", { email });
```

**Symptom:** a searchable PII index exported to a vendor.
**Fix:** bounded labels only; per-user detail in scoped records.

## Code-review questions

1. Is every context field classified, and is it permitted at the intended sink?
2. Could this string contain a secret, PII, PAN, or query token?
3. Is `cause` serialized per node, bounded, and cycle-checked?
4. Is the serializer fail-safe and deny-by-default?
5. Are logs treated as personal data with retention?
6. Is there a canary corpus covering secrets/PII/PAN per sink?
7. Are third-party sinks in the inventory and audited?

## Minimal policy snippet

```yaml
contextPolicy:
  classifyAtSource: true
  denyUnknownFields: true
  sinkAllowlist:
    response: [code, message, requestId, field, rule]
    log:      [code, message, class, provider, requestId, field, rule, userFp]
    tracker:  [code, class, provider, requestId, tenantId, userFp, stack]
  secrets: neverCollected
  pan: neverCollected
  pii: pseudonymize
  redactionBackstop: true
  bounds: { depth: 6, nodes: 10, message: 300, stack: 8000 }
  failSafe: genericPublicShape
  retention: { logs: 90d, dlq: 14d, tracker: 90d }
```

## Related

- [Redaction, Omission, Sanitization, and Allowlists](./../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)
- [Defining Sensitive Metadata](./../01-concepts/01-defining-sensitive-metadata.md)
- [Chapter 36 Reference](../05-reference/README.md)
- [Chapter 34 — Security Principles Do's and Don'ts](../../34-security-principles-for-error-handling/04-dos-and-donts/README.md)

