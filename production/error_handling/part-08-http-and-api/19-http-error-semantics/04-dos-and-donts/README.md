# Chapter 19 — Do's and Don'ts

> Part VIII · Chapter 19 · All sections

A condensed rule set distilled from the chapter. Use it as a review checklist for any PR that
touches an HTTP response.

## Status selection

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Select status from the registry/table, never handler literals | Write `res.status(500)` as a default |
| Keep `4xx` for anything the client can fix | Classify user mistakes as `5xx` |
| Reserve `500` for genuinely unexpected conditions | Map dependency outages to `500` |
| Return `503` + `Retry-After` for known temporary unavailability | Return `500` during maintenance/breaker-open |
| Ask the ordered drill: credentials → permission → parse → semantics | Decide from the exception class name alone |

## The fine-grained pairs

| ✅ Do | ❌ Don't |
| ----- | -------- |
| `400` for unparseable syntax; `422` for semantic/validation failures | Return `400` for business-rule violations |
| `401` (+`WWW-Authenticate`) for credential failures | Return `403` for expired tokens |
| `403` for authenticated-but-forbidden | Return `401` to mask authz bugs |
| `404` consistently for hidden/nonexistent resources | Alternate `403`/`404` for the same resource class |
| `405` + `Allow` for wrong method on routable paths | Return `404` for wrong methods |
| `409` for state conflicts (version clash, concurrent edit) | Return `422` when the world changed under the client |
| `410` for permanent, known removals | Return `404` for expired resources clients once held |
| `413` before buffering; `415` before parsing | Parse first, check size/type later |

## Headers and retry semantics

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach `Retry-After` (seconds) to every `429` and `503` | Return bare `429`/`503` and let clients guess |
| Rate-limit per identity (key/tenant) before global/IP | Let one tenant exhaust a global limit |
| Keep edge timeouts longer than app deadlines | Let the gateway cut first and erase your taxonomy |
| Emit `ETag`/current state alongside `409` | Return `409` with no way to re-apply |
| Mark only `429`/`503` (and edge `502`/`504`) retryable in the registry | Let clients retry `400`/`404`/`422` |

## Honesty and disclosure

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return error statuses whenever SDKs should enter error paths | Return `200` + `{ok:false}` for failures |
| Keep status and `detail` telling one story | `404` whose detail says "permission denied" |
| Project internal errors through the registry before serializing | Serialize raw `Error`/ORM/SQL messages |
| Keep stack traces, SQL, hostnames, vendor names server-side | Echo them in 4xx "for debugging" |
| Escape and truncate reflected input in messages | Reflect raw request bytes |

## Anti-patterns in the wild

1. **The Universal 500** — one status for every failure; alerts cry wolf and SDKs retry bugs.
2. **The Success-Shaped Failure** — `200` with an error body; monitors, caches, and SDK error
   paths all go blind.
3. **The Schema Oracle** — `403` on an ID that returned `404` yesterday; existence confirmed
   to exactly the wrong caller.
4. **The Bare 429** — rate limit without `Retry-After`; a thundering herd in slow motion.
5. **The Debugging Handout** — 400s carrying stack traces and constraint names to the public
   internet.
6. **The Retry-After Liar** — `Retry-After` on a `500` bug that will never heal on a timer.
7. **The Gateway Blur** — edge timeouts shorter than app deadlines, so every slow path
   becomes an anonymous `504`.

## Chapter checklist

- [ ] The selection table in `05-reference/README.md` matches our registry 1:1.
- [ ] No 4xx/5xx literal exists outside the mapping module.
- [ ] `401`/`405` always carry their RFC-required headers.
- [ ] Every `429`/`503` carries `Retry-After`.
- [ ] No `2xx`-for-failure paths except documented bulk/polling patterns.
- [ ] Contract tests assert one status per error code.

## Related

- [Chapter 19 Reference](../05-reference/README.md)
- [Misleading Responses and Internal Exposure](../02-deep-dive/02-misleading-responses-and-internal-exposure.md)
- [Do's and Don'ts (Ch. 20)](../../20-standardized-api-error-responses/04-dos-and-donts/README.md)
