# Dependency Injection, ORM, and Validation Mapping

> Part XVIII · Chapter 48 · Sections 48.5–48.8 · _Estimated reading time: 22 min_
> **Prerequisite:** [Framework Hierarchies and Handlers](./01-framework-hierarchies-and-handlers.md), [Chapter 24 — Repository and Data Access Error Handling](../../../part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)

## In one sentence

**DI, ORMs, and validation libraries are failure sources too** — constructor injection can fail
at bootstrap, ORMs throw vendor-specific exceptions, and validation libraries produce issue
objects — all of which must be translated to your stable error codes at the correct boundary.

## Why this matters in production

A misconfigured DI container can crash the process in a way that looks like a request error;
a Prisma `UniqueConstraintError` can bubble up as a 500 if not translated to `409`; zod's
`ZodError` can leak schema details to the client; a BullMQ job throwing an unknown error can be
retried infinitely. Each of these needs a deliberate translation rule.

## 48.5 — DI failure handling

Dependency Injection failures happen **before** a request reaches your handler. Treat them
differently from runtime request failures.

| Failure | When | Where to handle | Action |
| ------- | ---- | --------------- | ------ |
| **Constructor throws** | Module registration / container build | Bootstrap / `main` | Fail-fast with a clear message; exit non-zero |
| **Circular dependency** | Container resolution | Bootstrap | Fail-fast; fix the graph |
| **Missing provider** | Resolution at runtime or build time | Bootstrap (preferred) or provider factory | Fail-fast if required; use a factory with validation if optional |
| **Async provider rejects** | On application initialization | Bootstrap (NestJS `OnApplicationBootstrap`) | Fail-fast or retry with backoff if external |
| **Scope mismatch** | Request-scoped used in singleton | Bootstrap / lint | Fail-fast; catch in tests/CI |

**NestJS:** Use `onModuleInit`/`onApplicationBootstrap` and let exceptions propagate to crash
the app if critical dependencies fail. For optional dependencies, inject them via factories
with `try/catch` and return a disabled implementation.

**Spring:** Bean creation exceptions during context refresh are fatal by default. Use
`@ConditionalOnProperty` for optional beans and `ApplicationListener` for post-init checks.

## 48.6 — ORM exception mapping

ORMs abstract SQL but leak their own exception hierarchies. Translate at the **repository**
boundary so the domain never sees Prisma/SQLAlchemy types.

### Common mappings

| DB error | Prisma (TS) | SQLAlchemy (Python) | TypeORM/Sequelize | App code | Retryable | HTTP |
| -------- | ----------- | ------------------- | ----------------- | -------- | --------- | ---- |
| **Unique constraint** | `PrismaClientKnownRequestError` code `P2002` | `IntegrityError` + `unique_violation` (pg) | `UniqueConstraintError` | `DUPLICATE_RESOURCE` | false | `409` |
| **Foreign key violation** | `P2003` | `IntegrityError` + `foreign_key_violation` | `ForeignKeyConstraintError` | `REFERENCE_NOT_FOUND` | false | `422` |
| **Not null violation** | `P2011` | `IntegrityError` + `not_null_violation` | `NotNullConstraintError` | `VALIDATION_ERROR` | false | `422` |
| **Check constraint** | `P2004` | `IntegrityError` + `check_violation` | `CheckConstraintError` | `BUSINESS_RULE_VIOLATION` | false | `422` |
| **Deadlock detected** | `P2034` / driver error | `OperationalError` + `deadlock_detected` (`40P01`) | `TimeoutError`/driver | `CONCURRENCY_CONFLICT` | **true** | `409` |
| **Serialization failure** | Driver-specific | `OperationalError` + `serialization_failure` (`40001`) | Driver-specific | `CONCURRENCY_CONFLICT` | **true** | `409` |
| **Connection timeout/pool exhausted** | `PrismaClientInitializationError` / `PrismaClientRustPanicError` | `OperationalError` | `ConnectionError` | `DEPENDENCY_UNAVAILABLE` | **true** | `503` |
| **Query timeout** | Driver timeout | `OperationalError` | `TimeoutError` | `DEPENDENCY_TIMEOUT` | **true** | `504` |

**Rules:**

- Catch in the repository/DAO, translate to `AppError`, and attach the cause via the native
  chaining API.
- Never leak `meta.target`, constraint names, or SQL fragments to the client.
- For deadlocks/serialization failures, **retry at the service level with idempotency** (see
  Chapter 28), not inside the repository by default.
- Distinguish "record not found" (your `NOT_FOUND`) from "constraint violation" (a different
  failure mode).

## 48.7 — Validation library mapping

Validation errors are **expected, client-caused failures**. Normalize them to a consistent
field-error shape.

