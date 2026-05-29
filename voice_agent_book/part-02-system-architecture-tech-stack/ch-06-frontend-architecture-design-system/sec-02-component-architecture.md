# Section 02: Component Architecture

## Atomic Design Hierarchy

The component architecture follows the **atomic design methodology** with five distinct levels: atoms, molecules, organisms, templates, and pages. Each level enforces strict composition rules — atoms do not import molecules, molecules do not import organisms.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ATOMIC DESIGN HIERARCHY                          │
│                                                                     │
│   Level 1: ATOMS                                                    │
│   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│   │Button│ │ Input│ │ Label│ │ Icon │ │Avatar│ │ Badge│          │
│   └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘          │
│           \       /        |        \       /                      │
│   Level 2: MOLECULES                                                │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│   │   FormField      │  │   SearchBar     │  │   CardHeader    │   │
│   │ ┌───┐ ┌──────┐ │  │ ┌──────┐ ┌────┐ │  │ ┌──────┐ ┌────┐ │   │
│   │ │Icon│ │Input │ │  │ │Input │ │Btn │ │  │ │Avatar│ │Text│ │   │
│   │ └───┘ └──────┘ │  │ └──────┘ └────┘ │  │ └──────┘ └────┘ │   │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│           \       /        |        \       /                      │
│   Level 3: ORGANISMS                                                │
│   ┌────────────────────────────────────────────────────────────┐   │
│   │                    DataTable                               │   │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │   │
│   │  │SearchBar │ │ Filter   │ │  Table   │ │ Paginator│      │   │
│   │  │(Molecule)│ │ (Molecule)│ │ (Molecule)│ │(Molecule)│     │   │
│   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │   │
│   └────────────────────────────────────────────────────────────┘   │
│           \       /        |        \       /                      │
│   Level 4: TEMPLATES                                                │
│   ┌────────────────────────────────────────────────────────────┐   │
│   │                    DashboardTemplate                        │   │
│   │  ┌─────────┐ ┌─────────────────────────────────────────┐   │   │
│   │  │ Sidebar │ │ ████ Main Content Area █████████████████ │   │   │
│   │  │ (Nav)   │ │ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │   │
│   │  │         │ │ │ StatCard│ │ StatCard│ │ StatCard│   │   │   │
│   │  │         │ │ └─────────┘ └─────────┘ └─────────┘   │   │   │
│   │  │         │ │ ┌──────────────────────────────────┐   │   │   │
│   │  │         │ │ │          DataTable               │   │   │   │
│   │  │         │ │ └──────────────────────────────────┘   │   │   │
│   └─────────┘ └─────────────────────────────────────────┘   │   │
│   └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Compound Component Pattern

Complex components use the **compound component pattern** with implicit state sharing via React Context. This enables flexible composition without prop drilling.

```typescript
// Select compound component
<Select value={selected} onChange={handleChange}>
  <Select.Trigger>
    <Select.Value placeholder="Select agent..." />
    <Select.Icon />
  </Select.Trigger>
  <Select.Portal>
    <Select.Content>
      <Select.Group label="Active Agents">
        <Select.Item value="agent-1">Sales Agent Alpha</Select.Item>
        <Select.Item value="agent-2">Support Bot Beta</Select.Item>
      </Select.Group>
    </Select.Content>
  </Select.Portal>
</Select>

// Implementation pattern
interface SelectContextValue {
  value: string;
  onChange: (value: string) => void;
  open: boolean;
  setOpen: (open: boolean) => void;
}

const SelectContext = createContext<SelectContextValue | null>(null);

function Select({ children, value, onChange }: SelectProps) {
  const [open, setOpen] = useState(false);
  return (
    <SelectContext.Provider value={{ value, onChange, open, setOpen }}>
      {children}
    </SelectContext.Provider>
  );
}

Select.Trigger = SelectTrigger;
Select.Content = SelectContent;
Select.Item = SelectItem;
```

## Controlled vs Uncontrolled

Every form component supports both controlled and uncontrolled usage, following React's conventions:

```typescript
interface InputProps {
  // Controlled
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  // Uncontrolled
  defaultValue?: string;
  // Refs
  ref?: React.Ref<HTMLInputElement>;
}
```

## Polymorphic Components

Components that render different HTML elements use the `as` prop pattern with TypeScript generics for type safety:

```typescript
type PolymorphicRef<C extends React.ElementType> =
  React.ComponentPropsWithRef<C>['ref'];

interface PolymorphicComponentProps<
  C extends React.ElementType = 'div'
> {
  as?: C;
  children?: React.ReactNode;
}

// Usage
<Text as="h1" size="3xl" weight="bold">Heading</Text>
<Text as="p" size="md" color="secondary">Body text</Text>
<Text as="span" size="sm">Inline text</Text>
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Composition model | Compound components + Render props | Maximum flexibility without prop explosion |
| Styling approach | Tailwind CSS + cn() utility | Zero-runtime CSS, consistent with token system |
| State management | Local state + React Context | No external dependency for UI state |
| Component testing | Testing Library + Playwright | User-centric tests, cross-browser coverage |
| Documentation | Storybook 8 with MDX | Interactive playground, accessibility audits |

## Integration Points

- **Ch 03 (Database)** — Component data types align with entity schemas (AgentSelect maps to agents table)
- **Ch 04 (Real-Time)** — Compound components wrap real-time subscriptions (StatusIndicator with WebSocket)
- **Ch 07 (API Gateway)** — Form components render API configuration UI

## Production Considerations

- **Tree Shaking**: Each component exported individually to enable dead-code elimination
- **Bundle Size**: Average component ~2KB gzipped; full library ~35KB gzipped
- **Lazy Loading**: Heavy components (Monaco editor, charts) loaded via `next/dynamic` with SSR disabled
- **Error Boundaries**: Each organism-level component wrapped in error boundary to prevent cascade failures
- **Accessibility**: All compound components pass WAI-ARIA authoring practices with axe-core CI checks
