# Fake Door Testing: Validate Demand Before Building Features

## What is Fake Door Testing?

Fake door testing (also called "button testing" or "vapor testing") is a validation technique where you place a button, link, or feature in your product or landing page that LOOKS like it leads to a real feature — but instead leads to a "coming soon" message, a waitlist, or a feedback form.

The goal is to measure how many people click the button. Clicks = demand. No clicks = no demand.

**Why fake door testing works:**
- Measures action (not opinion)
- Gives quantitative data on demand
- Costs nothing to implement
- Takes days, not weeks
- Can test multiple features simultaneously
- Prevents building features nobody wants

## The Psychology Behind Fake Door Tests

People lie in surveys and interviews. They say "yes, I'd use that" to be polite or because they imagine they would. But when faced with an actual decision (click or don't click), their real preferences emerge.

Fake door testing captures revealed preference — what people ACTUALLY do, not what they SAY they'd do.

### The Survey vs. Fake Door Gap

| Method | "Would you use X?" | Click Rate on Fake Door |
|--------|-------------------|------------------------|
| Typical result | 40-60% say "yes" | 2-10% actually click |
| Gap | | 4-20x difference |

People overestimate their interest by 4-20x when asked hypothetically.

## Types of Fake Door Tests

### Type 1: The Pricing Page Test

Add a pricing tier that doesn't exist yet. Measure how many people try to click "Buy" or "Choose Plan."

**Example:**
```
Your current plans:
- Starter: $29/mo
- Professional: $79/mo

Fake plan:
- Enterprise: $249/mo [Coming Soon]

When someone clicks "Enterprise": "This plan is coming soon.
Join the waitlist to be notified."
```

**What you learn:** Is there demand for a higher tier? At what price?

### Type 2: The Feature Button Test

Add a button for a feature that doesn't exist. Measure clicks.

**Example:**
```
Your dashboard has: 
- [Export to CSV] ✓
- [Schedule Report] ✓
- [Generate PDF] ✓
- [AI Insights] → [Coming Soon button]

When someone clicks "AI Insights": "AI-powered insights are
coming soon. Would you like to be notified when they launch?"
```

**What you learn:** Which features to build next (prioritization by demand).

### Type 3: The Integration Test

List integrations on your website. Some exist, some are fake.

**Example:**
```
Integrations page:
- Slack ✓
- Salesforce ✓
- HubSpot ✓
- Mailchimp ✓
- Zendesk → [Click to "learn more" → Coming Soon]
- Jira → [Click to "learn more" → Coming Soon]

Track which fake integrations get the most clicks.
```

**What you learn:** Which integrations to build first.

### Type 4: The Workflow Test

Place a button in the user's workflow that leads to a non-existent feature.

**Example:**
```
In your analytics dashboard:
- [View Dashboard] ✓
- [Compare Periods] ✓
- [Export Report] ✓
- [Schedule Automated Report] → [Coming Soon]
- [Set Alert] → [Coming Soon]

If 40% of users click "Schedule Automated Report" but 0% click "Set Alert,"
you know which to build.
```

**What you learn:** Which workflow improvements to prioritize.

### Type 5: The Landing Page Feature List

On your landing page, list features — some built, some not. Track which features drive the most interest.

**Example:**
```
Headline: "The All-in-One Marketing Platform"

Features list:
- Email campaigns ✓
- Landing pages ✓
- Social media scheduling ✓
- A/B testing → [Learn More] → Coming Soon
- CRM integration → [Learn More] → Coming Soon

Use UTM parameters or click tracking to measure interest.
```

**What you learn:** Which features attract customers.

## When to Use Fake Door Testing

### Perfect Timing
- You have an existing product with traffic
- You're deciding between multiple features to build
- You're considering a new pricing tier
- You want to validate demand before a big build
- You need data to prioritize your roadmap

### OK Timing
- You have a landing page with traffic
- You're in beta with active users
- You have a mailing list you can survey (but fake door still better than survey)

### Bad Timing
- You have no traffic or users yet (no one to click)
- You need to validate the core product (use concierge MVP instead)
- You have < 100 visitors/month (not enough data)
- You're B2B with 1-2 potential customers (qualitative > quantitative)

## How to Run a Fake Door Test

### Step 1: Identify What to Test

Generate a list of potential features or pricing tiers you're considering:

```
Feature Candidates:
1. PDF export
2. CSV import
3. Automated email reports
4. Slack integration
5. API access
6. Custom branding
7. Team accounts
8. Audit logs
9. Two-factor authentication
10. White-labeling

Select 2-5 to test simultaneously.
```

### Step 2: Design the Button

**Best practices for fake door buttons:**

```
Do:
- Make it look real (same style, color, placement as real buttons)
- Use standard CTA language ("Get Started," "Enable," "Upgrade")
- Place it logically in the user journey
- Track clicks with analytics

Don't:
- Make it flashy or attention-grabbing (unfair advantage)
- Hide it or make it hard to find (unfair disadvantage)
- Use misleading language that tricks people into clicking
- Test something you're not seriously considering building
```

### Step 3: Build the Landing Page

When someone clicks, they should see:

```
Option A: Coming Soon Page
"Coming Soon! [Feature Name]
Join the waitlist to be first to know when it launches.
[Email Input → Submit]

Benefits of this feature:
- Benefit 1
- Benefit 2
- Benefit 3
```

```
Option B: Interest Survey
"[Feature Name] is under development.
Help us prioritize by telling us about your needs:

1. Would you use this feature? [Yes/No/Maybe]
2. How important is this to you? [1-5]
3. What problem would this solve? [Free text]

[Submit]
```

```
Option C: Pre-Signup
"[Feature Name] — Coming Q3 2025
Get early access: [Email Input]
Or: Pre-order now for 30% off founding member pricing [$Button]
```

### Step 4: Drive Users to the Test

**For existing products:**
- Add the button in-app for all users
- Segment users (50% see the button, 50% don't — control group)
- Track click-through rate for 1-4 weeks

**For landing pages:**
- Add the feature to your feature list
- Run A/B test (with/without the feature)
- Track: clicks, time on page, email signups

**For pricing pages:**
- Add the new pricing tier
- Track: clicks on the tier, comparison page visits

### Step 5: Measure Results

**Primary metric:** Click-through rate (CTR)

| CTR | Interpretation |
|-----|---------------|
| > 10% | Very high demand — build immediately |
| 5-10% | Strong demand — build soon |
| 2-5% | Moderate demand — consider building |
| 1-2% | Low demand — probably not worth it |
| < 1% | No demand — don't build |

**Secondary metrics:**
- Email signups on coming soon page
- Survey responses
- Time spent on coming soon page
- Bounce rate from coming soon page
- Follow-up survey responses

**Qualitative data:**
- What do people write in the survey?
- What do they say in the coming soon comments?
- Do they contact support asking about the feature?

### Step 6: Make the Decision

| Result | Decision |
|--------|----------|
| CTR > 5% AND high email signups | Build immediately |
| CTR > 5% AND low email signups | Build but reconsider positioning |
| CTR 2-5% AND existing users requesting it | Build on roadmap |
| CTR 2-5% AND no one asked for it | Low priority, maybe A/B test |
| CTR < 2% | Don't build |
| High demand + many survey responses | Build and incorporate feedback |

## Fake Door Testing with Paywalls

### Advanced: Fake Pricing with Real Checkout

For stronger validation, add a fake feature behind a paywall:

```
Button: "[Get AI Insights — $49/mo add-on]"
When clicked: "This add-on is coming soon. Enter your email
and we'll notify you when it's available."
```

**Even stronger:** Fake checkout process
```
Button: "[Upgrade to Pro — $99/mo]"
→ "Review your order: Pro Plan $99/mo, [Feature list including fake features]"
→ [Confirm Payment]
→ "This plan is launching soon. Join the waitlist to be first."
```

**Strongest:** Fake payment attempt
```
Button: "[Upgrade to Enterprise — $249/mo]"
→ Enter credit card details
→ [Complete Purchase]
→ "Enterprise is coming soon. You won't be charged.
   Join the waitlist to get early access."

You learn: Would people actually ENTER their credit card?
If 10% enter card details for a fake feature, you have REAL demand.
```

## Fake Door Testing for Pricing

### Testing Price Points

Create multiple fake pricing pages and A/B test them:

```
Version A: Starter $19, Pro $49, Enterprise $99
Version B: Starter $29, Pro $79, Enterprise $149  
Version C: Starter $9, Pro $29, Enterprise $79

Track: Which version gets the most clicks on "Choose Plan"?
Which gets the most total value (clicks × price)?
```

### Testing Pricing Models

```
Version A: $29/month (monthly only)
Version B: $29/month or $290/year (20% discount)
Version C: Free tier, $29/month Pro, $99/month Business

Track:
- Click distribution across tiers
- Which version converts best?
- What price anchors drive the most value?
```

### Testing Add-On Pricing

```
Base product: $79/month
Add-ons (fake):
- API access: +$29/month [Learn More]
- White-label: +$99/month [Learn More]
- Dedicated support: +$199/month [Learn More]

Track: Which add-ons get the most interest? At what price?
```

## Fake Door Testing in the Wild

### Real-World Examples

**Example 1: Buffer's Fake Pricing Page**
Buffer tested pricing before building the product. Their landing page had a "Pricing" link that led to a page showing planned pricing tiers. The signup rate from this page validated willingness to pay.

**Result:** Built Buffer, now a $20M+ ARR company.

**Example 2: Groove's Feature Validation**
Groove (helpdesk software) used fake door tests for features:
- Added buttons for features they were considering
- Tracked click rates over 30 days
- Only built features with > 5% click rate
- Reduced feature development by 40%

**Result:** Built only features customers actually wanted.

**Example 3: Stripe's Early Pricing**
Stripe's original page had pricing listed. They didn't have a product ready. People clicked "Sign Up" based on pricing alone. The number of signups validated pricing and demand.

**Result:** Proceeded with building, knowing demand existed at their price point.

**Example 4: Basecamp's Feature Requests**
Basecamp lists features on their pricing page with "Available in" labels. Some features show "Coming to [Plan]" before they're built. Click-through rates determine which features they build next.

**Result:** Data-driven roadmap, no wasted features.

## Fake Door Testing Tools

### Tracking Tools
- **Google Analytics** (free) — Event tracking for button clicks
- **Mixpanel** (free tier) — Product analytics with event tracking
- **Amplitude** (free tier) — Advanced product analytics
- **Hotjar** (free tier) — Heatmaps + click tracking
- **FullStory** (free tier) — Session recording + click tracking
- **PostHog** (free, self-host) — Product analytics suite

### A/B Testing Tools
- **Google Optimize** (free) — A/B test landing pages
- **VWO** ($99/month) — A/B testing + heatmaps
- **Optimizely** (custom pricing) — Enterprise A/B testing
- **Convert** ($99/month) — A/B testing for SaaS
- **GrowthBook** (free, open source) — Feature flag + A/B testing

### Coming Soon Page Builders
- **Carrd** ($19/year) — Simple coming soon pages
- **Webflow** ($14/month) — More complex coming soon pages
- **Unicorn Platform** ($9/month) — SaaS-specific pages
- **Notion** (free) — Quick coming soon with Notion sites
- **Tally** (free) — Form builder for coming soon surveys

## Fake Door Testing for Pre-Launch

Before you have a product, use fake door testing on your landing page:

**Method: The Fake Feature Tour**

```
Create a landing page that describes features:
- Feature 1: [description] ✓ (available at launch)
- Feature 2: [description] ✓ (available at launch)
- Feature 3: [description] → [Click for details]
- Feature 4: [description] → [Click for details]

Track: Which "Learn More" clicks for unreleased features get the most traction?

Add email collection:
"Leave your email to be notified when [Feature 3] launches"
Track: How many people sign up specifically for each feature?
```

**Method: The Two-Button Test**

```
CTA on landing page:
- Button 1: "Start Free Trial" (real CTA)
- Button 2: "See Enterprise Features" (fake door)

If 40% click Enterprise, build enterprise tier faster.
If 5% click Enterprise, focus on core product.

Track: Click distribution between real and fake CTAs.
```

## Interpreting Fake Door Results

### Common Patterns

**Pattern 1: High Clicks, Low Conversions**
Everyone clicks but nobody signs up.

**Possible explanations:**
- Curiosity clicks (they wanted to see what it was)
- The coming soon page doesn't sell well enough
- The feature is interesting but not valuable enough to give email

**Action:** Improve the coming soon page value prop. Or accept that interest is moderate.

**Pattern 2: Steady Clicks Over Time**
Clicks are consistent week over week.

**Interpretation:** Real, sustained demand exists.

**Action:** Build the feature.

**Pattern 3: Spike Then Drop**
First week has high clicks, then drops to near zero.

**Interpretation:** Novelty effect. People clicked because it was new. Sustained demand is low.

**Action:** Don't build, or test with a different approach.

**Pattern 4: Segment Difference**
Power users click at 15% rate, new users at 2%.

**Interpretation:** Feature is for advanced users only. Consider a higher-tier offering.

**Action:** Build for the appropriate segment. Price accordingly.

**Pattern 5: No Clicks**
Nobody clicks.

**Interpretation:** Either:
- Nobody sees the button (placement/design issue)
- Nobody wants the feature (demand doesn't exist)
- Everyone already has what they need

**Action:** Move button to more prominent position. If still no clicks, don't build.

### False Positives and Negatives

**False Positive (high clicks but no actual demand):**
- Curiosity: "What's this new thing?"
- Misleading button text: Users expected something else
- No pain: They clicked but wouldn't pay

**Prevention:**
- Use neutral button text (not exciting, not boring)
- Add a follow-up: "Would you pay $X/month for this?"
- Require email to see more (reduces curiosity clicks)

**False Negative (low clicks but real demand):**
- Button in wrong place (users didn't see it)
- Wrong label (users didn't understand what it does)
- Timing (users don't need it NOW but will later)

**Prevention:**
- Test button placement (top nav, sidebar, dashboard)
- A/B test button labels
- Run the test for 4+ weeks to catch timing issues

## Ethical Considerations

Fake door testing is a legitimate research method, but it can feel deceptive. Follow these guidelines:

### Do
- Be transparent when people engage: "This feature is planned but not yet available"
- Use "Coming Soon" language
- Collect feedback honestly
- Actually build features that receive strong validation
- Respect user privacy (don't track more than necessary)
- Limit test duration (2-4 weeks maximum)

### Don't
- Mislead users into thinking a feature exists when it doesn't (wastes their time)
- Collect payment information under false pretenses
- Run tests indefinitely without building
- Test critical workflow features (login, data export)
- Deceive users in ways that damage trust

### The Golden Rule
Would you be okay with a user discovering this was a test? If not, redesign the test.

## The Fake Door Testing Playbook

### 30-Day Fake Door Sprint

```
Day 1-2: Identify 3-5 features/pricing changes to test
Day 3-5: Design buttons and coming soon pages
Day 6-7: Implement tracking (Google Analytics events)
Day 8: Launch test (add buttons to product/landing page)
Day 8-28: Collect data (3 weeks minimum)
Day 15: Mid-test review — adjust anything clearly broken
Day 22: Analyze initial data — look for clear signals
Day 29-30: Final analysis and decisions

Results:
- Build: Features with >5% CTR
- Roadmap: Features with 2-5% CTR
- Deprioritize: Features with <2% CTR
- Re-test: Features with unclear results
```

### What NOT to Fake Door Test

- **Core value proposition:** Test this with concierge MVP or pre-sells
- **Login/signup flows:** These must work (critical path)
- **Data export:** Users will be furious if they can't export when they need to
- **Billing/invoicing:** Must work correctly
- **Account settings:** Password changes, email preferences
- **Compliance features:** GDPR data access, account deletion
- **Trial expiration:** Must work as expected

### What TO Fake Door Test

- **Add-on features:** Extra functionality beyond core
- **Premium features:** What to put in higher tiers
- **Integrations:** Which third-party tools to support
- **New pricing tiers:** Demand for higher/lower price points
- **Export formats:** Which formats users actually need
- **Dashboard widgets:** What data users care about
- **Notification types:** What users want to be alerted about
- **API endpoints:** What developers want to integrate with

## The Solo Founder's Fake Door Cheat Sheet

### When You Have 30 Minutes
```
1. Pick 1 feature you're considering
2. Add a button with the feature name to your admin/nav
3. Set up a simple Google Analytics event on clicks
4. Add a coming soon message: "We're working on this!"
5. Collect clicks for 2 weeks
6. If > 20 clicks from 500 visitors = moderate interest
7. If > 50 clicks = real demand
```

### When You Have 2 Hours
```
1. Pick 3 features to test
2. Design coming soon pages for each
3. Add buttons to relevant locations in product
4. Set up tracking for each button
5. Add email capture on coming soon pages
6. Run for 3 weeks
7. Analyze: Which features got the most clicks AND signups?
8. Build the winner
```

### When You Have 8 Hours
```
1. Build a full fake door test framework
2. Test pricing tiers + features + integrations simultaneously
3. Segment by user type (new vs power user, plan level)
4. Run A/B tests on button placement and copy
5. Collect qualitative feedback (what do users say?)
6. Run for 4 weeks
7. Build a prioritized roadmap based on data
8. Remove fake doors when tests conclude
```

## Final Thoughts

Fake door testing is one of the most cost-effective validation tools available to solo founders. It costs nothing but a few hours of implementation time and gives you quantitative demand data.

But remember: fake door tests measure INTEREST, not PURCHASE INTENT. Someone clicking "AI Insights" is interested. Someone putting their credit card in for "AI Insights" is committed. Use fake doors for prioritization, but use pre-sells for final validation.

**Build the buttons, measure the clicks, build what people actually want.**
