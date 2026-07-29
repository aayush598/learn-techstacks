# Setting Up Product Analytics

A practical guide for solo founders to implement product analytics — choosing the right tool, defining what to track, and building a data-informed product development process without drowning in data.

---

## Part 1: Why Product Analytics Matters for Solo Founders

### The Solo Founder Data Problem

As a solo founder, you have a unique relationship with your product:
- You know every feature intimately
- You talk to customers directly
- You can feel when something is wrong

But feelings lie. Data tells the truth. Product analytics gives you:

1. **Objective truth about usage** — You think feature X is critical. Only 8% of users touch it.
2. **Early warning of churn** — Usage drops 3 weeks before cancellation happens.
3. **Evidence for prioritization** — Stop building what nobody uses. Double down on what drives retention.
4. **Growth insights** — Discover which actions correlate with conversion.

### When to Set Up Product Analytics

| Stage | Action | Tool |
|-------|--------|------|
| Pre-revenue / Idea | Manual tracking only (talk to users) | Pen and paper |
| < 100 users | Basic event tracking | PostHog (self-hosted, free) |
| 100-1,000 users | Structured analytics | Amplitude (free tier) or Mixpanel |
| 1,000+ users | Full product analytics suite | Paid plan of any of the above |

**The earlier the better** — you want historical data before you need it.

---

## Part 2: Tool Comparison

### PostHog

**Best for:** Solo founders who want to self-host, need event pipelines, or want an all-in-one product + web analytics suite for free.

**Pricing:**
- Self-hosted: Free (unlimited events)
- Cloud: Free up to 1M events/month, then usage-based

**Key Features:**
- Event tracking (custom events, autocapture)
- Funnel analysis
- Retention analysis (cohorts)
- Session recording
- Feature flags
- A/B testing (experiments)
- Heatmaps
- Web analytics (pageviews, traffic)
- Group analytics (accounts)
- Correlation analysis

**Pros for Solo Founders:**
- Most generous free tier (unlimited self-hosted)
- All-in-one (no need for separate web analytics)
- Feature flags included (lets you ship to subsets)
- Open source (no vendor lock-in)
- Session recordings help you understand user struggles
- Self-host option means no data leaves your infrastructure

**Cons for Solo Founders:**
- Self-hosting requires server management
- Cloud version can get expensive at scale
- UI can be overwhelming with options
- Less mature than Amplitude/Mixpanel for some analyses
- Autocapture can create noise

**Setup Time:** 1-2 hours (self-hosted) or 15 minutes (cloud)

**Use When:** You want unlimited event tracking without paying, need session recordings, or value open source.

### Amplitude

**Best for:** Product-led growth, behavioral cohorts, and advanced analytics.

**Pricing:**
- Free: Up to 10M actions/month, 2 years data retention
- Plus: $49/month (billed annually)
- Growth: Custom pricing

**Key Features:**
- Behavioral event tracking
- Advanced cohort analysis
- Funnel analysis with conversion diagnostics
- Retention analysis
- Pathfinder (user flow visualization)
- Microscope (session replay)
- Experiment (A/B testing)
- Predict (churn, conversion predictions)

**Pros for Solo Founders:**
- Best-in-class cohort and funnel analysis
- Generous free tier (10M events/month)
- Excellent for understanding user behavior patterns
- Strong API and integrations
- Good mobile SDK support

**Cons for Solo Founders:**
- Can be overwhelming for simple needs
- Free tier limited to 2 years data retention
- Session replay is a paid add-on
- Less useful for web analytics (traffic, pageviews)
- Learning curve is steeper than PostHog

**Setup Time:** 2-3 hours (SDK integration + event planning)

**Use When:** You need complex funnel/cohort analysis, have product-led growth, or plan to scale past 10M events/month on a budget.

### Mixpanel

**Best for:** Companies that need real-time analytics and strong data modeling.

**Pricing:**
- Free: Up to 20M events/month (limited features)
- Growth: $25/month (billed annually) for 1M events
- Enterprise: Custom pricing

**Key Features:**
- Event tracking
- Funnel analysis
- Retention analysis
- Impact analysis (what actions predict outcomes)
- Signal (AI anomaly detection)
- Flows (user path analysis)
- Experiments (A/B testing)
- Data modeling (identities, groups, properties)

**Pros for Solo Founders:**
- Real-time event processing
- Strong data modeling for complex products
- Impact analysis is powerful for product decisions
- User-friendly interface
- Good documentation and community

