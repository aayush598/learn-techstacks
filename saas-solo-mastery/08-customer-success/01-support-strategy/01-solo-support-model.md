# Solo Support Model

## The Support Reality for Solo Founders

You are the product manager, the engineer, the salesperson, the marketer, and the support team. When a customer emails at 2am with a critical issue, it comes to you. When someone can't figure out a feature, they message you directly.

This is both a blessing and a curse.

**The blessing:** Nobody can support your product better than you. You know every line of code, every design decision, every edge case. Your customers get founder-level support, which is a competitive advantage.

**The curse:** Support is interrupt-driven, unpredictable, and scales poorly. One bad day of support can consume your entire building time.

The goal of this guide is to design a support system that works for your customers and doesn't destroy your productivity.

## The Support Philosophy

### The Solo Founder Support Principles

**1. Speed is your superpower.**
Enterprise companies have 24-48 hour response SLAs. You can respond in minutes. Use this. Fast responses make customers feel valued and reduce escalation.

**2. Be transparent about your capacity.**
"Thanks for reaching out. I'm the founder and handle support personally. I'll get back to you within [X hours]." Set expectations, then exceed them.

**3. Fix the root cause, not the symptom.**
Every support ticket is a product improvement opportunity. If you answer the same question three times, write a help article. If there's a confusing UI element, fix it.

**4. Self-service is a product feature.**
Your help docs, knowledge base, and in-app guidance are not secondary to the product. They are part of the product experience. Invest in them.

**5. Some customers aren't worth keeping.**
As a solo founder, every high-maintenance customer comes at the cost of product development. Learn to identify and gracefully exit bad-fit customers.

## The Triage System

### Priority Levels

**Critical (P0): System down, data loss, security breach**
- Response: < 1 hour | Resolution: < 4 hours | Drop everything

**High (P1): Core feature broken, major bug, billing issue**
- Response: < 4 hours | Resolution: < 24 hours | Fix within day

**Normal (P2): Feature not working as expected, question, minor bug**
- Response: < 24 hours | Resolution: < 72 hours | Support block

**Low (P3): Feature request, general question, doc unclear**
- Response: < 48 hours | Resolution: < 1 week | Batch process

### Triage Process

1. **All tickets hit one inbox** (support@yourdomain.com)
2. **First response acknowledges receipt** (automated for non-critical)
3. **Quick scan determines priority**
4. **Respond based on priority**
5. **Log the issue** to bug tracker, feature tracker, or KB gap tracker

### Triage Setup

- Set up email filters to flag keywords: "down", "broken", "error", "can't log in", "security"
- Auto-responder: "Thanks for your message. I'll respond within 24 hours."
- Blocked support time on your calendar (see below)

## Response Times

### Setting Expectations

Be honest. Under-promise and over-deliver.

**Public SLAs:**
- Critical: Within 1 hour (24/7)
- Normal: Within 24 hours (business days)
- Low: Within 48 hours (business days)

**Internal targets:**
- Critical: First response within 30 minutes
- Normal: First response within 4 hours
- Low: First response within 12 hours

### The First Response Is Everything

Even if you can't solve it immediately, acknowledge it.

"Hi [Name], thanks for reaching out. I'm sorry you're experiencing [issue]. I've looked into it and here's what I've found. I'm working on a fix and will have it resolved by [time]. In the meantime, here's a workaround: [workaround]."

## Self-Service Support

### The ROI of Self-Service

Every ticket you deflect is building time reclaimed.
- Average ticket: 5-30 minutes
- 1000 tickets/year at 15 min each = 250 hours = 6 weeks
- Reducing tickets by 50% saves 3 weeks per year

### Building Your Knowledge Base

**Minimum viable KB:**
- Getting Started Guide (5 min read)
- FAQ (10-20 common questions)
- Troubleshooting Guide (common errors)
- Video Tutorials (2-3 min each, 5-10 videos)
- API Documentation (if applicable)

**Platform options:**
- Notion (free, easy)
- Gitbook (developer-friendly, free tier)
- Helpjuice (SaaS KB)
- Intercom Articles (integrated with support)
- Crisp Knowledge Base (built into Crisp chat)

**Content strategy:**
Write one article per support ticket you've answered 3+ times. Over 6 months, this covers 80% of incoming questions.

**Article template:**
```
# [Question Title]

## What's happening
[Brief description]

## Why it happens
[Explanation of cause]

## How to fix it
[Step-by-step with screenshots]

## Related articles
[Links]
```

### In-App Guidance That Deflects Tickets

- Tooltips on confusing UI elements
- Empty states explaining what to do
- Contextual help icon linking to relevant article
- Onboarding checklist with clear steps
- Error messages that explain how to fix (not just "Error 500")

### Community Support

Let users help each other.

**Platforms:** Slack/Discord community, Discourse forum, GitHub Discussions, Subreddit

**Effort:**
- Moderate for spam (10 min/day)
- Answer unanswered questions (15 min/day)
- Recognize top contributors (5 min/week)
- Update pinned posts (30 min/month)

**Goal:** 50% of community questions answered by other members, not you.

## The Support Stack

### Stage-Based Recommendations

**Pre-revenue or < $2k MRR:**
- Email: Gmail + canned responses
- KB: Notion (free)
- No live chat yet

**$2k-$10k MRR:**
- Help Scout ($25/mo) or Crisp (free tier)
- KB: Gitbook or Helpjuice
- Loom for personalized video responses

**$10k-$50k MRR:**
- Intercom ($74/mo+) or Crisp ($25/mo)
- KB: Intercom Articles
- Basic chatbot for after-hours

