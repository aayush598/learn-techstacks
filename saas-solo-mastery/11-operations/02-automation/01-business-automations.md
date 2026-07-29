# Business Automations for Solo SaaS Founders

## Why Automation Is Existential for Solo Founders

As a solo founder, you have a finite amount of time and energy. Every manual, repetitive task you do is time stolen from product development, customer acquisition, or (most importantly) rest. Automation isn't a luxury — it's a force multiplier that lets you operate like a team of five when it's just you.

The goal of automation is not to eliminate all human touch. It's to eliminate the rote work so you can focus on high-value, human-required activities: product decisions, customer conversations, strategic thinking.

## Automation Philosophy

### Automate in This Order

1. **Revenue-critical** — billing, dunning, invoicing (money is the lifeblood)
2. **Customer-facing** — onboarding, support triage, status updates (customer experience)
3. **Operational** — backups, monitoring, reporting (keeping the lights on)
4. **Administrative** — expense tracking, tax prep, calendar management (busywork)
5. **Growth** — content distribution, lead nurturing, social media (nice to have)

### The 3x Rule

Only automate a task when:
- You've done it **at least 3 times** manually
- You've documented the process (so you know exactly what to automate)
- You can estimate it will **save you at least 1 hour per month**

Don't spend 5 hours building an automation that saves you 10 minutes a month. The ROI isn't there.

### Automation Tool Stack

| Tool | Best For | Pricing | Solo Score |
|------|----------|---------|-----------|
| **Zapier** | Broad integrations, simple workflows | Free (100 tasks/mo), $19.99/mo (750 tasks) | 9/10 |
| **Make (Integromat)** | Complex workflows, data transformation | Free (1k ops/mo), $9/mo (10k ops) | 9/10 |
| **n8n** | Self-hosted, unlimited workflows, privacy | Free (self-host), $20/mo (cloud) | 8/10 |
| **GitHub Actions** | Code-related automations (CI/CD, release) | 2000 min/mo (free) | 8/10 |
| **Stripe Webhooks** | Payment event handling | Free | 10/10 |
| **PostHog Hooks** | Action-based triggers from analytics | Based on plan | 7/10 |
| **Clay** | Sales prospecting, data enrichment | Free tier limited | 6/10 |
| **Browserless/Automa** | Browser automation, scraping | Free tier limited | 6/10 |

**Recommendation:** Start with Zapier for simplicity. Move to Make when you need more complex logic. Move to n8n when you want self-hosted control and unlimited volume.

## Essential Business Automations

### 1. Client Onboarding Automation

A smooth onboarding experience sets the tone for the entire customer relationship. Automate the process so every new customer gets the same high-quality introduction, regardless of when they sign up.

**Trigger:** Stripe invoice.paid event (first payment) OR new user signs up

**Workflow (Zapier/Make):**

```
Step 1: New subscription created in Stripe
  ↓
Step 2: Create user in your app (API call)
  ↓
Step 3: Send welcome email (SendGrid/MailerLite)
  → Welcome email (immediate)
  → Account details, login link
  → Quick start guide link
  → Support contact info
  ↓
Step 4: Create user in Help Scout (Crisp/Freshdesk)
  → Pre-populate customer profile
  → Tag as "New Customer"
  ↓
Step 5: Add user to CRM (HubSpot)
  → Create contact record
  → Set lifecycle stage to "Customer"
  → Set deal stage to "Closed Won"
  ↓
Step 6: Send Slack notification to you
  → "New customer joined: {{company}} (${{amount}}/mo)"
  ↓
Step 7: Schedule check-in email (day 7)
  → "How's it going? Need help with anything?"
  ↓
Step 8: Schedule review request (day 30) — conditional on activity
  → "Loving it? Leave a review on Product Hunt/G2"
  → Only send if user has been active (check via API)
```

**Implementation for the welcome email sequence:**

