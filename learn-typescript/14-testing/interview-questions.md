# Testing Interview Questions

## 25+ Questions with Detailed Answers

---

### 1. What is the difference between unit, integration, and E2E testing?

**Answer:**

- **Unit testing** — tests individual functions, classes, or modules in isolation. Fast, focused, easy to debug.
- **Integration testing** — tests how multiple components work together (API + database, service + repository). Slower, more realistic.
- **E2E testing** — tests the entire application flow from the user's perspective (browser automation). Slowest, most realistic, hardest to maintain.

```
Unit:         Function A → [mock B] → Result
Integration:  Function A → Real B → Real Database
E2E:          Browser → HTTP → Server → Database → Response
```

**Rule of thumb:** Follow the testing pyramid — many unit tests, fewer integration tests, even fewer E2E tests.

---

### 2. How do you set up Jest for TypeScript?

**Answer:**

```bash
npm install -D jest ts-jest @types/jest
npx ts-jest config:init
```

Key configuration in `jest.config.ts`:
- `preset: 'ts-jest'` — uses ts-jest for TypeScript compilation.
- `testEnvironment: 'node'` — for Node.js tests.
- `moduleNameMapper` — for path aliases.
- `setupFilesAfterEnv` — for global test setup.

---

### 3. What is the AAA pattern in testing?

**Answer:**

AAA stands for **Arrange, Act, Assert**:

```typescript
it('should add two numbers', () => {
  // Arrange — set up test data and conditions
  const a = 2;
  const b = 3;

  // Act — execute the code under test
  const result = add(a, b);

  // Assert — verify the result
  expect(result).toBe(5);
});
```

This pattern makes tests readable and consistent.

---

### 4. How do you type mock functions in Jest?

**Answer:**

```typescript
// Option 1: jest.Mocked<T>
jest.mock('./module');
const mockModule = jest.mocked(module);

// Option 2: jest.fn with generics
const mockFn = jest.fn<ReturnType, Parameters>();
const mockFn = jest.fn<Promise<boolean>, [string, number]>();

// Option 3: Type assertion
const mockFn = jest.fn() as jest.Mock<string, [number]>;

// Option 4: Manual typing
const mockFn: (a: number) => string = jest.fn().mockReturnValue('test');
```

---

### 5. What is `tsd` and how do you use it?

**Answer:**

`tsd` is a library for testing TypeScript type definitions at compile time:

```typescript
// index.test-d.ts
import { expectType, expectError } from 'tsd';
import { add } from '.';

expectType<number>(add(1, 2));     // Should be number
expectError(add('a', 'b'));       // Should cause compile error
expectError(add(1, 'b'));         // Should cause compile error
```

It runs during `tsc` compilation and fails if type assertions are wrong.

---

### 6. How do you mock API calls in tests?

**Answer:**

Three approaches:

```typescript
// 1. jest.mock
jest.mock('./api');
import { fetchUsers } from './api';
(fetchUsers as jest.Mock).mockResolvedValue([{ id: 1 }]);

// 2. MSW (Mock Service Worker)
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([{ id: 1 }]));
  })
);

// 3. nock
import nock from 'nock';
nock('http://localhost').get('/api/users').reply(200, [{ id: 1 }]);
```

---

### 7. What is snapshot testing and when should you use it?

**Answer:**

Snapshot testing captures the rendered output and compares it to a stored snapshot:

```typescript
it('should render correctly', () => {
  const { container } = render(<Button label="Click" />);
  expect(container).toMatchSnapshot();
});
```

**When to use:**
- UI components with complex output.
- Serialized data structures.
- Configuration objects.

**When to avoid:**
- Large snapshots that are hard to review.
- Frequently changing components.
- Tests where you need specific assertions.

---

### 8. How do you test async functions?

**Answer:**

```typescript
// Async/await (preferred)
it('should fetch user', async () => {
  const user = await fetchUser('1');
  expect(user.name).toBe('Alice');
});

// Reject testing
it('should throw on invalid id', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Invalid ID');
});

// With done callback (less preferred)
it('should fetch user', (done) => {
  fetchUser('1').then((user) => {
    expect(user.name).toBe('Alice');
    done();
  });
});
```

