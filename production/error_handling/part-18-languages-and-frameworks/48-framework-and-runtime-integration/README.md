# Chapter 48 — Framework and Runtime Integration

> Part XVIII · Chapter 48 · _Estimated reading time: 60–80 min_
> **Prerequisite:** [Chapter 47 — Language-Level Error Semantics](../47-language-level-error-semantics/README.md)

## One-sentence summary

**Frameworks own the request lifecycle, object graph, and worker loop** — you either wire your
error policy into their hooks deliberately, or they adopt their own defaults and erode your
taxonomy at the boundary.

## Why this chapter matters

Acme SaaS runs Express in Node, Fastify in edge routes, NestJS for billing, Spring Boot for
invoicing, Django for internal tools, and Celery/Sidekiq/BullMQ for jobs. Each comes with its
own error handler, its own ORM exception mapping, its own validation semantics, and its own
retry/shutdown behavior. This chapter teaches you to keep a **framework-independent policy**
in a core module and use thin, replaceable **adapters** to translate into each framework's
idiom without letting the framework leak into your domain.

## Chapter map

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-framework-hierarchies-and-handlers.md`](./01-concepts/01-framework-hierarchies-and-handlers.md) | 48.1–48.4, 48.9–48.12 | Framework hierarchies, built-in handlers, HTTP middleware, request lifecycle, startup/shutdown, defaults to preserve/customize |
| [`01-concepts/02-dependency-injection-orm-and-validation-mapping.md`](./01-concepts/02-dependency-injection-orm-and-validation-mapping.md) | 48.5–48.8 | DI failure handling, ORM exception mapping (SQLAlchemy/Prisma), validation library mapping (zod/joi/class-validator), queue framework semantics |
| [`01-concepts/03-framework-independent-policy-and-adapters.md`](./01-concepts/03-framework-independent-policy-and-adapters.md) | 48.13–48.14 | Keep policy framework-free, build reusable adapters, the dependency direction rule |
| [`02-deep-dive/01-custom-vs-built-in-handler-conflicts.md`](./02-deep-dive/01-custom-vs-built-in-handler-conflicts.md) | 48.1–48.4, 48.9–48.12 | Ordering conflicts, middleware swallowing, after-headers-sent cases, startup/shutdown failure, when to override |
| [`03-practical-examples/01-express-fastify-and-nestjs-adapters.md`](./03-practical-examples/01-express-fastify-and-nestjs-adapters.md) | 48.1–48.8 | Concrete adapters for Express, Fastify, and NestJS with DI, validation, and ORM mapping |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules for framework integration, DI/ORM/validation gotchas, adapter discipline |
| [`05-reference/README.md`](./05-reference/README.md) | all | Framework integration cheat sheet, DI failure guidance, ORM/validation mapping table |

## Learning objectives

By the end you can:

- Map a framework's **handler hierarchy** and **request lifecycle** to the boundaries in Chapters 15–16.
- Choose which framework defaults to **preserve** (Fastify schema errors, NestJS pipes) and which to **customize** (global error shape).
- Translate **DI construction failures**, **ORM exceptions** (Prisma/SQLAlchemy), and **validation issues** (zod/joi) to your stable error codes.
- Handle **queue framework semantics** (BullMQ/Sidekiq/Celery) at the worker boundary with retries and DLQs.
- Wire **startup/shutdown** failures deliberately without masking them with the HTTP error handler.
- Build a **framework-independent core** + thin **adapters** so you can swap frameworks without rewriting policy.

## Key takeaways

1. **The boundary belongs to the framework.** Express's 4-arg handler, Fastify's `setErrorHandler`, NestJS `ExceptionFilter`, Spring `@ControllerAdvice`, Django middleware — put translation and policy there, never in the domain.
2. **Translate in adapters, not in filters.** Filters should call pure `translate()` and `policyFor()` functions; they should not import business services to guess a status code.
3. **DI can fail before your code runs.** Constructor injection failures are framework errors; handle them at bootstrap or with framework-specific mechanisms.
4. **ORMs throw vendor exceptions.** Translate `UniqueConstraintError`, `ForeignKeyConstraintError`, `DeadlockDetected` to `DUPLICATE_RESOURCE`, `REFERENCE_NOT_FOUND`, `CONCURRENCY_CONFLICT` at the repository boundary.
5. **One core, many adapters.** Keep taxonomy, registry, and policy in a framework-free module. Adapters are the only place that imports framework types.

## Exercises

1. List every framework error hook in one service (middleware, filter, handler). Classify each as *translate*, *log*, or *pass-through*.
2. Map three ORM errors from your stack to app codes, with retryability, using the mapping table in §05-reference.
3. Wire a custom error handler for Express or Fastify that calls a pure `policyFor(code)` and returns RFC 9457.
4. Extract the policy from a framework-coupled handler into a pure function; prove no framework imports remain.

## Related

- [Chapter 47 — Language-Level Error Semantics](../47-language-level-error-semantics/README.md)
- [Chapter 15 — Error Boundaries](../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Chapter 16 — Error Translation and Normalization](../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Glossary](../../GLOSSARY.md)
