# Escalation Policies for Recommendation Systems

## 1. Overview

Escalation policies define how alerts progress from initial detection through resolution, ensuring the right people are notified at the right time. In recommendation systems, escalation is critical because outages directly impact user experience and revenue. A well-designed escalation policy prevents alert fatigue, reduces mean time to resolution (MTTR), and ensures accountability.

### 1.1 Why Escalation Policies Matter

- **Alert fatigue prevention**: Without structured escalation, engineers ignore alerts
- **Accountability**: Clear ownership at every severity level
- **Response time guarantees**: Escalation ensures no alert goes unacknowledged
- **Business impact mitigation**: Faster response means less revenue loss
- **Compliance**: Some regulations require documented incident response procedures

### 1.2 Escalation Policy Goals

| Goal | Metric | Target |
|---|---|---|
| Acknowledge time | Time from alert to acknowledgment | <5 min (P0), <15 min (P1) |
| Respond time | Time from alert to active investigation | <15 min (P0), <30 min (P1) |
| Resolve time | Time from alert to resolution | <1 hour (P0), <4 hours (P1) |
| Escalation rate | % of alerts that escalate beyond L1 | <20% |
| False positive rate | % of alerts that are false alarms | <10% |

---

## 2. Severity Levels (P0-P4)

### 2.1 Severity Definitions

| Severity | Name | Impact | Example |
|---|---|---|---|
| P0 | Critical | Complete service outage, data loss, revenue impact | All recommendations returning empty |
| P1 | High | Significant degradation, partial outage | P99 latency > 2s, error rate > 5% |
| P2 | Medium | Moderate degradation, no data loss | CTR drop > 20%, feature staleness > 5 min |
| P3 | Low | Minor issue, workaround available | Single model version lagging, minor coverage drop |
| P4 | Info | No user impact, maintenance needed | Training job failed, non-critical config drift |

### 2.2 Severity-Specific Targets

| Metric | P0 | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|
| Acknowledge time | 5 min | 15 min | 1 hour | 4 hours | Next business day |
| Respond time | 15 min | 30 min | 2 hours | 8 hours | Next business day |
| Resolve time | 1 hour | 4 hours | 24 hours | 1 week | Best effort |
| Notification channels | All (page + call) | Page + Slack | Slack + email | Email | Dashboard only |
| Escalation timeout | 10 min | 30 min | 2 hours | 8 hours | 24 hours |

### 2.3 Severity Assignment Criteria

```
P0: User-facing outage OR data loss OR security breach
    AND affects >10% of users
    AND no workaround exists

P1: User-facing degradation OR significant metric regression
    AND affects >5% of users
    OR workaround exists but is fragile

P2: Internal degradation OR metric regression
    AND affects <5% of users
    OR workaround exists and is reliable

P3: Non-user-facing issue OR minor regression
    AND affects <1% of users
    AND no immediate business impact

P4: Maintenance or optimization opportunity
    AND no current business impact
```

---

## 3. Escalation Chains

### 3.1 Escalation Chain Structure

```
Alert Fires
    |
    v
L1: On-Call Engineer (acknowledge + initial triage)
    | (no ack in 10 min / severity P0)
    v
L2: Secondary On-Call + Team Lead (deeper investigation)
    | (no resolution in 30 min / severity P0)
    v
L3: Engineering Manager + Domain Expert (escalation)
    | (no resolution in 1 hour / severity P0)
    v
L4: VP Engineering + Incident Commander (executive escalation)
    | (no resolution in 2 hours / severity P0)
    v
L5: CTO + External Support (vendor escalation if needed)
```

### 3.2 Escalation Chains by Severity

| Severity | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| P0 | On-call engineer | Team lead + secondary on-call | Engineering manager | VP engineering | CTO |
| P1 | On-call engineer | Team lead | Engineering manager | VP engineering | — |
| P2 | On-call engineer | Team lead | — | — | — |
| P3 | On-call engineer | — | — | — | — |
| P4 | Anyone on team | — | — | — | — |

### 3.3 Escalation Trigger Conditions

```yaml
escalation_triggers:
  - condition: "no_ack_in_10min AND severity=P0"
    action: "escalate_to_L2"
  - condition: "no_resolution_in_30min AND severity=P0"
    action: "escalate_to_L3"
  - condition: "no_resolution_in_1hr AND severity=P0"
    action: "escalate_to_L4"
  - condition: "no_ack_in_30min AND severity=P1"
    action: "escalate_to_L2"
  - condition: "no_resolution_in_2hr AND severity=P1"
    action: "escalate_to_L3"
  - condition: "alert_recurring_3x_in_1hr"
    action: "escalate_to_L2"
  - condition: "multiple_alerts_firing_simultaneously"
    action: "declare_incident, escalate_to_L3"
```

