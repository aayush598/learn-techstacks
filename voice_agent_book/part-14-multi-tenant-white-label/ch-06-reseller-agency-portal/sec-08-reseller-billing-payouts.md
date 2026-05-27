# Section 08: Reseller Billing & Payouts

Reseller billing manages how resellers are charged for their sub-accounts' usage and how they receive commission payouts. The system supports two billing models: consolidated billing (the reseller pays one invoice covering all sub-accounts) and direct billing (each sub-account pays separately, reseller earns commission). Payouts are processed through Stripe Connect with automated scheduling.

Consolidated billing generates a single invoice for the reseller covering all sub-account charges, minus their commission/discount. This simplifies the reseller's accounting. The invoice includes a detailed breakdown per sub-account. Net terms (Net-30, Net-60) can be configured for enterprise resellers.

Payouts are calculated monthly based on commissionable revenue from sub-accounts. The payout report shows: total revenue, commission rate, deductions (clawbacks, fees), net payout amount, and per-sub-account breakdown. Payouts are sent to the reseller's connected Stripe account. Minimum payout thresholds prevent micro-transactions.

For a voice agent platform, reseller billing integrates with tax compliance (1099 generation for US resellers, VAT handling for EU resellers). The billing dashboard shows payout history, upcoming payouts, and lifetime earnings.
