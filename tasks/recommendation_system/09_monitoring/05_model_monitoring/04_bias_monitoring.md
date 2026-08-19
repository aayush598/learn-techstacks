# Bias Monitoring for Recommendation Systems

## 1. Overview

Bias monitoring ensures that recommendation systems treat all user groups fairly and do not discriminate based on protected attributes. In production recommendation systems, bias can emerge from historical data, feedback loops, representation imbalance, and algorithmic amplification. Proactive bias monitoring is both an ethical imperative and a regulatory requirement.

### 1.1 Types of Bias in Recommendation Systems

| Bias Type | Description | Example |
|---|---|---|
| **Historical bias** | Training data reflects past discrimination | Jobs historically recommended more to men |
| **Representation bias** | Underrepresented groups in training data | Minority groups have fewer recommendations |
| **Popularity bias** | Popular items dominate, marginalizing niche content | Mainstream content crowds out diverse content |
| **Exposure bias** | Items shown more get more engagement | Feedback loop reinforces existing preferences |
| **Selection bias** | Observed data is biased by what was shown | Cannot learn preferences for unshown items |
| **Confirmation bias** | Model reinforces existing user beliefs | Filter bubble effect |

### 1.2 Why Bias Monitoring Matters

- **Legal compliance**: Regulations (EU AI Act, NYC Local Law 144) require bias auditing
- **User trust**: Fair recommendations build user trust and retention
- **Business value**: Diverse recommendations increase catalog utilization and discovery
- **Ethical responsibility**: Preventing discrimination is a fundamental requirement

---

## 2. Protected Attribute Tracking

### 2.1 Protected Attributes

| Category | Attributes | Tracking Method |
|---|---|---|
| Demographics | Age, gender, race, ethnicity | User profile (opt-in) |
| Geography | Country, region, urban/rural | IP-based or profile |
| Socioeconomic | Income level, education | Inferred or profile |
| Accessibility | Disability status, language | Profile or preference |
| Device/Platform | Mobile vs. desktop, OS | Request metadata |

### 2.2 Tracking Implementation

```promql
# Recommendation distribution by protected attribute
rec_recommendation_distribution{attribute="gender", value="male"} gauge
rec_recommendation_distribution{attribute="gender", value="female"} gauge
rec_recommendation_distribution{attribute="gender", value="unknown"} gauge

# Exposure distribution by protected attribute
rec_exposure_distribution{attribute="age_group", value="18-24"} gauge
rec_exposure_distribution{attribute="age_group", value="25-34"} gauge
rec_exposure_distribution{attribute="age_group", value="35-44"} gauge
rec_exposure_distribution{attribute="age_group", value="45+"} gauge
```

### 2.3 Privacy Considerations

- **Aggregation only**: Never track individual user attributes in logs
- **Differential privacy**: Add noise to aggregate statistics
- **Minimum group size**: Suppress statistics for groups with fewer than 100 users
- **Opt-in only**: Use demographic data only when users voluntarily provide it
- **Data minimization**: Collect only the minimum attributes needed for fairness analysis

---

## 3. Fairness Metrics

### 3.1 Demographic Parity

Definition: The probability of receiving a positive recommendation should be equal across groups.

```
P(recommended | group A) = P(recommended | group B)

For recommendation systems:
  Recommendation rate for group A ≈ Recommendation rate for group B

Disparity ratio:
  DR = min(rate_group) / max(rate_group)

  DR > 0.8: Acceptable disparity
  0.6 < DR <= 0.8: Moderate disparity, investigate
  DR <= 0.6: Severe disparity, take action
```

### 3.2 Equalized Odds

Definition: The true positive rate and false positive rate should be equal across groups.

```
For recommendation systems:
  TPR (precision) for group A ≈ TPR for group B
  FPR for group A ≈ FPR for group B

Where:
  TPR = relevant recommendations / total recommendations
  FPR = irrelevant recommendations / total irrelevant items
```

### 3.3 Calibration Across Groups

Definition: Predicted scores should have the same meaning across groups.

