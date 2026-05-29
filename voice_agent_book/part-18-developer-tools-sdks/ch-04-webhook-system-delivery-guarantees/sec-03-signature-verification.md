# Section 03: Signature Verification

## Overview

Every webhook payload is signed with HMAC-SHA256 using a per-endpoint secret key. The signature is delivered in the `X-VoiceAgent-Signature` header, allowing receivers to verify that the webhook originated from the Voice Agent platform and was not tampered with during transit. Signature verification is a critical security control for webhook receivers.

## Architecture

```
Signing Process
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Server Signs:
  Payload: JSON.stringify(event_body)
  Timestamp: current_unix_timestamp
  Secret: endpoint-specific shared secret

  Signing String:
    timestamp + '.' + payload

  Signature = HMAC-SHA256(secret, signing_string)

  Headers:
    X-VoiceAgent-Signature: sha256=<hex_encoded_signature>
    X-VoiceAgent-Timestamp: <unix_timestamp>

Client Verifies:
  1. Extract signature from header
  2. Extract timestamp from header
  3. Check timestamp freshness (within 5 minutes)
  4. Recompute HMAC-SHA256 with stored secret
  5. Compare signatures (constant-time)

Secret Rotation:
  ┌────────┐    ┌─────────┐    ┌────────┐
  │Secret A│───▶│Rotation │───▶│Secret B│
  │(active)│    │Trigger  │    │(active)│
  └────────┘    └─────────┘    └────────┘
       │                            │
  Old secret kept for 48h     New secret in use
  for verification lag

  Rotation notification sent via webhook:
  {
    "type": "webhook.secret_rotated",
    "data": {
      "endpoint_id": "wh_abc_123",
      "rotated_at": "2025-06-01T00:00:00Z",
      "old_secret_expires_at": "2025-06-03T00:00:00Z"
    }
  }
```

## Design Decisions

- **HMAC-SHA256**: Strong, widely supported, and efficient for webhook payload signing
- **Timestamp in Signature**: Prevents replay attacks — signature includes timestamp; receiver validates freshness
- **Per-Endpoint Secrets**: Each webhook endpoint has a unique secret; compromise of one endpoint doesn't affect others
- **Secret Rotation**: Secrets auto-rotated every 90 days; old secret retained for 48 hours for verification lag

## Implementation Approach

```typescript
import crypto from 'node:crypto';

// Webhook signer
class WebhookSigner {
  sign(payload: string, secret: string): { signature: string; timestamp: number } {
    const timestamp = Math.floor(Date.now() / 1000);
    const signingString = `${timestamp}.${payload}`;

    const signature = crypto
      .createHmac('sha256', secret)
      .update(signingString)
      .digest('hex');

    return { signature, timestamp };
  }

  verify(
    payload: string,
    signature: string,
    timestamp: number,
    secret: string,
    maxAgeSeconds = 300,
  ): boolean {
    // Check timestamp freshness
    const now = Math.floor(Date.now() / 1000);
    if (now - timestamp > maxAgeSeconds) {
      return false; // Too old — possible replay
    }

    if (timestamp > now + 30) {
      return false; // Future timestamp — clock skew or tampering
    }

    // Recompute signature
    const signingString = `${timestamp}.${payload}`;
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(signingString)
      .digest('hex');

    // Constant-time comparison
    return crypto.timingSafeEqual(
      Buffer.from(expectedSignature),
      Buffer.from(signature),
    );
  }
}

// Webhook headers extraction
interface SignedWebhookHeaders {
  signature: string;
  timestamp: number;
  eventId: string;
  deliveryAttempt: number;
  idempotencyKey: string;
}

function extractWebhookHeaders(headers: Record<string, string | string[] | undefined>): SignedWebhookHeaders {
  const getHeader = (name: string): string => {
    const value = headers[name] || headers[name.toLowerCase()];
    return Array.isArray(value) ? value[0] : (value || '');
  };

  const signatureHeader = getHeader('X-VoiceAgent-Signature');
  const signature = signatureHeader.replace('sha256=', '');

  return {
    signature,
    timestamp: parseInt(getHeader('X-VoiceAgent-Timestamp'), 10),
    eventId: getHeader('X-VoiceAgent-Event-Id'),
    deliveryAttempt: parseInt(getHeader('X-VoiceAgent-Delivery-Attempt'), 10),
    idempotencyKey: getHeader('X-VoiceAgent-Idempotency-Key'),
  };
}

// Verification middleware (for receiver side)
function webhookVerificationMiddleware(getSecret: (endpointId: string) => Promise<string>) {
  return async (req: Request, res: Response, next: Next) => {
    const rawBody = await req.text();
    const headers = extractWebhookHeaders(req.headers as Record<string, string>);

    // Determine which secret to use (support rotation)
    const secret = await getSecret(headers.eventId);

    const signer = new WebhookSigner();
    const isValid = signer.verify(
      rawBody,
      headers.signature,
      headers.timestamp,
      secret,
    );

    if (!isValid) {
      return res.status(401).json({
        error: {
          code: 'WEBHOOK_VERIFICATION_FAILED',
          message: 'Webhook signature verification failed',
        },
      });
    }

    req.webhookContext = { ...headers, rawBody };
    next();
  };
}

// SDK verification helper
class WebhookVerifier {
  private signer = new WebhookSigner();

  verify(
    body: string,
    signatureHeader: string,
    timestampHeader: string,
    secret: string,
  ): boolean {
    const signature = signatureHeader.replace('sha256=', '');
    const timestamp = parseInt(timestampHeader, 10);

    return this.signer.verify(body, signature, timestamp, secret);
  }
}
```

## Integration Points

- **End-User SDK**: WebhookVerifier utility provided in SDK for easy signature verification
- **Developer Portal**: Secret management UI with copy-to-clipboard and rotation controls
- **Security Monitoring**: Failed verification attempts logged and alerted for potential abuse

## Production Considerations

- **Secret Storage**: Webhook secrets stored encrypted at rest; access controlled via IAM
- **Replay Attack Prevention**: Include timestamp in signature; reject webhooks older than 5 minutes
- **Key Rotation**: Automated rotation every 90 days; notify customers 7 days before rotation
- **Multiple Active Secrets**: Support two simultaneous secrets during rotation period for zero-downtime key transition

## Open-Source Tools

- **Node crypto**: Built-in HMAC-SHA256 for webhook signing
- **TweetNaCl**: Alternative for Ed25519 signature scheme (if asymmetric signing preferred)
