# Pseudonymization

## 1. Overview

Pseudonymization replaces identifying data with artificial identifiers (pseudonyms)
while maintaining the ability to reverse the mapping for authorized purposes. For
recommendation systems, pseudonymization enables privacy-preserving ML training, analysis,
and sharing while maintaining compliance with GDPR Article 4(5) and CCPA. This document
covers reversible vs irreversible approaches, privacy models, ML training applications,
and re-identification risk assessment.

### 1.1 Pseudonymization vs Related Techniques

| Technique | Reversible | Utility | Re-identification Risk |
|---|---|---|---|
| Pseudonymization | Yes (with key) | High | Low (with proper controls) |
| Anonymization | No | Moderate | Very low |
| Tokenization | Yes (with vault) | High | Low |
| Encryption | Yes (with key) | Full | None (if key secure) |
| Aggregation | No | Low | Very low |

### 1.2 GDPR Pseudonymization Requirements

GDPR Article 4(5) defines pseudonymization as:

> Processing of personal data in such a manner that the data can no longer be attributed
> to a specific data subject without the use of additional information, provided that such
> additional information is kept separately and subject to technical and organizational
> measures.

---

## 2. Reversible vs Irreversible Pseudonymization

### 2.1 Reversible Pseudonymization

Reversible pseudonymization maintains a mapping that can be undone by authorized parties.

| Method | Key Management | Use Case |
|---|---|---|
| HMAC-based | Secret key stored in KMS | User ID mapping for ML |
| AES encryption | Encryption key in vault | Email pseudonymization |
| Format-preserving | Key per format | Credit card, SSN |
| Vault-based | Centralized token vault | Cross-system mapping |

**Reversible pseudonymization process:**

```
Original ID → HMAC(original_id, secret_key) → Pseudonym
                                                ↓
Pseudonym → Lookup vault → Original ID (for authorized access only)
```

### 2.2 Irreversible Pseudonymization

Irreversible pseudonymization cannot be reversed, providing stronger privacy guarantees.

| Method | Properties | Use Case |
|---|---|---|
| Cryptographic hash (SHA-256) | Deterministic, irreversible | Linking datasets |
| Salted hash | Irreversible, no rainbow tables | Secure pseudonymization |
| K-anonymity grouping | Groups records together | Publishing datasets |
| Differential privacy | Mathematical privacy guarantee | Analytics, ML training |

### 2.3 Choosing Between Reversible and Irreversible

| Scenario | Choose | Rationale |
|---|---|---|
| ML training data | Reversible | Need to re-identify for user-specific analysis |
| Published research data | Irreversible | No re-identification needed |
| Cross-system linking | Reversible | Need consistent pseudonyms across systems |
| Internal analytics | Reversible | May need to investigate specific users |
| External data sharing | Irreversible | No trust relationship for re-identification |

---

## 3. K-Anonymity

### 3.1 Definition

K-anonymity ensures that each record is indistinguishable from at least k-1 other records
with respect to quasi-identifiers (combination of attributes that could identify an individual).

### 3.2 K-Anonymity Application

| Quasi-Identifier | Original | 3-Anonymized |
|---|---|---|
| Age | 27 | 25-30 |
| ZIP code | 94102 | 941** |
| Gender | Female | * |
| Occupation | Software Engineer | Technology Professional |

### 3.3 K-Anonymity Levels

| K Value | Privacy Level | Utility | Use Case |
|---|---|---|---|
| k=2 | Low | High | Internal testing |
| k=5 | Moderate | Moderate | Internal analytics |
| k=10 | High | Moderate | Partner data sharing |
| k=50 | Very high | Low | Public data release |
| k=100+ | Maximum | Very low | Research publication |

### 3.4 K-Anonymity Limitations

- **Homogeneity attack**: All records in a group have same sensitive attribute
- **Background attack**: Attacker has external information
- **Solving**: Combine with l-diversity and t-closeness

---

## 4. L-Diversity

### 4.1 Definition

L-diversity extends k-anonymity by requiring at least l "well-represented" values for
the sensitive attribute in each equivalence class.

### 4.2 L-Diversity Examples

