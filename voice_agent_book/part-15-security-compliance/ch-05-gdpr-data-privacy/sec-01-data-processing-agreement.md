# Section 01: Data Processing Agreement (DPA)

A Data Processing Agreement (DPA) is a legally binding contract between the platform (data processor) and each tenant (data controller) that governs how personal data is processed. The DPA defines the scope of processing, data types, security measures, sub-processors, data subject rights procedures, and liability. GDPR Article 28 requires DPAs for all processing activities.

DPA lifecycle: tenant signs DPA during onboarding (digital signature via e-signature API) → DPA stored in tenant's document repository → terms reference standard platform DPA with tenant-specific addendums (if negotiated) → DPA auto-updated when platform changes sub-processors or processing activities → tenant notified of changes with 30-day acceptance period.

DPA contents: parties (controller and processor details), processing description (purpose, data categories, data subjects, retention), security measures (encryption, access controls, audit), sub-processors list (with notification obligation for changes), data subject rights (procedure for deletion, rectification, portability), data breach notification (72-hour SLA), international transfers (Standard Contractual Clauses), and liability and indemnification terms.
