# Chapter 48 — Do's and Don'ts

> Part XVIII · Chapter 48 · All sections (48.1–48.14)

A condensed rule set for framework and runtime integration. Use it as a review checklist.

## Framework hierarchies and handlers

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put translation and policy in exactly one error handler per transport | Scatter `res.status()` across controllers |
| Register Express error middleware last (4 args) | Register it before routes |
| Use Fastify's `setErrorHandler` to normalize schema and thrown errors | Let framework defaults leak stack traces |
| Use NestJS filters at the appropriate scope (global for cross-cutting) | Create filters that re-throw in loops |
| Respect middleware/filter precedence | Change order without tests |

## Startup, shutdown, and runtime

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fail fast on critical bootstrap failures before binding the HTTP port | Route startup errors to the HTTP error handler |
| Drain in-flight requests/jobs on `SIGTERM` with a timeout | `process.exit(0)` immediately |
| Make shutdown handlers idempotent and exception-safe | Throw during shutdown and prevent clean exit |
| Treat readiness as separate from liveness | Crash the process for a single optional dependency |
| Check `res.headersSent` in Express error handlers | Call `res.json()` after headers are sent |

## DI, ORM, and validation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate DI constructor failures at bootstrap | Let container errors become 500s with framework traces |
| Translate ORM errors in the repository to stable `AppError` codes | Let Prisma/SQLAlchemy exceptions bubble to controllers |
| Map deadlocks/serialization failures to `CONCURRENCY_CONFLICT` with `retryable: true` | Treat all DB errors as non-retryable |
| Normalize validation to a stable field-error shape | Return raw zod/Joi/Pydantic schemas to clients |
| Never leak constraint names or SQL fragments | Expose `meta.target` or query text in API responses |

## Queue frameworks

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify job errors by retryability from the registry | Retry `VALIDATION_ERROR`, `BUSINESS_RULE_VIOLATION`, or `PAYMENT_CARD_DECLINED` |
| Make job handlers idempotent (at-least-once delivery) | Assume exactly-once |
| Move exhausted jobs to DLQ with context (jobId, code, correlationId) | Retry forever |
| Track redelivery/attempt count | Ignore `attemptsMade` / receive count |
| Stop pulling on shutdown; let in-flight jobs finish or time out | Abort jobs mid-write without cleanup |

## Adapters and policy discipline

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep policy/registry in a framework-free core | Import Express/NestJS into `core/` |
| Use thin adapters for translation + serialization only | Put business decisions in filters/middleware |
| Use RFC 9457 for the wire format with a stable `code` field | Invent a new envelope per service |
| Make the registry lookup total (unknown → `INTERNAL_ERROR`) | Let unknown codes throw in the classifier |
| Enforce dependency direction with lint/dependency-cruiser | Allow circular deps between core and framework |

## Anti-patterns

1. **The Framework Leak** — importing `HttpException` into the domain.
2. **The Startup 500** — DB init failure routed through the HTTP error handler.
3. **The Swallowed Middleware Error** — caught exception with no `next(err)` and no response.
4. **The Infinite Retry** — throwing a non-retryable business error from a queue job.
5. **The Headers-Sent Crash** — writing an error response after streaming started.
6. **The Leaky Constraint** — returning `P2002` meta directly to the client.

## Chapter checklist

- [ ] Is there exactly one error handler per transport?
- [ ] Are startup failures separate and fatal?
- [ ] Are ORM/validation errors translated at the correct boundaries?
- [ ] Is queue retryability driven by the registry?
- [ ] Is the core framework-free and enforced by CI?
- [ ] Is the wire format consistent (RFC 9457 + stable codes)?

## Related

- [Chapter 48 Reference](../05-reference/README.md)
- [Chapter 48 Overview](../README.md)
- [Chapter 47 — Language-Level Error Semantics](../../47-language-level-error-semantics/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
