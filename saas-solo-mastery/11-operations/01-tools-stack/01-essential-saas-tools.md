# Essential SaaS Tools for Solo Founders

## Overview

Running a SaaS business as a solo founder means you wear every hat — product, engineering, marketing, sales, support, finance, and legal. The right tool stack is the difference between sustainable growth and burnout. This guide covers the complete tool ecosystem for a solo SaaS founder, organized by operational category, with cost-conscious recommendations that scale with you.

## Philosophy: Tool Minimalism for Solo Founders

Before diving into specific tools, adopt these principles:

- **One tool per category** — resist the urge to stack multiple tools doing the same thing
- **Free tier first** — almost every SaaS tool has a generous free tier for small operations
- **Pay only when it hurts** — upgrade only when the free tier becomes a bottleneck
- **Integration-friendly** — every tool you pick should play nice with Zapier/Make
- **Low switching cost** — avoid tools with proprietary formats or expensive migration paths
- **Time to value under 30 minutes** — if setup takes longer than that, find an alternative

## Project Management

### Recommended: Linear (free tier: up to 10 team members)

Linear is purpose-built for software teams. Its keyboard-first design, real-time collaboration, and speed make it ideal for a solo founder who thinks in terms of cycles and sprints.

**Free tier limits:**
- Up to 10 team members
- Unlimited issues and projects
- Roadmap view
- Cycles (sprints)
- Integrations with GitHub, GitLab, Slack, Sentry

**Key features for solo founders:**
- Very fast UI — no lag, which matters when you context-switch
- Triage workflow — auto-categorizes incoming issues
- View filtering by assignee, label, priority, status
- API for automation

**Setup for solo:**
- Create projects for each major initiative (e.g., "Q2 Growth", "Infrastructure", "Customer Requests")
- Use labels for categorization: `bug`, `feature`, `customer-request`, `chore`, `improvement`
- Set up cycles (2-week sprints) even if you're solo — they force scope discipline
- Connect GitHub repo — commits and PRs auto-link to issues

**Alternatives:**
- **Notion** (better for all-in-one docs + PM, free for individuals)
- **Todoist** (lighter, personal task management, great for daily todos)
- **Plane** (open source Linear alternative, self-hostable)
- **GitHub Projects** (free, integrated with your code, but limited)

### When to upgrade to paid Linear ($8/mo per user):
- You need multiple cycles running in parallel
- You want advanced roadmaps with dependencies
- You hit the 10-user limit (add a contractor or early hire)

### Daily Task Management (complementary)

**Recommended: Todoist (free tier)**

- Capture tasks throughout the day
- Set up recurring tasks for weekly ops (billing review, backup check, metrics review)
- Integrate with Linear — don't duplicate, use Todoist for personal tasks and Linear for product work

## Code Hosting & CI/CD

### Code Hosting: GitHub (free tier)

GitHub is the de facto standard. The free tier includes unlimited public/private repositories, GitHub Actions (2000 minutes/month), GitHub Pages, and community features.

**Essential GitHub setup for solo founders:**

```
Repository Structure:
/
├── .github/
│   ├── workflows/        # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/   # Standardized bug reports
│   └── CODEOWNERS        # Auto-assignment
├── docs/                 # Public documentation
├── src/                  # Application code
├── tests/                # Test suite
├── scripts/              # Automation scripts
└── infrastructure/       # Terraform, Docker, k8s configs
```

**Key features to leverage:**
- **GitHub Actions** — CI/CD, automated testing, deployment (2000 free minutes/month is often enough for a solo operation)
- **Dependabot** — automatic dependency vulnerability scanning and PR creation
- **Code scanning** — free for public repos, GitHub Advanced Security for private (paid)
- **GitHub Pages** — host your documentation site for free
- **GitHub Discussions** — community Q&A, feature requests (better than separate forum tool)
- **GitHub Projects** — lightweight project board if you don't need Linear

