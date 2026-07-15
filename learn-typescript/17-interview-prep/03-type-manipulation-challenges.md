# Type Manipulation Challenges

## 20+ Challenges with Solutions

---

## Challenge 1: Implement Exclude

**Problem**: Extract types from T that are not assignable to U.

```typescript
type MyExclude<T, U> = T extends U ? never : T;

// Test
type T1 = MyExclude<'a' | 'b' | 'c', 'a'>; // 'b' | 'c'
type T2 = MyExclude<string | number | boolean, string>; // number | boolean
```

---

## Challenge 2: Implement Extract

**Problem**: Extract types from T that are assignable to U.

```typescript
type MyExtract<T, U> = T extends U ? T : never;

// Test
type T1 = MyExtract<'a' | 'b' | 'c', 'a' | 'b'>; // 'a' | 'b'
type T2 = MyExtract<string | number | boolean, string>; // string
```

---

## Challenge 3: Implement NonNullable

**Problem**: Extract non-nullable types from T.

```typescript
type MyNonNullable<T> = T extends null | undefined ? never : T;

// Test
type T1 = MyNonNullable<string | null | undefined>; // string
type T2 = MyNonNullable<number | null | undefined | boolean>; // number | boolean
```

---

## Challenge 4: Implement ReturnType

**Problem**: Extract the return type of a function type.

```typescript
type MyReturnType<T extends (...args: any[]) => any> =
  T extends (...args: any[]) => infer R ? R : never;

// Test
function add(a: number, b: number): number { return a + b; }
type T1 = MyReturnType<typeof add>; // number

function greet(name: string): string { return `Hello, ${name}`; }
type T2 = MyReturnType<typeof greet>; // string
```

---

## Challenge 5: Implement Parameters

**Problem**: Extract the parameter types of a function.

```typescript
type MyParameters<T extends (...args: any[]) => any> =
  T extends (...args: infer P) => any ? P : never;

// Test
function add(a: number, b: string): void {}
type T1 = MyParameters<typeof add>; // [a: number, b: string]
```

---

## Challenge 6: Implement DeepReadonly

**Problem**: Make all properties deeply readonly.

```typescript
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? T[P] extends Function
      ? T[P]
      : DeepReadonly<T[P]>
    : T[P];
};

// Test
interface Mutable {
  nested: {
    items: string[];
    config: {
      debug: boolean;
    };
    fn: () => void;
  };
}

type Immutable = DeepReadonly<Mutable>;
// All nested properties are readonly, except functions
```

---

## Challenge 7: Implement PathJoin

**Problem**: Join two path strings with proper type inference.

```typescript
type PathJoin<A extends string, B extends string> =
  A extends `${string}/`
    ? B extends `/${infer BRest}`
      ? `${A}${BRest}`
      : `${A}${B}`
    : B extends `/${string}`
      ? `${A}${B}`
      : `${A}/${B}`;

// Test
type T1 = PathJoin<'/users', '/posts'>; // '/users/posts'
type T2 = PathJoin<'/users', 'posts'>; // '/users/posts'
type T3 = PathJoin<'/users/', '/posts'>; // '/users/posts'
```

---

## Challenge 8: Implement Parser Combinator Types

**Problem**: Create types for parser combinators.

```typescript
type Parser<T> = (input: string) => { value: T; rest: string } | null;

type Many<P extends Parser<any>> = P extends Parser<infer T>
  ? Parser<T[]>
  : never;

type Seq<P1 extends Parser<any>, P2 extends Parser<any>> =
  P1 extends Parser<infer T1>
    ? P2 extends Parser<infer T2>
      ? Parser<[T1, T2]>
      : never
    : never;

// Example parsers
const charParser = (expected: string): Parser<string> => {
  return (input) => {
    if (input.startsWith(expected)) {
      return { value: expected, rest: input.slice(expected.length) };
    }
    return null;
  };
};

const digitParser: Parser<string> = (input) => {
  const match = input.match(/^\d/);
  if (match) {
    return { value: match[0], rest: input.slice(1) };
  }
  return null;
};

// Usage
const result = digitParser('123');
// { value: '1', rest: '23' }
```

---

## Challenge 9: Implement SQL SELECT Types

**Problem**: Create types for SQL SELECT queries.

```typescript
type SelectColumns<T, C extends (keyof T)[]> = {
  [K in C[number]]: T[K];
};

type WhereClause<T> = Partial<Record<keyof T, any>>;

type SelectResult<T, C extends (keyof T)[] = (keyof T)[]> = C extends []
  ? T[]
  : SelectColumns<T, C>[];

// Example
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

// Select all columns
type AllUsers = SelectResult<User>; // User[]

// Select specific columns
type UserName = SelectResult<User, ['name', 'email']>;
// { name: string; email: string }[]
```

---

