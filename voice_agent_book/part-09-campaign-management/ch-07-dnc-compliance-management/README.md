# Chapter 07: DNC & Compliance Management

> **Part:** 09 - Campaign Management

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [DNC List Ingestion & Sources](sec-01-dnc-list-ingestion-sources.md) | National/state DNC lists, internal suppression, third-party DNC services, list format handling |
| 02 | [Real-Time DNC Check Engine](sec-02-real-time-dnc-check-engine.md) | Pre-dial DNC lookup — in-memory cache, Bloom filter, database query, performance optimization |
| 03 | [Per-Campaign DNC Management](sec-03-per-campaign-dnc-management.md) | Campaign-specific DNC lists, consent-based exceptions, brand-specific DNC rules |
| 04 | [TCPA Compliance Framework](sec-04-tcpa-compliance-framework.md) | TCPA regulation implementation — consent recording, time windows, opt-out mechanisms, record keeping |
| 05 | [Consent Tracking & Records](sec-05-consent-tracking-records.md) | Consent capture, timestamps, source tracking, consent withdrawal, proof of consent |
| 06 | [Scrub API Integration](sec-06-scrub-api-integration.md) | Third-party scrubbing services — list upload, scrub request, results processing, scheduling |
| 07 | [Compliance Reporting & Audit](sec-07-compliance-reporting-audit.md) | DNC compliance reports, audit trail, regulator-ready exports, violation detection |
| 08 | [State-Specific Regulation Handling](sec-08-state-specific-regulation-handling.md) | State-level variations — calling hours, consent requirements, additional restrictions, dynamic rules |

---

## Key Takeaways

- DNC checking must happen in real-time before every dial attempt with minimal latency
- Bloom filters enable efficient DNC lookups with configurable false-positive rates
- TCPA compliance requires granular consent tracking with timestamps and source attribution
- Consent records must be immutable and include proof of consent mechanism
- State-specific regulations require a configurable rules engine, not hard-coded logic
