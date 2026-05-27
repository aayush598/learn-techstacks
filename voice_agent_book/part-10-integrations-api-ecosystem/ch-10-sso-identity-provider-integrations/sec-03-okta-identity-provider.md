# Section 03: Okta Identity Provider

## Overview

Okta integration enables the voice agent platform to leverage Okta's Identity Cloud for SSO, user lifecycle management, and multi-factor authentication. Okta supports both SAML 2.0 and OIDC protocols, and the integration provides both options based on the customer's preference. Beyond SSO authentication, the integration leverages Okta's API for user provisioning (SCIM), group/role synchronization, and MFA enforcement.

Okta's integration follows a multi-step configuration: create an Okta application in the Okta admin console, configure the sign-on methods (SAML 2.0 or OIDC), assign users and groups, and exchange metadata between Okta and the platform. The integration includes both the IdP-side configuration guidance (documented steps for the Okta admin) and the SP-side configuration (automated via Okta's API where possible). The integration also supports Okta's adaptive MFA — requiring step-up authentication for sensitive platform operations.

## Architecture

```
                  Okta Integration

   User → Platform → Okta → Platform → User
              |               |
   +----------------------------------------------------------+
   |              Okta Integration Components                |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Okta Application |  | SSO Protocols     |            |
   |  | Mgmt             |  | • SAML 2.0        |            |
   |  | • Auto-create    |  | • OIDC            |            |
   |  |   via API        |  | • Metadata import |            |
   |  | • Config wizard  |  | • Attribute       |            |
   |  | • Deployment     |  |   mapping         |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | User Lifecycle    |  | Group Sync        |            |
   |  | • SCIM provisioning|  | • Group push      |            |
   |  | • Just-in-time    |  | • Role mapping    |            |
   |  |   provisioning    |  | • RBAC            |            |
   |  | • Deactivation    |  |   synchronization |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | MFA Enforcement  |  | Okta API Client   |             |
   |  | • Session MFA    |  | • Users API       |            |
   |  | • Step-up auth   |  | • Groups API      |            |
   |  | • MFA factors    |  | • Apps API        |            |
   |  +------------------+  | • Events API      |            |
   |                        +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **OIDC as primary protocol with SAML fallback:** Okta strongly recommends OIDC over SAML for new integrations — OIDC provides simpler token handling, better mobile support, and modern security features. SAML is offered for compatibility with existing enterprise deployments that require SAML. The integration auto-detects the configured protocol based on the Okta application metadata and routes accordingly. Trade-off: dual protocol support doubles maintenance but accommodates the full range of enterprise Okta configurations.

- **Just-in-time (JIT) provisioning as default with SCIM optional:** JIT provisioning creates user accounts in the platform on first SSO login using claims from the SAML assertion or ID token. This eliminates the need for a separate provisioning process. SCIM (System for Cross-domain Identity Management) is offered as an enhancement for enterprises that need to manage user lifecycle (create, update, deactivate) from Okta's dashboard. Trade-off: JIT is simpler but does not support deactivation workflows without SCIM.

- **Okta API integration for automated setup over manual configuration:** Where possible, the platform uses Okta's Management API to automate the application setup. When an admin enters their Okta subdomain and API token, the platform creates the Okta application, configures the sign-on settings, uploads the SP metadata, and tests the connection. This reduces setup from hours to minutes. For enterprises with restricted API access, the manual setup wizard guides the admin step-by-step. Trade-off: API-based setup requires an Okta API admin token with significant permissions but dramatically improves the setup experience.

## Implementation Approach

```
interface OktaConfig {
  orgUrl: string;            // https://{subdomain}.okta.com
  apiToken?: string;         // Okta API token for automated setup
  ssoProtocol: 'oidc' | 'saml';
  appId?: string;            // Okta application ID (if pre-created)
  clientId?: string;
  clientSecret?: string;
  idpMetadataUrl?: string;   // SAML metadata URL
  attributeMapping?: Record<string, string>;
  mfaPolicy?: 'optional' | 'required' | 'step_up';
  jitProvisioning: boolean;
  scimEnabled?: boolean;
}

class OktaIntegrationService {
  private samlService: SAMLSSOService;
  private oidcService: OIDCSSOService;

  async autoConfigure(tenantId: string, config: OktaConfig): Promise<void> {
    const oktaClient = new OktaClient({
      orgUrl: config.orgUrl,
      token: config.apiToken,
    });

    // Create Okta application
    const app = config.ssoProtocol === 'oidc'
      ? await oktaClient.createApplication({
          name: 'oidc_client',
          label: `Voice Agent Platform - ${tenantId}`,
          signOnMode: 'OPENID_CONNECT',
          settings: {
            oauthClient: {
              client_uri: 'https://app.voiceagent.com',
              logo_uri: 'https://app.voiceagent.com/logo.png',
              redirect_uris: ['https://app.voiceagent.com/auth/callback'],
              post_logout_redirect_uris: ['https://app.voiceagent.com/auth/logout'],
              response_types: ['code'],
              grant_types: ['authorization_code'],
              application_type: 'web',
              consent_method: 'REQUIRED',
            },
          },
        })
      : await oktaClient.createApplication({
          name: 'saml',
          label: `Voice Agent Platform - ${tenantId}`,
          signOnMode: 'SAML_2_0',
          settings: {
            saml: {
              audience: `https://api.voiceagent.com/saml/${tenantId}`,
              recipient: `https://app.voiceagent.com/auth/saml/callback`,
              destination: `https://app.voiceagent.com/auth/saml/callback`,
              subjectNameIdTemplate: '${user.userName}',
              subjectNameIdFormat: 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
              attributeStatements: [
                { name: 'email', value: '${user.email}' },
                { name: 'firstName', value: '${user.firstName}' },
                { name: 'lastName', value: '${user.lastName}' },
                { name: 'groups', value: '${group.name}' },
              ],
            },
          },
        });

    config.appId = app.id;
    config.clientId = app.credentials?.oauthClient?.client_id;
    config.clientSecret = app.credentials?.oauthClient?.client_secret;
    config.idpMetadataUrl = `${config.orgUrl}/apps/${app.id}/sso/saml/metadata`;

    // Assign default group
    await oktaClient.assignApplicationToGroup(app.id, 'EVERYONE');

    // Save configuration
    await this.db.oktaConfigs.insert({ tenantId, ...config });
    logger.info('Okta auto-configuration complete', { tenantId, appId: app.id, protocol: config.ssoProtocol });
  }

