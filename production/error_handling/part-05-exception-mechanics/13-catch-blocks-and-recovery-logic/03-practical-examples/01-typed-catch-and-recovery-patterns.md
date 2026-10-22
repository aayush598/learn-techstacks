# Typed Catch and Recovery Patterns

> Part V · Chapter 13 · Sections 13.3–13.8 (practical) · _Estimated reading time: 22 min_
> **Prerequisite:** [Recovery Inside Catch](../01-concepts/03-recovery-inside-catch.md)

## In one sentence

This file shows the same recovery decision — *handle a specific error, retry a transient one,
translate a domain one, rethrow the unknown* — implemented idiomatically in TypeScript, Python, Go,
and Java.

## Why this matters in production

Teams often know the *idea* of typed catches but write them ad hoc, producing inconsistent recovery
across services. Here is one realistic scenario implemented four ways, so you can copy the shape
into whichever runtime you maintain.

## Scenario

**Acme SaaS `WebhookIngest`** processes inbound Stripe events. For each event:

1. Verify the signature (local; can fail with `SignatureError`).
2. Reject duplicates (local DB unique constraint; `DuplicateError`).
3. Apply the event (calls a downstream service; can be `TransientError` or `PermanentError`).

Policy:
- `SignatureError` → **reject** (`400`), never retry, log as a potential attack.
- `DuplicateError` → **idempotent ack** (`200`), not an error.
- `TransientError` → **retry** with bounded backoff.
- `PermanentError` → **reject** (`422`), no retry.
- Anything else → **log + rethrow** (Stripe will retry the webhook).

## TypeScript

```ts
type Outcome = { status: 200 } | { status: 400 | 422 };

async function ingest(raw: Buffer, sig: string): Promise<Outcome> {
  try {
    verifySignature(raw, sig);
  } catch (err) {
    logger.warn({ err, len: raw.length }, "signature verification failed");
    return { status: 400 };                            // reject, do not retry
  }

  let event: StripeEvent;
  try {
    event = parseEvent(raw);
  } catch (err) {
    throw new WebhookParseError("malformed stripe payload", { cause: err }); // unknown → rethrow
  }

  try {
    await applyEvent(event);
    return { status: 200 };
  } catch (err) {
    if (err instanceof DuplicateError) return { status: 200 };   // idempotent success
    if (err instanceof TransientError) return retryApply(event); // bounded
    if (err instanceof PermanentError) return { status: 422 };   // reject
    logger.error({ err, eventId: event.id }, "unhandled webhook error");
    throw err;                                                    // let the boundary 500
  }
}
```

## Python

```python
def ingest(raw: bytes, sig: str) -> Outcome:
    try:
        verify_signature(raw, sig)
    except SignatureError as err:
        logger.warning("signature verification failed: %s", err)
        return Outcome(status=400)

    try:
        event = parse_event(raw)
    except ValueError as err:
        raise WebhookParseError("malformed stripe payload") from err   # unknown → rethrow

    try:
        apply_event(event)
        return Outcome(status=200)
    except DuplicateError:
        return Outcome(status=200)          # idempotent ack
    except TransientError:
        return retry_apply(event)           # bounded with deadline
    except PermanentError:
        return Outcome(status=422)
    except Exception as err:                # unknown — not a bare except
        logger.exception("unhandled webhook error for %s", event.id)
        raise                               # re-raise original, chain intact
```

## Go

Go has no catch; the recovery decision is explicit branching on returned errors.

```go
func Ingest(raw []byte, sig string) (Outcome, error) {
    if err := VerifySignature(raw, sig); err != nil {
        log.Warn("signature verification failed", "err", err)
        return Outcome{Status: 400}, nil
    }

    event, err := ParseEvent(raw)
    if err != nil {
        return Outcome{}, fmt.Errorf("malformed stripe payload: %w", err)
    }

    if err := ApplyEvent(event); err != nil {
        switch {
        case errors.Is(err, ErrDuplicate):
            return Outcome{Status: 200}, nil
        case errors.Is(err, ErrTransient):
            return retryApply(event) // bounded, deadline-aware
        case errors.Is(err, ErrPermanent):
            return Outcome{Status: 422}, nil
        default:
            log.Error("unhandled webhook error", "eventID", event.ID, "err", err)
            return Outcome{}, err // → boundary returns 500, Stripe retries
        }
    }
    return Outcome{Status: 200}, nil
}
```

