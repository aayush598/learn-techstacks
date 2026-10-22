# Part VI — Error Boundaries and Translation

> **Chapters 15–16.** Part IV told you *where* errors travel through your layers; Part V told you
> *how* exceptions propagate along the call stack. This part answers the two questions that make
> that travel safe and coherent: **where do you stop an error (a boundary), and what do you turn
> it into (translation)?** Every reliable system is a chain of boundaries connected by translations.

## Learning objectives

By the end of Part VI you will be able to:

1. Define an **error boundary** and place one at each level of your system — function, module,
   domain, request, transaction, job, process, service, third-party, and UI.
2. Choose **correct granularity**, decide **who owns** each boundary, and prevent information
   **leakage** across it.
3. Handle **nested boundaries** so an inner catch neither swallows a failure the outer layer must
   see nor steals a decision that belongs elsewhere.
4. **Translate and normalize** native, database, framework, OS, external, and domain errors into a
   consistent internal model without losing the root cause or retry metadata.
5. Build **translation tables and policies** that map vendor codes (`SQLSTATE 23505`) to stable
   application codes and HTTP statuses (`409`).

## Chapters

| # | Chapter | Focus |
| - | ------- | ----- |
| 15 | [Error Boundaries](./15-error-boundaries/README.md) | What a boundary is, every level it exists at, ownership, granularity, nesting, fallback, isolation vs propagation |
| 16 | [Error Translation and Normalization](./16-error-translation-and-normalization/README.md) | Why and how to translate; every direction (DB→domain, external→internal, domain→transport); preserving cause and retry metadata; vendor codes; tables and versioning |

## The one idea that unifies this part

> **A boundary is where an error's representation and its owner change. Translation is the change.**

When a Postgres driver raises `UniqueViolation` (`SQLSTATE 23505`) inside a repository, two things
must happen at the same architectural line:

1. **Contain or propagate** the error deliberately — this is the **boundary** decision (Ch. 15).
2. **Convert** the driver-specific exception into a stable domain error, then later into an HTTP
   response — this is the **translation** decision (Ch. 16).

```text
 Reality                Boundary                 Internal model          Boundary            External
 ───────                ────────                 ──────────────          ────────            ────────
 psycopg2               repository               DomainError             HTTP handler        RFC 9457
 UniqueViolation  ───▶  translates          ───▶ EMAIL_ALREADY_USED ───▶ maps to  ───▶ body:
 SQLSTATE 23505         + preserves cause        (category: conflict)    status 409         application/problem+json
```

Skip the boundary and the leak is direct: SQL text in an API response. Skip the translation and
the domain is coupled to Postgres, so switching databases (or testing without one) becomes a
rewrite.

## How to study this part

- Read Chapter 15 first and draw the boundaries in **your own** request path before reading the
  reference file.
- Keep the recurring cast in mind: `Acme SaaS` (request/transaction boundaries), `ExportJob`
  (job/process boundaries), `WebhookIngest` (third-party boundary), `AgentRun` (provider boundary).
- For Chapter 16, list every distinct error format that enters your system; each is a translation
  you owe a policy.

## Key takeaways

1. **Boundaries are architectural decisions, not `try/catch` placement.** You place one when the
   fallback behavior is meaningfully different from propagating.
2. **Translate at the boundary, not in the domain.** The domain should never see a driver code, an
   HTTP status, or a vendor string.
3. **Preserve the cause through every translation.** Chained errors (`Error.cause`, `%w`,
   `raise ... from`) are how you keep debuggability after normalizing.
4. **Preserve retry metadata.** If you translate a transient error into a generic one, you have
   silently disabled retries — a common and expensive bug.
5. **One error, one canonical internal shape.** Normalization is what lets every downstream
   consumer (retry, logging, API) make a decision without `switch`ing on vendor formats.

## Related

- [Part IV — Error-Handling Architecture and System Boundaries](../part-04-architecture/README.md)
- [Part V — Exception Handling Mechanics](../part-05-exception-mechanics/README.md)
- [Part VII — Input Validation and Business Errors](../part-07-validation-and-business-errors/README.md)
- [Glossary](../GLOSSARY.md)
