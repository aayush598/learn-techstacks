# Campaign Management for Outreach

## The Science of Systematic Outreach

Most freelancers do outreach sporadically: send 10 emails when they need work, get no replies, and give up. The top 1% run systematic campaigns: research, send, track, optimize, repeat.

This guide covers the infrastructure and processes to run outreach like a business.

---

## 1. CRM Setup for Freelancers

### Why You Need a CRM

A CRM (Customer Relationship Management) system tracks every interaction with every prospect. Without one, leads fall through the cracks and follow-ups are forgotten.

### CRM Options

**Free (Good for Starting):**
- **HubSpot CRM** — Free forever, contact management, deal pipeline, email tracking
- **Google Sheets** — Manual but flexible, create your own system
- **Notion** — Good for small lists (< 100 prospects)
- **Trello** — Kanban-style pipeline management

**Paid (Essential for Scaling):**
- **Pipedrive** ($15/month) — Best for sales pipelines, intuitive UI
- **Close** ($25/month) — Built for calling and sequences
- **Copper** ($25/month) — Google Workspace integration
- **HubSpot Starter** ($50/month) — Automation, sequences, analytics

### CRM Fields to Track

```
Contact Info:
  - Name
  - Company
  - Role
  - Email
  - Phone
  - LinkedIn

Company Info:
  - Industry
  - Size
  - Funding
  - Location
  - Website

Outreach Info:
  - Lead Source
  - Date Added
  - First Contact
  - Last Contact
  - Stage
  - Status

Activity:
  - Emails Sent
  - Emails Opened
  - Replies
  - Calls
  - Meetings
  - Notes

Conversion:
  - Deal Value
  - Close Date
  - Status (Won/Lost/Stalled)
```

### Pipeline Stages

```
1. Lead (identified, not contacted)
2. Contacted (first outreach sent)
3. Engaged (replied, interested)
4. Meeting Scheduled
5. Meeting Completed
6. Proposal Sent
7. Negotiation
8. Closed Won
9. Closed Lost
10. Nurture (not ready, but keep in touch)
```

### Daily CRM Workflow

```
Morning (15 min):
  - Check today's tasks
  - Review new leads
  - Plan outreach for the day

Mid-day (30 min):
  - Send emails/messages
  - Log replies
  - Move deals through pipeline

Evening (15 min):
  - Update notes
  - Schedule follow-ups
  - Review tomorrow's priorities
```

---

## 2. A/B Testing Subject Lines

### What to Test

**Subject Lines:**
- Personalization style ("[Name]" vs "[Company]" vs "Idea for...")
- Length (short vs long)
- Question vs statement
- Curiosity gap vs direct benefit
- Emoji vs no emoji

**Email Body:**
- Length (short 4 sentences vs long 8 sentences)
- Opening line style (compliment vs problem vs question)
- CTA type (call vs reply vs resource)
- Proof placement (beginning vs end)
- Personal vs professional tone

**Sending Variables:**
- Day of week
- Time of day
- Send from name
- Follow-up timing

### A/B Test Structure

**Step 1: Hypothesis**
"I believe that subject lines with curiosity gap will get higher open rates than direct benefit subject lines."

**Step 2: Split**
- Version A: "Quick question about your stack"
- Version B: "Idea to improve your page speed"

**Step 3: Sample Size**
- Minimum 50 emails per variant
- 100+ per variant for statistical significance

**Step 4: Duration**
- Run test for 5-7 days
- Or until 50+ opens per variant

**Step 5: Analyze**
- Winner = higher open rate
- Statistical significance = p < 0.05
- Use calculator: abtestguide.com

### A/B Testing Tracker

```
| Test # | Variable | Control | Variant | Opens A | Opens B | Winner |
|---|---|---|---|---|---|---|
| 1 | Subject | "[Name], quick question" | "Idea for [Company]" | 42% | 38% | A |
| 2 | Subject | "Quick question" | "Your [problem]" | 42% | 51% | B |
| 3 | Length | 4 sentences | 8 sentences | 12% reply | 8% reply | A |
```

### Common A/B Testing Mistakes

