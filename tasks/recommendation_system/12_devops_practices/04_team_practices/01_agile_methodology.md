# Agile Practices for ML Teams

## Overview

Agile methodologies were designed for software development, but ML work introduces unique challenges: experiments may fail, results are uncertain, and iteration cycles are longer and less predictable. Adapting Agile for ML teams requires modified ceremonies, acceptance of uncertainty, and practices that account for the experimental nature of machine learning work.

## Sprint Planning for ML Work

### Challenges of ML Sprint Planning

- **Uncertain outcomes**: An experiment may fail, requiring a different approach.
- **Variable iteration length**: Model training can take hours to days.
- **Dependency on data**: Data quality issues or pipeline failures can derail timelines.
- **Research vs engineering split**: Some work is exploratory (research) while other work is deterministic (engineering).
- **Metric lag**: Online metrics take days or weeks to materialize.

### Story Types in ML Projects

| Story Type | Description | Estimation Approach | Sprint Velocity Impact |
|------------|-------------|--------------------|-----------------------|
| Engineering | Build serving infrastructure, API endpoints | Standard story points | Predictable |
| Data | Build data pipelines, feature engineering | Standard story points | Predictable |
| Experiment | Test new model architecture, hyperparameter sweep | T-shirt sizing (S/M/L) | Variable |
| Analysis | Analyze experiment results, identify patterns | Time-boxed | Variable |
| Production | Deploy model, monitor, debug issues | Standard story points | Predictable |

### Sprint Structure for ML Teams

**Recommended Sprint Length**: 2 weeks.

**Sprint Allocation**:

- 60% engineering and data work (predictable).
- 25% experiments and research (variable).
- 15% maintenance, tech debt, and documentation.

**Planning Process**:

1. Start with engineering and data stories (high confidence estimates).
2. Plan experiments with explicit hypotheses and success criteria.
3. Define time-boxed analysis tasks (max 2 days per analysis).
4. Include buffer stories that can be pulled in if experiments finish early.
5. Identify dependencies and blockers before the sprint begins.

### Story Point Calibration

- Use Fibonacci sequence (1, 2, 3, 5, 8, 13) for estimation.
- Calibrate estimates based on past sprint velocity.
- Account for experiment uncertainty: a "5-point experiment" may become a "13-point experiment" if the first approach fails.
- Track estimation accuracy over time and adjust planning accordingly.

## Managing Uncertainty in ML Projects

### Uncertainty Taxonomy

| Uncertainty Type | Source | Mitigation |
|-----------------|--------|------------|
| Data uncertainty | Missing data, quality issues | Data validation, monitoring |
| Model uncertainty | Unknown model performance | Quick prototyping, baselines |
| Infrastructure uncertainty | New tools, scaling issues | Spike tasks, proof of concept |
| Requirements uncertainty | Changing business needs | Frequent stakeholder check-ins |
| Temporal uncertainty | Long training/evaluation cycles | Early stopping, checkpointing |

### Risk Management Strategies

**Early Validation**:

- Run small-scale experiments before committing to full-scale training.
- Validate data quality before feature engineering.
- Test infrastructure scalability before production deployment.
- Use hold-out sets for quick performance estimation.

**Time-Boxing**:

- Set maximum time for any single experiment (e.g., 3 days).
- If no progress after the time box, escalate or pivot.
- Document learnings from failed experiments.
- Move to the next priority if an approach is not working.

**Baseline Comparison**:

- Always establish a baseline before trying complex approaches.
- A simple model that works is better than a complex model that might work.
- Use the Pareto principle: 80% of improvement comes from 20% of effort.

**Progressive Elaboration**:

- Start with a rough understanding and refine as the sprint progresses.
- Update estimates as new information becomes available.
- Communicate uncertainty honestly to stakeholders.

## ML-Specific Ceremonies

### Experiment Review

**Frequency**: Biweekly (aligned with sprint cadence).

**Agenda**:

1. Review completed experiments and their results.
2. Compare against baselines and success criteria.
3. Identify patterns and insights from results.
4. Decide next experiments to run.
5. Update experiment tracking system.

**Attendees**: ML engineers, data scientists, ML lead.

**Outputs**: Updated experiment backlog, next sprint experiment priorities.

### Model Review

**Frequency**: Before every production deployment.

**Agenda**:

1. Present model performance (offline and online metrics).
2. Review training data and feature pipeline changes.
3. Discuss known limitations and edge cases.
4. Review deployment plan and rollback strategy.
5. Obtain approval for production deployment.

**Attendees**: ML engineers, SRE, product manager, domain expert.

**Outputs**: Deployment decision (approve/reject), deployment checklist.

### Data Quality Review

**Frequency**: Weekly.

**Agenda**:

1. Review data pipeline health and freshness.
2. Identify data quality issues (missing values, anomalies).
3. Discuss data collection changes or new data sources.
4. Review feature pipeline performance.

**Attendees**: Data engineers, ML engineers, data analyst.

**Outputs**: Data quality report, action items for data issues.

