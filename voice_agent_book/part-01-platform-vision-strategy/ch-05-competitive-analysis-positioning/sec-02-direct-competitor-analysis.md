# Section 02: Direct Competitor Analysis

## Competitor Deep Dives

This section provides detailed analysis of the 6 primary direct competitors in the pure-play voice AI space.

## Retell AI

**Overview:** Retell AI is the current market leader in enterprise voice AI. Founded 2022, HQ San Francisco. $75M raised (Series B). 10,000+ customers, $30M+ ARR. 120+ employees.

**Product:** Full-stack voice AI platform with custom fine-tuned ASR, LLM orchestration, and TTS. Emphasis on accuracy (claims 98% word error rate on noisy calls). Enterprise-focused with SOC 2, HIPAA compliance.

**Pricing:** No free tier. Usage-based: $0.12-0.18/min voice, $0.02/min transcription, custom LLM pricing. Enterprise minimum $5K/mo. No public pricing page.

**Strengths:** (1) Best-in-class accuracy for complex use cases, (2) Custom fine-tuned models outperform baseline Whisper, (3) Strong enterprise compliance (SOC 2, HIPAA), (4) 10K+ customers = massive data moat, (5) Strong brand recognition.

**Weaknesses:** (1) Closed-source — complete black box, (2) Highest pricing in market (2-3x competitors), (3) No white-label, (4) No SMB pricing tier, (5) No-code builder is limited, (6) No developer community.

**Our battle card:** "Retell is the gold standard for accuracy, but you pay for it — 3x our price, no customization, no white-label. For the same cost, you could run our platform AND your own LLM."

## Vapi

**Overview:** Developer-first voice AI API. Founded 2023, HQ New York. $40M raised (Series A). 5,000+ developers, $8M+ ARR. 40+ employees.

**Product:** Clean REST API for voice agents. Focus on developer experience (documentation, SDKs, quickstart). Supports custom LLMs but limited customization.

**Pricing:** Pay-as-you-go: $0.08-0.12/min voice, $0.01/min transcription. No subscription. Free tier: 5 minutes. No enterprise pricing.

**Strengths:** (1) Excellent developer experience (best docs in class), (2) Clean API design, (3) Fast deployment (<1 hour to first call), (4) Growing developer ecosystem, (5) Competitive for low-volume use cases.

**Weaknesses:** (1) Limited enterprise features (no SSO, no audit logs), (2) No compliance certifications (no SOC 2, no HIPAA), (3) No white-label, (4) No-code builder limited, (5) Per-minute pricing gets expensive at scale, (6) No marketplace.

**Our battle card:** "Vapi is great for prototypes, but when you need enterprise compliance, white-label, or cost predictability at scale, you'll outgrow them. Our platform scales from prototype to production without switching."

## Bland AI

**Overview:** No-code voice agent builder for SMBs. Founded 2023, HQ Austin. $28M raised (Seed + Series A). 3,000+ customers, $5M+ ARR. 25+ employees.

**Product:** Visual agent builder with pre-built templates. Focus on simplicity and speed. Limited customization, no custom LLM.

**Pricing:** $29/mo (Starter): 2,000 min, 1 agent. $99/mo (Growth): 10K min. $299/mo (Scale): 50K min. Overage: $0.06/min.

**Strengths:** (1) Very easy setup (<10 minutes to first call), (2) Pre-built templates common use cases, (3) Affordable entry price, (4) Good for simple use cases, (5) Clean UI.

**Weaknesses:** (1) No custom LLM support, (2) Limited customization, (3) No compliance (no HIPAA, no SOC 2), (4) Accuracy lower for complex flows, (5) No API access in lower tiers, (6) No white-label.

**Our battle card:** "Bland is the easiest to start with, but you'll hit walls fast. Need custom LLM? Need compliance? Need API access? You need our platform. And we start at $49 — only $20 more."

## PlayAI

**Overview:** TTS-centric platform expanding into full voice agents. Founded 2022, HQ San Francisco. $15M raised (Seed). 1,000+ customers. 15+ employees.

