# Part 14: Multi-Tenant & White-Label Architecture

> **Duration:** Infrastructure Phase (Weeks 16-24)  
> **Goal:** Build a true multi-tenant architecture with tenant isolation, custom domains, white-label branding, and reseller capabilities.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Multi-Tenancy Models & Strategy](ch-01-multi-tenancy-models-strategy/README.md) | Database-per-tenant vs schema-per-tenant vs shared, hybrid approach, tenant isolation levels, trade-offs |
| 02 | [Tenant Schema Design & Row-Level Security](ch-02-tenant-schema-row-level-security/README.md) | Tenant ID pattern, PostgreSQL RLS policies, tenant context middleware, cross-tenant safeguards |
| 03 | [Tenant Onboarding & Provisioning](ch-03-tenant-onboarding-provisioning/README.md) | Self-service signup, automated provisioning, default configuration, setup wizard, welcome flow |
| 04 | [Custom Domain & Subdomain Support](ch-04-custom-domain-subdomain/README.md) | Wildcard DNS, custom domain verification, Let's Encrypt SSL, reverse proxy configuration, domain mapping |
| 05 | [White-Label Branding System](ch-05-white-label-branding-system/README.md) | Custom logo, colors, typography, CSS variables, favicon, email templates, custom login page |
| 06 | [Reseller & Agency Portal](ch-06-reseller-agency-portal/README.md) | Sub-account management, reseller tiers, commission tracking, white-label reseller, APIs for resellers |
| 07 | [Tenant Usage & Quota Management](ch-07-tenant-usage-quota-management/README.md) | Usage tracking per tenant, quota enforcement, soft/hard limits, upgrade prompts, throttle alerts |
| 08 | [Tenant-Level API Security](ch-08-tenant-level-api-security/README.md) | API key scoping, tenant-specific keys, key rotation, permission boundaries, request validation |
| 09 | [Custom SLA & Support Tiers](ch-09-custom-sla-support-tiers/README.md) | SLA definitions, response time guarantees, uptime SLAs, support tier assignment, escalation matrix |
| 10 | [Data Migration & Tenant Portability](ch-10-data-migration-tenant-portability/README.md) | Tenant data export, import/self-host migration, data deletion (GDPR), tenant splitting/merging |

---

## Tenant Isolation Strategies

| Strategy | Isolation | Complexity | Cost | Best For |
|----------|-----------|------------|------|----------|
| Database-per-tenant | Highest | High | High | Enterprise |
| Schema-per-tenant | High | Medium | Medium | Mid-market |
| Shared + RLS | Medium | Low | Low | SMB / Starter |

---

## Key Open-Source Tools

- **PostgreSQL RLS** (PostgreSQL) — Row-level security
- **Caddy** (Apache 2.0) — Automatic HTTPS, reverse proxy
- **Let's Encrypt** (Mozilla) — Free SSL certificates
- **NextAuth.js / Auth.js** (ISC) — Authentication with tenant context
- **i18next** (MIT) — White-label localization

---

## Learning Objectives

- Choose the right multi-tenancy model for different customer segments
- Implement PostgreSQL row-level security for tenant isolation
- Build automated tenant provisioning with onboarding wizard
- Implement custom domain support with automatic SSL
- Create a white-label branding system using CSS variables
- Build a reseller portal with sub-account management
- Implement per-tenant usage quotas with enforcement
- Create tenant-scoped API security with key management
- Design custom SLA tracking and support tier system
- Build tenant data portability for GDPR compliance
