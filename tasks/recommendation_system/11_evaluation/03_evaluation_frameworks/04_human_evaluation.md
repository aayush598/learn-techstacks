# Human Evaluation

## Overview

Human evaluation uses trained or untrained people to assess recommendation quality in ways that automated metrics cannot. It captures nuanced judgments about relevance, diversity, serendipity, and user experience that require human understanding. Human evaluation is essential for validating offline metrics, calibrating automated systems, and ensuring recommendations align with human values and expectations.

## Expert Evaluation

### What Expert Evaluators Do

Expert evaluators are domain specialists who assess recommendation quality using deep knowledge of the domain, user needs, and content characteristics.

### Expert Evaluation Tasks

| Task | Description | Output |
|------|-------------|--------|
| **Relevance assessment** | Judge how relevant each recommended item is to a given user profile | 4–5 point relevance scale |
| **Diversity assessment** | Evaluate whether a recommendation list provides sufficient variety | Diversity score + qualitative feedback |
| **Serendipity assessment** | Identify unexpectedly good recommendations | Serendipity rating per item |
| **Fairness audit** | Check for bias across demographic groups | Bias report |
| **Error analysis** | Identify and categorize recommendation failures | Error taxonomy |

### Expert vs Non-Expert Evaluators

| Aspect | Expert Evaluators | Non-Expert Evaluators |
|--------|------------------|----------------------|
| **Domain knowledge** | Deep | Variable |
| **Consistency** | High | Lower |
| **Cost** | High ($50–150/hour) | Low ($10–30/hour) |
| **Scalability** | Limited (small panels) | High (crowdsourcing) |
| **Bias** | May over-index on domain specifics | May miss domain nuances |
| **Best for** | Domain-specific quality, edge cases | Broad user perspective, scale |

### Expert Panel Design

1. **Panel size**: 3–7 experts for qualitative assessment; 10–20 for quantitative measurement
2. **Selection criteria**: Domain expertise, understanding of user needs, attention to detail
3. **Training**: 2–4 hour orientation on evaluation guidelines, scales, and examples
4. **Calibration**: Joint evaluation of 20–50 items to ensure agreement before independent work

## Crowd-Sourced Evaluation

### Platform Options

| Platform | Cost Range | Quality Control | Best For |
|----------|-----------|----------------|----------|
| **Amazon Mechanical Turk** | $0.10–$1.00/task | Qualifications, attention checks | Large-scale relevance judgments |
| **Prolific** | $0.50–$2.00/task | Built-in quality controls | Research-grade evaluations |
| **Upwork** | $15–50/hour | Manual vetting | Specialized evaluation tasks |
| **Internal crowd** | Employee time | Highest quality, limited scale | High-stakes evaluations |

### Quality Control Mechanisms

| Mechanism | Description | Implementation |
|-----------|-------------|---------------|
| **Attention checks** | Include obvious questions to filter inattentive workers | "Select 'Strongly Agree' for this question" |
| **Gold standard items** | Include pre-labeled items to measure worker accuracy | Workers must score ≥80% on gold items |
| **Inter-annotator agreement** | Require agreement with other workers on overlapping items | Cohen's κ > 0.6 required |
| **Time filters** | Exclude workers who complete tasks too quickly | Remove responses < 50% of median time |
| **Reputation thresholds** | Only accept workers with high approval ratings | ≥95% approval, ≥1000 HITs completed |

### Crowd-Sourced Evaluation Protocol

```
1. Define evaluation task and guidelines (1–2 days)
2. Create test items with gold standard labels (1 day)
3. Pilot with 5–10 workers, refine guidelines (1–2 days)
4. Deploy to main worker pool (2–5 days)
5. Quality control: filter low-quality workers (1 day)
6. Aggregate judgments: majority vote or weighted average (1 day)
7. Analyze results and report (1–2 days)
```

## Evaluation Guidelines

### Creating Evaluation Guidelines

Evaluation guidelines ensure consistency and reproducibility across evaluators.

#### Guideline Document Structure

| Section | Content |
|---------|---------|
| **Task overview** | What the evaluator is assessing and why |
| **Scale definitions** | Clear definitions for each rating level with examples |
| **Anchoring examples** | Pre-rated examples for each scale level (5–10 per level) |
| **Edge cases** | How to handle ambiguous situations |
| **Context information** | What user profile/context information is provided |
| **Do's and don'ts** | Common mistakes and how to avoid them |

### Example Scale Definition (Relevance)

```
4 (Highly Relevant): The item directly matches the user's demonstrated interest.
    Example: User watches sci-fi movies → recommending "Interstellar"
    
3 (Relevant): The item is related to the user's interests but not a perfect match.
    Example: User watches sci-fi → recommending "The Martian" (sci-fi adjacent)
    
2 (Slightly Relevant): The item has some connection to the user's interests.
    Example: User watches sci-fi → recommending "Gravity" (space, but more drama)
    
1 (Not Relevant): The item has no meaningful connection to the user's interests.
    Example: User watches sci-fi → recommending "The Notebook" (romance)
```

### Guideline Iteration

1. **Version 1**: Draft based on task requirements
2. **Pilot round 1**: 3–5 evaluators test on 20–50 items
3. **Calibration meeting**: Discuss disagreements, refine guidelines
4. **Pilot round 2**: Re-evaluate same items with updated guidelines
5. **Finalize**: Lock guidelines, begin formal evaluation

