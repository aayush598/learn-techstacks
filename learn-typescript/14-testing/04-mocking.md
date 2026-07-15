# Mocking in TypeScript

## Overview

Mocking replaces real dependencies with controlled substitutes for testing. TypeScript provides type-safe mocking patterns that ensure mocks match the real implementation.

---

## 1. jest.mock Typing

```typescript
// Mocking an entire module
import { UserService } from '../src/services/user.service';
import { PrismaClient } from '@prisma/client';

// jest.mock automatically creates typed mocks
jest.mock('@prisma/client');

describe('UserService', () => {
  let service: UserService;
  let mockPrisma: jest.Mocked<PrismaClient>;

  beforeEach(() => {
    mockPrisma = new PrismaClient() as jest.Mocked<PrismaClient>;
    service = new UserService(mockPrisma);
  });

  it('should find user by email', async () => {
    // Mock is typed — TypeScript knows the shape
    mockPrisma.user.findUnique.mockResolvedValue({
      id: '1',
      name: 'Alice',
      email: 'alice@test.com',
    });

    const user = await service.findByEmail('alice@test.com');

    expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({
      where: { email: 'alice@test.com' },
    });
    expect(user?.name).toBe('Alice');
  });
});

// Mock with factory
jest.mock('../src/services/email.service', () => ({
  EmailService: jest.fn().mockImplementation(() => ({
    sendEmail: jest.fn().mockResolvedValue(true),
    sendBulkEmails: jest.fn().mockResolvedValue({ sent: 5, failed: 0 }),
  })),
}));

// Partial mock
jest.mock('../src/services/user.service', () => {
  const actual = jest.requireActual('../src/services/user.service');
  return {
    ...actual,
    UserService: jest.fn().mockImplementation(() => ({
      ...actual,
      findById: jest.fn().mockResolvedValue(null),
    })),
  };
});
```

---

## 2. jest.fn Typing

```typescript
// Typed mock functions
interface EmailService {
  sendEmail: (to: string, subject: string, body: string) => Promise<boolean>;
  sendBulkEmails: (emails: Array<{ to: string; subject: string; body: string }>) => Promise<{ sent: number; failed: number }>;
}

// Create typed mock
const mockSendEmail = jest.fn<Promise<boolean>, [string, string, string]>();
const mockSendBulkEmails = jest.fn<Promise<{ sent: number; failed: number }>, [Array<{ to: string; subject: string; body: string }>]>();

const emailService: EmailService = {
  sendEmail: mockSendEmail,
  sendBulkEmails: mockSendBulkEmails,
};

// Mock implementation with typed return
mockSendEmail.mockImplementation(async (to, subject, body) => {
  console.log(`Sending email to ${to}`);
  return true;
});

// Mock resolved value
mockSendEmail.mockResolvedValue(true);

// Mock rejected value
mockSendEmail.mockRejectedValue(new Error('SMTP error'));

// Mock with different return values
mockSendEmail
  .mockResolvedValueOnce(true)
  .mockResolvedValueOnce(false)
  .mockResolvedValue(true);

// Typed mock with arguments
const mockCalculate = jest.fn<(a: number, b: number) => number>();

mockCalculate.mockImplementation((a, b) => a + b);

expect(mockCalculate(2, 3)).toBe(5);
expect(mockCalculate).toHaveBeenCalledWith(2, 3);
expect(mockCalculate).toHaveBeenCalledTimes(1);

// Mock with complex arguments
interface QueryOptions {
  where?: Record<string, any>;
  orderBy?: Record<string, 'asc' | 'desc'>;
  include?: Record<string, boolean>;
}

const mockFindMany = jest.fn<(options: QueryOptions) => Promise<any[]>>();

mockFindMany.mockResolvedValue([
  { id: '1', name: 'Alice' },
  { id: '2', name: 'Bob' },
]);

const results = await mockFindMany({
  where: { role: 'admin' },
  orderBy: { name: 'asc' },
});

expect(results).toHaveLength(2);
```

