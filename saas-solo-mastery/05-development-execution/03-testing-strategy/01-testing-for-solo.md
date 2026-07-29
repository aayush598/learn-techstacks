# Testing Strategy for Solo Founders

## The Testing Dilemma

Every solo founder faces the same question: "How much should I test?" Test too little, and bugs slip through. Test too much, and you never ship anything.

The answer isn't "test everything" (impossible) or "test nothing" (irresponsible). It's a strategic approach: test what matters most, automate what you can, and accept managed risk for the rest.

---

## 1. The Solo Testing Philosophy

### The Testing Pyramid (Reduced)

The traditional testing pyramid has three layers. For solo founders, the emphasis shifts:

```
Traditional:          Solo SaaS:
    /\\                  /\\
   /  \\                /  \\
  / E2E \\              / Unit \\
 /________\\           /________\\
   /\\  /\\                /\\
  /  \\/  \\              /  \\
 / Inte-  \\            / E2E  \\
/gration   \\          / (crit-  \\
/___________\\        / ical only)\\
   /\\                      /\\
  /  \\                    /  \\
 / Unit \\                / Inte- \\
/________\\              / gration \\
                        /__________\\
```

**Solo priority**:
1. **Unit tests**: Test business logic (highest ROI per minute)
2. **Integration tests**: Test critical data flows
3. **E2E tests**: Test only the most critical user paths

### The 80/20 of Testing

80% of bugs come from 20% of your code. Focus testing on:
- Core business logic (algorithms, calculations, data processing)
- Authentication and authorization
- Payment processing
- Data integrity (create, update, delete operations)
- User-facing forms (validation, submission)

The other 80% of code (UI rendering, static pages, simple CRUD) gets basic manual testing.

### The Risk-Based Testing Matrix

| Code Area | Risk | Testing Approach |
|-----------|------|------------------|
| Payment logic | Critical | Unit + Integration + Manual |
| Auth/Access control | Critical | Unit + Integration |
| Data mutations | High | Unit + Integration |
| Core business logic | High | Unit tests |
| API endpoints | Medium | Integration (key ones) |
| UI components | Medium | Manual (Visual check) |
| Static pages | Low | Manual (once) |
| Admin panels | Low | Manual |

---

## 2. What to Test vs. What to Skip

### Always Test

**Business logic**:
- Calculations (pricing, discounts, taxes, time tracking)
- Data transformations (import, export, format conversion)
- Business rules (permissions, workflows, validation)

**Data integrity**:
- CRUD operations (create, read, update, delete)
- Data validation (required fields, formats, limits)
- Relationships (foreign keys, cascading deletes)
- Race conditions (concurrent edits, double submissions)

**Authentication and authorization**:
- Signup, login, logout
- Session management
- Role-based access control
- API key validation

**Payment and billing**:
- Subscription creation and cancellation
- Plan upgrades and downgrades
- Refund calculations
- Invoice generation

### Sometimes Test (Based on Complexity)

- API endpoint handlers
- Form validation logic
- Email templates
- Search functionality
- File uploads
- Background jobs

### Don't Test (Test Manually)

- UI layout and styling
- Static content
- Simple CRUD with no custom logic
- Third-party integrations (trust the provider)
- One-time migration scripts
- Admin panels (low usage, low impact)

---

## 3. Unit Testing Strategy

### What to Unit Test

Test functions and modules that contain business logic:

```typescript
// Test: Pricing calculation
function calculateSubscriptionPrice(plan: Plan, billingPeriod: BillingPeriod): number {
  const basePrice = plan.basePrice
  const discount = billingPeriod === 'annual' ? 0.2 : 0
  return basePrice * (1 - discount)
}

test('annual billing applies 20% discount', () => {
  expect(calculateSubscriptionPrice({ basePrice: 100 }, 'annual')).toBe(80)
})
```

### What NOT to Unit Test in a Solo SaaS

- Framework features (Next.js routing, Prisma queries)
- Third-party library code
- Simple getter/setter functions
- UI components that just render data (test visually)
- Configuration files

### The 10x Unit Test Rule

A unit test should be 10x faster than running the app and testing manually. If it's not, skip the unit test and test at a higher level.

### Testing Framework Setup

```bash
# Vitest (fast, native TypeScript)
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./test/setup.ts'],
  },
})
```

```bash
# Run tests
npx vitest           # Watch mode
npx vitest run       # CI mode
```

---

## 4. Integration Testing Strategy

