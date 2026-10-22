# Boundary Ownership and Preventing Leakage

> Part VI · Chapter 15 · Sections 15.13–15.14 · _Estimated reading time: 18 min_
> **Prerequisite:** [What an Error Boundary Is](../01-concepts/01-what-error-boundaries-are.md)

## In one sentence

Ownership is the **single accountable layer per boundary**, and preventing leakage is the
mechanical guarantee that **no raw infrastructure, vendor, or secret detail crosses that layer's
edge** — enforced by translation and redaction, not by hoping no one logs the wrong object.

## Why this matters in production

Leakage is a security incident waiting to happen: schema names, connection strings, API keys, and
PII all routinely ride inside error objects and `cause` chains. Diffuse ownership is the reason it
happens — when three layers each feel responsible for "handling" an error, none owns its safe
representation. This file makes both concrete.

## Ownership: a matrix, not a vibe

For each boundary, write down four things: **unit**, **owner**, **decision**, **leak rule**. A
filled matrix is your boundary spec.

| Boundary | Owner | Decision owned | Must not leak |
| -------- | ----- | -------------- | ------------- |
| Function | author of the function | absorb one owned error | up anything not in its contract |
| Module | package maintainer | module error vocabulary | driver/vendor types |
| Domain | domain team | business outcome | any I/O or infra concept |
| Request | transport layer | status + body | stacks, SQL, hostnames, secrets |
| Transaction | application service | commit/rollback/compensate | driver errors outside the service |
| Job | worker/consumer | retry/DLQ/done | provider payloads to the DLQ metadata |
| Process | bootstrap | shutdown/exit | nothing (logs only, server-side) |
| Service | API layer | protocol mapping | upstream service internals |
| Integration | adapter owner | translate + degrade | vendor error identity |
| UI | component/route owner | fallback + recovery | internal codes not meant for users |

> **Rule:** if two owners claim the same decision, remove one. If no owner claims a decision, the
> error will reach the process boundary and become a generic crash.

## Ownership in code: make it structural

Ownership should be visible in the directory/module structure, not in comments. A common layout:

```text
src/
├── http/
│   └── errorHandler.ts        # request boundary — the ONLY file that sets status codes
├── application/
│   └── services/             # transaction boundaries — the ONLY layer that commits
├── domain/
│   └── errors.ts             # domain vocabulary — the ONLY layer that defines business errors
├── infra/
│   ├── repositories/         # module boundaries — the ONLY layer that knows SQLSTATE
│   └── integrations/         # integration boundaries — the ONLY layer that knows vendor codes
```

Then a lint/architecture test can enforce: *no `status` literal outside `http/`, no `SQLSTATE`
outside `infra/repositories/`, no vendor string outside `infra/integrations/`.* This turns
ownership from a convention into a compile/CI failure.

## Preventing leakage: the four channels

An error can leak through four channels. Close all four.

### Channel 1 — The response body

The most visible leak. Fix: translate at the boundary and serialize **only** the internal model's
safe fields.

```ts
// ❌ res.json(err) walks enumerable props and .cause → leaks everything.
res.status(500).json({ error: err });

// ✅ serialize an allowlisted projection only.
function problem(err: AppError, instance: string) {
  return {
    type: `https://errors.acme.example/${err.category}`,
    title: err.code,             // machine-readable, stable
    status: err.httpStatus,
    detail: err.safeMessage,     // curated, no internals
    instance,
  };
}
```

### Channel 2 — The log

Logs are internal, but they still leak to log aggregators, third-party SaaS, and support tools.
Fix: log the full error server-side **with redaction**; never log secrets or PII (Ch. 36).

```ts
log.error({
  err,                             // full stack/cause, server-side only
  requestId,
  tenantId,
  // ❌ do NOT include: authorization header, card PAN, raw body, tokens
}, "request failed");
```

### Channel 3 — The `cause` chain

A translated error keeps its original as `cause` for debugging — but any serializer that walks
`cause` re-leaks it. Fix: **the cause is for logs; the payload is for the network.** Never
`JSON.stringify` an error tree.

```python
# ❌ Serializing the chain page-by-page leaks the driver error to the API.
json.dumps({"error": {"message": e.args[0], "cause": repr(e.__cause__)}})
```

### Channel 4 — The error *message*

Messages frequently embed the offending value, a query, a path, or a token. Fix: domain errors
carry a **stable code** and a curated `safeMessage`; the raw message lives only in `cause`.
(Vocabulary from Ch. 6: `code` is machine-readable, `safeMessage` is user-safe.)

## A redaction pass at the outermost boundary

Treat the request boundary as a **sanitizing filter**. Before serialization, run an allowlist
projection and a scrub for known-sensitive patterns.

```ts
const SENSITIVE = [/api[_-]?key/i, /bearer\s+[a-z0-9._-]+/i, /\b\d{13,19}\b/]; // defensive

