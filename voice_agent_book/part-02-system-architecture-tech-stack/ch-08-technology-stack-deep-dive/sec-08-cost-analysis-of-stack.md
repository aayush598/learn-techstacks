# Section 08: Cost Analysis of Stack

## Infrastructure Cost Breakdown

Monthly infrastructure costs are estimated per tier, showing that the open-source-first approach enables a fully functional SaaS platform at **$200-500/month for MVP scale**, scaling predictably as usage grows.

```
┌─────────────────────────────────────────────────────────────────────┐
│                  MONTHLY INFRASTRUCTURE COSTS                       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Component            MVP        Growth     Enterprise       │   │
│  │                       (100       (1K calls/  (10K calls/    │   │
│  │                       calls/d)   day)        day)            │   │
│  │  ─────────────────────────────────────────────────────────   │   │
│  │  Compute (K3s)         $50        $150        $500           │   │
│  │  GPU (Voice Infer.)    $100       $300        $1,000         │   │
│  │  PostgreSQL            $25        $75         $250           │   │
│  │  Redis                 $15        $30         $100           │   │
│  │  MinIO (Storage)       $10        $25         $100           │   │
│  │  ClickHouse            $0         $25         $100           │   │
│  │  Kafka                 $0         $25         $75            │   │
│  │  CDN (Static)          $5         $15         $50            │   │
│  │  API Costs (LLM)       $50        $200        $1,500         │   │
│  │  Monitoring (Self)     $0         $10         $25            │   │
│  │  Domain + Email        $10        $10         $10            │   │
│  │  ─────────────────────────────────────────────────────────   │   │
│  │  TOTAL                 $265       $865        $3,710         │   │
│  │  Open-Source Savings   80%        75%         70%            │   │
│  │  (vs proprietary stack)                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Comparison: Proprietary Stack Costs (Same Scale)                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Service          Proprietary         Monthly Cost           │   │
│  │  ────────────────────────────────────────────────────       │   │
│  │  STT              Deepgram             $0.06/min → $180     │   │
│  │  TTS              ElevenLabs           $0.30/min → $900     │   │
│  │  LLM              OpenAI GPT-4o        $2.50/1M tok → $400 │   │
│  │  Database          Supabase Pro         $125/mo              │   │
│  │  Object Store      AWS S3               $23/mo               │   │
│  │  Queue             AWS SQS              $10/mo               │   │
│  │  Auth              Clerk                $99/mo               │   │
│  │  Monitoring        Datadog              $150/mo              │   │
│  │  ────────────────────────────────────────────────────       │   │
│  │  TOTAL (1K calls/d)                   ~$1,887/mo            │   │
│  │  Our Stack (1K calls/d)               ~$865/mo  (54% less) │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Cost Calculation

```typescript
interface CostComponent {
  name: string;
  category: 'compute' | 'storage' | 'network' | 'api' | 'services';
  mvpMonthly: number;
  growthMonthly: number;
  enterpriseMonthly: number;
  pricingModel: string;
  scalingFactor: string;
}

const COST_BREAKDOWN: CostComponent[] = [
  {
    name: 'K3s Compute (3 nodes)',
    category: 'compute',
    mvpMonthly: 50,
    growthMonthly: 150,
    enterpriseMonthly: 500,
    pricingModel: 'Hetzner CX21 ($5/mo) → CAX31 ($15/mo) → CAX41 ($50/mo)',
    scalingFactor: 'Linear with nodes (3 → 6 → 15)',
  },
  {
    name: 'GPU Instance (Voice)',
    category: 'compute',
    mvpMonthly: 100,
    growthMonthly: 300,
    enterpriseMonthly: 1000,
    pricingModel: 'Hetzner GPU (A10G) ~$100/mo spot → reserved',
    scalingFactor: 'Per active call: 1 GPU per ~5 concurrent calls',
  },
  {
    name: 'PostgreSQL',
    category: 'storage',
    mvpMonthly: 25,
    growthMonthly: 75,
    enterpriseMonthly: 250,
    pricingModel: 'Self-hosted on CX21 → dedicated CX31 → cluster',
    scalingFactor: 'Storage: 10GB → 100GB → 1TB',
  },
  {
    name: 'LLM API Costs',
    category: 'api',
    mvpMonthly: 50,
    growthMonthly: 200,
    enterpriseMonthly: 1500,
    pricingModel: 'GPT-4o-mini $0.15/1M input, $0.60/1M output',
    scalingFactor: 'Per call: ~2K tokens input, ~500 output → $0.006/call',
  },
  {
    name: 'Object Storage (MinIO)',
    category: 'storage',
    mvpMonthly: 10,
    growthMonthly: 25,
    enterpriseMonthly: 100,
    pricingModel: 'NVMe storage $0.05/GB/mo, call recording ~1MB/min',
    scalingFactor: 'Per call: ~10MB recording → 10K calls = 100GB → $5',
  },
];

