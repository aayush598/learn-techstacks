# Data Masking

## 1. Overview

Data masking transforms sensitive data into a safe representation that preserves data
utility while preventing unauthorized access to original values. For recommendation
systems, data masking is essential for protecting user PII in non-production environments,
logs, debugging outputs, and shared datasets. This document covers static masking, dynamic
masking, tokenization, format-preserving encryption, masking strategies for non-production
environments, and PII detection.

### 1.1 Data Classification for Masking

| Classification | Examples | Masking Required | Masking Level |
|---|---|---|---|
| Highly sensitive | SSN, credit card, health data | Always | Full masking |
| Personally identifiable | Name, email, phone, address | Always | Full or partial masking |
| Indirectly identifiable | IP, device ID, location | Context-dependent | Partial masking or tokenization |
| Behavioral | Click history, purchase patterns | Rarely | Aggregation or anonymization |
| Non-sensitive | Item data, categories, prices | Never | None |

---

## 2. Static Masking

### 2.1 What is Static Masking?

Static masking permanently replaces sensitive data with masked values. The original data
is not recoverable. Used for creating non-production environments and shared datasets.

### 2.2 Static Masking Techniques

| Technique | Example | Reversible | Utility Preserved |
|---|---|---|---|
| Full redaction | `john@email.com` → `[REDACTED]` | No | None |
| Partial masking | `john@email.com` → `j***@email.com` | No | Partial (domain visible) |
| Hashing | `john@email.com` → `a3f2b8c1d4e5...` | No | Pseudonymity |
| Shuffling | `john@email.com` → `mike@other.com` | No | Distribution preserved |
| Nullification | `john@email.com` → `null` | No | None |
| Constant | `john@email.com` → `test@test.com` | No | None |
| Generalization | `age: 27` → `age: 25-30` | No | Partial |

### 2.3 Static Masking Pipeline

```
Source Data → PII Detection → Classification → Masking Rules → Masked Output → Validation
      ↓              ↓              ↓                ↓              ↓             ↓
  Production    Detect all     Classify by       Apply type-     Write masked  Verify no
  database      sensitive      sensitivity       specific        data to       original
                fields         level             masking         target        data remains
```

### 2.4 Static Masking Consistency

Ensure consistent masking across related data:

- **Referential integrity**: Same email masked to same value across all tables
- **Cross-table consistency**: User ID mappings consistent across databases
- **Temporal consistency**: Same user masked consistently over time
- **Cross-system consistency**: Same PII masked identically across services

---

## 3. Dynamic Masking

### 3.1 What is Dynamic Masking?

Dynamic masking masks data in real-time based on the requester's authorization level.
Original data is preserved but different users see different representations.

### 3.2 Dynamic Masking Levels

| User Role | Name | Email | Phone | Location |
|---|---|---|---|---|
| Admin | Full name | Full email | Full phone | Exact location |
| Data scientist | First name + last initial | Partial email | Masked | City level |
| Analyst | Anonymous ID | Masked | Masked | Region level |
| External partner | Token | Redacted | Redacted | Country level |
| Public | Not available | Not available | Not available | Not available |

### 3.3 Dynamic Masking Implementation

```
Query Request → Authorization Check → Apply Masking Rules → Return Masked Data
      ↓                ↓                     ↓                    ↓
  User identifies   Check user role      Role determines     Different users
  themselves        and permissions      masking level       see different data
```

### 3.4 Database-Level Dynamic Masking

Most databases support native dynamic masking:

- **PostgreSQL**: Column-level security policies with masking functions
- **MySQL**: View-based masking with different views per role
- **SQL Server**: Dynamic data masking (built-in feature)
- **BigQuery**: Column-level security with policy tags

---

## 4. Tokenization

### 4.1 What is Tokenization?

Tokenization replaces sensitive data with a non-sensitive equivalent (token) that has
no exploitable value. Unlike hashing, tokenization is reversible with the token vault.

### 4.2 Tokenization Architecture

```
Original Data → Tokenization Service → Token Vault → Token
                                          ↓
                                    ┌─────┴─────┐
                                    ↓           ↓
                              Token Store   Mapping Table
                              (Redis)       (Encrypted DB)
```

### 4.3 Tokenization Properties

| Property | Description |
|---|---|
| Irreversibility without vault | Token alone reveals nothing about original |
| Format flexibility | Token can match original format or differ |
| Deterministic | Same input → same token (deterministic tokenization) |
| Vault security | Token vault encrypted with HSM-backed keys |
| Audit trail | All tokenization/detokenization events logged |

### 4.4 Tokenization Use Cases

