# Chapter 20 — Do's and Don'ts

> Part VIII · Chapter 20 · All sections

## Envelope and RFC 9457

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `application/problem+json` for every 4xx/5xx | Serve API errors as `text/html` or bare strings |
| Give each problem type one stable `type` and fixed `title` | Put instance data (IDs/amounts) into `title` |
| Put instance facts in `detail`; put occurrence in `instance` | Write essays in `detail`; hide the request |
| Mirror HTTP status into the `status` member | Omit or contradict `status` |
| Extend via documented members; don't invent new top-level shapes | Create `{ok:false,...}` variants per endpoint |

## App codes, fields, and IDs

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use stable public `code`s from the registry (aliases applied) | Expose internal/vendor codes |
| Put field failures in `errors[]` with `field` + `code` + `message` | Return a field→message map with no machine code |
| Use dotted/array paths for `field` (request shape, not DB) | Leak column names |
| Emit opaque `requestId`s, propagate them, echo in body+header | Use sequential IDs or new IDs per layer |
| Cap `errors[]` (e.g. first 20) | Unbounded arrays on hostile input |

## Multiple and pagination errors

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep validation as single `422` + `errors[]` | Turn form validation into `200` + per-field errors |
| Use per-item results for independent bulk operations | All-or-nothing-fail 999 on item 1,000 |
| Signal partial/incomplete pagination explicitly | Silently drop rows from a page |
| Error distinctly on invalid/expired cursors | Return `[]` to masquerade an invalid cursor |
| Document batch limits | Accept unbounded bulk arrays |

## Consistency and safety

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Serialize only the typed public problem | Serialize `Error` objects directly |
| Use one generic `INTERNAL_ERROR` document for all bugs | Vary 500 detail by exception type |
| Keep stacks/SQL/host/vendor names in logs only | Leak them in client bodies/headers |
| Contract-test shape for every error code | Rely on manual spot checks |
| Apply aliases before serialization | Let internal codes reach the wire |

## Anti-patterns

1. **The Shape Soup** — five error shapes across one API.
2. **The Stack Handout** — HTML or JSON with a full traceback in production.
3. **The Message-Only API** — `{message}` only, clients string-match forever.
4. **The Silent Truncation** — paginated list drops rows with no `partial` flag.
5. **The Bulk Bomb** — one bad row kills an entire bulk request with no results.
6. **The Leaky ID** — `requestId` that encodes host/pod/timestamp aiding enumeration.
7. **The Versioned Type** — `/v1/problems/...` coupling types to API versions.

## Checklist

- [ ] Every 4xx/5xx uses `application/problem+json`.
- [ ] `type`/`title` fixed per type; instance data only in `detail`/`instance`.
- [ ] Public codes only; `requestId` present everywhere.
- [ ] Validation uses `errors[]`; bulk uses per-item results when independent.
- [ ] Contract tests enforce shape + denylist; CI blocks shape drift.

## Related

- [Chapter 20 Reference](../05-reference/README.md)
- [Error Shapes Across Scenarios](../03-practical-examples/02-error-shapes-across-scenarios.md)
- [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