- Changing multiple variables at once (you won't know what worked)
- Not running the test long enough (small sample = unreliable)
- Stopping too early (early results fluctuate)
- Ignoring statistical significance
- Testing variables that don't matter

---

## 3. Follow-Up Automation

### The Follow-Up Sequence Structure

```
Email 1 (Day 1): Initial outreach
Email 2 (Day 3): Follow-up with value-add
Email 3 (Day 6): Case study or social proof
Email 4 (Day 10): Problem deep dive
Email 5 (Day 14): Breakup
```

### Automated vs Manual Follow-Up

**Automated Sequences (Instantly, Mailshake, Lemlist):**
- Pros: Set it and forget it, consistent timing, trackable
- Cons: Can feel impersonal, deliverability concerns
- Best for: Large lists (500+), initial outreach

**Manual Follow-Up (CRM reminders):**
- Pros: More personal, can reference previous conversation
- Cons: Time-consuming, easy to forget
- Best for: Small lists (< 100), warm leads, high-value prospects

### Hybrid Approach (Recommended)

```
Automated sequence for first 3 emails
Manual follow-up for replies and warm leads
Manual outreach for high-value (top 20%) prospects
```

### Follow-Up Email Timing

| Days Since Last Contact | Action |
|---|---|
| 0-2 | Wait for reply |
| 3 | Send follow-up email |
| 5 | LinkedIn connection request |
| 7 | Send third email |
| 10 | Engage with their content |
| 14 | Breakup email |

### Automated Follow-Up Rules

- Stop sequence on reply (immediately)
- Stop sequence on unsubscribe
- Stop sequence on bounce
- Skip weekends and holidays
- Pause during holiday seasons
- Personalize every follow-up

---

## 4. Tracking Key Metrics

### The Essential Dashboard

```
Overall Campaign:
  Leads in pipeline: 247
  Emails sent this week: 158
  Open rate: 44%
  Reply rate: 12%
  Meetings booked: 5
  Deal value: $14,200

Channel Breakdown:
  Email: 44% open, 12% reply
  LinkedIn: 52% accept, 18% reply
  Twitter: 38% open, 22% reply
  Reddit: N/A (community driven)
  Discord: N/A (community driven)
```

### Campaign Performance Metrics

| Metric | Target | Formula |
|---|---|---|
| Delivery rate | 95%+ | Delivered / Sent |
| Open rate | 40%+ | Opens / Delivered |
| Click rate | 5%+ | Clicks / Delivered |
| Reply rate | 10%+ | Replies / Delivered |
| Meeting rate | 3%+ | Meetings / Delivered |
| Close rate | 1%+ | Clients / Delivered |
| Revenue per lead | $500+ | Total revenue / Leads |

### Pipeline Health Metrics

| Metric | Target | What It Means |
|---|---|---|
| Leads added/week | 50+ | Healthy top of funnel |
| Active deals | 10-15 | Enough pipeline for consistent revenue |
| Deal velocity | 14-30 days | How fast leads convert |
| Win rate | 25%+ | Proposals → Clients |
| Pipeline coverage | 3x target | Pipeline value / Monthly target |

### Tracking Tools

- **HubSpot CRM** — Built-in dashboards and reports
- **Google Sheets** — Manual tracking with pivot tables
- **Mixpanel** — Advanced analytics
- **Databox** — Goal tracking and visualization

---

## 5. Lead Sourcing and Management

### Lead Sources to Track

```
Source 1: LinkedIn Sales Navigator — $99/month
Source 2: Apollo.io — $49/month
Source 3: Upwork (convert to direct)
Source 4: Referrals (free)
Source 5: Content marketing (free)
Source 6: Communities (free)
Source 7: Events/conferences (cost varies)
```

### Source ROI Tracking

```
| Source | Monthly Cost | Leads/mo | Clients/mo | Revenue | ROI |
|---|---|---|---|---|---|
| Apollo.io | $49 | 200 | 2 | $10,000 | 20,308% |
| Sales Nav | $99 | 100 | 1 | $5,000 | 4,950% |
| Referrals | $0 | 5 | 1 | $5,000 | Infinite |
| Content | $0 | 10 | 0.5 | $2,500 | Infinite |
```

### Lead Qualification (BANT Framework)

**Budget:** Do they have budget for your services?
**Authority:** Can they make the decision to hire you?
**Need:** Do they have a problem you can solve?
**Timeline:** When do they need it solved?

Score each on 1-5. Only pursue leads with 15+ total.

### Lead Scoring Model

```
Fit Score (0-10):
  - 3 points: Target industry
  - 3 points: Company size (11-200)
  - 2 points: Decision-maker role
  - 2 points: Has budget for services

Engagement Score (0-10):
  - 3 points: Opened email
  - 3 points: Replied to email
  - 2 points: Visited website
  - 2 points: Engaged on LinkedIn

Priority = Fit Score × Engagement Score
```

---

## 6. Campaign Optimization

### The Weekly Optimization Cycle

**Monday: Review**
- Review last week's metrics
- Identify what worked and what didn't
- Set goals for this week

**Tuesday: Research**
- Add new leads to pipeline
- Research warm leads
- Find decision-makers

**Wednesday: Send**
- Send initial outreach
- Follow up with engaged leads
- Test new subject lines

**Thursday: Engage**
- Reply to responses
- Schedule calls
- Continue sequence

**Friday: Prepare**
- Update CRM
- Prepare for next week
- Learn and document

### Campaign Adjustment Based on Data

| Issue | Likely Cause | Fix |
|---|---|---|
| Low open rate (< 30%) | Bad subject lines | A/B test new subject lines |
| Low reply rate (< 8%) | Bad email copy | Rewrite email body, improve personalization |
| High bounce rate (> 5%) | Bad data quality | Improve verification process |
| Low meeting rate (< 2%) | Weak CTA | Make CTA more compelling, offer specific value |
| No shows for meetings | Poor qualification | Better pre-call screening |
| Low close rate (< 20%) | Wrong prospects | Refine targeting criteria |

### The 10x Rule

When you find a campaign that works, 10x it:

1. Identify the winning combination (channel, message, offer)
2. Increase volume (2x, 5x, 10x more outreach)
3. Double down on what works
4. Cut what doesn't work
5. Systemize and delegate

---

## 7. Tools Stack

### Essential Tools

| Category | Tool | Cost | Purpose |
|---|---|---|---|
| CRM | HubSpot | Free | Contact management |
| Lead sourcing | Apollo.io | $49/mo | Find emails |
| Email verification | ZeroBounce | $15/mo | Verify emails |
| Email sending | Instantly | $30/mo | Send campaigns |
| Calendar | Calendly | Free | Schedule calls |
| Doc signing | DocuSign | $10/mo | Contracts |
| Invoicing | Wave | Free | Get paid |

### Nice-to-Have Tools

| Category | Tool | Cost | Purpose |
|---|---|---|---|
| LinkedIn automation | Expandi | $99/mo | Scale LinkedIn (risky) |
| Website | Carrd | $19/yr | Portfolio page |
| Booking | Cal.com | Free | Open source calendar |
| Analytics | Google Analytics | Free | Website tracking |
| Screen recording | Loom | Free | Personalized videos |
| AI copywriting | ChatGPT | $20/mo | Draft emails |

### Total Monthly Investment

```
Essential: $104/month
  - HubSpot: Free
  - Apollo.io: $49
  - ZeroBounce: $15
  - Instantly: $30
  - Calendly: Free
  - Wave: Free
  - $10 budget for misc

Nice-to-Have: $119/month
  - Expandi: $99 (if LinkedIn is primary)
  - ChatGPT: $20

Total: $104-$223/month
```

---

## 8. Compliance and Deliverability

### Sending Infrastructure

- **Separate domain** for cold outreach (not your main domain)
- **2-3 email addresses** on that domain
- **Proper SPF, DKIM, DMARC** configuration
- **Domain warmup** before mass sending

### Warmup Process

```
Week 1: 5-10 emails/day (warmup only)
Week 2: 10-20 emails/day (warmup + 5-10 cold)
Week 3: 20-30 emails/day
Week 4: 30-50 emails/day (target volume)
```

### Bounce Management

- Verify all emails before sending
- Remove bounces immediately
- Clean list every 30 days
- Keep bounce rate under 3%

### Unsubscribe Management

- Include unsubscribe link in every email
- Process unsubscribes within 24 hours
- Never email someone who unsubscribed
- Maintain suppression list

### Blacklist Monitoring

- Check domain reputation weekly
- Use mxtoolbox.com to check blacklists
- Monitor spam complaint rate
- Keep spam complaints under 0.1%

---

## 9. Scaling Beyond One Person

### When to Scale

Signs you're ready to scale:
- You have a repeatable campaign that generates consistent leads
- You're turning down work due to capacity
- You have systems documented
- You have the budget to hire

### First Hire: Outreach VA

**Cost:** $5-10/hour (overseas)
**Tasks:**
- Lead research and sourcing
- Data entry into CRM
- LinkedIn profile visits
- Basic personalization
- Scheduling

### Second Hire: SDR (Sales Development Rep)

**Cost:** $15-25/hour (overseas)
**Tasks:**
- Send initial outreach sequences
- Qualify leads
- Book meetings
- Follow up
- Manage pipeline

### Systems to Document

Before hiring, document:
1. ICP definition (who are you targeting?)
2. Lead sourcing process (where to find them)
3. Outreach sequence (what to send and when)
4. Qualification criteria (who is a good lead?)
5. CRM usage (how to track everything)
6. Reporting (what to measure)

### The Scalable Outreach Machine

```
Lead Sourcing (VA, tools)
  → List Building (Apollo, Sales Nav)
  → Verification (ZeroBounce)
  → Sequence (Instantly, HubSpot)
  → Qualification (SDR)
  → Meeting (You)
  → Close (You)
  → Delivery (You + team)
```

---

## 10. The 90-Day Campaign Plan

### Month 1: Foundation

**Week 1-2: Setup**
- Set up CRM
- Set up email infrastructure
- Define ICP
- Create first 100-lead list

**Week 3-4: Test**
- Send first campaign (100-200 emails)
- Track results
- Refine approach
- A/B test subject lines

### Month 2: Optimization

**Week 5-6: Scale**
- Increase volume to 50-100 emails/day
- Add LinkedIn outreach
- Add 200+ leads to pipeline

**Week 7-8: Refine**
- Analyze results
- Cut what doesn't work
- Double down on what works
- Start getting meetings

### Month 3: Results

**Week 9-10: Convert**
- Active pipeline management
- Focus on closing
- Nurture warm leads

**Week 11-12: Systemize**
- Document processes
- Plan for next quarter
- Set higher targets
- Consider hiring help

---

## Final Truth

Campaign management is not about sending more emails. It's about building a system that generates predictable, consistent leads.

The system should run on auto-pilot for the administrative parts, freeing you to focus on the high-value activities: personalization, conversations, and closing.

Invest in the system first. The results will follow.
