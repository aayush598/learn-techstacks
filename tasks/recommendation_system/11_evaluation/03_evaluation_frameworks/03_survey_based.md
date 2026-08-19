# Survey-Based Evaluation

## Overview

Survey-based evaluation collects explicit human judgments about recommendation quality through structured questionnaires. Unlike behavioral metrics (clicks, purchases), surveys capture subjective satisfaction, perceived relevance, and user intent that cannot be inferred from implicit signals alone. Surveys are essential for understanding why users are satisfied or dissatisfied, not just whether they are.

## Relevance Judgments

### Definition

Relevance judgments are explicit assessments of how well a recommended item matches a user's needs, preferences, or intent at the time of recommendation.

### Relevance Scales

| Scale | Levels | Typical Labels |
|-------|--------|---------------|
| Binary | 2 | Relevant / Not Relevant |
| 3-point | 3 | Relevant / Partially Relevant / Not Relevant |
| 4-point | 4 | Highly Relevant / Relevant / Slightly Relevant / Not Relevant |
| 5-point | 5 | Perfect / Excellent / Good / Fair / Bad |
| Graded | 7+ | Continuous scale with anchoring examples |

### Best Practice: 4-Point or 5-Point Scales

Research shows 4-point and 5-point scales provide the best balance between:
- **Discrimination**: Enough levels to distinguish quality differences
- **Reliability**: Few enough levels that annotators agree consistently
- **Cognitive load**: Manageable for respondents

### Relevance Assessment Methods

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| **Retrospective relevance** | Users rate items they previously interacted with | Recall-based, context-aware | Memory decay, selection bias |
| **Prospective relevance** | Users rate items before interacting | No interaction bias | Hypothetical, may differ from actual |
| **Got It Right (GIR)** | Binary: "Did this recommendation get you right?" | Quick, intuitive | Low granularity |
| **Categorical relevance** | Multi-level: "How relevant is this?" | Rich signal | Slower, more cognitive load |

### Relevance Judgment Collection

1. **In-app micro-surveys**: Show a thumbs up/down after clicking a recommendation
2. **Post-session surveys**: Ask about the overall session quality after the user leaves
3. **Periodic surveys**: Send email/push surveys to a random sample of users
4. **Dedicated evaluation sessions**: Invite users for structured evaluation sessions

## User Satisfaction Surveys

### Standard Survey Instruments

#### Net Promoter Score (NPS)
```
"How likely are you to recommend [platform] to a friend?"
Scale: 0 (Not at all likely) to 10 (Extremely likely)
NPS = % Promoters (9–10) - % Detractors (0–6)
```

#### Customer Satisfaction Score (CSAT)
```
"How satisfied are you with today's recommendations?"
Scale: 1 (Very Dissatisfied) to 5 (Very Satisfied)
CSAT = (Number of 4–5 ratings) / (Total responses) × 100%
```

#### Customer Effort Score (CES)
```
"How easy was it to find what you were looking for?"
Scale: 1 (Very Difficult) to 7 (Very Easy)
```

### Recommendation-Specific Survey Questions

| Dimension | Sample Question | Scale |
|-----------|----------------|-------|
| **Relevance** | "How relevant were today's recommendations?" | 1–5 stars |
| **Diversity** | "Did you see a good variety of recommendations?" | 1–5 stars |
| **Novelty** | "Did you discover something new?" | Yes/No/Maybe |
| **Trust** | "Do you trust these recommendations?" | 1–5 Likert |
| **Control** | "Do you feel in control of your recommendations?" | 1–5 Likert |
| **Satisfaction** | "Overall, how satisfied are you with the recommendations?" | 1–5 stars |

### Survey Timing

| Timing | Pros | Cons |
|--------|------|------|
| **In-session (micro-survey)** | Low recall bias, contextual | Interrupts experience |
| **End of session** | Better overall assessment | Recall bias for early items |
| **Next-day push/email** | Less intrusive | Higher memory decay |
| **Weekly digest** | Comprehensive view | Low response rate, high recall bias |

## Comparative Evaluations (Side-by-Side)

### Design

Present two or more recommendation lists to users and ask them to compare:

```
"Which set of recommendations do you prefer?"
[List A] vs [List B]
```

### Comparison Formats

| Format | Description | Pros |
|--------|-------------|------|
| **Paired comparison** | Two lists side by side | Simple, interpretable |
| **Best-Worst scaling** | Pick best and worst from N lists | More efficient than pairwise |
| **Ranking** | Rank N lists from best to worst | Full ordering information |
| **Tournament** | Systematic pairwise comparisons | Comprehensive but time-consuming |

### Side-by-Side Analysis

#### Bradley-Terry Model
Model the probability that list A is preferred over list B:

