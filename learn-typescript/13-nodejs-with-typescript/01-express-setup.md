# Express with TypeScript

## Overview

Express is the most popular Node.js web framework. TypeScript adds type safety to request/response handling, middleware, routing, and error handling.

---

## 1. Express + TypeScript Setup

```bash
# Install dependencies
npm install express
npm install -D typescript @types/express @types/node ts-node

# Initialize tsconfig
npx tsc --init
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

```typescript
// src/index.ts
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.json({ message: 'Hello, TypeScript!' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

---

## 2. Typing Request and Response

```typescript
import { Request, Response } from 'express';

// Basic typed handler
app.get('/users', (req: Request, res: Response) => {
  res.json({ users: [] });
});

// Typed route params
interface UserIdParams {
  id: string;
}

app.get('/users/:id', (req: Request<UserIdParams>, res: Response) => {
  const { id } = req.params; // id is string
  res.json({ userId: id });
});

// Typed query strings
interface SearchQuery {
  q?: string;
  page?: string;
  limit?: string;
  sort?: 'asc' | 'desc';
}

app.get('/search', (req: Request<{}, {}, {}, SearchQuery>, res: Response) => {
  const { q, page = '1', limit = '10', sort = 'desc' } = req.query;
  // q, page, limit are string | undefined
  // sort is 'asc' | 'desc' | undefined
  res.json({ query: q, page, limit, sort });
});

// Typed request body
interface CreateUserBody {
  name: string;
  email: string;
  age?: number;
}

app.post('/users', (req: Request<{}, {}, CreateUserBody>, res: Response) => {
  const { name, email, age } = req.body; // Fully typed
  res.status(201).json({ id: '1', name, email, age });
});

// Typed response
interface UserResponse {
  id: string;
  name: string;
  email: string;
}

app.get('/users/:id', (req: Request<UserIdParams>, res: Response<UserResponse>) => {
  res.json({ id: '1', name: 'Alice', email: 'alice@example.com' });
});
```

---

## 3. RequestHandler Type

```typescript
import { RequestHandler } from 'express';

// Using RequestHandler for reusable handlers
interface GetUserParams { id: string }
interface GetUserQuery { fields?: string }

const getUserHandler: RequestHandler<GetUserParams, any, any, GetUserQuery> = (req, res) => {
  const { id } = req.params;
  const { fields } = req.query;
  res.json({ id, fields });
};

app.get('/users/:id', getUserHandler);

// RequestHandler with body
interface LoginBody {
  email: string;
  password: string;
}

interface LoginResponse {
  token: string;
  user: { id: string; name: string };
}

interface LoginError {
  error: string;
  code: string;
}

const loginHandler: RequestHandler<{}, LoginResponse | LoginError, LoginBody> = async (req, res) => {
  const { email, password } = req.body;

  try {
    const result = await authenticate(email, password);
    res.json(result);
  } catch (err) {
    res.status(401).json({ error: 'Invalid credentials', code: 'AUTH_FAILED' });
  }
};

app.post('/login', loginHandler);
```

---

## 4. Typed Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

// Basic typed middleware
function logger(req: Request, res: Response, next: NextFunction): void {
  console.log(`${req.method} ${req.path}`);
  next();
}

// Middleware with options
interface RateLimitOptions {
  windowMs: number;
  max: number;
}

function rateLimit(options: RateLimitOptions) {
  const clients = new Map<string, { count: number; resetTime: number }>();

  return (req: Request, res: Response, next: NextFunction): void => {
    const ip = req.ip || req.socket.remoteAddress || 'unknown';
    const now = Date.now();
    const client = clients.get(ip);

    if (!client || now > client.resetTime) {
      clients.set(ip, { count: 1, resetTime: now + options.windowMs });
      next();
      return;
    }

    if (client.count >= options.max) {
      res.status(429).json({ error: 'Too many requests' });
      return;
    }

    client.count++;
    next();
  };
}

// Augment Express Request
declare global {
  namespace Express {
    interface Request {
      userId?: string;
      userRole?: string;
    }
  }
}

// Auth middleware
function authenticate(req: Request, res: Response, next: NextFunction): void {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    res.status(401).json({ error: 'No token provided' });
    return;
  }

  try {
    const payload = verifyToken(token);
    req.userId = payload.userId;
    req.userRole = payload.role;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// Role-based middleware
function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.userRole || !roles.includes(req.userRole)) {
      res.status(403).json({ error: 'Insufficient permissions' });
      return;
    }
    next();
  };
}

// Usage
app.get('/admin', authenticate, requireRole('admin'), (req, res) => {
  res.json({ message: `Hello, admin ${req.userId}` });
});
```

---

## 5. Typed Router

```typescript
import { Router, Request, Response } from 'express';

