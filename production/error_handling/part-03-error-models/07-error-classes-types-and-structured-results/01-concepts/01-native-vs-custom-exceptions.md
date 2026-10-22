# Native vs Custom Exceptions

> Part III · Chapter 7 · Sections 7.1–7.6 · _Estimated reading time: 18 min_
> **Prerequisite:** [What an Error Object Represents](../../06-designing-the-applications-error-model/01-concepts/01-what-an-error-object-represents.md)

## In one sentence

Use **native errors only at the edge** where you immediately translate them, and **custom error
classes at the layers that own meaning** — domain, infrastructure, application — so each layer
speaks its own vocabulary and never leaks another layer's.

## Why this matters in production

If infrastructure detail leaks into the domain (`PostgresError: duplicate key value violates...`
reaching business logic), then a database swap becomes a domain rewrite, and business rules depend
on vendor quirks. If everything is one giant `AppError`, then a type check cannot tell a validation
failure from an outage. Layer-specific classes keep the layers decoupled and make handling
precise.

## Native vs custom (7.1)

| Aspect | Native (`Error`, `TypeError`, `RangeError`, …) | Custom (`PaymentError`, `NotFoundError`, …) |
| ------ | ---------------------------------------------- | ------------------------------------------- |
| Origin | Language/runtime | Your application |
| Meaning | "A JS thing went wrong" | "This specific condition occurred" |
| Carries a code | No | Yes (the model's `code`) |
| `instanceof` useful | Rarely | Yes, for category checks |
| Best used | At edges, immediately wrapped | Everywhere meaning exists |

Native errors are not "bad" — they are the **raw material**. You catch them and translate.

```ts
try {
  JSON.parse(body);                 // native SyntaxError possible
} catch (native) {
  throw new ValidationError("VALIDATION_MALFORMED_BODY", "Body is not valid JSON", {
    cause: native,
  });
}
```

## When to create a custom class (7.2)

Create a class when **all** of the following hold:

1. The condition has a **stable code** in the registry.
2. Callers will **branch on it** (a type check or a code switch changes behavior).
3. It belongs to a **layer** with a distinct vocabulary.
4. Handling it collectively (e.g. "all `ValidationError`s") is useful.

Do **not** create a class when:

- The condition is one-off and handled once at the edge.
- Two classes would differ only by message.
- It is a native condition you are about to wrap anyway.

> ⚠️ **Hazard.** A class per message is a classic anti-pattern: hundreds of near-identical types
> that no `instanceof` ever uses. If the only difference is *text*, use one class and a different
> **code**.

## Layer-specific classes (7.3–7.5)

Each layer has its own error vocabulary, and **classes define the boundary**.

### Domain-specific (7.3)

Domain classes express invariants and business rules. They must not depend on frameworks or
infrastructure.

```ts
class InsufficientBalanceError extends AppError {
  constructor(accountId: string, shortfall: Money) {
    super({
      code: "BILLING_INSUFFICIENT_BALANCE",
      category: "business",
      message: `Account ${accountId} is short by ${shortfall.format()}`,
      metadata: { accountId, shortfall: shortfall.amount, currency: shortfall.currency },
    });
  }
}
```

### Infrastructure-specific (7.4)

Infrastructure classes wrap driver/vendor errors and stay **inside** the adapter. They are the
translation source, not the exported type.

```ts
class RepositoryError extends AppError {
  constructor(code: string, message: string, cause: unknown, meta?: Record<string, unknown>) {
    super({ code, category: "database", message, cause, metadata: meta });
  }
}
```

### Application-level (7.5)

Application-service errors express orchestration failures: a saga step failed, a workflow
precondition was not met. They are the layer most likely to be consumed by transport handlers.

```ts
class CheckoutFailedError extends AppError {
  constructor(step: string, cause: unknown) {
    super({
      code: "CHECKOUT_STEP_FAILED",
      category: "payment",
      message: `Checkout failed during ${step}`,
      cause,
      metadata: { step },
      operation: "checkout",
    });
  }
}
```

## Framework exceptions (7.6)

Frameworks ship their own hierarchies (`HttpException`, `NotFoundException`, `ValidationException`,
ORM exceptions, queue exceptions). Two rules:

1. **Treat framework exceptions as foreign input.** Translate them at the framework boundary into
   your model; never let them be your domain vocabulary.
2. **Do not extend them across layers.** A domain error should not inherit from an HTTP framework
   class, or the domain now depends on the transport.

```ts
// Adapter: translate framework exception → application error.
function fromHttpException(e: HttpException): AppError {
  if (e.status === 404) return new NotFoundError("RESOURCE_NOT_FOUND", e.message);
  if (e.status === 409) return new ConflictError("RESOURCE_CONFLICT", e.message);
  return toErrorObject(e);
}
```

## Worked example

```ts
// A repository adapter keeps DB detail contained.
class UserRepository {
  constructor(private readonly db: Pool) {}

  async findById(id: string): Promise<User | null> {
    try {
      const { rows } = await this.db.query("SELECT * FROM users WHERE id = $1", [id]);
      return rows[0] ? mapUser(rows[0]) : null;
    } catch (native) {
      // Native pg error → infrastructure class. Callers never see SQLSTATE.
      throw new RepositoryError(
        "DB_QUERY_FAILED",
        `User lookup failed for id ${id}`,
        native,
        { table: "users" },
      );
    }
  }
}
```

The domain calls `findById`; it sees a `RepositoryError` (or `null`), never a `pg` error. If the
database changes, only this adapter changes.

## Key data / numbers

- **`instanceof` works across `Error` subclasses** in a single realm; across worker/iframe
  boundaries it does not — rely on `code`, not `instanceof`, at those boundaries.
- **`Error.captureStackTrace`** (V8) trims internal frames from the stack.
- **PostgreSQL SQLSTATE** classes are 2 characters (e.g. `23` integrity constraint, `40`
  transaction rollback); full codes are 5 (e.g. `23505` unique_violation, `40001`
  serialization_failure) — translate these, never expose them.
- **HTTP framework status codes** are a transport concern; do not bake them into domain classes.

## Real-world use case — Acme SaaS

Acme's billing domain originally threw raw `pg` errors and framework `HttpException`s. A database
migration renamed a column, and the domain—keying on `e.message.includes("column")`—started
treating a schema error as a validation error, returning `422` for a genuine `500` and retrying a
permanent failure. Introducing `InsufficientBalanceError`, `PaymentError`, and a
`RepositoryError` that wraps all driver errors fixed it: the domain branches on types and codes,
the repository owns SQL, and the transport layer maps codes to HTTP. The migration touched one
adapter.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Native only, wrap at edge | Minimal types | No layer vocabulary | Tiny services |
| One `AppError` + codes | Simple, flat | No `instanceof` distinction | Most teams |
| Class per layer/category | Precise checks | Slightly more code | Layered/domain-rich apps |
| Class per message | "Specific" | Explodes, unusable | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap natives immediately at the edge | Let driver errors reach the domain |
| Give each layer a small error vocabulary | Extend framework exceptions in the domain |
| Differentiate by `code`, not by class-per-message | Create a class for every message |
| Translate framework exceptions at the boundary | Leak `HttpException` into business logic |

## Common mistakes

- **Class explosion** — one type per message; no `instanceof` ever uses them.
- **Domain extends framework** — coupling business rules to HTTP/ORM.
- **`instanceof` across realms** — fails silently in workers/iframes; use `code`.
- **No infrastructure class** — SQLSTATE strings reach business logic.

## Checklist

- [ ] Are natives always wrapped before crossing a layer?
- [ ] Does each layer have a small, purposeful error vocabulary?
- [ ] Are classes justified by code + branching, not by message?
- [ ] Are framework exceptions translated at the boundary?
- [ ] Do domain classes avoid framework/infrastructure imports?

## Related

- [Typed vs Untyped and Union Types](./02-typed-vs-untyped-and-unions.md)
- [Hierarchies, Composition, and Naming](./05-hierarchies-composition-and-naming.md)
- [Custom Error Class Design in Practice](../03-practical-examples/02-custom-error-class-design.md)
