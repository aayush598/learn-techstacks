# Parameter Decorators in TypeScript

## Table of Contents

- [Overview](#overview)
- [Parameter Decorator Signature](#parameter-decorator-signature)
- [Dependency Injection with Parameter Decorators](#dependency-injection-with-parameter-decorators)
- [Validation Decorators](#validation-decorators)
- [NestJS Parameter Decorators](#nestjs-parameter-decorators)
- [Combining Parameter Decorators with Other Decorators](#combining-parameter-decorators-with-other-decorators)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Parameter decorators are applied to individual parameters of a method or constructor. They're commonly used in dependency injection frameworks, validation libraries, and web frameworks like NestJS. Unlike other decorators, they can't modify the parameter itself — they only record metadata about it.

---

## Parameter Decorator Signature

### Legacy Signature

```typescript
function MyParamDecorator(
  target: any,                        // The prototype of the class
  propertyKey: string | undefined,    // Method name (undefined for constructor)
  parameterIndex: number              // Position of the parameter (0-indexed)
) {
  // Store metadata about this parameter
}
```

### Stage 3 Signature

```typescript
function MyParamDecorator(
  value: undefined,                    // Always undefined for parameters
  context: ClassMethodDecoratorContext | ClassDecoratorContext
  // context.kind === 'method' or 'class' (for constructor)
  // For method params: context.name is the method name
) {
  // Note: no parameterIndex in Stage 3 — need workaround
}
```

### Basic Example

```typescript
function LogParam(
  target: any,
  propertyKey: string | undefined,
  parameterIndex: number
) {
  const methodName = propertyKey ?? 'constructor';
  console.log(
    `Parameter decorator applied to position ${parameterIndex} of ${methodName}`
  );
}

class UserService {
  getUser(
    @LogParam id: string,
    @LogParam format: string
  ) {
    return { id, format };
  }

  constructor(
    @LogParam db: any,
    @LogParam logger: any
  ) {}
}

// Output:
// "Parameter decorator applied to position 0 of constructor"
// "Parameter decorator applied to position 1 of constructor"
// "Parameter decorator applied to position 0 of getUser"
// "Parameter decorator applied to position 1 of getUser"
```

---

## Dependency Injection with Parameter Decorators

### Basic DI Container

```typescript
// Simple DI container
const injectionTokens = new Map<string, Map<number, string>>();

function Inject(token: string) {
  return function (
    target: any,
    propertyKey: string | undefined,
    parameterIndex: number
  ) {
    const key = propertyKey ?? 'constructor';
    if (!injectionTokens.has(key)) {
      injectionTokens.set(key, new Map());
    }
    injectionTokens.get(key)!.set(parameterIndex, token);
  };
}

// Service registry
const services = new Map<string, any>();

function registerService(token: string, implementation: any) {
  services.set(token, implementation);
}

// Auto-inject decorator for the class
function Injectable() {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    return class extends constructor {
      constructor(...args: any[]) {
        // Get injection tokens for constructor
        const tokens = injectionTokens.get('constructor') || new Map();
        const resolvedArgs: any[] = [];

        for (let i = 0; i < constructor.length; i++) {
          const token = tokens.get(i);
          if (token) {
            const service = services.get(token);
            if (!service) {
              throw new Error(`No service registered for token: ${token}`);
            }
            resolvedArgs.push(service);
          } else {
            resolvedArgs.push(args[i - resolvedArgs.length]);
          }
        }

        super(...resolvedArgs);
      }
    };
  };
}

// Register services
registerService('database', { query: (sql: string) => console.log(`Exec: ${sql}`) });
registerService('logger', { log: (msg: string) => console.log(`Log: ${msg}`) });

// Use in a class
@Injectable()
class UserService {
  constructor(
    @Inject('database') private db: any,
    @Inject('logger') private logger: any
  ) {
    console.log('UserService created');
  }

  getUser(id: string) {
    this.logger.log(`Fetching user ${id}`);
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

const userService = new UserService(); // Auto-injects db and logger
userService.getUser('123');
```

### Reflect-metadata Based DI

```typescript
import 'reflect-metadata';

const INJECTION_METADATA = 'design:inject';

function Inject(token: string) {
  return function (
    target: any,
    propertyKey: string | undefined,
    parameterIndex: number
  ) {
    const existingTokens: string[] =
      Reflect.getMetadata(INJECTION_METADATA, target, propertyKey ?? 'constructor') || [];
    existingTokens[parameterIndex] = token;
    Reflect.defineMetadata(
      INJECTION_METADATA,
      existingTokens,
      target,
      propertyKey ?? 'constructor'
    );
  };
}

function resolve<T>(constructor: new (...args: any[]) => T): T {
  const tokens: string[] =
    Reflect.getMetadata(INJECTION_METADATA, constructor, 'constructor') || [];

  const args = tokens.map((token) => {
    // In real DI, resolve the actual implementation
    return getService(token);
  });

  return new constructor(...args);
}

function getService(token: string): any {
  // Lookup from a registry
  return { token };
}
```

---

## Validation Decorators

### Validate Parameters at Runtime

```typescript
import 'reflect-metadata';

const VALIDATION_KEY = 'validation:params';

function ValidateParam(
  validator: (value: any) => boolean,
  errorMessage: string
) {
  return function (
    target: any,
    propertyKey: string | undefined,
    parameterIndex: number
  ) {
    const existingValidators =
      Reflect.getMetadata(VALIDATION_KEY, target, propertyKey ?? 'constructor') || [];
    existingValidators[parameterIndex] = { validator, errorMessage };
    Reflect.defineMetadata(
      VALIDATION_KEY,
      existingValidators,
      target,
      propertyKey ?? 'constructor'
    );
  };
}

// Decorator for the method to trigger validation
function Validated(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    const validators: Array<{ validator: (v: any) => boolean; errorMessage: string }> =
      Reflect.getMetadata(VALIDATION_KEY, target, propertyKey) || [];

    for (let i = 0; i < validators.length; i++) {
      const { validator, errorMessage } = validators[i];
      if (validator && !validator(args[i])) {
        throw new Error(`Validation failed for parameter ${i}: ${errorMessage}`);
      }
    }

    return originalMethod.apply(this, args);
  };
}

// Common validators
const isString = (v: any) => typeof v === 'string';
const isNumber = (v: any) => typeof v === 'number' && !isNaN(v);
const isEmail = (v: any) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
const minLength = (min: number) => (v: any) => typeof v === 'string' && v.length >= min;

class UserController {
  @Validated
  createUser(
    @ValidateParam(isString, 'Name must be a string')
    @ValidateParam(minLength(2), 'Name must be at least 2 characters')
    name: string,
    @ValidateParam(isEmail, 'Must be a valid email')
    email: string,
    @ValidateParam(isNumber, 'Age must be a number')
    age: number
  ) {
    return { name, email, age };
  }
}

const controller = new UserController();
controller.createUser('Alice', 'alice@example.com', 25); // OK
controller.createUser('A', 'not-an-email', 'not-a-number'); // Error!
```

---

## NestJS Parameter Decorators

### Built-in Param Decorators

```typescript
import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Query,
  Headers,
  Req,
  Res,
  HttpCode,
  HttpStatus,
} from '@nestjs/common';

@Controller('users')
class UserController {
  // @Param extracts route parameters
  @Get(':id')
  findOne(
    @Param('id') id: string,
    @Query('format') format: string
  ) {
    return { id, format };
  }

  // @Body extracts request body
  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return createUserDto;
  }

  // @Headers extracts request headers
  @Get('profile')
  getProfile(@Headers('authorization') auth: string) {
    return { auth };
  }
}
```

### Custom Parameter Decorator

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

// Custom decorator to extract user from request
const CurrentUser = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  }
);

// Usage
@Controller('users')
class UserController {
  @Get('me')
  getProfile(@CurrentUser() user: User) {
    return user;
  }

  @Get('me/email')
  getEmail(@CurrentUser('email') email: string) {
    return email;
  }
}

// Another custom decorator: extract specific body field
const BodyField = createParamDecorator(
  (field: string, ctx: ExecutionContext) => {
    const body = ctx.switchToHttp().getRequest().body;
    return body?.[field];
  }
);

@Controller('auth')
class AuthController {
  @Post('login')
  login(
    @BodyField('username') username: string,
    @BodyField('password') password: string
  ) {
    return { username, password };
  }
}
```

---

## Combining Parameter Decorators with Other Decorators

### Complete API Method Decoration

```typescript
// Parameter decorator: marks which params are validated
function ValidParam(
  validationRules: Array<(val: any) => boolean>,
  errorMessage: string
) {
  return function (target: any, propertyKey: string | undefined, parameterIndex: number) {
    const key = `${propertyKey ?? 'constructor'}:${parameterIndex}`;
    Reflect.defineMetadata(`valid:${key}`, { rules: validationRules, errorMessage }, target);
  };
}

// Method decorator: triggers validation
function Validate(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    for (let i = 0; i < args.length; i++) {
      const meta = Reflect.getMetadata(`valid:${propertyKey}:${i}`, target);
      if (meta) {
        const isValid = meta.rules.some((rule: (v: any) => boolean) => rule(args[i]));
        if (!isValid) {
          throw new Error(`Parameter ${i}: ${meta.errorMessage}`);
        }
      }
    }
    return originalMethod.apply(this, args);
  };
}

// Log decorator: logs method calls
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`${propertyKey} called with`, args);
    return originalMethod.apply(this, args);
  };
}

