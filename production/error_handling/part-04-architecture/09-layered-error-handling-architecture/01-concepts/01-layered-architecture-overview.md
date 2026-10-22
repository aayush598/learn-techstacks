# The Layers of an Error-Handling Architecture

> Part IV · Chapter 9 · Sections 9.1–9.12 · _Estimated reading time: 22 min_
> **Prerequisite:** [Part III — Error Models](../../../part-03-error-models/README.md)

## In one sentence

An error-handling architecture is a stack of **layers**, each of which owns a class of failure and
a translation step, so that an error entering at any point travels a **predictable path** to a
defined outcome.

## Why this matters in production

When layers are merely import boundaries and not **error ownership** boundaries, three failures
appear:

- **Infrastructure leakage** — a Postgres driver error (`SQLSTATE 23505`) reaches an HTTP
  response, exposing schema and vendor detail.
- **Domain meaning loss** — a repository wrapper catches everything and rethrows `new Error("db
  failed")`, so the application can no longer tell a duplicate key from a connection reset.
- **Duplicate handling** — both the application service and the controller retry, producing
  double side effects.

Naming the layers and their error jobs is what makes these impossible by construction.

## The layer inventory

These are the layers this chapter uses. Not every system has all of them, but every system has
*equivalent* roles.

| # | Layer | Role | Owns errors from |
| - | ----- | ---- | ---------------- |
| 9.1 | **Presentation** | HTML/UI rendering, client-side state | render failures, form state |
| 9.2 | **Transport** | HTTP/gRPC/queue framing, parsing, auth | malformed requests, auth challenges |
| 9.3 | **Controller / handler** | maps request → use case; shapes response | request-shape errors, status mapping |
| 9.4 | **Application service** | orchestrates a use case, owns a transaction | orchestration, conflicts, partial failure |
| 9.5 | **Domain** | invariants and business rules | rule violations, invalid state transitions |
| 9.6 | **Repository** | persistence access, query execution | missing rows, constraint violations |
| 9.7 | **Infrastructure** | DB drivers, cache, object storage, config | connection, config, resource errors |
| 9.8 | **Integration** | third-party APIs (Stripe, LLM, tools) | vendor errors, timeouts, malformed payloads |
| 9.9 | **Background worker** | dequeues and runs jobs | job-level failure, retries, poison messages |
| 9.10 | **Scheduled task** | cron-style periodic work | run-level failure, overlap, drift |
| 9.11 | **Bootstrap** | startup wiring, DI, config load | startup/init failures |
| 9.12 | **Process boundary** | OS process/thread/container | crashes, OOM, uncaught exceptions |

## The layer diagram

```text
                        ┌──────────────────────────────────────────┐
   external             │             PRESENTATION  9.1            │
   user / browser ─────▶│  (React page, error boundary, form UI)   │
                        └────────────────────┬─────────────────────┘
                                             │ HTTP / gRPC / WS
                        ┌────────────────────▼─────────────────────┐
   network ────────────▶│               TRANSPORT  9.2             │
   (TLS, load bal.)     │  parse · authn · authz · rate-limit      │
                        └────────────────────┬─────────────────────┘
                                             │ parsed request
                        ┌────────────────────▼─────────────────────┐
                        │            CONTROLLER  9.3               │
                        │  request → use case · response shaping   │
                        └────────────────────┬─────────────────────┘
                                             │ command / query
                        ┌────────────────────▼─────────────────────┐
                        │        APPLICATION SERVICE  9.4         │
                        │  orchestration · transaction · policy    │
                        └───────┬─────────────────────────┬────────┘
                                │                         │
             ┌──────────────────▼───────┐    ┌────────────▼──────────────┐
             │        DOMAIN  9.5       │    │      INTEGRATION  9.8     │
             │  invariants · rules      │    │  Stripe · LLM · tools     │
             └──────────────────┬───────┘    └───────────────────────────┘
                                │
                        ┌───────▼──────────────────────────────────┐
                        │            REPOSITORY  9.6               │
                        │  persistence access · query execution    │
                        └────────────────────┬─────────────────────┘
                                             │
                        ┌────────────────────▼─────────────────────┐
                        │          INFRASTRUCTURE  9.7            │
                        │  DB driver · cache · S3 · config · pool  │
                        └────────────────────┬─────────────────────┘
                                             │
                        ┌────────────────────▼─────────────────────┐
                        │          PROCESS BOUNDARY  9.12         │
                        │  runtime, signals, OOM, crash handlers   │
                        └──────────────────────────────────────────┘

   ASYNC PATH (no HTTP request in scope):
   queue ──▶ BACKGROUND WORKER 9.9 ──▶ APPLICATION 9.4 ──▶ DOMAIN 9.5 ──▶ REPOSITORY 9.6
   scheduler ──▶ SCHEDULED TASK 9.10 ─▶ APPLICATION 9.4 ──▶ REPOSITORY 9.6
   boot ────▶ BOOTSTRAP 9.11 (wires all of the above; startup failures are terminal)
```

The arrow direction is **control flow (calls)**. Errors flow the **opposite way** (upward), being
translated at each boundary until a layer decides the outcome.

