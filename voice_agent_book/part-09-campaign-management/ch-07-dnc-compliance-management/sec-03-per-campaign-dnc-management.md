# Section 03: Per-Campaign DNC Management

## Overview

Per-campaign DNC management handles the campaign-specific exclusion rules that go beyond global DNC lists. Different campaigns may have different consent requirements, different types of contacts, and different regulatory obligations. For example, a debt collection campaign has stricter DNC rules than a survey campaign, and a campaign targeting existing customers may use the "established business relationship" (EBR) exception that a prospecting campaign cannot.

The per-campaign DNC system allows configuring which DNC sources apply to each campaign, whether EBR exceptions are allowed, campaign-specific suppression lists, and custom consent requirements. It also manages the interaction between campaigns — if a contact opts out of one campaign, that opt-out may or may not affect other campaigns depending on tenant configuration.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Per-Campaign DNC Management                     │
├─────────────────────────────────────────────────────────────┤
│  Campaign DNC Configuration:                                │
│                                                             │
│  Campaign: "Summer Sales 2025"                              │
│  ├── DNC Sources: [national_dnc, state_dnc, internal]      │
│  ├── Allow EBR Exceptions: true                            │
│  ├── Allow Prior Consent: true                             │
│  ├── Campaign-Specific Suppression: [camp_123_dnc]        │
│  ├── Opt-Out Scope: "campaign" (only this campaign)       │
│  └── Calling Hours Restriction: "standard_residential"     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Campaign DNC Resolution Logic                       │   │
│  │                                                      │   │
│  │  For each dial attempt:                             │   │
│  │  1. Apply global DNC check                           │   │
│  │  2. Check campaign-specific suppression list         │   │
│  │  3. Check EBR/consent for campaign type             │   │
│  │  4. Check cross-campaign opt-out scope               │   │
│  │  5. Check campaign-specific calling hours            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Campaign-level DNC configuration:** Each campaign specifies which DNC sources apply, allowing different campaign types to have different compliance requirements. Trade-off: configuration overhead vs. campaign-specific compliance flexibility.

- **Campaign-scoped opt-out:** By default, opt-outs are scoped to the campaign. Tenants can configure global opt-out (across all campaigns) or brand-scoped opt-out. Trade-off: opt-out scope flexibility vs. complexity.

- **EBR-based exceptions:** Campaigns can declare whether they rely on the Established Business Relationship exception. EBR has a regulatory time limit (18 months in the US, varying elsewhere). The system tracks EBR expiration. Trade-off: EBR tracking overhead vs. expanded calling permission.

- **Campaign-type specific DNC rules:** Different campaign types (sales, survey, collection, reminder) have different DNC requirements baked in. Collection campaigns, for example, cannot use certain exceptions. Trade-off: rule maintenance vs. compliance safety.

## Implementation Approach

