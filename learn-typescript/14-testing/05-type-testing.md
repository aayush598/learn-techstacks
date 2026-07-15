# Type Testing in TypeScript

## Overview

Type testing verifies that your TypeScript types behave as expected at compile time. Libraries like `tsd` and `expect-type` let you write tests that assert type compatibility, catching type errors before they reach production.

---

## 1. tsd Library Setup

```bash
npm install -D tsd
```

```typescript
// types/index.d.ts
export type User = {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
};

export type CreateUserInput = Omit<User, 'id' | 'createdAt'>;

export type UpdateUserInput = Partial<CreateUserInput>;

export type UserResponse = Omit<User, 'createdAt'> & {
  createdAt: string; // ISO string
};

export function createUser(input: CreateUserInput): Promise<User>;
export function findUser(id: string): Promise<User | null>;
export function updateUser(id: string, input: UpdateUserInput): Promise<User>;
export function deleteUser(id: string): Promise<boolean>;

// Generic function
export function paginate<T>(
  items: T[],
  options: { page: number; limit: number }
): { data: T[]; total: number; page: number; pages: number };

// Utility types
export type NonEmptyArray<T> = [T, ...T[]];
export type Prettify<T> = { [K in keyof T]: T[K] } & {};
export type StrictOmit<T, K extends keyof T> = Omit<T, K>;
```

```typescript
// index.test-d.ts
import { expectType, expectError } from 'tsd';
import {
  User,
  CreateUserInput,
  UpdateUserInput,
  UserResponse,
  createUser,
  findUser,
  updateUser,
  paginate,
  Prettify,
  StrictOmit,
} from '.';

// Test createUser return type
expectType<Promise<User>>(createUser({ name: 'Alice', email: 'a@b.com', role: 'user' }));

// Test CreateUserInput type
expectType<CreateUserInput>({
  name: 'Alice',
  email: 'a@b.com',
  role: 'admin',
});

// Should error — missing required fields
expectError(createUser({ name: 'Alice' }));

// Should error — invalid role
expectError(createUser({ name: 'Alice', email: 'a@b.com', role: 'superadmin' }));

// Test findUser return type
expectType<Promise<User | null>>(findUser('1'));

// Test updateUser input
expectType<Promise<User>>(updateUser('1', { name: 'Bob' }));
expectType<Promise<User>>(updateUser('1', { role: 'admin' }));
expectType<Promise<User>>(updateUser('1', {}));

// Test UserResponse type
expectType<string>({} as UserResponse['createdAt']);
expectType<string>({} as UserResponse['name']);
expectType<string>({} as UserResponse['id']);

// Test paginate generic
const result = paginate([{ id: 1 }, { id: 2 }], { page: 1, limit: 10 });
expectType<{ data: { id: number }[]; total: number; page: number; pages: number }>(result);

// Test Prettify type
type Original = { a: string; b: number };
type Pretty = Prettify<Original>;
expectType<{ a: string; b: number }>({} as Pretty);

// Test StrictOmit
type Strict = StrictOmit<User, 'id' | 'email'>;
expectType<{ name: string; role: 'admin' | 'user'; createdAt: Date }>({} as Strict);
```

---

## 2. expect-type Library

```bash
npm install -D expect-type
```

```typescript
import { expectType, expectError, expectAssignable, expectNotAssignable } from 'expect-type';

// Basic type assertions
expectType<string>('hello');
expectType<number>(42);
expectType<boolean>(true);

// Should fail — wrong type
expectError<string>(42); // Compile error

// Test function return types
function add(a: number, b: number): number {
  return a + b;
}

expectType<number>(add(1, 2));
expectError<string>(add(1, 2));

// Test generic constraints
function identity<T>(value: T): T {
  return value;
}

expectType<string>(identity('hello'));
expectType<number>(identity(42));
expectType<{ name: string }>(identity({ name: 'Alice' }));

// Test conditional types
type IsString<T> = T extends string ? true : false;

expectType<true>({} as IsString<'hello'>);
expectType<false>({} as IsString<42>);

// Test union types
type Status = 'pending' | 'active' | 'inactive';
expectAssignable<Status>('pending');
expectAssignable<Status>('active');
expectNotAssignable<Status>('deleted');

// Test mapped types
type ReadonlyUser = Readonly<User>;
expectType<Readonly<string>>({} as ReadonlyUser['id']);
expectType<Readonly<string>>({} as ReadonlyUser['name']);

// Test function overloads
function process(value: string): string;
function process(value: number): number;
function process(value: string | number): string | number {
  return value;
}

expectType<string>(process('hello'));
expectType<number>(process(42));
expectError<boolean>(process(true));

// Test template literal types
type EventName = `on${Capitalize<'click' | 'hover' | 'focus'>}`;
expectAssignable<EventName>('onClick');
expectAssignable<EventName>('onHover');
expectNotAssignable<EventName>('click');

// Test utility types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

type UserKeys = keyof User;
expectType<'id' | 'name' | 'email' | 'role'>({} as UserKeys);

type UserValues = User[keyof User];
expectType<string | 'admin' | 'user'>({} as UserValues);
```

