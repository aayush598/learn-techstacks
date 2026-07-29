# MVP to V1 Roadmap

## The Post-MVP Landscape

You shipped your MVP. You have a handful of paying customers. Congratulations — this is where most solo founders fail. They either stop building (coasting on the MVP) or they build the wrong things (adding features nobody asked for).

This guide covers how to move from MVP to a proper V1 product, using customer feedback to drive your roadmap while maintaining the speed that got you here.

## The MVP-to-V1 Mindset Shift

### The Four Phases of Product Maturity

```
Phase 0 — Pre-MVP:
  Goal: Get first paying customer
  Timeline: 2-4 weeks
  Risk: Never shipping

Phase 1 — MVP (YOU ARE HERE):
  Goal: Validate demand, learn from real users
  Timeline: 1-3 months
  Risk: Building too much, not listening

Phase 2 — V1:
  Goal: Product-market fit in a specific niche
  Timeline: 3-9 months
  Risk: Feature creep, losing focus

Phase 3 — Growth:
  Goal: Scale customer acquisition
  Timeline: 9-24 months
  Risk: Scaling before product-market fit

Phase 4 — Maturity:
  Goal: Defensible market position
  Timeline: 24+ months
  Risk: Competition, stagnation
```

### What Changes from MVP to V1

| Aspect | MVP | V1 |
|---|---|---|
| Goal | Validate demand | Achieve product-market fit |
| Customers | 1-10 | 10-100 |
| Features | The absolute minimum | Complete core workflow |
| UX | Functional but ugly | Polished and intuitive |
| Reliability | "Works on my machine" | Production-grade |
| Support | Invasive, personal | Scalable systems |
| Code quality | Ship at all costs | Maintainable |
| Testing | None | Critical paths covered |
| Architecture | Minimalist | Future-proofed |

## Customer-Driven Prioritization

### The Feedback Collection System

You need a systematic way to collect, categorize, and prioritize customer feedback. A spreadsheet will not cut it once you have 10+ customers.

### Set Up a Feedback Pipeline

```
Channel 1: In-app feedback widget
  └─> Simple form: "What's one thing we could improve?"
  └─> Store in database with user context

Channel 2: Support emails
  └─> Tag every support request by category
  └─> Track: bug, feature request, confusion, compliment

Channel 3: User interviews
  └─> Weekly calls with customers
  └─> Ask: "What almost made you not sign up?"
  └─> Ask: "What's the one thing you wish this did?"

Channel 4: Usage analytics
  └─> Track feature adoption
  └─> Track drop-off points
  └─> Watch session recordings (e.g., Hotjar free tier)
```

### The Feedback Categorization Matrix

```
                    | High Frequency (many users ask) | Low Frequency (few users ask)
                    |                                |
Urgent (blocking)   | BUILD IMMEDIATELY              | Check if real pain
                    | This is your next feature       | or just one user's issue
                    |                                |
Nice-to-have        | Strong V1 candidate             | V2 or later
                    | High value, validate first      | Probably ignore
                    |                                |
```

### The "One User" Trap

One user begging for a feature does not mean you should build it. Especially if they ask nicely. Or offer to pay more. Or threaten to leave.

**How to handle feature requests from a single user:**

```
User: "If you add X, I'll pay double!"
You: "That's great to hear. I'll consider it for the roadmap."
     [Don't build it yet — wait for 3+ users to ask]

User: "I'm going to cancel unless you add Y."
You: "I understand. Let me check if this is something other users need."
     [If one user cancels, that's 1 lost customer. If you build the wrong
      feature, you lose focus and potentially all customers.]

User: "Everyone needs Z!"
You: "Can you introduce me to 3 other people who need Z?"
     [If they can't, it's probably just them.]
```

### Running User Interviews

Schedule 30-minute calls with customers weekly. Template:

```markdown
**User Interview Template (Weekly)**

Questions to ask:
1. What did you accomplish with [Product] this week?
2. What was the most frustrating thing that happened?
3. What feature would you pay double for?
4. What feature would you be sad to lose?
5. If you could change one thing, what would it be?
6. Have you recommended [Product] to anyone? Why/why not?
7. What almost stopped you from signing up?

Questions to answer (for yourself, after call):
1. Did they struggle with anything I thought was easy?
2. Did they find value in something I considered minor?
3. What do I need to build/change this week?
4. What assumption was I wrong about?
```

### The Data-Driven Priority Score

Combine quantitative and qualitative data to score every potential feature:

```markdown
**Feature Priority Score Formula:**

Request Count (R): Number of unique customers who asked
Impact Score (I): 1-10 estimate of value delivered per customer
Urgency (U): 1-10 how much this blocks current usage
Confidence (C): 1-10 how sure you are it's the right solution
Effort (E): 1-10 (1 = easy, 10 = very hard)

Priority Score = (R × I × U × C) / E
```

**Example:**

| Feature | R | I | U | C | E | Score |
|---|---|---|---|---|---|---|
| CSV Export | 8 | 7 | 5 | 9 | 2 | 1260 |
| Team Accounts | 3 | 9 | 3 | 4 | 8 | 40.5 |
| Dark Mode | 4 | 2 | 1 | 8 | 3 | 21.3 |
| Calendar View | 2 | 6 | 4 | 5 | 7 | 34.2 |

CSV Export wins. Build that first.

## Post-MVP Roadmap Structure

### The 90-Day Horizon

Don't plan beyond 90 days. The further out you plan, the more wrong you'll be. Plan in three 30-day cycles:

```markdown
Cycle 1 (Month 1): "The Fixes"
  - Fix all critical bugs from MVP
  - Address top 3 friction points from user feedback
  - Improve onboarding to reduce drop-off
  - Goal: Retention (users who stay)

Cycle 2 (Month 2): "The Core"
  - Add the single most-requested feature
  - Complete the core workflow (fill MVP gaps)
  - Improve performance and reliability
  - Goal: Engagement (users who use daily)

Cycle 3 (Month 3): "The Growth"
  - Add features that enable word-of-mouth
  - Build sharing/referral capabilities
  - Polish for public launch
  - Goal: Acquisition (users who invite others)
```

### The V1 Definition Checklist

Your V1 is complete when:

```
[ ] Core workflow has no gaps — user can complete tasks end-to-end
[ ] Onboarding takes < 2 minutes to reach "aha moment"
[ ] Error states don't break the experience
[ ] Loading times are acceptable (< 2s for main actions)
[ ] Mobile-responsive layout works
[ ] Basic email notifications work for key events
[ ] Payment flows handle edge cases (trial end, card decline, etc.)
[ ] Data export is available (minimum CSV)
[ ] Help/documentation covers 80% of use cases
[ ] Admin tools let you manage customers without touching the DB
[ ] Monitoring alerts you to critical issues
[ ] Backups are automated and tested
```

### The V1 Feature Roadmap Template

```markdown
# V1 Roadmap: [Product Name]

## Current Status (MVP)
- [Number] paying customers
- [Number] monthly active users
- [Core metric] baseline

## Month 1: Foundation (Due: [Date])

### Critical Fixes
- [Bug] [Description] — [Priority: High/Med/Low]
- [Bug] [Description]
- [Bug] [Description]

### UX Improvements
- [Improvement based on feedback]
- [Improvement based on analytics]
- [Improvement based on interview]

### Onboarding
- [ ] Reduce time-to-value from [X] to [Y]
- [ ] Add [missing step] to onboarding flow
- [ ] Create help documentation for core features

## Month 2: Core Features (Due: [Date])

### Major Feature: [Feature Name]
- [Sub-feature]
- [Sub-feature]
- [Sub-feature]

### Integration: [Integration]
- [Integration details]

### Performance
- [ ] Page load target: < [X] seconds
- [ ] API response target: < [X] ms
- [ ] Reduce database queries per page

### Reliability
- [ ] Add error monitoring
- [ ] Improve error handling
- [ ] Add database read replicas if needed

## Month 3: Growth (Due: [Date])

### Virality Features
- [ ] Share/export functionality
- [ ] Referral tracking
- [ ] Team/collaboration features

### Public Launch Prep
- [ ] Landing page redesign
- [ ] Case studies from early customers
- [ ] Pricing page polish
- [ ] SEO optimization
- [ ] Launch to Product Hunt/other platforms

### Scalability
- [ ] Performance optimization
- [ ] Load testing
- [ ] Infrastructure hardening

## Explicit Deferrals (Not in V1)
- [Feature 1] — Planned for V2
- [Feature 2] — Planned for V2
- [Feature 3] — No demand yet
```

