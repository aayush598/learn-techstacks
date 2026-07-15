# Integration Testing in TypeScript

## Overview

Integration testing verifies that multiple components work together correctly. This guide covers testing API endpoints, databases, external services, and test containers.

---

## 1. Integration Testing Setup

```typescript
// tests/integration/setup.ts
import { PrismaClient } from '@prisma/client';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

let prisma: PrismaClient;

beforeAll(async () => {
  // Run migrations on test database
  process.env.DATABASE_URL = 'postgresql://test:test@localhost:5433/test_db';
  await execAsync('npx prisma migrate deploy');

  prisma = new PrismaClient();
});

afterAll(async () => {
  await prisma.$disconnect();
});

afterEach(async () => {
  // Clean database after each test
  await prisma.comment.deleteMany();
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();
});

export { prisma };
```

---

## 2. Testing API Endpoints

```typescript
import request from 'supertest';
import express from 'express';
import { createApp } from '../../src/app';

describe('User API', () => {
  let app: express.Application;

  beforeAll(async () => {
    app = await createApp();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'Alice',
          email: 'alice@test.com',
          password: 'SecurePass123',
          age: 30,
        })
        .expect(201);

      expect(response.body).toMatchObject({
        name: 'Alice',
        email: 'alice@test.com',
        role: 'user',
      });
      expect(response.body.id).toBeDefined();
      expect(response.body.password).toBeUndefined(); // Password not returned
    });

    it('should return 400 for invalid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: '',
          email: 'invalid-email',
          age: 5,
        })
        .expect(400);

      expect(response.body.error).toBe('Validation failed');
      expect(response.body.details).toBeDefined();
    });

    it('should return 409 for duplicate email', async () => {
      // Create first user
      await request(app)
        .post('/api/users')
        .send({
          name: 'Alice',
          email: 'alice@test.com',
          password: 'SecurePass123',
        });

      // Try to create with same email
      await request(app)
        .post('/api/users')
        .send({
          name: 'Bob',
          email: 'alice@test.com',
          password: 'SecurePass123',
        })
        .expect(409);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by id', async () => {
      // Create user first
      const createResponse = await request(app)
        .post('/api/users')
        .send({
          name: 'Alice',
          email: 'alice@test.com',
          password: 'SecurePass123',
        });

      const userId = createResponse.body.id;

      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body.name).toBe('Alice');
      expect(response.body.email).toBe('alice@test.com');
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/nonexistent')
        .expect(404);
    });
  });

  describe('GET /api/users', () => {
    it('should return paginated users', async () => {
      // Create multiple users
      for (let i = 0; i < 15; i++) {
        await request(app)
          .post('/api/users')
          .send({
            name: `User ${i}`,
            email: `user${i}@test.com`,
            password: 'SecurePass123',
          });
      }

      // Get first page
      const page1 = await request(app)
        .get('/api/users?page=1&limit=10')
        .expect(200);

      expect(page1.body.data).toHaveLength(10);
      expect(page1.body.pagination.total).toBe(15);
      expect(page1.body.pagination.pages).toBe(2);

      // Get second page
      const page2 = await request(app)
        .get('/api/users?page=2&limit=10')
        .expect(200);

      expect(page2.body.data).toHaveLength(5);
    });

    it('should filter users by role', async () => {
      await request(app)
        .post('/api/users')
        .send({ name: 'Admin', email: 'admin@test.com', password: 'Pass', role: 'ADMIN' });

      await request(app)
        .post('/api/users')
        .send({ name: 'User', email: 'user@test.com', password: 'Pass', role: 'USER' });

      const response = await request(app)
        .get('/api/users?role=ADMIN')
        .expect(200);

      expect(response.body.data).toHaveLength(1);
      expect(response.body.data[0].role).toBe('ADMIN');
    });
  });
});
```

---

## 3. Testing with Authentication

```typescript
import request from 'supertest';
import express from 'express';

describe('Authenticated API', () => {
  let app: express.Application;
  let authToken: string;

  beforeAll(async () => {
    app = await createApp();

    // Create user and get token
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@test.com', password: 'SecurePass123' });

    authToken = response.body.token;
  });

  it('should access protected route with valid token', async () => {
    const response = await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(response.body.email).toBe('admin@test.com');
  });

  it('should reject request without token', async () => {
    await request(app)
      .get('/api/profile')
      .expect(401);
  });

  it('should reject request with invalid token', async () => {
    await request(app)
      .get('/api/profile')
      .set('Authorization', 'Bearer invalid-token')
      .expect(401);
  });

  it('should reject request with expired token', async () => {
    const expiredToken = generateExpiredToken();
    await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${expiredToken}`)
      .expect(401);
  });
});
```

---

## 4. Testing Databases

```typescript
import { PrismaClient } from '@prisma/client';

