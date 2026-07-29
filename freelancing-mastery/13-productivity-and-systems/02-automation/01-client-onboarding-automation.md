# Client Onboarding Automation

## Why Automate Onboarding

Every time you onboard a client manually, you lose $500-$2,000 in unbillable labor. The average freelancer spends 8-15 hours per client on:

- Back-and-forth emails with scope details
- Creating and sending proposals
- Revising proposals
- Sending and tracking contracts
- Chasing deposits
- Setting up project management tools
- Creating shared folders and access
- Writing onboarding documents
- Scheduling kickoff calls
- Explaining your process

**The Solution:** Automate every step of this process. The one-time investment of 10-20 hours to build your automation system pays for itself with the first 2-3 clients, then becomes pure profit.

**The Goal:** From "yes" to "signed, paid, and started" in under 24 hours, with zero manual effort.

## The Complete Automated Onboarding Flow

```
Client Says Yes
        ↓
[Automated] Proposal acceptance confirmation
        ↓
[Automated] Contract generated and sent (e-signature)
        ↓
[Automated] Deposit invoice sent
        ↓
[Automated] Payment received → trigger
        ↓
[Automated] Welcome packet delivered
        ↓
[Automated] Project management workspace created
        ↓
[Automated] File storage folders created and shared
        ↓
[Automated] Kickoff call scheduled
        ↓
[Automated] Onboarding questionnaire sent
        ↓
[Automated] Development/design environment provisioned
        ↓
[Automated] Welcome email sequence begins
        ↓
[Automated] First project milestone begins
```

## Tool Stack for Onboarding Automation

### All-in-One Platforms

**HoneyBook:** Best for freelancers. Proposals, contracts, invoices, payments, and client portal all in one. $39/month. Handles the entire workflow.

**Bonsai:** Popular with freelancers. Proposals, contracts, invoices, tracking. $25/month. Good for solo operators.

**Dubsado:** More robust, better for agencies. Proposals, contracts, invoices, CRM, workflows. $35/month. Steep learning curve but powerful.

**PandaDoc:** Best for complex proposals and contracts. More enterprise-focused. $19/month.

### Best-of-Breed Stack (Recommended for Maximum Control)

**Proposals:** Better Proposals, Qwilr, or PandaDoc
**Contracts:** Hellosign (Dropbox Sign), DocuSign, or PandaDoc
**Invoicing:** Stripe Invoicing, FreshBooks, or Xero
**Payments:** Stripe, Square
**Project Management:** Notion, Asana, ClickUp, or Monday.com
**CRM:** HubSpot (free), Pipedrive, or Folk
**Communication:** Slack, Discord, or Client portal
**File Sharing:** Google Drive, Dropbox, or Box
**Automation:** Zapier, Make (Integromat), or n8n

## Step 1: The Proposal Automation

### Template Structure

Create 3-5 proposal templates for different project types:
- **Fixed Price Web Dev:** For standard website/feature builds
- **Retainer Maintenance:** For ongoing support
- **Consulting Package:** For strategy/consulting engagements
- **Design Sprint:** For design-only projects
- **Custom Enterprise:** For large, complex projects

### Proposal Template Elements

**Static (reusable in every proposal):**
- Your bio and credentials
- Your process/methodology
- Testimonials and case studies
- Terms and conditions
- FAQ section
- Guarantee/warranty

**Dynamic (auto-filled by tools):**
- Client name and company
- Project scope summary
- Timeline and milestones
- Pricing breakdown
- Payment schedule
- Specific deliverables

### Automation Triggers

**Trigger 1: Discovery call completed:**
- Action: Send proposal template with call notes auto-filled
- Tool: Calendly webhook → Zapier → Better Proposals

**Trigger 2: Client asks for proposal:**
- Action: Send personalized proposal link
- Tool: Gmail template + proposal tool link

**Trigger 3: Proposal viewed (tracking):**
- Action: Get notification when client opens proposal
- Action: Get notification when client spends time on pricing section
- Follow-up: If viewed >2x without action, send follow-up email

### Proposal Best Practices

**Pricing Presentation:**
- Always show 3 tiers (good, better, best)
- Highlight the middle tier as "recommended"
- Show ROI calculation (what client gains vs cost)
- Include payment terms (50% upfront, 50% on completion)

**Social Proof:**
- Include 2-3 relevant case studies
- Client logos (if applicable)
- Testimonials specific to similar projects
- Results data (time saved, revenue increased, etc.)

**Call to Action:**
- Single button: "Accept Proposal"
- Auto-opens contract if accepted
- No negotiation — price is the price

## Step 2: The Contract Automation

### What Your Contract Needs

**Legally Required:**
- Full legal names of both parties
- Scope of work (detailed)
- Deliverables list
- Timeline and milestones
- Payment terms (amount, schedule, method)
- Late payment terms (interest, fees)
- Intellectual property rights
- Confidentiality clause
- Termination clause
- Limitation of liability
- Dispute resolution

