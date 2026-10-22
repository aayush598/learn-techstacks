# Mapping API→UI and Validation→Fields

> Part XIV · Chapter 38 · Sections 38.3–38.4 · _Estimated reading time: 17 min_
> **Prerequisite:** [Aligning Taxonomies and Shared Codes](./01-aligning-taxonomies-shared-codes.md), [Chapter 37 — Forms/Mapping](../../37-frontend-error-handling/01-concepts/04-forms-api-validation-mapping.md)

## In one sentence

**Map the contract to UI intent:** use a pure mapping layer to translate `(status, code, invalid_params)` into UI actions (field error, summary, toast, modal CTA, auth flow) — same logic for web and mobile.

## Why this matters in production

For **Checkout** and **Acme SaaS**, scattered `if (err.code === ...)` across components create duplication and drift. A centralized mapper is testable, supports i18n, and makes unknown codes safe.

## API→UI mapping (38.3)

| Code/Status | UI Action | Surface | Notes |
| ----------- | --------- | ------- | ----- |
| `UNAUTHENTICATED` / 401 | Auth flow | Modal/redirect | Trigger refresh or login; preserve intent (38.8) |
| `UNAUTHORIZED` / 403 | Permission banner | Page/section | Explain + upgrade/contact |
| `VALIDATION_FAILED` + `invalid_params` | Field + summary | Form | Map per field (38.4) |
| `EMAIL_TAKEN`, `SLUG_TAKEN` | Field error | Input | Specific correction |
| `CONFLICT` | Resolution UI | Modal/banner | Show conflict details/options |
| `SEAT_LIMIT_EXCEEDED` | CTA | Summary/banner | Upgrade/plan action |
| `RATE_LIMITED` + `Retry-After` | Retry with countdown | Inline/disabled | Honor header |
| `SERVICE_UNAVAILABLE` / 5xx | Retry/fallback | Toast or boundary | Recoverable with backoff |
| `INTERNAL_ERROR` (unknown details) | Fallback + errorId | Toast/boundary | No internal details |

## Validation→Fields mapping (38.4)

```ts
type UiAction =
  | { kind: 'field'; field: string; code: string; message: string }
  | { kind: 'summary'; code: string; message: string }
  | { kind: 'toast'; code: string; message: string; retryAfter?: number }
  | { kind: 'auth'; flow: 'refresh' | 'login'; intent?: unknown }
  | { kind: 'cta'; code: string; message: string; cta: 'upgrade'|'contact' }
  | { kind: 'boundary' | 'fallback'; errorId?: string };

function mapProblemToUi(p: ProblemDetails): UiAction[] {
  const actions: UiAction[] = [];
  const code = p.code as string | undefined;
  const status = p.status;
  // Field errors first
  if (Array.isArray(p.invalid_params) && p.invalid_params.length) {
    for (const ip of p.invalid_params) {
      if (ip.field && ip.field !== 'form') {
        actions.push({ kind: 'field', field: ip.field, code: String(ip.code||'VALIDATION'), message: localize(ip.code, ip.message) });
      } else {
        actions.push({ kind: 'summary', code: String(ip.code||'VALIDATION_FAILED'), message: localize(ip.code, ip.message || p.detail) });
      }
    }
    if (actions.length) return actions;
  }
  // Non-field
  if (status === 401 || code === 'UNAUTHENTICATED' || code === 'SESSION_EXPIRED') {
    return [{ kind: 'auth', flow: code === 'SESSION_EXPIRED' ? 'refresh' : 'login' }];
  }
  if (code === 'SEAT_LIMIT_EXCEEDED') return [{ kind: 'cta', code, message: localize(code), cta: 'upgrade' }];
  if (code === 'RATE_LIMITED') return [{ kind: 'toast', code, message: localize(code), retryAfter: parseRetryAfter(p) }];
  // Fallback
  return [{ kind: 'fallback', errorId: p.error_id }];
}
```

## i18n considerations

- **Key by code:** `errors.codes.SLUG_TAKEN` not by English server text.
- **Fallback chain:** code → default English → generic safe message.
- **Parameterized:** include values safely (no PII).
- **Pluralization/variants:** handle by locale.

## Real-world use case — Checkout

Address validation fails on `address.zip` → field error. Card declined with `code: 'PAYMENT_DECLINED'` → summary with safe message (never expose processor details). Inventory conflict on quantity → resolution UI with available count.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Scattered checks | Quick | Duplication, inconsistent | Never |
| Central mapper | Testable, consistent, i18n-friendly | Initial setup | **Recommended default** |
| Per-component mapping | Local | Hard to keep in sync | Only trivial cases |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pure function: `(ProblemDetails) -> UiAction[]` | Side effects in mapper |
| Localize by code, fallback to safe generic | Render `p.detail` verbatim as user message |
| Handle nested field paths | Only support top-level |
| Return array to support multiple actions | Assume single error |

## Checklist

- [ ] Mapper covers field, summary, auth, CTA, toast, fallback
- [ ] Uses shared ErrorCode enum
- [ ] i18n keyed by code with fallback
- [ ] Handles `invalid_params` fully
- [ ] Safe messages, diagnostics via `error_id`

## Related

- [API Error → Form Field Mapping (Practical)](../../37-frontend-error-handling/03-practical-examples/02-api-error-to-form-field-mapping.md)
- [Unknown Codes, Version Incompatibility](./03-unknown-codes-version-incompatibility.md)
- [Localization, Diagnostics vs User Messages](../02-deep-dive/02-localization-diagnostics-vs-user-messages.md)
