# Defining the MVP Scope

## The Solo Founder's MVP Trap

Most solo founders fail because they build too much before launching. The single biggest predictor of SaaS success is how quickly you get something into paying customers' hands. This guide covers systematic techniques for defining, scoping, and ruthlessly cutting your MVP to the absolute minimum while still delivering real value.

## What MVP Really Means for SaaS

### The Only Thing That Matters

Your MVP's goal is not to validate your idea. It's not to build a perfect product. It's to get a paying customer. A single person who gives you money is infinitely more valuable than 100 people who say they "like the idea."

```
MVP Success = First Paid Customer in < 30 Days
```

If your MVP takes longer than 30 days to build, you've built too much.

### The Three Gates of MVP Scope

Every feature must pass through three gates:

1. **Does this directly enable someone to pay us?** (Payment processing, core value prop)
2. **Does this prevent an immediate churn risk?** (Basic error handling, data loss prevention)
3. **Does this make us look credible enough to get the first sale?** (Minimal branding, basic onboarding)

If a feature doesn't pass at least one gate, it's cut.

### The "No" Framework

As a solo founder, "no" is your most powerful tool. Every feature you say no to is time you can spend on the features that matter. Create a personal mantra:

> "If I don't absolutely need this for the first paying customer, it doesn't exist."

Write this on a sticky note. Put it on your monitor. Internalize it.

## Must-Have vs Nice-to-Have: The Exhaustive Framework

### The Four-Quadrant Method

For every potential feature, place it in one of four quadrants:

| | High Customer Value | Low Customer Value |
|---|---|---|
| **High Complexity** | Evaluate carefully — may be a differentiator | Cut immediately |
| **Low Complexity** | Include in MVP | Cut — nice-to-have later |

### Must-Have Categories (MVP)

These are the only features that belong in your MVP:

**1. Core Value Proposition (The "Job")**
- The single action your product performs that solves the customer's problem
- Must work end-to-end, even if ugly
- Example: For a project management tool, creating a task and marking it done

**2. Payment Processing**
- Ability to accept money
- Basic billing (one plan, one price)
- Invoice generation (even if manual)
- Payment receipts

**3. Authentication**
- Sign up / sign in
- Password reset
- Session management

**4. Data Persistence**
- User data is saved and retrievable
- Basic data integrity
- Error states that prevent data loss

**5. Absolute Minimum Onboarding**
- Get user from signup to first value in < 2 minutes
- Can be a manual walkthrough via email for first customer

**6. Basic Error Handling**
- Don't lose user data
- Don't show stack traces to users
- Basic 404 pages

### Nice-to-Have Categories (Cut These)

These features are explicitly excluded from MVP:

**1. Admin Dashboard**
- You don't need an admin panel for < 10 customers
- Manage data via database directly

**2. Team Collaboration**
- Multi-user, permissions, roles — all cut
- First customer is a single user

**3. Advanced Reporting**
- Analytics, charts, export — cut
- Manual reporting is fine for first customers

**4. Integrations**
- Zapier, API access, webhooks — cut
- Manual data transfer works for MVP

**5. Mobile App**
- Responsive web only
- Never build a mobile app for MVP

**6. Multi-Tenant Optimization**
- Separate databases per customer — cut
- Shared database with tenant_id is fine

**7. White-Labeling**
- Custom branding, domains — cut
- Your brand on everything

**8. Audit Logs**
- Activity history — cut for MVP
- Basic logging to terminal is fine

**9. Dark Mode**
- Never include this in an MVP

**10. Localization**
- English only. Always.

### The 80/20 Rule Applied

For each feature area, identify the 20% of work that delivers 80% of value:

| Feature Area | 20% (MVP) | 80% (Cut) |
|---|---|---|
| Authentication | Email + password | SSO, MFA, social login, magic links |
| Onboarding | Email welcome + manual call | In-app tutorial, drip campaigns |
| Billing | Stripe checkout link | Usage-based billing, proration, coupons |
| Search | Basic SQL LIKE query | Full-text search, Elasticsearch, filters |
| Notifications | In-app message | Email, SMS, push, webhook |
| Export | Manual CSV from DB | Automated scheduled exports, API |

## Scope Cutting Techniques

### Technique 1: The "Skateboard" Approach

Instead of building the perfect car, build something that gets the user from A to B:

