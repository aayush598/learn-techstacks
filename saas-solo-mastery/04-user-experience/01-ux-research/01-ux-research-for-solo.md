# UX Research for Solo Founders

## The Solo Founder's Research Paradox

As a solo founder, you face a unique challenge: you need user research to build something people want, but you have limited time, no dedicated UX researcher, and usually no existing user base. This guide covers lightweight, high-impact research methods that work when you're building alone.

The key insight: **something is better than nothing**. A 15-minute conversation with one real user is worth more than a month of speculation. Do not fall into the trap of feeling like you need "proper" research with large sample sizes and statistical rigor. In early-stage SaaS, qualitative insights from even 3-5 users will dramatically improve your product.

---

## 1. Lean User Research Philosophy

### The 80/20 of UX Research

Focus on the 20% of research methods that give you 80% of the insights:

| Method | Time Investment | Insight Quality | When To Use |
|--------|----------------|-----------------|-------------|
| 5-minute user interviews | Low | High | Throughout |
| Session replay analysis | Medium | Very High | Post-launch |
| Guerrilla usability testing | Medium | High | Pre-launch |
| Survey feedback | Low | Medium | At scale |
| Analytics review | Low | Medium | Ongoing |
| Competitive UX audit | Medium | Medium | Quarterly |

### The Research Spiral

Don't treat research as a one-time activity. Build a continuous research spiral:

1. **Learn** (interviews, analytics)
2. **Build** (prototype, feature)
3. **Test** (usability, feedback)
4. **Measure** (analytics, retention)
5. **Repeat**

As a solo founder, you can complete one full spiral every 1-2 weeks.

### Avoiding Research Biases

Solo founders are especially vulnerable to certain biases:

- **Confirmation bias**: You want to believe your idea is good, so you ask leading questions and interpret ambiguous feedback positively.
- **Self-selection bias**: The only people giving you feedback early on may be friends or overly enthusiastic early adopters who don't represent your target market.
- **Survivorship bias**: You only hear from users who stuck around, not those who churned.
- **False consensus bias**: You assume others think like you do.

**Counter-strategies**:
- Write interview questions in advance and stick to them
- Ask "what would make you stop using this?" to surface negatives
- Interview churned users aggressively
- Record sessions and review them later with fresh eyes

---

## 2. Lightweight User Interviews

### The 5-User Interview Strategy

Jakob Nielsen's research shows that 5 users uncover ~85% of usability problems. Here's how to run 5-user interviews as a solo founder:

**Recruiting participants**:
1. **Your existing users** (if you have any): Send a personal email asking for 15 minutes
2. **Target audience in your network**: LinkedIn, Twitter, industry Slack groups
3. **UserInterviews.com** or similar services: $50-100 per participant
4. **Cold outreach**: Find people in your target demographic on LinkedIn
5. **Intercom/Rocketlane in-app messaging**: Trigger after specific behaviors

**The interview structure** (keep to 15 minutes max):

```
0:00-2:00 - Introduction and context
  "Thanks for joining. I'm building [product]. I want to understand how you currently handle [problem]. There are no wrong answers - I'm testing the product, not you."

2:00-7:00 - Problem exploration (BEFORE showing your product)
  "Walk me through how you handled [situation] last week."
  "What's the hardest part about [problem]?"
  "What tools do you use currently? What do you hate about them?"

7:00-12:00 - Product interaction
  Share your screen and give them a task to complete in your product
  "Show me how you would [core action]."
  Do NOT help them unless they're completely stuck
  Ask "What are you thinking?" when they pause

12:00-15:00 - Wrap-up
  "If you could wave a magic wand and change one thing, what would it be?"
  "Is there anything else I should have asked about?"
  "Would you be open to a follow-up in a few weeks?"
```

**Tools for solo interviews**:
- Calendly or SavvyCal for scheduling
- Zoom or Google Meet for sessions
- Otter.ai for transcription
- A simple Notion or Google Doc for notes

### The "Micro-Interview" Technique

When you can't get 15 minutes, get 3 minutes:

- **In-app polls**: Single question with a follow-up
- **Exit-intent surveys**: "Before you go, what almost made you stay?"
- **Post-signup quick question**: "What's the one thing you want to accomplish?"
- **Support conversation mining**: Read every support ticket for UX insights

### The Churn Interview

Churned users are your best source of truth. They have nothing to lose by being brutally honest.

**Churn interview script**:
1. "When did you first realize [product] wasn't right for you?"
2. "What specific feature or experience was missing?"
3. "Where did you go instead?"
4. "What would have to change for you to come back?"
5. "Was there a specific moment when you decided to cancel?"