---

## 3. jest.spyOn Typing

```typescript
// Spying on existing methods
import { UserService } from '../src/services/user.service';

describe('UserService', () => {
  let service: UserService;
  let spy: jest.SpyInstance;

  beforeEach(() => {
    service = new UserService(prisma);
  });

  afterEach(() => {
    spy.mockRestore();
  });

  it('should log when creating user', async () => {
    spy = jest.spyOn(console, 'log').mockImplementation();

    await service.create({
      name: 'Alice',
      email: 'alice@test.com',
    });

    expect(spy).toHaveBeenCalledWith('Creating user: Alice');
  });

  it('should track method calls', async () => {
    spy = jest.spyOn(service, 'findById');

    await service.findById('1');
    await service.findById('2');

    expect(spy).toHaveBeenCalledTimes(2);
    expect(spy).toHaveBeenCalledWith('1');
    expect(spy).toHaveBeenCalledWith('2');
  });

  it('should mock return value', async () => {
    spy = jest.spyOn(service, 'findById').mockResolvedValue({
      id: 'mocked',
      name: 'Mocked User',
    });

    const user = await service.findById('1');

    expect(user?.name).toBe('Mocked User');
  });

  it('should spy on class method', async () => {
    const instance = new Counter();
    spy = jest.spyOn(instance, 'increment');

    instance.increment();
    instance.increment();

    expect(spy).toHaveBeenCalledTimes(2);
  });
});

// Spying on module functions
import * as emailModule from '../src/services/email.service';

describe('Email', () => {
  it('should spy on module function', async () => {
    const spy = jest.spyOn(emailModule, 'sendEmail').mockResolvedValue(true);

    await emailModule.sendEmail('test@test.com', 'Subject', 'Body');

    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});
```

---

## 4. Mock Implementations

```typescript
// Complex mock implementations
interface CacheStore {
  get: <T>(key: string) => Promise<T | null>;
  set: <T>(key: string, value: T, ttl?: number) => Promise<void>;
  delete: (key: string) => Promise<boolean>;
  clear: () => Promise<void>;
}

function createMockCache(): jest.Mocked<CacheStore> {
  const store = new Map<string, any>();

  return {
    get: jest.fn(async <T>(key: string): Promise<T | null> => {
      return store.get(key) ?? null;
    }),
    set: jest.fn(async <T>(key: string, value: T): Promise<void> => {
      store.set(key, value);
    }),
    delete: jest.fn(async (key: string): Promise<boolean> => {
      return store.delete(key);
    }),
    clear: jest.fn(async (): Promise<void> => {
      store.clear();
    }),
  };
}

// Mock with class implementation
class MockLogger {
  logs: string[] = [];

  info = jest.fn((message: string) => {
    this.logs.push(`INFO: ${message}`);
  });

  error = jest.fn((message: string) => {
    this.logs.push(`ERROR: ${message}`);
  });

  warn = jest.fn((message: string) => {
    this.logs.push(`WARN: ${message}`);
  });

  debug = jest.fn((message: string) => {
    this.logs.push(`DEBUG: ${message}`);
  });
}

// Usage
describe('UserService', () => {
  let logger: MockLogger;

  beforeEach(() => {
    logger = new MockLogger();
    service = new UserService(prisma, logger);
  });

  it('should log user creation', async () => {
    await service.create({ name: 'Alice', email: 'alice@test.com' });

    expect(logger.info).toHaveBeenCalledWith('Creating user: Alice');
  });
});
```

---

## 5. Manual Mocks

