# Stack Traces and Cause Chains

> Part V · Chapter 12 · Sections 12.14, 12.18 (mechanics) · _Estimated reading time: 20 min_
> **Prerequisite:** [Rethrow, Wrap, and Preserve Cause](../01-concepts/04-rethrow-wrap-and-preserve-cause.md)

## In one sentence

A **stack trace** records the frames captured at construction, while a **cause chain** links
errors across layers — and the two together are the only artifact that tells you *what failed and
where*, so both must survive every wrap, hop, and translation.

## Why this matters in production

When an incident is live, the trace is the map. If a wrap created a new error without `cause`, you
get a map that starts at the wrapper. If a logger prints only `err.message`, you get no map at
all. Engineers then reproduce blindly, extend the incident, and add logging that ships with the
next release. Mastering traces and cause chains is what separates a five-minute from a five-hour
diagnosis.

## Core concept

Two orthogonal pieces of information:

| Artifact | Answers | Captured when | Survives wrap only if |
| -------- | ------- | ------------- | --------------------- |
| **Stack trace** | Where (which frames)? | `Error` construction / raise | cause is attached |
| **Cause chain** | Why / through what? | Each wrap adds a link | `cause`/`from`/`%w` used |

```text
┌── top error (most context, least specificity)
│   CheckoutFailed: charging card for order 8891
│     at checkout (service.ts:41)
│     cause ────────────────────────────────┐
│                                            ▼
│   PaymentDeclined: card declined           (boundary translation)
│     at charge (gateway.ts:12)
│     cause ────────────────────────────────┐
│                                            ▼
│   GatewayHTTPError: 402                    (transport)
│     at post (http.ts:88)
│     cause ────────────────────────────────┐
│                                            ▼
└── TLSHandshakeTimeout: handshake timed out (deepest, most specific)
      at connect (tls.ts:7)
```

Read it bottom-up for *cause*, top-down for *context*.

## How it works (mechanics)

### Stack capture

When you create an `Error`/`Exception`, the runtime walks the current call stack and stores an
array of frames (function name, file, line, column). This is cheap-ish but not free; deep stacks
cost more. In async code the captured stack ends at the `await` boundary — the continuation's
frames are *not* included.

### Cause chaining

Chaining is explicit in most languages:

```ts
throw new CheckoutFailed("charging card", { cause: err });
```

```python
raise CheckoutFailed("charging card") from err
```

```go
return fmt.Errorf("charging card: %w", err)
```

```java
throw new CheckoutFailed("charging card", err);
```

The result is a **tree**, not a line, once suppressed/nested errors enter (a rejection *and* a
cleanup failure). `errors.Is`, `__cause__`, `getCause()`, and `err.cause` traverse it.

### Before / after view

**Before** (masking) — stack points at the wrong place; nothing below:

```text
Error: Charge failed
    at checkout (service.ts:39)     ← the catch block, NOT the failure
```

**After** (wrapping with cause) — full story:

```text
PaymentFailed: charging card for order 8891
    at chargeCard (payment.ts:14)
    at checkout (service.ts:39)
caused by GatewayHTTPError: 502 from payments-api
    at post (http.ts:88)
caused by SocketError: ECONNRESET
    at TLSSocket.onError (net.js:1712)
```

## Worked example — one failure, viewed two ways

The failure originates in a TLS handshake. Watch it move through four layers in Go:

```go
// driver layer
func (c *client) do(req *http.Request) (*http.Response, error) {
    resp, err := c.http.Do(req)
    if err != nil {
        return nil, fmt.Errorf("http do: %w", err) // cause: net error
    }
    return resp, nil
}

// adapter layer
func (g *Gateway) Charge(ctx context.Context, p Payment) error {
    if err := g.client.post(ctx, "/charges", p); err != nil {
        return fmt.Errorf("gateway charge: %w", err)
    }
    return nil
}

// domain layer
func (s *Checkout) Checkout(ctx context.Context, o Order) error {
    if err := s.gateway.Charge(ctx, o.Payment); err != nil {
        return fmt.Errorf("checkout order %s: %w", o.ID, err)
    }
    return nil
}
```

Querying the chain still works through every layer:

```go
var netErr net.Error
if errors.As(err, &netErr) && netErr.Timeout() {
    // retry — the timeout is visible 3 wraps deep
}
if errors.Is(err, context.DeadlineExceeded) {
    // deadline hit
}
```

The printed chain:

```text
checkout order 8891: gateway charge: http do: dial tcp 10.0.3.7:443: i/o timeout
```

Each `%w` added a frame of meaning; the leaf is untouched.

## Key data / numbers

- **Node/V8**: `Error.captureStackTrace`, `Error.stackTraceLimit` (default 10 frames; raise for
  deep async paths). `cause` is ES2022.
- **Java**: `Throwable.getStackTrace()` length equals frames captured; `-XX` flags and
  `StackWalker` control capture cost.
- **Python**: `__traceback__` accumulates frames as the exception propagates; `sys.tracebacklimit`
  caps printed depth.
- **Go**: `%w` wraps; `runtime/debug.Stack()` captures goroutine stacks; panics carry a stack
  unless recovered and discarded.
- **Rust**: not all errors capture backtraces by default; `RUST_BACKTRACE=1` and `anyhow` with the
  `backtrace` feature do.

## Real-world use case — Acme SaaS

Acme's `Checkout` logged `err.message` only. A gateway `502` appeared in support tickets as
"checkout failed" with no cause. After adopting structured logging that serializes the full
`cause` chain and raising `Error.stackTraceLimit` to 30, the same class of incident was traced to a
provider-side TLS negotiation failure in minutes. The wrapper messages also got action names
("charging card", "reserving inventory"), so the chain read as a sentence.

## Trade-offs

| Technique | Pros | Cons | When to use |
| --------- | ---- | ---- | ----------- |
| Wrap with operation name + cause | Readable, complete | Slightly more types | Every meaningful layer |
| Single deep stack, no wrapping | Simple | No layer meaning; async loses it | Trivial internal helpers |
| Log whole chain structurally | Complete diagnosis | More log volume | Always |
| Log message string | Cheap | Destroys structure/chains | Never for errors |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap with a named operation and `%w`/`cause` | Replace the error with `new Error(msg)` |
| Log the full cause chain | Log `err.message` only |
| Preserve the deepest stack | Re-throw from a catch that re-creates the error |
| Raise stack depth for deep async paths | Leave the default 10 frames on a 40-frame path |
| Include correlation IDs alongside traces | Assume the trace is portable across services |

## Common mistakes

- **Async stack truncation** mistaken for the real origin.
- **`err.message` logging** that serializes a string, losing `cause` and frames.
- **Wrapping without `cause`** — the most common cause of "why is the stack pointing here?".
- **Logging the same error at every layer** — five identical entries, one useful.
- **Storing only `.toString()`** on the error object for later — irreversible information loss.

## Checklist

- [ ] Does every wrapper preserve `cause`?
- [ ] Do logs serialize the whole chain, not just the message?
- [ ] Is `stackTraceLimit` (or equivalent) sized for your deepest path?
- [ ] Do cross-service errors carry a correlation ID to join traces?
- [ ] Can you read a chain bottom-up for cause and top-down for context?

## Related

- [Rethrow, Wrap, and Preserve Cause](../01-concepts/04-rethrow-wrap-and-preserve-cause.md)
- [Preserving Cause — Before/After](../03-practical-examples/02-preserving-cause-before-after.md)
- [Async Propagation and Unhandled Rejections](./02-async-propagation-and-unhandled-rejections.md)
- [Designing the Application's Error Model (Part III)](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
