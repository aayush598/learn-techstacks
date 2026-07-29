# Shipping Velocity for Solo Founders

## Why Shipping Velocity Matters

Shipping velocity — how often and how reliably you ship code to production — is the single best predictor of SaaS success for solo founders. High-velocity teams:

- Get feedback faster
- Build products users actually want
- Fix bugs before they compound
- Outpace competitors
- Maintain momentum (critical for solo motivation)

Amazon's famous rule: "Teams that ship every week outperform teams that ship every month by a factor of 3."

---

## 1. The Shipping Cadence

### Daily vs. Weekly vs. Monthly

| Cadence | Best For | Risk | Feedback Loop |
|---------|----------|------|---------------|
| **Multiple times/day** | Bug fixes, hotfixes, small tweaks | Low (small changes) | Immediate |
| **Daily** | Active development, early-stage | Medium | Hours |
| **Weekly** | Stable product, growth stage | Low to Medium | Days |
| **Bi-weekly** | Enterprise, regulated | Low | Weeks |
| **Monthly** | Major releases | High | Very slow |

### The Ideal Solo Cadence

**Early stage (pre-PMF)**: Ship daily
**Growth stage (PMF - 1000 users)**: Ship 3-5 times per week
**Scale stage (1000+ users)**: Ship 2-3 times per week

### The "Ship Something" Rule

Every day, ship something — even if it's a one-line fix.

- A typo fix
- A small CSS improvement
- An analytics event
- A readme update
- A bug fix

This builds the shipping habit and keeps momentum.

---

## 2. Small Batch Sizes

### The Power of Small

Amazon CEO Andy Jassy: "Small batches of work lead to higher quality, faster delivery, and better outcomes."

**Large batch**: 2-week feature, 500 lines changed, high risk, slow feedback
**Small batch**: 2-hour feature, 50 lines changed, low risk, fast feedback

### Breaking Features into Small Batches

Instead of "Build the dashboard" (2 weeks):

1. Add a basic stats card (2 hours) → Ship
2. Add user list to dashboard (2 hours) → Ship
3. Add chart to dashboard (3 hours) → Ship
4. Add filters to dashboard (2 hours) → Ship
5. Polish dashboard layout (1 hour) → Ship

Each small batch ships independently. Users get value incrementally. You get feedback on each piece.

### The Art of Slicing

How to slice any feature into small batches:

**Vertical slicing** (recommended): Build a thin version of the full feature
- Instead of: Build all backend → Build all frontend → Integrate
- Do: Build backend + frontend for ONE thing → Ship → Repeat

**Horizontal slicing**: Build one layer at a time
- First: All database work
- Then: All API work
- Then: All frontend work

Use vertical slices for solo. You get a working (if limited) feature faster.

### Example: Build "Project Management"

**Bad slicing** (horizontal):
1. Week 1: All database schemas (projects, tasks, comments)
2. Week 2: All API endpoints
3. Week 3: All UI pages
4. Week 4: Integration and testing
5. Week 5: Ship (maybe)

**Good slicing** (vertical):
1. Day 1: Create a project (backend + frontend) → Ship
2. Day 2: View project list (backend + frontend) → Ship
3. Day 3: Add tasks to project → Ship
4. Day 4: Edit and delete tasks → Ship
5. Day 5: Add comments to tasks → Ship

After Day 1, users can already create projects (limited but valuable).

---

## 3. Feature Flags

### What Are Feature Flags

Feature flags let you deploy code to production WITHOUT releasing it to users. You can:
- Deploy unfinished features (safe in production)
- Test with specific users
- Gradually roll out changes
- Instantly disable problematic features
- Run A/B tests

### Why Solo Founders Need Feature Flags

Even without a team, feature flags are essential:
- **Deploy fearlessly**: Ship incomplete code, enable when ready
- **Rollback instantly**: Disable a flag instead of reverting code
- **Test in production**: Enable for yourself or beta users
- **Gradual rollout**: Enable for 10%, 50%, then 100% of users

### Feature Flag Implementation

Using PostHog (free tier):

```typescript
import { useFeatureFlag } from 'posthog-js/react'

export function Dashboard() {
  const newDashboard = useFeatureFlag('new-dashboard')
  
  if (newDashboard) {
    return <NewDashboard />
  }
  
  return <CurrentDashboard />
}
```

### Feature Flag Lifecycle

1. **Create flag**: Define the flag in PostHog
2. **Implement**: Wrap new code in flag check
3. **Deploy**: Ship code (feature is OFF by default)
4. **Test**: Enable for yourself/beta users
5. **Rollout**: Gradually enable for more users
6. **Monitor**: Check for errors, performance issues
7. **Full release**: Enable for 100% of users
8. **Clean up**: Remove flag and old code

### Flag Types

| Flag Type | Use Case | Visibility |
|-----------|----------|------------|
| Release flag | New feature rollout | Invisible to users |
| Experiment flag | A/B testing | Invisible to users |
| Permission flag | Feature by plan level | Visible to users |
| Kill switch | Disable feature in emergency | Invisible |

---

## 4. Trunk-Based Development

### What Is Trunk-Based Development