**Pro tips:**
- Use conventional commits (`feat:`, `fix:`, `chore:`) for auto-changelog generation
- Set up branch protection rules on `main` even as a solo — it prevents accidental pushes
- Use GitHub Templates for issue and PR descriptions
- Enable GitHub Sponsors on your repo if it's open source

**Alternatives:**
- **GitLab** (free self-hosted option, better CI/CD, but more overhead)
- **SourceHut** (minimalist, ethical, paid but cheap)
- **Codeberg** (fOSS-focused, free)

### CI/CD: GitHub Actions (free)

As a solo founder, you need automation for:

1. **Test on every PR** — run test suite, linting, type checking
2. **Deploy on merge to main** — automated staging and production deploys
3. **Dependency updates** — Dependabot creates PRs for outdated packages
4. **Daily backups** — scheduled action for database and file backups
5. **Scheduled tasks** — cron jobs for maintenance, cleanup, reporting
6. **Security scanning** — dependency vulnerability checks

**Sample minimal workflow:**

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

**When to upgrade:** If you exceed 2000 minutes/month, consider:
- Self-hosting a runner on a cheap VPS ($5-10/mo)
- Switching to GitLab CI (unlimited minutes for public repos)
- Optimizing your workflows (cache dependencies, skip CI for docs-only changes)

## Monitoring & Observability

### Application Monitoring: Sentry (free tier)

Sentry is the gold standard for error tracking. The free tier (5k events/month, 1 user) is enough for early-stage SaaS.

**Essential setup:**
```javascript
// Frontend: Initialize with performance monitoring
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,  // 10% sampling in production
  release: process.env.RELEASE_VERSION,
  integrations: [new Sentry.BrowserTracing()],
});
```

```javascript
// Backend: Capture server-side errors
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  release: process.env.RELEASE_VERSION,
});

// Manually capture specific failures
app.use((err, req, res, next) => {
  Sentry.captureException(err);
  res.status(500).json({ error: 'Internal server error' });
});
```

**Key things to monitor as a solo founder:**
- **Error rate by endpoint** — which API routes fail most
- **Crash-free rate** — percentage of users unaffected by crashes
- **Performance (Apdex)** — is your app slow for users?
- **Breadcrumbs** — user actions leading to errors
- **Releases** — did the latest deploy introduce regressions?

