# PLG Metrics: Viral Coefficient, Time-to-Value, Self-Serve Conversion Rate, Expansion MRR

## Why PLG Metrics Matter

PLG metrics are different from traditional SaaS metrics. They measure how well your product drives growth without sales or marketing intervention. These metrics tell you:

- Is your product actually viral, or just popular?
- Are users experiencing value quickly enough?
- Is the self-serve funnel working?
- Are customers expanding their usage over time?

For a solo founder, PLG metrics are especially important because you don't have a sales team to compensate for product weaknesses. If the product doesn't drive growth, there is no growth.

## Metric 1: Viral Coefficient (K-Factor)

### What It Is

The viral coefficient (K) measures how many new users each existing user brings in.

```
K = I × C

I = Average number of invitations sent per user
C = Conversion rate of those invitations to active users

Example:
- Average user sends 5 invitations
- 20% of invitations convert to active users
- K = 5 × 0.20 = 1.0

K > 1.0: Exponential growth (each user brings > 1 new user)
K = 1.0: Linear growth (each user replaces themselves)
K < 1.0: Decaying growth (need other channels to sustain)
```

### How to Measure K

```typescript
class ViralCoefficientCalculator {
  async calculate({
    dateRange,
    includeOrganic = false
  }) {
    // Get all users who joined in the window
    const cohort = await db.users.findMany({
      where: {
        createdAt: { gte: dateRange.start, lte: dateRange.end }
      },
      select: { id: true }
    })

    // Count invitations sent by this cohort
    const invitations = await db.invitations.aggregate({
      where: {
        senderId: { in: cohort.map(u => u.id) },
        createdAt: { gte: dateRange.start }
      },
      _count: true
    })

    // Count new users from those invitations
    const newUsers = await db.users.count({
      where: {
        referredById: { in: cohort.map(u => u.id) },
        createdAt: { gte: dateRange.start }
      }
    })

    const totalUsers = cohort.length
    if (totalUsers === 0) return { k: 0, invitationsPerUser: 0, conversionRate: 0 }

    const invitationsPerUser = invitations._count / totalUsers
    const conversionRate = newUsers / invitations._count

    return {
      k: invitationsPerUser * conversionRate,
      invitationsPerUser,
      conversionRate,
      totalUsers,
      totalInvitations: invitations._count,
      totalNewUsers: newUsers
    }
  }

  async getViralCoefficientTrend() {
    // Track K over time to see if it's improving
    const monthlyData = []
    for (let i = 0; i < 12; i++) {
      const start = new Date()
      start.setMonth(start.getMonth() - i)
      const end = new Date(start)
      end.setMonth(end.getMonth() + 1)

      monthlyData.push({
        month: start.toISOString().slice(0, 7),
        ...(await this.calculate({ dateRange: { start, end } }))
      })
    }
    return monthlyData
  }
}
```

### The Viral Coefficient Breakdown

Not all viral loops are equal. Breakdown your K by type:

```
K by Virality Type:

Inherent virality: K = 0.4 (sharing is required for product use)
Collaboration virality: K = 0.3 (inviting teammates)
Content virality: K = 0.2 (sharing created content)
Referral virality: K = 0.1 (explicit referral program)

Total K = 1.0 ✓
```

Track which type drives the most growth and optimize accordingly.

### Improving K-Factor

```
If K < 0.5 (weak virality):
- Reduce sharing friction (make it easier to invite)
- Increase incentives (or make sharing inherent)
- Improve the invite experience (prettier, clearer value)

If K = 0.5-0.9 (moderate virality):
- Optimize the invite conversion rate
- Improve the new user onboarding (convert more invites to active users)
- Add more share triggers in the product

If K = 0.9-1.0 (near-critical):
- Find the last 10% improvement (it's worth massive growth)
- Test different share channels (email vs. social vs. link)
- Add viral moments at different stages (not just signup)

If K > 1.0 (viral growth):
- Protect the viral loop (don't break it)
- Measure cycle time (faster cycles = faster growth)
- Add more virality to sustain as market saturates
```

### Viral Cycle Time

Viral coefficient alone isn't enough. You also need to measure cycle time:

```
Viral Cycle Time = Time from user signup to that user bringing another user

Shorter cycle = faster growth

Example:
- K = 1.0, Cycle = 7 days → User base doubles every 7 days
- K = 0.5, Cycle = 3 days → Slower but faster compounding

Optimize for:
1. Reduce time to first share trigger
2. Make sharing immediate (during onboarding)
3. Accelerate invite conversion (improve new user experience)
```

