# Routes and Middleware with TypeScript

## Overview

This guide covers advanced patterns for typed route handlers, middleware chains, request validation, and error handling in Express with TypeScript.

---

## 1. Typed Route Handlers

```typescript
import { Router, Request, Response, NextFunction } from 'express';

// Generic route handler type
type TypedHandler<Params = {}, ResBody = any, ReqBody = any, ReqQuery = any> = (
  req: Request<Params, ResBody, ReqBody, ReqQuery>,
  res: Response<ResBody>,
  next: NextFunction
) => void | Promise<void>;

// Product routes with full typing
interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

interface ProductParams {
  id: string;
}

interface ProductQuery {
  category?: string;
  minPrice?: string;
  maxPrice?: string;
  sort?: 'price' | 'name';
  order?: 'asc' | 'desc';
  page?: string;
  limit?: string;
}

interface CreateProductBody {
  name: string;
  price: number;
  category: string;
  inStock?: boolean;
}

interface UpdateProductBody {
  name?: string;
  price?: number;
  category?: string;
  inStock?: boolean;
}

interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

const router = Router();

// GET /products — list with filtering and pagination
router.get('/', async (req: Request<{}, PaginatedResponse<Product>, {}, ProductQuery>, res) => {
  const {
    category,
    minPrice,
    maxPrice,
    sort = 'name',
    order = 'asc',
    page = '1',
    limit = '10',
  } = req.query;

  const pageNum = parseInt(page, 10);
  const limitNum = parseInt(limit, 10);

  // Build filter from typed query params
  const filter: Partial<Product> = {};
  if (category) filter.category = category;
  if (minPrice) filter.price = { $gte: parseFloat(minPrice) } as any;
  if (maxPrice) filter.price = { $lte: parseFloat(maxPrice) } as any;

  const products = await ProductModel.find(filter)
    .sort({ [sort]: order })
    .skip((pageNum - 1) * limitNum)
    .limit(limitNum);

  const total = await ProductModel.countDocuments(filter);

  res.json({
    data: products,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total,
      totalPages: Math.ceil(total / limitNum),
    },
  });
});

// POST /products — create
router.post('/', async (
  req: Request<{}, Product, CreateProductBody>,
  res: Response<Product>
) => {
  const product = await ProductModel.create({
    name: req.body.name,
    price: req.body.price,
    category: req.body.category,
    inStock: req.body.inStock ?? true,
  });
  res.status(201).json(product);
});

// PUT /products/:id — update
router.put('/:id', async (
  req: Request<ProductParams, Product, UpdateProductBody>,
  res: Response<Product>
) => {
  const product = await ProductModel.findByIdAndUpdate(
    req.params.id,
    { $set: req.body },
    { new: true }
  );
  if (!product) {
    res.status(404).json({ error: 'Product not found' } as any);
    return;
  }
  res.json(product);
});

// DELETE /products/:id
router.delete('/:id', async (
  req: Request<ProductParams>,
  res: Response<void>
) => {
  await ProductModel.findByIdAndDelete(req.params.id);
  res.status(204).send();
});
```

---

## 2. Request Validation with Zod

```typescript
import { z } from 'zod';
import { Request, Response, NextFunction } from 'express';

// Define schemas
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/, 'Must contain uppercase letter'),
  age: z.number().int().min(13).max(120),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
});

const UpdateUserSchema = CreateUserSchema.partial();

const UserQuerySchema = z.object({
  page: z.string().regex(/^\d+$/).transform(Number).default('1'),
  limit: z.string().regex(/^\d+$/).transform(Number).default('10'),
  search: z.string().optional(),
  role: z.enum(['admin', 'user', 'guest']).optional(),
});

// Inferred types from schemas
type CreateUserInput = z.infer<typeof CreateUserSchema>;
type UpdateUserInput = z.infer<typeof UpdateUserSchema>;
type UserQueryInput = z.infer<typeof UserQuerySchema>;

// Validation middleware factory
function validate(schema: z.ZodSchema<any>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });

    if (!result.success) {
      const formatted = result.error.format();
      res.status(400).json({
        error: 'Validation failed',
        details: formatted,
      });
      return;
    }

    // Replace with parsed/validated data
    req.body = result.data.body;
    req.query = result.data.query;
    req.params = result.data.params;
    next();
  };
}

// Body-only validation
function validateBody<T extends z.ZodSchema<any>>(schema: T) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      res.status(400).json({
        error: 'Invalid request body',
        details: result.error.format(),
      });
      return;
    }
    req.body = result.data;
    next();
  };
}

// Query-only validation
function validateQuery<T extends z.ZodSchema<any>>(schema: T) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.query);
    if (!result.success) {
      res.status(400).json({
        error: 'Invalid query parameters',
        details: result.error.format(),
      });
      return;
    }
    req.query = result.data;
    next();
  };
}

// Usage
router.post('/',
  validateBody(CreateUserSchema),
  async (req: Request<{}, {}, CreateUserInput>, res: Response) => {
    // req.body is fully typed and validated
    const user = await UserService.create(req.body);
    res.status(201).json(user);
  }
);

router.get('/',
  validateQuery(UserQuerySchema),
  async (req: Request<{}, {}, {}, UserQueryInput>, res: Response) => {
    const { page, limit, search, role } = req.query;
    const users = await UserService.findAll({ page, limit, search, role });
    res.json(users);
  }
);
```

---

## 3. Request Validation with Joi

