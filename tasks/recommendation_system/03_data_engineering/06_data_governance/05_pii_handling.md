# PII Handling in Recommendation Systems

## Overview

Personally Identifiable Information (PII) is any data that can identify a specific individual. Recommendation systems process vast amounts of PII—user identifiers, behavioral data, demographic information, location data, and device identifiers. Proper PII handling is a legal requirement (GDPR, CCPA, LGPD) and a trust imperative. This document covers detection, classification, pseudonymization, tokenization, masking, consent management, and right to erasure implementation.

---

## PII Detection and Classification

### PII Categories

| Category | Examples | Sensitivity | Regulatory Scope |
|---|---|---|---|
| **Direct identifiers** | Name, email, phone, SSN, passport number | Critical | GDPR, CCPA, all regulations |
| **Indirect identifiers** | User ID, device ID, IP address, cookie ID | High | GDPR (if linkable to individual) |
| **Demographic** | Age, gender, nationality, religion | High | GDPR special categories |
| **Behavioral** | Browsing history, search queries, purchase history | Medium | GDPR (personal data) |
| **Location** | GPS coordinates, IP geolocation, address | High | GDPR (personal data) |
| **Financial** | Credit card numbers, bank accounts, income | Critical | PCI DSS, GDPR |
| **Health** | Medical history, fitness data, dietary restrictions | Critical | GDPR special categories, HIPAA |

### PII Detection Methods

**Pattern-based detection**: Regular expressions and pattern matching for structured PII:

| PII Type | Detection Pattern |
|---|---|
| Email addresses | RFC 5322 regex pattern |
| Phone numbers | E.164 format, country-specific patterns |
| Credit card numbers | Luhn algorithm + BIN ranges |
| Social security numbers | Country-specific formats (XXX-XX-XXXX for US) |
| IP addresses | IPv4 and IPv6 regex patterns |
| UUIDs | Standard UUID format (check if used as user identifiers) |

**ML-based detection**: Train a named entity recognition (NER) model to detect PII in unstructured text (search queries, reviews, messages):

- **Model**: Fine-tuned BERT or spaCy NER model on PII-annotated data.
- **Entity types**: PERSON, EMAIL, PHONE, ADDRESS, ORGANIZATION, IP_ADDRESS.
- **Confidence threshold**: High confidence (> 0.9) for automated masking, medium (0.7–0.9) for human review.

**Metadata-based detection**: Identify PII by analyzing column names, data types, and data distributions:

- Column names containing `name`, `email`, `phone`, `address`, `ssn`, `dob` are likely PII.
- High-cardinality string columns in user tables may contain PII.
- Columns with formats matching PII patterns (e.g., date columns with birthdate ranges) may be PII.

### PII Classification Framework

| Classification Level | Description | Handling Requirements |
|---|---|---|
| **Restricted** | Direct identifiers (name, SSN, email) | Encrypt at rest, mask for non-prod, access logging |
| **Confidential** | Indirect identifiers (user ID, device ID) | Encrypt at rest, pseudonymize for non-prod |
| **Internal** | Behavioral data (clicks, views) | Access controls, retention limits |
| **Public** | Non-personal data (item catalog, categories) | No special handling required |

---

## Pseudonymization

### What is Pseudonymization?

Pseudonymization replaces PII with artificial identifiers (pseudonyms) that cannot be directly linked back to the individual without access to a separate mapping table. It is a GDPR-recognized safeguard that reduces risk while preserving data utility for ML training.

### Pseudonymization Approaches

**Deterministic hashing**: Apply a cryptographic hash function (SHA-256) with a secret salt to PII fields:

- **Advantage**: Consistent—same input always produces the same pseudonym. Enables joins and aggregations.
- **Disadvantage**: Reversible if the salt is compromised. Not suitable for the highest-sensitivity PII.
- **Use case**: User IDs, email addresses for feature computation.

**Format-preserving encryption (FPE)**: Encrypt PII while preserving its format (e.g., email address remains a valid email format):

- **Advantage**: Downstream systems that expect a specific format continue to work.
- **Disadvantage**: More complex to implement. Limited standardization.
- **Use case**: Phone numbers, credit card numbers where format validation exists.

**Tokenization**: Replace PII with random tokens managed by a tokenization service:

- **Advantage**: Tokens are not reversible without the token vault. Strong security.
- **Disadvantage**: Requires a high-availability tokenization service. Adds latency to joins.
- **Use case**: Highest-sensitivity PII (SSN, financial data).

### Pseudonymization for ML Training

When preparing data for model training:

1. **Pseudonymize user identifiers**: Replace user_id with a pseudonym that is consistent across the training dataset.
2. **Preserve item identifiers**: Item IDs are typically not PII and can be retained as-is.
3. **Pseudonymize free text**: Replace named entities in search queries, reviews, and messages with generic tokens.
4. **Retain behavioral features**: Click sequences, purchase patterns, and browsing behavior are pseudonymized at the user level but retain their temporal and categorical properties.

---

## Data Masking for Non-Production Environments

### Masking Strategies

