# Data Minimization

## 1. Overview

Data minimization is the principle of collecting, processing, and retaining only the
minimum personal data necessary for the specified purpose. For recommendation systems,
this means balancing personalization quality against privacy impact. GDPR Article 5(1)(c)
requires that personal data must be "adequate, relevant and limited to what is necessary."
This document covers purpose limitation, data lifecycle management, retention minimization,
and anonymization as an alternative to data collection.

### 1.1 Data Minimization Principles

| Principle | Description | Implementation |
|---|---|---|
| Necessity | Collect only what's needed | Data necessity assessment |
| Proportionality | Processing proportional to purpose | Privacy impact assessment |
| Purpose limitation | Use data only for stated purpose | Purpose-based access control |
| Storage limitation | Retain only as long as needed | Automated data deletion |
| Data quality | Keep data accurate and current | Regular data validation |

### 1.2 Recommendation System Data Necessity

| Data Type | Necessity for Recommendations | Alternative if Not Collected |
|---|---|---|
| User click history | High (core signal) | Non-personalized recommendations |
| User purchase history | High (strong signal) | Category-based recommendations |
| User demographics | Medium (cold start) | Anonymous preferences |
| Device information | Low-Medium | Default device settings |
| Location (precise) | Low-Medium | City-level from IP |
| Cross-device data | Low | Per-device recommendations |

---

## 2. Collecting Only Necessary Data

### 2.1 Data Collection Audit

For every data point collected, document:

| Question | Required Answer |
|---|---|
| What data is collected? | Specific data fields |
| Why is it collected? | Business purpose |
| Is it necessary? | Could the purpose be achieved without this data? |
| How long is it kept? | Retention period |
| Who has access? | Access control list |
| How is it protected? | Security measures |

### 2.2 Data Collection Reduction Strategies

| Strategy | Implementation | Privacy Impact | Recommendation Quality Impact |
|---|---|---|---|
| Reduce frequency | Collect hourly instead of per-event | Moderate reduction | Minor degradation |
| Aggregate early | Collect aggregated metrics, not raw events | Significant reduction | Minor degradation |
| Sample | Collect subset of users/events | Moderate reduction | Minimal impact |
| Delay collection | Collect after user action confirmed | Minor reduction | No impact |
| Skip collection | Don't collect specific data point | Maximum reduction | Varies |

### 2.3 Feature Engineering Minimization

| Feature Category | Full Data | Minimized Data | Quality Impact |
|---|---|---|---|
| Click count | Exact count per item | Binned count (0, 1-5, 6-20, 20+) | < 2% NDCG loss |
| Dwell time | Exact seconds | Binned (< 30s, 30-120s, > 120s) | < 3% NDCG loss |
| Purchase value | Exact amount | Binned (low, medium, high) | < 1% NDCG loss |
| Location | GPS coordinates | City-level | < 5% NDCG loss |
| Device info | Full user agent | Device type only | < 1% NDCG loss |

---

## 3. Purpose Limitation

### 3.1 Purpose Specification

| Purpose | Data Required | Access Control |
|---|---|---|
| Personalized recommendations | Click history, purchase history, preferences | Recommendation service |
| Cold-start recommendations | Anonymous behavior, demographics | Recommendation service |
| Analytics | Aggregated metrics, no PII | Analytics service only |
| Model training | Pseudonymized interaction data | ML pipeline only |
| A/B testing | Experiment group assignment | Experiment service |

### 3.2 Purpose-Based Access Control

```
Data Access Request → Verify Purpose → Check Authorization → Grant/Deny
                           ↓                  ↓
                     Purpose matches     Authorization
                     data use case       matches role
```

### 3.3 Purpose Drift Prevention

- **Regular audits**: Quarterly review of data usage vs stated purpose
- **Access logging**: Track all data access with purpose metadata
- **Anomaly detection**: Alert on unusual data access patterns
- **Purpose change process**: Formal review and approval for new purposes

---

## 4. Data Lifecycle Management

### 4.1 Data Lifecycle Stages

