# Chapter 36 — Sensitive Data and Error Context

> Part XIII · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 34 — Security Principles for Error Handling](../34-security-principles-for-error-handling/README.md)

## One-sentence summary

Error **context** is where sensitive data hides: production-grade error handling means every piece of
context an error carries is **classified before it can leave the process**, redacted or omitted by
policy, and emitted through an **allowlist serializer** — never a `JSON.stringify(err)`.

## Why this chapter matters

An error object accumulates context as it propagates: a request body, a DB row, a provider payload, a
user's free-text input, a query string, a nested cause. Each is a potential secret, PII, financial
value, or third-party token. Teams usually handle the top-level message and forget the **cause chain**
and the **metadata bag** — which is exactly where a Stripe payload, a bearer token, or a customer email
rides along into logs, DLQs, and error responses. This chapter gives you the classification, the
redaction mechanics, and the standards that make "nothing sensitive leaves" a verifiable property.

## Chapter map

The chapter has 14 sections grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-defining-sensitive-metadata.md`](./01-concepts/01-defining-sensitive-metadata.md) | 36.1 | What counts as sensitive metadata, and how to classify it |
| [`01-concepts/02-secrets-and-tokens.md`](./01-concepts/02-secrets-and-tokens.md) | 36.2 | Secrets/tokens: non-collection, fingerprints, header stripping |
| [`01-concepts/03-pii-and-user-input.md`](./01-concepts/03-pii-and-user-input.md) | 36.3, 36.5 | PII categories and untrusted user input in errors |
| [`01-concepts/04-payment-financial-query-and-third-party.md`](./01-concepts/04-payment-financial-query-and-third-party.md) | 36.4, 36.6–36.7 | Payment/financial data (PCI), query parameters, third-party payloads |
| [`01-concepts/05-redaction-omission-sanitization-and-allowlists.md`](./01-concepts/05-redaction-omission-sanitization-and-allowlists.md) | 36.8–36.11 | Redaction vs omission, sanitizing messages, safe serialization, context allowlists |
| [`02-deep-dive/01-nested-causes-and-leakage-via-chains.md`](./02-deep-dive/01-nested-causes-and-leakage-via-chains.md) | 36.12–36.13 | How sensitive data hides in causes and leaks through chains |
| [`02-deep-dive/02-safe-serialization-and-context-allowlists.md`](./02-deep-dive/02-safe-serialization-and-context-allowlists.md) | 36.9–36.11 (mechanics) | Bounded, allowlist-based serialization of context |
| [`02-deep-dive/03-privacy-aware-standards.md`](./02-deep-dive/03-privacy-aware-standards.md) | 36.14 | GDPR/PCI/CCPA constraints on error context and retention |
| [`03-practical-examples/01-redacting-pii-and-secrets-in-context.md`](./03-practical-examples/01-redacting-pii-and-secrets-in-context.md) | 36.2–36.6, 36.8 | A redaction pass for PII, secrets, payment, and query values |
| [`03-practical-examples/02-context-allowlist-for-errors.md`](./03-practical-examples/02-context-allowlist-for-errors.md) | 36.7, 36.10–36.13 | An allowlist context builder + safe chain serializer |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Sensitive-data rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Data classification, redaction table, standards map |

## Learning objectives

By the end you can:

- Classify every piece of error context as public/internal/sensitive/PII/secret/payment.
- Apply **non-collection to secrets** and redaction to unavoidable sensitive values.
- Recognize **PII and user input** that arrive through messages, query strings, and provider payloads.
- Handle **payment/financial data** under PCI DSS constraints.
- Serialize error context safely with an **allowlist** and bounded cause depth.
- State the privacy obligations (GDPR/CCPA/PCI) that govern error context.

## Key takeaways

1. **Classification comes first.** You cannot redact what you have not labeled.
2. **Non-collection beats redaction** for secrets: never read the value into the error.
3. **Causes are the leak you forget.** Sensitive data rides in nested `cause` chains.
4. **Allowlist, deny unknown.** A new context field is denied until classified.
5. **Retention is part of the risk.** The longer a sink keeps data, the more dangerous it is.
6. **Privacy law treats error logs as personal data.** A PII-in-logs incident is a reportable breach.

## Exercises

1. Take one error type and list every field it can carry; classify each. Which are unclassified?
2. Walk a nested cause chain from a real DB/provider error and mark every sensitive value.
3. Find every place a request body, query string, or provider payload is attached to an error; apply
   the allowlist builder.
4. Write a canary test injecting a synthetic PAN, email, and token through a failure path.
5. Document retention per sink and confirm secrets/PII are absent from the longest-lived ones.

## Related

- [Chapter 34 — Security Principles for Error Handling](../34-security-principles-for-error-handling/README.md)
- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 6 — Designing the Application's Error Model](../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Chapter 6 §6.18 — Preventing Sensitive Data](../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Glossary](../../GLOSSARY.md)
