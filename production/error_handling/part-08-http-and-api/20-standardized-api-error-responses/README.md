# Chapter 20 — Standardized API Error Responses

> Part VIII · _Estimated reading time: 70–95 min_
> **Prerequisite:** [HTTP Error Semantics (Ch. 19)](../19-http-error-semantics/README.md)

## One-sentence summary

An error response is a **contract object** — status + headers + a structured body — and
RFC 9457 Problem Details (`application/problem+json`) is the modern default shape for that
body, extended with your **stable application codes**, field-level errors, and request IDs
while never leaking internals.

## Why this matters in production

Ad-hoc error bodies are the most common source of client-side fragility in SaaS APIs:
`{message}` here, `{error: {code}}` there, a bare string for legacy endpoints, HTML for the
rest. Every inconsistency forces SDK authors to write per-endpoint special cases, forces
support to string-match messages that were never stable, and forces your own frontend to
guess. A single standardized envelope turns errors into **first-class data**: SDKs branch on
`code`, UIs render `errors[]` field-by-field, support greps `requestId`, and documentation
stays honest because the shape is generated from one type.

## Chapter map

The chapter has 20 sections. They are grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-error-envelope-and-rfc-9457.md`](./01-concepts/01-error-envelope-and-rfc-9457.md) | 20.1, 20.2 | What an error envelope is; RFC 9457's five members and why it replaced ad-hoc shapes |
| [`01-concepts/02-problem-detail-fields.md`](./01-concepts/02-problem-detail-fields.md) | 20.3, 20.4, 20.5, 20.6 | `type`, `title`, `detail`, `instance`: what each field may and may not say |
| [`01-concepts/03-app-codes-ids-and-field-details.md`](./01-concepts/03-app-codes-ids-and-field-details.md) | 20.7, 20.8, 20.9 | Extending Problem Details: stable `code`, `errors[]` field details, `requestId` |
| [`01-concepts/04-multiple-and-pagination-errors.md`](./01-concepts/04-multiple-and-pagination-errors.md) | 20.10, 20.11 | Multiple errors: validation arrays vs multi-status; error handling inside paginated list endpoints |
| [`01-concepts/05-consistency-and-information-safety.md`](./01-concepts/05-consistency-and-information-safety.md) | 20.14, 20.15, 20.16, 20.17 | One shape everywhere; why stack traces and DB/infra details never ship |
| [`02-deep-dive/01-problem-details-mechanics-and-versioning.md`](./02-deep-dive/01-problem-details-mechanics-and-versioning.md) | 20.12, 20.13, 20.18, 20.19, 20.20 | Serialization mechanics, `Content-Type`/`Accept` negotiation, response versioning, generated-SDK tolerance, third-party contracts |
| [`03-practical-examples/01-problem-details-envelope-in-code.md`](./03-practical-examples/01-problem-details-envelope-in-code.md) | 20.1–20.13 applied | A full envelope builder in TypeScript, end-to-end examples |
| [`03-practical-examples/02-error-shapes-across-scenarios.md`](./03-practical-examples/02-error-shapes-across-scenarios.md) | 20.1–20.20 applied | Complete JSON bodies for 400/401/403/404/409/422/429/5xx, bulk, and pagination errors |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Envelope rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | The error envelope spec: field table, extension registry, naming rules |

## Learning objectives

By the end you can:

- Design an RFC 9457-compliant envelope and defend every field choice (`type` as identifier,
  `detail` as instance-specific prose, `instance` as the occurrence pointer).
- Extend Problem Details with `code`, `errors[]`, and `requestId` **without** breaking the
  standard's contract or generic tooling.
- Produce field-level validation payloads that clients can render directly, with stable
  per-field codes.
- Keep one envelope shape across every endpoint, content type, and API version — and
  version changes so old SDKs keep working.
- Guarantee the serializer can never emit stack traces, SQL, or infrastructure details,
  regardless of which handler threw.

## Key takeaways

1. **RFC 9457 is the envelope; your registry is the vocabulary.** The standard gives you the
   five members and the media type; your stable `code` values give clients something to
   branch on that `title`/`detail` prose never can.
2. **`type` is an identifier, not a sentence.** It should be stable, documentable, and
   machine-comparable; `detail` is the human, instance-specific sentence.
3. **One shape beats ten pretty shapes.** Bulk errors, validation errors, auth errors, and
   server errors all use the same base object — variation happens in *members*, not in
   alternate top-level shapes.
4. **Safety is structural.** Don't redact at call sites; make the public problem type
   incapable of holding a stack trace or SQL string, and serialize only that type.
5. **Version the additions, not the surprises.** New optional members are backward-compatible;
   renamed/removed members are not. Publish tolerance rules so SDKs survive evolution.

## Exercises

1. List every distinct error body your API returns today. Count the shapes. (Usually: too
   many.) Map each to the envelope spec and write the migration diff.
2. Design the `errors[]` entry schema for your top validation endpoint; write the JSON for a
   cross-field failure (e.g. `startDate` after `endDate`) — which field gets the error?
3. Draft your `type` URI namespace (`/problems/...`) for your ten most common codes; check
   for collisions with the registry's public codes.
4. Write the SDK tolerance rule for unknown members: ignore-or-crash? (Answer in
   [`02-deep-dive/01-problem-details-mechanics-and-versioning.md`](./02-deep-dive/01-problem-details-mechanics-and-versioning.md)
   — then verify your own SDK actually behaves that way.)

## Related

- [HTTP Error Semantics (Ch. 19)](../19-http-error-semantics/README.md)
- [API Boundary and Middleware Error Handling (Ch. 21)](../21-api-boundary-and-middleware-error-handling/README.md)
- [Designing the Application's Error Model](../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Glossary](../../GLOSSARY.md)