```
P(A > B) = π_A / (π_A + π_B)
```

Where π_A and π_B are the "strength" parameters estimated from comparison data.

####win/tie/loss Analysis

| Outcome | Count | Percentage |
|---------|-------|-----------|
| List A wins | W_A | W_A / N |
| Tie | T | T / N |
| List B wins | W_B | W_B / N |

Use McNemar's test or binomial test to determine if the win rate is significantly different from 50%.

### Best Practices for Comparative Evaluation

1. **Randomize left-right position** to avoid position bias
2. **Counterbalance list presentation** (show both orders equally)
3. **Blind the evaluation** (don't label which algorithm produced which list)
4. **Collect confidence ratings** ("How confident are you in your preference?")
5. **Collect reasons** ("Why do you prefer this list?") for qualitative insight

## Likert Scales

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Odd number of points** | Allows neutral midpoint (5 or 7 points typical) |
| **Balanced anchors** | Equal positive and negative labels |
| **Clear labels** | Label every point, not just endpoints |
| **Avoid double-barreled items** | One concept per question |
| **Randomize scale direction** | Sometimes reverse-score to reduce acquiescence bias |

### Likert Scale Analysis

#### Per-Item Analysis
```
Mean score for item i = (1/n) * Σ Likert_score(i)
```

#### Agree/Disagree Method
```
% Agreement = (% selecting "Agree" or "Strongly Agree") / Total responses × 100%
```

#### Top-Box Analysis
```
Top-Box % = (% selecting highest category) / Total responses × 100%
```

### Statistical Tests for Likert Data

| Test | Use Case | Assumption |
|------|---------|------------|
| Mann-Whitney U | Compare two groups | Ordinal data, independent samples |
| Kruskal-Wallis | Compare three+ groups | Ordinal data, independent samples |
| Wilcoxon signed-rank | Paired comparison | Ordinal data, paired samples |
| Friedman test | Repeated measures comparison | Ordinal data, related samples |

### Likert Scale Reliability

| Reliability Type | Measure | Target |
|-----------------|---------|--------|
| Internal consistency | Cronbach's alpha | > 0.70 |
| Test-retest | Correlation between administrations | > 0.70 |
| Inter-rater | Agreement across respondents | Varies by construct |

## Survey Design Best Practices

### Question Design

| Do | Don't |
|----|-------|
| Use clear, simple language | Use jargon or technical terms |
| Ask one thing per question | Double-barrel questions |
| Provide balanced scales | Leading questions |
| Include "N/A" option when appropriate | Force responses that don't apply |
| Pilot test with 10–20 users | Deploy without testing |
| Keep surveys short (5–10 questions) | Long surveys (>15 minutes) |

### Survey Flow

```
1. Screening questions (ensure eligibility)
2. Behavioral context (what did you do today?)
3. Core satisfaction questions (5–7 Likert items)
4. Open-ended feedback (optional, "Anything else?")
5. Demographics (only if needed)
6. Thank you + incentive (if applicable)
```

### Response Rate Optimization

| Technique | Impact on Response Rate |
|-----------|----------------------|
| Short surveys (< 5 min) | +20–30% completion |
| Mobile-optimized design | +15–25% completion |
| Incentives (points, credits) | +30–50% completion |
| Personalized invitations | +10–20% completion |
| Timing (not during peak hours) | +10–15% completion |
| Progress bar | +5–10% completion |

## Survey Bias Mitigation

### Common Biases

| Bias | Description | Mitigation |
|------|-------------|-----------|
| **Acquiescence bias** | Tendency to agree with statements | Reverse-score some items |
| **Social desirability** | Reporting what sounds good | Anonymize responses, indirect questions |
| **Recency bias** | Remembering recent items more | Collect immediately after exposure |
| **Selection bias** | Only engaged users respond | Weight responses by engagement level |
| **Non-response bias** | Non-respondents differ from respondents | Compare respondent demographics to population |
| **Framing effect** | Question wording influences answers | Standardize and A/B test question wording |
| **Order effect** | Question order influences answers | Randomize question order |

### Statistical Bias Correction

1. **Raking/Post-stratification**: Weight survey responses to match population demographics
2. **Propensity score adjustment**: Model response propensity and adjust estimates
3. **Sensitivity analysis**: Test how robust findings are to different bias assumptions
4. **Multiple imputation**: Handle missing responses using imputation models

### Survey Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Response rate | % of invited users who respond | > 15% for in-app, > 5% for email |
| Completion rate | % of started surveys that are completed | > 80% |
| Average time | Time to complete the survey | < 5 minutes |
| Open-text rate | % providing open-ended feedback | > 30% |
| Inter-rater reliability | Agreement among raters (if applicable) | Cohen's κ > 0.6 |
