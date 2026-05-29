# Section 02: Phase 1 — Foundation (Months 1-3)

## Phase Overview

Phase 1 establishes the technical foundation and delivers the MVP. The goal is to build a working voice AI platform, validate with design partners, and prepare for multi-tenant architecture.

```
Phase 1 Timeline
Month 1                       Month 2                       Month 3
┌─────────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Week 1-2: Setup & Pipeline │ Week 3-4: Agent Builder    │ Week 5-6: Dashboard        │
│ ────────────────────────── │ ──────────────────────────  │ ──────────────────────────  │
│ • Repo, CI/CD, infra       │ • Agent config form         │ • Call log view            │
│ • Whisper deployment       │ • Basic prompt editor       │ • Basic metrics            │
│ • Coqui deployment         │ • Voice selection           │ • Filtering & search       │
│ • LangChain integration    │ • Agent create/deploy       │ • Recording playback       │
├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Week 7-8: Telephony       │ Week 9-10: Outbound + SMS  │ Week 11-12: Launch         │
│ ────────────────────────── │ ──────────────────────────  │ ──────────────────────────  │
│ • Twilio inbound           │ • Outbound call support     │ • Auth (Clerk)             │
│ • WebRTC/telephony stream  │ • SMS fallback             │ • Team management          │
│ • Call routing             │ • Contact list mgmt         │ • Billing (Stripe)         │
│ • Basic IVR (DTMF)         │                             │ • Docs + quickstart        │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

## Key Deliverables

### Month 1: Core Pipeline
- **Voice pipeline:** STT (Whisper) → LLM (GPT-4 + Llama) → TTS (Coqui XTTS) running end-to-end
- **API skeleton:** REST API for agent creation, call management, user authentication
- **Infrastructure:** Kubernetes cluster with GPU node pool, CI/CD pipeline, monitoring stack
- **Decision:** Use Whisper large for accuracy, Coqui XTTS for voice quality, GPT-4 for intelligence

### Month 2: Agent Builder + Dashboard
- **Agent builder:** Simple web form to configure agent name, system prompt, voice, language
- **Dashboard:** Call log with timestamp, duration, transcript, recording
- **Basic metrics:** Total calls, average duration, success rate, minutes used

### Month 3: Telephony + Launch Prep
- **Inbound calling:** Twilio SIP trunk → WebRTC → voice pipeline
- **Outbound calling:** API-initiated outbound calls
- **SMS fallback:** Text-based conversation when voice not available
- **Authentication:** Email/password + Google OAuth via Clerk
- **Team management:** Basic invitation system
- **Billing:** Stripe integration for subscription management
- **Design partner program:** 50 early users for feedback

## Phase 1 Technical Decisions

| Decision | Option | Chosen | Rationale |
|----------|--------|--------|-----------|
| STT Model | Whisper, DeepSpeech, Custom | Whisper large | Best accuracy, MIT license |
| TTS Model | Coqui, ElevenLabs, PlayAI | Coqui XTTS | Voice cloning, self-hosted |
| LLM | GPT-4, Claude, Llama 3 | GPT-4 primary + Llama fallback | Best quality, fallback for cost |
| Telephony | Twilio, Telnyx, SignalWire | Twilio | Best DX, global coverage |
| Framework | Next.js, Remix, SvelteKit | Next.js | Good balance of SSR/API |
| Auth | Clerk, Auth0, Supabase Auth | Clerk | Good DX, pre-built components |
| Payments | Stripe, Paddle, LemonSqueezy | Stripe | Standard, flexible |
| Database | PostgreSQL, MySQL, SQLite | PostgreSQL | Reliability, features |
| Queue | BullMQ, Sidekiq, Celery | BullMQ (Redis) | Node.js native, reliable |

## Infrastructure Setup

```typescript
interface Phase1Infrastructure {
  compute: {
    orchestration: 'kubernetes';
    gpuNodes: 'g4dn.xlarge' | 'g5.xlarge'; // NVIDIA T4 GPU
    cpuNodes: 't3.medium' | 't3.large';
    autoScaling: true;
    minNodes: 2;
    maxNodes: 10;
  };
  storage: {
    recordings: 's3' | 'cloudflare-r2';
    database: 'rds-postgresql' | 'aurora';
    cache: 'elasticache-redis';
    vector: 'qdrant' | 'pinecone'; // For future RAG
  };
  networking: {
    cdn: 'cloudfront' | 'cloudflare';
    dns: 'route53' | 'cloudflare';
    waf: 'cloudflare' | 'aws-waf';
  };
  monitoring: {
    logs: 'grafana-loki' | 'datadog';
    metrics: 'prometheus' | 'datadog';
    errors: 'sentry';
    uptime: 'betterstack' | 'checkly';
    apm: 'datadog' | 'grafana-tempo';
  };
}
```

## Phase 1 Team

| Role | Count | Notes |
|------|-------|-------|
| Full-stack engineer | 2 | Dashboard, API, infrastructure |
| ML/voice engineer | 1 | Voice pipeline optimization |
| Product manager | 1 | Requirements, design partners |
| Designer | 0.5 | UI/UX (contract) |
| DevOps | 0.5 | Shared with other projects |

## Phase 1 Budget

| Category | Estimated Cost |
|----------|---------------|
| Cloud infrastructure | $3K-5K/month |
| GPU compute | $2K-3K/month |
| SaaS (Clerk, Twilio, Sentry) | $1K-2K/month |
| Compensation (4 FTE) | $60K-80K/month |
| Contractors | $5K-10K/month |
| **Total Phase 1** | **~$210K-300K** |

## Phase 1 Exit Criteria

- [ ] End-to-end call pipeline working (STT → LLM → TTS) with <2s latency
- [ ] 50 design partners actively using platform
- [ ] 10K+ call minutes processed
- [ ] Call success rate >95%
- [ ] Uptime >99.5%
- [ ] Onboarding completion >60%
- [ ] NPS score >30
- [ ] All critical bugs resolved
- [ ] Documentation published
- [ ] Open-source repository public

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| GPU cost overrun | High | 40% | Use spot instances, model quantization |
| Voice quality below expectations | High | 30% | Early user testing, fallback to ElevenLabs |
| Pipeline latency too high | High | 30% | Streaming STT, response caching |
| Telephony integration issues | Medium | 20% | Twilio support plan, WebRTC fallback |
| Design partner churn | Medium | 40% | Over-provision design partners (target 50, enroll 80) |

## Tools & Resources

- **Infrastructure as code:** Terraform, Pulumi
- **CI/CD:** GitHub Actions, Docker
- **Monitor stack:** Grafana + Prometheus + Loki + Tempo
- **Error tracking:** Sentry
- **User feedback:** Canny, Sprig, Intercom
- **Documentation:** Nextra, Docusaurus
- **Design:** Figma (component library setup)