```yaml
# Email sequence (SendGrid dynamic template)
Day 0 - Welcome: "Welcome to {{app_name}}! Here's your account."
  → Account details
  → Login button
  → Support email

Day 1 - Quick Start: "Get started in 5 minutes"
  → Step-by-step setup guide
  → Link to getting-started docs

Day 3 - First Value: "Here's what our customers love most"
  → Highlight key feature
  → Case study or example

Day 7 - Check-in: "How are things going?"
  → Ask for feedback
  → Offer 1:1 setup call (Calendly link)

Day 14 - Power User: "You might not know about this feature"
  → Deep-dive into advanced feature
  → Link to webinar or tutorial

Day 30 - Review Request: "Loving {{app_name}}? Share your experience"
  → G2/Capterra/Product Hunt review link
  → Referral program offer
  → Conditional: only if user is active
```

**Tools needed:** Stripe, your app (API), Zapier/Make, SendGrid, Help Scout, HubSpot, Slack

**Time saved:** 2-3 hours per week of manual setup and follow-up

### 2. Dunning Management (Failed Payment Recovery)

Failed payments are the #1 cause of involuntary churn. Automating the recovery process can recover 30-60% of failed payments.

**Trigger:** Stripe invoice.payment_failed event

**Workflow:**

```
Step 1: Payment fails
  ↓
Step 2: Immediately
  → Send email: "Payment failed — we'll retry"
  → Include payment link (Stripe Customer Portal)
  → No urgency, just informational
  ↓
Step 3: Wait 3 days, Smart Retry
  → Stripe automatically retries
  ↓
Step 4: Payment fails again (Day 3)
  → Send email: "Second attempt failed — update your card"
  → More urgent tone
  → Direct link to update payment method
  ↓
Step 5: Wait 3 days, Second Smart Retry
  ↓
Step 6: Payment fails again (Day 6)
  → Send email: "Last attempt before account suspension"
  → Warning tone
  → "Update payment method within 3 days to keep access"
  ↓
Step 7: Final Smart Retry (Day 9)
  ↓
Step 8: Payment fails (Day 9)
  → Send email: "Account suspended"
  → Access restricted
  → Include reactivation link
  → Data preserved for 30 days
  ↓
Step 9: Move user to "past_due" status in your app
  → Grace period: limited access (read-only)
  ↘
  If user updates card during grace period:
    → Invoice auto-paid
    → Access restored
    → Send email: "Payment successful — welcome back!"
  ↘
  If 30 days pass without payment:
    → Send email: "Account permanently closed"
    → Archive user data
    → Update CRM: Churned (involuntary)
```

**Smart Retry Schedule (configure in Stripe):**

| Attempt | Timing | Description |
|---------|--------|-------------|
| 1 | Immediate | Initial automatic retry |
| 2 | +3 hours | Retry |
| 3 | +1 day | Retry |
| 4 | +3 days | Retry (send email) |
| 5 | +5 days | Retry (send warning) |
| 6 | +5 days | Final retry |

**Dunning email templates:**

```markdown
Subject (Attempt 1): Quick heads up — payment didn't go through
Hey {{name}},
We tried to process your {{plan_name}} payment of {{amount}}, but it didn't go through.
No action needed right now — we'll retry automatically in a few days.
If you'd like to update your payment method, you can do so here:
[Update Payment Method →]({{customer_portal_link}})
Thanks,
{{app_name}}

Subject (Attempt 3): Action needed — payment method
Hey {{name}},
We've tried to process your {{plan_name}} payment a few times now, but it keeps failing.
To keep your account active, please update your payment method:
[Update Payment Method →]({{customer_portal_link}})
If we don't receive payment within 7 days, your account will be downgraded.
Thanks,
{{app_name}}

Subject (Final): Your account has been suspended
Hey {{name}},
Unfortunately, we were unable to process your payment after multiple attempts.
Your account has been suspended. Your data will be preserved for 30 days.
To reactivate your account, please update your payment method:
[Reactivate →]({{customer_portal_link}})
If you need help or want to discuss payment options, reply to this email.
Thanks,
{{app_name}}
```

**Tools needed:** Stripe (Smart Retries, Customer Portal), SendGrid, Zapier/Make

**Recovery impact:** 30-60% of failed payments recovered, worth 3-10% of MRR

### 3. New User/Lead Alert & Triage

