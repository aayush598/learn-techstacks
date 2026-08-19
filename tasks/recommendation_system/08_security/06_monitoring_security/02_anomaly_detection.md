# Security Anomaly Detection

## 1. Overview

Security anomaly detection identifies unusual patterns in system behavior that may indicate
attacks, data breaches, or compromised accounts. For recommendation systems, anomaly
detection must balance security sensitivity against false positive rates, as alerts can
trigger costly incident response processes. This document covers unusual access patterns,
brute force detection, data exfiltration detection, privilege escalation detection, and
ML-based anomaly detection.

### 1.1 Detection Architecture

```
Data Sources → Collection → Analysis → Detection → Alerting → Response
     ↓              ↓           ↓           ↓           ↓          ↓
  Logs,         Fluentd,    Stream      Rule engine   PagerDuty  Auto-block,
  metrics,      Kafka       processing  + ML models   Slack      investigate
  traces                    (Flink)
```

---

## 2. Unusual Access Patterns

### 2.1 Detection Categories

| Pattern | Description | Risk Level |
|---|---|---|
| Geographic anomaly | Login from unusual location | Medium |
| Temporal anomaly | Access at unusual time | Low-Medium |
| Volume anomaly | Unusual request volume | Medium |
| Behavioral anomaly | Unusual API usage pattern | Medium-High |
| Device anomaly | New/unrecognized device | Medium |

### 2.2 Geographic Anomaly Detection

```
Detection Logic:
├── Baseline: User's typical login locations
├── Detection: Login from location > 500km from baseline
├── Time window: > 2 hours between locations (impossible travel)
├── Risk score: Distance / time > speed of travel
└── Action: Block + require additional verification
```

**Impossible travel detection:**

| Location A | Location B | Time Difference | Speed Required | Verdict |
|---|---|---|---|---|
| New York | London | 2 hours | 3,500 km/h | Impossible (flight) |
| New York | London | 8 hours | 875 km/h | Possible (flight) |
| New York | San Francisco | 1 hour | 4,000 km/h | Impossible |
| New York | San Francisco | 6 hours | 670 km/h | Possible (flight) |

### 2.3 Temporal Anomaly Detection

| Pattern | Detection | Risk |
|---|---|---|
| Access at 3 AM local time | Time outside user's normal hours | Low |
| Weekend admin access | Admin action outside business hours | Medium |
| Holiday access spike | Unusual volume on holidays | Medium |
| Rapid sequential access | Multiple requests in < 1 second | High |

### 2.4 Volume Anomaly Detection

**Statistical methods:**

- **Z-score**: Flag when request volume > 3σ from baseline
- **EWMA**: Exponentially weighted moving average for trend detection
- **Seasonal decomposition**: Remove daily/weekly patterns, detect residuals
- **Change point detection**: PELT algorithm for sudden shifts

---

## 3. Brute Force Detection

### 3.1 Authentication Brute Force

| Detection Criteria | Threshold | Window | Action |
|---|---|---|---|
| Failed login attempts | > 5 | 5 minutes | Temp lockout |
| Failed login attempts | > 10 | 1 hour | Account lockout |
| Failed login (different accounts) | > 20 | 5 minutes | IP block |
| Password reset requests | > 3 | 1 hour | Account lockout |
| API key failures | > 10 | 5 minutes | Key suspension |

### 3.2 Account Lockout Strategy

```
Failed Attempt 1-4: Log and continue
Failed Attempt 5: Temporary lockout (5 minutes)
Failed Attempt 6: Extended lockout (15 minutes)
Failed Attempt 7+: Account locked (require admin unlock)
    ↓
Notification sent to account owner
    ↓
Admin review for suspicious activity
```

### 3.3 API Brute Force

| Target | Detection | Action |
|---|---|---|
| Rate limit bypass | > 10x rate limit from same IP | IP block |
| Authentication endpoint | > 100 failed auth attempts/hour | IP block |
| Specific endpoint | > 1000 requests/minute from single user | User suspension |

### 3.4 Credential Stuffing Detection

| Signal | Detection | Response |
|---|---|---|
| High login failure rate | > 50% failure rate from IP range | Block IP range |
| Known compromised passwords | Password in breach database | Force password reset |
| Multiple account targeting | > 10 accounts from same IP | Block + alert |
| Distributed attacks | > 100 IPs with same pattern | WAF rule + investigate |

