# Data Quality Standards for Recommendation Systems

## Overview

Data quality standards define the minimum acceptable quality for data products in a recommendation system. These standards are enforced through SLAs, automated gates, scoring mechanisms, and organizational culture. Without explicit standards, quality degrades incrementally until it impacts model performance and user experience.

---

## Data Quality SLAs per Feature

### SLA Framework

Every feature in the feature store should have an explicitly defined SLA covering freshness, completeness, accuracy, and availability.

| SLA Dimension | Definition | Measurement |
|---|---|---|
| **Freshness** | Maximum age of feature data | Time since last successful update |
| **Completeness** | Minimum percentage of non-null values | Null count / total count |
| **Accuracy** | Percentage of values within valid range | Valid count / total count |
| **Availability** | Percentage of time the feature is accessible | Uptime / total time |
| **Consistency** | Agreement between online and offline values | Cross-system comparison |

### SLA Tiers

| Tier | Freshness | Completeness | Availability | Use Case |
|---|---|---|---|---|
| **Tier 0 (Critical)** | < 1 minute | > 99.9% | 99.99% | Real-time ranking features |
| **Tier 1 (High)** | < 5 minutes | > 99.5% | 99.9% | Near-real-time features |
| **Tier 2 (Medium)** | < 1 hour | > 99% | 99.5% | Batch-computed features |
| **Tier 3 (Low)** | < 24 hours | > 95% | 99% | Experimental features |

### SLA Definition Process

1. **Catalog features**: Inventory all features and their consumers (models, dashboards, experiments).
2. **Classify by impact**: Determine the business impact of each feature's quality degradation.
3. **Set SLAs**: Define tier-appropriate SLAs based on impact classification.
4. **Implement monitoring**: Deploy automated checks to measure SLA compliance.
5. **Review and adjust**: Quarterly review of SLAs based on operational experience and changing requirements.

### SLA Violation Response

| Violation Type | Response | Timeline |
|---|---|---|
| Freshness SLA breach | Alert on-call, investigate | < 15 minutes |
| Completeness SLA breach | Alert data engineer, check pipeline | < 30 minutes |
| Accuracy SLA breach | Quarantine feature, notify model owners | < 1 hour |
| Availability SLA breach | Page infrastructure team | < 5 minutes |
| Consistency SLA breach | Investigate pipeline divergence | < 4 hours |

---

## Automated Quality Gates

### Gate Architecture

Quality gates are automated checkpoints that validate data before allowing downstream consumption. They operate at three levels:

| Gate Level | Location | Purpose |
|---|---|---|
| **Ingestion gate** | After data arrives | Validate raw data quality |
| **Transformation gate** | After ETL processing | Validate computed features |
| **Consumption gate** | Before model serving | Validate features are ready for inference |

### Gate Decision Logic

Each gate evaluates a set of quality checks and produces one of three outcomes:

- **PASS**: All checks meet thresholds. Data proceeds to downstream systems.
- **WARN**: Soft quality issues detected. Data proceeds but alerts are raised for investigation.
- **FAIL**: Critical quality issues detected. Data is quarantined and downstream systems fall back to the last known good version.

### Gate Configuration

| Parameter | Description |
|---|---|
| `check_suite` | Collection of quality checks to execute |
| `timeout` | Maximum time for gate evaluation |
| `on_pass` | Action when gate passes (proceed, notify) |
| `on_warn` | Action when gate warns (proceed with alert, log) |
| `on_fail` | Action when gate fails (halt, quarantine, fallback) |
| `fallback_strategy` | How to handle data unavailability (last good version, default values) |

### Gate as Code

Define gates in configuration files that are version-controlled and deployed alongside pipeline code:

```yaml
gate: user_features_daily
checks:
  - name: row_count
    type: range
    min: 9000000
    max: 11000000
  - name: null_rate
    type: threshold
    column: user_id
    max_null_percent: 0.0
  - name: freshness
    type: age
    max_age_hours: 25
  - name: distribution
    type: ks_test
    column: click_count_7d
    reference: previous_day
    p_value_threshold: 0.01
on_fail: quarantine
fallback: use_previous_day_features
```

---

## Quality Scoring

### Feature Quality Score

Compute a composite quality score for each feature that summarizes its current quality state. The score is a weighted average of individual quality dimensions:

**Quality Score = Σ (weight_i × dimension_score_i)**

| Dimension | Weight | Scoring Method |
|---|---|---|
| Completeness | 0.30 | Percentage of non-null values |
| Freshness | 0.25 | 1.0 if within SLA, linear decay beyond |
| Accuracy | 0.25 | Percentage of values within valid range |
| Consistency | 0.10 | Cross-system agreement ratio |
| Uniqueness | 0.10 | 1 - duplicate rate |

### Dataset Quality Score

Aggregate feature-level scores into dataset-level scores:

- **Minimum score**: The lowest individual feature score. Useful for identifying the weakest link.
- **Weighted average**: Weighted by feature importance (usage in models). Critical features have higher weights.
- **P5/P50/P95**: Distribution of feature quality scores. P5 identifies the worst 5% of features.

### Quality Score Thresholds