Know immediately when someone signs up, especially a high-value lead, so you can engage quickly.

**Trigger:** New user signup OR trial account creation

**Workflow (simple):**

```
New user signs up →
  → Check: is this user from a target account (company domain)?
  → If yes (target): Send urgent Slack notification + classify as "Hot Lead"
  → If no: Send Slack notification (optional, less urgent)
  → Check: did user fill in company name/role?
  → Add to HubSpot CRM
  → Tag by source (Google, referral, Product Hunt, etc.)
  → If from paid channel: tag for ROI tracking
```

**Implementation in Make/Zapier:**

```javascript
// Pseudo-logic for lead triage
const lead = {
  email: user.email,
  company: user.company_domain,
  plan: user.plan,
  source: user.signup_source
};

// Check if target account
const targetDomains = ['acme.com', 'megacorp.io', 'enterprise.org'];
const isTarget = targetDomains.some(d => lead.company?.includes(d));

// Check lead quality
const hasCompanyInfo = !!lead.company;
const isPaidPlan = lead.plan !== 'free';
const isEnterpriseDomain = /\.(gov|edu)$/.test(lead.email.split('@')[1]);

const priority = isTarget ? '🔥 HIGH' : isEnterpriseDomain ? '⭐ MEDIUM' : 'ℹ️ LOW';

slack.send({
  channel: '#leads',
  text: `${priority} New signup: ${lead.email} from ${lead.company || 'unknown'}
         Plan: ${lead.plan}
         Source: ${lead.source}
         ${isTarget ? '🚨 TARGET ACCOUNT — drop what you're doing!' : ''}`
});
```

**Tools needed:** Your app (webhook), Slack, HubSpot, Zapier/Make

**Time saved:** 10-15 minutes per lead, plus faster response times

### 4. Customer Status Change Notifications

Stay informed about important changes in your customer base without checking dashboards.

**Workflows to set up:**

**Plan Change:**
```
Trigger: Stripe subscription.updated (plan change)
Action: Notify you in Slack
  → "{{company}} upgraded from Starter to Pro ($29 → $99/mo)"
  or
  → "{{company}} downgraded from Pro to Starter ($99 → $29/mo)"
```

**Cancellation Flow:**
```
Trigger: Stripe subscription.deleted (or cancellation initiated)
Actions:
  → Send cancellation confirmation email
  → Send exit survey (Typeform/Google Forms)
  → Notify you in Slack: "{{company}} cancelled {{plan}} (reason: {{reason}})"
  → Schedule reactivation offer email (day 7): "Hope to see you back"
  → Schedule re-engagement email (day 30): "We've made improvements"
  → Update HubSpot: Lifecycle stage → "Lost Customer"
  → Tag for churn analysis
```

**High Usage Alert:**
```
Trigger: API usage exceeds threshold (e.g., 80% of plan limit)
Action: Notify you in Slack
  → "{{company}} has used 80% of their API quota ({{used}}/{{limit}})"
  → Optionally: Send email to user suggesting upgrade
```

**Long-term Inactive User:**
```
Trigger: No login for 30 days
Action: Send re-engagement email sequence
  → Day 30: "We miss you — here's what's new"
  → Day 60: "Is there anything we can help with?"
  → Day 90: "Last chance — we'll archive your data"
  → Day 90+ : Archive account, send goodbye email
```

**Tools needed:** Stripe webhooks, SendGrid, Slack, HubSpot, Zapier/Make

### 5. Billing & Invoicing Automation

**Recurring Invoice Generation:**
```
Every month on the 1st:
  → Generate invoices for all active subscriptions (Stripe auto-does this)
  → Send invoice PDFs to customers (Stripe auto-does this)
  → Nothing to automate here — Stripe handles it

For manual invoicing (enterprise/annual):
  → Trigger: New annual contract signed
  → Action: Create Stripe invoice
  → Action: Send invoice email with payment link
  → Action: Set reminder for 30-day follow-up (if unpaid)
```

**Expense Categorization:**
```
Trigger: New transaction in business bank account (via Plaid/automated)
Action: Categorize in Wave/Xero
  → SaaS subscriptions → "Software & Tools"
  → Cloud hosting → "Infrastructure"
  → Contractor payments → "Contract Labor"
  → Office supplies → "Office Expenses"
  → Meals → "Meals & Entertainment"
