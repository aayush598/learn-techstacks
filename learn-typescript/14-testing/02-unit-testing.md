# Unit Testing in TypeScript

## Overview

Unit testing verifies individual functions, classes, and modules in isolation. This guide covers patterns for testing pure functions, classes, hooks, and snapshot testing with TypeScript.

---

## 1. Unit Testing Functions

```typescript
// src/utils/math.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) throw new Error('Cannot divide by zero');
  return a / b;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function fibonacci(n: number): number {
  if (n < 0) throw new Error('Input must be non-negative');
  if (n <= 1) return n;
  let a = 0, b = 1;
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b];
  }
  return b;
}

// tests/utils/math.test.ts
import { add, divide, clamp, fibonacci } from '../../src/utils/math';

describe('add', () => {
  it('should add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(add(-1, -2)).toBe(-3);
  });

  it('should handle zero', () => {
    expect(add(5, 0)).toBe(5);
  });
});

describe('divide', () => {
  it('should divide two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should handle decimal results', () => {
    expect(divide(10, 3)).toBeCloseTo(3.333, 2);
  });

  it('should throw on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });
});

describe('clamp', () => {
  it.each<{ value: number; min: number; max: number; expected: number }>([
    { value: 5, min: 0, max: 10, expected: 5 },
    { value: -5, min: 0, max: 10, expected: 0 },
    { value: 15, min: 0, max: 10, expected: 10 },
    { value: 5.5, min: 0, max: 10, expected: 5.5 },
  ])('clamps $value to [$min, $max] = $expected', ({ value, min, max, expected }) => {
    expect(clamp(value, min, max)).toBe(expected);
  });
});

describe('fibonacci', () => {
  it('should return correct fibonacci numbers', () => {
    const expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34];
    expected.forEach((val, i) => {
      expect(fibonacci(i)).toBe(val);
    });
  });

  it('should throw on negative input', () => {
    expect(() => fibonacci(-1)).toThrow('Input must be non-negative');
  });
});
```

---

## 2. Unit Testing Classes

```typescript
// src/services/counter.ts
export class Counter {
  private count: number;
  private readonly min: number;
  private readonly max: number;
  private history: number[] = [];

  constructor(initialValue: number = 0, min: number = -Infinity, max: number = Infinity) {
    this.count = initialValue;
    this.min = min;
    this.max = max;
    this.history.push(initialValue);
  }

  increment(step: number = 1): number {
    this.count = Math.min(this.count + step, this.max);
    this.history.push(this.count);
    return this.count;
  }

  decrement(step: number = 1): number {
    this.count = Math.max(this.count - step, this.min);
    this.history.push(this.count);
    return this.count;
  }

  reset(): number {
    const initial = this.history[0];
    this.count = initial;
    this.history.push(initial);
    return this.count;
  }

  getCount(): number {
    return this.count;
  }

  getHistory(): number[] {
    return [...this.history];
  }
}

// tests/services/counter.test.ts
import { Counter } from '../../src/services/counter';

describe('Counter', () => {
  let counter: Counter;

  beforeEach(() => {
    counter = new Counter(0);
  });

  describe('constructor', () => {
    it('should initialize with default value', () => {
      expect(new Counter().getCount()).toBe(0);
    });

    it('should initialize with custom value', () => {
      expect(new Counter(10).getCount()).toBe(10);
    });

    it('should respect min/max bounds', () => {
      const bounded = new Counter(5, 0, 10);
      expect(bounded.getCount()).toBe(5);
    });
  });

  describe('increment', () => {
    it('should increment by 1 by default', () => {
      expect(counter.increment()).toBe(1);
      expect(counter.increment()).toBe(2);
    });

    it('should increment by custom step', () => {
      expect(counter.increment(5)).toBe(5);
      expect(counter.increment(3)).toBe(8);
    });

    it('should not exceed max', () => {
      const bounded = new Counter(0, -Infinity, 5);
      expect(bounded.increment(10)).toBe(5);
    });

    it('should record history', () => {
      counter.increment(1);
      counter.increment(2);
      expect(counter.getHistory()).toEqual([0, 1, 3]);
    });
  });

  describe('decrement', () => {
    it('should decrement by 1 by default', () => {
      expect(counter.decrement()).toBe(-1);
    });

    it('should not go below min', () => {
      const bounded = new Counter(0, 0, 10);
      expect(bounded.decrement(10)).toBe(0);
    });
  });

  describe('reset', () => {
    it('should reset to initial value', () => {
      counter.increment(5);
      counter.increment(3);
      counter.reset();
      expect(counter.getCount()).toBe(0);
    });

    it('should record reset in history', () => {
      counter.increment(5);
      counter.reset();
      expect(counter.getHistory()).toEqual([0, 5, 0]);
    });
  });
});
```

