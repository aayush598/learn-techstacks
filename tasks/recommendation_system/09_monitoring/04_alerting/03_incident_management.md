# Incident Management for Recommendation Systems

## 1. Overview

Incident management is the structured process for detecting, triaging, resolving, and learning from service disruptions. For recommendation systems, incidents directly impact user experience and revenue — every minute of downtime or degradation translates to lost engagement and sales. A mature incident management process reduces MTTR, prevents repeat incidents, and builds organizational resilience.

### 1.1 Incident Definition

An incident is any unplanned event that causes:
- Service degradation or outage
- Data quality issues affecting recommendations
- User-facing errors or incorrect behavior
- Security or compliance violations
- Revenue or engagement loss

### 1.2 Incident Management Goals

| Goal | Metric | Target |
|---|---|---|
| Detection time | Time from incident start to alert | <5 minutes |
| Acknowledgment time | Time from alert to human response | <5 min (P0), <15 min (P1) |
| Time to mitigate | Time from detection to user impact resolved | <30 min (P0), <2 hr (P1) |
| Time to resolve | Time from detection to root cause fixed | <4 hr (P0), <24 hr (P1) |
| Postmortem completion | P0/P1 incidents with postmortem | 100% within 5 business days |
| Repeat incident rate | Same root cause causing multiple incidents | <5% |

---

## 2. Severity Classification

### 2.1 Impact Assessment Matrix

| Impact维度 | P0 - Critical | P1 - High | P2 - Medium | P3 - Low |
|---|---|---|---|---|
| User impact | >10% users affected | 5-10% users affected | 1-5% users affected | <1% users affected |
| Revenue impact | >$10K/hour lost | $1K-10K/hour lost | $100-1K/hour lost | <$100/hour lost |
| Data integrity | Data loss or corruption | Data delayed or stale | Data partially incorrect | Minor data quality issue |
| Service availability | Complete outage | Major degradation | Partial degradation | Minor issue |
| Compliance | Active violation | Potential violation | Risk identified | No compliance impact |

### 2.2 Recommendation System Specific Incidents

| Incident Type | Typical Severity | Example |
|---|---|---|
| All recommendations failing | P0 | Model server crash, feature store down |
| High error rate (>5%) | P1 | Model inference timeout, index corruption |
| High latency (>2s P99) | P1-P2 | Database slow query, cache eviction storm |
| Feature staleness (>5 min) | P2 | Kafka lag, batch job failure |
| Incorrect recommendations | P1-P0 | Model trained on wrong data, feature pipeline bug |
| A/B test misconfiguration | P2 | Wrong traffic split, metric collection broken |
| Coverage drop (>20%) | P2-P3 | Index shard failure, catalog ingestion delay |

---

## 3. Incident Commander Role

### 3.1 Incident Commander Responsibilities

The Incident Commander (IC) owns the incident process (not necessarily the technical fix):

| Phase | IC Responsibility |
|---|---|
| Detection | Validate alert, confirm incident, declare severity |
| Triage | Assign roles (investigator, communicator, scribe) |
| Communication | Internal status updates, external communication |
| Coordination | Bring in experts, manage escalation, unblock teams |
| Resolution | Confirm mitigation, verify recovery, close incident |
| Postmortem | Schedule postmortem, assign action items, track completion |

### 3.2 IC Selection

| Severity | IC Assignment |
|---|---|
| P0 | Engineering manager or senior engineer |
| P1 | Team lead or senior on-call engineer |
| P2 | On-call engineer (self-managed) |
| P3 | On-call engineer (self-managed) |

### 3.3 IC Decision Framework

```
1. Is this a real incident? (not a false alarm)
2. What is the user impact? (severity classification)
3. Who needs to be involved? (domain experts, stakeholders)
4. What is the mitigation plan? (quickest path to recovery)
5. What communication is needed? (internal, external, status page)
6. Is escalation needed? (based on timeout and complexity)
```

---

## 4. Communication Templates

### 4.1 Incident Declaration Template

```
INCIDENT DECLARED
=================
Severity: [P0/P1/P2]
Incident ID: [INC-YYYY-MMDD-NNN]
Incident Commander: [Name]
Start Time: [UTC timestamp]
Impact: [Description of user/business impact]
Services Affected: [List of affected services]

Status: INVESTIGATING
Next Update: [Time]

Slack Channel: #incident-[INC-ID]
War Room: [Link to video call]
```

### 4.2 Status Update Template

```
INCIDENT UPDATE #[N]
====================
Time: [UTC timestamp]
Duration: [Time since incident start]
Status: [Investigating | Identified | Monitoring | Resolved]

What we know:
- [Key finding 1]
- [Key finding 2]

What we're doing:
- [Current action 1]
- [Current action 2]

Next update: [Time]
```