```

**Monthly Revenue Report:**
```
Trigger: First day of month
Actions:
  → Run MRR calculation (from Stripe API)
  → Calculate: New MRR, Churn MRR, Expansion MRR
  → Calculate: Churn rate, ARPU, LTV
  → Send report to you in Slack/Email:
    📊 Monthly Revenue Report — January
    MRR: $12,450 (+5.2% from last month)
    New MRR: $1,200
    Churn MRR: -$550 (4.4% logo churn)
    Expansion MRR: $340
    ARPU: $42/customer
```

**Implementation for revenue report script (Python, run via cron/GitHub Actions):**

```python
import stripe
import os
from datetime import datetime, timedelta

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

def calculate_mrr():
    # Get all active subscriptions
    subs = stripe.Subscription.list(status='active', limit=100)
    total_mrr = 0
    for sub in subs.auto_paging_iter():
        total_mrr += sub.items.data[0].price.unit_amount * sub.quantity
    
    return total_mrr / 100  # Convert cents to dollars

def calculate_new_mrr():
    # Subscriptions created in the last 30 days
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())
    subs = stripe.Subscription.list(
        status='active',
        created={'gte': thirty_days_ago},
        limit=100
    )
    new_mrr = 0
    for sub in subs.auto_paging_iter():
        new_mrr += sub.items.data[0].price.unit_amount * sub.quantity
    return new_mrr / 100

# Format and send report
# ... (integration with Slack/Email)
```

**Tools needed:** Stripe API, Wave/Xero API, Slack, script/cron

**Time saved:** 2-3 hours per month of manual reporting

### 6. Content Distribution Automation

If you write content (blog posts, social media, newsletter), automate the distribution.

**Blog Post Published Workflow:**

```
Trigger: New blog post published (RSS feed or webhook from CMS)
Actions:
  → Post to Twitter/X (share link + excerpt)
  → Post to LinkedIn (summary + link)
  → Post to Hacker News (optional, only if high-quality)
  → Post to Reddit (relevant subreddit)
  → Add to newsletter queue (MailerLite/ConvertKit)
  → Notify in Slack: "New post published"
  → Add to sitemap (if dynamic)
  → Ping Google Search Console
```

**Social Media Content Bank:**

```
Trigger: Weekly schedule (e.g., every Monday, Wednesday, Friday)
Actions:
  → Pick from content bank (Google Sheet/Notion database)
  → Customize for each platform
  → Schedule post
  → Log post in content calendar
```

**Tools needed:** Buffer/Hootsuite (scheduling), Zapier/Make, RSS feed

### 7. Customer Support Triage

Automatically categorize and route support tickets so you know what's urgent.

**Support Workflow:**

```
Trigger: New email to support@yourdomain.com or new chat message
Actions:
  → Check for keywords → auto-tag
    "billing", "payment", "refund" → Tag: Billing → Priority: High
    "bug", "error", "crash", "broken" → Tag: Bug → Priority: High
    "feature", "suggestion", "would like" → Tag: Feature Request → Priority: Low
    "api", "integration", "webhook" → Tag: Technical → Priority: Medium
    "cancel", "delete", "close account" → Tag: At-Risk → Priority: Urgent
    "password", "login", "access" → Tag: Account → Priority: Medium
  
  → Check sender email against customer database:
    Is this a paying customer? → Priority boost
    Is this a trial user? → Standard priority
    Is this an unknown sender? → Could be spam/new lead
  
  → If Priority = Urgent:
    → Send SMS alert (via Twilio/Better Uptime)
    → Slack notification: "⚠️ URGENT: Cancellation request from {{company}}"
  
  → If Priority = High:
    → Slack notification: "Support ticket from {{sender}}: {{subject}} ({{tag}})"
  
  → For known FAQs:
    → Auto-reply with knowledge base article link
    → Tag as "Auto-replied"
  
  → For feature requests:
    → Auto-reply: "Thanks for the suggestion! We'll review it"
    → Log in Linear/issue tracker
    → Add to feature request counter