| Group | Sensitive Attribute | L Value | Assessment |
|---|---|---|---|
| {Age: 25-30, ZIP: 941**} | {Purchase: electronics, books, clothing} | l=3 | Good diversity |
| {Age: 30-35, ZIP: 100**} | {Purchase: electronics, electronics, electronics} | l=1 | Poor diversity |
| {Age: 35-40, ZIP: 606**} | {Purchase: books, clothing, food, health} | l=4 | Excellent diversity |

### 4.3 L-Diversity Levels

| L Value | Privacy Level | Use Case |
|---|---|---|
| l=2 | Basic | Internal dashboards |
| l=3 | Standard | Partner data sharing |
| l=5 | Strong | Research datasets |
| l=10+ | Maximum | Public releases |

---

## 5. T-Closeness

### 5.1 Definition

T-closeness further refines privacy by requiring that the distribution of the sensitive
attribute in each equivalence class is close to the overall distribution, within threshold t.

### 5.2 T-Closeness Application

| Metric | Formula | Threshold |
|---|---|---|
| Earth Mover's Distance | EMD(class_distribution, overall_distribution) | t < 0.1 |
| KL Divergence | KL(class_distribution || overall_distribution) | t < 0.05 |
| Total Variation Distance | TV(class, overall) | t < 0.1 |

### 5.3 Privacy Model Comparison

| Model | Protects Against | Limitation |
|---|---|---|
| K-anonymity | Identity disclosure | Homogeneity attack |
| L-diversity | Attribute disclosure (homogeneity) | Skewed distribution attack |
| T-closeness | Attribute disclosure (distribution) | Reduces utility significantly |

---

## 6. Pseudonymization for ML Training

### 6.1 Training Data Pseudonymization

| Step | Process | Reversible? |
|---|---|---|
| User ID mapping | Replace user IDs with pseudonymous IDs | Yes (with key) |
| PII removal | Remove names, emails, addresses | No |
| Location generalization | GPS → City → Region | No (by design) |
| Temporal jittering | Add ±random to timestamps | No |
| Feature pseudonymization | Hash sensitive features | No (for training) |

### 6.2 Pseudonymized Training Pipeline

```
Raw Data → PII Detection → Pseudonymization → Feature Engineering → Model Training
                              ↓                      ↓
                      ┌───────┼───────┐         Use pseudonymous
                      ↓       ↓       ↓         IDs throughout
                  Hash    Generalize  Tokenize
                  (irrev) (location) (format)
```

### 6.3 Model Privacy Considerations

- **Membership inference**: Can an attacker determine if a user's data was in training?
- **Attribute inference**: Can an attacker predict sensitive attributes?
- **Model inversion**: Can an attacker reconstruct training data from model?
- **Mitigations**: Differential privacy, federated learning, data minimization

---

## 7. Re-Identification Risk Assessment

### 7.1 Risk Assessment Framework

```
Re-identification Risk = f(Quasi-Identifier Uniqueness, External Data Availability, Attack Sophistication)
```

### 7.2 Risk Factors

| Factor | Low Risk | Medium Risk | High Risk |
|---|---|---|---|
| Quasi-identifiers | Few, general | Some specific | Many specific |
| External data | Not available | Partially available | Widely available |
| Record uniqueness | Common patterns | Somewhat unique | Highly unique |
| Sensitive attributes | Low sensitivity | Moderate sensitivity | High sensitivity |
| Data volume | Very large (1M+) | Medium (10K-1M) | Small (<10K) |

### 7.3 Risk Mitigation Strategies

| Risk Level | Mitigation |
|---|---|
| Low | Standard pseudonymization sufficient |
| Medium | Combine with k-anonymity (k≥5) and l-diversity |
| High | Apply differential privacy (ε ≤ 1.0) or full anonymization |
| Very high | Do not release data; use secure computation |

### 7.4 Re-Identification Testing

| Test | Method | Frequency |
|---|---|---|
| Unique record detection | Count unique quasi-identifier combinations | Per dataset creation |
| Linkage attack simulation | Attempt to link with external datasets | Quarterly |
| Attribute inference test | Attempt to infer sensitive attributes | Quarterly |
| Formal privacy audit | Differential privacy guarantees verification | Annually |
