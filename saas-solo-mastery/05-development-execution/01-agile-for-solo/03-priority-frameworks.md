# Priority Frameworks for Solo Founders

## The Decision Dilemma

As a solo founder, you face an endless stream of decisions:
- What feature should I build next?
- Which bug should I fix first?
- Should I spend time on marketing or development?
- Is this user request worth implementing?
- Should I refactor this code or ship the feature now?

Without a structured approach to prioritization, you'll:
- Build features nobody uses
- Fix bugs that don't matter
- Waste time on low-impact work
- Feel overwhelmed by competing priorities

Priority frameworks give you an objective way to make decisions. They replace gut feelings with structured thinking.

---

## 1. The RICE Framework

### What Is RICE

RICE is a scoring framework for prioritizing features and projects:

**R**each: How many users will this affect?
**I**mpact: How much will this affect each user?
**C**onfidence: How confident are we in our estimates?
**E**ffort: How much time will this take?

### Scoring Each Factor

**Reach** (per timeframe, e.g., per month):
- 1 = < 10 users
- 2 = 10-100 users
- 3 = 100-1,000 users
- 4 = 1,000-10,000 users
- 5 = 10,000+ users

**Impact** (per user):
- 1 = Minimal (nice-to-have)
- 2 = Low (small improvement)
- 3 = Medium (noticeable improvement)
- 4 = High (significant improvement)
- 5 = Massive (transformative)

**Confidence**:
- 1 = Pure guess
- 2 = Low confidence (some evidence)
- 3 = Medium (mix of data and intuition)
- 4 = High (strong data or experience)
- 5 = Very high (clear data)

**Effort** (total person-days):
- 1 = > 30 days
- 2 = 10-30 days
- 3 = 3-10 days
- 4 = 1-3 days
- 5 = < 1 day

### The RICE Score

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Example**:

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| CSV Export | 4 | 3 | 4 | 3 | 16.0 |
| Dark Mode | 5 | 2 | 3 | 4 | 7.5 |
| Team Dashboard | 3 | 4 | 2 | 2 | 12.0 |
| API Access | 2 | 5 | 1 | 1 | 10.0 |

CSV Export scores highest because it affects many users, has decent impact, high confidence, and moderate effort.

### When to Use RICE

**Best for**: Feature prioritization when you have data (even rough estimates)
**Avoid when**: You have purely emotional decisions (user requests from a single user)

### Solo Adaptation

As a solo founder, your confidence is often lower (less data). That's OK. Use RICE as a thinking tool, not a precise calculator. The act of scoring forces you to think about each dimension.

**Pro tip**: If a feature's RICE score is inflated because you're guessing on reach/impact, the low confidence will bring it down naturally.

---

## 2. The Eisenhower Matrix

### What Is It

The Eisenhower Matrix categorizes tasks by urgency and importance:

| | Urgent | Not Urgent |
|--|--------|------------|
| **Important** | Quadrant 1: Do First | Quadrant 2: Schedule |
| **Not Important** | Quadrant 3: Delegate | Quadrant 4: Eliminate |

### Applied to Solo SaaS

| | Urgent | Not Urgent |
|--|--------|------------|
| **Important** | **Q1: Do Now** | **Q2: Plan** |
| | Server down, security issue, critical bug, payment failing | Feature development, refactoring, marketing, strategy |
| **Not Important** | **Q3: Schedule/Quick** | **Q4: Eliminate** |
| | Non-critical bug, user request (one person), internal tooling | Meetings that could be emails, perfecting designs, bike-shedding |

### How to Use It

1. List every task you need to do
2. Categorize each into one quadrant
3. Q1: Do immediately
4. Q2: Schedule into your week
5. Q3: Do quickly if you have time, or batch
6. Q4: Delete — don't do these

### Common Solo Founder Mistakes

**Mistake**: Treating everything as Q1 (urgent + important)

Many solo founders operate in crisis mode. Not everything is urgent. Learn to distinguish:
- **Truly urgent**: Server down, security breach, critical bug affecting all users
- **False urgency**: User complaining about a minor issue, email from a prospect, social media notification

**Mistake**: Ignoring Q2

Q2 is where your product grows: features, marketing, strategy, learning. But it's never "urgent," so it gets postponed.

**Fix**: Schedule Q2 tasks first, before you get sucked into Q1 and Q3.

### The 80/20 of Q2

Not all Q2 tasks are equal. Within Q2, prioritize:
- The feature most users request (reach)
- The improvement that reduces churn (retention)
- The marketing that brings the most traffic (acquisition)

---

## 3. Impact/Effort Matrix

### What Is It

A simple 2x2 grid comparing effort vs. impact:

