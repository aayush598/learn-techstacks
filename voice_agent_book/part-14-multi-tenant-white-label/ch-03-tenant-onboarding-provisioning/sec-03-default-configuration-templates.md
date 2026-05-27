# Section 03: Default Configuration Templates

## Overview

Default configuration templates ensure every newly provisioned tenant starts with sensible defaults tailored to their plan tier, industry, and use case. These templates define feature flags, quota limits, rate limits, AI model defaults, voice settings, integration presets, and compliance configurations that are appropriate for the tenant's subscription level. A starter tenant should not have enterprise-level quotas (they'd be misleading), and an enterprise tenant should not have starter-level restrictions (they'd be frustrating).

Configuration templates are defined as JSON/YAML files stored in a configuration registry, versioned for auditability, and assigned to tenants during provisioning. The template inheritance model allows base templates per tier with industry-specific overrides. For example, a healthcare tenant on the Growth plan inherits Growth defaults plus healthcare-specific settings (HIPAA logging, PHI handling, consent recording).

The templates are not static—they evolve as the platform adds features and adjusts limits. When a template is updated, existing tenants may be migrated to the new template (opt-in or automatic depending on the change type). Breaking changes to limits or features require notification and opt-in migration.

## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface TenantConfiguration {
  features: Record<string, boolean>;
  quotas: {
    monthlyCallMinutes: number;
    maxAgents: number;
    maxCampaigns: number;
    storageGB: number;
    apiRateLimit: number;
  };
  defaults: {
    voiceProvider: string;
    voiceId: string;
    sttProvider: string;
    llmProvider: string;
    language: string;
    timezone: string;
  };
  compliance: {
    hipaa: boolean;
    gdpr: boolean;
    callRecording: boolean;
    consentRecording: boolean;
  };
  branding: WhiteLabelConfig;
}

const TIER_TEMPLATES: Record<string, TenantConfiguration> = {
  starter: {
    features: { analytics: true, apiAccess: true, webhooks: false, customVoice: false },
    quotas: { monthlyCallMinutes: 1000, maxAgents: 3, maxCampaigns: 2, storageGB: 5, apiRateLimit: 100 },
    defaults: { voiceProvider: 'elevenlabs', voiceId: 'default', sttProvider: 'whisper', llmProvider: 'gpt-4o-mini', language: 'en', timezone: 'UTC' },
    compliance: { hipaa: false, gdpr: true, callRecording: true, consentRecording: false },
    branding: { logo: null, colors: {}, domain: null },
  },
  growth: {
    features: { analytics: true, apiAccess: true, webhooks: true, customVoice: true },
    quotas: { monthlyCallMinutes: 10000, maxAgents: 10, maxCampaigns: 10, storageGB: 50, apiRateLimit: 1000 },
    defaults: { voiceProvider: 'elevenlabs', voiceId: 'premium', sttProvider: 'deepgram', llmProvider: 'gpt-4o', language: 'en', timezone: 'UTC' },
    compliance: { hipaa: false, gdpr: true, callRecording: true, consentRecording: true },
    branding: { logo: null, colors: {}, domain: 'custom' },
  },
  enterprise: {
    features: { analytics: true, apiAccess: true, webhooks: true, customVoice: true, sso: true, sla: true },
    quotas: { monthlyCallMinutes: 100000, maxAgents: 100, maxCampaigns: 100, storageGB: 500, apiRateLimit: 10000 },
    defaults: { voiceProvider: 'elevenlabs', voiceId: 'premium', sttProvider: 'deepgram', llmProvider: 'gpt-4o', language: 'en', timezone: 'UTC' },
    compliance: { hipaa: true, gdpr: true, callRecording: true, consentRecording: true },
    branding: { logo: { maxSize: 5 }, colors: { primary: '#000', secondary: '#fff' }, domain: 'custom' },
  },
};

const INDUSTRY_OVERLAYS: Record<string, Partial<TenantConfiguration>> = {
  healthcare: {
    compliance: { hipaa: true, callRecording: true, consentRecording: true },
    defaults: { language: 'en', timezone: 'US/Eastern' },
  },
  finance: {
    compliance: { callRecording: true, consentRecording: true },
    defaults: { language: 'en', timezone: 'US/Eastern' },
    features: { complianceLogging: true },
  },
};

function getConfigurationTemplate(tier: string, industry?: string): TenantConfiguration {
  const base = deepClone(TIER_TEMPLATES[tier] || TIER_TEMPLATES.starter);
  
  if (industry && INDUSTRY_OVERLAYS[industry]) {
    deepMerge(base, INDUSTRY_OVERLAYS[industry]);
  }
  
  return base;
}
```

## Integration Points

- **Provisioning (Sec 02):** Template applied during tenant creation
- **Feature Flags:** Template defines initial feature flag state
- **Billing (Part 17):** Quota limits defined in template and used for overage enforcement
- **White-Label (Ch 05):** Branding defaults feed into white-label configuration
- **Analytics:** Configuration version tracking for feature adoption analysis

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Template Evolution:** Add new fields with backward-compatible defaults. Never remove fields that existing tenants reference. Use semantic versioning for templates.
- **Opt-In vs Auto-Apply:** Non-breaking template changes (new feature flags defaulting to false) can auto-apply. Breaking changes (reducing quotas) require tenant opt-in with notification.
- **Configuration Drift Detection:** Tenants may have custom configurations that differ from their template. Detect drift and report in admin dashboard. Allow re-syncing to template.
- **Template Preview:** Provide a tool for sales/support to preview what configuration a prospect would receive based on tier and industry selection.
- **Audit Log:** Every template assignment and override is logged with the admin who made the change and the reason.
