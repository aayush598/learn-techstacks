# Chapter 8 — Reference

> Part III · Chapter 8 · Cheat sheet, decision tables, and glossary.

## Cheat sheet — code anatomy

```text
<DOMAIN>[_<OBJECT>]_<REASON>      SCREAMING_SNAKE_CASE, ≤ 64 chars
PAYMENT_CARD_DECLINED             domain + object + reason
DB_UNIQUE_VIOLATION               behavior, not SQLSTATE
EXPORT_STORAGE_UNAVAILABLE        object disambiguates within domain
```

## Cheat sheet — registry row

```text
code · domain · category · http · retryable · visibility(public|internal)
     · publicAlias · clientAction · messageKey · description · owner · since · deprecated?
```

## Cheat sheet — one code, five mappings

```text
code ──┬─▶ http          503
       ├─▶ retryable     true  (max attempts from category)
       ├─▶ clientAction  retry
       ├─▶ messageKey    errors.payment.providerTimeout
       └─▶ alias         SERVICE_UNAVAILABLE   (if internal)
```

## Decision table — HTTP by category

| Category | Default | Common override |
| -------- | ------- | --------------- |
| validation | 422 | 400 malformed, 413 too large |
| auth | 401/403 | 402 entitlement |
| business | 409 | 404 not found, 402 |
| payment | 402 | 429 provider rate limit |
| database | 503 | 409 unique violation |
| external | 502 | 504 upstream timeout |
| resource | 429 | 503 maintenance |
| unexpected | 500 | — |

## Decision table — client action

| Action | User can… | Typical codes |
| ------ | --------- | ------------- |
| `retry` | wait and try again | `*_TIMEOUT`, `RATE_LIMIT_EXCEEDED` |
| `reauthenticate` | log in again | `AUTH_SESSION_EXPIRED` |
| `fix_input` | correct fields | `VALIDATION_*` |
| `choose_alternative` | pick another option | `PAYMENT_CARD_DECLINED`, `USER_EMAIL_TAKEN` |
| `contact_support` | nothing self-service | `INTERNAL_*`, `*_INVARIANT` |
| `none` | nothing (informational) | `EXPORT_EMPTY`, `WEBHOOK_DUPLICATE_EVENT` |

## Decision table — change type → compatibility

| Change | Safe? | Do this |
| ------ | ----- | ------- |
| Add a code | ✅ | Ensure consumers fall back on unknown |
| Change message text | ✅ | Nothing (messages are not contract) |
| Rename a code | ❌ | Alias + dual-emit window |
| Change a code's HTTP | ❌ | New code |
| Change a code's meaning | ❌ | New code |
| Remove a code | ❌ | Retire → telemetry → remove |

## Decision table — scope structure

| Team size / codes | Structure |
| ----------------- | --------- |
| Small, < 300 codes | Centralized registry module |
| Many teams/domains | Domain-owned slices + central merge |
| Public/partner codes | Add product prefix; versioned contract |

## Naming quick rules

```text
prefix  := reserved domain (VALIDATION, AUTH, USER, BILLING, PAYMENT, DB,
           EXPORT, WEBHOOK, AGENT, RATE, SYSTEM, INTERNAL)
reason  := state/verb: _DECLINED _TIMEOUT _TAKEN _EXCEEDED _INVALID
           _NOT_FOUND _CONFLICT _UNAVAILABLE _EXPIRED
never   := SQLSTATE, vendor codes, line numbers, per-occurrence IDs, sentences
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Error code | Stable machine-readable identifier for a condition |
| Error registry | Single source of truth mapping codes to behavior |
| Reserved domain | Registry-owned code prefix |
| Visibility | public (client-safe) or internal |
| Public alias | Code shown to clients in place of an internal code |
| Client action | What a client should do for a code |
| Message key | i18n key for the user-facing message |
| Coverage table | `Record<ErrorCode, T>` forcing complete mapping |
| Dual emission | Emitting old and new codes during a rename window |
| Alias map | Old code → canonical code on input |
| Undocumented code | A code produced but absent from the registry |
| Deprecation window | Period a code stays working before removal |

## Standard references (by name, no links)

- **RFC 9457 Problem Details** — `type` URI often carries the code.
- **gRPC status codes** — stable, small; a model for behavior-derived naming.
- **PostgreSQL SQLSTATE** — `23505` unique_violation, `40001` serialization_failure,
  `40P01` deadlock_detected (translate, never expose).
- **Stripe decline codes** — `card_declined`, `insufficient_funds` (map to your own codes).

## Signposts

- HTTP status semantics → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- API error responses → [Ch. 20](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- Contract versioning → [Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)

## Related

- [Chapter 8 Do's and Don'ts](../04-dos-and-donts/README.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
- [Chapter 8 Overview](../README.md)