## Inter-Annotator Agreement

### Why Agreement Matters

Inter-annotator agreement (IAA) measures the consistency of judgments across evaluators. High IAA indicates that the evaluation task is well-defined and the guidelines are clear. Low IAA suggests ambiguity in the task, the scale, or the guidelines.

### Cohen's Kappa (Two Annotators)

```
κ = (P_o - P_e) / (1 - P_e)
```

Where:
- P_o = Observed agreement (proportion of items where annotators agree)
- P_e = Expected agreement by chance

| κ Value | Interpretation |
|---------|---------------|
| 0.81–1.00 | Almost perfect agreement |
| 0.61–0.80 | Substantial agreement |
| 0.41–0.60 | Moderate agreement |
| 0.21–0.40 | Fair agreement |
| 0.00–0.20 | Slight agreement |
| < 0.00 | Less than chance |

### Fleiss' Kappa (Multiple Annotators)

Extension of Cohen's κ for more than two annotators:

```
κ = (P̄ - P̄_e) / (1 - P̄_e)
```

Where P̄ is the average observed agreement and P̄_e is the expected agreement by chance.

### Krippendorff's Alpha

A more general agreement measure that handles:
- Any number of annotators
- Missing data (not all annotators rate all items)
- Different scale types (nominal, ordinal, interval, ratio)

```
α = 1 - D_o / D_e
```

Where D_o is the observed disagreement and D_e is the expected disagreement.

| α Value | Interpretation |
|---------|---------------|
| > 0.80 | Reliable for firm conclusions |
| 0.67–0.80 | Tentative conclusions acceptable |
| < 0.67 | Unreliable; improve guidelines |

### Agreement by Scale Type

| Scale Type | Appropriate Agreement Measure | Notes |
|-----------|------------------------------|-------|
| Binary | Cohen's κ, Fleiss' κ | Simplest case |
| Ordinal | Weighted κ, Krippendorff's α (ordinal) | Accounts for near-misses |
| Interval | Krippendorff's α (interval) | Assumes equal spacing |
| Ratio | Krippendorff's α (ratio) | Handles bounded scales |

### Improving Agreement

1. **Clarify guidelines**: Ambiguous guidelines are the #1 cause of low agreement
2. **Add examples**: More anchoring examples reduce ambiguity
3. **Simplify the scale**: Fewer categories → higher agreement
4. **Train evaluators**: Calibration sessions improve consistency
5. **Reduce cognitive load**: Shorter evaluation sessions reduce fatigue
6. **Split complex judgments**: Separate relevance and quality into different tasks

## Evaluation Cost

### Cost Components

| Component | Typical Cost | Scaling Factor |
|-----------|-------------|---------------|
| **Guideline development** | $2,000–5,000 (one-time) | Fixed |
| **Pilot testing** | $500–1,000 | Fixed |
| **Expert evaluation** | $50–150/hour per expert | Linear with items |
| **Crowd-sourced evaluation** | $0.10–1.00 per item per annotator | Linear with items × annotators |
| **Quality control** | $500–1,000 per round | Fixed + marginal |
| **Analysis and reporting** | $1,000–3,000 per round | Fixed |

### Cost Optimization Strategies

| Strategy | Savings | Tradeoff |
|----------|---------|----------|
| **Active learning for item selection** | Evaluate 20–30% of items | May miss edge cases |
| **Adjudication only disagreements** | 30–50% fewer judgments | Requires initial dual annotation |
| **Reduced item sampling** | Variable savings | Statistical power reduction |
| **Tiered evaluation** | 40–60% savings | Different quality levels for different tiers |

### Cost-Effective Evaluation Pipeline

```
Tier 1: Crowd-sourced workers evaluate a large sample (1000+ items)
Tier 2: Experts evaluate a small sample (100–200 items) for calibration
Tier 3: Expert panel evaluates disagreements and edge cases (50–100 items)
Tier 4: Automated metrics calibrated against human judgments
```

## When to Use Human Evaluation

### Use Human Evaluation When:

1. **Developing a new recommendation algorithm**: Validate that automated metrics correlate with human judgments
2. **Evaluating subjective quality**: Serendipity, diversity, and novelty are inherently subjective
3. **Launching in a new domain**: Domain-specific relevance requires human assessment
4. **Conducting fairness audits**: Bias detection requires human judgment across demographic groups
5. **Debugging model failures**: Understanding why the model fails on specific cases
6. **Regulatory compliance**: Some regulations require human review of algorithmic decisions

### When Automated Metrics Are Sufficient:

1. **Iterating on a well-understood problem**: When automated metrics are validated against human judgment
2. **Large-scale continuous monitoring**: Human evaluation is too slow for daily monitoring
3. **Simple ranking comparison**: When differences are large enough for automated metrics to detect

### Human Evaluation Schedule

| Phase | Frequency | Scope |
|-------|----------|-------|
| Model development | Per experiment cycle | Validate against automated metrics |
| Pre-deployment | Before every major release | Full evaluation (500+ items) |
| Post-deployment | Weekly for first month | Spot-check (50–100 items) |
| Ongoing | Monthly | Random sampling (100–200 items) |
| Special | As needed | Edge cases, new domains, fairness audits |
