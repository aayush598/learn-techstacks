# Part VII — Input Validation and Business Errors

> **Chapters 17–18.** Parts I–VI gave you semantics, a taxonomy, an error model, and the
> architecture to move errors around. This part covers the two error families you meet on
> **every single request**: the input was unacceptable (**validation**), or the input was fine but
> the world says no (**domain/business**). Both are *expected outcomes*, not bugs — and mishandling
> them is what turns a normal product into a support-ticket machine.

## Learning objectives

By the end of Part VII you will be able to:

1. Separate **syntactic**, **semantic**, and **business** checks, and place each at the layer that
   owns it — so a coupon rule never leaks into a JSON parser and a `TypeError` never reaches a user.
2. Produce a **complete, aggregated, field-level validation response** (HTTP `422` with a stable
   per-field error schema) instead of a vague `400 Bad Request`.
3. Give every validation rule a **stable machine code**, avoid duplicate codes, and keep responses
   **localizable and contract-stable** without leaking your schema.
4. Model **domain errors** — invariants, state transitions, ownership, duplicates, quota,
   entitlements, preconditions — as first-class values with codes, categories, and HTTP mappings.
5. Choose deliberately between an **expected outcome** (return/result) and an **exception** for
   domain failures, and keep the domain free of framework and transport dependencies.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 17 | [Input Validation Error Handling](./17-input-validation-error-handling/README.md) | Rule classes (required, type, range, format, cross-field, conditional, nested, list), aggregation vs fail-fast, field-level representation, stable codes, trust boundaries, malformed/oversized input, localization, contract consistency |
| 18 | [Domain and Business Logic Errors](./18-domain-and-business-logic-errors/README.md) | Invariants, business rules, state transitions and lifecycle, ownership, duplicates, quota/balance, entitlements, preconditions, expected outcomes vs exceptions, domain services, aggregates, DDD, backward-compatible contracts |

## The one idea that unifies this part

> **Validation answers "is this request acceptable *as input*?" The domain answers "is this action
> acceptable *right now, for this tenant, in this state*?" The failure shapes look similar; the
> owners, codes, and status codes do not.**

```text
 bytes ──▶ parse ──▶ shape/type ──▶ semantics ──▶ DOMAIN ──▶ infrastructure
          │          │              │              │            │
          ▼          ▼              ▼              ▼            ▼
        400/413    422 field      422 field      409/403/404  5xx
        415        errors         errors         402/422/429  (Ch. 22+)
        malformed  required,      cross-field,   state,       DB/queue/
        oversized  type, range,   conditional,   ownership,   provider
        JSON       format         uniqueness*    entitlement  failures
                     └──── Chapter 17 ─────┘    └── Chapter 18 ──┘
```

`*` Uniqueness is the hinge: *well-formed and unique-looking input* colliding with existing data is
a **domain conflict** (Ch. 18), while "this field must be unique" checked syntactically before the
write is still validation territory. Chapter 17 draws the line; Chapter 18 owns the collision.

Two rules follow from the diagram:

1. **Never skip a stage.** Domain checks run only on input that already passed validation, so the
   domain can assume well-typed, present, in-range data and keep its code readable.
2. **Never blur a stage.** A `422` means "we understood you and your request is invalid"; a `409`
   means "your request is valid but conflicts with current state". Clients branch on that
   difference — so must you.

## How to study this part

- Read Chapter 17 top to bottom, then write the validation contract for **one** real endpoint in
  your codebase: every rule, its stable code, and its `pointer`.
- Keep the recurring cast in mind: `Checkout` (cross-field and business rules on a subscription),
  `ExportJob` (bulk row validation with partial success), `WebhookIngest` (payload validation at an
  untrusted boundary — signature first), `AgentRun` (tool-argument validation).
- For Chapter 18, list the five things your domain most often says "no" to (state, owner, duplicate,
  quota, entitlement) — each one deserves a named error, a code, and an HTTP mapping.

## Key takeaways

1. **Validation is cheap, local, and complete; domain checks are meaningful, stateful, and
   specific.** Put required/type/range/format at the edge; put invariants and preconditions where
   the state lives.
2. **Aggregate field errors, fail fast on the first *fatal* parse error.** A user fixing three
   fields should learn about all three at once (17.12).
3. **One rule, one stable code; messages are presentation.** Codes survive refactors and
   localization; sentences do not (17.14, 17.20).
4. **The client is a convenience, not a control.** Client-side validation is a UX nicety;
   the server-side check at the trust boundary is the security boundary (17.18).
5. **A domain error is data, not an accident.** Model it with the same care as your entities:
   named, coded, categorized, and versioned — never a bare `throw new Error("invalid")` (18.1).
6. **Expected outcomes are not exceptions.** "Already subscribed", "insufficient seats", and
   "cannot cancel an active trial" are results your API documents, not crashes you recover from
   (18.12).

## Related

- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- [Part VIII — HTTP and API Error Handling](../part-08-http-and-api/README.md)
- [Part XVI — Authentication, Billing, and Subscription Workflows](../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
- [Glossary](../GLOSSARY.md)
