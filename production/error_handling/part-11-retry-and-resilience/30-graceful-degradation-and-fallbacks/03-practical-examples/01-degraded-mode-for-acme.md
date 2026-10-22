# Degraded Mode for Acme

> Part XI · Chapter 30 · Sections 30.1–30.15 · _Estimated reading time: 24 min_
> **Prerequisite:** [Partial Features, Degraded Mode, and Disabling Work](../01-concepts/03-partial-features-degraded-mode-and-disabling.md)

## In one sentence

Acme implements degraded mode as **one computed level plus a feature matrix**, exposed through the
same middleware to HTTP, UI, logs, and metrics — so an operator changes one number and every surface
agrees.

## Why this matters in production

Degraded mode fails when it lives in three places: a config flag, a hard-coded list of disabled
features, and a status page updated by hand. This implementation makes the level the single source of
truth, computes it from dependency health with hysteresis, and derives every feature decision from the
matrix. It also shows how manual pins interact with automatic detection, and how the mode is
communicated to clients without leaking internals.

## The level model

| Level | Name | Entry condition | User-visible effect |
| ----- | ---- | --------------- | ------------------- |
| 0 | Normal | All required + important healthy | None |
| 1 | Reduced | Optional dependency down | Hide/label optional features |
| 2 | Essential | Important dependency down | Core tasks only |
| 3 | Read-only | Primary writer unavailable | Writes rejected |
| 4 | Unavailable | Auth or primary DB down | Maintenance page |

Each level is a superset of the one above: level 2 behaves like level 1 plus more restrictions. That
makes the matrix easy to reason about and prevents gaps.

## The feature matrix

```ts
export type Level = 0 | 1 | 2 | 3 | 4;

type Behavior = "on" | "reduced" | "deferred" | "off" | "readonly";

export const MATRIX: Record<Level, Record<string, Behavior>> = {
  0: { checkout: "on", auth: "on", search: "on", recommendations: "on",
       llm_summary: "on", exports: "on", emails: "on", analytics: "on" },
  1: { checkout: "on", auth: "on", search: "reduced", recommendations: "off",
       llm_summary: "reduced", exports: "on", emails: "on", analytics: "on" },
  2: { checkout: "on", auth: "on", search: "reduced", recommendations: "off",
       llm_summary: "off", exports: "deferred", emails: "deferred", analytics: "off" },
  3: { checkout: "readonly", auth: "on", search: "reduced", recommendations: "off",
       llm_summary: "off", exports: "off", emails: "deferred", analytics: "off" },
  4: { checkout: "off", auth: "off", search: "off", recommendations: "off",
       llm_summary: "off", exports: "off", emails: "off", analytics: "off" },
};
```

Matrix rules:

- **Required** capabilities are `on` or `off`/`readonly`, never `reduced`.
- Letter levels never *increase* a feature's behavior.
- `deferred` means "accept and process later," not "drop."
- Changing the matrix requires the same review as a product change.

## Computing the level

```ts
interface HealthInputs {
  auth: { healthy: boolean };
  primaryDb: { healthy: boolean; writable: boolean };
  importantDeps: string[];   // e.g. ["search", "tax"]
  optionalDeps: string[];    // e.g. ["llm", "email", "recommender"]
  utilization: number;
}

export function computeLevel(h: HealthInputs): Level {
  if (!h.auth.healthy || !h.primaryDb.healthy) return 4;
  if (!h.primaryDb.writable) return 3;
  if (h.importantDeps.some((d) => deps.down(d))) return 2;
  if (h.optionalDeps.some((d) => deps.down(d)) || h.utilization > 0.85) return 1;
  return 0;
}
```

### Hysteresis and manual pins

