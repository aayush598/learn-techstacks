# Code Review Process

## Overview

Code review is a systematic examination of code changes before they are merged into the main branch. For recommendation systems, code review is especially critical because changes can affect user experience for millions of users, introduce biases, or degrade model performance. Effective code review catches bugs, ensures quality, shares knowledge, and maintains consistency across the team.

## Review Checklist for ML Code

### Data Handling

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Data leakage** | No future data used in training features | Inflated offline metrics, poor online performance |
| **Train/eval split integrity** | No overlap between train and test sets | Overoptimistic evaluation results |
| **Feature computation correctness** | Features computed identically in training and serving | Train-serve skew |
| **Null handling** | Missing values handled consistently | Silent model failures |
| **Data bias awareness** | Training data biases documented | Unfair recommendations |
| **PII handling** | Personal information properly anonymized | Privacy violations |

### Model Design

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Architecture appropriateness** | Model fits the problem scale and constraints | Wasted resources or underperformance |
| **Loss function correctness** | Loss function matches the optimization objective | Model learns wrong thing |
| **Gradient flow** | No vanishing/exploding gradients in deep models | Training instability |
| **Regularization** | Appropriate regularization to prevent overfitting | Poor generalization |
| **Scalability** | Model can handle production traffic volumes | Serving failures |
| **Cold-start handling** | Model gracefully handles new users/items | Poor new user experience |

### Feature Engineering

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Feature schema** | Features match the defined schema | Runtime errors |
| **Feature freshness** | Temporal features use correct time windows | Stale predictions |
| **Feature importance** | Feature contributions are reasonable | Model using proxy features |
| **Feature interactions** | Interaction features are correctly computed | Incorrect feature combinations |
| **Feature scaling** | Numerical features appropriately scaled | Training instability |

### Evaluation

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Metric implementation** | Metrics computed correctly | Wrong evaluation conclusions |
| **Test set validity** | Test set represents production distribution | Misleading offline results |
| **Baseline comparison** | Results compared against baselines | Overestimating model quality |
| **Statistical significance** | Results are statistically validated | Deploying a non-improvement |
| **Fairness metrics** | Fairness evaluated across relevant groups | Deploying biased model |
| **Ablation study** | Component contributions understood | Unnecessary complexity |

### Deployment

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Inference latency** | Model meets latency requirements (p99 < 100ms) | Slow page loads |
| **Memory usage** | Model fits within memory budget | OOM errors |
| **Resource requirements** | GPU/CPU/memory requirements documented | Capacity planning failures |
| **Rollback plan** | Can quickly revert to previous model | Prolonged outages |
| **Monitoring** | Metrics and alerts configured | Undetected degradation |
| **Feature store integration** | Features served correctly from feature store | Feature drift |

### Security

| Check | Description | Risk if Missed |
|-------|-------------|----------------|
| **Secrets management** | No hardcoded credentials | Security breach |
| **Input validation** | User inputs sanitized | Injection attacks |
| **Model poisoning defense** | Adversarial inputs handled | Model manipulation |
| **API authentication** | Endpoints properly authenticated | Unauthorized access |
| **Data access controls** | Training data access restricted | Data breach |

## Review Guidelines

### Scope and Size

| PR Size | Review Time | Review Depth |
|---------|-----------|-------------|
| < 100 lines | 15–30 minutes | Thorough review |
| 100–300 lines | 30–60 minutes | Standard review |
| 300–500 lines | 1–2 hours | May need decomposition |
| > 500 lines | 2+ hours | Should be split into smaller PRs |

**Rule of thumb**: If a PR takes more than 60 minutes to review, it's too large. Ask the author to split it.

### Feedback Style

| Approach | Example | When to Use |
|----------|---------|------------|
| **Suggest changes** | "Consider using X instead of Y because..." | Clear improvements |
| **Ask questions** | "What happens if the input is empty?" | Unclear design decisions |
| **Point out risks** | "This could cause issues if..." | Potential problems |
| **Acknowledge good work** | "Nice approach to handling the edge case" | Positive reinforcement |
| **Nitpick** | "Minor: consider renaming this variable" | Style issues (use sparingly) |

### Review Priorities

