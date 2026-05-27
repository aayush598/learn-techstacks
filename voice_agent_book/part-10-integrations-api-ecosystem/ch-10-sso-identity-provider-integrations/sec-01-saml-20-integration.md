# Section 01: SAML 2.0 Integration

## Overview

SAML 2.0 integration enables the voice agent platform to participate in enterprise single sign-on ecosystems as a Service Provider (SP). Enterprises configure their Identity Provider (IdP) — such as Okta, Azure AD, OneLogin, or PingFederate — to trust the voice agent platform, allowing employees to log in using their corporate credentials. SAML 2.0 is the most widely supported enterprise SSO protocol, required by most mid-market and enterprise customers.

The SAML integration handles the complete SP-initiated and IdP-initiated SSO flow: generating the SAML authentication request (AuthnRequest), sending the user to the IdP for authentication, receiving and validating the SAML response (Assertion), extracting user attributes (email, name, groups/roles), and creating/updating the local user account. The integration also handles SAML logout (Single Logout Protocol), metadata exchange, certificate rotation, and artifact binding.

## Architecture

```
                 SAML 2.0 SSO Flow

   User → Platform SP → IdP → Platform SP → User
              |                       |
   +----------------------------------------------------------+
   |              SAML 2.0 Integration Components             |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Metadata         |  | AuthnRequest      |            |
   |  | • SP metadata    |  | Generator         |            |
   |  | • IdP metadata   |  | • Signed/unsigned |            |
   |  | • Certificate    |  | • ForceAuthn      |            |
   |  |   exchange       |  | • RelayState      |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Response Handler |  | Attribute         |             |
   |  | • Assertion      |  | Extractor         |            |
   |  |   validation     |  | • Email mapping   |            |
   |  | • Signature      |  | • Group/role      |            |
   |  |   verification   |  |   mapping         |            |
   |  | • Audience check |  | • Custom claims   |            |
   |  | • Recipient check|  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Session Mgmt     |  | Logout            |             |
   |  | • Session create |  | • SP-initiated    |            |
   |  | • Session mapping|  | • IdP-initiated   |            |
   |  | • IdP session ref|  | • SOAP logout     |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **SP-initiated SSO as default with IdP-initiated support:** SP-initiated flow (user clicks "Login with SSO" on the platform) is the primary use case. The platform generates an AuthnRequest, signs it (if configured), and redirects the user to the IdP. IdP-initiated flow (user clicks the platform app icon in their IdP portal) is supported via an assertion consumer endpoint that accepts POST assertions. Trade-off: supporting both flows doubles the entry point handling but covers all enterprise access patterns.

- **SAML XML signature verification with certificate caching:** SAML assertions are verified using the IdP's public certificate, which is obtained from the IdP metadata XML. The certificate is cached with a configurable TTL (default 24 hours) and refreshed on demand if verification fails (certificate rotation). The platform supports multiple active certificates for smooth rotation — the old certificate continues to work while the new one is deployed. Trade-off: certificate caching introduces a window where a rotated certificate causes authentication failures but caching reduces IdP metadata fetch overhead.

- **Attribute mapping via configuration over code:** SAML attributes (claims) are mapped to platform user fields through a configuration file per IdP. The mapping defines which SAML attribute name maps to which platform field (email, firstName, lastName, groups). This allows customizing attribute mapping for different enterprise IdPs without code changes. Default mapping uses common attribute names (http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress). Trade-off: configurable mapping requires a configuration interface but supports diverse IdP attribute naming conventions.

## Implementation Approach

```
interface SAMLConfig {
  idpMetadataUrl: string;
  spEntityId: string;
  acsUrl: string;           // Assertion Consumer Service URL
  audienceUrl?: string;
  spPrivateKey?: string;    // For signed AuthnRequest
  spCertificate?: string;
  attributeMapping: {
    email: string;
    firstName?: string;
    lastName?: string;
    groups?: string;
    [key: string]: string | undefined;
  };
  forceAuthn?: boolean;
  authnContextClassRef?: string; // e.g., "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport"
}

class SAMLSSOService {
  private spConfigs = new Map<string, SAMLConfig>(); // tenant → config

  async configureSSO(tenantId: string, config: SAMLConfig): Promise<void> {
    this.spConfigs.set(tenantId, config);
    await this.db.samlConfigs.insert({ tenantId, ...config });
  }

