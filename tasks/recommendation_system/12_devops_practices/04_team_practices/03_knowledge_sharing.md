# Knowledge Sharing

## Overview

Knowledge sharing in ML teams is critical because expertise spans software engineering, data science, statistics, domain knowledge, and infrastructure. Unlike traditional software teams, ML teams must bridge multiple disciplines. Effective knowledge sharing prevents silos, accelerates onboarding, and builds collective capability.

## Tech Talks

### Internal Tech Talk Program

| Aspect | Description |
|--------|-------------|
| **Frequency** | Bi-weekly (30-60 minutes) |
| **Presenter rotation** | Every team member presents at least once per quarter |
| **Audience** | ML team + interested engineers from other teams |
| **Format** | 20-30 min presentation + 10-15 min Q&A |
| **Recording** | All talks recorded and posted to internal wiki |

### Tech Talk Topics

| Category | Example Topics |
|----------|---------------|
| **Model deep-dives** | How our ranking model works, attention mechanisms in recs |
| **Experiment results** | "We tried transformer-based recommendations - here is what happened" |
| **Industry trends** | Foundation models for recommendations, new research papers |
| **Tooling** | "How we use DVC for data versioning," "Our feature store architecture" |
| **Postmortems** | "What we learned from the latency incident" |
| **Domain knowledge** | "Understanding user behavior in e-commerce," "Recommendation fairness 101" |
| **Career growth** | "How to read ML papers efficiently," "Preparing for ML system design interviews" |

### Tech Talk Best Practices

1. **Start with the problem**: Why should the audience care?
2. **Use concrete examples**: Abstract concepts need real-world grounding
3. **Include live demos**: Working code is more convincing than slides
4. **Share slides and code**: Post materials for asynchronous learning
5. **Encourage questions**: Create a safe space for questions
6. **Follow up**: Share key takeaways and action items in Slack

## Paper Reading Groups

### Structure

| Aspect | Description |
|--------|-------------|
| **Frequency** | Weekly (1 hour) |
| **Paper selection** | Rotate responsibility weekly |
| **Format** | One presenter + group discussion |
| **Scope** | Recent papers from top venues (RecSys, KDD, NeurIPS, WWW) |
| **Output** | Summary document, relevance assessment, implementation ideas |

### Paper Reading Template

```markdown
# Paper Reading: [Paper Title]

## Paper Info
- Authors: ...
- Venue: ...
- Date: ...
- Link: ...

## Summary (1 paragraph)
Brief description of what the paper does and why it matters.

## Key Contributions
1. ...
2. ...

## Relevance to Our Work
- Directly applicable: [Yes/No]
- Potential application: ...
- Key insight: ...

## Questions/Discussions
1. How does this compare to our current approach?
2. What are the limitations?
3. Could we implement this? What would it take?

## Action Items
- Try approach X in next experiment
- Read related paper Y
- Discuss with team Z
```

### Recommended Venues

| Venue | Focus | Relevance |
|-------|-------|-----------|
| **RecSys** | Recommendation systems | Directly relevant |
| **KDD** | Knowledge discovery and data mining | Data and ML techniques |
| **NeurIPS** | Machine learning research | Cutting-edge ML |
| **WWW** | Web systems and applications | Systems and applications |
| **WSDM** | Web search and data mining | Search and recommendations |
| **SIGIR** | Information retrieval | Ranking and retrieval |
| **ICML** | Machine learning | General ML |

## ML Newsletter

### Internal Newsletter Sections

| Section | Content | Frequency |
|---------|---------|-----------|
| **Highlights** | Top 3 accomplishments this week | Weekly |
| **Experiments** | Key experiment results | Weekly |
| **Metrics** | Production metrics update | Weekly |
| **Papers** | Paper reading group summaries | Weekly |
| **Hiring** | New team members, open positions | Bi-weekly |
| **Events** | Upcoming talks, workshops, conferences | Monthly |
| **Learning** | Recommended resources, courses | Monthly |

### Newsletter Template

```markdown
# ML Team Weekly Digest - Week of [Date]

## Highlights
- New ranking model deployed: +3.2% NDCG@10 in A/B test
- Completed fairness audit for job recommendations
- Fixed feature store latency issue (p99 from 200ms to 50ms)

## Experiments
| Experiment | Status | Key Result |
|-----------|--------|-----------|
| Transformer ranking | Running | Interim: +1.5% CTR |
| Diversity re-ranking | Completed | +8% ILD, -0.5% NDCG |
| Cold-start embeddings | Planning | Starting next week |

## Metrics Update
- DAU: 1.2M (+2% WoW)
- Recommendation CTR: 4.8% (+0.3% WoW)
- Revenue per user: $12.50 (+1.2% WoW)

## Paper Reading
Paper: "Self-Attentive Sequential Recommendation" (Kang and McAuley, ICDM 2018)
Summary: Transformer-based approach for sequential recommendations.
Relevance: Could improve our session-based recommendations.
```

