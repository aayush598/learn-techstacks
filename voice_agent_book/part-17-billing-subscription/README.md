# Part 17: Billing, Subscription & Monetization

> **Duration:** Billing Phase (Weeks 16-24)  
> **Goal:** Build the complete billing and subscription management system with usage-based pricing, tiered plans, invoicing, and revenue operations.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Subscription Plans & Tier Strategy](ch-01-subscription-plans-tier-strategy/README.md) | Plan definition (Free/Starter/Pro/Business/Enterprise), feature mapping, usage limits, plan comparison |
| 02 | [Usage-Based Metering & Tracking](ch-02-usage-based-metering-tracking/README.md) | Usage event collection, metering pipeline, real-time counters, usage aggregation, quota tracking |
| 03 | [Stripe Billing Integration](ch-03-stripe-billing-integration/README.md) | Stripe Connect, customer portal, subscription lifecycle, payment method management |
| 04 | [Invoice Generation & Payment History](ch-04-invoice-generation-payment-history/README.md) | Automatic invoicing, invoice PDF generation, payment reconciliation, credit notes, billing history |
| 05 | [Free Trial & Freemium Tier](ch-05-free-trial-freemium-tier/README.md) | Trial period configuration, feature gating, trial conversion, expiration handling, upgrade flow |
| 06 | [Credit System & Prepaid Billing](ch-06-credit-system-prepaid-billing/README.md) | Credit wallet, credit purchase, per-use deduction, credit expiry, top-up automation |
| 07 | [Overage Handling & Alerts](ch-07-overage-handling-alerts/README.md) | Overage thresholds, automatic overage billing, usage alerts, soft/hard caps, upgrade prompts |
| 08 | [Tax Calculation & Compliance](ch-08-tax-calculation-compliance/README.md) | Sales tax (US), VAT (EU), GST (IN), tax ID validation, automated tax calculation, tax reports |
| 09 | [Dunning Management & Failed Payments](ch-09-dunning-management-failed-payments/README.md) | Payment retry logic, dunning emails, subscription pause, grace period, downgrade flow |
| 10 | [Enterprise Contracts & Custom Pricing](ch-10-enterprise-contracts-custom-pricing/README.md) | Custom contracts, negotiated rates, invoicing terms, PO processing, sales-assisted ordering |

---

## Billing Architecture

```
Usage Events → Metering Pipeline → Aggregation → Billing Engine → Stripe API
                   ↓                                     ↓
              Redis Counters                         Invoice Gen
                   ↓                                     ↓
              Alert Engine                          Customer Portal
```

---

## Key Open-Source Tools

- **Stripe** (Proprietary, free tier) — Payment processing
- **Lemon Squeezy** (Proprietary) — Alternative payment processor
- **Invoice Ninja** (MIT) — Invoice generation (self-hosted)
- **pdfmake** (MIT) — PDF generation for invoices
- **BullMQ** (MIT) — Billing job scheduling

---

## Learning Objectives

- Design subscription plans aligned with customer segments
- Build a real-time usage metering pipeline
- Integrate Stripe for subscription and payment management
- Implement automated invoicing with PDF generation
- Create a free trial system with conversion optimization
- Build a prepaid credit system for usage-based billing
- Implement overage handling with configurable thresholds
- Handle tax calculation for global compliance
- Build dunning management for failed payment recovery
- Create enterprise contract support with custom pricing