**Pro tips:**
- Tag events with `user_id`, `plan_type`, `version` for filtering
- Set up alerts for critical errors only (don't alert on every 404)
- Use beforeSend to filter out noise (bots, test accounts)
- Monitor error rate changes after each deploy

**Free tier alternatives:**
- **Rollbar** (5k events/month)
- **Bugsnag** (2k events/month)
- **Highlight.io** (open source, generous free tier)
- **GlitchTip** (self-hosted Sentry alternative)

### Uptime Monitoring: Better Uptime (free tier)

Better Uptime provides uptime monitoring, status pages, and on-call scheduling. Free tier includes 10 monitors, 3 status page subscribers, email/SMS alerts.

**What to monitor:**
- Your main application URL
- API endpoint health checks (`GET /health`)
- Database connection health
- Critical third-party integrations (Stripe, SendGrid, etc.)
- SSL certificate expiry

**Setup checklist:**
1. Add 5-minute interval checks for your main app and API
2. Create a public status page (builds trust with customers)
3. Set up email/SMS alerts for downtime
4. Configure confirmation windows (don't alert on single failure — wait 2-3 retries)
5. Add SSL expiry monitoring (30-day warning)

**Pro tips:**
- Monitor synthetic transactions (login flow, checkout flow) not just static pages
- Set up maintenance windows in your status page for planned downtime
- Include the status page URL in your app footer

**Alternatives:**
- **Pingdom** (more features, less generous free tier)
- **Uptime Robot** (50 monitors on free tier, no status page)
- **Checkly** (browser monitoring, generous free tier)
- **Open status page** (self-hosted, free)

### Server Infrastructure: Grafana + Prometheus (self-hosted/free)

For more detailed infrastructure monitoring, run Grafana and Prometheus on your server:

```yaml
# docker-compose.yml for monitoring stack
version: '3'
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=changeme
    volumes:
      - grafana-data:/var/lib/grafana
```

## Analytics

### Product Analytics: PostHog (free tier: 1M events/month)

PostHog is an all-in-one product analytics suite that includes:
- Event tracking and user journeys
- Session recording (5k recordings/month on free tier)
- Feature flags (unlimited)
- A/B testing
- Heatmaps (1M events/month)
- Surveys (unlimited)

**Why PostHog over alternatives:**
- Generous free tier for solo founders
- Self-hostable (if you have privacy concerns or compliance needs)
- Combined analytics + feature flags + session recording — replaces multiple tools
- Open source core
- No cookie consent needed for self-hosted version

**Essential events to track:**

```javascript
// User lifecycle
posthog.identify(user.id, { email: user.email, plan: user.plan });
posthog.capture('user_signed_up', { source: 'google_ads', plan: 'starter' });
posthog.capture('user_upgraded', { from_plan: 'free', to_plan: 'pro' });
posthog.capture('user_cancelled', { reason: 'too_expensive', days_active: 30 });
posthog.capture('user_churned', { plan: 'pro', lifetime_value: 240 });

// Feature usage
posthog.capture('feature_used', { feature: 'export_csv', count: 100 });
posthog.capture('feature_used', { feature: 'api_call', endpoint: '/v1/analyze' });
posthog.capture('dashboard_created', { template: 'default' });
posthog.capture('integration_connected', { service: 'slack' });

// Funnel events
posthog.capture('started_onboarding');
posthog.capture('completed_onboarding');
posthog.capture('invited_team_member');
posthog.capture('first_payment');
```

**Key reports to set up:**
1. **Activation funnel** — signup → setup → first value → paid conversion
2. **Retention cohort** — weekly/monthly retention by signup cohort
3. **Feature adoption** — percentage of users using each feature
4. **Stickiness** — DAU/MAU ratio (target >20%)
5. **Revenue tracking** — MRR, ARPU, LTV by acquisition channel

**Pro tips:**
- Create dashboards for different personas (yourself, investors, advisor)
- Set up alerts for metric drops (e.g., signups drop >20% in a day)
- Use session recordings to understand user struggles (limit to 1% sampling)
- A/B test pricing page changes using PostHog feature flags

**Free tier alternatives:**
- **Plausible** (simple, privacy-focused, 1k monthly pageviews free)
- **Umami** (self-hosted, free, privacy-focused)
- **Matomo** (self-hosted, full-featured, free)
- **Fathom** (privacy-focused, paid but reasonable)

### Website Analytics: Plausible (free trial)

For basic website traffic analytics, Plausible is lightweight, privacy-compliant, and dead simple:

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

**Why use Plausible alongside PostHog:**
- PostHog tracks user behavior inside your app
- Plausible tracks marketing website visitors (anonymous, no cookie banner needed)
- Clean separation between marketing analytics and product analytics

## CRM & Sales

### CRM: Pipedrive (free tier: limited) or HubSpot (free tier: generous)

**For simple sales tracking: HubSpot Free CRM**

HubSpot's free CRM includes:
- Contact management (unlimited)
- Deal pipeline tracking
- Meeting scheduling
- Email tracking (limited)
- Live chat
- Basic reporting

**Essential CRM setup for solo founders:**

```
Pipeline Stages:
1. Lead (inbound) / Cold (outbound)
2. Qualified (fit + budget confirmed)
3. Demo Scheduled
4. Demo Completed
5. Proposal Sent
6. Negotiation
7. Closed Won / Closed Lost
```

**What to track per deal:**
- Company name and size
- Decision maker contact info
- Source (Google, referral, Product Hunt, etc.)
- Estimated deal value
- Probability of close
- Pain points identified
- Competitors considered
- Objections raised
- Next follow-up date

**Pro tips for solo founders:**
- Automate lead capture from website (HubSpot forms are free)
- Set up email templates for common responses
- Use meeting scheduling link (HubSpot Meetings) — eliminates back-and-forth
- Track all communication in the contact timeline
- Review pipeline weekly (15-minute Friday session)

**Alternatives:**
- **Pipedrive** (sales-focused, great UI, paid)
- **Copper** (Google Workspace integration, paid)
- **Salesforce** (too heavy for solo, expensive)
- **Less Annoying CRM** ($15/user/month, simple and effective)
- **Battlesnake Stacks** (ATS-focused)

### Customer Communication: Intercom (free tier: limited) or Crisp (free tier: generous)

**Recommended: Crisp (free tier)**

Crisp offers:
- Live chat (unlimited)
- Shared inbox (unlimited)
- Knowledge base (basic)
- Chatbot (limited)
- Email integration

**Free tier vs paid:**

| Feature | Free | Paid ($25/mo) |
|---------|------|---------------|
| Conversations | Unlimited | Unlimited |
| Team members | 2 | Unlimited |
| Knowledge base | Limited articles | Unlimited articles |
| Chatbot | Basic | Advanced rules |
| CRM | Limited | Full |
| Analytics | Basic | Advanced |

**Alternatives:**
- **Intercom** (best but expensive — $74/mo)
- **Freshdesk Messaging** (free for up to 10 agents)
- **Tidio** (generous free tier, good for e-commerce)
- **LiveChat** ($20/mo starting)

## Email & Communications

### Transactional Email: SendGrid (free tier: 100 emails/day)

SendGrid is the standard for transactional email delivery (password resets, invoices, notifications).

**Important: Use a dedicated subdomain for sending.**

```
send.yourdomain.com — used for all transactional emails
Authentication records:
- SPF record: v=spf1 include:sendgrid.net ~all
- DKIM record: auto-generated by SendGrid
- DMARC record: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

**Email templates to create:**
1. Welcome email (day 1)
2. Password reset
3. Payment confirmation/receipt
4. Subscription renewal notice
5. Payment failure notification
6. Account cancellation confirmation
7. Feature announcement (monthly)
8. Inactivity re-engagement (day 30, 60, 90)

**Sample transactional email flow:**

```
User signs up →
  → Welcome email (immediate)
  → Product tour (24h later, if not activated)
  → Value milestone email (when they complete key action)
  → Feedback request (day 7)
  → Upgrade nudge (day 14, if still on free plan)
  → Re-engagement (day 30, if inactive)
```

**Pro tips:**
- Warm up your sending domain before sending bulk (start with 10-20/day, increase gradually)
- Monitor delivery rates, open rates, spam complaints
- Set up webhook notifications for bounces and complaints
- Use dynamic templates for personalized content
- Always include unsubscribe link (CAN-SPAM compliance)

**When to upgrade:** $19.95/month for 50k emails/month

**Alternatives:**
- **Amazon SES** ($0.10 per 1000 emails, cheapest at scale)
- **Postmark** (best deliverability, $10 for 10k emails)
- **Resend** (modern, developer-friendly, free tier: 100 emails/day)
- **Mailgun** (flexible API, free tier: 5k emails/month for 3 months)

### Marketing Email: MailerLite (free tier: 1k subscribers)

For newsletters, drip campaigns, and marketing emails:

**Free tier:**
- Up to 1,000 subscribers
- 12,000 emails/month
- Basic automation
- Landing pages
- Signup forms

**Essential email sequences to build:**

**Onboarding sequence (5 emails):**
1. Welcome + what to expect
2. Quick start guide (3 steps to first value)
3. Advanced feature highlight
4. Best practices from power users
5. Case study / social proof + upgrade offer

**Re-engagement sequence (3 emails):**
1. "We miss you" + what's new
2. "Is there anything we can help with?"
3. "Last chance" + discount offer (optional)

**Monthly newsletter:**
- Product updates and new features
- Tips and best practices
- Customer spotlight or case study
- Industry news and insights

**Pro tips:**
- Segment subscribers by plan, activity level, interests
- A/B test subject lines (MailerLite has free A/B testing)
- Clean your list quarterly (remove hard bounces, inactive subscribers)
- Set up Google Analytics integration for click tracking
- Always have a welcome automation ready

**Alternatives:**
- **ConvertKit** (creator-focused, free up to 1k subscribers)
- **Buttondown** (minimalist, $9/month up to 1k subscribers)
- **Listmonk** (self-hosted, free, powerful)
- **Loops** (developer-friendly, clean UI)

### Business Email: Google Workspace ($6/user/month)

Custom domain email is non-negotiable for professional credibility.

**Minimum setup:**
```
you@yourdomain.com
support@yourdomain.com
billing@yourdomain.com
team@yourdomain.com (if you have a co-founder or help)
```

**Pro tips:**
- Set up email aliases for different functions (sales@, hello@, jobs@) that all route to your inbox
- Use catch-all address (then filter out spam)
- Set up vacation auto-responder for time off
- Configure SPF, DKIM, DMARC for deliverability

**Cheaper alternative:**
- **Zoho Mail** (free for 5 users, 5GB each)
- **ProtonMail** (privacy-focused, paid)
- **MXRoute** ($15/year for unlimited domains/mailboxes)

## Customer Support

### Help Desk: Help Scout (free tier: 2 users, limited)

Help Scout is purpose-built for customer support with a shared inbox, knowledge base, and reports.

**Free tier limits:**
- 2 users (you + a contractor)
- Limited reports
- Email-only (no chat or phone)

**Essential setup for solo founders:**

```
Mailboxes:
├── Support (support@yourdomain.com)
├── Billing (billing@yourdomain.com)
└── Sales (sales@yourdomain.com) — optional, combine with support at first

Workflows:
├── Auto-reply to common questions (FAQ-based)
├── Tag by category (bug, feature request, billing, account)
├── Assign to yourself automatically
└── Send satisfaction survey after resolution
```

**Knowledge base structure:**
```
Getting Started
├── Quick start guide
├── Account setup
└── Team management
Tutorials
├── Feature A deep dive
├── Feature B workflows
└── API integration guide
Troubleshooting
├── Common errors
├── Known issues
└── How to report a bug
Billing
├── Plans and pricing
├── How to upgrade/downgrade
└── Refund policy
```

**Pro tips:**
- Set up saved replies for common answers (saves hours)
- Use collision detection to avoid duplicate responses
- Track response time and CSAT (customer satisfaction score)
- Integrate with your app (link to user account, show plan and activity)

**Alternatives:**
- **Freshdesk** (forever free for up to 10 agents)
- **Zendesk** (the standard, expensive — $55/mo/agent)
- **FreeScout** (self-hosted, free, Help Scout alternative)
- **Papercups** (open source, self-hostable)

### Knowledge Base & Docs

**Recommended: GitBook or Docusaurus (free)**

- **GitBook** — hosted, beautiful, free for public docs, integrates with GitHub
- **Docusaurus** — open source, static site generator, host on GitHub Pages or Vercel (free)
- **Notion** — quick and dirty, free for individuals, limited customization

**Documentation structure:**
```
/docs
├── index.md (welcome, overview)
├── getting-started/
│   ├── quickstart.md
│   ├── installation.md
│   └── first-project.md
├── guides/
│   ├── feature-a.md
│   ├── feature-b.md
│   └── best-practices.md
├── api/
│   ├── overview.md
│   ├── authentication.md
│   ├── endpoints.md
│   └── errors.md
├── integrations/
│   ├── slack.md
│   ├── zapier.md
│   └── webhooks.md
├── troubleshooting/
│   ├── common-errors.md
│   └── faq.md
└── changelog.md
```

## Finance & Accounting

### Accounting: Wave (free) or Xero (paid)

**Recommended for solo: Wave (free)**

Wave offers free:
- Invoicing (unlimited)
- Accounting (income/expense tracking)
- Receipt scanning
- Bank connections

**Paid add-ons:**
- Payment processing (2.9% + 30¢ per transaction)
- Payroll ($20/month + per employee)

**Essential accounting setup:**
1. Connect your business bank account and credit cards
2. Categorize expenses (SaaS subscriptions, contractor payments, hosting, marketing)
3. Set up recurring invoices for subscription customers
4. Create expense categories for tax deductions
5. Run monthly P&L statement
6. Track receipts digitally (IRS requires documentation for deductions)

**When to upgrade:** When you need inventory management, project profitability, or multi-currency — switch to Xero ($13/month)

**Alternatives:**
- **Xero** (better for growing SaaS, $13/month)
- **QuickBooks Self-Employed** ($15/month, good for solo)
- **FreshBooks** (freelancer-friendly, $17/month)
- **Ledger** (command-line accounting, free, high learning curve)

### Payment Processing: Stripe (standard: 2.9% + 30¢)

Stripe is the default for SaaS payment processing.

**Essential Stripe setup:**

```javascript
// Subscription setup
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Create a customer
const customer = await stripe.customers.create({
  email: user.email,
  metadata: { internal_user_id: user.id }
});

// Create a subscription
const subscription = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: process.env.STRIPE_PRICE_PRO_MONTHLY }],
  payment_behavior: 'default_incomplete',
  expand: ['latest_invoice.payment_intent'],
  metadata: { user_id: user.id }
});
```

**Key Stripe features for solo founders:**
- **Invoicing** — generate professional invoices automatically
- **Customer Portal** — let users manage their own subscriptions (saves support time)
- **Test mode** — full sandbox environment
- **Webhooks** — listen for subscription events: `invoice.paid`, `invoice.payment_failed`, `customer.subscription.deleted`
- **Tax** — automatic tax calculation (for US, EU VAT, GST)
- **Billing** — metered billing, usage-based pricing
- **Connect** — marketplace payments (if you build a platform)

**Pro tips:**
- Handle payment failures gracefully — retry with smart retries (3, 5, 10 days)
- Send dunning emails before subscription cancellation
- Monitor MRR, churn, and failed payments daily
- Store Stripe customer ID in your database as soon as it's created
- Webhook endpoints must return 200 quickly — use a queue for processing

### Subscription Analytics: Baremetrics (paid) or takehome (free)

**Free option: Build your own with PostHog or Metabase**

Simple MRR dashboard SQL query concept:

```sql
SELECT
  DATE_TRUNC('month', created_at) as month,
  COUNT(CASE WHEN action = 'new_subscription' THEN 1 END) as new_subs,
  COUNT(CASE WHEN action = 'cancellation' THEN 1 END) as cancellations,
  SUM(CASE WHEN action = 'new_subscription' THEN mrr ELSE 0 END) as new_mrr,
  SUM(CASE WHEN action = 'upgrade' THEN mrr_change ELSE 0 END) as expansion_mrr,
  SUM(CASE WHEN action = 'downgrade' THEN mrr_change ELSE 0 END) as contraction_mrr,
  SUM(CASE WHEN action = 'cancellation' THEN -mrr ELSE 0 END) as churned_mrr
