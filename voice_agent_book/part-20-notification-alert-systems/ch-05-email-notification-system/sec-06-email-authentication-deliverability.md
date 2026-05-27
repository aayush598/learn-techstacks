# Section 06: Email Authentication & Deliverability

## Overview

Email authentication ensures emails are properly authenticated and delivered to inboxes. SPF, DKIM, and DMARC records verify sender identity. Domain warmup gradually increases sending volume to build reputation. Reputation monitoring tracks sending reputation across major mailboxes.

## Implementation Approach

```typescript
interface DomainConfig {
  domain: string;
  spfRecord: string;
  dkimRecords: DkimRecord[];
  dmarcRecord: string;
  warmupStatus: 'not_started' | 'warming' | 'active' | 'at_risk';
  reputation: DomainReputation;
}

interface DkimRecord {
  selector: string;
  publicKey: string;
  privateKey: string; // encrypted
}

interface DomainReputation {
  score: number; // 0-100
  providerScores: Record<string, number>;
  lastChecked: string;
  issues: ReputationIssue[];
}

class EmailAuthenticationManager {
  async setupDomain(domain: string): Promise<DomainConfig> {
    const dkimKeys = await this.generateDkimKeys();
    const config: DomainConfig = {
      domain,
      spfRecord: `v=spf1 include:${this.mailProvider.spfHost} ~all`,
      dkimRecords: [{
        selector: this.getSelector(domain),
        publicKey: dkimKeys.public,
        privateKey: dkimKeys.private,
      }],
      dmarcRecord: `v=DMARC1; p=quarantine; rua=mailto:dmarc@${domain}`,
      warmupStatus: 'not_started',
      reputation: {
        score: 50,
        providerScores: {},
        lastChecked: new Date().toISOString(),
        issues: [],
      },
    };
    await this.storage.save(config);
    return config;
  }

  async checkDnsRecords(domain: string): Promise<DNSValidationResult> {
    const [spf, dkim, dmarc] = await Promise.all([
      this.resolveTxt(`${domain}`, 'v=spf1'),
      this.resolveTxt(`_domainkey.${domain}`, 'v=DKIM1'),
      this.resolveTxt(`_dmarc.${domain}`, 'v=DMARC1'),
    ]);
    return { spf: spf.found, dkim: dkim.found, dmarc: dmarc.found };
  }

  async warmupDomain(domain: string): Promise<void> {
    const config = await this.getDomainConfig(domain);
    config.warmupStatus = 'warming';

    // Gradual volume increase over 2-4 weeks
    const warmupSchedule = [
      { day: 1, maxPerDay: 50 },
      { day: 7, maxPerDay: 500 },
      { day: 14, maxPerDay: 5000 },
      { day: 21, maxPerDay: 50000 },
      { day: 28, maxPerDay: 'unlimited' },
    ];

    await this.warmupStore.saveSchedule(domain, warmupSchedule);
    await this.storage.update(config);
  }

  async checkReputation(domain: string): Promise<DomainReputation> {
    const config = await this.getDomainConfig(domain);
    const results = await Promise.all([
      this.checkGoogleReputation(domain),
      this.checkMicrosoftReputation(domain),
      this.checkYahooReputation(domain),
    ]);
    config.reputation = {
      score: Math.round(results.reduce((s, r) => s + r.score, 0) / results.length),
      providerScores: Object.fromEntries(results.map(r => [r.provider, r.score])),
      lastChecked: new Date().toISOString(),
      issues: results.flatMap(r => r.issues),
    };
    await this.storage.update(config);
    return config.reputation;
  }

  private async generateDkimKeys(): Promise<{ public: string; private: string }> {
    const crypto = require('crypto');
    const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
      modulusLength: 2048,
      publicKeyEncoding: { type: 'spki', format: 'pem' },
      privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
    });
    return { public: publicKey.toString(), private: privateKey.toString() };
  }
}
```

## Integration Points

- **DNS Management**: Automated DNS record creation via provider API
- **Reputation Services**: Google Postmaster, Microsoft SNDS
- **Monitoring Dashboard**: Domain health and reputation display

## Production Considerations

- **Key Rotation**: Rotate DKIM keys every 6 months
- **DMARC Policy**: Start with p=none, move to p=quarantine, then p=reject
- **Warmup Compliance**: Stay within volume limits during warmup
