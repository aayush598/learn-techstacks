# Section 04: Signature Verification and Security

## Overview

Webhook signature verification ensures that every webhook delivery is authentic (originated from the platform), has integrity (not tampered during transit), and cannot be replayed by an attacker. The security layer provides consumers with the tools to verify that incoming webhook POST requests are genuine, using HMAC-based payload signing, timestamp verification, and optional consumer-side IP allowlisting.

The security model follows industry best practices established by Stripe, GitHub, and Twilio webhook systems. Each webhook endpoint is configured with a unique signing secret at registration time. Every webhook delivery includes an HMAC-SHA256 signature header, an event timestamp, and an idempotency key. Consumers verify the signature by recomputing the HMAC using the shared secret and comparing it to the provided signature. The timestamp prevents replay attacks — consumers reject events with timestamps older than a configurable threshold (default 5 minutes).

## Architecture

```
               Webhook Security Architecture

   Webhook Engine → HMAC Sign → HTTPS → Consumer → HMAC Verify
                        |                              |
   +----------------------------------------------------------+
   |              Security Components                         |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | HMAC-SHA256      |  | Timestamp         |            |
   |  | Signer           |  | • ISO 8601 in     |            |
   |  | • Payload hash   |  |   envelope        |            |
   |  | • Secret based   |  | • Consumer        |            |
   |  | • Constant-time  |  |   tolerance (5min)|            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Idempotency Key  |  | IP Allowlisting    |           |
   |  | • Event ID       |  | • Optional filter  |           |
   |  | • Dedup window   |  | • Egress CIDR      |           |
   |  |   (24h)          |  | • Published ranges |           |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Secret Rotation  |  | Replay Protection  |            |
   |  | • Key rotation   |  | • Timestamp check  |            |
   |  |   endpoint       |  | • Nonce store      |            |
   |  | • Dual-key phase |  | • Expiry window    |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **HMAC-SHA256 over RSA/ECDSA signatures:** Symmetric HMAC signatures are simpler to compute (no asymmetric key management), faster (sign and verify in microseconds), and have smaller signature headers (64 hex chars vs. hundreds of base64 chars for RSA). The trade-off is that both the platform and consumer share the same secret — if a consumer's secret is compromised, the attacker can forge webhooks to that consumer. Trade-off: symmetric requires careful secret storage at the consumer but provides simpler implementation and better performance.

- **Stripe-style signature scheme over raw payload hash:** The signature covers a signed payload string: the timestamp concatenated with the JSON body (`${timestamp}.${body}`). The signature header is `t=<timestamp>,v1=<hmac>`. This scheme binds the timestamp to the payload in the HMAC computation, preventing attackers from modifying the timestamp without invalidating the signature. The `v1` prefix allows future algorithm evolution (v2, v3) without breaking existing consumers. Trade-off: the signed payload string is slightly more complex to construct but provides stronger security properties.

- **Consumer-optional IP verification over mandatory allowlisting:** IP allowlisting is available but optional. The platform publishes its egress IP ranges (for cloud deployments, these are known CIDR blocks). Consumers can configure their firewall to allow traffic only from these ranges as a defense-in-depth measure. However, pure IP-based security is fragile (IPs change with cloud provider rebalancing). Signature verification remains the primary authentication mechanism. Trade-off: IP allowlisting adds operational overhead (keeping CIDR ranges updated) but provides an additional security layer for high-security consumers.

## Implementation Approach

```
interface SignatureHeaders {
  timestamp: string;           // Unix timestamp
  signature: string;           // HMAC-SHA256 hex
  scheme: 'v1';
}

class WebhookSecurity {
  static readonly TOLERANCE_MS = 5 * 60 * 1000; // 5 minutes
  static readonly SIGNATURE_VERSION = 'v1';

  signPayload(body: string, secret: string, timestamp?: string): SignatureHeaders {
    const ts = timestamp || Math.floor(Date.now() / 1000).toString();
    const signedPayload = `${ts}.${body}`;
    const hmac = crypto.createHmac('sha256', secret).update(signedPayload).digest('hex');

    return { timestamp: ts, signature: hmac, scheme: 'v1' };
  }

  formatSignatureHeader(headers: SignatureHeaders): string {
    return `t=${headers.timestamp},${headers.scheme}=${headers.signature}`;
  }

