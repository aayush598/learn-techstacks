# Injection, DoS, Serialization, and Reflection

> Part XIII · Chapter 34 · Sections 34.11–34.15 · _Estimated reading time: 18 min_
> **Prerequisite:** [Authorization Disclosure, Enumeration, and Timing](./04-authorization-disclosure-enumeration-and-timing.md)

## In one sentence

Error handling can *introduce* vulnerabilities — **injection** through error strings that reach a
query/shell/log, **DoS** from errors that are expensive to produce or unbounded to serialize,
**unsafe serialization** of error objects, and **reflection of untrusted input** into responses or
pages — so each sink needs a sanitizer, not just a formatter.

## Why this matters in production

Most teams secure their happy path and forget that errors are a second, less-reviewed path into the
same sinks. Four specific ways error handling becomes the vulnerability:

1. **Injection** — an error message built by concatenating user input is later executed (SQL), the
   shell, a template, or a downstream API.
2. **DoS from pathological failures** — an error that triggers an expensive retry loop, a huge
   serialization, or a circular-structure crash converts a handled failure into an outage.
3. **Unsafe serialization** — `JSON.stringify(err)` can throw on circular references or leak
   non-enumerable internals; deserializing error payloads can execute gadget code.
4. **Reflection** — echoing request input (a path, a query value, a header) into an error page
   yields XSS, response splitting, or log injection.

## Core concept — the four hazards

| Hazard | Where the error enters | What the attacker gains |
| ------ | ---------------------- | ----------------------- |
| **Injection** | A message concatenated into SQL, shell, template, header | Arbitrary query/command execution |
| **Pathological-failure DoS** | Error construction/serialization under load | Resource exhaustion, crash |
| **Unsafe deserialization** | Parsing an error payload from elsewhere | Code execution / type confusion |
| **Reflection** | Request input echoed into response/page/log | XSS, header injection, log forging |

### Injection (CWE-89, CWE-78, CWE-117)

The classic mistake is putting the failing value *into* the query that failed:

```ts
// ❌ The unmatched value is concatenated into a query. Attacker controls `code`.
const user = await db.query(`SELECT * FROM users WHERE invite_code = '${code}'`);
```

More subtly, an error handler may re-issue a "diagnostic" query with user input, or write the
message to a shell for "repair". The fix is the same as for the happy path: **parameterize**, never
concatenate, and prefer structured logging (JSON) over string interpolation.

### Pathological-failure DoS (CWE-400)

Errors should be *cheap*. Three anti-patterns make them expensive:

- **Retry amplification** — every error triggers immediate retries against an already-struggling
  dependency.
- **Unbounded serialization** — serializing a 50 MB payload because the error object references it.
- **Unbounded cause chains / circular refs** — walking the `cause` chain or `JSON.stringify` on a
  cyclic object can loop or stack-overflow.

### Unsafe serialization (CWE-502)

`JSON.stringify(err)` on an arbitrary thrown value is not safe: it can throw on cycles, include
non-serializable values, or expose fields you never inspected. Deserializing an error from a queue
or peer must use a **schema-validated** parser, not `eval`/`pickle`/native deserialization.

### Reflection (CWE-79, CWE-113)

Any error that echoes request input is a potential injection sink:

```text
GET /files/..%2f..%2fetc%2fpasswd
→ 404 {"message": "No file named '../../etc/passwd'"}
```

If that JSON is rendered into an HTML error page without escaping, it is XSS. If echoed into a
response header, it can be response splitting. If logged raw, it can forge log lines.

## How it works (mechanics)

```text
  untrusted input ──▶ validation fails
                          │
                          ▼
              build error with a STABLE code
              (input is NOT interpolated)
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
   log sink          response sink      page/HTML sink
   JSON encode,      allowlist fields,  HTML-escape,
   strip newlines    no raw input       CSP
```

Two invariants:
- **The error message is a constant chosen by you, not a template filled by the attacker.**
- **Every sink escapes for its own context**: JSON for logs, HTML for pages, header-safe for
  headers.

## Worked example — reflection and injection together

