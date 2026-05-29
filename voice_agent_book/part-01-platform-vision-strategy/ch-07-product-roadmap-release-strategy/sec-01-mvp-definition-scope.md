# Section 01: MVP Definition & Scope

## MVP Philosophy

Our MVP is the smallest possible product that delivers core value to early adopters. It focuses on the essential voice agent pipeline (STT → AI → TTS) with the minimum features needed for a production-grade experience.

```
MVP Scope Definition
┌─────────────────────────────────────────────────────────────────────────┐
│ MUST HAVE (Core Pipeline)                                              │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │ Inbound Call │  │ STT → AI     │  │ Outbound     │                │
│ │ Handling     │  │ → TTS        │  │ Call Support │                │
│ └──────────────┘  └──────────────┘  └──────────────┘                │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │ Basic Agent  │  │ Simple       │  │ Call         │                │
│ │ Builder      │  │ Dashboard    │  │ Recording    │                │
│ └──────────────┘  └──────────────┘  └──────────────┘                │
├─────────────────────────────────────────────────────────────────────────┤
│ SHOULD HAVE (Enhance Experience)                                       │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │ SMS         │  │ Team         │  │ Usage        │                │
│ │ Capability  │  │ Management   │  │ Analytics    │                │
│ └──────────────┘  └──────────────┘  └──────────────┘                │
├─────────────────────────────────────────────────────────────────────────┤
│ COULD HAVE (Delighters)                                                │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│ │ Custom Voices │  │ Sentiment    │  │ Template     │                │
│ │              │  │ Analysis     │  │ Library      │                │
│ └──────────────┘  └──────────────┘  └──────────────┘                │
├─────────────────────────────────────────────────────────────────────────┤
│ WON'T HAVE (Post-MVP)                                                  │
│ Multi-tenant, white-label, marketplace, advanced analytics,           │
│ custom integrations, SSO, self-hosting, compliance certs               │
└─────────────────────────────────────────────────────────────────────────┘
```

## MVP Feature Details

### Core Pipeline (Must Have)
- **Inbound call handling:** Receive incoming calls via Twilio/Telnyx, route to AI agent
- **STT → AI → TTS pipeline:** Whisper STT → LangChain/LLM orchestration → Coqui TTS
- **Outbound call support:** Initiate calls from platform, AI agent handles conversation
- **Basic agent builder:** Configure prompt, voice, language via simple form (UI or API)
- **Simple dashboard:** Call log, basic metrics (volume, duration, success rate)
- **Call recording:** Store recordings + transcripts in S3-compatible storage

### Enhanced Experience (Should Have)
- **SMS fallback:** When voice not possible (low signal, declined), switch to SMS
- **Team management:** Invite team members, basic role assignment
- **Usage analytics:** Minutes used, cost tracking, basic trends

## MVP Timeline (3 Months)

```
Week 1-4:   Foundation
  ┌────────────────────────────────────────────────────────────────┐
  │ • Repository setup, CI/CD, development environment            │
  │ • Core voice pipeline (Whisper → Coqui → basic LLM)          │
  │ • Basic telephony integration (Twilio)                        │
  └────────────────────────────────────────────────────────────────┘
Week 5-8:   Core Features
  ┌────────────────────────────────────────────────────────────────┐
  │ • Agent builder (basic form-based)                            │
  │ • Simple dashboard with call log                              │
  │ • Call recording + transcript storage                         │
  │ • Outbound call support                                       │
  └────────────────────────────────────────────────────────────────┘
Week 9-12:  Polish & Launch
  ┌────────────────────────────────────────────────────────────────┐
  │ • Auth (email/password + Google OAuth)                        │
  │ • Team management (basic)                                     │
  │ • Usage tracking + analytics                                  │
  │ • Billing integration (Stripe)                                │
  │ • Documentation + quickstart guide                            │
  │ • Beta launch to 50 design partners                           │
  └────────────────────────────────────────────────────────────────┘
```

## MVP Success Criteria

