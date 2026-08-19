# Test Data Management for Recommendation Systems

## 1. Overview

Test data management is the foundation of reliable ML system testing. For recommendation
systems, test data must accurately represent production data characteristics while remaining
safe for testing environments. This document defines the comprehensive test data management
strategy covering golden datasets, synthetic data generation, production sampling, versioning,
masking, and freshness management.

### 1.1 Test Data Challenges in Recommendation Systems

- **Scale**: Production datasets span terabytes; test data must be representative yet manageable
- **Temporal dynamics**: User-item interactions evolve over time; test data must capture temporal patterns
- **Sparsity**: User-item matrices are 99%+ sparse; test data must preserve sparsity characteristics
- **Privacy**: Production data contains PII; test data must be anonymized or synthetic
- **Reproducibility**: Tests must produce deterministic results despite stochastic data sources
- **Multi-modal data**: Interactions, content features, user profiles, and contextual signals

---

## 2. Golden Datasets

### 2.1 What is a Golden Dataset?

A golden dataset is a curated, validated, and versioned snapshot of production data used as
the authoritative reference for regression testing. It serves as the ground truth against
which all system changes are evaluated.

### 2.2 Golden Dataset Characteristics

| Characteristic | Requirement | Rationale |
|---|---|---|
| Representativeness | Matches production distribution | Ensures test results predict production behavior |
| Stability | Fixed content (no mutation) | Enables deterministic regression comparisons |
| Coverage | Spans all edge cases | Catches regressions in rare scenarios |
| Anonymization | No real PII | Safe for testing environments |
| Ground truth | Known correct outputs | Enables automated validation |
| Versioned | Immutable with metadata | Enables historical comparison |

### 2.3 Golden Dataset Construction

**Step 1: Data Selection**

Production data is sampled using stratified sampling to ensure representation across:

- **User segments**: Active, dormant, new, power users (by activity percentile)
- **Item categories**: All content categories with minimum sample sizes
- **Interaction types**: Clicks, purchases, saves, shares, dismissals
- **Temporal ranges**: Multiple time windows capturing seasonal patterns
- **Geographic diversity**: Different regions if recommendations are geo-sensitive

**Step 2: Ground Truth Annotation**

For each user-item pair in the golden dataset, ground truth labels are established:

```
Ground Truth Categories:
├── Explicit positive: User purchased, saved, or shared the item
├── Implicit positive: User spent > 2x average dwell time on item
├── Explicit negative: User dismissed or reported the item
├── Implicit negative: Item shown but not interacted (with impression data)
└── Unknown: Insufficient signal (excluded from evaluation)
```

**Step 3: Validation and Quality Gates**

- Statistical tests comparing golden dataset distributions to production
- Manual review of sampled records for annotation accuracy
- Consistency checks across related data points
- Completeness verification (no missing required fields)

### 2.4 Golden Dataset Versioning

Each golden dataset version includes:

| Field | Description | Example |
|---|---|---|
| Version | Semantic version string | `2.4.0` |
| Source date range | Production data time window | `2026-01-01 to 2026-01-31` |
| Sampling method | How the subset was selected | `Stratified by user segment` |
| Size | Record count and storage | `5M interactions, 2.3 GB` |
| Annotation method | How ground truth was established | `Manual + heuristic` |
| Known limitations | Coverage gaps or biases | `Under-represents new users` |
| Retention date | When this version expires | `2026-07-01` |

### 2.5 Golden Dataset Refresh Cadence

- **Monthly refresh**: Update golden dataset with recent production data
- **Quarterly audit**: Full review of representativeness and annotation quality
- **Event-driven refresh**: Update when major product changes alter data patterns
- **Rolling golden datasets**: Maintain 3 versions (current, previous, legacy) for trend analysis

---

## 3. Synthetic Data Generation

### 3.1 When to Use Synthetic Data

- Testing edge cases not present in production data
- Generating large-scale datasets for performance testing
- Creating controlled scenarios for targeted testing
- Filling coverage gaps identified by test analysis
- Testing with data patterns that don't yet exist in production

### 3.2 Synthetic Data Generation Approaches

#### 3.2.1 Rule-Based Generation

