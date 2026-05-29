# Section 08: Financial Projections

## Financial Model Overview

This section presents the 3-year financial projection for the AI Voice Agent SaaS platform. Projections are based on unit economics, market analysis, and comparable company benchmarks.

```
Revenue Growth Projection (36 Months)
    $6M ┤
        │                                   ┌── $5.0M
    $5M ┤                              ┌────┤
        │                              │    └── $4.2M
    $4M ┤                         ┌────┤
        │                         │    └── $3.4M
    $3M ┤                    ┌────┤
        │                    │    └── $2.6M
    $2M ┤               ┌────┤
        │               │    └── $1.8M
    $1M ┤          ┌────┤
        │          │    └── $1.0M
      $0 ┤─────────┤
        │         └── $0.3M
        └────────────────────────────────────►
          Q1  Q2  Q3  Q4  Q5  Q6  Q7  Q8  Q9  Q10 Q11 Q12
```

## Key Assumptions

| Assumption | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Free tier users | 5,000 | 15,000 | 40,000 |
| Starter customers | 200 | 800 | 2,500 |
| Pro customers | 50 | 300 | 1,200 |
| Business customers | 15 | 80 | 300 |
| Enterprise customers | 3 | 15 | 50 |
| Active users (DAU) | 500 | 3,000 | 10,000 |
| Monthly call minutes | 250K | 2.5M | 15M |
| Gross margin | 55% | 72% | 80% |
| Monthly churn (avg) | 8% | 5% | 3.5% |
| CAC blended | $180 | $250 | $300 |
| Headcount | 8 | 18 | 35 |

## Revenue Projections

### Year 1: Foundation Phase

| Quarter | Subscription | Usage | Marketplace | Services | Total MRR | Total ARR |
|---------|-------------|-------|-------------|----------|-----------|-----------|
| Q1 | $8K | $2K | $0 | $0 | $10K | $120K |
| Q2 | $18K | $7K | $0 | $5K | $30K | $360K |
| Q3 | $35K | $15K | $2K | $10K | $62K | $744K |
| Q4 | $60K | $25K | $5K | $15K | $105K | $1.26M |
| **Total** | **$121K** | **$49K** | **$7K** | **$30K** | | **$1.26M ARR** |

### Year 2: Growth Phase

| Quarter | Subscription | Usage | Marketplace | Services | Total MRR | Total ARR |
|---------|-------------|-------|-------------|----------|-----------|-----------|
| Q1 | $96K | $40K | $8K | $20K | $164K | $1.97M |
| Q2 | $146K | $60K | $12K | $25K | $243K | $2.92M |
| Q3 | $200K | $85K | $18K | $30K | $333K | $4.00M |
| Q4 | $260K | $110K | $25K | $35K | $430K | $5.16M |

### Year 3: Scale Phase

| Quarter | Subscription | Usage | Marketplace | Services | Total MRR | Total ARR |
|---------|-------------|-------|-------------|----------|-----------|-----------|
| Q1 | $330K | $140K | $32K | $40K | $542K | $6.50M |
| Q2 | $400K | $170K | $40K | $45K | $655K | $7.86M |
| Q3 | $475K | $200K | $48K | $50K | $773K | $9.28M |
| Q4 | $550K | $240K | $55K | $55K | $900K | $10.8M |

## Cost Structure

```
Cost Breakdown by Category (% of Revenue)
┌─────────────────────────────────────────────────────────────────────┐
│ Category          │ Year 1  │ Year 2  │ Year 3  │ Industry Avg     │
├─────────────────────────────────────────────────────────────────────┤
│ Infrastructure    │ 30%     │ 20%     │ 14%     │ 15-25%           │
│ R&D (Engineering) │ 50%     │ 35%     │ 28%     │ 20-30%           │
│ Sales & Marketing │ 25%     │ 30%     │ 28%     │ 30-40%           │
│ G&A               │ 15%     │ 12%     │ 10%     │ 10-15%           │
│ Total OpEx        │ 120%    │ 97%     │ 80%     │ 75-110%          │
└─────────────────────────────────────────────────────────────────────┘
```

## Financial Projection Data Model

