# SRE Services: Incident Response, Reliability Consulting, SLI/SLO Setup

## Overview

Site Reliability Engineering (SRE) services are among the highest-paying DevOps niches. Companies lose millions from downtime — they'll pay premium rates for reliability expertise.

This guide covers how to freelance as an SRE consultant, the services you can offer, and how to price them.

## Why SRE Consulting Pays Premium Rates

1. **Direct revenue impact**: 1 hour of downtime can cost $100K-$1M+ for enterprise clients
2. **High barrier to entry**: SRE requires deep knowledge of systems, code, and operations
3. **Desperation**: Companies hit by outages will pay anything to prevent recurrence
4. **Scarcity**: Real SREs (not just DevOps rebranded) are genuinely rare
5. **Measurable ROI**: Uptime improvements are directly quantifiable

### Rate Reality

| Service | Junior (3-5yr) | Mid (5-8yr) | Senior (8-12yr) | Expert (12yr+) |
|---------|---------------|-------------|-----------------|----------------|
| Incident Response (hourly) | $100-150/hr | $150-200/hr | $200-300/hr | $300-500/hr |
| On-Call (retainer) | $3-5K/month | $5-8K/month | $8-15K/month | $15-25K/month |
| SLI/SLO Setup (project) | $8-15K | $15-30K | $30-60K | $60-100K |
| Reliability Audit | $10-20K | $20-40K | $40-80K | $80-150K |
| Training/Coaching | $100-150/hr | $150-200/hr | $200-300/hr | $300-500/hr |
| Emergency (firefight) | $200-300/hr | $300-500/hr | $500-1000/hr | $1000-2000/hr |

## SRE vs DevOps: The Distinction

**DevOps**: Focus on automation, CI/CD, infrastructure
**SRE**: Focus on reliability, SLIs, SLOs, error budgets, incident management

As an SRE consultant, you're not just "a DevOps person." You're a reliability engineer who brings a data-driven approach to system reliability.

### Core SRE Principles You Sell

1. **Service Level Indicators (SLIs)**: What you measure (latency, error rate, throughput, availability)
2. **Service Level Objectives (SLOs)**: Your targets (99.9%, 99.99%, 99.999%)
3. **Error Budgets**: The acceptable amount of unreliability (100% - SLO)
4. **Toil reduction**: Automating repetitive operational work
5. **Blameless post-mortems**: Learning from incidents without blame
6. **Capacity planning**: Ensuring systems can handle growth

## Service Offerings

### Service 1: Reliability Audit

**What you do**: Evaluate a client's current reliability posture and provide a roadmap.

**Scope**:
- Current SLIs/SLOs (or lack thereof)
- Incident response process
- Monitoring and alerting quality
- Disaster recovery and backup testing
- Capacity planning
- Toil assessment
- Error budget implementation
- Post-mortem culture

**Deliverables**:
- Reliability scorecard (1-10 across dimensions)
- Critical gaps and risks
- Prioritized improvement roadmap (30/60/90 day)
- Quick wins (things to fix this week)

**Pricing**:
- Small (single service, simple architecture): $8-15K
- Medium (multi-service, moderate complexity): $15-40K
- Large (microservices, high-scale, compliance): $40-100K

**Sample findings** (justifying your fee):
- No SLOs defined — team can't answer "is the system healthy?"
- Alert fatigue — 200 alerts/day, only 5 are actionable
- No disaster recovery testing — recovery plan hasn't been tested in 2 years
- 40% of on-call time is toil (manual, repetitive, automatable)
- No error budget — every outage is a crisis, no data-driven decision making
- Post-mortems blame individuals — systemic issues never get fixed

### Service 2: SLI/SLO Implementation

**What you do**: Define, implement, and operationalize SLIs and SLOs.

**This is the highest-leverage SRE service.** Most engineering teams know they should have SLOs but don't know how to implement them correctly.

**Process**:

