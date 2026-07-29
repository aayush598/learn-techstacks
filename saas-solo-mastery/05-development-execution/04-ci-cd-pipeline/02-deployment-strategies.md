# Deployment Strategies for Solo Founders

## Why Deployment Strategy Matters

Deployment is the moment of truth. It's when your code meets your users. A good deployment strategy minimizes risk while maximizing shipping velocity.

For solo founders, the consequences of bad deployments are amplified:
- You're the only one who can fix it
- You have no on-call rotation
- Bad deployments during weekends ruin your personal time
- Users leave when your product is unreliable

---

## 1. The Solo Deployment Spectrum

| Strategy | Risk | Speed | Complexity | When to Use |
|----------|------|-------|------------|-------------|
| Direct deploy | Medium | Fastest | None | Minor changes, bug fixes |
| Feature flags | Low | Fast | Low | All features |
| Canary releases | Low | Medium | Medium | Major changes |
| Blue-green | Very low | Fast | High | High-traffic apps |
| Staged rollout | Very low | Slow | Medium | Risk-averse changes |

### Recommended for Solo

**Standard**: Feature flags for everything
**Major changes**: Feature flags + canary (10% → 50% → 100%)
**Emergency fixes**: Direct deploy with monitoring

---

## 2. Direct Deployment

### When to Use Direct Deploy

Direct deployment means pushing code to production immediately. Use it for:
- Bug fixes
- Small UI tweaks
- Documentation changes
- Configuration updates
- Dependency updates

### The Direct Deploy Process

```
1. Make change
2. Test locally (smoke test)
3. Commit and push
4. CI runs (type check, lint, test, build)
5. Deploy automatically
6. Monitor for 5 minutes
```

### Safety Requirements

Before you can safely deploy directly:
- CI pipeline catches most issues
- Feature flags are available to disable if needed
- Monitoring is in place to detect issues
- Rollback takes < 2 minutes

---

## 3. Feature Flags

### The Feature Flag Pattern

Feature flags let you deploy code to production without enabling it for users:

```typescript
// app/lib/features.ts
export async function isFeatureEnabled(userId: string, feature: string): Promise<boolean> {
  // Check PostHog feature flag
  return posthog.isFeatureEnabled(feature, userId)
}

// Usage in components
export default async function Dashboard() {
  const newDashboard = await isFeatureEnabled(user.id, 'new-dashboard')
  
  if (newDashboard) {
    return <NewDashboard />
  }
  return <CurrentDashboard />
}
```

### Feature Flag Workflow

```
1. Create flag in PostHog (or flag service)
2. Implement feature behind flag (default: off)
3. Deploy code (feature is inactive)
4. Test in production (enable for yourself)
5. Enable for beta users
6. Monitor for issues
7. Gradually increase rollout (10% → 50% → 100%)
8. After success: remove flag and old code
```

### Types of Feature Flags

| Flag Type | Lifetime | Example |
|-----------|----------|---------|
| **Release flag** | Short (days-weeks) | New feature rollout |
| **Experiment flag** | Short (weeks) | A/B test variant |
| **Permission flag** | Long (months-years) | Feature by plan level |
| **Kill switch** | Permanent | Emergency disable |

### PostHog Feature Flag Setup

```typescript
// Server-side check
const flags = await posthog.getAllFlags(user.id)
const showNewFeature = flags['new-export'] === true

// Client-side check
const showNewFeature = useFeatureFlag('new-export')
```

---

## 4. Canary Releases

### What Is a Canary Release

A canary release gradually rolls out a change to a subset of users before full release:

```
Phase 1: Enable for internal users (you + beta testers)
Phase 2: Enable for 10% of users
Phase 3: Enable for 50% of users
Phase 4: Enable for 100% of users
```

### Canary with Feature Flags

Feature flags make canary releases trivial:

1. Set flag to 10% rollout
2. Monitor for 30 minutes
3. If no issues: increase to 50%
4. Monitor for 30 minutes
5. If no issues: increase to 100%

### What to Monitor During Canary

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 0.1% increase | Pause rollout |
| API response time | > 20% increase | Rollback |
| Signup conversion | > 5% decrease | Rollback |
| Support tickets | > 2x increase | Pause and investigate |

### Canary Without Feature Flags

If you don't have feature flags, you can do manual canary:

```
1. Deploy to staging
2. Route 10% of traffic to staging
3. Monitor for issues
4. Route 50% to staging
5. Route 100% to staging (now production)
```

This requires more infrastructure (load balancer, multiple environments) but offers the same safety.

---

## 5. Blue-Green Deployment

### What Is Blue-Green

Blue-green deployment runs two identical environments:
- **Blue**: Current production
- **Green**: New version

Switch traffic from Blue to Green when ready. If issues arise, switch back.

### Blue-Green for Solo

