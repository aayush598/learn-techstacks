# Jest with TypeScript

## Overview

Jest is the most popular testing framework for JavaScript/TypeScript. This guide covers setup, configuration, and typing for Jest in TypeScript projects.

---

## 1. Setup and Installation

```bash
# Install dependencies
npm install -D jest ts-jest @types/jest

# Initialize Jest config
npx ts-jest config:init
```

```json
// tsconfig.json (add test files)
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "types": ["jest", "node"]
  },
  "include": ["src/**/*", "tests/**/*"]
}
```

---

## 2. jest.config.ts

```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',

  // File patterns
  testMatch: [
    '**/__tests__/**/*.ts',
    '**/*.test.ts',
    '**/*.spec.ts',
  ],

  // Module resolution
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1',
  },

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],

  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/types/**',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // Transform configuration
  transform: {
    '^.+\\.ts$': ['ts-jest', {
      tsconfig: 'tsconfig.test.json',
      diagnostics: true,
    }],
  },

  // Timeout
  testTimeout: 10000,

  // Clear mocks between tests
  clearMocks: true,

  // Verbose output
  verbose: true,
};

export default config;
```

---

## 3. Typed Test Files

```typescript
// tests/user.test.ts
import { UserService } from '../src/services/user.service';
import { PrismaClient, User } from '@prisma/client';

// Mock PrismaClient with typed mock
jest.mock('@prisma/client');

describe('UserService', () => {
  let service: UserService;
  let prisma: jest.Mocked<PrismaClient>;

  beforeEach(() => {
    prisma = {
      user: {
        findMany: jest.fn(),
        findUnique: jest.fn(),
        create: jest.fn(),
        update: jest.fn(),
        delete: jest.fn(),
        count: jest.fn(),
      },
    } as any;

    service = new UserService(prisma);
  });

  describe('findAll', () => {
    it('should return paginated users', async () => {
      const mockUsers: User[] = [
        { id: '1', name: 'Alice', email: 'alice@test.com', role: 'USER', createdAt: new Date(), updatedAt: new Date() },
        { id: '2', name: 'Bob', email: 'bob@test.com', role: 'ADMIN', createdAt: new Date(), updatedAt: new Date() },
      ];

      (prisma.user.findMany as jest.Mock).mockResolvedValue(mockUsers);
      (prisma.user.count as jest.Mock).mockResolvedValue(2);

      const result = await service.findAll({ page: 1, limit: 10 });

      expect(result.data).toEqual(mockUsers);
      expect(result.total).toBe(2);
      expect(result.pages).toBe(1);
      expect(prisma.user.findMany).toHaveBeenCalledWith({
        skip: 0,
        take: 10,
        where: {},
      });
    });
  });

  describe('findById', () => {
    it('should return a user by id', async () => {
      const mockUser: User = {
        id: '1',
        name: 'Alice',
        email: 'alice@test.com',
        role: 'USER',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      (prisma.user.findUnique as jest.Mock).mockResolvedValue(mockUser);

      const result = await service.findById('1');

      expect(result).toEqual(mockUser);
      expect(prisma.user.findUnique).toHaveBeenCalledWith({
        where: { id: '1' },
      });
    });

    it('should return null if user not found', async () => {
      (prisma.user.findUnique as jest.Mock).mockResolvedValue(null);

      const result = await service.findById('nonexistent');

      expect(result).toBeNull();
    });
  });
});
```

---

## 4. Typed describe/it/expect

