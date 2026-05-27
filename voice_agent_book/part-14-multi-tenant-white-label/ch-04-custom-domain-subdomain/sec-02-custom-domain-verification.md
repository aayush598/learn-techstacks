# Section 02: Custom Domain Verification

## Overview

Custom domain verification ensures that a tenant actually controls the domain they want to use with the platform. Without verification, a malicious tenant could point another company's domain to their account, intercepting traffic intended for that company. Verification is performed by asking the tenant to add a specific DNS record (TXT or CNAME) to their domain's DNS configuration, then verifying that the record exists before activating the domain.

The verification process: tenant enters their custom domain in the dashboard, the system generates a unique verification token, the tenant adds a DNS TXT record with that token to their domain, the system periodically checks for the record (typically via DNS lookup), and once verified, the system provisions an SSL certificate and activates the domain. The entire process is automated except for the DNS change that the tenant must make in their own DNS provider.

For a voice agent platform, custom domain support is essential for white-label and enterprise customers who want their agents to be accessible from their own domain (e.g., `voiceagent.acmecorp.com`). The verification process must be simple enough for non-technical users to follow, with clear instructions for common DNS providers (Cloudflare, GoDaddy, AWS Route53, Namecheap, Google Domains).

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface CustomDomain {
  id: string;
  tenantId: string;
  domain: string;
  verificationToken: string;
  status: 'pending' | 'verifying' | 'active' | 'failed' | 'expired';
  verifiedAt?: Date;
  sslExpiresAt?: Date;
  lastCheckAt?: Date;
}

class DomainVerificationService {
  private dnsResolver: DnsResolver;
  private sslService: SSLService;

  async initiateVerification(tenantId: string, domain: string): Promise<CustomDomain> {
    // Validate domain format
    if (!this.isValidDomain(domain)) {
      throw new Error('Invalid domain format');
    }

    // Check domain not already in use
    const existing = await this.findDomainByDomain(domain);
    if (existing) {
      throw new Error('Domain is already configured for another account');
    }

    // Generate verification token
    const verificationToken = `va_verify_${crypto.randomBytes(16).toString('hex')}`;

    // Create domain record
    const domainRecord = await this.pool.query(`
      INSERT INTO custom_domains (tenant_id, domain, verification_token, status)
      VALUES ($1, $2, $3, 'pending')
      RETURNING *
    `, [tenantId, domain, verificationToken]);

    // Start async verification
    await this.queue.add('verify-domain', {
      domainId: domainRecord.rows[0].id,
      domain,
      verificationToken,
    });

    return domainRecord.rows[0];
  }

  async verifyDomain(job: Job): Promise<void> {
    const { domainId, domain, verificationToken } = job.data;
    
    // DNS record format: _voiceagent-verification.example.com → TXT "va_verify_abc123"
    const dnsRecord = `_voiceagent-verification.${domain}`;

    // Check up to 10 times with 30s interval (DNS propagation can be slow)
    for (let attempt = 0; attempt < 10; attempt++) {
      const records = await this.dnsResolver.resolveTxt(dnsRecord);
      
      if (records.includes(verificationToken)) {
        // Verification successful
        await this.activateDomain(domainId, domain);
        return;
      }

      // Wait for DNS propagation
      await this.sleep(30000);
    }

    // Verification failed
    await this.markFailed(domainId);
  }

  private async activateDomain(domainId: string, domain: string): Promise<void> {
    // Issue SSL certificate via Let's Encrypt DNS-01
    const sslCert = await this.sslService.issueCertificate(domain);

    // Update domain record
    await this.pool.query(`
      UPDATE custom_domains 
      SET status = 'active', 
          verified_at = NOW(),
          ssl_cert_arn = $1,
          ssl_expires_at = $2
      WHERE id = $3
    `, [sslCert.arn, sslCert.expiresAt, domainId]);

    // Update reverse proxy configuration
    await this.updateProxyConfig(domain);

    // Notify tenant
    await this.notificationService.send({
      tenantId: this.getTenantId(domainId),
      type: 'domain_verified',
      data: { domain },
    });
  }

  async reVerifyDomain(domainId: string): Promise<boolean> {
    const domain = await this.getDomain(domainId);
    const dnsRecord = `_voiceagent-verification.${domain.domain}`;
    const records = await this.dnsResolver.resolveTxt(dnsRecord);
    
    if (records.includes(domain.verification_token)) {
      return true;
    }

    // Domain verification lost
    await this.pool.query(
      `UPDATE custom_domains SET status = 'expired' WHERE id = $1`,
      [domainId]
    );
    
    await this.notificationService.send({
      tenantId: domain.tenant_id,
      type: 'domain_verification_lost',
      data: { domain: domain.domain },
    });

    return false;
  }

  getDnsInstructions(domain: string): DnsInstruction[] {
    return [
      {
        type: 'TXT',
        name: `_voiceagent-verification`,
        value: this.getVerificationToken(domain),
        ttl: 300,
        purpose: 'Domain ownership verification',
      },
      {
        type: 'CNAME',
        name: '@',
        value: 'app.voiceagent.com',
        ttl: 300,
        purpose: 'Route traffic to Voice Agent',
      },
    ];
  }

  private isValidDomain(domain: string): boolean {
    const domainRegex = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$/;
    return domainRegex.test(domain);
  }
}
```

## Integration Points

- **Reverse Proxy (Sec 04):** Domain verification triggers proxy configuration update
- **SSL Certificates (Sec 03):** Let's Encrypt integration for certificate issuance
- **Tenant Dashboard:** Domain management UI showing verification status
- **Email Notifications:** Domain verification status changes sent to tenant admin
- **DNS Provider Configuration:** Instructions for common DNS providers

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **DNS Propagation Delay:** DNS changes can take 5-30 minutes to propagate, sometimes up to 48 hours with long TTLs. Instruct tenants to set TTL to 300 seconds (5 minutes) for faster verification.
- **Verification Token Security:** The verification token is a secret. Treat it like a password. It proves domain ownership and should be unique per domain, stored hashed in the database.
- **Domain Takeover Prevention:** When a domain is verified, lock it to the tenant. If the tenant later deletes their account, remove the proxy configuration to prevent domain reuse by malicious actors.
- **Re-verification Timer:** Schedule re-verification checks weekly for active domains. If verification fails 3 consecutive times, notify the tenant and deactivate the domain after 30 days.
- **Rate Limiting:** Limit domain verification attempts to 3 per day per tenant. DNS lookups are not free (cost and latency), and abuse is possible.
- **Domain Wildcard:** If a tenant verifies `example.com`, they should also be able to use `*.example.com` for subdomain-based routing. Support wildcard domain verification.
