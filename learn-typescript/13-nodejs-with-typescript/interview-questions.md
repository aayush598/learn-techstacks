# Node.js + TypeScript Interview Questions

## 25+ Questions with Detailed Answers

---

### 1. How do you set up Express with TypeScript?

**Answer:**

```bash
npm install express
npm install -D typescript @types/express @types/node
npx tsc --init
```

Key points:
- Use `@types/express` for Express type definitions.
- Set `esModuleInterop: true` in tsconfig for default imports.
- Use `ts-node` for development execution.
- Target Node.js-compatible JS version (ES2020+).

---

### 2. How do you type Express route handlers?

**Answer:**

```typescript
import { Request, Response } from 'express';

// Params, ResBody, ReqBody, ReqQuery
app.get('/users/:id', (req: Request<{ id: string }, UserResponse>, res) => {
  const { id } = req.params; // string
  res.json({ id, name: 'Alice' });
});

// With body
app.post('/users', (req: Request<{}, UserResponse, CreateUserBody>, res) => {
  const { name, email } = req.body; // typed
  res.status(201).json(user);
});

// With query
app.get('/search', (req: Request<{}, {}, {}, SearchQuery>, res) => {
  const { q, page } = req.query; // typed
});
```

---

### 3. How do you type Express middleware?

**Answer:**

```typescript
import { Request, Response, NextFunction } from 'express';

// Basic middleware
function logger(req: Request, res: Response, next: NextFunction): void {
  console.log(`${req.method} ${req.path}`);
  next();
}

// Error middleware (4 params)
const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  res.status(500).json({ error: err.message });
};

// Middleware factory with options
function rateLimit(options: { max: number; windowMs: number }) {
  return (req: Request, res: Response, next: NextFunction): void => {
    // Implementation
    next();
  };
}
```

---

### 4. How do you handle async errors in Express?

**Answer:**

```typescript
// Wrapper function
function asyncHandler(fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
app.get('/users', asyncHandler(async (req, res) => {
  const users = await UserService.findAll();
  res.json(users);
}));

// In Express 5, async errors are caught automatically
```

---

### 5. How do you type a Mongoose model?

**Answer:**

```typescript
import { Document, Model, Schema, model } from 'mongoose';

interface IUser {
  name: string;
  email: string;
}

interface IUserDocument extends IUser, Document {
  fullName(): string;
}

interface IUserModel extends Model<IUserDocument> {
  findByEmail(email: string): Promise<IUserDocument | null>;
}

const schema = new Schema<IUserDocument, IUserModel>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
});

schema.methods.fullName = function() { return this.name; };
schema.statics.findByEmail = function(email) { return this.findOne({ email }); };

const User = model<IUserDocument, IUserModel>('User', schema);
```

---

### 6. What are the benefits of Prisma over Mongoose for TypeScript?

**Answer:**

1. **Auto-generated types** — Prisma generates TypeScript types from schema.
2. **Type-safe queries** — every query is type-checked at compile time.
3. **Auto-complete** — IDE provides full auto-complete for all operations.
4. **Relation types** — types reflect populated relations.
5. **Migration system** — database migrations are type-safe.
6. **No manual type definitions** — eliminates interface duplication.

---

### 7. How do you type GraphQL resolvers?

**Answer:**

```typescript
// With TypeGraphQL
@Resolver()
class UserResolver {
  @Query(() => [User])
  async users(): Promise<User[]> {
    return UserService.findAll();
  }

  @Mutation(() => User)
  async createUser(@Arg('data') data: CreateUserInput): Promise<User> {
    return UserService.create(data);
  }
}

// With plain resolvers
interface Resolvers {
  Query: {
    users: (parent: any, args: {}, context: Context) => Promise<User[]>;
    user: (parent: any, args: { id: string }, context: Context) => Promise<User | null>;
  };
}
```

---

### 8. How do you type Socket.io events?

**Answer:**

```typescript
interface ServerToClientEvents {
  'message:received': (message: ChatMessage) => void;
  'user:joined': (data: { userId: string }) => void;
}

interface ClientToServerEvents {
  'message:send': (data: { content: string; room: string }) => void;
}

// Server
const io = new Server<ClientToServerEvents, ServerToClientEvents>(httpServer);

// Client
const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(url);
```