```

**SLA escalation:**

```
If response time > 4 hours for urgent tickets:
  → Alert you again in Slack
  → If > 8 hours: Send SMS

If response time > 24 hours for normal tickets:
  → Snooze reminder
  → If > 48 hours: Customer satisfaction risk alert
```

**Tools needed:** Help Scout/Crisp/Freshdesk API, Slack, Twilio (SMS), Zapier/Make

**Time saved:** 1-2 hours per week of triage and routing

### 8. Contract & Document Automation

Generate and send contracts, proposals, and legal documents without manual work.

**NDA Workflow:**

```
Trigger: New potential partner/vendor
Actions:
  → Send pre-signed NDA (via PandaDoc/Hellosign)
  → When signed: notify you + store in Google Drive
  → Add contact to CRM with tag "NDA signed"
```

**Proposal Generation:**

```
Trigger: Qualifying lead requests pricing
Actions:
  → Generate proposal from template (PandaDoc)
  → Pull company info from CRM
  → Fill in pricing from Stripe
  → Send for e-signature
  → Track: opened, time spent, signed
  → When signed: Create subscription in Stripe
```

**Tools needed:** PandaDoc/DocuSign/Hellosign, HubSpot, Zapier/Make

**Time saved:** 1-2 hours per proposal

### 9. Social Proof & Review Collection

Automate the collection of testimonials, reviews, and case studies.

**Review Request Workflow:**

```
Trigger: Customer has been active for 60+ days AND has used core features
Conditions:
  → Not already requested (check CRM)
  → Customer has >80% feature usage
  → No recent support tickets about dissatisfaction

Actions:
  → Send review request email (G2, Capterra, Product Hunt)
  → Alternative: Request testimonial (for website)
  → When review posted: Notify you in Slack
  → When testimonial received: Add to website, add to CRM
```

**Tools needed:** Email, CRM, review platforms

### 10. Security & Compliance Automation

Automate security tasks to maintain compliance without manual effort.

**SSL Certificate Monitoring:**

```
Weekly check:
  → Check SSL expiry date for all domains
  → If < 30 days: Send alert
  → If < 14 days: Urgent alert + auto-renew if possible
  → If < 7 days: SMS alert
```

**Dependency Vulnerability Scan:**

```
Schedule: Weekly (via GitHub Actions Dependabot + Snyk)
Actions:
  → Scan all dependencies
  → If critical vulnerability found:
    → Create GitHub issue
    → Send Slack alert
    → If fix available: auto-create PR
```

**Data Backup Verification:**

```
Schedule: Daily
Actions:
  → Verify last backup exists
  → Check backup file size (not empty)
  → If backup missing or empty:
    → Trigger immediate backup
    → Send alert: "Backup failed — manual intervention needed"
```

**API Key Rotation Reminder:**

```
Schedule: Quarterly
Actions:
  → Reminder: "Time to rotate API keys"
  → Check list of all keys from all services
  → Send to-do list for rotation
```

## Building Your Automation Command Center

Create a central dashboard or document that tracks all your automations:

```markdown
# Automation Registry

## Revenue (Critical)
- [x] Dunning management — Stripe + SendGrid — Active
- [x] Invoice generation — Stripe (auto) — Active
- [x] Subscription lifecycle notifications — Slack — Active

## Customer Experience (High)
- [x] New customer onboarding — Zapier sequence — Active
- [x] Support ticket triage — Help Scout + Zapier — Active
- [x] Re-engagement for inactive users — API + SendGrid — Active
- [x] Review request for happy customers — Manual trigger — Paused

## Operations (Medium)
- [x] Backup verification — Cron script — Active
- [x] SSL monitoring — Cron script — Active
- [x] Monthly revenue report — Python script — Active
- [x] Expense categorization — Wave (auto) — Active