**Incentive**: Offer a $20-50 gift card or a free month if they return.

---

## 3. Guerrilla Usability Testing

### What Is Guerrilla Testing

Guerrilla testing means going where your target users are and asking them to try your product for 5 minutes. No lab, no recruitment firm, no scheduling.

**Where to find participants**:
- Coworking spaces
- Industry meetups and conferences
- Coffee shops near business districts
- Online communities (Reddit, Discord, Slack)
- LinkedIn direct messages
- Twitter/X polls with follow-up DMs

### Running a Guerrilla Test

**Preparation (30 minutes)**:
1. Define 3 specific tasks you want to test
2. Prepare your prototype (can be Figma, coded prototype, or even paper)
3. Write a 30-second pitch to recruit participants
4. Set up recording (QuickTime + microphone)

**The ask**:
"Hi, I'm building [product] to help [target] with [problem]. I'd love 5 minutes of your time to get your feedback. In exchange, I'll buy your coffee."

**During the test**:
1. Don't explain how the product works
2. Ask them to "think aloud"
3. Give one task at a time
4. Watch where they struggle
5. Take notes on specific moments of confusion

**After 5 people**: Stop and analyze. Fix the biggest issues. Test again.

### The Parking Lot Test

A specific guerrilla technique for SaaS:

1. Find a parking lot or area where your target demographic congregates
2. Approach with a tablet or laptop
3. Say: "I'm building a tool for [profession]. Can I show you the landing page and get your reaction?"
4. Show for 5 seconds. Ask: "What does this product do?"
5. If they can't answer in 5 seconds, your messaging needs work

---

## 4. Session Recording Analysis

### Setting Up Session Recording

Tools for solo founders:
- **PostHog** (free tier up to 1M events/month)
- **Hotjar** (free tier: 35 daily sessions)
- **FullStory** (free tier: 5,000 sessions/month)
- **Clarity** (free, unlimited)
- **OpenReplay** (open source, self-host)

**What to record**:
- Page views and click maps
- Full session replays
- Rage clicks (repeated clicking on non-interactive elements)
- Dead clicks (clicking with no response)
- Scroll depth
- Form interactions

### Analyzing Session Recordings Efficiently

As a solo founder, you don't have time to watch every session. Use this systematic approach:

**Step 1: Filter by segments**
Recordings are noise without segmentation. Watch sessions for:
- Users who signed up but didn't complete onboarding
- Users who visited the pricing page but didn't convert
- Users who churned
- Users who triggered an error

**Step 2: Watch at 2x-4x speed**
Focus on:
- Where does the mouse hesitate?
- Where does the user backtrack?
- Where does the user rage-click?
- Where does scrolling stop?

**Step 3: Create a session analysis log**

| Session ID | User Type | Key Behavior | Friction Point | Severity |
|------------|-----------|-------------|----------------|----------|
| #123 | Trial user | Clicked button 5x with no feedback | Missing loading state | Critical |
| #124 | Returning | Scrolled pricing table 3x | Pricing comparison unclear | Medium |
| #125 | New visitor | Left after 8 seconds | Hero text not clear | High |

**Step 4: Quantify patterns**
If 3 out of 10 sessions show the same issue, it's a priority. If 1 out of 10, it might be a one-off.

**Step 5: Create a 30-second highlight reel**
Most session recording tools let you create highlight reels. Watch these weekly to stay connected to user struggles.

### Key Metrics from Session Recordings

Track these weekly:
- **Average session duration**: Are users engaging or bouncing?
- **Error rate**: How often do users encounter errors?
- **Conversion funnel drop-off**: Where do users leave?
- **Feature adoption**: Which features do users actually use?
- **Time-to-value**: How long until users experience the core benefit?

---

## 5. Survey-Based Research

### When Surveys Work for Solo Founders

Surveys are useful when:
- You have 50+ active users
- You need quantitative data to validate qualitative observations
- You want to measure satisfaction (NPS, CSAT)
- You need feature prioritization input

### The Solo-Friendly Survey Stack

- **Typeform**: Beautiful, conversational surveys
- **Google Forms**: Free, no-frills
- **PostHog surveys**: Integrated with product analytics
- **Intercom**: In-app message surveys
- **Tally**: Free, modern form builder

### Survey Best Practices

**Keep it to 5 questions maximum**:
1. How would you describe [product] to a friend? (open)
2. What's the main benefit you get from [product]? (open)
3. How likely are you to recommend [product] to a colleague? (0-10 scale)
4. What's the one thing we could do better? (open)
5. Can we follow up with you? (yes/no + email)

