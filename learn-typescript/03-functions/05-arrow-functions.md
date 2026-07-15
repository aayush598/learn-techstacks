# Arrow Functions in TypeScript

## Table of Contents

1. [Arrow Function Syntax with Types](#arrow-function-syntax-with-types)
2. [This Binding Differences](#this-binding-differences)
3. [Arrow Functions as Callbacks](#arrow-functions-as-callbacks)
4. [Arrow Functions in Classes](#arrow-functions-in-classes)
5. [Arrow Function vs Function Expression](#arrow-function-vs-function-expression)
6. [Implicit Return with Arrow Functions](#implicit-return-with-arrow-functions)
7. [Arrow Functions and Generics](#arrow-functions-and-generics)
8. [Readonly This](#readonly-this)
9. [Advanced Patterns](#advanced-patterns)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Arrow Function Syntax with Types

Arrow functions provide a concise syntax for writing functions with TypeScript type annotations.

```typescript
// Basic arrow function with types
const greet = (name: string): string => {
  return `Hello, ${name}!`;
};

// With explicit parameter types and return type
const add = (a: number, b: number): number => a + b;

// No parameters
const getCurrentTime = (): Date => new Date();

// Single parameter (parentheses optional)
const double = (x: number): number => x * 2;
const doubleAlternative = x: number => x * 2; // Also valid, but less readable

// Multiple statements
const processUser = (user: User): ProcessedUser => {
  const fullName = `${user.firstName} ${user.lastName}`;
  const age = calculateAge(user.birthDate);
  return { ...user, fullName, age };
};

// Returning objects (needs parentheses)
const createUser = (name: string, age: number) => ({
  name,
  age,
  createdAt: new Date(),
});

// Type annotation for the variable
const multiply: (a: number, b: number) => number = (a, b) => a * b;
```

### Detailed Syntax Examples

```typescript
// Arrow function with destructuring
const getFullName = ({ firstName, lastName }: { firstName: string; lastName: string }): string =>
  `${firstName} ${lastName}`;

// Arrow function with optional parameters
const formatName = (first: string, last?: string): string =>
  last ? `${first} ${last}` : first;

// Arrow function with default parameters
const createGreeting = (name: string, greeting: string = "Hello"): string =>
  `${greeting}, ${name}!`;

// Arrow function with rest parameters
const sum = (...numbers: number[]): number =>
  numbers.reduce((total, n) => total + n, 0);

// Arrow function with complex return types
interface Result<T> {
  data: T;
  success: boolean;
  timestamp: Date;
}

const fetchData = async <T>(url: string): Promise<Result<T>> => {
  const response = await fetch(url);
  const data = await response.json();
  return {
    data,
    success: response.ok,
    timestamp: new Date(),
  };
};

// Arrow function in object literal
const calculator = {
  add: (a: number, b: number): number => a + b,
  subtract: (a: number, b: number): number => a - b,
  multiply: (a: number, b: number): number => a * b,
  divide: (a: number, b: number): number => {
    if (b === 0) throw new Error("Division by zero");
    return a / b;
  },
};
```

---

## This Binding Differences

Arrow functions do not have their own `this` binding. They inherit `this` from the enclosing lexical scope.

```typescript
// Regular function: 'this' depends on how it's called
class Counter {
  count = 0;

  // Regular method: 'this' is the instance when called as obj.method()
  increment() {
    this.count++;
    return this;
  }

  // Arrow function: 'this' is lexically bound to the instance
  incrementArrow = () => {
    this.count++;
    return this;
  };
}

const counter = new Counter();

// Regular method - 'this' is lost when extracted
const increment = counter.increment;
// increment(); // Error: 'this' is undefined (or global in non-strict)

// Arrow function - 'this' is preserved
const incrementArrow = counter.incrementArrow;
incrementArrow(); // Works! 'this' is the Counter instance

// Callback pattern - classic problem
class Timer {
  seconds = 0;

  // BAD: Regular function callback loses 'this'
  startRegular() {
    setInterval(function () {
      this.seconds++; // 'this' is undefined/global, not Timer
      console.log(this.seconds);
    }, 1000);
  }

  // GOOD: Arrow function callback preserves 'this'
  startArrow() {
    setInterval(() => {
      this.seconds++; // 'this' is the Timer instance
      console.log(this.seconds);
    }, 1000);
  }
}
```

### This in Different Contexts

```typescript
// Arrow functions in event handlers
class ButtonHandler {
  label = "Click me";

  setup() {
    const button = document.querySelector("button");

    // Regular function: 'this' would be the button element
    button?.addEventListener("click", function () {
      console.log(this.label); // undefined (this is the button)
    });

    // Arrow function: 'this' is the ButtonHandler instance
    button?.addEventListener("click", () => {
      console.log(this.label); // "Click me"
    });
  }
}

// Arrow functions and object methods (anti-pattern)
const person = {
  name: "Alice",

  // BAD: Arrow function as method - 'this' is not the object
  greet: () => {
    return `Hello, I'm ${this.name}`; // 'this' is not 'person'
  },

  // GOOD: Regular function as method
  greetProper() {
    return `Hello, I'm ${this.name}`;
  },
};

// Arrow in object literal captures outer 'this'
const outerThis = this; // Module-level this

const obj = {
  name: "Bob",
  // This captures outerThis, not obj
  getName: () => outerThis.name,
};
```

---

## Arrow Functions as Callbacks

Arrow functions excel as callbacks due to their concise syntax and lexical `this`.

```typescript
// Array methods with arrow callbacks
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evens = numbers.filter((n) => n % 2 === 0);
const doubled = numbers.map((n) => n * 2);
const sum = numbers.reduce((acc, n) => acc + n, 0);
const firstBig = numbers.find((n) => n > 5);
const allPositive = numbers.every((n) => n > 0);
const hasNegative = numbers.some((n) => n < 0);

// Promise chains
fetchUser(id)
  .then((user) => fetchOrders(user.id))
  .then((orders) => processOrders(orders))
  .catch((error) => console.error(error));

// Async/await (syntactic sugar over promises)
async function handleRequest(url: string): Promise<Response> {
  const response = await fetch(url);
  const data = await response.json();
  return new Response(JSON.stringify(data));
}

// Event listeners
button.addEventListener("click", () => {
  console.log("Button clicked");
});

// Timer callbacks
setTimeout(() => {
  console.log("Delayed message");
}, 1000);

// Array sorting
const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
  { name: "Charlie", age: 35 },
];

const sortedByAge = [...users].sort((a, b) => a.age - b.age);
const sortedByName = [...users].sort((a, b) => a.name.localeCompare(b.name));
```

### Complex Callback Patterns

```typescript
// Callback with type inference
const processItems = <T>(items: T[], callback: (item: T, index: number) => T): T[] =>
  items.map((item, index) => callback(item, index));

// Callback returning void
const forEachWithIndex = <T>(items: T[], callback: (item: T, index: number) => void): void =>
  items.forEach((item, index) => callback(item, index));

// Nested callbacks with arrow functions
const pipeline = <T>(value: T, ...transforms: Array<(v: T) => T>): T =>
  transforms.reduce((result, transform) => transform(result), value);

const result = pipeline(
  "  Hello World  ",
  (s) => s.trim(),
  (s) => s.toLowerCase(),
  (s) => s.replace(/\s+/g, "_")
);
// result: "hello_world"
```

---

## Arrow Functions in Classes

Using arrow functions as class properties and methods.

```typescript
// Arrow function as class property
class UserService {
  private users: User[] = [];

  // Arrow function property - 'this' is always the instance
  addUser = (user: User): void => {
    this.users.push(user);
  };

  // Regular method - 'this' depends on call context
  getUser(id: string): User | undefined {
    return this.users.find((u) => u.id === id);
  }

  // Arrow function for callbacks
  setupListeners = (): void => {
    document.addEventListener("click", () => {
      // 'this' is UserService instance
      console.log(`Users: ${this.users.length}`);
    });
  };
}

// Arrow functions as private methods (TypeScript 3.8+)
class DataProcessor {
  // Private field
  #data: number[] = [];

  // Arrow function as private method equivalent
  validate = (item: number): boolean => {
    return item >= 0 && item <= 100;
  };

  process = (items: number[]): number[] => {
    return items.filter(this.validate).map((item) => item * 2);
  };
}
```

### Class Property vs Method

```typescript
class Example {
  value = 42;

  // Method: defined on prototype, shared between instances
  getValue() {
    return this.value;
  }

  // Arrow function property: defined on each instance
  getValueArrow = () => {
    return this.value;
  };
}

const a = new Example();
const b = new Example();

// Method is shared
console.log(a.getValue === b.getValue); // true

// Arrow function property is not shared
console.log(a.getValueArrow === b.getValueArrow); // false

// Performance implication: Arrow functions create new closures per instance
// Use methods when performance is critical
// Use arrow functions when you need lexical 'this'
```

---

## Arrow Function vs Function Expression

Key differences between arrow functions and function expressions.

```typescript
// 1. Syntax
const addArrow = (a: number, b: number): number => a + b;
const addExpression = function (a: number, b: number): number {
  return a + b;
};

// 2. 'this' binding
class Context {
  value = 10;

  // Arrow: 'this' is Context
  arrowMethod = () => this.value;

  // Expression: 'this' depends on call
  expressionMethod = function () {
    return this.value;
  };
}

// 3. Arguments object
const arrowFunc = (...args: number[]) => args; // Use rest params
const expressionFunc = function () {
  return arguments; // Has arguments object
};

// 4. Constructor
// const Arrow = new (class Arrow { /* ... */ })(); // Arrow functions can't be constructors
const Expression = function (this: { name: string }) {
  this.name = "test";
};

// 5. Prototype
// Arrow functions don't have prototype
console.log(typeof arrowFunc.prototype); // undefined
console.log(typeof addExpression.prototype); // object

// 6. Generator functions
// Arrow functions cannot be generators
// const gen = function* () { yield 1; }; // OK
// const genArrow = *() => { yield 1; }; // Error

// 7. Hoisting
// Function expressions are NOT hoisted (like arrow functions)
// console.log(hoisted()); // Error
// function hoisted() { return 1; } // Function declaration IS hoisted
```

---

## Implicit Return with Arrow Functions

Arrow functions allow concise body syntax with implicit returns.

```typescript
// Explicit return (block body)
const addExplicit = (a: number, b: number): number => {
  return a + b;
};

// Implicit return (concise body)
const addImplicit = (a: number, b: number): number => a + b;

// Implicit return with object (needs parentheses)
const createUser = (name: string, age: number) => ({
  name,
  age,
  createdAt: new Date(),
});

// Implicit return with array
const range = (start: number, end: number): number[] =>
  Array.from({ length: end - start + 1 }, (_, i) => start + i);

// Implicit return with conditional
const clamp = (value: number, min: number, max: number): number =>
  Math.min(Math.max(value, min), max);

// Implicit return with template literal
const formatCurrency = (amount: number, currency: string = "USD"): string =>
  `${currency} ${amount.toFixed(2)}`;

// Implicit return with destructuring
const getFirstAndLast = <T>([first, ...rest]: T[]): [T, T] =>
  [first, rest[rest.length - 1]];

// Complex implicit returns (be careful with readability)
const processScore = (score: number): string =>
  score >= 90 ? "A" :
  score >= 80 ? "B" :
  score >= 70 ? "C" :
  score >= 60 ? "D" : "F";
```

---

## Arrow Functions and Generics

Arrow functions work with generics, but syntax has some nuances.

```typescript
// Generic arrow function with explicit type parameter
const identity = <T>(x: T): T => x;

// Generic arrow function with constraints
const getProperty = <T, K extends keyof T>(obj: T, key: K): T[K] =>
  obj[key];

// Generic arrow function in array methods
const unique = <T>(items: T[]): T[] => [...new Set(items)];

const groupBy = <T, K extends string | number>(
  items: T[],
  keyFn: (item: T) => K
): Record<K, T[]> =>
  items.reduce((groups, item) => {
    const key = keyFn(item);
    return { ...groups, [key]: [...(groups[key] || []), item] };
  }, {} as Record<K, T[]>);

// Generic arrow function with default type
const createArray = <T = unknown>(length: number, fill: T): T[] =>
  Array(length).fill(fill);

// Generic arrow function with complex constraints
const sortBy = <T extends Record<string, unknown>>(
  items: T[],
  key: keyof T,
  order: "asc" | "desc" = "asc"
): T[] =>
  [...items].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    const comparison = String(aVal).localeCompare(String(bVal));
    return order === "asc" ? comparison : -comparison;
  });

// React-style generic arrow function
const useState = <T>(initialValue: T): [T, (newValue: T) => void] => {
  let value = initialValue;
  const setValue = (newValue: T) => {
    value = newValue;
  };
  return [value, setValue];
};
```

---

## Readonly This

Using `readonly this` parameter to prevent method chaining modifications.

```typescript
// readonly this prevents modification of the instance
class Calculator {
  private result = 0;

  add(n: number): this {
    this.result += n;
    return this;
  }

  subtract(n: number): this {
    this.result -= n;
    return this;
  }

  getValue(): number {
    return this.result;
  }
}

// With readonly this, TypeScript prevents reassignment
class ImmutableCalc {
  private readonly result: number;

  constructor(result: number = 0) {
    this.result = result;
  }

  add(n: number): ImmutableCalc {
    return new ImmutableCalc(this.result + n);
  }

  subtract(n: number): ImmutableCalc {
    return new ImmutableCalc(this.result - n);
  }

  getValue(): number {
    return this.result;
  }
}

// Arrow functions with readonly this
class Config {
  readonly apiUrl: string;
  readonly timeout: number;

  constructor(apiUrl: string, timeout: number) {
    this.apiUrl = apiUrl;
    this.timeout = timeout;
  }

  // Arrow function that returns new instance (immutable update)
  withUrl = (newUrl: string): Config =>
    new Config(newUrl, this.timeout);

  withTimeout = (newTimeout: number): Config =>
    new Config(this.apiUrl, newTimeout);
}
```

---

## Advanced Patterns

```typescript
// Currying with arrow functions
const curry = <A extends unknown[], R>(
  fn: (...args: A) => R
): ((...args: Partial<A>) => (...args: any[]) => R) | ((...args: A) => R) => {
  const arity = fn.length;
  const curried = (...args: unknown[]): unknown =>
    args.length >= arity
      ? fn(...(args as A))
      : (...moreArgs: unknown[]) => curried(...args, ...moreArgs);
  return curried as any;
};

// Function composition with arrow functions
const compose = <A, B, C>(
  f: (b: B) => C,
  g: (a: A) => B
): ((a: A) => C) =>
  (a) => f(g(a));

const pipe = <A, B>(f: (a: A) => B) => (g: (b: B) => C) => (...args: unknown[]) =>
  g(f(...args));

// Memoization with arrow functions
const memoize = <Args extends unknown[], R>(
  fn: (...args: Args) => R
): ((...args: Args) => R) => {
  const cache = new Map<string, R>();
  return (...args: Args): R => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};

// Throttle with arrow functions
const throttle = <Args extends unknown[], R>(
  fn: (...args: Args) => R,
  delay: number
): ((...args: Args) => R | undefined) => {
  let lastCall = 0;
  return (...args: Args): R | undefined => {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      return fn(...args);
    }
    return undefined;
  };
};
```

---

## Best Practices

```typescript
// 1. Use arrow functions for callbacks
numbers.map((n) => n * 2); // GOOD
numbers.map(function (n) { return n * 2; }); // Less ideal

// 2. Use regular functions for object methods
const obj = {
  name: "test",
  // BAD: Arrow function as method
  getName: () => this.name, // 'this' is wrong
  // GOOD: Regular function as method
  getName() { return this.name; },
};

// 3. Be explicit about return types for public APIs
export const processData = (input: string): ProcessedData => {
  // Implementation
};

// 4. Use concise body for simple operations
const double = (x: number) => x * 2;
const isPositive = (n: number) => n > 0;

// 5. Use block body for complex operations
const complexOperation = (data: InputData): OutputData => {
  const validated = validate(data);
  const transformed = transform(validated);
  return format(transformed);
};

// 6. Consider performance for class methods
// Arrow functions create new closures per instance
// Use methods when you have many instances
class MyClass {
  // Method is more memory-efficient
  process() { return this.value * 2; }
  // Arrow function preserves 'this' but uses more memory
  processArrow = () => this.value * 2;
}
```

---

## Interview Questions

### Q1: What is the difference between arrow functions and regular functions in TypeScript?

**Answer:** Arrow functions: (1) don't have their own `this` binding, (2) can't be used as constructors, (3) don't have `arguments` object, (4) can't be generators, (5) have concise syntax. Regular functions have all these features.

### Q2: When should you use arrow functions vs regular functions?

**Answer:** Use arrow functions for callbacks, array methods, and when you need lexical `this`. Use regular functions for object methods, constructors, and when you need `this` to depend on call context.

### Q3: Why can't arrow functions be used as constructors?

**Answer:** Arrow functions lack a `prototype` property and don't have their own `this` binding. The `new` keyword requires these to create and initialize objects properly.

### Q4: What is lexical `this` in arrow functions?

**Answer:** Arrow functions inherit `this` from the enclosing lexical scope (the surrounding non-arrow function or global scope). This makes them ideal for callbacks where you need access to the outer context.