**Freelancer Protections:**
- Scope change process (change order required)
- Client responsibility clause (they must provide X by Y date)
- Kill fee (if project cancelled mid-way, you get paid for work done)
- Late payment penalties (1.5% monthly or $50 late fee)
- Approval window (5 business days to review, then auto-approved)
- Independent contractor status (not employee)

### Contract Automation Flow

**Trigger: Proposal accepted:**
- Action: Generate contract from template
- Action: Pre-fill with proposal details (scope, price, timeline)
- Action: Send via Dropbox Sign / DocuSign for e-signature

**Trigger: Contract signed:**
- Action: Store signed PDF in client folder
- Action: Send signed copy to client
- Action: Trigger invoice/deposit request
- Action: Add to CRM as "Active Client"

### E-Signature Tools

**Dropbox Sign (Hellosign):** $20/month. Templates, bulk send, API access. Best for most freelancers.

**DocuSign:** $25/month. More features, more expensive. Better for legal-heavy industries.

**PandaDoc:** $19/month. Combined proposals + contracts + e-signature. Good all-in-one.

**Adobe Sign:** Included with Adobe Acrobat. If you already have Adobe, use this.

### Contract Automation with Zapier

```zapier
Trigger: PandaDoc contract signed
Actions:
  1. Create folder in Google Drive: "Client Name - Project Name"
  2. Create project in Asana/ClickUp
  3. Send Slack notification to onboarding channel
  4. Send invoice via Stripe
  5. Add client to HubSpot with "Onboarding" tag
  6. Send welcome email via Gmail
  7. Create calendar event for kickoff call (2 days later)
  8. Create task for you: "Send onboarding questionnaire"
```

## Step 3: The Deposit Automation

### Payment Collection

**Trigger: Contract signed:**
- Action: Send invoice for deposit (30-50% of total)
- Tool: Stripe Invoicing or FreshBooks
- Method: Credit card or ACH (bank transfer)

**Invoice Content:**
- Line items matching proposal
- Deposit amount clearly stated
- Remaining balance schedule
- Payment link (Stripe Checkout or Stripe Payment Links)
- Due date: "Due upon receipt"

### Deposit Structures by Project Size

| Project Value | Deposit | Milestone 2 | Milestone 3 | Final |
|--------------|---------|-------------|-------------|-------|
| <$1,000 | 100% | - | - | - |
| $1K-$5K | 50% | - | - | 50% |
| $5K-$15K | 33% | 33% | - | 34% |
| $15K-$50K | 25% | 25% | 25% | 25% |
| $50K+ | 20% | 20% | 30% | 30% |

### Payment Automation Tools

**Stripe:**
- Payment links (create once, reuse)
- Recurring invoices
- Automatic receipts
- Stripe Tax (auto-calculates taxes)
- Stripe Invoicing (free with Stripe payments)

**Square:** Similar to Stripe. Better if you do in-person payments too.

**FreshBooks:** Built-in invoicing + payment processing. Good for simple needs.

**Xero + Stripe:** More accounting-focused. Better for complex business finances.

### Payment Verification

Use Stripe webhooks to confirm payment:
```stripe webhook
Event: invoice.payment_succeeded
Actions:
  1. Update project status to "Funded"
  2. Send payment confirmation to client
  3. Trigger onboarding sequence
  4. Start project timeline
  5. Notify you: "Deposit received. Onboarding activated."
```

## Step 4: The Project Setup Automation

### Once Payment is Confirmed

**Trigger: Deposit received (payment succeeded):**
- Action sequence (via Zapier/Make):

**1. Client Portal/Welcome Packet:**
- Send welcome PDF with:
  - Project timeline overview
  - Communication channels and response times
  - Process documentation (how we work together)
  - Key contacts (you, any team members)
  - FAQ about your workflow
  - Emergency contact protocol

**2. Project Management Setup:**
- Automatically create project in Notion/Asana/ClickUp
- Add client as guest (limited permissions)
- Create milestones based on proposal template
- Assign tasks for first sprint
- Set up project timeline

**3. File Storage Setup:**
- Create shared Google Drive/Dropbox folder
- Create subfolders: Assets, Deliverables, References, Invoices
- Set sharing permissions (client can view/edit specific folders)
- Share folder link via email

**4. Communication Channels:**
- Create dedicated Slack channel or Discord room
- Add client as guest
- Set channel purpose and pinned guidelines
- Post welcome message with project overview

**5. Development/Design Environment:**
- Create staging server or development environment
- Set up repository (GitHub/GitLab) with access
- Create feature branches for first sprint
- Deploy initial project skeleton
- Share access credentials via 1Password/LastPass

**6. Kickoff Call Scheduling:**
- Send Calendly link for kickoff call (45-60 min)
- Suggest 3 dates (within first week)
- Agenda: Project kickoff, requirements review, roles, next steps
- Pre-call questionnaire: "What does success look like?"

## Step 5: The Onboarding Questionnaire

### Automated Questionnaire

