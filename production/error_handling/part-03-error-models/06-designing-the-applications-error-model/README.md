# Chapter 6 — Designing the Application's Error Model

> Part III · _Estimated reading time: 70–90 min_
> **Prerequisite:** [Chapter 4 — Designing a Comprehensive Error Taxonomy](../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)

## One-sentence summary

The **application error model** is the one internal data structure every error in your system is
represented as — a small, fixed set of typed fields that carries an error from where it is created
to where it is decided on, without leaking, losing its cause, or changing shape.

## Why this chapter matters

A taxonomy without a representation cannot be enforced. If one module throws a bare `Error`, another
returns `{ error: true, msg }`, and a third returns a vendor blob, then handlers cannot route
reliably, logs are inconsistent, and public responses leak whatever happened to be in the string.
A single model makes the taxonomy *executable*: routing, retry, disclosure, and alerting become
straightforward lookups on typed fields. It is also the prerequisite for Chapters 7 (types) and 8
(codes), and for every boundary decision in Part IV.

## Chapter map

The chapter has 20 sections. They are grouped into eight files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-what-an-error-object-represents.md`](./01-concepts/01-what-an-error-object-represents.md) | 6.1–6.2 | What the object is for; the standard internal structure |
| [`01-concepts/02-core-identity-fields.md`](./01-concepts/02-core-identity-fields.md) | 6.3–6.7 | name & code, message, machine-readable id, category, severity/recoverability |
| [`01-concepts/03-cause-context-and-correlation.md`](./01-concepts/03-cause-context-and-correlation.md) | 6.8–6.12 | original cause, safe metadata, stack traces, time/operation context, correlation IDs |
| [`01-concepts/04-validation-details-and-chaining.md`](./01-concepts/04-validation-details-and-chaining.md) | 6.13–6.14 | field-level details; causal chains |
| [`01-concepts/05-immutability-serialization-and-safety.md`](./01-concepts/05-immutability-serialization-and-safety.md) | 6.15–6.18 | immutable vs mutable, serializable vs not, circular refs, sensitive data |
| [`02-deep-dive/01-model-invariants.md`](./02-deep-dive/01-model-invariants.md) | 6.19 | The invariants every instance must hold |
| [`02-deep-dive/02-versioning-the-internal-contract.md`](./02-deep-dive/02-versioning-the-internal-contract.md) | 6.20 | Evolving the shape without breaking consumers |
| [`03-practical-examples/01-error-object-spec.md`](./03-practical-examples/01-error-object-spec.md) | 6.1–6.20 | A complete TypeScript + JSON specification you can copy |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Field cheat sheet, decision tables, glossary |

## Learning objectives

By the end you can:

- State what an error object *represents* and what it must *not* contain.
- Write an `AppError` interface with every load-bearing field and justify each one.
- Preserve an original `cause` and a causal chain across wrapping and translation.
- Enforce model invariants (non-empty code, safe context, no secrets) mechanically.
- Version the internal contract so consumers keep working as fields are added.

## Key takeaways

1. **The model is data, not a mechanism.** It is independent of `throw`, `Result`, or an HTTP
   response.
2. **Codes, not messages, are the contract.** Everything routable and stable is a code.
3. **Cause and context are mandatory** for debugging; correlation is mandatory for tracing.
4. **Invariants are enforced at construction**, not by convention.
5. **Serialize deliberately.** Not every field should cross a process or trust boundary.

## Exercises

1. Write your current error shape as an interface. Mark which fields you have and which you lack.
2. Take a real stack trace and reconstruct the causal chain as nested `cause` links.
3. List three fields in your current errors that could leak PII or secrets to a client.

## Related

- [Chapter 7 — Error Classes, Types, and Structured Results](../07-error-classes-types-and-structured-results/README.md)
- [Chapter 8 — Error Codes and Error Registries](../08-error-codes-and-error-registries/README.md)
- [Part II — Error Taxonomy and Classification](../../part-02-error-taxonomy/README.md)
