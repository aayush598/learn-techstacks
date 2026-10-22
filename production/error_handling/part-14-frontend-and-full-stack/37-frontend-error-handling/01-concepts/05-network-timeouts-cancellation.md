# Network Failures, Timeouts, Cancellation, and Navigation

> Part XIV · Chapter 37 · Sections 37.9–37.11 · _Estimated reading time: 18 min_
> **Prerequisite:** [Expected vs Unexpected](./01-expected-vs-unexpected.md), [Recoverable vs Unrecoverable](./03-recoverable-vs-unrecoverable-ui.md)

## In one sentence

**The browser is unreliable:** treat network failures/timeouts as recoverable with backoff, use **AbortController** for cancellation, and **ignore stale responses on navigation/unmount** to avoid setting state after teardown or overwriting newer results.

## Why this matters in production

For **ExportJob** infinite lists and **AgentRun** long-running tool calls, users navigate quickly. Without cancellation, slow responses resolve after unmount and corrupt state; timeouts hang indefinitely without UX. Offline/drops are normal, not exceptional.

## Core concept

| Aspect | Network failures (37.9) | Timeouts (37.10) | Cancellation/Navigation (37.11) |
| ------ | ----------------------- | ---------------- | ------------------------------- |
| **What** | Offline, DNS, connection refused, CORS errors | Request exceeds max wait | User navigates, unmounts, cancels action |
| **Classification** | Expected/recoverable (transient) | Recoverable | Control signal (not an error in most cases) |
| **Indicator** | `NetworkError`, navigator.onLine | `AbortError`/timeout error | `AbortError` (DOMException/AbortError) |
| **UX** | "You're offline" + retry when online | "Request timed out" + retry | Silently ignore stale response |
| **Policy** | Retry with jittered backoff; respect backpressure | Per request budget + per flow | Abort on unmount/route change; dedupe |

## Timeouts and budgets

Set per-endpoint budgets. Avoid a single global timeout for very different operations:

| Operation | Suggested timeout (ms) | Rationale |
| --------- | -------------------- | --------- |
| **Interactive CRUD** (forms, Checkout) | 5000–10000 | Balance UX vs reliability |
| **Search/autocomplete** | 2000–3500 | Debounce + shorter budget |
| **Uploads** (large files) | No fixed short timeout or progress-based | Track progress; use `AbortController` |
| **Exports/AgentRun** (long) | 15000–30000+ or use polling | Prefer async jobs + polling over long HTTP waits |

## AbortController (cancellation)

```ts
useEffect(() => {
  const controller = new AbortController();
  const signal = controller.signal;
  (async () => {
    try {
      setState(s=>({...s, status:'loading'}));
      const data = await api.get('/export-jobs', { signal });
      if (signal.aborted) return; // stale
      setState({status:'ok', data});
    } catch (e:any) {
      if (e.name === 'AbortError' || signal.aborted) return; // ignore cancellation
      // classify e.status/network/timeout
      setState({status:'error', error: classify(e)});
    }
  })();
  return () => controller.abort(); // on unmount/navigation
}, [filters]);
```

**Critical:** Check `signal.aborted` after `await` (race) and in catch; never call `setState` after abort/unmount.

## Navigation and stale responses

When the user navigates away (React Router), in-flight requests for the previous page must be aborted. Keep request keys (route+filters) to ignore mismatched responses. For lists with filters, abort on filter change immediately.

## Retry guidance

- **Network/timeout/503:** Retry with exponential backoff + jitter; cap attempts.
- **AbortError:** **Never** retry on cancellation (it's intentional).
- **429:** Respect `Retry-After` header (see [Part XI](../../../part-11-retry-and-resilience/README.md)).
- **4xx except 408/429:** Usually not retryable.

## Key data / numbers

| Item | Guidance | Notes |
| --- | -------- | ----- |
| **Default connect timeout** | 5s (client) | Tune per critical flow |
| **Retry max attempts** | 2–3 for user-initiated | Avoid retry storms |
| **Backoff** | exponential + jitter (e.g., 200, 400, 800ms + jitter) | Prevent thundering herd |
| **`Retry-After`** | Honor seconds/date | Required for 429 fairness |

## Real-world use case — ExportJob (pagination + navigation)

**Context:** User scrolls **ExportJob** list, changes filters rapidly, then navigates to a job detail.

**Failure:** Slow filter request completes after navigation and overwrites detail/list state, causing flash of stale data.

**Fix:** Use AbortController per request; on filter change abort previous; on unmount/route change abort in-flight; ignore `AbortError`. Track request id to drop mismatched responses.

**Result:** No stale writes; smooth navigation without state corruption.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No cancellation | Simple | Stale state, leaks, poor UX | Never in route-based apps |
| Global timeout only | Easy | Wrong for uploads/long jobs | Insufficient |
| Per-request abort + timeouts | Correct | Slight boilerplate | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Abort on unmount and route change | Call setState after `AbortError`/aborted |
| Treat cancellation as non-error (silent ignore) | Toast "Request cancelled" on navigation |
| Use timeouts per flow | Let requests hang forever |
| Retry network/timeout with jitter; never retry AbortError | Retry on user-initiated cancellation |

## Common mistakes

- **Setting state after unmount.** Memory leaks and React warnings → always guard.
- **Retrying cancellation.** Creates loops.
- **Ignoring `Retry-After`.** Hammering rate-limited endpoints.
- **One timeout for everything.** Uploads fail prematurely.

## Checklist

- [ ] All data-fetching uses AbortController with cleanup.
- [ ] Navigation aborts previous requests.
- [ ] Timeouts configured per endpoint/flow.
- [ ] Cancellation is ignored (no user-facing error).
- [ ] Retry policy excludes AbortError and honors Retry-After.

## Related

- [Stale Data, Refresh, Optimistic Rollback](../02-deep-dive/01-stale-data-refresh-optimistic-rollback.md)
- [Retry/Recovery Controls](../02-deep-dive/03-state-transitions-retry-notifications-corruption.md)
- [Retry and Resilience (Part XI)](../../../part-11-retry-and-resilience/README.md)