---

### 9. How do you augment Express Request for custom properties?

**Answer:**

```typescript
declare global {
  namespace Express {
    interface Request {
      userId?: string;
      userRole?: string;
    }
  }
}

// Middleware sets properties
function auth(req: Request, res: Response, next: NextFunction) {
  req.userId = '123';
  req.userRole = 'admin';
  next();
}

// Handler reads properties
app.get('/profile', (req, res) => {
  console.log(req.userId); // string | undefined
});
```

---

### 10. How do you create a type-safe API response?

**Answer:**

```typescript
interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: { page: number; total: number };
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

// Usage
app.get('/users', (req, res) => {
  res.json({
    success: true,
    data: users,
    meta: { page: 1, total: 100 },
  } satisfies ApiResponse<User[]>);
});
```

---

### 11. How do you validate request bodies with Zod?

**Answer:**

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().min(13),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.format() });
    }
    req.body = result.data;
    next();
  };
}

app.post('/users', validate(CreateUserSchema), handler);
```

---

### 12. How do you type a middleware that adds properties to req?

**Answer:**

```typescript
// Augment Express namespace
declare global {
  namespace Express {
    interface Request {
      currentUser?: {
        id: string;
        email: string;
        role: string;
      };
    }
  }
}

// Typed middleware
function authenticate(req: Request, res: Response, next: NextFunction): void {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    res.status(401).json({ error: 'No token' });
    return;
  }

  const payload = verifyToken(token);
  req.currentUser = {
    id: payload.userId,
    email: payload.email,
    role: payload.role,
  };
  next();
}

// Usage — req.currentUser is typed
app.get('/profile', authenticate, (req, res) => {
  res.json(req.currentUser); // { id: string; email: string; role: string } | undefined
});
```

---

### 13. How do you handle file uploads with types?

**Answer:**

```typescript
import multer from 'multer';

// Type the file object
interface TypedRequest extends Request {
  file?: Express.Multer.File;
  files?: Express.Multer.File[];
}

const upload = multer({ dest: 'uploads/' });

// Single file upload
app.post('/upload', upload.single('file'), (req: TypedRequest, res) => {
  if (req.file) {
    console.log(req.file.filename);  // string
    console.log(req.file.mimetype);  // string
    console.log(req.file.size);      // number
  }
});

// Multiple file upload
app.post('/uploads', upload.array('files', 5), (req: TypedRequest, res) => {
  if (req.files) {
    req.files.forEach((file) => console.log(file.originalname));
  }
});
```

---

### 14. How do you type environment variables?

**Answer:**

```typescript
// src/types/env.d.ts
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
    PORT: string;
    DATABASE_URL: string;
    JWT_SECRET: string;
    REDIS_URL?: string;
    LOG_LEVEL?: string;
  }
}

// Usage — fully typed
const port = parseInt(process.env.PORT, 10); // number
const dbUrl = process.env.DATABASE_URL;      // string
const redisUrl = process.env.REDIS_URL;      // string | undefined

// Runtime validation
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().default('3000'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
});

const env = envSchema.parse(process.env);
```

---

### 15. How do you type a service layer?

**Answer:**

```typescript
// Interface
interface IUserService {
  findAll(params: FindParams): Promise<PaginatedResult<User>>;
  findById(id: string): Promise<User | null>;
  create(data: CreateUserInput): Promise<User>;
  update(id: string, data: UpdateUserInput): Promise<User>;
  delete(id: string): Promise<boolean>;
}

// Implementation
class UserService implements IUserService {
  constructor(private prisma: PrismaClient) {}

  async findAll(params: FindParams): Promise<PaginatedResult<User>> {
    const { page = 1, limit = 10, where = {} } = params;
    const [data, total] = await Promise.all([
      this.prisma.user.findMany({ where, skip: (page - 1) * limit, take: limit }),
      this.prisma.user.count({ where }),
    ]);
    return { data, total, page, pages: Math.ceil(total / limit) };
  }

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async create(data: CreateUserInput): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserInput): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }

  async delete(id: string): Promise<boolean> {
    await this.prisma.user.delete({ where: { id } });
    return true;
  }
}
```

---

### 16. How do you type Express error classes?

**Answer:**

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public isOperational = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public fields: Record<string, string[]>) {
    super(400, 'VALIDATION_ERROR', message);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(401, 'UNAUTHORIZED', message);
  }
}
```