## Metric 2: Time-to-Value (TTV)

### What It Is

Time-to-value measures how long it takes a new user to experience the core value of your product. This is the single most important PLG metric.

```
TTV = Time from signup to "aha moment" completion

Examples:
- Canva: Time to first design
- Slack: Time to 2,000 team messages
- Calendly: Time to first scheduled meeting
- Notion: Time to first published page
- Zapier: Time to first active Zap
```

### How to Measure TTV

```typescript
class TimeToValueTracker {
  async calculateTTV() {
    const users = await db.users.findMany({
      where: {
        createdAt: { gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) },
        ahaMomentCompleted: true
      },
      select: {
        id: true,
        createdAt: true,
        ahaMomentCompletedAt: true
      }
    })

    // Calculate individual TTFs
    const ttvs = users.map(user => ({
      userId: user.id,
      time: (user.ahaMomentCompletedAt - user.createdAt) / 1000 / 60 // minutes
    }))

    // Aggregate
    const sorted = ttvs.sort((a, b) => a.time - b.time)
    const total = sorted.length

    return {
      median: sorted[Math.floor(total / 2)].time,
      average: sorted.reduce((s, u) => s + u.time, 0) / total,
      p25: sorted[Math.floor(total * 0.25)].time,
      p75: sorted[Math.floor(total * 0.75)].time,
      distribution: {
        under5min: sorted.filter(u => u.time < 5).length / total,
        under15min: sorted.filter(u => u.time < 15).length / total,
        under60min: sorted.filter(u => u.time < 60).length / total,
        over60min: sorted.filter(u => u.time >= 60).length / total
      }
    }
  }

  async getTTVBySegment() {
    return {
      byAcquisitionChannel: await this.segmentBy('acquisitionChannel'),
      byUserRole: await this.segmentBy('role'),
      byPlan: await this.segmentBy('plan'),
      byReferralSource: await this.segmentBy('referralSource')
    }
  }

  async segmentBy(field) {
    const users = await db.users.groupBy({
      by: [field],
      where: { ahaMomentCompleted: true },
      _count: { id: true },
      _avg: {
        timeToValue: true
      }
    })
    return users
  }
}
```

### TTV Benchmarks

| Product Type | Good TTV | Great TTV | World-Class |
|-------------|----------|-----------|-------------|
| Simple tool | < 5 min | < 2 min | < 30 sec |
| Content creation | < 10 min | < 5 min | < 2 min |
| Collaboration | < 30 min | < 15 min | < 5 min |
| Data/analytics | < 60 min | < 30 min | < 15 min |
| Developer tool | < 30 min | < 15 min | < 5 min |

### Reducing TTV

```
TTV Optimization Checklist:

1. Remove signup friction
   - Social login saves 30 seconds average
   - No email verification needed immediately
   - Skip onboarding questions that aren't essential

2. Pre-configure defaults
   - Templates for common use cases  
   - Sample data pre-loaded
   - Smart defaults (automatically detect user's situation)

3. Guide to the aha moment
   - Onboarding checklist (3 steps max)
   - Tooltips pointing to the core action
   - One-click example generation

4. Remove all non-essential steps
   - Every click before the aha moment is a potential drop-off
   - Hide settings/configuration until later
   - Skip the "welcome" video — they can watch later

5. Show value during the process
   - "You're saving [X] by doing it this way"
   - Progress bar: "You're 80% there"
   - Pre-comparison: "Without [Product], this takes 10 min. With it, 30 seconds."
```

### The "5-Minute Test"

Before every onboarding change, ask: "Can a new user experience the core value in under 5 minutes?" If not, you haven't optimized enough.

```
5-Minute Test Checklist:

[ ] User can sign up in under 30 seconds
[ ] No email verification required
[ ] Template or sample data is provided
[ ] First action is guided (tooltip or flow)
[ ] Core value is demonstrated in < 5 minutes
[ ] User knows what to do next after aha moment
```

## Metric 3: Self-Serve Conversion Rate

### What It Is

The percentage of free users who convert to paid without any human intervention.

```
Self-Serve Conversion Rate = 
(Users who started a paid plan / Total users who completed activation) × 100
```