```ts
class ModeController {
  private current: Level = 0;
  private lastChange = 0;
  private manual: Level | null = null;

  constructor(
    private readonly minDwellMs = 60_000,
    private readonly recoveryHoldMs = 120_000,
    private readonly now = Date.now,
  ) {}

  evaluate(h: HealthInputs): Level {
    const auto = computeLevel(h);
    const target = this.manual !== null ? Math.max(auto, this.manual) : auto;

    if (target === this.current) return this.current;
    if (this.now() - this.lastChange < this.minDwellMs) return this.current;

    // Recovering (level decreasing) waits longer to avoid flapping.
    if (target < this.current && this.now() - this.lastChange < this.recoveryHoldMs) {
      return this.current;
    }

    this.current = target;
    this.lastChange = this.now();
    metrics.gauge("degraded_mode", target);
    log.warn({ level: target, manual: this.manual }, "degraded mode changed");
    return this.current;
  }

  pin(level: Level | null) {
    this.manual = level;
  }
}
```

The effective level is `max(auto, manual)`: an operator can escalate but never force the system below
its detected level.

### Recovery hold

Recovery is slower than degradation on purpose:

| Direction | Hold |
| --------- | ---- |
| Worsening | 60s minimum dwell |
| Improving | 2× breaker cooldown (e.g. 120s) |

This prevents oscillation while a dependency is half-recovered.

## Request middleware

```ts
export function degradedMode(controller: ModeController) {
  return async (req: Request, res: Response, next: Next) => {
    const level = controller.current;
    const feature = featureForRoute(req.route);
    const behavior = MATRIX[level][feature] ?? "on";

    res.setHeader("X-Degraded-Mode", String(level));
    if (level > 0) res.setHeader("X-Degraded-Features", disabledList(level).join(","));

    if (behavior === "off") {
      return res.status(503).json({
        error: {
          code: "FEATURE_UNAVAILABLE",
          message: "This feature is temporarily unavailable.",
          retryable: true,
          retry_after_s: 30,
        },
      });
    }

    if (behavior === "readonly" && req.method !== "GET") {
      return res.status(503).json({
        error: { code: "READ_ONLY_MODE", message: "Changes are temporarily unavailable.", retryable: true },
      });
    }

    (req as any).degraded = { level, feature, behavior };
    next();
  };
}
```

### Handling `reduced` and `deferred`

- `reduced`: the handler checks `req.degraded.behavior` and selects the partial implementation.
- `deferred`: the handler enqueues work and returns `202 Accepted` with a `Location` to the job.

```ts
if (req.degraded?.behavior === "deferred") {
  const job = await jobs.enqueue({ type: "export", tenantId, deadlineMs: Date.now() + 3_600_000 });
  return res.status(202).json({ job_id: job.id, status: "deferred" });
}
```

## Communication surfaces

### HTTP

```http
HTTP/1.1 200 OK
X-Degraded-Mode: 1
X-Degraded-Features: recommendations,llm_summary
X-Data-As-Of: 2026-10-21T09:12:00Z
Warning: 199 - "Some features are temporarily limited"
```

### UI

```ts
function bannerFor(level: Level) {
  if (level === 0) return null;
  if (level === 1) return "Some features are temporarily limited. Core functionality is unaffected.";
  if (level === 2) return "We're experiencing higher load. Some features are paused to keep things running.";
  if (level === 3) return "You can browse, but changes are temporarily unavailable.";
  return "We're performing maintenance and will be back shortly.";
}
```

Per-widget states:

| Feature | Level 1 UI |
| ------- | ---------- |
| Recommendations | Hidden, no placeholder |
| LLM summary | "Summary unavailable" |
| Search | "Showing basic results" |
| Exports | Normal or "processing" |
| Emails | Normal |

### Operators

Every log line carries `degraded_mode` and the request's feature, so a query can show which features
are being exercised in a degraded state. Metrics:

```text
degraded_mode{level}
degraded_requests_total{level,feature}
fallback_used_total{feature,source}
manual_pin_active{level}
```

## Incident workflow

