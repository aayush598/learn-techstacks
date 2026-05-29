# Section 06: Enterprise & White-Label Pricing

## Enterprise Pricing Philosophy

Enterprise pricing is fundamentally different from self-serve pricing. It's value-based, contract-driven, and includes services beyond software access. Our approach balances standardization (for efficiency) with customization (for enterprise requirements).

```
Enterprise Pricing Framework
┌────────────────────────────────────────────────────────────────────┐
│ Component Based Pricing                                           │
│                                                                   │
│ ┌───────────────────┐ ┌───────────────────┐ ┌──────────────────┐ │
│ │ Base Platform     │ │ Usage Volume      │ │ Add-On Modules   │ │
│ │ • Core voice AI   │ │ • Per-minute tier │ │ • HIPAA add-on   │ │
│ │ • Agent builder   │ │ • Committed usage │ │ • White-label    │ │
│ │ • Dashboard       │ │ • Overage rate    │ │ • Self-host      │ │
│ │ • API             │ │ • Annual prepay   │ │ • Advanced audit │ │
│ └───────────────────┘ └───────────────────┘ └──────────────────┘ │
│                                                                   │
│ ┌───────────────────┐ ┌───────────────────┐ ┌──────────────────┐ │
│ │ SLA Tiers         │ │ Professional      │ │ Support          │ │
│ │ • 99.9% standard  │ │ Services          │ │ • 24/7 phone     │ │
│ │ • 99.95% premium  │ │ • Implementation  │ │ • Dedicated TAM  │ │
│ │ • 99.99% critical │ │ • Training        │ │ • Custom SLA     │ │
│ └───────────────────┘ └───────────────────┘ └──────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

## Enterprise Pricing Tiers

| Component | Standard Enterprise | Premium Enterprise | Strategic Enterprise |
|-----------|-------------------|-------------------|---------------------|
| Base platform | $2,000/mo | $5,000/mo | $10,000/mo |
| Included minutes | 50K/mo | 200K/mo | 500K/mo |
| Overage rate | $0.03/min | $0.025/min | $0.02/min |
| SLA | 99.9% | 99.95% | 99.99% |
| Support | Email + Chat | 24/7 Phone + TAM | Dedicated team |
| SSO/SAML | ✅ | ✅ | ✅ |
| Audit logs | Basic | Advanced | Real-time |
| HIPAA | Add-on ($1K/mo) | Included | Included |
| Self-hosted | Add-on ($2K/mo) | Add-on ($1K/mo) | Included |
| White-label | Add-on ($500/mo) | Included | Included |
| Minimum commitment | Annual | Annual | Multi-year |
| Typical deal size | $36K/yr | $96K/yr | $240K+/yr |

## White-Label Pricing

White-label enables agencies and SaaS companies to resell our platform under their own brand. This is a unique differentiator versus all competitors.

### White-Label Tiers

| Tier | Price | Features | Use Case |
|------|-------|----------|----------|
| White-Label Basic | $500/mo | Custom domain, logo, primary color | Single client deployment |
| White-Label Pro | $1,500/mo | + Sub-account management, custom theme, agent templates | Agency with 5-20 client deployments |
| White-Label Enterprise | $5,000/mo | + Dedicated infrastructure, custom auth, billing integration | Platform embedding (white-label at scale) |

### White-Label Cost vs Pricing

```
White-Label Margin Analysis
┌────────────────────────────────────────────────────────────────────────┐
│ Tier          │ Our Cost │ Our Price │ Agency Price to Client │ Agency Margin│
├────────────────────────────────────────────────────────────────────────┤
│ Basic         │ $200     │ $500      │ $1,000-2,000           │ 50-75%      │
│ Pro           │ $500     │ $1,500    │ $3,000-5,000           │ 50-67%      │
│ Enterprise    │ $1,500   │ $5,000    │ $10,000-20,000         │ 50-75%      │
└────────────────────────────────────────────────────────────────────────┘
```

## Enterprise Contract Structure

```typescript
interface EnterpriseContract {
  tenantId: string;
  tier: 'standard' | 'premium' | 'strategic';
  term: {
    startDate: Date;
    endDate: Date;
    type: 'annual' | 'multi-year';
    renewalTerms: string;
  };
  pricing: {
    baseMonthly: number;
    committedUsage: number; // monthly minute commitment
    overageRate: number;
    addons: AddOnPricing[];
    discountTiers: VolumeDiscount[];
  };
  compliance: {
    hipaa: boolean;
    soc2: boolean;
    pciDss: boolean;
    lastAuditDate: Date;
    baas: string[]; // BAA agreements
  };
  sla: SLA;
  support: SupportLevel;
}