## Challenge 10: Implement DeepPartial with Arrays

**Problem**: Make all properties optional, including array elements.

```typescript
type DeepPartialWithArrays<T> = {
  [P in keyof T]?: T[P] extends (infer U)[]
    ? DeepPartialWithArrays<U>[]
    : T[P] extends object
      ? DeepPartialWithArrays<T[P]>
      : T[P];
};

// Test
interface Config {
  database: {
    hosts: string[];
    credentials: {
      user: string;
      password: string;
    };
  };
}

const config: DeepPartialWithArrays<Config> = {
  database: {
    hosts: ['localhost'], // Partial array
    credentials: {
      user: 'admin', // Partial nested
    },
  },
};
```

---

## Challenge 11: Implement Tuple Length

**Problem**: Get the length of a tuple type.

```typescript
type TupleLength<T extends any[]> = T['length'];

// Test
type T1 = TupleLength<[1, 2, 3]>; // 3
type T2 = TupleLength<[]>; // 0
type T3 = TupleLength<[string, number, boolean, null]>; // 4
```

---

## Challenge 12: Implement Tuple Concat

**Problem**: Concatenate two tuple types.

```typescript
type Concat<A extends any[], B extends any[]> = [...A, ...B];

// Test
type T1 = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]
type T2 = Concat<[string], [number, boolean]>; // [string, number, boolean]
```

---

## Challenge 13: Implement Tuple Push

**Problem**: Push a type to the end of a tuple.

```typescript
type Push<T extends any[], V> = [...T, V];

// Test
type T1 = Push<[1, 2], 3>; // [1, 2, 3]
type T2 = Push<[string], number>; // [string, number]
```

---

## Challenge 14: Implement Tuple Unshift

**Problem**: Unshift a type to the beginning of a tuple.

```typescript
type Unshift<T extends any[], V> = [V, ...T];

// Test
type T1 = Unshift<[2, 3], 1>; // [1, 2, 3]
type T2 = Unshift<[number], string>; // [string, number]
```

---

## Challenge 15: Implement Tuple Reverse

**Problem**: Reverse a tuple type.

```typescript
type Reverse<T extends any[]> = T extends [infer First, ...infer Rest]
  ? [...Reverse<Rest>, First]
  : [];

// Test
type T1 = Reverse<[1, 2, 3]>; // [3, 2, 1]
type T2 = Reverse<[string, number]>; // [number, string]
```

---

## Challenge 16: Implement Tuple Includes

**Problem**: Check if a tuple includes a type.

```typescript
type Includes<T extends any[], U> = T extends [infer First, ...infer Rest]
  ? First extends U
    ? true
    : Includes<Rest, U>
  : false;

// Test
type T1 = Includes<[1, 2, 3], 2>; // true
type T2 = Includes<[1, 2, 3], 4>; // false
type T3 = Includes<[string, number], string>; // true
```

---

## Challenge 17: Implement Tuple FindIndex

**Problem**: Find the index of a type in a tuple.

```typescript
type FindIndex<T extends any[], U, Acc extends any[] = []> =
  T extends [infer First, ...infer Rest]
    ? First extends U
      ? Acc['length']
      : FindIndex<Rest, U, [...Acc, any]>
    : never;

// Test
type T1 = FindIndex<[1, 2, 3], 2>; // 1
type T2 = FindIndex<[string, number, boolean], number>; // 1
```

---

## Challenge 18: Implement Flatten Tuple

**Problem**: Flatten nested tuples.

```typescript
type FlattenTuple<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends any[]
    ? [...FlattenTuple<First>, ...FlattenTuple<Rest>]
    : [First, ...FlattenTuple<Rest>]
  : [];

// Test
type T1 = FlattenTuple<[[1, 2], [3, [4, 5]]]>; // [1, 2, 3, 4, 5]
```

---

## Challenge 19: Implement Repeat

**Problem**: Repeat a type N times in a tuple.

```typescript
type Repeat<T, N extends number, Acc extends any[] = []> =
  Acc['length'] extends N
    ? Acc
    : Repeat<T, N, [...Acc, T]>;

// Test
type T1 = Repeat<string, 3>; // [string, string, string]
type T2 = Repeat<number, 5>; // [number, number, number, number, number]
```

---

## Challenge 20: Implement Zip

**Problem**: Zip two tuples into a tuple of pairs.

```typescript
type Zip<A extends any[], B extends any[]> =
  A extends [infer AFirst, ...ARest]
    ? B extends [infer BFirst, ...BRest]
      ? [[AFirst, BFirst], ...Zip<ARest, BRest>]
      : []
    : [];

// Test
type T1 = Zip<[1, 2, 3], ['a', 'b', 'c']>;
// [[1, 'a'], [2, 'b'], [3, 'c']]
```

---

## Challenge 21: Implement GroupBy

