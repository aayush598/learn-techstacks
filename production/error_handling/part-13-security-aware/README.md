# Part XIII — Security-Aware Error Handling

> **Chapters 34–36.** Every error is a message you did not fully design — and attackers read
> messages for a living. This part teaches you to treat error handling as a **security control
> surface**: errors must be useful enough for operators and honest enough for users, while leaking
> nothing an adversary can exploit — no stack traces, no schema fragments, no tenant data, no
> timing signals, no credential material.

## Learning objectives

By the end of Part XIII you will be able to:

1. Treat every error path as a potential **information disclosure channel** and close the channels
   that matter (stack traces, SQL fragments, hostnames, secrets, PII, tenant identifiers).
2. Apply **secure defaults for unknown exceptions**: a generic external response, a correlation ID,
   and full detail confined to internal sinks.
3. Choose **401 vs 403 vs 404 consistently**, without disclosing whether a resource exists to
   callers who must not know.
4. Defeat **user enumeration and timing disclosure** with uniform messages, constant-time
   comparison, and constant-work authentication paths.
5. Enforce **tenant isolation** in error handling: context must be explicit, checks must fail
   closed, and errors must never confirm another tenant's data.
6. Build a **redaction strategy**: classify sensitive data, redact at the source, serialize through
   an allowlist, and keep sensitive values out of nested causes and error chains.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 34 | [Security Principles for Error Handling](./34-security-principles-for-error-handling/README.md) | Errors as a disclosure channel, leakage classes (stack/schema/host/secret/PII/tenant), enumeration, timing, injection, unsafe serialization, disclosure policy |
| 35 | [Authentication, Authorization, and Tenant Isolation Errors](./35-auth-authorization-and-tenant-isolation-errors/README.md) | Credential and token failures, permissions, ownership, cross-tenant access, 401/403/404 discipline, IdP and policy-engine failure modes |
| 36 | [Sensitive Data and Error Context](./36-sensitive-data-and-error-context/README.md) | Sensitive metadata taxonomy, secrets, PII, payment data, redaction vs omission, allowlist serialization, nested-cause leakage, privacy-aware standards |

## How the chapters fit together

```text
              ┌──────────────────────────────────────────────────────┐
              │            an error crosses a trust boundary         │
              └───────────────────────────┬──────────────────────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
   Ch. 34 principles              Ch. 35 authz errors           Ch. 36 data classes
   "what can this error           "did this caller               "which fields are
    reveal, and to whom?"          deserve to see it?"            sensitive, and how
                                                                  do they leave?"
            │                             │                             │
            └─────────────────────────────┼─────────────────────────────┘
                                          ▼
                    one sanitized, policy-checked error response
```

- **Chapter 34** is the threat model: *channels* an attacker reads and the *defaults* that keep
  unknown failures safe.
- **Chapter 35** is the access-control layer: which status code, which message, and what the
  answer must *not* confirm when credentials, tokens, or tenancy are involved.
- **Chapter 36** is the data layer: a classification of sensitive payloads and the redaction and
  serialization mechanics that keep them inside your perimeter.

## The recurring cast in this part

| Cast member | Role in Part XIII |
| ----------- | ----------------- |
| **Acme SaaS** | Multi-tenant platform: tenant isolation, role checks, support tooling |
| **Checkout** | Payment flow: PCI DSS constraints on error context, idempotency keys as secrets |
| **ExportJob** | Background export: failure context for operators without leaking row data |
| **WebhookIngest** | Inbound Stripe webhooks: signature comparison, replay errors, payload redaction |
| **AgentRun** | LLM tool-calling agent: tool errors echoing prompts, provider error passthrough |

## Key takeaways

- **Errors are an API you did not intend to design.** Anything the exception object can carry —
  message, cause chain, stack, metadata — can leave the process unless you bound it.
- **Deny by default, disclose by policy.** Unknown exceptions get a generic 500 plus a correlation
  ID; detail goes to internal sinks only.
- **401 vs 403 vs 404 is a security decision, not a style choice.** 404 often protects better
  than 403 because it confirms nothing.
- **Timing is a channel.** A fast "user not found" versus a slow "wrong password" is user
  enumeration solved for free by an attacker with a stopwatch.
- **Redaction is a data-classification problem first, a regex problem second.** Allowlists beat
  denylists; classification drives serialization.
- **Fail closed on authorization dependencies.** If the policy engine or IdP is unavailable, the
  safe answer is "deny", not "allow and sort it out later".

## Exercises

1. Take five real error responses from your API and list every field an unauthenticated caller
   learns from each. Mark any field that reveals infrastructure, data shape, or tenancy.
2. Write your disclosure policy as a table: audience (public / authenticated user / tenant admin /
   operator / internal system) × what each may see (status, code, message, detail, stack, context).
3. Find every place your codebase compares a secret (token, API key, webhook signature). Convert
   each comparison to a constant-time primitive and verify the failure path is constant-work.
4. Pick your login, password-reset, and signup endpoints. Prove with measurements that response
   time does not distinguish "unknown user" from "known user, wrong password".
5. Audit one error path end-to-end (e.g. `ExportJob` failure): from thrown exception through
   serialization to log, queue record, and API response. Classify every value as public, internal,
   or sensitive, and redact everything that is not public.

## Related

- [Part XII — Asynchronous Processing and Background Jobs](../part-12-async-and-background-jobs/README.md)
- [Part VIII — HTTP and API Error Handling](../part-08-http-and-api/README.md)
- [Glossary](../GLOSSARY.md)
- [Style guide](../_STYLE_GUIDE.md)