function estimateMonthlyCost(tier: 'mvp' | 'growth' | 'enterprise'): number {
  return COST_BREAKDOWN.reduce((sum, c) => sum + c[`${tier}Monthly`], 0);
}
```

## Voice Pipeline Cost per Call

```typescript
interface CallCostBreakdown {
  component: string;
  costPerMinute: number;
  notes: string;
}

const CALL_COST: CallCostBreakdown[] = [
  { component: 'STT (Whisper)', costPerMinute: 0.0003, notes: 'Self-hosted GPU, electricity only' },
  { component: 'LLM (GPT-4o-mini)', costPerMinute: 0.0020, notes: '~1500 tokens per minute of conversation' },
  { component: 'TTS (Coqui)', costPerMinute: 0.0005, notes: 'Self-hosted GPU, electricity only' },
  { component: 'Network/Egress', costPerMinute: 0.0001, notes: 'CDN egress at $0.01/GB' },
  { component: 'Storage', costPerMinute: 0.0005, notes: 'Recording + transcription at $0.05/GB/mo' },
  { component: 'Compute Overhead', costPerMinute: 0.0010, notes: 'K3s node allocation per call' },
  // Total: ~$0.0044/min or $0.26/hour
];

// Raw cost comparison
// Our stack:  $0.0044/min
// Deepgram:   $0.0059/min (STT only)
// ElevenLabs: $0.30/min   (TTS only)
// Twilio Voice: $0.014/min (carrier costs not included in either)
```

## Cost Optimization Strategies

```typescript
interface CostOptimization {
  strategy: string;
  savings: string;
  implementation: string;
  impact: 'low' | 'medium' | 'high';
}

const COST_OPTIMIZATIONS: CostOptimization[] = [
  {
    strategy: 'GPU Spot Instances',
    savings: '60-80% on GPU costs',
    implementation: 'Use preemptible/spot instances for Whisper + Coqui; graceful migration on preemption',
    impact: 'high',
  },
  {
    strategy: 'LLM Caching',
    savings: '30-50% on API costs',
    implementation: 'Cache frequent LLM responses (greetings, FAQs) with semantic similarity cache',
    impact: 'medium',
  },
  {
    strategy: 'Audio Compression',
    savings: '40-60% on storage',
    implementation: 'Store recordings as Opus (64kbps) instead of WAV; transcode on write',
    impact: 'high',
  },
  {
    strategy: 'Auto-scaling',
    savings: '30-50% on compute',
    implementation: 'KEDA-based scaling: 0 replicas during no-call hours, scale up on demand',
    impact: 'medium',
  },
  {
    strategy: 'Batch Processing',
    savings: '50% on non-real-time tasks',
    implementation: 'Batch transcription/analysis jobs every 30s instead of per-call processing',
    impact: 'low',
  },
];
```

## Projected Cost at Scale

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COST PROJECTION (12 MONTHS)                     │
│                                                                     │
│  Month │ Calls/Day  │ Monthly Cost │ Cost/Call    │ Notes          │
│  ──────┼────────────┼──────────────┼──────────────┼────────────────│
│   1    │    10      │   $200       │   $0.67      │ MVP launch     │
│   3    │    100     │   $265       │   $0.088     │ Paid tier open │
│   6    │    500     │   $500       │   $0.033     │ Growth phase   │
│   9    │   1,000    │   $865       │   $0.029     │ Stable growth  │
│  12    │   5,000    │   $2,100     │   $0.014     │ Scaling        │
│  18    │  10,000    │   $3,710     │   $0.012     │ Enterprise     │
│  24    │  50,000    │   $12,000    │   $0.008     │ Volume pricing │
│                                                                     │
│  Unit economics:                                                    │
│  Cost/call (avg 3 min): $0.088 (MVP) → $0.036 (scale)              │
│  Revenue/call (Pro tier): $0.50 (fixed) + $0.05/min                │
│  Gross margin: 82% (MVP) → 93% (scale)                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Hosting strategy | Self-hosted on Hetzner | 5-10x cheaper than AWS/GCP for equivalent specs |
| GPU strategy | Spot instances + fallback | 80% savings with proper interruption handling |
| LLM strategy | GPT-4o-mini default + caching | Best quality-to-cost ratio in 2026 |
| Storage strategy | MinIO + Opus compression | No egress fees, efficient storage |
| Monitoring strategy | Self-hosted Prometheus/Grafana | 90% of Datadog at 5% cost |

## Integration Points

- **Ch 08 (Tech Stack)** — Cost anchored to specific technology choices
- **Ch 08 (Open-Source vs Proprietary)** — Savings quantified for each swap
- **Ch 01 (System Architecture)** — Cost per architectural component

## Production Considerations

- **Cost Alerts**: Budget thresholds per component; email alert if > 80% of monthly budget
- **Anomaly Detection**: Usage anomaly detection flags unexpected cost spikes
- **Chargebacks**: Per-tenant cost tracking for Enterprise billing
- **Reserved Instances**: 1-year reservation for steady-state compute (30% discount)
- **Free Tier**: Free tier costs ~$50/month per tenant (10 calls/day) — subsidized by paid tiers
