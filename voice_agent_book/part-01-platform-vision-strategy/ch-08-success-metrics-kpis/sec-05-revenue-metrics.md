# Section 05: Revenue Metrics

## Revenue Dashboard

Revenue metrics provide visibility into business health, growth trajectory, and unit economics. These are reviewed daily (core metrics) and monthly (detailed).

```
Revenue Metrics Tree
┌─────────────────────────────────────────────────────────────────────────┐
│ MRR / ARR                 │  Revenue Growth Rate                      │
│ $105K / $1.26M (Month 12) │  15% MoM │  180% YoY                      │
├───────────────────────────┴───────────────────────────────────────────┤
│ ┌─────────────────────┐   ┌─────────────────────┐                    │
│ │ New Business MRR    │   │ Expansion MRR       │                    │
│ │ $8.5K/mo (new subs) │   │ $12.2K/mo (upgrades)│                    │
│ └─────────────────────┘   └─────────────────────┘                    │
│ ┌─────────────────────┐   ┌─────────────────────┐                    │
│ │ Churn MRR           │   │ Contraction MRR     │                    │
│ │ -$3.2K/mo (lost)    │   │ -$1.1K/mo (downgr.) │                    │
│ └─────────────────────┘   └─────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Revenue Metrics

### Top-Line Metrics
- **Monthly Recurring Revenue (MRR):** Sum of recurring subscription revenue
- **Annual Recurring Revenue (ARR):** MRR × 12
- **Net Revenue Retention (NRR):** (Starting MRR + Expansion - Churn - Contraction) / Starting MRR
- **Gross Revenue Retention (GRR):** (Starting MRR - Churn - Contraction) / Starting MRR

### Per-Customer Metrics
- **Average Revenue Per User (ARPU):** MRR / total customers
- **Average Revenue Per Account (ARPA):** MRR / total accounts
- **Lifetime Value (LTV):** Total revenue expected from a customer
- **Customer Acquisition Cost (CAC):** Total sales & marketing / new customers

### Growth Metrics
- **MoM Growth Rate:** (This month MRR - Last month MRR) / Last month MRR
- **Quick Ratio:** (New MRR + Expansion MRR) / (Churn MRR + Contraction MRR)
- **Rule of 40:** Revenue growth % + EBITDA margin % (target: >40%)

## Revenue Data Model

```typescript
interface RevenueMetrics {
  mrr: number;
  arr: number;
  growthRate: number; // MoM
  
  components: {
    newBusinessMRR: number;
    expansionMRR: number;
    churnMRR: number;
    contractionMRR: number;
    reactivationMRR: number;
  };
  
  perCustomer: {
    arpu: number;
    arpa: number;
    ltv: number;
    ltvCAC: number;
    cac: number;
  };
  
  retention: {
    netRevenueRetention: number;
    grossRevenueRetention: number;
    logoRetention: number; // customer count retention
  };
  
  byTier: Record<string, TierRevenue>;
}

