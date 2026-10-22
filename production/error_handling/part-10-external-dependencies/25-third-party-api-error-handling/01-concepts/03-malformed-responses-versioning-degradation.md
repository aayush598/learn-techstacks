# Malformed Responses, Versioning, and Degradation

> Part X · Chapter 25 · Sections 25.10, 25.11, 25.12, 25.13 · _Estimated reading time: 14 min_

## In one sentence

**Never assume provider responses are well-formed**: validate/defensively parse, handle version incompatibility explicitly, and degrade gracefully when dependencies are partially available.

## Why this matters in production

For **Acme SaaS**, a provider can change their error schema between API versions, return HTML on an error path (behind a misconfigured proxy), or return truncated JSON. **AgentRun** calling an LLM provider might get unexpected fields. **ExportJob** calling object storage might get a non-JSON error. If you blindly `JSON.parse` and access `error.code` without checks, you turn a parse failure into an unhandled exception that loses the original context.

## Core concept

| Issue | Example | Action |
| ----- | ------- | ------ |
| **Malformed responses** | Invalid JSON, HTML error page, truncated body | Treat as upstream parse failure; don't guess structure; include content-type/length in safe context. |
| **Unexpected formats** | Schema changed, missing expected fields | Validate with schema (or defensive checks); translate to `UPSTREAM_UNEXPECTED_FORMAT`. |
| **Degradation** | Provider returns partial data or slower responses | Detect degraded mode; use cached/fallback data if safe; communicate degradation. |
| **Version incompatibility** | Deprecated fields, removed endpoints, changed error codes | Pin API version; detect incompatibility; fail with clear message; plan migration. |

## How it works (mechanics)

### Defensive parsing
1. **Check content-type** — if expecting JSON, verify; otherwise handle as text/blob.
2. **Parse safely** — `try/catch` JSON parse; if fails, treat as parse failure (not "unknown HTTP error").
3. **Validate shape** — use schema validation or defensive property access with defaults.
4. **Preserve raw safely** — never log full response bodies with PII; log truncated/safe snippets.

### Versioning
- **Pin versions** where possible (e.g. `Stripe-Version` header).
- **Detect incompatibility** — unknown error codes, missing required fields, 410 Gone.
- **Translation tables versioned** — update mappers when provider changes.
- **Backward compatibility** — your internal codes must remain stable even if provider changes.

### Degradation
- **Optional deps**: If address verification fails due to malformed response, fall back to basic validation (if business allows).
- **Critical deps**: If payment gateway returns unexpected format, **fail closed** — don't guess and charge.
- **Stale cache**: For read-only non-critical data, cached fallback may be acceptable with staleness indicators.

## Worked example

```ts
// Defensive parse + validation
async function parseUpstream(res: Response): Promise<ParsedUpstream> {
  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("application/json")) {
    // HTML/text error page
    const text = await res.text().catch(() => "");
    return { kind: "non_json", status: res.status, snippet: truncate(text, 200) };
  }
  let body: unknown;
  try {
    body = await res.json();
  } catch (e) {
    return { kind: "malformed_json", status: res.status };
  }
  // defensive shape check
  if (!isExpectedErrorShape(body) && res.ok) {
    // 200 with unexpected shape
    return { kind: "unexpected_format", status: res.status, body };
  }
  return { kind: "json", status: res.status, body };
}

function isExpectedErrorShape(b: any): boolean {
  return b && typeof b === "object" && ("error" in b || "errors" in b);
}
```

**Key data:**
- **Content-Type**: Don't trust it blindly; validate.
- **HTML error pages**: Common behind proxies/LB when upstream is down (see Chapter 26).
- **410 Gone**: Often means API version deprecated — non-retryable without migration.

## Real-world use case

**AgentRun calling an LLM provider:** Provider changes error schema. Old mapper expects `error.message`, new schema nests differently. Without defensive parsing, the code throws `TypeError` and loses the HTTP status/retryability. With schema checks and translation to `UPSTREAM_UNEXPECTED_FORMAT` (non-retryable until fixed), the error is logged with safe context and the agent can fall back to another provider or degrade gracefully.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Strict schema validation** | Catches breaks early | Brittle if provider is loose | For critical paths where shape is strict |
| **Defensive checks + fallbacks** | Resilient | May mask real issues | **Recommended** default with logging/alerts |
| **Version pinning** | Predictable | Requires upgrade planning | **Recommended** for production |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Parse defensively; handle non-JSON errors | Assume every error response is JSON |
| Validate shapes before accessing nested fields | Do `body.error.code` without null checks |
| Pin API versions and track deprecations | Use latest version with no upgrade plan |
| Degrade only for non-critical, read-only paths | Guess and proceed on critical payment paths |
| Alert on unexpected formats/version issues | Swallow parse failures silently |

## Common mistakes

- **Trusting Content-Type:** A server can return HTML with `application/json` header or vice versa.
- **Over-trusting 200:** Treating any 200 as success; some providers return error payloads with 200.
- **No version strategy:** Breaking provider changes cause sudden failures across all calls.
- **Degrading critical flows:** Falling back to "charge without verification" is dangerous.

## Checklist

- [ ] Non-JSON responses handled explicitly.
- [ ] JSON parse failures classified as `UPSTREAM_MALFORMED_RESPONSE`.
- [ ] Unexpected shapes mapped to `UPSTREAM_UNEXPECTED_FORMAT` with safe context.
- [ ] API version pinned; deprecation notices monitored.
- [ ] Degradation policy defined per dependency (critical vs optional).

## Related

- [Auth, Rate Limits, Quotas, and Billing](./02-auth-rate-limits-quotas-and-billing.md)
- [Translation, Adapters, and Outages](./04-translation-adapters-and-outages.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../26-network-and-distributed-communication-errors/README.md)
- [Glossary](../../../GLOSSARY.md)
