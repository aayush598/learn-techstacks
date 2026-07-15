# NestJS Decorators in TypeScript

## Table of Contents

- [Overview](#overview)
- [NestJS Decorator Ecosystem](#nestjs-decorator-ecosystem)
- [@Injectable](#injectable)
- [@Controller](#controller)
- [@Module](#module)
- [@Inject](#inject)
- [Custom Decorators in NestJS](#custom-decorators-in-nestjs)
- [Pipe Decorators](#pipe-decorators)
- [Guard Decorators](#guard-decorators)
- [Interceptor Decorators](#interceptor-decorators)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

NestJS is heavily built on decorators. Almost every aspect of a NestJS application — controllers, services, modules, pipes, guards, interceptors — is configured using TypeScript decorators. Understanding NestJS decorators is essential for effective NestJS development.

---

## NestJS Decorator Ecosystem

### Categories of NestJS Decorators

```typescript
// 1. Module decorators
import { Module, Global } from '@nestjs/common';

// 2. Controller decorators
import { Controller, Get, Post, Put, Delete, Req, Res, Body, Param, Query } from '@nestjs/common';

// 3. Provider/Service decorators
import { Injectable, Inject } from '@nestjs/common';

// 4. Execution context decorators
import { UseGuards, UseInterceptors, UsePipes } from '@nestjs/common';

// 5. Custom decorators
import { createParamDecorator, SetMetadata } from '@nestjs/common';
```

---

## @Injectable

Marks a class as a provider that can be managed by the NestJS IoC container.

```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  constructor(
    private readonly databaseService: DatabaseService,
    private readonly emailService: EmailService
  ) {}

  async findAll(): Promise<User[]> {
    return this.databaseService.query('SELECT * FROM users');
  }

  async create(data: CreateUserDto): Promise<User> {
    const user = await this.databaseService.insert('users', data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

### Injectable with Scope

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Default: Singleton scope
@Injectable()
export class ConfigService {
  get(key: string): string {
    return process.env[key] || '';
  }
}

// Request scope: new instance per request
@Injectable({ scope: Scope.REQUEST })
export class RequestContext {
  constructor() {
    this.requestId = crypto.randomUUID();
  }
  requestId: string;
}

// Transient scope: new instance each time injected
@Injectable({ scope: Scope.TRANSIENT })
export class IdGenerator {
  generate(): string {
    return crypto.randomUUID();
  }
}
```

---

## @Controller

Defines a controller class that handles incoming HTTP requests.

```typescript
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  findAll(@Query('page') page: number = 1): Promise<User[]> {
    return this.userService.findAll(page);
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<User> {
    return this.userService.findOne(id);
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.userService.create(createUserDto);
  }
}
```

### Route-Level Decorators

```typescript
import {
  Get, Post, Put, Delete, Patch,
  Req, Res, HttpCode, HttpStatus,
  Header, Redirect,
} from '@nestjs/common';

@Controller('products')
export class ProductController {
  @Get()
  @HttpCode(200)
  @Header('X-Custom', 'value')
  findAll() {
    return [];
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() data: CreateProductDto) {
    return data;
  }

  @Get('docs')
  @Redirect('https://docs.nestjs.com', 301)
  getDocs() {}

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id') id: string) {
    return this.userService.remove(id);
  }
}
```

---

## @Module

Defines a NestJS module that organizes related components.

```typescript
import { Module, Global, DynamicModule } from '@nestjs/common';

@Module({
  imports: [DatabaseModule, AuthModule],        // Other modules this module depends on
  controllers: [UserController],                // Controllers handled by this module
  providers: [UserService, UserRepository],     // Services/providers owned by this module
  exports: [UserService],                       // Providers available to other modules
})
export class UserModule {}

// Global module: providers available everywhere without importing
@Global()
@Module({
  providers: [ConfigService],
  exports: [ConfigService],
})
export class ConfigModule {}
```

### Dynamic Module

```typescript
import { Module, DynamicModule } from '@nestjs/common';

@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        {
          provide: 'DATABASE_OPTIONS',
          useValue: options,
        },
        DatabaseService,
      ],
      exports: [DatabaseService],
    };
  }

  static forFeature(entities: Function[]): DynamicModule {
    return {
      module: DatabaseModule,
      providers: entities.map((entity) => ({
        provide: `REPOSITORY_${entity.name}`,
        useFactory: (db: DatabaseService) => db.getRepository(entity),
        inject: [DatabaseService],
      })),
    };
  }
}

// Usage in app.module.ts
@Module({
  imports: [
    DatabaseModule.forRoot({
      host: 'localhost',
      port: 5432,
    }),
  ],
})
export class AppModule {}
```

---

## @Inject

Injects a custom token or value from the IoC container.

```typescript
import { Module, Inject } from '@nestjs/common';

// Custom token injection
const REDIS_CLIENT = 'REDIS_CLIENT';

@Module({
  providers: [
    {
      provide: REDIS_CLIENT,
      useFactory: () => createRedisClient(),
    },
  ],
  exports: [REDIS_CLIENT],
})
export class RedisModule {}

@Injectable()
export class CacheService {
  constructor(
    @Inject(REDIS_CLIENT) private readonly redis: RedisClient,
    @Inject('DATABASE_URL') private readonly dbUrl: string
  ) {}

  async get(key: string): Promise<string | null> {
    return this.redis.get(key);
  }
}
```

### Injection Tokens

```typescript
// String tokens
@Injectable()
export class Service {
  constructor(
    @Inject('CACHE_TTL') private ttl: number,
    @Inject('API_KEY') private apiKey: string
  ) {}
}

// Class tokens (works the same as constructor injection)
@Injectable()
export class Service {
  constructor(
    @Inject(DatabaseService) private db: DatabaseService
  ) {}
}
```

---

## Custom Decorators in NestJS

### createParamDecorator

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

// Extract user from request
export const CurrentUser = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  }
);

// Extract specific header
export const ClientIp = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): string => {
    const request = ctx.switchToHttp().getRequest();
    return request.ip || request.connection.remoteAddress;
  }
);

// Usage
@Controller('profile')
export class ProfileController {
  @Get()
  getProfile(@CurrentUser() user: User) {
    return user;
  }

  @Get('email')
  getEmail(@CurrentUser('email') email: string) {
    return email;
  }

  @Get('ip')
  getIp(@ClientIp() ip: string) {
    return { ip };
  }
}
```

### SetMetadata

```typescript
import { SetMetadata } from '@nestjs/common';

// Attach custom metadata to handlers
export const ROLES_KEY = 'roles';
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);

export const CACHE_KEY = 'cache';
export const Cache = (ttl: number) => SetMetadata(CACHE_KEY, ttl);

// Usage
@Controller('admin')
export class AdminController {
  @Get('dashboard')
  @Roles('admin', 'super-admin')
  @Cache(60)
  getDashboard() {
    return { data: 'sensitive' };
  }
}

// Reading metadata in a guard:
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) return true;

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

---

## Pipe Decorators

### Built-in Pipes

```typescript
import { ValidationPipe, ParseIntPipe, ParseUUIDPipe, ParseBoolPipe } from '@nestjs/common';

@Controller('users')
export class UserController {
  @Get(':id')
  findOne(
    @Param('id', ParseIntPipe) id: number,
    @Query('verbose', ParseBoolPipe) verbose: boolean
  ) {
    return { id, verbose };
  }

  @Post()
  @UsePipes(new ValidationPipe({ transform: true, whitelist: true }))
  create(@Body() createUserDto: CreateUserDto) {
    return createUserDto;
  }
}
```

### Custom Pipe

```typescript
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseObjectIdPipe implements PipeTransform<string> {
  transform(value: string): string {
    if (!/^[0-9a-fA-F]{24}$/.test(value)) {
      throw new BadRequestException(`${value} is not a valid ObjectId`);
    }
    return value;
  }
}

// Usage
@Get(':id')
findOne(@Param('id', ParseObjectIdPipe) id: string) {
  return this.service.findById(id);
}
```

---

## Guard Decorators

### Built-in Auth Guard

```typescript
import { AuthGuard } from '@nestjs/passport';

@Controller('profile')
export class ProfileController {
  @UseGuards(AuthGuard('jwt'))
  @Get()
  getProfile(@Req() req) {
    return req.user;
  }
}
```

### Custom Guard

```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';

@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    const requiredRoles = Reflect.getMetadata('roles', context.getHandler());

    if (!requiredRoles || requiredRoles.length === 0) return true;

    return requiredRoles.some((role: string) => user.roles?.includes(role));
  }
}

// Usage
@Controller('admin')
@UseGuards(RolesGuard)
export class AdminController {
  @Get()
  @Roles('admin')
  adminOnly() {
    return 'Admin content';
  }
}
```

---

## Interceptor Decorators

### Logging Interceptor

```typescript
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    const request = context.switchToHttp().getRequest();

    return next.handle().pipe(
      tap(() => {
        const elapsed = Date.now() - now;
        console.log(
          `${request.method} ${request.url} - ${elapsed}ms`
        );
      })
    );
  }
}

// Apply globally or per-controller
@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => ({
        data,
        timestamp: new Date().toISOString(),
        statusCode: context.switchToHttp().getResponse().statusCode,
      }))
    );
  }
}

// Usage
@Controller('users')
@UseInterceptors(LoggingInterceptor, TransformInterceptor)
export class UserController {}
```

---

## Best Practices

1. **Use `@Injectable()` on all services** — even if constructor injection isn't used, it enables future DI.

2. **Use `SetMetadata` with custom guards** for role-based access control.

3. **Create param decorators** for common request data extraction (user, IP, tenant, etc.).

4. **Use `ValidationPipe` globally** in `main.ts` for automatic DTO validation.

5. **Keep custom decorators simple** — NestJS decorators are just metadata containers.

---

## Interview Questions

### Q1: What does `@Injectable()` do in NestJS?

**Answer**: It marks a class as a provider that can be managed by NestJS's IoC container, enabling automatic dependency injection. Without it, NestJS can't inject the class's dependencies. It also allows configuring the provider's scope (singleton, request, or transient).

### Q2: How does NestJS's dependency injection work with decorators?

**Answer**: NestJS uses `Reflect.defineMetadata('design:paramtypes', ...)` (from `emitDecoratorMetadata`) to determine constructor parameter types at runtime. It then resolves each type from the IoC container. `@Inject(token)` overrides this for custom tokens by storing metadata about which token to use for a specific parameter.

### Q3: What is the difference between `@Inject()` and automatic injection?

**Answer**: Automatic injection uses the parameter's TypeScript type to look up the provider in the IoC container. `@Inject(token)` explicitly specifies which provider to inject by its token (string, symbol, or class). Use `@Inject()` when the token doesn't match the type (custom tokens, primitive values).

### Q4: How do you create a custom parameter decorator in NestJS?

**Answer**: Use `createParamDecorator((data, ctx) => { ... })`. The first argument is custom data passed when applying the decorator, and the second is the `ExecutionContext`. Use `ctx.switchToHttp().getRequest()` to access the HTTP request and extract the needed data.

### Q5: What are pipes, guards, and interceptors in NestJS?

**Answer**: Pipes transform input data (validation, parsing). Guards determine whether a request should be handled (authentication, authorization). Interceptors wrap request/response handling (logging, caching, transformation). All are decorated onto controllers or methods using `@UsePipes()`, `@UseGuards()`, and `@UseInterceptors()`.
