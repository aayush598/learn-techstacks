# Defining Sensitive Metadata

> Part XIII · Chapter 36 · Section 36.1 · _Estimated reading time: 15 min_
> **Prerequisite:** [Chapter 34 — Errors as a Disclosure Channel](../../34-security-principles-for-error-handling/01-concepts/01-errors-as-a-disclosure-channel.md)

## In one sentence

**Sensitive metadata** is any context an error can carry that must not reach every sink — and the
whole of Chapter 36 rests on one act: **classifying each field before it enters an error**, so policy
(not memory) decides where it may go.

## Why this matters in production

An error object is a bag. It holds what the developer attached during debugging: the request body, the
failing entity, the provider response, the user's input, a nested cause. Nobody decided field by field
what was safe — the default was "attach it, we'll figure it out later". Sensitive metadata is the name
for the part of that bag that carries secrets, PII, financial data, or third-party material. Defining
it is the prerequisite for redacting it: you cannot protect a field you never named.

## Core concept — a classification taxonomy

| Class | Definition | Typical error fields | Allowed sinks |
| ----- | ---------- | -------------------- | ------------- |
| **Public** | Safe for any audience | code, message, HTTP status | all |
| **Internal** | Operators/engineers only | class, provider name, retryable | logs, tracker |
| **Tenant-confidential** | Own-tenant only | own resource ids, own quota | tenant-scoped sinks |
| **Sensitive** | Broadly restricted | tenantId, userId, internal reasons | DLQ, tracker (RBAC) |
| **PII** | Regulated personal data | email, name, phone, IP, address | tracker (RBAC), minimized |
| **Payment / financial** | PCI/PII scope | PAN, last4, amounts tied to a person | never (PAN); restricted otherwise |
| **Secret** | Credentials/material | tokens, keys, passwords, cookies, signatures | never |

The classes are cumulative in risk: a **secret** is denied everywhere including the tracker; **PII**
and **payment** are permitted only in a narrowly scoped, RBAC-controlled sink.

## What "metadata" means here

Error context splits into distinct pockets, each of which accumulates different data:

| Context pocket | Common contents | Typical sensitivity |
| -------------- | --------------- | ------------------- |
| Message / safe message | constant, chosen text | public (must stay constant) |
| Codes / class | stable identifiers | public / internal |
| Field-level details | field name, rule, code | public (never the value) |
| Request context | path, method, requestId, tenantId | internal / sensitive |
| Payload context | body, params, query | PII / secret / payment |
| Provider context | upstream message, requestId, status | internal / PII |
| Cause chain | nested errors, driver text | mixed — often the worst offender |

> ⚠️ **Hazard.** The **payload context** and the **cause chain** are where sensitive data hides, because
> they are populated by convenience rather than design.

## Classifying in practice

Attach a sensitivity label at the point a value is added to an error:

```ts
type Sensitivity = "public" | "internal" | "tenant" | "sensitive" | "pii" | "payment" | "secret";

// A typed context builder forces a classification per field.
interface Classified<T> { value: T; sensitivity: Sensitivity }

function field<T>(value: T, sensitivity: Sensitivity): Classified<T> {
  return { value, sensitivity };
}

const ctx = {
  requestId: field(req.id, "internal"),
  tenantId: field(principal.tenantId, "sensitive"),
  email: field(user.email, "pii"),
  last4: field(card.last4, "payment"),
  idempotencyKey: field(key, "secret"), // or better: don't attach at all
};
```

The classification travels with the value, so the serializer can decide per sink without guessing.

## Decision rule

```text
When you attach a field to an error, answer three questions:
  1. Can this value ever be a secret/credential?      -> if yes, do NOT collect it
  2. Is it personal / financial data?                  -> if yes, classify PII/payment
  3. Could an attacker use it? (internal host, id, query)
                                                       -> if yes, classify sensitive/internal
  Unclassified -> DENIED at every sink (deny by default).
```

## Key data / numbers

- **PII categories commonly cited**: name, email, phone, postal address, date of birth, government ID,
  IP address, device identifier, financial account, biometric data.
- **PCI DSS** scope: PAN (16-digit card number) must never be stored/logged after authorization;
  last4 is out of PCI scope but still PII-linked.
- **GDPR Article 4(1)**: "personal data" is any information relating to an identifiable person; error
  logs containing emails are personal data and fall under breach rules (Article 33, 72 hours).
- **CWE-359** (exposure of private personal information), **CWE-532** (sensitive info in logs),
  **CWE-312** (cleartext storage).
- **Deny-by-default**: an unclassified field is treated as if it were a secret.

## Real-world use case — Acme SaaS

Acme attached a `context` bag to every error containing `req.body`, `req.query`, and the resolved
entity. Most fields were fine; three were not — a `password` on the signup path, a `card` object on the
Checkout path, and a `token` in a query parameter. None were classified, so all reached the log and the
DLQ. Fix: the error model now requires every context field to pass through `field(value, sensitivity)`;
unclassified fields are dropped by the serializer; and a lint rule bans attaching raw `req.body` /
`req.query` to errors. The classification act alone surfaced the three leaks.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Classify every field (typed) | Policy-driven, auditable | Boilerplate | All error context |
| Classify only at the sink | Less upfront work | Easy to forget a sink | Never as the only layer |
| Manual review per change | No code overhead | Scales poorly, drifts | Supplement only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify each context field at the source | Attach a `req.body` blob |
| Deny unclassified fields | Assume a field is "probably fine" |
| Keep messages constant | Interpolate values into messages |
| Treat `cause` as context needing classification | Trust nested causes to be safe |
| Document the classes | Rely on tribal knowledge |

## Common mistakes

- **No taxonomy.** "Sensitive" becomes everyone's judgment call.
- **Classifying late.** By the time it reaches the sink, it has already spread.
- **Forgetting request/query context.** Query strings carry tokens and PII.
- **Ignoring causes.** The nested driver/provider error is often the worst leak.
- **Assuming internal = safe.** Logs are widely readable.

## Checklist

- [ ] Is there a written sensitivity taxonomy?
- [ ] Does every context field carry a classification?
- [ ] Are unclassified fields denied by default?
- [ ] Are messages constants, not templates?
- [ ] Is `cause` treated as context subject to classification?
- [ ] Is the taxonomy documented and reviewed?

## Related

- [Secrets and Tokens](./02-secrets-and-tokens.md)
- [PII and User Input](./03-pii-and-user-input.md)
- [Redaction, Omission, Sanitization, and Allowlists](./05-redaction-omission-sanitization-and-allowlists.md)
- [Deep dive: Safe Serialization and Context Allowlists](../02-deep-dive/02-safe-serialization-and-context-allowlists.md)
- [Glossary](../../../GLOSSARY.md)