### 4.3 Resolution Template

```
INCIDENT RESOLVED
==================
Incident ID: [INC-YYYY-MMDD-NNN]
Resolution Time: [UTC timestamp]
Duration: [Total incident duration]
Root Cause: [Brief description]
Impact Summary:
- Users affected: [Number/percentage]
- Duration of impact: [Time]
- Revenue impact: [Estimated amount]

Resolution:
- [What was done to fix the issue]
- [Mitigations applied]

Follow-up:
- Postmortem scheduled: [Date]
- Action items: [Link to tracking]
```

### 4.4 External Communication Template (Status Page)

```
[Investigating] We are investigating issues with personalized recommendations.
Some users may experience slower than usual load times or generic recommendations.

Started: 14:23 UTC
Impact: Some users affected
Next update: 14:53 UTC

---

[Identified] We have identified the issue as a problem with our recommendation 
model serving infrastructure. We are working on a mitigation.

---

[Resolved] The issue has been resolved. Personalized recommendations are now 
functioning normally. We will provide a full postmortem within 5 business days.

Duration: 47 minutes
```

---

## 5. Status Pages

### 5.1 Status Page Design

| Component | Description | Update Frequency |
|---|---|---|
| Overall status | Operational / Degraded / Outage | Per incident |
| Service components | Recommendation API, Feature Pipeline, Model Serving, etc. | Per incident |
| Incident history | List of recent incidents with timeline | Per incident |
| Scheduled maintenance | Planned maintenance windows | As scheduled |
| Subscribe options | Email, Slack, webhook notifications | Real-time |

### 5.2 Status Page for Recommendation Systems

```
Component Status:
  Recommendation API:     [Operational]
  Feature Pipeline:       [Operational]
  Candidate Generation:   [Degraded Performance]  <-- Current issue
  Model Serving:          [Operational]
  Event Processing:       [Operational]
  A/B Testing Platform:   [Operational]
```

### 5.3 Status Page Providers

| Provider | Cost | Features | Best For |
|---|---|---|---|
| Statuspage (Atlassian) | $29+/mo | Integrations, sub-components | Small-medium teams |
| Instatus | $20+/mo | Modern UI, AI summaries | Growing teams |
| Cachet (self-hosted) | Free | Open source, customizable | Budget-conscious |
| Custom (Grafana) | Free | Full control, Prometheus integration | Technical teams |

---

## 6. Blameless Postmortems

### 6.1 Postmortem Principles

1. **Blameless**: Focus on systems and processes, not individuals
2. **Written**: Document findings in a structured format
3. **Timely**: Complete within 5 business days of incident resolution
4. **Actionable**: Every finding has an associated action item
5. **Shared**: Postmortems are read by the team and leadership

### 6.2 Postmortem Template

```
POSTMORTEM: [Incident Title]
================================
Incident ID: [INC-YYYY-MMDD-NNN]
Date: [Incident date]
Author: [Author name]
Reviewers: [List of reviewers]

EXECUTIVE SUMMARY
- Impact: [1-2 sentence summary of impact]
- Duration: [Total duration]
- Root Cause: [1-2 sentence root cause]
- Resolution: [How it was resolved]

TIMELINE (UTC)
14:23 - Alert fires for high error rate
14:24 - On-call engineer acknowledges
14:26 - Investigating, identified feature service timeout
14:30 - Mitigated by increasing timeout threshold
14:35 - Monitoring, confirmed recovery
14:45 - Incident resolved

ROOT CAUSE ANALYSIS
- What happened: [Detailed technical explanation]
- Why it happened: [Root cause chain]
- Why it wasn't caught earlier: [Detection gap analysis]

IMPACT ANALYSIS
- Users affected: [Number]
- Duration: [Minutes]
- Revenue impact: $[Amount]
- Data impact: [Any data quality issues]

WHAT WENT WELL
1. [Positive aspect 1]
2. [Positive aspect 2]

WHAT WENT WRONG
1. [Negative aspect 1]
2. [Negative aspect 2]

WHERE WE GOT LUCKY
1. [Lucky factor 1]

ACTION ITEMS
| # | Action | Owner | Priority | Due Date | Status |
|---|--------|-------|----------|----------|--------|
| 1 | Add circuit breaker to feature service | Alice | P1 | 2026-08-26 | Open |
| 2 | Add feature freshness monitoring | Bob | P1 | 2026-08-26 | Open |
| 3 | Update runbook for feature service failures | Carol | P2 | 2026-09-02 | Open |

LESSONS LEARNED
- [Key takeaway 1]
- [Key takeaway 2]
```

### 6.3 Postmortem Quality Checklist