describe('User Repository', () => {
  let prisma: PrismaClient;

  beforeAll(async () => {
    prisma = new PrismaClient();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  beforeEach(async () => {
    await prisma.comment.deleteMany();
    await prisma.post.deleteMany();
    await prisma.user.deleteMany();
  });

  describe('create', () => {
    it('should create user with all fields', async () => {
      const user = await prisma.user.create({
        data: {
          name: 'Alice',
          email: 'alice@test.com',
          password: await hash('password'),
          role: 'ADMIN',
          age: 30,
          tags: ['developer', 'admin'],
        },
      });

      expect(user.id).toBeDefined();
      expect(user.name).toBe('Alice');
      expect(user.email).toBe('alice@test.com');
      expect(user.role).toBe('ADMIN');
      expect(user.tags).toEqual(['developer', 'admin']);
    });

    it('should enforce unique email constraint', async () => {
      await prisma.user.create({
        data: {
          name: 'Alice',
          email: 'alice@test.com',
          password: await hash('password'),
        },
      });

      await expect(
        prisma.user.create({
          data: {
            name: 'Bob',
            email: 'alice@test.com',
            password: await hash('password'),
          },
        })
      ).rejects.toThrow();
    });
  });

  describe('queries', () => {
    beforeEach(async () => {
      await prisma.user.createMany({
        data: [
          { name: 'Alice', email: 'alice@test.com', password: 'hash', role: 'ADMIN' },
          { name: 'Bob', email: 'bob@test.com', password: 'hash', role: 'USER' },
          { name: 'Charlie', email: 'charlie@test.com', password: 'hash', role: 'USER' },
        ],
      });
    });

    it('should find users by role', async () => {
      const admins = await prisma.user.findMany({
        where: { role: 'ADMIN' },
      });
      expect(admins).toHaveLength(1);
      expect(admins[0].name).toBe('Alice');
    });

    it('should search users by name', async () => {
      const users = await prisma.user.findMany({
        where: {
          name: { contains: 'li', mode: 'insensitive' },
        },
      });
      expect(users).toHaveLength(2); // Alice and Charlie
    });

    it('should count users', async () => {
      const count = await prisma.user.count();
      expect(count).toBe(3);
    });
  });

  describe('transactions', () => {
    it('should create post and user in transaction', async () => {
      const result = await prisma.$transaction(async (tx) => {
        const user = await tx.user.create({
          data: { name: 'Alice', email: 'alice@test.com', password: 'hash' },
        });

        const post = await tx.post.create({
          data: { title: 'Hello', authorId: user.id },
        });

        return { user, post };
      });

      expect(result.user.id).toBeDefined();
      expect(result.post.authorId).toBe(result.user.id);
    });

    it('should rollback on error', async () => {
      await expect(
        prisma.$transaction(async (tx) => {
          await tx.user.create({
            data: { name: 'Alice', email: 'alice@test.com', password: 'hash' },
          });
          throw new Error('Transaction failed');
        })
      ).rejects.toThrow('Transaction failed');

      const count = await prisma.user.count();
      expect(count).toBe(0);
    });
  });
});
```

---

## 5. Test Containers

```typescript
// tests/integration/with-containers.ts
import { GenericContainer, StartedTestContainer } from 'testcontainers';

let postgresContainer: StartedTestContainer;
let redisContainer: StartedTestContainer;

beforeAll(async () => {
  postgresContainer = await new GenericContainer('postgres')
    .withEnv('POSTGRES_DB', 'test_db')
    .withEnv('POSTGRES_USER', 'test')
    .withEnv('POSTGRES_PASSWORD', 'test')
    .withExposedPorts(5432)
    .start();

  redisContainer = await new GenericContainer('redis')
    .withExposedPorts(6379)
    .start();

  process.env.DATABASE_URL = `postgresql://test:test@localhost:${postgresContainer.getMappedPort(5432)}/test_db`;
  process.env.REDIS_URL = `redis://localhost:${redisContainer.getMappedPort(6379)}`;
});

afterAll(async () => {
  await postgresContainer?.stop();
  await redisContainer?.stop();
});
```

---

## 6. Typed Test Fixtures

```typescript
// tests/fixtures/user.fixture.ts
import { PrismaClient, User } from '@prisma/client';

interface TestUser {
  name: string;
  email: string;
  role: 'ADMIN' | 'USER' | 'GUEST';
  age?: number;
}

const defaultUser: TestUser = {
  name: 'Test User',
  email: `test-${Date.now()}@example.com`,
  role: 'USER',
};

export class UserFixture {
  constructor(private prisma: PrismaClient) {}

  async create(overrides?: Partial<TestUser>): Promise<User> {
    const data = { ...defaultUser, ...overrides, email: overrides?.email || `test-${Date.now()}@example.com` };
    return this.prisma.user.create({
      data: { ...data, password: 'hashed_password' },
    });
  }

  async createMany(count: number): Promise<User[]> {
    return Promise.all(
      Array.from({ length: count }, (_, i) =>
        this.create({ name: `User ${i}`, email: `user${i}-${Date.now()}@test.com` })
      )
    );
  }

  async createAdmin(): Promise<User> {
    return this.create({ role: 'ADMIN', name: 'Admin User' });
  }
}

// Usage in tests
describe('User API', () => {
  let fixture: UserFixture;

  beforeEach(async () => {
    fixture = new UserFixture(prisma);
    await prisma.user.deleteMany();
  });

  it('should list users', async () => {
    await fixture.createMany(5);
    const response = await request(app).get('/api/users');
    expect(response.body.data).toHaveLength(5);
  });
});
```

---

## 7. Best Practices

1. **Use a separate test database** — never test against production.
2. **Clean up after each test** — restore database to known state.
3. **Use test containers** for database and service dependencies.
4. **Create test fixtures** for consistent test data.
5. **Test the full request/response cycle** — HTTP status, headers, body.
6. **Test authentication and authorization** separately.
7. **Use `supertest`** for Express API testing.
8. **Test error scenarios** — invalid input, not found, unauthorized.
9. **Keep integration tests independent** — no test should depend on another.
10. **Use `beforeEach`** for database cleanup, not `afterEach`.

---

## Interview Questions

1. What is the difference between unit and integration testing?
2. How do you set up a test database for integration tests?
3. How do you test API endpoints with authentication?
4. What are test containers and when should you use them?
5. How do you create reusable test fixtures?
6. How do you test database transactions?
7. How do you clean up test data between tests?
8. How do you test error handling in API endpoints?
9. What is the `supertest` library and how do you use it?
10. How do you test WebSocket connections in integration tests?
