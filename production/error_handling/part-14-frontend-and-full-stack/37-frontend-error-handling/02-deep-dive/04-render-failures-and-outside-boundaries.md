# Render Failures, Error Boundaries Mechanics and Limits, Errors Outside Boundaries

> Part XIV · Chapter 37 · Sections 37.21–37.22 · _Estimated reading time: 19 min_
> **Prerequisite:** [Component, Page, App Boundaries](../01-concepts/02-boundaries-component-page-app.md), [React Error Boundary + Retry UI (Practical)](../03-practical-examples/01-react-error-boundary-retry-tsx.md)

## In one sentence

**React error boundaries catch render/lifecycle/constructor errors below them — nothing else.** Async errors, event handlers, `setTimeout`/promises, SSR, and code outside the React tree must be handled explicitly; combine boundaries with global handlers and safe fallbacks.

## Why this matters in production

A thrown error in a `useEffect` async callback or click handler will **not** reach a parent error boundary. If you rely only on boundaries, those failures become unhandled rejections or silent corruption. For **Acme SaaS** widgets and third-party components, understanding limits prevents false confidence.

## Error boundary mechanics (37.21)

**How they work (React):**
- Implement `getDerivedStateFromError(error)` to render fallback.
- Implement `componentDidCatch(error, info)` to log/report with component stack.
- Boundaries are class components in current React patterns; some frameworks provide equivalents.
- They catch errors during rendering, in lifecycle methods, and in constructors of the whole tree below them.

**Behavior:**
- Only errors thrown **during render** propagate to nearest boundary above.
- Errors in **event handlers** do not propagate to boundaries (React doesn't catch them by design).
- Errors in **async code** (`setTimeout`, `Promise.then`, `async/await` callbacks) do not propagate.
- Errors during **server rendering** behave differently; need framework-specific handling.
- Errors in **error boundary itself** are not caught by that boundary.

## Errors outside boundaries (37.22)

| Source | Caught by boundary? | How to handle |
| ------ | ------------------- | ------------- |
| **Render throw** | Yes | Boundary + fallback + reset keys |
| **Lifecycle method throw** | Yes | Same as render |
| **Constructor throw** | Yes | Same as render |
| **Event handler (`onClick`) throw** | **No** | `try/catch` inside handler, or global handler, or re-throw to boundary via state (`throw error` from render triggered by state) |
| **`useEffect` async throw** | **No** (if unhandled in async fn) | `try/catch` inside async function; store in state; render fallback or report |
| **`setTimeout`/`setInterval`** | **No** | `try/catch` |
| **Promise rejection** | **No** | `catch`, `.catch()`, or `window.onunhandledrejection` |
| **SSR rendering** | **Framework dependent** | Use framework error boundaries/pages |
| **Third-party scripts** | **No** | Global `window.onerror`/`onunhandledrejection` with isolation |
| **Workers/websockets** | **No** | Handle in worker + postMessage; don't rely on React boundary |

## Pattern: catch async/errors into render

To route an async/event error to a boundary, store it in state and throw during render:

```tsx
function SafeAsync() {
  const [err, setErr] = useState<Error|null>(null);
  if (err) throw err; // triggers boundary
  async function load() {
    try { await api.get(); }
    catch(e:any) { setErr(e instanceof Error ? e : new Error(String(e))); }
  }
  return <button onClick={load}>Load</button>;
}
```

Or use a small error boundary that resets; be careful not to create infinite loops.

## Global handlers

```ts
window.addEventListener('unhandledrejection', (event) => {
  event.preventDefault();
  reportToTelemetry(event.reason, { type: 'unhandledrejection' });
  // Optionally show toast if user can recover
});

window.addEventListener('error', (event) => {
  reportToTelemetry(event.error || event.message, { type: 'window.error' });
});
```

**Note:** These catch outside React tree; still need to surface safe UX.

## Key data / numbers

| Item | Guidance | Notes |
| --- | -------- | ----- |
| **Boundary coverage** | Component/page/app as needed | Not a global try/catch for everything |
| **Reset strategy** | `resetKeys` on route/id change | Prevent stuck fallback |
| **Error reporting** | Include component stack + route + errorId | In `componentDidCatch` |
| **Async coverage** | 100% of async in try/catch or mapped | Must be explicit |

## Real-world use case — AgentRun

**Context:** **AgentRun** triggers tool calls from button clicks. A tool invocation throws synchronously in handler.

**Failure:** Error boundary above doesn't catch it; UI freezes or logs unhandled error with no feedback.

**Fix:** Wrap handler in `try/catch`, classify expected vs unexpected, show toast for recoverable or route to boundary via state throw. For async tool calls, catch and surface recoverable "Tool failed — retry".

**Result:** No unhandled errors, correct UX.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Only boundaries | Declarative for render | Misses most async/event errors | Insufficient alone |
| Only try/catch | Covers handlers | Repetitive, easy to miss | Necessary everywhere |
| Boundaries + try/catch + global handlers | Complete coverage | More code | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Know boundary limits exactly | Assume boundary catches async |
| Use `try/catch` in event handlers and async functions | Let promises reject unhandled |
| Route async errors to boundary via state throw when subtree must crash | Throw from non-render code expecting boundary to catch |
| Log in `componentDidCatch` + global handlers | Rely on boundaries for all failures |

## Common mistakes

- **"Error boundary catches everything" myth.** Most frontend errors are async/event-based.
- **Throwing from `setTimeout`.** Not caught.
- **Forgetting cleanup.** Global handlers can leak if not careful.
- **Double-reporting.** Report once with full context.

## Checklist

- [ ] Boundaries placed per scope (37.2–37.4).
- [ ] All async functions have try/catch.
- [ ] Event handlers handle errors explicitly.
- [ ] Global unhandledrejection/error handlers log safely.
- [ ] Async/event errors that must crash subtree use state→throw pattern.

## Related

- [React Error Boundary + Retry UI (Practical)](../03-practical-examples/01-react-error-boundary-retry-tsx.md)
- [Boundaries: Component, Page, App](../01-concepts/02-boundaries-component-page-app.md)
- [Recoverable vs Unrecoverable UI](../01-concepts/03-recoverable-vs-unrecoverable-ui.md)
