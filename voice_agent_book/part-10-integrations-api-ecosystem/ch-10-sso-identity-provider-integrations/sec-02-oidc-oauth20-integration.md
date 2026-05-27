# Section 02: OpenID Connect / OAuth 2.0 Integration

## Overview

OpenID Connect (OIDC) integration enables the voice agent platform to act as a Relying Party (RP) for OIDC-compliant Identity Providers, including Google Workspace, Microsoft Azure AD (implementing OIDC alongside SAML), Auth0, Cognito, and generic OIDC providers. OIDC provides a modern, REST-based SSO protocol using JSON Web Tokens (JWT) instead of SAML XML assertions, making it simpler to implement and debug than SAML.

The OIDC integration implements the Authorization Code flow with PKCE (Proof Key for Code Exchange) for public clients and the Authorization Code flow with client secret for confidential clients. The flow: redirect the user to the IdP's authorization endpoint, receive an authorization code, exchange it for an ID token and access token at the token endpoint, validate the ID token (signature, issuer, audience, nonce, expiry), extract user claims from the ID token and/or UserInfo endpoint, and create/update the local user account.

## Architecture

```
                 OIDC SSO Flow

   User → Platform → IdP Auth URL → Platform → User
              |                        |
   +----------------------------------------------------------+
   |              OIDC Integration Components                 |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | OpenID Discovery |  | Authorization     |            |
   |  | • .well-known    |  | • Auth code flow  |            |
   |  |   config fetch   |  | • PKCE support    |            |
   |  | • JWKS endpoint  |  | • Scope mapping   |            |
   |  | • Issuer         |  | • Redirect URI    |            |
   |  |   validation     |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Token Exchange   |  | ID Token          |             |
   |  | • Auth code →    |  | Validation        |            |
   |  |   tokens         |  | • JWT signature   |            |
   |  | • Client auth    |  | • Issuer (iss)    |            |
   |  | • Token refresh  |  | • Audience (aud)  |            |
   |  | • Token revoke   |  | • Nonce           |            |
   |  +------------------+  | • Expiry (exp)    |            |
   |  +------------------+  +-------------------+            |
   |  | Claim Mapping    |  +-------------------+            |
   |  | • Subject → user |  | UserInfo Endpoint |             |
   |  | • Email/name     |  | • Additional      |            |
   |  | • Groups/roles   |  |   claims fetch    |            |
   |  | • Custom claims  |  | • Bearer token    |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Authorization Code with PKCE for all client types over implicit flow:** PKCE (Proof Key for Code Exchange) is mandatory for all OIDC flows, even confidential clients that could use the authorization code flow alone. PKCE prevents authorization code interception attacks by binding the authorization code to the client's code verifier. The implicit flow (returning tokens directly from the authorization endpoint) is deprecated and not supported. Trade-off: PKCE adds a code challenge/verifier generation step but eliminates an entire class of OAuth security vulnerabilities.

- **ID token as primary identity source with UserInfo fallback:** The ID token (JWT) contains the core user claims (sub, email, name) and is verified locally using the IdP's JWKS (JSON Web Key Set). The UserInfo endpoint is called only if additional claims are needed that are not in the ID token. This reduces network round trips during login. The ID token is preferred because it is signed and can be verified without additional API calls. Trade-off: ID tokens have a size limit and may not contain all desired claims, requiring a UserInfo call for some IdPs.

- **Dynamic OIDC discovery over hard-coded endpoints:** The integration fetches the IdP's OpenID Connect Discovery Document from the `/.well-known/openid-configuration` URL. This document provides all OIDC endpoints (authorization, token, userinfo, jwks, end_session) and supported features (scopes, claims, response types). This eliminates hard-coded endpoint URLs and enables support for any OIDC-compliant IdP without per-IdP configuration. Trade-off: dynamic discovery requires an additional HTTP request during configuration and relies on IdP uptime for initial setup.

## Implementation Approach

```
interface OIDCConfig {
  issuer: string;
  clientId: string;
  clientSecret?: string;  // Optional for public clients
  redirectUri: string;
  scopes: string[];        // Default: ['openid', 'email', 'profile']
  enablePKCE: boolean;
  claimMapping: {
    sub: string;           // Platform user ID field
    email?: string;
    name?: string;
    preferred_username?: string;
    groups?: string;
    [key: string]: string | undefined;
  };
  tokenEndpointAuthMethod?: 'client_secret_basic' | 'client_secret_post' | 'none';
}

class OIDCSSOService {
  private discoveryCache = new Map<string, OIDCDiscovery>();

  async getAuthorizationUrl(tenantId: string): Promise<{ url: string; state: string; codeVerifier?: string }> {
    const config = await this.getTenantConfig(tenantId);
    const discovery = await this.fetchDiscovery(config.issuer);

    const state = crypto.randomUUID();
    let codeChallenge: string | undefined;
    let codeVerifier: string | undefined;

    if (config.enablePKCE) {
      codeVerifier = this.generateCodeVerifier();
      codeChallenge = await this.generateCodeChallenge(codeVerifier);
    }

    const params = new URLSearchParams({
      response_type: 'code',
      client_id: config.clientId,
      redirect_uri: config.redirectUri,
      scope: config.scopes.join(' '),
      state,
      nonce: crypto.randomUUID(),
    });

    if (codeChallenge) {
      params.set('code_challenge', codeChallenge);
      params.set('code_challenge_method', 'S256');
    }

    const url = `${discovery.authorization_endpoint}?${params.toString()}`;

    // Store state for verification
    await this.db.oidcStates.insert({ state, tenantId, codeVerifier, expiresAt: new Date(Date.now() + 600000) });

    return { url, state, codeVerifier };
  }