FROM subscription_events
GROUP BY 1
ORDER BY 1;
```

**Paid alternative: Baremetrics ($79/month)** — connects to Stripe and gives you MRR, ARR, LTV, churn, cohort analysis, and forecasting.

## Communication & Collaboration

### Team Chat: Discord (free) or Slack (free tier)

**Recommended for solo: Discord (free)**

- Unlimited message history (Slack free tier only shows last 90 days)
- Voice channels
- Thread support
- Community features if you have a user community

**Slack alternative:** If you need professional customer-facing communication, use Slack. The free tier has 90-day message history, 10 app integrations, and 1:1 calls.

### Video Conferencing: Google Meet (free)

Google Meet is free, integrates with Google Calendar, and doesn't require any app download for participants. It handles up to 60 minutes per meeting (free).

**Alternatives:**
- **Zoom** (40-minute limit on free, $15.99/mo for unlimited)
- **Whereby** (free for 1:1, $6.99/mo for group)
- **Calendly** (free tier) — essential for scheduling demos without email ping-pong

### Document Collaboration: Google Workspace or Notion

**Recommended: Notion (free for personal use)**

Notion serves as wiki, docs, and lightweight project management. As a solo founder, use Notion for:
- Business plan and strategy docs
- Meeting notes
- Product roadmap (high-level view)
- Customer research notes
- Standard operating procedures (SOPs)
- Financial tracking (simple spreadsheets)

**Essential Notion pages for solo:**

```
Workspace Structure:
├── Dashboard (links to key pages, metrics snapshot)
├── Strategy/
│   ├── Business Plan
│   ├── Competitive Analysis
│   ├── Pricing Strategy
│   └── OKRs & Goals
├── Product/
│   ├── Roadmap
│   ├── Feature Requests (linked from Linear)
│   ├── User Research Notes
│   └── Product Specs
├── Operations/
│   ├── SOPs
│   ├── Tool Inventory
│   ├── Password Management
│   └── Backup Procedures
├── Marketing/
│   ├── Content Calendar
│   ├── SEO Keywords
│   ├── Launch Checklist
│   └── Ad Performance
├── Finance/
│   ├── Revenue Tracking
│   ├── Expense Tracking
│   ├── Tax Documents
│   └── Budget
└── Customers/
    ├── VIP Customers
    ├── Feedback Log
    └── Case Studies