```
class PerCampaignDncManager {
  constructor(dncChecker, campaignConfig, consentService) {
    this.dnc = dncChecker;
    this.campaignConfig = campaignConfig;
    this.consent = consentService;
  }

  async checkCampaignDnc(contact, campaign) {
    const config = await this.getCampaignDncConfig(campaign.id);
    const phone = contact.phone;

    // 1. Global DNC check (always applies)
    const globalCheck = await this.dnc.check(phone, contact.tenantId, campaign.id);
    if (globalCheck.blocked && !this.isGlobalDncOverridable(campaign)) {
      return { blocked: true, reason: 'global_dnc', source: globalCheck.source };
    }

    // 2. Campaign-specific suppression
    const campaignSuppressed = await this.checkCampaignSuppression(
      phone, campaign.id
    );
    if (campaignSuppressed) {
      return { blocked: true, reason: 'campaign_suppression' };
    }

    // 3. EBR check for campaign type
    if (config.requireEBR && campaign.type !== 'transactional') {
      const ebr = await this.consent.checkEBR(contact.id, campaign.id);
      if (!ebr.valid) {
        return { blocked: true, reason: 'no_ebr' };
      }
      if (ebr.expiring) {
        return { blocked: false, warning: 'ebr_expiring_soon', expiresAt: ebr.expiresAt };
      }
    }

    // 4. Prior consent check
    if (config.requireConsent) {
      const consent = await this.consent.checkConsent(contact.id, 'voice', campaign.id);
      if (!consent.granted) {
        return { blocked: true, reason: 'no_consent' };
      }
    }

    // 5. Cross-campaign opt-out check
    if (config.optOutScope === 'brand') {
      const brandOptOut = await this.consent.checkBrandOptOut(
        contact.id, 
        campaign.brandId
      );
      if (brandOptOut) {
        return { blocked: true, reason: 'brand_opt_out' };
      }
    }

    return { blocked: false };
  }

  async handleCampaignOptOut(contact, campaign, source) {
    const config = await this.getCampaignDncConfig(campaign.id);
    
    // Add to campaign-specific suppression
    await this.addCampaignSuppression(contact.phone, campaign.id, {
      source: 'opt_out',
      timestamp: new Date(),
      campaignId: campaign.id
    });

    // If global scope, add to global DNC
    if (config.optOutScope === 'global') {
      await this.dnc.handleOptOut(
        contact.phone,
        contact.tenantId,
        'campaign_opt_out',
        campaign.id
      );
    }

    // If brand scope, note the brand opt-out
    if (config.optOutScope === 'brand') {
      await this.consent.recordBrandOptOut(
        contact.id,
        campaign.brandId,
        { source: 'voice_campaign', campaignId: campaign.id }
      );
    }

    // Log the opt-out
    await this.logOptOut({
      contactId: contact.id,
      campaignId: campaign.id,
      scope: config.optOutScope,
      source,
      timestamp: new Date()
    });
  }

  async getCampaignDncConfig(campaignId) {
    const cacheKey = `campaign:dnc:config:${campaignId}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const campaign = await this.campaignConfig.getCampaign(campaignId);
    const config = {
      dncSources: campaign.dncSources || ['national_dnc', 'state_dnc', 'internal'],
      allowEBR: campaign.allowEbr ?? true,
      requireConsent: campaign.requireConsent ?? false,
      optOutScope: campaign.optOutScope || 'campaign',
      requireEBR: campaign.type === 'sales' || campaign.type === 'collection',
      campaignType: campaign.type
    };

    await this.cache.setex(cacheKey, 3600, JSON.stringify(config));
    return config;
  }

  isGlobalDncOverridable(campaign) {
    // Transactional and emergency campaigns may override DNC
    return ['transactional', 'emergency', 'service'].includes(campaign.type);
  }

  async checkCampaignSuppression(phone, campaignId) {
    return this.db.campaignSuppression.findUnique({
      where: {
        campaign_phone: {
          campaign_id: campaignId,
          phone: phone
        }
      }
    });
  }

  async addCampaignSuppression(phone, campaignId, metadata) {
    await this.db.campaignSuppression.create({
      data: {
        campaign_id: campaignId,
        phone,
        metadata
      }
    });
  }
}
```

## Integration Points

- **Real-Time DNC Engine (sec-02):** Global DNC check feeds into campaign-level decision
- **Consent/EBR Service (sec-05):** Tracks consent and EBR for exception handling
- **Campaign Configuration (Ch 01):** DNC settings per campaign type
- **Opt-Out Recording:** Captures campaign-level and global opt-outs
- **Compliance Audit (sec-07):** Campaign-level DNC decisions logged for audit
- **Campaign Analytics (Ch 09):** DNC block rate per campaign tracking

## Open-Source Tools

- **PostgreSQL:** Campaign suppression list storage with composite indexes
- **Redis:** Campaign DNC configuration cache
- **BullMQ:** Campaign-level opt-out propagation to other campaigns
- **Zod:** Campaign DNC configuration schema validation

## Production Considerations

- Campaign-specific suppression lists should be checked alongside global DNC for consistent performance
- Opt-out scope configuration affects legal liability — "global" scope reduces legal risk but may limit marketing effectiveness
- EBR tracking is complex — the 18-month clock resets with each purchase or customer interaction
- Different campaign types within the same tenant may have conflicting DNC requirements — collection vs. marketing campaigns
- Campaign DNC configuration should be auditable — changes should be logged with author and reason
- Campaign superset suppression: if a contact opts out of a brand, all campaigns for that brand should respect it
- Test cross-campaign interactions — if a contact opts out of campaign A, can campaign B still call them?
- Provide a DNC configuration summary in the campaign setup UI showing effective restrictions
- Campaign DNC rules change when regulations change — notify operators when campaign-level rules need review
- Monitor campaign DNC block rate — a sudden increase may indicate a configuration error
