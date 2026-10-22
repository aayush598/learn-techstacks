# Generated Clients, Auth Expiration, and Repeated Redirects

> Part XIV · Chapter 38 · Sections 38.7–38.9 · _Estimated reading time: 19 min_
> **Prerequisite:** [Mapping API→UI](./02-mapping-api-to-ui-and-validation-to-fields.md), [Chapter 37 — Network/Cancellation](../../37-frontend-error-handling/01-concepts/05-network-timeouts-cancellation.md)

## In one sentence

**Wrap generated API clients at the boundary:** map errors to Problem Details/UiActions, implement the **HTTP 401 refresh flow** with single-flight and a request queue, replay the original request once, preserve intent, and prevent repeated redirects/loops.

## Why this matters in production

For **Acme SaaS** and **Checkout**, token expiry mid-request is common. Without single-flight, parallel requests all trigger refresh simultaneously; without queuing, requests fail or cause redirect storms. Generated clients often throw generic errors and leak types — wrap them.

## Generated clients (38.7)

**Strategy:**
1. **Generate types from OpenAPI** but don't let them leak to UI directly.
2. **Create an API client wrapper** (fetch/axios) that:
   - Normalizes errors to `ApiError`/`ProblemDetails`
   - Attaches auth headers
   - Handles 401 refresh
   - Maps to domain errors/UI actions
3. **Validate at boundary** (defensive parsing of envelope)
4. **Version compatibility:** handle unknown fields safely

```ts
// Wrapper
export async function apiFetch<T>(input: RequestInfo, init: ApiInit = {}): Promise<T> {
  const res = await fetch(input, withAuth(init));
  if (!res.ok) {
    const prob = await parseProblem(res); // safe parse
    throw mapToApiError(res.status, prob, res.headers);
  }
  return res.json();
}
```

## Auth expiration flow (38.8) — HTTP 401 refresh

**Requirements:**
- **Detect** `401` with `code === 'UNAUTHENTICATED'` or `SESSION_EXPIRED`
- **Single-flight refresh:** only one refresh in progress; others wait
- **Queue requests** made during refresh
- **Replay original request** once after successful refresh (with new tokens)
- **On refresh failure:** clear session, redirect to login preserving **original intent** (return URL/path + query)
- **No retry loops:** if replayed request returns 401 again → don't refresh again, go to login
- **Rotate tokens safely** (httpOnly cookies or secure storage)

## Implementation sketch

```ts
let refreshPromise: Promise<boolean> | null = null;
const pending: Array<(ok: boolean) => void> = [];

async function refresh(): Promise<boolean> {
  if (refreshPromise) return refreshPromise;
  refreshPromise = (async () => {
    try {
      const r = await fetch('/auth/refresh', { method: 'POST', credentials: 'include' });
      return r.ok;
    } catch { return false; }
  })();
  const ok = await refreshPromise;
  refreshPromise = null;
  pending.forEach(cb => cb(ok));
  pending.length = 0;
  return ok;
}

export async function apiFetchWithRefresh<T>(input: RequestInfo, init: RequestInit = {}): Promise<T> {
  const res = await fetch(input, { ...init, credentials: 'include' });
  if (res.status !== 401) {
    if (!res.ok) throw await toApiError(res);
    return res.json();
  }
  // Try refresh once
  const ok = await refresh();
  if (!ok) {
    // Clear session, redirect with intent
    redirectToLogin({ returnTo: location.pathname + location.search });
    throw new AuthExpiredError();
  }
  // Replay original request once
  const res2 = await fetch(input, { ...init, credentials: 'include' });
  if (!res2.ok) throw await toApiError(res2);
  return res2.json();
}
```

**Notes:**
- Use `credentials: 'include'` for httpOnly cookies or attach access token
- Track "retried" flag to prevent infinite loop
- Preserve intent: store in query/state before redirect
- **Checkout**: ensure cart not lost on auth redirect

## Repeated redirects (38.9)

**Prevention:**
- **Single-flight refresh** (critical)
- **Don't redirect from API layer multiple times** — use a flag (`isRedirecting`)
- **Check session before redirect** (race between tabs)
- **Backoff/guard**: if already on login page, don't redirect again
- **Handle concurrent tabs** (broadcast logout/refresh)

```ts
let redirecting = false;
function redirectToLogin(opts: {returnTo?: string}) {
  if (redirecting || location.pathname.startsWith('/login')) return;
  redirecting = true;
  const rt = encodeURIComponent(opts.returnTo || location.href);
  location.assign(`/login?return_to=${rt}`);
}
```

## Key data / numbers

| Item | Guidance | Notes |
| --- | -------- | ----- |
| **Refresh attempts** | **Once** per 401 trigger set | Single-flight + no re-refresh on replay 401 |
| **Queue size** | Unbounded in memory but short-lived | During single refresh |
| **Retry after refresh** | Exactly **once** | Then fail to login |
| **Redirect guard** | Global flag + pathname check | Prevent storms |

## Real-world use case — Checkout

User adds to cart (guest or session), token expires on payment submit. API returns 401 → refresh single-flight, queue payment request, replay after refresh, submit succeeds. If refresh fails, redirect to login with `return_to=/checkout` preserving cart state.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No refresh, always redirect | Simple | Poor UX, loses intent | Never for SPAs |
| Refresh per request | Simple | Race condition, multiple refreshes | Buggy |
| Single-flight + queue + replay | Correct | More complex | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Single-flight refresh | Call refresh for every 401 in parallel |
| Queue requests during refresh | Fail all queued requests immediately |
| Replay original request once only | Infinite retry loop on replay 401 |
| Preserve original intent on redirect | Redirect to login without `return_to` |
| Use httpOnly secure cookies where possible | Store refresh tokens in localStorage carelessly |

## Common mistakes

- **Redirect storm.** Multiple tabs/components trigger redirects.
- **Lost intent.** User sent to login, loses cart/checkout step.
- **Re-refresh loop.** Don't refresh again if replay fails with 401.
- **Leaking generated types.** UI should use mapped domain types.

## Checklist

- [ ] Generated client wrapped at boundary
- [ ] 401 triggers single-flight refresh
- [ ] Requests queued and replayed once
- [ ] Redirect guard prevents storms
- [ ] Intent preserved; session cleared on failure
- [ ] No infinite loops

## Related

- [Chapter 37 — Network/Timeouts/Cancellation](../../37-frontend-error-handling/01-concepts/05-network-timeouts-cancellation.md)
- [Full-Stack — Optimistic Update Failures](../02-deep-dive/01-optimistic-update-failures-cross-platform.md)
- [Auth Expiry/Refresh Flow (Practical)](../03-practical-examples/03-auth-expiry-refresh-flow-end-to-end.md)
- [Part XIII — Security-Aware Error Handling](../../../part-13-security-aware-error-handling/README.md)