```

## Security & Password Management

### Password Manager: Bitwarden (free)

Bitwarden is open source, has unlimited password storage on the free tier, and works across all devices.

**What to store:**
- All SaaS tool credentials
- API keys and secrets
- Database passwords
- Cloud provider keys
- SSL certificate management
- Two-factor recovery codes

**Pro tips:**
- Use Bitwarden's password generator for every new account
- Store API keys in Bitwarden notes (not in code)
- Share vault items with contractors (Bitwarden Send)
- Enable 2FA on your Bitwarden account itself
- Export your vault quarterly and store encrypted backup

### VPN: Mullvad ($5/month)

If you work from coffee shops or co-working spaces, use a VPN. Mullvad is privacy-focused, accepts anonymous payments, and is recommended by security experts.

## Backup & Disaster Recovery

### Code Backup: Git (automatic via GitHub)

Your code is already backed up via GitHub. But don't forget:

### Database Backup: pg_dump to S3 (automated)

```bash
#!/bin/bash
# Backup PostgreSQL database to S3
BACKUP_FILE="backup-$(date +%Y%m%d-%H%M%S).sql.gz"
pg_dump $DATABASE_URL | gzip > /tmp/$BACKUP_FILE
aws s3 cp /tmp/$BACKUP_FILE s3://your-backup-bucket/database/
echo "Backup complete: $BACKUP_FILE"
```

**Cron job:** Run daily, keep 30 days of backups

### File Backup: Rclone + Backblaze B2

For user-uploaded files, media, and other assets:
```bash
# Sync to Backblaze B2 daily
rclone sync /data/uploads b2:your-backup-bucket/uploads/ --progress
```

## Tool Stack Summary Table

| Category | Primary Tool | Free Tier | Upgrade Cost | Upgrade Trigger |
|----------|-------------|-----------|-------------|----------------|
| Project Management | Linear | 10 users | $8/user/mo | Need advanced workflows |
| Code Hosting | GitHub | Unlimited repos | $4/mo (Pro) | Need advanced code scanning |
| CI/CD | GitHub Actions | 2000 min/mo | $4/mo (Pro) | Exceed free minutes |
| Error Monitoring | Sentry | 5k events/mo | $26/mo | Exceed event quota |
| Uptime Monitoring | Better Uptime | 10 monitors | $20/mo | Need advanced alerts |
| Product Analytics | PostHog | 1M events/mo | $30/mo | Exceed event quota |
| Website Analytics | Plausible | 1k pageviews/mo | $9/mo | Exceed pageview quota |
| CRM | HubSpot Free | Unlimited | $45/mo (Starter) | Need automation |
| Live Chat | Crisp | Unlimited convos | $25/mo | Need advanced routing |
| Transactional Email | SendGrid | 100/day | $19.95/mo | Exceed daily limit |
| Marketing Email | MailerLite | 1k subscribers | $10/mo | Exceed subscriber limit |
| Business Email | Google Workspace | — | $6/user/mo | Always needed |
| Help Desk | Help Scout | 2 users | $25/mo | Need tickets/automation |
| Accounting | Wave | Free | Add-ons | Need payroll |
| Payment Processing | Stripe | Free to start | 2.9%+30¢ | First transaction |
| Password Manager | Bitwarden | Free | $10/year | Need TOTP/attachments |
| Backup | Scripts + S3 | S3 free tier | Usage-based | As data grows |

## Monthly Tool Cost by Stage

| Stage | Monthly Cost | Notes |
|-------|-------------|-------|
| Pre-launch / Idea | $6 | Only Google Workspace |
| MVP / Beta | $11 | GW + one paid tool (e.g., Sentry) |
| First 10 customers | $25-40 | Maybe upgrade email or add analytics |
| 50-100 customers | $50-100 | Start paying for monitoring, analytics |
| 500+ customers | $150-300 | Most tools on paid plans |
| 1000+ customers | $500+ | Enterprise-grade tools, multiple seats |

## Tool Migration Path

As you grow, migrate tools strategically:

1. **Spreadsheet → Free CRM** when you have 10+ leads to track
2. **Email + spreadsheet → Help desk** when support volume exceeds 20 tickets/week
3. **Free monitoring → Paid** when you need advanced alerting or 99.9%+ uptime SLA
4. **Basic analytics → Paid** when you hit event limits or need funnel analysis
5. **Dedicated support person → Paid support tool** when you hire your first support person

## Anti-Patterns: What NOT to Do

1. **Tool hoarding** — Don't sign up for every free tool. Each tool costs time to learn and maintain.
2. **Premature upgrades** — Don't pay for features you don't need yet. Free tiers are generous for a reason.
3. **Siloed data** — Don't let data live in tools that don't integrate. If it can't send to Zapier, reconsider.
4. **No backup plan** — Don't build dependency on a tool with no export. Always know how to migrate out.
5. **Ignoring free tiers' limits** — Know what happens when you exceed limits (automatic upgrade, blocked access, data loss).
6. **Over-automation** — Not everything needs a workflow. Sometimes the simplest tool is your brain + a checklist.

## Tool Stack Audit Schedule

Quarterly, review your tool stack:

- **Is this tool still providing value?** Cancel anything you haven't used in 30 days.
- **Has a better/cheaper alternative emerged?** The SaaS tool landscape changes fast.
- **Are there unused features I'm paying for?** Often you can downgrade to a cheaper plan.
- **Am I approaching any limits?** Plan upgrades before they become emergencies.
- **Are there integrations I should set up?** Connect tools that are still siloed.

## Resources

- [SaaS Tool Stack Spreadsheet Template](https://docs.google.com/spreadsheets/d/1x7Yk8z9Z0X0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0Y0/edit)
- [Zapier App Directory](https://zapier.com/apps) — Check which tools integrate
- [AlternativeTo](https://alternativeto.net) — Find alternatives to expensive tools
- [Product Hunt](https://producthunt.com) — Discover new tools (but beware of shiny object syndrome)
