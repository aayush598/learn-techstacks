# Mean Reciprocal Rank (MRR)

## Overview

Mean Reciprocal Rank (MRR) is a metric that evaluates the quality of a ranked list by focusing on a single aspect: the position of the first relevant item. It is particularly useful in scenarios where there is exactly one correct or most relevant result, such as navigational search queries, question answering, or "find me the right product" scenarios.

MRR assigns a score equal to the reciprocal of the rank position at which the first relevant item appears. Averaging these scores across all queries gives the Mean Reciprocal Rank.

## Formal Definition

### Reciprocal Rank (RR)

For a single query q with a ranked list of results, the Reciprocal Rank is:

```
RR(q) = 1 / rank(f)
```

Where `rank(f)` is the position (1-indexed) of the first relevant item in the ranked list. If no relevant item appears in the ranked list, RR(q) = 0.

### Mean Reciprocal Rank (MRR)

MRR averages RR across all queries:

```
MRR = (1 / |Q|) * Σ (i=1 to |Q|) 1 / rank_i(f)
```

Where:
- `|Q|` is the total number of queries
- `rank_i(f)` is the rank of the first relevant item for query i

### MRR@K Variant

MRR@K restricts evaluation to the top-K positions. If the first relevant item appears after position K, the score for that query is 0:

```
MRR@K(q) = 1 / rank(f)  if rank(f) ≤ K
            0              otherwise
```

The choice of K reflects how many results a user is willing to examine before giving up.

## Worked Example

Consider a system evaluated on 5 queries, with a ranked list of 5 items each (R = relevant):

| Query | Position 1 | Position 2 | Position 3 | Position 4 | Position 5 | RR |
|-------|-----------|-----------|-----------|-----------|-----------|-----|
| Q1    | R         | N         | N         | N         | N         | 1/1 = 1.0 |
| Q2    | N         | R         | N         | N         | N         | 1/2 = 0.5 |
| Q3    | N         | N         | N         | R         | N         | 1/4 = 0.25 |
| Q4    | N         | N         | N         | N         | N         | 0 |
| Q5    | N         | N         | R         | N         | N         | 1/3 = 0.333 |

**MRR** = (1.0 + 0.5 + 0.25 + 0 + 0.333) / 5 = **0.417**

**MRR@3** = (1.0 + 0.5 + 0 + 0 + 0.333) / 5 = **0.367** (Q4 and Q3 contribute 0 because first relevant is beyond position 3 or absent)

## MRR for Single Relevant Item Scenarios

MRR is most naturally suited to single-relevant-item scenarios:

### Navigational Search
- User wants to find a specific website (e.g., "Amazon login")
- There is exactly one correct result
- RR directly measures how quickly the user finds what they need

### Question Answering
- A QA system returns ranked answers
- The top answer is the "correct" one
- MRR measures whether the correct answer appears first, second, etc.

### Entity Resolution
- Given a query, the system returns ranked entity matches
- One entity is the ground truth
- MRR captures how early the correct entity appears

### Command/Intent Execution
- Voice assistants interpret user commands
- The system proposes ranked interpretations
- The first correct interpretation determines success

## Handling Multiple Relevant Items

When there are multiple relevant items for a query, MRR can be adapted:

| Strategy | Formula | When to Use |
|----------|---------|-------------|
| **First relevant** | RR = 1/rank(first relevant) | Standard MRR, focus on earliest match |
| **Best relevant** | RR = 1/rank(most relevant) | When relevance is graded |
| **Average over all** | RR = (1/|R|) * Σ 1/rank(r_j) for all relevant items r_j | When each relevant item has independent value |

The standard MRR formulation uses the "first relevant" strategy. The others are variants sometimes called "Reciprocal Rank of Average" or similar.

## Comparison with MAP and NDCG

