# Stack Traces, Schemas, and Infrastructure Leakage

> Part XIII · Chapter 34 · Sections 34.2–34.4 · _Estimated reading time: 16 min_
> **Prerequisite:** [Errors as a Disclosure Channel](./01-errors-as-a-disclosure-channel.md)

## In one sentence

**Stack traces**, **database schemas**, and **infrastructure identifiers** are the three most
common accidental disclosures in production errors — each hands an attacker a different part of
your map, and each is trivially avoided at the boundary.

## Why this matters in production

Attackers chain small disclosures into large ones. A stack trace names your framework and version,
which points to a known CVE. A SQL error reveals table and column names, which turns a blind
injection attempt into a precise one. A hostname like `ip-10-0-3-17.internal` reveals your network
topology and cloud provider. Individually these look harmless; together they compose a cheap
reconnaissance report produced by your own application.

## The three leakage classes

| Class | Typical source | What leaks | Downstream use |
| ----- | -------------- | ---------- | -------------- |
| **Stack trace** | Unhandled exception | File paths, function names, library versions, line numbers | CVE targeting, logic reconstruction |
| **Schema / query** | DB driver exception | Table names, column names, constraints, sometimes SQL text and parameter values | Injection refinement, data mapping |
| **Infrastructure** | Connection errors, headers | Hostnames, IPs, ports, bucket names, region, cloud provider | Topology mapping, SSRF targets, lateral movement |

### Stack traces (CWE-209)

A stack trace is designed for a developer with source access. Its contents — `node_modules`,
absolute paths, internal package names — are exactly what an external attacker should never see.

```ts
// What a raw unhandled error returns:
{
  "message": "Cannot read properties of undefined (reading 'tenantId')",
  "stack": "TypeError: ... at BillingService.charge (/srv/app/src/billing/charge.ts:42:17)\n at ... "
}
```

The attacker learns: the service is on `/srv/app`, the language and runtime assumptions, a billing
class, and a line number to correlate with public package versions.

### Schema and query leakage

Database drivers are verbose by design. A failed query can include the offending SQL, the table
name, and constraint identifiers.

```text
error: duplicate key value violates unique constraint "users_email_key"
```

From one line an attacker learns there is a `users` table, an `email` column, and a unique index
naming convention. In verbose mode some drivers echo the full statement and bind values.

### Infrastructure leakage

DNS failures, TLS errors, and connection errors often name internal hosts:

```text
getaddrinfo ENOTFOUND redis-cache-prod-03.internal.svc
connect ECONNREFUSED 10.0.4.19:5432
```

Response headers such as `Server: nginx/1.18.0 (Ubuntu)` and `X-Powered-By: Express` are
infrastructure leakage too, just at the transport layer.

## How it works (mechanics)

```text
  raw driver/exception
        │  carries: SQL text, host, stack
        ▼
  translation boundary         <-- FIRST place to strip
        │  keep: stable code, safe message, retry info
        ▼
  public serialization
        │  emit: policy-approved fields only
        ▼
  external response            <-- must contain none of the three classes
```

The critical rule: **strip at the translation boundary, not at the serialization boundary.** If
the driver exception's `message` is copied into an application error at translation time, every
later sink inherits the leak. If the driver text is dropped there, no sink can leak it.

## Worked example — DB → domain translation

```ts
// ❌ The raw pg error (with SQL and table names) flows to the caller.
catch (err) {
  throw new Error(`DB failed: ${(err as Error).message}`);
}

// ✅ Translate to a stable domain error; keep the cause internally only.
catch (err: unknown) {
  const pg = err as { code?: string; constraint?: string };
  if (pg.code === "23505") {
    // unique_violation — map by constraint, never expose the constraint name
    if (pg.constraint === "users_email_key") {
      throw new ConflictError("EMAIL_ALREADY_USED", "That email is already registered.");
    }
    throw new ConflictError("DUPLICATE", "This record already exists.");
  }
  if (pg.code === "23503") {
    // foreign_key_violation — do not name the referenced table
    throw new ValidationError("INVALID_REFERENCE", "One referenced item does not exist.");
  }
  // Unknown DB error: generic external outcome, full cause logged internally.
  throw new InternalError("DATABASE_ERROR", "A storage error occurred.", { cause: err });
}
```