### Architecture Review

**Frequency**: Monthly or as needed for significant changes.

**Agenda**:

1. Review proposed architectural changes.
2. Discuss tradeoffs and alternatives.
3. Write or update ADRs for accepted decisions.
4. Review system health and scalability concerns.

**Attendees**: Tech lead, senior engineers, SRE.

**Outputs**: Updated ADRs, architectural recommendations.

## Velocity Tracking

### ML-Adjusted Velocity Metrics

**Story Points Completed**:

- Track total story points completed per sprint.
- Separate points by type (engineering, data, experiment, analysis).
- Track estimation accuracy (estimated vs. actual).

**Experiment Velocity**:

- Number of experiments completed per sprint.
- Experiment success rate (percentage meeting success criteria).
- Time from hypothesis to conclusion per experiment.

**Production Velocity**:

- Number of model deployments per sprint.
- Time from experiment completion to production deployment.
- Deployment success rate (no rollback required).

### Velocity Dashboard Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Sprint velocity | Stable (+/- 10%) | Story points completed |
| Experiment velocity | 3-5 per sprint | Experiments concluded |
| Deployment frequency | 1-2 per sprint | Models deployed to production |
| Estimation accuracy | Within 20% | Estimated vs. actual points |
| Experiment success rate | 30-50% | Experiments meeting criteria |

### Using Velocity for Planning

- Use 3-sprint rolling average for sprint capacity planning.
- Reserve 20% of capacity for unplanned work (incidents, urgent fixes).
- Adjust capacity for team changes (vacations, new hires).
- Track velocity trends to identify process improvements or problems.

## Technical Debt Sprints

### Identifying Technical Debt

- Maintain a technical debt register (backlog of debt items).
- Categorize debt: code quality, ML debt, infrastructure debt, documentation debt.
- Estimate effort and impact for each debt item.
- Prioritize using effort-impact matrix.

### Debt Sprint Cadence

- Schedule one debt sprint per quarter (or every 6 sprints).
- Allocate 20% of each regular sprint to debt reduction.
- Include debt stories in sprint planning alongside feature work.
- Track debt reduction as a velocity metric.

### Debt Reduction Priorities

| Priority | Debt Type | Example | Impact |
|----------|----------|---------|--------|
| 1 | Training-serving skew | Inconsistent feature computation | Bugs |
| 2 | Untested model logic | Missing unit tests for ranking | Regressions |
| 3 | Stale configurations | Hardcoded hyperparameters | Reproducibility |
| 4 | Missing documentation | Undocumented pipelines | Onboarding |
| 5 | Outdated dependencies | Old library versions | Security |
| 6 | Code duplication | Same feature in 3 places | Maintenance |

## Cross-Functional Collaboration

### Team Structure

| Role | Responsibility | Primary Ceremonies |
|------|---------------|-------------------|
| ML Engineer | Model development, training, serving | Experiment review, model review |
| Data Engineer | Data pipelines, feature engineering | Data quality review |
| SRE | Infrastructure, monitoring, deployment | Architecture review, on-call |
| Product Manager | Requirements, priorities, stakeholder alignment | Sprint planning, demos |
| Domain Expert | Business context, evaluation criteria | Experiment review, model review |

### Collaboration Patterns

- **Pair Programming**: ML engineer + SRE for production deployment code.
- **Mob Programming**: For complex feature engineering or debugging.
- **Knowledge Sharing**: Weekly tech talks or reading groups.
- **Code Review**: Cross-functional reviews for significant changes.
- **Shadowing**: Junior members shadow senior members during critical operations.

### Communication Channels

| Channel | Purpose | Frequency |
|---------|---------|-----------|
| Sprint planning | Plan work, estimate stories | Biweekly |
| Daily standup | Sync on progress, blockers | Daily |
| Experiment review | Review experiment results | Biweekly |
| Model review | Pre-deployment review | As needed |
| Tech talk | Share knowledge, discuss trends | Weekly |
| Architecture review | Discuss system design | Monthly |

## Documentation as Code

### Documentation Principles

- Documentation lives alongside code in the same repository.
- Documentation is version-controlled and reviewed in pull requests.
- Documentation is generated from code where possible (API docs, config schemas).
- Documentation is tested (broken links, code examples that execute).

### Documentation Types

| Type | Tool | Update Cadence | Owner |
|------|------|----------------|-------|
| Architecture | ADRs in Markdown | On decision | Tech lead |
| API Reference | Auto-generated (Sphinx, MkDocs) | On code change | ML engineers |
| Runbooks | Markdown in docs/ | On incident | SRE |
| Experiment Logs | Experiment tracking tool (MLflow) | Per experiment | ML engineers |
| Onboarding | Markdown in docs/ | Monthly | Team lead |

### Documentation Standards

- Write for your audience (new hire, domain expert, SRE).
- Include examples and code snippets where applicable.
- Keep documentation up to date; stale documentation is worse than no documentation.
- Use consistent formatting and structure across all documentation.
- Link between related documents for easy navigation.