// Create typed router
const userRouter = Router();

// Define types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface CreateUserBody {
  name: string;
  email: string;
  role?: 'admin' | 'user';
}

interface UpdateUserBody {
  name?: string;
  email?: string;
}

interface UserParams {
  id: string;
}

// Routes
userRouter.get('/', (req: Request, res: Response<User[]>) => {
  res.json([]);
});

userRouter.post('/', (req: Request<{}, {}, CreateUserBody>, res: Response) => {
  const user: User = {
    id: '1',
    name: req.body.name,
    email: req.body.email,
    role: req.body.role || 'user',
  };
  res.status(201).json(user);
});

userRouter.get('/:id', (req: Request<UserParams>, res: Response<User>) => {
  res.json({ id: req.params.id, name: 'Alice', email: 'alice@test.com', role: 'user' });
});

userRouter.put('/:id', (req: Request<UserParams, {}, UpdateUserBody>, res: Response) => {
  res.json({ id: req.params.id, ...req.body });
});

userRouter.delete('/:id', (req: Request<UserParams>, res: Response) => {
  res.status(204).send();
});

// Mount router
app.use('/api/users', userRouter);
```

---

## 6. Typed Error Middleware

```typescript
import { Request, Response, NextFunction, ErrorRequestHandler } from 'express';

// Custom error class
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Typed error response
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    stack?: string;
  };
}

// Error handling middleware
const errorHandler: ErrorRequestHandler = (
  err: Error | AppError,
  req: Request,
  res: Response<ErrorResponse>,
  next: NextFunction
): void => {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
    });
    return;
  }

  console.error('Unhandled error:', err);
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : err.message,
    },
  });
};

// 404 handler
function notFoundHandler(req: Request, res: Response, next: NextFunction): void {
  const error = new AppError(404, 'NOT_FOUND', `Route ${req.method} ${req.path} not found`);
  next(error);
}

// Usage
app.use(notFoundHandler);
app.use(errorHandler);

// Throwing typed errors in handlers
app.get('/users/:id', async (req: Request, res: Response) => {
  const user = await findUser(req.params.id);
  if (!user) {
    throw new AppError(404, 'USER_NOT_FOUND', `User ${req.params.id} not found`);
  }
  res.json(user);
});

// Async error wrapper
function asyncHandler(fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) {
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
}

app.get('/users', asyncHandler(async (req, res) => {
  const users = await getAllUsers();
  res.json(users);
}));
```

---

## 7. Typed Route Params

```typescript
import { Router, Request, Response } from 'express';

// Complex route with params, body, query
interface RouteTypes {
  '/api/users/:userId/posts/:postId': {
    params: { userId: string; postId: string };
    body: { title: string; content: string };
    query: { draft?: string };
  };
}

// Helper to extract types
type ExtractParams<T extends string> =
  T extends `${infer _}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<Rest>]: string }
    : T extends `${infer _}:${infer Param}`
    ? { [K in Param]: string }
    : {};

// Usage
type PostParams = ExtractParams<'/api/users/:userId/posts/:postId'>;
// { userId: string; postId: string }

const postRouter = Router();

postRouter.post('/:userId/posts/:postId', (
  req: Request<{ userId: string; postId: string }, {}, { title: string; content: string }, { draft?: string }>,
  res: Response
) => {
  const { userId, postId } = req.params;
  const { title, content } = req.body;
  const { draft } = req.query;
  res.json({ userId, postId, title, content, draft });
});
```

---

## 8. Best Practices

1. **Always type `req` and `res`** — never use `any` for Express handlers.
2. **Use `RequestHandler` type** for reusable handler functions.
3. **Create custom error classes** with status codes and error codes.
4. **Use `asyncHandler` wrapper** to catch async errors automatically.
5. **Type middleware with `NextFunction`** — always call `next()` or send a response.
6. **Define route types centrally** for consistency.
7. **Augment Express Request** for custom properties like `userId`.
8. **Use `ErrorRequestHandler`** for error middleware (4 params).
9. **Type route params, body, and query** as separate generic parameters.
10. **Use `express-serve-static-core`** types for advanced typing.

---

## Interview Questions

1. How do you type Express route params, body, and query?
2. What is `RequestHandler` and when should you use it?
3. How do you type Express middleware?
4. How do you create typed error handling in Express?
5. What is the `asyncHandler` pattern and why is it needed?
6. How do you augment Express Request with custom properties?
7. How do you type a Router with multiple routes?
8. What is the difference between `Request` and `RequestHandler`?
9. How do you handle typed file uploads in Express?
10. How do you type WebSocket connections with Express?