Send this automatically after kickoff call is scheduled:

**Project Context:**
- What problem is this project solving?
- Who are the end users?
- What does success look like? (measurable metrics)
- What is the timeline driver? (why now?)
- Who are the stakeholders?

**Technical Requirements:**
- Existing tech stack (if any)
- Hosting/platform preferences
- Third-party integrations needed
- Security/compliance requirements
- Performance expectations

**Design/Brand Requirements:**
- Brand guidelines (colors, fonts, logos)
- Competitor examples
- Design inspiration/samples
- Accessibility requirements
- Preferred design style

**Content:**
- Do you have content ready?
- Who is writing the copy?
- Do you have images/videos?
- SEO keywords/target terms
- Content deadlines

**Access:**
- Domain/DNS access
- Social media accounts
- Analytics access
- Third-party tool access
- Existing hosting credentials

### Questionnaire Tools

- **Typeform:** Beautiful, interactive forms. Best for client-facing.
- **Jotform:** More powerful, more integrations. Good for complex forms.
- **Google Forms:** Free, simple. Good enough.
- **Notion Forms:** If you use Notion, this is seamless.

## Step 6: The Welcome Email Sequence

### Day 0 (Immediately After Payment)

**Email 1: Welcome & Excitement**
- Subject: "Let's build something amazing, [Client Name] 🚀"
- Content: Thank them, express excitement, overview of what's next
- CTA: Complete onboarding questionnaire

**Email 2: Project Timeline**
- Subject: "Here's what to expect over the next [X weeks]"
- Content: Milestone overview, delivery dates, communication schedule
- CTA: Mark your calendar for kickoff call

**Email 3: How We Work**
- Subject: "How to get the most out of our partnership"
- Content: Process, response times, how to give feedback, how to request changes
- CTA: Add notes/questions to shared doc

### Day 1

**Email 4: Resources Needed**
- Subject: "What I need from you to get started"
- Content: List of assets, access, information needed
- CTA: Share assets via shared folder

### Day 3 (If Questionnaire Not Completed)

**Email 5: Gentle Reminder**
- Subject: "Quick reminder: onboarding questionnaire"
- Content: Friendly nudge, offer to hop on a quick call if easier
- CTA: Complete questionnaire (5 minutes)

### Day 7

**Email 6: Kickoff Call Prep**
- Subject: "Preparing for our kickoff call"
- Content: Agenda, what to bring, who should attend
- CTA: Confirm attendance

## Full Automation Architecture (Zapier/Make)

### The Master Zap

```yaml
Triggers:
  - Contract signed (PandaDoc/DocuSign)
  - Payment received (Stripe)

Actions (parallel):
  1. Create client folder in Google Drive
  2. Create project in Asana/ClickUp
  3. Create Slack channel
  4. Send welcome email sequence (HubSpot/Mailchimp)
  5. Send onboarding questionnaire (Typeform)
  6. Schedule kickoff call (Calendly)
  7. Add client to mailing list (if opted in)
  8. Create invoice template for future milestones
  9. Set up recurring invoicing (if retainer)
  10. Send notification to your phone: "New client onboarded!"
```

## Onboarding Checklist (For Manual Review)

Even with automation, review these items before kickoff:

- [ ] Proposal accurately reflects scope
- [ ] Contract is signed by both parties
- [ ] Deposit received (check Stripe dashboard)
- [ ] Shared folders created and accessible
- [ ] Project management set up with milestones
- [ ] Client has access to communication channel
- [ ] Onboarding questionnaire submitted
- [ ] Kickoff call scheduled
- [ ] All required assets received
- [ ] Development environment ready
- [ ] First sprint tasks created and assigned
- [ ] Welcome sequence verified as sent

## Measuring Onboarding Efficiency

**Key Metrics:**
- Time from "yes" to signed contract: Target <24 hours
- Time from signed to deposit received: Target <48 hours
- Time from deposit to project started: Target <72 hours
- Hours of your manual time per onboarding: Target <1 hour
- Client satisfaction with onboarding (survey): Target 9+/10

**Track in Your CRM:**
- Source of lead
- Proposal sent date
- Proposal acceptance date
- Contract signed date
- Deposit received date
- Kickoff call date
- First deliverable date
- Onboarding completion date

## ROI of Onboarding Automation

**Investment:**
- Setup time: 15-20 hours (one-time)
- Tools: $50-150/month
- Maintenance: 1 hour/month

**Return:**
- 5-10 hours saved per new client
- At $150/hr: $750-$1,500 saved per client
- If you onboard 2 clients/month: $1,500-$3,000/month saved
- Faster start = faster revenue
- Professional impression = better client relationships
- Reduced errors = fewer problems later

**30-Day ROI:** Even with setup time, payback is within 1-2 clients.

---

**Summary:** Client onboarding automation is the highest-ROI automation you can build. It saves you 5-10 hours per client, makes you look incredibly professional, and gets projects started faster. Invest 15-20 hours building this once, and it pays dividends for years.