**Phase 1: Discovery (1-2 weeks)** — $5-15K
- Map all user journeys and critical paths
- Identify key metrics for each journey
- Define SLIs (Latency, Error Rate, Throughput, Availability)
- Set initial SLO targets based on current performance
- Define error budgets

**Phase 2: Implementation (2-4 weeks)** — $15-30K
- Instrument code for SLI measurement
- Build SLO monitoring dashboards
- Set up alerting based on error budget burn rate
- Implement error budget policy (stop features when budget exhausted)

**Phase 3: Operationalize (2-4 weeks)** — $10-20K
- Train team on SLO-driven decision making
- Set up regular SLO reviews
- Implement automation for error budget enforcement
- Document everything

**Pricing**: $30-60K total for most implementations.

**Common SLI/SLO examples you'll implement**:

| Service Type | SLI | SLO Target | Measurement |
|-------------|-----|-----------|-------------|
| API Service | P99 Latency | 95% of requests < 200ms | Prometheus histograms |
| API Service | Error Rate | < 0.1% errors | Logs or metrics |
| Web App | Page Load | P95 < 3s | RUM (Real User Monitoring) |
| Database | Query Latency | P99 < 100ms | Database metrics |
| Background Jobs | Processing Time | 99% complete within 5 min | Job queue metrics |
| CDN | Availability | 99.99% | External monitoring |

### Service 3: Incident Response Consulting

**What you do**: Improve how a client handles incidents.

**Services**:

**Incident Response Process Design** ($10-25K)
- Define severity levels (SEV1, SEV2, SEV3, SEV4)
- Create incident response runbooks
- Establish communication templates (internal, status page, customer)
- Set up incident management tools (PagerDuty, Opsgenie, FireHydrant)
- Train team on incident commander process

**Post-Mortem Facilitation** ($2-5K per session)
- Facilitate blameless post-mortem after major incidents
- Identify systemic issues (not just "who did what wrong")
- Generate actionable follow-up items
- Track resolution of action items

**On-Call Optimization** ($8-20K)
- Analyze on-call load and distribution
- Reduce alert fatigue (tune alerts, eliminate false positives)
- Implement escalations and rotation
- Improve runbook quality
- Set up automated remediation

### Service 4: Chaos Engineering

**What you do**: Proactively test system reliability by injecting failures.

**This is a differentiator — most SREs don't do this.**

**Approach**:
1. Define steady state (normal system behavior)
2. Hypothesize what will happen when failures occur
3. Run experiments (kill pods, fail AZs, throttle network)
4. Compare results to hypothesis
5. Fix weaknesses discovered

**Tools**: Chaos Mesh, Litmus, Gremlin, AWS Fault Injection Simulator, Azure Chaos Studio

**Pricing**:
- Chaos engineering workshop (2-3 days): $10-20K
- Ongoing chaos program (monthly): $5-10K/month
- Full chaos implementation (quarterly): $25-50K

### Service 5: Capacity Planning

**What you do**: Ensure systems can handle future growth.

**Activities**:
- Analyze current growth trends (traffic, data, users)
- Model future growth scenarios
- Identify bottlenecks before they cause issues
- Recommend scaling strategy (vertical, horizontal, architecture changes)
- Set up auto-scaling and load testing

**Pricing**:
- Basic capacity review: $5-10K
- Full capacity planning engagement: $15-40K
- Ongoing capacity monitoring (retainer): $3-5K/month

### Service 6: Emergency / Firefighting SRE

**What you do**: Jump into an active crisis and stabilize the system.

**This commands premium rates because:**
1. It's high pressure and high stakes
2. You need deep experience across many systems
3. The client is desperate

**Pricing**:
- Emergency response: $500-1000/hr (during crisis)
- Stabilization period: $300-500/hr (first week post-crisis)
- Follow-up: Standard rates after stabilization

**What you deliver**:
- Immediate: Triage and stabilize
- Short-term: Root cause analysis and hotfix
- Medium-term: Long-term fix and prevention plan
- Long-term: Architecture recommendations

## Technical Skills Required