```text
1. Alert fires (breaker open / error rate).
2. Controller auto-escalates within 5s + dwell.
3. Incident commander confirms level on the status page.
4. If the auto level is too low, pin a higher level.
5. Fix the dependency; breaker probes.
6. Controller holds recovery for 2× cooldown, then lowers the level.
7. Clear the manual pin only after the auto level is stable.
8. Postmortem reviews matrix and thresholds.
```

## Testing

```ts
it("escalates to level 2 when an important dependency is down", () => {
  const c = new ModeController(0, 0, () => now);
  expect(c.evaluate({ ...healthy, importantDeps: ["tax"] })).toBe(2);
});

it("never goes below an operator pin", () => {
  const c = new ModeController(0, 0, () => now);
  c.pin(3);
  expect(c.evaluate(healthy)).toBe(3);
});

it("rejects writes in read-only mode", async () => {
  const res = await request(app).post("/orders").set("X-Test-Level", "3");
  expect(res.status).toBe(503);
  expect(res.body.error.code).toBe("READ_ONLY_MODE");
});
```

Fault injection: force each level in staging and run the full checkout, export, and webhook flows.

## Key data / numbers

- Levels: **5** (0–4).
- Dwell before worsening: **60s**; recovery hold: **2× cooldown (~120s)**.
- Auto recompute interval: **5s**.
- Level-1 triggers: optional dependency down or utilization **> 85%**.
- Manual pin: escalates only; `effective = max(auto, manual)`.
- Deferred work: `202` + job id, never silently dropped.

## Real-world use case — Acme SaaS

Acme introduced the matrix after a tax-service outage caused every checkout to fail. The new behavior:
tax down → level 2 → tax estimate shown as "estimated, confirmed at payment," but **charge** blocked
(fail-closed). Checkout stayed visible, conversion fell only ~8% during the outage instead of going to
zero, and support had a single banner to reference. The matrix review also revealed that `analytics`
was consuming 6% of worker capacity during incidents; it is now shed at level 2.

## Trade-offs

| Choice | Benefit | Cost |
| ------ | ------- | ---- |
| Coarse levels | Simple operations | Some features over-restricted |
| Fine matrix | Precise | More review surface |
| Auto + manual max | Safe | Operators cannot force normal |
| Slow recovery | No flapping | Longer degraded period |
| `deferred` for exports | No data loss | Delayed user feedback |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive behavior from one level | Hard-code disabled features per route |
| Keep required features binary | "Reduce" payment or auth |
| Use `max(auto, manual)` | Let a pin force normal |
| Hold recovery for 2× cooldown | Flip back the instant a probe succeeds |
| Return `202` for deferred work | Drop jobs silently |
| Expose the level on every surface | Only update the status page |

## Common mistakes

- **Level computed from error rate only**, missing latency and saturation.
- **Matrix drift**, where a route is missing from the map and silently defaults to `on`.
- **Manual pin forgotten** after the incident, leaving the system degraded for days.
- **`reduced` applied to required data**, producing incorrect money.
- **No test at level 3**, so read-only mode breaks on a write path.

## Checklist

- [ ] Five levels with documented entry conditions.
- [ ] Feature matrix covers every route/capability.
- [ ] Required features are never `reduced`.
- [ ] Level computed from health + utilization.
- [ ] Worsening and recovery have hysteresis.
- [ ] Manual pins can only escalate.
- [ ] Middleware rejects `off`/`readonly` consistently.
- [ ] UI, logs, metrics, and status page show the same level.
- [ ] Every level is exercised in staging.

## Related

- [Partial Features, Degraded Mode, and Disabling Work](../01-concepts/03-partial-features-degraded-mode-and-disabling.md)
- [Fallback Chains](../02-deep-dive/01-fallback-chains.md)
- [Fallback Chain for LLM Summary](./02-fallback-chain-llm-summary.md)
- [Chapter 30 Reference](../05-reference/README.md)
