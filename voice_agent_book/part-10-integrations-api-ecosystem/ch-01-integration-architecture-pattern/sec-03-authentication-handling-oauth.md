# Section 03: Authentication Handling & OAuth

## Overview

Authentication handling manages the secure exchange of credentials between the voice platform and external APIs. The system supports multiple authentication methods: OAuth 2.0 (the most common for modern APIs), API keys (for simpler integrations), basic authentication (for legacy systems), and mutual TLS (for high-security enterprise integrations). Each method requires different handling for credential storage, token lifecycle management, refresh flows, and error recovery.

OAuth 2.0 is the most complex authentication protocol to handle. It involves authorization code grants (for user-delegated access), client credentials grants (for server-to-server), refresh tokens (for long-lived access), and PKCE (for public clients). The authentication handler must manage the complete OAuth lifecycle: initiating the authorization flow, exchanging authorization codes for tokens, storing tokens securely, detecting expired tokens, refreshing tokens transparently, and handling revocation. The system also manages multiple OAuth configurations per tenant (different integrations may use different OAuth providers).

## Architecture

```
                  Authentication Handling Architecture

   +------------------------------------------------------+
   |              Authentication Manager                   |
   |                                                      |
   |  +------------------+  +-------------------------+   |
   |  | Auth Method      |  | Token Vault             |   |
   |  | Selector         |  | (Encrypted Storage)     |   |
   |  | • OAuth2         |  | • Access tokens         |   |
   |  | • API Key        |  | • Refresh tokens        |   |
   |  | • Basic Auth     |  | • Client credentials    |   |
   |  | • Mutual TLS     |  | • Expiry tracking       |   |
   |  +------------------+  +-------------------------+   |
   |  +------------------+  +-------------------------+   |
   |  | Token Refresher  |  | Auth Error Handler     |   |
   |  | • Proactive      |  | • 401 interception     |   |
   |  |   refresh        |  | • Token expiry recovery|   |
   |  | • Reactive       |  | • Auth failure         |   |
   |  |   refresh        |  |   classification       |   |
   |  +------------------+  +-------------------------+   |
   +------------------------------------------------------+
```

## Design Decisions

- **Proactive token refresh with jitter over reactive refresh:** Tokens are refreshed before they expire (at 80% of TTL) rather than waiting for a 401 response. This prevents request failures caused by expired tokens and reduces latency (no need for retry on 401). A random jitter (+/- 10% of TTL) is added to refresh timing to prevent thundering herd when multiple instances refresh simultaneously. Trade-off: proactive refresh uses more API calls if tokens would have expired naturally without use.

- **Encrypted token vault with envelope encryption:** Tokens are encrypted at rest using AES-256-GCM with a key encryption key (KEK) stored in a hardware security module (HSM) or cloud KMS. The data encryption key (DEK) is generated per-token and encrypted with the KEK. This provides strong encryption with the ability to rotate the KEK without re-encrypting all tokens. Trade-off: envelope encryption adds latency to token retrieval (two decryption operations) and depends on KMS availability.

- **Multi-tenant credential isolation with shared infrastructure:** Each tenant's credentials are stored in a separate encryption context (different KEK or different DEK). The authentication manager enforces that tenant A cannot access tenant B's tokens. However, the authentication infrastructure (OAuth endpoints, token refresh logic) is shared across tenants for operational efficiency. Trade-off: shared infrastructure means a vulnerability in the refresh logic could theoretically affect all tenants, requiring rigorous testing.

## Implementation Approach

```
type AuthMethod = 'oauth2' | 'api_key' | 'basic' | 'mtls';

interface AuthCredentials {
  method: AuthMethod;
  tenantId: string;
  integrationId: string;
  // OAuth2
  clientId?: string;
  clientSecret?: string;  // Encrypted
  accessToken?: string;    // Encrypted
  refreshToken?: string;   // Encrypted
  tokenExpiry?: number;
  // API Key
  apiKey?: string;         // Encrypted
  // Basic Auth
  username?: string;
  password?: string;       // Encrypted
  // Mutual TLS
  cert?: string;           // Encrypted
  key?: string;            // Encrypted
}

class AuthenticationManager {
  constructor(private vault: TokenVault, private httpClient: HttpClient) {}

  async getAuthHeader(integrationId: string, tenantId: string): Promise<string> {
    const credentials = await this.vault.getCredentials(integrationId, tenantId);

    if (credentials.method === 'oauth2') {
      return this.getOAuthHeader(credentials);
    }
    if (credentials.method === 'api_key') {
      return `Bearer ${credentials.apiKey}`;
    }
    if (credentials.method === 'basic') {
      const encoded = Buffer.from(`${credentials.username}:${credentials.password}`).toString('base64');
      return `Basic ${encoded}`;
    }
    throw new Error(`Unsupported auth method: ${credentials.method}`);
  }

  private async getOAuthHeader(credentials: AuthCredentials): Promise<string> {
    if (this.isTokenExpiring(credentials.tokenExpiry)) {
      await this.refreshToken(credentials);
    }
    return `Bearer ${credentials.accessToken}`;
  }

  private isTokenExpiring(expiry: number): boolean {
    const bufferPeriod = (expiry - Date.now()) * 0.2;  // Refresh at 80% TTL
    return Date.now() + bufferPeriod >= expiry;
  }

  private async refreshToken(credentials: AuthCredentials): Promise<void> {
    const response = await this.httpClient.post(credentials.tokenEndpoint, {
      grant_type: 'refresh_token',
      refresh_token: credentials.refreshToken,
      client_id: credentials.clientId,
      client_secret: credentials.clientSecret
    });
    await this.vault.updateTokens(
      credentials.integrationId,
      credentials.tenantId,
      response.data.access_token,
      response.data.refresh_token || credentials.refreshToken,
      Date.now() + response.data.expires_in * 1000
    );
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **OAuth.js** (MIT) | Node.js | OAuth2 client library |
| **simple-oauth2** (MIT) | Node.js | OAuth2 flow handling |
| **node-vault** (MIT) | Node.js | HashiCorp Vault client |
| **AWS KMS SDK** (Apache 2.0) | Encryption | Key management |

## Production Considerations

**Scaling:** Token refresh operations are I/O-bound network calls. Use a connection pool for token endpoints. Implement token caching in memory with a short TTL (30 seconds) to avoid redundant decrypt operations. For high-throughput integrations, pre-warm tokens by refreshing before they expire across all instances.

**Security:** Never log tokens or secrets. Implement token binding where possible (pin tokens to client certificates). Monitor for unusual token usage patterns that might indicate token theft. Support token revocation flows when a tenant disables an integration. Rotate client secrets periodically.

**Monitoring:** Track token refresh success rate (should be > 99%), time to token expiry across all active tokens, token refresh latency (p95 < 500ms), auth failure reasons (expired, invalid, revoked, insufficient scope). Alert on refresh failures exceeding 5%, tokens expiring within 1 hour, and any authentication errors after refresh attempt.
