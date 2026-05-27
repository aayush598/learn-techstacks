# Section 04: Azure AD / Entra ID Integration

## Overview

Azure Active Directory (now Microsoft Entra ID) integration enables the voice agent platform to authenticate users through Microsoft's cloud identity service. Microsoft Entra ID supports both SAML 2.0 and OpenID Connect, with OIDC being the recommended approach for new integrations. Thousands of enterprise customers use Microsoft 365, and integrating with Entra ID allows them to use their existing corporate credentials for platform access.

The integration covers Entra ID enterprise application configuration (gallery and non-gallery), OIDC and SAML protocol support, group-based access control via Microsoft Graph API, conditional access policy enforcement, and user provisioning via Microsoft Graph's directory synchronization. The integration also supports Microsoft's emerging security features: token protection (binding tokens to the client device), continuous access evaluation (real-time token revocation), and Microsoft Authenticator for MFA.

## Architecture

```
            Azure AD / Entra ID Integration

   User → Platform → Entra ID → Platform → User
              |                       |
   +----------------------------------------------------------+
   |           Entra ID Integration Components               |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Enterprise App   |  | Microsoft Graph   |             |
   |  | • Gallery/non-   |  | Client            |            |
   |  |   gallery setup  |  | • Users API       |            |
   |  | • SAML/OIDC      |  | • Groups API      |            |
   |  |   configuration  |  | • Directory       |            |
   |  | • App roles      |  |   synchronization |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Conditional      |  | Claims Mapping    |             |
   |  | Access           |  | • Tenant ID       |            |
   |  | • CAE support    |  | • Object ID       |            |
   |  | • Token binding  |  | • Groups/roles    |            |
   |  | • IP restriction |  | • App roles       |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Provisioning     |  | B2B Guest Access  |             |
   |  | • SCIM (planned) |  | • External users  |            |
   |  | • Group sync     |  | • Cross-tenant    |            |
   |  | • Role mapping   |  |   collaboration   |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **OIDC as primary protocol over SAML for Entra ID:** Microsoft recommends OIDC for new Entra ID application integrations. OIDC provides simpler token validation (JWT vs. XML), better integration with Microsoft Authentication Library (MSAL), and support for modern features like Conditional Access Evaluation and token binding. SAML is supported for legacy integration requirements. The integration uses the Microsoft Identity Platform endpoint (v2.0) which supports both Microsoft Accounts (MSA) and Entra ID accounts. Trade-off: OIDC requires the platform to manage JWKS and JWT verification but provides a more modern, flexible authentication experience.

- **Microsoft Graph API for directory information over Entra ID tokens:** While ID tokens contain basic user info (sub, email, name), group membership information may exceed the token size limit for users in many groups. The integration uses Microsoft Graph API (`/users/{id}/memberOf` and `/users/{id}/transitiveMemberOf`) to fetch full group membership, overriding the `groups` claim from the token. Graph queries are cached for 1 hour with forced refresh on profile update. Trade-off: Graph API calls add latency and require delegated or application permissions but provide complete group information without token size limitations.

- **Configuration-driven app role mapping over hard-coded role assignment:** Entra ID enterprise applications can define custom app roles that are assigned to users and groups by the Entra ID admin. The integration reads the `roles` claim from the ID token and maps it to platform roles via a configuration file. This allows the enterprise admin to control role assignment from within Entra ID rather than within the platform. Trade-off: app role mapping requires the admin to configure roles in both Entra ID and the platform but provides centralized role management.

## Implementation Approach

```
interface EntraIDConfig {
  tenantId: string;
  clientId: string;
  clientSecret?: string;
  ssoProtocol: 'oidc' | 'saml';
  useGraphForGroups: boolean;
  roleMapping: Record<string, string>; // Entra ID app role ID → platform role name
  conditionalAccessPolicy?: 'default' | 'require_mfa' | 'require_compliant_device' | 'require_hybrid_join';
}

class EntraIDIntegrationService {
  private graphClient: GraphClient;
  private msalClient: MSALClient;

  constructor() {
    this.graphClient = new GraphClient();
    this.msalClient = new MSALClient();
  }

  async createEnterpriseApp(tenantId: string): Promise<{ appId: string; config: EntraIDConfig }> {
    const client = await this.getGraphClient(tenantId);

    // Create service principal and app registration
    const app = await client.api('/applications').post({
      displayName: `Voice Agent Platform - ${tenantId}`,
      signInAudience: 'AzureADMyOrg',
      web: {
        redirectUris: [
          'https://app.voiceagent.com/auth/callback',
          'https://app.voiceagent.com/auth/saml/callback',
        ],
        implicitGrantSettings: { enableIdTokenIssuance: false },
      },
      requiredResourceAccess: [{
        resourceAppId: '00000003-0000-0000-c000-000000000000', // Microsoft Graph
        resourceAccess: [
          { id: 'e1fe6dd8-ba31-4d61-89e7-88639da4923c', type: 'Scope' }, // User.Read
          { id: '5b567255-7703-4780-807c-7be8301ae99b', type: 'Scope' }, // GroupMember.Read.All
        ],
      }],
    });

    // Create service principal
    const sp = await client.api('/servicePrincipals').post({
      appId: app.appId,
      displayName: app.displayName,
    });

    const config: EntraIDConfig = {
      tenantId: this.tenantContext,
      clientId: app.appId,
      ssoProtocol: 'oidc',
      useGraphForGroups: true,
      roleMapping: {},
    };

    await this.db.entraIdConfigs.insert({ tenantId, ...config });
    return { appId: app.id, config };
  }