**Cons for Solo Founders:**
- Free tier has limited features
- Can get expensive as you grow (pricing by volume)
- Less generous than Amplitude's free tier
- No session recording built in
- Overkill for simple products

**Setup Time:** 2-4 hours

**Use When:** You need real-time analytics, have complex event modeling needs, or prefer Mixpanel's interface.

### Plausible

**Best for:** Simple web analytics (pageviews, traffic sources, goals).

**Pricing:** €9/month for 10K pageviews (flat rate, no per-event pricing)

**Key Features:**
- Pageview tracking
- Goal conversion tracking
- Traffic sources
- Country breakdown
- Device/browser breakdown
- Custom events (limited)
- No cookies (GDPR compliant)

**Pros for Solo Founders:**
- Dead simple to set up (one script tag)
- Privacy-first (no cookie banner needed)
- Clean, minimal interface
- Predictable pricing (flat rate, not usage-based)
- Lightweight (doesn't slow down your site)

**Cons for Solo Founders:**
- Web analytics only (no product analytics)
- Cannot track user-level behavior
- No funnel analysis
- No retention cohorts
- Not suitable for SaaS product analysis

**Setup Time:** 10 minutes

**Use When:** You need simple web analytics (traffic, marketing attribution) alongside a dedicated product analytics tool.

### Recommendation Matrix

| Criteria | PostHog | Amplitude | Mixpanel | Plausible |
|----------|---------|-----------|----------|-----------|
| Event tracking | ★★★★★ | ★★★★★ | ★★★★★ | ★★ |
| Funnels | ★★★★ | ★★★★★ | ★★★★★ | ★ |
| Retention | ★★★★ | ★★★★★ | ★★★★★ | ★ |
| Session recording | ★★★★★ | ★★ | ★ | ★ |
| Feature flags | ★★★★★ | ★ | ★★ | ★ |
| A/B testing | ★★★★ | ★★★ | ★★★ | ★ |
| Web analytics | ★★★★ | ★ | ★ | ★★★★★ |
| Free tier | ★★★★★ | ★★★★★ | ★★★ | ★★ |
| Ease of setup | ★★★★ | ★★★ | ★★★ | ★★★★★ |
| Solo founder value | ★★★★★ | ★★★★ | ★★★ | ★★★ |

**The Solo Founder Recommendation:**

1. **Start with PostHog (self-hosted)** for unlimited free product analytics + session recordings + feature flags
2. **Add Plausible** for simple web traffic analytics ($9/month)
3. **Upgrade to Amplitude** if/when you need advanced behavioral cohorts and funnel diagnostics

---

## Part 3: What to Track — The Solo Founder Event Taxonomy

### The Minimum Viable Event Set

Don't track everything. Track what drives decisions. Start with these events:

```
Core Events (track these from day one):

Identity Events (user setup)
  - User Signed Up        { method: 'email' | 'google' | 'github' }
  - User Set Up Profile   { company, role }
  - User Invited Team     { invite_count }

Activation Events (aha moment)
  - First Core Action     { [your product's primary action] }
  - First Export          { export_type }
  - First Integration     { integration_name }
  - First Share/Invite    { share_type }

Engagement Events (ongoing usage)
  - App Opened            { source: 'web' | 'mobile' | 'api' }
  - Core Action           { [repeat of primary action] }
  - Feature Used          { feature_name, duration }
  - Search Performed      { query, results_count }

Monetization Events
  - Started Trial         { plan, trial_duration }
  - Viewed Pricing        { page_location }
  - Upgraded Plan         { from_plan, to_plan, price }
  - Downgraded Plan       { from_plan, to_plan }
  - Canceled Subscription { reason, feedback }
  - Reactivated           { previous_plan }
```

### Defining Your "Core Action"

Your core action is the ONE thing that defines your product's value. It's different for every product:

| Product Type | Core Action |
|-------------|-------------|
| Project management | Task Created or Task Completed |
| Analytics | Report Generated |
| CRM | Deal Updated |
| Communication | Message Sent |
| Design tool | Design Published |
| API tool | API Call Made |
| Content tool | Content Published |
| E-commerce | Order Placed |
| Education | Lesson Completed |

If you can't identify ONE core action, your product might be too broad for a solo founder to build.

### Event Naming Convention

Establish a consistent naming convention from day one:

```
[Object] [Action] [Context]

Examples:
  User Signed Up
  Report Generated
  Invoice Paid
  Team Member Added
  Integration Connected
  Plan Upgraded
  Task Completed
  API Key Created
```

**Naming rules:**
1. Use past tense (Signed Up, not Sign Up)
2. Use Title Case consistently
3. Be specific (Report Generated, not Report Saved)
4. No abbreviations (Integration Connected, not Int Conn)
5. Use underscores or spaces consistently (pick one)

### Event Properties

Every event should carry context:

```
Event: Task Created
Properties:
  - task_type: 'bug' | 'feature' | 'improvement'
  - project_id: string
  - assignee_count: number
  - due_date_set: boolean
  - priority: 'low' | 'medium' | 'high' | 'critical'
  - source: 'manual' | 'import' | 'api'
  - is_first_task: boolean
```

**Rule of thumb:** Each event should have 3-7 properties. Too few and you can't segment. Too many and you'll never use most.

### User Properties

Track these for every user:

```
User Properties (set once, update as needed):

Identity:
  - user_id (internal)
  - email
  - name
  - company
  - role / title
  - team_size

Account:
  - plan_tier ('free' | 'basic' | 'pro' | 'enterprise')
  - subscription_status ('trialing' | 'active' | 'canceled' | 'past_due')
  - mrr (calculated, updated monthly)
  - signup_date
  - acquisition_channel ('organic' | 'paid' | 'referral' | 'social')
  - referral_source (specific URL or campaign)

Usage:
  - last_seen_date
  - days_since_signup
  - total_logins
  - features_used (array of feature names)
  - core_action_count (total times core action performed)
  - integration_count
  - team_member_count
```

---

## Part 4: Implementation Guide

### Step 1: Choose Your Tool

Based on your stage:

| Stage | Tool Choice | Rationale |
|-------|-------------|-----------|
| Pre-revenue | None (manual only) | Don't over-engineer before you have users |
| Launched (< 100 users) | PostHog self-hosted | Free, gives you everything you need |
| Growing (100-1K users) | Amplitude free tier | Better cohort analysis for growth |
| Scaling (1K+ users) | Amplitude paid or Mixpanel | Need advanced segmentation at scale |

### Step 2: Identify Your Events

Don't start coding yet. First, map out your events:

1. Draw your user journey (signup → activation → daily use → upgrade/cancel)
2. Identify 10-15 key moments
3. Define event names and properties
4. Write them in a tracking plan document

**Tracking Plan Template:**

```yaml
events:
  - name: User Signed Up
    description: User creates an account
    properties:
      - name: method
        type: string
        values: ['email', 'google', 'github']
      - name: referral_code
        type: string
        required: false
    
  - name: First Core Action
    description: User performs core action for first time
    properties:
      - name: time_since_signup
        type: number
        unit: minutes
      - name: from_onboarding
        type: boolean

  # ... more events
```

### Step 3: Implement SDK

#### PostHog Implementation (JavaScript)

```javascript
// 1. Install: npm install posthog-js
// 2. Initialize in your app entry point

import posthog from 'posthog-js';

// Initialize (once, on app load)
posthog.init('YOUR_API_KEY', {
  api_host: 'https://app.posthog.com', // or your self-hosted URL
  person_profiles: 'identified_only', // Don't track anonymous users
  capture_pageview: true, // Automatic pageview tracking
  autocapture: false, // Disable autocapture (too noisy for most SaaS)
});

// Identify user (after login/signup)
posthog.identify(user.id, {
  email: user.email,
  name: user.name,
  plan: user.plan,
  signupDate: user.created_at,
});

// Track events
// After signup:
posthog.capture('User Signed Up', {
  method: 'google',
});

// After core action:
posthog.capture('Task Created', {
  task_type: 'feature',
  project_id: projectId,
  assignee_count: assignees.length,
  priority: 'high',
});

// Set user properties
posthog.people.set({
  plan_tier: 'pro',
  team_size: 5,
});
```

#### Amplitude Implementation (JavaScript)

```javascript
// 1. Install: npm install @amplitude/analytics-browser
// 2. Initialize

import * as amplitude from '@amplitude/analytics-browser';

amplitude.init('YOUR_API_KEY', {
  defaultTracking: {
    pageViews: true,
    sessions: true,
    formInteractions: false,
    fileDownloads: false,
  },
});

// Identify user
amplitude.setUserId(user.id);
amplitude.setUserProperties({
  plan: user.plan,
  email: user.email,
  signupDate: user.created_at,
});

// Track event
amplitude.track('Task Created', {
  task_type: 'feature',
  priority: 'high',
});
```

### Step 4: Set Up Key Dashboards

#### Dashboard 1: Activation Funnel

Track the critical path from signup to "aha moment":

```
Signup (100%)
  → Set up profile (72%)
    → First integration (58%)
      → First core action (42%) ← THIS IS YOUR ACTIVATION RATE
        → First export (35%)
          → Second core action (31%)
```

#### Dashboard 2: Retention Curve

Track what percentage of users come back:

```
Day 0: 100% (signup)
Day 1: 45% (next day)
Day 7: 28% (one week)
Day 30: 18% (one month)
Day 60: 14%
Day 90: 12%
```

Benchmark your retention against:
- Good SaaS: 40%+ Day 1, 20%+ Day 7, 10%+ Day 30
- Great SaaS: 50%+ Day 1, 30%+ Day 7, 15%+ Day 30

#### Dashboard 3: Feature Adoption Matrix

Track which features users adopt and when:

```
Feature          | Ever Used | Weekly Active | Stickiness | Core?
-----------------|-----------|---------------|------------|------
Core: Task Create| 92%       | 68%           | 74%        | ✅
Core: Task Complete| 85%    | 45%           | 53%        | ✅
Project Dashboard| 55%       | 22%           | 40%        | ❌
Calendar View    | 30%       | 8%            | 27%        | ❌
API Access       | 18%       | 12%           | 67%        | Niche
Team Management  | 25%       | 5%            | 20%        | ❌
Export Reports   | 40%       | 15%           | 38%        | ❌
```

### Step 5: Set Up Key Metrics

Create these metric definitions in your analytics tool:

```
Metric 1: Weekly Active Users (WAU)
  Definition: Users who performed a core action in the last 7 days
  Why: Engagement health
  
Metric 2: Activation Rate
  Definition: % of signups who perform core action within 7 days
  Why: Predicts retention
  
Metric 3: Feature Stickiness
  Definition: DAU using core feature / Total DAU
  Why: Shows if core feature is habit-forming
  
Metric 4: Bounce Rate (product)
  Definition: % of new users who don't perform a core action within 24 hours
  Why: Onboarding effectiveness
  
Metric 5: Power User Ratio
  Definition: % of users who perform core action 5+ times per week
  Why: Product-market fit signal
```

---

## Part 5: The Solo Founder's Analytics Workflow

### Daily (5 minutes)

Check:
1. Any anomalies? (zero signups, massive usage drop)
2. Any session recordings showing user struggles?
3. One interesting data point → translate to Slack note

### Weekly (30 minutes)

Review:
1. Activation funnel (is onboarding working?)
2. Weekly active users (are we growing?)
3. Feature adoption (is anyone using what we built?)
4. Churn indicators (usage decline in existing customers?)
5. Update tracking plan if needed

### Monthly (1 hour)

Deep dive:
1. Retention cohort analysis (are newer cohorts retaining better?)
2. Feature adoption trends (over last 3 months)
3. Power user analysis (what do retained users have in common?)
4. Identify features to kill (built 3 months ago, < 10% usage)
5. Plan next month's tracking improvements

### Quarterly (2 hours)

Strategic:
1. Product-market fit score (would users be very disappointed without your product?)
2. Competitive feature analysis
3. Long-term retention trends (6+ month cohorts)
4. Revenue correlation (which events correlate with upgrading?)
5. Full tracking plan audit (are we missing anything important?)

---

## Part 6: Common Implementation Mistakes

### Mistake 1: Tracking Everything (Data Noise)

**Problem:** You enable autocapture in PostHog and suddenly have 200 event types, most meaningless.

**Fix:** Disable autocapture. Define 15-20 events manually. Add more only when you have a specific question.

### Mistake 2: Inconsistent Event Names

**Problem:** Your code says `task_created`, `Task Created`, and `Create Task` for the same event.

**Fix:** Define your event taxonomy in a tracking plan document. Review it before any sprint.

### Mistake 3: Not Tracking Properties

**Problem:** You know someone did the core action, but not what type, when, or in what context.

**Fix:** Every event needs at least 3 properties. What, when, and how.

### Mistake 4: Premature Optimization

**Problem:** You spend 3 weeks setting up the perfect analytics infrastructure before you have 100 users.

**Fix:** Use PostHog self-hosted (15 minute setup) until you have 1,000 users. Then optimize.

### Mistake 5: Data Hoarding

**Problem:** You collect data but never look at it. Dashboard was built once, never reviewed.

**Fix:** Set a weekly calendar reminder to review analytics. If you're not using the data, stop collecting it.

### Mistake 6: Vanity Metrics

**Problem:** Celebrating 10K signups when only 50 converted to paying.

**Fix:** Focus on events that correlate with revenue. Remove everything else from your dashboard.

---

## Part 7: Privacy and Compliance

### GDPR Requirements (EU Users)

If you have EU users, you need:
1. Cookie consent banner
2. Data processing agreement with your analytics provider
3. Right to data deletion
4. Data stored in EU (or adequacy decision)

**Tool-specific compliance:**
- PostHog (EU cloud): Compliant, data stays in EU
- Amplitude: EU data hosting available (paid plan)
- Mixpanel: EU data hosting available
- Plausible: GDPR compliant by design (no cookies)

### Consent Implementation

```javascript
import posthog from 'posthog-js';

// Don't track until consent
if (localStorage.getItem('analytics_consent') === 'true') {
  posthog.opt_in_capturing();
} else {
  posthog.opt_out_capturing();
}

// On consent button click
function acceptAnalytics() {
  localStorage.setItem('analytics_consent', 'true');
  posthog.opt_in_capturing();
  posthog.capture('Analytics Consent Given');
}
```

### Data Retention Policy

Set up auto-deletion for old data:

| Data Type | Retention | Rationale |
|-----------|-----------|-----------|
| Raw events | 24 months | Cohort analysis needs 12+ months |
| User properties | Indefinite | Identity data should persist |
| Session recordings | 3 months | Debugging purposes only |
| Aggregated data | Indefinite | Anonymized, no PII concerns |

---

## Part 8: Taking Action on Analytics

### The Analytics → Action Loop

```
1. See a data point
2. Form a hypothesis
3. Run an experiment
4. Measure the result
5. Decide: Keep, Kill, or Iterate
```

### Example: Fixing Activation

**Data:** Only 42% of signups perform the core action within 7 days.

**Hypothesis:** Users don't understand the core value during onboarding.

**Experiment:** Add an interactive tutorial on first login.

**Measure:** Check activation rate before → after for 2 weeks.

**Decision:**
- If activation improves to > 50% → Keep the tutorial
- If activation improves but < 50% → Iterate on tutorial content
- If no improvement → Try a different hypothesis

### Example: Identifying Features to Kill

**Data:** Calendar View has 30% adoption and 8% weekly active.

**Hypothesis:** Calendar View is not a core need for our users.

**Experiment:** Move Calendar View to a secondary tab (don't remove yet).

**Measure:** Check if any customer complains (vocal minority) vs usage decline.

**Decision:**
- If nobody notices → Remove the feature
- If 1-2 customers complain → Proactively reach out, see if they'd pay for it as an add-on
- If 10+ customers complain → Keep and improve it

---

## Recommended Tool Setup for Solo Founders

### Stage 1: Pre-Ship (before first user)

```
Set up:
- PostHog self-hosted (Docker on your VPS)
  OR
- Amplitude free tier (quicker setup)

Events to track:
- 10 core events
- User identification on signup

Time investment: 2 hours
```

### Stage 2: Early Launch (0-100 users)

```
Set up:
- Activation funnel dashboard
- Weekly retention report
- Session recordings (review weekly)

What to look for:
- Where do users drop off?
- How long to activation?
- What features are they using?

Time investment: 30 min/week
```

### Stage 3: Growth (100-1,000 users)

```
Set up:
- Behavioral cohorts
- Feature adoption matrix
- Power user analysis
- A/B testing (experiments)

What to look for:
- Cohort trends (improving or declining?)
- Feature stickiness
- What predicts upgrading?
- What predicts churn?

Time investment: 1 hour/week
```

### Stage 4: Scale (1,000+ users)

```
Set up:
- Advanced segmentation
- Predictive analytics
- Custom dashboards for different stakeholders

What to look for:
- Segment-specific trends
- Automated alerts for anomalies
- Long-term retention patterns

Time investment: 2 hours/week (you can hire an analyst now)
```

---

## Quick Start Checklist

```
☐ Choose product analytics tool (PostHog recommended for solo founders)
☐ Install SDK or tracking script
☐ Define 10-15 core events in a tracking plan
☐ Set up user identification on signup
☐ Create activation funnel dashboard
☐ Set up weekly retention report
☐ Add session recordings (PostHog) or session replay (Amplitude paid)
☐ Define first A/B test or experiment
☐ Set calendar reminders: 5min daily, 30min weekly, 1hr monthly
☐ Share dashboard link with an advisor or mentor
```

The goal isn't to track everything. The goal is to track what matters and act on it. Start small, add as you learn, and never let analytics become a distraction from building for your users.