---

### 17. How do you create typed Express router?

**Answer:**

```typescript
import { Router } from 'express';

interface UserRoutes {
  'GET /': { response: User[] };
  'POST /': { body: CreateUserInput; response: User };
  'GET /:id': { params: { id: string }; response: User };
  'PUT /:id': { params: { id: string }; body: UpdateUserInput; response: User };
  'DELETE /:id': { params: { id: string }; response: void };
}

const userRouter = Router();

userRouter.get('/', async (req, res) => {
  const users = await UserService.findAll();
  res.json(users);
});

userRouter.post('/', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201).json(user);
});

export default userRouter;
```

---

### 18. How do you handle CORS with typed options?

**Answer:**

```typescript
import cors from 'cors';

interface CorsOptions {
  origin: string | string[] | ((origin: string, callback: (err: Error | null, allow?: boolean) => void) => void);
  methods?: string[];
  allowedHeaders?: string[];
  credentials?: boolean;
  maxAge?: number;
}

const corsOptions: CorsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = ['http://localhost:3000', 'https://example.com'];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
  maxAge: 86400,
};

app.use(cors(corsOptions));
```

---

### 19. How do you type a dependency injection container?

**Answer:**

```typescript
// Simple DI container
interface Container {
  UserService: UserService;
  PostService: PostService;
  AuthService: AuthService;
}

function createContainer(): Container {
  const prisma = new PrismaClient();

  return {
    UserService: new UserService(prisma),
    PostService: new PostService(prisma),
    AuthService: new AuthService(prisma),
  };
}

// Typed injection
function inject<K extends keyof Container>(key: K): Container[K] {
  const container = createContainer();
  return container[key];
}

// Usage
const userService = inject('UserService'); // UserService type
const users = await userService.findAll();
```

---

### 20. How do you type a middleware chain?

**Answer:**

```typescript
// Compose multiple typed middlewares
type Middleware = (req: Request, res: Response, next: NextFunction) => void;

function compose(...middlewares: Middleware[]): Middleware {
  return (req, res, next) => {
    let index = 0;
    const run = () => {
      if (index < middlewares.length) {
        middlewares[index++](req, res, run);
      } else {
        next();
      }
    };
    run();
  };
}

// Usage
const authMiddleware = compose(
  authenticate,
  requireRole('admin'),
  validateRequest(schema)
);
```

---

### 21. How do you handle graceful shutdown with TypeScript?

**Answer:**

```typescript
import { Server } from 'http';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

function gracefulShutdown(server: Server): void {
  const shutdown = async (signal: string) => {
    console.log(`${signal} received. Starting graceful shutdown...`);

    server.close(async () => {
      console.log('HTTP server closed');
      await prisma.$disconnect();
      console.log('Database disconnected');
      process.exit(0);
    });

    // Force close after 30s
    setTimeout(() => {
      console.error('Forced shutdown');
      process.exit(1);
    }, 30000);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
}
```

---

### 22. How do you type a background job queue?

**Answer: 

```typescript
import Bull from 'bull';

// Job data types
interface EmailJobData {
  to: string;
  subject: string;
  body: string;
  template: 'welcome' | 'reset-password' | 'notification';
}

interface ImageJobData {
  imageUrl: string;
  userId: string;
  operations: ('resize' | 'compress' | 'watermark')[];
}

// Typed queues
const emailQueue = new Bull<EmailJobData>('email', 'redis://localhost:6379');
const imageQueue = new Bull<ImageJobData>('image', 'redis://localhost:6379');

// Typed processor
emailQueue.process(async (job: Bull.Job<EmailJobData>) => {
  const { to, subject, body, template } = job.data; // Fully typed
  await sendEmail(to, subject, body, template);
  return { sent: true };
});

// Typed event listeners
emailQueue.on('completed', (job: Bull.Job<EmailJobData>, result) => {
  console.log(`Email sent to ${job.data.to}`);
});
```

---