  async generateAuthnRequest(tenantId: string, relayState?: string): Promise<{ redirectUrl: string; requestId: string }> {
    const config = this.spConfigs.get(tenantId);
    if (!config) throw new Error('SAML not configured for this tenant');

    const idpMetadata = await this.fetchIdPMetadata(config.idpMetadataUrl);
    const requestId = `_${uuidv4()}`;
    const issueInstant = new Date().toISOString();

    let authnRequest = `
      <samlp:AuthnRequest
        xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
        xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
        ID="${requestId}"
        Version="2.0"
        IssueInstant="${issueInstant}"
        Destination="${idpMetadata.ssoUrl}"
        AssertionConsumerServiceURL="${config.acsUrl}"
        ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        ForceAuthn="${config.forceAuthn || false}">
        <saml:Issuer>${config.spEntityId}</saml:Issuer>
    `;

    if (config.authnContextClassRef) {
      authnRequest += `
        <samlp:RequestedAuthnContext Comparison="exact">
          <saml:AuthnContextClassRef>${config.authnContextClassRef}</saml:AuthnContextClassRef>
        </samlp:RequestedAuthnContext>
      `;
    }

    authnRequest += '</samlp:AuthnRequest>';

    // Sign if SP private key configured
    if (config.spPrivateKey) {
      authnRequest = await this.signXML(authnRequest, config.spPrivateKey, config.spCertificate!);
    }

    const encoded = Buffer.from(authnRequest).toString('base64url');
    const redirectUrl = `${idpMetadata.ssoUrl}?SAMLRequest=${encoded}${relayState ? `&RelayState=${relayState}` : ''}`;

    await this.db.authnRequests.insert({ id: requestId, tenantId, relayState, createdAt: new Date() });
    return { redirectUrl, requestId };
  }

  async handleAssertion(tenantId: string, samlResponse: string): Promise<SSOResult> {
    const config = this.spConfigs.get(tenantId);
    if (!config) throw new Error('SAML not configured for this tenant');

    // Decode and parse
    const decoded = Buffer.from(samlResponse, 'base64').toString('utf8');
    const parsed = await parseXML(decoded);

    const assertion = parsed.Response.Assertion;
    const idpMetadata = await this.fetchIdPMetadata(config.idpMetadataUrl);

    // Validate signature
    const validSignature = await this.verifyAssertionSignature(assertion, idpMetadata.certificates);
    if (!validSignature) throw new Error('SAML assertion signature verification failed');

    // Validate conditions
    const conditions = assertion.Conditions;
    const now = new Date();
    if (new Date(conditions.NotBefore) > now || new Date(conditions.NotOnOrAfter) < now) {
      throw new Error('SAML assertion outside valid time window');
    }

    // Audience restriction
    const audience = conditions.AudienceRestriction?.Audience;
    if (audience && audience !== (config.audienceUrl || config.spEntityId)) {
      throw new Error(`SAML audience mismatch: ${audience}`);
    }

    // Extract attributes
    const attributes = this.extractAttributes(assertion.AttributeStatement, config.attributeMapping);
    const nameId = assertion.Subject.NameID?._text;

    // Create or update user
    const user = await this.userService.findOrCreateSSOUser({
      tenantId,
      idpUserId: nameId,
      email: attributes.email,
      firstName: attributes.firstName,
      lastName: attributes.lastName,
      groups: attributes.groups,
      idp: 'saml',
    });

    // Create session
    const session = await this.sessionService.createSession({
      userId: user.id,
      tenantId,
      authMethod: 'saml',
      idpSessionIndex: assertion.AuthnStatement?.SessionIndex,
    });

    return { user, session, attributes };
  }

  private extractAttributes(
    attributeStatement: any, mapping: SAMLConfig['attributeMapping']
  ): Record<string, string> {
    const extracted: Record<string, string> = {};
    const attributes = attributeStatement?.Attribute || [];

    for (const attr of attributes) {
      const attrName = attr.Name || attr._attr?.Name;
      const attrValue = attr.AttributeValue?._text || attr.AttributeValue?.[0]?._text;

      // Check against mapping
      for (const [field, samlAttr] of Object.entries(mapping)) {
        if (samlAttr && attrName === samlAttr) {
          extracted[field] = attrValue;
        }
      }
    }

    return extracted;
  }

  async handleIdPInitiatedSSO(tenantId: string, samlResponse: string, relayState?: string): Promise<SSOResult> {
    return this.handleAssertion(tenantId, samlResponse);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| samlify (MIT) | Node.js | SAML protocol implementation |
| xml-crypto (MIT) | Node.js | XML signature verification |
| xml2js (MIT) | Node.js | XML parsing |
| Node-forge (BSD) | Node.js | Certificate management |

## Production Considerations

**Scaling:** SAML authentication is low-volume (every user login event, not every API call). The SAML service must be highly available since SSO failures block all user access. Cache IdP metadata aggressively (24-hour TTL) but check certificate validity on each authentication. The AuthnRequest ID must be unique — use UUIDv4 with sufficient entropy. Support horizontal scaling by sharing session state across instances through a distributed session store.

**Security:** Validate all SAML assertions strictly: signature verification, audience restriction, timestamp validity, recipient check (AssertionConsumerServiceURL must match the configured ACS URL), and replay attack prevention (store assertion IDs for the assertion validity period). Support signed AuthnRequest to prevent man-in-the-middle attacks during the SSO initiation. Never log SAML assertions (they may contain sensitive attributes). Rotate SP signing certificates regularly.

**Monitoring:** Track SAML authentication success/failure rates, IdP response times, assertion validation failure reasons (signature, timing, audience), IdP metadata fetch failures, and per-IdP authentication volume. Alert on authentication failure rates exceeding 5%, metadata fetch failures, certificate expiry (60 days before), and unusual IdP response patterns. Monitor IdP-side configuration changes that may affect the integration.
