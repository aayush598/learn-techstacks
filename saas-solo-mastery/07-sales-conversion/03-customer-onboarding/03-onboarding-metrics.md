# Onboarding Metrics

## Why Onboarding Metrics Matter

You cannot improve what you don't measure. For solo founders, metrics are especially critical because your time is limited. You need to know exactly where to invest your improvement efforts.

Onboarding metrics tell you:
- How many users are getting value from your product
- Where users get stuck and drop off
- Whether your onboarding improvements are working
- Which users need personal attention
- How your product experience translates to revenue

## The North Star Metric: Activation Rate

### What Is Activation?

Activation is the moment a user experiences the core value of your product for the first time. It's the "aha moment" that makes them think "this is worth continuing."

**Activation is NOT:**
- Signing up (that's acquisition)
- Logging in (that's engagement)
- Completing a tutorial (that's education)
- Staying for 30 days (that's retention)

**Activation IS:**
- The specific action that predicts long-term retention
- Different for every product
- Usually a compound action (multiple steps that lead to value)

### Finding Your Activation Event

**Method 1: Retrospective Analysis**
1. Export data for users who signed up 90+ days ago
2. Identify which users are still active (retained)
3. For each user, list the actions they took in their first 7 days
4. Find the actions that retained users have in common that churned users don't
5. That set of actions is your activation criteria

**Method 2: User Interviews**
1. Interview 10-20 retained users
2. Ask: "What was the moment you realized [Product] was valuable?"
3. Look for patterns in their answers
4. Translate those moments into specific product actions

**Method 3: Cohort Analysis**
1. Group users by signup week
2. For each cohort, measure the relationship between early actions and 30-day retention
3. Identify which early actions have the highest correlation with retention

### Activation Examples

| Product Type | Activation Event |
|-------------|-----------------|
| Collaboration tool | Send a message + receive a reply (within 1 day) |
| Analytics tool | Create a dashboard + view data (within 3 days) |
| Project management | Create a project + invite a team member (within 3 days) |
| Developer tool | Deploy code to production (within 7 days) |
| Design tool | Create a design + export (within 2 days) |
| CRM | Import contacts + send an email (within 7 days) |

### Measuring Activation Rate

```
Activation Rate = (Users who completed activation event) / (Total signups in period)
```

**Benchmark:** 40-60% is good for most B2B SaaS. Below 20% means your onboarding or product has fundamental issues.

**Track by:**
- Overall activation rate (weekly, monthly)
- Activation rate by signup source
- Activation rate by user segment (role, company size, industry)
- Activation rate by product area/feature
- Time from signup to activation (median, P75, P90)

## Time to First Value (TTFV)

### What Is TTFV?

The elapsed time between a user signing up and experiencing the activation event. This is the most important onboarding efficiency metric.

**Why TTFV matters:**
- Every hour of delay increases the chance of churn
- Users are most engaged in their first session — capitalize on it
- Long TTFV means your onboarding has friction
- Short TTFV correlates strongly with higher conversion and retention

### Measuring TTFV

```
TTFV = Time of activation event - Time of signup
```

**Measurements:**
- Median TTFV (the middle value — most representative)
- Average TTFV (skewed by outliers — less useful)
- P75 TTFV (75% of users activate within this time — good for SLOs)
- P90 TTFV (90% activate within this time — identifies problem users)

**Benchmark:**
- Under 5 minutes: Excellent (consumer/utility product)
- 5-30 minutes: Great
- 30-120 minutes: Good
- 2-24 hours: Needs improvement
- 24+ hours: Problematic — likely high drop-off

### Reducing TTFV

**Strategies:**
- Reduce number of steps to activation
- Pre-fill or autodetect settings
- Provide sample data
- Offer one-click setup from common integrations
- Remove required fields that aren't essential
- Show value before setup is complete (demo mode)
- Offer guided setup (video, walkthrough)
- Allow skipping non-essential steps

**Example before/after:**
Before: Signup → Verify email → Set up profile → Import data → Configure settings → Create report = 45 minutes
After: Signup (SSO) → Auto-import data from connected account → See sample report immediately = 3 minutes

## Onboarding Funnel Metrics

### The Onboarding Funnel

```
Signups → Started Onboarding → Completed Step 1 → Completed Step 2 → ... → Activated → Engaged → Converted
```

### Funnel Stage Definitions

**Signups:** User creates an account. (Top of funnel)

**Started Onboarding:** User clicks "Get Started" or begins the first onboarding step. (You expect 95%+ of signups to reach this.)

**Completed Step 1:** User completes the first required action. (E.g., connected data source.)

**Completed Step N:** Each subsequent step in your onboarding checklist.

**Activated:** User completed the activation event (as defined above).

**Engaged:** User returns and uses the product at least N times per week for 2+ weeks.

**Converted:** User becomes a paying customer.

### Drop-Off Analysis

For each stage, calculate the drop-off rate:

```
Drop-off Rate = 1 - (Users who reached Stage N+1 / Users who reached Stage N)
```

**Example funnel:**
| Stage | Users | Drop-off |
|-------|-------|----------|
| Signups | 1,000 | - |
| Started onboarding | 950 | 5% |
| Completed Step 1 | 600 | 37% |
| Completed Step 2 | 450 | 25% |
| Activated | 400 | 11% |
| Engaged | 200 | 50% |
| Converted | 50 | 75% |

**Analysis:** Step 1 has the biggest drop-off (37%). Fixing Step 1 would have the largest impact on overall activation.

### Identifying Bottlenecks

**Bottleneck criteria:**
1. High drop-off rate (> 20% per step)
2. High absolute number of users lost
3. Users spend significantly longer than expected on this step

**Investigation:**
- Watch session recordings of users at the bottleneck step
- Look for confusion, hesitation, errors
- Check if tooltips or documentation are helping
- Interview users who dropped off (if possible)
- Test the step yourself with fresh eyes

## Cohort Analysis

### What Is Cohort Analysis?

Tracking the behavior of groups of users who signed up in the same time period. This shows how your onboarding and product changes affect user behavior over time.

### Weekly Cohort Table

```
Cohort | Size | Wk1 Activated | Wk2 Retained | Wk3 Retained | Wk4 Converted
Jan 1  | 100  | 45%           | 30%          | 25%          | 8%
Jan 8  | 120  | 48%           | 32%          | 28%          | 10%
Jan 15 | 90   | 52%           | 35%          | 30%          | 12%
Jan 22 | 110  | 55%           | 40%          | 33%          | 14%
```

**Analysis:** Activation rate is improving (45% → 55%) and retention is trending up. The changes made in January (new onboarding flow, perhaps) are working.

### Monthly Retention Cohort

```
Cohort  | Mo1 | Mo2 | Mo3 | Mo4 | Mo5 | Mo6
Jan     | 100%| 65% | 55% | 50% | 48% | 45%
Feb     | 100%| 68% | 58% | 52% | 50% | -
Mar     | 100%| 70% | 60% | 55% | -   | -
Apr     | 100%| 72% | 62% | -   | -   | -
```

**Read this:**
- The Jan cohort had 45% retention at month 6
- Retention is improving with each cohort (good)
- The biggest drop is month 1 to month 2 (can you improve first-month engagement?)

### Building Cohort Analysis as a Solo Founder

**Method 1: Spreadsheet (simplest)**
1. Export user signup dates and activity from your database
2. Group by signup week/month
3. Count who is active in each subsequent period
4. Calculate percentages
5. Update weekly

**Method 2: Analytics tool**
- PostHog: Built-in cohort analysis (free tier available)
- Mixpanel: Powerful cohort analysis (paid)
- Amplitude: Best-in-class cohort analysis (paid)
- Baremetrics: Revenue-focused cohort analysis (paid)

## Activation Score

### What Is an Activation Score?

A composite metric that measures how "activated" a user is, based on multiple weighted actions. More nuanced than binary "activated/not activated."

### Building an Activation Score

**Step 1: Identify predictive actions**
List all actions users take in their first 7 days. For each, measure how it correlates with 30-day retention.

**Step 2: Weight each action**
Actions that strongly predict retention get higher weights (1-10). Weak predictors get lower weights.

**Step 3: Score users**
Sum up weighted actions for each user. Normalize to 0-100.

**Step 4: Define thresholds**
- 0-30: Low activation (unlikely to retain)
- 31-60: Moderate activation (may retain with help)
- 61-80: High activation (likely to retain)
- 81-100: Power user (very likely to retain and upgrade)

### Activation Score Example

| Action | Weight | User A | User B |
|--------|--------|--------|--------|
| Created account | 1 (auto) | 1 | 1 |
| Verified email | 2 | 2 | 2 |
| Completed first project | 10 | 10 | 10 |
| Invited team member | 8 | 0 | 8 |
| Connected integration | 5 | 5 | 5 |
| Customized settings | 3 | 3 | 0 |
| Viewed analytics | 7 | 7 | 7 |
| Shared with team | 6 | 0 | 6 |
| **Total Score** | | **28** | **39** |

User A: 28 — Low activation. They tried it but didn't engage deeply.
User B: 39 — Moderate activation. More engaged but not fully activated.

**Action:** Send User A personalized help to complete more actions. User B is on the right track but could use encouragement to do one more thing.

## Friction Metrics

### Time on Task

Measure how long users spend on each onboarding step.

**Tool:** Product analytics (PostHog, Mixpanel) can track time between events.

**What to look for:**
- Step that takes significantly longer than expected
- High variance (some users finish in 10 seconds, others take 10 minutes)
- Increasing time on task over time (product is getting more complex)

**Action:** If Step 3 takes 5+ minutes but should take 1 minute, that step has friction.

### Error Rate

% of users who encounter errors during onboarding.

**Track:**
- Form validation errors
- API failures
- Integration connection failures
- Missing required data

**Benchmark:** Error rate should be under 5% for each onboarding step.

**Action:** If users frequently get errors connecting an integration, the integration either has bugs or unclear setup instructions.

### Rage Clicks

Users clicking the same element multiple times in frustration.

**Tools:** Session recording tools (Hotjar, FullStory, PostHog) can detect rage clicks.

**What to look for:**
- Buttons that don't respond
- Links that don't go where expected
- UI that users assume is clickable but isn't

**Action:** If users rage-click the "Save" button, maybe it's not obvious that saving succeeded. Add a confirmation animation.

### Support Tickets During Onboarding

Track how many support tickets are submitted during the onboarding period.

**What to analyze:**
- Most common onboarding questions
- What steps trigger support requests
- How quickly support resolves onboarding issues

**Action:** If 20% of users submit a ticket about "how to connect my data," improve that step in onboarding.

## Engagement Metrics

### Session Metrics

- **Sessions per week:** How often users return during onboarding
- **Session duration:** How long they spend per visit
- **Actions per session:** How much they accomplish each visit

**Benchmarks (B2B SaaS):**
- 3+ sessions in first week: Good
- 5+ minutes per session: Engaged
- 5+ actions per session: Productive

### Feature Adoption

% of users who use each feature during onboarding.

**Track for each feature:**
- What % of users try it in their first week
- What % of users adopt it long-term
- What's the time-to-first-use for each feature

**Action:** If 90% of users never try the "sharing" feature during onboarding, either:
- They don't know it exists (add a tooltip)
- It's not valuable to them (reconsider the feature)
- It requires too many steps (simplify)

### Power User Score

% of users who exhibit power user behavior during onboarding.

**Power user behaviors:**
- Use keyboard shortcuts
- Create templates
- Use API
- Customize extensively
- Invite many team members

**Significance:** Power users convert at much higher rates. Identify them early and nurture them.

## Conversion Metrics from Onboarding

### Trial-to-Paid by Onboarding Completion

Segment conversion rate by how much of onboarding users completed.

| Onboarding % | Conversion Rate |
|-------------|----------------|
| 0-20% | 1% |
| 21-40% | 3% |
| 41-60% | 8% |
| 61-80% | 15% |
| 81-100% | 25% |

**This data proves:** Completing onboarding is highly predictive of conversion. Invest in getting every user to 80%+ onboarding completion.

### Time to Convert by Onboarding Speed

| Time to Activation | Average Time to Convert | Conversion Rate |
|-------------------|------------------------|-----------------|
| < 1 hour | 5 days | 22% |
| 1-24 hours | 8 days | 14% |
| 1-3 days | 14 days | 8% |
| 3-7 days | 21 days | 4% |
| 7+ days | 35+ days | 2% |

**This data proves:** Faster activation leads to faster conversion at higher rates. Every hour of delay costs you customers.

## Satisfaction Metrics

### Onboarding NPS

Send a single question after onboarding completion:

"How likely are you to recommend [Product] to a friend based on your onboarding experience?"

- 9-10: Promoters (onboarding was excellent)
- 7-8: Passives (onboarding was adequate)
- 0-6: Detractors (onboarding needs work)

**Calculation:** % Promoters - % Detractors = NPS

**Benchmark:** Onboarding NPS of 30+ is good. 50+ is excellent.

### Onboarding CSAT

Send after each major onboarding step:

"How easy was it to [complete this step]?"

- Very difficult (1) → Very easy (5)

**Benchmark:** Average score of 4+ out of 5 is good.

## Building Your Onboarding Dashboard

### Essential Metrics to Display

**Leading indicators (daily/weekly):**
- New signups
- Activation rate
- Onboarding completion rate
- Time to first value (median)
- Drop-off at each onboarding step
- Active trial users

**Lagging indicators (monthly):**
- Trial-to-paid conversion rate
- Onboarding NPS
- 30-day retention by onboarding cohort
- Support tickets during onboarding

### Dashboard Tools

- **Simple:** Google Sheets (update manually each week)
- **Better:** Metabase or Superset (free, connect to your database)
- **Good:** PostHog (usage analytics + dashboards)
- **Best:** Mixpanel/Amplitude (product analytics with built-in dashboards)

### Weekly Onboarding Review (30 min)

**Monday morning routine:**
1. Open onboarding dashboard (5 min)
2. Review activation rate vs target (2 min)
3. Check onboarding funnel for new drop-offs (5 min)
4. Read 5 most recent onboarding survey responses (5 min)
5. Review support tickets from new users (5 min)
6. Identify top 1 thing to improve this week (3 min)
7. Update improvement tracker (5 min)

### Monthly Onboarding Review (2 hours)

1. Deep dive on activation rate trends (30 min)
2. Cohort analysis review (30 min)
3. User interview findings from past month (20 min)
4. Competitive onboarding analysis (20 min)
5. Prioritize improvements for next month (20 min)

## Using Metrics to Drive Improvements

### The Improvement Cycle

1. **Identify opportunity:** Metric is below target or declining
   - Example: Activation rate dropped from 50% to 40%

2. **Investigate root cause:** Analyze funnel, watch recordings, read feedback
   - Example: Drop-off at Step 2 increased from 15% to 40%

3. **Form hypothesis:** "If we [change], then [metric] will improve because [reason]."
   - Example: "If we simplify Step 2 to require one click instead of three, activation rate will improve because users won't get confused."

4. **Implement change:** Ship the improvement
   - Example: Combined three Step 2 screens into one

5. **Measure impact:** Track metric for 2-4 weeks after change
   - Example: Activation rate recovered to 48% — close to original, improvement validated

6. **Standardize or revert:** If it worked, keep it. If not, try something else.

### Prioritizing Improvements

Use the RICE framework for solo founders:

**Reach:** How many users will this affect?
**Impact:** How much will this improve the metric?
**Confidence:** How sure are you it will work?
**Effort:** How much time will it take?

Score each 1-10, then calculate: (Reach × Impact × Confidence) / Effort

Highest score = highest priority.

### Common Onboarding Metric Problems and Fixes

**Problem: Low activation rate (< 20%)**
- Users don't understand the product's value
- Too many steps to reach value
- Product doesn't solve a real problem

- Fixes: Reduce friction, improve messaging, add sample data, simplify first workflow

**Problem: High drop-off at specific step (> 40%)**
- Step is confusing, slow, or technically broken
- Users don't see why this step matters

- Fixes: Add tooltip/guidance, combine with another step, make optional, fix bugs

**Problem: Long TTFV (> 24 hours)**
- Users sign up but don't return to complete setup
- Setup requires too many separate sessions

- Fixes: Single-session activation design, email reminders, offer personal help

**Problem: Low onboarding completion rate (< 30%)**
- Onboarding checklist is too long or tedious
- Steps aren't clearly connected to value

- Fixes: Reduce checklist length, highlight value of each step, auto-complete steps

**Problem: Onboarding generates high support volume**
- Product is confusing
- Documentation is insufficient

- Fixes: Fix product UX, improve documentation, add in-app guidance

## Advanced Metrics

### The Activation Efficiency Ratio

```
AER = Activation Rate / Median TTFV (hours)
```

A high AER means users activate quickly and consistently. Use this to compare onboarding quality across segments.

**Example:**
- Segment A: 50% activation, 2 hours TTFV → AER = 25
- Segment B: 40% activation, 5 hours TTFV → AER = 8

Segment B's onboarding is less efficient. Invest improvement effort there.

### Onboarding Contribution to LTV

```
LTV of activated users vs LTV of non-activated users
```

If activated users have 5x higher LTV, improving activation by 10% points has massive revenue impact.

**Revenue impact calculation:**
- Current: 1,000 signups/month × 40% activation × 10% trial conversion × $100/mo × 12 months = $48,000 LTV/cohort
- Improved: 1,000 × 50% activation × 10% conversion × $100 × 12 = $60,000 LTV/cohort
- Improvement value: $12,000/cohort

### Onboarding Health Score

A composite score combining multiple metrics into a single number.

**Components (weighted):**
- Activation rate (30%)
- TTFV score (25%) — normalized (lower = better)
- Onboarding completion rate (20%)
- Onboarding satisfaction (15%)
- Error rate during onboarding (10% — inverted)

**Scale:** 0-100. Green (80+), Yellow (50-79), Red (< 50)

**Use for:** At-a-glance onboarding health. Track weekly.

## Avoiding Metric Traps

### Vanity Metrics

**Don't track** (or at least, don't prioritize):
- Total signups (absolute number, not ratio)
- Total active users (without segmenting by cohort)
- Email open rates without connection to activation

**Do track:**
- Activation rate (ratio)
- Activated user retention (cohort-based)
- Onboarding funnel conversion rates

### Metric Myopia

Don't optimize one metric at the expense of others.

**Example:** You optimize for "time to first value" by making signup simpler (no email verification). Activation speed improves, but you get more spam signups and lower quality users.

**Balance:** Track multiple metrics together. If one improves but others decline, the "improvement" may be harmful.

### Not Segmenting

Aggregated metrics hide problems. Always segment.

**Bad:** "Activation rate is 45%"
**Good:** "Activation rate is 55% for organic users, 30% for paid users"

Segment reveals where to invest.

## Conclusion

Onboarding metrics are your compass. They tell you whether your product experience is working, where users struggle, and where to invest your limited time.

Start simple: track activation rate and TTFV. Add more metrics as you grow. The key is not to measure everything — it's to measure the right things and act on them.

Weekly review of your onboarding metrics will consistently surface improvement opportunities. Invest 30 minutes per week in your onboarding dashboard. It will pay back in higher activation, faster conversion, and more customers.
