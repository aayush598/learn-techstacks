# Deep Dive — Privacy-Aware Standards

> Part XIII · Chapter 36 · Section 36.14 (mechanics) · _Estimated reading time: 18 min_
> **Prerequisite:** [Defining Sensitive Metadata](../01-concepts/01-defining-sensitive-metadata.md)

## In one sentence

Error context is governed by **privacy and payment standards** — GDPR (personal data, breach
notification, minimization), CCPA/CPRA (rights to know/delete), and PCI DSS (card data, log access) —
so retention, access, and minimization must be designed, not assumed.

## Why this matters in production

Compliance teams treat logs as a data store, because they are. An error log containing customer emails
is personal data with a retention clock and a breach-notification obligation. A debug log with a card
number is a PCI finding. A DLQ holding webhook bodies is a processing activity. None of this is about
"security theater" — it is the difference between a contained incident and a reportable breach with a
72-hour deadline and possible fines.

## GDPR (EU personal data)

| Article | Requirement | Error-handling implication |
| ------- | ----------- | -------------------------- |
| Art. 4(1) | Definition of personal data | Emails, IPs, ids in errors are personal data |
| Art. 5(1)(c) | Data minimization | Collect only what the error needs |
| Art. 5(1)(e) | Storage limitation | Retention limits per sink |
| Art. 25 | Data protection by design | Classify + minimize at the source |
| Art. 32 | Security of processing | Pseudonymize; restrict access |
| Art. 33 | Breach notification (72 h) | A PII-in-logs event may be reportable |
| Art. 15/17 | Access / erasure rights | Can you find and delete a user's data in logs? |

Practical consequences:

- **Minimize** — do not attach PII to errors when a field name and rule suffice.
- **Pseudonymize** — salted hashes for correlation instead of raw values.
- **Bound retention** — logs days–months, DLQ days–weeks; delete on schedule.
- **Access requests** — you must be able to search logs for a data subject and, where required, delete.
- **Erasure** — design logs so personal data can be removed (or is stored pseudonymized).

## CCPA/CPRA (California)

| Right | Error-handling implication |
| ----- | -------------------------- |
| Right to know | Be able to report what personal info you hold, including in logs |
| Right to delete | Deletable or pseudonymized personal info |
| Right to opt out of "sale" | Log exports to third parties (metrics/trackers) must be audited |
| "Sensitive personal information" | Restrict use; note in classification |

The practical action is the same as GDPR: **minimize, pseudonymize, and know your sinks** (especially
third-party ones, which complicate "sale"/"share" analysis).

## PCI DSS (card data)

| Requirement | Error-handling implication |
| ----------- | -------------------------- |
| Req 3.3 | Sensitive authentication data not stored after auth; PAN unreadable |
| Req 3.4 | Render PAN unreadable wherever stored |
| Req 10.3 | Do not log card data; restrict log access |
| Req 10.5 | Secure audit trails |
| Req 8 | Protect credentials (tokens/keys) in logs |

Practical consequences:

- **Never collect** PAN/CVC — not in messages, context, DLQ, or tracker.
- **Provider payloads** must be allowlisted (they echo card data).
- **Log access** must be restricted and audited.
- **Idempotency keys** and secrets are fingerprinted, never stored raw.

## Retention and access design

```text
Sink            Retention        Access               Contains
─────────────   ──────────────   ──────────────────   ──────────────────────
response        none             public               public fields only
logs            days–months      broad internal       no secrets; minimized PII
metrics         long             dashboards/vendors   bounded labels only
DLQ             days–weeks       operators            secrets stripped, tenant-scoped
support UI      long             support (RBAC)       tenant-scoped projection
tracker         months           engineers (RBAC)     full detail, no secrets/PAN
```

Two rules: **secrets and PAN are absent from every sink**, and the **longest-lived sinks hold the
least sensitive data**.

## Data-subject requests in error data

To support access/erasure, error records should: (a) key personal data by a **pseudonym** (salted hash
of user id), (b) be **searchable** by that pseudonym, and (c) be **deletable** or expire on schedule.
Storing raw emails in logs makes all three hard.

## Key data / numbers

- **GDPR Art. 33**: notify supervisory authority within **72 hours** of awareness of a breach.
- **CCPA/CPRA**: applies to California residents' personal information; includes sensitive personal
  information category.
- **PCI DSS v4.0**: Req 3.3/3.4 (card data), Req 10.3 (no card data in logs), Req 10.5 (audit trails).
- **Pseudonymization**: likely means "personal data that can no longer be attributed without additional
  information" — a salted hash plus protected salt.
- **Retention defaults (recommendation)**: logs 30–90 days, DLQ 14 days, tracker 90 days.

## Real-world use case — Acme SaaS

Acme received a GDPR access request for a customer and could not reliably find their personal data,
because it was scattered across raw request bodies in error logs with no pseudonym key. Fix: errors now
key personal data by a salted hash of the user id (`uidHash`), logs are searchable by that hash, raw
PII is minimized, retention was reduced to 90 days for logs and 14 for DLQ, and the DLQ payload is
tenant-scoped and secret-stripped. The change made the access and erasure processes feasible and was
required for Acme's SOC 2 / GDPR readiness review.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Pseudonymize + minimize | Compliance-friendly | Slightly less direct debugging | All personal data |
| Short retention | Lower exposure | Less historical forensics | Default |
| Raw PII in logs | Easy | Subject to retention/erasure duties | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Minimize PII in error context | Attach raw user records |
| Pseudonymize with a salted hash | Store raw emails for correlation |
| Bound retention per sink | Keep logs forever |
| Keep PAN out of every sink | Log card data "temporarily" |
| Document the sink inventory | Discover sinks during an incident |

## Common mistakes

- **Treating logs as exempt.** They are personal data.
- **No retention policy.** Erasure and storage-limitation duties fail.
- **Third-party sinks unaccounted.** Metrics/tracker exports complicate compliance.
- **Raw PII for correlation.** Should be pseudonymized.
- **PAN in the tracker.** PCI violation regardless of RBAC.

## Checklist

- [ ] Are error-context personal data minimized and pseudonymized?
- [ ] Is there a retention policy per sink?
- [ ] Can you search logs by data subject, and delete if required?
- [ ] Is PAN/CVC absent from every sink including the tracker?
- [ ] Is the sink inventory documented, including third parties?
- [ ] Is log access restricted and audited (PCI Req 10.3/10.5)?

## Related

- [Defining Sensitive Metadata](../01-concepts/01-defining-sensitive-metadata.md)
- [Payment, Financial, Query, and Third-Party Context](../01-concepts/04-payment-financial-query-and-third-party.md)
- [Chapter reference: Data classification and redaction table](../05-reference/README.md)
- [Chapter 34 — Security Principles for Error Handling](../../34-security-principles-for-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)