---

### 9. How do you test error-throwing functions?

**Answer:**

```typescript
// Synchronous errors
it('should throw on division by zero', () => {
  expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
});

// With error type
it('should throw TypeError', () => {
  expect(() => parse('invalid')).toThrow(TypeError);
});

// Async errors
it('should reject with error', async () => {
  await expect(asyncOperation()).rejects.toThrow('Operation failed');
});

// Custom error classes
it('should throw NotFoundError', async () => {
  await expect(findUser('missing')).rejects.toThrow(NotFoundError);
});
```

---

### 10. What are test containers?

**Answer:**

Test containers are disposable Docker containers for integration testing:

```typescript
import { GenericContainer } from 'testcontainers';

let container: StartedTestContainer;

beforeAll(async () => {
  container = await new GenericContainer('postgres')
    .withEnv('POSTGRES_DB', 'test_db')
    .withExposedPorts(5432)
    .start();

  process.env.DATABASE_URL = `postgresql://test:test@localhost:${container.getMappedPort(5432)}/test_db`;
});

afterAll(async () => {
  await container.stop();
});
```

Benefits: real database behavior, isolated tests, no shared state.

---

### 11. How do you test React hooks?

**Answer:**

```typescript
import { renderHook, act } from '@testing-library/react-hooks';

describe('useCounter', () => {
  it('should increment count', () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should reset count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(0);
  });
});
```

---

### 12. How do you test custom React hooks with dependencies?

**Answer:**

```typescript
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

it('should fetch user data', async () => {
  const wrapper = createTestWrapper();

  const { result, waitForNextUpdate } = renderHook(
    () => useUser('1'),
    { wrapper }
  );

  expect(result.current.loading).toBe(true);

  await waitForNextUpdate();

  expect(result.current.loading).toBe(false);
  expect(result.current.data).toBeDefined();
});
```

---

### 13. How do you test API endpoints?

**Answer:**

```typescript
import request from 'supertest';
import { createApp } from '../src/app';

describe('GET /api/users', () => {
  let app: Express.Application;

  beforeAll(async () => {
    app = await createApp();
  });

  it('should return 200 with users', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200);

    expect(response.body.data).toBeInstanceOf(Array);
    expect(response.body.pagination).toBeDefined();
  });

  it('should return 401 without auth token', async () => {
    await request(app)
      .get('/api/users')
      .expect(401);
  });
});
```

---

### 14. How do you test form validation?

**Answer:**

```typescript
// Test the validation schema directly
import { CreateUserSchema } from '../src/validation';

describe('CreateUserSchema', () => {
  it('should accept valid data', () => {
    const result = CreateUserSchema.safeParse({
      name: 'Alice',
      email: 'alice@test.com',
      age: 25,
    });
    expect(result.success).toBe(true);
  });

  it('should reject invalid email', () => {
    const result = CreateUserSchema.safeParse({
      name: 'Alice',
      email: 'invalid',
      age: 25,
    });
    expect(result.success).toBe(false);
  });

  it('should reject age under 13', () => {
    const result = CreateUserSchema.safeParse({
      name: 'Alice',
      email: 'alice@test.com',
      age: 10,
    });
    expect(result.success).toBe(false);
  });
});
```

---

### 15. How do you test error handling middleware?

**Answer:**

```typescript
import { errorHandler } from '../src/middleware/error';
import { AppError } from '../src/errors';

describe('Error Handler', () => {
  let req: Partial<Request>;
  let res: Partial<Response>;
  let next: NextFunction;

  beforeEach(() => {
    req = {};
    res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn(),
    };
    next = jest.fn();
  });

  it('should handle AppError', () => {
    const error = new AppError(404, 'NOT_FOUND', 'User not found');

    errorHandler(error, req as Request, res as Response, next);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      error: { code: 'NOT_FOUND', message: 'User not found' },
    });
  });

  it('should handle unknown errors', () => {
    const error = new Error('Unexpected');

    errorHandler(error, req as Request, res as Response, next);

    expect(res.status).toHaveBeenCalledWith(500);
  });
});
```

---

### 16. What is test-driven development (TDD)?

**Answer:**

TDD is a development process where you:
1. **Write a failing test** (Red)
2. **Write minimum code** to pass the test (Green)
3. **Refactor** the code while keeping tests passing (Refactor)

```typescript
// Step 1: Write failing test
it('should calculate factorial', () => {
  expect(factorial(5)).toBe(120);
});