For most solo SaaS products, blue-green is overkill. Use it if:
- You have high traffic (1000+ concurrent users)
- Zero downtime is required
- Your users are enterprise (SLA-bound)
- You can afford the infrastructure cost (2x servers)

### Simplified Blue-Green with Vercel

Vercel handles blue-green-like behavior automatically:
- Every deploy is a new version
- Instant rollback to any previous version
- Zero-downtime deploys

---

## 6. Database Migrations

### The Migration Problem

Database migrations are the riskiest part of any deploy:
- A backward-incompatible migration can break production
- Long-running migrations can timeout
- Failed migrations can leave the database in an inconsistent state

### Safe Migration Strategy

**Rule 1: Always backward-compatible**
- Add columns as nullable (or with defaults)
- Don't rename columns (add new, migrate, remove old)
- Don't remove columns in the same deploy as code changes

**Rule 2: Separate migration from code deploy**
```
Deploy 1: Add new column + write code that handles both old and new
Migration: Backfill new column data
Deploy 2: Remove old column + code that only uses new
```

### Prisma Migrations

```yaml
# In CI/CD
- name: Run migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Migration Safety Checklist

- [ ] Migration is backward-compatible (existing code works with new schema)
- [ ] Rollback migration is prepared if needed
- [ ] Migration won't lock tables for too long
- [ ] Data is backed up before running migration
- [ ] Migration is tested against a copy of production data

---

## 7. Rollback Automation

### Why Rollback Needs to Be Automatic

During an incident, every second counts. Manual rollback:
1. Realize there's a problem (30 seconds)
2. Find the previous working version (1 minute)
3. Run the rollback command (30 seconds)
4. Wait for redeploy (2 minutes)
5. Verify the fix (1 minute)

Total: 5+ minutes of downtime

**Automated rollback**:
1. Monitoring detects error spike (instant)
2. Automated rollback triggered (instant)
3. Previous version deployed (2 minutes)
4. Issue mitigated

### Automated Rollback with Feature Flags

The simplest automated rollback:

```typescript
// Check error rate every minute
setInterval(async () => {
  const errorRate = await getErrorRate()
  if (errorRate > 0.05) { // 5% error rate threshold
    await disableFeatureFlag('my-feature')
    await sendAlert('Feature disabled due to high error rate')
  }
}, 60000)
```

### Automated Rollback with Vercel

If you deploy through Vercel, rollback is one click:
- Vercel Dashboard → Deployments → Last known good → ... → Promote to Production

### The Rollback Policy

| Situation | Action | Target Time |
|-----------|--------|-------------|
| Error rate > 5% | Auto-rollback feature flag | 1 minute |
| Error rate > 10% | Auto-rollback full deploy | 2 minutes |
| Security incident | Manual rollback | Immediate |
| Data corruption | Stop servers, restore from backup | ASAP |

---

## 8. Deployment Schedule

### When to Deploy

| Time | Safety | Notes |
|------|--------|-------|
| Monday AM | Medium | Fresh start, full week ahead |
| Tuesday AM | High | Best day for major changes |
| Wednesday AM | High | Good for medium changes |
| Thursday AM | Medium | OK for small changes |
| Friday | Low | AVOID — weekend risk |
| Weekend | Very low | Only for critical security fixes |

### The "No Friday Deploy" Rule

Never deploy on Friday unless it's a critical security fix. If something breaks:
- You work all weekend
- Users suffer until Monday
- You're stressed and can't enjoy your weekend

### The Pre-Weekend Checklist

If you deploy Thursday or Friday:
- [ ] Feature flag exists to disable the change
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured
- [ ] Someone (you) is available if things break

---

## 9. Deployment Documentation

### The Runbook

For each type of deploy, document:

```markdown
# Deployment Runbook

## Normal Deployment
1. Push to main → CI/CD handles the rest
2. If Vercel: deployment is automatic
3. Monitor for 5 minutes after deploy

## Feature Flag Deployment
1. Deploy code (feature is OFF)
2. Enable feature for beta users
3. Enable for 10% → 50% → 100%
4. Remove flag and old code after 1 week

## Rollback
1. Feature flag rollback: Disable flag in PostHog
2. Full rollback: Vercel dashboard → Deployments → Promote previous version
3. Database rollback: `npx prisma migrate resolve --rolled-back <migration>`

## Emergency Deploy
1. Create fix branch
2. Commit fix
3. Push to main (bypass CI if urgent)
4. Monitor closely
5. Fix CI later
```

### The Changelog

Track what's deployed:

```
# Changelog

## 2024-03-15 (v2.3.1)
- Fixed: Login redirect for Safari users
- Changed: Password minimum length to 8 characters

