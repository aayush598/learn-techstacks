# GDPR Compliance for Recommendation Systems

## Overview

The General Data Protection Regulation (GDPR) imposes strict requirements on how recommendation
systems collect, process, store, and share personal data. Recommendation systems are particularly
affected because they process behavioral data (clicks, views, purchases), infer preferences,
and create user profiles for personalization. This document covers lawful basis for processing,
data minimization, consent management, user rights implementation, privacy by design, and
cross-border data transfer requirements.

## How GDPR Applies to Recommendation Systems

### Personal Data in Recommendation Context

| Data Category          | Examples                                      | GDPR Classification |
|-----------------------|-----------------------------------------------|---------------------|
| Direct identifiers    | Email, name, phone number                     | Personal data       |
| Behavioral data       | Clicks, views, searches, purchases            | Personal data       |
| Inferred preferences  | Genre affinity, price sensitivity scores      | Personal data       |
| Device/browser data   | IP address, user agent, device ID             | Personal data       |
| Location data         | GPS coordinates, city-level location          | Personal data       |
| Derived profiles      | User embedding vectors, segment assignments  | Personal data       |
| Recommendation logs   | What was recommended, what was clicked        | Personal data       |

### Special Categories

Behavioral data used for profiling may constitute "special categories" if it reveals:
- Political opinions
- Religious beliefs
- Health conditions
- Sexual orientation
- Trade union membership

A movie recommendation system that infers political leanings from viewing habits processes
special category data and requires explicit consent.

## Lawful Basis for Processing

### Basis Selection for Recommendation Processing

| Processing Activity              | Lawful Basis       | Rationale                                    |
|----------------------------------|--------------------|----------------------------------------------|
| Collecting browsing behavior     | Legitimate interest| Required for service functionality            |
| Creating user profiles           | Consent            | Profiling requires explicit consent           |
| Personalized recommendations     | Consent            | Direct marketing / profiling                  |
| Anonymous analytics              | Legitimate interest| No personal data processed                    |
| Fraud detection                  | Legitimate interest| Security is legitimate interest               |
| Sharing with third parties       | Consent            | Data sharing requires explicit consent        |
| Storing interaction history      | Legitimate interest| Required for service improvement              |

### Legitimate Interest Assessment (LIA)

For each processing activity based on legitimate interest:

1. **Purpose test**: Is there a legitimate interest? (Yes — providing relevant recommendations)
2. **Necessity test**: Is processing necessary for that purpose? (Yes — cannot personalize without data)
3. **Balancing test**: Do individual rights override? (Assess and document)

### Consent Requirements

Consent must be:
- **Freely given**: Not bundled with terms of service
- **Specific**: Separate consent for each processing purpose
- **Informed**: Clear explanation of what data is collected and how used
- **Unambiguous**: Affirmative action (no pre-checked boxes)
- **Withdrawable**: Easy as giving consent, accessible at any time

## Data Minimization

### Collect Only What Is Necessary

| Data Point              | Necessary? | Justification                               |
|------------------------|-----------|----------------------------------------------|
| User ID                | Yes       | Required to identify user                    |
| Item interactions      | Yes       | Core input for recommendations               |
| Timestamps of actions  | Yes       | Required for recency weighting               |
| Email address          | No*       | Only for account creation, not for recs      |
| Full name              | No        | Never needed for recommendations             |
| Location (GPS)         | Maybe     | Only if location-based recs are a feature    |
| Browsing history       | Depends   | Only if cross-site personalization is active |
| Device fingerprint     | No        | Excessive for recommendation purposes        |
| Social connections     | Maybe     | Only for social recommendations              |

### Data Retention Policy

```
Retention Schedule:
├── Active user interactions:    Duration of account + 30 days
├── Inactive user interactions:  90 days after last activity
├── Recommendation logs:         30 days
├── A/B test assignment data:    Duration of experiment + 30 days
├── Model training data:         Anonymize after model deployment
├── Feature vectors:             Duration of account + 30 days
├── Audit logs:                  7 years (legal requirement)
└── Consent records:             Duration of account + 3 years
```

### Anonymization and Pseudonymization

**Pseudonymization** (recommended for most processing):
- Replace user_id with a pseudonymous identifier
- Keep mapping table in separate, access-controlled store
- Enables data recovery if needed
- Still considered personal data under GDPR

**Anonymization** (for analytics and model training):
- Irreversible removal of personal identifiers
- K-anonymity: each record is indistinguishable from at least K-1 others
- Data is no longer personal data under GDPR
- Cannot be used to generate personalized recommendations

## User Consent Management

### Consent Banner Implementation

```
Consent Categories:
├── Essential cookies        (always active, no consent needed)
│   └── Session management, security tokens
├── Functional cookies       (consent required)
│   └── Language preferences, UI customization
├── Analytics cookies        (consent required)
│   └── Page views, feature usage, performance
└── Personalization cookies  (consent required)
    └── Recommendation tracking, preference learning
```

### Consent Record Schema

Every consent decision must be recorded with:
- User identifier (pseudonymous)
- Timestamp of consent decision
- Specific purposes consented to
- Version of privacy notice presented
- Method of consent collection (banner, settings page, etc.)
- IP address at time of consent (for fraud detection)
- Withdrawal timestamp (if consent was withdrawn)

### Consent API

```
Endpoints:
  POST   /api/v1/consent           — Record consent decision
  GET    /api/v1/consent/{user_id} — Retrieve consent status
  PUT    /api/v1/consent/{user_id} — Update consent preferences
  DELETE /api/v1/consent/{user_id} — Withdraw all consent
```

