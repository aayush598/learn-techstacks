# Section 06: Open-Source vs Proprietary Trade-offs

## Decision Framework

Every technology decision follows a **build-vs-buy framework** that evaluates total cost of ownership, team expertise, time to market, and long-term maintainability. The platform strongly favors open-source with permissive licenses, reserving proprietary services only when they provide clear and significant advantage.

```
┌─────────────────────────────────────────────────────────────────────┐
│               BUILD vs BUY DECISION FRAMEWORK                      │
│                                                                     │
│  Question                                                           │
│  Is there a mature open-source alternative?                        │
│  ├── YES ───→ Does it meet 80% of requirements?                   │
│  │           ├── YES ───→ Use open-source                         │
│  │           └── NO  ───→ Can we contribute the missing 20%?      │
│  │                       ├── YES ───→ Fork/Contribute + use       │
│  │                       └── NO  ───→ Evaluate proprietary        │
│  │                                                                 │
│  └── NO ───→ Is there a proprietary service that saves 6+ mo?    │
│              ├── YES ───→ Use proprietary (with exit plan)        │
│              └── NO  ───→ Build in-house                          │
│                                                                     │
│                                                                     │
│  Example: Database                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Need: Relational database with vector search                │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │   │
│  │  │  PostgreSQL 16 │  │  Pinecone      │  │  Supabase      │ │   │
│  │  │  + pgvector    │  │  (Proprietary) │  │  (Hosted PG)   │ │   │
│  │  │  (Open Source) │  │                │  │                │ │   │
│  │  ├────────────────┤  ├────────────────┤  ├────────────────┤ │   │
│  │  │  Cost: Free    │  │  Cost: $70/mo  │  │  Cost: $25/mo │ │   │
│  │  │  Ops: Self     │  │  Ops: Managed  │  │  Ops: Managed  │ │   │
│  │  │  Maturity: 30+ │  │  Vector-only   │  │  PG + vector   │ │   │
│  │  │       years    │  │                │  │                │ │   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │   │
│  │  Decision: PostgreSQL 16 + pgvector (meets 95% of needs)    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Technology Trade-off Matrix

| Need | Open-Source Option | Proprietary Option | Decision | Rationale |
|------|-------------------|-------------------|----------|-----------|
| **STT** | Whisper (faster-whisper) | Deepgram, Azure Speech | Whisper | Best accuracy, self-hosted GPU, no per-minute cost |
| **TTS** | Coqui XTTS v2 | ElevenLabs, Azure TTS | Coqui XTTS | Voice cloning, no usage costs, 17 languages |
| **VAD** | Silero VAD | Google VAD, WebRTC VAD | Silero VAD | ONNX runtime, real-time, 1MB model |
| **LLM** | Llama 3 / Mistral | OpenAI GPT-4, Claude 3 | GPT-4o-mini (hybrid) | Best performance/cost; Llama for sensitive data |
| **Object Storage** | MinIO | AWS S3, GCS | MinIO | S3 API compatible, self-hosted, no egress fees |
| **Queue** | BullMQ (Redis) | Amazon SQS, GCP Pub/Sub | BullMQ | Simpler stack, no extra infra, Redis already present |
| **Monitoring** | Prometheus + Grafana | Datadog, New Relic | Prometheus + Grafana | 10-20x cost savings, self-hosted option |
| **Auth** | Auth.js (NextAuth) | Clerk, Auth0 | Auth.js | Open-source, self-hosted, no per-user pricing |
| **Search** | PostgreSQL FTS + pgvector | Algolia, Meilisearch | pgvector | No extra infra, good enough for MVP |
| **CI/CD** | GitHub Actions + ArgoCD | CircleCI, GitLab | GitHub Actions | Co-located with code, generous free tier |

## Build vs Buy Examples

```typescript
// Hybrid approach: LLM with fallback
interface AIModelProvider {
  name: string;
  type: 'open-source' | 'proprietary';
  models: string[];
  costPerToken: number;
  latencyP50: number;
  supportedFeatures: string[];
}

const AI_PROVIDERS: AIModelProvider[] = [
  {
    name: 'OpenAI',
    type: 'proprietary',
    models: ['gpt-4o', 'gpt-4o-mini'],
    costPerToken: 0.0000025,  // $2.50/1M input tokens
    latencyP50: 500,           // ms
    supportedFeatures: ['streaming', 'tool_calling', 'json_mode', 'vision'],
  },
  {
    name: 'Local Llama',
    type: 'open-source',
    models: ['llama-3.1-8b', 'llama-3.1-70b'],
    costPerToken: 0.0000001,  // ~$0.10/1M tokens (electricity + GPU)
    latencyP50: 800,           // ms (GPU inference)
    supportedFeatures: ['streaming', 'tool_calling', 'json_mode'],
  },
];

// Routing logic: Use local model for sensitive data, GPT for complex tasks
function selectModel(input: { content: string; tenantTier: string }): string {
  if (containsPII(input.content)) {
    return 'llama-3.1-70b'; // Self-hosted for data privacy
  }
  if (input.tenantTier === 'enterprise') {
    return 'gpt-4o'; // Best quality for premium
  }
  return 'gpt-4o-mini'; // Cost-efficient default
}
```

## Open-Source Contribution Strategy

```typescript
// When an OSS project lacks a critical feature, we:
// 1. Evaluate contribution effort vs internal fork maintenance
// 2. Contribute upstream when possible
// 3. Maintain minimal internal patch set when not

interface OSSContribution {
  project: string;
  feature: string;
  effort: 'small' | 'medium' | 'large';
  upstreamMerged: boolean;
  internalPatch: string; // Path to patch file

  // Decision logic
  get strategy(): 'contribute' | 'fork' | 'workaround' {
    if (this.effort === 'small' || (this.effort === 'medium' && this.upstreamMerged)) {
      return 'contribute';
    }
    if (this.effort === 'large' && !this.upstreamMerged) {
      return 'workaround'; // Find alternative approach
    }
    return 'fork'; // Maintain internal patch temporarily
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Overall strategy | Open-source first | Lower cost, no vendor lock-in, community support |
| LLM approach | Hybrid (GPT-4 + Llama) | GPT for quality, Llama for sensitive/cost-sensitive |
| Database | PostgreSQL + pgvector | Single DB for relational + vector — simpler ops |
| Monitoring | Prometheus + Grafana | 90% of Datadog features at 5% of cost |
| Build-vs-buy threshold | If proprietary saves 6+ months of dev, buy | Pragmatic time-to-market consideration |

## Integration Points

- **Ch 08 (License Compatibility)** — OSS license review for each dependency
- **Ch 08 (Cost Analysis)** — Cost comparison tables for open-source vs proprietary
- **Ch 10 (Supply Chain Security)** — Dependency scanning for OSS components

## Production Considerations

- **Vendor Exit Plan**: Every proprietary service has a documented migration path to open-source alternative
- **Cost Ceiling**: Proprietary service costs capped at 20% of monthly infrastructure budget
- **OSS Maintenance**: Key dependencies monitored for activity; 3 maintainers per critical project
- **Security Patches**: Automated Dependabot + Renovate for OSS dependency updates
- **Community Engagement**: Active contribution to PostgreSQL, Whisper, LangChain ecosystem
