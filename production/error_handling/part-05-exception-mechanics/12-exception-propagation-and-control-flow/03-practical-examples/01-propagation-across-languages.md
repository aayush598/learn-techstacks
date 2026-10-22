# Propagation Across Languages

> Part V · Chapter 12 · Sections 12.1–12.9 (practical) · _Estimated reading time: 22 min_
> **Prerequisite:** [Propagation Through Call Stacks](../01-concepts/01-propagation-through-call-stacks.md)

## In one sentence

The same checkout step — *reserve inventory, charge, persist* — propagates errors differently in
TypeScript, Python, Go, and Java, and the correct pattern in each preserves the **cause** while
choosing the **right catch level**.

## Why this matters in production

A team split across languages will produce inconsistent error behavior unless everyone knows how
propagation *actually* works in each runtime. This file walks one scenario end to end in four
languages so you can translate the mental model, not just the syntax.

## Scenario

**Acme SaaS `Checkout`**: a request handler calls a service that reserves inventory, charges the
payment gateway, and persists the order. Inventory is a local DB; the charge is a remote call that
can time out; persistence can hit a unique constraint.

```text
http handler
  └ service.checkout()
      ├ inventory.reserve()   (local DB)
      ├ gateway.charge()      (remote, may timeout)
      └ orders.insert()       (local DB, may conflict)
```

Rules we insist on across all four:

1. Let unexpected errors propagate to the request boundary.
2. Wrap each step with the operation name, preserving the cause.
3. Catch at the **service** level only to translate a transient charge timeout into one retry.
4. The boundary maps to an HTTP response; no internals leak (Chapter 20).

## TypeScript

```ts
class StepFailed extends Error {
  constructor(step: string, cause: unknown) {
    super(`checkout step failed: ${step}`, { cause });
    this.name = "StepFailed";
  }
}

async function checkout(cmd: CheckoutCmd): Promise<Order> {
  await inventory.reserve(cmd.items).catch(e => { throw new StepFailed("reserve inventory", e); });
  await gateway.charge(cmd.payment).catch(e => { throw new StepFailed("charge payment", e); });
  return orders.insert(cmd).catch(e => { throw new StepFailed("persist order", e); });
}

// One retry, only for a transient charge error.
async function checkoutWithRetry(cmd: CheckoutCmd): Promise<Order> {
  try {
    return await checkout(cmd);
  } catch (err) {
    if (err instanceof StepFailed && isTransient(err.cause) && !charged) {
      return await checkout(cmd);
    }
    throw err;
  }
}
```

Note: every `.catch` **throws a new error with the cause** — it wraps rather than swallows.

## Python

```python
class StepFailed(Exception):
    def __init__(self, step: str, cause: BaseException):
        super().__init__(f"checkout step failed: {step}")
        self.step = step
        self.__cause__ = cause  # or use `raise ... from`

async def checkout(cmd: CheckoutCmd) -> Order:
    try:
        await inventory.reserve(cmd.items)
    except Exception as e:
        raise StepFailed("reserve inventory", e) from e
    try:
        await gateway.charge(cmd.payment)
    except TransientGatewayError as e:
        raise StepFailed("charge payment", e) from e
    try:
        return await orders.insert(cmd)
    except Exception as e:
        raise StepFailed("persist order", e) from e
```

`raise ... from e` sets `__cause__`, so `traceback` prints the full "The above exception was the
direct cause of the following exception" chain.

## Go

Go returns errors; there is no throw. Wrap with `%w`, retry by inspecting with `errors.As`.

```go
func (s *Service) Checkout(ctx context.Context, cmd CheckoutCmd) (Order, error) {
    if err := s.inventory.Reserve(ctx, cmd.Items); err != nil {
        return Order{}, fmt.Errorf("reserve inventory: %w", err)
    }
    if err := s.gateway.Charge(ctx, cmd.Payment); err != nil {
        return Order{}, fmt.Errorf("charge payment: %w", err)
    }
    o, err := s.orders.Insert(ctx, cmd)
    if err != nil {
        return Order{}, fmt.Errorf("persist order: %w", err)
    }
    return o, nil
}

func (s *Service) CheckoutWithRetry(ctx context.Context, cmd CheckoutCmd) (Order, error) {
    o, err := s.Checkout(ctx, cmd)
    if err == nil {
        return o, nil
    }
    var gwe *GatewayError
    if errors.As(err, &gwe) && gwe.Transient {
        return s.Checkout(ctx, cmd) // one retry
    }
    return Order{}, err
}
```

