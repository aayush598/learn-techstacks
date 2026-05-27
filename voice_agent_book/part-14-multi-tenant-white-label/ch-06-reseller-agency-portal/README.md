# Chapter 06: Reseller & Agency Portal

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Sub-Account Management](sec-01-sub-account-management.md) | Hierarchical tenant structure, parent-child relationships, delegated administration |
| 02 | [Reseller Tier Configuration](sec-02-reseller-tier-configuration.md) | Reseller tiers, discount schedules, markup capabilities, feature access control per tier |
| 03 | [Commission Tracking System](sec-03-commission-tracking.md) | Commission calculation rules, payout scheduling, commission reports, dispute resolution |
| 04 | [White-Label Reseller Experience](sec-04-white-label-reseller.md) | Full white-label for resellers, custom domain, branded dashboard, reseller as platform owner |
| 05 | [Reseller API Access](sec-05-reseller-api-access.md) | Scoped API keys for resellers, sub-account management APIs, provisioning endpoints |
| 06 | [Agency Dashboard & Analytics](sec-06-agency-dashboard.md) | Multi-tenant analytics view, aggregate reporting, client performance comparison, churn alerts |
| 07 | [Reseller Onboarding Flow](sec-07-reseller-onboarding.md) | Reseller application, approval workflow, training materials, certification tracking |
| 08 | [Reseller Billing & Payouts](sec-08-reseller-billing-payouts.md) | Reseller invoicing, net terms, minimum commit, consolidated billing, payout automation |

---

## Reseller Hierarchy

```
Platform Owner
    └── Master Reseller
         ├── Sub-Reseller A
         │    ├── Tenant A1
         │    └── Tenant A2
         └── Sub-Reseller B
              └── Tenant B1
    └── Direct Reseller
         ├── Tenant C1
         └── Tenant C2
```

---

## Learning Objectives

- Implement hierarchical tenant management for reseller/agency model
- Design reseller tier configuration with discount and markup controls
- Build commission tracking with automated payout calculations
- Create white-label reseller experience with full brand isolation
- Provide scoped API access for reseller automation
- Build multi-tenant analytics dashboard for agencies
- Design reseller onboarding with approval workflow
- Implement reseller billing, invoicing, and automated payouts
