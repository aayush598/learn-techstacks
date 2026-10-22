# Part III — Error Models and Representation

> **Chapters 6–8.** Taxonomy (Part II) answers *what kinds of failures exist*. This part answers
> a different question: **how does a single error travel through your code as data?** An error
> model, a set of error types, and a code registry are the three artifacts that make every other
> decision — retry, translation, disclosure, alerting — possible.

## Why this part matters

The taxonomy in Part II lives in design documents. The *error model* lives in every `throw`, every
`return err`, and every JSON response. If those representations are inconsistent, the taxonomy
cannot be enforced: a handler physically cannot route on a field that does not exist. This part
turns vocabulary into a **portable, inspectable data structure** that survives serialization,
logging, and process boundaries.

## Learning objectives

By the end of Part III you will be able to:

1. Define a **single internal error shape** every subsystem populates, with typed fields for
   code, message, category, severity, cause, context, correlation, and validation details.
2. Decide when to use **native exceptions, custom classes, union types, or `Result` types**, and
   when to mix them without creating two dialects in one codebase.
3. Design a **stable, machine-readable code** set and a **registry** that maps each code to HTTP
   status, retry policy, user message, and client action — and keeps working as the product grows.

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 6 | [Designing the Application's Error Model](./06-designing-the-applications-error-model/README.md) | The canonical internal error object: fields, cause, context, invariants, versioning |
| 7 | [Error Classes, Types, and Structured Results](./07-error-classes-types-and-structured-results/README.md) | Custom classes vs unions vs `Result`; type-safe control flow; exhaustiveness |
| 8 | [Error Codes and Error Registries](./08-error-codes-and-error-registries/README.md) | Stable codes, naming, uniqueness, registries, mapping, deprecation |

## How to study this part

- Read Chapter 6 first and **write the error object down as an interface**. Every later chapter
  assumes it exists.
- For Chapter 7, pick **one** failure-handling convention for your codebase and note the
  exception where you deliberately deviate (e.g. `Result` in domain, exceptions at the edge).
- For Chapter 8, start a registry file (even 10 rows) and fill in the HTTP and retry columns.
  An undocumented code is a bug waiting to happen.

## Running example

All three chapters use the recurring cast. The `Checkout` flow produces `PAYMENT_*` codes, the
`ExportJob` worker produces `EXPORT_*` codes, `WebhookIngest` produces `WEBHOOK_*` codes, and
`AgentRun` produces `AGENT_*` codes — each owned by a different domain but all conforming to the
same error shape and registry rules.

## Key takeaways

- **An error is data before it is an exception.** Design the data first; the mechanism is a
  detail.
- **Codes are the contract; messages are not.** Clients and handlers branch on stable codes, never
  on prose.
- **A registry is the single source of truth.** If a code exists in code but not in the registry,
  the system is not production-grade.
- **Consistency beats cleverness.** One model, applied everywhere, is worth more than a bespoke
  hierarchy per module.

## Related

- [Part II — Error Taxonomy and Classification](../part-02-error-taxonomy/README.md)
- [Part IV — Error-Handling Architecture and System Boundaries](../part-04-architecture/README.md)
- [Glossary: error model, error code, error registry](../GLOSSARY.md)