```
If model predicts 80% relevance for both groups:
  - Actual relevance for group A should be ≈ 80%
  - Actual relevance for group B should be ≈ 80%

Calibration gap:
  CG = |calibration_group_A - calibration_group_B|

  CG < 0.05: Well calibrated across groups
  0.05 <= CG < 0.10: Moderate calibration gap
  CG >= 0.10: Significant calibration gap
```

### 3.4 Exposure Fairness

Definition: All content providers (or content categories) should receive fair exposure.

```
Exposure ratio = actual_exposure / expected_exposure

Where expected_exposure is proportional to:
  - Content quality (relevance)
  - Content volume (supply)
  - User demand (interest)

Exposure ratio < 0.5: Underexposed (content provider disadvantaged)
Exposure ratio > 2.0: Overexposed (content provider advantaged)
```

### 3.5 Fairness Metrics Summary

| Metric | What It Measures | Target | Alert Threshold |
|---|---|---|---|
| Demographic parity | Equal recommendation rates | DR > 0.8 | DR < 0.7 |
| Equalized odds | Equal precision/recall across groups | Gap < 0.05 | Gap > 0.10 |
| Calibration gap | Consistent score meaning | Gap < 0.05 | Gap > 0.10 |
| Exposure ratio | Fair content exposure | 0.5-2.0 | <0.3 or >3.0 |
| Representation gap | Training data balance | Gap < 0.2 | Gap > 0.3 |
| Long-tail exposure | Niche content discoverability | >20% | <10% |

---

## 4. Bias Drift Detection

### 4.1 Monitoring Pipeline

```
Recommendations -> Fairness Calculator -> Bias Detector -> Alert System
      |                    |                    |                |
  User requests      Per-group stats      Trend analysis    Alerts
  with protected     (aggregated,         (drift detection) (demographic,
  attributes         anonymized)                             equalized odds)
```

### 4.2 Drift Detection Methods

**Statistical tests for bias drift:**

```
For each fairness metric:
  1. Calculate baseline distribution (from model training or historical)
  2. Calculate current distribution (rolling window)
  3. Apply statistical test:
     - Chi-squared test for categorical outcomes
     - Z-test for proportion differences
     - KS test for distribution shifts
  4. Alert if p-value < 0.05 AND effect size > threshold
```

**Temporal monitoring:**

```
Monitor fairness metrics over time:
  - Daily demographic parity scores
  - Weekly equalized odds trends
  - Monthly exposure ratio changes
  - Quarterly calibration gap analysis
```

### 4.3 Bias Drift Alerts

```yaml
bias_alerts:
  - name: "Demographic parity violation"
    condition: "rec_fairness_demographic_parity < 0.7 for 7d"
    severity: warning
    action: "Investigate recommendation distribution by group"

  - name: "Severe demographic parity violation"
    condition: "rec_fairness_demographic_parity < 0.5 for 3d"
    severity: critical
    action: "Emergency review, consider model rollback"

  - name: "Equalized odds gap increasing"
    condition: "rec_fairness_equalized_odds_gap > 0.15 for 7d"
    severity: warning
    action: "Analyze precision/recall by group"

  - name: "Content provider exposure imbalance"
    condition: "rec_fairness_exposure_ratio > 3.0 OR < 0.3 for 14d"
    severity: warning
    action: "Review content exposure distribution"
```

---

## 5. Fairness Dashboards

### 5.1 Dashboard Design

**Executive Fairness Dashboard:**
- Overall fairness score (composite of multiple metrics)
- Trend of fairness metrics over time
- Comparison across protected attributes
- Regulatory compliance status

**Operational Fairness Dashboard:**
- Per-group recommendation rates
- Per-group click-through rates
- Per-group conversion rates
- Exposure distribution by content provider

**Debugging Fairness Dashboard:**
- Feature importance by group
- Prediction distribution by group
- Model confidence by group
- Error analysis by group

### 5.2 Key Visualizations

**Fairness trend chart:**
```
Metric: Demographic Parity Ratio
Target: > 0.8
Timeline: Last 30 days

1.0 |                    - - - - - - - - - - - - - -
0.9 |              - -
0.8 | ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ TARGET ─ ─ ─ ─ ─ ─
0.7 |        -
0.6 | -
0.5 |
    └─────────────────────────────────────────────
    Week 1   Week 2   Week 3   Week 4
```

