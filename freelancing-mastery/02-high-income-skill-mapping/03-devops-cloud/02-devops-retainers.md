# DevOps Retainers: CI/CD, Infrastructure as Code, Monitoring

## Overview

DevOps retainers are the holy grail of tech freelancing: recurring monthly income for providing ongoing infrastructure and CI/CD support. Unlike project-based work where you're constantly hunting for the next client, retainers provide predictable revenue and deep client relationships.

This guide covers how to structure, price, sell, and deliver DevOps retainer services.

## Why DevOps Retainers Are Profitable

1. **Recurring revenue**: Predictable income every month — no feast/famine cycle
2. **Deep relationships**: After 3+ months, you're indispensable (high switching costs)
3. **Growing scope**: Systems evolve, new services get added, retainer grows
4. **Multiple clients**: 3-5 retainers at $5-10K/month = $180-600K/year
5. **Low sales cost**: One sale = months or years of revenue
6. **Efficiency**: Infrastructure patterns repeat — build once, reuse everywhere

### Rate Reality

| Renter Size | Hours/Month | Rate | Monthly Revenue | Best For |
|-------------|-------------|------|-----------------|----------|
| Micro | 5-10 hrs | $100-150/hr | $500-1.5K | Early stage startups, side income |
| Standard | 15-25 hrs | $125-175/hr | $1.9-4.4K | Growing startups, mid-market |
| Premium | 30-50 hrs | $150-200/hr | $4.5-10K | Mid-market, established SaaS |
| Enterprise | 50-100 hrs | $175-250/hr | $8.8-25K | Large enterprises, high compliance |

## Service Offerings

### Core Retainer Services

**1. CI/CD Pipeline Management** (30% of typical retainer work)

What you do: Maintain, improve, and troubleshoot CI/CD pipelines.

Activities:
- Pipeline maintenance (fix broken builds, update dependencies)
- Pipeline improvements (add stages, optimize build times)
- New service onboarding (add new services to CI/CD)
- Secret rotation (update credentials, API keys)
- Deploy strategy improvements (blue/green, canary, rolling)
- Multi-environment management (dev, staging, production)

Tools: GitHub Actions, GitLab CI, CircleCI, Jenkins, ArgoCD, CodePipeline

**2. Infrastructure as Code (IaC) Management** (30% of typical retainer work)

What you do: Maintain and evolve infrastructure code.

Activities:
- Terraform state management
- Module updates and improvements
- New resource provisioning
- Decommissioning old resources
- Policy as Code (Sentinel, OPA)
- Compliance validation (checkov, tfsec, terrascan)

Tools: Terraform, Pulumi, CloudFormation, CDK

**3. Monitoring and Observability** (20% of typical retainer work)

What you do: Keep monitoring systems healthy and useful.

Activities:
- Alert tuning (reduce noise, improve signal)
- Dashboard creation and maintenance
- Log aggregation and analysis
- Tracing setup and improvement
- Uptime monitoring configuration
- Incident response (during business hours)

Tools: Datadog, New Relic, Grafana + Prometheus, Sentry, PagerDuty

**4. Security and Compliance** (10% of typical retainer work)

What you do: Maintain security posture.

Activities:
- Dependency scanning and updates
- Container image scanning and remediation
- IAM policy review and cleanup
- Secret scanning
- Compliance report generation (SOC2, HIPAA)
- Security patch management

Tools: Snyk, Trivy, Checkov, AWS GuardDuty, Azure Defender

**5. Cost Optimization** (10% of typical retainer work)

What you do: Keep cloud costs under control.

Activities:
- Monthly cost review
- Rightsizing recommendations
- Reserved instance/Savings Plan management
- Idle resource cleanup
- Budget alert maintenance

Tools: AWS Cost Explorer, CloudHealth, Vantage, in-house scripts

### On-Call / Incident Response Add-on

