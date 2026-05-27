# Authentication Telemetry

## Overview

Authentication telemetry provides observability into login patterns, security events, and auth system health. This enables early detection of brute force attacks, credential stuffing, and anomalous login behavior while providing operational insights into auth system performance.

## Telemetry Architecture

```
[Auth Events] → [Event Bus] → [Telemetry Pipeline]
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌────────────┐ ┌────────────┐ ┌────────────────┐
            │ Metrics    │ │ Logs       │ │ Anomaly        │
            │ (Prometheus)│ │ (Elastic) │ │ Detection      │
            └────────────┘ └────────────┘ └────────────────┘
                    │               │               │
                    ▼               ▼               ▼
            ┌────────────┐ ┌────────────┐ ┌────────────────┐
            │ Grafana    │ │ Kibana     │ │ Alert Manager  │
            │ Dashboards │ │ Discovery  │ │ (PagerDuty)    │
            └────────────┘ └────────────┘ └────────────────┘
```

## Event Types

```typescript
interface AuthEvent {
  id: string;
  timestamp: string;
  type: AuthEventType;
  tenantId: string;
  userId?: string;
  ipAddress: string;
  userAgent: string;
  metadata: Record<string, unknown>;
}

type AuthEventType =
  | 'login.success'
  | 'login.failure'
  | 'login.locked'
  | 'logout'
  | 'password.change'
  | 'password.reset.request'
  | 'password.reset.complete'
  | 'mfa.challenge'
  | 'mfa.success'
  | 'mfa.failure'
  | 'session.refresh'
  | 'session.revoke'
  | 'token.invalid'
  | 'token.expired'
  | 'sso.login.success'
  | 'sso.login.failure'
  | 'account.created'
  | 'account.deleted'
  | 'account.suspended';
```

## Metrics Collection

```typescript
interface AuthMetrics {
  // Rate metrics
  loginAttempts: Counter;
  loginSuccesses: Counter;
  loginFailures: Counter;
  mfaChallenges: Counter;
  tokenRefreshes: Counter;

  // Latency metrics
  authLatency: Histogram;
  tokenValidationLatency: Histogram;
  mfaVerificationLatency: Histogram;

  // Gauge metrics
  activeSessions: Gauge;
  lockedAccounts: Gauge;
  concurrentUsersByTenant: GaugeMap;

  // Error tracking
  authErrorsByType: CounterMap;
  providerErrors: CounterMap;
}
```

### Prometheus Metric Definitions

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

export const authMetrics = {
  loginAttempts: new Counter({
    name: 'auth_login_attempts_total',
    help: 'Total login attempts',
    labelNames: ['tenant_id', 'provider', 'status'],
  }),

  authLatency: new Histogram({
    name: 'auth_latency_seconds',
    help: 'Authentication latency in seconds',
    labelNames: ['operation', 'provider'],
    buckets: [0.1, 0.25, 0.5, 1, 2, 5],
  }),

  activeSessions: new Gauge({
    name: 'auth_active_sessions',
    help: 'Currently active sessions',
    labelNames: ['tenant_id'],
  }),

  bruteForceLockouts: new Counter({
    name: 'auth_brute_force_lockouts_total',
    help: 'Accounts locked due to brute force detection',
    labelNames: ['tenant_id'],
  }),
};
```

## Anomaly Detection

### Impossible Travel Detection

```typescript
interface ImpossibleTravelDetector {
  async detect(request: AuthRequest): Promise<TravelRisk> {
    const { userId, ipAddress } = request;
    const lastLogin = await getLastLoginRecord(userId);

    if (!lastLogin) {
      return { risk: 'low', reason: 'first_login' };
    }

    const distance = calculateDistance(ipAddress, lastLogin.ipAddress);
    const timeSinceLast = Date.now() - lastLogin.timestamp.getTime();
    const speedKmh = distance / (timeSinceLast / 3600000);

    if (speedKmh > 900 && timeSinceLast < 3600000) {
      return {
        risk: 'critical',
        reason: 'impossible_travel',
        details: {
          distance_km: distance,
          previous_ip: lastLogin.ipAddress,
          current_ip: ipAddress,
          time_minutes: timeSinceLast / 60000,
        },
      };
    }

    if (speedKmh > 500) {
      return { risk: 'high', reason: 'unusual_travel_pattern' };
    }

    return { risk: 'low', reason: 'normal' };
  }
}
```

### Brute Force Protection

```typescript
interface BruteForceProtection {
  private attempts: Map<string, AttemptRecord[]>;

  async recordAttempt(key: string, success: boolean): Promise<LockoutStatus> {
    const now = Date.now();
    const window = await getConfig('brute_force_window_ms', 900000);
    const threshold = await getConfig('brute_force_threshold', 10);

    if (!this.attempts.has(key)) {
      this.attempts.set(key, []);
    }

    const records = this.attempts.get(key)!;
    records.push({ timestamp: now, success });

    // Clean old records outside window
    const recent = records.filter(r => now - r.timestamp < window);
    this.attempts.set(key, recent);

    // Check threshold
    const failures = recent.filter(r => !r.success).length;
    if (failures >= threshold) {
      return { locked: true, retryAfter: window, failureCount: failures };
    }

    return { locked: false, remainingAttempts: threshold - failures };
  }
}
```

## Alerting Rules

```typescript
// Prometheus alerting rules
const alertingRules = [
  {
    alert: 'HighLoginFailureRate',
    expr: 'rate(auth_login_failures_total[5m]) / rate(auth_login_attempts_total[5m]) > 0.3',
    for: '5m',
    labels: { severity: 'warning' },
    annotations: {
      summary: 'Login failure rate exceeds 30%',
    },
  },
  {
    alert: 'BruteForceAttack',
    expr: 'rate(auth_brute_force_lockouts_total[5m]) > 5',
    for: '2m',
    labels: { severity: 'critical' },
    annotations: {
      summary: 'Multiple accounts locked due to brute force',
    },
  },
  {
    alert: 'AuthLatencyHigh',
    expr: 'histogram_quantile(0.99, rate(auth_latency_seconds_bucket[5m])) > 3',
    for: '5m',
    labels: { severity: 'warning' },
    annotations: {
      summary: 'P99 auth latency exceeds 3 seconds',
    },
  },
];
```

## Telemetry Dashboard

Key dashboard panels:
- Login success/failure rate over time (per tenant)
- Active sessions trend (per tenant, last 24h)
- Auth latency heatmap (p50/p95/p99)
- Geographic login distribution
- Top failed authentication reasons
- Brute force lockout events timeline
- Auth provider health (upstream latency and error rate)

## Open-Source Tools

- **Prometheus** — Metrics collection and alerting
- **Grafana** — Dashboards and visualization
- **OpenTelemetry** — Distributed tracing for auth flows
- **Elasticsearch + Kibana** — Log aggregation and search
- **Alertmanager** — Alert routing and deduplication

## Production Considerations

- Ensure telemetry pipeline has sufficient capacity for login spikes (e.g., product launches)
- Never log passwords, tokens, or secrets in auth telemetry
- Aggregate metrics at tenant level to avoid high-cardinality issues
- Set up separate telemetry ingestion for auth events vs general application events
- Implement sampling for high-volume events (e.g., token validation) to reduce storage costs
- Store auth logs with shorter retention (30-90 days) and aggregate metrics longer (13 months)
- Include correlation IDs in all auth events for end-to-end tracing
