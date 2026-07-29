# Technical Architecture Consulting: System Design, Scalability, Tech Stack

## Overview

Technical architecture consulting is where senior engineers command $200-500+/hr by providing strategic guidance rather than writing code. Companies pay for your judgment on which technologies to use, how to structure systems, and how to scale.

This guide covers the specific services, pricing strategies, and client acquisition for architecture consulting.

## Why Architecture Consulting Pays the Most

1. **Experience is the product**: You sell your judgment, not your coding speed
2. **High leverage**: One good architecture decision saves months of rework
3. **C-suite audience**: You talk to CTOs, VPs of Engineering — not individual contributors
4. **No implementation risk**: You advise; they implement (you're not on the hook for bugs)
5. **Scalable**: With good frameworks, you can serve multiple clients simultaneously

### Rate Reality

| Service | Senior (8-12yr) | Expert (12-15yr) | Principal (15yr+) | Legend (20yr+) |
|---------|-----------------|-----------------|-------------------|----------------|
| Architecture Review | $175-250/hr | $250-350/hr | $350-500/hr | $500-750/hr |
| System Design | $200-300/hr | $300-400/hr | $400-600/hr | $600-1000/hr |
| Tech Stack Advisory | $200-300/hr | $300-450/hr | $450-650/hr | $650-1000/hr |
| Scalability Audit | $200-300/hr | $300-450/hr | $450-650/hr | $650-1000/hr |
| Fractional CTO | $175-250/hr | $250-350/hr | $350-500/hr | $500-800/hr |
| Due Diligence | $200-300/hr | $300-400/hr | $400-600/hr | $600-1000/hr |

## Service Offerings

### Service 1: Architecture Review

**What you do**: Review existing system architecture and provide recommendations.

**Common triggers**:
- System is slow / crashing under load
- Team is struggling to add features
- Technical debt is blocking progress
- Team wants to validate their architecture before building
- Due diligence for acquisition/investment

**Review scope**:
- System architecture (monolith, microservices, serverless)
- Database design (schema, indexing, query patterns)
- API design (REST, GraphQL, gRPC)
- Data flow and processing
- Security architecture
- Deployment and infrastructure
- Code quality and testing strategy
- Scalability and performance

**Deliverables**:
- Executive summary (1 page) — top findings and recommendations
- Detailed report — findings with evidence, impact, and recommendations
- Architecture diagram (current and target state)
- Prioritized roadmap (quick wins, medium-term, long-term)

**Pricing**:
- Light review (1 system, 2-3 days): $5-10K
- Standard review (2-5 systems, 1 week): $10-25K
- Deep review (full platform, 2-3 weeks): $25-60K
- Due diligence (for investors/acquirers): $30-80K

### Service 2: System Design for New Products

**What you do**: Design the architecture for new systems from scratch.

**This is where you have the most impact** — the right architecture from day one saves millions.

**Process**:

**Phase 1: Discovery (1-2 weeks)** — $10-20K
- Requirements gathering
- User story mapping
- Traffic estimates (current and projected)
- Constraints (budget, timeline, team skills)
- Non-functional requirements (latency, availability, durability, consistency)

**Phase 2: Architecture Design (2-4 weeks)** — $15-40K
- System architecture (components, interactions, data flow)
- Technology selection (database, compute, messaging, storage)
- Data model design
- API design
- Security architecture
- Deployment architecture
- Monitoring and observability

**Phase 3: Documentation and Handoff (1-2 weeks)** — $5-15K
- Architecture decision records (ADRs)
- Detailed architecture diagrams
- Implementation roadmap
- Team onboarding session

**Pricing**: $30-75K for full system design

### Service 3: Scalability Audit and Optimization

**What you do**: Identify bottlenecks and design solutions for scaling.

**Common clients**: Growing startups hitting performance walls. Their app works for 100 users but falls apart at 10K.

**Audit areas**:
- Database performance (slow queries, N+1 problems, connection pooling)
- Caching strategy (what to cache, where, invalidation)
- Async processing (background jobs, queues, event-driven)
- CDN and edge caching
- Microservices boundaries (wrong splits cause cross-service queries)
- Frontend performance (bundle size, rendering, code splitting)
- Infrastructure (auto-scaling, instance sizing, regional distribution)

**Deliverables**:
- Performance benchmark (current capacity)
- Bottleneck analysis
- Scaling recommendations (vertical, horizontal, architectural)
- Implementation roadmap

**Pricing**: $15-40K for scalability audit

**Sample findings** (justifying your fee):
- "Your database queries are doing tabel scans on a 10M-row table because of a missing index. Adding it will reduce query time from 2 seconds to 2 milliseconds."
- "You're using the monolith database as a message queue (polling table). Switching to a proper queue (SQS, RabbitMQ, Kafka) will handle 100x current load."
- "Your API returns 500KB of data when the UI only needs 10KB. GraphQL or field selection reduces bandwidth 50x."
- "Your frontend bundle is 5MB. Code splitting + tree shaking reduces it to 500KB."

### Service 4: Tech Stack Advisory

**What you do**: Help clients choose the right technologies for their needs.

**Why clients need this**:
- Too many options (React vs Vue vs Svelte, SQL vs NoSQL, monolith vs microservices)
- Previous bad decision (chose MongoDB when they needed PostgreSQL, chose microservices when they didn't have the team)
- CTO lacks experience with certain technologies
- Need to standardize across multiple teams

**Advisory areas**:
- **Frontend**: React vs Vue vs Svelte, Next.js vs Remix, state management
- **Backend**: Node vs Python vs Go vs Rust, framework selection
- **Database**: PostgreSQL vs MySQL vs MongoDB, SQLite vs server-based
- **Infrastructure**: AWS vs Azure vs GCP, serverless vs containers
- **Architecture**: Monolith vs microservices vs serverless
- **Mobile**: Native vs cross-platform

**Deliverables**:
- Technology comparison with pros/cons/risks
- Recommendation with rationale
- Migration plan (if switching from existing stack)

**Pricing**: $10-25K for tech stack advisory

### Service 5: Fractional CTO / Technical Advisor

**What you do**: Act as the client's part-time technical leader.

**Who needs this**:
- Startups too small for a full-time CTO ($250K+/year)
- Companies between CTOs (interim role)
- Technical founders who need mentorship
- Companies raising funds (investors want to see technical leadership)

**Activities**:
- Technical strategy and roadmap
- Architecture oversight
- Code review and quality standards
- Hiring technical talent (interviewing, job descriptions)
- Team structure and process
- Engineering budget planning
- Board/investor technical reporting
- Vendor evaluation and selection

**Engagement**:
- 10-30 hours/month (flexible)
- Weekly 1:1 with engineering leadership
- Monthly board/investor updates
- On-call for major decisions

**Pricing**:
- Advisory (10 hrs/month): $5-10K/month
- Active (20 hrs/month): $10-20K/month
- Intensive (30-40 hrs/month): $20-35K/month

### Service 6: Technical Due Diligence

**What you do**: Evaluate a company's technology for investors or acquirers.

**Who hires you**:
- Venture capital firms considering investment
- Companies considering acquisition
- PE firms doing buyout due diligence

**What you evaluate**:
- Architecture quality and scalability
- Code quality and technical debt
- Engineering team quality and processes
- Security posture
- Infrastructure costs and efficiency
- Technical risks and liabilities
- IP and proprietary technology

**Deliverables**:
- Technical due diligence report
- Risk assessment
- Recommended action items
- Valuation impact analysis

**Pricing**: $20-60K per engagement

## Client Acquisition

### Where Architecture Clients Come From

**1. CTO referrals** (50%+)
- CTOs know other CTOs who need help
- **Build**: Deliver exceptional value to every client, ask for referrals

**2. Investor referrals** (20%)
- VCs need technical due diligence for portfolio companies
- **Build**: Network with VC firms, offer pro-bono first engagement

**3. Content marketing** (15%)
- Blog posts about system design, scalability, architecture decisions
- Conference talks (QCon, Strange Loop, LeadDev, SREcon)
- Open-source architecture templates

**4. Direct outreach** (10%)
- Target companies that just raised Series A/B (they need architecture now)
- Target companies with public scaling problems (downtime, slow performance)

**5. Consulting firms** (5%)
- McKinsey, BCG, Deloitte — they need technical experts for projects

### Ideal Client Profile

**Startup (seed to Series A)** — $10-30K engagements
- 1-20 engineers
- Need architecture designed before building
- CTO is technical but may lack experience at scale
- Fast decisions, fast money

**Growth stage (Series A to C)** — $20-60K engagements
- 20-100 engineers
- Scaling problems emerging
- Architecture from early days no longer works
- Experienced CTO who knows they need help

**Enterprise** — $30-100K+ engagements
- 100+ engineers
- Legacy architecture, digital transformation
- Slow decisions, but large budgets
- Need consensus-building across teams

### Outreach Script

```
Subject: Architecture review for [Company]

Hi [Name],

I'm a technical architect who helps growing companies
design systems that scale.

I noticed [Company] is [growing fast / hitting performance
issues / building a new platform]. Most companies at this
stage benefit from an outside architecture review.

I recently worked with a similar company and found:
- 200ms database queries were actually full table scans
  (missing index — fixed in 1 hour)
- Auth was a bottleneck for all services (moved to
  centralized auth service)
- Unnecessary microservices adding latency (consolidated
  into 2 services)

I'd be happy to do a free 30-minute architecture review
— no strings attached.

Best,
[Your Name]
[Company / Portfolio link]
```

## Pricing Strategy

### Value-Based Pricing Examples

**Example: Architecture Review**
```
Client: Series A SaaS with 50 engineers
Pain: Deployments take 3 days, scaling is hitting limits
Your fee: $25K for architecture review
If you save them 3 days per deployment (12/year) at
$200K/engineer/year for 50 engineers:
Savings: 10 minutes/engineer per deployment avoided =
12 deployments x 50 engineers x 10 minutes x $100/hr =
$100K/year in reclaimed productivity
Your fee is 25% of the first year's savings
```

**Example: System Design**
```
Client: Building a new SaaS platform
Your fee: $50K for system design
Cost of getting architecture wrong:
- 6 months of rework = $1M+ in engineering costs
- 3 months delayed time-to-market = $500K in lost revenue
- Developer frustration = turnover costs
Your fee is 3% of the cost of getting it wrong
```

### Retainer vs Project

| Model | Best For | Pros | Cons |
|-------|---------|------|------|
| Project | Defined scope (review, design) | Clear boundaries, fixed price | Doesn't capture ongoing value |
| Hourly | Ad-hoc advice, Q&A calls | Simple, flexible | Harder to sell value |
| Retainer | Fractional CTO, ongoing advisory | Predictable income, deep relationship | Availability expectations |
| Value-based | High-ROI engagements | Highest earnings | Hardest to sell |

## Tools of the Trade

### Architecture Documentation

- **Diagrams**: Draw.io, Excalidraw, LucidChart, Miro
- **ADRs**: Architecture Decision Records (adr.github.io)
- **Documentation**: Notion, Confluence, GitBook
- **Architecture frameworks**: C4 model (context, containers, components, code)

### Case Study Template

```
# Case Study: Architecture Review for [Company]

## The Challenge
[Company] was experiencing [performance/scalability/velocity]
issues. Their [system/architecture] couldn't handle growth.

## Our Approach
1. Reviewed current architecture (code, infra, data flow)
2. Benchmarked performance under load
3. Interviewed engineering team (pain points, bottlenecks)
4. Identified top issues (with evidence)

## Key Findings
### Critical
1. [Finding] — [Impact] — [Recommendation]
2. [Finding] — [Impact] — [Recommendation]

### Important
3. [Finding] — [Impact] — [Recommendation]
4. [Finding] — [Impact] — [Recommendation]

## The Results
- Deploy time reduced from 3 days to 2 hours
- P95 latency reduced from 2s to 200ms
- Team velocity increased 3x
- Infrastructure costs reduced 40%

## Client Quote
"[Name]'s architecture review was eye-opening. We knew
we had problems, but couldn't see the forest for the
trees. His recommendations were practical and impactful."
```

## Quick-Start Action Plan

### Month 1: Foundation
- [ ] Define your architecture consulting methodology
- [ ] Create templates (ADRs, architecture diagrams, review framework)
- [ ] Build case studies (from past projects or create sample ones)
- [ ] Write 3 blog posts about architecture decisions

### Month 2: Visibility
- [ ] Optimize LinkedIn for "Technical Architect" / "Software Architect"
- [ ] Speak at 1-2 meetups or conferences
- [ ] Join CTO/architect communities
- [ ] Publish architecture decision framework

### Month 3: First Client
- [ ] Offer free 30-minute architecture review to 5 prospects
- [ ] Convert 1-2 to paid engagements ($10-25K)
- [ ] Deliver exceptional value
- [ ] Ask for referrals

### Month 4-6: Build Practice
- [ ] Complete 3-5 engagements
- [ ] Develop repeatable frameworks and templates
- [ ] Raise rates 25%
- [ ] Build referral partnerships (VCs, CTOs, consulting firms)

### Month 7-12: Establish
- [ ] Known as architecture expert in your niche
- [ ] Fractional CTO retainer ($15-25K/month)
- [ ] Inbound leads from content and referrals
- [ ] Consider writing a book or creating a course

## Final Word

Technical architecture consulting is the highest-leverage freelancing niche. You don't write code — you guide architecture decisions that affect millions of dollars in engineering investment.

Your value comes from experience. Every architecture mistake you've seen (and made) is a data point that helps your clients avoid the same mistake.

Build your reputation through content and referrals. Focus on delivering clear, actionable recommendations. Your rates will follow your reputation.

The best part: As you get older and more experienced, your rates go UP (unlike coding, where age is a liability in some markets). A 20-year architect at $500-1000/hr is common.
