# React Error Boundary + Retry UI (TypeScript)

> Part XIV · Chapter 37 · Sections 37.5, 37.18, 37.21 · _Estimated reading time: 20 min_
> **Prerequisite:** [Render Failures and Boundaries](../02-deep-dive/04-render-failures-and-outside-boundaries.md), [Recoverable vs Unrecoverable](../01-concepts/03-recoverable-vs-unrecoverable-ui.md)

## In one sentence

**Implement a typed React Error Boundary with reset keys and a recoverable retry UI** so widget/page crashes become recoverable without losing unrelated state; also include a safe error reporting hook and a state→throw helper for async/event errors.

## Real-world use case

**ExportJob** chart widget throws on unexpected API shape. We want a **component boundary**: show "Chart unavailable — Retry" scoped to the widget, preserve filters/pagination (recoverable). If it crashes repeatedly, escalate via reporting with `errorId`.

## Key data / numbers

| Item | Value | Notes |
| --- | ----- | ----- |
| **Catch scope** | Render/lifecycle/constructor only | Must handle async separately |
| **Reset** | On `resetKeys` change | Avoid stuck fallback on navigation |
| **Reporting** | Include `componentStack`, route, errorId | In `componentDidCatch` |
| **Retry semantics** | Reset boundary state | Clear local error, remount subtree |

## Worked example — Error Boundary (TSX)

```tsx
import React from 'react';

interface Props {
  children: React.ReactNode;
  fallback?: (props: FallbackProps) => React.ReactNode;
  onError?: (error: Error, info: React.ErrorInfo) => void;
  resetKeys?: readonly unknown[];
  errorIdPrefix?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorId: string | null;
}

interface FallbackProps {
  error: Error | null;
  errorId: string | null;
  reset: () => void;
}

function genErrorId(prefix = 'err') {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2,6)}`;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null, errorId: null };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error, errorId: null };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    const errorId = genErrorId(this.props.errorIdPrefix);
    this.setState({ errorId });
    // Report with safe diagnostics (no PII, no stack traces shown to user)
    this.props.onError?.(error, { ...info, errorId } as any);
    // console.error('ErrorBoundary caught:', error, info.componentStack);
  }

  componentDidUpdate(prevProps: Props) {
    if (this.state.hasError && this.props.resetKeys && prevProps.resetKeys) {
      const changed = this.props.resetKeys.some((k, i) => k !== prevProps.resetKeys?.[i]);
      if (changed) this.reset();
    }
  }

  reset = () => {
    this.setState({ hasError: false, error: null, errorId: null });
  };

  render() {
    if (this.state.hasError) {
      const fb = this.props.fallback ?? DefaultFallback;
      return fb({ error: this.state.error, errorId: this.state.errorId, reset: this.reset });
    }
    return this.props.children;
  }
}

function DefaultFallback({ errorId, reset }: FallbackProps) {
  return (
    <div role="alert" aria-live="polite" style={{ padding: '1rem', border: '1px solid #ccc' }}>
      <h3>Something went wrong</h3>
      <p>We couldn't load this section.</p>
      {errorId && <p>Reference ID: {errorId}</p>}
      <button type="button" onClick={reset}>Try again</button>
      <button type="button" onClick={() => window.location.reload()}>Reload page</button>
    </div>
  );
}
```

## Recoverable scoped fallback (ExportJob chart)

```tsx
function ChartFallback({ reset }: FallbackProps) {
  return (
    <div role="status" aria-live="polite" style={{ padding: '1rem', background: '#f5f5f5' }}>
      <p>Chart unavailable — you can still use filters and list.</p>
      <button type="button" onClick={reset}>Retry</button>
    </div>
  );
}

export function ExportJobChartScoped() {
  return (
    <ErrorBoundary fallback={ChartFallback} resetKeys={[/* route/filters id */]} errorIdPrefix="chart">
      <ExportJobChart />
    </ErrorBoundary>
  );
}
```

## State→throw helper (route async errors to boundary)

```tsx
import React, { useState } from 'react';

export function useErrorToBoundary() {
  const [err, setErr] = useState<Error | null>(null);
  if (err) throw err;
  return (e: unknown) => {
    setErr(e instanceof Error ? e : new Error(String(e)));
  };
}

export function LoadButton() {
  const throwToBoundary = useErrorToBoundary();
  const load = async () => {
    try {
      await api.get('/something');
    } catch (e) {
      // Classify: expected -> toast; unexpected -> boundary
      const cls = classify(e); // see mapping layer
      if (cls.type === 'unexpected') throwToBoundary(e);
      else toast.error(cls.userMessage);
    }
  };
  return <button onClick={load}>Load</button>;
}
```

## Reporting hook

```tsx
export function reportError(error: Error, extra: Record<string, unknown>) {
  // Send to telemetry (Sentry/Datadog). Never include PII.
  const payload = {
    message: error.message,
    name: error.name,
    stack: undefined, // do not send raw stacks to third-party logs if sensitive; hash or truncate
    extra,
  };
  // fetch('/api/telemetry/error', { method: 'post', body: JSON.stringify(payload) })
}
```

## Real-world use case recap

**Acme SaaS ExportJob:** component boundary around chart with scoped fallback preserves filters/pagination; retries remount subtree safely. Async failures go through classification (toast vs boundary). Repeated failures are reported with `errorId`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| No boundary | Simple | Widget crash takes whole page | Never for optional widgets |
| Global boundary only | Easy | Loses scoped context/work | App-level only |
| Scoped + reset keys | Recoverable, small blast radius | Boilerplate | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use `resetKeys` (route, filters, id) | Leave permanent fallback after navigation/fix |
| Report with `errorId`, no PII | Show raw stack traces to users |
| Handle async via try/catch + state→throw | Expect boundary to catch async/event errors |
| Provide scoped fallback for optional UI | Crash checkout flow for a non-critical widget |

## Common mistakes

- **Assuming async covered.** `useEffect` async throws go unhandled without try/catch.
- **Stuck boundary.** Missing reset on prop change/route.
- **Error boundary in fallback.** Can create loops if fallback throws.
- **Double reporting.** Call once in `componentDidCatch`.

## Checklist

- [ ] Error boundary catches only render/lifecycle (known limits documented).
- [ ] Scoped fallback preserves surrounding context.
- [ ] `resetKeys` reset on route/filter changes.
- [ ] Async/event errors classified (toast vs boundary).
- [ ] Safe diagnostics + `errorId` for support.

## Related

- [Render Failures and Outside Boundaries](../02-deep-dive/04-render-failures-and-outside-boundaries.md)
- [Recoverable vs Unrecoverable UI](../01-concepts/03-recoverable-vs-unrecoverable-ui.md)
- [Boundaries: Component, Page, App](../01-concepts/02-boundaries-component-page-app.md)
