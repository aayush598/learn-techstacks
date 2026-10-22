# Forms, API Response Errors, and Validation Mapping

> Part XIV · Chapter 37 · Sections 37.7–37.8 · _Estimated reading time: 17 min_
> **Prerequisite:** [Expected vs Unexpected](./01-expected-vs-unexpected.md)

## In one sentence

**Separate client validation (instant feedback) from server validation (source of truth):** map API errors (especially `invalid_params`) to specific form fields, keep a general error summary for cross-field issues, and never trust client checks alone.

## Why this matters in production

For **Acme SaaS** signup and **Checkout**, race conditions, multi-tenant rules, and business constraints can only be enforced server-side. Mis-mapping turns a field error into "Something went wrong" or worse, loses user input. Correct mapping preserves state and guides correction.

## Core concept

| Source | Type | When | Surface |
| ------ | ---- | ---- | ------- |
| **Client validation** | Expected, synchronous | On blur/change/submit before request | Inline per field, immediate |
| **Server validation** | Expected, authoritative | On submit/API response | Map to fields + summary for cross-field/global |
| **Business rule** | Expected | After validation (e.g., slug taken) | Field or summary depending on scope |
| **Unexpected** | See 37.1 | Network/500/bug | Fallback/boundary, not field list |

## API error shapes (common)

Prefer **RFC 9457 Problem Details** (`application/problem+json`) with extensions:

```json
{
  "type": "https://api.acme.com/errors/validation-failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "error_id": "err_9f3a",
  "invalid_params": [
    { "field": "email", "code": "EMAIL_TAKEN", "message": "Email already in use." },
    { "field": "slug", "code": "SLUG_INVALID", "message": "Invalid format." }
  ]
}
```

See [Chapter 38](../../38-full-stack-error-contracts/README.md) for full contract details.

## Mapping strategy

1. **Parse safely.** Validate envelope shape before mapping.
2. **Map field errors.** For each `invalid_params` entry, set field error by `field` path (handle nested `address.city`).
3. **Handle cross-field.** Put errors with no field or `form` into a summary banner.
4. **Fallback for unknown.** If codes unknown, show generic field message + log diagnostics.
5. **Preserve values.** Never clear the form on expected validation errors.

## Worked example

```ts
// Map API errors to react-hook-form / form state
function mapApiErrorsToForm(
  err: ApiError,
  setError: (name: string, e: {type:string,message:string}) => void,
  setFormError: (m: string) => void
) {
  if (err.status !== 422 || !Array.isArray(err.details?.invalid_params)) {
    throw err; // unexpected or unhandled
  }
  const params = err.details.invalid_params;
  let hadField = false;
  for (const p of params) {
    if (p.field && p.field !== 'form') {
      setError(p.field, { type: p.code || 'server', message: mapCodeToMessage(p.code, p.message) });
      hadField = true;
    } else {
      setFormError(mapCodeToMessage(p.code, p.message) || err.details.detail || 'Please fix the errors.');
    }
  }
  if (!hadField && !params.length) setFormError(err.details.detail || 'Validation failed.');
}
```

```tsx
<form onSubmit={handleSubmit(onSubmit)}>
  <Field name="email" error={errors.email?.message} />
  <Field name="slug" error={errors.slug?.message} />
  {formError && <Alert variant="error">{formError}</Alert>}
  <Button type="submit">Create</Button>
</form>
```

## Key data / numbers

| Status | Meaning | UI action |
| ------ | ------- | --------- |
| **400** | Bad request / malformed | Often unexpected or summary; validate shape |
| **422** | Semantic validation failed | **Primary** for field mapping (`invalid_params`) |
| **409** | Conflict (e.g., duplicate) | Field or summary depending on which resource conflicts |
| **429** | Rate limited | Summary + retry countdown, not field errors |

## Real-world use case — Acme SaaS (User invitation)

**Context:** Inviting a user to an org: email may be taken, org at seat limit, or domain restricted.

**Failure:** API returns `422` but UI shows "Something went wrong" and clears the email.

**Fix:** Map `EMAIL_TAKEN` to email field, `SEAT_LIMIT_EXCEEDED` to a summary banner with "Upgrade plan" CTA, and `DOMAIN_NOT_ALLOWED` to summary. Preserve email input.

**Result:** User fixes the specific issue or takes the correct action without retyping.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Only client validation | Fast feedback | Bypassable, misses business rules | First pass only |
| Only server messages | Authoritative | Slow, bad UX without mapping | Insufficient alone |
| Map server errors to fields | Best UX + correct | Needs schema mapping + i18n | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat server as source of truth for business rules | Clear form on 422 |
| Support nested field paths (`address.line1`) | Only handle flat field names |
| Provide cross-field summary | Put every error on a random field |
| Use error codes for mapping, keep messages overridable by i18n | Hardcode English from API verbatim everywhere |

## Common mistakes

- **Clearing inputs.** Loses user work.
- **Wrong field targeting.** `email` error shown on password.
- **Leaking details.** Showing internal constraint names.
- **Ignoring unknown codes.** Crash or blank message.

## Checklist

- [ ] Client validation + server mapping both implemented.
- [ ] `invalid_params` parsed safely with fallbacks.
- [ ] Cross-field errors in summary banner.
- [ ] Form state preserved on validation failures.
- [ ] Mapping layer uses codes (see Chapter 38).

## Related

- [API Error → Form Field Mapping (Practical)](../03-practical-examples/02-api-error-to-form-field-mapping.md)
- [Full-Stack Error Contracts — Mapping](../../38-full-stack-error-contracts/01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)
- [Validation and Business Errors (Part VII)](../../../part-07-validation-and-business-errors/README.md)
