# Incident Response

## Overview

Incident response for ML recommendation systems requires handling both traditional software incidents (latency, errors, outages) and ML-specific incidents (model degradation, data quality issues, fairness violations). A structured incident response process ensures rapid resolution, clear communication, and continuous improvement through blameless postmortems.

## Incident Severity Levels

### SEV1 - Critical

| Attribute | Description |
|-----------|-------------|
| **Impact** | Service completely unavailable or major business function broken |
| **User impact** | All users affected |
| **Revenue impact** | Significant revenue loss (> $10K/hour) |
| **Examples** | Recommendation serving down, data breach, complete model failure |
| **Response time** | Immediate (within 5 minutes) |
| **Resolution target** | 1 hour |
| **Communication** | Status page, executive notification, customer support briefing |

### SEV2 - Major

| Attribute | Description |
|-----------|-------------|
| **Impact** | Significant degradation of service quality |
| **User impact** | Large subset of users affected (> 10%) |
| **Revenue impact** | Moderate revenue impact ($1K-$10K/hour) |
| **Examples** | High latency (p99 > 1s), model quality degradation > 10%, partial feature outage |
| **Response time** | Within 15 minutes |
| **Resolution target** | 4 hours |
| **Communication** | Status page, team notification |

### SEV3 - Minor

| Attribute | Description |
|-----------|-------------|
| **Impact** | Noticeable degradation but service functional |
| **User impact** | Small subset of users affected (< 10%) |
| **Revenue impact** | Minor revenue impact (< $1K/hour) |
| **Examples** | Elevated error rate (1-5%), specific model variant issues, non-critical feature broken |
| **Response time** | Within 1 hour |
| **Resolution target** | 24 hours |
| **Communication** | Team channel notification |

### SEV4 - Low

| Attribute | Description |
|-----------|-------------|
| **Impact** | Minimal impact on service or users |
| **User impact** | Negligible |
| **Revenue impact** | None or negligible |
| **Examples** | Cosmetic issues, minor performance degradation, non-user-facing bugs |
| **Response time** | Next business day |
| **Resolution target** | 1 week |
| **Communication** | Ticket tracking |

### ML-Specific Severity Classification

| Incident Type | Default Severity | Examples |
|--------------|-----------------|---------|
| **Model serving outage** | SEV1 | No recommendations served |
| **Model quality crash** | SEV1-SEV2 | CTR drops > 20% |
| **Data pipeline failure** | SEV2-SEV3 | Features stale > 1 hour |
| **Fairness violation** | SEV2 | Demographic parity breach |
| **Feature store outage** | SEV1-SEV2 | Feature retrieval failing |
| **Training pipeline failure** | SEV3-SEV4 | Scheduled retraining failed |
| **Monitoring gap** | SEV4 | Missing alert for metric |

## Incident Commander Role

### Responsibilities

| Phase | Incident Commander Actions |
|-------|---------------------------|
| **Detection** | Acknowledge alert, classify severity |
| **Mobilization** | Assemble response team, create war room |
| **Diagnosis** | Guide investigation, identify root cause |
| **Mitigation** | Coordinate mitigation actions |
| **Resolution** | Verify fix, confirm service restored |
| **Communication** | Manage internal/external communication |
| **Postmortem** | Schedule and facilitate postmortem |

### Incident Commander Checklist

```
1. Acknowledge the alert (within SLA)
2. Classify severity (SEV1-SEV4)
3. Open war room (Slack channel or video call)
4. Assign roles:
   - Investigator: Leading diagnosis
   - Communicator: Updating stakeholders
   - Scribe: Documenting timeline and actions
5. Establish communication cadence:
   - SEV1: Every 15 minutes
   - SEV2: Every 30 minutes
   - SEV3: Every hour
6. Identify mitigation options
7. Execute mitigation
8. Verify resolution
9. Close incident
10. Schedule postmortem
```

## Communication Templates

### Initial Alert (Slack)

```
[SEV{1-4}] {Incident Title}
Status: Investigating
Impact: {Brief description of user/business impact}
Commander: @{name}
War room: #{channel-name}
Next update: {time}
```

