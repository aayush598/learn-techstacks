# Section 02: Data Subject Access Request (DSAR)

Data Subject Access Requests allow individuals to request access to their personal data held by the platform. The platform must respond within 30 days (GDPR) or 45 days (CCPA), providing a complete copy of the person's data in a portable format. The DSAR system automates data discovery, verification, and response.

DSAR flow: data subject submits request (via privacy portal or email to privacy@) → verify identity (government ID upload, proof of account ownership) → create DSAR ticket → system searches all data stores (database, object storage, logs, backups) for the subject's personal data → compile response package (export in machine-readable format with field descriptions) → review by privacy team (ensure no other individual's data included) → deliver to data subject via secure portal.

Identity verification is critical: without proper verification, the platform could inadvertently expose another person's data. Verification methods: email verification (send code to registered email), ID verification (passport/driver's license via automated verification service), and knowledge-based authentication (account-specific questions).