**Survey timing**:
- **Post-signup**: "What problem are you trying to solve?" (1 question)
- **Post-first-success**: "Did [specific action] help you accomplish [goal]?"
- **Post-cancellation**: "What's the primary reason you're leaving?"
- **Monthly**: "On a scale of 1-10, how would you rate your experience?"

### The 3-Question Cancellation Survey

When a user cancels, ask:

1. "What's the main reason you're canceling?" (multiple choice)
   - Too expensive
   - Missing features
   - Too complex
   - Not solving my problem
   - Found a better alternative (which one? _____)
   - Other: _____
2. "What would have to change for you to stay?"
3. "Is there anything else you'd like us to know?"

---

## 6. Competitive UX Analysis

### Analyzing Competitor UX

You can learn a massive amount from competitors' UX without talking to a single user.

**What to analyze**:
1. **Onboarding flow**: How many steps? What info do they collect? Do they show value first?
2. **Information architecture**: How is the nav structured? Where do they put things?
3. **Pricing page**: How do they present pricing? What comparisons do they include?
4. **Error states**: What happens when things go wrong?
5. **Empty states**: What do users see when they first sign up?
6. **Mobile experience**: Is it responsive? Mobile-first?
7. **Loading states**: How do they handle loading?

**Method**:
1. Sign up for 5 competitors
2. Record your first experience with each
3. Complete key tasks in each
4. Document what felt good and what felt frustrating
5. Look for patterns across all competitors

### Learning from Complementary Products

Don't just analyze direct competitors. Look at products your target users already love.

**Questions to ask**:
- What makes Slack's onboarding so smooth?
- Why do users love Notion's flexibility (or hate it)?
- How does Calendly reduce friction in scheduling?
- What makes Stripe's developer docs so good?

Extract patterns, not features. The pattern is "reduce friction," not "copy Stripe's docs."

---

## 7. Analytics-Driven Research

### Metrics That Reveal UX Problems

| Metric | What It Reveals | UX Issue |
|--------|----------------|----------|
| High bounce rate on landing page | Value proposition not clear | Messaging/positioning issue |
| Low trial-to-paid conversion | Onboarding not driving value | Activation problem |
| High feature adoption but low retention | Feature not sticky enough | Core loop issue |
| High support ticket volume | UX confusion | Usability problem |
| Low feature discovery | Poor information architecture | Navigation issue |
| High error rate on specific page | Bugs or confusing UI | Technical UX issue |

### Setting Up Actionable Dashboards

As a solo founder, you need one dashboard, not ten.

**The Solo Founder UX Dashboard**:
1. **Acquisition**: Landing page conversion rate, top traffic sources
2. **Activation**: % of signups who complete onboarding, time-to-value
3. **Revenue**: Trial-to-paid, expansion revenue, churn
4. **Retention**: DAU/MAU, weekly active users, feature retention
5. **Referral**: NPS, referral sources, viral coefficient

**Tools**: PostHog (free tier), Plausible, Umami, or Google Analytics 4

### Behavioral Cohorts

Segment users by behavior, not demographics:

- **Power users**: Daily active, use multiple features → Study what they love
- **Core users**: Weekly active, use key features → Study what keeps them coming back
- **Casual users**: Monthly active, limited feature use → Study what's missing
- **At-risk users**: Declining activity → Study what's driving them away
- **Churned users**: Cancelled → Study where they left

For each cohort, watch 3-5 session recordings to understand their experience.

---

## 8. The Solo Research Calendar

Here's a realistic weekly research cadence for a solo founder:

**Monday (30 min)**:
- Review weekend session recordings (watch at 4x speed)
- Check support tickets for UX patterns

**Tuesday (30 min)**:
- Run 1 user interview (if you have users)
- Or: Run 1 guerrilla test session

**Wednesday (15 min)**:
- Review analytics dashboard
- Note any metric changes

**Thursday (30 min)**:
- Competitive UX review (one competitor per week)
- Update UX issue tracker

**Friday (15 min)**:
- Write UX research summary (3 bullet points)
- Decide on one UX fix for the next week

**Monthly (2 hours)**:
- Review all session recordings for the month
- Update user personas
- Run full competitive audit
- Plan next month's research focus

---

## 9. Research Documentation for Solo

### The Minimal Research Artifact

You don't need a 50-page research report. You need:

**One-page research summary**:
1. **What we learned** (3-5 bullet points)
2. **What we validated** (hypothesis confirmed/rejected)
3. **What surprised us** (unexpected insights)
4. **What to do next** (action items with priority)

**The UX issue tracker** (in your project management tool):

| Issue | Source | Severity | Effort | Status |
|-------|--------|----------|--------|--------|
| Users confused by dashboard | 3/5 sessions | Critical | 2 days | Fixed |
| Pricing unclear | Support tickets | High | 1 day | In progress |
| Mobile nav broken | Analytics | Medium | 4 hours | Backlog |

### Sharing Research Findings

As a solo founder, you're the only stakeholder. But if you have a co-founder, contractor, or early employee:

- Record a 2-minute Loom video summarizing findings
- Share the one-pager in your shared drive
- Tag the specific issue in your issue tracker
- Reference research findings in PR descriptions

---

## 10. Common Research Mistakes Solo Founders Make

### Mistake 1: Researching Instead of Building

The trap: "I need to do more research before I build anything."

The reality: Research is only valuable when it leads to action. If you've identified a clear problem and have a plausible solution, build it and test it with real users. Don't research your way into inaction.

**Fix**: Set a time limit on research. "I will do 5 interviews, then build the MVP."

### Mistake 2: Asking Leading Questions

"We built this feature that lets you collaborate in real-time. How useful would that be for your team?"

Users will say yes because they want to be helpful. Instead, ask: "Walk me through how your team currently collaborates on documents."

**Fix**: Write your questions, then ask a friend to identify leading ones. Replace them with behavioral questions.

### Mistake 3: Ignoring What You Don't Want to Hear

Your product is your baby. It's hard to hear that it's ugly. But if you ignore critical feedback, you'll build something nobody wants.

**Fix**: Thank people for critical feedback. Ask follow-up questions. Look for patterns across multiple users. If 3 people say the same thing, it's probably true.

### Mistake 4: Over-Recruiting

"I need to interview 50 users before I can draw conclusions." No. For qualitative research, 5 users per segment is usually enough. More interviews give diminishing returns.

**Fix**: Do 5 interviews, identify patterns, make changes, then test again.

### Mistake 5: Testing with Friends and Family

Friends will be nice. They'll say "it's great!" even when it's not. They won't tell you the hard truths.

**Fix**: Test with strangers who match your target demographic. Offer an incentive like a gift card or free access.

---

## 11. Tools Summary for Solo Founders

### Free / Low-Cost Research Tools

| Tool | Cost | Best For |
|------|------|----------|
| PostHog | Free tier | Session recording, analytics, surveys |
| Clarity | Free | Session recording, heatmaps |
| Calendly | Free tier | Scheduling interviews |
| Otter.ai | Free tier | Transcription |
| Typeform | Free tier | Surveys |
| Tally | Free | Forms and surveys |
| Notion | Free tier | Research repository |
| Loom | Free tier | Recording findings |
| Hotjar | Free tier | Session recording |
| Google Analytics | Free | Web analytics |

### Paid Tools Worth Considering

| Tool | Cost | Best For |
|------|------|----------|
| FullStory | $50/mo | Advanced session replay |
| UserInterviews | $50/participant | Recruiting participants |
| Maze | $25/mo | Remote unmoderated testing |
| UserTesting | $49/test | Professional usability testing |
| Dovetail | $30/mo | Research repository and analysis |

---

## 12. When to Level Up Your Research

You know it's time to invest more in research when:

1. **Churn is high and you don't know why**: You need deeper qualitative research and exit interviews
2. **You're hiring**: A dedicated UX researcher becomes viable around 5-10 team members
3. **You're expanding to a new market**: Cross-cultural research requires more rigor
4. **You have a large user base**: Quantitative research with statistical significance becomes possible
5. **You're raising Series A**: Investors want to see evidence of product-market fit and user understanding

Until then, the lightweight methods in this guide will serve you better than trying to implement enterprise-grade research practices. The goal is not perfect research—it's enough research to make better product decisions.

---

## 13. Getting Started Today

If you haven't done any user research yet, here's your first week:

**Day 1**: Install session recording (Clarity or PostHog - free, 15 minutes)
**Day 2**: Find and interview 1 user (or 1 person in your target market)
**Day 3**: Watch 3 session recordings at 2x speed
**Day 4**: Create your UX issue tracker (a simple spreadsheet or Notion page)
**Day 5**: Fix the #1 issue you found
**Day 6**: Deploy the fix
**Day 7**: Interview 1 more user about the fix

Then repeat. You now have a research practice that will serve you through all stages of your SaaS.