### Status Update (Slack)

```
[UPDATE] {Incident Title}
Status: {Investigating | Identified | Monitoring | Resolved}
Update: {What we know so far}
Next steps: {What we are doing}
Next update: {time}
```

### Status Page Update

```json
{
  "incident": {
    "name": "Recommendation Service Degraded Performance",
    "status": "investigating",
    "impact": "major",
    "body": "We are investigating elevated latency in the recommendation service. Some users may experience slower than normal recommendation loading.",
    "components": ["recommendation-service"],
    "updates": [
      {
        "status": "investigating",
        "body": "Engineering team is investigating elevated latency observed since 14:30 UTC."
      }
    ]
  }
}
```

### Resolution Notification

```
[RESOLVED] {Incident Title}
Duration: {Start time} - {End time} ({total duration})
Impact: {Summary of what was affected}
Root cause: {Brief description}
Fix: {What was done to resolve}
Postmortem: {Link, scheduled for {date}}
```

## Escalation Matrix

### Escalation Path

| Time Without Resolution | SEV1 Action | SEV2 Action | SEV3 Action |
|------------------------|-------------|-------------|-------------|
| 0-15 min | IC + on-call | IC + on-call | On-call investigates |
| 15-30 min | Add tech lead | IC notification | Escalate if stuck |
| 30-60 min | Add engineering manager | Add tech lead | Next business day |
| 1-2 hours | Add VP Engineering | Escalate if stuck | -- |
| 2+ hours | Executive notification | Add engineering manager | -- |

### On-Call Rotation

| Role | Responsibility | Contact Method |
|------|---------------|---------------|
| **Primary on-call** | First responder, initial diagnosis | PagerDuty (phone + SMS) |
| **Secondary on-call** | Backup, escalation target | PagerDuty (phone + SMS) |
| **ML on-call** | ML-specific incidents (model, data, fairness) | PagerDuty + Slack |
| **SRE on-call** | Infrastructure incidents | PagerDuty + Slack |
| **Engineering manager** | Escalation, resource allocation | Phone |

### Escalation Contacts

| Level | Contact | When to Escalate |
|-------|---------|-----------------|
| **Team lead** | {name, phone} | Cannot resolve within SLA |
| **Engineering manager** | {name, phone} | Need additional resources |
| **VP Engineering** | {name, phone} | SEV1 > 1 hour, executive decision needed |
| **CTO** | {name, phone} | SEV1 > 2 hours, customer-facing impact |
| **Legal** | {name, phone} | Data breach, compliance violation |
| **PR/Comms** | {name, phone} | Public-facing incident, media inquiries |

## Mitigation vs Resolution

### Mitigation First

The priority during an incident is mitigation (reducing impact), not root cause analysis.

| Action | Type | Examples |
|--------|------|---------|
| **Rollback** | Mitigation | Revert to previous model version |
| **Feature flag** | Mitigation | Disable affected feature |
| **Circuit breaker** | Mitigation | Stop calling degraded dependency |
| **Manual override** | Mitigation | Serve popular items temporarily |
| **Scale up** | Mitigation | Add capacity to handle load |
| **Cache** | Mitigation | Serve cached recommendations |

### Resolution

Resolution means fixing the root cause so the mitigation can be removed.

| Action | Type | Examples |
|--------|------|---------|
| **Bug fix** | Resolution | Fix code error in model serving |
| **Data fix** | Resolution | Repair corrupted training data |
| **Config change** | Resolution | Update model configuration |
| **Infrastructure fix** | Resolution | Repair broken server |
| **Model retrain** | Resolution | Retrain model with corrected data |

### Mitigation Decision Tree

```
Is the service down?
  Yes -> Rollback to last known good version
  No -> Is the issue user-facing?
    Yes -> Enable feature flag / circuit breaker
    No -> Is the issue data-related?
      Yes -> Switch to cached data / default values
      No -> Scale up resources / restart affected services
```

## Blameless Postmortems

### Principles

