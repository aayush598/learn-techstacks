# Section 04: Phase 3 — Scale (Months 7-9)

## Phase Overview

Phase 3 transitions the platform from working prototype to scalable product. Key additions: full multi-tenant with billing, advanced analytics, campaign management, integrations, and WebSocket API.

```
Phase 3 Scale Features
┌─────────────────────────────────────────────────────────────────────────┐
│ Month 7: Multi-Tenant + Billing       Month 8: Analytics + Campaigns   │
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ Full multi-tenant         │  │ Advanced analytics          │        │
│ │ Tenant provisioning       │  │ ClickHouse data warehouse   │        │
│ │ Usage metering            │  │ Real-time dashboards        │        │
│ │ Stripe billing integration │  │ Custom metric builder      │        │
│ │ Automated invoicing       │  │ Campaign management         │        │
│ │ Dunning                    │  │ Outbound campaigns          │        │
│ │ Usage alerts              │  │ A/B testing agents          │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
├─────────────────────────────────────────────────────────────────────────┤
│ Month 9: Integrations + API Ecosystem                                  │
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ CRM integrations (5)      │  │ WebSocket API               │        │
│ │ • Salesforce, HubSpot     │  │ Real-time call events       │        │
│ │ • Zoho, Pipedrive         │  │ Live transcript streaming   │        │
│ │ • Close                   │  │ Custom UI development       │        │
│ │ n8n/Zapier integration    │  │ Webhook system              │        │
│ │ Merge.dev embedded iPaaS  │  │ API rate limiting           │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Deliverables

### Full Multi-Tenant & Billing
- **Tenant provisioning:** Automated tenant creation with isolated resources
- **Usage metering:** Real-time tracking of minutes, storage, API calls
- **Billing integration:** Stripe subscriptions with usage-based overages
- **Tier management:** Automated upgrades/downgrades between tiers
- **Usage alerts:** Email and in-app notifications at 80%, 100%, 120% of limits

### Advanced Analytics
- **ClickHouse data warehouse:** High-performance analytics queries
- **Real-time dashboards:** Live call metrics, agent performance, system health
- **Custom metrics:** Build-your-own metric from event data
- **Scheduled reports:** Daily/weekly email reports
- **Export:** CSV/JSON export of analytics data

### Campaign Management
- **Outbound campaigns:** Multi-contact, schedule-based outbound calling
- **List management:** Import/export contact lists (CSV, API)
- **A/B testing:** Test multiple agent configurations on split traffic
- **Scheduling:** Time-window-based calling, timezone-aware
- **Results tracking:** Per-campaign success metrics

### Integrations
- **CRM connectors:** Salesforce, HubSpot, Zoho, Pipedrive, Close
- **Embedded iPaaS:** Merge.dev for integration management
- **Zapier/Make:** No-code integration triggers and actions
- **n8n:** Self-hosted automation workflows

## Phase 3 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Phase 3 Architecture                             │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ New: ClickHouse Cluster (Analytics) • n8n (Automation)            │ │
│ │ Merge.dev (Integrations) • Campaign Engine                        │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────┐  ┌───────────────────────┐                  │
│ │ Billing Service       │  │ Campaign Service      │                  │
│ │ • Stripe integration  │  │ • Outbound engine     │                  │
│ │ • Usage metering      │  │ • List management     │                  │
│ │ • Invoice generation  │  │ • A/B testing         │                  │
│ └───────────────────────┘  └───────────────────────┘                  │
│ ┌───────────────────────┐  ┌───────────────────────┐                  │
│ │ Analytics Service     │  │ Integration Service   │                  │
│ │ • ClickHouse queries  │  │ • Merge.dev gateway   │                  │
│ │ • Dashboard API       │  │ • Webhook dispatch    │                  │
│ │ • Report scheduling   │  │ • Zapier/n8n          │                  │
│ └───────────────────────┘  └───────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Phase 3 Technical Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Analytics DB | ClickHouse, TimescaleDB, Druid | ClickHouse | Columnar, fast aggregations |
| Embedded iPaaS | Merge.dev, Paragon, Cyclr | Merge.dev | Unified CRM API, good DX |
| Automation | n8n, Zapier, Make | n8n (self-hosted) + Zapier (cloud) | Both extremes covered |
| Campaign engine | Custom, MessageBird, AWS Pinpoint | Custom | Tight coupling with voice agents |

## Phase 3 Team Growth

| Role | Phase 2 | Phase 3 Addition | Total |
|------|---------|-----------------|-------|
| Full-stack engineer | 3 | +2 | 5 |
| ML engineer | 2 | 0 | 2 |
| Product manager | 1 | +1 | 2 |
| Designer | 1 | 0 | 1 |
| DevOps | 0.5 | +0.5 | 1 |

## Phase 3 Exit Criteria

- [ ] Multi-tenant billing operational (auto-provision, invoice, dunning)
- [ ] ClickHouse analytics with <1s query for 30-day aggregates
- [ ] 5 CRM integrations live and tested
- [ ] Campaign management with A/B testing
- [ ] WebSocket API with <100ms event delivery
- [ ] 500+ active users
- [ ] 500K+ total call minutes
- [ ] $20K+ MRR
- [ ] Churn rate <8% monthly

## Phase 3 Budget

| Category | Monthly Cost |
|----------|-------------|
| Infrastructure | $8K-12K |
| GPU compute | $4K-6K |
| SaaS | $4K-5K |
| Compensation (10 FTE) | $160K-200K |
| **Total monthly** | **$176K-223K** |

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| ClickHouse complexity | Medium | 50% | Start with simple views, iterate |
| Billing metering accuracy | Critical | 20% | Multiple validation layers, manual checks |
| Integration maintenance burden | High | 60% | Use Merge.dev to reduce per-integration effort |
| Campaign scale issues | High | 30% | Rate limiting, queue-based processing |

## Open Source Tools Added

| Tool | Purpose | Alternative |
|------|---------|-------------|
| ClickHouse | Analytics database | TimescaleDB |
| n8n | Workflow automation | Huginn, Temporal |
| Grafana | Dashboard visualization | Metabase |
| BullMQ | Job queue for campaigns | RabbitMQ, Celery |
| Zod | Schema validation | Joi, Yup |

## Production Considerations

- ClickHouse: Use AggregatingMergeTree for pre-aggregated metrics
- Billing: Eventually consistent metering (5-minute delay acceptable)
- Campaigns: Rate limited per campaign (max 100 calls/hour to prevent TCPA issues)
- Integrations: Circuit breaker pattern for third-party API failures
- WebSocket: Redis PubSub for real-time event distribution
- Monitoring: Dashboard for real-time usage + billing accuracy alerts
