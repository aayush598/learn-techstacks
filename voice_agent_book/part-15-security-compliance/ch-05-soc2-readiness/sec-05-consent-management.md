# Section 05: Consent Management

Consent management tracks and records user consent for data processing activities. GDPR requires that consent be freely given, specific, informed, and unambiguous. The platform maintains a consent record for each data subject, including what they consented to, when, and how. Consent can be withdrawn at any time.

Consent types: account creation consent (terms of service, privacy policy), communication consent (marketing emails, product updates), processing consent (call recording, AI analysis), third-party sharing consent (integrations, analytics), and cookies consent (tracking, functional, analytics). Each consent has a timestamp, version, and method (checkbox, explicit button, API flag).

Consent records are stored immutably: event store with consent_id, subject_id, consent_type, granted (boolean), timestamp, and recording_method. The consent dashboard shows active consents per user, consent history (granted and withdrawn events), and consent expiry. Withdrawal of consent triggers automated data processing adjustments (stop marketing emails, delete analytics data).