---

## 3. Testing Generic Constraints

```typescript
import { expectType, expectError } from 'expect-type';

// Generic function with constraints
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find((item) => item.id === id);
}

// Should work — T extends HasId
expectType<{ id: string; name: string } | undefined>(
  findById([{ id: '1', name: 'Alice' }], '1')
);

// Should error — string doesn't have id property
expectError(findById(['hello', 'world'], '1'));

// Generic class with constraints
class Repository<T extends HasId> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  findById(id: string): T | undefined {
    return this.items.find((item) => item.id === id);
  }

  findAll(): T[] {
    return [...this.items];
  }
}

// Should work
const repo = new Repository<{ id: string; name: string }>();
repo.add({ id: '1', name: 'Alice' });

// Should error — missing id
expectError(repo.add({ name: 'Alice' }));

// Test generic constraints with multiple types
function merge<T extends Record<string, any>, U extends Record<string, any>>(
  obj1: T,
  obj2: U
): T & U {
  return { ...obj1, ...obj2 };
}

const merged = merge({ a: 1 }, { b: 'hello' });
expectType<{ a: number } & { b: string }>(merged);
```

---

## 4. Testing Conditional Types

```typescript
import { expectType } from 'expect-type';

// Conditional type
type IsArray<T> = T extends any[] ? true : false;
type ArrayElement<T> = T extends (infer E)[] ? E : never;

expectType<true>({} as IsArray<string[]>);
expectType<false>({} as IsArray<string>);
expectType<string>({} as ArrayElement<string[]>);
expectType<number>({} as ArrayElement<(string | number)[]>);

// Recursive conditional type
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

type Original = {
  name: string;
  nested: {
    value: number;
    deep: {
      items: string[];
    };
  };
};

type ReadonlyOriginal = DeepReadonly<Original>;

expectType<Readonly<string>>({} as ReadonlyOriginal['name']);
expectType<Readonly<number>>({} as ReadonlyOriginal['nested']['value']);
expectType<Readonly<readonly string[]>>({} as ReadonlyOriginal['nested']['deep']['items']);

// Test type inference
type ExtractReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ExtractParams<T> = T extends (...args: infer P) => any ? P : never;

function greet(name: string, age: number): string {
  return `Hello ${name}, ${age}`;
}

expectType<string>({} as ExtractReturnType<typeof greet>);
expectType<[string, number]>({} as ExtractParams<typeof greet>);
```

---

## 5. Testing Mapped Types

```typescript
import { expectType } from 'expect-type';

// Mapped type with modifiers
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

type Optional<T> = { [K in keyof T]?: T[K] };
type Required<T> = { [K in keyof T]-?: T[K] };
type Private<T> = Omit<T, 'password'>;

expectType<Optional<User>>({
  id: '1',
  name: 'Alice',
}); // All fields optional

expectType<Private<User>>({
  id: '1',
  name: 'Alice',
  email: 'alice@test.com',
}); // No password field

// Test key remapping
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;

expectType<() => string>({} as UserGetters['getId']);
expectType<() => string>({} as UserGetters['getName']);
expectType<() => string>({} as UserGetters['getEmail']);

// Test filter mapped types
type FilterByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

type StringFields = FilterByType<User, string>;
expectType<{ id: string; name: string; email: string; password: string }>({} as StringFields);

type DateFields = FilterByType<User, Date>;
expectType<{}>({} as DateFields); // No Date fields
```

---

## 6. Type Testing CI Integration

```json
// package.json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "type-test": "tsd",
    "test": "jest",
    "test:types": "tsd",
    "ci": "npm run typecheck && npm run type-test && npm run test"
  },
  "tsd": {
    "directory": "types",
    "testFilePattern": "*.test-d.ts"
  }
}
```

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run typecheck
      - run: npm run type-test
      - run: npm run test
```

---

## 7. Best Practices

1. **Use `tsd` or `expect-type`** for compile-time type assertions.
2. **Test generic constraints** — ensure they reject invalid types.
3. **Test conditional types** — verify type inference works correctly.
4. **Test utility types** — ensure mapped types produce expected results.
5. **Run type tests in CI** — catch type regressions early.
6. **Test type exports** — ensure public API types are correct.
7. **Test function overloads** — verify all overload signatures work.
8. **Test error cases** — use `expectError` for types that should fail.
9. **Keep type tests separate** — use `.test-d.ts` file extension.
10. **Test complex types** — recursive types, conditional types, template literals.

---

## Interview Questions

1. What is type testing and why is it important?
2. What is the difference between `tsd` and `expect-type`?
3. How do you test generic constraints?
4. How do you test conditional types?
5. How do you verify that a type should cause a compile error?
6. How do you integrate type testing into CI?
7. What are the benefits of type testing over runtime testing?
8. How do you test utility types?
9. How do you test type inference in functions?
10. When should you write type tests vs runtime tests?