interface VolumeDiscount {
  threshold: number; // monthly minutes
  discountPercent: number;
}

function calculateEnterprisePricing(contract: EnterpriseContract, actualUsage: number): number {
  const base = contract.pricing.baseMonthly;
  const committed = contract.pricing.committedUsage;
  const overage = Math.max(0, actualUsage - committed);
  
  const overageCost = overage * contract.pricing.overageRate;
  const volumeDiscount = applyVolumeDiscount(actualUsage, contract.pricing.discountTiers);
  const addonCost = contract.pricing.addons.reduce((sum, a) => sum + a.monthlyPrice, 0);
  
  return (base + overageCost + addonCost) * (1 - volumeDiscount / 100);
}
```

## Enterprise Sales Negotiation Levers

| Lever | Authority | Typical Range | Impact |
|-------|-----------|--------------|--------|
| Discount | AE up to 20%, Manager up to 30%, VP up to 40% | 10-30% off list | Reduces ACV but closes deal |
| Free months | Manager up to 2, VP up to 4 | 1-3 months free | Slightly reduces Year 1 revenue |
| Implementation | Included for $5K+ deals | $5-25K value | Lowers barrier to adoption |
| Custom term | VP can approve month-to-month | 12-36 months | Longer term = less flexibility |
| Overage rate | Minimum $0.02/min | $0.02-0.03/min | Protects on high usage |
| SLA uplift | Standard SLA or premium | 99.9% → 99.99% | Differentiator for critical use cases |

## Enterprise Deal Economics

```
Enterprise Deal Sizing by Company Size
┌─────────────────────────────────────────────────────────────────────┐
│ Company Size  │ Typical Uses │ Annual Contract │ Deployment Time  │
├─────────────────────────────────────────────────────────────────────┤
│ 50-200 emp    │ 1-3 agents    │ $12-36K        │ 2-4 weeks        │
│ 200-1K emp    │ 3-10 agents   │ $36-120K       │ 4-8 weeks        │
│ 1K-5K emp     │ 10-50 agents  │ $120-500K      │ 8-16 weeks       │
│ 5K+ emp       │ 50+ agents    │ $500K-2M+      │ 3-6 months       │
└─────────────────────────────────────────────────────────────────────┘
```

## Competitive Enterprise Pricing

| Feature | Our Enterprise | Retell AI Enterprise | Twilio Flex |
|---------|---------------|---------------------|-------------|
| Starting price | $2K/mo | $5K/mo | $1K/mo + usage |
| White-label | ✅ | ❌ | ❌ |
| Self-hosted | ✅ | Limited | ❌ |
| HIPAA included | Premium tier | $2K/mo add-on | $500/mo add-on |
| API rate limit | 10K req/s | 5K req/s | 100K req/s |
| Implementation | $5-25K | $25-100K | $50-200K |

## Enterprise Expansion Playbook

**Year 1:** Land with 1 department (e.g., customer service). **Year 2:** Expand to sales (outbound), collections, or other departments. **Year 3:** Enterprise-wide deployment, self-hosted, custom models.

**Expansion triggers:** Usage hitting 70% of committed, new champion in another department, successful quarterly business review, product launch with new capability.

## Tools & Resources

- **CPQ (Configure, Price, Quote):** Salesforce CPQ, PandaDoc, Quotient
- **Contract management:** Ironclad, Evisort, Icertis
- **Enterprise sales CRM:** Salesforce, HubSpot Enterprise
- **Deal desk:** Internal Slack/Teams channel + approval workflow
- **Usage tracking dashboard:** Metabase, Retool (for enterprise customer reporting)
