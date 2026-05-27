# Chapter 05: White-Label Branding System

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [CSS Variable-Based Theming](sec-01-css-variable-theming.md) | Design token system, CSS custom properties, runtime theme switching, dark/light mode per tenant |
| 02 | [Custom Logo & Favicon Management](sec-02-custom-logo-favicon.md) | Logo upload & resizing, CDN delivery, favicon generation, SVG support, format conversion |
| 03 | [Color Palette & Typography System](sec-03-color-palette-typography.md) | Primary/secondary/accent colors, font selection, type scale, accessibility compliance (WCAG) |
| 04 | [White-Label Email Templates](sec-04-email-templates.md) | Branded transactional emails, template inheritance, header/footer customization, preview mode |
| 05 | [Custom Login Page & Auth UI](sec-05-custom-login-page.md) | Branded authentication screens, custom SSO login, tenant-specific terms of service, privacy links |
| 06 | [Brand Asset CDN Strategy](sec-06-brand-asset-cdn.md) | Asset upload pipeline, image optimization, cache invalidation, versioned asset URLs |
| 07 | [White-Label Mobile App Support](sec-07-mobile-app-white-label.md) | Branded mobile apps, app icon/splash screen, custom app store listing, deep linking |
| 08 | [Branding Preview & Versioning](sec-08-branding-preview-versioning.md) | Live preview of branding changes, draft vs published state, branding version history, rollback |

---

## Design Token Architecture

```
:root {
  /* Tenant-specific tokens injected at runtime */
  --brand-primary: var(--tenant-primary, #6366f1);
  --brand-secondary: var(--tenant-secondary, #8b5cf6);
  --brand-font-family: var(--tenant-font, 'Inter', sans-serif);
  --brand-logo-url: var(--tenant-logo, '/default-logo.svg');
  --brand-favicon: var(--tenant-favicon, '/default-favicon.ico');
  --brand-radius: var(--tenant-radius, 8px);
}
```

---

## Learning Objectives

- Build a CSS variable-based theming engine for per-tenant branding
- Implement custom logo and favicon management with CDN delivery
- Design color palette and typography customization system
- Create white-label email templates with brand inheritance
- Build custom login page and authentication UI per tenant
- Architect brand asset pipeline with CDN optimization
- Extend white-label branding to mobile applications
- Implement branding preview with version control and rollback
