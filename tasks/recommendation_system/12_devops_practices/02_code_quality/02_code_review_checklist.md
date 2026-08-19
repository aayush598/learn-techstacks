# ML Code Review Checklist

## Overview

This checklist is a comprehensive guide for reviewing machine learning code in recommendation systems. Unlike traditional software code reviews, ML code reviews must verify correctness across data handling, model design, feature engineering, evaluation methodology, deployment safety, and security. Each category addresses unique risks that can silently corrupt model quality or cause production failures.

## Data Handling

### Data Leakage

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **No future information in features** | Features computed using information not available at prediction time | Trace feature computation; verify temporal ordering |
| **No target leakage** | Target variable doesn't leak into features through transformations | Check feature-target correlations |
| **No train-test contamination** | Test set not used for any training decisions (including hyperparameter tuning) | Verify split is performed before any processing |
| **No identity leakage** | User/item IDs not used as features in ways that cause memorization | Check embedding dimensions vs. unique IDs |
| **No cross-validation leakage** | CV folds respect temporal ordering | Verify time-series split, not random split |

### Data Quality

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Null handling** | Missing values handled explicitly, not silently dropped or imputed incorrectly | Check for NaN handling in feature pipelines |
| **Type correctness** | Feature types match expected types (numeric vs. categorical) | Schema validation |
| **Distribution sanity** | Feature distributions reasonable (no impossible values) | Summary statistics, histograms |
| **Duplicate detection** | No duplicate records in training data | Check for duplicate user-item pairs |
| **Temporal validity** | No data from the future in training set | Verify timestamp ordering |

### Bias Awareness

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Sampling bias** | Training data representative of production distribution | Compare distributions |
| **Label bias** | Labels not systematically biased (e.g., only showing popular items) | Analyze label distribution by popularity |
| **Demographic bias** | Protected attributes don't correlate with labels in biased ways | Fairness analysis |
| **Feedback loop** | Model doesn't create self-reinforcing biases | Monitor exposure diversity over time |

## Model Design

### Architecture Appropriateness

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Complexity justified** | Model complexity matches problem complexity | Overfitting or underfitting |
| **Latency budget** | Model inference time meets serving requirements | Slow recommendations |
| **Scalability** | Model can handle production traffic | Serving failures at scale |
| **Cold-start strategy** | Model handles new users/items gracefully | Poor new user experience |
| **Graceful degradation** | Model produces reasonable defaults when features are missing | Silent failures |

### Training Correctness

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Loss function** | Loss function aligns with optimization objective | Model learns wrong thing |
| **Optimizer choice** | Appropriate optimizer for the model type | Training instability |
| **Learning rate schedule** | LR schedule prevents divergence and enables convergence | Poor model quality |
| **Regularization** | Appropriate regularization to prevent overfitting | Poor generalization |
| **Batch size** | Batch size appropriate for model and data | Training instability |
| **Early stopping** | Training stops before overfitting | Degraded test performance |
| **Reproducibility** | Results reproducible with same random seed | Non-reproducible experiments |

### Model Versioning

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Version metadata** | Model version includes training data version, hyperparameters | Lost experiment context |
| **Model card** | Documentation of model capabilities and limitations | Misuse of model |
| **Artifact storage** | Model saved to registry correctly | Lost model artifacts |
| **Backward compatibility** | New model compatible with existing serving infrastructure | Deployment failures |

## Feature Engineering

### Feature Computation

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Correct computation** | Features computed as intended | Unit tests for feature functions |
| **Consistency** | Same features computed identically in training and serving | Compare train vs. serve computations |
| **Temporal correctness** | Time-window features use correct boundaries | Verify window calculations |
| **Aggregation correctness** | Aggregations (mean, count, sum) computed over correct groups | Test with known values |
| **Normalization** | Numerical features appropriately scaled/normalized | Check scaling parameters |
| **Encoding** | Categorical features correctly encoded | Verify encoding mappings |