- 24/7 on-call for production incidents: +$2-5K/month
- SLA: 15-minute response time, 1-hour resolution target
- Tier 1: You handle initial triage
- Tier 2: Escalate to client team if needed
- Post-mortem and follow-up included

### Project-Based Add-ons (beyond retainer)

| Project | Typical Price | Frequency |
|---------|--------------|-----------|
| Migration (K8s, cloud, CI/CD) | $10-50K | 1-2x/year per client |
| New environment setup | $5-15K | As needed |
| Disaster recovery testing | $3-10K | Quarterly |
| Security audit | $5-15K | Quarterly/Annual |
| Architecture review | $5-20K | Annual |
| Training workshop | $5-15K | As needed |

## Structuring Your Retainer Agreement

### What to Include in Every Retainer Contract

**Scope of services**:
- Number of hours per month
- What's included (types of work)
- What's excluded (major projects, on-call, etc.)
- How to request work (Slack, tickets, async)

**Communication**:
- Primary channel (Slack, email, Discord)
- Response time expectations (same business day, within 4 hours)
- Meeting cadence (weekly status, monthly review)
- Reporting (monthly summary of work done)

**Boundaries**:
- Working hours (timezone, business days)
- Urgent vs non-urgent requests
- What constitutes out-of-scope
- Vacation and backup plan

**Pricing**:
- Monthly retainer fee
- Additional hours (rate for overage)
- On-call add-on pricing
- Project add-on pricing
- Payment terms (net-15 or net-30)
- Late payment penalties

**Term**:
- Initial term (3-6 months minimum)
- Renewal terms (month-to-month after initial)
- Notice period for cancellation (30-60 days)
- Rate increase terms (annual or with notice)

### Sample Retainer Agreement (Scope Section)

```
## Scope of DevOps Retainer Services

### Included (up to [X] hours/month):
1. CI/CD pipeline maintenance and minor improvements
2. Infrastructure as Code management and updates
3. Monitoring and alert maintenance
4. Security updates and dependency management
5. Cost optimization recommendations
6. Technical support via Slack (business hours)
7. Weekly 30-minute status call
8. Monthly written summary of work performed

### Not Included (separate project pricing):
1. New infrastructure projects (new environment, major migration)
2. Architecture design for new products/features
3. Security audits or penetration testing
4. Training and documentation outside ongoing maintenance
5. On-call / incident response outside business hours

### Scope Clarifications:
- "Minor improvements" = changes that take 4 hours or less
- "Security updates" = applying patches, not security architecture
- "Monitoring maintenance" = tuning alerts, not building new monitoring systems
```

## Pricing Strategies

### Value-Based Pricing for Retainers

Don't price based on hours. Price based on the value of reliability.

**Sample pitch**:
"Without reliable DevOps, your engineering team loses 10-20% of their time to infrastructure issues. That's 1-2 engineers worth of productivity. At $150K/year per engineer, that's $150-300K of lost productivity. My retainer of $8K/month ensures your team ships code, not fixes pipelines."

### Hourly-Based Pricing with Minimums

**Strategy**: Quote a monthly retainer based on estimated hours, with a minimum commitment.

Example:
"Based on the complexity of your infrastructure, I estimate this will take 20-30 hours per month. My retainer is $5K/month for 25 hours. Additional hours at $200/hr. We review and adjust after 3 months."

### Tiered Pricing

| Tier | Hours | Monthly | Features |
|------|-------|---------|----------|
| Essential | 10 hrs | $2K | CI/CD maintenance, basic monitoring, Slack support |
| Standard | 25 hrs | $5K | All Essential + IaC management, security updates, weekly call |
| Premium | 50 hrs | $9K | All Standard + cost optimization, architecture reviews, monthly report |
| Enterprise | Custom | $15-25K | All Premium + on-call, compliance support, dedicated Slack channel |

## Client Acquisition

### Ideal Client Profile for DevOps Retainers