Define explicit rules to generate data matching specific patterns:

```
Rule-Based Generation Parameters:
├── User profiles: Age distribution N(35, 10), activity rate Poisson(5/day)
├── Item catalog: Category weights from production distribution
├── Interaction patterns: CTR by category from historical data
├── Temporal patterns: Peak hours 7-9 AM, 6-10 PM local time
├── Social graph: Power law degree distribution for follows/connections
└── Implicit feedback: Dwell time Gamma(α=2, β=60) seconds
```

**Advantages:** Deterministic, explainable, easy to tune
**Limitations:** May miss complex real-world patterns and correlations

#### 3.2.2 Statistical Distribution Matching

Use statistical models fitted to production data to generate synthetic samples:

- Fit marginal distributions for each feature
- Model pairwise correlations using copulas
- Preserve temporal autocorrelation patterns
- Match sparsity patterns in interaction matrices

#### 3.2.3 Generative Model-Based

Use ML models trained on production data to generate synthetic samples:

- **GANs**: Generate realistic interaction sequences
- **VAEs**: Learn latent representations and sample new data points
- **LLMs**: Generate synthetic user profiles and behavior descriptions
- **Agent-based simulation**: Model individual user behavior rules and simulate populations

#### 3.2.4 Data Synthesis Tools

| Tool | Approach | Best For | Limitation |
|---|---|---|---|
| SDV (Synthetic Data Vault) | Statistical | Tabular data | Complex temporal patterns |
| Gretel.ai | Deep learning | Privacy-sensitive data | Requires training |
| Faker | Template-based | Simple entity generation | No correlation preservation |
| Custom simulators | Domain-specific | Recommendation interactions | Development overhead |
| SynthBio | Bayesian | User behavior sequences | Narrow domain |

### 3.3 Synthetic Data Quality Validation

Synthetic data must be validated against these quality dimensions:

- **Statistical fidelity**: Distribution similarity (KS test, Wasserstein distance)
- **Correlation preservation**: Pairwise feature correlations within tolerance
- **Privacy compliance**: No memorization of real records (nearest neighbor distance)
- **Utility preservation**: ML models trained on synthetic data perform comparably
- **Plausibility**: Human review of sampled records for logical consistency

---

## 4. Production Data Sampling

### 4.1 Sampling Strategies

| Strategy | Description | Use Case | Bias Risk |
|---|---|---|---|
| Random sampling | Uniform random selection | General testing | Low |
| Stratified sampling | Proportional to population strata | Representative testing | Low |
| Cluster sampling | Sample entire clusters | Multi-tenant testing | Medium |
| Reservoir sampling | Fixed-size sample from stream | Real-time testing | Low |
| Importance sampling | Weighted by relevance | Rare event testing | Medium |
| Temporal sampling | Time-windowed extraction | Seasonal pattern testing | Low |

### 4.2 Sampling Size Determination

Minimum sample sizes are calculated based on statistical requirements:

- **For distribution testing**: Minimum 10,000 records per category for KS test power
- **For metric estimation**: Sample size for 95% confidence interval width < 1% of metric
- **For A/B test validation**: Minimum detectable effect size determines sample requirements
- **For performance testing**: Sample must represent peak-hour traffic patterns

### 4.3 Production Data Sampling Pipeline

```
Production Database → Extraction Query → Anonymization → Validation → Publication
         ↓                    ↓                ↓              ↓             ↓
    Read replicas      Stratified SQL      PII removal    Distribution   Test env
    (no impact on      with sampling       hashing/       checks &       storage
     primary)          rate control        masking        gap detection
```

**Key constraints:**

- Never sample from primary database; use read replicas only
- Enforce rate limits on extraction to avoid production impact
- All sampled data must pass PII detection before leaving production environment
- Sampling queries must be logged and auditable
- Sampled data must be timestamped and traceable to source

---

## 5. Test Data Versioning

### 5.1 Versioning Strategy

Test data versions follow a structured scheme aligned with semantic versioning:

```
MAJOR.MINOR.PATCH-SCOPE

MAJOR: Breaking change in data schema or structure
MINOR: New data added or significant distribution change
PATCH: Bug fix, annotation correction, or minor update
SCOPE: Dataset identifier (golden-v1, synthetic-interactions, prod-sample-v2)
```

