# Auth, Rate Limits, Quotas, and Billing

> Part X · Chapter 25 · Sections 25.4, 25.5, 25.6, 25.7 · _Estimated reading time: 14 min_

## In one sentence

**Distinguish misconfigured credentials from expired tokens, and throttle failures from quota/billing blocks** because **Checkout** and **WebhookIngest** must not retry `401` the same way they retry `429`.

## Why this matters in production

At **Acme SaaS**, using the wrong Stripe secret key returns `401` — retrying with the same key will never work. A `429` with `Retry-After: 60` means "back off". A quota/billing error means "you've hit your account limit" — often not retryable until the account state changes. Misclassifying these causes alert storms and wasted retries.

## Core concept

| Failure | Typical HTTP | Retryable? | Action |
| -------- | ------------ | ---------- | ------ |
| **Invalid credentials** | `401` | Usually **no** | Fail fast; alert on misconfiguration; don't retry. |
| **Expired tokens** | `401` (or provider-specific) | Sometimes **yes** (once) | If you can refresh tokens/idempotently re-auth, retry once; else fail. |
| **Insufficient permissions** | `403` | Usually **no** | Check scopes/roles; don't retry with same credentials. |
| **Rate limit exceeded** | `429` | **Yes** (with backoff) | Respect `Retry-After`, apply jitter, use retry budget. |
| **Quota/usage limit** | `429` or `403`/`422` (provider-specific) | Usually **no** until reset | Surface to ops/billing; may require plan upgrade. |
| **Billing/subscription issues** | `402` or `403` | Usually **no** | Block affected operations; notify account owner; don't retry blindly. |

## How it works (mechanics)

### Credentials and tokens
- **Invalid credentials (`401`)**: Often indicates wrong key, revoked key, or misconfigured environment. Treat as configuration error.
- **Expired tokens**: If using OAuth, attempt **token refresh once** before retrying the original request (only if the original request was not already sent with the new token and is idempotent).
- **Permissions (`403`)**: Scope/role issues — no amount of retrying will help without changing permissions.

### Rate limits
Providers throttle by key/account/IP. Look for:
- **`Retry-After`** header (seconds or HTTP-date). Prefer this over fixed backoff when present.
- **Rate limit headers** (e.g. `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`).
- **Retry budgets**: Don't let retries amplify a burst across the fleet.

### Quotas and billing
- **Hard quotas** (monthly API calls) — hitting them is not transient; requires quota increase or time window reset.
- **Billing failures** — e.g. card on file declined for provider account; operations may be blocked until resolved.

## Worked example

```ts
// Translate auth/rate-limit/billing at adapter
function translateAuthRateLimit(err: UpstreamErr): InternalErr {
  if (err.status === 401) {
    // Distinguish invalid vs expired if provider exposes details
    if (err.body?.error?.code === "token_expired") {
      return new InternalErr("UPSTREAM_TOKEN_EXPIRED", { retryable: true, retryOnce: true });
    }
    return new InternalErr("UPSTREAM_AUTH_INVALID", { retryable: false, alert: "config" });
  }
  if (err.status === 403) {
    return new InternalErr("UPSTREAM_FORBIDDEN", { retryable: false });
  }
  if (err.status === 429) {
    const retryAfterSec = parseRetryAfter(err.headers.get("retry-after"));
    return new InternalErr("UPSTREAM_RATE_LIMITED", {
      retryable: true,
      retryAfterSec,
      useRetryBudget: true,
    });
  }
  if (err.status === 402) {
    return new InternalErr("UPSTREAM_BILLING_ISSUE", { retryable: false });
  }
  // ...
}
```

**Key data:**
- **`429` + `Retry-After`**: Respect provider instruction. If absent, use exponential backoff with jitter.
- **`401`**: Common for invalid API keys; log with redaction (never log raw keys).
- **gRPC**: `UNAUTHENTICATED`, `PERMISSION_DENIED`, `RESOURCE_EXHAUSTED` map similarly.

## Real-world use case

**WebhookIngest receiving Stripe webhooks:** Stripe signs requests; signature verification failure returns a local `401`-equivalent. This is **not retryable** by your worker in the sense of "retry the HTTP call" — it's a validation/auth failure. In contrast, if your webhook processor calls Stripe's API and gets `429`, you must back off and may need to respect `Retry-After` to avoid retry storms.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Retry all 4xx except 400** | Simple | Retries 401/403/429 incorrectly | **Never** in production |
| **Classify by specific codes + provider details** | Correct, safe | More per-vendor logic | **Recommended** |
| **Token refresh middleware** | Handles expiry cleanly | Complex; must ensure idempotency and avoid refresh loops | For OAuth flows with refresh tokens |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat `401` invalid as config error (alert, don't retry) | Retry `401` indefinitely |
| Respect `Retry-After` on `429` | Ignore provider throttling hints |
| Distinguish quota vs rate limit | Conflate "monthly quota exhausted" with "too many requests now" |
| Handle token expiry with single refresh attempt | Create refresh loops or retry with expired token repeatedly |
| Surface billing issues to the right team | Retry payment-provider billing failures as if transient |

## Common mistakes

- **Retrying misconfiguration:** Invalid API key in prod retried every second creates log spam and no recovery.
- **Ignoring `Retry-After`:** Using fixed backoff when provider says "wait 120s" can prolong throttling or hit harder limits.
- **Leaking key details:** Error messages must not include partial secrets.
- **Retrying permission changes:** `403` won't become `200` without scope change.

## Checklist

- [ ] `401`/`403` classified as non-retryable unless token refresh applies.
- [ ] `429` respects `Retry-After` and uses retry budget + jitter.
- [ ] Quota/billing (`402`/provider-specific) routed to ops/billing, not generic retry.
- [ ] Token refresh is idempotent and limited to once per original request.
- [ ] Secrets never appear in error messages/context logged.

## Related

- [Classifying Upstream Failures](./01-classifying-upstream-failures.md)
- [Malformed Responses, Versioning, and Degradation](./03-malformed-responses-versioning-degradation.md)
- [Translation, Adapters, and Outages](./04-translation-adapters-and-outages.md)
- [Glossary](../../../GLOSSARY.md)
