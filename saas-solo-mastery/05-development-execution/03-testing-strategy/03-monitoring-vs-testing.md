# Monitoring vs. Testing for Solo Founders

## The Testing Paradox

The more tests you write, the slower you ship. The fewer tests you write, the more bugs you ship. For solo founders, there's a third path: **shift testing to production**.

Production monitoring catches real bugs affecting real users, while testing catches theoretical bugs in artificial environments. For a solo founder with limited time, monitoring provides more value per minute invested than testing — especially once you have users.

This isn't an argument against testing. It's an argument for a balanced strategy where monitoring catches what tests miss.

---

## 1. Why Monitoring Is a Testing Strategy

### The Testing Safety Net

- **Unit tests**: Does this function work correctly? (You hope)
- **Integration tests**: Do these components work together? (You think)
- **E2E tests**: Can users complete this flow? (You believe)
- **Production monitoring**: What's actually happening with real users? (You know)

Production monitoring is the only testing strategy that uses real data, real users, and real conditions. It catches:
- Edge cases you didn't think of
- Browser-specific issues your tests didn't cover
- Performance problems that only appear under load
- User behavior that differs from your assumptions

### The Monitoring Advantage

| Test Type | Catches | Misses | Time Investment |
|-----------|---------|--------|-----------------|
| Unit tests | Logic errors | Integration issues | Medium |
| Integration | Component interaction | Real-world conditions | Medium |
| E2E tests | Critical path breaks | Edge cases, performance | High |
| Monitoring | Real bugs in production | Theoretical issues not yet encountered | Low |

---

## 2. Error Tracking

### Why Error Tracking Is Essential

Error tracking is the single most important monitoring tool for a solo founder. It tells you:
- What broke
- Who it affected
- When it happened
- How to reproduce it

Without error tracking, you're flying blind. Users encounter errors silently and leave without telling you.

### Setting Up Error Tracking

**Sentry** (free tier: 5,000 events/month):

```bash
npm install @sentry/nextjs
```

```typescript
// sentry.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,          // Sample 10% of transactions
  replaysSessionSampleRate: 0.1,  // Session replays
  environment: process.env.NODE_ENV,
})
```

**PostHog** (free tier: included):

```typescript
// PostHog includes error tracking
import { posthog } from 'posthog-js'

try {
  // risky operation
} catch (error) {
  posthog.capture('Error Occurred', {
    error: error.message,
    stack: error.stack,
    page: window.location.pathname,
  })
}
```

### What to Track

**Must track**:
- Unhandled exceptions (crashes)
- API errors (4xx, 5xx responses)
- Failed database queries
- Payment failures
- Authentication errors

**Nice to track**:
- Slow API responses (> 1 second)
- Client-side console errors
- Failed form submissions
- Timeout errors

### Alerting

Configure alerts for:
- **P0**: Payment failures, data loss, security issues → Notify immediately (SMS/call)
- **P1**: API returning 500 errors for > 1% of requests → Notify within 5 minutes (email)
- **P2**: New error type occurring for > 10 users → Daily digest

---

## 3. User Session Replay

### What Is Session Replay

Session replay records user interactions (clicks, scrolls, navigation) and lets you watch them. It's like being in the room with the user, watching them use your product.

**Tools**:
- **PostHog** (free tier: included with analytics)
- **FullStory** (free tier: 5,000 sessions/month)
- **Hotjar** (free tier: 35 daily sessions)
- **Clarity** (free, unlimited)

### What Session Replay Reveals

Session replay catches issues that NO test would ever catch:

1. **Confusion**: User hesitates, clicks around, can't find what they need
2. **Misunderstanding**: User clicks the wrong thing because the label is unclear
3. **Frustration**: User fills out a form, clicks submit, nothing happens
4. **Workarounds**: User finds a hacky way to achieve their goal
5. **Abandonment**: User leaves because they can't figure something out
6. **Rage clicks**: User clicks the same spot repeatedly
7. **Dead clicks**: User clicks on something that isn't interactive

### How to Use Session Replay

**Daily (5 minutes)**: Watch 3 sessions at 4x speed
**Weekly (15 minutes)**: Watch sessions from churned users
**Per feature launch**: Watch 10 sessions of the new feature

**Systematic approach**:
1. Filter sessions by key events (error, rage click, churn)
2. Watch at 2-4x speed
3. Note friction points
4. Prioritize fixes
5. Check if fixes worked (compare before/after)

### The Session Triage

```
Session | Behavior | Issue | Action
--------|----------|-------|-------
User clicks "Save" 5x | Save button has no loading state | Add spinner on submit | Fix today
User scrolls pricing page 3x | Pricing unclear | Add comparison table | This sprint
User enters wrong password 4x | Password reset link not visible | Move reset link above fold | Quick fix
```

---

## 4. Performance Monitoring

### What to Monitor

**Frontend**:
- Largest Contentful Paint (LCP) — How fast does the main content load?
- First Input Delay (FID) — How responsive is the page?
- Cumulative Layout Shift (CLS) — Does the page jump around?
- Time to First Byte (TTFB) — How fast is the server?

