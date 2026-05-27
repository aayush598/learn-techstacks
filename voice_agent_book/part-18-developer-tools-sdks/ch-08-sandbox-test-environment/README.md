# Chapter 08: Sandbox & Test Environment

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Sandbox Architecture](sec-01-sandbox-architecture.md) | Isolated environment, sandbox vs production, data isolation, configuration mirroring |
| 02 | [Test Phone Numbers](sec-02-test-phone-numbers.md) | Virtual test numbers, predefined scenarios, echo test numbers, SIP test endpoints |
| 03 | [Mock Voice Agent Engine](sec-03-mock-voice-agent-engine.md) | Simulated AI responses, predefined conversation flows, latency simulation, error injection |
| 04 | [Credit-Free Testing Mode](sec-04-credit-free-testing-mode.md) | Zero-cost testing, usage not billed, rate limits in sandbox, sandbox quotas |
| 05 | [Request/Response Logging](sec-05-request-response-logging.md) | Full request/response capture, replay capability, debug logs, inspection UI |
| 06 | [Scenario Simulation](sec-06-scenario-simulation.md) | Predefined test scenarios, custom scenario creation, edge case testing, load simulation |
| 07 | [Sandbox Isolation](sec-07-sandbox-isolation.md) | Tenant isolation in sandbox, no cross-contamination, separate databases, reset capability |
| 08 | [Sandbox-to-Production Promotion](sec-08-sandbox-to-production-promotion.md) | Configuration export from sandbox, validation checks, production import, environment diff |

---

## Sandbox Architecture

```
[Developer] → Sandbox API Endpoint: api.sandbox.voiceagent.com
                  │
            [Sandbox Gateway]
              ├── Auth (sandbox-only keys)
              └── Rate Limiting (higher limits)
                  │
            [Sandbox Services]
              ├── Mock STT (simulated transcription)
              ├── Mock AI (predefined responses)
              ├── Mock TTS (short audio clips)
              └── Test Phone Numbers (virtual)
                  │
            [Sandbox Database]
              ├── Isolated from production
              ├── Reset on demand
              └── Full request logging
```

---

## Learning Objectives

- Design isolated sandbox environment mirroring production
- Create test phone numbers with predefined scenarios
- Build mock voice agent engine for testing
- Implement credit-free testing with sandbox quotas
- Capture full request/response logs for debugging
- Create scenario simulation for edge case testing
- Ensure sandbox isolation with no cross-contamination
- Build sandbox-to-production promotion workflow
