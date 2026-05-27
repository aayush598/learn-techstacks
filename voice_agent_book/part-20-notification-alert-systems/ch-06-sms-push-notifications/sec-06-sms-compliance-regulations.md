# Section 06: SMS Compliance & Regulations

## Overview

SMS compliance ensures adherence to TCPA regulations in the US and similar regulations globally. The system manages opt-in/opt-out, message frequency caps, 10DLC registration, and consent records. Toll-free numbers and short codes have different compliance requirements.

## Implementation Approach

```typescript
interface SMSComplianceConfig {
  tenantId: string;
  provider: 'twilio' | 'vonage';
  numberType: 'toll_free' | '10dlc' | 'short_code';
  registrationStatus: 'not_registered' | 'pending' | 'approved' | 'rejected';
  brandId?: string;
  campaignId?: string;
  optInRequired: boolean;
  optInMessage?: string;
  optOutMessage?: string;
  dailyLimit: number;
  weeklyLimit: number;
  monthlyLimit: number;
}

interface ConsentRecord {
  id: string;
  userId: string;
  phoneNumber: string;
  consentType: 'opt_in' | 'opt_out';
  source: 'web_form' | 'sms_keyword' | 'api' | 'admin';
  timestamp: string;
  ipAddress?: string;
  userAgent?: string;
  campaignId?: string;
}

class SMSComplianceManager {
  async checkCompliance(to: string, tenantId: string): Promise<ComplianceResult> {
    const config = await this.getConfig(tenantId);
    const optInStatus = await this.getOptInStatus(to, tenantId);

    // Check opt-in
    if (config.optInRequired && !optInStatus.optedIn) {
      return { allowed: false, reason: 'not_opted_in', action: 'request_opt_in' };
    }

    // Check opt-out
    if (optInStatus.optedOut) {
      return { allowed: false, reason: 'opted_out', action: 'block' };
    }

    // Check frequency caps
    const recentCount = await this.getMessageCount(to, tenantId, '24h');
    if (recentCount >= config.dailyLimit) {
      return { allowed: false, reason: 'daily_limit_exceeded', action: 'block' };
    }

    return { allowed: true };
  }

  async handleOptIn(from: string, tenantId: string, source: string): Promise<void> {
    const consent: ConsentRecord = {
      id: generateId(),
      userId: await this.resolveUserId(from),
      phoneNumber: from,
      consentType: 'opt_in',
      source: source as ConsentRecord['source'],
      timestamp: new Date().toISOString(),
    };
    await this.consentStore.save(consent);
    await this.sendOptInConfirmation(from, tenantId);
  }

  async handleOptOut(from: string, tenantId: string): Promise<void> {
    const consent: ConsentRecord = {
      id: generateId(),
      userId: await this.resolveUserId(from),
      phoneNumber: from,
      consentType: 'opt_out',
      source: 'sms_keyword',
      timestamp: new Date().toISOString(),
    };
    await this.consentStore.save(consent);
    await this.sendOptOutConfirmation(from, tenantId);
  }

  async register10DLC(tenantId: string, brandInfo: BrandInfo): Promise<RegistrationResult> {
    // Register brand with TCR (The Campaign Registry)
    const brand = await this.tcrClient.registerBrand({
      name: brandInfo.name,
      ein: brandInfo.ein,
      vertical: brandInfo.vertical,
      stockSymbol: brandInfo.stockSymbol,
      stockExchange: brandInfo.stockExchange,
    });

    // Create campaign
    const campaign = await this.tcrClient.createCampaign({
      brandId: brand.brandId,
      description: brandInfo.campaignDescription,
      messageFlow: brandInfo.messageFlow,
      sampleMessages: brandInfo.sampleMessages,
    });

    const config = await this.getConfig(tenantId);
    config.brandId = brand.brandId;
    config.campaignId = campaign.campaignId;
    config.registrationStatus = 'approved';
    config.numberType = '10dlc';
    await this.storage.update(config);

    return { brandId: brand.brandId, campaignId: campaign.campaignId, status: 'approved' };
  }

  async getMessageCount(to: string, tenantId: string, window: string): Promise<number> {
    const windowMs = window === '24h' ? 86400000 : window === '7d' ? 604800000 : 2592000000;
    const since = new Date(Date.now() - windowMs).toISOString();
    return this.messageStore.count({ to, tenantId, createdAt: { $gte: since } });
  }
}
```

## Integration Points

- **Consent Store**: Database of opt-in/opt-out records
- **TCR API**: The Campaign Registry for 10DLC
- **Keyword Handling**: STOP/START/HELP keyword processing

## Production Considerations

- **Audit Trail**: Maintain consent records for compliance audits
- **Daily Caps**: Enforce per-user daily message limits
- **Legal Review**: Have SMS compliance reviewed by legal counsel
