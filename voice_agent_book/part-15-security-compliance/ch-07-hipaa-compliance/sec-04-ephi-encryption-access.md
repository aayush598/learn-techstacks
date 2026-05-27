# Section 04: ePHI Encryption & Access Control

ePHI encryption and access control implementation satisfies HIPAA's technical safeguard requirements. All ePHI is encrypted at rest (AES-256) and in transit (TLS 1.3). Access to ePHI is role-based with strict need-to-know principles. Every ePHI access is logged and audited.

ePHI data identification: call recordings (marked as potential PHI when healthcare context detected), transcripts (PHI scanned and tagged), patient metadata (name, DOB, phone, medical record number), and API payloads containing healthcare information. Encryption is applied at the field level for database storage and at the file level for recordings.

Access controls for ePHI: separate role "healthcare_worker" with specific PHI access permissions, time-based access restrictions (PHI access logged and flagged if outside business hours), geographic restrictions (PHI access from approved locations only), and emergency access procedure (break-glass with automatic post-event review). PHI data has a special visual indicator in the UI to prevent accidental exposure.