---

## 4. On-Call Rotation

### 4.1 Rotation Design

| Parameter | Recommendation | Rationale |
|---|---|---|
| Shift duration | 1 week | Balances context retention with burnout prevention |
| Handoff time | Start of business day (Tuesday) | Allows overlap for context transfer |
| Primary on-call | 1 engineer | Clear ownership |
| Secondary on-call | 1 engineer | Backup if primary is unavailable |
| Weekend rotation | Same as weekday | Equal distribution of burden |
| Holiday coverage | Voluntary with incentive | Fairness and morale |

### 4.2 On-Call Requirements

**Primary on-call:**
- Must be reachable within 5 minutes of page
- Must have laptop and internet access
- Must be within 30 minutes of a work-capable location
- Must not be engaged in other intensive work during shift

**Secondary on-call:**
- Must be reachable within 15 minutes of page
- Acts as backup if primary is unresponsive
- May be paged for complex incidents requiring two engineers

### 4.3 On-Call Compensation

| Compensation Type | Amount | Frequency |
|---|---|---|
| On-call stipend | $200–500/week | Per rotation |
| Incident response bonus | $100–200/incident | Per P0/P1 incident |
| After-hours page bonus | $50/ page | Per page outside business hours |
| Compensatory time off | 4 hours per P0 incident | Per incident |

### 4.4 On-Call Metrics

Track on-call health to prevent burnout:

| Metric | Target | Alert Threshold |
|---|---|---|
| Pages per week | <5 per on-call | >10 per week |
| After-hours pages per week | <2 per on-call | >5 per week |
| P0 incidents per month | <2 per team | >4 per month |
| Average incident duration | <2 hours | >4 hours |
| Post-incident review completion | 100% for P0/P1 | <100% |

---

## 5. Notification Channels

### 5.1 Channel Matrix

| Channel | Latency | Reliability | Use Case |
|---|---|---|---|
| PagerDuty/Opsgenie | <1 min | High | P0/P1 alerts requiring immediate action |
| Phone call | <2 min | High | Backup for P0 when pager is missed |
| SMS | <1 min | Medium | Backup for phone call |
| Slack/Teams | <1 min | High | P1/P2 alerts, team awareness |
| Email | <5 min | High | P2/P3 alerts, incident reports |
| Dashboard | Real-time | High | P3/P4 alerts, status monitoring |
| Status page | <5 min | High | External communication for P0/P1 |

### 5.2 Alert Routing Rules

```yaml
alert_routing:
  - severity: P0
    channels: [pagerduty, phone_call, slack_incident_channel]
    recipients: [on_call_primary, on_call_secondary, team_lead]
    repeat_interval: 5min
    acknowledge_timeout: 10min

  - severity: P1
    channels: [pagerduty, slack_team_channel]
    recipients: [on_call_primary, team_lead]
    repeat_interval: 15min
    acknowledge_timeout: 30min

  - severity: P2
    channels: [slack_team_channel, email]
    recipients: [on_call_primary]
    repeat_interval: 30min
    acknowledge_timeout: 2hr

  - severity: P3
    channels: [slack_team_channel]
    recipients: [on_call_primary]
    repeat_interval: 4hr
    acknowledge_timeout: 8hr

  - severity: P4
    channels: [dashboard_only]
    recipients: [team_lead]
    repeat_interval: daily
    acknowledge_timeout: next_business_day
```

### 5.3 Quiet Hours Configuration

```yaml
quiet_hours:
  enabled: true
  hours: "22:00-07:00 local time"
  override_for: [P0, P1]
  channels_during_quiet_hours:
    P0: [pagerduty, phone_call]
    P1: [pagerduty]
    P2: [email_only]
    P3: [dashboard_only]
    P4: [dashboard_only]
```

---

## 6. Alert Routing

### 6.1 Alert Routing Rules

Route alerts to the correct team based on alert labels:

```yaml
routing_rules:
  - match: {service: "ranking-service"}
    team: "ml-serving-team"
    oncall_rotation: "ml-serving-oncall"

  - match: {service: "feature-service"}
    team: "feature-platform-team"
    oncall_rotation: "feature-oncall"

  - match: {service: "candidate-service"}
    team: "discovery-team"
    oncall_rotation: "discovery-oncall"

  - match: {service: "serving-layer"}
    team: "platform-team"
    oncall_rotation: "platform-oncall"

  - match: {service: "model-training"}
    team: "ml-training-team"
    oncall_rotation: "ml-training-oncall"
```

### 6.2 Alert Grouping

