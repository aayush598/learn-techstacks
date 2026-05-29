# Section 06: UI Component Package

## Overview

The UI component package (`@voice-agent/ui`) provides a shared library of React components, design system tokens, and utility functions used by the web dashboard and potentially by embedded widgets. This package is the source of truth for the platform's visual identity and interaction patterns.

## Package Architecture

```text
packages/ui/src/
├── components/
│   ├── ui/                    # Primitive components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── badge.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── table.tsx
│   │   ├── tabs.tsx
│   │   ├── toast.tsx
│   │   └── tooltip.tsx
│   ├── layout/                # Layout components
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   ├── page-container.tsx
│   │   └── data-table.tsx
│   ├── forms/                 # Form components
│   │   ├── form-field.tsx
│   │   ├── phone-input.tsx
│   │   └── voice-selector.tsx
│   ├── charts/                # Chart components
│   │   ├── call-volume.tsx
│   │   ├── success-rate.tsx
│   │   └── duration-distribution.tsx
│   └── shared/
│       ├── loading.tsx
│       ├── empty-state.tsx
│       ├── error-boundary.tsx
│       └── confirmation-dialog.tsx
├── tokens/
│   ├── colors.ts
│   ├── spacing.ts
│   ├── typography.ts
│   ├── shadows.ts
│   ├── breakpoints.ts
│   └── animations.ts
├── hooks/
│   ├── use-media-query.ts
│   ├── use-breakpoint.ts
│   ├── use-debounce.ts
│   └── use-intersection.ts
├── utils/
│   ├── cn.ts                  # clsx + tailwind-merge utility
│   ├── format.ts              # Formatting utilities
│   └── constants.ts
├── index.ts                   # Public API barrel
└── styles.css                 # Global styles
```

## Package Configuration

```jsonc
{
  "name": "@voice-agent/ui",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./tokens": {
      "import": "./dist/tokens/index.js",
      "types": "./dist/tokens/index.d.ts"
    },
    "./styles": "./dist/styles.css"
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsc && tsc-alias && postcss src/styles.css -o dist/styles.css",
    "dev": "tsc --watch",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "dependencies": {
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.3.0",
    "lucide-react": "^0.400.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-tooltip": "^1.0.7",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-toast": "^1.1.5"
  },
  "peerDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "@voice-agent/config-typescript": "workspace:*",
    "@voice-agent/config-eslint": "workspace:*",
    "@voice-agent/config-tailwind": "workspace:*",
    "@storybook/react": "^8.0.0",
    "@storybook/addon-essentials": "^8.0.0",
    "typescript": "^5.4.0"
  }
}
```

## Design Tokens

```typescript
// packages/ui/src/tokens/colors.ts
export const colors = {
  brand: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49",
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a",
  },
  success: {
    50: "#f0fdf4",
    500: "#22c55e",
    900: "#14532d",
  },
  warning: {
    50: "#fffbeb",
    500: "#f59e0b",
    900: "#78350f",
  },
  error: {
    50: "#fef2f2",
    500: "#ef4444",
    900: "#7f1d1d",
  },
} as const;
```

## Component Implementation

### Button Component

```typescript
// packages/ui/src/components/ui/button.tsx
import { forwardRef } from "react";
import { cn } from "../../utils/cn";
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-brand-600 text-white hover:bg-brand-700",
        secondary: "bg-neutral-100 text-neutral-900 hover:bg-neutral-200",
        outline: "border border-neutral-300 bg-white hover:bg-neutral-50",
        ghost: "text-neutral-600 hover:bg-neutral-100",
        danger: "bg-error-500 text-white hover:bg-error-600",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, disabled, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
```

### cn Utility

```typescript
// packages/ui/src/utils/cn.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Tailwind Configuration Preset

```typescript
// packages/config/tailwind/preset.ts
import type { Config } from "tailwindcss";
import { colors } from "@voice-agent/ui/tokens";

export const tailwindPreset: Partial<Config> = {
  theme: {
    extend: {
      colors,
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      spacing: {
        18: "4.5rem",
        88: "22rem",
        120: "30rem",
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1rem",
      },
      animation: {
        "fade-in": "fadeIn 0.2s ease-out",
        "slide-in": "slideIn 0.3s ease-out",
      },
    },
  },
};
```

## Storybook Integration

Storybook is configured for visual development and documentation of components:

```typescript
// packages/ui/.storybook/main.ts
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
};

export default config;
```

## Tree-Shaking Configuration

Proper tree-shaking is essential for a UI package consumed by applications:

```jsonc
{
  "sideEffects": ["**/*.css"],
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

## Design Decisions

### Radix UI Primitives vs. Custom Components

**Decision**: Use Radix UI for primitive components (dialog, dropdown, tooltip, etc.) and wrap them in our own API.

**Rationale**: Radix provides accessible, headless components that handle keyboard navigation, focus management, and ARIA attributes. Wrapping them allows us to:
- Apply consistent styling via design tokens
- Add application-specific behavior (loading states, error handling)
- Replace the underlying library without changing consumer code

### class-variance-authority for Variants

CVA provides a type-safe way to define component variants. Compared to conditional classes or template literals:
- **Type safety**: Variants are validated at compile time
- **Composability**: Variants compose naturally with custom class overrides
- **Readability**: Variant definitions are declarative and self-documenting

## Integration Points

- **apps/web**: Primary consumer of the UI package
- **Storybook**: Component development environment at port 6006
- **Tailwind config preset**: Shared across all apps for consistent styling

## Production Considerations

1. **Bundle size**: Monitor with `size-limit` or `bundlephobia`. Keep the package under 50KB gzipped. Tree-shaking must work — verify with `esbuild --bundle --format=esm`
2. **CSS extraction**: Extract styles to a separate CSS file rather than using runtime CSS-in-JS. This enables better caching and smaller bundles
3. **Server Components**: Ensure components are properly marked with `"use client"` when they use React hooks or browser APIs
4. **Versioning**: Bump the UI package version independently. Use `"@voice-agent/ui": "^0.1.0"` in consuming apps to allow patch updates
5. **Accessibility auditing**: Run axe-core or Lighthouse CI on Storybook to catch accessibility regressions automatically