**Best clients**:
- SaaS companies with 5-50 engineers
- $1-50M ARR (funded and growing)
- Running on cloud (AWS, GCP, Azure)
- Current state: "We're managing infrastructure ourselves and it's a mess"
- Decision maker: CTO, VP Engineering, Head of Platform
- Pain: Too much time spent on infrastructure, not enough on product

**Red flags** (avoid or price higher):
- "We just need someone for a few hours" (scope will grow, they won't pay more)
- "We're trying to reduce costs" (they'll nickel-and-dime you)
- No dedicated DevOps person already (they don't understand the value)
- On-premise only (unless you're an expert, avoid)
- "We'll start with a trial project" (code for "we want to evaluate you without commitment")

### Where to Find Clients

**1. Engineering communities** (Slack/Discord)
- Join SaaS engineering communities (Rands Leadership, Devops Weekly)
- Answer infrastructure questions helpfully
- When someone asks "How do I set up X?" — offer help
- Build relationships, then offer retainer

**2. LinkedIn**
- Target: CTOs and VPs of Engineering at SaaS companies
- Share DevOps tips, case studies, and insights
- Connect and offer: "I noticed you're scaling. Are your DevOps processes keeping up?"

**3. Referral partnerships**
- Partner with dev shops / agencies who build software
- They build the product, you handle infrastructure
- Split the retainer or get a referral fee
- Partner with cloud consultants who find infra messes at clients

**4. Cold outreach**
"Most SaaS companies our size end up with DevOps as a bottleneck. The CTO is stuck doing Terraform instead of product strategy. I prevent that. One retainer, entire DevOps function handled."

**5. Content marketing**
- Write about common DevOps problems and solutions
- "GitHub Actions Best Practices" / "Terraform at Scale" / "Kubernetes Cost Optimization"
- Every post is a lead generation asset

### Outreach Email Template

```
Subject: DevOps support for [Company]

Hi [Name],

I help SaaS companies maintain their infrastructure so their
engineering team can focus on product.

Most companies your size end up with:
- Broken CI/CD pipelines that stall deployments
- Cloud costs growing 20%+ month over month
- Security vulnerabilities from unpatched dependencies
- An engineer spending 30% of their time on infrastructure

I handle all of that on a monthly retainer.

Recent results for a similar company:
- Cut deployment time from 45 minutes to 8 minutes
- Reduced cloud costs by 35% ($12K/month savings)
- Zero security incidents in 18 months

Would you be open to a 15-minute call to see if this
makes sense for you?

Best,
[Your Name]
```

## Delivery Process

### Onboarding a New Retainer Client

**Week 1: Discovery and Baseline**
- Document current infrastructure (diagrams, configs, access)
- Review CI/CD pipelines
- Review monitoring and alerting
- Identify quick wins (things to fix in week 1-2)
- Set up communication channels

**Week 2: Stabilization**
- Fix critical issues (broken pipelines, alert noise, security gaps)
- Set up monitoring dashboards
- Document runbooks for common issues
- Establish SLA expectations

**Week 3-4: Optimization**
- Implement quick wins from discovery
- Improve CI/CD pipelines
- Optimize cloud costs
- Set up regular reporting

**Ongoing (monthly cycle)**:
- Week 1: Major improvements, new projects
- Week 2: Maintenance, updates, minor fixes
- Week 3: Optimization and cleanup
- Week 4: Reporting, planning, communication

### Monthly Reporting Template

```
# DevOps Retainer Monthly Report — [Month] [Year]

## Client: [Company Name]

### Summary
Hours worked this month: [X]
Incidents handled: [Y]
Major changes: [Z]

### Work Completed
1. [CI/CD improvement] — reduced build time by X%
2. [Security update] — patched X vulnerabilities
3. [Cost optimization] — saved $X/month
4. [Monitoring] — added X alerts, removed Y false positives

### Incidents
| Date | Issue | Resolution | Time to Resolve |
|------|-------|-----------|-----------------|
| [Date] | [Brief] | [Solution] | [Time] |

### Recommendations
1. [Priority recommendation] — estimate X hours, impact Y
2. [Nice-to-have] — estimate X hours
3. [Future consideration] — worth discussing in next planning

### Next Month Plan
- [Planned project 1]
- [Planned project 2]
- [Ongoing maintenance]
```

## Toolkit for DevOps Retainers

### Must-Have Tools

**Infrastructure as Code**:
- Terraform (primary)
- Terragrunt (DRY Terraform)
- Terraform Cloud / Enterprise (state management, collaboration)

**CI/CD**:
- GitHub Actions (most popular)
- GitLab CI (if client uses GitLab)
- CircleCI (fast, debuggable)
- ArgoCD (Kubernetes GitOps)

**Container Orchestration**:
- Kubernetes (EKS, AKS, GKE, or self-managed)
- Docker Compose (simple environments)
- Helm (Kubernetes package management)

**Monitoring**:
- Prometheus + Grafana (best open-source stack)
- Datadog (best SaaS option — expensive but excellent)
- New Relic (good APM, expensive)
- Sentry (error tracking)
- PagerDuty / Opsgenie (incident management)

**Security**:
- Snyk (dependency scanning)
- Trivy (container scanning)
- Checkov / tfsec (IaC scanning)
- SonarQube (code quality/security)

**Cost Management**:
- AWS Cost Explorer (free)
- CloudHealth / Vantage (if client needs more)

### Infrastructure Templates (Reusable)

Build a library of reusable templates for common tasks:

1. **Standard CI/CD pipeline** (build → test → security scan → deploy)
2. **Terraform module for ECS/Fargate** (app + load balancer + auto-scaling)
3. **Terraform module for EKS** (cluster + node groups + IAM)
4. **Monitoring dashboard template** (standard metrics + alerts)
5. **Backup automation** (database snapshots, S3 replication)
6. **Disaster recovery plan template** (RTO/RPO, runbooks)
7. **Cost optimization script** (find idle resources, rightsizing recommendations)
8. **Security baseline** (IAM policies, encryption, logging)

Each template saves you 4-8 hours per new client. After 5 clients, you've saved 20-40 hours.

## Common Challenges and Solutions

### Challenge 1: Scope Creep

Client keeps asking for "small things" that add up to 20+ extra hours.

**Solution**:
- Define clear scope in the contract
- Track all requests (even "small ones")
- Send a monthly summary: "This month I did 35 hours of work on your $5K/25hr retainer"
- Overage billing: "These 10 hours are over your retainer. I'll proceed at $200/hr unless you say otherwise."
- Raise retainer when average hours consistently exceed commitment

### Challenge 2: Being Treated Like an Employee

Client expects 9-5 availability, daily standups, and timesheets.

**Solution**:
- Set boundaries upfront
- "I work async and handle things within 24 hours on business days"
- Weekly call for sync, everything else is Slack
- If they want employee-like engagement, quote employee-like salary (they won't pay)

### Challenge 3: Knowledge Hoarding

Client has no documentation, everything is tribal knowledge.

**Solution**:
- Write documentation as part of your retainer
- "I'll document everything I work on in Notion"
- Build runbooks for common procedures
- Leave everything better than you found it
- Happy problem: they'll need you more if you document well (job security)

### Challenge 4: Unpaid Invoices

Client pays late or disputes hours.

**Solution**:
- Net-15 terms (not net-30)
- Automatic credit card payments (Stripe)
- Pause work if invoice is 15+ days late
- Late fee (5% after 30 days)
- For large retainers: monthly in advance

## Scaling Your DevOps Retainer Practice

### Solo Operator (Max 5-6 clients)

- 20-30 hours per client per month = 100-150 billable hours
- At $150/hr average = $15-22.5K/month
- Plus projects = $20-35K/month total
- Cap: You're the bottleneck

### With Junior Support (10-15 clients)

- Hire a junior DevOps engineer ($3-6K/month)
- They handle 60-70% of retainer work
- You handle architecture, escalations, client management
- Your effective rate: $200-300/hr (you make money on junior's hours)
- Revenue: 10 clients x $5K = $50K/month
- Cost: $5K junior + $1K tools = $6K
- Profit: $44K/month

### Mini-Agency (20-30 clients)

- 3-5 DevOps engineers
- 1 account manager (handles client communication)
- You: Sales, architecture, business development
- Revenue: 20 clients x $7K average = $140K/month
- Cost: $30K team + $5K tools/overhead = $35K
- Profit: $105K/month

### Efficiency Multipliers

| Investment | Impact | Payback Period |
|-----------|--------|---------------|
| Infrastructure templates | 50% faster onboarding | 1-2 clients |
| Monitoring as code | 80% less manual setup | 2-3 clients |
| Automated reporting | 90% less report writing | 1 month |
| Junior DevOps engineer | 3x client capacity | 2-3 months |
| Client portal | 50% less status call time | 3-4 months |

## Case Study Template

```
# Case Study: DevOps Retainer for [Client]

## The Situation
[Client] was a [stage] SaaS company with [X] engineers.
They had [describe infrastructure state — no CI/CD, manual deploys,
frequent outages, etc.].

## The Engagement
[Client] brought me on as their DevOps retainer at [$X/month].

### Month 1-2: Foundation
- Set up CI/CD pipeline (GitHub Actions → ECR → ECS)
- Terraform'd entire infrastructure
- Set up monitoring and alerts (Datadog)
- Documented everything

### Month 3-6: Optimization
- Reduced deployment time from 45 min to 8 min
- Set up auto-scaling (handles 10x traffic without manual intervention)
- Implemented security scanning (Snyk, Trivy)
- Reduced cloud costs by 35%

### Month 7+: Ongoing
- 2-3 hours/week of maintenance
- Zero major incidents in 12 months
- Engineering team ships 2x faster

## The Results
- [X] hours/year saved for engineering team
- [$Y]/year saved in cloud costs
- Zero security incidents
- 99.99% uptime
- Engineering team focuses on product, not infrastructure

## Client Quote
"[Name] transformed our DevOps. We went from dreading deployments to
deploying multiple times a day with confidence. Our engineering team
is 2x more productive."
```

## Quick-Start Action Plan

### Week 1
- [ ] Define your retainer packages (Essential, Standard, Premium)
- [ ] Write your retainer agreement template
- [ ] Build 3 reusable infrastructure templates
- [ ] Create a portfolio case study (your own infra or a previous client)

### Week 2
- [ ] Identify 20 target companies (SaaS, 5-50 engineers, $1-50M ARR)
- [ ] Find decision-makers on LinkedIn (CTO, VP Eng)
- [ ] Connect and start conversations
- [ ] Post 3 DevOps tips on LinkedIn

### Week 3
- [ ] Send 10 personalized outreach emails
- [ ] Offer free 30-minute infrastructure review
- [ ] Conduct 3 discovery calls
- [ ] Send 2 proposals

### Week 4
- [ ] Close first retainer client
- [ ] Onboard thoroughly (documentation, quick wins)
- [ ] Deliver exceptional results month 1
- [ ] Ask for testimonial and referral

### Month 2-3
- [ ] Close 2 more retainer clients
- [ ] Refine pricing based on feedback
- [ ] Build 3 more reusable templates
- [ ] Start posting regular content

### Month 4-6
- [ ] 5 retainer clients at $5K average = $25K MRR
- [ ] Consider hiring first junior
- [ ] Raise rates 15-25%
- [ ] Target larger clients

## Final Word

DevOps retainers are the closest thing to "passive income" in tech freelancing. Once you build the infrastructure and processes, the ongoing work stabilizes to a few hours per week per client. The relationship deepens over time, switching costs increase, and your income becomes predictable.

The key is getting those first few clients. Once you have a track record and case studies, referrals will sustain your practice.

Start by finding one SaaS company with a messy infrastructure. Offer to fix it. Prove your value. Then scale.
