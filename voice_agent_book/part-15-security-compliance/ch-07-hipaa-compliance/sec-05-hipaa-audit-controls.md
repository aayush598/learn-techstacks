# Section 05: HIPAA Audit Controls

HIPAA audit controls require mechanisms to record and examine access to ePHI. The platform's audit system captures every ePHI access event: who accessed, what PHI, when, from where, and for what purpose. Audit logs are protected from modification and retained for 6 years (HIPAA minimum).

HIPAA-specific audit events: create/access/update/delete ePHI records, user authentication for ePHI systems, permission changes affecting ePHI access, encryption key access, PHI export/download, BAA status changes, and emergency access (break-glass) events. Each event includes the specific PHI accessed (e.g., recording ID, patient MRN).

Audit log protection: logs are stored in WORM (write-once, read-many) storage, encrypted at rest, and replicated to a separate secure location. Access to audit logs is restricted to the security/compliance team. Logs are reviewed regularly for suspicious patterns. Automated alerts trigger on: multiple failed PHI access attempts, PHI access outside normal hours, bulk PHI export, and unauthorized PHI access attempts.
