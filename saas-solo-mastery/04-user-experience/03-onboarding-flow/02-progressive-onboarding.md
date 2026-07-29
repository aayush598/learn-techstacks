# Progressive Onboarding

## The Problem with Traditional Onboarding

Traditional onboarding approaches fall into two camps, both flawed:

**The Walled Garden**: Lock users into a 20-step setup wizard before they can use the product. "Complete all 20 steps to unlock your workspace." Users bounce before they see value.

**The Firehose**: Dump all features at once on day one. "Here's everything you can do!" Users are overwhelmed, retain nothing, and leave confused.

Progressive onboarding is the middle path: reveal features and complexity gradually as the user's needs grow. It matches the user's skill progression with your feature depth.

---

## 1. The Progressive Onboarding Philosophy

### Core Principle

Don't teach users everything at once. Teach them just enough to accomplish their current goal, and reveal more sophistication when they're ready for it.

This mirrors how people naturally learn:
- A new driver doesn't learn how to drift on day one
- A new chef doesn't start with soufflés
- A new SaaS user doesn't need API access on day one

### The Three Levels of User Progression

| Level | User Mindset | What They Need | Timeframe |
|-------|-------------|----------------|-----------|
| **Novice** | "Can this solve my problem?" | Fast activation, clear next steps, hand-holding | First session |
| **Competent** | "I know how to use the basics. What else can this do?" | Discoverability, shortcuts, best practices | Week 1-4 |
| **Expert** | "I want to go faster and do more." | Automation, API, keyboard shortcuts, customization | Month 1+ |

### The Progression Funnel

```
Novice users: 100% (all users start here)
    ↓
Competent users: 40% (of those who activate and stick around)
    ↓
Expert users: 10-15% (of power users who deeply adopt the product)
```

Your onboarding should serve all three levels, not just novices.

---

## 2. Feature Adoption Sequencing

### What Is Feature Sequencing

Feature sequencing is the deliberate order in which you introduce features to users. Not all features are equal, and the order matters enormously.

### The Sequencing Framework

**Phase 1: Core Value Features (Day 1)**
- Features required for activation
- The absolute minimum set that delivers value
- No more than 3-5 features exposed

**Phase 2: Stickiness Features (Week 1-2)**
- Features that increase retention
- Notifications, sharing, templates
- Integrations with other tools the user already uses

**Phase 3: Expansion Features (Month 1-2)**
- Features that increase usage depth
- Advanced reporting, automation, custom fields
- Team collaboration features

**Phase 4: Power Features (Month 2+)**
- Features for expert users
- API access, webhooks, custom integrations
- Bulk operations, keyboard shortcuts

### Feature Sequencing Matrix

| Feature | Phase | Why Here | How to Introduce |
|---------|-------|----------|-----------------|
| Core action | 1 | Required for activation | Front and center in UI |
| Dashboard | 1 | See the value | Default landing page |
| Templates | 1 | Quick start | Shown during setup |
| Notifications | 2 | Bring user back | Enabled by default |
| Sharing | 2 | Viral loop | "Invite team" prompt |
| Reports | 2 | Deeper value | After enough data collected |
| API | 4 | Power user | In developer docs |
| Automation | 3 | Efficiency | Suggested after repeated manual actions |

---

## 3. Progressive Onboarding vs. Walled Gardens

### Walled Garden Approach

```
Signup → Complete Profile → Import Data → Set Up Workspace → Invite Team → Configure Settings → SEE PRODUCT
```

The product is locked behind a sequence of tasks. Users must complete all setup before seeing value.

**Works for**: Enterprise products where configuration is mandatory (and sale is already made)
**Fails for**: Self-serve SaaS where users need to see value to stay

### Progressive Onboarding Approach

```
Signup → SEE PRODUCT → Complete Core Action → Get Value → Configure More (at their pace)
```

The product is open immediately. Setup happens gradually, with the user, at their speed.

**Advantages**:
- Users see value fast
- No forced commitment before value
- Users can skip what they don't need
- Lower drop-off at every step

### When to Use Walled Gardens

There ARE cases where walled gardens work:
- **Compliance-focused products**: Must enforce certain configurations (GDPR, HIPAA)
- **Hardware/IoT products**: Need physical setup before use
- **Enterprise procurement**: The buyer (not user) has already purchased
- **On-premise software**: Requires installation

For 90% of SaaS products, progressive onboarding is better.

