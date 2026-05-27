# Section 01: Usage Tracking & Metering

Usage tracking captures every billable action a tenant performs—API calls, call minutes, storage, AI model tokens, and SMS messages. Metering data flows from the production systems (call processing, API gateway, media servers) into a time-series database for real-time aggregation and billing. Each event is tagged with the tenant ID, resource type, quantity, and timestamp.

The metering pipeline consists of: event producers (each service emits usage events as JSON messages), message queue (events are buffered for reliability), aggregation service (rolls up raw events into hourly/daily buckets), and storage (time-series database for queries). The pipeline must handle high throughput (millions of events per day) with minimal latency.

For a voice agent platform, metered resources include: call duration (per-minute), AI processing (seconds of STT/TTS/LLM), storage (GB-days for recordings), phone numbers (per-number per-day), SMS (per-message), API calls (per-endpoint), and concurrent call slots. Each resource has a unit and rate for billing.
