# Section 06: Tenant Deletion & Data Retention

Tenant deletion removes all tenant data from the platform. The process must be reversible for a grace period (typically 30 days) to account for accidental deletion or customer recovery requests. After the grace period, data is permanently purged. Deletion respects data retention policies and regulatory requirements.

Deletion flow: initiate deletion (dashboard or API) → confirmation (type tenant name to confirm) → tenant suspended immediately → grace period starts (30 days, tenant cannot login but data intact) → during grace, admin can restore (re-activates tenant with all data) → after grace, permanent deletion begins→ async worker iterates through all services (database, object storage, cache, analytics) and removes data → deletion complete notification sent to billing contact.

Data retention policies: call recordings retained for 90 days after deletion (regulatory), billing records retained for 7 years (tax compliance), audit logs retained for 3 years, personally identifiable information (PII) deleted within 30 days (GDPR). The retention manager enforces these policies automatically with purge jobs.
