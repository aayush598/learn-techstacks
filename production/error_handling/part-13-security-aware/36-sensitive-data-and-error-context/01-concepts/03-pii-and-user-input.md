# PII and User Input

> Part XIII · Chapter 36 · Sections 36.3, 36.5 · _Estimated reading time: 16 min_
> **Prerequisite:** [Secrets and Tokens](./02-secrets-and-tokens.md)

## In one sentence

**PII** (regulated personal data) and **user input** (untrusted, often personal) are the two most common
sensitive values in error context — they must be **minimized**, kept out of messages, and permitted only
in a narrowly scoped, RBAC-controlled sink, because a PII-in-logs incident is a reportable breach.

## Why this matters in production

Developers attach personal data to errors to make debugging easier — the email that failed validation,
the address that could not be geocoded, the free-text a user typed. That is convenient and, under GDPR/CCPA,
expensive: personal data in error logs is a data-processing activity subject to breach-notification rules.
User input is worse, because it is *untrusted*: the same value that is PII may also be an injection
payload, so it must be handled for both privacy and safety (see [Chapter 34 §34.15](../../34-security-principles-for-error-handling/01-concepts/05-injection-dos-serialization-and-reflection.md)).

## PII categories

| Category | Examples | In error context |
| -------- | -------- | ---------------- |
| Identifiers | name, email, phone, address, DOB, government ID | Validation, lookup, notification errors |
| Online identifiers | IP address, device id, cookie id, session id | Request context, rate-limit errors |
| Financial | account number, IBAN | Payment/billing errors |
| Sensitive/special | health, biometric, precise location, beliefs (GDPR Art. 9) | Domain-specific features |
| Free-text user input | comments, messages, prompts, filenames | Validation, LLM, upload errors |

> ⚠️ **Hazard.** **Free-text user input is both PII and untrusted.** A comment that failed validation may
> contain personal data, an injection string, or a full credit card someone typed into the wrong field.

## User input as an error-context problem

Attaching raw user input to an error creates three risks at once:

1. **Privacy** — the input is often personal data.
2. **Injection** — the input may contain payloads (SQL, shell, log newlines, HTML).
3. **Bulk disclosure** — a large input in an error body/log is a data dump.

The rule: **reference the input, do not reproduce it.**

```ts
// ❌ Reproduces the value (PII + injection + bulk).
throw new ValidationError(`invalid email: ${email}`);
throw new ValidationError(`invalid comment: ${comment}`); // may be huge, may be a payload

// ✅ Reference the field and rule; never the value.
throw new ValidationError("EMAIL_INVALID", "The email address is not valid.", {
  field: "email",     // field name only
  rule: "format",     // rule name only
});
```

The client already has its own input; it does not need it echoed back, and the server should never
reproduce an untrusted value into a response or a log.

## Minimization and hashing

When you genuinely need to correlate user input across events, use a **salted hash** instead of the value:

```python
import hashlib, os

SALT = os.environ["PII_HASH_SALT"].encode()  # per-environment, not committed

def correlate(value: str) -> str:
    # Non-reversible pseudonym for correlation; not PII.
    return hashlib.sha256(SALT + value.encode()).hexdigest()[:16]
```

```text
Correlation aids that are safe:
  • field name + rule name + stable code
  • length bucket ("comment length 1024-2048") instead of the text
  • salted hash for "did the same value appear twice?"
  • character class counts ("contains digits: true") instead of the value
```

## PII minimization in messages

| Anti-pattern | Problem | Fix |
| ------------ | ------- | --- |
| `\`User ${email} not found\`` | PII in message | `"USER_NOT_FOUND"` + field reference |
| Echo validated value | PII/untrusted reflection | Return the field name, not the value |
| Log full request body | Bulk PII | Allowlist + redaction |
| Include IP in URL/logs | Online identifier | Truncate (e.g. `/24`) or omit if not needed |
| Filenames in upload errors | May contain names/PII | Return a generated id, not the filename |

## Key data / numbers

- **GDPR Art. 4(1)**: personal data = any info about an identifiable person; Art. 32 requires
  appropriate measures; Art. 33 requires breach notification within **72 hours**.
- **CCPA/CPRA**: personal information includes identifiers and online identifiers; note the right to
  know/delete.
- **CWE-359** (exposure of private personal information), **CWE-209** (info in error message),
  **CWE-117** (log injection — relevant because user input is untrusted).
- **IP truncation**: `/24` (IPv4) or `/48` (IPv6) is a common de-identification technique when full IP
  is not needed.

## Real-world use case — Acme SaaS

Acme's comment-validation error echoed the offending comment: `throw new ValidationError(\`invalid comment: ${comment}\`)`.
The comment field was also used as an LLM prompt elsewhere, and one customer pasted their account recovery
codes into a comment. The codes appeared in the validation error, which was logged and surfaced in the
tenant's UI. Fix: validation errors now return `{ field: "comment", rule: "length" }` with a constant
message and a length bucket; a canary test injects a fake "recovery code" and asserts it reaches no sink;
and a lint rule bans interpolating request-derived values into error messages. The fix removed both the
privacy and the injection risk on the same path.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Reference, never reproduce | Safe, no PII/injection | Slightly less direct debugging | Default |
| Salted hash for correlation | Safe, debuggable | Needs salt management | Cross-event correlation |
| Redacted value in tracker (RBAC) | Debuggable | Tracker must be tightly controlled | Deep investigation only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return field name + rule, not the value | Echo the validated value |
| Use length buckets and class counts | Attach the raw free-text input |
| Salt-hash for correlation | Store the raw value for correlation |
| Truncate/omit IP when not needed | Log full IPs by default |
| Treat user input as PII **and** untrusted | Assume input is safe because it is "just a comment" |

## Common mistakes

- **Echoing the offending value.** PII plus injection.
- **Logging the request body.** Bulk PII.
- **Filenames and prompts in errors.** They contain names and content.
- **Full IP in every log.** Unnecessary online identifier.
- **Forgetting free-text fields.** Comments, filenames, prompts are the worst offenders.

## Checklist

- [ ] Does any error message contain a PII value?
- [ ] Are validated values referenced (field/rule), not reproduced?
- [ ] Are free-text inputs excluded from messages and logs?
- [ ] Is correlation done with a salted hash, not the value?
- [ ] Are IPs truncated or omitted where not needed?
- [ ] Does a canary test cover PII on failure paths?

## Related

- [Secrets and Tokens](./02-secrets-and-tokens.md)
- [Payment, Financial, Query, and Third-Party Context](./04-payment-financial-query-and-third-party.md)
- [Chapter 34 — Injection, DoS, Serialization, and Reflection](../../34-security-principles-for-error-handling/01-concepts/05-injection-dos-serialization-and-reflection.md)
- [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
