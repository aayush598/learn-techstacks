# Recursion in TypeScript

## Table of Contents

1. [Recursive Function Typing](#recursive-function-typing)
2. [Tail Recursion](#tail-recursion)
3. [Type-Safe Recursion](#type-safe-recursion)
4. [Recursive Type Inference](#recursive-type-inference)
5. [Memoized Recursion](#memoized-recursion)
6. [Tree Traversal with Recursion](#tree-traversal-with-recursion)
7. [Stack Overflow Prevention](#stack-overflow-prevention)
8. [Trampolining](#trampolining)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Recursive Function Typing

Recursive functions call themselves. TypeScript requires explicit return types for recursive functions in many cases.

```typescript
// Basic recursion: factorial
function factorial(n: number): number {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

console.log(factorial(5)); // 120

// Recursive countdown
function countdown(n: number): string[] {
  if (n <= 0) return ["Done!"];
  return [`${n}...`, ...countdown(n - 1)];
}

console.log(countdown(5)); // ["5...", "4...", "3...", "2...", "1...", "Done!"]

// Fibonacci with explicit return type (required for recursion)
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// Recursive string reversal
function reverseString(str: string): string {
  if (str.length <= 1) return str;
  return reverseString(str.slice(1)) + str[0];
}

console.log(reverseString("hello")); // "olleh"

// Recursive sum
function sumArray(arr: number[]): number {
  if (arr.length === 0) return 0;
  const [first, ...rest] = arr;
  return first + sumArray(rest);
}

// Recursive power
function power(base: number, exponent: number): number {
  if (exponent === 0) return 1;
  if (exponent < 0) return 1 / power(base, -exponent);
  return base * power(base, exponent - 1);
}
```

### More Recursive Examples

```typescript
// Recursive flatten
function flatten<T>(arr: (T | T[])[]): T[] {
  const result: T[] = [];
  for (const item of arr) {
    if (Array.isArray(item)) {
      result.push(...flatten(item));
    } else {
      result.push(item);
    }
  }
  return result;
}

console.log(flatten([1, [2, 3], [4, [5, 6]]])); // [1, 2, 3, 4, 5, 6]

// Recursive deep clone
function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) return obj.map(deepClone) as T;

  const cloned = {} as T;
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      cloned[key] = deepClone(obj[key]);
    }
  }
  return cloned;
}

// Recursive GCD (Greatest Common Divisor)
function gcd(a: number, b: number): number {
  if (b === 0) return a;
  return gcd(b, a % b);
}

// Recursive binary search
function binarySearch(
  arr: number[],
  target: number,
  low: number = 0,
  high: number = arr.length - 1
): number {
  if (low > high) return -1;

  const mid = Math.floor((low + high) / 2);

  if (arr[mid] === target) return mid;
  if (arr[mid] < target) return binarySearch(arr, target, mid + 1, high);
  return binarySearch(arr, target, low, mid - 1);
}

// Recursive permutations
function permutations<T>(arr: T[]): T[][] {
  if (arr.length <= 1) return [arr];

  const result: T[][] = [];

  for (let i = 0; i < arr.length; i++) {
    const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
    const perms = permutations(rest);

    for (const perm of perms) {
      result.push([arr[i], ...perm]);
    }
  }

  return result;
}

console.log(permutations([1, 2, 3]));
// [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

---

## Tail Recursion

Tail recursion places the recursive call as the last operation, enabling optimization.

```typescript
// NOT tail-recursive (must multiply after returning)
function factorialNotTail(n: number): number {
  if (n <= 1) return 1;
  return n * factorialNotTail(n - 1); // Multiplication happens AFTER recursive call
}

// Tail-recursive (accumulator pattern)
function factorialTail(n: number, acc: number = 1): number {
  if (n <= 1) return acc;
  return factorialTail(n - 1, n * acc); // Recursive call is the LAST operation
}

console.log(factorialTail(5)); // 120

// Tail-recursive fibonacci
function fibonacciTail(n: number, a: number = 0, b: number = 1): number {
  if (n === 0) return a;
  if (n === 1) return b;
  return fibonacciTail(n - 1, b, a + b);
}

// Tail-recursive sum
function sumTail(arr: number[], index: number = 0, acc: number = 0): number {
  if (index >= arr.length) return acc;
  return sumTail(arr, index + 1, acc + arr[index]);
}

// Tail-recursive power
function powerTail(base: number, exp: number, acc: number = 1): number {
  if (exp === 0) return acc;
  if (exp < 0) return powerTail(base, exp + 1, acc / base);
  return powerTail(base, exp - 1, acc * base);
}

// Tail-recursive flatten
function flattenTail<T>(
  arr: (T | T[])[],
  index: number = 0,
  acc: T[] = []
): T[] {
  if (index >= arr.length) return acc;

  const item = arr[index];
  if (Array.isArray(item)) {
    return flattenTail(arr, index + 1, [...acc, ...item]);
  }
  return flattenTail(arr, index + 1, [...acc, item]);
}

// Helper: Convert non-tail to tail-recursive with accumulator
function toTailRecursive<T, U>(
  fn: (arr: T[], index: number, acc: U) => U,
  identity: U
): (arr: T[]) => U {
  return (arr: T[]) => fn(arr, 0, identity);
}

const sum = toTailRecursive<number, number>(
  (arr, i, acc) => (i >= arr.length ? acc : sum(arr, i + 1, acc + arr[i])),
  0
);
```

---

## Type-Safe Recursion

Ensuring recursive functions are type-safe at compile time.

```typescript
// Recursive type for nested arrays
type NestedArray<T> = T | NestedArray<T>[];

function flattenDeep<T>(arr: NestedArray<T>[]): T[] {
  const result: T[] = [];
  for (const item of arr) {
    if (Array.isArray(item)) {
      result.push(...flattenDeep(item));
    } else {
      result.push(item);
    }
  }
  return result;
}

// Recursive type for linked lists
type LinkedList<T> = { value: T; next: LinkedList<T> } | null;

function listLength<T>(list: LinkedList<T>): number {
  if (list === null) return 0;
  return 1 + listLength(list.next);
}

function listToArray<T>(list: LinkedList<T>): T[] {
  if (list === null) return [];
  return [list.value, ...listToArray(list.next)];
}

// Recursive type for trees
interface TreeNode<T> {
  value: T;
  children: TreeNode<T>[];
}

function treeDepth<T>(node: TreeNode<T>): number {
  if (node.children.length === 0) return 1;
  return 1 + Math.max(...node.children.map(treeDepth));
}

function treeSize<T>(node: TreeNode<T>): number {
  return 1 + node.children.reduce((sum, child) => sum + treeSize(child), 0);
}

// Recursive conditional type
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Recursive omit type
type DeepOmit<T, K extends string> = {
  [P in keyof T as P extends K ? never : P]: T[P] extends object
    ? DeepOmit<T[P], K>
    : T[P];
};

// Type-safe recursive function with generics
function mapTree<T, U>(node: TreeNode<T>, fn: (value: T) => U): TreeNode<U> {
  return {
    value: fn(node.value),
    children: node.children.map((child) => mapTree(child, fn)),
  };
}
```

---

## Recursive Type Inference

Using TypeScript's type inference with recursive types.

```typescript
// Tuple length as a type
type Length<T extends unknown[]> = T["length"];

// Recursive tuple type
type BuildTuple<N extends number, T extends unknown[] = []> =
  T["length"] extends N ? T : BuildTuple<N, [...T, unknown]>;

// Recursive string manipulation
type Split<S extends string, D extends string> =
  S extends `${infer Head}${D}${infer Tail}`
    ? [Head, ...Split<Tail, D>]
    : [S];

type Result = Split<"a,b,c", ",">; // ["a", "b", "c"]

// Recursive object path
type GetNested<T, Path extends string> =
  Path extends `${infer Head}.${infer Tail}`
    ? Head extends keyof T
      ? GetNested<T[Head], Tail>
      : never
    : Path extends keyof T
    ? T[Path]
    : never;

interface Config {
  db: {
    host: string;
    port: number;
    auth: {
      user: string;
      password: string;
    };
  };
}

type DbHost = GetNested<Config, "db.host">; // string
type DbUser = GetNested<Config, "db.auth.user">; // string

// Recursive template literal type
type CamelToSnake<S extends string> =
  S extends `${infer Head}${infer Tail}`
    ? Head extends Uppercase<Head>
      ? Head extends Lowercase<Head>
        ? `${Head}${CamelToSnake<Tail>}`
        : `_${Lowercase<Head>}${CamelToSnake<Tail>}`
      : `${Head}${CamelToSnake<Tail>}`
    : S;

type SnakeCase = CamelToSnake<"helloWorld">; // "hello_world"
type SnakeCase2 = CamelToSnake<"firstName">; // "first_name"

// Recursive mapped type
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Recursive partial with depth control
type PartialDepth<T, Depth extends number, Current extends unknown[] = []> =
  Current["length"] extends Depth
    ? Partial<T>
    : {
        [P in keyof T]?: T[P] extends object
          ? PartialDepth<T[P], Depth, [...Current, unknown]>
          : T[P];
      };
```

---

## Memoized Recursion

Combining memoization with recursion for performance.

```typescript
// Basic memoized recursion
function memoizedFactorial(n: number): number {
  const cache = new Map<number, number>();

  function fact(n: number): number {
    if (n <= 1) return 1;
    if (cache.has(n)) return cache.get(n)!;
    const result = n * fact(n - 1);
    cache.set(n, result);
    return result;
  }

  return fact(n);
}

// Generic memoization wrapper
function memoize<T extends (...args: any[]) => any>(
  fn: T
): T {
  const cache = new Map<string, ReturnType<T>>();

  return ((...args: any[]) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

// Memoized fibonacci
const fib = memoize((n: number): number => {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
});

console.log(fib(100)); // Fast! Without memoization this would be impossible

// Memoized tree traversal
const memoizedTreeDepth = memoize(<T>(node: TreeNode<T>): number => {
  if (node.children.length === 0) return 1;
  return 1 + Math.max(...node.children.map(memoizedTreeDepth));
});

// Memoized withLRU cache
function memoizeWithLRU<T extends (...args: any[]) => any>(
  fn: T,
  maxSize: number
): T {
  const cache = new Map<string, ReturnType<T>>();

  return ((...args: any[]) => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      const value = cache.get(key)!;
      cache.delete(key);
      cache.set(key, value);
      return value;
    }

    const result = fn(...args);

    if (cache.size >= maxSize) {
      const firstKey = cache.keys().next().value!;
      cache.delete(firstKey);
    }

    cache.set(key, result);
    return result;
  }) as T;
}

// Practical: Memoized recursive directory scanner
const scanDir = memoize((path: string): string[] => {
  const results: string[] = [path];
  const entries = readDirectory(path);

  for (const entry of entries) {
    if (isDirectory(entry)) {
      results.push(...scanDir(joinPath(path, entry)));
    } else {
      results.push(joinPath(path, entry));
    }
  }

  return results;
});
```

---

## Tree Traversal with Recursion

Recursive patterns for tree data structures.

```typescript
// Binary tree definition
interface BinaryTreeNode<T> {
  value: T;
  left: BinaryTreeNode<T> | null;
  right: BinaryTreeNode<T> | null;
}

// In-order traversal (Left, Root, Right)
function inOrder<T>(node: BinaryTreeNode<T> | null): T[] {
  if (node === null) return [];
  return [...inOrder(node.left), node.value, ...inOrder(node.right)];
}

// Pre-order traversal (Root, Left, Right)
function preOrder<T>(node: BinaryTreeNode<T> | null): T[] {
  if (node === null) return [];
  return [node.value, ...preOrder(node.left), ...preOrder(node.right)];
}

// Post-order traversal (Left, Right, Root)
function postOrder<T>(node: BinaryTreeNode<T> | null): T[] {
  if (node === null) return [];
  return [...postOrder(node.left), ...postOrder(node.right), node.value];
}

// Level-order traversal (BFS using recursion with helper)
function levelOrder<T>(node: BinaryTreeNode<T> | null): T[][] {
  const result: T[][] = [];

  function traverse(node: BinaryTreeNode<T> | null, level: number): void {
    if (node === null) return;

    if (!result[level]) result[level] = [];
    result[level].push(node.value);

    traverse(node.left, level + 1);
    traverse(node.right, level + 1);
  }

  traverse(node, 0);
  return result;
}

// Search in binary tree
function search<T>(
  node: BinaryTreeNode<T> | null,
  target: T
): boolean {
  if (node === null) return false;
  if (node.value === target) return true;
  return search(node.left, target) || search(node.right, target);
}

// Count nodes
function countNodes<T>(node: BinaryTreeNode<T> | null): number {
  if (node === null) return 0;
  return 1 + countNodes(node.left) + countNodes(node.right);
}

// Find height
function height<T>(node: BinaryTreeNode<T> | null): number {
  if (node === null) return 0;
  return 1 + Math.max(height(node.left), height(node.right));
}

// Check if balanced
function isBalanced<T>(node: BinaryTreeNode<T> | null): boolean {
  if (node === null) return true;

  const leftHeight = height(node.left);
  const rightHeight = height(node.right);

  return (
    Math.abs(leftHeight - rightHeight) <= 1 &&
    isBalanced(node.left) &&
    isBalanced(node.right)
  );
}

// Generic tree traversal
function traverseTree<T>(
  node: TreeNode<T>,
  visitor: (value: T, depth: number) => void,
  depth: number = 0
): void {
  visitor(node.value, depth);
  for (const child of node.children) {
    traverseTree(child, visitor, depth + 1);
  }
}

// Find path between two nodes
function findPath<T>(
  node: TreeNode<T> | null,
  target: T,
  path: T[] = []
): T[] | null {
  if (node === null) return null;

  path.push(node.value);

  if (node.value === target) return path;

  for (const child of node.children) {
    const result = findPath(child, target, [...path]);
    if (result) return result;
  }

  return null;
}
```

---

## Stack Overflow Prevention

Preventing stack overflow in deep recursion.

```typescript
// Problem: Deep recursion can cause stack overflow
function dangerousRecursion(n: number): number {
  if (n === 0) return 0;
  return dangerousRecursion(n - 1) + 1;
}

// dangerousRecursion(100000); // RangeError: Maximum call stack size exceeded

// Solution 1: Convert to iteration
function safeIteration(n: number): number {
  let result = 0;
  for (let i = 0; i < n; i++) {
    result += 1;
  }
  return result;
}

// Solution 2: Tail recursion (if engine supports TCO)
function tailRecursive(n: number, acc: number = 0): number {
  if (n === 0) return acc;
  return tailRecursive(n - 1, acc + 1);
}

// Solution 3: Trampolining
function trampoline<T>(
  fn: (...args: any[]) => T | (() => T)
): (...args: any[]) => T {
  return function (...args: any[]): T {
    let result = fn(...args);

    while (typeof result === "function") {
      result = result();
    }

    return result;
  };
}

// Solution 4: Chunked processing
function processInChunks<T, U>(
  items: T[],
  processor: (chunk: T[]) => U,
  chunkSize: number = 1000
): U[] {
  const results: U[] = [];

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    results.push(processor(chunk));
  }

  return results;
}

// Solution 5: Using async/await to break up stack
async function asyncRecursion(n: number): Promise<number> {
  if (n === 0) return 0;

  // Yield to event loop every N iterations
  if (n % 1000 === 0) {
    await new Promise((resolve) => setTimeout(resolve, 0));
  }

  return asyncRecursion(n - 1) + 1;
}

// Solution 6: Explicit stack (simulating recursion iteratively)
function iterativeDFS<T>(root: TreeNode<T>): T[] {
  const stack: Array<{ node: TreeNode<T>; depth: number }> = [{ node: root, depth: 0 }];
  const result: T[] = [];

  while (stack.length > 0) {
    const { node } = stack.pop()!;
    result.push(node.value);

    // Push children in reverse order for left-to-right traversal
    for (let i = node.children.length - 1; i >= 0; i--) {
      stack.push({ node: node.children[i], depth: 1 });
    }
  }

  return result;
}
```

---

## Trampolining

Technique to avoid stack overflow by converting recursion to iteration.

```typescript
// Trampoline function type
type Thunk<T> = () => T | Trampoline<T>;

class Trampoline<T> {
  constructor(private readonly fn: Thunk<T>) {}

  evaluate(): T {
    let result: T | Trampoline<T> = this;

    while (result instanceof Trampoline) {
      result = result.fn();
    }

    return result;
  }
}

function trampoline<T>(fn: (...args: any[]) => T | Trampoline<T>) {
  return (...args: any[]): T => {
    const trampolined = new Trampoline<T>(() => fn(...args));
    return trampolined.evaluate();
  };
}

// Usage: Convert recursive factorial to trampolined version
function factorialThunk(n: number, acc: number = 1): number | Trampoline<number> {
  if (n <= 1) return acc;
  return new Trampoline(() => factorialThunk(n - 1, n * acc));
}

const safeFactorial = trampoline(factorialThunk);
console.log(safeFactorial(100000)); // Works! No stack overflow

// Trampolined fibonacci
function fibThunk(n: number, a: number = 0, b: number = 1): number | Trampoline<number> {
  if (n === 0) return a;
  if (n === 1) return b;
  return new Trampoline(() => fibThunk(n - 1, b, a + b));
}

const safeFib = trampoline(fibThunk);
console.log(safeFib(100000)); // Fast and safe!

// Simpler trampoline using functions directly
function simpleTrampoline<A extends unknown[], R>(
  fn: (...args: A) => R | (() => R | (() => R))
): (...args: A) => R {
  return (...args: A): R => {
    let result = fn(...args);
    while (typeof result === "function") {
      result = result();
    }
    return result as R;
  };
}

// Practical example: Deep tree processing without stack overflow
function flattenTree<T>(node: TreeNode<T>): T[] {
  const stack: TreeNode<T>[] = [node];
  const result: T[] = [];

  while (stack.length > 0) {
    const current = stack.pop()!;
    result.push(current.value);

    for (const child of current.children) {
      stack.push(child);
    }
  }

  return result;
}
```

---

## Best Practices

```typescript
// 1. Always define a base case
function recursion(n: number): number {
  if (n <= 0) return 0; // Base case - MUST have this
  return recursion(n - 1) + 1;
}

// 2. Use tail recursion when possible
function factorial(n: number, acc: number = 1): number {
  if (n <= 1) return acc;
  return factorial(n - 1, n * acc); // Tail position
}

// 3. Memoize expensive recursive functions
const fib = memoize((n: number): number => {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
});

// 4. Add explicit return types for recursive functions
function depth<T>(node: TreeNode<T> | null): number {
  if (node === null) return 0;
  return 1 + Math.max(...node.children.map(depth));
}

// 5. Consider iteration for very deep recursion
function safeProcess(n: number): number {
  let result = 0;
  for (let i = 0; i < n; i++) {
    result += 1;
  }
  return result;
}

// 6. Use trampolining for guaranteed stack safety
const safeRecursion = trampoline((n: number, acc: number = 0): number | Trampoline<number> => {
  if (n === 0) return acc;
  return new Trampoline(() => safeRecursion(n - 1, acc + 1));
});

// 7. Document recursion depth expectations
/** Computes factorial. Max safe depth: ~10,000 (varies by runtime). */
function documentedFactorial(n: number): number {
  if (n <= 1) return 1;
  return n * documentedFactorial(n - 1);
}
```

---

## Interview Questions

### Q1: What is tail recursion and why is it important?

**Answer:** Tail recursion is when the recursive call is the last operation in the function. It allows engines to optimize by reusing the current stack frame, preventing stack overflow for deep recursion. Not all TypeScript/JavaScript engines support this optimization.

### Q2: How do you prevent stack overflow in recursive functions?

**Answer:** Several approaches: (1) Convert to iteration, (2) Use tail recursion with TCO-capable engines, (3) Use trampolining, (4) Process in chunks with async/await, (5) Use explicit stack data structure.

### Q3: When should you use recursion vs iteration?

**Answer:** Use recursion for: tree/graph traversal, divide-and-conquer algorithms, problems with recursive structure (fibonacci, permutations). Use iteration for: simple loops, performance-critical code, deep recursion that might overflow the stack.

### Q4: What is memoized recursion?

**Answer:** Memoized recursion combines memoization with recursive functions to cache previously computed results, eliminating redundant calculations. This reduces time complexity from exponential to linear for problems like fibonacci.
