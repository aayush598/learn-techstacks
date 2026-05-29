# Section 05: Vendor & Sub-Processor Management

Vendor management ensures third-party services (sub-processors) meet the platform's security standards. SOC 2 CC3.2/3.3 requires vendor risk assessments and contractual security requirements. The platform maintains a vendor register with risk ratings, due diligence documents, and contract terms.

Vendor assessment: vendor identified (for a new integration) → risk classification (critical: cloud hosting, payment processing; high: AI/ML APIs; medium: analytics, email; low: utilities) → due diligence (SOC 2 report, ISO 27001 cert, security questionnaire, penetration test results) → contract review (DPA, SLA, security addendum) → approval → ongoing monitoring (annual re-assessment, breach notification monitoring).

Sub-processor register: maintained publicly (in DPA) and internally (with operational details). New sub-processors require 30-day notice to tenants (contractual obligation). Register includes: sub-processor name, service provided, data processed, location, security certifications, and contract status. Automated alerts when sub-processor certifications expire.