```typescript
interface MVPSuccessCriteria {
  technical: {
    callSuccessRate: number; // Target: >95%
    avgLatencyMs: number; // Target: <2000ms (end-to-end)
    uptimePercent: number; // Target: >99.5%
    maxConcurrentCalls: number; // Target: 50
    transcriptAccuracy: number; // Target: >92%
  };
  user: {
    timeToFirstCall: number; // Target: <10 minutes
    onboardingCompletion: number; // Target: >60%
    npsScore: number; // Target: >30
  };
  business: {
    designPartnerCount: number; // Target: 50
    weeklyActiveUsers: number; // Target: 100
    userFeedbackCollected: number; // Target: 200+ responses
    minutesProcessed: number; // Target: 10,000+ minutes
  };
}

function evaluateMVPReadiness(criteria: MVPSuccessCriteria): MVPReadiness {
  const technicalPass = criteria.technical.callSuccessRate > 0.95 &&
    criteria.technical.avgLatencyMs < 2000 &&
    criteria.technical.uptimePercent > 99.5;
  
  const userPass = criteria.user.timeToFirstCall < 10 &&
    criteria.user.onboardingCompletion > 0.6;
  
  return {
    readyForProduction: technicalPass && userPass,
    technicalReadiness: technicalPass,
    userReadiness: userPass,
    businessReadiness: criteria.business.designPartnerCount >= 50,
    gaps: [],
    recommendations: [],
  };
}
```

## MVP Exclusions (Explicitly Not Included)

- Multi-tenant architecture (single tenant MVP, multi-tenant is Phase 2)
- White-label (Phase 4)
- Marketplace (Phase 4)
- Advanced analytics (Phase 2)
- Compliance certifications (SOC 2 starts in Phase 1 but cert in Phase 2)
- Self-hosting (Phase 3)
- Custom integrations (Phase 2)
- SSO/SAML (Phase 5)
- Advanced IVR (Phase 2)
- Voice cloning (Phase 2)
- Sentiment analysis (Phase 2)
- RAG/knowledge base (Phase 2)

## MVP Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MVP System Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│ Client Layer                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────────────┐  │
│  │ Web Dashboard │  │ API Client   │  │ Phone (PSTN/VoIP)          │  │
│  └──────────────┘  └──────────────┘  └─────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│ Service Layer                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │ Voice        │  │ Agent        │  │ Dashboard    │               │  │
│  │ Service      │  │ Service      │  │ Service      │               │  │
│  │ (Twilio)     │  │ (LangChain)  │  │ (Next.js)    │               │  │
│  └──────────────┘  └──────────────┘  └──────────────┘               │  │
├─────────────────────────────────────────────────────────────────────────┤
│ AI Layer (GPU-backed)                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │ Whisper (STT)│  │ LLM        │  │ Coqui (TTS)  │               │  │
│  └──────────────┘  └──────────────┘  └──────────────┘               │  │
├─────────────────────────────────────────────────────────────────────────┤
│ Data Layer                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │ PostgreSQL   │  │ Redis        │  │ S3 (Records) │               │  │
│  └──────────────┘  └──────────────┘  └──────────────┘               │  │
└─────────────────────────────────────────────────────────────────────────┘
```

## MVP Team

| Role | Count | Primary Responsibility |
|------|-------|----------------------|
| Full-stack engineer | 2 | Dashboard, API, infrastructure |
| ML/AI engineer | 1 | Voice pipeline (STT, LLM, TTS) |
| Product manager | 1 | Requirements, prioritization, design partner management |
| Designer | 1 (contract) | UI/UX for dashboard and agent builder |
| DevOps | 1 (shared) | Infrastructure, CI/CD, monitoring |

## MVP Build vs. Buy Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| STT (Whisper) | Build (self-host) | Best accuracy, saves 80% vs API costs |
| TTS (Coqui) | Build (self-host) | Voice cloning capability, cost savings |
| LLM | Buy (API) + Local | GPT-4 for accuracy, Llama for cost-sensitive |
| Telephony (Twilio) | Buy | $0.014/min, best developer experience |
| Auth (Clerk) | Buy | Faster than building, but custom lock-in risk |
| Payments (Stripe) | Buy | Industry standard, PCI compliant |
| Queue (Redis/Bull) | Build (OSS) | Deferred jobs for post-call processing |
| Storage (S3) | Buy | Durable, cheap, scalable |

## Tools & Resources

- **Project management:** Linear, Notion
- **Design:** Figma (design system started in MVP)
- **Documentation:** Nextra, Docusaurus
- **CI/CD:** GitHub Actions, Vercel (frontend), Railway/Render (backend)
- **Monitoring:** Sentry (errors), Grafana (metrics), BetterStack (uptime)
- **User feedback:** Sprig, Canny, Intercom
