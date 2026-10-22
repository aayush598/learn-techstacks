# Catching Specific Types and Categories

> Part V · Chapter 13 · Sections 13.3, 13.4, 13.5 · _Estimated reading time: 16 min_
> _Prerequisite:_ [When to Catch and When Not To](./01-when-to-catch-and-when-not.md)

## In one sentence

Catch the **narrowest type you can handle**, handle several known categories explicitly, and treat
everything else as **unknown** — log it with context and rethrow, never absorb it.

## Why this matters in production

A `catch (Exception e)` or `catch (e)` intercepts programming bugs, cancellation, and infrastructure
failures with the same "handling" as an expected business error. The bug is then never fixed, the
cancellation is ignored (work continues after the user left), and the outage is logged as a warning.
Specific catches make the *set of handled outcomes* an explicit contract.

## Core concept

Three tiers of error come toward a catch block:

| Tier | Examples | Posture |
| ---- | -------- | ------- |
| **Known, expected** | Validation, not-found, conflict, declined card | Handle explicitly |
| **Known, transient** | Timeout, `503`, deadlock, serialization failure | Retry per policy (Ch. 27) |
| **Unknown** | Programming bugs, new/unmodeled conditions | Log + rethrow, never swallow |

### Catching specific types (13.3)

```text
try { ... }
catch (NotFound)         → return 404 / null-result
catch (Conflict)         → return 409 / surface to user
catch (TransientError)   → retry
catch (e)                → log unknown with context, RETHROW
```

### Multiple categories (13.4)

Group errors by **what you will do**, not by which module raised them. Categories that share a
policy can share a handler; categories that differ must not. Order handlers most-specific first.

| Category grouping | Shared handling |
| ----------------- | --------------- |
| `{ Validation, Parse }` | Return field-level 4xx |
| `{ Timeout, Unavailable }` | Retry / degrade |
| `{ NotFound }` | Return empty/404 |
| `{ Permission, Auth }` | 401/403, no retry |

### Known vs unknown (13.5)

The unknown branch is **mandatory** and must **rethrow**. Its job is to record that something
unmodeled happened, with enough context to triage — not to make the error go away.

## How it works (mechanics)

Languages express specificity differently:

- **Java**: `catch` clauses are ordered; the compiler rejects an unreachable subtype after a
  supertype.
- **JS/TS**: first matching `catch`/`.catch` wins; order is manual. Use `instanceof` or a `code`
  field. `instanceof` can fail across realms/duplicated module copies — prefer a `code`.
- **Python**: `except` clauses are ordered; a bare `except:` catches *everything including
  `KeyboardInterrupt` and `SystemExit`* — avoid; use `except Exception`.
- **Go**: no exceptions; use `errors.Is`/`errors.As` on wrapped errors to discriminate.
- **Rust**: `match` on an enum is exhaustive — the compiler forces you to name the unknown.

```text
most specific ─────────────────────────────────▶ least specific
NotFound → Conflict → Transient → Unknown(Error/Exception) → (bare catch: ❌)
```

## Worked example

```ts
class NotFoundError extends Error { readonly code = "NOT_FOUND"; }
class ConflictError extends Error { readonly code = "CONFLICT"; }
class TransientError extends Error { readonly code = "TRANSIENT"; }

async function updateProject(id: string, patch: Patch): Promise<Result> {
  try {
    return { ok: true, value: await repo.update(id, patch) };
  } catch (err) {
    if (err instanceof NotFoundError) return { ok: false, reason: "not_found" };
    if (err instanceof ConflictError) return { ok: false, reason: "version_conflict" };
    if (err instanceof TransientError) throw err; // let a retry owner handle it
    logger.error({ err, id }, "unexpected error updating project");
    throw err; // ← unknown: never absorb
  }
}
```

Go discrimination through wraps:

```go
switch {
case errors.Is(err, ErrNotFound):
    return Result{}, nil
case errors.Is(err, ErrConflict):
    return Result{}, ErrConflict
default:
    return Result{}, fmt.Errorf("update project %s: %w", id, err) // rewrap, keep chain
}
```

Python — note the `except Exception`, not a bare `except`:

```python
try:
    return repo.update(pid, patch)
except NotFoundError:
    return None
except ConflictError:
    raise
except TransientError:
    raise
except Exception as e:            # unknown
    logger.exception("unexpected error updating project %s", pid)
    raise                          # re-raise original, chain intact
```

## Key data / numbers

- **Python**: a bare `except:` also catches `KeyboardInterrupt` and `SystemExit`; use
  `except Exception` and let those propagate.
- **Java**: subtype-after-supertype in a `try` is a compile error for *reachable* checked types;
  it silently hides logic bugs for unchecked.
- **JS**: `Error` subclasses from different realm/module instances fail `instanceof`; prefer a
  stable `code` string for cross-boundary discrimination.
- **Go**: `errors.Is` follows `%w` chains; add `errors.As` for typed inspection.
- **Rust**: exhaustive `match` prevents the unknown branch from being forgotten.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` had a single `catch (e)` that returned `200` for everything to "avoid
Stripe retries". This swallowed signature-verification failures (a security issue), duplicate-key
errors (expected), and a genuine parser bug (unknown). They split the catch: `SignatureError` →
`400` (never acknowledge unverified events), `DuplicateError` → `200` (idempotent), and everything
else → log + `500` so Stripe retries. Security posture and correctness both improved.

## Trade-offs

| Approach | Pros | Cons | When |
| -------- | ---- | ---- | ---- |
| One broad catch | Short | Hides bugs; wrong policy | Never for mixed error sets |
| Explicit per-type | Precise policies | More code | Most production paths |
| Category handlers | Balanced | Needs category design (Ch.4) | Layered services |
| `code`-based (vs `instanceof`) | Cross-realm safe | Stringtypos possible | Serialized/multi-realm errors |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Order most-specific first | Catch `Exception`/`Error` first |
| Handle known categories by policy | Group unrelated errors to save lines |
| Keep an unknown branch that rethrows | Absorb unknown errors |
| Prefer stable `code` across boundaries | Rely on `instanceof` across realms |
| Use `except Exception` (not bare `except`) | Use a bare `except:`/`catch {}` |

## Common mistakes

- **Broad catch above specific ones** — later handlers are dead code.
- **No unknown branch** — a bare `catch` pretends coverage; instead rethrow explicitly.
- **Grouping by module** instead of by policy — a `DBError` category mixes transient and permanent.
- **String matching messages** to discriminate — messages change; codes do not.

## Checklist

- [ ] Catches are ordered most-specific first.
- [ ] Each group shares one policy.
- [ ] An explicit unknown branch logs and rethrows.
- [ ] Discrimination uses stable codes where errors cross boundaries.
- [ ] No bare `except:` / `catch {}`.

## Related

- [When to Catch and When Not To](./01-when-to-catch-and-when-not.md)
- [Recovery Inside Catch](./03-recovery-inside-catch.md)
- [Error Classes, Types, and Structured Results (Part III)](../../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [Error-Handling Patterns and Anti-Patterns (Part XVII)](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
