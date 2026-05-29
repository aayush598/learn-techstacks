# Section 07: Geographic Markets

## Geographic Expansion Strategy

Our geographic rollout follows a phased approach: North America (Year 1), UK/Europe (Year 2), APAC and Rest of World (Year 3). Each phase requires localization, compliance, and go-to-market adaptation.

```
Geographic Market Expansion Timeline
Year 1: North America          Year 2: Europe          Year 3: APAC + ROW
┌─────────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ USA               │    │ UK               │    │ Japan            │
│ Canada            │    │ Germany           │    │ Australia        │
│ (Mexico in Q4)    │    │ France            │    │ South Korea      │
│                    │    │ Netherlands       │    │ India            │
│                    │    │ Spain             │    │ Brazil           │
│                    │    │ Nordics           │    │ Mexico (if not   │
│                    │    │                   │    │ Year 1)          │
└─────────────────────┘    └──────────────────┘    └──────────────────┘
```

## Market Prioritization Scorecard

| Country | TAM ($M) | Voice AI Readiness | Compliance Complexity | Language Support | Competition | Priority Score |
|---------|----------|-------------------|---------------------|-----------------|-------------|----------------|
| USA | $8,500 | 9/10 | 7/10 | English | High | 85 |
| Canada | $900 | 8/10 | 7/10 | English/French | Medium | 75 |
| UK | $2,100 | 8/10 | 6/10 (GDPR) | English | Medium | 78 |
| Germany | $1,800 | 7/10 | 5/10 (Strict GDPR) | German | Low | 68 |
| France | $1,200 | 6/10 | 5/10 (CNIL) | French | Low | 60 |
| Japan | $1,500 | 6/10 | 7/10 | Japanese | Very Low | 58 |
| Australia | $600 | 7/10 | 8/10 | English | Low | 65 |
| India | $800 | 8/10 | 8/10 | English + 22 langs | Medium | 55 |
| Brazil | $500 | 5/10 | 6/10 (LGPD) | Portuguese | Very Low | 42 |

## Localization Requirements

### Phase 1: North America (Year 1)
**Languages:** English (US, UK, CA variants), Spanish (US). **Compliance:** TCPA (federal + state), FCC, state-level consent laws (11 two-party consent states). **Telephony:** North American Numbering Plan (NANP), Twilio/Telnyx local termination. **Data residency:** US-based (AWS us-east-1, us-west-2). **Payment:** USD, credit card (Stripe). **Support:** US Eastern/Central/Pacific time zones, English + Spanish.

### Phase 2: Europe (Year 2)
**Languages:** UK English, German, French, Dutch, Spanish, Swedish, Norwegian, Danish. **Compliance:** GDPR (EU), ePrivacy Directive, UK GDPR, national data protection laws (BDSG, LFPDPPP). **Data residency:** EU-based (AWS eu-west-1, eu-central-1). **Telephony:** E.164 numbering, local DIDs, SIP trunking with European carriers. **Payment:** EUR, GBP, SEPA/credit card, VAT handling. **Support:** CET time zone, local language support for top 3 markets.

### Phase 3: APAC & ROW (Year 3)
**Languages:** Japanese, Korean, Mandarin (simplified), Hindi, Portuguese. **Compliance:** APPI (Japan), PIPA (Korea), PIPL (China), IDPR (India), LGPD (Brazil). **Data residency:** Local regions (ap-northeast-1, ap-south-1, sa-east-1). **Telephony:** Local carrier partnerships, country-specific numbering. **Payment:** Local payment methods, multi-currency. **Support:** Follow-the-sun model, local partners.

## Localization Architecture

```typescript
interface LocalizedContent {
  locale: string;
  language: string;
  region: string;
  
  // Voice-specific
  sttModel: string; // Whisper model fine-tuned for this locale
  ttsVoices: VoiceConfig[];
  llmPromptTemplate: string;
  supportedDialects: string[];
  
  // Business
  currency: string;
  taxRate: number;
  pricingFormatter: (amount: number) => string;
  dateTimeFormatter: (date: Date) => string;
  
  // Compliance
  consentRequirements: ConsentRule[];
  dataResidency: string;
  regulations: string[];
}

class LocalizationManager {
  private locales: Map<string, LocalizedContent> = new Map();
  
  async detectLocale(phoneNumber: string): Promise<string> {
    const country = await this.lookupCountry(phoneNumber);
    const language = await this.detectLanguage(phoneNumber);
    return `${language}-${country}`;
  }
  
  localizeVoicePipeline(locale: string): VoicePipelineConfig {
    const config = this.locales.get(locale);
    if (!config) throw new Error(`Unsupported locale: ${locale}`);
    
    return {
      stt: { model: config.sttModel, language: locale.split('-')[0] },
      tts: { voice: config.ttsVoices[0] },
      llm: { promptTemplate: config.llmPromptTemplate },
      compliance: config.consentRequirements,
    };
  }
}
```

## Localization Tools

| Tool | Purpose | Alternative |
|------|---------|-------------|
| i18next | JavaScript i18n framework | Lingui, FormatJS |
| DeepL | Translation API | Google Translate, Amazon Translate |
| Crowdin | Translation management | Lokalise, Transifex |
| Whisper fine-tuning | Locale-specific STT | Massively Multilingual Speech (Meta) |
| Coqui XTTS | Locale-specific TTS | Piper, Bark |
| Local payment | Stripe, Adyen | Paddle, GoCardless |

## International Pricing Strategy

| Market | Pricing Strategy | Starter | Pro | Business |
|--------|-----------------|---------|-----|----------|
| US | Standard | $49 | $199 | $499 |
| UK | Localized (1:1 GBP) | £39 | £159 | £399 |
| EU | Localized (PPP-adjusted) | €45 | €179 | €449 |
| Japan | PPP-adjusted | ¥5,500 | ¥22,000 | ¥55,000 |
| India | Reduced (1:2 USD ratio) | ₹2,500 | ₹10,000 | ₹25,000 |

## Geographic KPI Targets

| Region | Year 1 Rev | Year 2 Rev | Year 3 Rev | % of Total (Y3) |
|--------|-----------|-----------|-----------|-----------------|
| North America | $1.0M | $3.5M | $6.0M | 55% |
| Europe | $0.1M | $1.0M | $3.0M | 28% |
| APAC | $0 | $0.3M | $1.0M | 9% |
| ROW | $0 | $0.1M | $0.8M | 8% |

## Tools & Resources

- **Market research:** Statista, eMarketer, GSMA mobile reports
- **Local payments:** Stripe (multi-currency), Adyen, Paystack (Africa)
- **Local DIDs:** Twilio, Telnyx, Voxbone (now Bandwidth)
- **Translation management:** Crowdin, Lokalise, Transifex
- **Compliance (EU):** OneTrust, TransPerfect, local legal counsel
- **Data residency:** AWS Local Zones, GCP regions, Cloudflare