```ts
// ❌ Two bugs: reflection into the response, and concatenation into a log line.
app.get("/api/items/:id", (req, res) => {
  const id = req.params.id;
  try {
    return res.json(db.get(id));
  } catch (e) {
    log.info(`item lookup failed for id=${id}`);          // log injection (newline forging)
    res.status(404).send(`Item ${id} not found`);          // XSS / reflection
  }
});

// ✅ Stable code, structured log, escaped/typed response, validated input.
app.get("/api/items/:id", (req, res) => {
  const parsed = itemIdSchema.safeParse(req.params.id); // reject at the boundary first
  if (!parsed.success) {
    return res.status(400).json({ code: "INVALID_ID" }); // no echo of the raw value
  }
  const item = db.get(parsed.data); // parameterized internally
  if (!item) {
    log.info({ event: "item_lookup_miss", id: parsed.data }); // JSON: no forging
    return res.status(404).json({ code: "NOT_FOUND" });
  }
  res.json(item);
});
```

## Key data / numbers

- **OWASP Top 10 (2021)**: **A03: Injection**, **A05: Security Misconfiguration** (verbose errors
  as a config flaw).
- **CWE-89** SQL injection, **CWE-78** OS command injection, **CWE-117** improper output
  neutralization for logs (log injection), **CWE-79** cross-site scripting, **CWE-113** HTTP
  response splitting, **CWE-400** uncontrolled resource consumption, **CWE-502** deserialization of
  untrusted data.
- **Structured logging** (one JSON object per line) neutralizes log injection because newlines and
  control characters are encoded, not interpreted.
- **Response size bound**: cap serialized error payloads (commonly a few KB) and refuse to include
  bulk payloads in errors.
- **Cause-chain depth**: walk at most a small fixed depth (commonly 5–10) when serializing causes.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` logged failures with a template string that included the raw request body and
the `Stripe-Signature` header value. A crafted webhook containing `\n[ERROR] payment_captured` forged
a log line that paged the on-call team into investigating a payment that never happened, and the
signature value (a secret-derived material) landed in the log stream. Fix: `WebhookIngest` now logs a
structured record (`{ event, status, requestId, tenant }`) with no body and no signature, the raw
payload goes only to an access-controlled DLQ with secrets stripped, and a lint rule bans
request-derived values inside template-string log calls. Incident-to-fix time dropped because the
structured fields were queryable.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Structured JSON logs, stable messages | No injection, queryable | Slightly less human-readable | Default everywhere |
| Echo input for developer clarity | Easier local debugging | Injection/reflection risk | Never for untrusted input |
| Schema-validated error parsing across boundaries | Safe deserialization | Must maintain schemas | Queue/peer error messages |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Interpolate stable codes, never raw input | Build messages from `req.params` |
| Use parameterized queries in error paths | Re-issue a "diagnostic" query with input |
| Emit one bounded JSON log object | `log.info(\`... ${value}\`)` with user data |
| Cap cause-chain depth and payload size | Serialize the whole entity on a cycle |
| Escape per sink (HTML/header/JSON) | Render raw error text into HTML |

## Common mistakes

- **Treating the error path as trusted.** It is a second path into every same sink.
- **String-building the log line.** The single most common log-injection source.
- **Walking `cause` unbounded.** Circular chains crash the serializer.
- **Deserializing "error" payloads with native parsers.** Use a schema.
- **Echoing input "so the user knows what they typed".** Validate and reference, don't reflect.

## Checklist

- [ ] Does any error message interpolate a request-derived value?
- [ ] Are all logs structured (JSON) with stable, constant messages?
- [ ] Are diagnostic queries parameterized and free of user input?
- [ ] Is error serialization bounded in size and cause depth?
- [ ] Is any peer/queue error payload schema-validated before use?
- [ ] Are error pages HTML-escaped and covered by CSP?

## Related

- [Errors as a Disclosure Channel](./01-errors-as-a-disclosure-channel.md)
- [Deep dive: Redaction Strategy](../02-deep-dive/03-redaction-strategy.md)
- [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
- [Chapter 21 — API Boundary and Middleware Error Handling](../../../part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