---

## 4. Data Exfiltration Detection

### 4.1 Exfiltration Patterns

| Pattern | Detection | Risk |
|---|---|---|
| Bulk data download | > 10MB data export in 1 hour | High |
| API scraping | > 1000 API calls/minute | High |
| Sequential data access | Accessing records in ID order | High |
| Off-hours data access | Large data access outside business hours | Medium-High |
| New endpoint access | Accessing previously unused endpoints | Medium |

### 4.2 Data Volume Monitoring

```
Monitoring Points:
├── Database query result size
├── API response payload size
├── File download volume
├── Export operation volume
└── Feature store read volume
```

### 4.3 Exfiltration Prevention

| Prevention Layer | Implementation |
|---|---|
| Rate limiting | Per-user and per-IP rate limits |
| Data classification | Restrict sensitive data access |
| DLP (Data Loss Prevention) | Monitor outbound data flows |
| Network monitoring | Detect unusual outbound traffic |
| API monitoring | Track data volume per API call |

---

## 5. Privilege Escalation Detection

### 5.1 Privilege Escalation Patterns

| Pattern | Detection | Risk |
|---|---|---|
| Role change without approval | Admin role assigned without ticket | Critical |
| Permission boundary crossing | User accessing resources outside scope | High |
| API scope expansion | API key accessing new endpoints | High |
| Admin action by non-admin | Non-admin performing admin operations | Critical |

### 5.2 Privilege Escalation Monitoring

```
Monitoring Events:
├── Role changes (user, admin, service account)
├── Permission grants and revocations
├── Admin operations (user management, config changes)
├── API key scope changes
├── Access control policy changes
└── Database permission changes
```

### 5.3 Privilege Escalation Prevention

| Prevention | Implementation |
|---|---|
| Role change approval | Require manager approval for role changes |
| Permission audit | Monthly review of all permissions |
| Just-in-time access | Temporary elevated permissions |
| Standing privilege reduction | Remove unused permissions |
| Break-glass procedure | Emergency access with audit trail |

---

## 6. ML-Based Anomaly Detection

### 6.1 ML Models for Security

| Model Type | Use Case | Advantages |
|---|---|---|
| Isolation Forest | Unsupervised anomaly detection | No labeled data needed |
| Autoencoder | Reconstruction-based detection | Complex pattern detection |
| LSTM | Sequential behavior modeling | Temporal pattern detection |
| Graph neural network | Relationship-based detection | Entity relationship modeling |
| Ensemble methods | Combined detection | Higher accuracy |

### 6.2 ML Anomaly Detection Pipeline

```
Security Events → Feature Engineering → Model Inference → Anomaly Score → Alert Decision
       ↓                ↓                    ↓                ↓              ↓
  Auth events,      Behavioral         Trained model      Threshold      Alert if
  API access,       features per       scores each        comparison     score exceeds
  data access       user/session       event                             threshold
```

### 6.3 Feature Engineering for Security ML

| Feature | Description | Type |
|---|---|---|
| Request frequency | Requests per minute/hour | Temporal |
| Data volume | Bytes accessed per request | Volume |
| Endpoint pattern | Sequence of endpoints accessed | Sequential |
| Time of day | Hour of access | Temporal |
| Geographic location | IP geolocation | Spatial |
| Device fingerprint | Browser/device characteristics | Behavioral |
| Error rate | Percentage of failed requests | Behavioral |

### 6.4 ML Model Retraining

- **Frequency**: Weekly retraining with latest security events
- **Data**: Labeled security events (true positives and false positives)
- **Evaluation**: Precision, recall, F1 score on held-out test set
- **Deployment**: Shadow mode first, then production with monitoring
- **Drift detection**: Monitor model performance over time

### 6.5 False Positive Management

| Strategy | Description | Target |
|---|---|---|
| Alert tuning | Adjust thresholds based on feedback | < 5% false positive rate |
| User feedback loop | Analysts label alerts as true/false | Continuous improvement |
| Whitelist management | Exclude known-safe patterns | Reduce noise |
| Risk scoring | Multi-factor risk assessment | Prioritize high-risk alerts |
| Human-in-the-loop | ML flags, human decides | Critical decisions only |