## Layer 9.1 — Presentation

Owns rendering and user-facing state. Its error job is to **render a defined UI for every error
category** (field errors, a toast, a page-level boundary). It never contains business rules; it
maps a received error contract to UI. Frontend boundaries are covered in Chapter 37.

## Layer 9.2 — Transport

Owns the wire. It **parses** the request and **authenticates/authorizes** before any application
code runs. Failures here (`400` malformed, `401`, `403`, `413`, `415`, `429`) never reach the
domain. Transport is the first place an error is converted to an external response.

## Layer 9.3 — Controller / handler

Owns **request → use case** mapping and **response shaping**. It converts a domain/application
outcome into a status code and body. Controllers must stay thin: no retries, no business
decisions. Their errors are mostly mapping errors.

## Layer 9.4 — Application service

Owns the **use case and the transaction**. This is the layer that decides **orchestration policy**:
retry a transient step, compensate a partial step, or fail the whole operation. It is the natural
owner of the handle-once decision for most business operations.

## Layer 9.5 — Domain

Owns **invariants and business rules**. A domain error means "this operation is not valid in the
domain" — `InsufficientFunds`, `SeatAlreadyTaken`, `InvalidStateTransition`. The domain must not
know about HTTP, SQL, or Stripe.

## Layer 9.6 — Repository

Owns **persistence access**. It translates driver errors into application-level persistence errors
(`DuplicateKey`, `RecordNotFound`) and distinguishes "no row" from "query failed". It must not
invent business meaning.

## Layer 9.7 — Infrastructure

Owns the **mechanisms**: DB drivers, connection pools, cache clients, object storage, config
loading. Its failures are operational: connection refused, pool exhausted, config missing.

## Layer 9.8 — Integration

Owns **third-party adapters**. It normalizes vendor errors into stable internal codes and hides
vendor-specific shapes. This is where a Stripe `card_declined` becomes `PAYMENT_CARD_DECLINED`.

## Layer 9.9 — Background worker

Owns **job lifecycle**. It wraps the application call, classifies job failure as retryable vs
terminal, applies backoff, and routes exhausted jobs to a dead-letter queue. See Chapter 32.

## Layer 9.10 — Scheduled task

Owns **periodic run semantics**: overlap prevention, idempotent re-runs, and failure of a run that
must not corrupt the next. See Chapter 32.

## Layer 9.11 — Bootstrap

Owns **startup**. Initialization failures (bad config, unreachable DB at boot) are **terminal**:
fail fast, do not serve traffic in a half-wired state. See Chapter 41.

## Layer 9.12 — Process boundary

Owns the **runtime**. `uncaughtException`, `unhandledRejection`, OOM, and signals are the last line
of defense. The only correct action is to log safely, flush, and terminate so an orchestrator
restarts a clean process. See Chapter 41.

## Real-world use case — Acme SaaS

Acme's original code caught `SequelizeUniqueConstraintError` in the **controller** and returned
`500`. The fix moved translation to the **repository** (→ `DuplicateKey`), made the **application
service** map it to the `EmailAlreadyRegistered` domain outcome, and let the **controller** render
`409` with code `EMAIL_ALREADY_REGISTERED`. Duplicate-email attempts dropped from paging alerts to
a clean, actionable `409`, and the domain stopped importing Sequelize types entirely.

## Key data / numbers

- HTTP status ranges owned by transport: `400`, `401`, `403`, `404` (routing), `405`, `413`, `415`,
  `429`.
- Postgres constraint violation: `SQLSTATE 23505` (unique), `23503` (foreign key), `23502` (not
  null).
- Postgres transaction conflict: `40001` (serialization_failure), `40P01` (deadlock_detected).
- Node.js process-level events: `uncaughtException`, `unhandledRejection`, `SIGTERM`, `SIGKILL`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Full ten-layer split | Clear ownership, testable | More files, more translation code | Medium/large SaaS, multi-team |
| Collapsed (controller+application) | Less boilerplate | Policy and mapping entangled | Early MVP |
| Domain-pure + thin adapters | Domain cannot leak | Discipline required | Any system with real invariants |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each layer one error job | Handle the same error in three layers |
| Translate at boundaries | Pass driver errors through the domain |
| Keep the domain free of infra types | Import `Sequelize`/`pg` in domain code |
| Treat workers/schedulers as layers | Assume async paths "don't need" layering |

## Common mistakes

- **Importing a driver type in a controller** to inspect a `code` field — translate in the
  repository instead.
- **Catching in the domain** what the transport should reject (e.g. auth) before it arrives.
- **Skipping the application layer** for async work, so retry policy scatters into workers.

## Checklist

- [ ] Can you name every layer in your request path?
- [ ] Can you name the owning layer for your top ten error categories?
- [ ] Does any domain module import an infrastructure library?
- [ ] Do background workers reuse the same application service as the HTTP path?

## Related

- [Responsibilities per Layer](./02-responsibilities-per-layer.md)
- [Where to Handle, Translate, and Propagate](./03-where-to-handle-translate-and-propagate.md)
- [Part VI — Error Boundaries and Translation](../../../part-06-boundaries-and-translation/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