1. **Focus on systems, not people**: What systemic factors allowed this to happen?
2. **No blame or punishment**: Everyone acted with the information they had
3. **Learning-oriented**: The goal is improvement, not attribution
4. **Action-oriented**: Every postmortem must produce actionable items
5. **Timely**: Conduct within 1 week of incident resolution

### Postmortem Meeting Structure

| Agenda Item | Duration | Facilitator |
|-------------|----------|-------------|
| Incident summary | 5 min | Incident Commander |
| Timeline walkthrough | 10 min | Scribe |
| Root cause analysis | 15 min | Investigator |
| What went well | 5 min | Open discussion |
| What went wrong | 5 min | Open discussion |
| Action items | 10 min | Incident Commander |
| Process improvement | 5 min | Open discussion |

### Root Cause Analysis Techniques

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| **5 Whys** | Ask "why" repeatedly until root cause | Simple incidents |
| **Fishbone diagram** | Categorize causes (people, process, technology, environment) | Complex incidents |
| **Timeline analysis** | Map events to identify causal chain | All incidents |
| **Fault tree analysis** | Top-down decomposition of failure modes | Safety-critical systems |

### 5 Whys Example

```
Why did recommendations fail?
  -> Model serving returned 500 errors.
Why did model serving return 500 errors?
  -> The model file was corrupted during loading.
Why was the model file corrupted?
  -> A partial write occurred during the last deployment.
Why did a partial write occur?
  -> The deployment script did not use atomic file replacement.
Why did the deployment script not use atomic replacement?
  -> The original deployment was written as a quick prototype.
Why was the prototype still in use?
  -> We did not have a deployment review process for ML artifacts.
```

## Action Item Tracking

### Action Item Template

```markdown
- **Action**: {Description of what needs to be done}
- **Owner**: {Person responsible}
- **Priority**: {High/Medium/Low}
- **Due date**: {When it should be completed}
- **Status**: {Not started/In progress/Completed}
- **Related incident**: {Incident ID}
- **Tracking issue**: {Link to Jira/Linear ticket}
```

### Action Item Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Immediate** | Fix the immediate issue | Patch the bug |
| **Preventive** | Prevent similar incidents | Add monitoring |
| **Systemic** | Address root causes | Improve deployment process |
| **Process** | Improve incident response | Update runbooks |

### Action Item Review

| Review Type | Frequency | Participants |
|-------------|----------|-------------|
| **Incident follow-up** | 1 week post-incident | IC + response team |
| **Action item review** | Weekly standup | Team leads |
| **Action item audit** | Monthly | Engineering manager |
| **Postmortem quality review** | Quarterly | Engineering leadership |

## Incident Response Drills

### Drill Types

| Drill Type | Description | Frequency | Duration |
|-----------|-------------|----------|----------|
| **Tabletop exercise** | Walk through incident scenario verbally | Monthly | 30-60 min |
| **Chaos engineering** | Inject real failures in staging | Quarterly | 2-4 hours |
| **Surprise drill** | Inject failure without warning | Semi-annually | Variable |
| **Full-scale drill** | Simulate complete incident response | Annually | Half day |

### Chaos Engineering for ML

| Experiment | Failure Injected | Expected Behavior |
|-----------|-----------------|-------------------|
| **Model file deletion** | Delete model file from serving pod | Automatic reload from registry |
| **Feature store latency** | Add 500ms latency to feature store | Feature cache activated |
| **Training data corruption** | Inject bad data into training set | Data validation catches it |
| **Serving pod crash** | Kill random serving pods | Auto-scaling replaces pods |
| **Network partition** | Isolate model serving from feature store | Graceful degradation to cached features |

### Drill Success Criteria

| Criterion | Target |
|-----------|--------|
| **Detection time** | Alert fires within 5 minutes of failure |
| **Response time** | IC acknowledges within SLA |
| **Mitigation time** | Mitigation applied within resolution target |
| **Communication** | Stakeholders notified within 15 minutes |
| **Documentation** | Timeline documented during incident |
| **Postmortem** | Completed within 1 week |
| **Action items** | All high-priority items completed within 2 weeks |