## Making Trade-Offs as a Solo Founder

### The Trilemma

As a solo founder, you can only pursue two of three:

```
              Quality
                │
                │
    Speed ──────┼────── Features
```

**MVP Phase:** Speed + Features (low quality)
**V1 Phase:** Speed + Quality (fewer features)
**V2 Phase:** Quality + Features (slower release)

### When to Say No

You'll need to say no to customers constantly. Here's how:

```
Customer: "Can you add [feature]?"
You: "I love that idea. I've added it to the roadmap.
     Right now I'm focused on [current priority].
     Can I circle back to you when I'm ready to build it?"

Customer: "When will [feature] be ready?"
You: "I don't have a specific date yet. I want to make sure
     I build it right. In the meantime, is there a workaround
     that would help you?"

Customer: "I need [feature] to continue using this."
You: "I understand this is important to you. Let me share
     what I'm working on and why: [explain reasoning].
     If [feature] is a dealbreaker, I understand completely."
```

### The "Buy vs Build" Decision for V1

For every feature, decide: should you build it, buy it, or do it manually?

```
                        | Build | Buy | Manual |
Continuous integration  |   3   |  2  |   1    |
Email automation        |   1   |  3  |   2    |
Analytics               |   1   |  3  |   1    |
User onboarding         |   3   |  2  |   1    |
Customer support portal |   1   |  3  |   2    |
File storage            |   1   |  3  |   1    |
Scheduling              |   1   |  3  |   2    |

3 = Best approach
```

**Guidelines:**
- **Buy if:** It's not your core differentiator, and there's a good option available
- **Build if:** It IS your core differentiator, or no good option exists
- **Manual if:** It's infrequent and doesn't need to scale yet

## Version Planning Strategy

### Semantic Versioning for SaaS

