# Chapter 38 — Reference (Full-Stack Error Contracts)

> Part XIV · Chapter 38 · Section 05 · _Estimated reading time: 16 min_

## End-to-End Error Contract (Shape)

```json
{
  "type": "https://api.acme.com/errors/<slug>",
  "title": "Short summary",
  "status": 422,
  "detail": "Human-readable (may be safe or dev-oriented)",
  "instance": "/resource/path",
  "error_id": "err_01H...",
  "traceId": "req_...",
  "code": "VALIDATION_FAILED",
  "invalid_params": [
    {"field": "email", "code": "EMAIL_TAKEN", "message": "..."}
  ]
}
```

**Rules:** `code` is machine-stable (shared enum). `error_id` for correlation. User copy from frontend i18n by code. No secrets/stacks.

## Code → UI Action Mapping (Quick)

| Code | Status | UI Action | Surface |
| ---- | ------ | --------- | ------- |
| `UNAUTHENTICATED`/`SESSION_EXPIRED` | 401 | Auth flow (refresh/login) | Modal/redirect |
| `UNAUTHORIZED` | 403 | Permission message | Banner/page |
| `VALIDATION_FAILED` + `invalid_params` | 422 | Field + summary | Form |
| `EMAIL_TAKEN`/`SLUG_TAKEN` | 422/409 | Field error | Input |
| `CONFLICT` | 409 | Resolution UI | Modal/banner |
| `SEAT_LIMIT_EXCEEDED`/`DOMAIN_NOT_ALLOWED` | 403/422 | CTA (upgrade/contact) | Summary/banner |
| `RATE_LIMITED` | 429 | Countdown + retry | Inline/disabled (honor Retry-After) |
| `PAYMENT_DECLINED` | 422/402 | Safe summary | Checkout summary (no processor details) |
| `SERVICE_UNAVAILABLE` | 503 | Retry/fallback | Toast/boundary |
| `INTERNAL_ERROR`/unknown | 500 | Fallback + errorId | Toast/boundary |

## 401 Refresh Flow Checklist

- [ ] Detect 401 with auth code
- [ ] Single-flight `doRefresh()`; share `refreshPromise`
- [ ] Queue requests during refresh
- [ ] Replay original request **once** with `retried=true`
- [ ] If refresh fails: clear session, `redirectToLogin()` with `return_to`
- [ ] If replay returns 401: go to login (no re-refresh)
- [ ] Redirect guard (`isRedirecting`) prevents storms
- [ ] Preserve intent for **Checkout** flows

## Unknown Codes / Version Incompatibility

| Scenario | Handling |
| --------- | -------- |
| **Unknown `code`** | Map to `UNKNOWN` fallback; log with `error_id`; show safe generic message |
| **Unknown field in envelope** | Ignore (forward-compatible) |
| **API version mismatch** | Detect via header/version; show "Update app" or safe fallback; avoid breaking |
| **Old client + new codes** | Additive codes OK if unknown handled; breaking changes need version window |

## End-to-End Contract Checklist

- [ ] Shared envelope (RFC 9457) + extensions
- [ ] Shared `ErrorCode` enum with ownership/deprecation
- [ ] Central mapper pure + testable
- [ ] i18n by code, diagnostics separate
- [ ] 401 refresh correct
- [ ] Contract tests in CI
- [ ] Unknowns/fallbacks defined
- [ ] Correlation (`error_id`/traceId) on all errors
- [ ] No PII/secrets in client-visible messages

## Related

- [Chapter 38 README](../README.md)
- [Chapter 37 — Frontend Error Handling](../../37-frontend-error-handling/README.md)
- [Part VIII — HTTP and API](../../../part-08-http-and-api/README.md)