```
Ultimate Vision (Car):
  Engine, transmission, wheels, steering, seats, doors,
  windows, paint, sound system, AC, GPS, heated seats

MVP (Skateboard):
  A board with four wheels that moves forward

Next Iteration (Scooter):
  Skateboard + steering mechanism

Next (Bicycle):
  Scooter with better propulsion

Next (Motorcycle):
  Faster, more stable

Eventually (Car):
  The original vision
```

**Application to SaaS:**
- **Skateboard**: Manual process that looks like the product (e.g., you do the work manually for the first customer)
- **Scooter**: The core computation is automated, but input/output is manual
- **Bicycle**: Core flow automated end-to-end, but no edge cases handled
- **Motorcycle**: Handles 80% of edge cases, basic error handling
- **Car**: The full product vision

### Technique 2: The "Razor" (One Feature Deep)

Your entire MVP should do ONE thing but do it exceptionally well. Not ten things poorly.

**Exercise:** Describe your product in six words or fewer. If you can't, your MVP scope is too wide.

Good:
- "Send invoices and get paid"
- "Track time across projects"
- "Schedule social media posts"

Bad:
- "Project management with invoicing, time tracking, team messaging, file sharing, and reporting"

### Technique 3: Manual Backend

For your MVP, do the complex parts manually. Automate only the customer-facing parts.

**Example: AI Content Tool**
- **Customer sees**: Type a topic, get an article
- **Behind the scenes**: You manually write/tweak the first 50 articles
- **Automation**: Only the delivery mechanism is automated

This is valid. It's called the "Wizard of Oz" MVP. The customer experiences the full product, but there's a human behind the curtain.

**When this works:**
- The manual process is faster than building automation
- You're testing demand, not scalability
- You can process 10-50 requests manually before needing automation

**When this fails:**
- The manual process introduces significant latency
- You can't maintain quality consistency
- The task requires real-time processing

### Technique 4: Feature Scaffolding

Build the UI for a feature but stub the backend. This lets you:
1. Test if users find the feature (click tracking)
2. Show "Coming Soon" instead of nothing
3. Gauge interest before building

```javascript
// Instead of building the full feature:
// FeatureScaffold.jsx
function FeatureScaffold({ featureName, onNotifyMe }) {
  return (
    <div className="feature-scaffold">
      <h3>{featureName}</h3>
      <p>This feature is coming soon.</p>
      <button onClick={onNotifyMe}>Notify me when available</button>
      <input type="hidden" name="clicked_feature" value={featureName} />
    </div>
  );
}
```

### Technique 5: Lowest Fidelity First

For every feature, ask: "What's the lowest fidelity version that delivers value?"

| Feature | High Fidelity | Low Fidelity (MVP) |
|---|---|---|
| Report generation | PDF with charts, filtering, scheduling | Plain text email summary |
| Image upload | Dropzone, compression, CDN | Simple file input, raw storage |
| Collaboration | Real-time sync, conflict resolution | Sequential editing, last-write-wins |
| Workflow automation | Drag-and-drop builder, triggers | Pre-defined templates you configure manually |
| Search | Full-text search, facets, relevance scoring | Ctrl+F in the browser |

### Technique 6: The "Mise en Place" Method

Restaurant chefs prepare ingredients before cooking. In SaaS, "prep" everything before building:

1. **Prep the database**: Have all schemas designed (even for future features)
2. **Prep the models**: Have data models defined
3. **Prep the API**: Have endpoints designed (stubbed)
4. **Build only the MVP endpoints fully**: The rest return 501 Not Implemented

This ensures your architecture doesn't need a complete rewrite for v2, but you don't build the full thing yet.

### Technique 7: Concierge MVP

For your first 3-5 customers, be the product. Whatever your SaaS does, do it manually. Charge full price.

**Process:**
1. Customer signs up on a landing page (takes 2 hours to build)
2. Customer submits their request via email or a simple form
3. You do the work manually
4. You deliver results via email
5. You observe what customers actually use, how they describe value, what they complain about

**This is the fastest path to understanding your market.**

**Case Study:** The first version of most successful SaaS products was a manual service. Basecamp started as a consulting project. Airbnb founders manually photographed listings.

## The MVP Scope Document Template

### Section 1: Product Statement

```
Product Name: [Name]
One-Line Description: [What it does, for whom]
Target Customer: [Single persona, specific]
Core Job to Be Done: [What does the customer hire this product for?]
```

### Section 2: MVP Success Criteria

```
First Payment Target: [Date, ideally 2-4 weeks from start]
Number of Paid Customers for Validation: [1-3]
Key Metric That Proves Value: [One number, e.g., "Customer creates 10 reports/week"]
Churn Threshold: [At what point would we kill the product?]
```