### 23. How do you type a caching layer?

**Answer:**

```typescript
interface CacheOptions {
  ttl: number; // seconds
  prefix: string;
}

class TypedCache<T> {
  private store = new Map<string, { data: T; expiry: number }>();

  constructor(private options: CacheOptions) {}

  async get(key: string): Promise<T | null> {
    const fullKey = `${this.options.prefix}:${key}`;
    const item = this.store.get(fullKey);
    if (!item || Date.now() > item.expiry) {
      this.store.delete(fullKey);
      return null;
    }
    return item.data;
  }

  async set(key: string, data: T): Promise<void> {
    const fullKey = `${this.options.prefix}:${key}`;
    this.store.set(fullKey, {
      data,
      expiry: Date.now() + this.options.ttl * 1000,
    });
  }

  async invalidate(key: string): Promise<void> {
    this.store.delete(`${this.options.prefix}:${key}`);
  }
}

// Usage
const userCache = new TypedCache<User>({ ttl: 300, prefix: 'user' });
const cached = await userCache.get('123'); // User | null
```

---

### 24. How do you type a WebSocket server?

**Answer:**

```typescript
import WebSocket, { WebSocketServer } from 'ws';

interface WSMessage {
  type: 'auth' | 'message' | 'join' | 'leave';
  payload: any;
}

interface AuthPayload {
  token: string;
}

interface MessagePayload {
  content: string;
  room: string;
}

function handleMessage(ws: WebSocket, message: WSMessage): void {
  switch (message.type) {
    case 'auth':
      const authData = message.payload as AuthPayload;
      // Handle auth
      break;
    case 'message':
      const msgData = message.payload as MessagePayload;
      // Handle message
      break;
  }
}
```

---

### 25. How do you type a test helper?

**Answer:**

```typescript
// Typed test helper
interface TestUser {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

async function createTestUser(overrides?: Partial<TestUser>): Promise<TestUser> {
  const defaults: TestUser = {
    id: crypto.randomUUID(),
    name: 'Test User',
    email: `test-${Date.now()}@example.com`,
    role: 'user',
  };

  const user = { ...defaults, ...overrides };
  await prisma.user.create({ data: user });
  return user;
}

// Typed test fixtures
interface TestFixtures {
  users: TestUser[];
  posts: TestPost[];
}

async function createFixtures(): Promise<TestFixtures> {
  const users = await Promise.all([
    createTestUser({ role: 'admin' }),
    createTestUser({ role: 'user' }),
  ]);

  return { users, posts: [] };
}
```

---

### 26. How do you handle TypeScript with child processes?

**Answer:**

```typescript
import { fork, ForkOptions } from 'child_process';

interface WorkerMessage {
  type: 'task';
  data: { jobId: string; payload: any };
}

interface WorkerResponse {
  type: 'result';
  data: { jobId: string; result: any; error?: string };
}

function spawnWorker(scriptPath: string): ChildProcess {
  const child = fork(scriptPath);

  child.on('message', (message: WorkerResponse) => {
    if (message.type === 'result') {
      console.log(`Job ${message.data.jobId} completed`);
    }
  });

  return child;
}

// Send typed message
function sendJob(worker: ChildProcess, jobId: string, payload: any): void {
  const message: WorkerMessage = {
    type: 'task',
    data: { jobId, payload },
  };
  worker.send(message);
}
```

---

### 27. How do you type a middleware that validates against a database?

**Answer:**

```typescript
import { Request, Response, NextFunction } from 'express';

function validateResourceExists<T>(
  model: { findUnique: (args: any) => Promise<T | null> },
  paramName: string,
  resourceField: string = paramName
) {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const id = req.params[paramName];
    const resource = await model.findUnique({ where: { id } });

    if (!resource) {
      res.status(404).json({
        error: `${resourceField} not found`,
      });
      return;
    }

    // Attach to request
    (req as any)[resourceField] = resource;
    next();
  };
}

// Usage
app.get('/posts/:id/comments',
  validateResourceExists(prisma.post, 'id', 'post'),
  async (req, res) => {
    const post = (req as any).post;
    const comments = await prisma.comment.findMany({
      where: { postId: post.id },
    });
    res.json(comments);
  }
);
```