```typescript
// __mocks__/@prisma/client.ts
import { PrismaClient } from '@prisma/client';

const mockPrismaClient = {
  user: {
    findMany: jest.fn(),
    findUnique: jest.fn(),
    findFirst: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    deleteMany: jest.fn(),
    count: jest.fn(),
    upsert: jest.fn(),
  },
  post: {
    findMany: jest.fn(),
    findUnique: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    deleteMany: jest.fn(),
  },
  $transaction: jest.fn(),
  $disconnect: jest.fn(),
};

export const PrismaClient = jest.fn().mockImplementation(() => mockPrismaClient);

// __mocks__/../src/services/email.service.ts
export const mockEmailService = {
  sendEmail: jest.fn().mockResolvedValue(true),
  sendBulkEmails: jest.fn().mockResolvedValue({ sent: 0, failed: 0 }),
};

export const EmailService = jest.fn().mockImplementation(() => mockEmailService);
```

---

## 6. MSW (Mock Service Worker)

```typescript
// src/mocks/handlers.ts
import { rest } from 'msw';

interface User {
  id: string;
  name: string;
  email: string;
}

const users: User[] = [
  { id: '1', name: 'Alice', email: 'alice@test.com' },
  { id: '2', name: 'Bob', email: 'bob@test.com' },
];

export const handlers = [
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json({ data: users, total: users.length }));
  }),

  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params;
    const user = users.find((u) => u.id === id);
    if (!user) {
      return res(ctx.status(404), ctx.json({ error: 'User not found' }));
    }
    return res(ctx.json(user));
  }),

  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json() as Omit<User, 'id'>;
    const newUser: User = { ...body, id: String(users.length + 1) };
    users.push(newUser);
    return res(ctx.status(201), ctx.json(newUser));
  }),

  rest.put('/api/users/:id', async (req, res, ctx) => {
    const { id } = req.params;
    const body = await req.json() as Partial<User>;
    const index = users.findIndex((u) => u.id === id);
    if (index === -1) {
      return res(ctx.status(404), ctx.json({ error: 'User not found' }));
    }
    users[index] = { ...users[index], ...body };
    return res(ctx.json(users[index]));
  }),

  rest.delete('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params;
    const index = users.findIndex((u) => u.id === id);
    if (index === -1) {
      return res(ctx.status(404), ctx.json({ error: 'User not found' }));
    }
    users.splice(index, 1);
    return res(ctx.status(204));
  }),
];

// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// tests/setup.ts
import { server } from '../src/mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Usage in test
describe('User API client', () => {
  it('should fetch users', async () => {
    const result = await fetchUsers();
    expect(result.data).toHaveLength(2);
  });

  it('should handle 404', async () => {
    server.use(
      rest.get('/api/users/:id', (req, res, ctx) => {
        return res(ctx.status(404), ctx.json({ error: 'Not found' }));
      })
    );

    await expect(fetchUser('999')).rejects.toThrow('Not found');
  });
});
```

---

## 7. Best Practices

1. **Use `jest.Mocked<T>`** for type-safe mocks of classes and interfaces.
2. **Type `jest.fn()`** with generic parameters for return and argument types.
3. **Use manual mocks** for complex modules in `__mocks__` directories.
4. **Use MSW** for API mocking in integration and E2E tests.
5. **Mock at the boundary** — mock external services, not internal logic.
6. **Restore mocks** after each test with `mockRestore()` or `clearMocks`.
7. **Use `jest.spyOn`** when you need to mock a single method.
8. **Create mock factories** for reusable mock objects.
9. **Verify mock calls** with `toHaveBeenCalledWith`, `toHaveBeenCalledTimes`.
10. **Avoid over-mocking** — test as much real code as possible.

---

## Interview Questions

1. What is the difference between `jest.mock` and `jest.fn`?
2. How do you type a mock function in TypeScript?
3. What is `jest.Mocked<T>` and when should you use it?
4. How do you create manual mocks for modules?
5. What is MSW and how does it differ from jest mocking?
6. How do you mock class methods with `jest.spyOn`?
7. How do you mock async functions?
8. How do you verify that a mock was called with specific arguments?
9. How do you reset mocks between tests?
10. What are the best practices for mocking in TypeScript?
