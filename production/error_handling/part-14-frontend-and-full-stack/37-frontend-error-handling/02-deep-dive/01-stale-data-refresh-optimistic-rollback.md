# Stale Data, Refresh, Optimistic UI, and Rollback

> Part XIV · Chapter 37 · Sections 37.12–37.13 · _Estimated reading time: 19 min_
> **Prerequisite:** [Network Failures, Timeouts, Cancellation](../01-concepts/05-network-timeouts-cancellation.md), [Retry and Resilience (Part XI)](../../../part-11-retry-and-resilience/README.md)

## In one sentence

**Treat freshness as a policy:** show stale data safely with refresh/invalidation, use **optimistic updates only when idempotent and reversible**, and **always rollback to last known good state** on failure with reconciliation against the server.

## Why this matters in production

For **Acme SaaS** favorites/projects and **Checkout** cart updates, optimistic UI feels fast but is dangerous. Without rollback, a failed "add to cart" leaves phantom items; without reconciliation, concurrent changes cause lost updates. Stale data misleads users (wrong quotas, old prices).

## Stale data and refresh (37.12)

| Strategy | When | Notes |
| -------- | ---- | ----- |
| **Stale-while-revalidate** | Lists that change infrequently | Show cached, revalidate in background; avoid blocking UI. |
| **On focus/refetch** | Tabs return to app | Revalidate critical data (auth, quotas). |
| **Manual refresh** | User action | Pull-to-refresh/retry button. |
| **Invalidation** | After mutations | Invalidate related keys (projects list after create). |
| **TTL-based** | Non-critical | Set max age; show "stale" indicator if desired. |

**Key:** Never trust optimistic cache blindly; reconcile on success/failure.

## Optimistic updates and rollback (37.13)

**Mechanics:**
1. **Snapshot** `previous = currentState` before mutation.
2. **Apply optimistically** update UI immediately.
3. **Send request** with idempotency key if non-idempotent or critical.
4. **On success:** confirm/reconcile with server response (server may return normalized state).
5. **On failure:** **rollback** to `previous` exactly; show recoverable error with retry; do **not** leave partial state.
6. **On abort/navigation:** do not rollback due to cancellation unless action was never sent — cancellation means ignore, don't revert user intent mid-flight carefully.

## Worked example (toggle favorite)

```ts
function useToggleFavorite(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (next: boolean) => api.post(`/projects/${projectId}/favorite`, { favorite: next }, { idempotencyKey: `fav:${projectId}:${nonce}` }),
    onMutate: async (next) => {
      await qc.cancelQueries({ queryKey: ['projects'] });
      const prev = qc.getQueryData(['projects']);
      qc.setQueryData(['projects'], (old:any) =>
        old?.map((p:any)=> p.id===projectId ? {...p, favorite: next} : p)
      );
      return { prev };
    },
    onError: (_err, _next, ctx) => {
      if (ctx?.prev) qc.setQueryData(['projects'], ctx.prev); // rollback
      toast.error('Could not update favorite. Try again.');
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ['projects'] }),
  });
}
```

**Notes:**
- **Snapshot before mutation.** Store previous in context.
- **Rollback on error.** Restore exactly previous state.
- **Idempotency:** For toggles/POSTs, include idempotency key (see [Part XI](../../../part-11-retry-and-resilience/README.md)).
- **Reconcile.** `onSettled` invalidates to sync with server truth.

## Limits of optimistic UI

| Case | Safe? | Guidance |
| ---- | ----- | -------- |
| **Idempotent GET-derived toggle** | Usually yes with rollback | Low risk if server can recheck. |
| **Non-idempotent charge (Checkout)** | **No** | Never optimistic-charge; show loading, disable submit, use idempotency keys. |
| **Quota-limited actions** | Risky | Server may reject due to race; rollback required. |
| **Complex multi-step** | No | Use explicit pending states; prefer server confirmation. |
| **Offline** | Caution | Queue only if idempotent and you can replay safely with reconciliation. |

## Key data / numbers

| Item | Guidance | Notes |
| --- | -------- | ----- |
| **Rollback requirement** | Mandatory for any optimistic mutation that can fail | No silent "optimistic only" |
| **Idempotency key** | Required for POST mutations that change state/cost money | Header `Idempotency-Key` |
| **Revalidation** | After mutation or on focus | Prevent drift |
| **Concurrency** | Cancel in-flight queries on mutate | Avoid overwriting with stale results |

## Real-world use case — Checkout (cart quantity)

**Context:** User increases cart quantity to 3. Optimistic update shows 3 and updates total.

**Failure:** Inventory check fails (only 1 left) — API returns `409 CONFLICT` with available quantity.

**Fix:** Rollback to previous quantity (2), show recoverable error "Only 1 left" with option to set to 1. Do **not** charge or assume success.

**Result:** No phantom quantity, correct UX, no lost update.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Pessimistic only | Safe, simple | Slower perceived UX | **Required** for payments/charges |
| Optimistic with rollback | Fast, good UX | Complex, easy to corrupt state | Safe for reversible, idempotent UI state |
| Optimistic without rollback | Fast | **Data corruption bug** | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Snapshot before mutate; rollback on error | Assume mutation succeeds |
| Use idempotency keys for POSTs | Optimistically charge cards |
| Reconcile on success/settle | Leave UI in optimistic state after failure |
| Cancel related queries on mutate | Let stale GET responses overwrite optimistic state |

## Common mistakes

- **No rollback context.** Lost previous state.
- **Retrying optimistic failure blindly.** May double-apply if not idempotent.
- **Stale cache wins.** Old response overwrites new optimistic state.
- **Optimistic for non-reversible.** Deletions can be tricky — consider undo vs hard delete.

## Checklist

- [ ] Every optimistic mutation has snapshot + rollback path.
- [ ] Financial/non-idempotent actions are pessimistic.
- [ ] Idempotency keys used for state-changing POSTs.
- [ ] Stale responses aborted/cancelled on mutation.
- [ ] Failure shows recoverable error with retry.

## Related

- [Network Failures, Timeouts, Cancellation](../01-concepts/05-network-timeouts-cancellation.md)
- [Retry/Recovery Controls](./03-state-transitions-retry-notifications-corruption.md)
- [Full-Stack — Optimistic Update Failures](../../38-full-stack-error-contracts/02-deep-dive/01-optimistic-update-failures-cross-platform.md)
