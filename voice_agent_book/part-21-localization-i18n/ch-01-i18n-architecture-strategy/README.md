# Chapter 01: i18n Architecture & Strategy

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Translation Management Architecture](sec-01-translation-management-architecture.md) | Translation file structure, key naming conventions, namespace organization, translation registry |
| 02 | [Locale Detection & Selection](sec-02-locale-detection-selection.md) | Browser locale detection, user preference, account-based locale, geolocation detection |
| 03 | [Fallback Chains](sec-03-fallback-chains.md) | Multi-level fallback, regional fallback (es-MX → es → en), namespace fallback, missing key handling |
| 04 | [i18n Routing Strategy](sec-04-i18n-routing-strategy.md) | Subdomain-based (de.example.com), path-based (example.com/de), domain-based (example.de), SEO implications |
| 05 | [Translation File Structure](sec-05-translation-file-structure.md) | JSON/PO file format, nested vs flat keys, file splitting strategy, lazy loading |
| 06 | [Locale-Aware Static Generation](sec-06-locale-aware-static-generation.md) | Next.js SSG with i18n, per-locale builds, dynamic route generation, ISR with i18n |
| 07 | [Testing Internationalization](sec-07-testing-internationalization.md) | Locale switching in tests, translation key testing, RTL testing, visual regression per locale |
| 08 | [CDN & Caching for i18n](sec-08-cdn-caching-i18n.md) | Translation file CDN caching, cache invalidation on update, edge delivery of translations |
