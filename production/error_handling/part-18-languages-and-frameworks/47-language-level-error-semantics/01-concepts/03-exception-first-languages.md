# Exception-First Languages in Depth — JS/TS, Node.js, Python, Java, C#/.NET, PHP

> Part XVIII · Chapter 47 · Sections 47.2–47.5, 47.8–47.9 · _Estimated reading time: 24 min_
> **Prerequisite:** [Language Comparison at a Glance](./02-language-comparison-at-a-glance.md)

## In one sentence

In the six exception-first languages the failure mechanism is the same (`throw`/`raise` +
`catch`/`except`) but the **compiler's involvement, the chaining API, and the runtime's failure
shapes** differ enough to cause real incidents when teams assume they don't.

## Why this matters in production

Most SaaS codebases are majority exception-first (TS services, Python AgentRun workers, Java
billing, PHP storefronts on Laravel). The production failures in these languages share a pattern:
**the exception crossed a boundary nobody owned** — a floating promise in Node, a bare `except:`
in Python, a swallowed `catch (Exception)` in Java, a `catch (Throwable)` that ate a fatal `Error`
in PHP. This file gives you the per-language mechanics and the exact boundary rules.

## 47.2 / 47.3 — JavaScript, TypeScript, and Node.js

### Semantics

JS `throw` accepts **any value**; production convention is `Error` (or subclass) only.
TypeScript's type system does not model thrown errors at all — the signature is a promise about
returns, never about throws. Under `strict: true` (TS 4.4+, `useUnknownInCatchVariables`), the
`catch` variable is `unknown`, forcing narrowing — the single best default JS has for errors.

```ts
function parseExportPayload(body: unknown): ExportPayload {
  const result = schema.safeParse(body);
  if (!result.success) {
    throw new CheckoutError("EXPORT_PAYLOAD_INVALID", {
      cause: result.error,          // ES2022 cause
      details: result.error.issues,
    });
  }
  return result.data;
}

try {
  const payload = parseExportPayload(req.body);
} catch (err) {
  if (err instanceof CheckoutError && err.code === "EXPORT_PAYLOAD_INVALID") {
    return res.status(422).json(toProblemDetails(err));
  }
  throw err;                        // never swallow what you don't recognize
}
```

### Node.js specifics

| Node failure shape | What it carries | Handling rule |
| ------------------ | --------------- | ------------- |
| System error | `code` (`ENOENT`, `ECONNRESET`), `syscall`, `errno` | Classify by `code`, never by message |
| `AbortError` | `code: "ABORT_ERR"` | Not a failure — map to cancellation, do not retry |
| Unhandled rejection | Stack + value of the rejection | Fatal by default (Node ≥ 15); never rely on the default in a worker |
| `EventEmitter` `'error'` | Any value | No listener = thrown; always attach one on long-lived emitters |

```ts
// Node system errors are classifiable by code — the contract is `code`, not message.
try {
  await fs.readFile(exportPath);
} catch (err) {
  if (isErrnoException(err) && err.code === "ENOENT") return fallbackExport();
  throw err;
}
```

### The JS/TS pitfalls that page people

1. **Floating promise** — `void doWork()` with no `.catch`: failure becomes an
   `unhandledRejection`. Enforce `no-floating-promises`.
2. **`instanceof` across realms** — a `CheckoutError` from a bundled copy fails `instanceof`
   against another copy. Match `err instanceof Error && err.name === "CheckoutError"` or the
   `code` field.
3. **`throw nonError`** — `throw res.data` (an object) has no stack; logs show `undefined`.
4. **Double JSON serialization of errors** — `JSON.stringify(new Error("x"))` is `{}`; log
   `err.stack` or a serializer that knows about `cause`.

## 47.4 — Python

### Semantics

Python exceptions form a deep **runtime hierarchy**: `BaseException` → `Exception` → your app
errors, with `OSError` (incl. `FileNotFoundError`, `ConnectionError`), `ValueError`,
`KeyError`, `TimeoutError`, etc. Nothing is checked statically. `try/except/else/finally` is the
full contract; `else` runs only when no exception occurred (the least-used, most useful clause).

