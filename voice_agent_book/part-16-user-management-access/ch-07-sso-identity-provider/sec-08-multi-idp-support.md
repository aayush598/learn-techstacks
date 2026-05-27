# Multi-IdP Support

## Overview

Multi-IdP support allows tenants to configure multiple identity providers and route users to the appropriate IdP based on email domain, group membership, or other criteria. This supports acquisitions, contractor access, and gradual IdP migration.

## Configuration

```typescript
interface MultiIdpConfig {
  tenantId: string;
  idps: IdpEntry[];
  routingRules: IdpRoutingRule[];
  defaultIdp: string;
  failoverOrder: string[];
}

interface IdpEntry {
  id: string;
  type: 'saml' | 'oidc';
  label: string;
  domains: string[];              // Which domains route here
  config: SamlMetadata | OidcMetadata;
  priority: number;
  isActive: boolean;
}

interface IdpRoutingRule {
  id: string;
  name: string;
  condition: {
    type: 'domain' | 'group' | 'email_suffix' | 'ip_range' | 'device_type';
    value: string | string[];
  };
  targetIdp: string;
}
```

## Routing Engine

```typescript
class IdpRoutingService {
  async routeUser(email: string, context: AuthContext): Promise<IdpEntry> {
    const tenantConfig = await this.getTenantConfig(context.tenantId);
    const domain = email.split('@')[1];

    // Check routing rules in priority order
    for (const rule of this.getSortedRules(tenantConfig)) {
      const matches = await this.evaluateRule(rule, email, domain, context);
      if (matches) {
        const idp = tenantConfig.idps.find(i => i.id === rule.targetIdp);
        if (idp?.isActive) return idp;
      }
    }

    // Fall back to domain-based routing
    for (const idp of tenantConfig.idps) {
      if (idp.domains.includes(domain) && idp.isActive) {
        return idp;
      }
    }

    // Default IdP
    return tenantConfig.idps.find(i => i.id === tenantConfig.defaultIdp)!;
  }

  private async evaluateRule(rule: IdpRoutingRule, email: string, domain: string, context: AuthContext): Promise<boolean> {
    switch (rule.condition.type) {
      case 'domain':
        return rule.condition.value.includes(domain);
      case 'group':
        // Check if user's IdP groups match
        return context.groups?.some(g => rule.condition.value.includes(g)) || false;
      case 'email_suffix':
        return rule.condition.value.some((s: string) => email.endsWith(s));
      case 'ip_range':
        return this.ipInRange(context.ip, rule.condition.value as string);
      default:
        return false;
    }
  }

  async getLoginPageOptions(tenantId: string): Promise<LoginOption[]> {
    const config = await this.getTenantConfig(tenantId);
    return config.idps
      .filter(idp => idp.isActive)
      .map(idp => ({
        id: idp.id,
        label: idp.label,
        type: idp.type,
        hint: idp.domains.length > 0 ? `(@${idp.domains[0]})` : undefined,
      }));
  }
}
```

## Migration Support

```typescript
class IdpMigrationService {
  async migrateIdp(tenantId: string, fromIdpId: string, toIdpId: string): Promise<void> {
    // 1. Add new IdP with lower priority
    // 2. Route new users to new IdP
    // 3. Set up period of dual operation
    const config = await this.getTenantConfig(tenantId);
    const fromIdp = config.idps.find(i => i.id === fromIdpId);
    const toIdp = config.idps.find(i => i.id === toIdpId);

    // Re-route all domains from old IdP to new
    if (toIdp) {
      toIdp.domains = [...new Set([...toIdp.domains, ...(fromIdp?.domains || [])])];
    }

    await this.saveTenantConfig(tenantId, config);
  }
}
```

## Open-Source Tools

- **NextAuth.js** (ISC) — Multi-provider support
- **Clerk** (Commercial) — External IdP routing

## Production Considerations

- Max 5 IdPs per tenant to prevent configuration complexity
- Test each IdP configuration independently
- Monitor IdP health and failover automatically if primary IdP is unreachable
- Session continuity across IdP switches during migration
- Provide per-IdP login analytics (success rate, latency)
- Support IdP-specific attribute mapping
- Log IdP routing decisions for audit and debugging