### How to Measure Self-Serve Conversion

```typescript
class SelfServeConversionAnalyzer {
  async analyzeConversionFunnel() {
    const funnel = [
      { stage: 'visitor', query: () => db.visitors.count() },
      { stage: 'signup', query: () => db.users.count() },
      { stage: 'activated', query: () => db.users.count({ where: { isActivated: true } }) },
      { stage: 'trial_started', query: () => db.subscriptions.count({ where: { status: 'trialing' } }) },
      { stage: 'paid', query: () => db.subscriptions.count({ where: { status: 'active' } }) }
    ]

    const results = []
    for (const stage of funnel) {
      results.push({
        stage: stage.stage,
        count: await stage.query()
      })
    }

    // Calculate conversion between each stage
    return results.map((r, i) => ({
      ...r,
      conversionFromPrevious: i === 0 ? null : 
        `${((r.count / results[i - 1].count) * 100).toFixed(1)}%`
    }))
  }

  async getConversionByUserType() {
    return {
      organic: await this.conversionForSegment('organic'),
      referral: await this.conversionForSegment('referral'),
      paid: await this.conversionForSegment('paid'),
      direct: await this.conversionForSegment('direct')
    }
  }

  async conversionForSegment(channel) {
    const users = await db.users.findMany({
      where: { acquisitionChannel: channel }
    })

    const paid = users.filter(u => u.subscription?.status === 'active')
    return {
      total: users.length,
      paid: paid.length,
      conversionRate: users.length > 0 ? 
        `${((paid.length / users.length) * 100).toFixed(1)}%` : '0%'
    }
  }
}
```

### Self-Serve Conversion Benchmarks

| Metric | Weak | Good | Great |
|--------|------|------|-------|
| Signup → Trial | < 30% | 30-50% | 50%+ |
| Trial → Paid | < 10% | 10-25% | 25%+ |
| Free → Paid (no trial) | < 3% | 3-8% | 8%+ |
| Visitor → Paid | < 0.5% | 0.5-2% | 2%+ |

### Improving Self-Serve Conversion

```
Conversion Rate Optimization:

1. Improve activation first
   - Users who don't experience value won't pay
   - Fix activation before conversion
   - Each 10% improvement in activation = 5-10% improvement in conversion

2. Upgrade prompts at the right moment
   - When user hits a limit (usage, features)
   - When user achieves a success (celebrate → upgrade)
   - When user is in the middle of a flow (don't interrupt)
   - When user is frustrated by a restriction

3. Pricing page optimization
   - Comparison table makes decision easier
   - Annual pricing discount (20-30% off) increases LTV
   - Social proof: "Join 10,000+ teams"
   - FAQ addresses common objections

4. Trial structure matters
   - 14-day trial is standard (balance of urgency + time to value)
   - No credit card required (reduces signup friction)
   - Full features in trial (no crippled trial)
   - Clear trial end communication (countdown, reminders)

5. Reduce friction to purchase
   - Upgrade in 2 clicks from within the product
   - No sales call needed
   - Multiple payment methods (card, PayPal)
   - Auto-billing from day one
```

### The Self-Serve Conversion Funnel Analysis

Map your specific funnel:

```
Example Funnel:

10,000 monthly visitors
  → 8,000 bounce (80% bounce rate)
  → 2,000 signup (20% conversion)
    → 800 complete onboarding (40% activation rate)
      → 200 start trial (25% trial start rate)
        → 50 convert to paid (25% trial→paid)
        → 3% overall visitor→paid conversion
```

Find the biggest drop-off and fix it first.

## Metric 4: Expansion MRR

### What It Is

Expansion MRR measures revenue growth from existing customers through upgrades, add-ons, and increased usage.

```
Expansion MRR = [Upgrades + Add-ons + Usage Growth] - [Downgrades + Contractions]

Net Expansion MRR = 
(Starting MRR + Expansion - Contraction - Churn) / Starting MRR
```

### How to Measure Expansion MRR