---

## 3. Unit Testing with Mocking

```typescript
// src/services/email.service.ts
import { Transporter, createTransport } from 'nodemailer';

interface EmailOptions {
  to: string;
  subject: string;
  body: string;
}

export class EmailService {
  private transporter: Transporter;

  constructor() {
    this.transporter = createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
    });
  }

  async sendEmail(options: EmailOptions): Promise<boolean> {
    try {
      await this.transporter.sendMail({
        from: process.env.SMTP_FROM,
        to: options.to,
        subject: options.subject,
        html: options.body,
      });
      return true;
    } catch {
      return false;
    }
  }

  async sendBulkEmails(emails: EmailOptions[]): Promise<{ sent: number; failed: number }> {
    let sent = 0;
    let failed = 0;

    for (const email of emails) {
      const result = await this.sendEmail(email);
      if (result) sent++;
      else failed++;
    }

    return { sent, failed };
  }
}

// tests/services/email.service.test.ts
import { EmailService } from '../../src/services/email.service';

// Mock nodemailer
jest.mock('nodemailer', () => ({
  createTransport: jest.fn(() => ({
    sendMail: jest.fn(),
  })),
}));

describe('EmailService', () => {
  let service: EmailService;
  let mockSendMail: jest.Mock;

  beforeEach(() => {
    service = new EmailService();
    mockSendMail = (service as any).transporter.sendMail;
    mockSendMail.mockClear();
  });

  describe('sendEmail', () => {
    it('should send email successfully', async () => {
      mockSendMail.mockResolvedValue({ messageId: '123' });

      const result = await service.sendEmail({
        to: 'user@test.com',
        subject: 'Test',
        body: '<p>Hello</p>',
      });

      expect(result).toBe(true);
      expect(mockSendMail).toHaveBeenCalledWith({
        from: undefined,
        to: 'user@test.com',
        subject: 'Test',
        html: '<p>Hello</p>',
      });
    });

    it('should return false on failure', async () => {
      mockSendMail.mockRejectedValue(new Error('SMTP error'));

      const result = await service.sendEmail({
        to: 'user@test.com',
        subject: 'Test',
        body: 'Hello',
      });

      expect(result).toBe(false);
    });
  });

  describe('sendBulkEmails', () => {
    it('should track sent and failed counts', async () => {
      mockSendMail
        .mockResolvedValueOnce({ messageId: '1' })
        .mockRejectedValueOnce(new Error('Failed'))
        .mockResolvedValueOnce({ messageId: '3' });

      const result = await service.sendBulkEmails([
        { to: 'a@test.com', subject: 'A', body: 'A' },
        { to: 'b@test.com', subject: 'B', body: 'B' },
        { to: 'c@test.com', subject: 'C', body: 'C' },
      ]);

      expect(result).toEqual({ sent: 2, failed: 1 });
    });
  });
});
```

---

## 4. Snapshot Testing

```typescript
// Component snapshot test (React)
import { render } from '@testing-library/react';
import { UserProfile } from '../components/UserProfile';

const mockUser = {
  id: '1',
  name: 'Alice',
  email: 'alice@test.com',
  role: 'admin',
  createdAt: new Date('2024-01-01'),
};

describe('UserProfile', () => {
  it('should render correctly', () => {
    const { container } = render(<UserProfile user={mockUser} />);
    expect(container).toMatchSnapshot();
  });

  it('should render admin badge for admin users', () => {
    const { container } = render(<UserProfile user={mockUser} />);
    expect(container.querySelector('.admin-badge')).toMatchSnapshot();
  });
});

// Object snapshot test
describe('User serialization', () => {
  it('should serialize user correctly', () => {
    const serialized = serializeUser(mockUser);
    expect(serialized).toMatchSnapshot();
  });
});

// Inline snapshot
it('should format user for display', () => {
  const result = formatUser(mockUser);
  expect(result).toMatchInlineSnapshot(`
    "Alice (alice@test.com) - Admin"
  `);
});
```