// Step 2: Write implementation
function factorial(n: number): number {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// Step 3: Refactor if needed
```

Benefits: better design, higher coverage, confidence in changes.

---

### 17. How do you test database operations?

**Answer:**

```typescript
describe('User Repository', () => {
  let prisma: PrismaClient;

  beforeAll(() => { prisma = new PrismaClient(); });
  afterAll(() => prisma.$disconnect());
  beforeEach(() => prisma.user.deleteMany());

  it('should create and retrieve user', async () => {
    const created = await prisma.user.create({
      data: { name: 'Alice', email: 'alice@test.com' },
    });

    const found = await prisma.user.findUnique({
      where: { id: created.id },
    });

    expect(found?.name).toBe('Alice');
  });

  it('should handle transactions', async () => {
    await expect(
      prisma.$transaction(async (tx) => {
        await tx.user.create({ data: { name: 'Alice', email: 'a@test.com' } });
        throw new Error('Rollback');
      })
    ).rejects.toThrow('Rollback');

    expect(await prisma.user.count()).toBe(0);
  });
});
```

---

### 18. How do you test WebSocket connections?

**Answer:**

```typescript
import { Server } from 'socket.io';
import { io as Client } from 'socket.io-client';

describe('WebSocket', () => {
  let server: Server;
  let clientSocket: ReturnType<typeof Client>;

  beforeAll((done) => {
    server = new Server(3001);
    clientSocket = Client('http://localhost:3001');
    clientSocket.on('connect', done);
  });

  afterAll(() => {
    server.close();
    clientSocket.disconnect();
  });

  it('should receive broadcast message', (done) => {
    clientSocket.on('message', (data) => {
      expect(data.content).toBe('Hello');
      done();
    });

    server.emit('message', { content: 'Hello' });
  });
});
```

---

### 19. How do you achieve good test coverage?

**Answer:**

1. **Write tests for every bug** — regression tests prevent reoccurrence.
2. **Test edge cases** — empty inputs, null values, boundaries.
3. **Use coverage tools** — Istanbul/c8 for line/branch/function coverage.
4. **Set coverage thresholds** — fail CI if coverage drops.
5. **Focus on critical paths** — authentication, payments, data integrity.
6. **Don't chase 100%** — some code (types, configs) doesn't need tests.
7. **Test behavior, not implementation** — test what it does, not how.

---

### 20. How do you test performance?

**Answer:**

```typescript
describe('Performance', () => {
  it('should sort 10000 items under 100ms', () => {
    const items = Array.from({ length: 10000 }, () => Math.random());

    const start = performance.now();
    items.sort((a, b) => a - b);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
  });

  it('should handle concurrent requests', async () => {
    const promises = Array.from({ length: 100 }, (_, i) =>
      request(app).get(`/api/users/${i}`)
    );

    const start = performance.now();
    const results = await Promise.all(promises);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(5000);
    results.forEach((r) => expect(r.status).toBe(200));
  });
});
```

---

### 21. How do you test type safety?

**Answer:**

```typescript
// Using expect-type
import { expectType, expectError } from 'expect-type';

function add(a: number, b: number): number {
  return a + b;
}

expectType<number>(add(1, 2));
expectError(add('1', 2));   // Should fail
expectError(add(1));        // Should fail — missing argument

// Using tsd
import { expectType, expectError } from 'tsd';

expectType<number>(add(1, 2));
expectError(add('1', 2));
```

---

### 22. What is mocking and when should you use it?

**Answer:**

Mocking replaces real dependencies with controlled substitutes.

**When to mock:**
- External APIs (avoid network calls in tests).
- Database operations (faster, deterministic).
- Time-dependent code (Date, setTimeout).
- Random values (Math.random, UUIDs).
- File system operations.

**When NOT to mock:**
- The code under test itself.
- Simple pure functions.
- When you need to test real integration.

---

### 23. How do you test a React component?

**Answer:**

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserList } from './UserList';

describe('UserList', () => {
  it('should render users', async () => {
    render(<UserList users={[
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ]} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('should call onUserClick when user is clicked', async () => {
    const handleClick = jest.fn();
    render(<UserList users={[{ id: '1', name: 'Alice' }]} onUserClick={handleClick} />);

    fireEvent.click(screen.getByText('Alice'));

    expect(handleClick).toHaveBeenCalledWith('1');
  });

  it('should show loading state', async () => {
    render(<UserList loading={true} />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
```

---

### 24. How do you test a custom hook?

**Answer:**

```typescript
import { renderHook, act } from '@testing-library/react';

describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should return initial value', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'default'));
    expect(result.current[0]).toBe('default');
  });

  it('should update value', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'default'));

    act(() => {
      result.current[1]('new value');
    });

    expect(result.current[0]).toBe('new value');
    expect(localStorage.getItem('key')).toBe(JSON.stringify('new value'));
  });

  it('should persist across re-renders', () => {
    const { result, rerender } = renderHook(() => useLocalStorage('key', 'default'));

    act(() => {
      result.current[1]('persisted');
    });

    rerender();

    expect(result.current[0]).toBe('persisted');
  });
});
```

---

### 25. How do you test authentication flows?

**Answer:**

```typescript
describe('Authentication Flow', () => {
  it('should login and store token', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@test.com', password: 'password' })
      .expect(200);

    expect(response.body.token).toBeDefined();
    expect(response.body.user.email).toBe('user@test.com');
  });

  it('should reject invalid credentials', async () => {
    await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@test.com', password: 'wrong' })
      .expect(401);
  });

  it('should access protected route with valid token', async () => {
    const { token } = await loginAs('user@test.com', 'password');

    await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });

  it('should refresh expired token', async () => {
    const expiredToken = generateExpiredToken();
    const response = await request(app)
      .post('/api/auth/refresh')
      .send({ token: expiredToken })
      .expect(200);

    expect(response.body.token).toBeDefined();
  });
});
```

---

### 26. How do you test error boundaries?

**Answer:**

```typescript
import { render, screen } from '@testing-library/react';
import { ErrorBoundary } from './ErrorBoundary';

const ThrowingComponent = () => {
  throw new Error('Test error');
};

describe('ErrorBoundary', () => {
  it('should render fallback UI on error', () => {
    render(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  it('should render children when no error', () => {
    render(
      <ErrorBoundary>
        <div>Normal content</div>
      </ErrorBoundary>
    );

    expect(screen.getByText('Normal content')).toBeInTheDocument();
  });

  it('should have retry button', () => {
    render(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    );

    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });
});
```

---

### 27. What is the difference between mocks, stubs, and spies?

**Answer:**

- **Mock** — a fake implementation that verifies interactions. Records calls and allows assertions.
- **Stub** — a fake implementation that returns predefined data. Doesn't track interactions.
- **Spy** — wraps a real function to track calls while preserving original behavior.

```typescript
// Mock — full fake implementation
const mockService = {
  findById: jest.fn().mockResolvedValue({ id: '1', name: 'Alice' }),
};

// Stub — predefined return value
const stubService = {
  findById: () => Promise.resolve({ id: '1', name: 'Alice' }),
};

// Spy — wraps real implementation
const spy = jest.spyOn(realService, 'findById');
await realService.findById('1');
expect(spy).toHaveBeenCalledWith('1');
```

---

### 28. How do you test a file upload?

**Answer:**

```typescript
import request from 'supertest';
import path from 'path';

describe('File Upload', () => {
  it('should upload image successfully', async () => {
    const response = await request(app)
      .post('/api/upload')
      .attach('file', path.resolve(__dirname, 'fixtures/test-image.png'))
      .expect(200);

    expect(response.body.url).toBeDefined();
    expect(response.body.filename).toBe('test-image.png');
  });

  it('should reject non-image files', async () => {
    await request(app)
      .post('/api/upload')
      .attach('file', path.resolve(__dirname, 'fixtures/test.txt'))
      .expect(400);
  });

  it('should reject files over size limit', async () => {
    await request(app)
      .post('/api/upload')
      .attach('file', path.resolve(__dirname, 'fixtures/large-image.png'))
      .expect(413);
  });
});
```

---

### 29. How do you write maintainable tests?

**Answer:**

1. **Follow naming conventions** — `should [behavior] when [condition]`.
2. **Use `describe` blocks** for logical grouping.
3. **Keep tests independent** — no test should depend on another.
4. **Use `beforeEach`** for common setup.
5. **Avoid testing implementation details** — test behavior.
6. **Use page objects** for E2E tests.
7. **Create test utilities** for common operations.
8. **Use fixtures** for consistent test data.
9. **Keep tests simple** — one assertion per concept.
10. **Refactor tests** like production code.

---

### 30. How do you test a microservice?

**Answer:**

```typescript
// Test service-to-service communication
describe('Order Service', () => {
  let orderService: OrderService;
  let mockPaymentService: jest.Mocked<PaymentService>;
  let mockInventoryService: jest.Mocked<InventoryService>;

  beforeEach(() => {
    mockPaymentService = {
      charge: jest.fn().mockResolvedValue({ id: 'charge-1', status: 'success' }),
      refund: jest.fn().mockResolvedValue({ id: 'refund-1', status: 'success' }),
    } as any;

    mockInventoryService = {
      reserve: jest.fn().mockResolvedValue(true),
      release: jest.fn().mockResolvedValue(true),
    } as any;

    orderService = new OrderService(mockPaymentService, mockInventoryService);
  });

  it('should create order and process payment', async () => {
    const order = await orderService.create({
      userId: 'user-1',
      items: [{ productId: 'prod-1', quantity: 2 }],
    });

    expect(mockInventoryService.reserve).toHaveBeenCalledWith('prod-1', 2);
    expect(mockPaymentService.charge).toHaveBeenCalledWith('user-1', expect.any(Number));
    expect(order.status).toBe('confirmed');
  });

  it('should rollback on payment failure', async () => {
    mockPaymentService.charge.mockRejectedValue(new Error('Payment failed'));

    await expect(
      orderService.create({
        userId: 'user-1',
        items: [{ productId: 'prod-1', quantity: 2 }],
      })
    ).rejects.toThrow('Payment failed');

    expect(mockInventoryService.release).toHaveBeenCalledWith('prod-1', 2);
  });
});
```

---

### 31. How do you test a GraphQL API?

**Answer:**

```typescript
import { createTestClient } from 'apollo-server-testing';
import { createApolloServer } from '../src/server';

describe('GraphQL API', () => {
  let server: ApolloServer;
  let client: any;

  beforeAll(async () => {
    server = await createApolloServer();
    client = createTestClient(server);
  });

  it('should query users', async () => {
    const response = await client.query({
      query: gql`
        query GetUsers {
          users {
            id
            name
            email
          }
        }
      `,
    });

    expect(response.data.users).toBeInstanceOf(Array);
    expect(response.errors).toBeUndefined();
  });

  it('should create user with mutation', async () => {
    const response = await client.mutate({
      mutation: gql`
        mutation CreateUser($input: CreateUserInput!) {
          createUser(input: $input) {
            id
            name
          }
        }
      `,
      variables: {
        input: { name: 'Alice', email: 'alice@test.com', age: 30 },
      },
    });

    expect(response.data.createUser.name).toBe('Alice');
  });

  it('should return validation errors', async () => {
    const response = await client.mutate({
      mutation: gql`
        mutation CreateUser($input: CreateUserInput!) {
          createUser(input: $input) {
            id
          }
        }
      `,
      variables: {
        input: { name: '', email: 'invalid' },
      },
    });

    expect(response.errors).toBeDefined();
  });
});
```
