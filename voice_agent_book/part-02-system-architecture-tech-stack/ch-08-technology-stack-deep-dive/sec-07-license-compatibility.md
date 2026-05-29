# Section 07: License Compatibility

## License Overview

Every dependency in the stack is reviewed for license compatibility. The platform uses only **permissive licenses** (MIT, Apache 2.0, BSD, PostgreSQL) to avoid legal risk when distributing or selling the SaaS product. **Copyleft licenses** (AGPL, GPL) are avoided or carefully contained.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LICENSE COMPATIBILITY MATRIX                     │
│                                                                     │
│  Library           License      Compatible   Notes                 │
│  ──────────────────────────────────────────────────────────        │
│  Next.js            MIT          ✅          Safe for SaaS         │
│  React              MIT          ✅                                │
│  TypeScript         MIT          ✅                                │
│  Tailwind CSS       MIT          ✅                                │
│  Radix UI           MIT          ✅                                │
│  TanStack Query     MIT          ✅                                │
│  Prisma             Apache 2.0   ✅                                │
│  PostgreSQL         PostgreSQL   ✅          Permissive            │
│  Redis              BSD          ✅          Modified BSD          │
│  MinIO              AGPL v3      ⚠️         AGPL exception        │
│  ClickHouse         Apache 2.0   ✅                                │
│  Kafka              Apache 2.0   ✅                                │
│  Whisper (faster)   MIT          ✅                                │
│  Coqui TTS          CPML         ⚠️         Commercial use OK     │
│  Silero VAD         MIT          ✅                                │
│  LangChain          MIT          ✅                                │
│  Prometheus         Apache 2.0   ✅                                │
│  Grafana            AGPL v3      ⚠️         Grafana license       │
│  BullMQ             MIT          ✅                                │
│  Auth.js            ISC          ✅                                │
└─────────────────────────────────────────────────────────────────────┘
```

## Copyleft Risk Assessment

```typescript
interface LicenseAssessment {
  name: string;
  license: string;
  spdxId: string;
  risk: 'none' | 'low' | 'medium' | 'high';
  notes: string;
  mitigation: string;
}

const LICENSE_ASSESSMENTS: LicenseAssessment[] = [
  {
    name: 'MinIO',
    license: 'GNU AGPL v3',
    spdxId: 'AGPL-3.0-only',
    risk: 'low',
    notes: 'AGPL v3 with commercial exception — not triggered when used as a separate process (API access). Safe for SaaS.',
    mitigation: 'Access MinIO via S3 API over network; do not modify and redistribute MinIO source.',
  },
  {
    name: 'Grafana',
    license: 'GNU AGPL v3',
    spdxId: 'AGPL-3.0-only',
    risk: 'low',
    notes: 'Grafana AGPL applies only if you modify and distribute Grafana. Using unmodified Grafana behind our SaaS is safe.',
    mitigation: 'Use Grafana as-is; no custom forks distributed.',
  },
  {
    name: 'Coqui TTS',
    license: 'Coqui Public Model License (CPML)',
    spdxId: 'LicenseRef-CPML',
    risk: 'low',
    notes: 'CPML allows commercial use of the model outputs. Training derivative models requires additional licensing.',
    mitigation: 'Use pre-trained models via API; do not fine-tune or redistribute model weights.',
  },
];
```

## Dependency License Audit

```typescript
// Automated license auditing in CI
// .github/workflows/license-audit.yml
interface LicenseRule {
  allowed: string[];       // SPDX IDs that are permitted
  restricted: string[];    // SPDX IDs that require review
  forbidden: string[];     // SPDX IDs that are blocked
}

const LICENSE_RULES: LicenseRule = {
  allowed: [
    'MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause',
    'ISC', 'Unlicense', 'CC0-1.0', 'PostgreSQL', 'Python-2.0',
  ],
  restricted: [
    'AGPL-3.0-only', 'AGPL-3.0-or-later',
    'LGPL-3.0-only', 'LGPL-3.0-or-later',
    'MPL-2.0',
  ],
  forbidden: [
    'GPL-2.0-only', 'GPL-2.0-or-later',
    'GPL-3.0-only', 'GPL-3.0-or-later',
    'BUSL-1.1',     // Business Source License
    'SSPL-1.0',     // Server Side Public License
  ],
};

// CI check using license-checker
// npx license-checker --failOn "GPL-2.0;GPL-3.0;AGPL-3.0;BUSL-1.1;SSPL-1.0"
```

## Dependency Graph (Direct Dependencies)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LICENSE DEPENDENCY GRAPH                         │
│                                                                     │
│  MIT/ISC                                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Next.js  React  TypeScript  Tailwind  Radix  TanStack      │   │
│  │  Zustand  Zod  Lucide  Framer  BullMQ  LangChain  Auth.js   │   │
│  │  Prisma  Whisper  Silero  Pino  date-fns  Recharts          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Apache 2.0                                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ClickHouse  Kafka  Prometheus  Terraform  ArgoCD            │   │
│  │  OpenTelemetry  Helm  fluent-bit  envoy                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  AGPL v3 (with commercial exception / separate process)             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MinIO  Grafana                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Other Permissive                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL (PostgreSQL License)  Redis (BSD)               │   │
│  │  Coqui TTS (CPML)  Silero (MIT)                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## License Compliance for Distribution

```typescript
// If distributing the application (not just SaaS):
interface DistributionLicense {
  component: string;
  license: string;
  noticeRequired: boolean;  // Must include license text
  attributionText: string;  // Required attribution
}

const DISTRIBUTION_NOTICES: DistributionLicense[] = [
  {
    component: 'Next.js',
    license: 'MIT',
    noticeRequired: true,
    attributionText: 'Copyright (c) Vercel Inc. MIT License',
  },
  {
    component: 'OpenTelemetry',
    license: 'Apache 2.0',
    noticeRequired: true,
    attributionText: 'Copyright The OpenTelemetry Authors. Apache 2.0',
  },
  // Comprehensive list maintained in NOTICE.txt
];

// NOTICE.txt is included in all distributed builds
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Preferred license | MIT | Maximum permissiveness, no restrictions on SaaS/distribution |
| Copyleft policy | Avoid GPL/AGPL for direct dependencies | Legal complexity, potential viral effect |
| AGPL exception | Allowed if separate process (API access) | MinIO and Grafana used as separate services |
| Audit frequency | Every PR (automated) + quarterly review | Catch new restricted dependencies early |
| Attribution | NOTICE.txt in distribution | Apache 2.0 and MIT compliance requirement |

## Integration Points

- **Ch 08 (Open-Source vs Proprietary)** — License risk is a factor in build-vs-buy decisions
- **Ch 10 (Supply Chain Security)** — Dependency scanning includes license checks
- **Ch 08 (Cost Analysis)** — Open-source licensing eliminates per-seat/per-usage costs

## Production Considerations

- **Automated Checks**: CI pipeline fails on forbidden licenses, warns on restricted licenses
- **License Exceptions**: Reviewed by legal counsel; documented in LICENSE_EXCEPTIONS.md
- **SBOM Generation**: SPDX 2.3 SBOM generated per build via CycloneDX plugin
- **Dual Licensing**: If AGPL dependencies become problematic, maintain compatibility layer via containerization
- **Audit Trail**: All license reviews logged with date, reviewer, and rationale