class OrderService {
  @Log        // Method-level: logs the call
  @Validate   // Method-level: triggers validation
  createOrder(
    @ValidParam([(v) => typeof v === 'string'], 'Must be a string')
    productId: string,

    @ValidParam([(v) => typeof v === 'number' && v > 0], 'Must be positive number')
    quantity: number
  ) {
    return { productId, quantity };
  }
}
```

---

## Real-World Examples

### Permission Checker

```typescript
const permissionsMeta = new Map<string, string[]>();

function RequirePermission(permission: string) {
  return function (target: any, propertyKey: string | undefined, parameterIndex: number) {
    const key = propertyKey ?? 'constructor';
    const existing = permissionsMeta.get(key) || [];
    existing.push(permission);
    permissionsMeta.set(key, existing);
  };
}

function CheckPermissions(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    const required = permissionsMeta.get(propertyKey) || [];
    const user = (this as any).currentUser;
    const userPermissions = user?.permissions || [];

    for (const perm of required) {
      if (!userPermissions.includes(perm)) {
        throw new Error(`Missing permission: ${perm}`);
      }
    }

    return originalMethod.apply(this, args);
  };
}

class AdminController {
  @CheckPermissions
  deleteUser(
    @RequirePermission('users:delete')
    id: string
  ) {
    return { deleted: id };
  }
}
```

---

## Best Practices

1. **Parameter decorators record metadata only** — they can't modify parameters. Use method decorators to act on the metadata.

2. **Always pair with a method decorator** — parameter decorators store data; method decorators consume it.

3. **Use `reflect-metadata`** for storing and retrieving parameter metadata reliably.

4. **Use `emitDecoratorMetadata`** when you need automatic type information at runtime.

5. **Keep parameter decorators simple** — they should only tag metadata, not perform logic.

6. **Use index-based metadata** — store metadata keyed by parameter position.

---

## Interview Questions

### Q1: Why can't parameter decorators modify the parameter value?

**Answer**: Parameters are just positions in a function signature — they don't have values until the function is called. Parameter decorators can only record metadata (like validation rules or injection tokens) using `Reflect.defineMetadata`. A method decorator then reads this metadata and acts on it at call time.

### Q2: How does NestJS's `@Body()` decorator work?

**Answer**: It uses `createParamDecorator` which receives an `ExecutionContext`. The decorator extracts the HTTP request from the context and returns `request.body`. At runtime, NestJS calls each parameter decorator to extract values, then passes them as arguments to the handler method.

### Q3: What's the relationship between `emitDecoratorMetadata` and parameter decorators?

**Answer**: `emitDecoratorMetadata` causes TypeScript to emit `design:paramtypes` metadata — an array of parameter types for each decorated method/constructor. This is separate from custom parameter decorators. Both use `Reflect.metadata` but store different information: one stores types (automatic), the other stores custom data (manual).