### Chaining — the feature other languages envy

```python
class AcmeError(Exception):
    """Base for all Acme application errors."""
    def __init__(self, code: str, *, retryable: bool = False, **ctx):
        super().__init__(f"{code}: {ctx}")
        self.code = code
        self.retryable = retryable
        self.ctx = ctx

class CheckoutError(AcmeError):
    pass

async def capture(amount: int, idempotency_key: str) -> Receipt:
    try:
        return await stripe.capture(amount, idempotency_key=idempotency_key)
    except stripe.error.CardError as exc:
        # `from exc` sets __cause__ and suppresses the misleading implicit chain
        raise CheckoutError("CARD_DECLINED", retryable=False) from exc
    except stripe.error.RateLimitError as exc:
        raise CheckoutError("GATEWAY_RATE_LIMITED", retryable=True) from exc
```

- `raise X from Y` — explicit cause (`__cause__`), traceback shows "The above exception was the
  direct cause…".
- `raise X from None` — suppresses the implicit `__context__` chain (use when the inner
  exception is noise, not signal).
- Without `from`, Python still chains via `__context__` — the traceback says "During handling of
  the above exception" — which is *wrong semantics* when you intend cause.

### Rules that keep Python services alive

- **Ban bare `except:`** — it catches `KeyboardInterrupt`, `SystemExit`, and (critically)
  `asyncio.CancelledError`, which subclasses `BaseException` since Python 3.8. Catching it
  breaks task cancellation.
- Catch the **narrowest** exception you can handle; re-`raise` anything unrecognized.
- `contextlib.suppress(X)` for deliberate, documented ignoring (cleanup paths).
- **`ExceptionGroup` / `except*` (3.11+)** for parallel work: `asyncio.TaskGroup` raises an
  `ExceptionGroup` of child failures; `except* CheckoutError:` handles only that type out of
  the group.

## 47.5 — Java

### The checked/unchecked split

```text
Throwable
├── Error                    ← never catch (OOM, StackOverflow, LinkageError)
└── Exception
    ├── IOException, SQLException, …      ← CHECKED: catch or `throws` — compiler enforces
    └── RuntimeException
        ├── NullPointerException, IllegalArgumentException, …
        └── your CheckoutException       ← UNCHECKED: escapes silently
```

**Checked** = part of the method contract (`throws IOException`). Callers must handle or
propagate. **Unchecked** = not in the contract. Frameworks (Spring) almost always throw
unchecked; most modern codebases define domain errors as unchecked and reserve checked for
truly-forced handling at API boundaries.

```java
public final class CheckoutException extends RuntimeException {
    private final String code;
    private final boolean retryable;

    public CheckoutException(String code, boolean retryable, Throwable cause) {
        super(code, cause);                    // cause preserved natively
        this.code = code;
        this.retryable = retryable;
    }
    public String code() { return code; }
    public boolean retryable() { return retryable; }
}

public Receipt capture(PaymentIdempotency key) {
    try {
        return gateway.capture(key);
    } catch (IOException ioe) {
        // checked failure translated to unchecked domain error, cause attached
        throw new CheckoutException("GATEWAY_UNAVAILABLE", true, ioe);
    }
}
```

### Java's chaining and cleanup features

- **Cause**: every throwable's constructor takes `(message, cause)`; `initCause` for the rare
  no-cause constructor.
- **`addSuppressed`**: try-with-resources automatically attaches exceptions thrown while
  closing a resource as *suppressed* — visible in the stack trace, non-fatal to the primary
  error.
- **Multi-catch** `catch (TimeoutException | ConnectException e)` avoids duplicated blocks.
- **Sealed + exhaustive switch (17/21)**: model error outcomes as a sealed interface when you
  want Rust-like exhaustiveness without checked exceptions.

