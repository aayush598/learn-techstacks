# Section 05: Form & Builder Components

## Form Architecture

Forms use **React Hook Form** for performant form state management with **Zod** schemas for type-safe validation. The agent builder uses a drag-and-drop interface powered by **React DnD** and a **Monaco Editor** for advanced prompt/code editing.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FORM ARCHITECTURE                                │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    React Hook Form Core                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │
│  │  │ useForm  │ │useField  │ │FormProvider│ │ Controller   │   │   │
│  │  │          │ │Array     │ │           │ │ (controlled) │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬──────┘ └──────┬───────┘   │   │
│  │       │             │            │               │            │   │
│  │       ▼             ▼            ▼               ▼            │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │                  Zod Schema Layer                        │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │  │   │
│  │  │  │ Agent    │ │ Campaign │ │ Call     │ │ User       │  │  │   │
│  │  │  │ Schema   │ │ Schema   │ │ Settings │ │ Profile    │  │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │                              │                                 │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │              UI Component Layer                          │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │  │   │
│  │  │  │ FormField│ │ SubmitBtn│ │FieldArray│ │ ErrorText  │  │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Schema-Driven Form Generation

```typescript
import { z } from 'zod';

// Agent configuration schema
export const AgentConfigSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  description: z.string().max(500).optional(),
  voice: z.enum(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']),
  language: z.string().regex(/^[a-z]{2}-[A-Z]{2}$/),
  temperature: z.number().min(0).max(2).default(0.7),
  maxDuration: z.number().int().min(30).max(3600).default(600),
  tools: z.array(z.object({
    id: z.string().uuid(),
    name: z.string(),
    enabled: z.boolean(),
    config: z.record(z.unknown()).optional(),
  })).min(1),
  promptTemplate: z.string().min(10).max(10000),
  fallbackBehavior: z.discriminatedUnion('type', [
    z.object({ type: z.literal('transfer'), phoneNumber: z.string() }),
    z.object({ type: z.literal('voicemail'), message: z.string() }),
    z.object({ type: z.literal('escalate'), queue: z.string() }),
  ]),
});

export type AgentConfig = z.infer<typeof AgentConfigSchema>;
```

### Form Component Integration

```typescript
function AgentForm({ agent, onSubmit }: AgentFormProps) {
  const form = useForm<AgentConfig>({
    resolver: zodResolver(AgentConfigSchema),
    defaultValues: agent ?? {
      temperature: 0.7,
      maxDuration: 600,
      tools: [],
    },
    mode: 'onBlur',
  });

  return (
    <FormProvider {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          name="name"
          label="Agent Name"
          description="A unique name for this voice agent"
        >
          <Input placeholder="e.g., Sales Agent Alpha" />
        </FormField>

        <FormField name="voice" label="Voice Selection">
          <Select>
            {VOICES.map((v) => (
              <Select.Item key={v} value={v}>{v}</Select.Item>
            ))}
          </Select>
        </FormField>

        <FormField name="promptTemplate" label="System Prompt">
          <MonacoEditor
            language="markdown"
            height={300}
            options={{ minimap: { enabled: false } }}
          />
        </FormField>

        <ToolArrayField name="tools" />
      </form>
    </FormProvider>
  );
}
```

## Drag-and-Drop Builder

The agent workflow builder uses React DnD with a canvas-based layout:

```typescript
interface WorkflowNode {
  id: string;
  type: 'greeting' | 'question' | 'condition' | 'action' | 'transfer' | 'end';
  position: { x: number; y: number };
  config: Record<string, unknown>;
  connections: { from: string; to: string; label?: string }[];
}

// Drag-and-drop context
const NodeTypes = {
  greeting: { icon: Hand, color: 'blue', label: 'Greeting' },
  question: { icon: HelpCircle, color: 'purple', label: 'Question' },
  condition: { icon: GitBranch, color: 'yellow', label: 'Condition' },
  action: { icon: Zap, color: 'green', label: 'Action' },
  transfer: { icon: PhoneForwarded, color: 'orange', label: 'Transfer' },
  end: { icon: Square, color: 'red', label: 'End Call' },
};
```

## Dynamic Form Sections

Forms support conditional sections that appear/hide based on field values:

```typescript
function ConditionalSection({ watch, children, field, value }) {
  const watchedValue = watch(field);
  if (watchedValue !== value) return null;
  return <AnimatePresence><motion.div>{children}</motion.div></AnimatePresence>;
}

// Usage
<ConditionalSection watch={form.watch} field="fallbackBehavior.type" value="transfer">
  <FormField name="fallbackBehavior.phoneNumber" label="Transfer Number">
    <PhoneInput />
  </FormField>
</ConditionalSection>
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Form library | React Hook Form | Uncontrolled inputs, minimal re-renders, native form validation |
| Validation | Zod | TypeScript-first, composable schemas, discriminated unions |
| Drag-and-drop | React DnD | Flexible, touch support, custom drag previews |
| Code editor | Monaco Editor | VS Code quality, syntax highlighting, keybindings |
| Form field component | Compound pattern | Consistent styling, accessible error states |

## Integration Points

- **Ch 03 (Database)** — Zod schemas mirror PostgreSQL JSON validation at application layer
- **Ch 05 (Microservices)** — Agent configs submitted via form are published to Kafka for service consumption
- **Ch 07 (API Gateway)** — Form validation schemas reused as API request validation middleware
- **Ch 08 (Tech Stack)** — React Hook Form, Zod, React DnD, Monaco Editor setup details

## Production Considerations

- **Performance**: React Hook Form isolates re-renders to individual fields — 500-field forms rerender in < 5ms
- **Autosave**: Debounced autosave (2s after last change) with conflict detection via version field
- **Monaco Editor**: Lazy-loaded via `next/dynamic` with `ssr: false`, adds ~2MB uncompressed (450KB gzipped)
- **Mobile**: Monaco editor replaced with plain textarea on screens < 768px
- **Accessibility**: All form fields have associated labels, error messages linked via `aria-describedby`, drag-and-drop has keyboard alternative with arrow keys + Enter