**Problem**: Group array elements by a key function.

```typescript
type GroupBy<T extends any[], K extends keyof T[number]> = {
  [P in T[number][K]]: T[number][];
};

// Example usage at type level
interface Item {
  type: 'a' | 'b';
  value: number;
}

type Grouped = GroupBy<Item[], 'type'>;
// { a: Item[]; b: Item[] }
```

---

## Challenge 22: Implement Pipe with Type Safety

**Problem**: Create a type-safe pipe function.

```typescript
type LastElement<T extends any[]> = T extends [...any[], infer Last]
  ? Last
  : never;

type PipeFunctions<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends (arg: any) => any
    ? Rest extends [(arg: ReturnType<First>) => any, ...any[]]
      ? [First, ...PipeFunctions<Rest>]
      : [First]
    : never
  : [];

function pipe<T extends ((arg: any) => any)[]>(
  ...fns: T & PipeFunctions<T>
): (arg: Parameters<T[0]>[0]) => ReturnType<LastElement<T>> {
  return (arg: any) => {
    return fns.reduce((acc, fn) => fn(acc), arg);
  };
}

// Usage
const transform = pipe(
  (x: number) => x + 1,
  (x: number) => x * 2,
  (x: number) => x.toString()
);

const result = transform(5); // "12" (type: string)
```

---

## Challenge 23: Implement Branded Types

**Problem**: Create branded types for nominal typing.

```typescript
type Brand<K, T> = T & { __brand: K };

type UserId = Brand<'UserId', string>;
type PostId = Brand<'PostId', string>;

function createUserId(id: string): UserId {
  return id as UserId;
}

function createPostId(id: string): PostId {
  return id as PostId;
}

function getUser(id: UserId): void {
  console.log(`Getting user ${id}`);
}

// These are now type-safe:
const userId = createUserId('123');
const postId = createPostId('456');

getUser(userId); // ✅
getUser(postId); // ❌ Type error — can't pass PostId as UserId
```

---

## Challenge 24: Implement Builder Pattern with Type Safety

**Problem**: Create a type-safe builder that enforces required fields.

```typescript
type BuilderState<T, K extends keyof T = never> = {
  [P in keyof T]: P extends K ? T[P] : T[P] | undefined;
};

class TypeSafeBuilder<T> {
  private data: any = {};
  private required: Set<keyof T> = new Set();
  private provided: Set<keyof T> = new Set();

  require<K extends keyof T>(key: K): TypeSafeBuilder<T, K> {
    this.required.add(key);
    return this as any;
  }

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    this.provided.add(key);
    return this;
  }

  build(): T {
    for (const key of this.required) {
      if (!this.provided.has(key)) {
        throw new Error(`Missing required field: ${String(key)}`);
      }
    }
    return this.data as T;
  }
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
}

const user = new TypeSafeBuilder<User>()
  .require('id')
  .require('name')
  .require('email')
  .set('id', 1)
  .set('name', 'Alice')
  .set('email', 'alice@example.com')
  .set('age', 30)
  .build();
```

---

## Challenge 25: Implement Type-Safe State Machine

**Problem**: Create a type-safe state machine.

```typescript
type States = string;
type Events = string;

type StateMachineConfig<S extends States, E extends Events> = {
  [K in S]: {
    [P in E]?: S;
  };
};

class StateMachine<S extends States, E extends Events> {
  private current: S;
  private config: StateMachineConfig<S, E>;

  constructor(config: StateMachineConfig<S, E>, initial: S) {
    this.config = config;
    this.current = initial;
  }

  send(event: E): S {
    const transitions = this.config[this.current];
    if (!transitions || !(event in transitions)) {
      throw new Error(`Invalid event '${event}' in state '${this.current}'`);
    }
    this.current = transitions[event] as S;
    return this.current;
  }

  getState(): S {
    return this.current;
  }
}

// Usage
type TrafficLightState = 'green' | 'yellow' | 'red';
type TrafficLightEvent = 'next';

const trafficLight = new StateMachine<TrafficLightState, TrafficLightEvent>(
  {
    green: { next: 'yellow' },
    yellow: { next: 'red' },
    red: { next: 'green' },
  },
  'green'
);

trafficLight.send('next'); // yellow
trafficLight.send('next'); // red
trafficLight.send('next'); // green
```

---

## Complexity Analysis

| Challenge | Difficulty | Key Concept |
|-----------|------------|-------------|
| Exclude/Extract | Easy | Conditional types |
| NonNullable | Easy | Union elimination |
| ReturnType/Parameters | Medium | Infer keyword |
| DeepReadonly | Medium | Recursive types |
| PathJoin | Medium | Template literals |
| Tuple operations | Medium | Recursive tuples |
| SQL types | Hard | Complex type inference |
| Builder pattern | Hard | Generic constraints |
