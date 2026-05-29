# Section 05: Unit Economics Analysis

## Unit Economics Framework

Understanding unit economics at the per-customer and per-call level is critical for pricing optimization, growth planning, and investor communication.

```
Unit Economics Waterfall
                    Revenue per Customer
                           │
                           ▼
                    ┌──────────────┐
                    │ Gross Revenue │
                    └──────┬───────┘
                           │
                    Cost of Revenue
                    ┌──────┴───────┐
                    │ Infrastructure│
                    │ (STT, TTS,   │
                    │  LLM, Hosting)│
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Gross Margin  │
                    └──────┬───────┘
                           │
                    Operating Costs
                    ┌──────┴───────┐
                    │ Sales &      │
                    │ Marketing     │
                    │ R&D           │
                    │ G&A           │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Contribution │
                    │ Margin       │
                    └──────────────┘
```

## Per-Call Unit Economics

### Cost Breakdown per Call (4-minute average)

| Component | Cost | % of Total | Notes |
|-----------|------|-----------|-------|
| STT (Whisper) | $0.004 | 12% | Self-hosted GPU, ~$0.001/min |
| TTS (Coqui) | $0.002 | 6% | Self-hosted GPU |
| LLM (Llama 3) | $0.008 | 24% | Self-hosted, 500 tokens avg |
| VAD (Silero) | $0.0001 | 0.3% | CPU inference, negligible |
| WebRTC/Telephony | $0.002 | 6% | Twilio/Telnyx termination |
| Infrastructure overhead | $0.004 | 12% | K8s, monitoring, logging |
| Storage (recording + transcript) | $0.002 | 6% | S3/Cloudflare R2 |
| **Total Cost** | **$0.022** | | **Self-hosted infrastructure** |
| Platform fee (Stripe, etc.) | $0.005 | 15% | Payment processing |
| **Total Cost + Fees** | **$0.027** | | |

### Revenue per Call

| Tier | Price/min | Avg Call (4min) | Gross Profit | Gross Margin |
|------|-----------|----------------|-------------|-------------|
| Free | $0.00 | $0.00 | -$0.027 | -∞% |
| Starter | $0.08 | $0.32 | $0.293 | 91.6% |
| Pro | $0.06 | $0.24 | $0.213 | 88.8% |
| Business | $0.04 | $0.16 | $0.133 | 83.1% |
| Enterprise | $0.03 | $0.12 | $0.093 | 77.5% |

**Note:** Free tier is a loss leader. Serves as acquisition cost. Target: <10% of total minutes on free.

## Customer-Level Unit Economics

```typescript
interface CustomerUnitEconomics {
  tier: string;
  averageMonthlyMinutes: number;
  averageRevenuePerMinute: number;
  mrr: number;
  grossMargin: number;
  cac: number;
  ltv: number;
  ltvCACRatio: number;
  paybackPeriodMonths: number;
  churnRate: number;
  netRevenueRetention: number;
}

const unitEconomicsByTier: CustomerUnitEconomics[] = [
  {
    tier: 'Starter',
    averageMonthlyMinutes: 800,
    averageRevenuePerMinute: 0.08,
    mrr: 49 + (800 * 0.08 > 1000 * 0.08 ? 0 : 0), // $49 base + potential overage
    grossMargin: 0.85,
    cac: 150,
    ltv: 1470, // $49/mo avg * 30mo avg lifetime
    ltvCACRatio: 9.8,
    paybackPeriodMonths: 3.1,
    churnRate: 0.06,
    netRevenueRetention: 1.15,
  },
  {
    tier: 'Pro',
    averageMonthlyMinutes: 6000,
    averageRevenuePerMinute: 0.06,
    mrr: 199,
    grossMargin: 0.82,
    cac: 400,
    ltv: 5970,
    ltvCACRatio: 14.9,
    paybackPeriodMonths: 2.0,
    churnRate: 0.04,
    netRevenueRetention: 1.25,
  },
  {
    tier: 'Business',
    averageMonthlyMinutes: 50000,
    averageRevenuePerMinute: 0.04,
    mrr: 499,
    grossMargin: 0.78,
    cac: 1200,
    ltv: 17964,
    ltvCACRatio: 15.0,
    paybackPeriodMonths: 2.4,
    churnRate: 0.03,
    netRevenueRetention: 1.35,
  },
];
```