**Group comparison bar chart:**
```
Recommendation Rate by Gender:
  Male:     ████████████████████ 45%
  Female:   ██████████████████ 42%
  Unknown:  ████████████████ 38%
  Target: All groups within 10% of each other
```

---

## 6. Regulatory Compliance Monitoring

### 6.1 Regulatory Requirements

| Regulation | Requirement | Monitoring Need |
|---|---|---|
| EU AI Act | High-risk AI systems must be bias-tested | Regular fairness audits |
| NYC Local Law 144 | Annual bias audits for automated employment decisions | Annual fairness reports |
| GDPR | Right to non-discrimination | Per-group monitoring |
| CCPA | No discrimination in automated decisions | Per-group monitoring |
| EEOC | No employment discrimination | Protected attribute tracking |

### 6.2 Compliance Audit Process

```
Quarterly bias audit:
1. Collect recommendation data for all protected groups
2. Calculate fairness metrics (demographic parity, equalized odds, calibration)
3. Compare against regulatory thresholds
4. Document findings in compliance report
5. Identify any disparities requiring remediation
6. Submit report to compliance team
7. Track remediation actions to completion
```

### 6.3 Audit Trail

Maintain an audit trail for every bias check:

```json
{
  "audit_id": "bias-audit-2026-Q3",
  "timestamp": "2026-08-19T00:00:00Z",
  "model": "ranking-v3",
  "model_version": "2026.08.15-rc3",
  "protected_attributes": ["gender", "age_group", "region"],
  "metrics": {
    "demographic_parity": {"gender": 0.87, "age_group": 0.82, "region": 0.91},
    "equalized_odds_gap": {"gender": 0.03, "age_group": 0.07, "region": 0.04},
    "calibration_gap": {"gender": 0.02, "age_group": 0.05, "region": 0.03}
  },
  "compliance_status": "PASS",
  "reviewer": "ml-fairness-team",
  "next_audit_date": "2026-11-19"
}
```

---

## 7. Bias Mitigation Strategies

### 7.1 Pre-Processing Mitigation

| Strategy | Description | When to Use |
|---|---|---|
| Data balancing | Oversample underrepresented groups | Training data imbalance |
| Feature removal | Remove protected attributes from features | Legal requirement |
| Data augmentation | Generate synthetic data for underrepresented groups | Insufficient data |
| Reweighting | Assign higher weights to underrepresented groups | Moderate imbalance |

### 7.2 In-Processing Mitigation

| Strategy | Description | When to Use |
|---|---|---|
| Fairness constraints | Add fairness constraints to model objective | Known bias pattern |
| Adversarial debiasing | Train adversary to remove bias from embeddings | Embedding-based models |
| Calibrated equalized odds | Post-process to equalize odds | Post-deployment fix |
| Regularization | Add fairness regularization term | Prevent bias amplification |

### 7.3 Post-Processing Mitigation

| Strategy | Description | When to Use |
|---|---|---|
| Score adjustment | Adjust prediction scores for different groups | Quick fix |
| Threshold optimization | Different decision thresholds per group | Classification-based |
| Exposure capping | Limit exposure of overrepresented items | Content diversity |
| Re-ranking | Apply fairness-aware re-ranking | Real-time adjustment |

---

## 8. Key Takeaways

1. **Monitor fairness metrics continuously** — bias can emerge gradually
2. **Track protected attributes** with privacy-preserving methods (aggregation, differential privacy)
3. **Use multiple fairness metrics** — no single metric captures all aspects of fairness
4. **Set fairness SLOs** — treat fairness as seriously as performance SLOs
5. **Implement bias drift detection** — statistical tests detect emerging bias early
6. **Maintain fairness dashboards** — visibility enables accountability
7. **Conduct regular bias audits** — required for regulatory compliance
8. **Document bias decisions** — maintain audit trail for compliance and accountability
9. **Implement mitigation strategies** — pre-processing, in-processing, and post-processing
10. **Involve diverse stakeholders** — bias detection requires diverse perspectives