## 2024-03-14 (v2.3.0)
- Added: CSV export feature
- Added: Dark mode toggle
- Fixed: Dashboard loading on mobile
```

---

## 10. Choosing Your Deployment Strategy

### Decision Matrix

| Scenario | Strategy | Reason |
|----------|----------|--------|
| Bug fix | Direct deploy | Fast, low risk |
| Small UI change | Direct deploy | Low risk |
| New feature | Feature flag | Deploy early, release when ready |
| Major backend change | Feature flag + canary | High risk, needs gradual rollout |
| Database migration | Separate deploy cycle | Can't rollback easily |
| Security fix | Direct deploy | Urgent |
| Refactoring | Feature flag | Deploy, test, then enable |
| Dependency update | Direct deploy + monitoring | Low risk but monitor |

### The Solo Decision Tree

```
Is this a security fix?
  → Yes: Deploy immediately
  → No: Continue

Is this a new feature?
  → Yes: Deploy behind feature flag
  → No: Continue

Is this a database change?
  → Yes: Separate migration from code deploy
  → No: Continue

Is this a large change (> 100 lines)?
  → Yes: Feature flag + canary rollout
  → No: Direct deploy

Does this affect payment/auth?
  → Yes: Extra monitoring, canary rollout
  → No: Standard deploy
```

---

## 11. Deployment Monitoring

### Immediate Post-Deploy (5 minutes)

After every deploy, check:

1. **Error rate**: No spike in errors
2. **Response time**: No significant change
3. **Key metrics**: Signups, conversions, active users
4. **Error logs**: No new error types
5. **User sessions**: Quick check of 3 sessions

### Deployment Dashboard

```typescript
// Post-deploy monitoring check
async function postDeployCheck() {
  const checks = {
    errorRate: await getErrorRate(),
    responseTime: await getP95ResponseTime(),
    signupRate: await getSignupRate(),
    activeUsers: await getActiveUsers(),
  }
  
  const failures = []
  if (checks.errorRate > 0.01) failures.push('High error rate')
  if (checks.responseTime > 1000) failures.push('Slow responses')
  if (checks.signupRate < expected * 0.8) failures.push('Signups dropped')
  
  if (failures.length > 0) {
    await sendAlert(`Deploy issues: ${failures.join(', ')}`)
    return false
  }
  
  return true
}
```

---

## 12. Common Deployment Mistakes

### Mistake 1: No Rollback Plan

"I'll figure it out if something goes wrong."

**Reality**: When something goes wrong, you panic. Manual recovery takes 10x longer than automated recovery.

**Fix**: Know your rollback method BEFORE you deploy. Test it.

### Mistake 2: Deploying on Friday

"It's just a small fix, it'll be fine."

**Reality**: It breaks. You spend the weekend fixing it.

**Fix**: Don't deploy after Thursday noon. Period.

### Mistake 3: Big Bang Releases

"I've been working on this for 3 weeks. Time to deploy everything at once."

**Reality**: Something breaks. You don't know which of the 50 changes caused it.

**Fix**: Deploy each change incrementally. Use feature flags for incomplete work.

### Mistake 4: No Monitoring

"I deployed. I guess I'll find out if there's a problem when users complain."

**Reality**: Users don't complain. They just leave.

**Fix**: Set up error tracking before your first deploy.

### Mistake 5: Ignoring Database Migrations

"I'll just add this column and update the code in the same deploy."

**Reality**: The migration runs, the new code fails, and now you have a column with no code to use it.

**Fix**: Separate schema changes from code changes. Deploy in phases.

---

## 13. Quick Start: Your First Week

### Day 1: Set Up Basic Deploy
- [ ] Connect GitHub to Vercel (or configure your host)
- [ ] Push to main → It deploys automatically
- [ ] Verify the deployment works

### Day 2: Add Feature Flags
- [ ] Install PostHog (or feature flag service)
- [ ] Create your first feature flag
- [ ] Wrap a feature behind the flag

### Day 3: Add Rollback Plan
- [ ] Document how to rollback
- [ ] Test rollback (deploy a breaking change, then rollback)
- [ ] Verify monitoring alerts work

### Day 4: Set Up Canary Process
- [ ] Document canary rollout process
- [ ] Configure gradual rollout in feature flags
- [ ] Practice: deploy behind flag, enable for 10%, 50%, 100%

### Day 5: Create Deployment Schedule
- [ ] Decide on deploy days (Tue/Thu recommended)
- [ ] Create pre-deploy checklist
- [ ] Create post-deploy monitoring process

---

## 14. The Deployment Manifesto

1. **Feature flags for everything** — Deploy code before it's ready
2. **Test in production** — The real test environment is production
3. **Rollback is instant** — Know your rollback before you deploy
4. **Small batches** — Deploy small, deploy often
5. **No Friday deploys** — Protect your weekend
6. **Monitor after every deploy** — 5 minutes of watching
7. **Canary for risky changes** — 10% → 50% → 100%
8. **Separate migrations from code** — Deploy in phases
9. **Document your process** — A runbook prevents panic
10. **Deploy should be boring** — If it's exciting, something's wrong

The best deployment is the one nobody notices. When your deployment process is smooth, automated, and boring, you're free to focus on what matters: building features your users love.