### Feature Schema

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Schema compliance** | All features match defined schema | Schema validation (Pandera, Great Expectations) |
| **Feature names** | Consistent naming conventions | Linting rules |
| **Feature types** | Correct data types (int, float, string, array) | Type checking |
| **Feature ranges** | Values within expected bounds | Range validation |
| **Feature completeness** | No unexpected null rates | Null rate monitoring |

### Feature Store Integration

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Online/offline parity** | Features computed identically in batch and real-time | Compare batch vs. real-time values |
| **Feature freshness** | Features updated within acceptable latency | Monitor feature timestamps |
| **Feature lineage** | Feature dependencies tracked | Feature store metadata |

## Evaluation

### Methodology

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Proper train/eval split** | Temporal split for time-series data | Verify split methodology |
| **No data leakage in eval** | Evaluation data not used in any training decision | Audit evaluation pipeline |
| **Metric implementation** | Metrics computed correctly | Compare against reference implementation |
| **Baseline comparison** | Results compared against meaningful baselines | Verify baseline implementations |
| **Statistical significance** | Results validated with appropriate tests | Report p-values and confidence intervals |

### Evaluation Completeness

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Multiple metrics** | All relevant metrics reported (not just best one) | Check metric list |
| **Segment analysis** | Performance analyzed across user/item segments | Check segment breakdown |
| **Fairness metrics** | Fairness evaluated across protected groups | Check fairness dashboard |
| **Error analysis** | Common failure modes identified | Check error analysis report |
| **Offline-online correlation** | Offline metrics validated against online performance | Compare with A/B test results |

## Deployment

### Safety Checks

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Latency validation** | Inference latency within budget (p50, p95, p99) | Load testing |
| **Memory validation** | Model memory usage within budget | Memory profiling |
| **Rollback plan** | Ability to revert to previous model quickly | Document and test rollback |
| **Canary deployment** | New model deployed to small percentage first | Canary configuration |
| **Monitoring** | Metrics and alerts configured for new model | Alert configuration |

### Operational Readiness

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Health checks** | Model serving health endpoint configured | Test health endpoint |
| **Resource limits** | CPU, memory, GPU limits configured | Kubernetes resource specs |
| **Scaling rules** | Auto-scaling configured for traffic variations | Load test + verify scaling |
| **Logging** | Request/response logging enabled | Check logging configuration |
| **Error handling** | Graceful error handling for bad inputs | Test with malformed inputs |

## Security

### Secrets Management

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **No hardcoded secrets** | API keys, passwords not in code | Grep for secrets patterns |
| **Environment variables** | Secrets loaded from environment or secrets manager | Check config loading code |
| **Secret rotation** | Mechanism for rotating secrets without downtime | Secret rotation documentation |
| **Access logging** | Secret access logged for audit | Audit logging configuration |

### PII Handling

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Data anonymization** | PII properly anonymized in training data | Check data processing pipeline |
| **Access controls** | Training data access restricted to authorized personnel | IAM policy review |
| **Retention policy** | Data retention policies enforced | Check data lifecycle management |
| **GDPR/CCPA compliance** | Right to deletion supported | Verify deletion pipeline |

### Input Validation

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Input sanitization** | User inputs validated and sanitized | Input validation tests |
| **Rate limiting** | API endpoints rate-limited | Rate limit configuration |
| **Adversarial robustness** | Model handles adversarial inputs gracefully | Adversarial testing |
| **Model poisoning defense** | Training pipeline protected from data poisoning | Data validation in pipeline |

### Dependency Security

| Check | Description | How to Verify |
|-------|-------------|---------------|
| **Dependency scanning** | No known vulnerabilities in dependencies | Dependabot, safety |
| **Version pinning** | All dependencies pinned to specific versions | requirements.txt, poetry.lock |
| **Minimal dependencies** | Only necessary packages installed | Review dependency list |
| **Container security** | Docker image scanned for vulnerabilities | Trivy, Snyk scanning |
