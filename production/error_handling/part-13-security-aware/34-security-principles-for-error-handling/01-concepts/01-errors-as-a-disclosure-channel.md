# Errors as a Disclosure Channel

> Part XIII · Chapter 34 · Sections 34.1, 34.16–34.18 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)

## In one sentence

Every error is a message that leaves your process through some sink (response, log, queue record,
metric label), and unless you **bound what it may carry**, it will disclose more than the caller
deserves — so unknown failures need a **secure default**, not a helpful one.

## Why this matters in production

The default behavior of every framework is to help developers, not protect production:

- An unhandled exception in a Node/Express app leaks the full stack trace and file paths unless a
  handler catches it.
- A Django app with `DEBUG=True` shipped to production leaks settings, SQL, and installed apps.
- A gRPC server that forwards unknown status messages can leak backend hostnames to clients.

Attackers do not need a sophisticated exploit when the error page hands them the map. This section
frames error handling as a **security control surface**: every field you decide to include is an
authorization decision about who may see that information.

## Core concept — errors have sinks

An error rarely leaves through one place. Trace it and you find several sinks, each with its own
audience:

| Sink | Audience | Typical leak if unbounded |
| ---- | -------- | ------------------------- |
| HTTP response body | End user / attacker | Stack, SQL, internal codes |
| Response headers | End user / proxy | Server version, internal hostname |
| Structured logs | Operators (broad) | PII, tokens, request bodies |
| Exception tracker | Engineers | Everything (usually acceptable) |
| Job/queue record | Internal + future operators | Full payload detail |
| Metric labels | Dashboards | High-cardinality PII, e.g. email |
| Dead-letter queue | Operators | Raw secrets from payloads |
| Support tooling | Support agents | Cross-tenant context |

> ⚠️ **Hazard.** The exception tracker is the one sink where full detail is *expected*. The most
> common mistake is assuming the others behave the same way. They do not: logs are widely readable,
> metrics are often exported to third parties, and DLQ payloads are sometimes dumped into tickets.

The mental model is a **funnel**: an error is created with full internal detail, and each boundary
it crosses *narrows* what is allowed through, until only the policy-approved fields reach each
audience.

```text
 throw ──▶ boundary ──▶ boundary ──▶ external response
 (full)    (internal    (internal    (public fields
           log: full)    services)    only)
```

## The disclosure policy

A disclosure policy answers one question per audience: **what may this audience see?** Write it
once, encode it in the serializer (see `03-practical-examples/01`), and stop arguing in code
review.

| Audience | Status | Public code | Message | Detail | Stack | Internal context |
| -------- | ------ | ----------- | ------- | ------ | ----- | ---------------- |
| Public / unauthenticated | ✅ | ✅ (coarse) | ✅ generic | ✅ only if non-revealing | ❌ | ❌ |
| Authenticated user | ✅ | ✅ | ✅ | ✅ (own-resource only) | ❌ | ❌ |
| Tenant admin | ✅ | ✅ | ✅ | ✅ (tenant-scoped) | ❌ | ❌ |
| Operator / on-call | ✅ | ✅ | ✅ | ✅ | ✅ (in logs) | ✅ (internal sink) |
| Internal service | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ (over mTLS) |

The default landing spot for an **unknown** exception is the top row: a generic `500`, a coarse
code like `INTERNAL_ERROR`, a correlation ID, and nothing else.

## Secure defaults for unknown exceptions

1. **Catch at the outermost boundary.** One global handler per process; nothing reaches the client
   that it did not approve.
2. **Never send `err.message` for unknown errors.** It is written for developers and may contain
   hostnames, queries, or user input.
3. **Send a correlation ID.** Operators find the detail in logs; the caller cannot.
4. **Return a stable code, not a class name.** `INTERNAL_ERROR` beats `TypeError`.
5. **Log the full detail internally, with the same correlation ID**, so support can join them.
6. **Fail closed on security-relevant unknown errors** — authorization and authentication paths
   deny, they do not "continue unsafely".

## Worked example

