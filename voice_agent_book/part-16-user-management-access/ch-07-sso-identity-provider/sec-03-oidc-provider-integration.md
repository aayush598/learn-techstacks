# OIDC Provider Integration

## Overview

OpenID Connect (OIDC) extends OAuth 2.0 with an identity layer, providing a simpler JSON-based alternative to SAML. OIDC uses JWTs (ID tokens) for user identity verification and supports the authorization code flow with PKCE.

## Discovery & Configuration

```typescript
interface OidcMetadata {
  provider: string;
  issuer: string;
  authorizationEndpoint: string;
  tokenEndpoint: string;
  userinfoEndpoint: string;
  jwksUri: string;
  scopesSupported: string[];
  claimsSupported: string[];
  idTokenSigningAlgValuesSupported: string[];
}

class OidcDiscoveryService {
  async discover(issuerUrl: string): Promise<OidcMetadata> {
    const wellKnownUrl = `${issuerUrl.replace(/\/$/, '')}/.well-known/openid-configuration`;
    const response = await fetch(wellKnownUrl);
    const config = await response.json();

    return {
      provider: config.issuer,
      issuer: config.issuer,
      authorizationEndpoint: config.authorization_endpoint,
      tokenEndpoint: config.token_endpoint,
      userinfoEndpoint: config.userinfo_endpoint,
      jwksUri: config.jwks_uri,
      scopesSupported: config.scopes_supported,
      claimsSupported: config.claims_supported,
      idTokenSigningAlgValuesSupported: config.id_token_signing_alg_values_supported,
    };
  }
}
```

## Authorization Code Flow

```typescript
class OidcAuthService {
  async generateAuthUrl(config: OidcConfig, state: string, nonce: string): Promise<string> {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: config.clientId,
      redirect_uri: `${process.env.APP_URL}/auth/oidc/callback`,
      scope: 'openid email profile',
      state,
      nonce,
    });

    return `${config.authorizationEndpoint}?${params}`;
  }

  async handleCallback(code: string, state: string, expectedState: string): Promise<AuthResult> {
    if (state !== expectedState) {
      return { success: false, error: 'State mismatch - possible CSRF' };
    }

    // Exchange code for tokens
    const tokenResponse = await this.exchangeCode(code);
    const idToken = this.decodeIdToken(tokenResponse.id_token);

    // Validate ID token
    if (!this.validateIdToken(idToken, tokenResponse.id_token)) {
      return { success: false, error: 'ID token validation failed' };
    }

    // Get user info
    const userInfo = await this.getUserInfo(tokenResponse.access_token);

    // Find or create user
    const email = userInfo.email || idToken.email;
    let user = await this.userService.findByEmail(email, currentTenant);
    if (!user) {
      if (config.provisioning.jit) {
        user = await this.jitProvisioning.provisionUser({
          email, firstName: userInfo.given_name, lastName: userInfo.family_name,
        }, config);
      }
    }

    return { success: true, user, tokens: tokenResponse };
  }

  private async exchangeCode(code: string): Promise<TokenResponse> {
    const response = await fetch(config.tokenEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        client_id: config.clientId,
        client_secret: config.clientSecret,
        redirect_uri: `${process.env.APP_URL}/auth/oidc/callback`,
      }),
    });
    return response.json();
  }

  private validateIdToken(token: any, rawJwt: string): boolean {
    // Verify signature using JWKS
    // Verify issuer matches expected
    if (token.iss !== config.issuer) return false;
    // Verify audience
    if (!token.aud.includes(config.clientId)) return false;
    // Verify expiry
    if (token.exp < Math.floor(Date.now() / 1000)) return false;
    // Verify nonce
    if (token.nonce !== expectedNonce) return false;

    return true;
  }
}
```

## Open-Source Tools

- **openid-client** (MIT) — OIDC client implementation
- **jose** (MIT) — JWT signing and verification
- **NextAuth.js** (ISC) — Built-in OIDC provider support

## Production Considerations

- Use PKCE (Proof Key for Code Exchange) for mobile apps
- Cache JWKS keys with 24-hour TTL
- Support multiple OIDC providers per tenant
- Token refresh: use refresh_token to maintain session without re-auth
- Validate all ID token claims (iss, aud, exp, iat, nonce)
- Handle token expiration gracefully with refresh flow
- Log OIDC errors with correlation IDs for debugging
