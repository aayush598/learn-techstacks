# IdP Discovery & Metadata

## Overview

IdP discovery determines which identity provider a user should authenticate against based on their email domain. The system stores tenant-specific IdP configuration and enables auto-discovery when users enter their email.

## Tenant-Specific Configuration

```typescript
interface TenantIdpConfig {
  tenantId: string;
  domain: string;                     // e.g., "company.com"
  idpType: 'saml' | 'oidc';
  idpId: string;                      // References SAML or OIDC config
  isPrimary: boolean;
  priority: number;
  metadata: {
    label: string;
    iconUrl?: string;
    description?: string;
  };
  discoveryConfig: {
    autoRedirect: boolean;           // Auto-redirect to IdP on email entry
    showOnLoginPage: boolean;
    requiresDomain: boolean;         // Only for this domain
  };
}

class IdpDiscoveryService {
  async findByDomain(domain: string): Promise<TenantIdpConfig[]> {
    return this.db.find('tenant_idp_configs', {
      domain,
      isActive: true,
    }, { sort: { priority: 1 } });
  }

  async findByEmail(email: string): Promise<TenantIdpConfig | null> {
    const domain = email.split('@')[1];
    const configs = await this.findByDomain(domain);

    // Also check subdomain wildcards
    if (configs.length === 0) {
      const parts = domain.split('.');
      if (parts.length > 2) {
        const wildcardDomain = `*.${parts.slice(-2).join('.')}`;
        const wildcardConfigs = await this.findByDomain(wildcardDomain);
        return wildcardConfigs[0] || null;
      }
    }

    return configs[0] || null;
  }

  async getLoginPageOptions(): Promise<LoginPageOption[]> {
    // Get all IdPs configured for auto-redirect
    const configs = await this.db.find('tenant_idp_configs', {
      'discoveryConfig.showOnLoginPage': true,
      isActive: true,
    });

    return configs.map(c => ({
      id: c.idpId,
      label: c.metadata.label,
      iconUrl: c.metadata.iconUrl,
      type: c.idpType,
    }));
  }
}
```

## Email Domain Auto-Discovery

```
Login Page:
┌──────────────────────────────┐
│  Email: user@company.com     │
│                              │
│  [Continue]                  │
│                              │
│  → Detected SSO: Company SSO │
│  → Redirecting to IdP...     │
└──────────────────────────────┘
```

## Open-Source Tools

- **NextAuth.js** (ISC) — Built-in IdP discovery
- **Clerk** (Commercial) — Email-based IdP routing

## Production Considerations

- Cache IdP configs in Redis with 5-minute TTL
- Support domain aliases (multiple domains → same IdP)
- Allow users to bypass SSO detection and use password login
- Monitor IdP discovery failures per domain
- Support IdP override via URL parameter (?idp=okta)
- Validate domain ownership via DNS TXT record before enabling SSO