**$50k+ MRR:**
- Zendesk or Intercom full suite
- Consider first support hire

### Recommended Solo Setup ($5k MRR)

1. **Crisp** (free tier): Live chat + email + basic chatbot + KB widget
2. **Notion** (free): Public knowledge base
3. **Loom** (free): Personalized video responses

Total cost: $0/month for a functional support system.

## Daily Support Workflow

### Batch, Don't Interrupt

Don't check support throughout the day. Batch it.

**Morning (9:00-9:30 AM):**
- Check overnight tickets
- Triage critical items
- Quick responses to simple questions
- Check for P0 issues

**Mid-day (12:30-1:00 PM):**
- Quick check during lunch
- Respond to urgent items
- Clear easy tickets

**End of day (4:30-5:00 PM):**
- Final triage
- Ensure nothing critical is pending
- Set auto-responder for after-hours

**Total daily support: 60-90 minutes**

### Weekly Support Rituals

**Monday:**
- Review weekend tickets
- Plan KB articles to write this week
- Check trending issues

**Friday:**
- Review support metrics
- Identify top 3 friction points
- Schedule product improvements

### Weekly Support Review Questions

1. How many tickets? By category?
2. Median response time?
3. Most common question?
4. Any tickets requiring product changes?
5. Any patterns across multiple customers?

**Action items:**
- Write KB article for most common question
- Fix UI issue causing confusion
- Add in-app tooltip
- Update onboarding copy

## Automated Responses

### Good for Automation

- Acknowledging receipt
- Setting expectations
- Immediate answers to common questions
- After-hours responses
- Status updates on known issues

### Bad for Automation

- Complex problem resolution
- Empathetic responses to upset customers
- Anything requiring judgment or context

### Response Templates

**Ticket received:**
"Thanks for reaching out! I've received your message and will respond within [timeframe]. If urgent, reply with [URGENT]."

**After-hours:**
"Thanks for your message! It's outside business hours. I'll review first thing in the morning. Business hours are [timezone times]."

**Known issue:**
"We're aware of [issue] and are actively working on a fix. Follow progress: [status page]. Apologies for the inconvenience."

**Common question (keyword detected):**
"Great question! Here's an article that covers this: [link]. If this doesn't fully answer your question, let me know."

### Simple Chatbot Logic

1. User sends message
2. Bot: "Hi! How can I help?"
3. User types question
4. Bot: "Here's an article: [link]. Did this help?"
5. If yes: "Great! Need more help? Email support@"
6. If no: "I'll pass this to our team. They'll respond by [time]."

A simple keyword-to-article matcher handles 30-50% of questions.

## Support Metrics

### What to Measure

**Volume:**
- Tickets per week/month
- Tickets by category (bug, question, feature request)
- Tickets per active user (ratio should decrease)

**Quality:**
- First response time (median)
- Resolution time (median)
- Customer satisfaction (CSAT)
- Touchpoints to resolution (target 1-3)

**Efficiency:**
- Self-service rate (% resolved without ticket)
- Knowledge base usage and helpfulness rating
- Ticket deflection rate

### Measuring CSAT

After each ticket resolution, send one question:

"How satisfied were you with the support you received?"

Rating 1-5, optional comment.

**Target:** Average CSAT of 4.5+ out of 5.

**If CSAT dips below 4.0:**
- Review recent tickets for patterns
- Check if response time increased
- Check if you're rushing due to volume

## Handling Support Volume Spikes

### Planning for Growth

Support volume grows with user base.
- 100 active users: ~10 tickets/week
- 1,000 active users: ~100 tickets/week

At 100 tickets/week, you need:
- Strong triage system
- Robust self-service
- Automation for common questions
- ~2-3 hours/day on support

### When to Consider Hiring

- Support takes > 3 hours/day consistently
- You're sacrificing building time
- Response times are slipping
- CSAT is declining

### First Support Hire

**Model:** Part-time contractor (10-20 hours/week)
**Cost:** $500-$2,000/month depending on location
**Hire for:** Communication skills, empathy, product curiosity
**Train them on:**
- Your product (have them use it for a week)
- Your triage system
- Your KB and response templates
- When to escalate to you

## Protecting Your Focus

### The Support Toggle

When you need deep work (building features, fixing bugs), you need to not be interrupted.

**Techniques:**
- Set Slack/chat status to "Building - will respond to support at [time]"
- Use Crisp/Intercom's "away" mode
- Auto-responder: "I'm currently focused on building. For urgent issues, email support@ with [URGENT]. I'll respond by [time]."
- Close support tab during deep work blocks

### The "Support First" Day

Some days, support is overwhelming. Instead of fighting it, dedicate the day to support.

**Support day activities:**
- Respond to all pending tickets
- Write KB articles for common issues
- Fix quick UI bugs that cause confusion
- Update onboarding and documentation
- Review and improve support workflow

This turns a bad support day into a productive one.

### Monthly Support Audit

Review:
1. Top 10 most common support questions
2. How many could be prevented with product changes?
3. How many could be prevented with better docs?
4. What's the ROI of each fix?

**Categories fixes into:**
- Quick wins (< 2 hours): Do immediately
- Medium projects (2-8 hours): Schedule this month
- Large projects (8+ hours): Add to product roadmap

## Conclusion

Customer support as a solo founder is not about answering every email instantly. It's about designing a system that:
1. Routes critical issues to you immediately
2. Deflects common questions through self-service
3. Protects your deep work time
4. Uses support data to improve the product

The best support system makes customers feel cared for without consuming all your time. Build that system early, and it will scale with you.
