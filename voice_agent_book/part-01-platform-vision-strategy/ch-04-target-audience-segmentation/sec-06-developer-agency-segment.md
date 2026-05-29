# Section 06: Developer & Agency Segment

## Developer Segment

Developers are the technical influencers and builders who evaluate, integrate, and advocate for our platform. They may not have direct budget authority but their recommendation strongly influences purchasing decisions.

```
Developer Persona Spectrum
┌─────────────────────────────────────────────────────────────────────────┐
│ Independent Dev          Internal Tools Dev        Agency Dev          │
│ (Freelancer, builder)    (SaaS company builder)    (Client projects)   │
├─────────────────────────────────────────────────────────────────────────┤
│ • Side projects          • Building voice UI       • Client voice apps │
│ • API explorer           • Product integration     • White-label depl. │
│ • Open-source contrib.   • Internal automation     • Resell platform   │
│                          • POC evaluation          • Custom solutions  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Developer Motivations & Needs

**What developers want:** Clean API, excellent documentation, open-source access, TypeScript SDK, self-hosted option, reasonable rate limits on free tier.

**What they hate:** Closed platforms, opaque pricing, missing docs, breaking changes, vendor lock-in, capped rate limits without clarity.

**Open source motivation:** 68% of developers say open-source availability significantly influences their platform choice. Our MIT-licensed core gives us a decisive advantage over all closed-source competitors.

## Developer API Design

```typescript
// Developer-Facing SDK (TypeScript example)
import { VoiceAgent, VoiceConfig } from '@ourplatform/node-sdk';

const agent = new VoiceAgent({
  apiKey: process.env.OUR_API_KEY,
  environment: 'production', // or 'sandbox'
});

// Create a voice agent
const config: VoiceConfig = {
  name: 'Support Agent',
  language: 'en-US',
  voice: {
    provider: 'coqui', // or 'elevenlabs', 'azure'
    voiceId: 'female-1',
    speed: 1.0,
  },
  llm: {
    provider: 'openai', // or 'anthropic', 'llama', 'custom'
    model: 'gpt-4',
    systemPrompt: 'You are a helpful customer support agent...',
    temperature: 0.7,
  },
  stt: {
    provider: 'whisper',
    model: 'large-v3',
  },
  endpoints: [
    {
      phoneNumber: '+15551234567',
      inbound: true,
      outbound: false,
    },
  ],
};

const deployed = await agent.deploy(config);
console.log(`Agent deployed: ${deployed.id}`);

// Make an outbound call
const call = await agent.call({
  to: '+15559876543',
  context: {
    customerName: 'Jane Doe',
    accountId: 'ACC-12345',
  },
});

call.on('transcript', (text: string) => {
  console.log(`Transcript: ${text}`);
});

call.on('completed', (result: CallResult) => {
  console.log(`Outcome: ${result.outcome}`);
  console.log(`Duration: ${result.durationSeconds}s`);
});
```

## Agency Segment

Agencies are a high-value channel partner. They implement, customize, and manage voice AI solutions for their clients. White-label capability is the key differentiator for this segment.

```
Agency Segment Breakdown
┌──────────────────────────────────────────────────────────────────────────┐
│ Agency Type        │ Size  │ Client Count │ White-Label Need │ Revenue   │
├──────────────────────────────────────────────────────────────────────────┤
│ Digital agency     │ 5-50  │ 10-100       │ High             │ $5-50K/mo │
│ Dev shop           │ 2-20  │ 5-30         │ Medium           │ $2-20K/mo │
│ Contact center VAR │ 10-200│ 20-500       │ High             │ $20-500K/mo│
│ Telecom consultant │ 5-100 │ 10-200       │ Very High        │ $10-100K/mo│
│ Specialist (e.g.,  │ 2-10  │ 5-20         │ Medium           │ $5-10K/mo  │
│ healthcare IT)     │       │              │                  │            │
└──────────────────────────────────────────────────────────────────────────┘
```

## Agency Value Proposition

**For agencies:** (1) White-label platform under your brand, (2) 40%+ margins on resale, (3) Sub-account management for client deployments, (4) Agency portal with consolidated billing, (5) Marketplace to showcase your templates/voices, (6) Faster delivery than building from scratch.

## Agency Partnership Model

```typescript
interface AgencyPartner {
  id: string;
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  whiteLabelEnabled: boolean;
  subAccounts: number;
  
  economics: {
    wholesalePrice: number; // per minute rate
    retailPrice: number; // recommended retail
    margin: number;
    monthlyMinimum: number;
    revenueShare: number; // platform commission from marketplace sales
  };
  
  support: {
    dedicatedContact: boolean;
    responseTime: number; // hours
    onboardingSupport: 'self-serve' | 'guided' | 'white-glove';
  };
}

function calculateAgencyMargins(partner: AgencyPartner, monthlyMinutes: number): AgencyPayout {
  const wholesale = monthlyMinutes * partner.economics.wholesalePrice;
  const retail = monthlyMinutes * partner.economics.retailPrice;
  const monthlyFee = partner.economics.monthlyMinimum;
  
  return {
    wholesaleCost: wholesale + monthlyFee,
    retailRevenue: retail,
    grossProfit: retail - wholesale - monthlyFee,
    grossMargin: (retail - wholesale - monthlyFee) / retail,
    payoutToAgency: retail - (wholesale + monthlyFee),
    platformRevenue: wholesale + monthlyFee,
  };
}
```

## Developer & Agency Acquisition

**Developer acquisition:** (1) GitHub presence (open-source repos, active issues/PRs), (2) Hacker News launches, (3) Technical blog posts on dev.to, Medium, (4) Discord community, (5) Conference talks (TwilioCon, DevRel events).

**Agency acquisition:** (1) Partner program (tiered benefits), (2) Industry events (IT Expo, Contact Center shows), (3) Marketplace listings, (4) Referral program, (5) Content targeting agency decision-makers.

## Developer Community Building

```
Community Engagement Funnel
GitHub Star → Clone → Build POC → Share Feedback → GitHub Issue/PR → Become Contributor → Advocate
    │           │          │            │               │                   │              │
    ▼           ▼          ▼            ▼               ▼                   ▼              ▼
  Discover   Try       Build      Engage        Contribute           Deep              Refer
             Locally   Locally    Online        Code                 Involvement
```

## Open Source Governance

**Repository structure:** Monorepo with packages for core engine, SDK, CLI, dashboard, agent builder. **License:** MIT (core), polyform (enterprise add-ons). **CLA:** Standard Apache CLA for contributions. **Governance:** Core team (company) + community maintainers. **RFC process:** RFCs for significant changes.

## Developer & Agency KPIs

| Metric | Year 1 Target | Year 2 Target | Year 3 Target |
|--------|--------------|--------------|--------------|
| GitHub stars | 5K | 20K | 50K |
| Community contributors | 50 | 500 | 2K |
| Discord members | 1K | 5K | 15K |
| Agency partners | 20 | 100 | 500 |
| Agency-sourced revenue | $5K/mo | $50K/mo | $250K/mo |
| White-label deployments | 10 | 200 | 1K |
| SDK downloads (npm) | 10K/mo | 100K/mo | 500K/mo |

## Tools & Resources

- **Developer relations:** Orbit.love (community analytics), Common Room
- **API documentation:** Docusaurus, Nextra, Mintlify
- **SDK generation:** Fern, OpenAPI Generator, Speakeasy
- **Agency management:** PartnerStack, Impact, Crossbeam
- **Discord community:** Discord, Discourse, GitHub Discussions
- **Open-source program:** TODO Group guidelines, Linux Foundation best practices