| Score Range | Status | Action |
|---|---|---|
| 95–100 | Excellent | No action needed |
| 85–94 | Good | Monitor for degradation |
| 70–84 | Fair | Investigate and prioritize improvements |
| 50–69 | Poor | Active remediation required |
| < 50 | Critical | Feature may be unreliable, consider disabling |

### Quality Score Tracking

- **Time-series tracking**: Plot quality scores over time to identify trends and degradation patterns.
- **Anomaly detection**: Apply statistical anomaly detection to quality scores to catch sudden drops.
- **Correlation with model performance**: Track the correlation between feature quality scores and model metrics to quantify the business impact of quality issues.

---

## Quality Dashboards

### Dashboard Hierarchy

| Dashboard Level | Audience | Content |
|---|---|---|
| **Executive** | Leadership | Overall quality score, trend, business impact |
| **Operational** | Data/ML engineers | Feature-level quality, pipeline health, SLA compliance |
| **Investigative** | On-call engineers | Detailed check results, error logs, remediation status |
| **Self-service** | Feature owners | Feature-specific quality metrics and history |

### Executive Dashboard Components

- **Overall quality score**: Single number with trend arrow (improving, stable, degrading).
- **SLA compliance**: Percentage of features meeting their SLAs.
- **Quality incidents**: Open incidents count, mean time to resolution.
- **Business impact**: Estimated revenue/user impact of quality issues.
- **Quality trend**: 30-day quality score trend with annotations for incidents.

### Operational Dashboard Components

- **Feature quality matrix**: Heatmap of features × quality dimensions. Red cells indicate issues.
- **Pipeline health**: Status of each data pipeline (running, delayed, failed).
- **SLA violations**: List of current SLA breaches with duration and impact.
- **Quality check results**: Pass/fail rates for each quality check suite.
- **Data freshness timeline**: When each feature was last updated vs. its SLA.

### Dashboard Refresh and Retention

| Metric Type | Refresh Rate | Retention |
|---|---|---|
| Real-time quality | 1 minute | 7 days |
| Hourly aggregations | 1 hour | 90 days |
| Daily summaries | Daily | 1 year |
| Quality incidents | Real-time | Permanent |

---

## Quality Alerting

### Alert Rules

Define alert rules based on quality metrics:

| Rule | Condition | Severity | Notification |
|---|---|---|---|
| Feature freshness | Feature age > SLA threshold | High | Slack + PagerDuty |
| Completeness drop | Null rate increases > 5% from baseline | High | Slack |
| Quality score drop | Score decreases > 10 points from 7-day average | Medium | Slack |
| Schema change | Unexpected column added/removed/typed | Critical | PagerDuty |
| Distribution shift | KS test p-value < 0.01 | Medium | Slack |
| SLA compliance | Overall compliance drops below 95% | High | Slack + email |

### Alert Routing

| Alert Type | Primary Contact | Escalation | Channel |
|---|---|---|---|
| Feature quality | Feature owner | Data engineering lead | Slack #data-quality |
| Pipeline failure | Pipeline on-call | Engineering manager | PagerDuty |
| Schema violation | Schema owner | Platform team | Slack #schema-changes |
| Model quality | ML engineer | ML team lead | Slack #ml-quality |

### Alert Suppression and Grouping

- **Suppression windows**: After alerting on a known issue, suppress duplicate alerts for a configurable window.
- **Grouping**: Group related alerts (e.g., multiple features affected by the same pipeline failure) into a single notification.
- **Escalation chains**: If an alert is not acknowledged within the SLA, escalate to the next contact.
- **Quiet hours**: Configure non-critical alerts to be silenced during off-hours.

---

## Data Quality Culture

### Quality Ownership Model

| Role | Responsibility |
|---|---|
| **Data producers** | Ensure source data meets quality standards before publishing |
| **Data engineers** | Maintain pipeline quality, implement quality gates, monitor quality metrics |
| **ML engineers** | Validate feature quality, monitor model-feature quality correlation |
| **Feature owners** | Define and maintain feature SLAs, investigate quality issues |
| **Data stewards** | Define quality standards, audit compliance, drive quality improvements |
| **Engineering managers** | Allocate resources for quality initiatives, enforce quality processes |

### Quality Processes

- **Quality reviews**: Weekly review of quality metrics and open issues.
- **Quality retrospectives**: After quality incidents, conduct root cause analysis and implement preventive measures.
- **Quality sprints**: Dedicate engineering capacity to quality improvements each quarter.
- **Quality documentation**: Maintain runbooks for common quality issues and remediation steps.

### Quality Metrics in Performance Reviews

Incorporate data quality metrics into team and individual performance evaluations:

- **SLA compliance rate**: Percentage of time features meet their SLAs.
- **Mean time to resolution**: Average time to resolve quality incidents.
- **Quality improvement**: Quarter-over-quarter improvement in quality scores.
- **Prevention rate**: Percentage of quality issues prevented by automated checks vs. caught by users.

### Quality Tooling Investment

| Investment | Impact | Priority |
|---|---|---|
| Automated quality gates | Prevents bad data from reaching production | High |
| Quality dashboards | Provides visibility into quality state | High |
| Alerting system | Enables rapid response to quality issues | High |
| Quality scoring | Quantifies quality for prioritization | Medium |
| Lineage tracking | Enables root cause analysis | Medium |
| Self-service quality tools | Empowers feature owners | Low |
