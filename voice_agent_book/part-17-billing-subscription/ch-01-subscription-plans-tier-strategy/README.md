# Chapter 01: Subscription Plans & Tier Strategy

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Plan Design Framework](sec-01-plan-design-framework.md) | Tier definition methodology, feature packaging, value metric selection, plan naming conventions |
| 02 | [Feature Tier Mapping](sec-02-feature-tier-mapping.md) | Per-plan feature matrix, feature gating, add-on features, enterprise-only features |
| 03 | [Pricing Model Selection](sec-03-pricing-model-selection.md) | Flat-rate vs per-seat vs usage-based vs hybrid, price anchoring, psychological pricing |
| 04 | [Plan Versioning & Migration](sec-04-plan-versioning-migration.md) | Plan version history, grandfathering existing customers, migration paths, price increase handling |
| 05 | [Metered vs Flat Pricing](sec-05-metered-vs-flat-pricing.md) | Usage-based billing models, flat-rate simplicity, hybrid combinations, predictability vs flexibility |
| 06 | [Plan Configuration Schema](sec-06-plan-configuration-schema.md) | Plan definition data model, feature flag binding, quota definitions, rate limit tiers |
| 07 | [Plan Catalog Management](sec-07-plan-catalog-management.md) | Plan CRUD operations, staging vs production catalog, localization of plans, currency support |
| 08 | [Competitive Pricing Analysis](sec-08-competitive-pricing-analysis.md) | Competitor pricing benchmarks, willingness-to-pay analysis, value-based pricing, pricing elasticity |

---

## Tier Structure Example

| Feature | Free | Starter | Growth | Enterprise |
|---------|------|---------|--------|------------|
| Monthly Minutes | 100 | 1,000 | 10,000 | Custom |
| AI Agents | 1 | 3 | 10 | Unlimited |
| Voice Clones | 0 | 1 | 5 | Custom |
| Languages | 1 | 3 | 10 | All |
| Integrations | 0 | 5 | 15 | Unlimited |
| SLA | None | 99.9% | 99.95% | 99.99% |
| Support | Community | Email | Priority | 24/7 Dedicated |
| Price | $0 | $49/mo | $199/mo | Custom |