| Library | Error type | Structure | Mapping |
| ------- | ---------- | --------- | ------- |
| **zod (TS)** | `ZodError` | `error.issues[]` with `path`, `message`, `code` | `VALIDATION_ERROR` with `details.fields[] = { path, code, message }` |
| **joi (TS/Node)** | `ValidationError` | `error.details[]` with `context.key`, `message`, `type` | Same as above |
| **class-validator (NestJS)** | `ValidationError[]` | From `ValidationPipe`; nested constraints | Flatten to dot-notation paths |
| **Yup (TS)** | `ValidationError` | `inner[]` or `errors[]` with `path` | Normalize to the same shape |
| **Pydantic (Python)** | `ValidationError` | `errors()` returns list with `loc`, `msg`, `type` | `VALIDATION_ERROR` with field paths |
| **Marshmallow (Python)** | `ValidationError` | `messages` dict keyed by field | Normalize |
| **Bean Validation (Java)** | `ConstraintViolationException` | `ConstraintViolation<?>` set | `VALIDATION_ERROR` with property paths |
| **FluentValidation (.NET)** | `ValidationException` | `Errors` collection | `VALIDATION_ERROR` |

**Do / Don't:**

- **Do:** Return field-level errors under a stable `details` structure. Keep messages
  user-safe (don't echo raw regexes verbatim if they reveal implementation).
- **Don't:** Leak schema internals, library names, or stack traces. Don't treat validation as
  a 500.

## 48.8 — Queue framework semantics

Background jobs run outside the HTTP request lifecycle. Their errors need a **separate
contract** (retries, backoff, DLQ, terminal states).

| Framework | Retry config | Failure handling | Notes |
| --------- | ------------ | ----------------- | ----- |
| **BullMQ (Node)** | `attempts`, `backoff` (fixed/exponential/custom) | Throws → marked failed, retried per policy; after max attempts → failed/archived | Use `failedReason`, `stacktrace`; move to DLQ or keep failed jobs |
| **Sidekiq (Ruby)** | `retry: N` (default 25), exponential backoff | Exception → retry; after exhaustion → dead set (DLQ equivalent) | `Sidekiq::DeadSet`; configure `max_retries_exhausted` behavior |
| **Celery (Python)** | `task_acks_late`, `max_retries`, `autoretry_for`, `retry_backoff` | Exception → retry or fail; use `on_failure`/`on_retry` | `reject` vs `ack`; use `acks_late` for at-least-once carefully |
| **RabbitMQ (generic)** | Consumer retry via redelivery or DLX | `nack(requeue=true/false)`, DLX/DLQ | Track redelivery count to prevent infinite loops |
| **SQS (AWS)** | Visibility timeout, DLQ (max receive count) | Return failure → redeliver up to `maxReceiveCount` → DLQ | Idempotency is mandatory for at-least-once |

**Critical rules:**

- **Classify retryability:** Only retry `CONCURRENCY_CONFLICT`, `DEPENDENCY_TIMEOUT`,
  `DEPENDENCY_UNAVAILABLE`. Never retry `BUSINESS_RULE_VIOLATION`, `VALIDATION_ERROR`,
  `PAYMENT_CARD_DECLINED`.
- **Track redelivery/attempt count:** After N attempts, move to DLQ with full context
  (job name, id, last error code, correlation id). Do **not** retry forever.
- **Idempotency is mandatory:** Queue delivery is at-least-once. Every job handler must be
  idempotent (Chapter 28).
- **Poison messages:** A message that always throws must hit the DLQ, logged with alerts.
- **Shutdown:** On graceful shutdown, stop pulling new jobs, let in-flight jobs finish or
  time out, then exit.

## Key data / numbers

- Prisma P2002 = unique constraint violation; P2003 = foreign key; P2034 = transaction failed
- PostgreSQL SQLSTATE `40001` = serialization failure; `40P01` = deadlock detected; `23505` = unique violation
- BullMQ default `attempts: 1` (no retries) unless configured
- Sidekiq default `retry: 25`
- SQS DLQ `maxReceiveCount` is typically 3–10 depending on SLOs

## Real-world use case — ExportJob

Acme's `ExportJob` used BullMQ. A transient S3 timeout caused infinite retries because the
handler threw a generic `Error` with no classification — BullMQ retried it 25 times with
exponential backoff, hammering S3. The fix: classify the S3 timeout as
`DEPENDENCY_TIMEOUT` (retryable), cap to 5 attempts, move to DLQ after exhaustion with
`jobId`, `tenantId`, and `errorCode`, and alert on DLQ depth. The same classification made
the retry policy data-driven from the registry.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate ORM errors in the repository | Let Prisma/SQLAlchemy exceptions reach the controller |
| Normalize validation to a stable field-error shape | Return raw zod/Joi schemas to clients |
| Classify queue errors by retryability | Retry `BUSINESS_RULE_VIOLATION` or validation errors |
| Make job handlers idempotent | Assume exactly-once delivery |
| Fail fast on critical DI failures at bootstrap | Defer DI errors to the first request |

## Checklist

- [ ] Are all ORM exceptions translated at the repository boundary?
- [ ] Do validation errors return field-level details with stable codes?
- [ ] Is queue retryability driven by the error registry?
- [ ] Do job handlers have idempotency keys and DLQ routing?
- [ ] Are DI startup failures fatal and logged clearly?

## Related

- [Framework Hierarchies and Handlers](./01-framework-hierarchies-and-handlers.md)
- [Framework-Independent Policy and Adapters](./03-framework-independent-policy-and-adapters.md)
- [Express, Fastify, and NestJS Adapters](../03-practical-examples/01-express-fastify-and-nestjs-adapters.md)
- [Chapter 24 — Repository and Data Access Error Handling](../../../part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