## User Rights Implementation

### Right to Access (Article 15)

Users can request a copy of all personal data processed about them:

**Implementation requirements**:
- API endpoint to trigger data export
- Export must include all data categories (interactions, profiles, preferences)
- Machine-readable format (JSON or CSV)
- Delivered within 30 days of request
- Free of charge for first request

**Data categories to include in export**:
1. Account information
2. All interaction events (views, clicks, purchases, searches)
3. User profile and preference data
4. Recommendation history (what was shown, what was clicked)
5. Consent records
6. Feature vectors computed from their data
7. Any derived segments or categories

### Right to Erasure (Article 17)

Users can request deletion of all personal data:

**Implementation requirements**:
- Delete user profile, interactions, and derived data
- Remove from all recommendation model training pipelines
- Delete from backups within reasonable timeframe (or anonymize)
- Notify downstream processors of erasure request
- Log erasure event for compliance audit (but not the data itself)

**Erasure challenges for recommendation systems**:
- Model training data: Anonymize user's historical data in training sets
- Model artifacts: Retrain model excluding deleted user's data (if practical)
- Aggregated statistics: May be retained if anonymized
- Recommendation logs: Delete within 30 days
- Feature store entries: Delete immediately

### Right to Data Portability (Article 20)

Users can request their data in a machine-readable format:

- Export in JSON, CSV, or industry-standard format
- Include all data explicitly provided by the user
- Include data generated through usage (interactions, preferences)
- Deliver via secure download link or API endpoint
- Data must be structured, commonly used, and machine-readable

### Right to Object (Article 21)

Users can object to processing based on legitimate interest:

- Object to profiling for personalization
- Object to targeted recommendations
- System must honor objection immediately
- Provide non-personalized alternatives (popular items, editorial picks)
- Cannot degrade service quality for users who object

## Privacy by Design

### Architecture Principles

1. **Default privacy**: New features are privacy-protective by default
2. **Data minimization**: Default to collecting the minimum necessary data
3. **Purpose limitation**: Data collected for recommendations is not repurposed without consent
4. **Storage limitation**: Automatic data deletion after retention period
5. **Integrity and confidentiality**: Encryption and access controls by default

### Privacy Impact on System Design

| Component               | Privacy Design Decision                                |
|------------------------|--------------------------------------------------------|
| Event collection       | Pseudonymize user IDs before storage                    |
| Feature store          | Separate PII from behavioral features                  |
| Model training         | Train on anonymized/pseudonymized data                  |
| Recommendation logs    | Store only pseudonymous IDs, rotate pseudonyms         |
| API responses          | Never expose PII in recommendation responses           |
| Analytics              | Use differential privacy for aggregate metrics         |
| Logging                | Scrub PII from application logs                        |
| Cache                  | Encrypt cached user features at rest                   |

### Differential Privacy for Recommendations

When using user data for aggregate analytics or model improvement:
- Add calibrated noise to user interaction counts
- Set epsilon (privacy budget) based on sensitivity
- Typical epsilon for recommendation analytics: 1.0 - 10.0
- Track cumulative privacy budget per user
- Never query user data beyond their privacy budget

## Data Protection Impact Assessment (DPIA)

### When Is a DPIA Required?

A DPIA is required when processing is likely to result in high risk:
- Systematic profiling of users
- Large-scale processing of behavioral data
- Automated decision-making with significant effects
- Processing special category data

A recommendation system that profiles users for personalization **always requires a DPIA**.

### DPIA Content for Recommendation System

```
DPIA Document Structure:
1. Description of processing
   - What data is collected
   - How it is processed
   - What the purposes are

2. Assessment of necessity and proportionality
   - Is all collected data necessary?
   - Are there less intrusive alternatives?
   - How is data quality maintained?

3. Risk assessment
   - Risk of unauthorized access to user profiles
   - Risk of re-identification from pseudonymized data
   - Risk of discriminatory recommendations
   - Risk of manipulation through filter bubbles

4. Mitigation measures
   - Encryption at rest and in transit
   - Access controls and audit logging
   - Regular bias audits of recommendation algorithms
   - User transparency and control mechanisms

5. Consultation
   - DPO review and approval
   - Legal team sign-off
   - Technical architecture review
```

## Cross-Border Data Transfers

### Transfer Mechanisms

| Mechanism                           | When to Use                              |
|-------------------------------------|------------------------------------------|
| Standard Contractual Clauses (SCCs) | Default for EU-to-non-EU transfers       |
| Binding Corporate Rules (BCRs)      | Intra-company transfers within a group   |
| Adequacy Decision                   | Transfer to countries with adequacy ruling|
| derogations (Art. 49)               | One-off, specific situations only        |

### Technical Measures for Cross-Border Transfers

When personal data leaves the EU:
- Encrypt data in transit (TLS 1.3) and at rest (AES-256)
- Pseudonymize before transfer where possible
- Implement access controls preventing unauthorized access in destination country
- Maintain data transfer impact assessment
- Monitor for changes in destination country's legal framework

### Recommendation System Data Flow Compliance

```
EU User Data Flow:
User (EU) → API Gateway (EU) → Recommendation Service (EU)
                                    │
                                    ├── Feature Store (EU) ✓
                                    ├── Model Serving (EU) ✓
                                    ├── Analytics (EU) ✓
                                    └── ML Training (EU or adequate country)
                                           │
                                           └── If non-EU: SCCs + encryption + DPIA
```
