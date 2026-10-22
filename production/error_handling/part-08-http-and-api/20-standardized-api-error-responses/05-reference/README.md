# Chapter 20 — Reference

> Part VIII · Chapter 20 · The error envelope spec, extension registry, and glossary.

## Error envelope spec (RFC 9457 + Acme extensions)

### Required/standard members
| Member | Required | Type | Notes |
| ------ | -------- | ---- | ----- |
| `type` | No | URI reference | Problem type identifier. Default `about:blank`. Use root-relative `/problems/...` |
| `title` | No | String | Fixed per type; not for logic/localization |
| `status` | No | Number | Mirrors HTTP status line |
| `detail` | No | String | Instance-specific, safe for support |
| `instance` | No | URI reference | Occurrence pointer (`/api/...` or operation URI) |

### Acme extensions (documented)
| Member | Required | Type | Notes |
| ------ | -------- | ---- | ----- |
| `code` | **Yes** (coded API) | String | Stable public app code from registry (aliases applied) |
| `requestId` | **Yes** | String | Opaque trace handle, echoed in `X-Request-Id` header |
| `errors` | Conditional | `FieldError[]` | Present for validation (`422`) and schema failures |
| `retryAfterSeconds` | Conditional | Number | Present for `429`/`503` (mirror `Retry-After` header) |
| `currentVersion` | Conditional | Number | Present for `409` on optimistic concurrency |
| `summary` | Conditional | Object | Present for bulk results (`total`, `succeeded`, `failed`) |
| `results` | Conditional | Array | Present for bulk per-item results |
| `partial` | Conditional | Boolean | Present on incomplete paginated success responses |

### FieldError schema
```json
{ "field": "items[0].qty", "code": "out_of_range", "message": "..." }
```
- `field`: request-shape dotted path
- `code`: closed machine vocabulary (`required`, `type_mismatch`, `out_of_range`, `format_invalid`, `enum_invalid`, `cross_field`)
- `message`: human, safe

## Problem type namespace (example)
| type | title | status | when |
| ---- | ----- | ------ | ---- |
| `/problems/malformed-request` | Malformed Request | 400 | Unparseable JSON/syntax |
| `/problems/unauthenticated` | Unauthenticated | 401 | Credential failure |
| `/problems/forbidden` | Forbidden | 403 | Permission denied |
| `/problems/not-found` | Not Found | 404 | Missing/hidden |
| `/problems/unsupported-media-type` | Unsupported Media Type | 415 | Wrong Content-Type |
| `/problems/validation-error` | Validation Failed | 422 | Semantic/field errors |
| `/problems/conflict` | Conflict | 409 | State/version conflict |
| `/problems/rate-limited` | Too Many Requests | 429 | Quota exceeded |
| `/problems/service-unavailable` | Service Unavailable | 503 | Known temporary down |
| `/problems/internal-error` | Internal Server Error | 500 | Unexpected (generic) |

## Serialization rules
- Media type: **`application/problem+json`**
- Status + body status must match
- Internal codes → projected via registry before serialization
- 500s use generic `detail`; full details in logs only
- `errors[]` capped at 20; reflections truncated/escaped
- No stacks, SQL, hosts, vendor names on the wire

## Chapter glossary
| Term | Meaning |
| ---- | ------- |
| Error envelope | The standard response body shape used for all failures |
| Problem Details | RFC 9457 standard for HTTP API problem documents |
| Problem type | A stable identifier (`type` URI) for a class of error |
| Extension member | Non-standard member added to Problem Details (e.g. `code`, `requestId`) |
| Field error | A per-field validation entry in `errors[]` |
| Public projection | The sanitized view of an error sent to clients (aliases applied) |
| Bulk result | Per-item outcomes for multi-item operations |
| Incompleteness signal | Explicit flag (`partial`) showing omitted/truncated page data |

## Signposts
- Wire scenarios → [Error Shapes Across Scenarios](../03-practical-examples/02-error-shapes-across-scenarios.md)
- Code factory → [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
- Middleware enforcement → [Chapter 21](../../21-api-boundary-and-middleware-error-handling/README.md)

## Related
- [Chapter 20 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 19 HTTP Error Semantics](../../19-http-error-semantics/README.md)
- [Part VIII Index](../../README.md)