function calculateRevenueHealth(metrics: RevenueMetrics): RevenueHealth {
  const quickRatio = (metrics.components.newBusinessMRR + metrics.components.expansionMRR) /
    Math.abs(metrics.components.churnMRR + metrics.components.contractionMRR);
  
  const nrr = metrics.retention.netRevenueRetention;
  const grr = metrics.retention.grossRevenueRetention;
  const growthRate = metrics.growthRate;
  
  return {
    quickRatio,
    isHealthy: quickRatio > 4 && nrr > 120 && grr > 90,
    score: (quickRatio * 10 + nrr + growthRate * 10) / 3,
    recommendations: [
      quickRatio < 2 ? 'Increase new business or reduce churn' : null,
      nrr < 120 ? 'Focus on expansion revenue' : null,
      growthRate < 10 ? 'Accelerate acquisition' : null,
    ].filter(Boolean),
  };
}
```

## Revenue by Tier

| Tier | Customers | MRR | ARPU | % of MRR | Churn (MoM) | NRR |
|------|-----------|-----|------|----------|-------------|-----|
| Free | 4,200 | $0 | $0 | 0% | N/A | N/A |
| Starter ($49) | 180 | $8,820 | $49 | 8.4% | 6% | 115% |
| Pro ($199) | 48 | $9,552 | $199 | 9.1% | 4% | 125% |
| Business ($499) | 14 | $6,986 | $499 | 6.7% | 3% | 135% |
| Enterprise (custom) | 3 | $15,000 | $5,000 | 14.3% | 0% | 150% |
| Usage overage | All | $15,642 | N/A | 14.9% | N/A | N/A |
| Marketplace | N/A | $5,000 | N/A | 4.8% | N/A | N/A |
| Services | N/A | $12,000 | N/A | 11.4% | N/A | N/A |
| **Total** | **4,445** | **$73,000** | **$16.42** | **100%** | **5.3%** | **122%** |

## Revenue Forecasting

```typescript
function forecastMRR(
  currentMRR: number,
  historicalData: MonthlyData[],
  assumptions: ForecastingAssumptions
): MRRForecast {
  const seasonality = detectSeasonality(historicalData);
  const growthTrend = calculateGrowthTrend(historicalData);
  
  const forecasts: MonthlyForecast[] = [];
  let projectedMRR = currentMRR;
  
  for (let month = 1; month <= 12; month++) {
    // New business
    const newMRR = assumptions.newCustomers * assumptions.newCustomerARPU;
    // Expansion from existing
    const expansionMRR = projectedMRR * assumptions.monthlyExpansionRate;
    // Churn
    const churnMRR = projectedMRR * assumptions.monthlyChurnRate;
    
    projectedMRR = projectedMRR + newMRR + expansionMRR - churnMRR;
    projectedMRR *= (1 + (seasonality[month % 12] || 0));
    
    forecasts.push({
      month,
      projectedMRR,
      newMRR,
      expansionMRR,
      churnMRR,
      netNewMRR: newMRR + expansionMRR - churnMRR,
    });
  }
  
  return {
    monthly: forecasts,
    yearEndARR: projectedMRR * 12,
    totalNewMRR: forecasts.reduce((s, f) => s + f.newMRR, 0),
    totalExpansionMRR: forecasts.reduce((s, f) => s + f.expansionMRR, 0),
    totalChurnMRR: forecasts.reduce((s, f) => s + f.churnMRR, 0),
    confidenceInterval: calculateConfidence(historicalData),
  };
}
```

## Weekly Revenue Dashboard

```
Revenue Dashboard (Week of May 25)
┌─────────────────────────────────────────────────────────────────────────┐
│ MRR: $73,000 (+14.2% MoM)   ARR: $876K   Target: $1.26M by M12       │
│                                                                         │
│ Net New MRR This Week: +$3,150                                          │
│  New: +$2,400 │ Expansion: +$1,800 │ Churn: -$950 │ Contraction: -$100  │
│                                                                         │
│ Growth Rate: 14.2% MoM   Quick Ratio: 4.2   NRR: 122%                 │
│                                                                         │
│ ARPU: $16.42/mo   LTV (avg): $1,470   CAC: $198   LTV/CAC: 7.4x       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Revenue Optimization Levers

| Lever | Impact | Complexity | Timeline |
|-------|--------|------------|----------|
| Pricing optimization | +8-15% MRR | Medium | 2-4 weeks |
| Annual billing incentive | +20% cash flow | Low | 1 week |
| Upgrade prompts (in-app) | +5-10% expansion | Low | 2 weeks |
| Usage-based overage | +10-20% from power users | Medium | 4 weeks |
| Marketplace commissions | +5% MRR | High | 8 weeks |
| Enterprise sales motion | +30% ACV | High | 12+ weeks |

## Tools & Resources

- **MRR tracking:** ChartMogul, ProfitWell, Baremetrics
- **Financial modeling:** Causal, Pigment, spreadsheet
- **Revenue recognition:** Stripe, QuickBooks, Xero
- **Forecasting:** Causal, spreadsheet with Monte Carlo simulation
- **Usage metering:** Stripe Metering, OpenMeter
- **Dunning:** Stripe automated dunning, Chargebee
- **Analytics:** PostHog (correlate usage with revenue)