Group related alerts to reduce noise:

```yaml
grouping:
  - name: "ranking_service_group"
    match: {service: "ranking-service"}
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4hr

  - name: "feature_pipeline_group"
    match: {pipeline: "feature-pipeline"}
    group_wait: 1m
    group_interval: 10m
    repeat_interval: 1hr
```

### 6.3 Alert Inhibition

Suppress lower-severity alerts when higher-severity alerts are active:

```yaml
inhibition_rules:
  - source_match: {severity: P0}
    target_match: {severity: [P1, P2, P3, P4], service: "{{ .service }}"}
    equal: [service]

  - source_match: {alertname: "ServiceDown"}
    target_match: {alertname: "HighLatency", service: "{{ .service }}"}
    equal: [service]
```

---

## 7. Acknowledgment Requirements

### 7.1 Acknowledgment Workflow

```
Alert fires
    |
    v
On-call engineer receives notification
    |
    v
Engineer acknowledges in PagerDuty/Slack
    | (includes: "investigating", ETA for update)
    v
Engineer investigates
    | (provides updates every 15 min for P0, 1hr for P1)
    v
Engineer resolves or escalates
    | (includes: root cause, resolution, follow-up items)
    v
Incident documented
```

### 7.2 Acknowledgment Requirements by Severity

| Severity | Ack Required | Update Frequency | Resolution Required |
|---|---|---|---|
| P0 | Written acknowledgment | Every 15 min | Incident report + postmortem |
| P1 | Written acknowledgment | Every 30 min | Incident report |
| P2 | Written acknowledgment | Every 2 hours | Resolution notes |
| P3 | Written acknowledgment | Every 8 hours | Resolution notes |
| P4 | Auto-acknowledged | Weekly summary | Optional notes |

### 7.3 Unacknowledged Alert Escalation

If an alert goes unacknowledged:

```
T+0: Alert fires, notification sent to primary on-call
T+5min: Reminder notification to primary on-call
T+10min: Page secondary on-call, notify team lead
T+15min: Page engineering manager
T+30min: Page VP engineering (P0 only)
```

---

## 8. Escalation Timeouts

### 8.1 Timeout Configuration

```yaml
escalation_timeouts:
  P0:
    ack_timeout: 10min
    update_timeout: 15min
    resolution_timeout: 1hr
    executive_escalation: 2hr
    external_communication: 30min

  P1:
    ack_timeout: 30min
    update_timeout: 30min
    resolution_timeout: 4hr
    executive_escalation: 8hr

  P2:
    ack_timeout: 2hr
    update_timeout: 2hr
    resolution_timeout: 24hr

  P3:
    ack_timeout: 8hr
    update_timeout: 8hr
    resolution_timeout: 1week

  P4:
    ack_timeout: next_business_day
    resolution_timeout: best_effort
```

### 8.2 Timeout Actions

| Timeout | Action |
|---|---|
| Ack timeout exceeded | Escalate to next level, re-page |
| Update timeout exceeded | Send reminder, escalate if no response |
| Resolution timeout exceeded | Escalate, consider incident declaration |
| Executive escalation | Page VP+ with business impact summary |

---

## 9. Escalation Policy Maintenance

### 9.1 Regular Reviews

| Review | Frequency | Participants | Focus |
|---|---|---|---|
| Alert review | Weekly | Team | Remove noisy/unused alerts |
| Escalation policy review | Monthly | Team lead + on-call | Adjust timeouts and chains |
| On-call health review | Monthly | Engineering manager | Burnout prevention, coverage |
| Incident review | Per P0/P1 incident | Team | Policy effectiveness |
| Quarterly postmortem review | Quarterly | Leadership | Systemic improvements |

### 9.2 Policy Testing

- **Drills**: Monthly P0 simulation to test escalation chain
- **Chaos engineering**: Inject failures to test alerting and escalation
- **Tabletop exercises**: Quarterly scenario-based exercises
- **On-call shadowing**: New team members shadow experienced on-call

---

## 10. Key Takeaways

1. **Define clear severity levels** (P0-P4) with specific impact criteria
2. **Implement multi-level escalation chains** with timeout-based progression
3. **Design on-call rotations** that prevent burnout (1-week shifts, clear handoffs)
4. **Use multiple notification channels** for critical alerts (pager + phone + Slack)
5. **Require written acknowledgments** with update frequency requirements
6. **Implement alert inhibition** to suppress noise during major incidents
7. **Test escalation policies** regularly through drills and chaos engineering
8. **Track on-call health metrics** and adjust policies based on team feedback
9. **Document everything** — escalation policies should be living documents
10. **Review and iterate** — escalation policies are not set-and-forget