Trunk-based development means:
- All developers work on a single branch (main/trunk)
- Changes are small and frequent
- No long-lived feature branches
- Merge to main multiple times per day

### Why It Works for Solo

- **No merge hell**: You're the only developer
- **No stale branches**: Everything is on main
- **Continuous integration**: Code is always integrated
- **Less overhead**: No branch management
- **Faster shipping**: No merge → wait → deploy cycle

### The Solo Trunk-Based Workflow

```bash
# Create a simple workflow, no branching needed
git add .
git commit -m "Add task completion feature"
git push
# CI/CD deploys automatically
```

For solo, your workflow can be:

1. Pull latest main
2. Make changes
3. Commit (small, focused commits)
4. Push → Auto-deploys

No PRs. No code review. No branching. Just ship.

### When to Branch

Even with trunk-based development, you might branch for:
- **Large experiments**: You might discard this work
- **Preparing a big launch**: Multiple changes that need to ship together
- **If you ever add a team member**: Then you'll need PRs and reviews

### The "Branch for Emergencies Only" Rule

Keep branches for:
- Emergency fix that needs isolation
- Risky refactor you might abandon
- Major feature that needs multiple sessions (keep 3 days max)

---

## 5. Continuous Deployment

### What Is Continuous Deployment

Every push to main automatically deploys to production. No manual steps. No "release day." No deployment anxiety.

### Setting Up CD

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

### The CD Pipeline

```
Code commit → Tests pass → Build succeeds → Deploy to staging → 
Run smoke tests → Deploy to production → Monitor (15 min)
```

### CI/CD Checklist

- [ ] Tests run on every push
- [ ] Build succeeds before deploy
- [ ] Deployment is automated
- [ ] Rollback is one click
- [ ] Monitoring alerts on errors
- [ ] Feature flags control releases

---

## 6. The Deployment Pipeline

### Staging vs. Direct to Production

| Approach | Risk | Speed | Best For |
|----------|------|-------|----------|
| Deploy to production directly | Higher | Fastest | Simple changes |
| Deploy to staging first | Lower | Slower | Complex changes |
| Feature flags in production | Lower | Fast (behind flag) | All changes |

### The Solo Pipeline

For solo founders, the optimal pipeline:

1. **Develop locally**
2. **Git push** (to main)
3. **CI runs** (lint, type-check, tests)
4. **Build** (production build succeeds)
5. **Deploy to Vercel/your host**
6. **Production** (behind feature flag if needed)
7. **Monitor** (errors, performance)

This takes 2-5 minutes total.

### The No-Staging Strategy

Many solo founders skip staging entirely. Instead:
- Test locally (comprehensive)
- Deploy to production
- Enable behind feature flag
- Test in production (as the first user)
- Gradually roll out

This is faster and (with feature flags) as safe as staging.

---

## 7. Rollback Strategy

### Why Rollbacks Matter

Even with the best testing, things go wrong. A fast rollback capability is your safety net.

### Rollback Methods

**Method 1: Git revert** (fastest for code)
```bash
git revert HEAD
git push
```

**Method 2: Feature flag** (instant)
```typescript
posthog.updateFeatureFlag('my-feature', false) // Instantly disabled
```

**Method 3: Vercel rollback** (one click)
- Vercel dashboard → Deployments → ... → Rollback

### The Rollback Checklist

When something goes wrong:
1. **Don't panic** — Most issues are not emergencies
2. **Assess severity** — Is this P0 (all users affected)?
3. **If P0**: Disable feature flag or rollback deployment
4. **If non-P0**: Fix on main and deploy
5. **Communicate** — Tell users if they were affected
6. **Debug** — After resolution, understand root cause

### Rolling Forward vs. Rolling Back

| Situation | Action |
|-----------|--------|
| Minor bug | Roll forward (fix on main) |
| Major bug affecting many users | Rollback |
| Security issue | Rollback immediately |
| Broken UI | Roll forward (quick fix) |
| Data integrity issue | Rollback + data restore |

---

## 8. Monitoring Deployments

### What to Monitor After Each Deploy

| Metric | What to Watch | Action if Bad |
|--------|---------------|---------------|
| Error rate | Sudden spike | Rollback or disable flag |
| Response time | Slower than normal | Profile, optimize, rollback |
| Signup/conversion rate | Drop | Check signup flow |
| 404/500 errors | Increase | Check recent changes |
| API error rate | Spike | Check API changes |

### Automated Monitoring After Deploy

```typescript
// Deploy Hook (PostHog)
After every deploy:
  1. Wait 5 minutes
  2. Check error rate vs baseline
  3. If error rate > 2x baseline → Alert
  4. If alert not acknowledged in 10 min → Auto-rollback
```

### The "15-Minute Watch"

After deploying, spend 15 minutes watching:
1. Error tracking dashboard
2. Server response times
3. Key conversion metrics
4. Session recordings (sample)

After 15 minutes with no issues, the deploy is considered successful.

---

## 9. Shipping Cadence by Stage

### Pre-PMF (0-100 users)