## Java

```java
public Order checkout(CheckoutCmd cmd) {
    try {
        inventory.reserve(cmd.items());
    } catch (RuntimeException e) {
        throw new StepFailed("reserve inventory", e);
    }
    try {
        gateway.charge(cmd.payment());
    } catch (RuntimeException e) {
        throw new StepFailed("charge payment", e);
    }
    return orders.insert(cmd);
}

// Checked vs unchecked: keep the cause on both.
static final class StepFailed extends RuntimeException {
    StepFailed(String step, Throwable cause) {
        super("checkout step failed: " + step, cause); // cause preserved
    }
}
```

## What each language guarantees

| Language | Preserve cause with | Retry decision via | Boundary translation |
| -------- | ------------------- | ------------------ | -------------------- |
| TypeScript | `{ cause }` | `instanceof` + inspect | global error middleware |
| Python | `raise … from e` | `except Specific as e` | framework handler |
| Go | `%w` + `errors.As/Is` | `errors.As` | HTTP middleware |
| Java | constructor `cause` | `catch (Subtype e)` | `@ControllerAdvice` |

## Key data / numbers

- **TypeScript/Node**: `Error.cause` is ES2022; `instanceof` works for single-realm errors, use
  a `code`/`name` check across realms.
- **Python**: unhandled exception exits with code `1` and prints the full chain to stderr.
- **Go**: `%w` chains are introspectable; `%v` is not. `errors.Join` for multiple.
- **Java**: checked exceptions must be declared; unchecked propagate freely. Both keep `cause`.

## Real-world use case — Acme SaaS

Acme's services were TS (API), Python (ML summarizer), and Go (billing worker). Each wrapped
differently: TS threw generic errors, Python used `raise X` without `from`, Go used `%v`. On a
gateway outage, the three teams each saw a different, partial picture. They standardized on a
single **error envelope** with `code`, `operation`, and `cause`, and adopted the wrap idioms above
so a chain was readable in every language. Cross-team MTTR improved because everyone could read
the same shape.

## Trade-offs

| Language | Idiom | Ergonomic? | Cause safety |
| -------- | ----- | ---------- | ------------ |
| TS | `{ cause }` | High | Explicit |
| Python | `raise…from` | High | Explicit |
| Go | `%w` | Medium | Easy to forget `%w` |
| Java | ctor `cause` | Medium | Verbose but reliable |
| Rust | `#[source]`/`anyhow` | Medium | Opt-in by derive |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap each step with its operation name | Rethrow a generic `new Error("failed")` |
| Use `%w`/`from e`/`cause` | Use `%v`/plain `raise`/message-only |
| Retry in exactly one owner | Retry at every layer |
| Translate only at the boundary | Leak driver errors to the client |
| Use `errors.As` for typed retry decisions | String-match the error message |

## Common mistakes

- **TS**: `catch (e) { throw new Error(e.message) }` — no `cause`.
- **Python**: `raise X(...)` inside `except` without `from` sets only `__context__` (weaker, and
  may be suppressed by libraries).
- **Go**: `return fmt.Errorf("x: %v", err)` — chain lost.
- **Java**: catching `Exception` before a specific subtype.
- **All four**: catching only to log and rethrow, doubling log volume with no added signal.

## Checklist

- [ ] Every step wrapper names the operation.
- [ ] Cause is preserved in every language.
- [ ] Exactly one layer decides retry.
- [ ] Boundary translation strips internals.
- [ ] The printed chain reads as a sentence top-down.

## Related

- [Preserving Cause — Before/After](./02-preserving-cause-before-after.md)
- [Propagation Through Call Stacks](../01-concepts/01-propagation-through-call-stacks.md)
- [Language-Level Error Semantics (Part XVIII)](../../../part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
- [Standardized API Error Responses (Part VIII)](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
