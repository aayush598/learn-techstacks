# SSO Architecture Overview

## Overview

Single Sign-On (SSO) enables users to authenticate via their corporate identity provider (IdP) rather than a local password. The architecture supports SAML 2.0 and OIDC protocols, IdP-initiated and SP-initiated flows, and tenant-specific IdP configurations.

## SSO Flow Types

```
SP-Initiated SSO:
[User] → App Login → Select SSO → Enter Email → IdP Discovery
    → Redirect to IdP → Authenticate → SAML/OIDC Response
    → Validate → Create/Link User → Session Created

IdP-Initiated SSO:
[User] → IdP App Dashboard → Click App Icon
    → IdP sends SAML Response to ACS URL
    → Validate → Create/Link User → Session Created
```

## Core Components

```typescript
interface SsoConfig {
  tenantId: string;
  provider: 'saml' | 'oidc' | 'google' | 'microsoft' | 'okta';
  label: string;                          // "Login with Company SSO"
  isActive: boolean;
  isDefault: boolean;
  metadata: SamlMetadata | OidcMetadata;
  attributeMapping: AttributeMapping;
  provisioning: ProvisioningConfig;
  createdAt: Date;
}

interface AttributeMapping {
  email: string;          // IdP attribute → app email
  firstName: string;
  lastName: string;
  groups: string;
  role: string;
  department: string;
  custom: Record<string, string>;
}
```

## IdP Discovery

```typescript
class IdPDiscoveryService {
  async discoverIdP(email: string): Promise<SsoConfig | null> {
    const domain = email.split('@')[1];

    // Check exact domain match
    const config = await this.db.findOne('sso_configs', {
      domain,
      isActive: true,
    });
    if (config) return config;

    // Check wildcard domain match
    const wildcardConfig = await this.db.findOne('sso_configs', {
      domainPattern: `*.${domain.split('.').slice(-2).join('.')}`,
      isActive: true,
    });
    if (wildcardConfig) return wildcardConfig;

    return null;
  }

  async getLoginOptions(email: string): Promise<LoginOption[]> {
    const options: LoginOption[] = [];

    // Check SSO
    const ssoConfig = await this.discoverIdP(email);
    if (ssoConfig) {
      options.push({
        type: 'sso',
        label: ssoConfig.label,
        redirectUrl: `/auth/sso/${ssoConfig.id}`,
      });
    }

    // Always allow password login as fallback
    options.push({ type: 'password', label: 'Password' });

    return options;
  }
}
```

## Open-Source Tools

- **Passport.js** (MIT) — SSO strategies (SAML, OIDC)
- **NextAuth.js** (ISC) — Built-in SSO support
- **samlify** (MIT) — SAML 2.0 implementation
- **openid-client** (MIT) — OIDC client library

## Production Considerations

- Support multiple IdPs per tenant (primary + fallback)
- SAML metadata must be uploaded as XML or URL
- Session timeout alignment between IdP and app
- IdP-initiated SSO requires pre-configured ACS URL
- Test SSO configuration with test users before rolling out to all
- Monitor SSO login success/failure rates per IdP
- Fallback to email+password if SSO provider is unavailable