### What to Integration Test

Test interactions between components:

```typescript
// Test: Creating a project with tasks
test('can create project with initial tasks', async () => {
  const project = await createProject({
    name: 'Test Project',
    tasks: [{ title: 'Task 1' }, { title: 'Task 2' }],
  })
  
  expect(project.name).toBe('Test Project')
  expect(project.tasks).toHaveLength(2)
})
```

### The 5 Integration Tests Per Feature Rule

For each feature, write 5 integration tests max:

1. **Happy path**: Everything works
2. **Error path**: Something goes wrong
3. **Edge case**: Boundary condition
4. **Empty state**: No data
5. **Authorization**: Unauthorized access fails

### Database Testing

```typescript
// Integration test with database
import { prisma } from '@/lib/prisma'

describe('Project API', () => {
  beforeEach(async () => {
    await prisma.project.deleteMany()
  })

  test('creates a project', async () => {
    const res = await fetch('/api/projects', {
      method: 'POST',
      body: JSON.stringify({ name: 'New Project' }),
    })
    expect(res.status).toBe(201)
    
    const data = await res.json()
    expect(data.name).toBe('New Project')
  })
})
```

---

## 5. Test Automation Priority

### What to Automate First

Priority order for test automation:

1. **Payment and billing tests** — Automate (high risk, high cost of failure)
2. **Authentication tests** — Automate (security critical)
3. **Core business logic tests** — Automate (repetitive to test manually)
4. **Data migration tests** — Automate (one-time, but critical)
5. **Critical user path E2E tests** — Automate when you have traffic

### What to NOT Automate Yet

- Visual regression tests (expensive to set up)
- Performance tests (fix when slow)
- Accessibility regression tests (check with tools occasionally)
- Cross-browser tests (check the top 2 browsers)

### The Test Automation Budget

As a solo founder, spend:
- **Pre-PMF**: 5% of time on tests (just core logic)
- **Growth**: 10% of time on tests (add integration tests)
- **Scale**: 15-20% of time on tests (add E2E for critical paths)

---

## 6. Manual Testing Checklist

### Pre-Deploy Manual Test

Before each deploy, run through this quickly:

**Core functionality** (2 minutes):
- [ ] Can I sign up / log in?
- [ ] Can I perform the core action?
- [ ] Can I see my data?

**What changed** (5 minutes):
- [ ] The specific feature/change works correctly
- [ ] No obvious visual bugs
- [ ] Error states are handled (try to break it)

**Quick sanity** (3 minutes):
- [ ] No console errors
- [ ] No 500 errors
- [ ] Works on mobile viewport
- [ ] Works in Chrome and Safari

### The "Try to Break It" Session

Before shipping, spend 5 minutes trying to break the feature:
- Submit empty forms
- Enter invalid data
- Click buttons rapidly
- Navigate away mid-flow
- Use the back button

---

## 7. Testing for Common SaaS Patterns

### Testing Forms

```typescript
test('shows validation error for invalid email', async () => {
  render(<SignupForm />)
  
  await userEvent.type(screen.getByLabelText('Email'), 'invalid')
  await userEvent.click(screen.getByRole('button', { name: 'Sign Up' }))
  
  expect(screen.getByText('Please enter a valid email')).toBeInTheDocument()
})
```

### Testing Authentication

```typescript
test('redirects unauthenticated user to login', async () => {
  render(<DashboardPage />)
  
  expect(screen.getByText('Please sign in')).toBeInTheDocument()
  expect(window.location.pathname).toBe('/sign-in')
})
```

### Testing Data Display

```typescript
test('shows empty state when no projects', async () => {
  render(<ProjectList projects={[]} />)
  
  expect(screen.getByText('No projects yet')).toBeInTheDocument()
  expect(screen.getByText('Create your first project')).toBeInTheDocument()
})
```

### Testing Error Handling

```typescript
test('shows error message when API fails', async () => {
  server.use(
    rest.get('/api/projects', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )
  
  render(<ProjectList />)
  
  expect(await screen.findByText('Failed to load projects')).toBeInTheDocument()
})
```

---

## 8. Testing Third-Party Integrations

### Mocking External Services

```typescript
// Mock Stripe
vi.mock('@stripe/stripe-js', () => ({
  loadStripe: vi.fn(() => ({
    redirectToCheckout: vi.fn(),
  })),
}))

// Mock email service
vi.mock('@/lib/email', () => ({
  sendEmail: vi.fn(),
}))
```

