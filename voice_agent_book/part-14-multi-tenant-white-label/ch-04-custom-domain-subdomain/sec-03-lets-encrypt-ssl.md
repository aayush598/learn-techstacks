# Section 03: Let's Encrypt SSL Automation

## Overview

Automated SSL certificate management is essential for a multi-tenant platform supporting custom domains. Each custom domain requires a valid SSL certificate, and with potentially thousands of tenant domains, manual certificate management is impossible. Let's Encrypt provides free, automated SSL certificates via the ACME (Automatic Certificate Management Environment) protocol, enabling fully automated certificate issuance, renewal, and revocation.

The ACME DNS-01 challenge is the preferred method for multi-tenant SaaS platforms with custom domains. Unlike HTTP-01 (which requires serving a file on port 80), DNS-01 uses a DNS TXT record to prove domain ownership and can issue wildcard certificates. The challenge flow: the server generates a DNS TXT record value, the tenant adds it (or automation adds it via DNS provider API), Let's Encrypt validates, and the certificate is issued. Renewal is fully automated before expiration.

For a voice agent platform, SSL automation must handle: initial issuance on domain verification, automatic renewal before expiry (every 60 days), mass re-issuance on certificate authority changes, wildcard certificate support for tenant subdomains, and emergency revocation on security incidents.

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
class SSLService {
  private acmeClient: AcmeClient;
  private certificateStore: CertificateStore;

  async issueCertificate(domain: string, altNames?: string[]): Promise<SSLCertificate> {
    // 1. Generate account key (if first time)
    const accountKey = await this.getOrCreateAccountKey();

    // 2. Generate domain key pair
    const { privateKey, publicKey } = await this.generateKeyPair('ecdsa-p384');

    // 3. Create CSR
    const csr = await this.createCSR(privateKey, domain, altNames);

    // 4. DNS-01 challenge
    const challengeToken = await this.acmeClient.createChallenge(domain);
    await this.dnsProvider.addTxtRecord(
      `_acme-challenge.${domain}`,
      challengeToken,
      60 // short TTL
    );

    // 5. Wait for propagation
    await this.waitForDnsPropagation(domain, challengeToken);

    // 6. Complete challenge and get certificate
    const certificate = await this.acmeClient.completeChallenge(domain, challengeToken);

    // 7. Store certificate
    const certRecord = await this.certificateStore.save({
      domain,
      certificate: certificate.cert,
      privateKey,
      chain: certificate.chain,
      expiresAt: certificate.expiresAt,
    });

    // 8. Deploy to proxy
    await this.deployToProxy(domain, certificate);

    // 9. Schedule renewal
    await this.scheduleRenewal(domain, certificate.expiresAt);

    return certRecord;
  }

  async renewCertificate(domain: string): Promise<void> {
    const existing = await this.certificateStore.findByDomain(domain);
    if (!existing) {
      return this.issueCertificate(domain);
    }

    // Check if renewal is needed (30 days before expiry)
    const daysUntilExpiry = Math.floor(
      (existing.expiresAt.getTime() - Date.now()) / (1000 * 60 * 60 * 24)
    );

    if (daysUntilExpiry > 30) {
      return; // Not yet time for renewal
    }

    // Issue new certificate
    const newCert = await this.issueCertificate(domain);

    // Update proxy configuration
    await this.updateProxyCertificate(domain, newCert);

    // Log renewal
    await this.auditService.log('ssl.renewed', { domain, expiresAt: newCert.expiresAt });
  }

  async revokeCertificate(domain: string, reason?: string): Promise<void> {
    const cert = await this.certificateStore.findByDomain(domain);
    if (!cert) return;

    // Revoke with Let's Encrypt
    await this.acmeClient.revokeCertificate(cert.serialNumber);

    // Remove from proxy
    await this.removeFromProxy(domain);

    // Mark as revoked
    await this.certificateStore.markRevoked(cert.id, reason);
  }

  async renewAllCertificates(): Promise<RenewalSummary> {
    const expiringCerts = await this.certificateStore.findExpiringWithin(30); // days
    let renewed = 0;
    let failed = 0;

    for (const cert of expiringCerts) {
      try {
        await this.renewCertificate(cert.domain);
        renewed++;
      } catch (error) {
        failed++;
        await this.alertService.send({
          type: 'ssl_renewal_failed',
          domain: cert.domain,
          error: error.message,
        });
      }
    }

    return { renewed, failed, total: expiringCerts.length };
  }

  private async createCSR(
    privateKey: KeyObject,
    domain: string,
    altNames?: string[]
  ): Promise<string> {
    const csr = forge.pki.createCsr();
    csr.publicKey = forge.pki.setRsaPublicKey(privateKey.n, privateKey.e);
    
    const attrs = [{ name: 'commonName', value: domain }];
    csr.setSubject(attrs);
    
    // Add SANs
    const extensions = [{
      name: 'subjectAltName',
      altNames: [
        { type: 2, value: domain }, // DNS
        ...(altNames || []).map(name => ({ type: 2, value: name })),
      ],
    }];
    csr.setAttributes(extensions);

    // Sign CSR
    csr.sign(privateKey, forge.md.sha256.create());
    return forge.pki.csrToPem(csr);
  }

  private async deployToProxy(domain: string, certificate: SSLCertificate): Promise<void> {
    // Deploy to AWS ACM
    const acmResult = await acm.importCertificate({
      Certificate: certificate.cert,
      PrivateKey: certificate.privateKey,
      CertificateChain: certificate.chain,
    });

    // Update CloudFront / ALB listener
    await this.updateListenerCertificate(domain, acmResult.CertificateArn);
  }

  private async scheduleRenewal(domain: string, expiresAt: Date): Promise<void> {
    // Schedule renewal 30 days before expiry
    const renewalDate = new Date(expiresAt.getTime() - 30 * 24 * 60 * 60 * 1000);
    
    await this.queue.add(
      'renew-ssl',
      { domain },
      { delay: renewalDate.getTime() - Date.now() }
    );
  }
}
```

## Integration Points

- **Domain Verification (Sec 02):** Triggers SSL issuance after verification
- **Reverse Proxy (Sec 04):** Deploys certificates to proxy configuration
- **DNS Provider API:** Manages ACME DNS-01 challenge records
- **Monitoring:** Certificate expiry monitoring and renewal alerts
- **Audit Logging:** All certificate lifecycle events logged

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Let's Encrypt Rate Limits:** Let's Encrypt has rate limits: 50 certificates per domain per week, 300 pending authorizations, 5 failed authorizations per account per hour. Implement a queue to stay within limits.
- **Certificate Transparency:** All Let's Encrypt certificates are logged to Certificate Transparency logs. This is public information—anyone can see which domains have certificates. Acceptable for most SaaS.
- **Renewal Monitoring:** Track certificate expiry dates. Alert at 30, 14, 7, and 3 days before expiry. Automatic renewal should handle 99%+ of cases, but monitoring catches edge cases.
- **Revocation Distribution:** If a certificate is compromised, immediate revocation is critical. CDNs and browsers cache certificate status. OCSP stapling helps but doesn't fully solve revocation timing.
- **Private Key Security:** Store private keys encrypted at rest. Use hardware security modules (HSM) or cloud KMS for key management. Never log private keys.
- **Wildcard Certificates:** Use wildcard certificates (`*.voiceagent.com` and per-tenant `*.customdomain.com`) to reduce the number of certificates needed. Wildcard certs also simplify proxy configuration.
