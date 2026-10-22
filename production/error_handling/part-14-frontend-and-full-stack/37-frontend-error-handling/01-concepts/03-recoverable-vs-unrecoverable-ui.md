# Recoverable vs Unrecoverable UI

> Part XIV · Chapter 37 · Sections 37.5–37.6 · _Estimated reading time: 15 min_
> **Prerequisite:** [Boundaries: Component, Page, App](./02-boundaries-component-page-app.md)

## In one sentence

**Design two modes:** *recoverable* failures let the user retry/reload a scoped action without losing critical work; *unrecoverable* failures cannot be safely resumed and must present a safe fallback with diagnostics and a hard path forward.

## Why this matters in production

For **Checkout**, losing cart items on a transient network blip is a conversion loss; crashing the cart is often unacceptable. For corrupted app state due to a persistent bug, retrying forever is unsafe. The decision must be explicit, not accidental.

## Core concept

| Aspect | Recoverable (37.5) | Unrecoverable (37.6) |
| ------ | ------------------- | --------------------- |
| **Definition** | Error is transient or scoped; safe to retry/reload the action/subtree. | Cannot restore correct state safely; continuing risks corruption or incorrect action. |
| **Examples** | Network timeout, 503, widget render fail, failed image load, pagination fetch fail | Corrupted cache schema after deploy, missing required config, invariant broken, repeated unrecoverable render error |
| **User affordance** | "Retry", "Reload this section", "Try again", inline retry | "Something went wrong", "Reload page", support link with `errorId` |
| **State** | Preserve form inputs, filters, selection, cart where possible | May need to clear corrupted keys; avoid auto-retry storms |
| **Logging** | Warn/info + context | Error with full diagnostics, alerting |

## Decision criteria

Ask these questions in order:

1. **Is the action idempotent?** If retrying could cause double charge, it must not auto-retry blindly (see [Part XI](../../../part-11-retry-and-resilience/README.md)).
2. **Can I restore inputs?** If user data would be lost, prefer scoped recovery.
3. **Is state consistent?** If local cache is corrupted, retrying the same broken state is unsafe.
4. **Is it a known transient?** Network/503/timeouts are often recoverable; invariant violations often not.

## Worked example

```tsx
function ExportJobChart() {
  const [state, setState] = useState({status:'idle'});
  async function load() {
    try {
      setState({status:'loading'});
      const data = await api.getExportChart();
      setState({status:'ok', data});
    } catch (e:any) {
      if (e.status >= 500 || e.name === 'NetworkError') {
        // Recoverable: scoped retry
        setState({status:'recoverable', error:e});
      } else {
        // Unexpected mapping -> may escalate
        setState({status:'unrecoverable', errorId: report(e)});
      }
    }
  }
  if (state.status==='recoverable') return <RetryCard onRetry={load} message="Couldn't load chart." />;
  if (state.status==='unrecoverable') return <FallbackCard errorId={state.errorId} />;
  ...
}
```

## Key data / numbers

| Scenario | Classification | Guidance |
| -------- | --------------- | -------- |
| **Network offline/timeout** | Recoverable | Retry with backoff; show "Offline" state. |
| **429 + Retry-After** | Recoverable (rate-limited) | Respect `Retry-After`; disable action until time. |
| **503** | Usually recoverable | Retry with jittered backoff. |
| **Render throw (first time)** | May be recoverable via boundary retry | Reset boundary state and retry; if repeats, escalate. |
| **Schema migration/cache corruption** | Often unrecoverable | Clear affected cache keys, reload or show fallback. |
| **Invariant violation** | Unrecoverable | Do not retry; log + alert; safe fallback. |

## Real-world use case — Checkout

**Context:** During **Checkout**, a shipping rate API times out.

**Failure:** Team shows a full-page crash with no way back to cart.

**Fix:** Treat as **recoverable** at the shipping section (component boundary). Preserve cart, shipping address, and payment method; show "Couldn't fetch shipping rates — retry" with a retry button. The cart remains intact.

**Result:** User retries or selects an alternative method without losing their order.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Always recoverable | User can retry anything | Can mask corruption, cause retry storms, dangerous for non-idempotent ops | Never blindly |
| Always unrecoverable | Safe | Poor UX, high bounce | Only for true corruption/invariants |
| Explicit classification | Safe + good UX | Requires decision criteria per flow | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Preserve critical work on recoverable failures | Clear form/cart on transient network error |
| Escalate repeated recoverable failures to unrecoverable | Auto-retry non-idempotent actions without backoff/confirmation |
| Give `errorId` on unrecoverable for support | Show internal messages on unrecoverable surfaces |
| Consider idempotency before retry | Retry POSTs that may have side effects blindly |

## Common mistakes

- **Losing inputs.** Reloading the whole page on a widget timeout.
- **Infinite retry.** Retrying a corrupted cache forever.
- **Treating 500 as always recoverable.** Some 500s indicate invariant bugs.

## Checklist

- [ ] For each critical flow, list recoverable vs unrecoverable cases.
- [ ] I preserve user inputs/state on recoverable failures.
- [ ] Non-idempotent actions have no auto-retry or require confirmation.
- [ ] Unrecoverable shows diagnostics id + safe fallback.

## Related

- [Boundaries: Component, Page, App](./02-boundaries-component-page-app.md)
- [Retry/Recovery Controls](../02-deep-dive/03-state-transitions-retry-notifications-corruption.md)
- [Retry and Resilience (Part XI)](../../../part-11-retry-and-resilience/README.md)