  async handleCallback(tenantId: string, params: {
    code: string;
    state: string;
  }): Promise<SSOResult> {
    const config = await this.getTenantConfig(tenantId);
    const discovery = await this.fetchDiscovery(config.issuer);

    // Verify state
    const storedState = await this.db.oidcStates.findOne({ state: params.state, tenantId });
    if (!storedState) throw new Error('Invalid state parameter');
    if (storedState.expiresAt < new Date()) throw new Error('State parameter expired');
    await this.db.oidcStates.delete(storedState.id);

    // Exchange code for tokens
    const tokenParams = new URLSearchParams({
      grant_type: 'authorization_code',
      code: params.code,
      redirect_uri: config.redirectUri,
      client_id: config.clientId,
    });

    if (config.clientSecret) {
      if (config.tokenEndpointAuthMethod === 'client_secret_basic') {
        // Basic auth header
      } else {
        tokenParams.set('client_secret', config.clientSecret);
      }
    }

    if (storedState.codeVerifier) {
      tokenParams.set('code_verifier', storedState.codeVerifier);
    }

    const authHeader = config.tokenEndpointAuthMethod === 'client_secret_basic'
      ? `Basic ${Buffer.from(`${config.clientId}:${config.clientSecret}`).toString('base64')}`
      : undefined;

    const tokenResponse = await axios.post(discovery.token_endpoint, tokenParams.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        ...(authHeader ? { 'Authorization': authHeader } : {}),
      },
    });

    const { id_token, access_token } = tokenResponse.data;

    // Validate ID token
    const jwks = await this.fetchJWKS(discovery.jwks_uri);
    const idToken = await this.validateIDToken(id_token, {
      issuer: discovery.issuer,
      clientId: config.clientId,
      jwks,
    });

    // Extract claims
    const claims = this.mapClaims(idToken.claims, config.claimMapping);

    // Fetch UserInfo if needed
    if (!claims.email && access_token) {
      const userInfo = await axios.get(discovery.userinfo_endpoint, {
        headers: { 'Authorization': `Bearer ${access_token}` },
      });
      Object.assign(claims, {
        email: userInfo.data.email,
        name: userInfo.data.name,
      });
    }

    // Create or update user
    const user = await this.userService.findOrCreateSSOUser({
      tenantId,
      idpUserId: idToken.claims.sub,
      email: claims.email,
      name: claims.name,
      groups: claims.groups,
      idp: 'oidc',
      idpMetadata: { issuer: discovery.issuer, sub: idToken.claims.sub },
    });

    // Create session
    const session = await this.sessionService.createSession({
      userId: user.id,
      tenantId,
      authMethod: 'oidc',
    });

    return { user, session, claims };
  }

  private async validateIDToken(idToken: string, params: {
    issuer: string; clientId: string; jwks: JWKS;
  }): Promise<{ claims: any }> {
    const decoded = jwt.decode(idToken, { complete: true });
    const header = decoded.header;
    const payload = decoded.payload;

    // Verify signature
    const key = this.findJWK(params.jwks, header.kid);
    if (!key) throw new Error('JWK not found for kid');
    const publicKey = jwktopem(key);
    jwt.verify(idToken, publicKey, {
      issuer: params.issuer,
      audience: params.clientId,
      clockTolerance: 60,
    });

    // Verify nonce if stored
    const nonce = payload.nonce;
    if (nonce) {
      const stored = await this.db.oidcNonces.findOne({ nonce });
      if (!stored) throw new Error('Invalid nonce');
      await this.db.oidcNonces.delete(stored.id);
    }

    return { claims: payload };
  }

  private generateCodeVerifier(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    let verifier = '';
    for (let i = 0; i < 128; i++) {
      verifier += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return verifier;
  }

  private async generateCodeChallenge(verifier: string): Promise<string> {
    const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
    return Buffer.from(hash).toString('base64url');
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| jsonwebtoken (MIT) | Node.js | JWT verification |
| jwks-rsa (MIT) | Node.js | JWKS fetching + key conversion |
| node-jose (Apache 2.0) | Node.js | JOSE/JWT implementation |

## Production Considerations

**Scaling:** OIDC authentication is low-volume like SAML. The JWKS should be cached for the cache-control max-age from the JWKS endpoint (typically 1 hour). ID token verification is CPU-light (RSA/JWT verification). The OIDC state store must be shared across instances (use Redis with TTL matching the state expiry). Token refresh flows create moderate load — batch refresh token rotation to avoid race conditions.

**Security:** Strictly validate the ID token issuer (must match the configured issuer exactly), audience (must include the client ID), and expiry. Use the nonce to prevent replay attacks. Store OIDC states with short TTL (10 minutes). The authorization code must be exchanged within 60 seconds (most IdPs enforce this). Support token revocation (IdP's revocation_endpoint) for logout. Never log the client secret or access tokens.

**Monitoring:** Track OIDC authentication success rates, IDP response times, JWKS fetch frequency, token validation failure reasons (signature, expiry, issuer, audience), and userinfo endpoint calls. Alert on authentication failure rates exceeding 5%, JWKS fetch failures, and certificate expiry (JWK key rotation issues). Monitor the OIDC discovery document health — an unreachable discovery URL blocks new login configurations.
