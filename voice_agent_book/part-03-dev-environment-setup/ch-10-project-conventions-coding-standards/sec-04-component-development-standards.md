# Section 04: Component Development Standards

## Overview

React component development follows strict conventions for file organization, exports, prop typing, ref forwarding, and display name assignment. These standards ensure components are predictable to consume, tree-shakeable by bundlers, and debuggable in React DevTools. Every component in the `@voice-agent/ui` package conforms to the same structure.

## Component File Structure

```text
packages/ui/src/voice-call-button/
├── voice-call-button.tsx          # Component implementation
├── voice-call-button.test.tsx     # Unit tests
├── voice-call-button.stories.tsx  # Storybook stories
└── index.ts                       # Barrel export
```

Every component gets its own directory. This seems verbose for simple components, but the consistency pays off:
- Adding tests or stories never requires refactoring existing files
- Code review diffs are scoped to a single component
- Tree-shaking works at the component level (bundlers can drop entire directories)

## The One-Component-Per-File Rule

Each file exports exactly one component as a named export:

```typescript
// packages/ui/src/voice-call-button/voice-call-button.tsx
import { forwardRef } from 'react';
import type { ButtonHTMLAttributes, ForwardedRef } from 'react';

export interface VoiceCallButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  callId?: string;
}

function VoiceCallButtonComponent(
  { variant, size = 'md', isLoading = false, callId, children, ...props }: VoiceCallButtonProps,
  ref: ForwardedRef<HTMLButtonElement>
) {
  return (
    <button
      ref={ref}
      className={`voice-call-button voice-call-button--${variant} voice-call-button--${size}`}
      disabled={isLoading || props.disabled}
      data-call-id={callId}
      {...props}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}

VoiceCallButtonComponent.displayName = 'VoiceCallButton';

export const VoiceCallButton = forwardRef(VoiceCallButtonComponent);
```

Key conventions demonstrated:
1. **Named export** (`export const VoiceCallButton`), never default export
2. **Props interface** co-located and exported for reuse
3. **`forwardRef`** for all interactive elements (buttons, inputs, links)
4. **`displayName`** assigned for DevTools debugging
5. **`children`** as explicit prop (not `PropsWithChildren`)

## Default Export Prohibition

We never use `export default`. The reasoning:

```typescript
// BAD — default export
export default function VoiceCallButton() { ... }

// Import is ambiguous — the consumer chooses the name
import MyButton from './voice-call-button';  // Works, but confusing
import VoiceCallButton from './voice-call-button';  // Also works

// GOOD — named export
export function VoiceCallButton() { ... }

// Import is deterministic
import { VoiceCallButton } from './voice-call-button';
```

Named exports provide:
- **Deterministic imports**: The import name matches the export name
- **Tree-shaking**: Bundlers can identify unused exports
- **IDE support**: Auto-import works reliably
- **Re-exporting**: Barrel files re-export named exports naturally

## Prop Typing Convention

Props interfaces follow a strict naming pattern and structure:

```typescript
// Component props — always starts with the component name
export interface VoiceCallButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  callId?: string;
}

// Extend native HTML attributes for the base element
// This allows consumers to pass onClick, className, aria-*, etc.
```

**Minimum required props**: The `variant` prop is required (no default) to force consumers to explicitly choose a style. This prevents accidentally using a default variant that may not match the design intent.

**Semantic props over boolean flags**: Instead of `disabled={true} destructive={true}`, use `variant="danger"`. Boolean flags that change visual appearance are a code smell — they don't compose and create combinatorial explosion.

## ForwardRef and DisplayName

All interactive components use `forwardRef`:

```typescript
export const VoiceCallButton = forwardRef<HTMLButtonElement, VoiceCallButtonProps>(
  (props, ref) => { ... }
);
VoiceCallButton.displayName = 'VoiceCallButton';
```

`forwardRef` is necessary for:
1. **Form libraries** (React Hook Form, Formik) that need ref access for validation
2. **Tooltip/popover** libraries that measure the triggering element
3. **Focus management** in modals and dialogs

The `displayName` assignment is unfortunately required because `forwardRef` produces an anonymous component in DevTools. Without it, all forwarded components appear as `ForwardRef` in the React DevTools component tree.

## Composition Patterns

Components prefer composition over configuration:

```typescript
// GOOD — composition
<VoiceCallPanel>
  <VoiceCallHeader>
    <VoiceCallStatusIndicator status="connected" />
    <VoiceCallTimer startTime={startTime} />
  </VoiceCallHeader>
  <VoiceCallControls>
    <VoiceCallButton variant="danger" onClick={endCall}>
      End Call
    </VoiceCallButton>
    <VoiceCallButton variant="secondary" onClick={muteCall}>
      Mute
    </VoiceCallButton>
  </VoiceCallControls>
</VoiceCallPanel>

// BAD — configuration object
<ConfigurableVoicePanel
  header={{ showStatus: true, showTimer: true }}
  controls={[
    { label: "End Call", variant: "danger", action: endCall },
    { label: "Mute", variant: "secondary", action: muteCall },
  ]}
/>
```

Composition wins because:
1. **Customization doesn't require prop changes** — just rearrange children
2. **Type safety** — each child component has its own typed props
3. **Testability** — each sub-component can be tested independently
4. **Bundle size** — unused sub-components are tree-shaken

## Accessibility Standards

Every component follows WAI-ARIA patterns:

```typescript
export function VoiceCallStatusIndicator({ status }: VoiceCallStatusProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label={`Call status: ${status}`}
      className={`status-indicator status-indicator--${status}`}
    >
      <span className="status-dot" aria-hidden="true" />
      <span className="status-label">{statusLabelMap[status]}</span>
    </div>
  );
}
```

Required ARIA attributes:
- `role="status"` for live region updates
- `aria-live="polite"` for non-critical announcements
- `aria-label` for icon-only buttons
- `aria-expanded` for toggleable content
- `aria-controls` linking trigger to controlled content

## Integration Points

- **Storybook**: Every component has a `.stories.tsx` file with at least the default state, all variants, loading state, error state, and edge case (empty data, long text)
- **Testing Library**: Tests use `@testing-library/react` with `userEvent` (not `fireEvent`) for realistic interaction simulation
- **Tailwind CSS**: Class names follow the `component-name--variant` BEM-like convention for scoped styling
- **TypeScript**: Components are generic where appropriate, e.g., `VoiceList<T extends VoiceItem>`

## Production Considerations

1. **Bundle size monitoring**: Track component-level bundle impact. A 5 KB "simple button" is a red flag during code review.
2. **Server component compatibility**: UI components that use hooks (`useState`, `useEffect`) are marked with `'use client'` directive at the top. Server-compatible components omit this.
3. **Component library versioning**: The UI package follows semver independently. Breaking prop changes require a major version bump.
4. **Deprecation strategy**: Deprecated props show a console.warn in development and are removed after two minor versions. A codemod is provided for mechanical migrations.
5. **Performance profiling**: Components with expensive renders use `React.memo` after profiling confirms benefit, never preemptively.
