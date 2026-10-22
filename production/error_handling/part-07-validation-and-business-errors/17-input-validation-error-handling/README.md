# Chapter 17 — Input Validation Error Handling

> Part VII · _Estimated reading time: 90–130 min_
> **Prerequisite:** [Chapter 6 — Designing the Application's Error Model](../../part-03-error-models/06-designing-the-applications-error-model/README.md)

## One-sentence summary

Input validation is a **layered, aggregated, contract-driven check at the trust boundary** —
syntactic checks reject what cannot be parsed, semantic checks reject what does not fit the shape
and rules of the schema, and every rejection is reported as **stable field-level codes the client
can act on**, never as a vague "invalid request".

## Why this chapter matters

Validation is the highest-volume error path in any SaaS: most `4xx` responses your API produces
will be validation failures. If they are vague (`"400 Bad Request"` with no fields), users open
tickets; if they are inconsistent (a different shape per endpoint), SDKs break on every release;
if they are trusting (client-side only), you have a security hole; if they are duplicated across
layers, every rule change touches five files. Validation done right is **boring and mechanical** —
which is exactly what you want for the path 80% of your traffic walks.

## Chapter map

The chapter has 22 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-syntax-vs-semantic-and-rule-scope.md`](./01-concepts/01-syntax-vs-semantic-and-rule-scope.md) | 17.1, 17.16 | The three validation layers, and where validation stops and business rules begin |
| [`01-concepts/02-field-shape-and-format-rules.md`](./01-concepts/02-field-shape-and-format-rules.md) | 17.2–17.6 | Request structure, required fields, type mismatch, range/boundary, format |
| [`01-concepts/03-cross-field-conditional-nested-and-lists.md`](./01-concepts/03-cross-field-conditional-nested-and-lists.md) | 17.7–17.10 | Cross-field rules, conditional rules, nested objects, arrays/collections |
| [`01-concepts/04-aggregation-and-field-error-representation.md`](./01-concepts/04-aggregation-and-field-error-representation.md) | 17.11–17.15 | Bulk failures, aggregated vs fail-fast, field-level representation, stable codes, avoiding duplicates |
| [`01-concepts/05-trust-boundaries-clients-and-contracts.md`](./01-concepts/05-trust-boundaries-clients-and-contracts.md) | 17.17–17.22 | Trust-boundary validation, client-side vs server-side, malformed/oversized input, localization, schema leakage, consistent contracts |
| [`02-deep-dive/01-aggregation-mechanics.md`](./02-deep-dive/01-aggregation-mechanics.md) | 17.11–17.13 | How accumulation actually works: pipelines, ordering, caps, and partial validation |
| [`02-deep-dive/02-validation-at-the-trust-boundary.md`](./02-deep-dive/02-validation-at-the-trust-boundary.md) | 17.17–17.19, 17.21 | The exact parse pipeline, size/type guards, and what an attacker sees |
| [`02-deep-dive/03-stable-codes-dedup-and-localization.md`](./02-deep-dive/03-stable-codes-dedup-and-localization.md) | 17.14, 17.15, 17.20, 17.22 | Code registry, duplicate-code detection, message keys, contract versioning |
| [`03-practical-examples/01-create-project-dto-to-422-envelope.md`](./03-practical-examples/01-create-project-dto-to-422-envelope.md) | all | DTO → field errors → HTTP `422` Problem Details envelope, end to end |
| [`03-practical-examples/02-bulk-cross-field-and-cast.md`](./03-practical-examples/02-bulk-cross-field-and-cast.md) | all | Bulk row failures (`ExportJob`), cross-field rules (`Checkout`), untrusted payloads (`WebhookIngest`) |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Validation rules, anti-patterns, checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | The validation error contract, status decision tables, code catalogue |

## Learning objectives

By the end you can:

- Classify any incoming check as **syntactic**, **semantic**, or **business** and place it in the
  right layer (17.1, 17.16).
- Name and correctly report every field-rule class: structure, required, type, range, format,
  cross-field, conditional, nested, collection (17.2–17.10).
- Choose **aggregated vs fail-fast** per stage and design bulk validation with per-item outcomes
  (17.11, 17.12).
- Design a **field-level error representation** with stable codes and no duplicates (17.13–17.15).
- Validate at the **trust boundary**, treat the client as untrusted, handle malformed and oversized
  payloads, and keep responses localizable without leaking schema (17.17–17.21).
- Ship **one consistent validation contract** across every endpoint and version it safely (17.22).

## Key takeaways

1. **Validation lives at the trust boundary and runs before anything stateful.** Parse first,
   validate shape next, semantics after, domain last.
2. **Aggregate everything the user can fix in one round trip.** Fail-fast belongs to *parse*
   errors (stop on unparseable JSON), not to field errors.
3. **Report pointers, not prose.** `pointer` + `code` is the contract; `message` is a courtesy
   that may be localized or changed.
4. **One rule, one code.** Never encode the field name in the code (`EMAIL_FORMAT_INVALID` vs
   `ADDRESS_FORMAT_INVALID`), never use the message as the code, never duplicate a rule under two
   names.
5. **Server-side validation is the security boundary.** Client-side checks exist to save round
   trips, nothing more (17.18).
6. **Consistency beats cleverness.** The same envelope, the same status, the same code vocabulary
   on every endpoint — that is what lets one SDK serve your whole API.

## Exercises

1. Take your most-used POST endpoint and list every validation rule with a stable code; find the
   rules that currently return a bare `400`.
2. Find a rule implemented in two places (frontend + backend, or DTO + service) and decide which
   layer owns it.
3. Trigger your API with an oversized body, a wrong `Content-Type`, and malformed JSON; write down
   the three different responses you get today, then make them consistent.
4. Pick ten error messages your API returns; check how many could be a shared code with `params`
   for localization.

## Related

- [Chapter 18 — Domain and Business Logic Errors](../18-domain-and-business-logic-errors/README.md)
- [Chapter 20 — Standardized API Error Responses](../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter 5 — Error Categories in Detail (validation)](../../part-02-error-taxonomy/05-error-categories-in-detail/README.md)
- [Part VII — Part overview](../README.md)