## Key Unit Economics Targets

| Metric | Target | Industry Benchmark | Significance |
|--------|--------|-------------------|--------------|
| Gross margin | 70%+ | 60-80% (SaaS) | Higher = more efficient |
| CAC payback | <6 months | <12 months | Faster = capital efficient |
| LTV:CAC | >5x | >3x | Higher = profitable growth |
| Net revenue retention | >120% | >100% | Expansion > churn |
| Monthly churn | <5% | 3-7% | Lower = sticky product |
| Gross profit per call | >$0.10 | $0.05-0.15 | Per-unit profitability |

## CAC Analysis by Channel

```
Customer Acquisition Cost by Channel
┌────────────────────────────────────────────────────────────────────┐
│ Channel               │ CAC       │ Volume   │ Quality (Retention) │
├────────────────────────────────────────────────────────────────────┤
│ Organic (SEO, blog)   │ $50       │ 40% of total │ 85% @ 6mo       │
│ Direct (word of mouth)│ $75       │ 15% of total │ 90% @ 6mo       │
│ GitHub (open-source)  │ $100      │ 10% of total │ 88% @ 6mo       │
│ Google Ads            │ $200      │ 15% of total │ 75% @ 6mo       │
│ LinkedIn Ads          │ $350      │ 5% of total  │ 80% @ 6mo       │
│ Sales (outbound)      │ $2,000    │ 10% of total │ 95% @ 6mo       │
│ Partner referral      │ $500      │ 5% of total  │ 85% @ 6mo       │
└────────────────────────────────────────────────────────────────────┘
```

## LTV Calculation Model

```typescript
function calculateLTV(params: {
  monthlyRevenue: number;
  grossMargin: number;
  monthlyChurnRate: number;
  expansionRate: number; // monthly revenue expansion
  discountRate: number;
}): number {
  const retentionRate = 1 - params.monthlyChurnRate;
  const effectiveGrowth = 1 + params.expansionRate;
  const denominator = 1 + params.discountRate;
  
  // Sum of discounted future cash flows
  let ltv = 0;
  let currentRevenue = params.monthlyRevenue;
  
  for (let month = 0; month < 60; month++) { // 5 year horizon
    currentRevenue *= retentionRate * effectiveGrowth;
    const discountedRevenue = currentRevenue * Math.pow(denominator, -month);
    ltv += discountedRevenue * params.grossMargin;
  }
  
  return ltv;
}

// Typical LTV by tier (5-year horizon)
const ltvByTier = {
  starter: calculateLTV({ monthlyRevenue: 49, grossMargin: 0.85, monthlyChurnRate: 0.06, expansionRate: 0.02, discountRate: 0.10 }),
  pro: calculateLTV({ monthlyRevenue: 199, grossMargin: 0.82, monthlyChurnRate: 0.04, expansionRate: 0.03, discountRate: 0.10 }),
  business: calculateLTV({ monthlyRevenue: 499, grossMargin: 0.78, monthlyChurnRate: 0.03, expansionRate: 0.04, discountRate: 0.10 }),
};
```

## Path to Profitable Unit Economics

**Year 1:** Heavy investment in R&D and infrastructure. Per-call cost higher due to sub-scale GPU utilization. Target: Gross margin 55%. **Year 2:** Infrastructure optimization, GPU utilization improves, volume discounts on telephony. Target: Gross margin 70%. **Year 3:** Custom ASIC/inference optimization, telephony at-cost. Target: Gross margin 80%+.

## Infrastructure Cost Lessons

- GPU utilization optimization: Target >70% utilization (use spot instances + reserved mix)
- Model caching: Cache common LLM responses (hit rate >50% for Tier 1 queries)
- Batch processing: Batch transcription where real-time not needed
- Storage tiering: Hot (30 days) → Warm (90 days) → Cold (365 days) → Archive
- CDN for voice files: CloudFront for frequently accessed recordings

## Tools & Resources

- **Unit economics tracking:** ChartMogul, ProfitWell
- **Infrastructure cost monitoring:** Vantage, CloudHealth, Grafana + AWS Cost Explorer
- **GPU cost optimization:** Lambda Cloud, Vast.ai, RunPod
- **Financial modeling:** Causal, Pigment, spreadsheet
- **Analytics:** PostHog, Amplitude (track usage events for cost attribution)