```typescript
class ExpansionMRRAnalyzer {
  async calculateExpansionMRR(dateRange) {
    // Existing customers at start of period
    const startCustomers = await db.subscriptions.findMany({
      where: {
        startDate: { lte: dateRange.start },
        status: 'active'
      },
      include: { plan: true }
    })

    const startingMRR = startCustomers.reduce(
      (sum, sub) => sum + sub.plan.price, 0
    )

    // Track changes during the period
    const upgrades = await db.subscriptionChanges.findMany({
      where: {
        type: 'upgrade',
        date: { gte: dateRange.start, lte: dateRange.end }
      }
    })

    const downgrades = await db.subscriptionChanges.findMany({
      where: {
        type: 'downgrade',
        date: { gte: dateRange.start, lte: dateRange.end }
      }
    })

    const churned = await db.subscriptions.findMany({
      where: {
        cancelledAt: { gte: dateRange.start, lte: dateRange.end }
      }
    })

    const upgradeMRR = upgrades.reduce((sum, u) => sum + u.priceChange, 0)
    const downgradeMRR = downgrades.reduce((sum, d) => sum + d.priceChange, 0)
    const churnedMRR = churned.reduce((sum, c) => sum + c.plan.price, 0)

    const endingMRR = startingMRR + upgradeMRR + downgradeMRR - churnedMRR

    return {
      startingMRR,
      endingMRR,
      upgradeMRR,
      downgradeMRR,
      churnedMRR,
      netExpansionMRR: upgradeMRR + downgradeMRR, // negative if more downgrades
      netRetentionRate: (endingMRR / startingMRR) * 100,
      expansionBreakdown: {
        upgrades: upgradeMRR,
        downgrades: downgradeMRR,
        churn: churnedMRR,
        net: upgradeMRR + downgradeMRR - churnedMRR
      }
    }
  }

  async expansionBySegment() {
    return {
      byPlan: await this.segmentExpansion('plan'),
      byCohort: await this.segmentExpansion('cohort'),
      byFeature: await this.featureAdoptionImpact()
    }
  }
}
```

### Expansion MRR Benchmarks

| Gross MRR Churn | Net MRR Retention | Assessment |
|-----------------|-------------------|------------|
| > 5% monthly | < 80% | Negative expansion — losing existing revenue |
| 3-5% monthly | 80-100% | Neutral — barely replacing churned revenue |
| 1-3% monthly | 100-120% | Positive — existing customers grow |
| < 1% monthly | 120%+ | Excellent — strong expansion engine |

### PLG Expansion Drivers

```
Expansion in a PLG product comes from:

1. Natural usage growth
   - Users simply use the product more
   - Usage-based pricing captures this growth automatically
   - No sales needed — pricing model does the work

2. Team/seat expansion
   - More people on the team → more seats
   - Organic (team grows) or viral (existing member invites more)
   - Inherent PLG expansion

3. Feature adoption
   - Users discover and adopt higher-tier features
   - In-app prompts: "This is a Pro feature. Upgrade to use it."
   - Feature gating drives upgrades naturally

4. Plan upgrades
   - Self-serve upgrade in 2 clicks
   - Upgrade triggered by hitting limits
   - Upgrade triggered by seeing what higher tiers offer

5. Add-ons and integrations
   - Additional paid features
   - Integration marketplace
   - API access (usage-based)
```

### Building Expansion into PLG

```typescript
class ExpansionEngine {
  async identifyUpgradeOpportunities(userId) {
    const user = await db.users.findUnique({
      where: { id: userId },
      include: {
        subscription: { include: { plan: true } }
      }
    })

    const usage = await this.getCurrentUsage(userId)
    const limits = await this.getPlanLimits(user.subscription.plan)
    const opportunities = []

    // Usage-based upgrade trigger
    if (usage.queries > limits.queries * 0.8) {
      opportunities.push({
        type: 'usage_limit',
        current: usage.queries,
        limit: limits.queries,
        suggestedPlan: 'pro',
        reason: `You've used ${usage.queries} of ${limits.queries} queries`
      })
    }

    // Feature-based upgrade trigger
    const blockedFeatures = await this.getBlockedFeatures(userId)
    blockedFeatures.forEach(feature => {
      opportunities.push({
        type: 'feature_access',
        feature: feature.name,
        suggestedPlan: feature.requiredPlan,
        reason: `Unlock ${feature.name} by upgrading`
      })
    })

    // Team size trigger
    if (user.teamSize >= limits.maxTeamSize) {
      opportunities.push({
        type: 'team_limit',
        current: user.teamSize,
        limit: limits.maxTeamSize,
        suggestedPlan: 'business',
        reason: 'Add more team members'
      })
    }

    return opportunities
  }

  async triggerExpansion(userId) {
    const opportunities = await this.identifyUpgradeOpportunities(userId)
    
    if (opportunities.length > 0) {
      // Show the most compelling opportunity
      const best = opportunities.sort((a, b) => b.urgency - a.urgency)[0]
      
      await this.showUpgradePrompt(userId, best)
      return { prompted: true, reason: best.reason }
    }

    return { prompted: false }
  }
}
```

## Metric 5: Net Promoter Score (NPS) for PLG

### Why NPS Matters

NPS measures how likely users are to recommend your product. In PLG, this directly correlates with viral growth and organic acquisition.

### How to Measure NPS

```
Survey question: "How likely are you to recommend [Product] to a 
friend or colleague?" (0-10)