| | High Impact | Low Impact |
|--|------------|------------|
| **Low Effort** | **Quick Wins** (Do first) | **Fill-ins** (Do when you have time) |
| **High Effort** | **Major Projects** (Plan carefully) | **Avoid** (Don't do) |

### Prioritization Order

1. **Quick Wins**: High impact, low effort → Do NOW
2. **Major Projects**: High impact, high effort → Plan, break into smaller pieces
3. **Fill-ins**: Low impact, low effort → Do when you have downtime
4. **Avoid**: Low impact, high effort → Delete from backlog

### Scoring

**Impact** (1-10):
- 1 = No one cares
- 5 = Some users care
- 10 = Changes the business

**Effort** (1-10):
- 1 = 15 minutes
- 5 = 2-3 days
- 10 = 2+ weeks

### Example

| Task | Impact | Effort | Quadrant | Action |
|------|--------|--------|----------|--------|
| Fix signup button color | 7 | 1 | Quick win | Do today |
| Add dark mode | 3 | 7 | Avoid | Delete |
| Build CSV export | 8 | 5 | Major project | Break into 3-week project |
| Update footer link | 1 | 1 | Fill-in | Do when bored |
| Team collaboration | 9 | 9 | Major project | Break into milestones |
| Fix typo on pricing page | 2 | 1 | Fill-in | Do now (it's fast) |

### Solo Adaptation

The Impact/Effort matrix is the most practical framework for daily decisions because it's simple and intuitive. Use it for:
- Daily task prioritization
- Sprint planning
- Quick "should I do this now?" decisions

---

## 4. The ICE Framework

### What Is ICE

Similar to RICE but simpler:

**I**mpact: How much impact will this have?
**C**onfidence: How confident are we in success?
**E**ase: How easy is it to implement?

### Scoring

Each factor scored 1-10:

```
ICE Score = (Impact + Confidence + Ease) / 3
```

### Example

| Feature | Impact | Confidence | Ease | ICE Score |
|---------|--------|------------|------|-----------|
| Fix subscription flow | 9 | 8 | 7 | 8.0 |
| Add Google login | 7 | 9 | 5 | 7.0 |
| Redesign dashboard | 5 | 4 | 3 | 4.0 |
| Add chat widget | 4 | 3 | 6 | 4.3 |

### When to Use ICE

- Simple prioritization (less data analysis)
- When you need a quick decision
- When confidence is more important than reach

---

## 5. The MoSCoW Method

### What Is MoSCoW

**M**ust have: Non-negotiable for success
**S**hould have: Important but not critical
**C**ould have: Nice-to-have
**W**on't have: Explicitly out of scope

### Applied to Solo SaaS

**Must have** (for a release):
- Core functionality works
- No critical bugs
- Authentication
- Payment processing (if paid)

**Should have**:
- Nice UI on core pages
- Email notifications
- Basic analytics
- Export functionality

**Could have**:
- Dark mode
- API access
- Advanced reporting
- Team features

**Won't have**:
- Mobile app
- Enterprise SSO
- AI features
- Marketplace

### When to Use MoSCoW

**Best for**: Release planning, version scoping, saying "no"
**Avoid**: Day-to-day task prioritization

### Saying "No" with MoSCoW

As a solo founder, you MUST say no to most things. MoSCoW helps:

- "That feature is a 'Could have.' We're only doing 'Must have' this month."
- "That's a 'Won't have' for Q2. Let's revisit in Q3."
- "I hear you, but that's a 'Should have.' Here's what we're prioritizing first."

---

## 6. The Kano Model

### What Is the Kano Model

The Kano Model categorizes features by how they affect user satisfaction:

| Feature Type | Description | If Present | If Absent |
|-------------|-------------|------------|-----------|
| **Basic** (Threshold) | Expected, taken for granted | Neutral | Very dissatisfied |
| **Performance** (Linear) | More is better | Satisfied | Dissatisfied |
| **Delight** (Attractive) | Unexpected, surprising | Delighted | Neutral |

### Examples

| Type | Example | Notes |
|------|---------|-------|
| **Basic** | User can log in, data is secure, page loads | Must have, won't get credit |
| **Performance** | Faster loading, more features, better UI | Invest proportional to value |
| **Delight** | Beautiful animations, personalized dashboard, "magic" features | Invest after basics are solid |

### Using Kano as a Solo Founder

1. **Cover basics first**: Login, security, core functionality
2. **Invest in performance**: Speed, features, quality — proportional to user value
3. **Add delight sparingly**: Surprise and delight features create buzz

### Common Mistake

Building delight features before basics are covered.
- "We added AI-powered suggestions!" — But users can't even change their password.
- "Our dashboard has beautiful animations!" — But it takes 5 seconds to load.

Basics > Performance > Delight. In that order.

---

## 7. User Feedback Prioritization

### The Feature Request Funnel

Not all user requests are equal. Prioritize across these dimensions:

**Frequency**: How many users request this?
**Intensity**: How much do they want it? (How many times do they ask?)
**Value**: How much value would it add to the product?
**Alignment**: Does it fit your product vision?
**Effort**: How hard is it to build?

### The User Request Score

```
Score = (Frequency × 2) + (Intensity × 1.5) + (Value × 2) + (Alignment × 1.5) - (Effort × 1)
```

Each factor scored 1-5.

### Example

| Request | Freq | Inten | Value | Align | Effort | Score |
|---------|------|-------|-------|-------|--------|-------|
| "Add CSV import" | 5 | 4 | 5 | 5 | 3 | 38.5 |
| "Add dark mode" | 3 | 2 | 2 | 4 | 4 | 14.5 |
| "API access" | 2 | 5 | 4 | 5 | 2 | 32 |
| "Team feature" | 1 | 3 | 5 | 3 | 1 | 24 |

### When to Say Yes

Say yes when:
- Multiple users request the same thing
- A paying user requests it
- It aligns with your product vision
- The effort is low
- You would use it yourself

### When to Say No

Say no when:
- Only one user requests it
- It doesn't fit your vision
- The effort is high
- You wouldn't use it
- A workaround exists

---

## 8. Bug Prioritization

### The Bug Severity Matrix

| Severity | Description | Response Time | Fix Timeline |
|----------|-------------|---------------|--------------|
| **P0: Critical** | All users affected, data loss, security breach | Immediate | Hours |
| **P1: High** | Core feature broken for many users | < 4 hours | 1-2 days |
| **P2: Medium** | Feature broken for some users, workaround exists | < 24 hours | 1 week |
| **P3: Low** | Minor issue, cosmetic, edge case | < 1 week | Next sprint |
| **P4: Trivial** | Typo, minor UI glitch | When you get to it | Backlog |

### Bug Priority = Severity × Frequency

| | Many Users | Few Users |
|--|------------|-----------|
| **Critical** | P0 - Fix NOW | P1 - Fix today |
| **High** | P1 - Fix today | P2 - Fix this sprint |
| **Medium** | P2 - Fix this sprint | P3 - Next sprint |
| **Low** | P3 - Next sprint | P4 - Backlog |

### The Solo Bug Triage

1. User reports bug
2. Reproduce it (can you make it happen?)
3. Determine severity (how bad is it?)
4. Determine frequency (how many users affected?)
5. Score (severity × frequency)
6. Schedule based on score

Don't fix every bug immediately. Not all bugs are equal, and some users are more tolerant than others.

---

## 9. Technical Debt Prioritization

### When to Refactor

| Scenario | Action |
|----------|--------|
| "This code is ugly but works fine" | Don't touch it |
| "This code is slow and users are noticing" | Prioritize fix |
| "This code makes adding new features hard" | Schedule refactor |
| "This code has security vulnerabilities" | Fix immediately |
| "This code is hard to understand" | Add comments, don't refactor |

### The Refactor Decision Matrix

| | High Impact on Users | Low Impact on Users |
|--|---------------------|---------------------|
| **High Impact on Development** | Priority 1 | Priority 3 |
| **Low Impact on Development** | Priority 2 | Skip |

**Priority 1**: Fixes that users notice AND make your life easier → Do soon
**Priority 2**: Fixes only users notice → Do when you have time
**Priority 3**: Fixes only you notice → Do when the code bothers you enough
**Skip**: Nobody notices → Don't do

### Technical Debt Budget

Allocate 10-20% of your development time to technical debt. If you never pay it down, it accumulates and slows you down. If you spend too much on it, you never ship features.

**Rule**: Every month, spend 1-2 days on cleanup, refactoring, and paying down technical debt.

---

## 10. Marketing vs. Product Prioritization

### The Builder's Trap

Solo founders love building. It's concrete, controllable, and immediately satisfying. Marketing is fuzzy, uncertain, and slow.

**Result**: You spend 90% of your time building and 10% marketing. But the product that nobody knows about is worthless.

### The 50/30/20 Rule

As a solo founder, allocate your time:

| Activity | % Time | Example |
|----------|--------|---------|
| Product (building) | 50% | Features, fixes, improvements |
| Marketing (distribution) | 30% | Content, social, SEO, outreach |
| Business (operations) | 20% | Support, admin, legal, strategy |

### When to Shift

**Pre-PMF** (0-100 users):
- Product: 40%
- Marketing: 50% (you need users!)
- Business: 10%

**Post-PMF** (100-1000 users):
- Product: 50%
- Marketing: 30%
- Business: 20%

**Scale** (1000+ users):
- Product: 40%
- Marketing: 35%
- Business: 25%

### Making the Decision

Each week, ask: "What's the ONE thing that would move the needle most this week?"

If it's a feature → build
If it's getting users → market
If it's keeping users → support/improve

---

## 11. The Daily Priority Framework

### The 3-Task Rule

1. **One big task**: The most important thing for the business (feature, marketing push)
2. **One maintenance task**: Keep things running (bugs, support, ops)
3. **One small task**: Low effort, quick win (tweak, fix, improvement)

### The Ivy Lee Method

1. At end of each workday, write down the 6 most important things for tomorrow
2. Prioritize them in order of importance
3. When you start work tomorrow, focus only on task 1
4. Work through the list in order
5. Unfinished items move to tomorrow's list
6. Repeat daily

### The Warren Buffett Method

1. List your top 25 goals
2. Circle the top 5
3. The remaining 20 are your "avoid at all cost" list
4. Anything not in your top 5 gets zero time

---

## 12. Strategic vs. Tactical Prioritization

### Strategic Decisions

- **Timeframe**: Monthly/quarterly
- **Question**: "What should our product become?"
- **Examples**: Entering new market, changing pricing model, building new platform

**Framework for strategic**: Impact/Effort at the roadmap level

### Tactical Decisions

- **Timeframe**: Daily/weekly
- **Question**: "What should I build next?"
- **Examples**: Which feature to work on today, which bug to fix

**Framework for tactical**: RICE or ICE

### Connecting the Two

Strategic decisions set the direction; tactical decisions execute within it.

**Example**:
- Strategic: "We're going to focus on enterprise customers this quarter"
- Tactical: "Build SSO" (important to enterprise) > "Add emoji reactions" (not important to enterprise)

### The Weekly Strategy Check

Every week, ask:
1. "Does my weekly plan align with my quarterly strategy?"
2. "Am I spending time on things that matter?"
3. "What am I doing this week that doesn't serve the strategy?"

If you can't connect your weekly work to your strategy, you're in the weeds.

---

## 13. Saying No

### The Cost of Saying Yes

Every "yes" is a "no" to something else. When you say yes to:
- A feature request → You say no to a different feature
- A user's edge case → You say no to all users' core experience
- Technical debt cleanup → You say no to shipping a feature
- A partnership meeting → You say no to building

### How to Say No to Users

**The polite decline**:
"That's a great idea! We're focused on [core vision] right now, but I've added it to our feature consideration list."

**The redirect**:
"Instead of that, have you tried [workaround/existing feature]?"

**The honest truth**:
"I appreciate the suggestion. As a solo founder, I have to be very focused. I can't commit to this right now, but I'll keep it in mind for the future."

### How to Say No to Yourself

Your own ideas are the hardest to say no to:

1. **Write it down**: Put it in your idea list (don't discard it entirely)
2. **Wait a week**: If it still feels important in a week, evaluate it
3. **Apply your framework**: Score it against your current priorities
4. **Schedule it**: If it scores high, put it on the roadmap
5. **Ignore it**: If it scores low, let it go

---

## 14. Choosing the Right Framework

### Decision Tree

```
What kind of decision are you making?

Feature prioritization
  ├── Have data? → RICE
  └── Guessing? → ICE

Release planning
  └── What's in/out? → MoSCoW

Daily prioritization
  ├── Overwhelmed? → 3-Task Rule
  └── Need focus? → Ivy Lee

Saying no
  └── Need to cut scope? → MoSCoW

Bug triage
  └── Which bug to fix? → Severity × Frequency

Technical debt
  └── To refactor or not? → Impact on Users × Impact on Dev

Big picture
  └── Strategic decision? → Impact/Effort
```

### The Solo Framework

Most solo founders need just 2 frameworks:

1. **Impact/Effort**: Daily/weekly decisions (simple, intuitive)
2. **RICE**: Monthly feature prioritization (when you need more rigor)

Use these two consistently, and you'll make better decisions than 90% of solo founders who operate on intuition alone.

---

## 15. The Prioritization Manifesto

1. **Something > nothing** — Any framework is better than gut feeling
2. **Consistency > perfection** — Use the same framework consistently
3. **Data > opinion** — Score with data when possible, guess when necessary
4. **Impact is king** — Prioritize what moves the needle, not what's easy
5. **Effort matters** — A quick win beats a slow marathon
6. **Say no to most things** — Your time is your scarcest resource
7. **Strategy feeds tactics** — Weekly work should serve quarterly goals
8. **Revisit priorities** — What was important last month may not be now
9. **Protect your focus** — Once you start something, finish it
10. **Ship over perfect** — A shipped feature beats a perfectly prioritized backlog

Prioritization frameworks won't tell you the "right" answer every time. But they'll prevent you from building something that nobody wants, fixing something that isn't broken, and ignoring the work that actually matters.