```java
sealed interface CheckoutFailure permits Declined, RateLimited, Unavailable {}
// switch (failure) { case Declined d -> …; case RateLimited r -> …; case Unavailable u -> … }
// javac rejects non-exhaustive switches.
```

### The Java rules

- **Never catch `Throwable` or `Error`** — `OutOfMemoryError` must reach the JVM.
- Catching bare `Exception` at a boundary is allowed *only* as the outermost handler that logs
  and maps to 500.
- Creating exceptions is expensive (stack capture); do not use throw/catch as a loop's branch.
- `CompletionException`/`ExecutionException` **wrap** async failures — unwrap the cause before
  classifying, or every `CompletableFuture` failure looks like one type.

## 47.8 — C# / .NET

### Semantics and the rethrow rule

Exceptions are the only built-in failure mechanism. Two rules separate juniors from seniors:

```csharp
try { await checkout.CaptureAsync(key, ct); }
catch (GatewayTimeoutException ex)
{
    logger.LogWarning(ex, "gateway timeout for {Key}", key);
    throw;                       // ✅ preserves original stack trace
}
// throw ex;                    // ❌ resets stack trace to THIS line — destroys evidence
```

- **`throw;`** rethrows with the original stack. **`throw ex;`** resets it to the rethrow
  site. For async rethrows across awaits, use
  `ExceptionDispatchInfo.Capture(ex).Throw();` (`System.Runtime.ExceptionServices`) — the same
  mechanism `Task` uses internally.

```csharp
public async Task<Receipt> CaptureAsync(string idemKey, CancellationToken ct)
{
    try {
        return await _gateway.CaptureAsync(idemKey, ct);
    }
    catch (HttpRequestException ex) {
        throw new CheckoutException("GATEWAY_UNAVAILABLE", retryable: true, ex);
    }
    catch (TaskCanceledException ex) when (!ct.IsCancellationRequested) {
        // HttpClient timeout: NOT caller cancellation — retryable gateway timeout
        throw new CheckoutException("GATEWAY_TIMEOUT", retryable: true, ex);
    }
}
```

- **`when` filters** keep catch clauses selective without nested ifs; a filter that throws
  routes to the next handler (pitfall — keep filters pure).
- Inner exceptions: `new CheckoutException(msg, inner)` — chains; `AggregateException` bundles
  parallel failures (`Task.WhenAll`) and must be flattened/unwrapped before classification.
- `async void` exists only for event handlers; a throw inside one bypasses your handlers and
  reaches the SynchronizationContext — in services, always `async Task`.

## 47.9 — PHP

### `Throwable` is the contract

```text
Throwable (PHP 7+)
├── Exception          ← userland throwables (your classes, SPL exceptions)
└── Error               ← engine errors: TypeError, ArgumentCountError,
                          ValueError, DivisionByZeroError, AssertionError, ParseError
```

```php
final class CheckoutException extends \Exception
{
    public function __construct(
        public readonly string $errorCode,
        public readonly bool $retryable,
        string $message,
        ?\Throwable $previous = null,        // native chaining
    ) {
        parent::__construct($message, 0, $previous);
    }
}

try {
    $receipt = $stripe->capture($amount, $idempotencyKey);
} catch (\Stripe\Exception\CardException $e) {
    throw new CheckoutException('CARD_DECLINED', false, $e->getMessage(), $e);
} catch (\Throwable $e) {                    // catches BOTH Exception and Error
    throw new CheckoutException('CHECKOUT_FAILED', true, $e->getMessage(), $e);
}
```

Rules for PHP services:

- Catch **`Throwable`**, not `Exception`, at boundaries — otherwise `TypeError` from a bad SDK
  call bypasses your handler.
- Chain with the **`$previous`** constructor argument; PSR-friendly loggers print the full
  chain.
- PHP's own warnings/notices are **not** exceptions; a framework error handler or
  `set_error_handler` may convert them — know your platform's setting.
- Laravel/Symfony throw HTTP-aware hierarchies (`HttpException` → status code) that the
  framework maps for you — extend them rather than inventing parallel codes.