9-10: Promoters
7-8: Passives
0-6: Detractors

NPS = (% Promoters - % Detractors) × 100

Example:
- 50% Promoters
- 30% Passives
- 20% Detractors
- NPS = 50 - 20 = 30
```

### NPS Benchmarks for SaaS

| NPS Score | Assessment |
|-----------|------------|
| < 0 | Troubling — product has significant issues |
| 0-20 | Needs improvement — basic expectations aren't met |
| 20-40 | Good — product delivers expected value |
| 40-60 | Great — product delights users |
| 60+ | Excellent — users actively evangelize |

### PLG NPS Correlation

```
NPS correlates with PLG metrics:

NPS 30 ↔ Weak virality (< 0.5 K-factor)
NPS 40 ↔ Moderate virality (0.5-0.8 K-factor)
NPS 50 ↔ Strong virality (0.8-1.0 K-factor)
NPS 60+ ↔ Viral growth (> 1.0 K-factor)

If your NPS is high but virality is low:
→ The sharing experience is broken (not the product)
→ Users love the product but don't naturally share it

If your NPS is low but virality is high:
→ Growth is being driven by incentives, not love
→ Risky — if you remove incentives, growth stops
```

## Metric 6: Product Adoption Rate

### What It Is

Measures how many users adopt key features that drive retention and expansion.

```
Adoption Rate = 
(Users who used feature / Total active users) × 100

Core Feature Adoption = 
(Users who completed core action / Total activated users) × 100
```

### Feature Adoption Funnel

```typescript
class FeatureAdoptionAnalyzer {
  async analyzeFeatureAdoption(featureName, dateRange) {
    const totalUsers = await db.users.count({
      where: {
        lastActiveAt: { gte: dateRange.start }
      }
    })

    const featureUsers = await db.events.groupBy({
      by: ['userId'],
      where: {
        event: featureName,
        createdAt: { gte: dateRange.start, lte: dateRange.end }
      }
    })

    return {
      feature: featureName,
      totalActiveUsers: totalUsers,
      featureUsers: featureUsers.length,
      adoptionRate: (featureUsers.length / totalUsers) * 100,
      adoptionByCohort: await this.adoptionByCohort(featureName)
    }
  }

  async getAdoptionFunnel() {
    // Track user progression through features
    const features = ['signup', 'onboarded', 'first_query', 'first_export', 'shared', 'upgraded']
    
    const funnel = []
    for (const feature of features) {
      const users = await db.events.groupBy({
        by: ['userId'],
        where: { event: feature }
      })
      funnel.push({
        feature,
        userCount: users.length,
        dropoff: funnel.length > 0 ?
          `${((1 - users.length / funnel[funner.length - 1].userCount) * 100).toFixed(0)}%` : 'N/A'
      })
    }
    return funnel
  }
}
```

### Feature Adoption Benchmarks

| Feature Type | Target Adoption | Notes |
|-------------|----------------|-------|
| Core feature | 80%+ | Must-have for all users |
| Secondary feature | 40-60% | Valuable but not essential |
| Advanced feature | 20-40% | Power user differentiator |
| Referral/sharing | 20%+ | Depends on viral design |
| Integration | 10-30% | Depends on ecosystem |

### Improving Feature Adoption

```
1. In-app guidance
   - Feature announcements on login
   - Tooltips when user first encounters a feature
   - "Try this" buttons with pre-filled examples

2. Progressive disclosure
   - Don't show all features at once
   - Unlock advanced features when user is ready
   - "You've used [basic feature] 5 times — try [advanced]"

3. Feature adoption emails
   - "Did you know? [Feature] can help you [benefit]"
   - "Power users love [Feature]. Here's why."
   - Triggered after user completes related action

