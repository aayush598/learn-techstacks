# Chapter 34 — Security Principles for Error Handling

> Part XIII · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Chapter 20 — Standardized API Error Responses](../../part-08-http-and-api/20-standardized-api-error-responses/README.md)

## One-sentence summary

An error is an **unintended information disclosure channel**: production-grade error handling
means every failure leaves your process through a deliberate boundary that reveals what the
caller needs — and nothing an attacker can use.

## Why this chapter matters

Breach reports keep proving the same lesson: the exploited detail was often *in an error message*.
A stack trace reveals file paths and library versions; a database exception reveals table names
and sometimes query fragments; a verbose 500 on a forgotten password reveals which emails are
registered; a timing difference of 40 ms reveals the same thing without a single different
character. None of these look like security bugs in code review — they look like "helpful error
handling". This chapter gives you the threat model, the leakage classes, and the defaults that
make verbose debugging and tight disclosure coexist.

## Chapter map

The chapter has 18 sections grouped into twelve files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-errors-as-a-disclosure-channel.md`](./01-concepts/01-errors-as-a-disclosure-channel.md) | 34.1, 34.16–34.18 | Why errors leak by default; secure defaults for unknown exceptions; disclosure policy; feedback vs confidentiality |
| [`01-concepts/02-stack-traces-schemas-and-infrastructure-leakage.md`](./01-concepts/02-stack-traces-schemas-and-infrastructure-leakage.md) | 34.2–34.4 | Stack trace risks, schema/query leakage, hostname/infra leakage |
| [`01-concepts/03-secrets-pii-and-tenant-leakage.md`](./01-concepts/03-secrets-pii-and-tenant-leakage.md) | 34.5–34.7 | Secret/credential leakage, PII in messages, multi-tenant leakage |
| [`01-concepts/04-authorization-disclosure-enumeration-and-timing.md`](./01-concepts/04-authorization-disclosure-enumeration-and-timing.md) | 34.8–34.10 | Authorization failure disclosure, user enumeration, timing disclosure |
| [`01-concepts/05-injection-dos-serialization-and-reflection.md`](./01-concepts/05-injection-dos-serialization-and-reflection.md) | 34.11–34.15 | Injection risks, pathological-failure DoS, unsafe serialization, sanitizing external content, reflecting untrusted input |
| [`02-deep-dive/01-information-disclosure-channels.md`](./02-deep-dive/01-information-disclosure-channels.md) | 34.1–34.7 (mechanics) | The seven practical disclosure channels and how data actually travels through each |
| [`02-deep-dive/02-timing-attacks-and-user-enumeration.md`](./02-deep-dive/02-timing-attacks-and-user-enumeration.md) | 34.9–34.10 (mechanics) | Constant-time comparison, constant-work auth paths, measuring your own leakage |
| [`02-deep-dive/03-redaction-strategy.md`](./02-deep-dive/03-redaction-strategy.md) | 34.5–34.6, 34.13–34.14 (mechanics) | Classify, redact at source, allowlist-serialize, audit |
| [`03-practical-examples/01-error-sanitizer-allowlist-serializer.md`](./03-practical-examples/01-error-sanitizer-allowlist-serializer.md) | 34.13, 34.16 | A working allowlist serializer that sanitizes any error before it leaves the process |
| [`03-practical-examples/02-secure-default-error-boundary.md`](./03-practical-examples/02-secure-default-error-boundary.md) | 34.16–34.18 | A boundary that converts unknown exceptions into a generic 500 + correlation ID, with tiered detail |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Security rules and anti-patterns for error handling |
| [`05-reference/README.md`](./05-reference/README.md) | all | Disclosure policy matrix, leakage checklist, CWE/OWASP quick reference |

## Learning objectives

By the end you can:

- Name the channel an error uses to leak (response body, header, log, job record, metric label)
  and the class of data it can carry.
- Replace a verbose catch-all with **secure defaults**: generic message, correlation ID, internal
  detail.
- Recognize **schema, hostname, secret, PII, and tenant leakage** in messages you wrote yourself.
- Explain why **user enumeration** is an error-handling bug and fix it with uniform messages and
  constant-work paths.
- Pick safe behaviors for **injection, reflection, serialization, and pathological failure**
  scenarios.

## Key takeaways

1. **Errors leak by default.** The runtime's exception object is optimized for debugging, not for
   disclosure control. You must bound it before it crosses a trust boundary.
2. **Secure default for unknown exceptions:** external `500` with a stable code and correlation
   ID; full detail only in internal sinks (exception tracker, structured logs).
3. **404 often beats 403** when the caller must not learn that a resource exists at all.
4. **Timing is data.** Any response whose latency correlates with a secret comparison or a user
   lookup is a disclosure channel (CWE-203).
5. **Reflection is the attacker's compiler.** An error page that echoes request input becomes
   XSS, log injection, or response-splitting depending on the sink.
6. **Disclosure policy beats ad-hoc judgment.** Write down what each audience may see once, then
   enforce it in the serializer — not in forty catch blocks.

## Exercises

1. Trigger five different unhandled exceptions in a staging environment and diff the responses.
   List every field that differs and mark which ones an attacker learns from.
2. Write your error disclosure policy as a matrix (audience × visible fields) and map it onto the
   serializer from `03-practical-examples/01`.
3. Instrument your login endpoint to log per-stage timings (user lookup, hash compare, session
   issue). Measure whether "unknown user" and "wrong password" differ by more than noise.
4. Search your codebase for `JSON.stringify(err` and `err.stack` in code that can reach an HTTP
   response. Replace each with the sanitizer.
5. Feed your error serializer a pathological input (circular cause chain, 10-level nesting, 1 MB
   message) and verify it terminates quickly with a bounded output.

## Related

- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../36-sensitive-data-and-error-context/README.md)
- [Chapter 20 — Standardized API Error Responses](../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter 19 — HTTP Error Semantics](../../part-08-http-and-api/19-http-error-semantics/README.md)
- [Glossary](../../GLOSSARY.md)