Unlike packaged software, SaaS versions are more about milestones than releases. Still, use semantic versioning for your API:

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (API changes, database migrations that aren't backward-compatible)
MINOR: New features (non-breaking additions)
PATCH: Bug fixes and small improvements

For SaaS:
0.1.x: MVP
0.2.x: First post-MVP iteration
0.9.x: Approaching V1
1.0.0: V1 launch
1.1.0: V1.1 features
2.0.0: Major redesign
```

### The V1.1, V1.2 Pattern

Don't jump to V2 immediately. Plan iterative minor versions:

```markdown
V1.0 — Core V1
  - Complete core workflow
  - Polish, reliability, monitoring
  - Official launch

V1.1 — The Integration Update
  - Top 3 requested integrations
  - API improvements
  - Webhook support

V1.2 — The Team Update
  - Multi-user support
  - Basic permissions
  - Team management

V1.3 — The Enterprise Update
  - SSO
  - Audit logs
  - Role-based access control
  - Custom branding

V2.0 — The Platform Redesign
  - Major architecture changes
  - New core features
  - Possibly split into microservices
```

### When to Cut a Version Loose

Don't plan versions in stone. Use "themes" and adjust based on feedback:

```
Current theme: "Making existing users happier"
Next theme: "Enabling users to invite their team"
Future theme: "Opening the platform to developers"
```

When you have enough features in a theme, call it a version and ship it.

## Customer Feedback in Action: Case Studies

### Case Study 1: The Feature That Almost Wasn't Built

**Context:** A scheduling SaaS. MVP launched with basic calendar management.

**Feedback pattern:** 5 of 10 users mentioned "I want to send reminders."

**Initial reaction:** "That's not the core feature. I'll add it later."

**Deeper investigation:** Users were manually copy-pasting appointments into their calendar. The reminders would save 10 minutes per day.

**Build decision:** Moved to top of V1 roadmap.

**Result:** 30% increase in daily active usage, 2 user referrals from the feature.

**Lesson:** Features that seem "adjacent" may be essential to the workflow.

### Case Study 2: The Feature That Was Demanded but Not Used

**Context:** A data analytics SaaS. Users kept asking for "real-time dashboards."

**Feedback:** 8 of 15 users listed real-time as a top request.

**Build decision:** 4 weeks to build real-time updates with WebSockets.

**Result:** < 5% of users actually used the real-time feature. Most checked dashboards 1-2 times per day.

**Lesson:** What customers SAY they want and what they USE are different. Validate with a "Coming Soon" page and click tracking before building.

### Case Study 3: The Pivot That Saved the Product

**Context:** A document generation SaaS. MVP was built for HR teams to create offer letters.

**Feedback:** Users loved the tool but kept asking: "Can I use this for sales proposals?"

**Reaction:** At first, said no — "We're an HR tool."

**Data:** 40% of signups were from sales teams using the tool for completely different documents.

**Decision:** Pivoted to "general document automation" rather than HR-specific.

**Result:** Sales teams were willing to pay 3x more than HR teams. Revenue doubled.

**Lesson:** Follow the demand, not your original vision.

## Measurement: How to Know You're Ready for V1

### The V1 Readiness Score

Rate yourself 1-10 on each dimension. V1 is ready when you score 7+ on all.

```markdown
1. Core workflow completion
   [1] MVP barely works
   [5] Most paths work, some dead ends
   [10] All common paths work, edge cases handled

2. User satisfaction
   [1] Users complaining
   [5] Users tolerate it
   [10] Users would be upset if it disappeared

3. Retention
   [1] Users don't come back
   [5] Weekly active usage
   [10] Daily active usage

4. Performance
   [1] Slow and unreliable
   [5] Acceptable for most users
   [10] Fast and consistent

5. Support
   [1] Every interaction requires founder
   [5] Some self-service works
   [10] Most issues resolved without founder

6. Revenue
   [1] $0 or unsustainable
   [5] Consistent MRR growth
   [10] Predictable, growing MRR
```

### Key Metric Targets for V1

```markdown
**Before declaring V1, aim for:**
- Monthly churn < 5% (ideally < 3%)
- Net Promoter Score > 30
- DAU/MAU ratio > 20% (daily active / monthly active)
- Time-to-value < 5 minutes
- Support tickets per user per month < 1
- Core feature adoption > 60% (users use the main feature)
- MRR growth rate > 10% month-over-month
- At least 10 customers who say they'd "be very disappointed" without your product
```

## From V1 to Product-Market Fit

### The Product-Market Fit Signal

You know you're approaching product-market fit when:

```markdown
**Leading Indicators:**
- Users get visibly excited during demos
- Users refer others without being asked
- Users complain when features are down
- Users ask for annual plans (want to commit long-term)
- Support emails shift from "how do I use this?" to "can you add X?"

**Quantitative Signals:**
- Organic growth > 50% of new signups
- Net revenue retention > 100% (existing users spend more over time)
- Paying users > 100
- MRR > $5,000
- Churn < 3% monthly
- NPS > 40
- 40% of users would be "very disappointed" without your product
  (Sean Ellis test — send survey to users who haven't logged in for 2 weeks)
```

### The Pre-V1 Pivot Decision

If you're not seeing product-market fit signals by month 6 post-MVP, you need to consider:

```markdown
**Pivot or Persevere Decision Tree:**

Am I seeing organic growth (> 20% of signups from referrals)?
├── YES → Are my retention metrics good?
│   ├── YES → Stay the course. Double down.
│   └── NO → Fix retention before growth.
└── NO → Are my retention metrics good?
    ├── YES → Growth problem. Focus on marketing.
    └── NO → Product problem. Major pivot needed.

If you need to pivot, do it fast. Don't wait another 6 months.
Pivot options:
1. Different customer segment (same product, different users)
2. Different problem (same users, different product)
3. Different business model (same product, different pricing)
```

### The "Build-It-Anyway" Exception

Some features should be built even if no one asks for them:

```markdown
**Build these without being asked:**
- Performance improvements (users rarely ask, but churn from slowness)
- Data export (users need this when leaving — reduce exit friction)
- Password reset (users need it in panic moments)
- Payment failure handling (users forget, you lose revenue)
- Basic security (you mess up once, you lose trust forever)

**Don't build these without being asked:**
- New bells and whistles (shiny object syndrome)
- Integrations with niche tools (too specific)
- Enterprise features (too complex, not validated)
- Mobile apps (users ask for this, but web first)
```

## The Solo Founder's V1 Timeline

### Month 1: Fix and Polish

```
Week 1-2:
  - Fix all MVP bugs
  - Address top friction points
  - Improve error messages
  - Add loading states

Week 3-4:
  - Improve onboarding flow
  - Add tooltips and help text
  - Improve empty states ("no data" pages)
  - Performance optimization
```

### Month 2: Core Feature Completion

```
Week 5-6:
  - Build the #1 requested feature
  - Complete any gaps in core workflow
  - Add export functionality

Week 7-8:
  - Build the #2 requested feature
  - Improve existing features based on feedback
  - Add integrations (if validated)
```

### Month 3: Launch Readiness

```
Week 9-10:
  - Redesign landing page for V1 launch
  - Create case studies with early customers
  - Set up automated email sequences
  - SEO optimization

Week 11-12:
  - Final testing and bug fixes
  - Load testing
  - Public V1 launch
  - Monitor and iterate
```

## Common V1 Mistakes (And How to Avoid Them)

### 1. Building Features for the Wrong Users

You have 5 customers. 2 are power users, 3 are casual. If you build for the power users, you optimize for the minority.

**Solution:** Segment your users. Build for the majority first. Power user features come after you've retained the median user.

### 2. Premature Self-Serve

You try to build documentation, help centers, and chatbots before your product works reliably.

**Solution:** Be accessible. Reply to emails within hours. Your personal attention is a feature, not a bug. Add self-serve when you can't keep up with support.

### 3. Over-Relying on Feedback

You build everything users ask for, resulting in a bloated product that serves no one well.

**Solution:** Remember Steve Jobs: "People don't know what they want until you show it to them." Trust your vision, but verify with data.

### 4. Not Talking to Users

The opposite of #3 — you build in isolation based on your assumptions.

**Solution:** Talk to at least 1 user per day. Every day. No exceptions.

### 5. Premature Scaling

You add infrastructure for 100k users when you have 50.

**Solution:** When you think about scalability, ask: "Is this a problem today?" If not, don't solve it.

### 6. Neglecting the Business

You focus 100% on product and 0% on sales.

**Solution:** At minimum, spend 20% of your time on sales and marketing, even during V1 development.

### 7. Feature Bloat

The product grows to include everything, becoming a "jack of all trades, master of none."

**Solution:** Say no to 90% of feature requests. Be known for doing one thing exceptionally well.

## Summary: The Solo Founder's V1 Roadmap Principles

1. **Build for retention, not acquisition.** Users who stay are more valuable than users who sign up.
2. **Say no to most features.** Your roadmap is a list of things you will NOT build, not a list of things you will.
3. **Talk to users daily.** Your roadmap should change weekly based on what you learn.
4. **Plan 90 days ahead max.** Everything beyond 90 days is a guess.
5. **Measure everything.** If you can't measure it, you can't improve it.
6. **Ship continuously.** Don't save features for "V2." Ship as soon as they're ready.
7. **Stay focused.** One core problem. One target user. One product that does it best.
8. **Don't pivot too early.** Give your MVP enough time to prove or disprove itself.
9. **Don't pivot too late.** If the data says you're wrong, change directions quickly.
10. **Product-market fit is a spectrum, not a destination.** You'll always be improving.
