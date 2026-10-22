# Optimistic Update Failures Across Full Stack

> Part XIV · Chapter 38 · Sections 38.10–38.11 · _Estimated reading time: 15 min_
> **Prerequisite:** [Chapter 37 — Stale Data, Refresh, Optimistic Rollback](../../37-frontend-error-handling/02-deep-dive/01-stale-data-refresh-optimistic-rollback.md), [Auth/Generated Clients](../01-concepts/04-generated-clients-auth-expiry-redirects.md)

## In one sentence

**Optimistic updates are client-side only: treat them as reversible UI previews, require server reconciliation/idempotency, rollback on failure, and enforce consistent behavior across web and mobile (38.10–38.11).**

## Optimistic update failures (38.10)

| Failure mode | Cause | Full-stack response |
| ------------ | ----- | ------------------- |
| **Validation rejection** | Business rules fail | Rollback, show field/summary via problem details mapping |
| **Concurrency conflict** | Another user changed resource | Rollback, refetch/reconcile (version conflict), offer "refresh and retry" |
| **Auth expiry mid-request** | 401 during optimistic POST | Queue via refresh flow (38.8), replay once, or rollback on final failure |
| **Rate limit** | `429` | Rollback, honor `Retry-After`, disable retry auto-spam |
| **Quota exceeded** | Business constraint | Rollback, CTA (upgrade) via code mapping |
| **Network timeout** | Transient | Rollback, show recoverable retry; do not assume success |
| **Server 5xx** | Infrastructure | Rollback, retry with backoff if idempotent |

**Hard rule:** Never commit optimistic state on failure. Store snapshot in mutation context, rollback exactly.

## Web/Mobile consistency (38.11)

| Aspect | Consistency requirement |
| ------ | ----------------------- |
| **Error codes** | Same enum/types (shared package) across web/mobile |
| **Mapping** | Same `ProblemDetails → UiAction` logic; platform renders differently |
| **Auth flow** | Same refresh semantics (single-flight/queue/intent) per platform |
| **Idempotency keys** | Generated same way; client must attach to POSTs |
| **Rollback behavior** | Identical semantics (snapshot/reconcile) |
| **Offline handling** | Define common policy (queue if idempotent, rollback on fail) |
| **Localization** | Shared code keys; platform-specific formatting only |

## Real-world use case — Acme SaaS "favorite project"

Optimistic toggle succeeds or fails same way on web/mobile. On conflict (another user archived project) → 409 with code → rollback + show toast "Project changed, refreshed".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Pessimistic across all | Consistent | Slower | Payments/critical |
| Optimistic with shared semantics | Fast + consistent | Coordination | Reversible actions |
| Platform-specific rollback | Flexible | Drift | Avoid |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize error mapping shared across platforms | Re-implement mapping per mobile/web |
| Require idempotency + reconciliation | Assume success |
| Rollback on any failure (including 401 after failed refresh) | Leave optimistic state after final failure |

## Checklist

- [ ] Snapshot + rollback enforced on all optimistic mutations
- [ ] Shared mapping/error codes for web/mobile
- [ ] Auth refresh flow consistent
- [ ] Idempotency keys attached to state-changing ops
- [ ] Concurrency conflicts handled explicitly

## Related

- [Chapter 37 — Optimistic Rollback](../../37-frontend-error-handling/02-deep-dive/01-stale-data-refresh-optimistic-rollback.md)
- [Auth Expiry Flow](../03-practical-examples/03-auth-expiry-refresh-flow-end-to-end.md)
- [Mapping API→UI](../01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)
