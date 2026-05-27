# Chapter 05: Voicemail Detection & Drop

> **Part:** 09 - Campaign Management

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [AMD Technology Overview](sec-01-amd-technology-overview.md) | Answering Machine Detection — technology comparison, ML vs. heuristic approaches |
| 02 | [AMD Engine Implementation](sec-02-amd-engine-implementation.md) | Real-time AMD engine — audio feature extraction, classification model, confidence scoring |
| 03 | [Voicemail Drop Strategy](sec-03-voicemail-drop-strategy.md) | Voicemail drop — pre-recorded message delivery, silence detection, timing considerations |
| 04 | [Pre-Recorded Message Management](sec-04-pre-recorded-message-management.md) | Message library, per-campaign messages, dynamic content injection, A/B testing |
| 05 | [Voicemail Analysis & Classification](sec-05-voicemail-analysis-classification.md) | Voicemail transcription, intent classification, urgency detection, follow-up routing |
| 06 | [AMD Tuning & Calibration](sec-06-amd-tuning-calibration.md) | Sensitivity adjustment, per-carrier calibration, false positive/negative trade-offs |
| 07 | [Call Progress Analysis](sec-07-call-progress-analysis.md) | Live answer, SIT tones, fax/modem detection, fast busy, operator intercept detection |
| 08 | [AMD Fallback Strategies](sec-08-amd-fallback-strategies.md) | Human agent fallback, AMD retry, carrier-specific handling, confidence-based routing |

---

## Key Takeaways

- AMD accuracy depends on ML model quality, audio sampling, and carrier characteristics
- Voicemail drop requires precise timing between greeting detection and message playback
- Call progress analysis must handle diverse telephony signals (SIT tones, fax, intercept)
- AMD tuning involves balancing false positives (hanging up on humans) vs. false negatives (missing voicemail)
- Fallback strategies ensure graceful degradation when AMD confidence is low