---

## 5. Table-Driven Tests

```typescript
// Table-driven tests with types
interface TestCase {
  input: string;
  expected: string;
  description: string;
}

const capitalizeTestCases: TestCase[] = [
  { input: 'hello', expected: 'Hello', description: 'lowercase word' },
  { input: 'WORLD', expected: 'WORLD', description: 'uppercase word' },
  { input: '', expected: '', description: 'empty string' },
  { input: 'a', expected: 'A', description: 'single character' },
  { input: 'hello world', expected: 'Hello world', description: 'sentence with space' },
];

describe('capitalize', () => {
  it.each(capitalizeTestCases)('$description: "$input" → "$expected"', ({ input, expected }) => {
    expect(capitalize(input)).toBe(expected);
  });
});

// Numeric test cases
interface ArithmeticTestCase {
  a: number;
  b: number;
  expected: number;
}

describe('arithmetic operations', () => {
  describe.each([
    ['addition', (a: number, b: number) => a + b, [
      { a: 1, b: 1, expected: 2 },
      { a: -1, b: 1, expected: 0 },
      { a: 0, b: 0, expected: 0 },
    ] as ArithmeticTestCase[]],
    ['subtraction', (a: number, b: number) => a - b, [
      { a: 5, b: 3, expected: 2 },
      { a: 0, b: 5, expected: -5 },
    ] as ArithmeticTestCase[]],
    ['multiplication', (a: number, b: number) => a * b, [
      { a: 2, b: 3, expected: 6 },
      { a: -1, b: 5, expected: -5 },
    ] as ArithmeticTestCase[]],
  ])('%s', (_name, operation, cases) => {
    it.each(cases)('$a op $b = $expected', ({ a, b, expected }) => {
      expect(operation(a, b)).toBe(expected);
    });
  });
});
```

---

## 6. Test Organization Patterns

```typescript
// Describe block organization
describe('UserService', () => {
  // Setup shared across all tests
  let service: UserService;
  let prisma: MockPrismaClient;

  beforeEach(() => {
    prisma = createMockPrismaClient();
    service = new UserService(prisma);
  });

  // Group related tests
  describe('create', () => {
    describe('validation', () => {
      it('should reject empty name');
      it('should reject invalid email');
      it('should reject duplicate email');
    });

    describe('creation', () => {
      it('should create user with defaults');
      it('should hash password');
      it('should send welcome email');
    });

    describe('error handling', () => {
      it('should handle database errors');
      it('should handle email service errors');
    });
  });

  describe('update', () => {
    it('should update only provided fields');
    it('should not update password directly');
    it('should return updated user');
  });

  describe('delete', () => {
    it('should soft delete user');
    it('should clean up related resources');
  });
});

// Test naming conventions
describe('AuthMiddleware', () => {
  // Pattern: should [expected behavior] when [condition]
  it('should return 401 when no token is provided');
  it('should return 401 when token is expired');
  it('should return 403 when user lacks required role');
  it('should call next() when token is valid');
  it('should attach user to request when authenticated');
});
```

---

## 7. Best Practices

1. **Follow AAA pattern** — Arrange, Act, Assert.
2. **One assertion per concept** — each test should verify one behavior.
3. **Use `describe` blocks** to group related tests logically.
4. **Name tests descriptively** — "should [behavior] when [condition]".
5. **Use `beforeEach`** for common setup, not `beforeAll`.
6. **Mock external dependencies** — databases, APIs, file system.
7. **Use table-driven tests** for multiple input/output scenarios.
8. **Test edge cases** — empty inputs, boundaries, error conditions.
9. **Keep tests independent** — no test should depend on another.
10. **Use `it.each`** instead of writing similar tests repeatedly.

---

## Interview Questions

1. What is the AAA pattern in unit testing?
2. How do you test error-throwing functions?
3. What are table-driven tests and when should you use them?
4. How do you test class methods with dependencies?
5. When should you use snapshot testing?
6. How do you organize test files for a large codebase?
7. What is the difference between `beforeEach` and `beforeAll`?
8. How do you test async functions that can throw?
9. How do you mock modules in Jest?
10. What makes a good unit test?
