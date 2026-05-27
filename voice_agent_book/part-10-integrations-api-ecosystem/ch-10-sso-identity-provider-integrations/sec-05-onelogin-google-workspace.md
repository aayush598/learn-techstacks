# Section 05: OneLogin and Google Workspace

## Overview

OneLogin and Google Workspace integrations extend the platform's SSO support to two additional major identity providers. OneLogin is a popular standalone IdP for mid-market enterprises, offering SAML and OIDC support alongside user provisioning and MFA. Google Workspace (formerly G Suite) is the most widely used productivity suite, and its IdP capabilities enable organizations using Google Workspace to authenticate their users against the voice agent platform using their Google credentials.

Both integrations follow the same architectural pattern as the Okta and Entra ID integrations but are tuned to each provider's specific protocols, configuration workflows, and API capabilities. OneLogin supports both SAML (its primary protocol) and OIDC, while Google Workspace primarily supports OIDC through Google's Identity Platform. The integration provides provider-specific setup wizards, automated configuration (where APIs permit), and user provisioning via SCIM where available.

## Architecture

```
         OneLogin & Google Workspace Integration

   OneLogin/Google → Platform → Tenant → Platform → User
                          |
   +----------------------------------------------------------+
   |          OneLogin & Google Integration Components        |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Provider         |  | SSO Protocol      |            |
   |  | Detection        |  | • OneLogin: SAML  |            |
   |  | • Auto-detect    |  | • Google: OIDC    |            |
   |  |   provider type  |  | • Configurable    |            |
   |  | • Route to       |  | • Metadata import |            |
   |  |   proper handler |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | OneLogin API     |  | Google Identity    |            |
   |  | • Connector      |  | Platform API      |            |
   |  |   management     |  | • OAuth client    |            |
   |  | • User sync      |  |   creation        |            |
   |  | • Role mapping   |  | • Directory sync  |            |
   |  • MFA status       |  | • Domain-wide     |            |
   |  +------------------+  |   delegation      |            |
   |  +------------------+  +-------------------+            |
   |  | Provisioning     |  | Directory Sync    |             |
   |  | • SCIM (OneLogin)|  | • Google Workspace|            |
   |  | • JIT (both)     |  |   Directory API   |            |
   |  | • Group sync     |  | • Group/OU sync   |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **SAML-first for OneLogin, OIDC-first for Google Workspace:** OneLogin's strength and primary protocol is SAML 2.0 — their OIDC support is less mature. Google Workspace natively supports OIDC through Google's Identity Platform and does not support SAML for custom applications (Google supports SAML only for pre-integrated apps). The integration uses the provider-optimal protocol by default but allows override for advanced configurations. Trade-off: needing different default protocols for different providers adds complexity to the integration router but provides the most reliable authentication path for each provider.

- **Provider-specific setup wizards over generic SSO flow:** While all SSO integrations share common steps (metadata exchange, attribute mapping, test), the setup experience is tailored to each provider's specific configuration UI. OneLogin requires a Connector configuration (with specific field names like "ACS URL Validator" and "Audience" fields). Google Workspace requires OAuth consent screen configuration and OAuth client ID creation. The setup wizards include provider-specific screenshots, field references, and troubleshooting tips. Trade-off: provider-specific wizards require more maintenance but significantly reduce setup time and errors.

- **Google Workspace Directory API for user/group sync over token claims:** Google's ID token contains minimal claims (sub, email, name, hd — hosted domain). Full group membership and organizational unit information is fetched via Google Workspace Directory API (`https://admin.googleapis.com/admin/directory/v1/users` and `groups`). The integration requests the `https://www.googleapis.com/auth/admin.directory.user.readonly` and `admin.directory.group.readonly` scopes during the OAuth consent flow. Trade-off: Directory API requires domain-wide delegation or admin consent but provides complete organizational data.

## Implementation Approach