```
Collection → Processing → Storage → Usage → Sharing → Retention → Deletion
    ↓            ↓           ↓         ↓        ↓          ↓          ↓
  Minimize    Purpose-    Encrypt   Access   Contract   Auto-     Verify
  collection  limit       at rest   control  review     delete    deletion
```

### 4.2 Data Retention Policies

| Data Type | Retention Period | Justification | Deletion Method |
|---|---|---|---|
| User profiles | Account lifetime + 30 days | Service provision | Automated + manual |
| Click events | 90 days (raw), 2 years (aggregated) | Feature computation | Automated cascade |
| Purchase history | 3 years | Recommendation training | Automated cascade |
| Model training data | Until model retrained + 30 days | ML compliance | Automated purge |
| Analytics data | 2 years (aggregated) | Business reporting | Automated purge |
| Logs (with PI) | 30 days | Debugging, security | Automated purge |
| Backup data | 90 days | Disaster recovery | Automated purge |

### 4.3 Automated Data Deletion

```
Retention Policy Engine:
├── Schedule: Daily scan of data ages
├── Identification: Find data exceeding retention period
├── Notification: Alert data owners before deletion
├── Deletion: Execute deletion per policy
├── Verification: Confirm deletion completed
└── Audit: Log deletion event for compliance
```

### 4.4 Data Deletion Verification

After deletion, verify:

- Data is removed from all primary databases
- Data is removed from caches and temporary storage
- Data is removed from search indices
- Data is flagged for removal in backups (next backup cycle)
- No data leakage to downstream systems

---

## 5. Retention Minimization

### 5.1 Retention Period Determination

| Factor | Shorter Retention | Longer Retention |
|---|---|---|
| Data sensitivity | High (PII, financial) | Low (aggregated) |
| Purpose duration | One-time purpose | Ongoing purpose |
| Legal requirement | No requirement | Regulatory mandate |
| User expectation | Sensitive, personal | Non-sensitive |
| Re-identification risk | High unique combination | Low uniqueness |

### 5.2 Retention Minimization for Recommendations

| Data | Default Retention | Minimized Retention | Quality Impact |
|---|---|---|---|
| Raw clickstream | 1 year | 90 days | < 3% quality loss |
| User preferences | Indefinite | Account lifetime | No impact |
| Feature values | 1 year | 6 months | < 2% quality loss |
| Model training data | Indefinite | Until next training | No impact |
| Session data | 30 days | 7 days | No impact |

### 5.3 Retention Policy Enforcement

- **Automated checks**: Daily verification of retention compliance
- **Exception handling**: Manual review for retention exceptions
- **Legal holds**: Override retention for legal preservation requirements
- **Audit reporting**: Monthly retention compliance report

---

## 6. Anonymization as Alternative

### 6.1 When to Anonymize Instead of Minimize

| Scenario | Approach | Rationale |
|---|---|---|
| Research datasets | Full anonymization | No need for re-identification |
| Analytics | Aggregation + anonymization | Insights without individual data |
| Model training | Differential privacy | Privacy-preserving training |
| Data sharing | K-anonymity + l-diversity | Safe external sharing |

### 6.2 Anonymization Techniques for Recommendation Data

| Technique | Application | Privacy Level |
|---|---|---|
| Aggregation | Daily/weekly user metrics | High |
| Generalization | Age groups, location regions | High |
| Perturbation | Add noise to numerical features | Moderate-High |
| Differential privacy | Training data with formal guarantees | Mathematical guarantee |
| Federated learning | Train on device without centralizing | Maximum |

### 6.3 Anonymization Quality Assessment

| Metric | Target | Measurement |
|---|---|---|
| Re-identification risk | < 0.1% | Formal risk assessment |
| Data utility | > 80% of original | ML model performance comparison |
| K-anonymity | k ≥ 10 | Quasi-identifier analysis |
| L-diversity | l ≥ 3 | Sensitive attribute analysis |
| T-closeness | t ≤ 0.1 | Distribution analysis |
