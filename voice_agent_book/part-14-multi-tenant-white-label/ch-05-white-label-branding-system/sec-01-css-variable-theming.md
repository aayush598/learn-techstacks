# Section 01: CSS Variable-Based Theming

## Overview

CSS variable-based theming enables dynamic per-tenant white-label customization without recompiling styles or deploying new CSS bundles. By defining brand tokens as CSS custom properties (`--brand-primary`, `--brand-logo`, etc.) and setting them at runtime based on the tenant's configuration, the entire UI can be re-themed instantly. This approach supports light and dark modes per tenant, accessibility compliance (WCAG contrast ratios), and component-level consistency.

The theming system uses design tokens—a hierarchical set of named values that represent the brand's visual properties. Tokens are organized into global (shared across all tenants), brand (tenant-specific colors, fonts), and component-level (specific UI element overrides). The token values are injected into the CSS at runtime via inline styles on the root element, CSS-in-JS theme providers, or CSS custom properties on `:root`.

For a voice agent platform, branding applies to the dashboard UI, embedded agent widgets, email templates, login page, and any customer-facing components. Each of these can inherit from the same design token system, ensuring brand consistency.

## Design Decisions

**Decision 1: CSS custom properties over CSS-in-JS.** CSS variables are natively supported in all modern browsers, work with shadow DOM, and can be animated. They require no JavaScript runtime and are more performant than CSS-in-JS solutions.

**Decision 2: Dark and light mode per tenant.** Each tenant can configure both light and dark mode color schemes. The user's preference (system, light, dark) selects which set of variables to use.

**Decision 3: Token hierarchy with fallbacks.** Use `var(--brand-primary, #6366f1)` pattern so that unset tokens gracefully fall back to platform defaults.

## Implementation Approach

```css
/* tokens.css - Design token definitions */
:root {
  /* Global tokens (platform defaults) */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  
  /* Brand tokens (tenant overrides via inline style) */
  --brand-primary: #6366f1;
  --brand-primary-hover: #5558e6;
  --brand-secondary: #8b5cf6;
  --brand-accent: #f59e0b;
  --brand-background: #ffffff;
  --brand-surface: #f8fafc;
  --brand-text: #0f172a;
  --brand-text-secondary: #475569;
  --brand-border: #e2e8f0;
  --brand-font-family: var(--font-sans);
  --brand-border-radius: var(--radius-md);
  --brand-logo-url: url('/default-logo.svg');
  --brand-favicon: url('/default-favicon.ico');
}

/* Dark mode overrides */
[data-theme="dark"] {
  --brand-background: #0f172a;
  --brand-surface: #1e293b;
  --brand-text: #f1f5f9;
  --brand-text-secondary: #94a3b8;
  --brand-border: #334155;
}
```

```typescript
// Theme service
class ThemeService {
  async getTenantTheme(tenantId: string): Promise<ThemeTokens> {
    const cacheKey = `theme:${tenantId}`;
    let theme = await this.cache.get(cacheKey);
    if (theme) return JSON.parse(theme);

    theme = await this.db.query(
      'SELECT * FROM tenant_branding WHERE tenant_id = $1',
      [tenantId]
    );

    await this.cache.setex(cacheKey, 3600, JSON.stringify(theme));
    return theme;
  }

  generateThemeVariables(theme: ThemeTokens): Record<string, string> {
    return {
      '--brand-primary': theme.primaryColor,
      '--brand-primary-hover': this.darken(theme.primaryColor, 0.1),
      '--brand-secondary': theme.secondaryColor,
      '--brand-accent': theme.accentColor,
      '--brand-background': theme.backgroundColor,
      '--brand-surface': theme.surfaceColor,
      '--brand-text': theme.textColor,
      '--brand-text-secondary': theme.textSecondaryColor,
      '--brand-font-family': theme.fontFamily || 'Inter, sans-serif',
      '--brand-border-radius': `${theme.borderRadius}px`,
      '--brand-logo-url': `url('${theme.logoUrl}')`,
      '--brand-favicon': `url('${theme.faviconUrl}')`,
    };
  }
}

// React provider
function ThemeProvider({ tenantId, children }) {
  const { data: theme } = useQuery(['tenant-theme', tenantId], 
    () => themeService.getTenantTheme(tenantId)
  );

  const variables = theme ? themeService.generateThemeVariables(theme) : {};
  
  return (
    <div style={variables as React.CSSProperties}>
      {children}
    </div>
  );
}
```

## Open-Source Tools

- **Tailwind CSS** — Utility-first CSS with design token configuration
- **Radix UI Colors** — Accessible color palette system
- **Style Dictionary** — Design token transformation tool
- **Chroma.js** — Color manipulation library for computing hover/active states
- **Theme UI** — Constraint-based design system library

## Production Considerations

- **CSS Variable Inheritance:** CSS custom properties inherit through the DOM tree. Set them on a high-level container (html or body) and they'll cascade to all children. Be careful with shadow DOM boundaries.
- **Performance:** Setting CSS variables via inline styles triggers style recalc but is generally performant (<1ms). Avoid setting hundreds of variables per tenant.
- **Color Contrast:** Validate tenant-chosen colors for WCAG AA compliance (4.5:1 for normal text, 3:1 for large text). Reject or warn on insufficient contrast.
- **Cache Strategy:** Theme configuration rarely changes. Cache aggressively (1-hour CDN, longer on client). Invalidate cache on theme update.
- **Server-Side Rendering:** For SSR, extract tenant variables during request middleware and pass to the page template. Avoid flash of unstyled content (FOUC) by setting variables in a blocking <style> tag.
