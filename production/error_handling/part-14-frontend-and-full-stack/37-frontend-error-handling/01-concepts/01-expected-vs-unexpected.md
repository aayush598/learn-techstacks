# Expected vs Unexpected Frontend Failures

> Part XIV · Chapter 37 · Section 37.1 · _Estimated reading time: 16 min_
> **Prerequisite:** [Error, Fault, Failure, and Exception](../../../part-01-foundations/01-understanding-errors-and-failures/01-concepts/01-error-fault-failure-exception.md)

## In one sentence

**Treat failures as *expected* if they are part of the product contract** (validation, auth, not found, rate limits) and handle them inline; treat them as *unexpected* if they indicate bugs or unknown environment states and route them to error boundaries, logging, and safe recovery.

## Why this matters in production

Mixing the two is expensive. Surfacing a field validation as an app crash wastes a round trip; silently swallowing a render bug corrupts UI state. For **Acme SaaS**, **Checkout**, and **AgentRun**, the split determines whether a user corrects a form, retries a payment safely, or sees a blank screen with no path forward.

## Core concept

| Class | Definition | Examples | Where to handle | User surface |
| --- | ---------- | -------- | --------------- | ------------ |
| **Expected** | Anticipated outcomes defined by API/UI contract. | 400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 unprocessable, 429 rate limited, empty lists, offline indicator | Inline in component/route logic (forms, empty states, guards) | Field errors, inline banners, empty states, modals with actions |
| **Unexpected** | Unpredicted failures indicating a bug or unknown state. | Render throw, `TypeError` from bad data shape, unhandled promise rejection not mapped, corrupted cache, third-party script crash | Error boundary, global handler, crash reporting with diagnostics | Fallback UI with "Try again" or "Reload", hide details, preserve navigation where possible |

> **Note:** "Expected" does not mean "harmless" — **Checkout** payment failures are expected outcomes that must be surfaced safely and never treated as a crash.

## How it works (mechanics)

1. **Classify at the boundary.** When parsing an API response, map status codes and `error.code` to expected/unexpected (see [Chapter 38](../../38-full-stack-error-contracts/README.md)).
2. **Route early.** Expected errors never reach the error boundary; handle in the flow (form mapping, guards).
3. **Contain unexpected.** Throw to nearest appropriate boundary or catch in global handlers; log with context (route, userId hash, errorId) without leaking stack traces to users.
4. **Offer recovery.** Prefer targeted recovery (retry the action) over full reload when safe.

## Worked example

```tsx
// Expected: map API validation errors to fields
async function submitCheckout(values: CheckoutForm) {
  try {
    const res = await api.post("/checkout", values);
    navigate("/checkout/success", { state: { id: res.data.orderId } });
  } catch (err: any) {
    if (err.status === 422 && err.details?.invalid_params) {
      // Expected: surface to form fields
      setFieldErrors(mapInvalidParams(err.details.invalid_params));
      return; // do NOT throw
    }
    if (err.status === 401) {
      // Expected: trigger auth flow
      return triggerAuthExpiry(err); // single-flight refresh per Chapter 38
    }
    // Unexpected: let boundary handle or show fallback
    throw err; // or report + show recoverable fallback
  }
}
```

## Key data / numbers

| Item | Value/Guidance | Notes |
| --- | -------------- | ----- |
| **HTTP for validation** | `400`, `422` | Treat as expected; map to fields. |
| **Auth** | `401` | Expected flow: refresh or redirect (never crash). |
| **Rate limit** | `429` with `Retry-After` | Expected; show countdown + retry control. |
| **Server errors** | `500`, `503` | Often unexpected from client POV unless contract says otherwise; route to fallback. |
| **Client bugs** | Render throws | Unexpected; must hit error boundary. |

## Real-world use case — Acme SaaS (Project creation)

**Context:** In **Acme SaaS**, creating a project returns `422` if the slug is taken. The API includes `invalid_params: [{field: "slug", code: "SLUG_TAKEN"}]`. 

**Failure:** The team initially threw on any non-2xx and wrapped the whole modal in an app boundary — a slug collision crashed the modal. 

**Fix:** Classify `422` as **expected**, map `SLUG_TAKEN` to the `slug` field with an inline message. Only network drops and render bugs are treated as unexpected. 

**Result:** Users correct slugs without losing their form data; crash rate drops and support load decreases.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Throw everything** | Simple | Crashes for expected errors; poor UX | Never in production UI flows |
| **Inline handling only** | Great UX for expected | Unexpected still need containment | Required for expected; insufficient alone |
| **Classify + route** | Correct split, recoverable | Requires mapping layer and discipline | **Recommended default** for all SaaS UIs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify by contract (status + `error.code`) not by "is it an Error instance" | Treat every `catch` as "show generic error" |
| Handle 401/403/422 inline or via flow | Crash the page for form validation |
| Route unexpected to boundaries + telemetry with `errorId` | Leak stack traces or raw SQL/URLs to users |
| Keep user copy generic for unexpected; details in diagnostics only | Show "Cannot read property of undefined" to end users |

## Common mistakes

- **Exception ≠ unexpected.** A `throw` from validation is bad; use a typed result.
- **Over-crashing.** Wrapping large subtrees in one boundary makes everything unrecoverable.
- **Under-containment.** Async rejections not handled propagate nowhere visible — plan separately (37.22).

## Checklist

- [ ] I can list expected codes for my top flows (**Checkout**, forms, auth).
- [ ] I have a mapping from API errors to inline vs boundary.
- [ ] Unexpected failures go to boundary + logging with safe messages.
- [ ] I never let expected failures throw across the component tree unnecessarily.

## Related

- [Boundaries: Component, Page, App](./02-boundaries-component-page-app.md)
- [Recoverable vs Unrecoverable UI](./03-recoverable-vs-unrecoverable-ui.md)
- [API Error → Form Field Mapping (Practical)](../03-practical-examples/02-api-error-to-form-field-mapping.md)
- [Full-Stack Error Contracts](../../38-full-stack-error-contracts/README.md)