- [ ] Executive summary is clear and concise
- [ ] Timeline is accurate with UTC timestamps
- [ ] Root cause analysis goes beyond surface symptoms
- [ ] Action items are specific, assigned, and time-bound
- [ ] No blame language (no "Bob forgot to..." or "due to human error")
- [ ] Focuses on systemic improvements, not individual mistakes
- [ ] Reviewed by at least one person not involved in the incident
- [ ] Shared with relevant stakeholders

---

## 7. Action Item Tracking

### 7.1 Action Item Categories

| Category | Description | Priority |
|---|---|---|
| Prevention | Changes to prevent similar incidents | High |
| Detection | Improvements to alerting and monitoring | High |
| Mitigation | Faster recovery mechanisms | Medium |
| Communication | Better incident communication | Medium |
| Documentation | Updated runbooks and procedures | Low |

### 7.2 Action Item Lifecycle

```
Created -> Assigned -> In Progress -> In Review -> Completed -> Verified
                                                         |
                                                     -> Reopened (if verification fails)
```

### 7.3 Action Item Tracking Dashboard

Track action item completion across incidents:

```
Open Action Items: 23
Overdue Action Items: 5
Completion Rate (last 30 days): 78%
Average Time to Complete: 8 days

By Priority:
  P1 (Critical): 3 open, 0 overdue
  P2 (High): 10 open, 2 overdue
  P3 (Medium): 8 open, 3 overdue
  P4 (Low): 2 open, 0 overdue
```

### 7.4 Action Item Review Process

- **Weekly**: Team reviews open and overdue items
- **Monthly**: Engineering manager reviews completion rates
- **Quarterly**: Leadership reviews trends and systemic issues

---

## 8. SLA Impact Calculation

### 8.1 SLA Definitions for Recommendation Systems

| SLA | Target | Measurement |
|---|---|---|
| Availability | 99.95% | Uptime / (Uptime + Downtime) |
| Latency | 99.9% of requests < 200ms | Requests within SLO / Total requests |
| Correctness | 99% of recommendations are valid | Valid recommendations / Total recommendations |
| Freshness | Feature data < 5 min old | Fresh requests / Total requests |

### 8.2 SLA Breach Calculation

```
Monthly SLA Target: 99.95% availability
Allowed downtime per month: 0.05% × 30 days × 24 hours = 21.6 minutes

Incident impact:
- Downtime: 47 minutes
- SLA remaining after incident: 99.95% - (47 / (30 × 24 × 60)) × 100%
- SLA remaining: 99.95% - 0.11% = 99.84% (BREACH)
```

### 8.3 SLA Impact Dashboard

| Metric | Target | Current Month | Status |
|---|---|---|---|
| Availability | 99.95% | 99.87% | AT RISK |
| Latency SLO | 99.9% | 99.92% | OK |
| Correctness | 99% | 99.4% | OK |
| Freshness | 99.5% | 99.1% | AT RISK |
| Error budget remaining | >50% | 34% | WARNING |

---

## 9. Incident Management Tools

### 9.1 Tool Stack

| Tool | Purpose | Examples |
|---|---|---|
| Alerting | Detect and route alerts | PagerDuty, Opsgenie, Grafana Alerting |
| Incident tracking | Manage incident lifecycle | PagerDuty, Incident.io, Linear |
| Communication | War rooms, status updates | Slack, Zoom, Microsoft Teams |
| Status pages | External communication | Statuspage, Instatus, Cachet |
| Postmortems | Document and learn | Notion, Google Docs, Confluence |
| Action items | Track follow-ups | Linear, Jira, GitHub Issues |

### 9.2 Incident Management Workflow

```
Alert fires (PagerDuty)
    |
    v
Incident declared (PagerDuty/Incident.io)
    |
    v
Slack channel created (#incident-INC-123)
    |
    v
War room opened (Zoom/Meet)
    |
    v
Roles assigned (IC, investigator, communicator, scribe)
    |
    v
Investigation and mitigation
    |
    v
Status page updated
    |
    v
Incident resolved
    |
    v
Postmortem scheduled
    |
    v
Postmortem written and reviewed
    |
    v
Action items created and tracked
    |
    v
Action items completed and verified
```

---

## 10. Key Takeaways

1. **Classify severity consistently** using impact-based criteria
2. **Assign an Incident Commander** for every P0 and P1 incident
3. **Use communication templates** for consistent, clear status updates
4. **Maintain a status page** for external communication during outages
5. **Write blameless postmortems** within 5 business days of every P0/P1 incident
6. **Track action items** to completion — never let them fall through cracks
7. **Calculate SLA impact** for every incident to understand business consequences
8. **Test incident management processes** through regular game days and drills
9. **Iterate on the process** based on postmortem learnings and team feedback
10. **Celebrate improvements** — highlight how postmortem action items prevent future incidents