```ts
// ❌ Leaks everything the exception happened to carry.
app.use((err, req, res, next) => {
  res.status(500).json({ message: err.message, stack: err.stack });
});

// ✅ Secure default: generic external shape, full internal record.
app.use((err: unknown, req: Request, res: Response, _next: NextFunction) => {
  const cid = req.id; // correlation id set by upstream middleware
  const known = err instanceof AppError && err.disclosure === "public";

  log.error({ err, cid, path: req.path }, "unhandled error");

  const status = known ? err.httpStatus : 500;
  const code = known ? err.code : "INTERNAL_ERROR";
  const message = known ? err.safeMessage : "Something went wrong. Please try again.";

  res.status(status).json({ code, message, requestId: cid });
});
```

The internal log line carries `err` in full; the response carries four safe fields.

## Key data / numbers

- **OWASP Top 10 (2021) A01: Broken Access Control** and **A05: Security Misconfiguration** both
  call out verbose error messages and stack traces explicitly.
- **CWE-209: Generation of Error Message Containing Sensitive Information** is the canonical
  weakness for this chapter; **CWE-200: Exposure of Sensitive Information to an Unauthorized
  Actor** is its parent.
- **HTTP security headers** (`Server`, `X-Powered-By`, `X-AspNet-Version`) leak stack details and
  should be removed or blanked by the reverse proxy.
- **Correlation ID correlation rate** is a useful KPI: if >99% of external 500s carry a request ID
  that joins to an internal log line, support can debug without disclosure.

## Real-world use case — Acme SaaS

Acme's `AgentRun` feature called an LLM provider directly from the request handler. When the
provider returned an error, Acme forwarded the provider's message verbatim. One message included
the **provider API key prefix and the full prompt** (which contained a customer's email body).
That text landed in the customer's browser and in Acme's own analytics events. Fix: the LLM
adapter now maps every provider error to a stable internal code (`AI_PROVIDER_UNAVAILABLE`), the
provider payload is logged internally only, and the external response is a generic message plus a
correlation ID. Measurable result: zero sensitive strings in the `AgentRun` response path, verified
by an automated scan on every build.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Generic external + full internal | Safe by default; debuggable | Support must join by ID | Default for all unknown errors |
| Verbose external messages | Fast local debugging | Disclosure risk; hard to audit | Never in production for unknown errors |
| Per-audience tiered detail | Right information per role | More design work | Product with support/admin roles |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Default to a generic message for unknown errors | Send `err.message` to callers |
| Attach a correlation ID to every external error | Rely on the caller to describe the failure |
| Log full detail internally with the same ID | Log PII to make debugging easy |
| Remove version banners at the proxy | Advertise `X-Powered-By: Express` |
| Fail closed on security-path unknowns | Fall back to "allow" when a check throws |

## Common mistakes

- **Trusting `NODE_ENV`/`DEBUG` to gate verbosity.** A misconfigured deploy silently turns on
  verbose errors; gate on an explicit allowlist instead.
- **Assuming internal logs are safe.** Logs are read by many people and exported widely; treat
  them as a semi-trusted sink.
- **Only sanitizing the response.** The error also flows to logs, metrics, and queues — sanitize
  at classification time, not at one sink.
- **Using `err.toString()` in a template.** It folds the message (and sometimes the cause) into a
  string you then forget to inspect.

## Checklist

- [ ] Does every unknown exception hit exactly one outer boundary?
- [ ] Does the external response for unknown errors contain only approved fields?
- [ ] Is there a correlation ID on every external error and its internal log line?
- [ ] Have you removed stack/version banners from responses and headers?
- [ ] Is there a written disclosure policy per audience?
- [ ] Do auth/authz paths fail closed when an unexpected error occurs?

## Related

- [Stack Traces, Schemas, and Infrastructure Leakage](./02-stack-traces-schemas-and-infrastructure-leakage.md)
- [Secrets, PII, and Tenant Leakage](./03-secrets-pii-and-tenant-leakage.md)
- [Deep dive: Information Disclosure Channels](../02-deep-dive/01-information-disclosure-channels.md)
- [Chapter reference: Disclosure policy matrix](../05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