```typescript
interface FinancialProjection {
  period: string;
  revenue: {
    subscription: number;
    usage: number;
    marketplace: number;
    services: number;
    total: number;
  };
  costs: {
    infrastructure: number;
    rd: number;
    salesMarketing: number;
    ga: number;
    total: number;
  };
  metrics: {
    grossMargin: number;
    ebitda: number;
    ebitdaMargin: number;
    burnRate: number;
    cashBalance: number;
    arr: number;
    mrr: number;
  };
}

function projectFinancials(
  startDate: Date,
  months: number,
  assumptions: Assumptions
): FinancialProjection[] {
  const projections: FinancialProjection[] = [];
  let cashBalance = assumptions.startingCapital;
  
  for (let month = 0; month < months; month++) {
    const period = formatPeriod(startDate, month);
    const revenue = calculateRevenue(month, assumptions);
    const costs = calculateCosts(month, revenue.total, assumptions);
    const ebitda = revenue.total - costs.total;
    cashBalance += ebitda;
    
    projections.push({
      period,
      revenue,
      costs,
      metrics: {
        grossMargin: revenue.total > 0 ? (revenue.total - costs.infrastructure) / revenue.total : 0,
        ebitda,
        ebitdaMargin: revenue.total > 0 ? ebitda / revenue.total : 0,
        burnRate: ebitda < 0 ? Math.abs(ebitda) : 0,
        cashBalance,
        arr: revenue.total * 12,
        mrr: revenue.total,
      },
    });
  }
  
  return projections;
}
```

## Cash Flow & Funding Requirements

```
Cash Flow Projection
┌─────────────────────────────────────────────────────────────────────────┐
│ Month  │ Revenue │ Costs   │ EBITDA   │ Cash Balance │ Notes           │
├─────────────────────────────────────────────────────────────────────────┤
│ 1      │ $2K     │ $45K    │ -$43K    │ $457K        │ Pre-revenue     │
│ 3      │ $8K     │ $55K    │ -$47K    │ $363K        │ MVP launch      │
│ 6      │ $25K    │ $70K    │ -$45K    │ $228K        │ Team growth     │
│ 9      │ $55K    │ $80K    │ -$25K    │ $153K        │ Paid traction   │
│ 12     │ $105K   │ $85K    │ $20K     │ $175K        │ Breakeven       │
│ 18     │ $200K   │ $130K   │ $70K     | $390K        │ Profitable      │
│ 24     │ $430K   │ $220K   │ $210K    │ $890K        │ Scaling         │
│ 36     │ $900K   │ $430K   │ $470K    │ $2.5M        │ Strong cash     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Funding requirement:** $500K initial seed needed to reach breakeven at Month 12. Projected runway: $500K seed + $0 revenue = 9 months. With conservative revenue, runway extends to 14+ months.

## Key Financial Targets

| Metric | Year 1 | Year 2 | Year 3 | Significance |
|--------|--------|--------|--------|-------------|
| ARR | $1.26M | $5.16M | $10.8M | Top-line growth |
| Gross margin | 55% | 72% | 80% | Infrastructure efficiency |
| EBITDA margin | -20% | +15% | +30% | Profitability path |
| Net revenue retention | 110% | 125% | 135% | Expansion efficiency |
| CAC payback (months) | 4.2 | 3.5 | 3.0 | Capital efficiency |
| LTV:CAC | 8:1 | 12:1 | 15:1 | Unit economics |
| Headcount | 8 | 18 | 35 | Team efficiency |
| Customers | 268 | 1,195 | 4,050 | Market adoption |

## Scenario Analysis

| Scenario | Year 3 ARR | Key Driver | Probability |
|----------|-----------|------------|-------------|
| Base case | $10.8M | Steady growth, 70% gross margin | 50% |
| Bull case | $18.5M | Viral community adoption, fast enterprise sales | 20% |
| Bear case | $5.2M | Slow adoption, pricing pressure, competition | 20% |
| Worst case | $2.1M | Big tech enters, funding winter | 10% |

## Unit Economic Sensitivity

```typescript
function sensitivityAnalysis(baseAssumptions: Assumptions): SensitivityResult {
  const scenarios = {
    churn: [-1%, -0.5%, 0%, +0.5%, +1%],
    pricing: [-20%, -10%, 0%, +10%, +20%],
    infrastructure: [-30%, -15%, 0%, +15%, +30%],
  };
  
  const results = {};
  
  for (const [variable, variations] of Object.entries(scenarios)) {
    results[variable] = variations.map(variation => {
      const adjusted = { ...baseAssumptions, [variable]: baseAssumptions[variable] * (1 + variation) };
      return {
        variation: variation * 100,
        year3ARR: projectYear3ARR(adjusted),
        breakevenMonth: findBreakeven(adjusted),
      };
    });
  }
  
  return results;
}
```

## Worst-Case Contingency Plan

If revenue falls 30% below projection: (1) Reduce marketing spend by 50%, (2) Freeze hiring (reduce from 35 to 25 target), (3) Pause non-critical features (marketplace, advanced analytics), (4) Negotiate better GPU/cloud pricing, (5) Raise bridge round if needed.

## Tools & Resources

- **Financial modeling:** Causal, Pigment, spreadsheet (Excel/Google Sheets)
- **Revenue tracking:** ChartMogul, ProfitWell, Stripe Dashboard
- **Expense tracking:** QuickBooks, Xero, Ramp
- **Budget management:** Float, Planful, Adaptive Insights
- **Board reporting:** Visible.vc, Witness, Pitch
- **Cap table:** Carta, Pulley, AngelList