```typescript
// All Jest functions are typed through @types/jest
describe('String utilities', () => {
  it('should capitalize first letter', () => {
    const result: string = capitalize('hello');
    expect(result).toBe('Hello');
    expect(typeof result).toBe('string');
  });

  it('should handle empty string', () => {
    expect(capitalize('')).toBe('');
  });

  it('should throw on non-string input', () => {
    expect(() => capitalize(null as any)).toThrow('Input must be a string');
  });
});

// Typed test.each
describe.each<{ input: string; expected: string }>([
  { input: 'hello', expected: 'Hello' },
  { input: 'world', expected: 'World' },
  { input: '', expected: '' },
])('capitalize($input)', ({ input, expected }) => {
  it(`should return ${expected}`, () => {
    expect(capitalize(input)).toBe(expected);
  });
});

// Typed describe.each with table format
describe.each([
  ['addition', 1 + 1, 2],
  ['subtraction', 5 - 3, 2],
  ['multiplication', 2 * 3, 6],
] as const)('%s', (_, result, expected) => {
  it(`should equal ${expected}`, () => {
    expect(result).toBe(expected);
  });
});

// Type-safe matchers
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

// Custom matcher types
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeSuccessful(): R;
      toHaveStatus(status: number): R;
    }
  }
}

expect.extend({
  toBeSuccessful(received: ApiResponse<any>) {
    const pass = received.status >= 200 && received.status < 300;
    return {
      pass,
      message: () =>
        `expected ${received.status} ${pass ? 'not ' : ''}to be successful (2xx)`,
    };
  },

  toHaveStatus(received: ApiResponse<any>, status: number) {
    const pass = received.status === status;
    return {
      pass,
      message: () =>
        `expected ${received.status} ${pass ? 'not ' : ''}to be ${status}`,
    };
  },
});

// Usage
it('should return successful response', () => {
  const response: ApiResponse<User> = {
    data: { id: '1', name: 'Alice' } as User,
    status: 200,
  };
  expect(response).toBeSuccessful();
  expect(response).toHaveStatus(200);
});
```

---

## 5. Setup Files

```typescript
// tests/setup.ts
import { PrismaClient } from '@prisma/client';

// Global test setup
beforeAll(async () => {
  // Connect to test database
  process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test_db';
});

afterAll(async () => {
  // Cleanup
});

// Typed global test utilities
declare global {
  var testUtils: {
    createTestUser: (overrides?: Partial<User>) => Promise<User>;
    cleanupDatabase: () => Promise<void>;
  };
}

global.testUtils = {
  createTestUser: async (overrides) => {
    const prisma = new PrismaClient();
    const user = await prisma.user.create({
      data: {
        name: 'Test User',
        email: `test-${Date.now()}@example.com`,
        ...overrides,
      },
    });
    await prisma.$disconnect();
    return user;
  },

  cleanupDatabase: async () => {
    const prisma = new PrismaClient();
    await prisma.user.deleteMany();
    await prisma.$disconnect();
  },
};

// Custom Jest matchers
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} ${pass ? 'not ' : ''}to be within range ${floor} - ${ceiling}`,
    };
  },
});

declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
    }
  }
}
```

---

## 6. Global Setup/Teardown

```typescript
// jest.global-setup.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export default async function globalSetup() {
  console.log('Starting test database...');

  // Start test database
  await execAsync('docker-compose -f docker-compose.test.yml up -d');

  // Wait for database to be ready
  await new Promise((resolve) => setTimeout(resolve, 5000));

  // Run migrations
  await execAsync('npx prisma migrate deploy');

  console.log('Test database ready');
}

// jest.global-teardown.ts
export default async function globalTeardown() {
  console.log('Stopping test database...');
  await execAsync('docker-compose -f docker-compose.test.yml down');
}
```

---

## 7. Coverage Configuration

```typescript
// Coverage thresholds
const config: Config = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Per-file thresholds
    'src/services/user.service.ts': {
      branches: 90,
      functions: 100,
      lines: 90,
      statements: 90,
    },
  },

  // Coverage path ignore patterns
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/types/',
    '/__mocks__/',
  ],

  // Collect coverage from
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/types/**',
    '!src/**/*.mock.ts',
  ],
};
```

---

## 8. Best Practices

1. **Use `ts-jest`** for TypeScript compilation in tests.
2. **Always type mocks** — use `jest.Mock<T>` or `jest.Mocked<T>`.
3. **Use `moduleNameMapper`** for path aliases.
4. **Set coverage thresholds** to maintain code quality.
5. **Use `testMatch`** patterns that exclude non-test files.
6. **Create typed test utilities** for common operations.
7. **Use `setupFilesAfterEnv`** for global test configuration.
8. **Type custom matchers** with declaration merging.
9. **Use `test.each`** for table-driven tests with typed data.
10. **Keep test config separate** — use `tsconfig.test.json` if needed.

---

## Interview Questions

1. How do you configure Jest for TypeScript?
2. What is `ts-jest` and why is it needed?
3. How do you type mock functions in Jest?
4. How do you set up path aliases in Jest?
5. How do you create custom Jest matchers with types?
6. What is the difference between `setupFiles` and `setupFilesAfterEnv`?
7. How do you configure coverage thresholds?
8. How do you use `test.each` with TypeScript?
9. How do you mock ES modules in Jest?
10. How do you test async functions with TypeScript?