```
type SSOProvider = 'onelogin' | 'google_workspace';

interface OneLoginConfig {
  region: 'us' | 'eu';
  clientId: string;
  clientSecret: string;
  connectorId?: string;    // OneLogin connector ID for automated setup
  samlConfig: {
    acsUrl: string;
    audience: string;
    consumerUrl: string;
    attributeMapping: Record<string, string>;
  };
  scimEnabled?: boolean;
}

interface GoogleWorkspaceConfig {
  clientId: string;
  clientSecret: string;
  hostedDomain: string;     // e.g., "company.com"
  scopes: string[];
  directorySyncEnabled: boolean;
  oauthConsentConfig?: {
    projectId: string;
    authorizedDomains: string[];
  };
}

class OneLoginGoogleSSOService {
  async configureOneLogin(tenantId: string, config: OneLoginConfig): Promise<void> {
    const apiClient = new OneLoginClient({
      region: config.region,
      clientId: config.clientId,
      clientSecret: config.clientSecret,
    });

    // Create or update SAML connector
    const connector = config.connectorId
      ? await apiClient.updateConnector(config.connectorId, {
          name: `Voice Agent Platform - ${tenantId}`,
          saml: {
            acsUrl: config.samlConfig.acsUrl,
            audience: config.samlConfig.audience,
            consumerUrl: config.samlConfig.consumerUrl,
            certificate: { // Platform SP certificate
            },
          },
          configuration: {
            vendor: 'voiceagent',
            authn_request_signed: false,
            logout_url: `https://app.voiceagent.com/auth/saml/logout`,
            logout_request_url: `https://app.voiceagent.com/auth/saml/logout`,
          },
        })
      : await apiClient.createConnector({
          name: `Voice Agent Platform - ${tenantId}`,
          type: 'saml2',
          saml: {
            acsUrl: config.samlConfig.acsUrl,
            audience: config.samlConfig.audience,
            consumerUrl: config.samlConfig.consumerUrl,
          },
        });

    config.connectorId = connector.id;
    await this.db.oneloginConfigs.insert({ tenantId, ...config });
  }

  async configureGoogleWorkspace(tenantId: string, config: GoogleWorkspaceConfig): Promise<void> {
    // Validate the hosted domain
    const discoveryUrl = `https://accounts.google.com/.well-known/openid-configuration`;
    const discovery = await axios.get(discoveryUrl);

    // Store config
    await this.db.googleWorkspaceConfigs.insert({ tenantId, ...config });
    logger.info('Google Workspace SSO configured', { tenantId, hostedDomain: config.hostedDomain });
  }

  async handleGoogleCallback(tenantId: string, code: string, state: string): Promise<SSOResult> {
    const config = await this.db.googleWorkspaceConfigs.findOne({ tenantId });

    // Exchange code for tokens
    const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
      code,
      client_id: config.clientId,
      client_secret: config.clientSecret,
      redirect_uri: 'https://app.voiceagent.com/auth/callback',
      grant_type: 'authorization_code',
    });

    const { id_token, access_token } = tokenResponse.data;

    // Validate ID token
    const jwks = await this.fetchJWKS('https://www.googleapis.com/oauth2/v3/certs');
    const idToken = jwt.verify(id_token, this.getGooglePublicKey(jwks), {
      issuer: ['https://accounts.google.com', 'accounts.google.com'],
      audience: config.clientId,
      algorithms: ['RS256'],
    });

    // Verify hosted domain
    if (idToken.hd !== config.hostedDomain) {
      throw new Error(`Invalid hosted domain: ${idToken.hd}. Expected: ${config.hostedDomain}`);
    }

    const claims: Record<string, any> = {
      sub: idToken.sub,
      email: idToken.email,
      name: idToken.name || `${idToken.given_name} ${idToken.family_name}`,
      hostedDomain: idToken.hd,
    };

    // Fetch directory info if configured
    if (config.directorySyncEnabled && access_token) {
      const groups = await this.fetchGoogleGroups(access_token, idToken.email);
      claims.groups = groups;

      const ou = await this.fetchGoogleOrgUnit(access_token, idToken.email);
      claims.orgUnit = ou;
    }

    // Create user
    const user = await this.userService.findOrCreateSSOUser({
      tenantId,
      idpUserId: idToken.sub,
      email: idToken.email,
      name: claims.name,
      groups: claims.groups,
      idp: 'google_workspace',
    });

    const session = await this.sessionService.createSession({
      userId: user.id,
      tenantId,
      authMethod: 'oidc',
    });

    return { user, session, claims };
  }

  async handleOneLoginCallback(tenantId: string, samlResponse: string): Promise<SSOResult> {
    const config = await this.db.oneloginConfigs.findOne({ tenantId });
    if (!config) throw new Error('OneLogin not configured for this tenant');

    // Use the SAML SSO service to process the response
    return this.samlService.handleAssertion(tenantId, samlResponse);
  }

  private async fetchGoogleGroups(accessToken: string, userEmail: string): Promise<string[]> {
    try {
      const response = await axios.get(
        `https://admin.googleapis.com/admin/directory/v1/groups?userKey=${userEmail}`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      return response.data.groups?.map((g: any) => g.email) || [];
    } catch (error: any) {
      if (error.response?.status === 403) {
        logger.warn('Insufficient permissions to fetch Google Groups', { userEmail });
        return [];
      }
      throw error;
    }
  }

  private async fetchGoogleOrgUnit(accessToken: string, userEmail: string): Promise<string | undefined> {
    try {
      const response = await axios.get(
        `https://admin.googleapis.com/admin/directory/v1/users/${userEmail}?projection=full`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      return response.data.orgUnitPath;
    } catch {
      return undefined;
    }
  }

  async getOneLoginSetupGuide(tenantId: string): Promise<any> {
    return {
      provider: 'onelogin',
      steps: [
        { title: 'Create OneLogin Connector', detail: 'Navigate to Administration > Connectors > Add Connector' },
        { title: 'Configure SAML', detail: `ACS URL: https://app.voiceagent.com/auth/saml/callback\nAudience: https://api.voiceagent.com/saml/${tenantId}` },
        { title: 'Map Attributes', detail: 'Email → email, First Name → firstName, Last Name → lastName, Groups → groups' },
        { title: 'Assign App', detail: 'Create an application using this connector and assign users/groups' },
        { title: 'Test', detail: 'Use the OneLogin SAML Test tool to verify the integration' },
      ],
      metadataUrl: `https://${config.region}.onelogin.com/...`,
    };
  }

  async getGoogleSetupGuide(tenantId: string): Promise<any> {
    return {
      provider: 'google_workspace',
      steps: [
        { title: 'Configure OAuth Consent', detail: 'Google Cloud Console > APIs & Services > OAuth consent screen' },
        { title: 'Create Credentials', detail: 'Create OAuth 2.0 Client ID (Web application)' },
        { title: 'Set Redirect URI', detail: 'https://app.voiceagent.com/auth/callback' },
        { title: 'Enable Admin SDK', detail: 'Enable Admin SDK API for directory sync' },
        { title: 'Configure Domain', detail: 'Verify domain ownership and set authorized domain' },
      ],
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| onelogin-node-sdk (MIT) | Node.js | OneLogin API client |
| googleapis (Apache 2.0) | Node.js | Google Workspace API |
| google-auth-library (Apache 2.0) | Node.js | Google OAuth2 + token verification |

## Production Considerations

**Scaling:** OneLogin and Google authentication volumes depend on tenant size. Both providers have API rate limits for management operations — cache directory data aggressively (1-hour TTL for groups/OU). Google's OAuth2 token endpoint has a rate limit of 100 requests per 100 seconds per client ID — ensure refresh token logic respects this. OneLogin's API rate limit is 10,000 requests per hour for most tiers.

**Security:** For Google Workspace, validate the `hd` (hosted domain) claim strictly — this prevents users from other Google Workspace tenants from authenticating. For OneLogin, validate the SAML assertion `Issuer` matches the OneLogin connector's entity ID. Google directory API access requires domain-wide delegation — restrict the service account to only the necessary API scopes. Store OAuth client secrets encrypted.

**Monitoring:** Track authentication successes and failures per provider, OneLogin connector health, Google OAuth consent page issues, directory sync success rates, and group cache freshness. Alert on authentication failures from either provider (indicates configuration drift), Google API quota approaching limits, and OneLogin API token expiry. Monitor provider-specific deprecation roadmaps (Google frequently announces OAuth changes).