### 5.2 Version Metadata Schema

Each versioned dataset stores:

| Metadata | Description |
|---|---|
| Version identifier | Unique version string |
| Creation timestamp | When the version was created |
| Creator | Who or what created it |
| Source reference | Upstream data source and query |
| Size metrics | Record count, storage size, entity counts |
| Distribution statistics | Key feature distributions for comparison |
| Schema version | Associated schema version |
| Dependencies | Other datasets this version depends on |
| Retention policy | When this version expires |
| Quality score | Automated quality assessment score |

### 5.3 Data Lineage Tracking

Track the complete transformation history from production to test data:

```
Raw Production Data
    ↓ (extraction query)
Raw Sample
    ↓ (PII detection & masking)
Anonymized Sample
    ↓ (schema validation)
Validated Sample
    ↓ (golden dataset annotation)
Golden Dataset v3.2.1
    ↓ (derived datasets)
├── Unit test fixtures (subset)
├── Integration test data (subset)
├── Performance test dataset (scaled)
└── Chaos test dataset (perturbed)
```

### 5.4 Version Compatibility Matrix

| Dataset Version | Compatible System Versions | Expiration |
|---|---|---|
| golden-v3.2.1 | v8.0 - v8.3 | 2026-07-01 |
| golden-v3.1.0 | v7.5 - v8.0 | 2026-04-01 |
| synthetic-v2.0.0 | All versions | 2026-12-31 |
| prod-sample-v5.1.0 | v8.0+ | 2026-03-01 |

---

## 6. Data Masking for Test Environments

### 6.1 Data Classification for Masking

| Data Type | Sensitivity | Masking Required | Example Fields |
|---|---|---|---|
| PII - Direct | Critical | Always | Name, email, phone, SSN |
| PII - Indirect | High | Always | IP address, device ID, location |
| Behavioral data | Medium | Context-dependent | Click history, search queries |
| Content data | Low | Rarely | Item titles, categories, prices |
| Aggregated data | Low | Never | Daily active users, category CTR |

### 6.2 Masking Techniques

#### 6.2.1 Direct Identifier Masking

| Technique | Reversible | Utility Preserved | Example |
|---|---|---|---|
| Hashing (SHA-256) | No | ID uniqueness | `user_123` → `a3f2b8c1...` |
| Tokenization | Yes (with vault) | Full | `user_123` → `tok_4892` |
| Redaction | No | No | `john@email.com` → `[REDACTED]` |
| Generalization | No | Partial | `age: 27` → `age: 25-30` |
| Perturbation | No | Statistical properties | `income: 85000` → `income: 82000` |

#### 6.2.2 Behavioral Data Masking

- **User ID mapping**: Consistent one-way mapping preserving user uniqueness
- **Session shuffling**: Randomize session order while preserving within-session behavior
- **Temporal jittering**: Add ±random hours to timestamps while preserving daily patterns
- **Item ID mapping**: Consistent item ID remapping preserving item relationships
- **Geographic generalization**: City → region, zip code → partial zip code

### 6.3 Automated PII Detection

Implement automated PII detection pipeline:

1. **Pattern-based detection**: Regex patterns for emails, phones, SSNs, credit cards
2. **ML-based detection**: NER models trained to detect names, addresses, organizations
3. **Column-level analysis**: Statistical profiling to identify potentially sensitive columns
4. **Contextual analysis**: Examine column names, data distributions, and sampling patterns
5. **Manual review queue**: Flag uncertain cases for human review

### 6.4 Masking Pipeline Architecture

```
Raw Data → PII Scanner → Classification Engine → Masking Router → Masked Output
              ↓                  ↓                     ↓
         Regex + NER       Sensitivity           Technique
         patterns           scoring              selection
                                                   ↓
                                            ┌──────┼──────┐
                                            ↓      ↓      ↓
                                         Hash   Token  Generalize
                                                ize
```

---

## 7. Test Data Freshness

### 7.1 Freshness Requirements by Test Type