function sanitize(msg: string | undefined): string | undefined {
  if (!msg) return msg;
  return SENSITIVE.some((re) => re.test(msg)) ? "An error occurred." : msg;
}
```

Defense in depth: even if a translation is imperfect, the outermost boundary reduces the blast
radius of a leak to a generic message.

> ⚠️ **Hazard.** "The exception message is helpful for debugging" is exactly why it must not go to
> the client. Debug help lives in logs, keyed by `requestId`, not in the response.

## Detecting leakage automatically

| Check | Catches |
| ----- | ------- |
| Response-schema test asserting only allowlisted fields | Body leaks |
| CI grep: `\.message\b` near `res.send` / `HttpResponse` | Raw message usage |
| CI grep: vendor names / `SQLSTATE` outside infra dirs | Coupling leaks |
| Secret scanners over log configs | Credential/PII leaks |
| Fuzz test: force every error type, snapshot the response | Unknown-path leaks |

## Key data / numbers

- RFC 9457 Problem Details fields: `type`, `title`, `status`, `detail`, `instance` — none should
  contain a stack, SQL, hostname, or secret.
- Common leak triggers: `err.message`, `err.toString()`, `JSON.stringify(err)`, `repr(cause)`,
  ORM exception `.orig`, AWS SDK `$response`.
- Node: `Error.cause` and non-enumerable props are not serialized by `JSON.stringify` by default —
  but a custom serializer often adds them back.

## Real-world use case — Acme SaaS

A code review found that Acme's global handler did `res.json({ error: err.message })`. On a
malformed upload, the AWS SDK error message included the **bucket name and a pre-signed URL** —
a direct credential/PII leak. The fix had three parts: (1) the integration boundary translated SDK
errors to `StorageError` with a stable code; (2) the request boundary serialized only the
allowlisted Problem Details shape; (3) a CI grep banned `.message` near response calls. The leak
class disappeared, and support got `requestId`-keyed server logs instead of user-copied stack traces.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign one owner per boundary | Let multiple layers "handle" the same error |
| Serialize an allowlisted projection | `res.json(err)` or `JSON.stringify(err)` |
| Keep `cause` server-side only | Walk the cause chain into the response |
| Redact secrets/PII in logs | Log auth headers, tokens, or card data |
| Enforce ownership with CI/architecture tests | Rely on memory and code review alone |

## Common mistakes

- **Believing `JSON.stringify(err)` is safe** — custom `toJSON` often re-exposes `cause`.
- **Logging the whole request** to "debug faster" — captures `Authorization` and bodies.
- **Returning `err.message` for `4xx`** — vendor/schema text reaches users.
- **No owner for unknown errors** — they reach the process boundary as a crash.

## Checklist

- [ ] Every boundary has exactly one owner with a named decision.
- [ ] Ownership is enforced structurally (dirs, lint, tests).
- [ ] Responses serialize an allowlist, never an error object.
- [ ] The `cause` chain never crosses the network boundary.
- [ ] Logs redact secrets and PII; `requestId` links logs to responses.
- [ ] An outermost sanitizing pass reduces the blast radius of any missed leak.

## Related

- [What an Error Boundary Is](../01-concepts/01-what-error-boundaries-are.md)
- [Nested Boundaries](./01-nested-boundaries.md)
- [Part XIII — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