```typescript
import Joi from 'joi';
import { Request, Response, NextFunction } from 'express';

// Schema definition
const createUserSchema = Joi.object({
  name: Joi.string().min(1).max(100).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  age: Joi.number().integer().min(13).max(120).required(),
});

// TypeScript types derived from Joi
interface CreateUserInput {
  name: string;
  email: string;
  password: string;
  age: number;
}

// Validation middleware
function validateJoi<T>(schema: Joi.ObjectSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error, value } = schema.validate(req.body, { abortEarly: false });

    if (error) {
      const errors = error.details.map((d) => ({
        field: d.path.join('.'),
        message: d.message,
      }));
      res.status(400).json({ error: 'Validation failed', details: errors });
      return;
    }

    req.body = value as T;
    next();
  };
}

// Usage
router.post('/', validateJoi<CreateUserInput>(createUserSchema), async (req, res) => {
  const user = await UserService.create(req.body as CreateUserInput);
  res.status(201).json(user);
});
```

---

## 4. Typed Error Handling Middleware

```typescript
import { Request, Response, NextFunction, ErrorRequestHandler } from 'express';

// Error types
interface ApiError {
  statusCode: number;
  code: string;
  message: string;
  details?: any;
  isOperational: boolean;
}

// Custom error class
class AppError extends Error implements ApiError {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: any,
    public isOperational = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

// Validation error
class ValidationError extends AppError {
  constructor(message: string, details: Record<string, string[]>) {
    super(400, 'VALIDATION_ERROR', message, details);
  }
}

// Not found error
class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(404, 'NOT_FOUND', `${resource}${id ? ` with id ${id}` : ''} not found`);
  }
}

// Conflict error
class ConflictError extends AppError {
  constructor(message: string) {
    super(409, 'CONFLICT', message);
  }
}

// Typed error response
interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

interface SuccessResponse<T> {
  success: true;
  data: T;
}

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

// Error handler
const errorHandler: ErrorRequestHandler = (
  err: Error | AppError,
  req: Request,
  res: Response<ErrorResponse>,
  next: NextFunction
): void => {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        ...(err.details && { details: err.details }),
      },
    });
    return;
  }

  console.error('Unexpected error:', err);
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
};

// Async handler wrapper with proper typing
function asyncHandler<P = {}, ResBody = any, ReqBody = any, ReqQuery = any>(
  fn: (
    req: Request<P, ResBody, ReqBody, ReqQuery>,
    res: Response<ResBody>,
    next: NextFunction
  ) => Promise<any>
) {
  return (
    req: Request<P, ResBody, ReqBody, ReqQuery>,
    res: Response<ResBody>,
    next: NextFunction
  ) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage with typed responses
interface UserResponse {
  id: string;
  name: string;
  email: string;
}

router.get('/:id', asyncHandler<{ id: string }, ApiResponse<UserResponse>>(
  async (req, res) => {
    const user = await UserService.findById(req.params.id);
    if (!user) throw new NotFoundError('User', req.params.id);
    res.json({ success: true, data: user });
  }
));

router.post('/', asyncHandler<{}, ApiResponse<UserResponse>, CreateUserInput>(
  async (req, res) => {
    const existing = await UserService.findByEmail(req.body.email);
    if (existing) throw new ConflictError('Email already registered');
    const user = await UserService.create(req.body);
    res.status(201).json({ success: true, data: user });
  }
));
```

---

## 5. Typed Router Mounting

```typescript
import { Router, Application } from 'express';

// Create typed routers
const authRouter = Router();
const userRouter = Router();
const productRouter = Router();
const adminRouter = Router();

// Mount with type safety
function setupRoutes(app: Application): void {
  app.use('/api/auth', authRouter);
  app.use('/api/users', userRouter);
  app.use('/api/products', productRouter);
  app.use('/api/admin', adminRouter);
}

// Route prefix types
type ApiRoutes = '/api/auth' | '/api/users' | '/api/products' | '/api/admin';

// Type-safe route builder
class TypedRouter {
  private router: Router;

  constructor(private prefix: string) {
    this.router = Router();
  }

  get<Params = {}, ResBody = any, ReqBody = any, ReqQuery = {}>(
    path: string,
    handler: (req: any, res: any, next: any) => void | Promise<void>
  ): this {
    this.router.get(path, handler);
    return this;
  }

  post<Params = {}, ResBody = any, ReqBody = any, ReqQuery = {}>(
    path: string,
    handler: (req: any, res: any, next: any) => void | Promise<void>
  ): this {
    this.router.post(path, handler);
    return this;
  }

  build(): Router {
    return this.router;
  }
}
```

---

## 6. Best Practices

1. **Use Zod for request validation** — it infers TypeScript types from schemas.
2. **Always type middleware** — never use `any` for `req`, `res`, `next`.
3. **Create reusable validation middleware** — `validateBody`, `validateQuery`.
4. **Use `asyncHandler`** to catch async errors automatically.
5. **Type error responses** with a consistent interface.
6. **Use discriminated unions** for API responses (success/error).
7. **Create custom error classes** for different error types.
8. **Type route params explicitly** — don't rely on implicit `any`.
9. **Use `ErrorRequestHandler`** (4 params) for error middleware.
10. **Keep route types centralized** for consistency across the app.

---

## Interview Questions

1. How do you validate request bodies with Zod and TypeScript?
2. What is the `asyncHandler` pattern and why is it needed?
3. How do you create a typed error class hierarchy?
4. How do you type middleware that adds properties to `req`?
5. Explain the difference between operational and programmer errors.
6. How do you type a paginated API response?
7. How do you create reusable validation middleware?
8. How do you handle async errors in Express with TypeScript?
9. How do you type router mounting and route prefixes?
10. What is the benefit of using `ErrorRequestHandler` over regular middleware?