### Core SRE Skills

1. **Monitoring and observability**:
   - Prometheus + Grafana (open-source standard)
   - Datadog / New Relic (SaaS)
   - Distributed tracing (Jaeger, Tempo, Honeycomb)
   - Log aggregation (ELK, Loki, Splunk)

2. **Incident management**:
   - PagerDuty / Opsgenie / FireHydrant
   - Status page tools (Statuspage, Instatus)
   - Runbook automation (Rundeck, FireHydrant)

3. **Kubernetes and containers**:
   - Deployment, scaling, monitoring, debugging
   - Service mesh (Istio, Linkerd)
   - Chaos engineering tools

4. **Cloud platforms**:
   - AWS, GCP, or Azure at depth
   - Auto-scaling, load balancing, disaster recovery
   - Cost optimization

5. **Scripting and automation**:
   - Python (primary — for automation, analysis, tooling)
   - Go (for high-performance tooling)
   - Bash (for quick scripts)

6. **Database operations**:
   - Performance tuning, query optimization
   - Backup and recovery
   - Replication and failover

### SRE-Specific Knowledge (Differentiator)

1. **SLI/SLO theory**: Know the Google SRE book inside and out
2. **Error budget math**: Understand burn rate, budget depletion, multi-window approaches
3. **Queueing theory**: Understand how queues affect latency and throughput
4. **Reliability math**: Understand availability calculations, Nines, dependencies
5. **Chaos engineering**: Proactive failure testing
6. **Post-mortem facilitation**: Blameless culture, systems thinking

### Certifications That Matter

- **Google Professional Cloud DevOps Engineer** (most relevant — Google invented SRE)
- **AWS DevOps Engineer Professional**
- **Certified Kubernetes Administrator (CKA)**
- **Prometheus Certified Associate**

## Client Acquisition

### Where SRE Clients Come From

**1. Incident-driven inbound** (40% of engagements)
- Company has a major outage
- They realize they need SRE expertise
- You're introduced through network or they find you through content
- **How to capture this**: Write about post-mortems, reliability patterns

**2. Referrals** (30%)
- Past clients whose reliability improved
- Other consultants who see reliability gaps
- **How to build**: Every engagement → ask for referrals

**3. Content marketing** (20%)
- Blog posts about SRE topics
- Conference talks (SREcon, KubeCon, DevOps Days)
- Open-source SRE tools
- **How to start**: Write case studies about reliability improvements

**4. Direct outreach** (10%)
- Target companies that have had recent public outages
- Target companies hiring for SRE roles (they need help NOW)
- **How to approach**: "I saw your recent outage. Here's what I would have done differently."

### Ideal Client Profile

- SaaS companies with 20-200 engineers
- High reliability requirements (fintech, healthcare, e-commerce)
- $10M+ ARR (can afford premium rates)
- Current SRE maturity: "We have some monitoring but no SLOs"
- Pain: Unreliable systems, alert fatigue, on-call burnout

### Outreach Script (Incident-Driven)

```
Subject: [Company] reliability

Hi [Name],

I noticed [Company] had an incident on [date]. These are always
painful.

I specialize in helping growing SaaS companies build reliability
systems before the next crisis.

Specifically, I help teams:
1. Define and measure SLIs/SLOs (so you know when you're healthy)
2. Implement error budgets (so reliability is a business decision)
3. Reduce on-call burnout (by eliminating alert fatigue)
4. Build effective incident response (so outages are shorter)

I'd be happy to do a 30-minute reliability review — no obligation.

Does this sound valuable?

Best,
[Your Name]
[Link to SRE case studies or blog]
```

## Pricing SRE Services

### Value-Based Pricing Examples

**Example 1: Reliability Audit**
```
Client loses $100K per hour of downtime.
Current uptime: 99.5% (3.65 days of downtime per year).
My recommendations will improve to 99.9% (8.76 hours of downtime per year).
Savings: 3.34 days x 24 hours x $100K = $8M/year.
My fee: $80K (1% of savings).
```

