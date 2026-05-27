# Section 01: Export Tenant Data (JSON/CSV)

Data export enables tenants to download their data in portable formats (JSON, CSV, NDJSON). This supports data portability requirements (GDPR Article 20), tenant migration off the platform, and internal analytics. The export system generates archive files containing all tenant-owned data: agents, calls, recordings, transcripts, analytics, and configuration.

Export scope includes: agent configurations (name, prompts, voice settings), call logs (metadata, duration, outcome), recordings (audio files in WAV/MP3), transcripts (JSON with speaker labels and timestamps), analytics reports (aggregated metrics), and settings (branding, integrations, webhooks). Tenants select which data types to include.

The export pipeline: user initiates export from dashboard → job queued in async worker → worker queries tenant data from all services → data is written to temporary storage → archive is created (ZIP with organized directory structure) → tenant is notified with download link → archive is auto-deleted after 7 days. Exports of large tenants may take hours and are tracked with progress indicators.
