# Propagation Through Call Stacks

> Part V · Chapter 12 · Sections 12.1, 12.4, 12.10, 12.11 · _Estimated reading time: 16 min_
> **Prerequisite:** [Error, Fault, Failure, and Exception](../../../part-01-foundations/01-understanding-errors-and-failures/01-concepts/01-error-fault-failure-exception.md)

## In one sentence

When a function signals an error, control **unwinds the call stack** frame by frame until some
frame catches it — so where you *choose* to catch is the entire game.

## Why this matters in production

A 500 at the API edge is almost never where the failure originated. It originated in a repository
call six frames down, crossed a domain service, a controller, and middleware on the way up. If
each frame catches-and-wraps carelessly, the caller at the top sees a generic `Error` with no
cause, no code, and no retry hint. **Propagation is not "letting it bubble"; it is preserving
information while the error rises.**

## Core concept

A call stack is a stack of frames. Each frame knows its caller. When you `throw` (or return an
`Err`, or `panic`), the runtime discards frames in **last-in-first-out** order until it finds a
handler.

```text
  handler()          ← catch here? (outermost / API edge)
    └─ service()
         └─ domain()
              └─ repo()
                   └─ driver()  ← error originates here
```

The error travels *up* that chain. Three facts govern what happens:

1. **A frame either handles or does not.** There is no "partly handles" — if it does not rethrow,
   propagation stops there.
2. **Unwinding destroys local state.** If a frame opened a file and did not arrange cleanup, the
   resource leaks (see Chapter 14).
3. **Information is only preserved if someone carries it.** The raw error object is the only thing
   that travels automatically; context you add to a *different* object disappears.

### Nested calls (12.4)

Nested calls multiply the number of frames but not the rule. The subtle case is a nested call
*inside a catch block* — recovery that itself fails. That creates a second, overlapping
propagation (12.18, and Chapter 13.12).

### Boundaries (12.10)

A **boundary** is the frame where the fallback behavior is deliberately different from
propagating: return a safe default, retry, degrade, or translate to a transport error. Propagation
is *unbounded* by default, which is exactly why you place boundaries deliberately.

### Catching at the correct level (12.11)

Catch at the **lowest frame that can do something better than rethrow**. Concretely:

| If this frame can… | Then it should |
| ------------------ | -------------- |
| Recover with a safe fallback | Catch and recover |
| Translate to a domain/transport error | Catch and translate |
| Only add context | Catch, **wrap, and rethrow** |
| Do nothing useful | Not catch at all |

## How it works (mechanics)

Step by step, for a synchronous throw:

1. The runtime searches the current frame for an active `try`/`catch` (or `except`, `recover`).
2. No handler → the frame is popped, running any `finally` / `defer` / `with` cleanup registered
   in it.
3. Repeat up the stack.
4. First matching handler receives control **after** its `try` block, with the error bound.
5. No handler reaches the top → a default handler runs (process aborts, request returns 500,
   promise rejects with "unhandled rejection", goroutine panics the program).

> ⚠️ **Hazard.** `finally`/`defer` runs **during unwinding**. If it throws, it can *replace* the
> original error. Chapter 14 covers preserving the primary error.

## Worked example

A four-layer checkout path where the error originates in the repository:

```ts
// repo.ts — origin: the driver throws a low-level error
export async function insertOrder(row: OrderRow) {
  return db.query("insert into orders ...", [row]); // may throw PG error
}

// domain.ts — adds meaning, preserving cause
export async function placeOrder(cmd: PlaceOrder) {
  try {
    return await insertOrder(toRow(cmd));
  } catch (err) {
    throw new OrderPersistenceError("could not persist order", { cause: err });
  }
}

// service.ts — decides recovery (retry is owner of the transient policy)
export async function checkout(cmd: PlaceOrder) {
  try {
    return await placeOrder(cmd);
  } catch (err) {
    if (err instanceof OrderPersistenceError && isTransient(err.cause)) {
      return await retryOnce(() => placeOrder(cmd));
    }
    throw err; // not ours to swallow
  }
}

// http.ts — boundary: translate to the external contract, no internals leak
app.post("/checkout", async (req, res, next) => {
  try {
    const order = await checkout(req.body);
    res.status(201).json(order);
  } catch (err) {
    next(err); // global handler maps to a safe error envelope
  }
});
```

Trace: `driver` → `repo` (unwinds) → `domain` **wraps** → `service` decides → `http` boundary.
Each frame did exactly one thing: origin, wrap, decide, translate. None swallowed.

```text
OrderPersistenceError: could not persist order
  at placeOrder (domain.ts:8)
Caused by: error: duplicate key value violates unique constraint "orders_pkey"
  at insertOrder (repo.ts:3)
```

## Key data / numbers

- **PostgreSQL SQLSTATE `23505`** — `unique_violation`; a wrap-layer should not reclassify it as
  retryable (it is permanent for the same key).
- **PostgreSQL `40001`** — `serialization_failure`; genuinely transient, retry at the transaction
  owner.
- **HTTP/2 `GOAWAY`** and **gRPC `UNAVAILABLE`** propagate as *remote* errors; they cross a
  boundary and must be translated, not rethrown raw.
- **Node.js**: unhandled promise rejection default behavior is a fatal process exit (Node ≥ 15);
  no silent log.
- **Go**: an unrecovered panic in any goroutine terminates the whole program.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` handler called `verifySignature`, `parseEvent`, and `applySubscription`
inline. A malformed Stripe payload threw `SyntaxError` from `parseEvent`; nothing caught it until
the framework, which returned `400`. But the *cause* ("truncated JSON body, received 0 bytes")
was logged nowhere, and the wrapper had already overwritten the error. They introduced a boundary
at the ingest function: catch, classify as `WEBHOOK_MALFORMED`, log the raw body length, and return
`400` with a request ID. Propagation became *observable*.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Propagate everything | Minimal code; full context | Caller must know every error | Library/internal helpers |
| Catch-and-wrap at each layer | Rich local context | Verbose; risk of masking | When each layer adds meaning |
| Catch at one boundary only | Simple, consistent | Fallback decisions get lost | Small services |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch where the fallback differs | Catch in every layer "just in case" |
| Wrap and rethrow to add context | Replace the cause with a generic error |
| Let unexpected errors reach the boundary | Swallow unknown errors mid-stack |
| Register cleanup for every acquired resource | Release only on the happy path |

## Common mistakes

- **Catching purely to log, then rethrowing the same object** — duplicated logs, no added value.
- **Rethrowing a new `Error("failed")`** with no `cause` — the stack now points at the wrapper.
- **Assuming the nearest catch is the right one** — often the boundary is the right place.
- **Forgetting that `finally` runs during unwind** — cleanup that throws can hide the cause.

## Checklist

- [ ] For each error, can you name the frame where it is caught?
- [ ] Does every wrap pass the original error as `cause` / `%w` / suppressed?
- [ ] Does any frame catch just to log and rethrow? Remove it.
- [ ] Are cleanup handlers registered at the frame that acquired the resource?

## Related

- [Sync, Async, and Callback Propagation](./02-sync-async-and-callback-propagation.md)
- [Rethrow, Wrap, and Preserve Cause](./04-rethrow-wrap-and-preserve-cause.md)
- [Stack Traces and Cause Chains](../02-deep-dive/01-stack-traces-and-cause-chains.md)
- [Error Boundaries (Part VI)](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
