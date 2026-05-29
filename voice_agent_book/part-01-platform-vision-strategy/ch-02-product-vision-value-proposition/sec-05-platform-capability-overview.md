# Section 05: Platform Capability Overview

## Platform Map

Our platform spans 20 capability categories organized into 5 layers. This section provides a high-level reference map of every major feature area across the product.

```
Platform Capability Map
┌────────────────────────────────────────────────────────────────────┐
│ Layer 5: Ecosystem                                                 │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Part 22  │ │ Part 18  │ │ Part 24  │ │ Part 25              │  │
│ │Marketpl. │ │Dev Tools │ │ Scaling  │ │ Production Launch    │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Layer 4: Intelligence & Builder                                    │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Part 5   │ │ Part 6  │ │ Part 13  │ │ Part 11              │  │
│ │AI Engine │ │Agent Bld│ │Knowledge │ │Analytics/Reporting   │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Layer 3: Voice & Communication                                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Part 4   │ │ Part 7  │ │ Part 8   │ │ Part 12              │  │
│ │Core Voice│ │Telephony │ │Handoff   │ │Recording/Transcript  │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Layer 2: Business & Operations                                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Part 9   │ │ Part 10  │ │ Part 17  │ │ Part 20             │  │
│ │Campaigns │ │Integrat. │ │Billing   │ │Notifications         │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Layer 1: Platform Foundation                                       │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Part 14  │ │ Part 15  │ │ Part 16  │ │ Part 19             │  │
│ │Multi-    │ │Security  │ │User Mgmt │ │Testing/QA            │  │
│ │Tenant    │ │Compliance│ │          │ │                      │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ Part 2 + 3: Technology Stack & Environment Setup                  │
├────────────────────────────────────────────────────────────────────┤
│ Part 1: Vision & Strategy → This document                         │
└────────────────────────────────────────────────────────────────────┘
```

## Core Capabilities by Part

| Part | Category | Primary Capabilities | Key OSS Tools |
|------|----------|---------------------|---------------|
| 04 | Core Voice Engine | ASR, TTS, VAD, streaming, barge-in | Whisper, Coqui, Silero VAD |
| 05 | AI Conversation Intelligence | LLM integration, RAG, tool calling, memory | LangChain, LlamaIndex, Qdrant |
| 06 | Agent Builder | Visual builder, flows, conditions, variables | React Flow, Blockly |
| 07 | Telephony | SIP, WebRTC, IVR, routing, queueing | LiveKit, SIP.js, FreeSwitch |
| 08 | Human Handoff | Escalation, warm transfer, whisper, coach | N/A (protocol-driven) |
| 09 | Campaign Management | Outbound dialer, scheduling, lists, A/B testing | N/A (custom) |
| 10 | Integrations | CRM, ERP, custom webhooks, Zapier | Merge.dev, Paragon |
| 11 | Analytics | Dashboards, reporting, sentiment, funnels | ClickHouse, PostHog, ECharts |
| 12 | Recording/Transcription | Storage, search, redaction, compliance | MinIO, Elasticsearch |
| 13 | Knowledge Base | RAG, document ingestion, chunking, retrieval | Qdrant, Unstructured, LlamaIndex |
| 14 | Multi-Tenant | Isolation, branding, sub-accounts, reseller | N/A (architectural) |
| 15 | Security/Compliance | Encryption, audit, SOC 2, HIPAA, GDPR | OPA, Vault, CertManager |
| 16 | User Management | RBAC, SSO, SAML, SCIM, teams | Keycloak, Auth0, Casdoor |
| 17 | Billing/Subscription | Usage metering, invoicing, marketplace billing | Stripe, Lago, Metronome |
| 18 | Developer Tools | SDKs, CLI, API, webhooks, terraform | OpenAPI, Fern, docusaurus |
| 19 | Testing/QA | Load testing, voice testing, replay, monitoring | k6, Locust, Playwright |
| 20 | Notifications | Email, SMS, push, voice alerts, webhook | Novu, Courier, SendGrid |
| 21 | Localization | i18n, l10n, translations, locale detection | i18next, Lingui |
| 22 | Marketplace | Templates, voices, plugins, revenue sharing | N/A (custom marketplace) |
| 23 | DevOps | CI/CD, infra, monitoring, alerts, backups | Terraform, K8s, Helm, Prometheus |
| 24 | Scaling | Performance, caching, CDN, global distribution | Redis, CDN, K8s HPA |

## Architecture Decision Records by Capability

```typescript
interface CapabilityDecision {
  capability: string;
  decisions: ArchitecturalDecision[];
}

interface ArchitecturalDecision {
  id: string;
  title: string;
  context: string;
  decision: string;
  consequences: string;
  status: 'proposed' | 'accepted' | 'deprecated' | 'superseded';
}

const platformDecisions: CapabilityDecision[] = [
  {
    capability: 'Voice Engine',
    decisions: [{
      id: 'ADR-001',
      title: 'Use Whisper for STT with Coqui TTS fallback',
      context: 'Need high accuracy STT with low-cost TTS that supports voice cloning',
      decision: 'Whisper large as primary, Coqui XTTS for TTS with Piper as CPU fallback',
      consequences: 'GPU dependency for optimal performance, but best accuracy/cost tradeoff',
      status: 'accepted',
    }],
  },
  // Additional ADRs in respective part docs
];
```

## Feature Maturity Matrix

| Feature | MVP (M1-3) | Phase 2 (M4-6) | Phase 3 (M7-9) | Phase 4 (M10-12) | Phase 5 (M13-18) |
|---------|-----------|----------------|----------------|------------------|------------------|
| Voice Engine | ✅ Basic | ✅ Streaming | ✅ Barge-in | | |
| Agent Builder | ✅ Simple | ✅ Visual flow | ✅ Conditions | ✅ Templates | |
| Analytics | ⬜ | ✅ Basic | ✅ Advanced | ✅ Custom | ✅ AI insights |
| Telephony | ✅ Inbound | ✅ Outbound | ✅ IVR | ✅ SIP trunk | |
| White-Label | | | | ✅ | ✅ Advanced |
| Compliance | ⬜ | ⬜ | ✅ SOC 2 | ✅ HIPAA | ✅ PCI DSS |
| Marketplace | | | | ✅ MVP | ✅ Full |
| Multi-Tenant | ✅ Basic | | | ✅ Full | ✅ Enterprise |

## Integration Points Between Capabilities

```
Capability Integration Map
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│Voice   │────▶│AI      │────▶│Agent   │────▶│Tele-   │
│Engine  │     │Engine  │     │Builder │     │phony   │
└────────┘     └────────┘     └────────┘     └────────┘
    │              │                            │
    ▼              ▼                            ▼
┌────────┐     ┌────────┐                 ┌────────┐
│Record  │     │Analytics                 │Campaign│
│/Transc │     │Reporting│                 │Mgmt    │
└────────┘     └────────┘                 └────────┘
    │              │                            │
    ▼              ▼                            ▼
┌────────┐     ┌────────┐                 ┌────────┐
│Storage │     │BI Tools│                 │Integr. │
└────────┘     └────────┘                 └────────┘
```

## Tools & Documentation

- **UML/Architecture diagrams:** PlantUML, Mermaid, Diagrams.net
- **Documentation:** Docusaurus, Nextra, Storybook
- **API reference:** OpenAPI 3.1, Fern, ReadMe
- **Feature tracking:** Linear, Notion, ProductBoard
- **Decision records:** ADR directory in repository (adr/*.md)