| Use Case | Original | Token | Format |
|---|---|---|---|
| User ID mapping | `usr_a1b2c3d4` | `tok_x9y8z7w6` | Different format |
| Email pseudonym | `john@email.com` | `abc123@example.com` | Similar format |
| Phone masking | `+1-555-123-4567` | `+1-555-000-1234` | Same format |
| Credit card | `4111-1111-1111-1111` | `4111-0000-0000-1234` | Same format |

---

## 5. Format-Preserving Encryption (FPE)

### 5.1 What is FPE?

Format-Preserving Encryption encrypts data while maintaining the original format
(length, character set, pattern). Useful when downstream systems expect specific formats.

### 5.2 FPE Algorithms

| Algorithm | Standard | Format | Use Case |
|---|---|---|---|
| FF1 | NIST SP 800-38G | Variable length | General purpose |
| FF3-1 | NIST SP 800-38G | Fixed length | Credit cards, SSNs |
| FF3-1 (tweaked) | Custom | Variable | Flexible format |

### 5.3 FPE Examples

| Data Type | Original | FPE Output | Format Preserved |
|---|---|---|---|
| SSN | 123-45-6789 | 987-65-4321 | Yes (3-2-4 format) |
| Credit card | 4111-1111-1111-1111 | 4532-8194-7261-3057 | Yes (4-4-4-4 format) |
| Phone | (555) 123-4567 | (555) 987-6543 | Yes ((3) 3-4 format) |
| Email local | john.doe | k8m2.p9 | Partial (length varies) |

---

## 6. Masking for Non-Production Environments

### 6.1 Environment-Specific Masking

| Environment | Masking Level | Data Source | Purpose |
|---|---|---|---|
| Development | Full masking | Synthetic data | Local development |
| Testing | Full masking | Masked production | Integration testing |
| Staging | Partial masking | Anonymized production | Pre-deployment validation |
| Pre-production | Dynamic masking | Production (masked) | Performance testing |
| Production | Dynamic masking (per role) | Real data | Live serving |

### 6.2 Non-Production Data Pipeline

```
Production Data → Extraction → PII Detection → Masking Engine → Validation → Target Environment
                      ↓              ↓               ↓              ↓
                 Read replica    Detect PII      Apply masking   Verify no PII
                 (no impact)     fields          rules           remains
```

### 6.3 Masking Rule Configuration

```yaml
masking_rules:
  email:
    type: "partial_mask"
    pattern: "^([a-zA-Z0-9]).*?@(.+)$"
    mask: "$1***@$2"
    environments: ["staging", "testing", "development"]

  phone:
    type: "format_preserving"
    format: "+X-XXX-XXX-XXXX"
    mask_last_digits: 4
    environments: ["staging", "testing"]

  name:
    type: "shuffle"
    consistent: true
    salt: "environment_specific_salt"
    environments: ["testing", "development"]

  ssn:
    type: "full_redact"
    replacement: "[SSN_REDACTED]"
    environments: ["staging", "testing", "development"]
```

---

## 7. PII Detection and Masking

### 7.1 PII Detection Methods

| Method | Coverage | Accuracy | Speed |
|---|---|---|---|
| Regex patterns | Known formats | High | Fast |
| NER (Named Entity Recognition) | Names, organizations | Moderate | Slow |
| ML classification | Custom PII types | High | Moderate |
| Column profiling | Statistical patterns | Moderate | Fast |
| Schema-based | Known field names | High (if schema known) | Fast |

### 7.2 PII Detection Patterns

| PII Type | Detection Pattern | Example |
|---|---|---|
| Email | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | john@example.com |
| Phone (US) | `\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}` | +1-555-123-4567 |
| SSN | `[0-9]{3}-[0-9]{2}-[0-9]{4}` | 123-45-6789 |
| Credit card | `[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}` | 4111-1111-1111-1111 |
| IP address | `\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b` | 192.168.1.100 |
| UUID | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` | 550e8400-e29b-41d4-a716-446655440000 |

### 7.3 Automated PII Detection Pipeline

```
Data Ingestion → PII Scanner → Classification → Masking Rules Engine → Masked Output
                    ↓              ↓                    ↓
              ┌─────┼─────┐   Sensitivity         Rule selection
              ↓     ↓     ↓   scoring             per data type
           Regex  NER  Column
           scan  scan  profiling
```

### 7.4 PII Detection Monitoring

- **Detection rate**: Percentage of PII correctly identified
- **False positive rate**: Non-PII incorrectly flagged (target: < 1%)
- **False negative rate**: PII missed by detection (target: < 0.1%)
- **New PII type detection**: Monitoring for previously unknown PII patterns
- **Detection rule updates**: Regular updates to detection patterns