**Goal**: Learn what users want
**Cadence**: Ship daily
**Process**:
- Build smallest test → Ship → Get feedback → Iterate
- No feature flags needed (low user count = low risk)
- No rollback needed (just fix forward)
- Spend 50% of time shipping, 50% talking to users

### Early Growth (100-1000 users)

**Goal**: Improve retention and conversion
**Cadence**: Ship 3-5x per week
**Process**:
- Weekly goal → Break into daily tasks → Ship each task
- Use basic feature flags for major changes
- Monitor error rates
- Fix bugs within 24 hours

### Scale (1000+ users)

**Goal**: Maintain reliability while shipping
**Cadence**: Ship 2-3x per week
**Process**:
- Feature flags for all changes
- Gradual rollout (10% → 50% → 100%)
- Staged deploys if needed
- Automated monitoring and rollback
- Scheduled release windows (Tue/Thu, not Friday)

---

## 10. The Shipping Day

### The Ideal Shipping Day

```
9:00 - Review what to ship today
9:30 - Final testing of today's changes
10:00 - Deploy to production
10:15 - Monitor deployment (error rates, performance)
10:30 - Enable feature flags (if applicable)
10:45 - Verify in production
11:00 - Document what shipped
11:15 - Move on to next thing
```

### Friday Rule

Never deploy on Friday. If something breaks, you spend the weekend fixing it.

**Safe deploy days**: Tuesday, Wednesday, Thursday morning
**Risky deploy days**: Monday (fresh start, but weekend backlog), Friday (weekend risk)
**Never deploy**: Friday afternoon, Saturday, Sunday, before vacation

### The Pre-Deploy Checklist

- [ ] Changes tested locally
- [ ] TypeScript has no errors
- [ ] Lint passes
- [ ] Critical path smoke-tested
- [ ] No console errors
- [ ] Changes behind feature flag (if risky)
- [ ] Rollback plan ready
- [ ] Monitoring tools open

---

## 11. Measuring Shipping Velocity

### Key Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Deploy frequency** | Number of deploys per week | 3-5x/week |
| **Lead time** | Time from commit to production | < 1 hour |
| **Change failure rate** | % of deploys causing issues | < 5% |
| **Time to restore** | Time to fix a production issue | < 1 hour |

### Tracking Your Velocity

Simple tracking (in a spreadsheet or Notion):

```
Week 12:
  Mon: Deployed task completion feature
  Tue: Deployed bug fix for login
  Wed: No deploy (blocked by API issue)
  Thu: Deployed export feature, Deployed dashboard fix
  Fri: Deployed minor styling improvements
  
  Deploys: 5
  Lead time: ~30 min average
  Failures: 0
```

### Improving Velocity

**Too slow?** → Ship smaller batches, automate more, reduce testing scope
**Too many failures?** → Add more local testing, use feature flags, slow down
**Too few deploys?** → Ship smaller items, build the shipping habit
**Too many bugs?** → Improve local testing, monitor errors better

---

## 12. Common Shipping Mistakes

### Mistake 1: The Big Bang Release

Working on a feature for 3 weeks, then releasing everything at once.

**Problem**: High risk, delayed feedback, if it fails, everything fails
**Fix**: Ship each piece independently. Use feature flags for incomplete work.

### Mistake 2: Not Shipping Because "It's Not Perfect"

"I can't ship this yet, the button animation isn't quite right."

**Problem**: Perfectionism kills velocity. Users rarely notice what you think they will.
**Fix**: Ship "good enough." Iterate based on feedback.

### Mistake 3: Shipping Without Monitoring

"I deployed, but I don't know if it worked or broke anything."

**Problem**: You can't fix what you don't know is broken.
**Fix**: Set up error monitoring (Sentry, PostHog) and check after each deploy.

### Mistake 4: No Rollback Plan

"I shipped something broken and I don't know how to undo it."

**Problem**: Recovery takes too long, users suffer.
**Fix**: Know your rollback method (git revert, feature flag, Vercel rollback).

### Mistake 5: Deploying on Friday

"Let me just ship this quick change on Friday afternoon."

**Problem**: If it breaks, you work all weekend.
**Fix**: Deploy Tuesday-Thursday only.

### Mistake 6: Huge Commits

"I made 50 changes in one commit over 3 days."

**Problem**: Can't roll back individual changes, hard to debug issues.
**Fix**: Commit after each small change. Each commit should be < 50 lines when possible.

---

## 13. The Deployment Manifesto

1. **Ship daily** — Even a one-line fix counts
2. **Small batches** — Every deploy is small, low-risk, easy to debug
3. **Feature flags for everything** — Deploy incomplete code safely
4. **Automated deploy** — One push deploys to production
5. **Monitor after every deploy** — 15 minutes of watching
6. **Fix forward for small issues, rollback for big ones** — Know the difference
7. **No Friday deploys** — Protect your weekend
8. **Rollback is one click** — Know your rollback method
9. **Velocity is a habit** — The more you ship, the easier it becomes
10. **Ship before perfect** — A shipped feature is worth more than a perfect one

Shipping velocity is the engine of your SaaS. The faster you ship, the faster you learn, the faster you improve, and the faster you grow. Everything else is secondary.