**Product:** Exceptional text-to-speech with 100+ voices and emotional range. Recently added full voice agent capabilities (STT + LLM orchestration). Agent capabilities still early-stage.

**Pricing:** Pay-as-you-go: $0.06/min voice. TTS API: $0.001-0.003/character. Free tier: 10,000 TTS characters.

**Strengths:** (1) Best TTS quality (highest MOS scores in industry), (2) Emotional voice control, (3) Voice cloning, (4) Good for content creation.

**Weaknesses:** (1) Agent capabilities are early/immature, (2) Limited enterprise features, (3) No compliance, (4) Smallest customer base, (5) Funding may limit growth.

## Air AI

**Overview:** Outbound-focused voice AI for sales. Founded 2023, HQ Los Angeles. $55M raised (Series A). 500+ customers. 50+ employees.

**Product:** Purpose-built for outbound sales calls. AI sales agents that prospect, qualify, and book meetings. Human-like conversation capability. Outbound-only focus.

**Pricing:** $0.15-0.25/min (outbound, premium). Enterprise custom pricing.

**Strengths:** (1) Best in class for outbound, (2) Human-like conversation quality, (3) Good at objection handling, (4) Strong sales-focused features.

**Weaknesses:** (1) Outbound only (no inbound), (2) Very expensive, (3) Compliance concerns (TCPA risk for outbound AI), (4) No custom LLM, (5) No API.

## PolyAI

**Overview:** Enterprise conversational AI for contact centers. Founded 2017, HQ London. $100M+ raised (Series C). Notable customers: British Gas, Pizza Hut, Marriott.

**Product:** End-to-end conversational AI platform focused on contact center automation. Proprietary NLU, deep integration with CCaaS platforms.

**Pricing:** Enterprise only — estimated $5K-50K+/month.

**Strengths:** (1) Deepest enterprise experience, (2) Strong NLU for complex conversations, (3) Multi-language support (20+ languages), (4) CCaaS integration depth.

**Weaknesses:** (1) Very expensive, (2) Long implementation (3-6 months), (3) Closed-source, (4) No self-serve/SMB option, (5) Limited customization.

## Competitor Radar Tracking

```typescript
interface CompetitorRadar {
  competitor: string;
  lastUpdated: Date;
  
  // Product changes
  newFeatures: string[];
  pricingChanges: PriceChange[];
  partnershipAnnouncements: string[];
  
  // Business signals
  hiringActivity: number; // job postings this month
  fundingRumors: string;
  layoffs: boolean;
  acquisitions: string[];
  
  // Market presence
  g2Reviews: number;
  avgG2Rating: number;
  googleTrendsScore: number;
  twitterFollowers: number;
  
  // Our response
  recommendedAction: 'monitor' | 'respond' | 'counter' | 'ignore';
  battleCardUpdate: string;
}

function generateCompetitorAlert(radar: CompetitorRadar): Alert {
  const severity = radar.pricingChanges.some(p => p.percentChange < -10) ? 'high' :
                   radar.newFeatures.length > 2 ? 'medium' : 'low';
  
  return {
    competitor: radar.competitor,
    severity,
    summary: summarizeChanges(radar),
    recommendedAction: radar.recommendedAction,
    notifyTeams: ['product', 'marketing', 'sales'],
  };
}
```

## Competitive Battle Cards

**Sales enablement asset:** Each competitor has a 1-page battle card covering: positioning against them, proof points, objection handling, pricing comparison, ideal win/loss scenarios.

## Tools & Resources

- **Competitive intelligence:** Crayon, Klue, Kompyte
- **Pricing monitoring:** Custom scraper + manual monthly check
- **Social monitoring:** Brandwatch, Sprout Social
- **Review monitoring:** G2, Capterra alerts
- **Product monitoring:** Use competitor products monthly, track changes
- **Battle cards:** Internal wiki (Notion) + Salesforce integration