### Section 3: MVP Feature List

**Phase 1 — Must Have (Day 1):**
1. [Feature] — [Estimated time, must be < 1 week]
2. [Feature] — [Estimated time]
3. [Feature] — [Estimated time]

**Phase 2 — Should Have (Day 1-14):**
4. [Feature]
5. [Feature]

**Phase 3 — Nice to Have (if time permits):**
6. [Feature]
7. [Feature]

### Section 4: Explicit Exclusions

```
We will explicitly NOT build for MVP:
- [Feature everyone asks for but doesn't need]
- [Feature that's "standard" but not required]
- [Feature that's fun to build but provides zero value]
- [Feature that needs to be "perfect" — we'll make it ugly instead]
```

### Section 5: The "Good Enough" Bar

For each MVP feature, define what "good enough" looks like:

| Feature | Good Enough | Not Good Enough |
|---|---|---|
| Sign up | Email + password, works 95% of the time | Social login, magic links, MFA |
| Dashboard | Shows key data, loads in < 3s | Real-time updates, customization |
| Export | CSV download, manual trigger | Scheduled exports, all formats |

### Section 6: Technical Scope

```
Hosting: [Single VPS or serverless — simplest option]
Database: [One database, no replicas]
Auth: [Auth0/Firebase Auth/Clerk or hardcoded for first customer]
Payments: [Stripe checkout — simplest integration]
Monitoring: [None or basic uptime monitoring]
Backups: [Database snapshots once daily]
```

## Real-World MVP Scope Examples

### Example 1: Invoice SaaS (InvoiceNinja-style)

**MVP Scope (3 weeks):**
- Create and send invoices via email
- Accept payments via Stripe
- Mark invoices as paid
- Customer management (add, edit, delete)
- One user (solo business owner)

**Explicitly Cut:**
- Recurring invoices
- Expense tracking
- Time tracking
- Project management
- Multi-user
- Reports
- API
- Mobile app
- Templates

### Example 2: AI Writing Assistant

**MVP Scope (2 weeks):**
- One text input field
- One output of generated content
- Copy to clipboard button
- Credit system (1 credit = 1 generation)
- Stripe payment for credits
- Basic usage history

**Explicitly Cut:**
- Multiple tones/styles
- Long-form generation
- Templates
- Team accounts
- API access
- Browser extension
- Plagiarism checking

### Example 3: Project Management Tool

**MVP Scope (4 weeks):**
- Create projects
- Create tasks within projects
- Assign tasks to yourself
- Mark tasks complete
- Simple list view
- Email notifications for new tasks

**Explicitly Cut:**
- Kanban boards
- Gantt charts
- File attachments
- Comments
- Team permissions
- Time tracking
- Calendar view
- Dependencies

## The Solo Founder's MVP Timeline

### Week 1: Core Infrastructure & Auth
```
Day 1: Project setup, hosting, domain, SSL
Day 2: Authentication (signup/login)
Day 3: Database setup, user model
Day 4: Payment integration (Stripe)
Day 5: Landing page + signup flow
Day 6: Basic admin to view users
Day 7: Buffer/fix day
```

### Week 2: Core Feature
```
Day 8-9: Core feature — input handling
Day 10-11: Core feature — processing/output
Day 12: Polish the main flow
Day 13: Error handling for main flow
Day 14: Testing the happy path
```

### Week 3: Launch Prep
```
Day 15: Onboarding flow
Day 16: Email notifications (transactional)
Day 17: Privacy policy, terms of service
Day 18: Documentation/help page
Day 19: Final testing
Day 20: Soft launch to 5 potential customers
Day 21: Fix critical issues from soft launch
```

### Week 4: Launch
```
Day 22: Public launch
Day 23-28: Customer support, fix issues
Day 29-30: Evaluate: do we have paying customers?
```

## Anti-Patterns: What NOT to Do

### 1. "I Need Feature Parity"
You don't need every feature your competitor has. You need one feature they do better.

### 2. "But Enterprise Customers Need It"
You don't have enterprise customers. You have zero customers. Build for the solo operator or small team first.

### 3. "I'll Use Kubernetes Because I Might Need It"
You won't. Not for years. A single $20/mo VPS will handle thousands of customers for most SaaS products.

### 4. "I Need a Mobile App for Launch"
No you don't. Responsive web works perfectly fine. Mobile apps kill solo founder MVPs.

