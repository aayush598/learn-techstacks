# Middleware Ordering and the Swallowing Anti-Pattern

> Part VIII · Chapter 21 · Sections 21.16, 21.17 · _Estimated reading time: 16 min_
> **Prerequisite:** [Auth, Authz, and Rate-Limit Middleware](./03-auth-authz-and-rate-limit-middleware.md)

## In one sentence

Middleware order is a **correctness property** — the same middleware in the wrong sequence yields
wrong statuses, wrong keys, and missed failures — and **swallowing** (catching an error and
continuing without handling it) is the anti-pattern that turns observable failures into silent
corruption.

## Why this matters in production

Ordering bugs are subtle because the code "works" in the happy path. Rate limiting before auth
throttles the wrong key. Parsing after authz authorizes garbage. A logging middleware placed
outside the catch-all misses every error the catch-all handles. And swallowing is worse than a
crash: a `catch {}` that drops a failed audit log or a failed webhook ACK leaves the system in a
state that looks fine but is inconsistent — the hardest failures to detect and the most expensive
to unwind. Both problems are cheap to prevent with a documented order and a no-empty-catch rule.

## Core concept — order is the contract's assembly line

Each middleware transforms or rejects the request. The order encodes dependencies:

```text
  edge timeouts / headers
        │
   request id (correlation)          ← everything after needs requestId
        │
   size guard                         ← reject before allocating
        │
   content-type guard                 ← reject before parsing
        │
   parse body                         ← produces the parsed structure
        │
   authenticate                       ← needs headers; yields principal
        │
   authorize                          ← needs principal; may need parsed body
        │
   rate limit (per identity)          ← needs principal/tenant
        │
   route handler                      ← needs everything above
        │
   serialize + write                  ← owns the response head
        │
   global catch-all (outermost)       ← wraps ALL of the above
```

Rules that fall out of the dependencies:

- **`requestId` first.** Every log line and every error body needs it; generating it later means
  early failures have no correlation handle.
- **Size and content-type before parse.** Reject cheaply, before buffering.
- **Parse before authz-that-needs-body.** Authorizing unparsed data is a bypass vector.
- **Authenticate before identity-keyed rate limits.** You cannot key on an unknown principal.
- **Catch-all outermost.** In frameworks where `use()` order defines scope, a catch-all declared
  in the middle only sees errors from middleware registered *after* it.

## 21.16 — Ordering as a correctness property

Consider the same three middleware in two orders:

```ts
// ❌ WRONG: rate limit keyed on tenant runs before auth → key is undefined/IP
app.use(rateLimitByTenant);
app.use(authenticate);
app.use(authorize);

// ✅ RIGHT: principal exists before the identity-keyed limit
app.use(authenticate);
app.use(authorize);
app.use(rateLimitByTenant);
```

Beyond auth/limit, three more ordering traps:

1. **Logging outside the catch-all.** A `logger` registered before the catch-all sees the
   request but not the error the catch-all catches. Register error-aware logging inside the
   catch-all (or after it, harnessed to it).
2. **Error middleware before routes.** In Express, error-handling middleware (`(err,req,res,next)`)
   only catches errors from layers registered *before* the error handler. Placing it early means
   later route errors are uncaught.
3. **Compression/transform after commit.** Anything that buffers a response (compression, CORS
   header injection) must run before the head is committed; a middleware that assumes it can add
   headers after streaming is silently ignored or errors.

| Middleware | Must run before | Why |
| ---------- | --------------- | --- |
| Request-id | everything logged | correlation |
| Size / content-type guard | body parser | reject without buffering |
| Body parser | authz-needs-body, handler | structures the request |
| Auth | identity-keyed rate limit, authz | establishes principal |
| Authz | handler | prevents forbidden work |
| Rate limit (identity) | handler | throttles fair key |
| Catch-all | (nothing — it is outermost) | sees all failures |
| Compression / header transforms | response head commit | can only modify unwritten headers |

## 21.17 — Swallowing

Swallowing is any `catch` (or equivalent) that absorbs an error without either handling it
(producing the correct outcome) or propagating it to the boundary. Variants:

```ts
// ❌ Classic swallow: failure disappears.
try { await audit.log(event); } catch { /* ignore */ }

// ❌ Swallow-and-continue: pretends success after a failed side effect.
try { await charge(); } catch (e) { log.warn(e); }
return { ok: true };            // caller believes the charge happened

// ❌ Swallow by returning a default: masks a dependency outage.
let quota = 0;
try { quota = await quotaService.get(id); } catch {}
if (quota <= 0) reject();       // outage looks like "no quota"
```

Why swallowing is dangerous:

- **It converts failures into inconsistent state.** A dropped audit log, a missing metric, or a
  skipped rollback leaves the system in a state no one can reconstruct.
- **It hides dependency outages.** A `catch {}` around a cache/DB read makes an outage look like
  "empty" or "zero," which then drives wrong business decisions.
- **It defeats the boundary.** The catch-all never sees the error, so there is no `requestId`, no
  problem document, and no alert.

The legitimate alternatives:

| Situation | Instead of swallowing | Do this |
| --------- | --------------------- | ------- |
| Optional side effect (analytics) | `catch {}` | Log at warn with `requestId`; emit a metric; continue |
| Best-effort cache write | `catch {}` | Log; continue (the read path is the source of truth) |
| Side effect that matters (payment, audit, ACK) | skip it | Propagate to the boundary → error response |
| Dependency that drives a decision | `catch {}` defaulting to 0/false | Distinguish "unavailable" from "empty"; return `503` |
| Cleanup in `finally` | swallow the cleanup error silently | Log; if it masks the primary error, attach as suppressed |

