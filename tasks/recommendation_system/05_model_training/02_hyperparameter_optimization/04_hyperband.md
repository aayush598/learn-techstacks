# Hyperband and ASHA: Early Stopping for Hyperparameter Optimization

## Overview

Hyperband and its asynchronous variant (ASHA - Asynchronous Successive Halving) are hyperparameter optimization algorithms that intelligently allocate resources by progressively eliminating poor-performing configurations. They combine the exploration of random search with the efficiency of early stopping, making them particularly effective for deep learning hyperparameter tuning where training cost is the dominant bottleneck.

---

## Successive Halving Foundation

### Core Idea

1. Start with many configurations trained on a small budget
2. Keep the top fraction, discard the rest
3. Double the budget for surviving configurations
4. Repeat until one configuration remains

### Algorithm Mechanics

- Start with N configurations, each trained for R minimum resources
- At each round, keep top 1/η fraction (η = elimination rate, typically 2 or 3)
- Multiply resource allocation by η each round
- Final configuration gets full budget R

**Example with η = 2, N = 8, R = 64 epochs**:
```
Round 1: 8 configs × 8 epochs    → keep 4
Round 2: 4 configs × 16 epochs   → keep 2
Round 3: 2 configs × 32 epochs   → keep 1
Round 4: 1 config  × 64 epochs   → winner
Total epochs: 64 + 64 + 64 + 64 = 256 (vs 512 for full training)
```

### Bias in Successive Halving

- Configurations evaluated at low budgets are biased: some get lucky with early performance
- A configuration that performs well at 8 epochs may not be the best at 64 epochs
- This bias is the fundamental trade-off: efficiency vs. accuracy of selection

---

## Hyperband Algorithm

### Addressing the Exploration-Exploitation Trade-off

Hyperband runs multiple successive halving brackets with different initial configurations and budget allocations:

| Bracket | Initial Configs (n) | Min Resources (r) | Elimination Rate |
|---------|--------------------|--------------------|------------------|
| 0 | 81 | 1 | 3 |
| 1 | 27 | 3 | 3 |
| 2 | 9 | 9 | 3 |
| 3 | 3 | 27 | 3 |
| 4 | 1 | 81 | 3 |

**Bracket 0**: Start with 81 configs at 1 epoch; aggressive elimination
**Bracket 4**: Start with 1 config at 81 epochs; no elimination (full budget)

### Resource Allocation

Hyperband distributes total budget across brackets using the formula:
```
s_max = floor(log_η(R/r_min))
total_brackets = s_max + 1
budget_per_bracket ≈ total_budget / (s_max + 1)
```

### Key Properties

- **Anytime property**: At any point during execution, Hyperband has results from complete brackets
- **No tuning required**: η = 3 and r_min are the only hyperparameters
- **Adaptive**: More aggressive early stopping when budget is tight
- **Robust**: Good performance across a wide range of problems

---

## ASHA (Asynchronous Successive Halving)

### Problem with Synchronous Hyperband

- Synchronous execution wastes resources: all configurations in a bracket must finish before promotion
- Stragglers delay entire bracket
- GPU utilization drops during synchronization barriers

### ASHA Solution

- **Asynchronous promotion**: Promote configurations as soon as they reach the required resource level
- **No brackets**: Run all configurations in parallel with dynamic resource allocation
- **Race condition free**: Each configuration has a unique promotion path

### ASHA Algorithm

1. Start all configurations at minimum resource budget
2. As configurations finish evaluation, check if they are in the top 1/η
3. If yes, immediately promote to next resource level (no waiting)
4. If no, terminate and start a new configuration
5. Continue until target resource budget is reached

### ASHA vs Synchronous Hyperband

| Property | Hyperband (Synchronous) | ASHA (Asynchronous) |
|----------|------------------------|---------------------|
| Resource utilization | Lower (sync barriers) | Higher (no barriers) |
| Implementation complexity | Simple | Moderate |
| Straggler tolerance | Low | High |
| Kubernetes fit | Better (batch scheduling) | Better (continuous scheduling) |
| Worst-case performance | Better theoretical guarantees | Slightly worse in theory |

---

## Resource Allocation Strategies