| Test Type | Maximum Age | Rationale |
|---|---|---|
| Unit tests | Static (versioned) | Deterministic, no time dependency |
| Data quality tests | 7 days | Detect recent schema/distribution changes |
| Feature tests | 14 days | Ensure features compute correctly on recent data |
| Integration tests | 30 days | Representative of production patterns |
| ML quality tests | 30 days | Model performance on recent behavior patterns |
| Performance tests | 90 days | Scale characteristics are relatively stable |
| E2E tests | 30 days | End-to-end flow with realistic data |

### 7.2 Freshness Monitoring

Track and alert on test data freshness:

- **Dashboard metrics**: Age of data in each test environment
- **Alerts**: When data exceeds freshness threshold
- **Automated refresh**: Trigger data pipeline when freshness degrades
- **Staleness detection**: Compare test data distributions against production snapshots

### 7.3 Data Freshness Pipeline

```
Production Data → Daily Snapshot → Freshness Check → Auto-Refresh Trigger
                                          ↓
                                    ┌─────┴─────┐
                                    ↓           ↓
                               Fresh enough  Stale
                               (continue)   (refresh)
                                                ↓
                                    Sample → Mask → Validate → Publish
                                                ↓
                                    Update test environment data
                                                ↓
                                    Run smoke tests to validate
```

### 7.4 Freshness Quality Metrics

| Metric | Target | Measurement |
|---|---|---|
| Average data age (integration) | < 14 days | Automated daily check |
| Maximum data age (any env) | < 90 days | Automated daily check |
| Refresh success rate | > 99% | Pipeline monitoring |
| Refresh latency | < 4 hours | Pipeline SLA tracking |
| Distribution drift from production | < 5% KS statistic | Weekly comparison |

### 7.5 Handling Stale Data

When test data exceeds freshness thresholds:

1. **Automated alert**: Notify data engineering team and ML engineers
2. **Triage assessment**: Determine if staleness impacts current test priorities
3. **Emergency refresh**: If P0 tests are affected, trigger immediate refresh
4. **Scheduled refresh**: Otherwise, queue for next scheduled refresh window
5. **Test adjustment**: Temporarily adjust test thresholds if needed during refresh
6. **Root cause analysis**: Investigate why automated refresh failed

---

## 8. Test Data Infrastructure

### 8.1 Storage Architecture

| Storage Tier | Technology | Data Types | Retention |
|---|---|---|---|
| Hot | Redis / Memcached | Test fixtures, mock responses | Session duration |
| Warm | PostgreSQL / MySQL | Golden datasets, version metadata | 1 year |
| Cold | S3 / GCS | Raw samples, historical versions | 3 years |
| Archive | Glacier / Coldline | Compliance datasets | 7 years |

### 8.2 Test Data Service API

A centralized test data service provides:

- **Dataset registration**: Register new test datasets with metadata
- **Version management**: Create, tag, and retire dataset versions
- **Access control**: Role-based access to different dataset sensitivity levels
- **Freshness monitoring**: Automated tracking of dataset age and quality
- **Distribution reporting**: Statistical summaries for dataset comparison
- **Lineage tracking**: Complete transformation history from source to test data

### 8.3 Cost Management

- **Storage lifecycle policies**: Automatic tiering from hot to cold storage
- **Compression**: Columnar formats (Parquet, ORC) for 60-80% compression
- **Deduplication**: Content-addressable storage for identical dataset versions
- **Selective refresh**: Only refresh datasets needed for active test suites
- **Budget alerts**: Monthly cost tracking with budget threshold alerts

---

## 9. Compliance and Governance

### 9.1 Data Governance Requirements

- All test data must be inventoried with source, purpose, and retention period
- PII in test environments requires explicit approval from data protection officer
- Test data access must be logged and auditable
- Cross-region test data transfers must comply with data residency requirements
- Test data must be deleted when no longer needed per retention policies

### 9.2 Audit Trail

Every test data operation is logged:

```
Operation Log:
├── Dataset creation: Who, when, source, size, purpose
├── Access events: Who accessed what, when, from where
├── Modification events: What changed, why, approval reference
├── Deletion events: What was deleted, retention policy applied
└── Distribution events: Where data was sent, encryption status
```
