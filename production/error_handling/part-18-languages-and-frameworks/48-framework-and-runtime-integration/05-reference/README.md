# Chapter 48 — Reference

> Part XVIII · Chapter 48 · Cheat sheets and mappings.

## Framework integration cheat sheet

| Framework | Error hook | Order | Notes |
| --------- | ---------- | ----- | ----- |
| **Express** | 4-arg middleware `(err, req, res, next)` | Last | Check `res.headersSent`; exactly 4 args required |
| **Fastify** | `setErrorHandler(err, req, reply)` | Per context (inheritance) | Handle `err.validation` separately; can override per plugin |
| **NestJS** | `ExceptionFilter` via `@Catch()` | Method → Controller → Global | Filters catch exceptions from pipes/guards/interceptors/controllers |
| **Spring Boot** | `@ControllerAdvice` + `@ExceptionHandler` | Resolver chain | Use `ProblemDetail`; `@ExceptionHandler` by exception type |
| **Django** | Middleware `process_exception` / custom middleware | Middleware order (reverse on exception) | Use custom middleware for structured errors; `handler500` for defaults |
| **ASP.NET Core** | `UseExceptionHandler` / `IExceptionHandler` | Middleware pipeline | Prefer `IExceptionHandler` in modern .NET |

## DI failure guidance

| Failure | Phase | Action | Recoverable? |
| ------- | ----- | ------ | ------------ |
| Constructor throws (critical) | Bootstrap | Fail-fast, exit(1) | No |
| Missing required provider | Bootstrap/Resolve | Fail-fast | No |
| Circular dependency | Bootstrap | Fail-fast | No |
| Optional provider fails | Bootstrap/Factory | Use fallback/disables feature | Yes (if optional) |
| Runtime scope resolution fails | Request | Translate to `INTERNAL_ERROR` or `DEPENDENCY_UNAVAILABLE` | Depends |

## ORM/validation mapping table

### ORM mappings

| Error | Prisma | SQLAlchemy | App code | Retryable | HTTP |
| ----- | ------ | ---------- | -------- | --------- | ---- |
| Unique constraint | `P2002` | `IntegrityError` (unique) | `DUPLICATE_RESOURCE` | false | 409 |
| FK violation | `P2003` | `IntegrityError` (FK) | `REFERENCE_NOT_FOUND` | false | 422 |
| Not null | `P2011` | `IntegrityError` (not null) | `VALIDATION_ERROR` | false | 422 |
| Check | `P2004` | `IntegrityError` (check) | `BUSINESS_RULE_VIOLATION` | false | 422 |
| Deadlock | `P2034`/driver | `OperationalError` `40P01` | `CONCURRENCY_CONFLICT` | true | 409 |
| Serialization failure | driver | `OperationalError` `40001` | `CONCURRENCY_CONFLICT` | true | 409 |
| Connection/pool | init error | `OperationalError` | `DEPENDENCY_UNAVAILABLE` | true | 503 |
| Query timeout | driver timeout | `OperationalError` | `DEPENDENCY_TIMEOUT` | true | 504 |

### Validation mappings

| Library | Translate to | Field details |
| ------- | ------------ | ------------- |
| **zod** | `VALIDATION_ERROR` | `issues[]` → `fields[]` with `path`, `code`, `message` |
| **joi** | `VALIDATION_ERROR` | `details[]` → normalize to `fields[]` |
| **class-validator** | `VALIDATION_ERROR` | Flatten `ValidationError[]` with dot paths |
| **Pydantic** | `VALIDATION_ERROR` | `errors()` `loc`/`msg`/`type` → `fields[]` |
| **Bean Validation** | `VALIDATION_ERROR` | `ConstraintViolation` property paths → `fields[]` |

### Queue framework semantics

| Framework | Retry | DLQ | Notes |
| --------- | ----- | --- | ----- |
| **BullMQ** | `attempts` + `backoff` | Failed jobs / manual move | Classify exceptions; use `failedReason` |
| **Sidekiq** | `retry` (default 25) | Dead set | Exponential backoff built-in |
| **Celery** | `max_retries` + `autoretry_for` | DLQ via exchange/routing or custom | Use `acks_late` + idempotency |
| **SQS** | Redelivery up to `maxReceiveCount` | DLQ | At-least-once; idempotency mandatory |

## Adapter checklist

- [ ] Core has zero framework imports
- [ ] Single `policyFor()` used everywhere
- [ ] `normalize()` is total (unknown → `INTERNAL_ERROR`)
- [ ] ORM errors translated in repository
- [ ] Validation normalized at boundary
- [ ] RFC 9457 response with `code` field
- [ ] No stack traces in client responses
- [ ] Startup failures fail-fast
- [ ] Shutdown is time-bound
- [ ] Headers-sent guarded (Express)

## Glossary (chapter-specific)

| Term | Meaning |
| ---- | ------- |
| Adapter | Thin layer that translates between framework types and the framework-free core |
| Error filter | Framework mechanism (NestJS) that catches exceptions and produces responses |
| Error middleware | Framework mechanism (Express) with 4 args that handles errors |
| Error handler | Framework mechanism (Fastify) registered via `setErrorHandler` |
| Bootstrap boundary | Separate lifecycle where config/DI/init failures are handled (fail-fast) |
| Translation boundary | Where vendor/framework errors become `AppError` |
| Policy boundary | Where `AppError.code` becomes status/retry/alert (pure data lookup) |

## Signposts

- Handler hierarchies → [Framework Hierarchies and Handlers](../01-concepts/01-framework-hierarchies-and-handlers.md)
- DI/ORM/validation → [Dependency Injection, ORM, and Validation Mapping](../01-concepts/02-dependency-injection-orm-and-validation-mapping.md)
- Policy and adapters → [Framework-Independent Policy and Adapters](../01-concepts/03-framework-independent-policy-and-adapters.md)
- Conflicts → [Custom vs Built-in Handler Conflicts](../02-deep-dive/01-custom-vs-built-in-handler-conflicts.md)
- Worked examples → [Express, Fastify, and NestJS Adapters](../03-practical-examples/01-express-fastify-and-nestjs-adapters.md)
- Chapter 47 architecture → [Type-Safe Handling and the Common Architecture](../../47-language-level-error-semantics/02-deep-dive/02-type-safe-handling-and-common-architecture.md)

## Related

- [Chapter 48 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 48 Overview](../README.md)
- [Part XVIII Index](../../README.md)
- [Glossary](../../../GLOSSARY.md)