### 5. "I Should Use the Latest Tech"
Use whatever you know best. Speed to launch is all that matters. Rewrite later if needed.

### 6. "What If Someone Hacks It?"
Your MVP is unlikely to be targeted. Basic security (HTTPS, parameterized queries, rate limiting) is sufficient. Don't build Fort Knox for a bicycle.

### 7. "I Need Two-Factor Authentication"
No. You need a working product. Add 2FA when you have 1000 paying customers asking for it.

### 8. "Let's Plan for Scale"
Your MVP won't have scaling problems. Your problem is zero customers, not 100k concurrent users. A single Postgres instance handles millions of records.

## Making the Cut: Decision Trees

### Feature Elimination Decision Tree

```
Is this feature required for the user to
complete their primary goal?
├── YES → Is there a simpler way to achieve this?
│   ├── YES → Build the simpler version
│   └── NO → Include in MVP
└── NO → Does this feature prevent us from getting paid?
    ├── YES → Include (only if absolutely blocking payment)
    └── NO → Does this feature need to exist for the
              first customer to sign up?
        ├── YES → Minimum viable version only
        └── NO → CUT. It goes on the v2 list.
```

### Complexity Estimation Guide

| Complexity Level | Time Estimate | MVP Decision |
|---|---|---|
| Trivial | < 2 hours | Always include |
| Simple | 2-8 hours | Include if valuable |
| Moderate | 1-3 days | Evaluate carefully |
| Complex | 1-2 weeks | Almost always cut |
| Very Complex | 2+ weeks | Never include in MVP |

## From MVP Definition to Build: Your Action Plan

### Step 1: Write the Product Statement (30 minutes)

Write a single sentence describing your product. If you can't, you haven't scoped tightly enough.

### Step 2: Brain-Dump Every Feature (1 hour)

Write down every feature you think the product needs. Don't filter — just dump. Aim for 50+ features.

### Step 3: Categorize Using the Three Gates (2 hours)

Go through every feature and ask: does it enable payment, prevent churn, or add credibility? Yes to any = MVP candidate.

### Step 4: Estimate Complexity (1 hour)

For each MVP candidate, estimate how long it takes. Be honest. Multiply your estimate by 2 (solo founders are terrible estimators).

### Step 5: Apply the 30-Day Rule (1 hour)

Add up all estimates. If the total exceeds 30 days, cut features. Cut ruthlessly. Cut until you're at 20 days (buffer room).

### Step 6: Define "Good Enough" (1 hour)

For each remaining feature, define the minimum acceptable version. Be specific. "Fast" = loads in < 3 seconds. Not "fast."

### Step 7: Write the Explicit Exclusion List (30 minutes)

Document everything you will NOT build. This is as important as what you will build.

### Step 8: Get External Feedback (1 hour)

Show your scope document to 3 experienced founders. Ask them: "What should I cut?" Cut everything they suggest.

### Step 9: Start Building (Day 1)

Stop planning. Start building. Your plan is good enough. Perfection is the enemy of shipped.

## The MVP Commitment Contract

Print this and sign it:

```
I, [Name], commit to launching my MVP on or before [Date].

I will NOT add features to the MVP scope after starting.
I will NOT rewrite code that "isn't clean enough."
I will NOT compare my MVP to established products.
I will NOT wait for "perfect."
I will ship something imperfect that works.

My first goal is one paying customer. Nothing else matters.

Signed: ______________________ Date: ______________
```

## Measuring MVP Success

### The First 30 Days Checklist

- [ ] Customer #1 signed up
- [ ] Customer #1 completed core task
- [ ] Customer #1 paid
- [ ] Customer #1 is using the product 3x/week
- [ ] 5 total signups (paid or trial)
- [ ] 3 completed core task flows
- [ ] 2 paying customers total
- [ ] You've spoken to 10 potential customers
- [ ] You can articulate what's working and what's not

### Kill Criteria

If after 30 days of launch:
- 0 paying customers
- < 20 signups
- No repeat usage (users try once and leave)
- Users can't complete the core task

Then you need to pivot or significantly change your approach. This is not failure — this is learning. The MVP did its job by proving the idea doesn't work.

## Summary

A well-defined MVP is the single most important factor in solo founder success. The goal is not to build a great product — it's to build the smallest possible thing that gets someone to pay you. After that, you have real information. Before that, you have guesses.

**MVP Formula:**
```
MVP = (Core Value Delivery + Payment) × Speed
```

Build less. Ship faster. Listen more. Iterate endlessly.