| Aspect | MRR | MAP | NDCG |
|--------|-----|-----|------|
| **Focus** | Position of first relevant item | All relevant positions | All positions, weighted by relevance |
| **Multiple relevant items** | Only cares about the first | Considers all | Considers all |
| **Position sensitivity** | Only sensitive to first relevant rank | Sensitive to all relevant ranks | Exponentially sensitive to all positions |
| **Graded relevance** | Can adapt (use most relevant rank) | Requires adaptation | Native support |
| **Interpretation** | "Where does the user find the first hit?" | "How precise is the ranking overall?" | "How well-ranked is the entire list?" |
| **Appropriate when** | Single correct answer | Multiple relevant items matter | Position-weighted quality matters |

### When MRR Diverges from MAP/NDCG

Consider two ranked lists for a query with 3 relevant items:

**List A:** [R, N, N, R, R] → MRR = 1.0, but 2 relevant items are pushed far down
**List B:** [R, R, R, N, N] → MRR = 1.0, but all relevant items are at the top

MRR assigns identical scores, but List B is clearly better. MAP and NDCG would correctly distinguish them. This illustrates that MRR is only appropriate when the first relevant item is what matters.

## MRR@K Analysis

### Choosing K

The choice of K significantly impacts MRR@K:

| K | Interpretation | Typical Use Case |
|---|---------------|------------------|
| 1 | Did the first item succeed? | Binary pass/fail evaluation |
| 3 | Is the answer in the top 3? | Voice assistants, chatbots |
| 5 | Top page evaluation | Standard search evaluation |
| 10 | Full first page | Web search |
| 20 | Extended evaluation | E-commerce product search |

### K Sensitivity
- **Small K (1–3)**: MRR@K is very strict; even good systems may score low
- **Large K (10–20)**: MRR@K becomes more lenient, conflating systems that differ in early positions
- **K = 1**: MRR@1 is equivalent to Precision@1 (did the top item match?)

## When MRR Is Most Appropriate

### Ideal Scenarios
1. **One correct answer per query**: Navigational search, FAQ matching, entity lookup
2. **User patience is limited**: The user will scan until they find the right item, then stop
3. **Binary relevance**: Items are either correct or not; no partial credit needed
4. **Quick diagnostic**: MRR is fast to compute and easy to explain to non-technical stakeholders

### Poor Scenarios
1. **Multiple relevant items needed**: The user wants a set of diverse recommendations (use MAP or NDCG)
2. **Graded relevance matters**: A "highly relevant" item at position 5 is better than a "marginally relevant" item at position 1 (use NDCG)
3. **Full list quality matters**: The diversity and overall quality of the top-10 matters, not just the first hit (use coverage metrics + MAP)

## Practical Considerations

### Handling Queries with No Relevant Items
- Some evaluators exclude queries with no relevant items from the MRR calculation
- Others include them with RR = 0, which penalizes systems more harshly
- The standard approach includes them: if the system cannot find anything relevant, it deserves a zero for that query

### Confidence Intervals
- MRR is a mean of non-negative values bounded by [0, 1]
- Bootstrap confidence intervals are recommended over normal approximation, especially when many queries have RR = 0 (skewed distribution)

### Segmented Analysis
- Report MRR by query type (navigational vs. informational)
- Report MRR by user segment (new vs. returning users)
- Report MRR by item popularity (head vs. tail queries)

### Common Pitfalls
- Using MRR when the task actually requires multiple relevant items in the list
- Comparing MRR across different K values without noting the difference
- Ignoring queries where MRR = 0, which biases the average upward
- Failing to account for the bimodal distribution of RR (many 0s, many high values)

## Advanced Extensions

### MRR for Multi-Label Scenarios
When a query has multiple equally important relevant items, consider reporting the distribution of RR values rather than a single mean, since the first relevant item varies across users.

### Reciprocal Rank Fusion (RRF)
RRF combines ranked lists from multiple systems using reciprocal rank:
```
RRF_score(d) = Σ 1 / (k + rank_i(d))
```
Where k is a constant (typically 60) to smooth the contribution of high-ranked items. RRF is used in hybrid recommendation systems that combine collaborative filtering, content-based, and knowledge-based signals.

### Conditional MRR
C-MRR reports MRR conditioned on whether the first relevant item is within a specified threshold, providing a pass-rate view alongside the traditional average.
