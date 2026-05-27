# Section 04: Data Portability

Data portability (GDPR Article 20) enables data subjects to receive their personal data in a structured, commonly used, machine-readable format and transfer it to another controller. The platform provides self-service export in JSON and CSV formats covering all personal data. The export is available via the dashboard without requiring a formal request.

Portable data scope: account information (name, email, phone, address), communication data (call logs, transcripts, recordings), usage data (API usage, billing history), configuration data (agent configurations, settings, integrations), and interaction data (support tickets, feedback). Excluded: data that would infringe on others' rights (call recordings containing other parties' voices require consent for transfer).

The export system generates a portable package within 24 hours (automated) and makes it available for download for 7 days. The format follows common data portability standards (JSON Schema for account data, CSV for tabular data, WAV/MP3 for recordings). Large exports are split into multiple files with a manifest document describing the contents.
