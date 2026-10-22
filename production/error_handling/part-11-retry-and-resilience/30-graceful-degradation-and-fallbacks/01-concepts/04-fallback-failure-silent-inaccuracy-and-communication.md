# Fallback Failure, Silent Inaccuracy, and Communication

> Part XI · Chapter 30 · Sections 30.10–30.12 · _Estimated reading time: 20 min_
> **Prerequisite:** [Partial Features, Degraded Mode, and Disabling Work](./03-partial-features-degraded-mode-and-disabling.md)

## In one sentence

A fallback can fail too — and when it fails **silently**, it turns an availability incident into a
correctness incident; so every fallback needs a terminal error path and every degraded response needs
to say, in one place, that it is degraded.

## Why this matters in production

The dangerous failure is not the request that returns `503`. It is the request that returns `200` with
an empty list, a zero balance, a default tax rate, or a week-old snapshot, and lets the user believe it
is the truth. Silent inaccuracy erodes trust, causes wrong business decisions, and is much harder to
debug than an outage. Fallback failure is the sibling problem: a fallback that throws an unhandled
error, or that itself calls the primary, can cascade the incident to a second dependency.

## 30.10 — Fallback failure

### Ways a fallback fails

| Failure | Example | Result |
| ------- | ------- | ------ |
| **Throws** | Cache client also down | Unhandled error, 500 |
| **Times out** | Fallback queries a slow replica | Latency exceeds budget |
| **Recurses** | Fallback calls the primary again | Amplification / loop |
| **Returns wrong shape** | Template missing required field | Client crash |
| **Returns invalid data** | Default coordinates `(0,0)` | Silent wrongness |
| **Cascades** | Fallback depends on another failing service | Two outages |

### Make the fallback a first-class call

```ts
async function withFallback<T>(
  primary: () => Promise<T>,
  fallback: () => Promise<T>,
  budgetMs: number,
): Promise<{ value: T; degraded: boolean }> {
  try {
    return { value: await primary(), degraded: false };
  } catch (primaryErr) {
    // The fallback gets its own small budget and never re-calls the primary.
    try {
      const value = await withTimeout(fallback(), Math.min(budgetMs, 500));
      return { value, degraded: true };
    } catch (fallbackErr) {
      throw new BothFailedError(primaryErr, fallbackErr);
    }
  }
}
```

`BothFailedError` is a **first-class terminal state**, not an afterthought. It must carry both causes
for diagnosis, and it must map to a clear response (`503`), never to a default value.

### Loop and cascade protection

```text
primary → fails
fallback A (cache) → fails
fallback B (replica read) → replica is the failing dependency → must not be tried
→ terminal error
```

Tag each fallback with the dependencies it needs and skip any whose breaker is open. A fallback must
never be able to invoke the primary that just failed.

## 30.11 — Avoiding silent inaccuracy

Silent inaccuracy happens when the response is **well-formed but wrong**, and nothing marks it.

### High-risk patterns

| Pattern | Why it is dangerous |
| ------- | ------------------- |
| `catch { return [] }` | Empty looks like "none" |
| `catch { return null }` for totals | `null` rendered as `0` |
| Default tax/shipping rate | Under- or overcharges |
| `Date.now()` as a timestamp | Looks live, isn't |
| Last-known permissions | Grants access that was revoked |
| Stale balance shown as current | Financial decisions on old data |
| Fallback text presented as AI output | Misrepresents provenance |
| Swallowed partial batch failure | "All succeeded" is false |

### Defences

1. **Never use a bare `catch` that returns a default** for required data.
2. **Attach provenance** to every value: `{ value, source, asOf, degraded }`.
3. **Assert in the type system** that degraded responses carry a marker.

```ts
type Sourced<T> =
  | { value: T; source: "live"; asOf: number }
  | { value: T; source: "cache" | "template"; asOf: number; degraded: true };

function requireLive<T>(s: Sourced<T>): T {
  if (s.degraded) throw new DegradedDataError(s.source, s.asOf);
  return s.value;
}
```

`requireLive` makes the dangerous path explicit: monetary calculations call it, display code may not.

### The "would a user act differently?" test

If the user knew the data was stale or substituted, would they make a different decision? If yes, the
degradation **must** be visible and, for required data, the response must fail instead.

## 30.12 — Communicating degradation

Communication has four audiences, and they must agree.

| Audience | Channel | Example |
| -------- | ------- | ------- |
| **API caller** | Status + headers + body | `200`, `Warning`, `degraded: true` |
| **End user** | UI copy | "Rates delayed — showing last known values" |
| **Operator** | Logs + metrics | `degraded_mode=1`, `fallback_used_total` |
| **Status page** | Incident note | "AI summaries temporarily unavailable" |