**Example 2: On-Call Optimization**
```
Client has 5 engineers on-call, each spending 10 hours/week on toil.
Cost: 5 x 10 hrs x 50 weeks x $100/hr (loaded cost) = $250K/year.
My retainer of $15K/month = $180K/year.
I promise to reduce toil by 50% = $125K/year savings.
Net savings to client: $125K - $180K = ... first year is break-even.
But engineers get 50% of their time back. Productivity increase worth >$250K.
And you keep the retainer going (ongoing savings).
```

**Actual numbers from my practice**: A $30K SLO implementation for a Series B SaaS. Client had 4 major incidents in the previous quarter (each costing ~$50K in engineering time and customer churn). After SLO implementation and error budget policy: zero major incidents in the following quarter. ROI was immediate.

### Rate Benchmarks by Service Type

| Service | Hourly Rate | Project Rate | Retainer |
|---------|-------------|-------------|----------|
| Reliability Audit | $200-400/hr | $10-50K | N/A |
| SLO Implementation | $200-350/hr | $20-80K | N/A |
| Incident Response | $250-500/hr | N/A | $5-15K/month |
| On-Call Support | $150-250/hr | N/A | $5-20K/month |
| Chaos Engineering | $200-400/hr | $15-50K | $5-10K/month |
| Training/Mentoring | $200-350/hr | $5-20K | $3-8K/month |
| Emergency | $500-2000/hr | N/A | N/A |

## Toolkit

### Essential SRE Tools

| Category | Tools |
|----------|-------|
| Metrics | Prometheus, VictoriaMetrics, M3DB |
| Dashboards | Grafana |
| Logging | Loki, ELK Stack, Splunk |
| Tracing | Jaeger, Tempo, Honeycomb |
| Alerting | Alertmanager, PagerDuty, Opsgenie |
| Incident Mgmt | FireHydrant, Incident.io, Rootly |
| Runbooks | FireHydrant, Rundeck |
| Chaos | Chaos Mesh, Litmus, Gremlin |
| Load Testing | k6, Locust, Artillery |
| Kubernetes | kubectl, Helm, Istio, Linkerd |
| SLO tooling | Sloth, Pyrexia, Nobl9 |
| Status pages | Instatus, Statuspage, Checkly |

### Your SRE Arsenal (Create These)

Build reusable templates for:
1. **SLO definition template** (covering common service types)
2. **Error budget policy** (template for what happens when budget runs out)
3. **Post-mortem template** (blame-free, systems-oriented)
4. **Incident severity matrix** (clear definitions for SEV1-4)
5. **On-call runbook template** (rotations, escalation, handoff)
6. **Reliability scorecard** (assessment framework for audits)
7. **Prometheus recording rules** (for common SLO calculations)
8. **Grafana dashboard templates** (SLO burn rate, error budget, etc.)

## Sample Project Lifecycle

### SLO Implementation (8 weeks, $40K)

**Week 1-2: Discovery**
- Map system architecture and user journeys
- Interview team about current reliability practice
- Review existing monitoring and alerting
- Define initial SLIs and SLOs

**Week 3-4: Instrumentation**
- Add SLI measurement to services (latency, errors, throughput)
- Set up Prometheus recording rules for SLO calculation
- Build Grafana dashboards for SLO tracking
- Implement error budget calculation

**Week 5-6: Alerting and Policy**
- Set up multi-window, multi-burn-rate alerting
- Implement error budget policy
- Define on-call escalation for SLO violations
- Train team on SLO-driven decision making

**Week 7-8: Operationalize**
- Run SLO review with stakeholders
- Document everything
- Handoff to team
- 30-day support and adjustment period

### Sample SLO Implementation Proposal