4. Social proof in-product
   - "80% of users in your role use this feature"
   - "Your team hasn't tried [Feature] yet"
   - Use case examples from similar users
```

## The PLG Metrics Dashboard

Create a single dashboard you check weekly:

```
PLG METRICS DASHBOARD

VIRALITY:
  Viral Coefficient (K): ___ (target: > 1.0)
  Viral Cycle Time: ___ days (target: < 7)
  Invitations per User: ___ (target: > 3)
  Invite Conversion Rate: ___% (target: > 20%)

ACTIVATION:
  Time to Value (median): ___ min (target: < 5)
  Activation Rate (Day 1): ___% (target: > 40%)
  Activation Rate (Day 7): ___% (target: > 60%)
  Funnel Drop-off: ___ → ___ → ___

CONVERSION:
  Free → Paid: ___% (target: > 5%)
  Trial → Paid: ___% (target: > 20%)
  Visitor → Paid: ___% (target: > 1%)
  Avg Time to Pay: ___ days (target: < 30)

EXPANSION:
  Net Revenue Retention: ___% (target: > 100%)
  Expansion MRR: $___ (target: > 0)
  Upgrade Rate: ___% (target: > 5%)
  Feature Adoption (Core): ___%

RETENTION:
  D1 Retention: ___% (target: > 50%)
  D7 Retention: ___% (target: > 30%)
  D30 Retention: ___% (target: > 20%)
  Monthly Churn: ___% (target: < 5%)

NPS:
  Current NPS: ___ (target: > 40)
  Promoters: ___% (target: > 40%)
  Detractors: ___% (target: < 20%)

PLG HEALTH SCORE: ___ / 100
```

## Monthly PLG Review

Spend 2 hours each month analyzing these metrics:

```
1. What's trending up?
   - Celebrate and protect
   - Identify what caused the improvement
   - Double down on what's working

2. What's trending down?
   - Investigate root cause
   - Is it seasonal, product change, or market change?
   - Create action plan to reverse

3. What's the biggest opportunity?
   - Largest drop-off in the funnel
   - Lowest adoption feature
   - Viral coefficient below 1.0

4. What's the biggest risk?
   - Churn increasing
   - Viral coefficient decreasing
   - NPS declining

5. Next month's focus:
   - ONE metric to improve
   - Specific actions to take
   - Expected impact
```

## The Solo Founder's PLG Metrics Focus

With limited time, focus on the metrics that have the highest impact:

```
PRIORITY 1: Activation Rate
- If users don't activate, nothing else matters
- Check: Time to value < 5 min, activation rate > 40%
- If failing: Fix onboarding first

PRIORITY 2: Viral Coefficient
- This is your growth engine as a solo founder
- Check: K > 1.0 for exponential growth
- If failing: Fix sharing mechanic

PRIORITY 3: Self-Serve Conversion
- This replaces your sales team
- Check: Free → Paid > 5%
- If failing: Fix upgrade triggers or pricing

PRIORITY 4: NRR (Net Revenue Retention)
- Existing customers should grow, not shrink
- Check: NRR > 100%
- If failing: Fix expansion mechanics or fix churn

PRIORITY 5: Everything Else
- Only look at other metrics monthly
- Don't optimize what doesn't matter yet
```

## Final Thoughts

- **PLG metrics are leading indicators of SaaS success.** Traditional SaaS metrics (MRR, ARR) are lagging indicators. PLG metrics tell you what will happen next.

- **Viral coefficient is the most powerful growth metric.** If K > 1.0, you grow exponentially. If K < 1.0, you need other channels. Focus on getting K above 1.0.

- **Time-to-value is the most underrated metric.** Most SaaS products take too long to deliver value. Every minute you shave off TTV increases activation, retention, and virality.

- **Self-serve conversion is your sales team.** If conversion is below 5%, your product isn't compelling enough or your upgrade flow is broken.

- **Expansion MRR is the silent growth engine.** Growing existing customers is cheaper than acquiring new ones. Build expansion into your product and pricing model.

- **Track only what you'll act on.** Don't build dashboards full of metrics you never use. Focus on the 5-7 metrics that directly inform your decisions.

Your product IS your growth engine. These metrics tell you how well that engine is running. Monitor them, improve them, and your SaaS will grow with or without a marketing budget.