1. **Correctness**: Does the code do what it claims?
2. **Design**: Is the architecture appropriate?
3. **Safety**: Will this cause issues in production?
4. **Performance**: Are there efficiency concerns?
5. **Readability**: Is the code maintainable?
6. **Style**: Does it follow team conventions? (lowest priority)

## Review for Data Pipelines

### Data Pipeline Review Checklist

| Check | Description |
|-------|-------------|
| **Schema validation** | Output schema matches expected schema |
| **Data quality checks** | Null rates, value distributions, outlier detection |
| **Idempotency** | Pipeline can be safely re-run |
| **Backfill capability** | Pipeline can process historical data |
| **Monitoring** | Data freshness and quality alerts configured |
| **Downstream impact** | Changes don't break dependent models |

## Review for Model Changes

### Model Code Review Checklist

| Check | Description |
|-------|-------------|
| **Reproducibility** | Training produces same results with same seed |
| **Versioning** | Model version properly incremented |
| **Artifact storage** | Model saved to registry correctly |
| **Performance validation** | Offline metrics meet minimum thresholds |
| **Fairness validation** | No fairness regression on protected groups |
| **Serving compatibility** | Model compatible with serving infrastructure |
| **Inference correctness** | Predictions match expected format |

## Automated Review

### CI/CD Integration

| Tool | Purpose | Integration Point |
|------|---------|------------------|
| **Linting** | Code style enforcement | Pre-commit, CI |
| **Type checking** | Type safety validation | CI pipeline |
| **Unit tests** | Functional correctness | CI pipeline |
| **Integration tests** | End-to-end validation | CI pipeline |
| **Security scanning** | Vulnerability detection | CI pipeline |
| **Model tests** | Model behavior validation | CI pipeline |
| **Data validation** | Schema and quality checks | Data pipeline CI |

### Automated Checks Before Review

```
1. Linting (ruff, pylint) - must pass
2. Type checking (mypy) - must pass
3. Unit tests - must pass
4. Integration tests - must pass
5. Security scan (bandit) - must pass
6. Data validation - must pass (for data PRs)
7. Model performance check - must meet thresholds (for model PRs)
```

### ML-Specific Automated Checks

| Check | Tool | Threshold |
|-------|------|-----------|
| Feature schema validation | Great Expectations, Pandera | All columns present, correct types |
| Model performance | Custom evaluation script | NDCG@10 > baseline - 0.01 |
| Fairness metrics | Custom fairness check | Demographic parity < threshold |
| Inference latency | Load testing script | p99 < 100ms |
| Memory usage | Profiling script | < available memory |
| No data leakage | Custom check | No future features in training |

## Review Metrics

### Tracking Review Quality

| Metric | Formula | Target |
|--------|---------|--------|
| **Review turnaround time** | Time from PR creation to first review | < 4 hours |
| **Time to merge** | Time from PR creation to merge | < 24 hours |
| **Approval rate** | PRs approved on first review / total PRs | > 60% |
| **Revision rate** | PRs requiring changes / total PRs | < 40% |
| **Bug escape rate** | Bugs found in production / total reviews | < 5% |
| **Review coverage** | Lines reviewed / total lines changed | > 90% |

### Review Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|---------|
| Rubber-stamping | Approving without reading | Require specific comments |
| Nitpick overload | Too many style comments | Focus on substance |
| Gatekeeping | Blocking on minor issues | Separate style from substance |
| Solo review | Same person always reviews | Rotate reviewers |
| Review avoidance | PRs sit unreviewed | Set SLA for first review |
| Author defends everything | No receptiveness to feedback | Foster collaborative culture |

## Review for ML Projects: Special Considerations

### Research vs Engineering Review

| Aspect | Research Code | Production Code |
|--------|--------------|-----------------|
| **Priority** | Correctness, flexibility | Reliability, performance |
| **Review depth** | Methodology, math | Code quality, safety |
| **Documentation** | Experiment notes, results | API docs, runbooks |
| **Testing** | Evaluation correctness | Integration, load tests |
| **Style** | Flexible | Strict |

### Model Registry Review

When reviewing model changes, additionally verify:

1. **Model card** is updated (description, intended use, limitations)
2. **Version metadata** includes training data version, hyperparameters, and evaluation results
3. **Performance comparison** against the current production model
4. **Backward compatibility** with existing serving infrastructure
5. **Rollback procedure** is documented and tested
