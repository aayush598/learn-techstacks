# Reusable API and Job Handling

> Part XXI · Chapter 54 · Sections 54.11, 54.12 · _Estimated reading time: 17 min_
> **Prerequisite:** [Shared Retry and Recovery Policies](./03-shared-retry-and-recovery-policies.md)

## In one sentence

A reusable API handler and a reusable job handler are the **two boundaries every service
needs** — and sharing them is what turns per-service error contracts into one contract.

## Why this matters in production

The boundary is where an error stops being internal and becomes a promise. Every service
that writes its own boundary makes its own promises — and the promises diverge in the
details nobody notices until a client integrates with two services at once.

The divergence is always in the same places:

- The **body shape** differs (`{"error": "..."}` versus `{"code": "...", "message": "..."}`).
- The **status code** for the same category differs.
- The **request id** is present in one and missing in the other.
- One includes a **stack trace** in development and the other in production.
- One returns `200` with an error body (Chapter 19's "when not to return 200 for
  failures").

A shared boundary eliminates all five at once, and it is one of the highest-value things
in the package: it is the difference between "each service has an error contract" and "the
platform has an error contract".

## Core concept

### 54.11 — Reusable API handling

The shared HTTP adapter turns an unknown error into an RFC 9457 problem-details response.
It is **not** a framework middleware — it is a pure function, so any framework can call it.

```ts
export interface ProblemContext {
  readonly operation: string;
  readonly correlationId?: string;
  readonly requestId?: string;
  readonly phase: "request" | "job" | "schedule" | "startup";
  readonly instance?: string;
}

export function toProblemDetails(err: unknown, ctx: ProblemContext): {
  status: number; body: ProblemBody;
} {
  const app = toAppError(err);                       // mapper chain, then internal fallback
  const policy = CATEGORY_POLICY[app.category];
  return {
    status: policy.httpStatus,
    body: {
      type: `${PROBLEM_BASE_URI}/${app.category.replace(/_/g, "-")}`,
      title: policy.publicCode,
      status: policy.httpStatus,
      detail: app.publicMessage ?? policy.publicCode,
      instance: ctx.instance,
      code: app.code,
      request_id: ctx.requestId,
    },
  };
}
```

Six rules the shared adapter enforces, so that no service can get them wrong:

| Rule | What it prevents |
| ---- | ---------------- |
| **No stack traces, ever** | Stack traces in a response leak internals (Chapter 34) |
| **No internal message** | The internal `message` may contain SQL, hostnames, or file paths |
| **No cause chain** | The cause chain is where secrets hide |
| **`request_id` always present** | A user cannot report a failure you cannot find |
| **Status comes from the category table** | Two services answering the same category differently |
| **Unknown errors → `500` + `INTERNAL_ERROR`** | A default that is safe for an unrecognised error |

The **internal fallback** is the important part. `toAppError` runs the mapper chain; if
nothing matches, it produces an `internal` category error with a generic message and the
original error preserved as the cause — for the logs, not for the response.

```ts
export function toAppError(err: unknown, mappers: readonly ErrorMapper[] = []): AppError {
  for (const mapper of mappers) {
    if (mapper.canMap(err)) return mapper.map(err);
  }
  if (isAppError(err)) return err;
  return createError("INTERNAL_ERROR", err instanceof Error ? err.message : "unknown error", {
    kind: "internal", cause: err,
  });
}
```

The `mappers` argument is the **only** configuration point in the whole adapter — and it is
a *list*, not a settings object. That is the difference between a policy and a framework.

### The framework wrapper

The wrapper is the smallest possible piece of framework code:

```ts
// adapters/http-express.ts
export function expressErrorHandler(mappers: readonly ErrorMapper[] = []) {
  return (err: unknown, req: Request, res: Response, _next: NextFunction) => {
    const { status, body } = toProblemDetails(err, {
      operation: `${req.method} ${req.path}`,
      correlationId: res.locals.correlationId,
      requestId: res.locals.requestId,
      instance: req.originalUrl,
      phase: "request",
    });
    if (res.headersSent) { res.end(); return; }     // never write twice
    res.status(status).json(body);
  };
}
```

**20 lines, zero policy.** A second framework's wrapper is the same shape with its own
request/response types.

### 54.12 — Reusable job handling

A job boundary is different from an HTTP boundary in four ways, and the shared job adapter
handles all four:

| Aspect | HTTP | Job |
| ------ | ---- | --- |
| The failure is seen by | a client waiting | nobody (the job is retried) |
| The contract is | a response body | a **status + a reason + an attempt count** |
| Retries are | the client's business | the queue's business |
| Terminal state | a `4xx`/`5xx` | **the DLQ** |

```ts
export interface JobFailure {
  readonly status: "failed" | "retryable" | "dead_lettered";
  readonly code: string;
  readonly category: ErrorCategory;
  readonly reason: string;              // safe to store in the DLQ
  readonly attempts: number;
  readonly maxAttempts: number;
  readonly retryAt?: string;            // ISO-8601, when retryable
  readonly cause?: SerializedCause;    // structured, truncated
  readonly occurredAt: string;
}

export function toJobFailure(err: unknown, attempts: number, maxAttempts: number, mappers: readonly ErrorMapper[] = []): JobFailure {
  const app = toAppError(err, mappers);
  const recovery = CATEGORY_POLICY[app.category].recovery;

  if (recovery.action === "retry" && attempts < maxAttempts) {
    return { status: "retryable", code: app.code, category: app.category, reason: app.message, attempts, maxAttempts, retryAt: computeRetryAt(attempts), cause: app.cause, occurredAt: app.occurredAt };
  }
  return { status: recovery.action === "terminate" ? "dead_lettered" : "failed", code: app.code, category: app.category, reason: app.message, attempts, maxAttempts, cause: app.cause, occurredAt: app.occurredAt };
}
```

The rules the job adapter enforces:

| Rule | Why |
| ---- | --- |
| **The failure carries the attempt count** | The operator needs to know if the retries were exhausted |
| **The reason is DLQ-safe** | The DLQ is stored, indexed, and sometimes read by humans and support |
| **The cause is truncated** | A DLQ row with a 4 MB stack trace is a storage incident |
| **A `resolve_later` category never lands in the DLQ as a failure** | It is a pending resolution, not a failure |
| **The status is one of three values** | `failed`, `retryable`, `dead_lettered` — the queue's vocabulary |
| **The category is preserved** | The DLQ can be filtered by category when triaging |

### The two boundaries, side by side

| | HTTP adapter | Job adapter |
| --- | ------------ | ----------- |
| Input | `unknown` | `unknown` |
| Output | `{status, body}` | `JobFailure` |
| Decides | the status and the public body | the status, the reason, the attempt count |
| Uses | the category table | the category table + the recovery policy |
| Knows about the transport | no (a wrapper does) | no |
| Configurable | the mapper list | the mapper list + `maxAttempts` |

Both are **pure functions**. That is the property that makes them shareable: a pure function
can be tested exhaustively in the package's own test suite, once, and every consumer gets
the benefit.

## How it works (mechanics)

The service's wiring, which is the entire adoption cost:

```ts
// src/platform/errors.ts — one file per service
import { expressErrorHandler } from "@acme/errors/adapters/http-express";
import { toJobFailure } from "@acme/errors/adapters/jobs";
import { stripeMapper, postgresMapper } from "@acme/errors/adapters/all";

export const mappers = [stripeMapper, postgresMapper];

app.use(expressErrorHandler(mappers));

// in the worker
const failure = toJobFailure(err, attempt, MAX_ATTEMPTS, mappers);
await jobQueue.deadLetter(failure);
```

**Wiring: 3 lines.** Everything else — the status, the body, the public code, the request id,
the redaction, the attempt count — comes from the package.

## Worked example

Acme's `WebhookIngest` service, before and after the shared adapters.

**Before** — a per-service handler, written by a different engineer in a different quarter:

```ts
app.use((err, req, res, next) => {
  log.error({ err }, "unhandled");
  if (err.name === "StripeSignatureError") {
    res.status(400).json({ error: "invalid signature" });
  } else if (err.code === "23505") {
    res.status(409).json({ error: "duplicate", requestId: req.id });
  } else {
    res.status(500).json({ error: "Internal server error", stack: err.stack });   // ← stack leak
  }
});
```

Note the **stack in the response**, and the **missing `request_id`** on two of the three
arms, and a `400` for a signature failure where the shared contract says `401`.

**After** — 3 lines of wiring:

```ts
app.use(expressErrorHandler([stripeMapper, postgresMapper]));
```

The response for the same three failures is now:

```json
{
  "type": "https://acme.internal/problems/auth-error",
  "title": "Unauthenticated",
  "status": 401,
  "detail": "Webhook signature could not be verified.",
  "instance": "/webhooks/stripe",
  "code": "WEBHOOK_SIGNATURE_INVALID",
  "request_id": "req_7f2c"
}
```

The **job** side had the same shape of problem. Acme's export worker had its own failure
record with **7 fields**, three of which were optional and none of which were guaranteed to
be present, so the DLQ triage tool had to handle missing fields. With the shared job
adapter, every DLQ row has the same **8 fields**, all present.

The measurable result across Acme's 11 services:

| Metric | Before | After |
| ------ | ------ | ----- |
| Distinct error response shapes | **9** | **1** |
| Responses containing a stack trace | **2 services** | **0** |
| Responses missing a `request_id` | **5 services** | **0** |
| DLQ record shapes | **4** | **1** |
| Lines of handler code per service | **~45** | **3** |
| Services to change to add a field to the error body | **11** | **1** (the package) |

## Key data / numbers

- **Shared HTTP adapter rules: 6** (no stack, no internal message, no cause chain, always a
  request id, status from the table, unknown → `500`).
- **Framework wrapper size: ~20 lines**, with **0** policy inside it.
- **Job failure record: 8 fields**, all present, 3 status values (`failed`, `retryable`,
  `dead_lettered`).
- **Configuration points in the adapters: 1** — the mapper list. There is no settings
  object.
- **Adoption cost per service: 3 lines of wiring.**
- **Truncation limit for a DLQ cause: 4 KB** (recommended; a DLQ is a database row, not a
  log).
- **Response bodies with a stack trace: 2 services → 0.**
- **Distinct error response shapes across 11 services: 9 → 1.**
- **Handler code per service: ~45 lines → 3 lines.**
- **Public contract fields: 7** (`type`, `title`, `status`, `detail`, `instance`, `code`,
  `request_id`) — the RFC 9457 fields plus `code` and `request_id`.

## Real-world use case — Acme SaaS, the partner integration that broke

Acme's partner API and its internal API returned the same failure in two different shapes:

```json
// internal API
{ "error": "validation failed", "fields": { "email": "invalid" } }

// partner API
{ "type": "...", "title": "Unprocessable Entity", "status": 422, "detail": "The request body failed validation." }
```

A partner integration that read both — because their integration layer was written by two
different teams — had to branch on the presence of a `type` field. The branch worked until
the internal API added a new field, and the partner's parser then **threw on the unknown
key**, turning a `422` into a `500` at the partner. The partner escalated; Acme's
engineering time went into a **3-week** investigation of a bug that was a shape difference.

The shared adapter fixed the shape problem, but the **real** fix was a contract: the public
API error body is now specified in the package, and a **CI check** verifies that every
service's error responses validate against the shared schema.

The measurable outcome: partner-facing errors now come from **one** adapter, and the
partner's integration team deleted **1,100 lines** of shape-detection code. Cross-service
contract bugs went from **4/quarter** to **0** in the following two quarters.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared adapter for all services | One contract; one place to change | One release to fix a bug everywhere | The default |
| Per-service adapters | Local autonomy | Divergence; N copies of a bug | Only where the contract is genuinely different (a public partner API) |
| A shared schema, per-service bodies | Flexible bodies, one validation | Bodies still differ; clients still branch | When a partner has a fixed contract |
| A framework-provided error handler | No code to write | Ties the contract to the framework | Only with one framework in the org |
| No shared adapter | No coupling | Nine shapes, as measured | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the shared adapter a pure function | Put framework types in the shared adapter |
| Keep the wrapper to ~20 lines | Add status codes to a framework wrapper |
| Always return a `request_id` | Return a body that sometimes has an id |
| Truncate the cause in a DLQ record | Store a whole stack trace in the DLQ |
| Use one of three job status values | Invent a status per job type |
| Specify the public body in the package | Let each service define its own body |
| Return the same shape for an unknown error | Return a different shape for "unexpected" |

## Common mistakes

- **The stack trace in the response.** One service leaks internals while the others do not;
  the partner's error parser then sees a field nobody expected.
- **The optional field.** `request_id` present on three arms and absent on the fourth
  breaks the partner's client.
- **The shared adapter with a settings object.** The moment it grows a flag, it is a
  framework.
- **The DLQ record with optional fields.** Triage tools must then handle missing values,
  and the tool is where the bug hides.
- **The `200` with an error body.** A boundary that returns `200` for a failure teaches
  every client to check the body, which they will not do consistently.

## Checklist

- [ ] The shared HTTP adapter is a pure function with no framework types.
- [ ] Every framework wrapper is ~20 lines and contains no policy.
- [ ] Every error response has the same 7 fields, including `request_id`.
- [ ] No response contains a stack trace, an internal message, or a cause chain.
- [ ] Every job failure record has the same 8 fields, with the cause truncated.
- [ ] A CI check validates every service's error responses against the shared schema.

## Related

- [The Reusable Core Library](./01-the-reusable-core-library.md)
- [Multiple Frameworks, Languages, and Scope](./05-multiple-frameworks-languages-and-scope.md)
- [Chapter 20 — Standardized API Error Responses](../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