## Java

```java
public Outcome ingest(byte[] raw, String sig) {
    try {
        verifySignature(raw, sig);
    } catch (SignatureException e) {
        log.warn("signature verification failed", e);
        return Outcome.of(400);
    }

    StripeEvent event;
    try {
        event = parseEvent(raw);
    } catch (JsonProcessingException e) {
        throw new WebhookParseException("malformed stripe payload", e); // unknown → rethrow
    }

    try {
        applyEvent(event);
        return Outcome.of(200);
    } catch (DuplicateException e) {
        return Outcome.of(200);
    } catch (TransientException e) {
        return retryApply(event);                    // bounded
    } catch (PermanentException e) {
        return Outcome.of(422);
    } catch (RuntimeException e) {                    // unknown — specific supertype, not Error
        log.error("unhandled webhook error for {}", event.id(), e);
        throw e;
    }
}
```

## Comparison

| Decision | TS | Python | Go | Java |
| -------- | -- | ------ | -- | ---- |
| Specific catch | `instanceof` | `except T` | `errors.Is` | `catch (T)` |
| Unknown branch | rethrow | `except Exception: raise` | `default: return err` | `catch (RuntimeException)` |
| Idempotent ack | return 200 | return 200 | return 200 | return 200 |
| Wrap cause | `{ cause }` | `raise … from` | `%w` | ctor cause |
| Bounded retry | loop | loop | loop | loop |

## Key data / numbers

- **Stripe webhooks**: return `2xx` to acknowledge, `4xx` for permanent rejection, `5xx` to have
  Stripe retry. Stripe retries with exponential backoff over up to ~3 days.
- **Signature mismatch** must never return `2xx` — acknowledging unverified events is a security
  bug.
- **Duplicate events** are normal with at-least-once delivery; ack them idempotently.
- **Retry budget**: bound by attempts *and* a deadline; a webhook handler should respond quickly.

## Real-world use case — Acme SaaS

Acme originally returned `200` for all outcomes to "keep Stripe quiet", which acknowledged
signature failures and lost retries for transient downstream outages. After splitting by type as
above, security-relevant rejections returned `400`, transient failures propagated as `5xx` so
Stripe retried, and duplicates were acked. Billing-state drift incidents dropped sharply.

## Trade-offs

| Choice | Pros | Cons | When |
| ------ | ---- | ---- | ---- |
| Translate locally to Outcome | Handler stays small | Must map every known type | Stable, small error set |
| Throw to a global handler | Central mapping | Coarse per-request policy | Uniform APIs |
| Retry in the handler | Immediate recovery | Ties up the request | Fast transient blips |
| Queue for retry | Durable, decoupled | More infrastructure | Long/unreliable work |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reject signature failures with 4xx | Return 200 for unverified events |
| Ack duplicates idempotently | Treat duplicates as errors |
| Rethrow the unknown | Swallow it to "keep the provider quiet" |
| Bound retries with a deadline | Retry inside the request forever |
| Preserve cause in every wrap | Rethrow a fresh generic error |

## Common mistakes

- **Ack-everything** to avoid provider retries — hides real failures and security issues.
- **Bare `except:`/`catch (Exception)`** — also catches cancellation and bugs.
- **Retrying a `422`/`400`** — permanent; wastes quota and delays the real fix.
- **Not preserving the parser error** — malformed-payload incidents become undiagnosable.

## Checklist

- [ ] Signature failure → 4xx, never acknowledged.
- [ ] Duplicate → idempotent 2xx.
- [ ] Transient → bounded retry/degrade.
- [ ] Unknown → log + rethrow (boundary 5xx).
- [ ] Cause preserved in every language.

## Related

- [Recovery Preconditions and State Guards](./02-recovery-preconditions-and-state-guards.md)
- [Typed Handlers and Error Discrimination](../02-deep-dive/01-typed-handlers-and-discrimination.md)
- [Events, Webhooks, and Message Processing (Part XII)](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- [HTTP Error Semantics (Part VIII)](../../../part-08-http-and-api/19-http-error-semantics/README.md)