The key distinction: **swallowing is acceptable only when the operation is explicitly optional,
and even then it must be logged and metered.** "I forgot this could fail" is not optionality.

> ⚠️ **Hazard.** The most dangerous swallow is around a side effect whose success the client
> assumes. `WebhookIngest` that catches a failed signature-store write and returns `200` tells
> Stripe the event was processed; it wasn't, and the retry never comes.

## How it works — a review procedure for the chain

```text
1. List middleware in registration order.
2. For each pair, check the dependency (does B need A's output?).
3. Verify the catch-all is outermost (or in the correct terminal position
   for the framework).
4. Grep for empty catch blocks and catch-and-return-default.
5. For each catch, answer: is this operation truly optional?
     yes → is it logged + metered?
     no  → does it propagate or translate to the boundary?
```

This is a five-minute review that catches the majority of boundary bugs before they ship.

## Worked example — WebhookIngest ordering + swallow

`POST /api/v1/webhooks/stripe` (fast-ACK endpoint):

```text
requestId → signature verify (auth-like) → parse event → dedupe check
          → enqueue for processing → 200 ack
```

Two bugs Acme found in review:

1. **Ordering.** The dedupe check (a Redis lookup keyed on event id) ran *after* enqueue. A
   duplicate event could be enqueued twice before the dedupe write was confirmed. Fix: dedupe
   *before* enqueue, inside the same idempotent unit.
2. **Swallowing.** The enqueue's `catch` logged and returned `200`, so a broker outage looked
   like a successful ACK and Stripe never retried. Fix: an enqueue failure now propagates to the
   boundary and returns `503` with `Retry-After`, so Stripe retries the event.

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 15
Content-Type: application/problem+json
X-Request-Id: req_h4

{
  "type": "/problems/service-unavailable", "title": "Service Unavailable",
  "status": 503, "detail": "Webhook queue is temporarily unavailable. Retry shortly.",
  "instance": "/api/v1/webhooks/stripe", "code": "WEBHOOK_QUEUE_UNAVAILABLE",
  "requestId": "req_h4", "retryAfterSeconds": 15
}
```

Same endpoint, correct order, no swallow — the provider's retry mechanism now does its job.

## Key data / numbers

- **Express:** error handlers (`(err,req,res,next)`) must be registered after routes; they catch
  errors from earlier layers only.
- **Koa:** `await next()` composes an onion; error-handling middleware must wrap *around* the
  downstream stack (registered before it, awaiting `next()` inside a `try`).
- **Fastify:** error handling is centralized via `setErrorHandler`, and hooks/plugins have a
  defined encapsulation order — plugins do not leak to siblings by default.
- **Empty `catch {}` counts as swallowing** even when it "can't happen"; linters
  (`no-empty`, `no-empty-catch`) are the cheapest enforcement.
- **Dedupe ordering:** idempotency records must be written/checked before the non-idempotent
  side effect, never after (Ch. 28).

## Real-world use case — Acme SaaS per-IP rate limit

Acme's `Checkout` route registered a per-tenant rate limiter *before* authentication to "fail
fast." Because the tenant was unknown at that point, the limiter silently fell back to the client
IP. A partner integration behind a single egress IP triggered the limit and all its requests
failed with `429`, while the intended per-tenant protection never applied. Reviewing the chain
order (21.16) made the bug obvious: an identity-keyed middleware placed before identity existed.
Moving the limiter after auth restored fairness; the IP fallback was retained only for anonymous
endpoints, where it is correct. No code was rewritten — only reordered.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Strict documented order, catch-all outermost | Predictable; testable | Rigid; must be enforced | Default |
| Ad hoc per-route middleware | Local flexibility | Order bugs recur; shape drift | Prototypes only |
| Empty catch with a lint exception | Silences noise | Hides real failures | Never |
| Optional-side-effect catch with log + metric | Resilient; visible | Slightly more code | Analytics/best-effort only |
| Propagate every error to the boundary | No hidden failures | Some optional ops fail requests | When correctness > availability |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Generate `requestId` first | Emit errors with no correlation handle |
| Order middleware by real dependencies | Copy an ordering that "looks right" |
| Register the catch-all outermost/last | Place it before routes it must cover |
| Log and meter best-effort failures | Use empty `catch {}` |
| Propagate side effects the client assumes | Return `200` after a failed enqueue |
| Distinguish "unavailable" from "empty" | Default a failed dependency read to 0/false |

## Common mistakes

- **Assuming framework order semantics are universal.** Express, Koa, and Fastify differ; know
  yours (see the ordering deep-dive).
- **Placing logging before the catch-all.** The error is logged nowhere.
- **Catch-and-return-default around a decision dependency.** An outage becomes a wrong business
  answer.
- **`catch (e) { res.status(500) }` in middleware.** Bypasses the registry and the envelope.
- **Treating a lint-disabled empty catch as "handled."** It is still swallowing.

## Checklist

- [ ] The chain order is documented and matches real dependencies.
- [ ] `requestId` is generated first; the catch-all is outermost.
- [ ] No empty `catch {}` remains (`no-empty`/`no-empty-catch` enabled).
- [ ] Every best-effort catch logs and emits a metric.
- [ ] Side-effecting operations the client assumes success for propagate on failure.
- [ ] Dedupe/idempotency records are written before the side effect, not after.

## Related

- [Middleware Ordering Mechanics](../02-deep-dive/01-middleware-ordering-mechanics.md)
- [Global Handlers and the Request Boundary](./01-global-handlers-and-the-request-boundary.md)
- [Error-Handling Patterns and Anti-Patterns (Ch. 46)](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
