# Section 06: Request Signing

## Overview

Request signing provides an additional layer of security for sensitive API operations. Clients sign requests using HMAC-SHA256 with their secret key, including a nonce and timestamp to prevent replay attacks. The server verifies the signature before processing the request. This is particularly important for webhook payload delivery and inter-service communication.

## Architecture

```
Request Signing Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Client Signing:
  Components:
    HTTP Method:   POST
    Path:          /v1/agents/:id/deploy
    Body:          {"agent_id":"ag_123"}
    Timestamp:     1684512345 (Unix time)
    Nonce:         n7kL3pQrStUvWxYz

  Signing String:
    POST
    /v1/agents/ag_123/deploy
    1684512345
    n7kL3pQrStUvWxYz
    {"agent_id":"ag_123"}

  Signature = HMAC-SHA256(secret, signing_string) → base64

  Headers:
    X-Signature-Timestamp: 1684512345
    X-Signature-Nonce: n7kL3pQrStUvWxYz
    X-Signature: aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789=

Server Verification:
  [Server] → Receive Request
    │
    ├── Check Timestamp (within 5 minutes)
    ├── Check Nonce (not reused)
    ├── Reconstruct signing string
    ├── Compute HMAC-SHA256 with stored secret
    └── Compare signatures (constant-time)
```

## Design Decisions

- **HMAC-SHA256**: Standard, widely supported algorithm with strong security properties
- **Timestamp Window**: 5-minute tolerance prevents replay while accommodating clock skew
- **Nonce + Timestamp Pair**: Nonce ensures uniqueness; timestamp bounds the replay window
- **Body Included in Signing**: Prevents tampering with request payload during transit

## Implementation Approach

```typescript
// Request signing utility
interface SignatureConfig {
  secret: string;
  algorithm?: string;
  maxTimestampAge?: number; // seconds
}

interface SignatureHeaders {
  'X-Signature-Timestamp': string;
  'X-Signature-Nonce': string;
  'X-Signature': string;
}

class RequestSigner {
  constructor(private config: SignatureConfig) {}

  sign(method: string, path: string, body: string): SignatureHeaders {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const nonce = crypto.randomBytes(16).toString('hex');

    const signingString = this.buildSigningString(method, path, timestamp, nonce, body);
    const signature = this.computeSignature(signingString);

    return {
      'X-Signature-Timestamp': timestamp,
      'X-Signature-Nonce': nonce,
      'X-Signature': signature,
    };
  }

  verify(
    method: string,
    path: string,
    headers: Record<string, string>,
    body: string,
  ): { valid: boolean; reason?: string } {
    const timestamp = headers['x-signature-timestamp'];
    const nonce = headers['x-signature-nonce'];
    const signature = headers['x-signature'];

    if (!timestamp || !nonce || !signature) {
      return { valid: false, reason: 'Missing signature headers' };
    }

    // Check timestamp freshness
    const now = Math.floor(Date.now() / 1000);
    const age = now - parseInt(timestamp);

    if (age > (this.config.maxTimestampAge || 300)) {
      return { valid: false, reason: 'Signature timestamp expired' };
    }

    if (age < 0) {
      return { valid: false, reason: 'Signature timestamp in future' };
    }

    // Check nonce reuse (against stored nonces)
    if (this.isNonceReused(nonce)) {
      return { valid: false, reason: 'Nonce already used' };
    }

    // Recompute signature
    const signingString = this.buildSigningString(method, path, timestamp, nonce, body);
    const expectedSignature = this.computeSignature(signingString);

    // Constant-time comparison
    if (!crypto.timingSafeEqual(
      Buffer.from(expectedSignature),
      Buffer.from(signature),
    )) {
      return { valid: false, reason: 'Signature mismatch' };
    }

    // Mark nonce as used
    this.recordNonce(nonce, parseInt(timestamp));

    return { valid: true };
  }

  private buildSigningString(
    method: string,
    path: string,
    timestamp: string,
    nonce: string,
    body: string,
  ): string {
    return [
      method.toUpperCase(),
      path,
      timestamp,
      nonce,
      body,
    ].join('\n');
  }

  private computeSignature(signingString: string): string {
    return crypto
      .createHmac('sha256', this.config.secret)
      .update(signingString)
      .digest('base64');
  }

  private nonceStore = new Map<string, number>();

  private isNonceReused(nonce: string): boolean {
    return this.nonceStore.has(nonce);
  }

  private recordNonce(nonce: string, timestamp: number): void {
    this.nonceStore.set(nonce, timestamp);
    // Clean up old nonces after 10 minutes
    const fiveMinutesAgo = Math.floor(Date.now() / 1000) - 300;
    for (const [key, ts] of this.nonceStore) {
      if (ts < fiveMinutesAgo) this.nonceStore.delete(key);
    }
  }
}

// Server-side verification middleware
function signatureVerification(config: SignatureConfig) {
  const signer = new RequestSigner(config);

  return async (c: Context, next: Next) => {
    const body = await c.req.text();
    const result = signer.verify(
      c.req.method,
      c.req.path,
      Object.fromEntries(c.req.raw.headers),
      body,
    );

    if (!result.valid) {
      throw new ApiErrorResponse(401, 'UNAUTHORIZED',
        `Request signature verification failed: ${result.reason}`);
    }

    await next();
  };
}
```

## Integration Points

- **Webhook Delivery**: Outgoing webhooks are signed so receivers can verify authenticity
- **Inter-Service Communication**: Internal microservice requests use signing for service-to-service auth
- **SDK**: Request signing is transparent in the SDK — users configure API key, SDK handles signing

## Production Considerations

- **Secret Rotation**: Rotate signing secrets regularly; support parallel validations during rotation using key IDs
- **Clock Skew Handling**: 5-minute window accommodates most clock skew scenarios
- **Nonce Storage**: For distributed systems, nonce deduplication requires shared Redis store
- **Body Caching**: Reading the body for verification caches it; ensure downstream handlers can access it

## Open-Source Tools

- **Node crypto**: Built-in HMAC-SHA256 implementation
- **Redis**: Shared nonce deduplication store for multi-instance deployments
