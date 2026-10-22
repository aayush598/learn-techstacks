# Code-Level Boundaries: Function, Module, and Domain

> Part VI · Chapter 15 · Sections 15.3–15.5 · _Estimated reading time: 16 min_
> **Prerequisite:** [What an Error Boundary Is](./01-what-error-boundaries-are.md)

## In one sentence

The three innermost boundaries — **function** (a local fallback), **module** (a stable public
contract), and **domain** (a business decision) — are about keeping failure *local* and keeping
infrastructure *out of the domain*.

## Why this matters in production

Most leaked SQL, most swallowed bugs, and most coupled code start at these three levels. A function
that catches too broadly hides a defect; a module that lets its implementation exception escape
freezes its API; a domain that catches a driver error has imported a database it should not know
exists. Getting these right makes the outer boundaries trivial.

## 15.3 — Function-level boundaries

A function-level boundary is a `try/catch` (or `Result` match) **inside one function**, where the
function can substitute a safe value or convert one specific error. It is the narrowest boundary
and the easiest to abuse.

**When it is legitimate:**

- A pure helper with a well-defined fallback (`parseIntSafe` returns `null` on `NaN`).
- A single specific, expected error that the function can absorb (`ENOENT` → treat as "not
  cached").
- Converting a mechanism error into a value at a leaf (`Number()` → `NaN`).

**When it is a mistake:**

- Catching everything to "be safe" — this is the silent swallow.
- Catching an error the caller needs to see (a failed DB write inside a helper).

```ts
// ✅ Legitimate function boundary: a specific, expected failure with a safe fallback.
function parseTimeout(raw: string | undefined, fallbackMs = 5_000): number {
  const n = Number(raw);
  return Number.isFinite(n) && n > 0 ? n : fallbackMs; // bad config → safe default
}

// ❌ Abusive function boundary: swallows a write failure the caller must know about.
async function saveUser(user: User) {
  try {
    await db.insert(user);
  } catch {
    /* ignore */ // bug is now invisible; caller thinks the user was saved
  }
}
```

Rule of thumb: **a function boundary must name the exact error it handles and provide a default
that is safe for every caller.** If the default depends on caller context, the boundary belongs
higher.

## 15.4 — Module-level boundaries

A module (a package, a repository, an SDK wrapper) presents a **public contract**. Everything
inside is an implementation detail. A module boundary ensures the module's exceptions are declared
by the contract — never a leaked `node:fs`, driver, or vendor error.

Think of the module as a small system: its public functions speak the module's error vocabulary;
its internals may speak anything, but they are translated at the edge.

```python
# repository module — public contract is DomainError; driver errors never escape
class UserRepository:
    def create(self, email: str) -> User:
        try:
            row = self._db.execute("insert into users(email) values(%s) returning id", (email,))
        except psycopg2.errors.UniqueViolation as e:
            # module boundary: translate + preserve cause
            raise DomainError("EMAIL_ALREADY_USED", cause=e) from e
        except psycopg2.OperationalError as e:
            raise InfrastructureError("DB_UNAVAILABLE", transient=True, cause=e) from e
        return User(id=row["id"], email=email)
```

Characteristics of a good module boundary:

| Property | Meaning |
| -------- | ------- |
| **Closed vocabulary** | Callers only ever see errors the module documents |
| **Cause preserved** | Internal error attached, not discarded |
| **No infra types in signature** | No `SQLException`, `pg.errors`, no HTTP status |
| **Stable across rewrites** | Swapping the DB does not change what callers catch |

The module boundary is the single most important one to get right for **replaceability**: if the
repository leaks `psycopg2` errors, you cannot switch to `asyncpg` without touching every caller.

```go
// Go module boundary: return only sentinel/typed errors declared by the package.
var (
    ErrEmailTaken = errors.New("email already used")
    ErrUnavailable = errors.New("user store unavailable")
)

func (r *UserRepo) Create(ctx context.Context, email string) (User, error) {
    var u User
    err := r.insert(ctx, email, &u)
    var pgErr *pgconn.PgError
    if errors.As(err, &pgErr) {
        switch pgErr.Code {
        case "23505": // unique_violation
            return User{}, fmt.Errorf("%w: %v", ErrEmailTaken, pgErr) // %w preserves cause
        case "53300", "08006": // too_many_connections, connection_failure
            return User{}, fmt.Errorf("%w: %v", ErrUnavailable, pgErr)
        }
    }
    if err != nil {
        return User{}, err
    }
    return u, nil
}
```

## 15.5 — Domain-level boundaries

A domain boundary is where the **business decision** lives: accept this outcome as a valid result,
or reject it as a rule violation. The domain owns meaning; it must not own infrastructure.

Two legitimate domain boundary styles:

1. **Throw a typed domain error** — when the outcome is exceptional to the caller.
2. **Return a `Result`** — when the outcome is an expected alternative the caller handles inline
   (see Part III and Ch. 18).

```ts
// Domain boundary: the rule lives here; no DB, no HTTP, no vendor types.
export class Subscription {
  constructor(
    private plan: Plan,
    private seatsInUse: number,
  ) {}

  addSeats(requested: number): void {
    const total = this.seatsInUse + requested;
    if (total > this.plan.maxSeats) {
      // business decision, thrown as a typed domain error
      throw new DomainError("SEAT_LIMIT_EXCEEDED", {
        details: { requested, available: this.plan.maxSeats - this.seatsInUse },
      });
    }
    this.seatsInUse = total;
  }
}
```

What must **never** appear in a domain boundary:

- A `SQLSTATE`, `errno`, HTTP status, or vendor string.
- A `try/catch` around I/O (the domain does not perform I/O).
- A fallback that hides a rule violation.

The domain boundary *decides*; the repository boundary *translates*; the request boundary
*exposes*. Keep them separate.

## Choosing among the three

```text
Is the fallback safe for ALL callers?        → function boundary
Is this the public edge of a module/package? → module boundary
Is this a business rule / invariant?         → domain boundary
Otherwise                                    → do not catch; propagate
```

## Key data / numbers

- Python DBAPI hierarchy: `UniqueViolation` is a subclass of `IntegrityError`; catching the base
  class `IntegrityError` collapses distinct constraint failures — prefer the specific class.
- Go: `errors.Is(err, ErrEmailTaken)` works only if the module used `%w`; a plain `fmt.Errorf`
  with `%v` breaks the chain.
- TypeScript: `Error.cause` (ES2022) is the standard way to preserve the module-internal error.

## Real-world use case — ExportJob

`ExportJob` has a `StorageModule` that writes chunks to S3. The module boundary catches S3's
`SlowDown` (HTTP `503`) and `RequestTimeout` and translates them to
`TransientStorageError`, while `AccessDenied` becomes `PermanentStorageError`. The job runner
(retry boundary, Ch. 32) only needs to check `isTransient(err)` — it never imports the AWS SDK.
When the team later adds a GCS backend, no caller changes: the new module simply maps GCS `503`
responses to the same `TransientStorageError`.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the exact error a function boundary handles | Catch-all "just in case" at every function |
| Translate to the module's documented errors at its edge | Let driver/vendor errors escape a module |
| Keep business decisions in the domain | Put `try/catch` around I/O in the domain |
| Use `%w` / `Error.cause` / `raise from` | String-concatenate and lose the chain |

## Common mistakes

- **Catching `IntegrityError` instead of `UniqueViolation`** — maps FK and not-null failures to
  "duplicate," confusing users.
- **Returning `nil, nil` from a module** to signal "not found," which callers interpret as success.
- **Domain importing a repository type** to distinguish errors it should never have seen.

## Checklist

- [ ] Every function-level catch names a specific error and a safe default.
- [ ] Each module documents its error vocabulary and only emits it.
- [ ] No driver/vendor type appears in a module's public signature.
- [ ] Domain boundaries contain no I/O and no infrastructure types.
- [ ] Error chains are preserved with native mechanisms.

## Related

- [What an Error Boundary Is](./01-what-error-boundaries-are.md)
- [Runtime Boundaries](./03-runtime-boundaries.md)
- [Part III — Error Classes, Types, and Structured Results](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