**Backend**:
- API response times (p50, p95, p99)
- Database query performance
- Error rate by endpoint
- Memory and CPU usage

### Tools

**Vercel Analytics** (free): Frontend performance, Web Vitals
**Sentry Performance** (free tier): Backend tracing
**Lighthouse CI**: Performance regression detection
**Self-hosted**: Grafana + Prometheus (if needed)

### Setting Up Performance Monitoring

```typescript
// Web Vitals (Next.js)
import { useReportWebVitals } from 'next/web-vitals'

export function Analytics() {
  useReportWebVitals((metric) => {
    posthog.capture('Web Vital', {
      name: metric.name,
      value: metric.value,
      rating: metric.rating,
    })
  })
}
```

### Performance Budgets

Set budgets and alert when exceeded:

| Metric | Good | Needs Work | Poor | Alert |
|--------|------|------------|------|-------|
| LCP | < 1.5s | < 2.5s | > 2.5s | Daily |
| FID | < 50ms | < 100ms | > 100ms | Daily |
| CLS | < 0.1 | < 0.25 | > 0.25 | Weekly |
| API p95 | < 500ms | < 1s | > 1s | Alert |

---

## 5. Analytics as Testing

### Behavioral Analytics as Bug Detection

Analytics can reveal bugs before error tracking catches them:

- **Signup conversion drops**: Signup flow might be broken
- **Feature usage drops**: Feature might be broken or confusing
- **Page views drop**: Page might not be loading
- **Bounce rate spikes**: Something is driving users away

### Setting Up Behavioral Monitoring

```typescript
// Track key events for anomalies
posthog.capture('Signup Completed', {
  method: 'google',
  time_to_complete: 45,
})

posthog.capture('Project Created', {
  project_type: 'personal',
})

posthog.capture('Payment Completed', {
  plan: 'pro',
  amount: 29,
  currency: 'USD',
})
```

### Anomaly Detection

Monitor these metrics for sudden changes:

| Event | Expected Rate | Investigate If |
|-------|---------------|----------------|
| Signup completion | 80%+ | Drops below 60% |
| Trial activation | 40%+ | Drops below 20% |
| Payment success | 95%+ | Drops below 85% |
| API success | 99%+ | Drops below 95% |
| Daily active users | Stable/Up | Sudden drop > 10% |

---

## 6. Logging Strategy

### What to Log

**Every API request**:
```typescript
// Structured logging
logger.info('API request', {
  method: req.method,
  path: req.url,
  userId: req.user?.id,
  status: res.statusCode,
  duration: Date.now() - start,
})
```

**Business events**:
```typescript
logger.info('Subscription created', {
  userId: user.id,
  plan: 'pro',
  billing: 'annual',
  amount: 348,
})
```

**Errors with context**:
```typescript
logger.error('Payment failed', {
  userId: user.id,
  error: error.message,
  paymentIntentId: paymentIntent.id,
  amount: 29,
})
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **ERROR** | Something is broken | API returns 500, payment fails |
| **WARN** | Something unexpected but handled | Rate limit hit, deprecated API called |
| **INFO** | Important business events | User signed up, subscription created |
| **DEBUG** | Development troubleshooting | Variable values, execution paths |

### Logging Tools

- **Sentry**: Error logging + context
- **PostHog**: Event tracking (not log storage)
- **Better Stack/Logtail**: Centralized logging (free tier available)
- **Datadog**: Enterprise (expensive for solo)
- **Self-hosted Loki**: If you need full control

---

## 7. Health Check Endpoints

### The /health Endpoint

Create a simple health check endpoint:

```typescript
// app/api/health/route.ts
export async function GET() {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    database: await checkDatabase(),
    redis: await checkRedis(),
    version: process.env.VERSION,
  }
  
  return NextResponse.json(health)
}

async function checkDatabase() {
  try {
    await prisma.$queryRaw`SELECT 1`
    return { status: 'ok' }
  } catch (error) {
    return { status: 'error', message: error.message }
  }
}
```

### Uptime Monitoring

Use a free uptime monitor (UptimeRobot, Better Stack) to ping your health endpoint every 5 minutes. Get alerted if it returns non-200.

### What to Check in Health Endpoint

- [ ] Database connectivity
- [ ] Cache (Redis, if used)
- [ ] Disk space
- [ ] Memory usage
- [ ] Recent error rate
- [ ] SSL certificate expiry

---

## 8. The Monitoring Dashboard

### The Solo Monitoring Dashboard

A single dashboard that shows:

**Health**:
- All services operational? (green/red)
- Uptime (99.9%+?)
- SSL certificate valid?

**Errors**:
- Error rate (last hour, last 24 hours)
- Top errors
- Errors by endpoint

**Performance**:
- p50 / p95 / p99 API response times
- Frontend Web Vitals (LCP, FID, CLS)
- Database query performance

**Business**:
- Active users
- Signups (today, this week)
- Revenue (today, this month)
- Churn rate

### Tools for the Dashboard

- **PostHog**: Business metrics + errors + session replay (all in one!)
- **Better Stack**: Uptime + status page + logging
- **Vercel Dashboard**: Deployment + performance + analytics
- **Sentry**: Errors + performance tracing

---

## 9. The Monitoring-First Workflow

### Daily Monitoring Routine

```
9:00 - Check health dashboard (2 min)
  - All services green?
  - Error rate normal?
  - No alerts overnight?

