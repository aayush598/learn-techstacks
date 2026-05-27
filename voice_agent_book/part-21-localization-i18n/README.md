# Part 21: Localization & Internationalization

> **Duration:** i18n Phase (Weeks 16-24)  
> **Goal:** Build a comprehensive localization system supporting 20+ languages, RTL, regional compliance, and cultural adaptation.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [i18n Architecture & Strategy](ch-01-i18n-architecture-strategy/README.md) | Translation management, locale detection, fallback chains, i18n routing, translation file structure |
| 02 | [React/Next.js Internationalization](ch-02-react-nextjs-internationalization/README.md) | next-intl setup, server component i18n, client component i18n, dynamic content, pluralization |
| 03 | [Translation Management Workflow](ch-03-translation-management-workflow/README.md) | Translation files, PO/JSON format, translator workflow, automated translation (DeepL/LibreTranslate), versioning |
| 04 | [RTL Language Support](ch-04-rtl-language-support/README.md) | CSS logical properties, RTL layout testing, bidirectional text, number formatting, font selection |
| 05 | [Regional Number & Currency Formatting](ch-05-regional-number-currency-formatting/README.md) | Intl.NumberFormat, locale-aware formats, currency display, date/time formatting, measurement units |
| 06 | [Per-Agent Language Configuration](ch-06-per-agent-language-configuration/README.md) | Language assignment, STT/TTS language sync, fallback language, multi-language agents |
| 07 | [Region-Specific Compliance Presets](ch-07-region-specific-compliance-presets/README.md) | Country-specific regulations, compliance profiles, auto-detection, preset library |
| 08 | [Cultural Tone Adaptation](ch-08-cultural-tone-adaptation/README.md) | Politeness levels, formality per culture, greeting customs, time references, cultural sensitivities |
| 09 | [Local Phone Number Provisioning](ch-09-local-phone-number-provisioning/README.md) | Per-country number search, local presence, number availability, regulatory requirements per country |
| 10 | [Platform UI Translation Workflow](ch-10-platform-ui-translation-workflow/README.md) | CrowdIn/Lokalise alternative, community translations, translation memory, quality assurance |

---

## Key Open-Source Tools

- **next-intl** (MIT) — Next.js internationalization
- **i18next** (MIT) — JavaScript i18n framework
- **Lingui** (MIT) — i18n for React
- **LibreTranslate** (AGPL 3.0) — Self-hosted machine translation
- **date-fns** (MIT) — Locale-aware date formatting
- **Intl** (built-in) — Native browser i18n APIs

---

## Learning Objectives

- Design a scalable i18n architecture for a multi-tenant SaaS
- Implement internationalization in Next.js with next-intl
- Build a translation management workflow for translators
- Support RTL languages with proper CSS and testing
- Implement locale-aware number, currency, and date formatting
- Configure per-agent language with STT/TTS sync
- Create region-specific compliance presets
- Adapt conversation tone for cultural differences
- Implement local phone number provisioning by country
- Build a platform UI translation workflow with community contributions