### The Hybrid Approach

Some products use a hybrid: small walled garden (3-5 essential steps) then open up:

```
1. Choose a template (pre-populates everything)
2. Customize name (one field)
3. See your ready workspace!
4. Optional: invite team, customize further
```

This preserves the "see value fast" principle while ensuring some minimum configuration.

---

## 4. The Novice Experience (Day 1)

### Design Goals

1. User experiences core value in < 5 minutes
2. User understands what the product does for them
3. User knows what to do next
4. User feels successful, not stupid

### What to Show

| Element | What to Include | What to Hide |
|---------|----------------|--------------|
| Navigation | Dashboard, primary feature, settings | Admin panel, integrations, billing |
| Dashboard | Core metric, quick action, recent activity | All widgets, reports, charts |
| Actions | Primary action (big button), template, import | Bulk actions, advanced filters |
| Settings | Name, timezone, notification prefs | API keys, team roles, billing |
| Help | Tooltip on key elements, getting started guide | Full docs, API reference |

### The First Session Template

```
1. User signs up → lands on dashboard with pre-populated data
2. Dashboard shows: "Welcome! Here's [example of core value]."
3. Primary CTA: "Do [core action]" button
4. User takes core action → sees immediate result
5. "Great! You just [achieved something]. Want to [secondary action]?"
6. Optional: Tour of 2-3 key features (just-in-time, tooltip style)
7. User ends session having experienced value
```

### The Novice UX Principles

- **Everything is obvious**: No hidden menus, no ambiguous icons
- **Every action has feedback**: Loading states, success messages, error explanations
- **Nothing is destructive**: Undo available on everything
- **Help is always one click away**: Question mark icon, tooltips, inline help
- **No dead ends**: Every page has a clear next action

---

## 5. The Competent User Experience (Week 1-4)

### When a User Becomes Competent

Signs a user is ready for more:
- They've completed the core action 3+ times
- They're returning to the product without prompting
- They're exploring features outside the core flow
- They haven't asked basic questions in support

### What to Reveal

**Phase 2 features**:
- Keyboard shortcuts
- Batch operations
- Templates and saved configurations
- Reports and analytics
- Notifications and alerts
- Basic customization

### How to Reveal

**Pattern 1: "Did you know?" prompts**
When user performs a basic action, suggest an advanced version:
- "You just created a task. Did you know you can create 10 tasks at once?"
- "You filtered your list. Save this filter for next time?"

**Pattern 2: Progressive enhancement**
Add subtle UI enhancements that become visible:
- Keyboard shortcut hints appear next to buttons after week 1
- "More options" expandable section appears after core features used

**Pattern 3: Feature discovery emails**
- Day 3: "Pro tip: Use templates to save time"
- Day 7: "Did you know you can automate [tedious task]?"
- Day 14: "Your team is waiting! Invite them to collaborate."

**Pattern 4: Contextual suggestions**
Based on user behavior:
- User manually exports data weekly → "Try our API for automatic exports"
- User repeats same action 5x → "Create a template for this"
- User checks reports daily → "Save this report as a scheduled email"

### The Competent UX Principles

- **Efficiency is king**: Show shortcuts, batch operations, automation
- **Discovery is built-in**: Don't rely on users reading docs
- **Proactive suggestions**: The product should teach itself
- **Personalization matters**: Different users need different features revealed

---

## 6. The Expert User Experience (Month 2+)

### Identifying Expert Users

- Using the product daily
- Using advanced features already
- Requesting API/webhook access
- Asking about custom workflows
- Referring other users

### What to Reveal

- API and webhooks
- Custom integrations
- Advanced automation
- Custom fields and workflows
- Bulk operations
- Admin panel (if applicable)
- Usage analytics
- Custom reporting

### How to Reveal

**Pattern 1: The "Advanced" section**
Group power features in an "Advanced" section of settings or a developer portal. Don't show by default; let users discover when they're ready.

**Pattern 2: User-initiated discovery**
Power users will find advanced features:
- Search for "API" in your help docs
- Ask support about integrations
- Explore settings pages

Make sure these features are discoverable through search and settings exploration.

**Pattern 3: Community-driven learning**
- User forums and communities
- User-contributed templates and workflows
- Power user webinars (recorded)
- Case studies of advanced usage