  async getSetupGuide(tenantId: string): Promise<OktaSetupGuide> {
    const config = await this.db.oktaConfigs.findOne({ tenantId });
    const spMetadata = config.ssoProtocol === 'saml'
      ? this.samlService.generateSPMetadata(tenantId)
      : null;

    return {
      summary: 'Configure Okta for voice agent platform SSO',
      steps: [
        {
          title: 'Create Okta Application',
          instructions: 'Navigate to Applications > Add Application > Create New App',
        },
        {
          title: 'Configure SAML Settings',
          instructions: `Use the following values:\n- Single sign-on URL: ${spMetadata?.acsUrl}\n- Audience URI: ${spMetadata?.entityId}\n- Name ID format: EmailAddress\n- Attribute mapping: (see below)`,
          attributeMappings: [
            { oktaAttr: '${user.email}', platformAttr: 'email' },
            { oktaAttr: '${user.firstName}', platformAttr: 'firstName' },
            { oktaAttr: '${user.lastName}', platformAttr: 'lastName' },
            { oktaAttr: '${group.name}', platformAttr: 'groups' },
          ].filter(() => config.ssoProtocol === 'saml'),
        },
        {
          title: 'Upload IDP Metadata',
          instructions: `Copy the IdP metadata URL from Okta and paste it here`,
          metadataUrl: config.idpMetadataUrl,
        },
        {
          title: 'Assign Users',
          instructions: 'Assign users or groups to the application in Okta.',
        },
        {
          title: 'Test Connection',
          instructions: 'Click "Test Connection" below to verify the integration.',
        },
      ],
      spMetadataUrl: spMetadata?.metadataUrl,
      mfaRecommendation: config.mfaPolicy === 'required'
        ? 'MFA is required for this application. Ensure Okta MFA policies are configured.'
        : undefined,
    };
  }

  async handleSCIMProvisioning(params: {
    tenantId: string;
    operation: 'createUser' | 'updateUser' | 'deactivateUser' | 'pushGroup';
    data: any;
  }): Promise<void> {
    switch (params.operation) {
      case 'createUser':
        await this.userService.createUser({
          tenantId: params.tenantId,
          email: params.data.emails?.[0]?.value,
          name: params.data.name?.givenName + ' ' + params.data.name?.familyName,
          externalId: params.data.id,
          source: 'scim',
        });
        break;
      case 'deactivateUser':
        await this.userService.deactivateUser(params.tenantId, params.data.id);
        break;
      case 'pushGroup':
        await this.roleService.syncGroup(params.tenantId, {
          groupName: params.data.displayName,
          members: params.data.members?.map((m: any) => m.value) || [],
        });
        break;
    }
  }

  async enforceStepUpMFA(userId: string, requiredAction: string): Promise<boolean> {
    const user = await this.userService.getUser(userId);
    if (!user.ssoProvider || user.ssoProvider !== 'okta') return true;

    const config = await this.db.oktaConfigs.findOne({ tenantId: user.tenantId });
    if (!config || config.mfaPolicy !== 'step_up') return true;

    // Redirect user to Okta for MFA step-up
    // This returns a session_token after MFA verification
    return false; // Caller redirects to MFA page
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| @okta/okta-sdk-nodejs (Apache 2.0) | Node.js | Okta Management API |
| @okta/jwt-verifier (Apache 2.0) | Node.js | Okta JWT verification |

## Production Considerations

**Scaling:** Okta API rate limits apply to Management API calls (varying by Okta plan, typically 600 requests per minute). The auto-configuration feature makes approximately 10 API calls during setup — this is a one-time cost per tenant. SCIM provisioning creates ongoing API traffic proportional to user/group changes. Cache Okta JWKS keys with TTL matching the Cache-Control header. Use Okta's event webhooks to receive real-time user provisioning events instead of polling.

**Security:** The Okta API token used for auto-configuration must be stored encrypted — it provides significant access to the Okta org. Use Okta's API token with the minimum required scopes (okta.apps.manage, okta.users.read, okta.groups.read). Validate data returned from Okta's API before processing (never trust user data from an external IdP directly). Support Okta's Sign-On Policy for IP-based access restrictions.

**Monitoring:** Track Okta SSO success rates, SCIM provisioning events (users created/updated/deactivated), Okta API rate limit utilization, JIT provisioning failures, and group sync health. Alert on Okta API rate limit approaching, SCIM provisioning failures (operations that fail more than 3 times), and Okta JWT verification failures (potential key rotation issue). Monitor Okta service status page for planned maintenance and incidents.
