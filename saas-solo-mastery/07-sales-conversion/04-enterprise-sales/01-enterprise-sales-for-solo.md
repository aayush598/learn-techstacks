# Enterprise Sales for Solo Founders

## The Solo Founder's Enterprise Paradox

Enterprise sales as a solo founder sounds impossible. Procurement processes require multiple approvals. Security reviews demand extensive documentation. RFPs require dedicated response teams. Implementation needs training and support.

Yet solo founders successfully sell to enterprises every day. The key is not to compete with enterprise sales teams on their terms. It's to use your unique advantages while mitigating your gaps.

**Your advantages over larger competitors:**
- Founder access: They talk to the person who built the product
- Flexibility: You can customize terms, pricing, and timeline in one conversation
- Speed: You can respond to security questionnaires in hours, not weeks
- Expertise: You know the technical details better than any sales engineer
- Focus: Enterprise customers get your full attention

**Your gaps:**
- No dedicated security team for reviews
- Limited references and case studies
- No compliance certifications initially
- No enterprise account management team
- Thin implementation support

## Is Your Product Ready for Enterprise?

### The Enterprise Readiness Checklist

Before investing in enterprise sales, confirm:

- [ ] Product can handle enterprise scale (performance, reliability)
- [ ] Core data is encrypted at rest and in transit
- [ ] You have basic documentation for architecture/security
- [ ] You've handled at least 5+ enterprise-level support requests
- [ ] Your pricing supports per-seat or commitment-based models
- [ ] You have a stable API that won't break with changes
- [ ] Uptime is 99.5%+ over the last 90 days
- [ ] You can support SAML/SSO or have a plan to build it
- [ ] You have a backup/disaster recovery plan

If you're missing 4+ of these, your product isn't enterprise-ready. Focus on getting these in place before targeting enterprise customers.

### The Enterprise Sales Readiness Checklist

- [ ] You've done at least 3 enterprise discovery calls
- [ ] You understand the enterprise buying process
- [ ] You have pricing for 50+ seat deals
- [ ] You have a security questionnaire response template
- [ ] You have at least 1 enterprise case study (or can write a disguised version)
- [ ] You have a standard MSLA (Master Service Level Agreement) template
- [ ] You have a data processing agreement (DPA) template
- [ ] You have a standard implementation plan

## Finding Enterprise Prospects

### Inbound Enterprise Leads

