# Part 12: Call Recording & Transcription

> **Duration:** Recording Phase (Weeks 12-18)  
> **Goal:** Build a comprehensive call recording and transcription system with speaker diarization, PII redaction, search, and compliance.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Call Recording Pipeline](ch-01-call-recording-pipeline/README.md) | Dual-channel recording, mix-minus, storage strategy (MinIO/S3), record on demand, automatic recording |
| 02 | [Real-Time Transcription Engine](ch-02-real-time-transcription-engine/README.md) | Streaming STT, interim results, final transcripts, punctuation restoration, formatting post-processing |
| 03 | [Speaker Diarization (Who Said What)](ch-03-speaker-diarization/README.md) | Speaker identification, diarization models, speaker labeling, overlap handling, channel-based diarization |
| 04 | [Secure Storage & Archival](ch-04-secure-storage-archival/README.md) | MinIO/S3 bucket structure, encryption at rest, lifecycle policies, archival tier, retention compliance |
| 05 | [Transcript Search & Archive](ch-05-transcript-search-archive/README.md) | Full-text search (PostgreSQL tsvector), phonetic search, filter by date/speaker/sentiment, pagination |
| 06 | [PII Redaction & Data Privacy](ch-06-pii-redaction-data-privacy/README.md) | SSN, credit card, name, address detection, redaction modes (mask/remove/warning), audio redaction |
| 07 | [Keyword & Phrase Spotting](ch-07-keyword-phrase-spotting/README.md) | Real-time keyword detection, phrase matching, alert triggers, compliance phrases, competitive mentions |
| 08 | [Call Highlight Extraction](ch-08-call-highlight-extraction/README.md) | Key moment detection, sentiment spikes, action items, objection points, auto-generated highlights |
| 09 | [Transcript Export & Translation](ch-09-transcript-export-translation/README.md) | Export formats (TXT, PDF, DOCX, SRT, VTT), auto-translation, bilingual transcripts, subtitle generation |
| 10 | [Compliance-Hold & Audit Trail](ch-10-compliance-hold-audit-trail/README.md) | Legal hold, tamper-proof storage, access logs, chain of custody, eDiscovery export, retention holds |

---

## Recording Pipeline

```
Audio Stream → Dual-Channel Mixer → Recording Buffer → MinIO/S3
                     ↓
               STT Stream → Diarization → Transcript DB
                     ↓
               PII Detector → Redacted Copy
                     ↓
               Keyword Spotter → Alerts
```

---

## Key Open-Source Tools

- **MinIO** (AGPL 3.0) — S3-compatible object storage
- **Whisper** (MIT) — Transcription
- **PostgreSQL** (PostgreSQL) — Full-text search
- **presidio** (MIT) — PII detection & redaction (Microsoft)
- **LibreOffice** (MPL 2.0) — Document conversion for exports

---

## Learning Objectives

- Build a dual-channel audio recording pipeline with cloud storage
- Implement real-time streaming transcription with speaker diarization
- Design a secure storage system with encryption and lifecycle management
- Build a searchable transcript archive with full-text search
- Implement PII redaction for both text transcripts and audio recordings
- Create real-time keyword and phrase spotting for compliance
- Build automatic call highlight extraction for key moments
- Support multiple export formats with auto-translation
- Implement legal hold and tamper-proof audit trails
