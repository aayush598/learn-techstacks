# Sprint Planning for ML

## Overview

Sprint planning for ML teams requires adapting traditional Agile practices to accommodate the inherent uncertainty of research and experimentation. ML work is less predictable than traditional software engineering—a model improvement that seems simple may require weeks of data investigation, or a complex architecture change may work on the first try. Effective sprint planning balances structured delivery with the flexibility needed for ML discovery.

## Sprint Cadence

### Standard 2-Week Sprint

| Week | Focus | Activities |
|------|-------|-----------|
| **Week 1** | Execution | Model development, feature engineering, experimentation |
| **Week 2** | Delivery + Planning | Finalize experiments, prepare deployment, plan next sprint |

### Sprint Calendar

```
Monday    - Sprint planning (2 hours)
Tuesday   - Development
Wednesday - Development + Mid-sprint check-in (15 min)
Thursday  - Development
Friday    - Development + Code review
Monday    - Development + Experiment review
Tuesday   - Development
Wednesday - Development + Mid-sprint check-in (15 min)
Thursday  - Development + Sprint demo prep
Friday    - Sprint review + retrospective (1.5 hours)
```

### Why 2 Weeks for ML

| Duration | Pros | Cons |
|----------|------|------|
| 1 week | Fast feedback, low commitment | Too short for meaningful experiments |
| **2 weeks** | **Balance of speed and depth** | **Good default for ML teams** |
| 3 weeks | More time for complex experiments | Slower feedback, harder to course-correct |
| 4 weeks | Good for research projects | Too long, loses urgency |

## Story Estimation for ML Tasks

### The Uncertainty Challenge

ML tasks have higher uncertainty than traditional software tasks:

| Task Type | Uncertainty | Typical Estimation Error |
|-----------|------------|------------------------|
| Bug fix | Low | 10–20% |
| Feature implementation | Medium | 20–40% |
| Model improvement | High | 50–200% |
| Research exploration | Very high | 200–500% |
| Infrastructure work | Low–Medium | 20–40% |

### Estimation Strategies

#### T-Shirt Sizing (Recommended for ML)

| Size | Time Range | Description |
|------|-----------|-------------|
| **XS** | 0.5–1 day | Config change, simple fix, documentation |
| **S** | 1–2 days | Feature engineering, small model change |
| **M** | 3–5 days | New model component, significant feature |
| **L** | 1–2 weeks | New model architecture, major pipeline change |
| **XL** | 2–4 weeks | Research project, major infrastructure |
| **XXL** | 4+ weeks | Break into smaller stories |

#### Cone of Uncertainty

```
Estimate accuracy by story size:
  XS: ±20%
  S:  ±30%
  M:  ±50%
  L:  ±75%
  XL: ±100%
```

#### Uncertainty Buffers

For ML tasks, add uncertainty buffers:

```
Estimated time × Uncertainty factor = Planned time

Where uncertainty factor:
  Well-understood task: 1.0–1.3
  Partially understood: 1.5–2.0
  Research/exploration: 2.0–3.0
```

### Story Point Approximation

| Points | Approximate Time | Example |
|--------|-----------------|---------|
| 1 | Half day | Fix config typo, update docs |
| 2 | 1 day | Add a feature, write tests |
| 3 | 2 days | Implement new feature, refactor module |
| 5 | 3–4 days | New model component, significant pipeline work |
| 8 | 1 week | New model architecture, major feature |
| 13 | 2 weeks | Complex research project (should be broken down) |

## Sprint Capacity Planning

### Capacity Calculation

```
Sprint capacity = Team size × Sprint days × Focus factor - Overhead

Where:
  Team size: Number of engineers on the team
  Sprint days: Working days in sprint (typically 10)
  Focus factor: % of time on sprint work (typically 0.6–0.8)
  Overhead: Meetings, on-call, admin (typically 20–30%)
```

### Example Capacity Calculation

| Component | Value |
|-----------|-------|
| Team size | 4 engineers |
| Sprint days | 10 |
| Focus factor | 0.7 |
| Overhead | 0.25 |
| **Available capacity** | **4 × 10 × 0.7 × 0.75 = 21 days** |

### ML-Specific Capacity Adjustments

| Factor | Impact | Adjustment |
|--------|--------|-----------|
| **Experiment iteration** | Experiments may need multiple runs | Add 30–50% buffer |
| **Data investigation** | Unexpected data issues | Add 20% buffer for data tasks |
| **On-call rotation** | Engineer unavailable for 1–2 days | Reduce capacity by on-call days |
| **Experiment review** | Weekly meeting + prep | 2 hours/week per ML engineer |
| **Paper reading** | Research time allocation | 10–20% of capacity |

