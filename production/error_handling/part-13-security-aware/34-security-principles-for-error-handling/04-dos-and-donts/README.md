# Chapter 34 — Do's and Don'ts

> Part XIII · Chapter 34 · all sections · _Estimated reading time: 9 min_

## In one sentence

Security-aware error handling is defined by **bounded disclosure**: every error crosses one
reviewed boundary, every channel gets only policy-approved fields, secrets are never collected, and
the boundary fails **closed**.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | Treat every error path as a disclosure channel | Assume only the response matters |
| 2 | Default unknown errors to a generic `500` + `requestId` | Send `err.message` or `err.stack` |
| 3 | Route full detail to the RBAC-protected tracker only | Dump full detail to logs and DLQ |
| 4 | Translate DB errors by SQLSTATE to stable codes | Forward driver messages with table names |
| 5 | Remove `Server`/`X-Powered-By` at the proxy | Advertise versions and runtimes |
| 6 | Never read a secret into an error object | `throw new Error(\`bad key ${key}\`)` |
| 7 | Fingerprint secrets you must correlate | Store the raw token anywhere |
| 8 | Classify every error field, allowlist each sink | Blocklist "known-bad" strings |
| 9 | Return a uniform `404` for opaque resources | Return a distinguishing `403` |
| 10 | Use one generic code for all login failures | Say "no such user" |
| 11 | Always run a real-cost hash, real or dummy | Early-return before hashing |
| 12 | Compare secrets with constant-time primitives | Compare secrets with `===` |
| 13 | Return uniform reset/signup responses | Confirm account existence |
| 14 | Emit structured JSON logs | Interpolate user input into log lines |
| 15 | Parameterize diagnostic queries | Re-run a query with user input |
| 16 | Bound cause-chain depth and payload size | Serialize the whole entity |
| 17 | Schema-validate peer/queue error payloads | Deserialize errors with native parsers |
| 18 | HTML-escape error pages; set CSP | Render raw error text as HTML |
| 19 | Fail closed on auth/authz errors | `catch (e) { next(); }` in auth middleware |
| 20 | Guard `res.status()` with `headersSent` | Write a second response |
| 21 | Keep the boundary itself from throwing | Let a sink error change the outcome |
| 22 | Canary-test secrets/PII on failure paths | Trust redaction without a test |

## Anti-patterns with symptoms

### ❌ Verbose global handler

```ts
app.use((err, _req, res) => res.status(500).json({ message: err.message, stack: err.stack }));
```

**Symptom:** stack traces and internal paths in production responses; scanners flag them instantly.
**Fix:** generic `500` + `requestId`; full detail to the tracker.

### ❌ Interpolated secret

```python
raise AuthError(f"invalid token {token}")
```

**Symptom:** a live credential appears in logs, alerts, and sometimes support tickets.
**Fix:** never read the token into the error; store a fingerprint instead.

### ❌ Enumeration by code

```ts
if (!user) return res.status(404).json({ code: "NO_USER" });
if (!ok)  return res.status(401).json({ code: "BAD_PASSWORD" });
```

**Symptom:** attacker harvests valid accounts from distinct codes.
**Fix:** one `401 { code: "INVALID_CREDENTIALS" }` for both.

### ❌ Timing oracle

```ts
if (!user) return res.status(401); // fast path — no hash work
await verifyPassword(password, user.passwordHash);
```

**Symptom:** unknown-user requests are measurably faster than wrong-password requests.
**Fix:** always run `verifyPassword` against a dummy hash of the current algorithm/cost.

### ❌ Leaky DB translation

```ts
throw new Error(`DB error: ${pgErr.message}`);
```

**Symptom:** table and column names in user-facing responses.
**Fix:** map by SQLSTATE to stable codes; keep the driver error as an internal cause.

### ❌ Log injection

```ts
log.info(`webhook failed: body=${JSON.stringify(body)}`);
```

**Symptom:** attacker-controlled newlines forge log lines; secrets land in logs.
**Fix:** structured record with an allowlist of fields; never raw body.

### ❌ Metric label with PII

```ts
metrics.increment("login_failed", { email });
```

**Symptom:** a private dashboard becomes a searchable PII index exported to a vendor.
**Fix:** bounded labels only (`{ code, provider }`); per-user detail in scoped records.

### ❌ Fail-open authorization

```ts
try { check(req); } catch { next(); } // continues on error
```

**Symptom:** a policy-engine outage becomes an authorization bypass.
**Fix:** catch → `AuthzError` → fail closed; alarm on `authz_check_error_total`.

## Code-review questions

1. Which of the seven channels does this error reach, and what does each see?
2. Could this message interpolate a secret, PII, or a cross-tenant value?
3. Is the source a driver/provider error being forwarded raw?
4. Does any comparison here touch a secret? Is it constant-time?
5. Do unknown-user and wrong-password take the same time?
6. Does an authz check here fail closed?
7. Is serialization bounded in depth and size?
8. Could the error body differ between own-resource and other-tenant cases?
9. Is there a canary test covering this path?

## Minimal policy snippet

```yaml
disclosurePolicy:
  unknownError: { status: 500, code: INTERNAL_ERROR, message: generic }
  securityPath: { status: 404, body: uniform }
  responseFields: [code, message, requestId]
  logFields: [code, class, provider, requestId]
  metricLabels: [code, provider]
  tracker: fullDetail                # RBAC + audited
  secrets: neverCollected            # fingerprint if correlation needed
  causeDepth: 6
  canary: { secrets: true, pii: true }
```

## Related

- [Errors as a Disclosure Channel](./../01-concepts/01-errors-as-a-disclosure-channel.md)
- [Authorization Disclosure, Enumeration, and Timing](./../01-concepts/04-authorization-disclosure-enumeration-and-timing.md)
- [Chapter 34 Reference](../05-reference/README.md)
- [Chapter 35 — Auth Errors Do's and Don'ts](../../35-auth-authorization-and-tenant-isolation-errors/04-dos-and-donts/README.md)

