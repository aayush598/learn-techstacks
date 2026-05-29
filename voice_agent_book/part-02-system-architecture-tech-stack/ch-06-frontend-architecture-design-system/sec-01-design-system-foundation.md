# Section 01: Design System Foundation

## Design Token Architecture

The design system foundation is built on a three-tier token hierarchy: **global tokens** (raw values), **alias tokens** (semantic mappings), and **component tokens** (scoped overrides). This structure enables consistent theming across all 79+ UI components while allowing per-tenant white-label customization.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DESIGN TOKEN HIERARCHY                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   GLOBAL TOKENS (Raw Values)                 │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │
│  │  │  Color   │ │  Type   │ │ Spacing  │ │  Shadows/    │   │   │
│  │  │  #1A1A2E │ │ Inter 16│ │  4,8,12  │ │  Borders    │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │ Map                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   ALIAS TOKENS (Semantic)                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │
│  │  │  primary │ │  body-md │ │  space-  │ │  elevation-  │   │   │
│  │  │  #1A1A2E │ │  16px    │ │  section │ │     card     │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │ Apply                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 COMPONENT TOKENS (Scoped)                    │   │
│  │  ┌──────────────────┐  ┌─────────────────────────────────┐  │   │
│  │  │  Button: {       │  │  Card: {                        │  │   │
│  │  │    bg: primary,  │  │    padding: space-section,      │  │   │
│  │  │    text: white,  │  │    shadow: elevation-card,      │  │   │
│  │  │    radius: md    │  │    radius: lg                   │  │   │
│  │  │  }               │  │  }                              │  │   │
│  │  └──────────────────┘  └─────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Global Token Categories

```typescript
interface GlobalTokens {
  colors: {
    grey: { 50: string; 100: string; 200: string; 300: string; 400: string; 500: string; 600: string; 700: string; 800: string; 900: string; 950: string };
    blue: { 50: string; 100: string; 200: string; 300: string; 400: string; 500: string; 600: string; 700: string; 800: string; 900: string };
    green: { 50: string; 100: string; 200: string; 300: string; 400: string; 500: string; 600: string; 700: string; 800: string; 900: string };
    red: { 50: string; 100: string; 200: string; 300: string; 400: string; 500: string; 600: string; 700: string; 800: string; 900: string };
    yellow: { 50: string; 100: string; 200: string; 300: string; 400: string; 500: string; 600: string; 700: string; 800: string; 900: string };
  };
  typography: {
    fontFamily: { sans: string; mono: string };
    fontSize: { xs: string; sm: string; md: string; lg: string; xl: string; '2xl': string; '3xl': string; '4xl': string };
    fontWeight: { normal: number; medium: number; semibold: number; bold: number };
    lineHeight: { tight: string; normal: string; relaxed: string };
  };
  spacing: Record<string, string>; // 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24
  shadows: Record<string, string>; // sm, md, lg, xl, '2xl'
  borderRadius: Record<string, string>; // none, sm, md, lg, xl, full
}
```

### Alias Token Mapping

```typescript
interface AliasTokens {
  colors: {
    brand: { primary: string; secondary: string; accent: string };
    text: { primary: string; secondary: string; muted: string; inverse: string };
    background: { page: string; surface: string; elevated: string; overlay: string };
    border: { default: string; muted: string; focus: string };
    status: { success: string; warning: string; error: string; info: string };
  };
  typography: {
    heading: { '1': FontSpec; '2': FontSpec; '3': FontSpec; '4': FontSpec };
    body: { xs: FontSpec; sm: FontSpec; md: FontSpec; lg: FontSpec };
  };
}
```

## Accessibility Foundation (WCAG 2.1 AA)

Every token combination is validated against WCAG 2.1 AA contrast ratios. The design system enforces a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ACCESSIBILITY VALIDATION                        │
│                                                                     │
│  Token Pair              Contrast Ratio     Pass (AA)               │
│  ───────────────────────────────────────────────────────────       │
│  text.primary (#1A1A2E)      13.8:1           ✅                    │
│    on bg.page (#F8F9FA)                                            │
│  text.secondary (#6B7280)    4.7:1            ✅                    │
│    on bg.page (#F8F9FA)                                            │
│  text.muted (#9CA3AF)        3.2:1            ❌ (large only)       │
│    on bg.page (#F8F9FA)                                            │
│  text.inverse (#FFFFFF)      15.2:1           ✅                    │
│    on brand.primary (#1A1A2E)                                       │
│  border.focus (#3B82F6)      3.1:1            ✅ (3:1 minimum)     │
│    on bg.surface (#FFFFFF)                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Focus Management
- All interactive elements have visible focus indicators (3px offset ring)
- Skip-to-content link visible on first tab
- Focus order follows DOM order (no positive tabindex values)
- ARIA landmarks applied to all layout regions

## Component Primitives

```typescript
// Polymorphic component pattern
interface PolymorphicProps<C extends React.ElementType> {
  as?: C;
  children?: React.ReactNode;
  className?: string;
}

// Button primitive with full ARIA support
interface ButtonProps extends PolymorphicProps<'button'> {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger' | 'link';
  size: 'xs' | 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  type?: 'button' | 'submit' | 'reset';
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Token delivery | CSS custom properties | Runtime theming, no rebuild needed, browser-native |
| Tailwind integration | Tailwind CSS v3 with CSS variable plugin | Utility-first, small bundle, consistent with token system |
| Component library | Radix UI (headless) + shadcn/ui | Accessible, unstyled, full control over visuals |
| Icon system | Lucide React (tree-shakeable) | Small bundle (each icon ~1KB), consistent style |
| Animation library | Framer Motion | Declarative, layout animations, gesture support |

## Integration Points

- **Ch 03 (Database)** — Token values stored in tenant config for white-label API
- **Ch 04 (Real-Time)** — Design system components consumed in live dashboard views
- **Ch 08 (Tech Stack)** — Tailwind CSS, Radix UI, Framer Motion detailed setup

## Production Considerations

- **Bundle Impact**: Design tokens add ~4KB gzipped; Radix UI primitives ~15KB gzipped
- **CSS Delivery**: Critical CSS inlined via Next.js, token CSS loaded as `@layer base` for cascade control
- **Runtime Theming**: CSS custom properties updated via `document.documentElement.style.setProperty()` — no Flash of Unstyled Content (FOUC) when using SSR with cookie-based theme detection
- **Token Validation**: CI pipeline validates contrast ratios using `@contrast-ratio/core` and fails builds below 4.5:1