  verifySignature(params: {
    body: string;
    header: string;
    secret: string;
    toleranceMs?: number;
  }): VerificationResult {
    const parts = params.header.split(',').reduce((acc, part) => {
      const [key, value] = part.split('=');
      acc[key] = value;
      return acc;
    }, {} as Record<string, string>);

    const timestamp = parts['t'];
    const receivedSig = parts[this.SIGNATURE_VERSION] || parts['v1'];

    if (!timestamp || !receivedSig) {
      return { valid: false, reason: 'Missing signature components' };
    }

    // Check timestamp tolerance
    const now = Date.now();
    const eventTime = parseInt(timestamp) * 1000;
    const tolerance = params.toleranceMs || WebhookSecurity.TOLERANCE_MS;

    if (Math.abs(now - eventTime) > tolerance) {
      return {
        valid: false,
        reason: `Timestamp outside tolerance: ${Math.abs(now - eventTime)}ms > ${tolerance}ms`,
      };
    }

    // Verify signature (constant-time comparison)
    const signedPayload = `${timestamp}.${params.body}`;
    const expectedSig = crypto.createHmac('sha256', params.secret).update(signedPayload).digest('hex');

    const valid = crypto.timingSafeEqual(
      Buffer.from(expectedSig, 'hex'),
      Buffer.from(receivedSig, 'hex')
    );

    if (!valid) {
      return { valid: false, reason: 'Signature mismatch' };
    }

    return { valid: true, reason: 'ok' };
  }

  // Support dual-key rotation: consumers can verify against both old and new secret
  verifyWithKeyRotation(params: {
    body: string;
    header: string;
    secrets: string[];         // [current, previous] during rotation
    toleranceMs?: number;
  }): VerificationResult {
    for (const secret of params.secrets) {
      const result = this.verifySignature({
        body: params.body,
        header: params.header,
        secret,
        toleranceMs: params.toleranceMs,
      });
      if (result.valid) return result;
    }
    return { valid: false, reason: 'No matching secret found' };
  }

  // Consumer-side: Express/Fastify middleware factory
  createVerificationMiddleware(secret: string, toleranceMs?: number) {
    return (req: Request, res: Response, next: NextFunction) => {
      const signatureHeader = req.headers['x-webhook-signature'] as string;
      if (!signatureHeader) {
        res.status(401).json({ error: 'Missing signature header' });
        return;
      }

      const rawBody = (req as any).rawBody;
      if (!rawBody) {
        res.status(400).json({ error: 'Missing raw body' });
        return;
      }

      const result = this.verifySignature({
        body: rawBody.toString(),
        header: signatureHeader,
        secret,
        toleranceMs,
      });

      if (!result.valid) {
        logger.warn('Webhook verification failed', {
          ip: req.ip,
          path: req.path,
          reason: result.reason,
        });
        res.status(401).json({ error: `Webhook verification failed: ${result.reason}` });
        return;
      }

      next();
    };
  }

  // Key rotation support: generate new secret, keep old for transition period
  async rotateSecret(endpointId: string): Promise<{ newSecret: string; oldSecret: string }> {
    const endpoint = await this.db.webhookEndpoints.find(endpointId);
    const oldSecret = endpoint.secret;
    const newSecret = crypto.randomBytes(32).toString('hex');

    endpoint.secret = newSecret;
    endpoint.previousSecret = oldSecret;
    endpoint.secretRotatedAt = new Date();

    await this.db.webhookEndpoints.update(endpoint);

    // Notify consumer of new secret (outside band, e.g., via dashboard notification)
    await this.notifyConsumerSecretRotation(endpoint, newSecret);

    return { newSecret, oldSecret };
  }

  getEgressIPRanges(): string[] {
    // Return current cloud provider egress CIDR ranges
    return [
      '203.0.113.0/24',   // Example ranges
      '198.51.100.0/24',
    ];
  }
}

// Consumer verification utility (published as SDK)
class WebhookConsumer {
  static verifyEvent(
    body: string,
    signatureHeader: string,
    secret: string,
    options?: { toleranceMs?: number }
  ): boolean {
    const security = new WebhookSecurity();
    const result = security.verifySignature({
      body,
      header: signatureHeader,
      secret,
      toleranceMs: options?.toleranceMs,
    });
    return result.valid;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| crypto (Node.js built-in) | Node.js | HMAC-SHA256 |
| ip-range-check (MIT) | Node.js | CIDR matching |

## Production Considerations

**Scaling:** Signature generation is CPU-light (microseconds per sign). No special scaling considerations beyond normal webhook throughput. The major scaling factor is secret rotation — rotating secrets for thousands of endpoints should be batched and rate-limited to avoid database load. Publish egress IP ranges to a well-known URL that consumers can poll or subscribe to changes via a notification webhook.

**Security:** Secrets must be generated using cryptographically secure randomness (crypto.randomBytes). Secrets are stored encrypted at rest and decrypted only in memory for the duration of signing. Never log secrets or full signatures. Implement constant-time comparison (crypto.timingSafeEqual) to prevent timing attacks. Support webhook endpoint URL validation to prevent SSRF — validate URLs against an allowlist of schemes (https only) and host patterns.

**Monitoring:** Track verification success/failure rates by endpoint, signature version distribution, timestamp tolerance violations (events outside the window), secret rotation events, and IP allowlisting usage. Alert on high verification failure rates (potential attack or misconfiguration), sudden spikes in out-of-tolerance events (clock skew issues), and expired secrets (secrets older than 2 years). Log all verification failures with reason and source IP for security auditing.