```
# SLO Implementation Proposal — [Client]

## Problem
[Client] currently has no structured approach to reliability. The team
can't answer "Is the system healthy enough to deploy?" or "What level
of reliability do our customers actually need?"

## Solution
Implement SLIs, SLOs, and error budgets across [X] critical services.

## Scope
1. Define SLIs and SLOs for [X] services (API, web app, background jobs)
2. Instrument code for SLI measurement
3. Build SLO monitoring dashboards in Grafana
4. Implement error budget burn-rate alerting
5. Define error budget policy
6. Train team on SLO operations

## Timeline: 8 weeks

## Investment: $40K

## Deliverables
- SLO documentation for all services
- Production-ready SLI instrumentation
- Grafana SLO dashboards
- Error budget policy document
- Alert configuration
- Team training session

## Success Metrics
- All X services have defined and measured SLOs
- Error budget burn rate alerts in place
- Team uses error budget for deployment decisions
- Reduced incident response time (baseline now, measure in 3 months)

## Risk Mitigation
- Schedule buffer for unexpected instrumentation challenges
- Close collaboration with team for SLI definition
- Post-implementation support for 30 days
```

## Case Study Template

```
# Case Study: SLO Implementation for [Client]

## The Challenge
[Client] was experiencing frequent outages with no way to measure
reliability. The team was reactive — they knew they had problems
but couldn't quantify them. On-call was burning out engineers.

## The Solution
Over 8 weeks, I:
1. Defined SLIs and SLOs for 5 critical services
2. Instrumented code to measure latency, errors, and availability
3. Built Grafana dashboards showing real-time SLO status
4. Implemented error budget burn-rate alerting
5. Created error budget policy (team stops shipping when budget runs out)

## The Results
- 85% reduction in SEV2+ incidents (from 20/quarter to 3/quarter)
- On-call burden reduced 60% (less false alarms, better runbooks)
- Engineering team ships with confidence: "We know when it's safe to deploy"
- Error budget gives leadership data-driven decisions about reliability vs features

## Technologies Used
Prometheus, Grafana, Sloth (SLO generator), PagerDuty, FireHydrant

## Client Quote
"Before, reliability was a feeling. Now it's a number we can track,
discuss, and improve. This was the best investment we've made in our
infrastructure."
```

## Quick-Start Action Plan

### Week 1-2: Foundation
- [ ] Read Google SRE book (if you haven't) — it's the SRE bible
- [ ] Read SRE Workbook (practical implementation patterns)
- [ ] Set up your own SLO stack (Prometheus + Grafana + Sloth)
- [ ] Write a blog post about SLO implementation

### Week 3-4: Visibility
- [ ] Create SRE-focused LinkedIn profile
- [ ] Publish 1-2 case studies (even from past roles)
- [ ] Join SRE communities (SRE community Discord, r/SRE)
- [ ] Attend SREcon or local DevOps/SRE meetup

### Week 5-8: First Engagement
- [ ] Offer a free 30-minute reliability review to 5 prospects
- [ ] Conduct 3 discovery calls
- [ ] Land first paid engagement ($10-20K audit)
- [ ] Deliver exceptional value

### Month 3-6: Build Practice
- [ ] Complete 2-3 engagements
- [ ] Develop reusable templates and frameworks
- [ ] Raise rates 25%
- [ ] Build referral pipeline
- [ ] Submit talk to SREcon or DevOpsDays

### Month 7-12: Establish
- [ ] Known as SRE expert in your niche
- [ ] 2-3 retainer clients ($5-15K/month each)
- [ ] Inbound leads from content and referrals
- [ ] Consider scaling (hire junior SRE, partner with MSP)

## Final Word

SRE consulting is the pinnacle of infrastructure freelancing. It requires deep knowledge, but the rewards are correspondingly high — both financially and intellectually.

The key insight: Most companies need SRE expertise but can't hire a full-time SRE (too expensive, too scarce). You bridge that gap as a consultant.

Focus on SLO implementation as your core service. It's the highest-impact, highest-value, and most repeatable engagement. Once SLIs/SLOs are in place, everything else (incident response, on-call, chaos engineering) flows naturally from the data.

Start with the Google SRE book. Implement what you learn. Then sell that expertise to companies that need it.