### API contract

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Degraded: recommendations,v2-summary
X-Degraded-Reason: dependency_unavailable
X-Data-As-Of: 2026-10-21T09:12:00Z
Warning: 199 - "Response contains degraded data"

{
  "items": [],
  "degraded": true,
  "degraded_parts": ["recommendations", "summary"],
  "as_of": "2026-10-21T09:12:00Z",
  "notice": "Some recommendations are unavailable."
}
```

Rules:

- **One vocabulary.** Pick header names and body fields and use them everywhere.
- **Machine-readable first.** `X-Degraded` is a list of part names, not prose.
- **Human copy second.** The `notice` is for display, not parsing.
- **No leaking internals.** Do not put provider names, hostnames, or stack traces in the notice.

### UI copy guidelines

| Situation | Say | Avoid |
| --------- | --- | ----- |
| Stale data | "Updated 2 hours ago" | "Live" |
| Feature off | "Temporarily unavailable" | Blank area |
| Reduced quality | "Basic results" | Pretending full |
| Queued action | "We'll email you shortly" | "Sent" |
| Partial failure | "3 of 5 items loaded" | "Loaded" |

### Observability

```text
fallback_used_total{dependency,fallback}
fallback_failed_total{dependency,fallback}
degraded_response_total{part}
degraded_mode{level}
stale_served_total{dataset,age_bucket}
```

Alert when `fallback_failed_total` rises (fallback itself is unhealthy) and when a required dataset is
served stale (should be an error, not an alert-only event).

## Worked example — the empty recommendations bug

Acme's product page did this:

```ts
let recs: Item[] = [];
try { recs = await recommender.forUser(user.id); } catch {}
return { recs };
```

During an outage, every page showed no recommendations. The UI displayed "No recommendations yet," and
the merchandising team concluded users had lost interest. Nobody noticed the outage for two days.

The fix:

```ts
const recs = await withFallback(
  () => recommender.forUser(user.id),
  () => popularItems(),          // cheap, correct substitute
  300,                            // fallback budget
);
return {
  recs: recs.value,
  degraded: recs.degraded,
  notice: recs.degraded ? "Showing popular items instead of personalized picks." : undefined,
};
```

Now the page stays useful, the data is honest, and `fallback_used_total` fires within seconds.

## Key data / numbers

- Fallback budget: **≤ 20%** of the remaining deadline, often **≤ 500ms**.
- Required-data staleness tolerance: **0** — fail instead.
- Display-data tolerance: **minutes–hours**, with `as_of`.
- Alerts on `fallback_failed_total` within **5 minutes**.
- Degraded marker: **one** header convention + **one** body field.
- Loop protection: fallbacks must not depend on the primary's dependency.

## Real-world use case — Acme SaaS

A tax provider outage caused Acme to fall back to a hard-coded 10% tax rate. Orders were accepted with
wrong tax, and finance discovered the discrepancy a month later. The postmortem changed the
classification: tax is **required**, so the endpoint now fails closed with `503` and a clear message.
The fallback remains only for the **estimate** shown before checkout, labelled "estimated tax." The
incident also introduced `fallback_used_total` and a dashboard panel for stale financial data.

## Trade-offs

| Approach | Availability | Correctness | Trust |
| -------- | ------------ | ----------- | ----- |
| Silent default | High | Low | Low |
| Visible fallback | High | Medium–High | High |
| Fail closed | Low | High | High |
| Both-failed terminal error | Low | High | High |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give the fallback its own budget | Let it run unbounded |
| Wrap fallback errors as terminal | Let them become 500s |
| Skip fallbacks whose dependency is down | Cascade into a second outage |
| Label every degraded response | Return a well-formed lie |
| Use one header vocabulary | Invent a new field per endpoint |
| Alert on fallback use/failure | Wait for a customer report |

## Common mistakes

- **Bare `catch {}` returning a default**, the canonical silent-inaccuracy bug.
- **Fallback re-calls the primary**, causing amplification.
- **Wrong-shaped fallback**, crashing clients.
- **No `as_of`**, so stale data looks live.
- **Provider names in user-facing notices**, leaking internals.
- **No metric on fallback use**, so nobody knows it happened.

## Checklist

- [ ] Every fallback has a budget and a timeout.
- [ ] Fallback errors become a terminal `BothFailedError`.
- [ ] Fallbacks cannot call the primary or depend on the failed dependency.
- [ ] Required data never silently defaults.
- [ ] Degraded responses carry a machine-readable marker and `as_of`.
- [ ] UI copy states what is degraded.
- [ ] Fallback use and failure are counted and alerted.
- [ ] Notices contain no internal details.

## Related

- [Fallback Responses and Cached Fallbacks](./02-fallback-responses-and-cached-fallbacks.md)
- [Fallback Chains](../02-deep-dive/01-fallback-chains.md)
- [Fail-Open vs Fail-Closed](../02-deep-dive/02-fail-open-vs-closed.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