### The Integration Trust Boundary

Don't test third-party services directly. Test how YOUR code handles their responses:

```typescript
test('handles successful payment', async () => {
  stripe.checkout.sessions.create.mockResolvedValue({
    id: 'cs_test_123',
    url: 'https://checkout.stripe.com/...',
  })
  
  const result = await createCheckoutSession({ priceId: 'price_123' })
  expect(result.url).toContain('checkout.stripe.com')
})

test('handles payment failure', async () => {
  stripe.checkout.sessions.create.mockRejectedValue(
    new Error('Card declined')
  )
  
  await expect(createCheckoutSession({ priceId: 'price_123' }))
    .rejects.toThrow('Payment failed')
})
```

---

## 9. The Solo Testing Workflow

### Daily Testing

1. **Write code**
2. **Write tests for business logic** (5-10 min)
3. **Run tests** (`npm run test`)
4. **Manual smoke test** (3 min)
5. **Ship**

### Weekly Testing

1. **Run full test suite** (should take < 1 minute)
2. **Check test coverage** for new code
3. **Review error tracking** for production issues
4. **Add tests for any bugs found** (regression prevention)

### Monthly Testing

1. **Review test quality** (are tests actually testing the right things?)
2. **Remove flaky tests** (tests that sometimes fail)
3. **Add integration tests** for new critical flows
4. **Update manual test checklist**

---

## 10. Test Infrastructure Setup

### Minimal Test Configuration

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ci": "vitest run --coverage",
    "test:e2e": "playwright test"
  }
}
```

### GitHub Actions for Tests

```yaml
# .github/workflows/test.yml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run test:ci
      - run: npm run build
```

---

## 11. Testing Debt

### What Is Testing Debt

Like technical debt, testing debt accumulates when you skip tests:
- Untested code is harder to refactor
- Bugs regress that you've already fixed
- Manual testing takes longer each time
- You're afraid to change code without tests

### The Testing Debt Budget

Allocate 10% of your development time to paying down testing debt:
- Add tests for frequently-buggy code
- Add tests before refactoring
- Convert manual checks to automated tests
- Fix flaky tests

### When to Write Tests

| Scenario | When to Test |
|----------|-------------|
| New business logic | Write tests alongside code (TDD-lite) |
| Bug fix | Write test first (prevent regression) |
| Refactoring | Write tests before refactoring |
| New API endpoint | Write integration test |
| Simple UI component | Don't test (visual check) |

---

## 12. Common Testing Mistakes

### Mistake 1: Testing Implementation Details

```typescript
// Bad: testing internal state
test('increments counter', () => {
  expect(component.state.count).toBe(1)
})

// Good: testing behavior
test('shows count after click', () => {
  await userEvent.click(button)
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})
```

### Mistake 2: Brittle Tests

```typescript
// Bad: too specific
test('renders correctly', () => {
  expect(container.innerHTML).toMatchSnapshot()
})

// Good: tests what matters
test('shows user name', () => {
  expect(screen.getByText('John Doe')).toBeInTheDocument()
})
```

### Mistake 3: Testing Everything

Writing tests for every single component, utility, and page. Results: slow test suite, high maintenance, low value.

**Fix**: Test business logic, not plumbing.

### Mistake 4: No Regression Tests

You fixed a bug. You deployed it. Two weeks later, it's back.

**Fix**: Write a test for every bug you fix. This prevents regression and builds test coverage over time.

### Mistake 5: Flaky Tests

Tests that pass sometimes and fail other times. They erode trust in the test suite.

**Fix**: If a test is flaky, fix it immediately or remove it. Flaky tests are worse than no tests.

---

## 13. The Solo Testing Manifesto

1. **Test business logic** — That's where the bugs are
2. **Skip UI tests** — Look at it, it's faster
3. **Write a test for every bug** — Prevent regression
4. **Integration tests > Unit tests** — For Solo SaaS
5. **Don't test the framework** — Trust Next.js, Prisma, React
6. **Flaky tests are toxic** — Fix or remove them immediately
7. **Tests should be fast** — If they take > 30 seconds, you have too many
8. **Manual testing is testing too** — Don't automate everything
9. **Test debt is real** — Allocate 10% time to paying it down
10. **Ship before perfect** — Don't delay shipping for 100% coverage

Testing for solo founders is about maximizing bug-prevention per minute spent. Strategic testing means you catch the important bugs and accept the risk on minor issues. This approach lets you ship fast with confidence.
