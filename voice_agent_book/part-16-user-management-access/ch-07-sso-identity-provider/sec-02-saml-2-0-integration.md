# SAML 2.0 Integration

## Overview

SAML 2.0 is an XML-based SSO protocol widely used by enterprise identity providers. The integration involves metadata exchange, assertion validation, attribute mapping, and certificate management.

## Metadata Exchange

```typescript
interface SamlMetadata {
  idpEntityId: string;
  idpSsoUrl: string;           // IdP Single Sign-On URL
  idpCertificate: string;      // IdP signing certificate (X.509)
  spEntityId: string;          // Our entity ID
  spAcsUrl: string;            // Assertion Consumer Service URL
  spCertificate?: string;      // Our signing certificate
  nameIdFormat: string;
  authnContextClassRef: string[];
}

class SamlService {
  async parseIdpMetadata(xmlUrlOrString: string): Promise<SamlMetadata> {
    const metadata = await this.metadataParser.parse(xmlUrlOrString);
    return {
      idpEntityId: metadata.entityID,
      idpSsoUrl: metadata.ssoURL,
      idpCertificate: metadata.certificate,
      spEntityId: `${process.env.APP_URL}/auth/saml/metadata`,
      spAcsUrl: `${process.env.APP_URL}/auth/saml/acs`,
      nameIdFormat: 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
      authnContextClassRef: [
        'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport',
      ],
    };
  }

  async generateSpMetadata(ssoConfig: SamlMetadata): Promise<string> {
    return `<?xml version="1.0"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
  entityID="${ssoConfig.spEntityId}">
  <md:SPSSODescriptor AuthnRequestsSigned="true"
    WantAssertionsSigned="true" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
      Location="${ssoConfig.spAcsUrl}" index="0" isDefault="true"/>
    <md:NameIDFormat>${ssoConfig.nameIdFormat}</md:NameIDFormat>
  </md:SPSSODescriptor>
</md:EntityDescriptor>`;
  }
}
```

## Assertion Consumer

```typescript
class SamlAssertionConsumer {
  async handleResponse(samlResponse: string, relayState?: string): Promise<AuthResult> {
    const config = await this.getConfigForRelayState(relayState);
    const parsed = await this.samlParser.parse(samlResponse, {
      certificate: config.idpCertificate,
      audience: config.spEntityId,
    });

    // Validate assertion
    if (!this.validateAssertion(parsed)) {
      return { success: false, error: 'Invalid assertion' };
    }

    // Extract user attributes
    const attributes = parsed.attributes;
    const email = attributes[config.attributeMapping.email];

    // Find or create user
    let user = await this.userService.findByEmail(email, config.tenantId);
    if (!user) {
      if (config.provisioning.jit) {
        user = await this.jitProvisioning.provisionUser(attributes, config);
      } else {
        return { success: false, error: 'User not found and JIT disabled' };
      }
    }

    // Update attributes
    await this.userService.updateUser(user.id, {
      name: `${attributes[config.attributeMapping.firstName]} ${attributes[config.attributeMapping.lastName]}`,
      lastLoginIp: relayState,
    });

    // Create session
    const session = await this.sessionService.createSession(user.id, config.tenantId);

    return { success: true, user, session };
  }

  private validateAssertion(assertion: any): boolean {
    // Check NotBefore/NotOnOrAfter conditions
    const now = new Date();
    if (assertion.conditions.notBefore && new Date(assertion.conditions.notBefore) > now) return false;
    if (assertion.conditions.notOnOrAfter && new Date(assertion.conditions.notOnOrAfter) < now) return false;

    // Verify audience restriction
    if (!assertion.conditions.audienceRestrictions?.includes(config.spEntityId)) return false;

    return true;
  }
}
```

## Open-Source Tools

- **samlify** (MIT) — SAML 2.0 library for Node.js
- **@node-saml/node-saml** (MIT) — Passport SAML strategy
- **xml-crypto** (MIT) — XML signature verification

## Production Considerations

- Rotate SP signing certificates annually
- Validate SAML response timestamps with 5-minute clock skew allowance
- Log all SAML assertion details for debugging (except sensitive attributes)
- Test SAML integration with multiple test IdPs before production rollout
- Support encrypted SAML assertions for sensitive environments
- Allow download of SP metadata XML for IdP configuration
