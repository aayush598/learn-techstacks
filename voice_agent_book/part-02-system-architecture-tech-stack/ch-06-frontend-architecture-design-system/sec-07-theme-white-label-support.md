# Section 07: Theme & White-Label Support

## CSS Variable Architecture

Theming uses **CSS custom properties** scoped to `:root` for default theme and `[data-theme="tenant-{id}"]` for per-tenant overrides. Dark mode is handled via `prefers-color-scheme` media query with manual override support.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THEME VARIABLE ARCHITECTURE                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  :root (Default / Light Theme)                              │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  --color-brand-primary: #1A1A2E;                       │  │   │
│  │  │  --color-background-page: #F8F9FA;                     │  │   │
│  │  │  --color-text-primary: #1A1A2E;                        │  │   │
│  │  │  --color-text-secondary: #6B7280;                      │  │   │
│  │  │  --radius-md: 6px;                                     │  │   │
│  │  │  --shadow-card: 0 1px 3px rgba(0,0,0,0.1);            │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  @media (prefers-color-scheme: dark)                        │   │
│  │  [data-theme="dark"], [data-theme="tenant-{id}-dark"]       │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  --color-brand-primary: #4A4A6E;                       │  │   │
│  │  │  --color-background-page: #0F172A;                     │  │   │
│  │  │  --color-text-primary: #F1F5F9;                        │  │   │
│  │  │  --shadow-card: 0 1px 3px rgba(0,0,0,0.4);            │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [data-theme="tenant-abc"] (White-Label Overrides)          │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  --color-brand-primary: #E11D48;                       │  │   │
│  │  │  --color-brand-secondary: #BE123C;                     │  │   │
│  │  │  --fonts-sans: "Inter", system-ui;                      │  │   │
│  │  │  --color-background-page: #FFF1F2;                     │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Theme Provider

```typescript
interface ThemeConfig {
  mode: 'light' | 'dark' | 'system';
  tenantId?: string;
  tenantOverrides?: Partial<ThemeTokens>;
}

interface ThemeTokens {
  colors: {
    brand: { primary: string; secondary: string; accent: string };
    background: { page: string; surface: string; elevated: string };
    text: { primary: string; secondary: string; muted: string };
    border: { default: string; muted: string; focus: string };
    status: { success: string; warning: string; error: string; info: string };
  };
  fonts: {
    sans: string;
    mono: string;
    heading?: string;
  };
  radii: Record<string, string>;
  shadows: Record<string, string>;
}

function ThemeProvider({ children, config }: { children: React.ReactNode; config: ThemeConfig }) {
  const resolvedMode = useResolvedMode(config.mode);
  const themeId = config.tenantId
    ? `${config.tenantId}${resolvedMode === 'dark' ? '-dark' : ''}`
    : resolvedMode;

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', themeId);
    if (config.tenantOverrides) {
      applyTenantOverrides(config.tenantOverrides);
    }
    return () => document.documentElement.removeAttribute('data-theme');
  }, [themeId, config.tenantOverrides]);

  return <>{children}</>;
}
```

## Server-Side Theme Detection

```typescript
// Middleware detects tenant from subdomain/cookie and injects theme
export function middleware(request: NextRequest) {
  const tenantId = request.headers.get('x-tenant-id')
    ?? request.cookies.get('tenant')?.value;

  if (tenantId) {
    const response = NextResponse.next();
    response.cookies.set('tenant', tenantId, {
      httpOnly: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 365, // 1 year
    });
    return response;
  }

  return NextResponse.next();
}
```

## Tenant Branding API

```typescript
// API endpoint to serve tenant theme
// GET /api/tenants/:id/theme
interface TenantThemeResponse {
  id: string;
  name: string;
  logo: string; // URL to uploaded logo
  favicon: string;
  theme: ThemeTokens;
  customCss?: string; // Tenant-injected CSS
  fonts: { family: string; url: string; weight?: number }[];
}

// Server component fetches theme data
async function TenantThemeProvider({ tenantId, children }: Props) {
  const theme = await fetchTenantTheme(tenantId);
  return (
    <ThemeProvider config={{
      mode: 'system',
      tenantId,
      tenantOverrides: theme.theme,
    }}>
      {children}
    </ThemeProvider>
  );
}
```

## Dark Mode Strategy

```typescript
function useResolvedMode(preference: 'light' | 'dark' | 'system'): 'light' | 'dark' {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    if (preference !== 'system') {
      setMode(preference);
      return;
    }

    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    setMode(mq.matches ? 'dark' : 'light');

    const handler = (e: MediaQueryListEvent) => setMode(e.matches ? 'dark' : 'light');
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [preference]);

  return mode;
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Theme delivery | CSS custom properties | Runtime switching, no rebuild, browser paint optimization |
| Server integration | Cookie + data-theme attribute | SSR-compatible, no FOUC |
| Dark mode | prefers-color-scheme + manual toggle | Respects OS preference, allows user override |
| Tenant overrides | Per-tenant CSS variables | Isolated, no global pollution |
| Custom CSS | Sanitized injection with CSP | Tenant flexibility without XSS risk |

## Integration Points

- **Ch 03 (Database)** — Tenant theme stored in `tenant_themes` table with JSON column for tokens
- **Ch 07 (API Gateway)** — Tenant subdomain resolution in middleware triggers theme fetch
- **Ch 10 (Security)** — Custom CSS sanitized via DOMPurify, CSP nonce for inline styles

## Production Considerations

- **FOUC Prevention**: Cookie-based theme detection in middleware, theme CSS inlined in `<head>` before paint
- **Font Loading**: `font-display: swap` with preload for primary fonts, fallback system fonts during load
- **Logo Delivery**: Tenant logos served via signed MinIO URLs with CDN caching, resized to 120x40
- **Theme Cache**: Tenant theme data cached in Redis (TTL: 1 hour), invalidated on theme update webhook
- **Bundle Impact**: Theme system adds ~2KB gzipped — zero additional JS for theme switching (CSS-only)
- **Accessibility**: Dark mode colors validated at 4.5:1 contrast ratio, forced-colors media query for high contrast