The `cause` is preserved on the internal error object so the exception tracker sees it; the public
serializer must never emit it (see [redaction strategy](../02-deep-dive/03-redaction-strategy.md)).

## Key data / numbers

- **PostgreSQL SQLSTATE**: `23505` unique_violation, `23503` foreign_key_violation, `23502`
  not_null_violation, `23514` check_violation, `42P01` undefined_table, `42703` undefined_column.
  Map these to application codes; never forward the driver message.
- **MySQL** duplicate-entry is error `1062`; **SQLite** constraint errors surface as
  `SQLITE_CONSTRAINT` variants. The principle is identical: translate by code.
- **Framework banners to strip**: `X-Powered-By`, `Server`, `X-AspNet-Version`, `X-AspNetMvc-Version`.
- **OWASP Top 10 (2021) A05: Security Misconfiguration** explicitly lists "verbose error messages
  containing stack traces or other sensitive information".
- **CWE-209** (error message info), **CWE-200** (exposure), **CWE-497** (exposure of system data
  to an unauthorized control sphere).

## Real-world use case — Acme SaaS

An Acme `ExportJob` wrote to S3 through a misconfigured client. The raised error included the
bucket name (`acme-exports-prod-ap-south-1`), the region, and the IAM role ARN. The `ExportJob`
failure was surfaced in the tenant's UI as "Export failed: [that message]". A customer's security
team noticed the ARN in a screenshot and filed a disclosure report. Fix: the S3 adapter now maps
every storage failure to one of three stable codes (`EXPORT_STORAGE_UNAVAILABLE`,
`EXPORT_STORAGE_DENIED`, `EXPORT_STORAGE_NOT_FOUND`) with generic messages, and the bucket/ARN
detail goes only to the internal job record. The tenant UI shows the code plus a support link.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Include stack in dev only, gated by config | Great DX locally | Misconfig risk | Local/dev environments only |
| Strip at translation boundary | Leak impossible downstream | Requires discipline | Default in all shared code |
| Strip at serialization boundary | Centralized | Late; other sinks may leak | Acceptable as defense-in-depth, not as the only layer |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map DB errors by SQLSTATE to application codes | Forward the driver message |
| Keep the raw cause on the internal error object | Copy driver text into `message` |
| Remove `X-Powered-By`/`Server` at the proxy | Advertise versions |
| Use generic messages for connection errors | Echo hostnames and ports |
| Gate stack output on an explicit allowlist | Gate it on `NODE_ENV !== "production"` alone |

## Common mistakes

- **Relying on a single gate.** One env var is one mistake away from leaking; use translation-time
  stripping plus a serializer.
- **Translating generic `Error`.** Wrapping everything in `new Error(msg)` collapses categories and
  invites leaking the original text.
- **Leaving driver libraries in verbose mode.** Some clients log full statements at `info` level.
- **Forgetting the non-response sinks.** Hostnames in metric labels are just as leaked as in bodies.

## Checklist

- [ ] Are DB errors translated by SQLSTATE before they leave the repository layer?
- [ ] Does any external response ever contain `.stack`?
- [ ] Are `Server`/`X-Powered-By` and friends removed at the edge?
- [ ] Do connection-error messages name internal hosts, ports, or buckets?
- [ ] Is the full cause retained internally for operators?

## Related

- [Errors as a Disclosure Channel](./01-errors-as-a-disclosure-channel.md)
- [Secrets, PII, and Tenant Leakage](./03-secrets-pii-and-tenant-leakage.md)
- [Deep dive: Information Disclosure Channels](../02-deep-dive/01-information-disclosure-channels.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Glossary](../../../GLOSSARY.md)