Enterprise prospects often find you through:
- Content marketing (in-depth technical content)
- Integration marketplaces (they're using a tool you integrate with)
- Developer advocacy (enterprise developers discover your API)
- Industry events and conferences
- Referrals from existing customers
- Competitive analysis (they're evaluating your competitor)

**Identifying enterprise prospects:**
- Company email domain (not gmail.com)
- Multiple signups from the same company
- Team accounts with 5+ members
- API usage at significant volume
- Support tickets about security, compliance, or scalability

### Outbound Enterprise Prospecting

As a solo founder, outbound must be surgical. You can't spray and pray.

**Target qualification:**
- Company size: 50-500 employees is ideal for first enterprise deals
- Budget: Likely $50k-500k ARR for software tools
- Need: Clear pain that your product solves
- Access: Warm intro preferred, cold outreach as backup

**Getting warm intros:**
- LinkedIn mutual connections
- Shared Slack/Discord communities
- Previous colleagues or classmates
- Investors or advisors
- Existing customers (ask for introductions)

**Cold outreach for enterprise:**
- Find the right person (Head of [Department], CTO, VP of Engineering)
- Reference something specific about their company
- Lead with insight, not pitch
- Offer value: "I noticed you're doing [X]. Here's how [Customer] approached it."

## The Enterprise Buying Process

### Stakeholder Map

Enterprise deals involve multiple people with different priorities:

**The Champion (Internal seller):**
- Uses/believes in your product
- Wants to convince others to buy
- Needs: Ammo to sell internally (ROI data, comparison docs, case studies)
- Threat: If they leave the company, you lose the deal

**The Economic Buyer (Budget holder):**
- Controls the budget
- Cares about: ROI, TCO, strategic value
- Needs: Business case, pricing, implementation timeline
- Threat: Budget reallocation, competing priorities

**The Technical Evaluator (IT/Security):**
- Evaluates technical fit
- Cares about: Security, compliance, integration, scalability
- Needs: Documentation, architecture review, security questionnaire
- Threat: Security concerns, technical debt

**The User (End user):**
- Will use the product daily
- Cares about: Ease of use, features, support
- Needs: Demo of workflows, training plan, migration support
- Threat: Change resistance, learning curve

**The Procurement (Legal/Finance):**
- Negotiates terms and pricing
- Cares about: Contract terms, payment terms, SLAs
- Needs: Standard contract, pricing proposal, vendor onboarding
- Threat: Legal concerns, compliance requirements

### The Buying Process Timeline

**Typical enterprise buying process (2-6 months):**

1. **Problem identification** (week 1-2): Someone realizes there's a problem worth solving
   - Your role: Educational content, awareness

2. **Solution discovery** (week 2-4): They find options, including you
   - Your role: Be findable (content, SEO, community)

3. **Evaluation** (week 4-8): They evaluate 2-4 solutions
   - Your role: Demo, trial, technical evaluation

4. **Selection** (week 8-10): They choose a vendor
   - Your role: Final demo, pricing, references

5. **Procurement** (week 10-16): Legal, security, procurement
   - Your role: Security review, contract negotiation, DPA

6. **Onboarding** (week 16-20): Implementation and rollout
   - Your role: Setup assistance, training, migration

7. **Go-live** (week 20+): Full deployment
   - Your role: Launch support, celebration

### Why Enterprise Deals Fail

- No champion (nobody is selling internally)
- Champion has no power or influence
- Security review uncovers blockers
- Procurement kills on price or terms
- Budget gets reallocated
- Timeline drags and loses momentum
- Technical evaluation reveals gaps
- Competitor offers better terms at the last minute

## Security Reviews

### The Security Review Process

Enterprise prospects will ask for:

1. **Security questionnaire** — 20-200 questions about your security practices
2. **Architecture review** — How your system works, data flow, encryption
3. **Penetration test results** — Third-party security testing
4. **SOC 2 report** or similar certification (often a requirement)
5. **Data processing agreement (DPA)** — For GDPR compliance
6. **Business continuity plan** — Disaster recovery, backup procedures

### Handling Security Reviews as a Solo Founder

**Before you have SOC 2:**

Most early-stage companies don't have SOC 2. Here's how to handle it:

**Option 1: Answer honestly and thoroughly**
"I'm a solo founder and we don't have SOC 2 yet. What I can provide is:
- Our architecture documentation
- Our encryption practices (AES-256 at rest, TLS 1.3 in transit)
- Our data handling procedures
- Our hosting provider's certifications (AWS SOC 2, etc.)
- My personal commitment to your security needs"

Many mid-market enterprises will accept this if you're transparent and thorough.

**Option 2: Leverage your cloud provider's certifications**
If you're on AWS/GCP/Azure, your infrastructure inherits their compliance:
"We run on AWS, which maintains SOC 2, ISO 27001, HIPAA, and more. Here's our shared responsibility model..."

**Option 3: Use a compliance automation tool**
- Vanta ($500/mo) — automate SOC 2 evidence collection
- Drata ($400/mo) — similar to Vanta
- Secureframe ($500/mo) — compliance automation
- These tools guide you through SOC 2 preparation

**Option 4: Offer a security call with the founder**
"I'd be happy to hop on a call with your security team. I built the infrastructure myself and can answer any technical question they have."

### Building a Security Questionnaire Response Library

Create a document with responses to the most common security questions. Update as you go.

**Categories to prepare:**
- Organization and administration
- Data security (encryption, access controls)
- Infrastructure security (hosting, network)
- Application security (auth, input validation)
- Operational security (monitoring, incident response)
- Business continuity (backup, DR)
- Compliance (GDPR, SOC2, HIPAA)

**Question sources:**
- CommonSecurityQuestionnaire.com (standard library)
- SIG (Standard Information Gathering) questionnaire
- Vanta's questionnaire library
- Your own experience from previous reviews

When you get a questionnaire, answer it once, save your answers, and reuse in future reviews.

### Penetration Testing

For your first enterprise deals, you may need a penetration test.

**Budget options:**
- Small independent pentesters ($2k-5k)
- Upwork or Fiverr (variable quality, but cheap)
- HackerOne or Bugcrowd (pay per finding)
- Automated scanners (covers basics, not comprehensive)

**What to test:**
- Authentication and authorization
- API endpoints
- Data handling
- Injection points (XSS, SQLi, etc.)
- Session management

Fix findings before sharing with enterprise clients.

## RFP Response

### What Is an RFP?

Request for Proposal. A formal document from enterprise buyers asking vendors to propose solutions.

**RFP sections typically include:**
- Company background
- Problem statement
- Technical requirements (must-haves and nice-to-haves)
- Implementation requirements
- Support requirements
- Pricing requirements
- Evaluation criteria
- Submission instructions

### RFP Response Strategy for Solo Founders

**When to respond to an RFP:**
- You have a relationship with someone at the company
- You know your product is a strong fit
- You have the time to do it justice
- The deal size justifies the effort (ideally $10k+/year)

**When to skip an RFP:**
- You're responding blind (no relationship)
- The requirements don't match your product
- The evaluation criteria favor incumbent/differentiators
- You don't have the certifications they require
- The deal size is too small for the effort

### Efficient RFP Response

**Preparation (one-time effort):**
Create an RFP response library with pre-written answers to common questions.

**Categories for your library:**
- Company overview
- Product features (one paragraph per feature)
- Technical architecture
- Security practices
- Implementation methodology
- Support and SLAs
- Pricing models
- Integration capabilities
- Customer references

**When responding:**
1. Review requirements (30 min)
2. Identify gaps — can you meet each requirement? (15 min)
3. Fill in from library (60 min)
4. Customize for this specific RFP (90 min)
5. Review and polish (30 min)

Total: 3-4 hours for a well-prepared founder.

**If you can't meet a requirement:**
- "We don't support [feature] natively, but here's how customers achieve this through [workaround/integration]."
- "This is on our roadmap for Q[Quarter]."
- "We can build this as a custom solution for your deployment."

### Winning RFPs

Enterprises use RFPs to:
1. Get competitive pricing
2. Create a paper trail for compliance
3. Compare apples to apples
4. Protect themselves from blame if the vendor fails

**To win:**
- Respond to every question (even if "not applicable" — explain why)
- Be specific about what you can and cannot do
- Provide pricing in the format they request
- Include customer references (even if you have to offer a discount for early reference customers)
- Submit before the deadline (always)
- Follow up within 24 hours of submission

## Enterprise Pricing

### Pricing Models

**Per-seat pricing:**
"$X/user/month. Minimum 50 seats."
Best for: Products with clear per-user value.

**Usage-based pricing:**
"$X per [unit]. Volume discounts at [Y] units."
Best for: API products, infrastructure tools.

**Tiered pricing:**
"Team: $X/mo for 10 users. Business: $Y/mo for 50 users. Enterprise: Custom."
Best for: Feature-differentiated products.

**Flat annual:**
"$X/year for unlimited usage within [scope]."
Best for: Enterprise platform deals.

### Enterprise Pricing Psychology

- Enterprise buyers expect to negotiate. Leave room.
- Quote annual pricing (monthly is for SMBs).
- Include implementation and training costs separately.
- Offer "Enterprise" tier with custom pricing (no public price).
- Always anchor high — you can come down, you can't go up.

**Pricing anchoring example:**
"Our standard enterprise pricing is $50,000/year. However, based on your specific needs and size, I think we can do something in the $30,000-$40,000 range."

### Creating an Enterprise Pricing Proposal

**Proposal sections:**
1. Executive summary (what they're buying and why)
2. Solution overview (how your product addresses their needs)
3. Pricing (clear, itemized)
4. Implementation timeline
5. Service and support commitments
6. Case studies (relevant, similar companies)
7. Terms and conditions (or reference to contract)
8. Next steps

## Procurement and Contracts

### The Procurement Process

Enterprise procurement typically involves:
1. **Vendor registration** — Fill out forms, provide W-9, insurance certificates
2. **Contract review** — Legal reviews your MSLA and DPA
3. **Negotiation** — Terms, pricing, SLAs, liability
4. **Approval** — Multi-level approval (department, legal, finance, exec)
5. **Purchase order** — They issue a PO, you invoice

### Contract Essentials

**Your contract should cover:**
- Scope of services (what you're providing)
- Fees and payment terms (Net 30 is standard enterprise)
- Term and termination (annual auto-renew is standard)
- Service level agreement (uptime, support response times)
- Data protection (GDPR, data processing, data residency)
- Confidentiality (both parties)
- Limitation of liability (standard is fees paid in last 12 months)
- Intellectual property (you own your IP, they own their data)
- Insurance requirements (they may require you to carry certain coverage)

### Key Contract Terms

**Indemnification:**
Enterprise will want you to indemnify them if your IP infringes. Limit to:
- Your IP only (not their use of it)
- With conditions (prompt notice, defense control, mitigation)

**Limitation of liability:**
Enterprise will try to remove or increase this. Standard:
- Cap at fees paid in last 12 months
- Exclusions for confidentiality breaches, IP infringement

**Auto-renew:**
Enterprise prefers manual renewal. Offer:
- 30-60 day notice for non-renewal
- Auto-renew with email notification

**Most favored nation (MFN) clause:**
Enterprise may ask that you give them the best pricing you offer anyone.
- Avoid if possible
- If required, limit to "similar volume and scope"

### Working with Enterprise Legal

**Tips for solo founders:**
- Use a standard contract template — don't negotiate from scratch
- Have a lawyer review your template once, then reuse
- Most enterprise legal changes are standard — don't take them personally
- Be willing to walk away from unreasonable terms
- Your time is valuable — legal negotiation can consume weeks

## Implementation and Onboarding

### Enterprise Implementation Plan

**Week 1: Setup and configuration**
- Account provisioning
- SSO/SAML configuration
- User import/creation
- Integration setup
- Security configuration

**Week 2-3: Testing and validation**
- Core workflow testing with pilot users
- Integration testing
- Performance validation
- User acceptance testing (UAT)

**Week 4: Training**
- Admin training (you train their admins)
- End-user training (they train their users)
- Documentation handoff
- FAQ creation

**Week 5: Rollout**
- Phased rollout to user groups
- Monitoring and support during launch
- Issue triage and resolution

**Week 6: Go-live**
- Full deployment
- Post-launch support (daily check-ins for week 1)
- Success metrics review

### Solo Founder Implementation Tips

- Start with a pilot group (5-10 users) before full rollout
- Offer to do the initial configuration yourself (you know the product best)
- Create an enterprise onboarding checklist specific to each customer
- Record training sessions for future reference
- Over-communicate during implementation — enterprise hates surprises
- Set up a dedicated Slack channel or email for the implementation period

## Enterprise Support

### Support Commitments

**Standard enterprise support:**
- Response time: 4 hours for critical, 8 hours for normal, 24 hours for low
- Resolution time: 24 hours for critical (or workaround), best effort for others
- Support channels: Email, chat, phone (if feasible)
- Support hours: Business hours in their timezone (or 24/5)

**As a solo founder, be realistic:**
"I provide personalized support as the founder. For critical issues, my response time is [X]. For standard issues, [Y]. I'm transparent about my capacity, and I'll always communicate honestly about timelines."

### The Enterprise SLA

**Standard SLAs:**
- 99.5% uptime (monthly)
- Credits if uptime drops below 99.5%
- Scheduled maintenance with 48-hour notice
- Emergency maintenance as needed (with notification)

**Don't offer SLAs you can't meet:**
- 99.9% uptime requires redundant infrastructure
- 24/7 phone support requires coverage in all timezones
- 1-hour response time means you're always on call

## Managing Enterprise Expectations

### Setting Boundaries

**Be clear about what you can and can't do:**
- "I'm the founder and also the support team. Here's how that works..."
- "I can commit to [X] response time for critical issues."
- "New features go on the public roadmap. I can't build custom features for individual customers."
- "I'll be transparent about my availability and capacity."

### Over-Communication

Enterprise customers tolerate your size if you communicate proactively.

**Communication cadence:**
- Weekly check-in during implementation
- Monthly business review after go-live
- Immediate notification of any incidents
- Quarterly product roadmap update
- Annual review and renewal planning

### When to Say No

**Enterprise requests you should decline:**
- Custom features that only benefit one customer
- On-site visits (you don't have an office — offer video instead)
- Unlimited liability in contracts
- 99.99% uptime SLAs
- Full-time dedicated support engineer (you're the only engineer)
- Source code escrow (mostly legacy, rarely happens)

## Building Enterprise Credibility

### References and Case Studies

For your first enterprise deals, you need references. Bootstrap this:

- Offer significant discounts (40-50% off) for first 3 enterprise customers in exchange for being a reference
- Write anonymized case studies: "A Fortune 500 company in [industry] used [Product] to [result]"
- Get testimonials on specific dimensions: "Their support is incredible — the founder responded within 2 hours."
- Ask satisfied customers for LinkedIn recommendations

### Partnerships

Partner with complementary vendors that already serve enterprises:
- Integration partners (your product integrates with theirs)
- Implementation partners (consultancies that can help deploy)
- Referral partners (they refer you in exchange for commission)
- Technology partners (co-market and co-sell)

### Social Proof for Enterprise

- Blog about your enterprise features and roadmap
- Publish your security practices (even if not certified)
- Share customer logos (with permission)
- Speak at industry events
- Get listed on integration marketplaces
- Publish case studies with measurable results

## The Enterprise Sales Motion as a Solo Founder

### Monthly Enterprise Sales Rhythm

**Week 1: Prospecting**
- Identify 5-10 target accounts
- Research each account
- Find warm intros
- Prepare outreach

**Week 2: Outreach**
- Send personalized outreach
- Follow up on inbound enterprise leads
- Nurture existing pipeline

**Week 3: Demos and evaluations**
- Run enterprise demos
- Handle technical evaluations
- Respond to security questionnaires

**Week 4: Proposals and closes**
- Send proposals
- Negotiate contracts
- Close deals

### Pipeline Management

**Enterprise pipeline stages:**
1. Target (not yet contacted)
2. Contacted (outreach sent)
3. Connected (conversation started)
4. Evaluating (demo done, trial started)
5. Technical review (security, integration testing)
6. Procurement (legal, contract)
7. Closing (final negotiation, signatures)
8. Won/Lost

**At any time, aim for:**
- 10-20 targets in prospecting
- 5-10 active conversations
- 2-3 in evaluation
- 1-2 in procurement
- 1 closing per month (to hit 12+ enterprise deals/year)

## Case Study: How a Solo Founder Closed an Enterprise Deal

### The Deal

- Product: Developer tool API
- Company: Fortune 500 financial services
- Deal size: $36,000/year (two-year commit)
- Timeline: 4 months from first contact to signed contract

### The Process

**Month 1:** Inbound signup from senior engineer at company. Started trial, invited 3 teammates. Reached out with personal Loom. Discovery call with engineering team.

**Month 2:** Follow-up demo with Head of Engineering. Security questionnaire submitted (48 pages). Answered within 1 week by leveraging prepared response library.

**Month 3:** Security call with their CISO. Architecture walkthrough. Contract negotiation — they wanted unlimited liability and 99.99% SLA. Held firm on standard terms. Compromised on 99.9% SLA with increased credits.

**Month 4:** Final approval from procurement. Two-year commit at 15% discount. Signed. Onboarding completed in 2 weeks.

**Key success factors:**
- Champion was the initial signup (engineer who loved the product)
- Prepared security response library saved weeks
- Founder-to-CISO call built trust
- Willingness to walk away from unreasonable terms
- Two-year commit made the deal economics work

## Conclusion

Enterprise sales as a solo founder is challenging but achievable. You won't win every deal, and you shouldn't try to. Focus on the deals where:
- Your product is a clear fit
- You have an internal champion
- The prospect values founder access and speed
- The deal economics justify your time investment

Build your systems — security questionnaires, RFP library, contract templates — once and reuse them. Your efficiency improves with every enterprise deal.

And remember: you don't need 100 enterprise customers. You need 10-20 good ones at $10k-50k/year each. That's a $200k-$1M ARR business with just enterprise customers. Plus your self-serve revenue on top.

That's the solo founder enterprise dream — and it's achievable with focus, systems, and a willingness to punch above your weight.
