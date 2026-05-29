# Section 07: Feature Prioritization Framework

## Prioritization Methodology

We use a weighted scoring framework combining four factors: Customer Value, Business Value, Implementation Effort, and Strategic Alignment. This ensures data-driven prioritization that balances user needs with business goals.

```
Scoring Framework
┌─────────────────────────────────────────────────────────────────────────┐
│ Factor              │ Weight │ Assessed By          │ Scale            │
├─────────────────────────────────────────────────────────────────────────┤
│ Customer Value      │ 35%    │ User research, data   │ 1-10            │
│ Business Value      │ 30%    │ Revenue impact,       │ 1-10            │
│                     │        │ retention, growth     │                 │
│ Implementation      │ 20%    │ Engineering estimate  │ 1-10 (inverted) │
│ Effort              │        │ (higher = easier)     │                 │
│ Strategic           │ 15%    │ Product strategy,     │ 1-10            │
│ Alignment           │        │ competitive position   │                 │
└─────────────────────────────────────────────────────────────────────────┘
```

## Scoring Model

```typescript
interface FeatureRequest {
  id: string;
  title: string;
  description: string;
  
  // Customer Value (35%)
  userImpact: number; // 1-10: how many users benefit
  problemSeverity: number; // 1-10: how painful is the problem
  userRequests: number; // count of user requests
  csatImpact: number; // 1-10: expected CSAT change
  
  // Business Value (30%)
  revenueImpact: number; // 1-10: expected revenue change
  retentionImpact: number; // 1-10: expected churn reduction
  competitiveAdvantage: number; // 1-10: differentiation
  marketability: number; // 1-10: ease of selling
  
  // Implementation Effort (20%) - inverted (higher = easier)
  engineeringDays: number;
  complexity: 'low' | 'medium' | 'high' | 'critical';
  dependencies: string[]; // blocking features
  riskLevel: 'low' | 'medium' | 'high';
  
  // Strategic Alignment (15%)
  visionAlignment: number; // 1-10: fits product vision
  platformReuse: number; // 1-10: benefits other features
  complianceRequired: boolean;
}

function calculatePriorityScore(feature: FeatureRequest): number {
  const customerValue = (
    feature.userImpact * 0.4 +
    feature.problemSeverity * 0.3 +
    Math.min(feature.userRequests / 10, 10) * 0.15 +
    feature.csatImpact * 0.15
  );
  
  const businessValue = (
    feature.revenueImpact * 0.4 +
    feature.retentionImpact * 0.3 +
    feature.competitiveAdvantage * 0.2 +
    feature.marketability * 0.1
  );
  
  const effortScore = (
    (feature.complexity === 'low' ? 10 : feature.complexity === 'medium' ? 6 : feature.complexity === 'high' ? 3 : 1) * 0.5 +
    (feature.riskLevel === 'low' ? 10 : feature.riskLevel === 'medium' ? 5 : 1) * 0.3 +
    Math.max(0, 10 - feature.engineeringDays / 30) * 0.2
  );
  
  const strategicAlignment = (
    feature.visionAlignment * 0.5 +
    feature.platformReuse * 0.3 +
    (feature.complianceRequired ? 10 : 5) * 0.2
  );
  
  return (
    customerValue * 0.35 +
    businessValue * 0.30 +
    effortScore * 0.20 +
    strategicAlignment * 0.15
  );
}
```

## Opportunity Scoring

For customer-sourced feature requests, we use an opportunity scoring model based on the KANO methodology:

| Type | Description | Score Impact | Action |
|------|-------------|--------------|--------|
| Must-have | Expected, stated | +3 points | Required for launch |
| Performance | Wanted, stated | +2 points | Prioritize by value |
| Delighters | Unexpected, unstated | +1 point | Differentiators |
| Indifferent | Don't care | 0 points | Don't build |
| Reverse | Actively disliked | -5 points | Investigate |

## Prioritization Cadence

```
Monthly Prioritization Cycle
Week 1: Collect → Gather ideas from all sources (support, sales, product, analytics)
Week 2: Score → Apply framework, generate initial ranking
Week 3: Review → Product team reviews, adjusts weights
Week 4: Commit → Finalize next sprint/quarter priorities
```

## Priority Buckets

### P0: Critical (Must do this quarter)
- Features that unblock revenue, fix critical bugs, or address compliance
- Examples: SSO (unblocks enterprise deals), HIPAA (unblocks healthcare)

### P1: High Priority (Should do this quarter)
- Features with high customer value and/or business value
- Examples: Visual agent builder, marketplace

### P2: Medium Priority (Nice to have this quarter)
- Features that improve existing capabilities
- Examples: Additional voices, performance improvements

### P3: Low Priority (Backlog)
- Features that are valuable but not yet urgent
- Examples: Additional languages, niche integrations

### P4: Future (Not yet scoped)
- Strategic features aligned with long-term vision
- Examples: FedRAMP, multi-modal AI

## Feature Voting & Input Sources

| Source | Weight | Collection Method | Frequency |
|--------|--------|-------------------|-----------|
| Customer support tickets | High | Zendesk/Intercom tags | Weekly |
| Sales feedback | High | Salesforce win/loss | Bi-weekly |
| User interviews | Very high | User Interviews, Sprig | Monthly |
| In-app surveys | Medium | Sprig, PostHog surveys | Weekly |
| Usage analytics | Very high | PostHog, Amplitude | Ongoing |
| Community (Discord, GitHub) | Medium | GitHub issues, Discord | Ongoing |
| Competitive analysis | High | Crayon, Klue, manual | Monthly |
| Strategic initiatives | Very high | Leadership | Quarterly |

## Example Prioritization

| Feature | Customer Value | Business Value | Effort | Strategic | Total | Priority |
|---------|---------------|---------------|--------|-----------|-------|----------|
| SSO/SAML | 9 | 10 | 4 | 9 | 8.55 | P0 |
| Visual agent builder | 10 | 9 | 3 | 10 | 8.45 | P0 |
| Marketplace | 7 | 9 | 5 | 10 | 7.80 | P1 |
| Slack integration | 6 | 5 | 7 | 5 | 5.70 | P2 |
| Custom dashboard colors | 3 | 2 | 8 | 3 | 3.55 | P3 |

## De-prioritization Guidelines

Features are de-prioritized when: (1) Engineering effort outweighs expected value, (2) Strategic misalignment (doesn't move north star), (3) Too early (market not ready), (4) Can be solved by integration/partner, (5) Duplicates existing functionality.

## Tools & Resources

- **Product management:** Linear (primary), ProductBoard (roadmapping)
- **User feedback:** Canny, Sprig, User Interviews
- **Usage analytics:** PostHog, Amplitude
- **Competitive intelligence:** Crayon, Klue
- **Roadmap sharing:** Notion (internal), Canny (public roadmap)
- **Prioritization templates:** RICE scoring spreadsheet, KANO survey template
