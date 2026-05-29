# Section 06: Phase 5 — Enterprise (Months 13-18)

## Phase Overview

Phase 5 delivers enterprise-grade features required by large organizations: SSO, advanced compliance (HIPAA, PCI DSS), dedicated infrastructure, custom SLAs, and advanced analytics. This phase captures the highest-revenue customer segment.

```
Phase 5 Enterprise Features
┌─────────────────────────────────────────────────────────────────────────┐
│ Month 13-14: Enterprise Foundation     Month 15-16: Advanced Compliance│
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ SSO/SAML/SCIM             │  │ HIPAA certification         │        │
│ │ Okta, Azure AD, Google WS  │  │ PCI DSS certification      │        │
│ │ Directory sync (SCIM)      │  │ BAAs + DPAs signed          │        │
│ │ Role-based access control  │  │ PHI handling controls       │        │
│ │ Audit logging (detailed)   │  │ Tokenization for payments   │        │
│ │ IP allow/block list        │  │ Encryption key management   │        │
│ │ Custom password policies   │  │ Data retention policies     │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
├─────────────────────────────────────────────────────────────────────────┤
│ Month 17-18: Enterprise Scale + Advanced                               │
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ Dedicated infrastructure   │  │ Advanced analytics          │        │
│ │ Single-tenant deployment   │  │ Custom report builder       │        │
│ │ VPC peering options        │  │ AI-powered insights         │        │
│ │ Custom SLA (99.99%)        │  │ Predictive analytics        │        │
│ │ EU data residency          │  │ Anomaly detection           │        │
│ │ Capacity planning reports  │  │ Custom dashboards           │        │
│ │ Disaster recovery testing  │  │ Scheduled exports           │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Deliverables

### Enterprise Foundation
- **SSO/SAML:** Okta, Azure AD, Google Workspace, OneLogin
- **SCIM:** Automatic user provisioning/deprovisioning
- **RBAC:** Custom roles with granular permissions
- **Audit logging:** Immutable, searchable audit trail (6-year retention)
- **Security controls:** IP allowlisting, session policies, MFA enforcement

### Advanced Compliance
- **HIPAA:** Full compliance with BAAs, PHI handling, audit controls
- **PCI DSS:** Tokenization, ASV scanning, SAQ D
- **Data residency:** EU region for EU customers
- **Key management:** Customer-managed encryption keys (AWS KMS)
- **Data retention:** Configurable retention policies per tenant

### Enterprise Scale
- **Dedicated infrastructure:** Single-tenant clusters for large customers
- **VPC peering:** Direct connection to customer VPC
- **Custom SLA:** 99.99% uptime with financial penalties
- **Disaster recovery:** Cross-region failover, RPO <1 minute, RTO <15 minutes
- **Capacity planning:** Quarterly capacity reviews with customer

## Enterprise Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Enterprise Architecture                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Customer VPC                            Our Platform                   │
│ ┌─────────────────────┐                ┌─────────────────────┐        │
│ │ IdP (Okta/Azure AD) │◄──SAML──SCIM──►│ Auth Service       │        │
│ └─────────────────────┘                └─────────────────────┘        │
│ ┌─────────────────────┐                ┌─────────────────────┐        │
│ │ Customer Network    │◄──VPC Peering──►│ App Tier            │        │
│ │ (Internal apps)     │                │ (K8s)               │        │
│ └─────────────────────┘                └─────────────────────┘        │
│                                         ┌─────────────────────┐        │
│                                         │ Compliance Layer    │        │
│                                         │ • Audit logs        │        │
│                                         │ • PHI/CHD controls  │        │
│                                         │ • Key management    │        │
│                                         └─────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Phase 5 Team Growth

| Role | Phase 4 | Phase 5 Addition | Total |
|------|---------|-----------------|-------|
| Full-stack engineer | 6 | +1 | 7 |
| ML engineer | 2 | +1 | 3 |
| Product manager | 2 | +1 (Enterprise PM) | 3 |
| Designer | 2 | 0 | 2 |
| DevOps | 2 | +1 | 3 |
| DevRel | 1 | 0 | 1 |
| Sales/CS | 0 | +2 | 2 |
| Compliance | 0.5 | +1 | 1.5 |

## Phase 5 Exit Criteria

- [ ] SSO/SAML/SCIM with Okta, Azure AD, Google Workspace
- [ ] HIPAA certification complete
- [ ] PCI DSS SAQ D complete
- [ ] 3 enterprise customers on dedicated infrastructure
- [ ] Custom SLA (99.99%) offered and monitored
- [ ] EU data residency operational
- [ ] $120K+ MRR
- [ ] 10 enterprise customers (non-dedicated)
- [ ] Net revenue retention >120%

## Phase 5 Budget

| Category | Monthly Cost |
|----------|-------------|
| Infrastructure | $15K-25K |
| GPU compute | $5K-8K |
| SaaS | $6K-8K |
| Compliance | $10K-15K |
| Compensation (17 FTE) | $280K-340K |
| **Total monthly** | **$316K-396K** |

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| HIPAA audit failure | Critical | 20% | Pre-audit gap assessment |
| Enterprise sales cycle too long | High | 60% | Begin enterprise outreach in Phase 4 |
| Dedicated infrastructure complexity | High | 40% | Infrastructure-as-code, GitOps |
| Global team coordination | Medium | 50% | Async communication, good documentation |

## Open Source Tools Added

| Tool | Purpose | Alternative |
|------|---------|-------------|
| Keycloak | SSO/SAML (self-hosted option) | Casdoor |
| CertManager | TLS certificate management | acme.sh |
| Velero | Backup & disaster recovery | K8up |
| Crossplane | Infrastructure orchestration | Terraform |

## Enterprise Sales Process

```
Enterprise Deal Cycle: 4-8 months
Discovery → Technical Evaluation → POC (30-60 days) → Security Review → Legal → Procurement → Onboarding
```

## Production Considerations

- SSO: Test with all major IdPs before GA
- HIPAA: Engage external auditor (3rd-party) for gap assessment
- Dedicated infra: GitOps with ArgoCD, tenant-specific Helm values
- Multi-region: Active-passive with Route53 failover
- Compliance evidence: Automated collection (Vanta/Drata)
- Enterprise dashboards: Real-time usage, billing, SLA compliance
