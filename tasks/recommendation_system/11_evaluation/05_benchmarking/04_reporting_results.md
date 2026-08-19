# Reporting Results

## Overview

Reporting results effectively is as important as the evaluation itself. A well-reported evaluation enables stakeholders to understand what was tested, what was found, and what decisions should follow. Poor reporting—missing context, cherry-picked metrics, or hidden limitations—leads to misinformed decisions and erodes trust in the evaluation process.

## Result Tables

### Essential Components

A result table should include:
- Method names (clear, consistent)
- All relevant metrics (not just the best ones)
- Confidence intervals or standard errors
- Statistical significance markers
- Sample size information

### Standard Table Format

```
Method          | NDCG@10       | Precision@10   | Recall@100     | Coverage@100
                | (95% CI)      | (95% CI)       | (95% CI)       | (95% CI)
----------------|---------------|----------------|----------------|---------------
Random          | 0.021±0.002   | 0.008±0.001    | 0.052±0.005    | 0.950±0.003
Popularity      | 0.064±0.003*  | 0.032±0.002*   | 0.118±0.008*   | 0.020±0.001*
Item-KNN        | 0.098±0.004*  | 0.051±0.003*   | 0.143±0.010*   | 0.350±0.008*
ALS (k=100)     | 0.112±0.004*  | 0.058±0.003*   | 0.156±0.011*   | 0.420±0.009*
Our Model       | 0.128±0.004†  | 0.067±0.003†   | 0.171±0.011†   | 0.480±0.010†

* p < 0.05 vs Random, † p < 0.05 vs ALS (Holm-corrected)
n = 10,000 users, test set interactions = 245,000
```

### Table Best Practices

| Do | Don't |
|----|-------|
| Report ALL pre-specified metrics | Cherry-pick only favorable metrics |
| Include confidence intervals | Report point estimates only |
| Mark statistical significance clearly | Claim significance without testing |
| Report sample sizes | Hide insufficient data |
| Use consistent decimal places | Mix precision levels |
| Bold the best result per column | Bold all your model's results |

## Confidence Intervals

### Why Confidence Intervals Matter

Confidence intervals convey the uncertainty in your estimates. A narrow CI indicates precise estimation; a wide CI indicates high uncertainty.

### CI Reporting Format

| Format | Example | When to Use |
|--------|---------|------------|
| **± notation** | 0.128 ± 0.004 | Simple, compact |
| **Bracket notation** | [0.120, 0.136] | Formal reporting |
| **Full sentence** | "NDCG@10 = 0.128 (95% CI: 0.120–0.136)" | Narrative text |

### CI Interpretation

- A 95% CI means that if we repeated the experiment many times, 95% of the CIs would contain the true parameter
- Two CIs that overlap do NOT necessarily mean the difference is not significant
- Two CIs that do not overlap DO necessarily mean the difference is significant
- Use hypothesis tests for direct comparison, CIs for estimation

### CI Width Guidelines

| CI Width | Interpretation | Action |
|----------|---------------|--------|
| Narrow (< 5% of mean) | Precise estimate | Results are reliable |
| Medium (5–15% of mean) | Moderate uncertainty | Interpret with caution |
| Wide (> 15% of mean) | High uncertainty | Collect more data or reduce variance |

## Visualization Best Practices

### Recommended Chart Types

| Comparison | Chart Type | Key Features |
|-----------|-----------|-------------|
| Model vs. baseline | Grouped bar chart with error bars | Show CIs clearly |
| Metric across K | Line chart with CI bands | Plot NDCG@1, NDCG@5, NDCG@10 |
| Metric over time | Line chart with trend | Show seasonal patterns |
| User segment analysis | Heatmap | Rows = segments, columns = metrics |
| Ablation study | Stacked bar or waterfall | Show cumulative contribution |
| Tradeoff (accuracy vs fairness) | Scatter plot | Pareto frontier highlighted |

### Visualization Principles

1. **Always include error bars or CI bands**: Never show point estimates alone
2. **Use consistent scales**: Same axis ranges across related plots
3. **Label clearly**: Axis labels, units, legend, title
4. **Avoid chart junk**: Minimal gridlines, no 3D effects, no unnecessary decoration
5. **Color-accessible**: Use colorblind-friendly palettes (viridis, ColorBrewer)
6. **Show the data**: Distributions > summaries (box plots > bar charts for distributions)

### Common Visualization Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Truncated y-axis | Exaggerates small differences | Start y-axis at 0 or use zoom insets |
| No error bars | Hides uncertainty | Add 95% CIs |
| Too many lines | Hard to read | Focus on key comparisons |
| 3D effects | Distorts perception | Use 2D charts |
| Inconsistent scales | Misleading comparisons | Use same axes across plots |

## Ablation Studies

### Purpose

Ablation studies systematically remove components from a model to understand each component's contribution.

### Ablation Table Format

| Variant | NDCG@10 | Δ from Full | Component Tested |
|---------|---------|------------|-----------------|
| Full model | 0.128 | — | All components |
| - User embedding | 0.115 | -0.013 | User representation |
| - Item embedding | 0.118 | -0.010 | Item representation |
| - Attention mechanism | 0.121 | -0.007 | Cross-feature interaction |
| - Temporal features | 0.124 | -0.004 | Time-awareness |
| - Popularity features | 0.125 | -0.003 | Trend awareness |

