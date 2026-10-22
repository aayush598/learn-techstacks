# Secrets and Tokens

> Part XIII · Chapter 36 · Section 36.2 · _Estimated reading time: 15 min_
> **Prerequisite:** [Defining Sensitive Metadata](./01-defining-sensitive-metadata.md)

## In one sentence

Secrets and tokens must **never be collected into an error object** — not because redaction might fail,
but because a value you never read cannot leak, so the correct control is **non-collection**, with a
non-reversible **fingerprint** used when you need to correlate "which secret".

## Why this matters in production

Secrets leak into errors through mundane paths: an HTTP client that includes request headers in its
error, a config validator that prints the parsed object on failure, a JWT library that echoes the token
in its message, a webhook handler that logs the signature, a query string that carries an API key. Once
a secret is in an error, it flows to logs, DLQs, the exception tracker, and sometimes the response.
Non-collection closes every one of those paths at once.

## Core concept — non-collection, not redaction

| Control | Definition | Strength |
| ------- | ---------- | -------- |
| **Non-collection** | The secret is never read into the error | Strongest: cannot be forgotten |
| **Fingerprint** | A short non-reversible hash prefix for correlation | Strong: enables debugging without the value |
| **Redaction** | The value is collected, then masked before a sink | Weakest: depends on every sink remembering |

Chapter 34's [redaction strategy](../../34-security-principles-for-error-handling/02-deep-dive/03-redaction-strategy.md)
treats redaction as a backstop. For secrets specifically, prefer non-collection.

## The fingerprint pattern

A fingerprint lets operators answer "was this the same token?" without storing it:

```ts
import { createHash } from "node:crypto";

function fingerprint(secret: string): string {
  // Short, hex, non-reversible prefix. Document that it is NOT a secret.
  return createHash("sha256").update(secret).digest("hex").slice(0, 8);
}

// ❌ The token is in the error.
throw new AuthError(`invalid token ${token}`);

// ✅ Only a fingerprint is attached; the token never enters the error.
throw new AuthError("INVALID_TOKEN", { tokenFp: fingerprint(token) });
```

Operators can correlate "same fingerprint appears 1,000 times" without ever holding the token.

## Where secrets hide in errors

| Path | Secret | Control |
| ---- | ------ | ------- |
| HTTP client error (axios/fetch) | `Authorization`, cookies, URL query tokens | Strip headers/URL; allowlist error fields |
| JWT library error | The raw token | Catch and re-throw with a constant message |
| Config validation | Parsed config with passwords/keys | Never log the parsed object; allowlist |
| Webhook handler | Signature secret, raw body | Log a status/requestId, not the secret |
| DB connection error | Connection string with password | Translate by code; drop the string |
| LLM provider error | API key, prompt (may contain tokens) | Map to a stable code; log an allowlist |
| Query string | `?api_key=`, `?token=` | Never log raw query strings |

## Worked example — HTTP client and query string

```ts
// ❌ Many clients throw errors carrying the URL (with tokens) and headers.
try {
  await api.get(`/data?api_key=${API_KEY}`);
} catch (err: unknown) {
  log.error({ err }, "api call failed"); // leaks API_KEY
  throw new InternalError(`upstream failed: ${String(err)}`);
}

// ✅ Structured, allowlisted, no URL/headers/key.
try {
  await api.get("/data", { headers: { authorization: `Bearer ${API_KEY}` } });
} catch (err: unknown) {
  log.error(
    { provider: "acme-upstream", status: (err as any)?.response?.status, requestId, keyFp: fingerprint(API_KEY) },
    "upstream call failed",
  );
  throw new UpstreamError("UPSTREAM_ERROR", "The upstream service could not be reached.");
}
```

Note that the query-string key was removed from the URL entirely — non-collection.

## Detecting secrets in existing errors

- **Static scan** for `Authorization`, `Bearer`, `apiKey`, `token`, `password`, `secret` near error
  construction and log calls.
- **Canary test**: inject a synthetic token through a failure path; assert it appears in no sink.
- **Log sampling**: pattern-scan a sample of production logs for key-like strings and JWTs.

## Key data / numbers

- **CWE-532** (insertion of sensitive info into log file), **CWE-798** (hard-coded credentials),
  **CWE-312** (cleartext storage of sensitive information).
- **PCI DSS Req 3.3/10**: card data and keys must not be logged; log access is restricted.
- **Fingerprint**: a commonly used length is 8 hex chars (32 bits); it is a correlation aid, not a
  secret, and must be documented as such.
- **Secret formats worth pattern-matching (as a backstop only)**: `sk_live_*`/`rk_live_*` (Stripe),
  `Bearer <token>`, JWT `xxxxx.yyyyy.zzzzz`, AWS `AKIA[0-9A-Z]{16}`, PEM `-----BEGIN ... KEY-----`.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` logged the failing Stripe signature comparison with the raw `Stripe-Signature`
header and the endpoint secret for "debugging". During a signature mismatch, both landed in the log
aggregator, and the endpoint secret — used to verify all webhooks — was exposed to anyone with log
read access. Fix: the handler now logs `{ requestId, signaturePresent: true, mismatch: true }` and a
fingerprint of the secret, never the secret or the signature. The secret was rotated, and a canary test
now asserts no webhook secret reaches any sink. The non-collection change removed the class of leak.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Non-collection | Cannot be forgotten | Sometimes need to redesign logging | Always for secrets |
| Fingerprint for correlation | Debuggable without the value | Slight loss of directness | When correlation is needed |
| Redaction at sink | Catches third-party text | Depends on every sink | Backstop only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Never read a secret into an error | `throw new Error(\`bad key ${key}\`)` |
| Attach a fingerprint for correlation | Store the raw token |
| Strip Authorization/Cookie at the HTTP edge | Log request headers wholesale |
| Translate config/connection errors by code | Print the parsed config |
| Remove tokens from URLs | Log raw query strings |

## Common mistakes

- **Logging the whole HTTP client error.** It carries headers, URL, and body.
- **Trusting a library to redact.** Many echo the token in the message.
- **"Temporarily" logging the secret during an incident.** It outlives the incident.
- **Redacting only at the response.** Logs and DLQ leak too.
- **Storing the token "just in case".** Non-collection is the fix.

## Checklist

- [ ] Does any error message contain a raw secret or token?
- [ ] Are HTTP client errors logged via an allowlist, not the raw object?
- [ ] Are query strings with tokens excluded from logging?
- [ ] Do config/connection errors avoid printing credentials?
- [ ] Is a fingerprint used where correlation is needed?
- [ ] Does a canary test confirm no secret reaches any sink?

## Related

- [Defining Sensitive Metadata](./01-defining-sensitive-metadata.md)
- [Payment, Financial, Query, and Third-Party Context](./04-payment-financial-query-and-third-party.md)
- [Practical: Redacting PII and Secrets in Context](../03-practical-examples/01-redacting-pii-and-secrets-in-context.md)
- [Chapter 34 — Redaction Strategy](../../34-security-principles-for-error-handling/02-deep-dive/03-redaction-strategy.md)
- [Glossary](../../../GLOSSARY.md)