## Documentation Culture

### Documentation Standards

| Document Type | Owner | Update Frequency | Review |
|--------------|-------|-----------------|--------|
| **API documentation** | API team | On every API change | Automated (CI) |
| **Architecture docs** | Tech lead | Quarterly | Team review |
| **Runbooks** | SRE + ML team | After every incident | Quarterly audit |
| **Experiment reports** | Experiment owner | After each experiment | Peer review |
| **Onboarding guide** | Team lead | Monthly | New hire feedback |
| **Model cards** | Model owner | On every model update | Peer review |

### Documentation as Code

All documentation lives in the repository and is reviewed like code:

```
docs/
  architecture/
    system-overview.md
    data-pipeline.md
    model-serving.md
  guides/
    getting-started.md
    local-development.md
    experiment-tracking.md
  runbooks/
    high-latency.md
    model-degradation.md
    data-pipeline-failure.md
  api/
    openapi.yaml
    changelog.md
  experiments/
    2024-01-transformer-ranking.md
    2024-02-diversity-reranking.md
```

### Documentation Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Coverage** | > 90% of key components documented | Audit quarterly |
| **Freshness** | All docs updated within 90 days | Automated check |
| **Accuracy** | Zero outdated procedures followed | Incident reports |
| **Accessibility** | New hire can find what they need | Onboarding feedback |

## Postmortem Sharing

### Blameless Postmortem Structure

```markdown
# Postmortem: [Incident Title]

## Incident Summary
- Date: ...
- Duration: ...
- Severity: SEV...
- Impact: [user count, revenue, metrics affected]

## Timeline
- HH:MM - Event 1
- HH:MM - Event 2
...

## Root Cause
Technical description of what went wrong.

## What Went Well
Things that helped during the incident.

## What Went Wrong
Things that made the incident worse or harder to resolve.

## Action Items
| Owner | Action | Priority | Due Date |
|-------|--------|----------|----------|
| Alice | Add monitoring for X | High | 2 weeks |
| Bob | Update runbook for Y | Medium | 1 month |

## Lessons Learned
Key takeaways for the team.
```

### Postmortem Sharing Process

1. **Write within 48 hours** of incident resolution
2. **Share in team channel** within 1 week
3. **Present at team meeting** within 2 weeks
4. **Archive in knowledge base** for future reference
5. **Track action items** to completion

## Cross-Team Knowledge Transfer

### Transfer Mechanisms

| Mechanism | Description | Frequency |
|-----------|-------------|----------|
| **Tech talks to other teams** | Share ML capabilities with product teams | Monthly |
| **Documentation sharing** | Publish ML guides on company wiki | Ongoing |
| **Pair programming** | Work with other teams on ML integration | As needed |
| **Rotation programs** | Temporarily embed in other teams | Quarterly |
| **Brown bag sessions** | Informal lunch-and-learn presentations | Bi-weekly |

### Cross-Team Topics

| Topic | Target Audience | Format |
|-------|----------------|--------|
| How recommendations work | Product managers | Presentation |
| ML API integration guide | Backend engineers | Workshop |
| Feature engineering basics | Data engineers | Pair programming |
| Experiment design for PMs | Product managers | Workshop |
| ML metrics interpretation | Business analysts | Presentation |

## External Conference Participation

### Conference Attendance Policy

| Conference Type | Attendance Policy | Knowledge Return |
|----------------|------------------|-----------------|
| **Top-tier research** (NeurIPS, ICML) | Sponsor 2-3 engineers/year | Present paper or poster |
| **Applied ML** (RecSys, KDD) | Send 1-2 engineers/year | Blog post + internal talk |
| **Industry** (QCon, StrangeLoop) | Open to all with manager approval | Internal presentation |
| **Local meetups** | Encourage attendance | Share learnings in Slack |

### Conference Return on Investment

After attending a conference, attendees should:

1. **Write a summary** (1 page) of key takeaways within 1 week
2. **Present findings** at next tech talk
3. **Identify action items** (papers to read, techniques to try)
4. **Share slides and notes** on company wiki
5. **Connect with contacts** made at the conference

## Internal Wiki

### Wiki Structure

```
Wiki Home
  Team/
    People and roles
    Team norms and values
    Hiring process
  ML Platform/
    System architecture
    Model serving guide
    Feature store documentation
    Experiment tracking guide
  Research/
    Paper reading summaries
    Experiment logs
    Research roadmap
  Operations/
    On-call guide
    Runbooks
    Incident reports
    Deployment procedures
  Learning/
    Recommended reading
    Online courses
    Internal tutorials
    Career development
```

### Wiki Maintenance

| Responsibility | Action | Frequency |
|---------------|--------|-----------|
| **Page owners** | Update their pages | Monthly |
| **Team lead** | Review wiki health | Monthly |
| **New hires** | Flag outdated or missing content | During onboarding |
| **Wiki champion** | Reorganize and prune stale content | Quarterly |