### Ablation Best Practices

1. **Test one component at a time**: Isolate each component's contribution
2. **Report confidence intervals**: Ablation differences may not be significant
3. **Test combinations**: Some components may be redundant together
4. **Ablate to simple baselines**: Don't just ablate to a slightly worse model
5. **Report negative results**: If a component doesn't help, say so

## Error Analysis

### Error Taxonomy

Categorize recommendation errors to understand model weaknesses:

| Error Type | Description | Example | Mitigation |
|-----------|-------------|---------|-----------|
| **Popularity bias** | Over-recommending popular items | Same top-10 for all users | Diversity constraints |
| **Cold-start failure** | Poor recommendations for new users | Random-quality recs for new users | Content-based cold-start |
| **Stale recommendations** | Recommending outdated items | Old news, discontinued products | Temporal features |
| **Irrelevant recommendations** | Completely off-target items | Recommending diapers to a teen | Better feature engineering |
| **Redundant recommendations** | Similar items repeated | 5 nearly identical products | Diversity re-ranking |
| **Fairness violation** | Systematic bias across groups | Gender-skewed job recommendations | Fairness constraints |

### Error Analysis Process

```
1. Identify error clusters (automated or manual)
2. Sample errors from each cluster (100–500 per type)
3. Manually analyze root causes
4. Quantify the frequency and impact of each error type
5. Prioritize fixes by impact × frequency
6. Report findings with examples
```

### Error Impact Assessment

| Error Type | Frequency | User Impact | Revenue Impact | Priority |
|-----------|----------|------------|---------------|----------|
| Irrelevant recs | 8% of impressions | High (user frustration) | High (lost clicks) | P0 |
| Stale recs | 3% of impressions | Medium | Medium | P1 |
| Redundant recs | 5% of impressions | Medium (boring) | Low | P2 |
| Popularity bias | 15% of impressions | Low (but widespread) | Medium | P2 |
| Fairness violation | 2% of impressions | High (for affected groups) | Variable | P1 |

## Limitations Section

### Essential Limitations to Report

| Category | Example Limitation |
|----------|-------------------|
| **Data** | "Training data is from a 6-month period; seasonal effects may not be captured" |
| **Evaluation** | "Offline metrics may not correlate perfectly with online performance" |
| **Scope** | "Results are specific to the movie domain; generalizability untested" |
| **Methodology** | "Binary relevance labels may not capture nuanced preferences" |
| **Computational** | "Model requires 4× more inference time than baseline" |
| **Ethical** | "Potential for filter bubbles due to strong personalization" |

### Limitations Writing Template

```
This evaluation has several limitations:

1. **Data limitations**: [Describe data constraints]
2. **Evaluation limitations**: [Describe metric/methodology constraints]
3. **Scope limitations**: [Describe generalizability constraints]
4. **Practical limitations**: [Describe deployment constraints]
5. **Ethical considerations**: [Describe fairness/bias concerns]
```

## Reproducibility Checklist

### For Every Evaluation Report

| Item | Description | Check |
|------|-------------|-------|
| **Dataset description** | Size, source, time period, domain | ☐ |
| **Preprocessing** | How data was cleaned and split | ☐ |
| **Train/valid/test split** | Split sizes and methodology | ☐ |
| **Baseline implementations** | Versions, hyperparameters, libraries | ☐ |
| **Hyperparameter tuning** | Search space, method, budget | ☐ |
| **Evaluation metrics** | All metrics with K values | ☐ |
| **Statistical tests** | Tests used, correction method | ☐ |
| **Confidence intervals** | Method (bootstrap B value, etc.) | ☐ |
| **Random seeds** | Seeds used for reproducibility | ☐ |
| **Hardware/software** | GPU, library versions, Python version | ☐ |
| **Code availability** | Repository link or availability statement | ☐ |
| **Compute time** | Total training and evaluation time | ☐ |

## Paper/Report Templates

### Standard Structure for Evaluation Reports

```
1. Executive Summary
   - Key findings (2–3 bullet points)
   - Recommended action

2. Experimental Setup
   2.1 Dataset
   2.2 Baselines
   2.3 Metrics
   2.4 Statistical methodology

3. Results
   3.1 Main results (table + discussion)
   3.2 Ablation study
   3.3 Error analysis
   3.4 Segment-level analysis

4. Discussion
   4.1 Interpretation of results
   4.2 Limitations
   4.3 Implications for production

5. Conclusion & Recommendations
   - Go/no-go recommendation
   - Next steps
   - Risks

Appendix:
   - Full result tables
   - Additional visualizations
   - Reproducibility checklist
```

### Executive Summary Template

```
We evaluated [Model Name] against [N] baselines on [Dataset] using [M] metrics.

Key findings:
1. [Model] improved NDCG@10 by [X]% (p < 0.05, d = [effect size]) over [best baseline]
2. [Model] maintained comparable coverage/diversity to [baseline]
3. [Notable limitation or concern]

Recommendation: [Deploy / Further testing needed / Do not deploy]
```
