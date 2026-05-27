# Chapter 08: Tax Calculation & Compliance

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Tax Engine Architecture](sec-01-tax-engine-architecture.md) | Tax determination logic, rate lookup, jurisdiction identification, third-party tax providers (Stripe Tax, TaxJar) |
| 02 | [EU VAT Compliance](sec-02-eu-vat-compliance.md) | VAT registration thresholds, MOSS/IOSS, reverse charge, VAT rate lookup per member state, VAT validation (VIES) |
| 03 | [US Sales Tax Automation](sec-03-us-sales-tax-automation.md) | Economic nexus, state-by-state rates, product taxability, origin vs destination sourcing |
| 04 | [Tax Exemption Handling](sec-04-tax-exemption-handling.md) | Exemption certificate collection, validation, exemption status storage, exempt vs taxable line items |
| 05 | [Tax Report Generation](sec-05-tax-report-generation.md) | Monthly/quarterly tax reports, jurisdiction summaries, marketplace facilitator reports, VAT return data |
| 06 | [Marketplace Facilitator Rules](sec-06-marketplace-facilitator-rules.md) | Marketplace vs seller of record, tax collection responsibility, reporting requirements |
| 07 | [Cross-Border Tax](sec-07-cross-border-tax.md) | Digital services taxes, withholding tax, double taxation treaties, cross-border invoicing |
| 08 | [Tax Audit Trail](sec-08-tax-audit-trail.md) | Per-transaction tax records, rate snapshot at time of transaction, tax code mappings, exemption records |

---

## Tax Calculation Flow

```
[Invoice Generation]
    ↓
[Determine Jurisdiction]
    ├── Customer billing address
    └── Service location (for voice services)
    ↓
[Lookup Tax Rate]
    ├── Product taxability
    ├── Customer exemption status
    └── Current rate (snapshotted)
    ↓
[Calculate Tax]
    ├── Per line item
    ├── Subtotal + tax
    └── Total with tax
    ↓
[Record Tax Details]
    ├── Rate used
    ├── Jurisdiction details
    ├── Exemption reference
    └── Tax calculation method
```

---

## Learning Objectives

- Architect tax engine with third-party provider integration
- Implement EU VAT compliance with MOSS/IOSS
- Automate US sales tax with economic nexus tracking
- Handle tax exemptions with certificate management
- Generate tax reports for filing
- Comply with marketplace facilitator rules
- Handle cross-border tax and digital services taxes
- Build comprehensive tax audit trail
