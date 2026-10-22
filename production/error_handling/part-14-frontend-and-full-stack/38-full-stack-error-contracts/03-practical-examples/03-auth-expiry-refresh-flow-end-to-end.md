# Auth Expiry / Refresh Flow — End-to-End (HTTP 401)

> Part XIV · Chapter 38 · Sections 38.8–38.9 · _Estimated reading time: 20 min_
> **Prerequisite:** [Auth Expiry/Redirects Concepts](../01-concepts/04-generated-clients-auth-expiry-redirects.md), [Chapter 37 — Network/Cancellation](../../37-frontend-error-handling/01-concepts/05-network-timeouts-cancellation.md)

## In one sentence

**Implement correct 401 handling:** single-flight refresh, request queue, replay original request once, preserve intent, prevent redirect storms, clear session on final failure.

## Requirements

- Detect 401 (`UNAUTHENTICATED`/`SESSION_EXPIRED`)
- Only one refresh in flight
- Queue all requests during refresh
- On success: replay queued + original request once
- On failure: clear session, redirect to login with `return_to` preserving intent
- Never refresh again on replayed 401
- Guard against multiple redirects and loops
- Works across tabs reasonably

## Implementation (TypeScript)

### State

```ts
let isRefreshing = false;
let refreshPromise: Promise<boolean> | null = null;
const queue: Array<{
  resolve: (v: Response) => void;
  reject: (e: any) => void;
  input: RequestInfo;
  init: RequestInit;
}> = [];
let isRedirecting = false;
```

### Refresh

```ts
async function doRefresh(): Promise<boolean> {
  try {
    const res = await fetch('/auth/refresh', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Accept': 'application/json' }
    });
    return res.ok;
  } catch {
    return false;
  }
}

function getRefreshPromise(): Promise<boolean> {
  if (refreshPromise) return refreshPromise;
  isRefreshing = true;
  refreshPromise = doRefresh().finally(() => {
    isRefreshing = false;
    refreshPromise = null;
  });
  return refreshPromise;
}
```

### Redirect with intent

```ts
function redirectToLogin() {
  if (isRedirecting) return;
  if (typeof location !== 'undefined' && location.pathname.startsWith('/login')) return;
  isRedirecting = true;
  const returnTo = typeof location !== 'undefined' ? (location.pathname + location.search) : '/';
  try { localStorage.setItem('acme.return_to', returnTo); } catch {}
  location.assign(`/login?return_to=${encodeURIComponent(returnTo)}`);
}
```

### API fetch with refresh

```ts
export async function apiFetch(input: RequestInfo, init: RequestInit = {}, retried = false): Promise<Response> {
  const res = await fetch(input, { ...init, credentials: 'include' });
  if (res.status !== 401) return res;
  if (retried) {
    // Replay already tried, refresh failed or replay failed
    clearSession();
    redirectToLogin();
    throw new Error('Session expired');
  }
  if (isRefreshing && refreshPromise) {
    // Queue this request
    return new Promise<Response>((resolve, reject) => {
      queue.push({ resolve, reject, input, init });
    }).then(() => apiFetch(input, init, true));
  }
  // Start refresh
  const ok = await getRefreshPromise();
  // Flush queue
  if (ok) {
    const q = queue.splice(0, queue.length);
    for (const item of q) {
      fetch(item.input, { ...item.init, credentials: 'include' }).then(item.resolve).catch(item.reject);
    }
    // Replay original once
    return apiFetch(input, init, true);
  } else {
    // Flush queue with failure
    const q = queue.splice(0, queue.length);
    for (const item of q) item.reject(new Error('Session expired'));
    clearSession();
    redirectToLogin();
    throw new Error('Session expired');
  }
}
```

### Clear session

```ts
function clearSession() {
  try { localStorage.removeItem('auth.token'); } catch {}
  // httpOnly cookies cleared by server on refresh fail or explicit logout
}
```

## Usage notes

- **Checkout:** preserve cart (server-side or localStorage) before redirect; restore after login
- **Parallel requests:** all queued correctly
- **Token rotation:** server rotates refresh token on refresh
- **Tabs:** consider BroadcastChannel for logout sync
- **Non-401 errors:** never trigger refresh

## Real-world use case — Checkout payment

User submits payment, access token expires mid-request → 401 → single refresh, queue payment, replay with new token, succeeds. If refresh fails, cart preserved, redirect to login with return_to `/checkout`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Refresh per request | Simple | Race storms | Broken |
| Single-flight + queue + replay-once | Correct, safe | Complex state machine | **Recommended default** |
| Silent refresh in background | Nice UX | Still need queueing | Combine with above |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Single-flight | Parallel refreshes |
| Queue during refresh | Drop queued requests |
| Replay original once only | Loop on replay 401 |
| Guard redirects | Multiple location.assign calls |
| Preserve intent | Redirect without return_to |

## Common mistakes

- **Forgetting retried flag** → infinite loop
- **Not queuing** → concurrent requests all fail
- **Redirect storm** → bad UX, loops
- **Losing checkout state** → cart empty after login

## Checklist

- [ ] 401 detected correctly
- [ ] Single-flight refresh implemented
- [ ] Queue + replay once
- [ ] Redirect guard + intent preservation
- [ ] Session cleared on final failure
- [ ] Works for parallel requests

## Related

- [Auth Expiry/Redirects Concepts](../01-concepts/04-generated-clients-auth-expiry-redirects.md)
- [Chapter 37 — Network/Cancellation](../../37-frontend-error-handling/01-concepts/05-network-timeouts-cancellation.md)
- [Optimistic Update Failures](../02-deep-dive/01-optimistic-update-failures-cross-platform.md)
