# Section 03: Right to Erasure (Data Deletion)

The Right to Erasure (GDPR Article 17) requires the platform to delete an individual's personal data on request, subject to certain exceptions (legal obligation, contract necessity, public interest). The deletion system must find and remove all instances of the person's data across all systems, including backups and disaster recovery copies.

Deletion flow: receive erasure request → verify identity → determine scope (which data belongs to this data subject) → identify all data locations (production DB, analytics, backups, logs, third-party services) → execute deletion: remove primary records, purge from search indexes, overwrite backup records (if feasible), request deletion from third-party sub-processors → verify deletion (confirm records removed) → provide confirmation to data subject.

Backup handling: traditional backups make immediate erasure difficult. Strategy: exclude the data subject's records from future backups, mark records as "deleted" with encryption key destruction (making data irrecoverable even if backup exists), or maintain a "deletion shadow" that masks deleted records during restore. Regulatory guidance increasingly accepts encryption key destruction as equivalent to deletion.