### Proportional Allocation

- Resources allocated proportionally to configuration rank
- Top-ranked configurations get exponentially more resources
- Provides strong exploration at low budgets while maintaining exploitation

### Aggressive Early Stopping

- Use η = 4 or η = 8 for very aggressive elimination
- Reduces total compute by 75-87%
- Risk: may eliminate configurations that improve slowly but ultimately outperform
- Best for: large-scale sweeps where many configurations can be tried

### Conservative Early Stopping

- Use η = 2 for gentle elimination
- Preserves more configurations for longer
- Risk: less compute savings
- Best for: problems where slow-starting configurations may be optimal

### Dynamic Budget Allocation

- Adjust minimum resource budget based on observed convergence speed
- If early epochs are highly predictive, use more aggressive early stopping
- If early performance is noisy, increase minimum budget
- Adaptive approach: start with small r_min, increase if too many false eliminations

---

## Integration with Optuna

### ASHA Pruner in Optuna

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    dropout = trial.suggest_float("dropout", 0.0, 0.5)
    n_layers = trial.suggest_int("n_layers", 1, 8)
    
    # Model training with epoch-level reporting
    for epoch in range(100):
        train_loss = train_one_epoch(model, lr, dropout, n_layers)
        val_metric = evaluate(model, val_data)
        
        # Report to Optuna for ASHA pruning
        trial.report(val_metric, epoch)
        
        if trial.should_prune():
            raise optuna.TrialPruned()
    
    return val_metric

study = optuna.create_study(
    pruner=optuna.pruners.HyperbandPruner(
        min_resource=1,
        max_resource=100,
        reduction_factor=3
    ),
    direction="maximize"
)
study.optimize(objective, n_trials=500)
```

### Optuna Configuration for ASHA

- `min_resource`: Minimum epochs/iterations before pruning
- `max_resource`: Maximum epochs/iterations for full training
- `reduction_factor`: Elimination rate (η); 3 is default
- `bootstrap_count`: Number of configs to keep at minimum resource (reduces early bias)
- `n_brackets`: Number of Hyperband brackets (0 = pure ASHA)

### Integration with MLflow

- Log each trial's epochs to MLflow for visualization
- Use Optuna's MLflow integration for automatic trial logging
- Compare pruned vs completed trials to assess pruning quality
- Track intermediate learning curves to validate pruning decisions

---

## When to Use Hyperband/ASHA

### Strong Use Cases

- **Deep learning hyperparameter tuning**: Training cost dominates; early epochs are informative
- **Large-scale sweeps**: 100+ configurations with limited GPU budget
- **Embedding model tuning**: Embedding dimensions and regularization often show early signals
- **Quick iteration**: Want to test many configurations in a few hours

### Moderate Use Cases

- **Transfer learning**: Fine-tuning where convergence is fast but parameter sensitivity varies
- **Architecture search**: When combined with weight sharing (NAS)
- **Multi-objective optimization**: Can be combined with Pareto ranking

### Not Ideal When

- **Early performance is not predictive**: Some models need many epochs to differentiate
- **Very small hyperparameter spaces**: Grid or random search may suffice
- **Sequential experiments needed**: Bayesian optimization may be more efficient
- **Single evaluation**: Cannot apply early stopping to a single run

---

## Practical Recommendations

### Choosing Parameters

- η = 3 is a good default for most recommendation model tuning
- Set r_min to roughly 10% of total epochs (enough for initial convergence signal)
- Use bootstrap_count = 1 or 3 to reduce early stopping bias
- Total budget: aim for 3-5x more configurations than grid search would evaluate

### Common Pitfalls

- **Too aggressive pruning**: η = 8 may eliminate slow-improving configurations
- **Too small r_min**: Early epochs may not correlate with final performance
- **Ignoring learning rate schedule**: Pruning at epoch 5 may not reflect warmup behavior
- **Not validating with full training**: Always retrain top configurations with full budget

### Monitoring

- Track fraction of configurations pruned at each level
- Compare early-stopped vs. full-budget performance for surviving configurations
- Monitor false positive rate: how often pruned configs would have been better
- Use visualization to assess bracket completion and resource utilization