### Capacity Planning Template

```
Sprint 12 Capacity Plan

Team:
  - Alice: 8 days (1 day on-call)
  - Bob: 9 days
  - Carol: 7 days (2 days meetings)
  - Dave: 9 days

Total capacity: 33 days
Buffer (20%): 6.6 days
Available for sprint work: 26.4 days

Planned work:
  - Story A (model improvement): 8 points → 5 days
  - Story B (feature engineering): 5 points → 3 days
  - Story C (bug fix): 2 points → 1 day
  - Story D (infrastructure): 8 points → 5 days
  - Technical debt: 5 points → 3 days

Total planned: 28 days (within capacity with buffer)
```

## ML-Specific Ceremonies

### Experiment Review (Weekly)

| Agenda Item | Duration | Description |
|-------------|----------|-------------|
| Experiment status update | 15 min | What experiments are running, results |
| Results discussion | 20 min | Analyze results, interpret metrics |
| Next steps | 10 min | Decide what to try next |
| Blockers | 5 min | Data, compute, or infrastructure issues |

### Model Review (Before Deployment)

| Agenda Item | Duration | Description |
|-------------|----------|-------------|
| Model overview | 10 min | Architecture, training data, approach |
| Evaluation results | 15 min | Offline metrics, fairness audit |
| Error analysis | 10 min | Common failure modes |
| Deployment plan | 10 min | Rollout strategy, monitoring |
| Go/No-go decision | 5 min | Vote on deployment readiness |

### Sprint Review (Bi-weekly)

For ML teams, the sprint review should include:

| Section | Duration | Content |
|---------|----------|---------|
| Demo | 15 min | Show working features/model improvements |
| Metrics review | 10 min | Key metrics since last review |
| Experiment outcomes | 10 min | What we learned from experiments |
| Next sprint preview | 10 min | Upcoming priorities |

## Handling Research vs Engineering Work

### The Research-Engineering Balance

| Work Type | Description | Sprint Allocation |
|-----------|-------------|------------------|
| **Research** | Exploring new approaches, reading papers | 20–30% |
| **Engineering** | Building production features, fixing bugs | 50–60% |
| **Maintenance** | Tech debt, infrastructure, documentation | 15–25% |

### Research in Sprints

#### Option 1: Dedicated Research Sprint
- Every 4th sprint is a "research sprint" focused on exploration
- No delivery commitments
- Output: research findings, proof-of-concept code

#### Option 2: Research Capacity Allocation
- Allocate 20–30% of each sprint to research
- Research stories have "research" label
- Lower estimation confidence (use ranges)

#### Option 3: Innovation Time
- 10% of time (Fridays) reserved for research
- Engineers choose research topics
- Monthly sharing of findings

### Research Story Handling

```
Research Story Template:
  Title: Explore [approach] for [problem]
  Hypothesis: [What we believe]
  Success criteria: [How we'll know if it works]
  Time budget: [Maximum time to spend]
  Decision point: [When to decide go/no-go]
  Output: [What we'll deliver - findings, PoC, recommendation]
```

## Velocity Tracking

### ML Velocity Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Story points completed** | Sum of completed story points | Overall throughput |
| **Experiment completion rate** | Completed experiments / planned experiments | Research productivity |
| **Model deployment frequency** | Deployments per sprint | Delivery cadence |
| **Time to experiment result** | Days from start to result | Experimentation speed |
| **Story point accuracy** | Estimated / Actual (per story) | Estimation improvement |

### Velocity Tracking Dashboard

| Sprint | Planned | Completed | Accuracy | Deployments | Experiments |
|--------|---------|-----------|----------|-------------|-------------|
| Sprint 8 | 28 | 24 | 86% | 1 | 3 |
| Sprint 9 | 30 | 31 | 103% | 2 | 4 |
| Sprint 10 | 26 | 22 | 85% | 1 | 2 |
| Sprint 11 | 28 | 29 | 104% | 2 | 5 |
| **Average** | **28** | **26.5** | **95%** | **1.5** | **3.5** |

### Velocity Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|---------|
| **Velocity inflation** | Team overestimates to look productive | Use historical data, not commitments |
| **Research without timebox** | Research never ends | Set strict time limits on research |
| **Ignoring failed experiments** | Failed experiments count as "incomplete" | Celebrate learning, count experiments completed |
| **Mixing research and delivery** | Research stories steal delivery capacity | Separate research and delivery tracking |
| **Commitment-driven planning** | Team commits to more than capacity | Use capacity-driven planning |