**Pattern 4: Personal onboarding (for high-value users)**
For your top 10% of users:
- Personal demo of advanced features
- Custom setup help
- Beta access to new features
- Direct line to founder (that's you)

### The Expert UX Principles

- **Speed over guidance**: Experts don't want hand-holding, they want speed
- **Flexibility and customization**: Experts want the product to adapt to them
- **Automation**: Experts don't want to repeat manual tasks
- **Integration**: Experts want the product to work with their stack
- **Control**: Experts want fine-grained control over everything

---

## 7. Progressive Onboarding Design Patterns

### Pattern 1: Layered Complexity

The simplest interface has only the essential features. Additional complexity is added in layers as users express readiness.

**Example**: Photo editor
- Layer 1: One "Auto-enhance" button
- Layer 2: Brightness, contrast, saturation sliders
- Layer 3: Curves, levels, color grading
- Layer 4: LUTs, presets, batch processing

**Implementation**: UI elements that are "collapsed" by default with a "Show more" reveal mechanism.

### Pattern 2: Master-Apprentice Model

The product initially does things for the user (master), then gradually lets the user take over (apprentice).

**Example**: Accounting software
- Month 1: Auto-categorize all transactions
- Month 2: Show user the categories, let them override
- Month 3: Suggest rules based on their overrides
- Month 4: Let user create their own categorization rules

**Implementation**: Start with full automation, expose the automation settings, suggest improvements, let user customize.

### Pattern 3: Just-in-Time Education

Teach features right when the user needs them, not before.

**Example**: CRM
- When user creates a contact from scratch → "Quick tip: Import contacts from a CSV to save time"
- When user has 10+ contacts → "Try our list view for easier navigation"
- When user searches for a contact → "Save this search for one-click access"
- When user sends 5 emails → "Create email templates for common replies"

**Implementation**: Behavior-triggered tooltips, banners, or emails.

### Pattern 4: Challenge-Based Progression

Gamify the learning process by presenting challenges that teach new features.

**Example**: Design tool
- Challenge 1: "Create a button" (teaches basic shape creation)
- Challenge 2: "Make it look clickable" (teaches color and shadow)
- Challenge 3: "Export it for web" (teaches export settings)
- Challenge 4: "Create a button component" (teaches components)

**Implementation**: Optional challenge system with progress tracking and rewards.

### Pattern 5: Gradual Exposure

Don't show all options at once. Reveal them over time based on usage patterns.

**Example**: Analytics dashboard
- Week 1: One chart showing total visitors
- Week 2: A comparison toggle appears (compare periods)
- Week 3: Filter options appear
- Week 4: Custom chart builder appears
- Month 2: Advanced segmentation appears

**Implementation**: Feature flags based on account age or usage milestones.

---

## 8. Setting Up Progressive Feature Flags

### Feature Flags for Onboarding

Use feature flags to control which features each user sees:

```js
const features = {
  basic_export: true,        // Available to all
  bulk_export: false,         // Unlock after basic export used 3x
  api_access: false,          // Unlock after 30 days
  custom_reports: false,      // Unlock on upgrade
  team_collaboration: false,  // Unlock on upgrade to pro
}

// Check feature access
if (user.features.api_access) {
  showAPISection()
}
```

### Feature Flag Services

- **PostHog**: Feature flags + analytics (free tier)
- **LaunchDarkly**: Enterprise-grade (expensive)
- **Flagsmith**: Open source
- **GrowthBook**: Open source
- **Custom**: Simple flag system in your database

### Milestone-Based Unlocking

Unlock features based on user milestones:

| Milestone | Unlock |
|-----------|--------|
| Signed up | Core features |
| Completed core action 3x | Templates, export |
| Active for 7 days | Reports, analytics |
| Invited a team member | Team features |
| Upgraded to paid plan | All premium features |
| Active for 30 days | API access |
| Requested advanced feature | Beta features |

### Implementation Pattern

```js
// Check if user has earned a feature
function hasFeature(user, feature) {
  const milestones = {
    templates: user.coreActions >= 3,
    reports: user.daysActive >= 7,
    api_access: user.daysActive >= 30 || user.plan === 'pro',
    team: user.teamInvites > 0 || user.plan === 'business',
  }
  return milestones[feature] || false
}
```

---

## 9. The Onboarding Communication Calendar

### Email Sequence (Progressive)

**Day 1 (post-signup)**:
- "Welcome! Your workspace is ready"
- Single CTA: "Complete your first [core action]" 
- No secondary messages

**Day 3**:
- "You're off to a great start"
- Feature tip: "Did you know you can use templates?"
- Case study: "How [customer] saved [time/money] with [feature]"

**Day 7**:
- "Go deeper with [advanced feature]"
- Tutorial: Specific guide for a secondary feature
- Invitation to upgrade (if free trial)

**Day 14**:
- "You've mastered the basics. Here's what's next"
- Introduction to power features
- Personal check-in: "Reply if you need help"

**Day 30**:
- "You're a power user now"
- API and integration documentation
- Beta feature invitation
- Referral program invitation

### In-App Messages

**Session 2**:
Banner: "Welcome back! Here's what changed this week."

**Session 3-5**:
Tooltip on feature: "Try batch operations to save time."

**Session 5+**:
"Power user tip: Press ? to see keyboard shortcuts."

**After upgrade**:
"Welcome to Pro! Here are your new features."

---

## 10. Measuring Progression Success

### Key Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Feature adoption rate | % of users who try each feature | > 30% per major feature |
| Feature stickiness | % of users who use feature again within 7 days | > 40% |
| Time to second feature | Days until user tries a non-core feature | < 7 days |
| Novice-to-competent rate | % of users who use 3+ features in first 14 days | > 50% |
| Competent-to-expert rate | % of users who use advanced features by day 30 | > 15% |

### Feature Tracking

Track every feature interaction:

```js
// Track feature usage
analytics.track('Feature Used', {
  feature: 'template_import',
  user_tier: 'novice', // novice, competent, expert
  session_number: 3,
  days_since_signup: 5,
})
```

### Progression Dashboard

```
Feature Adoption Funnel (Last 30 days):

Core Feature (Track time)    83% of users
Templates                     42% of users
Export/Reports                28% of users
Team Collaboration            15% of users
API                            5% of users
Automation                     3% of users

Average time between features:
  Core → Templates: 3.2 days
  Templates → Reports: 5.1 days
  Reports → Team: 8.7 days
  Team → API: 15.3 days
```

---

## 11. Common Progressive Onboarding Mistakes

### Mistake 1: Holding Back Too Much

"I won't show any advanced features until day 30." Some users are ready for advanced features on day 1. Let users advance at their own pace.

**Fix**: Make advanced features discoverable without being loud. A subtle "Advanced" tab or search that finds everything.

### Mistake 2: Gating Features Artificially

"Users can only use this feature after 14 days." If a user discovers and wants to use a feature, let them. Artificial gates frustrate power users.

**Fix**: Gate by behavior, not time. "Use core feature 3x" is better than "wait 14 days."

### Mistake 3: No Clear Progression Path

Users don't know what features exist or how to discover them.

**Fix**: Show a clear progression path: "Getting started → Level up → Power user" with specific milestones.

### Mistake 4: Treating All Users the Same

A novice and an expert see the same interface. The novice is overwhelmed, the expert is annoyed.

**Fix**: Segment by behavior and adjust UI complexity accordingly.

### Mistake 5: Ignoring Power Users

All onboarding effort goes to new users. Power users get ignored.

**Fix**: Create an expert onboarding track: API docs, advanced tutorials, community features.

### Mistake 6: Over-Engineering Progression

Building complex feature flag systems before you have product-market fit.

**Fix**: Start simple. Use a few manual segments (new/mostly there/power user) and adjust as you learn.

---

## 12. Progressive Onboarding Examples

### Example 1: Notion

**Novice**: Opens to a blank page. Can start typing immediately. Template gallery shown as "Get started."

**Competent**: Discovers databases, kanban boards, linked pages through use and template exploration.

**Expert**: Uses databases, formulas, linked databases, API integration, custom templates.

**Key pattern**: The blank canvas is the simplest possible interface. Complexity is added as user needs grow.

### Example 2: Canva

**Novice**: Lands on template gallery. Picks one, edits text, exports. Core loop: pick → edit → export.

**Competent**: Discovers brand kits, photo editing, animation, team templates.

**Expert**: Creates brand templates, uses bulk create, API integrations, custom fonts.

**Key pattern**: Templates are the gateway drug. Users start by customizing, graduate to creating.

### Example 3: Linear

**Novice**: Creates issues, moves through workflow. Clean interface with minimal options.

**Competent**: Discovers keyboard shortcuts (shown with ? key), command palette, issue templates.

**Expert**: Uses API, cycle analytics, advanced filters, automation rules.

**Key pattern**: Keyboard shortcuts are the bridge from novice to expert. The product never shows all features at once.

### Example 4: Stripe

**Novice**: Single API key, one endpoint, charge a card. Core loop: charge → confirm → dashboard.

**Competent**: Webhooks, subscriptions, Connect platform, Stripe Billing.

**Expert**: Radar risk rules, Sigma analytics, Treasury, Issuing.

**Key pattern**: Progressive complexity via documentation. The API is simple at first, with advanced features only a link away.

---

## 13. Building Progressive Onboarding as a Solo Founder

### The Lean Approach

You don't need a sophisticated feature flag system. Start with:

**Phase 1: Three user states**
1. **New** (< 7 days since signup)
2. **Active** (used product 3+ times)
3. **Power** (used advanced features or 30+ days)

Store in user profile: `user_tier: 'new' | 'active' | 'power'`

**Phase 2: Simple conditional UI**
```jsx
{user.tier === 'new' && <NewUserWelcome />}
{user.tier === 'active' && <ProTipBanner />}
{user.tier === 'power' && <APIPrompt />}
```

**Phase 3: Behavior-triggered**
```jsx
// Show advanced export after user exports 3 times
{user.exportCount >= 3 && <BulkExportPromo />}
```

That's all you need for 90% of the benefit. Only invest in a full feature flag system when you have 1000+ users.

### Implementation Priority

1. **Define user tiers**: new, active, power (database field)
2. **Add conditional UI**: Show/hide elements based on tier
3. **Track feature usage**: 5-10 key events
4. **Create milestones**: When to unlock/show features
5. **Build progression content**: Emails, tooltips, prompts
6. **Analyze and iterate**: What's working? What's not?

### Tools for Solo Progression Tracking

- **PostHog**: Event tracking + feature flags (free tier)
- **Clerk**: User management with metadata (free tier)
- **Supabase**: Database + auth, store user state
- **Custom**: Simple database flags + JavaScript

---

## 14. Progressive Onboarding Checklist

### Novice Experience
- [ ] Core value delivered in < 5 minutes
- [ ] Only 3-5 features visible
- [ ] Clear primary action on every screen
- [ ] All non-essential UI hidden
- [ ] Help is obvious and accessible
- [ ] Guided first action with pre-populated data
- [ ] Activation is celebrated
- [ ] Next step is clear

### Competent Experience
- [ ] Features unlock based on behavior, not just time
- [ ] Keyboard shortcuts are discoverable
- [ ] Templates and saved configurations are suggested
- [ ] Batch operations are introduced
- [ ] Proactive hints appear at the right moment
- [ ] Personalization options are revealed
- [ ] Feature discovery emails are sent on schedule

### Expert Experience
- [ ] API access is available
- [ ] Custom integrations can be configured
- [ ] Automation features are accessible
- [ ] Advanced settings and customization
- [ ] Bulk operations are supported
- [ ] Performance shortcuts are documented
- [ ] Power user community exists

### Technical Implementation
- [ ] User tiers defined (new, active, power)
- [ ] Feature usage tracked (5-10 key events)
- [ ] Conditional UI based on tier/milestones
- [ ] Milestone-triggered communications
- [ ] Simple feature flag system in place
- [ ] Analytics to measure progression

### Ongoing Optimization
- [ ] Feature adoption tracked weekly
- [ ] Novice-to-competent conversion measured
- [ ] Progression bottlenecks identified
- [ ] A/B test different progression timings
- [ ] User feedback collected on feature discovery

---

## 15. The Solo Progressive Onboarding Manifesto

1. **Show value first, complexity later** — The first session should be the simplest
2. **Reveal, don't gate** — Features should be discoverable, not locked
3. **Progress is personal** — Let users advance at their own speed
4. **Behavior beats time** — Gate on actions, not calendar days
5. **Novice, competent, expert** — Three tiers handle 90% of users
6. **Just-in-time teaching** — Teach features when users need them
7. **Simple wins** — Feature flags in a database column, not a complex system
8. **Power users are your secret weapon** — Invest in their experience
9. **Every user starts as a novice** — No matter how sophisticated
10. **Perfect progression is invisible** — Users shouldn't know they're being progressively onboarded

Progressive onboarding is not about holding features back. It's about serving the right features to the right user at the right time. When done well, users never feel overwhelmed or bored—they feel like the product is adapting to them.