9:05 - Watch 3 session recordings (5 min)
  - Any new friction points?
  - Users doing something unexpected?

9:10 - Check key metrics (3 min)
  - Signups vs. yesterday?
  - Revenue vs. yesterday?
  - Active users tracking?

9:15 - Start the day
  - Fix any issues found
  - Continue feature work
```

### The Bug Discovery Pipeline

Most bugs should be discovered through monitoring, not testing:

```
Real user encounters issue
  → Error tracking captures it (Sentry)
  → Session replay shows the context
  → Metrics show the impact
  → You fix it
  → You write a unit test to prevent regression
  → Monitoring confirms the fix
```

### When to Write a Test

Write a test for production bugs:
- If the same bug could affect many users
- If the bug could cause data loss
- If the bug could lose you money
- If you've fixed this type of bug before

Don't write a test for every edge case — write a test if the bug actually happened in production.

---

## 10. Setting Up as a Solo Founder

### The Minimum Monitoring Stack

This is all you need to start:

**Free tier stack**:
1. **PostHog**: Analytics + session replay + feature flags
2. **Sentry**: Error tracking + performance
3. **Better Stack**: Uptime monitoring + status page

**Setup time**: 2 hours total

### Configuration Checklist

- [ ] Sentry or PostHog error tracking installed (1 hour)
- [ ] PostHog session recording enabled (15 min)
- [ ] Key business events tracked (signup, core action, payment) (30 min)
- [ ] Uptime monitor pointing to /health endpoint (15 min)
- [ ] Alerts configured for P0/P1 issues (15 min)
- [ ] Health dashboard reviewed (ongoing, 10 min/day)

### The Monitoring Budget

Spend 2 hours setting up monitoring initially. Then 10 minutes per day reviewing.

Compare this to writing tests: 2 hours of monitoring setup catches more bugs than 20 hours of test writing.

---

## 11. Common Monitoring Mistakes

### Mistake 1: No Error Tracking

"I'll know if something breaks because users will tell me."

**Reality**: Most users who encounter errors leave silently. They don't file a bug report. They just disappear.

**Fix**: Install error tracking on day one. It takes 15 minutes.

### Mistake 2: Alert Fatigue

Alerting for every minor issue. You get 50 emails per day and start ignoring them.

**Fix**: Only alert for P0 (all users affected, data loss) and P1 (core feature broken). Everything else goes in a daily digest.

### Mistake 3: No Context in Errors

```typescript
// Bad
logger.error('Something went wrong')

// Good
logger.error('Payment processing failed', {
  userId: user.id,
  subscriptionId: sub.id,
  amount: 29,
  errorCode: 'card_declined',
  attempt: 3,
})
```

### Mistake 4: Not Watching Session Recordings

"I have error tracking, so I know when things break."

**Reality**: Session recordings show you WHY things break and how users react. Error tracking tells you WHAT. Both are essential.

**Fix**: Watch 3 sessions per day. You'll find issues that error tracking never catches.

### Mistake 5: Ignoring the Dashboard

Spent 2 hours setting up a beautiful dashboard. Never looks at it.

**Fix**: Make it your browser's home page. Check it every morning.

---

## 12. Testing vs. Monitoring: Decision Matrix

| Scenario | Best Approach |
|----------|---------------|
| Payment processing | Unit test + monitoring |
| Authentication flow | Integration test + monitoring |
| Profile page | Monitoring only |
| CSV export logic | Unit test |
| Landing page | Monitoring only |
| Core business logic | Unit test + monitoring |
| Third-party integration | Monitoring only |
| Data migration | Unit test + manual verification |
| Simple CRUD | Monitoring only |
| Critical user path | E2E test + monitoring |

### The 80/20 of Quality Assurance

Spend your QA budget:
- 20% on pre-production testing (unit, integration, E2E)
- 80% on production monitoring (error tracking, session replay, analytics)

This ratio catches more bugs per hour invested.

---

## 13. The Monitoring Manifesto

1. **Install error tracking first** — 15 minutes, catches 90% of production bugs
2. **Watch session recordings daily** — See what users actually experience
3. **Log everything with context** — A log without context is noise
4. **Alert only for P0/P1** — Everything else can wait
5. **Set up a health endpoint** — Know your system is alive
6. **Monitor business metrics** — A drop in signups might be a signup bug
7. **Test in production** — Real users > synthetic tests
8. **Fix forward, then test** — Fix the bug, then write a test
9. **Check the dashboard daily** — 5 minutes every morning
10. **Monitoring > Testing for solo** — More bugs caught per hour invested

Testing and monitoring are not either/or. They're complementary. But if you can only invest in one as a solo founder, invest in monitoring. It catches more bugs, with less effort, using real user data — and that's the testing strategy that actually protects your users.
