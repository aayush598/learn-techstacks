# Frontend Architecture & Infrastructure

---

## Frontend Architecture

The frontend uses **Next.js 14 App Router** with three main sections:

### 1. Marketing Section (`app/(marketing)/`)

Public-facing pages:
- **Landing Page** (`page.tsx`): Hero, Features, HowItWorks, Pricing, Testimonials, CTA, FAQ, Profiles sections
- **Blog** (`blogs/`): Blog listing + individual blog pages with markdown data
- **Hub** (`hub/`): Guardrail and profile marketplace with search/filter
- **Pricing** (`pricing/page.tsx`): Pricing plans
- **Auth Pages**: Sign-in (`/sign-in`), Sign-up (`/sign-up`) using Clerk

**Components**: `_components/` directory with sections (Hero, Features, FAQ, Pricing, CTA, Testimonials, Profiles, HowItWorks, CheckoutButton)

### 2. Dashboard Section (`app/dashboard/`)

Protected pages (require auth):
- **Overview** (`page.tsx`): Dashboard home
- **Analytics** (`analytics/`): Charts and graphs using Recharts
- **API Keys** (`api-keys/`): Create/manage API keys with per-key analytics
- **Playground** (`playground/`): Test guardrails interactively
- **Profiles** (`profiles/`): CRUD guardrail profiles with GuardrailPicker component
- **Settings** (`settings/`): User settings

**Key Dashboard Components:**
- `CreateProfileDialog.tsx`, `EditProfileDialog.tsx`: Profile creation/editing
- `GuardrailPicker.tsx`: Guardrail selection UI
- `ProfilesClient.tsx`: Profile listing with delete capability
- `ApiKeysClient.tsx`: API key management
- `PlaygroundClient.tsx`: Interactive test environment

### 3. Documentation Section (`app/docs/`)

MDX-based documentation:
- **Content**: 20+ MDX files in `_content/` organized by topic (introduction, getting-started, guardrails, profiles, analytics, api, sdk, deployment)
- **Components**: Callout, DocSearch, DocsBreadcrumb, DocsCodeBlock, DocsHeader, DocsSidebar
- **Search**: Full-text search via MiniSearch with build-time indexing
- **Navigation**: Sidebar navigation from `_config/navigation.ts`
- **Versioning**: Version config from `_config/versions.ts`

---

## Infrastructure & Configuration

### Docker

**Multi-stage Dockerfile** (`Dockerfile`):
1. **Base**: Node 20 Alpine with libc6-compat
2. **Deps**: Install npm dependencies
3. **Builder**: Production build
4. **Runner**: Non-root `nextjs` user, only copies build artifacts

**Docker Compose** (`docker-compose.yml`):
```yaml
services:
  app:    # GuardrailZ app on port 3000
  db:     # PostgreSQL 16 on port 5432
volumes:
  pgdata:  # Persistent database storage
```

### CI/CD (`.github/workflows/ci.yml`)

GitHub Actions workflow for:
- Linting (ESLint)
- Type checking (TypeScript)
- Testing (Vitest)
- Building

### Package Manager

Uses **yarn** (classic v1.22), with `packageManager` specified in `package.json`.

### Development Setup

```bash
# 1. Clone and install
git clone ... && cd guardrailz
npm install

# 2. Set up environment
cp .env.example .env.local
# Fill in: DATABASE_URL, Clerk keys, Razorpay keys

# 3. Database
npm run db:generate   # Generate Drizzle migrations
npm run db:migrate    # Run migrations

# 4. Run
npm run dev           # Next.js dev server on port 3000
```

### Key Dependencies

| Package | Purpose |
|---------|---------|
| `next` | Framework (14.2.25) |
| `@clerk/nextjs` | Authentication |
| `drizzle-orm` / `drizzle-kit` | Database ORM & migrations |
| `postgres` | PostgreSQL driver |
| `zod` | Schema validation |
| `ajv` | JSON Schema validation |
| `razorpay` | Payment processing |
| `framer-motion` | Animations |
| `recharts` | Charts |
| `lucide-react` | Icons |
| `shadcn/ui` (Radix) | UI component primitives |
| `minisearch` | Documentation search |
| `rehype-pretty-code` / `shiki` | Code syntax highlighting |
| `tailwindcss` | CSS framework |
| `vitest` | Testing framework |

### Test Suite (`tests/`)

- **Unit tests** (`tests/unit/`): Executor, register, normalize
- **Guardrail tests** (`tests/guardrails/`): Individual tests for each guardrail (45+ test files)
- **Integration tests** (`tests/integration/`): End-to-end guardrail workflow
- **Fixtures** (`tests/fixtures/`): IAM context, tool context test data

Test config: `vitest.config.ts`

### Code Quality

- **ESLint**: `.eslintrc.cjs` with `eslint-config-next`
- **Prettier**: `.prettierignore`, `prettier.config.cjs` with Tailwind plugin
- **Husky**: pre-commit hooks for linting
- **Commitlint**: Conventional commit enforcement
- **Lint-staged**: Run linters on staged files
