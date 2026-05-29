# Section 03: Payload Signing & Verification

## Overview

Webhook payloads are signed with HMAC-SHA256 to verify authenticity and integrity. Consumers verify signatures using a shared secret to ensure the payload originated from the platform and hasn't been tampered with. Signature headers, replay attack prevention, and key rotation provide comprehensive security.

## Architecture

```
Payload Signing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Platform]                              [Consumer]
     │                                       │
  Event JSON                             Receive webhook
     │                                       │
  Stringify payload → JSON.stringify     Extract signature
     │                                  from header
  Compute HMAC-SHA256                        │
  (payload + timestamp + secret)         Recompute HMAC
     │                                  with stored secret
  Set headers:                               │
  X-Signature-256: <hmac>               Compare signatures
  X-Timestamp: <unix_ts>                     │
  X-Webhook-ID: <uuid>                  If match → process
     │                                  If no match → reject
  Send POST request
     │
[Consumer receives]

Replay Attack Prevention:
  Consumer checks X-Timestamp is within 5 minutes
  of current time — rejects old deliveries

Key Rotation:
  Two active keys: primary + secondary
  Roll: add new key as secondary → swap → remove old
  No downtime during rotation
```

## Design Decisions

- **HMAC-SHA256**: Industry standard for payload signing
- **Timestamp Binding**: Prevents replay attacks
- **Dual-Key Rotation**: Zero-downtime secret rotation
- **Signature in Header**: Doesn't modify original payload

## Implementation Approach

```typescript
interface SignatureHeaders {
  signature: string;
  timestamp: string;
  webhookId: string;
  version: string;
}

class WebhookSigner {
  sign(payload: Record<string, unknown>, secret: string, webhookId: string): SignatureHeaders {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const version = 'v1';

    const signedPayload = `${version}.${timestamp}.${webhookId}.${JSON.stringify(payload)}`;
    const signature = crypto
      .createHmac('sha256', secret)
      .update(signedPayload)
      .digest('hex');

    return { signature, timestamp, webhookId, version };
  }

  verify(
    payload: Record<string, unknown>,
    headers: SignatureHeaders,
    secret: string,
    toleranceMs: number = 300000, // 5 minutes
  ): boolean {
    // Check timestamp freshness (replay protection)
    const timestampMs = parseInt(headers.timestamp, 10) * 1000;
    const now = Date.now();
    if (Math.abs(now - timestampMs) > toleranceMs) {
      return false; // Timestamp outside tolerance window
    }

    // Recompute signature
    const signedPayload = `${headers.version}.${headers.timestamp}.${headers.webhookId}.${JSON.stringify(payload)}`;
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(signedPayload)
      .digest('hex');

    // Constant-time comparison prevents timing attacks
    return crypto.timingSafeEqual(
      Buffer.from(expectedSignature, 'hex'),
      Buffer.from(headers.signature, 'hex'),
    );
  }
}

class SecretRotationManager {
  async rotateSecret(endpointId: string): Promise<void> {
    const endpoint = await this.getEndpoint(endpointId);
    const newSecret = crypto.randomBytes(32).toString('hex');

    // Phase 1: Add new secret as secondary
    await this.db.update('webhook_endpoints', { id: endpointId }, {
      secondarySecret: newSecret,
      rotationStatus: 'in_progress',
      rotationStartedAt: new Date(),
    });

    // Wait for consumers to update (grace period)
    await new Promise(resolve => setTimeout(resolve, 24 * 60 * 60 * 1000));

    // Phase 2: Promote secondary to primary
    await this.db.update('webhook_endpoints', { id: endpointId }, {
      secret: newSecret,
      secondarySecret: null,
      rotationStatus: 'completed',
      rotationCompletedAt: new Date(),
    });
  }

  async signWithRotation(
    payload: Record<string, unknown>,
    endpoint: WebhookEndpoint,
    webhookId: string,
  ): Promise<SignatureHeaders> {
    // Sign with primary secret
    const signer = new WebhookSigner();
    const headers = signer.sign(payload, endpoint.secret, webhookId);

    // If rotation in progress, also include secondary signature
    if (endpoint.rotationStatus === 'in_progress' && endpoint.secondarySecret) {
      const secondaryHeaders = signer.sign(payload, endpoint.secondarySecret, webhookId);
      return {
        ...headers,
        signature: `${headers.signature},${secondaryHeaders.signature}`,
        version: 'v1,v1',
      };
    }

    return headers;
  }
}

// Consumer-side verification SDK
class WebhookVerifier {
  private currentSecret: string;
  private previousSecrets: string[] = [];

  verify(
    payload: Record<string, unknown>,
    rawSignature: string,
    timestamp: string,
    webhookId: string,
    version: string,
    toleranceMs = 300000,
  ): boolean {
    const signer = new WebhookSigner();

    // Try current secret first
    const currentResult = signer.verify(
      payload,
      { signature: rawSignature, timestamp, webhookId, version },
      this.currentSecret,
      toleranceMs,
    );

    if (currentResult) return true;

    // Try previous secrets (during rotation)
    for (const prevSecret of this.previousSecrets) {
      const result = signer.verify(
        payload,
        { signature: rawSignature, timestamp, webhookId, version },
        prevSecret,
        toleranceMs,
      );
      if (result) return true;
    }

    return false;
  }

  rotateSecret(newSecret: string): void {
    this.previousSecrets.push(this.currentSecret);
    // Keep only last 2 previous secrets
    if (this.previousSecrets.length > 2) {
      this.previousSecrets.shift();
    }
    this.currentSecret = newSecret;
  }
}
```

## Integration Points

- **Webhook Delivery**: Signer integrated into delivery worker
- **Consumer SDK**: Verifier distributed in consumer SDK package
- **Key Management**: Secrets stored in encrypted database or vault

## Production Considerations

- **Timestamp Tolerance**: 5 minute window to account for clock skew
- **Secret Strength**: 256-bit random secrets (64 hex chars)
- **Rotation Grace Period**: 24 hours for consumers to update
- **Failed Verification Log**: Log all verification failures for security audit

## Open-Source Tools

- **Node.js crypto**: HMAC, random bytes, timing-safe comparison
- **HashiCorp Vault**: Secret storage and rotation