## Growth (Low)
- [ ] Content distribution — Not built yet — Planned
- [ ] Social media scheduling — Buffer — Active
```

## Automation Anti-Patterns

### 1. Over-Automation

**Problem:** Building complex automations for tasks that happen once a quarter.

**Solution:** Apply the 3x rule. If you've only done something once, don't automate it yet. If twice, consider documenting it. If three times, automate it — but only if the automation saves significant time.

### 2. Silent Failures

**Problem:** An automation breaks and you don't notice for weeks.

**Solution:** Every critical automation should have:
- A success notification (optional, for high-value flows)
- A failure notification (mandatory for all flows)
- A weekly health check email listing all automation statuses

### 3. Bypassing Human Judgment

**Problem:** Automating responses to sensitive customer situations.

**Solution:** Never fully automate:
- Cancellation conversations (always respond personally)
- Refund decisions (especially for large amounts)
- Abuse/banned user decisions
- Enterprise negotiations
- Personal apologies for service issues

### 4. Automation Sprawl

**Problem:** 50+ automations, half of which you don't remember exist.

**Solution:** Run a quarterly automation audit:
- Delete automations you haven't updated in 6 months
- Test all critical automations end-to-end
- Document any undocumented automations
- Check if a tool update broke anything

## Automation Maturity Model

| Stage | Characteristics | Automations Running | Time Saved/Week |
|-------|-----------------|-------------------|-----------------|
| **1: Manual** | Everything done by hand | 0-3 | 0 hours |
| **2: Reactive** | Built when pain is acute | 3-8 | 2-5 hours |
| **3: Proactive** | Planned automation roadmap | 8-15 | 5-10 hours |
| **4: Optimized** | Regular audits, metrics on savings | 15-25 | 10-20 hours |
| **5: Autonomous** | Self-healing, proactive alerts | 25+ | 20+ hours |

## Sample Automation Architecture Diagram

```
                   ┌─────────────────────────────────┐
                   │     Your Application (API)       │
                   └──────────┬──────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │  Stripe │          │ HelpDesk│          │   App   │
   │  Events │          │ Tickets │          │ Webhooks│
   └────┬────┘          └────┬────┘          └────┬────┘
        │                    │                     │
        └──────────┬─────────┴──────────┬──────────┘
                   │                    │
                   ▼                    ▼
            ┌─────────────┐     ┌──────────────┐
            │    Zapier    │     │  GitHub      │
            │     /Make    │     │  Actions     │
            └─────────────┘     └──────┬───────┘
                   │                    │
        ┌──────────┼──────────┐        │
        │          │          │        │
        ▼          ▼          ▼        ▼
    ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
    │ Slack│  │Email │  │ CRM  │  │ API  │
    │ Notif│  │SendGrid│  │HubSpot│  │Calls │
    └──────┘  └──────┘  └──────┘  └──────┘
```

## Getting Started: Implementation Roadmap

### Week 1: Foundation
1. Set up Zapier/Make account
2. Connect your core tools (Stripe, Email, Slack, CRM)
3. Implement **new customer onboarding** workflow (highest impact)
4. Implement **new user alert** (immediate value)

### Week 2: Revenue Protection
1. Configure **Stripe Smart Retries**
2. Implement payment failure **email sequence**
3. Set up **subscription change alerts** to Slack

### Week 3: Customer Experience
1. Implement **support ticket triage**
2. Set up **auto-reply for FAQs**
3. Create **inactive user re-engagement** sequence

### Week 4: Operations
1. Set up **monthly revenue report**
2. Implement **backup verification**
3. Create your **Automation Registry** document

### Month 2: Optimization
1. Run your first **automation audit**
2. Identify 3 more tasks to automate using the 3x rule
3. Create **failure notifications** for all critical automations

### Month 3: Scale
1. Review automation **health metrics**
2. Consider upgrading from Zapier to Make or n8n if hitting limits
3. Build **self-service customer portal** features to reduce support load

## Resources

- [Zapier University](https://zapier.com/learn/) — Free courses on building workflows
- [Make Academy](https://www.make.com/en/academy) — Scenario building tutorials
- [n8n Templates](https://n8n.io/workflows/) — Pre-built workflow templates
- [Stripe Webhook Events](https://stripe.com/docs/api/events/types) — Complete event reference
- [Automation ROI Calculator](https://zapier.com/blog/automation-roi-calculator/)
