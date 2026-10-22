# Practical — Partial-Success Aggregation for Acme's Dashboard

> Part XII · Chapter 31 · Sections 31.5–31.7, 31.10 · _Estimated reading time: 18 min_
> **Prerequisite:** [Concurrent Failures and Aggregation](../01-concepts/02-concurrent-failures-and-aggregation.md)

## Scenario

Acme's dashboard loads data from six sources. Three are **required** (account, invoices, quota);
three are **optional** (activity feed, recommendations, usage chart). Optional sources are slow and
occasionally unavailable. The old handler used one `Promise.all` for all six, so a single optional
timeout blanked the whole page with a `500`.

The goal: **required data fails the request; optional data degrades gracefully and is reported.**

## Contract first

Before writing code, define what the client receives:

```ts
type DashboardResponse = {
  account: Account;
  invoices: InvoiceSummary[];
  quota: Quota;
  widgets: {
    activity: ActivityItem[] | null;
    recommendations: Recommendation[] | null;
    usage: UsagePoint[] | null;
  };
  degraded: Array<{
    widget: string;
    code: string;       // stable, e.g. ACTIVITY_TIMEOUT
    retryable: boolean;
  }>;
};
```

`null` means "unavailable," not "empty." The client renders a placeholder from `degraded` and can
show a retry control for `retryable: true`.

## Step 1 — Classify the failures

```ts
type Failure = { code: string; retryable: boolean };

function classify(err: unknown): Failure {
  if (isTimeout(err)) return { code: "SOURCE_TIMEOUT", retryable: true };
  if (isAbort(err)) return { code: "SOURCE_CANCELLED", retryable: false };
  if (isHttpStatus(err, 429)) return { code: "SOURCE_RATE_LIMITED", retryable: true };
  if (isHttpStatus(err, 403)) return { code: "SOURCE_FORBIDDEN", retryable: false };
  return { code: "SOURCE_FAILED", retryable: true };
}
```

Classification is what makes the `degraded` array actionable. "Something failed" is not.

## Step 2 — Required sources: fail fast

```ts
async function loadRequired(tenantId: string, signal: AbortSignal) {
  return Promise.all([
    accounts.get(tenantId, { signal }),
    invoices.recent(tenantId, { signal }),
    quota.get(tenantId, { signal }),
  ]);
}
```

If any required source fails, the request fails. The signal lets us abort siblings so a failed
required source does not leave two queries running.

## Step 3 — Optional sources: collect all

```ts
type WidgetResult<T> =
  | { ok: true; value: T }
  | { ok: false; failure: Failure };

async function optional<T>(
  name: string,
  run: (signal: AbortSignal) => Promise<T>,
  signal: AbortSignal,
): Promise<WidgetResult<T>> {
  try {
    return { ok: true, value: await run(signal) };
  } catch (err) {
    return { ok: false, failure: classify(err) };
  }
}
```

Each optional branch catches **inside** its own promise, so `allSettled` never sees a rejection and
we keep per-widget typing. This is stronger than filtering `allSettled` results because the failure
is already classified at the source.

## Step 4 — Assemble with a deadline

```ts
const DEADLINE_MS = 4_000;

export async function getDashboard(tenantId: string, clientSignal: AbortSignal) {
  const deadline = Date.now() + DEADLINE_MS;
  const signal = AbortSignal.any([
    clientSignal,
    AbortSignal.timeout(DEADLINE_MS),
  ]);

  const [account, invoiceList, quota] = await loadRequired(tenantId, signal);

  const optionalResults = await Promise.all([
    optional("activity", (s) => activity.recent(tenantId, { signal: s }), signal),
    optional("recommendations", (s) => recs.forTenant(tenantId, { signal: s }), signal),
    optional("usage", (s) => usage.series(tenantId, { signal: s }), signal),
  ]);

  const degraded = optionalResults.flatMap((r, i) =>
    r.ok ? [] : [{ widget: WIDGETS[i], code: r.failure.code, retryable: r.failure.retryable }],
  );

  const value = (i: number) => {
    const r = optionalResults[i];
    return r.ok ? r.value : null;
  };

  return {
    account,
    invoices: invoiceList,
    quota,
    widgets: {
      activity: value(0),
      recommendations: value(1),
      usage: value(2),
    },
    degraded,
  } satisfies DashboardResponse;
}
```

