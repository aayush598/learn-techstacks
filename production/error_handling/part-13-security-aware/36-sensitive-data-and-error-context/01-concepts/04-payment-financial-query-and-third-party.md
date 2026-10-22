# Payment, Financial, Query, and Third-Party Context

> Part XIII · Chapter 36 · Sections 36.4, 36.6–36.7 · _Estimated reading time: 17 min_
> **Prerequisite:** [PII and User Input](./03-pii-and-user-input.md)

## In one sentence

**Payment/financial data** is governed by PCI DSS and must never carry a PAN; **query parameters** leak
tokens and PII because they are logged by default; and **third-party payloads** are untrusted, verbose,
and often sensitive — so each is handled by its own explicit rule set.

## Why this matters in production

Three context sources produce most real-world leaks, and each has a distinct failure mode:

- **Payment context** — an error that includes the full card number or CVC is a PCI violation the moment
  it is stored; `Checkout` failures routinely carry provider payloads with payment details.
- **Query parameters** — access logs, error logs, and correlation IDs frequently include the raw query
  string, so `?token=` and `?email=` end up in places nobody reviewed.
- **Third-party payloads** — a Stripe/OpenAI/AWS error body is verbose and untrusted; forwarding it
  leaks provider internals *and* whatever sensitive data the provider echoed back.

## Payment and financial data (PCI scope)

| Data | PCI status | In error context |
| ---- | ---------- | ---------------- |
| PAN (full card number) | Sensitive Auth Data — never store/log post-auth | **Never** in any sink |
| CVC/CVV | Sensitive Auth Data — never store | **Never** in any sink |
| Track/PIN data | Sensitive Auth Data — never store | **Never** in any sink |
| Expiry, cardholder name | Cardholder data (if stored with PAN) | Avoid; minimize |
| Last4, brand | Out of PCI scope but PII-linked | Restricted; tenant-scoped only |
| Amount, currency | Not card data but financial/PII-linked | Internal; avoid per-person detail |
| Idempotency key | Secret-ish | Fingerprint; never raw |

```ts
// ❌ The provider payload (with payment method details) rides into the error.
catch (e) { throw new PaymentError(`stripe failed: ${JSON.stringify(stripeErr)}`); }

// ✅ Allowlist non-sensitive provider fields; never store the raw object.
catch (e: unknown) {
  const s = e as { code?: string; statusCode?: number; requestId?: string };
  throw new PaymentError("PAYMENT_DECLINED", "The payment could not be completed.", {
    providerCode: s.code,          // internal: e.g. "card_declined"
    providerStatus: s.statusCode,  // internal
    providerRequestId: s.requestId, // internal (correlation)
    // no card object, no last4, no raw payload
  });
}
```

Never round-trip a payment provider's raw error object. Extract an allowlist of non-sensitive fields.

## Query parameters

Query strings are a favorite hiding place because they are logged automatically:

```text
GET /reset?token=eyJhbGci...&email=alice@corp.com
     ^ logs, error messages, referrers, analytics all may capture this
```

| Rule | Detail |
| ---- | ------ |
| Never log the raw query string | Log route names, not `req.originalUrl` |
| Never include query in error messages | Reference the parameter name, not the value |
| Move secrets out of the query | Use headers or the body |
| Redact known keys as a backstop | `token`, `key`, `api_key`, `password`, `code` |
| Be careful with correlation IDs | Do not encode query values into them |

```ts
// ❌ Logs the full URL including token/email.
log.info({ url: req.originalUrl }, "reset requested");

// ✅ Route + redacted presence flags only.
log.info({ route: "POST /reset", hasToken: !!req.query.token, requestId: req.id });
```

## Third-party payloads

Provider error bodies are untrusted, verbose, and may include the request you sent (with your secrets)
and the data you sent (with customer PII).

| Source | Typical payload risk | Control |
| ------ | -------------------- | ------- |
| Stripe error | Request echo, payment method details | Allowlist code/status/requestId |
| OpenAI/LLM error | Prompt echo (user content), API key prefix | Stable code; no prompt |
| AWS SDK error | Request params, ARN, bucket, credentials context | Map by error code; drop params |
| Webhook body | Any customer data; signatures | Redact; tenant-scope; DLQ with secrets stripped |
| SMTP/email provider | Recipient addresses, body | Stable code; no body |

```python
# ❌ Blindly storing the provider payload.
raise UpstreamError(f"provider error: {resp.text}")

# ✅ Allowlisted, sanitized summary.
def translate(resp) -> UpstreamError:
    return UpstreamError("PROVIDER_ERROR", "The provider rejected the request.", {
        "provider_status": resp.status_code,
        "provider_code": safe_provider_code(resp),  # from an allowlist, never raw text
    })
```

## Key data / numbers

- **PCI DSS v4.0**: Req 3.3 — do not store sensitive authentication data after authorization; PAN must be
  rendered unreadable wherever stored; Req 10.3 restricts logging of cardholder data; Req 8 protects
  credentials.
- **GDPR**: provider payloads containing EU users' data are personal data; a leak triggers Art. 33 (72 h).
- **CWE-532** (sensitive info in logs), **CWE-359** (private personal information), **CWE-209**
  (info in error messages), **CWE-502** (unsafe deserialization of third-party payloads).
- **Allowlist commonly safe provider fields**: `code`, `type`, `statusCode`, `requestId`, `retryAfter`.

## Real-world use case — Acme SaaS

Acme's `Checkout` wrapped Stripe errors as `throw new PaymentError(JSON.stringify(stripeErr))`. The Stripe
error object included the request echo with the customer's `card[number]` **and** Acme's Stripe secret
key in the URL. Both reached the error log on the first declined card. Fix: the adapter extracts only
`code`, `statusCode`, and `requestId`; it never serializes the provider object; the idempotency key is
fingerprinted; and a canary test injects a fake PAN and asserts no sink contains it. The change was
required for Acme's PCI assessment, which had flagged the provider payload as the top risk.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Allowlist provider fields | Safe, PCI-compliant | Less raw debugging detail | All provider integrations |
| Store raw payload in a secured store | Full debugging | High compliance burden | Rare, with justification |
| Log raw payload | Easy | Violates PCI/GDPR | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Allowlist provider code/status/requestId | Serialize the raw provider object |
| Never store PAN/CVC anywhere | Log payment method details |
| Log route + presence flags, not query strings | Log `req.originalUrl` |
| Move secrets out of query strings | Put tokens in `?token=` |
| Treat provider payloads as untrusted | Trust a provider's PII handling |

## Common mistakes

- **`JSON.stringify(providerError)`.** The single most common PCI bug.
- **Logging `originalUrl`.** Captures query tokens and emails.
- **Storing webhook bodies raw.** Contains customer data and signatures.
- **Echoing the prompt in LLM errors.** The prompt is user content.
- **Keeping last4 in shared logs.** PII-linked even if out of PCI scope.

## Checklist

- [ ] Does any error path store a PAN/CVC or the raw provider payload?
- [ ] Are provider errors reduced to an allowlist of safe fields?
- [ ] Is the raw query string excluded from logs and messages?
- [ ] Are secrets kept out of query strings?
- [ ] Are webhook bodies redacted and tenant-scoped?
- [ ] Does a canary test cover payment data on failure paths?

## Related

- [PII and User Input](./03-pii-and-user-input.md)
- [Redaction, Omission, Sanitization, and Allowlists](./05-redaction-omission-sanitization-and-allowlists.md)
- [Practical: Redacting PII and Secrets in Context](../03-practical-examples/01-redacting-pii-and-secrets-in-context.md)
- [Chapter 25 — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