## Key data / numbers

- TS `useUnknownInCatchVariables`: **TypeScript 4.4** (2021), on under `strict: true`.
- Node unhandled-rejection default **fatal since Node 15**; `AbortError.code = "ABORT_ERR"`.
- Python `CancelledError` moved to `BaseException` in **Python 3.8** — `except Exception` no
  longer catches it (a feature; bare `except:` still does, and that's the bug).
- `ExceptionGroup`/`except*`: **Python 3.11** (2022).
- Java try-with-resources + multi-catch: **Java 7** (2011); sealed types: **Java 17**;
  pattern-matching switch: **Java 21**.
- .NET `ExceptionDispatchInfo`: since **.NET Framework 4.5 / .NET Core 1.0**.
- PHP `Throwable` unification: **PHP 7.0** (2015); `Error` hierarchy same release.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` (Python) verified Stripe signatures in middleware, then called a shared
`handle_event()`. A `stripe.error.SignatureVerificationError` was caught by a broad
`except Exception` around the whole handler and logged as a 500-retryable — Stripe retried
webhooks that would **never** verify, for hours. The fix: catch `SignatureVerificationError`
narrowly at the trust boundary, translate to `WebhookError("SIGNATURE_INVALID", retryable=False)`,
ack the event, and add a metric. Python's narrow-catch rule turned a retry storm into a
classified rejection.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Unchecked domain errors + narrow catches (Java/C#) | Flexible, framework-friendly | Compiler doesn't force handling | Default for services |
| Checked exceptions at the edge only (Java) | Forces edge handling | Propagates through signatures | Boundary adapters |
| `Result`-style via libraries (C#, TS) | Explicit signatures | Non-std; team learning | Library/internal APIs |
| Broad `catch (Throwable)` everywhere | "Safe" | Swallows OOM, cancellation, bugs | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Match Node system errors on `code` | Match on `err.message` substrings |
| `raise … from exc` in Python | Bare `raise` after catching a different type |
| `throw;` / `ExceptionDispatchInfo` in C# | `throw ex;` in a catch |
| Catch `Throwable` at PHP boundaries | Catch `Exception` and miss `TypeError` |
| Narrow catches; rethrow unknown | `catch (Exception)` with a log-and-continue in Java/Python |
| Unwrap `CompletionException`/`AggregateException` | Classify the wrapper type |

## Common mistakes

- **`catch (err)` + `err instanceof Error` as the only guard in TS** — true for every Error but
  not for `throw "str"`; still narrow by `code`.
- **Python `except Exception` around `await`** — hides cancellation and turns aborts into 500s.
- **Java `catch (Throwable t)` in a worker loop** — swallows `OutOfMemoryError` and keeps the
  loop running on a dying JVM.
- **C# async void handlers** — exceptions escape the pipeline; use `async Task`.
- **PHP catching `Exception` only** — engine `Error`s bypass and hit the framework's raw 500.
- **Logging the wrapper, not the cause** — log `AggregateException.InnerExceptions`,
  `CompletionException.getCause()`, or the Python `__cause__` chain.

## Checklist

- [ ] Is every catch clause either handling a *specific* type or an owned boundary that maps to 500?
- [ ] Does every Python `raise` across a library boundary use `from`?
- [ ] Are Node system errors classified by `code` with a shared table?
- [ ] Does every C# rethrow use `throw;` or `ExceptionDispatchInfo`?
- [ ] Does every PHP boundary catch `Throwable`?
- [ ] Are floating promises, bare excepts, and `async void` banned by lint/CI?

## Related

- [Async Constructs and Common Pitfalls](./05-async-constructs-and-pitfalls.md)
- [Native Chaining and Wrapping](../02-deep-dive/01-native-chaining-and-wrapping-capabilities.md)
- [Same Error, Five Languages](../03-practical-examples/01-same-error-across-languages.md)
- [Chapter 13 — Catch Blocks and Recovery Logic](../../../part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)