| Strategy | Description | Use Case |
|---|---|---|
| **Redaction** | Replace with fixed string (e.g., `[REDACTED]`) | Maximum privacy, low utility |
| **Substitution** | Replace with realistic fake data | Development, testing |
| **Shuffling** | Randomly permute values within a column | Preserves distribution, breaks associations |
| **Nulling** | Set to NULL | Simple, loses distribution properties |
| **Truncation** | Remove partial data (e.g., mask middle digits) | Partial utility retention |
| **Aggregation** | Replace with aggregated values | Preserves statistical properties |

### Masking Rules by Environment

| Environment | Masking Level | Rationale |
|---|---|---|
| **Production** | No masking (full data) | Required for real-time serving |
| **Staging** | Partial masking (pseudonymized) | Test with realistic data shapes |
| **Development** | Full masking (fake data) | Maximum privacy protection |
| **CI/CD** | Synthetic data only | No real PII in test pipelines |
| **Data science notebooks** | Pseudonymized with access controls | Research requires realistic data |
| **Third-party vendors** | Fully anonymized or synthetic | Contractual and regulatory requirements |

### Automated Masking Pipeline

1. **Scan**: Automatically detect PII in datasets using detection rules and ML models.
2. **Classify**: Assign sensitivity levels based on PII type and context.
3. **Select strategy**: Choose the appropriate masking strategy based on the target environment.
4. **Apply**: Execute masking transformations consistently across all copies of the data.
5. **Verify**: Validate that masked data no longer contains detectable PII.
6. **Document**: Record masking decisions for audit purposes.

---

## Consent Management

### Consent Framework

Consent management tracks user consent for data collection and processing. It determines what data can be collected, how it can be used, and for what purposes.

| Consent Type | Scope | Granularity |
|---|---|---|
| **Essential** | Data necessary for service operation | Cannot be declined |
| **Personalization** | Data used for recommendations | Per-category opt-in |
| **Analytics** | Data used for analytics and reporting | Global opt-in |
| **Marketing** | Data used for targeted advertising | Per-channel opt-in |
| **Third-party sharing** | Data shared with partners | Per-partner opt-in |

### Consent in Recommendation Systems

| Feature Category | Required Consent | Fallback Without Consent |
|---|---|---|
| Personalized recommendations | Personalization consent | Popularity-based recommendations |
| Targeted ads | Marketing consent | Contextual ads |
| Cross-device tracking | Personalization + third-party | Device-specific recommendations |
| Behavioral analytics | Analytics consent | Aggregate analytics only |
| Profile building | Personalization consent | No profile, session-only features |

### Consent Storage and Enforcement

- **Consent registry**: Store user consent records with timestamp, consent version, and revocation history.
- **Real-time enforcement**: Check consent status before collecting or using data. Use a low-latency consent service (Redis-cached).
- **Consent propagation**: When consent is revoked, propagate the revocation to all downstream systems within the required timeframe.
- **Audit trail**: Log all consent changes and consent checks for regulatory compliance.

---

## Right to Erasure Implementation

### Erasure Request Workflow

| Step | Action | Timeline |
|---|---|---|
| 1. **Receive request** | User submits deletion request via app/API | Immediate |
| 2. **Verify identity** | Confirm the requester is the data subject | < 24 hours |
| 3. **Assess scope** | Identify all systems containing the user's data | < 24 hours |
| 4. **Check exceptions** | Legal hold, active transactions, regulatory requirements | < 48 hours |
| 5. **Execute deletion** | Delete from all applicable systems | < 30 days (GDPR) |
| 6. **Notify downstream** | Inform partners/systems that received the data | < 30 days |
| 7. **Verify deletion** | Confirm data is removed from all systems | < 45 days |
| 8. **Certificate** | Issue deletion certificate to the user | < 48 hours after verification |

### Erasure in Recommendation Systems

| System | Erasure Method | Challenge |
|---|---|---|
| **Feature store** | Delete user feature vectors | Must not affect other users' features |
| **Training data** | Exclude user data from future training, retrain models | Models may retain learned patterns |
| **Interaction logs** | Delete or anonymize user events | Must maintain aggregate statistics |
| **Search indices** | Rebuild index excluding user data | Time-consuming for large indices |
| **Cache (Redis)** | Delete user cache keys | May cause temporary cache misses |
| **Backups** | Mark for deletion at next rotation | Data persists until backup expires |
| **Third-party systems** | Notify partners to delete | Enforcement relies on contracts |

### Erasure Impact on Recommendations

Deleting a user's data affects:

- **User features**: All user-specific features are removed. The user reverts to cold-start recommendations.
- **Collaborative filtering**: The user's interactions are removed from co-occurrence matrices. Impact is minimal for large datasets.
- **Social features**: Friend connections and social graph edges involving the user are removed.
- **A/B test data**: The user's experiment assignments and outcomes are removed. This may slightly affect experiment statistics.

### Erasure Monitoring

- **Deletion SLA tracking**: Monitor the time from request to completion. Alert if approaching the 30-day GDPR deadline.
- **Completeness verification**: Periodically scan all systems to verify that deleted users' data is actually removed.
- **Third-party compliance**: Track deletion confirmation from third-party partners.
- **Audit reporting**: Generate regular reports on deletion requests, completion rates, and SLA compliance.