Note the `signal` is shared, so when the overall deadline fires, **all still-running optional
queries abort** rather than continuing in the background.

## Step 5 — Track degradation as a metric

```ts
for (const item of degraded) {
  metrics.increment("dashboard_widget_degraded", {
    widget: item.widget,
    code: item.code,
  });
}
```

This turns "the dashboard feels slow" into a per-widget failure rate you can alert on. A widget
that degrades for 20% of tenants is a dependency problem, not a UI problem.

## Result

```json
{
  "account": { "id": "acct_123", "plan": "pro" },
  "invoices": [{ "id": "inv_9", "total": 4900 }],
  "quota": { "used": 820, "limit": 1000 },
  "widgets": {
    "activity": [{ "id": "evt_1", "kind": "comment" }],
    "recommendations": null,
    "usage": [{ "day": "2026-10-20", "value": 42 }]
  },
  "degraded": [
    { "widget": "recommendations", "code": "SOURCE_TIMEOUT", "retryable": true }
  ]
}
```

The page renders with one placeholder; the other five panels are usable. Without the change, this
same incident returned `500` to every user on the tenant.

## Why not just wrap everything in `allSettled`?

`allSettled` alone gives you untyped `reason` values and no distinction between required and
optional. You would still have to:

1. decide which rejections are fatal,
2. classify each reason,
3. abort siblings when a required branch fails.

The explicit split above makes those decisions **visible in the code** instead of implicit in a
`flatMap` over statuses.

## Failure-mode review

| What fails | Behavior | Customer impact |
| ---------- | -------- | --------------- |
| Account query | Request fails, siblings aborted | Cannot load dashboard (correct) |
| Activity timeout | Placeholder + `degraded` entry | One card unavailable |
| Recommendations `403` | Placeholder, non-retryable | One card permanently off |
| Overall deadline | All optional aborted, required already done | Page loads with placeholders |
| Client disconnects | Signal aborts everything; no response | No wasted provider calls |

## Real-world use case — Acme SaaS

After shipping this, Acme's dashboard `5xx` rate during a recommendations outage dropped from 38% of
page loads to **0%**; only the recommendations card degraded. The `degraded` metric also revealed
that the recommendations provider timed out for one large tenant every morning at 09:00, which led
to a dedicated read replica rather than an alert nobody read.

## Key data / numbers

- Overall dashboard deadline: **4 s** (below the 5 s client fetch timeout).
- Optional branch classification codes: `SOURCE_TIMEOUT`, `SOURCE_RATE_LIMITED`,
  `SOURCE_FORBIDDEN`, `SOURCE_FAILED`.
- `AbortSignal.timeout` produces `TimeoutError`; `controller.abort()` produces `AbortError`.
- Fan-out is bounded at six branches; no pool needed, but a 20-widget dashboard should cap at ~10.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Separate required vs optional branches | One `Promise.all` for everything |
| Classify failures at the source | Return raw `reason` to the client |
| Return `null` + `degraded[]` | Return `200` with silently empty arrays |
| Abort siblings on required failure | Leave queries running after `500` |
| Emit a per-widget degradation metric | Only log a generic warning |

## Checklist

- [ ] Required and optional branches are separated in code.
- [ ] Every optional failure is classified into a stable code.
- [ ] `degraded` distinguishes retryable from terminal.
- [ ] One shared deadline aborts all in-flight branches.
- [ ] Client renders placeholders, not fake empty data.
- [ ] Degradation is measured per widget.

## Related

- [Promise.all vs allSettled — Mechanics](../02-deep-dive/01-promise-all-vs-allsettled.md)
- [Concurrent Failures and Aggregation](../01-concepts/02-concurrent-failures-and-aggregation.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Promise.all vs Promise.allSettled](../02-deep-dive/01-promise-all-vs-allsettled.md)