  async handleOIDCCallback(tenantId: string, code: string, state: string): Promise<SSOResult> {
    const config = await this.db.entraIdConfigs.findOne({ tenantId });

    const tokenResponse = await this.msalClient.acquireTokenByCode({
      code,
      scopes: ['User.Read', 'GroupMember.Read.All'],
      redirectUri: 'https://app.voiceagent.com/auth/callback',
    });

    // Validate ID token
    const idToken = await this.verifyEntraIDJWT(tokenResponse.idToken, config);

    // Extract basic claims
    const claims: Record<string, any> = {
      sub: idToken.sub || idToken.oid,
      email: idToken.preferred_username || idToken.email,
      name: idToken.name,
      tenantId: idToken.tid,
    };

    // Fetch group membership via Graph if needed
    if (config.useGraphForGroups && tokenResponse.accessToken) {
      const groups = await this.fetchGroupMembership(tokenResponse.accessToken, idToken.oid || idToken.sub);
      claims.groups = groups;
      claims.roles = this.mapAppRoles(groups, config.roleMapping);
    }

    // Create or update user
    const user = await this.userService.findOrCreateSSOUser({
      tenantId,
      idpUserId: claims.sub,
      email: claims.email,
      name: claims.name,
      groups: claims.groups,
      roles: claims.roles,
      idp: 'entra_id',
    });

    const session = await this.sessionService.createSession({
      userId: user.id,
      tenantId,
      authMethod: 'oidc',
      metadata: { homeTenantId: idToken.tid },
    });

    return { user, session, claims };
  }

  private async verifyEntraIDJWT(idToken: string, config: EntraIDConfig): Promise<any> {
    const issuer = `https://login.microsoftonline.com/${config.tenantId}/v2.0`;
    const jwksUri = `https://login.microsoftonline.com/${config.tenantId}/discovery/v2.0/keys`;

    const jwks = await this.fetchJWKS(jwksUri);
    const decoded = jwt.decode(idToken, { complete: true });
    const key = this.findJWK(jwks, decoded.header.kid);

    return jwt.verify(idToken, jwktopem(key), {
      issuer,
      audience: config.clientId,
      algorithms: ['RS256'],
      clockTolerance: 60,
    });
  }

  private async fetchGroupMembership(accessToken: string, userId: string): Promise<string[]> {
    const response = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${userId}/transitiveMemberOf`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );

    return response.data.value
      .filter((g: any) => g['@odata.type'] === '#microsoft.graph.group')
      .map((g: any) => ({ id: g.id, name: g.displayName }));
  }

  async handleConditionalAccessPolicy(tenantId: string, userId: string): Promise<CAPolicyResult> {
    const config = await this.db.entraIdConfigs.findOne({ tenantId });
    if (!config?.conditionalAccessPolicy || config.conditionalAccessPolicy === 'default') {
      return { required: false };
    }

    // Check if the session meets CA requirements
    // For specific policies, redirect the user to re-authenticate with the required context
    return {
      required: true,
      redirectUrl: `https://login.microsoftonline.com/${config.tenantId}/oauth2/v2.0/authorize?${new URLSearchParams({
        client_id: config.clientId,
        response_type: 'code',
        redirect_uri: 'https://app.voiceagent.com/auth/callback',
        scope: 'openid profile email',
        claims: JSON.stringify({
          access_token: { xms_cc: { values: ['cp1'] } },  // Conditional Access
        }),
      })}`,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| @azure/msal-node (MIT) | Node.js | MSAL authentication library |
| @microsoft/microsoft-graph-client (MIT) | Node.js | Microsoft Graph API |
| @azure/identity (MIT) | Node.js | Azure SDK identity |

## Production Considerations

**Scaling:** Entra ID authentication handles millions of users per tenant. The integration must handle token validation at scale (every page load requires session validation, not re-authentication). Cache JWKS from the Microsoft identity platform (they rotate every 6 weeks minimum). Microsoft Graph queries for groups should be cached with 1-hour TTL. Use Microsoft's continuous access evaluation (CAE) for real-time session revocation — the platform must handle CAE claims challenges.

**Security:** Validate the `tid` (tenant ID) claim in the ID token — it must match the configured tenant ID to prevent cross-tenant authentication. Support token protection (bound tokens) when available. Use MSAL's acquireTokenSilent with refresh token rotation. Never log access tokens or refresh tokens. Implement Microsoft's recommended token validation logic: issuer, audience, tenant ID, app ID, signature, and expiry.

**Monitoring:** Track Entra ID authentication success rates, token validation failure reasons (issuer, audience, tenant mismatch), Microsoft Graph API response times, group cache hit rates, and Conditional Access policy enforcement counts. Alert on authentication failure rates exceeding 5%, Graph API throttling responses (429), and CAE claims challenge frequency. Monitor Microsoft Entra ID service health for tenant-wide authentication issues.
