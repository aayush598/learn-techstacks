# JavaScript Interview Questions and Answers - Part 2

## Q1: How does JavaScript's `Proxy` object work?
**A:** `Proxy` enables creating custom behavior for fundamental operations on objects. It wraps a target object and intercepts operations via handler methods called traps. Common traps: `get`, `set`, `has`, `deleteProperty`, `apply`, `construct`, `getPrototypeOf`, `setPrototypeOf`, `isExtensible`, `preventExtensions`, `getOwnPropertyDescriptor`, `defineProperty`, `ownKeys`, `enumerate`. Proxies are used for: validation, logging, memoization, lazy initialization, data binding, revocable references, and implementing domain-specific languages. `Proxy.revocable()` creates a revocable proxy. Proxies don't have a `this` context — `this` in traps refers to the handler, not the proxy. They're transparent to the target but not to identity checks (`===`).

## Q2: What are JavaScript iterators and the iteration protocol?
**A:** The iteration protocol has two parts: `Iterable` (object with `Symbol.iterator` method) and `Iterator` (object with `next()` method returning `{value, done}`). Built-in iterables: Arrays, Strings, Maps, Sets, NodeLists, TypedArrays, arguments. Custom iterables implement `[Symbol.iterator]()`. The `for...of` loop consumes iterables. `spread` operator (`...`), `Array.from()`, and destructuring also work with iterables. `Generator` functions return iterators. `return()` and `throw()` methods on iterators allow early termination. Async iteration uses `Symbol.asyncIterator` with `next()` returning promises, consumed by `for await...of`.

## Q3: How does `Object.create()` differ from constructor functions or classes?
**A:** `Object.create(proto, propertiesObject)` creates a new object with the specified prototype and optional property descriptors. It enables explicit prototypal inheritance without constructors. Unlike constructors (which run initialization code) or classes (syntactic sugar over constructors), `Object.create` directly sets up the prototype chain. It's useful for: creating objects with `null` prototype (`Object.create(null)` — no inherited properties), implementing the prototype without running side effects, and composing behavior through prototype chains. `Object.create` is the purest form of prototypal inheritance in JavaScript.

## Q4: What are JavaScript `TypedArrays` and when should they be used?
**A:** `TypedArray` (actually `Int8Array`, `Uint8Array`, `Uint8ClampedArray`, `Int16Array`, `Uint16Array`, `Int32Array`, `Uint32Array`, `Float32Array`, `Float64Array`, `BigInt64Array`, `BigUint64Array`) provide array-like views over binary data buffers. They store data in contiguous memory with fixed types. Use cases: WebGL graphics, audio processing, video manipulation, file parsing, network protocols, WebAssembly interop, and any performance-critical numeric computation. TypedArrays are created from `ArrayBuffer` (raw memory). `DataView` provides flexible access to `ArrayBuffer` with explicit byte offsets and endianness. They offer better performance and memory usage than regular Arrays for numeric data.

## Q5: Explain JavaScript's `WeakMap` and `WeakSet`.
**A:** `WeakMap` and `WeakSet` hold "weak" references to their keys (objects only, not primitives). If no other references to a key exist, the key-value pair is garbage collected. WeakMap keys are not enumerable — there's no way to iterate or inspect WeakMap contents. Use cases: (1) private data attached to objects without preventing GC, (2) caching/computed values associated with objects, (3) DOM element metadata (when DOM nodes are removed, associated data is freed), (4) preventing memory leaks in long-lived applications. WeakSet holds unique objects weakly. Neither WeakMap nor WeakSet has `size` property or iteration methods. `FinalizationRegistry` (ES2021) provides callbacks when objects are garbage collected.

## Q6: How does JavaScript's `Reflect` API work?
**A:** `Reflect` (ES2015) is a built-in object with methods for interceptable JavaScript operations. Every `Proxy` trap has a corresponding `Reflect` method: `Reflect.get()`, `Reflect.set()`, `Reflect.has()`, `Reflect.deleteProperty()`, `Reflect.construct()`, `Reflect.apply()`, `Reflect.defineProperty()`, `Reflect.getPrototypeOf()`, `Reflect.setPrototypeOf()`, `Reflect.isExtensible()`, `Reflect.preventExtensions()`, `Reflect.getOwnPropertyDescriptor()`, `Reflect.ownKeys()`. Using `Reflect` methods in Proxy traps provides default behavior and ensures proper `this` binding. Unlike older methods (like `delete` operator or `in` operator), `Reflect` methods return success values instead of throwing exceptions.

## Q7: What is the difference between `Object.freeze()`, `Object.seal()`, and `Object.preventExtensions()`?
**A:** `Object.preventExtensions(obj)` prevents adding new properties but allows deleting and modifying existing ones. `Object.seal(obj)` calls `preventExtensions` plus makes all properties non-configurable (can't delete or change property descriptors). Existing writable properties can still be modified. `Object.freeze(obj)` calls `seal` plus makes all properties non-writable (read-only). All three are shallow — they affect only direct properties, not nested objects. Freezing/sealing in strict mode throws `TypeError` on violations; in sloppy mode, they silently fail. `Object.isFrozen()`, `Object.isSealed()`, `Object.isExtensible()` check the state. These are used for immutability patterns and defensive programming.

## Q8: How do you detect JavaScript data types accurately?
**A:** Detection methods: (1) `typeof` — works for primitives (`string`, `number`, `boolean`, `undefined`, `symbol`, `bigint`) but returns `"object"` for `null` and most objects, (2) `Object.prototype.toString.call(value)` — returns `"[object Type]"` (most reliable), e.g., `"[object Array]"`, `"[object Null]"`, `"[object Date]"`, `"[object RegExp]"`, (3) `Array.isArray()` — best for arrays, (4) `instanceof` — checks prototype chain (fails across realms/iframes), (5) `value.constructor` — unreliable (can be modified), (6) duck typing — check for capabilities rather than types. The most robust approach: `Object.prototype.toString.call(value).slice(8, -1).toLowerCase()`.

## Q9: Explain the difference between `Object.assign()` and the spread operator.
**A:** Both perform shallow copying of own enumerable properties. `Object.assign(target, ...sources)` mutates the target and returns it. Spread (`{...obj}`) creates a new object literal, doesn't mutate anything. `Object.assign` triggers setters on the target; spread doesn't (it defines new properties). Spread is more readable and commonly used for immutable updates. `Object.assign` is useful when you need to mutate an existing object or merge into a specific target. Both are shallow — nested objects are copied by reference. For deep cloning, use structured cloning (`structuredClone()`) or libraries like Lodash's `cloneDeep`.

## Q10: How does JavaScript's `Intl` object work for internationalization?
**A:** The `Intl` object provides language-sensitive string comparison, number formatting, date/time formatting, relative time formatting, list formatting, and collation. Key constructors: `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.Collator`, `Intl.ListFormat`, `Intl.RelativeTimeFormat`, `Intl.PluralRules`, `Intl.Segmenter` (ES2022). They accept locale strings (BCP 47 language tags) and options objects. Examples: `new Intl.DateTimeFormat('en-US', {dateStyle: 'full'}).format(date)`, `new Intl.NumberFormat('de-DE', {style: 'currency', currency: 'EUR'}).format(amount)`. `Intl.Collator` provides locale-aware string comparison with sensitivity options. `Intl` is built into modern browsers and Node.js, providing efficient native implementations.

## Q11: What are JavaScript `Symbol` types and their use cases?
**A:** `Symbol` (ES2015) is a unique, immutable primitive value used as object property keys. Each `Symbol()` call creates a unique symbol. `Symbol.for(key)` creates/retrieves registered global symbols. Use cases: (1) defining protocol methods (`Symbol.iterator`, `Symbol.asyncIterator`, `Symbol.hasInstance`), (2) creating "hidden" properties (unique keys that don't conflict with other code), (3) implementing metadata or internal state, (4) customizing language behavior via well-known symbols (`Symbol.toPrimitive`, `Symbol.toStringTag`, `Symbol.species`, `Symbol.match`, `Symbol.replace`, `Symbol.search`, `Symbol.split`, `Symbol.unscopables`). Symbols are not included in `for...in` or `Object.keys()` but are visible via `Object.getOwnPropertySymbols()` and `Reflect.ownKeys()`.

## Q12: How does the Event Loop work with `requestAnimationFrame` and `requestIdleCallback`?
**A:** The event loop processes tasks in phases: macrotasks (setTimeout, setInterval, I/O, UI rendering), microtasks (Promise callbacks, queueMicrotask, MutationObserver), and rendering. `requestAnimationFrame(callback)` schedules the callback before the next repaint, making it ideal for animations — the callback receives a high-resolution timestamp. `requestIdleCallback(callback)` schedules the callback during idle periods (when the event loop has no high-priority work). Both are scheduled per rendering frame. Microtasks are processed after each macrotask but before rendering. `requestAnimationFrame` callbacks run before rendering/repaint but after microtasks. Task prioritization varies across environments.

## Q13: Explain JavaScript's `BigInt` and its limitations.
**A:** `BigInt` (ES2020) represents integers of arbitrary precision, created via `BigInt(value)` or `123n` suffix. It enables operations on integers larger than `Number.MAX_SAFE_INTEGER` (2^53 - 1). Limitations: (1) cannot mix with regular `Number` in operations (`1n + 1` throws TypeError), (2) `Math` object methods don't support BigInt, (3) BigInt loses precision when converted to Number (use explicit `Number()` or `toString()`), (4) not JSON-serializable by default (requires custom `toJSON`), (5) division truncates toward zero (no fractional part), (6) unary `+` operator not supported, (7) bitwise operations only work with other BigInts. BigInt operations are slower than Number operations.

## Q14: What are JavaScript modules (ESM) and how do they differ from CommonJS?
**A:** ES modules (ESM) are the official JavaScript module system (ES2015). Syntax: `import`/`export`. They're static — imports/exports are resolved at parse time, enabling tree shaking and dead code elimination. ESM supports named exports, default exports, and re-exports. ESM runs in strict mode by default and has lexical `this` at top level (`undefined`). CommonJS (Node.js) uses `require()`/`module.exports` — dynamic loading, module wrapping, and `this` equals `exports`. ESM is asynchronous (using promises), while CommonJS is synchronous. ESM supports top-level `await`; CommonJS doesn't. ESM can import CommonJS modules (default export), but CommonJS cannot `require` ESM modules (use dynamic `import()`).

## Q15: How does JavaScript's `structuredClone()` work?
**A:** `structuredClone(value, transfer)` (ES2022) creates a deep clone of a value using the structured clone algorithm. It handles: objects, arrays, primitives, `Date`, `RegExp`, `Map`, `Set`, `Blob`, `File`, `ImageData`, `ArrayBuffer`, `TypedArray`, and circular references. It does NOT handle: functions, DOM elements, Error objects, WeakMap, WeakSet, Symbols, prototype chain (clones are plain objects). The `transfer` option moves `ArrayBuffer` ownership (zero-copy). `structuredClone` is safer and faster than `JSON.parse(JSON.stringify())` — it preserves `undefined`, `Infinity`, `NaN`, `BigInt`, and circular references. It's available in browsers and Node.js 17+.

## Q16: What are JavaScript `Atomics` and `SharedArrayBuffer`?
**A:** `SharedArrayBuffer` allows multiple threads (Web Workers) to share a fixed-length binary data buffer. `Atomics` provides static methods for thread-safe operations on `SharedArrayBuffer`: `Atomics.add()`, `Atomics.sub()`, `Atomics.and()`, `Atomics.or()`, `Atomics.xor()`, `Atomics.exchange()`, `Atomics.compareExchange()`, `Atomics.load()`, `Atomics.store()`, `Atomics.wait()`, `Atomics.notify()`, `Atomics.isLockFree()`. These ensure atomic read-modify-write operations and provide wait/notify synchronization primitives. `Atomics.wait()` (available in browsers but not all contexts) blocks the thread until notified. Used in advanced parallelism patterns, game engines, and high-performance computing in the browser.

## Q17: How do you handle concurrency with Web Workers?
**A:** Web Workers run JavaScript in background threads. Main thread creates workers via `new Worker('script.js')`. Communication uses `postMessage()` and `message` event (structured clone, not shared memory by default). Workers have no DOM access, no `window` object, and limited APIs. Types: Dedicated Workers (single owner), Shared Workers (multiple browsing contexts), Service Workers (network proxy, offline support). Workers can spawn sub-workers. `importScripts()` imports scripts in workers. For shared memory, use `SharedArrayBuffer` with `Atomics`. `Worker` termination: `worker.terminate()` from main thread or `close()` inside worker. Workers are heavyweight — pool them for frequent tasks.

## Q18: Explain the difference between `for...in` and `for...of`.
**A:** `for...in` iterates over enumerable string-keyed property keys (including inherited ones from prototype chain). It's intended for object property enumeration, not arrays. `for...of` iterates over values from iterable objects (arrays, strings, Maps, Sets, generators). `for...of` uses the Symbol.iterator protocol. `for...in` iterates keys (property names), `for...of` iterates values. `for...in` on arrays iterates indices as strings; `for...of` iterates elements. `for...in` includes inherited properties (filter with `hasOwnProperty`). `for...of` doesn't iterate prototype properties. Neither includes Symbol-keyed properties.

## Q19: How does JavaScript handle `this` in different contexts?
**A:** `this` is determined by the execution context: (1) Global context — `this` is `window` (browser) or `global` (Node.js) or `undefined` (ESM strict mode). (2) Function context — in strict mode, `this` is `undefined`; in sloppy mode, it's the global object. (3) Method call — `this` is the object the method is called on. (4) Constructor with `new` — `this` is the newly created instance. (5) Arrow functions — `this` is lexically bound from the enclosing scope (not re-bound). (6) `call`/`apply`/`bind` — `this` is explicitly set. (7) Event handlers — `this` is the element the handler is attached to (unless arrow function). (8) DOM event listener with `addEventListener` — `this` is the element.

## Q20: What are JavaScript's `Temporal` API and its advantages over `Date`?
**A:** The `Temporal` API (Stage 3, planned for ES2024+) is a modern date/time replacement for the legacy `Date` object. It provides: `Temporal.Now` (current time), `Temporal.Instant` (UTC timestamps), `Temporal.ZonedDateTime` (timezone-aware), `Temporal.PlainDate`, `Temporal.PlainTime`, `Temporal.PlainDateTime`, `Temporal.PlainYearMonth`, `Temporal.PlainMonthDay`, `Temporal.Duration`. Advantages over `Date`: (1) immutable objects, (2) proper timezone support (IANA time zones), (3) separate types for different date/time concepts, (4) human-readable API, (5) duration math, (6) calendar system support (non-Gregorian), (7) exact and wall-clock time separation, (8) ISO 8601 string parsing, (9) no mutation-side effects, (10) no epoch-centric behavior.

## Q21: How do you implement custom error types in JavaScript?
**A:** Extend the `Error` class:

```javascript
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ValidationError);
    }
  }
}
```

Custom errors should: extend `Error`, set the `name` property, capture stack trace, accept extra context properties. They enable precise error handling with `instanceof` checks. `Error.captureStackTrace` (V8-only) excludes the constructor from the stack trace. `cause` option (ES2022) chains errors: `new Error('message', { cause: originalError })`. Multiple custom errors can form a hierarchy. Always verify custom errors work with `instanceof` across different realms.

## Q22: What are JavaScript getters and setters?
**A:** Getters and setters are accessor properties that execute functions on property access. Defined with `get` and `set` syntax in object literals, classes, or via `Object.defineProperty()`. Getters are called when a property is read; setters when a property is assigned. They enable: computed properties, validation, lazy initialization, logging, encapsulation (private backing fields). Example:

```javascript
class User {
  #fullName;
  get fullName() { return this.#fullName; }
  set fullName(val) { this.#fullName = val.trim(); }
}
```

Getters should not have side effects. Setters can validate and transform values. Both are inherited via prototype chain. `Object.defineProperty` creates accessors on existing objects. `Object.getOwnPropertyDescriptor` distinguishes data vs accessor properties.

## Q23: How does JavaScript's `Generator.prototype.return()` and `Generator.prototype.throw()` work?
**A:** `generator.return(value)` terminates the generator at the current yield point, returning `{value, done: true}`. Inside the generator, any `finally` block executes before termination. `generator.throw(error)` throws an exception at the current yield point inside the generator. If caught, the generator can continue; otherwise, it terminates. These methods enable external control of generator execution. Combined with delegation (`yield*`), they allow sophisticated control flow. Both can be used to clean up resources when a generator is no longer needed. Return and throw cause the suspended yield to complete with the specified action.

## Q24: Explain the difference between `setTimeout(fn, 0)` and `queueMicrotask()`.
**A:** `setTimeout(fn, 0)` schedules a macrotask that runs after the current macrotask completes, after pending microtasks. `queueMicrotask(fn)` schedules a microtask that runs immediately after the current task completes, before any macrotasks. Microtasks are processed before the event loop continues to macrotasks. `queueMicrotask` callbacks run before `setTimeout` callbacks (even with 0 delay). Microtasks are used for promise-like callbacks, while `setTimeout` is used for deferring work to a later macrotask. Excessive microtask queuing can starve macrotasks (like rendering). `queueMicrotask` is preferred for promise-style sequencing without creating a Promise.

## Q25: What are JavaScript `tagged template literals`?
**A:** Tagged templates allow calling a function with a template literal. The function receives the string parts array and interpolated values as arguments:

```javascript
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => 
    result + str + (values[i] ? `<mark>${values[i]}</mark>` : ''), '');
}
const name = 'World';
highlight`Hello ${name}!`; // "Hello <mark>World</mark>!"
```

First argument: array of string literals (with a `raw` property for raw strings). Remaining arguments: interpolated values. Use cases: HTML escaping, localization, custom DSLs (like `styled-components` in React), SQL query building, and string sanitization. Tags can return any value, not just strings.

## Q26: How does JavaScript handle binary data with `Blob` and `File`?
**A:** `Blob` represents immutable raw binary data. Created via `new Blob(parts, options)` where parts are `Blob`, `BufferSource`, `String` (text), or `ArrayBuffer`. `File` extends `Blob` with name and lastModified metadata. `Blob` methods: `slice(start, end, type)`, `stream()`, `text()`, `arrayBuffer()`. Used with: `FileReader` (legacy), `URL.createObjectURL`, `Response` (fetch API), `File` from `<input type="file">`. `Blob` can be converted to other formats: `blob.arrayBuffer()`, `blob.text()`, `blob.stream()`. `FileReader` provides progress events for large blobs. Blobs are garbage-collected only when no references remain — revoke object URLs with `URL.revokeObjectURL()`.

## Q27: What are JavaScript static class fields and private static methods?
**A:** Static class fields (ES2022) define properties on the class constructor: `static count = 0`. Private static fields (`static #count = 0`) are only accessible within the class. Private static methods (`static #method() {}`) can only be called from other methods of the class. Static initialization blocks (`static {}`) run once when the class is evaluated, useful for complex static initialization. These features enable: shared counters, factory registries, private utility functions, and class-level configuration. Private static members follow the same privacy rules as private instance members — truly private at the language level (enforced by the engine).

## Q28: How does the `AbortController` and `AbortSignal` work?
**A:** `AbortController` provides a way to abort asynchronous operations. `controller.signal` is an `AbortSignal` passed to abortable APIs. `controller.abort()` triggers the signal, setting `signal.aborted` to `true` and dispatching an `abort` event. Supported APIs: `fetch()`, `addEventListener()`, `await`, `Blob`, `FileReader`, `Response`, streams, and custom async operations. AbortSignals can be combined: `AbortSignal.timeout(ms)` (ES2022) creates a signal that aborts after timeout. `AbortSignal.any([signals])` (ES2023) combines multiple signals. This is the standard pattern for cancellation in modern JavaScript, replacing ad-hoc cancellation flags.

## Q29: Explain JavaScript's `Intl.Segmenter` for locale-aware text segmentation.
**A:** `Intl.Segmenter` (ES2022) segments text into graphemes, words, or sentences respecting locale rules. Usage: `new Intl.Segmenter(locale, {granularity: 'grapheme'|'word'|'sentence'})`. Returns a `Segments` iterable — each segment has `segment`, `index`, and `input` properties. For word granularity, segments include `isWordLike` property. Essential for: proper text editing (cursor movement, selection), word counting, sentence boundary detection, and emoji handling (grapheme clusters like emoji sequences). Before `Intl.Segmenter`, text segmentation required complex regex or libraries. It correctly handles complex scripts (Thai, Japanese, Arabic) and emoji ZWJ sequences.

## Q30: What are JavaScript `Error` causes and error chaining?
**A:** The `cause` option (ES2022) chains errors: `throw new Error('Failed to process', { cause: originalError })`. The cause appears in the `.cause` property and in stack traces (V8, Firefox). Benefits: preserving the original error context when re-throwing, building error hierarchies, debugging multi-layered applications. Patterns:

```javascript
try {
  await db.query(...);
} catch (err) {
  throw new DatabaseError('Query failed', { cause: err });
}
```

Nested causes (`.cause.cause...`) track the full chain. `Error.prototype.stack` includes cause stacks in supporting engines. This replaces the common pattern of manually concatenating error messages.

## Q31: How does JavaScript's `Array.prototype.sort()` work and what are gotchas?
**A:** `Array.prototype.sort([compareFn])` sorts in-place and returns the array. Without compareFn, elements are converted to strings and sorted lexicographically (by UTF-16 code units). This causes `[1, 2, 10].sort()` to return `[1, 10, 2]`. Compare function returns negative (a before b), positive (b before a), or zero (equal order — stable sort since ES2019). Gotchas: (1) sorts in-place (mutates original), (2) default sort is lexicographic, (3) not stable before ES2019, (4) returns the same array reference (confusing with immutable patterns), (5) sparse arrays preserve empty slots, (6) performance varies across engines (TimSort in V8, QuickSort in older engines). Use `.slice().sort()` for immutable sorting.

## Q32: Explain the difference between `Object.keys()`, `Object.values()`, and `Object.entries()`.
**A:** `Object.keys(obj)` returns an array of own enumerable string-keyed property names. `Object.values(obj)` returns an array of own enumerable values. `Object.entries(obj)` returns an array of `[key, value]` pairs. All three only include own properties (not inherited), and only enumerable properties (non-enumerable like those set with `Object.defineProperty(obj, key, {enumerable: false})` are excluded). None include Symbol-keyed properties. The order is: integer-like keys in ascending order, then insertion order for string keys. These methods enable convenient iteration and transformation of object data. `Object.fromEntries()` (ES2019) reverses `Object.entries()`.

## Q33: How do JavaScript template literal types work in TypeScript?
**A:** Template literal types (TypeScript 4.1+) allow string manipulation at the type level: `type EventName = 'click' | 'hover'`; `type Handler = `on${Capitalize<EventName>}`` creates `'onClick' | 'onHover'`. Built-in string transformation types: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`. Template literal types use placeholders (`${...}`) and distribute over union constituents. They're used for: typed event handlers, CSS property typing, route parameter inference, Redux action types. They enable parsing string patterns at the type level, creating precise string typing without runtime cost.

## Q34: What are JavaScript `WeakRef` and `FinalizationRegistry`?
**A:** `WeakRef` (ES2021) holds a weak reference to an object, allowing it to be garbage collected. Dereference with `.deref()` — returns the object or `undefined` if collected. `FinalizationRegistry` registers cleanup callbacks when objects are garbage collected. Usage patterns: caching large objects that should be freed under memory pressure, tracking resources, implementing object pools. Risks: (1) garbage collection timing is unpredictable, (2) `deref()` may return `undefined` at any time, (3) cleanup callbacks run on microtask timing, (4) not available in all environments (some disable WeakRef). Never rely on `FinalizationRegistry` for critical cleanup — it's advisory only.

## Q35: How does JavaScript's `at()` method work on arrays and strings?
**A:** `Array.prototype.at(index)` and `String.prototype.at(index)` (ES2022) return the element at the given index, supporting negative indexing (relative from end). `-1` returns the last element, `-2` returns the second-to-last, etc. This solves the common `arr[arr.length - 1]` pattern with cleaner `arr.at(-1)`. The method returns `undefined` for out-of-bounds indices. It's available on all typed arrays too. Compared to bracket notation, `at()` is slightly slower but much more readable for negative indexing. It's preferred when working with relative positions, especially for accessing last elements.

## Q36: Explain the concept of "Temporal Dead Zone" (TDZ) in JavaScript.
**A:** The Temporal Dead Zone is the time between entering a scope and the variable's declaration where `let`, `const`, and `class` variables exist but are not yet initialized. Accessing a variable in TDZ throws `ReferenceError`. Unlike `var` (which is hoisted with `undefined` value), `let`/`const` are hoisted but not initialized. TDZ also applies to class expressions and default function parameters (where accessing a parameter before its declaration causes TDZ). Examples: `let x = y; let y = 1;` throws. `typeof` operator also throws in TDZ (unlike undeclared variables). TDZ prevents accessing uninitialized variables, catching bugs early.

## Q37: What are JavaScript async iteration and `for await...of`?
**A:** Async iteration enables consuming asynchronous data sources. The async iteration protocol uses `Symbol.asyncIterator` returning an object with `next()` returning `Promise<{value, done}>`. `for await...of` loops consume async iterables. Use cases: streaming data (file reads, network requests, paginated APIs), real-time data (WebSocket messages, database cursors), async generators. `for await...of` can only be used in async functions or top-level modules. It handles errors: if the promise rejects, the loop throws. `break`, `return`, and `throw` close the async iterator (calling its `return()` method if available). Async generators (`async function*`) simplify creating async iterables.

## Q38: How does JavaScript's `Object.groupBy()` work?
**A:** `Object.groupBy(items, callback)` (ES2024) groups array elements by the string key returned by the callback. Returns an object with groups as arrays. Example: `Object.groupBy(users, user => user.role)`. `Map.groupBy()` returns a Map (for non-string keys). The callback receives (element, index). Groups maintain insertion order. This replaces manual grouping with `reduce()` in a standard, optimized way. `Object.groupBy` is available in Node.js 21+ and modern browsers. It's part of the change-array-by-copy proposal alongside `toSorted`, `toReversed`, `toSpliced`.

## Q39: What are JavaScript's "Well-Known Symbols" and their purposes?
**A:** Well-known symbols are built-in Symbol values that customize language behavior: `Symbol.iterator` (make objects iterable), `Symbol.asyncIterator` (async iteration), `Symbol.hasInstance` (custom `instanceof`), `Symbol.toPrimitive` (custom type coercion), `Symbol.toStringTag` (custom `Object.prototype.toString` output), `Symbol.species` (constructor for derived objects), `Symbol.match`/`Symbol.replace`/`Symbol.search`/`Symbol.split` (custom regex behavior), `Symbol.unscopables` (exclude properties from `with` bindings), `Symbol.isConcatSpreadable` (control `Array.prototype.concat` flattening), `Symbol.description` (ES2019, access symbol description). These symbols allow objects to hook into JavaScript's internal operations.

## Q40: How does JavaScript's `Array.prototype.flat()` and `flatMap()` work?
**A:** `Array.prototype.flat(depth=1)` creates a new array with sub-array elements concatenated recursively up to specified depth. Removes empty slots. `Infinity` depth flattens completely. `Array.prototype.flatMap(callback)` maps each element then flattens by one level (equivalent to `map().flat(1)` but more efficient). `flatMap` is useful for: filtering and mapping in one pass, handling optional values (return empty array to omit, array to expand), breaking one element into multiple, handling nested data from APIs. Both create shallow copies. `flat` depth default is 1 (only shallow nesting). Custom flattening logic can be implemented with `reduce` and `concat`.

## Q41: Explain the difference between `Object.create()` and `new Constructor()`.
**A:** `Object.create(proto)` creates a new object with the specified prototype, without running any constructor code. `new Constructor()` creates an object with `Constructor.prototype` as prototype, then runs the constructor function with `this` bound to the new object. `Object.create` gives explicit control over the prototype (including `null` for no prototype) and can add property descriptors. `new` runs initialization code and implicitly returns `this` (or another object if explicitly returned). `new` also handles constructor return values (ignores non-object returns). `Object.create` is more flexible for setting up prototypes; `new` is the standard for class-based instantiation.

## Q42: What are JavaScript `DataView` and when would you use it?
**A:** `DataView` provides a low-level interface for reading/writing multiple number types from an `ArrayBuffer` at arbitrary byte offsets, with explicit endianness control. Methods: `getInt8`, `getUint8`, `getInt16`, `getUint16`, `getInt32`, `getUint32`, `getFloat32`, `getFloat64`, `getBigInt64`, `getBigUint64`, and corresponding `set*` methods. Unlike TypedArrays (which have fixed view types and platform endianness), `DataView` is flexible — you can read different types at different offsets from the same buffer. Use cases: binary file parsers (WAV, PNG, ZIP), network protocol implementations, WebAssembly integration, and any situation requiring binary data manipulation with specific byte layouts.

## Q43: How do JavaScript's `globalThis` work?
**A:** `globalThis` (ES2020) is a standard global object reference across environments — returns `window` (browsers), `global` (Node.js), `self` (Web Workers), or the global `this` in other contexts. Before `globalThis`, code had to detect the environment. `globalThis` solves this inconsistency. It's a read-only global property referring to the global object. In strict mode, the global `this` is `undefined`, making `globalThis` essential for accessing global state. `globalThis.Array === Array` is `true`. Polyfilling `globalThis` requires platform detection.

## Q44: Explain JavaScript's `Intl.Collator` for string comparison.
**A:** `Intl.Collator(locales, options)` provides locale-aware string comparison. Options: `localeMatcher`, `usage` ('sort' or 'search'), `sensitivity` ('base', 'accent', 'case', 'variant'), `ignorePunctuation`, `numeric` (numeric sorting: "a2" < "a10"), `caseFirst` ('upper', 'lower', 'false'). Usage: `collator.compare(a, b)` returns negative, zero, or positive. More efficient than `String.prototype.localeCompare()` when comparing arrays (sort once, compare many times). Essential for correct multilingual sorting, especially for languages with special collation rules (German ß, Swedish å, Chinese).

## Q45: How does JavaScript's `ArrayBuffer` and `SharedArrayBuffer` differ?
**A:** `ArrayBuffer` is a fixed-length binary data buffer that cannot be shared between threads. `SharedArrayBuffer` can be shared between the main thread and Web Workers, providing zero-copy shared memory. `ArrayBuffer` transfer requires structured clone (copy). `SharedArrayBuffer` requires `Atomics` for synchronization (avoid race conditions). `SharedArrayBuffer` was re-enabled in browsers with cross-origin isolation headers (`Cross-Origin-Opener-Policy` and `Cross-Origin-Embedder-Policy`). Both can be resized (ES2023) with `resizable` option. `ArrayBuffer` views (`TypedArray`, `DataView`) work on both, but views on `SharedArrayBuffer` must use `Atomics` for correct multi-threaded access.

## Q46: What is the difference between `event.preventDefault()` and `return false`?
**A:** `event.preventDefault()` prevents the browser's default action (e.g., link navigation, form submission), but doesn't stop event propagation. `return false` in an event handler (jQuery) both prevents default and stops propagation. In vanilla JavaScript DOM 0 handlers (`onclick="return false"`), `return false` prevents default. In `addEventListener` callbacks, `return false` does nothing special (the return value is ignored). `event.preventDefault` is explicit and preferred. jQuery's `return false` is equivalent to calling both `preventDefault()` and `stopPropagation()`. Modern code should call `preventDefault()` explicitly.

## Q47: How does JavaScript's `Promise.allSettled()` differ from `Promise.all()`?
**A:** `Promise.allSettled(iterable)` (ES2020) waits for all promises to settle (either fulfill or reject) and returns an array of result objects: `{status: 'fulfilled', value}` or `{status: 'rejected', reason}`. Unlike `Promise.all()` which short-circuits on first rejection, `allSettled` never short-circuits — every promise result is collected. Use `allSettled` when you need all results regardless of failures (e.g., batch independent API calls, validation checks). Use `all` when any failure should immediately fail the whole operation. `Promise.allSettled` is always safe — it never rejects.

## Q48: Explain JavaScript's `await using` and explicit resource management.
**A:** `await using` and `using` are part of the Explicit Resource Management proposal (ES2024). `using` declares a disposable resource: `using file = new FileHandle()` — automatically calls `[Symbol.dispose]()` when the variable goes out of scope. `await using` does the same with `[Symbol.asyncDispose]()` for async disposal. Use cases: file handles, database connections, locks, streams. Resources are disposed in reverse declaration order. This pattern ensures cleanup even on early returns or exceptions, replacing `try/finally` for resource management. `DisposableStack` and `AsyncDisposableStack` provide programmatic resource management.

## Q49: How do JavaScript `Error.cause` and `Error.stack` relate?
**A:** `Error` objects have `.stack` property (non-standard but widely supported) providing a string trace of function calls. In engines supporting both (V8, SpiderMonkey), when `cause` is provided, the stack trace includes the cause chain. The stack format varies: V8 shows "Caused by:", SpiderMonkey shows "Stack trace of cause:". `stack` is lazily computed when first accessed. `Error.prepareStackTrace` (V8 custom API) allows custom stack formatting. The `stack` property is not part of structured clone (lost in `postMessage`, `structuredClone`). `.fileName`, `.lineNumber`, `.columnNumber` are non-standard SpiderMonkey extensions.

## Q50: What is the purpose of `Symbol.asyncDispose` and `Symbol.dispose`?
**A:** `Symbol.asyncDispose` and `Symbol.dispose` are well-known symbols used by the Explicit Resource Management proposal (ES2024). Objects implementing `[Symbol.dispose]()` are disposable — they can be used with `using`. Objects implementing `[Symbol.asyncDispose]()` are async disposable — used with `await using`. These methods handle cleanup logic: closing files, releasing locks, disconnecting streams. The runtime guarantees disposal when the block exits (normal return, break, continue, throw, or early return). Resources are disposed in reverse order of declaration. This standardizes a long-standing pattern in JavaScript resource management.

## Q51: How does JavaScript's `Function.prototype.toString()` behave?
**A:** `Function.prototype.toString()` returns a string representation of the function. For user-defined functions, it returns the source code (including comments in V8). For native functions, it returns `function name() { [native code] }`. Since ES2019, `toString()` must return the exact source text (including whitespace, comments) for functions defined in source code. This enables: function serialization, code instrumentation, and certain metaprogramming patterns. For arrow functions, the return includes the full expression body. For generator functions, it includes the `*`. The behavior varies slightly across engines for bound functions and proxy functions.

## Q52: Explain the difference between `Object.defineProperty()` and direct property assignment.
**A:** `Object.defineProperty(obj, key, descriptor)` creates or configures a property with fine-grained control: `value`, `writable`, `enumerable`, `configurable`, `get`, `set`. Direct assignment (`obj.key = value`) creates an enumerable, writable, configurable data property. `defineProperty` can create: (1) non-enumerable properties (hidden from `for...in`, `Object.keys`), (2) non-writable (read-only) properties, (3) non-configurable (can't be deleted or reconfigured) properties, (4) accessor properties (getters/setters). `Object.defineProperties()` for multiple properties. `Object.getOwnPropertyDescriptor()` to inspect. Used for: polyfills, library internals, hiding implementation details, creating computed/intrinsic properties.

## Q53: What are JavaScript "nullish coalescing" `??` and "logical nullish assignment" `??=`?
**A:** The nullish coalescing operator `??` (ES2020) returns the right operand if the left is `null` or `undefined`, otherwise the left. Unlike `||` (which treats `0`, `''`, `false` as falsy), `??` only treats `null`/`undefined` as nullish. Useful for default values: `const name = input ?? 'default'`. Can't be combined with `||`/`&&` without parentheses. The nullish assignment `??=` (ES2021) assigns only if the current value is null/undefined: `x ??= defaultValue`. This combines null checking with assignment, useful for lazy initialization and optional defaults.

## Q54: How does JavaScript's `Object.hasOwn()` differ from `hasOwnProperty()`?
**A:** `Object.hasOwn(object, property)` (ES2022) is a static method that checks if an object has a property as its own (not inherited). It replaces `Object.prototype.hasOwnProperty.call(obj, prop)` usage. Advantages: (1) works for objects created with `Object.create(null)` (which don't inherit `hasOwnProperty`), (2) safer against objects that override `hasOwnProperty`, (3) more ergonomic — doesn't require `call`, (4) built-in optimization in engines. Both check only own properties (not inherited), and only string-keyed properties (not Symbols with `hasOwnProperty`, but `Object.hasOwn` also works with Symbols). `in` operator checks own and inherited properties.

## Q55: What is JavaScript's "optional chaining" `?.` operator?
**A:** Optional chaining `?.` (ES2020) safely accesses nested properties without throwing if an intermediate reference is `null`/`undefined`. Variants: `obj?.prop` (property access), `obj?.[expr]` (computed access), `func?.(args)` (function call). Returns `undefined` if the left side is null/undefined, otherwise proceeds normally. Short-circuits — if `?.` encounters null/undefined, the expression stops evaluating. Useful for: deeply nested API responses, optional configuration objects, chain-of-responsibility patterns. `?.` cannot be used on the left side of an assignment. It prevents the common "Cannot read property of undefined" errors.

## Q56: How do JavaScript's dynamic imports (`import()`) work?
**A:** Dynamic `import()` (ES2020) returns a promise for the module namespace object of a module. It enables: (1) code splitting (loading modules on demand), (2) conditional module loading (based on environment, user input), (3) lazy loading (deferring module load until needed), (4) module loading from computed paths. `import()` works in both ESM and CommonJS contexts. The returned promise resolves to a module namespace — use `.default` for default exports. Dynamic imports trigger separate network requests (browser) or file reads (Node.js). They integrate with the module cache — multiple `import()` calls to the same module share the same cached module. Error handling: `import().catch()`.

## Q57: Explain the difference between `String.prototype.localeCompare()` and comparison operators.
**A:** `String.prototype.localeCompare(compareString, locales, options)` returns -1, 0, or 1 based on locale-aware ordering. It correctly handles accented characters, ligatures, and language-specific rules. Options: `sensitivity`, `ignorePunctuation`, `numeric`, `caseFirst`. Comparison operators (`<`, `>`, `===`) use UTF-16 code unit ordering, which is incorrect for many languages. Examples: "é" vs "e" — in some locales they're equal; "ä" vs "a" — varies by language. `localeCompare` is slower than `===` but essential for correct multilingual sorting. For sorting arrays, use `Intl.Collator` (more efficient for multiple comparisons).

## Q58: What are JavaScript `Error` stacks and source maps?
**A:** Error stacks show the call chain at the point of error. In modern environments, source maps map compiled/minified code back to original source. Error stacks can reference original source positions when source maps are available and enabled. Chrome DevTools, Node.js (with `--enable-source-maps`), and bundlers (webpack, Vite) support source maps. `Error.captureStackTrace` (V8) customizes stack traces. Source maps are `.map` files following the Source Map Specification (version 3). They map: minified JS → original JS, TypeScript → JS, JSX → JS. Enable source maps in production debugging without exposing source code publicly (server-side only).

## Q59: How does JavaScript's `Array.prototype.reduceRight()` work?
**A:** `Array.prototype.reduceRight(callback, initialValue)` works like `reduce()` but processes array elements from right to left (last to first). The callback receives (accumulator, currentValue, index, array). Useful for: right-associative operations, reversing operations, nested structure building from the end, and certain mathematical operations. Example: `[[1, 2], [3, 4]].reduceRight((acc, val) => acc.concat(val), [])` produces `[3, 4, 1, 2]`. Same edge cases as `reduce` — throws on empty array without initialValue. Performance is similar to `reduce` since array traversal is equally efficient in either direction.

## Q60: How do JavaScript `Intl.ListFormat` and `Intl.DateTimeFormat` handle advanced formatting?
**A:** `Intl.ListFormat(locales, options)` formats lists: `new Intl.ListFormat('en', {type: 'conjunction', style: 'long'}).format(['A', 'B', 'C'])` → "A, B, and C". Options: type ('conjunction', 'disjunction', 'unit'), style ('long', 'short', 'narrow'). `Intl.DateTimeFormat` handles complex formatting with options: `dateStyle`/`timeStyle` (ES2021, 'full', 'long', 'medium', 'short'), `fractionalSecondDigits`, `dayPeriod`, `era`, `timeZoneName` ('long', 'short', 'shortOffset', 'longOffset', 'shortGeneric', 'longGeneric'). `formatRange(date1, date2)` formats date ranges. `formatToParts()` returns structured format components. These handle locale-specific conventions automatically (right-to-left languages, different calendar systems).

## Q61: Explain the concept of "tail call optimization" in JavaScript.
**A:** Tail call optimization (TCO) allows recursive functions to execute in constant stack space when the recursive call is in tail position (the last operation before return). ES2015 specifies proper tail calls (PTC) in strict mode. However, only Safari (JavaScriptCore) implements TCO. V8 (Chrome, Node.js) and SpiderMonkey (Firefox) don't implement it (they cite implementation difficulties and debugging impact). Without TCO, deeply recursive code causes stack overflow. Alternatives: trampolining (return a function that performs the next step), converting recursion to iteration, or using `while` loops. TCO only applies to direct tail calls in strict mode.

## Q62: How does JavaScript's `structuredClone` handle errors and unsupported types?
**A:** `structuredClone(value, {transfer})` throws `DataCloneError` DOMException for unsupported types: functions, Symbols, DOM nodes (non-clonable), WeakRef, WeakMap, WeakSet, Error objects (type-specific support varies), and objects with `[Symbol.toPrimitive]` (in some engines). The `transfer` parameter moves ArrayBuffers — after cloning, the source buffer is detached (zero-length). Transfer errors throw `TypeError` if the same buffer is transferred multiple times. The algorithm handles: circular references (re-uses cloned references), `Map`/`Set` (deep clones entries), `RegExp` (preserves flags, lastIndex), `Date` (copies timestamp), Blob/File (copies data). Use try/catch around `structuredClone` for safety.

## Q63: What are JavaScript's `import.meta` and `import.meta.url`?
**A:** `import.meta` (ES2020) is an object containing metadata about the current module. `import.meta.url` is the absolute URL of the current module (file:// in Node.js, http:// or https:// in browser). Use cases: (1) resolving relative paths: `new URL('./asset.txt', import.meta.url)`, (2) feature detection, (3) environment detection. `import.meta.resolve(moduleSpecifier)` (import assertions proposal, available in Node.js experimental) resolves specifiers without loading. `import.meta` is available only in ESM modules, not CommonJS. It's immutable — properties can't be added or modified.

## Q64: How do JavaScript's `Intl.RelativeTimeFormat` and `Intl.NumberFormat` handle advanced cases?
**A:** `Intl.RelativeTimeFormat(locales, options)` formats relative time: "yesterday", "in 3 days". Options: `numeric` ('always', 'auto' for "yesterday" vs "1 day ago"), `style` ('long', 'short', 'narrow'). `Intl.NumberFormat` supports: `style: 'unit'` (with `unit` option: 'kilobyte', 'mile-per-hour'), `notation` ('scientific', 'engineering', 'compact'), `compactDisplay` ('short', 'long'), `signDisplay` ('auto', 'always', 'exceptZero', 'never'), `currencySign` ('standard', 'accounting'), `trailingZeroDisplay` ('auto', 'stripIfInteger'). `formatRange()` and `formatRangeToParts()` handle value ranges. `NumberFormat` can format compact numbers: `1.2M` instead of `1,200,000`.

## Q65: Explain the difference between `document.cookie`, `localStorage`, and `sessionStorage`.
**A:** `document.cookie`: old API, max ~4KB, sent with every HTTP request (including subresource requests), supports `HttpOnly` (no JS access), `Secure` (HTTPS only), `SameSite`, domain/path scoping, expiration, max 20-50 cookies per domain. `localStorage`: persistent, max ~5-10MB, not sent with requests, synchronous API, per-origin, no expiration, string-only storage (serialize objects manually). `sessionStorage`: same as localStorage but cleared when tab closes, per-tab, not shared between tabs. For sensitive data: use cookies with `HttpOnly` + server-side session. For client data: use localStorage. For temporary session: use sessionStorage. IndexedDB for larger structured data. All are synchronous except IndexedDB.

## Q66: How does JavaScript's `Promise.any()` work?
**A:** `Promise.any(iterable)` (ES2021) resolves with the first fulfilled promise. If all promises reject, it rejects with `AggregateError` (containing all rejection reasons in `.errors` array). Unlike `Promise.race()` (which settles on first settled promise, rejection or fulfillment), `Promise.any` ignores rejections until all are rejected. Use cases: (1) racing multiple data sources and taking the first successful response, (2) timeout with fallback: `Promise.any([fetch(url), timeout(5000).then(() => fallback)])`, (3) fast-failover systems. `AggregateError` must be caught with `error instanceof AggregateError` to access individual errors.

## Q67: What is the `Intl.Segmenter` and how does it handle emoji?
**A:** `Intl.Segmenter` correctly handles emoji grapheme clusters, including: (1) skin tone modifiers (👍🏽), (2) ZWJ sequences (👨‍👩‍👧‍👦 family, 🧑‍💻 developer), (3) flag emoji regional indicator pairs (🇺🇸), (4) keycap sequences (#️⃣), (5) variation selectors (☠️ vs ☠). Without segmenter, emoji sequences appear as multiple characters (each code point). `segmenter.segment(text)` returns an iterable of segments, each with proper grapheme boundaries. Essential for: text editors (cursor movement through emoji), character counters (Twitter counts emoji as 2 chars but display length may differ), text truncation that preserves emoji integrity.

## Q68: How do JavaScript `Error` subclasses behave with `instanceof`?
**A:** Custom Error subclasses created with `class MyError extends Error {}` work with `instanceof MyError`. However, `instanceof` can fail across different realms/iframes (each realm has its own Error constructor). To check error type robustly: check `error.name === 'MyError'` or `error.constructor.name`. The `.name` property is reliable and serializable. `Error` subclasses should set `.name` explicitly. V8's `stack` property correctly reflects subclass names. `AggregateError` (ES2021) is a built-in Error subclass with `.errors` array. `TypeError`, `RangeError`, `SyntaxError`, `ReferenceError`, `URIError`, `EvalError` are built-in Error subclasses.

## Q69: Explain the difference between `document.querySelector()` and `document.getElementById()`.
**A:** `document.getElementById(id)` returns the element with the specified ID (fastest — uses hash map). Only available on `document`, not on elements. `document.querySelector(selector)` returns the first matching element by CSS selector (slower — parses selector, traverses DOM). Use `getElementById` for IDs (performance-critical loops), `querySelector` for all other selector needs (classes, attributes, complex selectors). `querySelectorAll` returns a static (non-live) NodeList. `getElementsByClassName`, `getElementsByTagName` return live HTMLCollections (reflect DOM changes). Modern code prefers `querySelector` for consistency, `getElementById` for performance.

## Q70: How does JavaScript's `Intl.NumberFormat` handle currency formatting?
**A:** `new Intl.NumberFormat(locale, {style: 'currency', currency: 'USD'})` formats currency respecting locale conventions. Options: `currencyDisplay` ('symbol': $, 'code': USD, 'name': US dollars), `currencySign` ('standard', 'accounting' for negative in parentheses), `useGrouping` (boolean), `minimumFractionDigits`, `maximumFractionDigits`, `minimumSignificantDigits`, `maximumSignificantDigits`. Currency codes follow ISO 4217. Different locales format differently: en-US `$1,234.56`, de-DE `1.234,56 €`, ja-JP `￥1,235`. For crypto or non-ISO currencies, provide custom formatting. `NumberFormat` also handles rounding modes: `roundingMode` (ES2023): 'ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'.

## Q71: What are JavaScript's `static initialization blocks`?
**A:** Static initialization blocks (`static {}`) in classes (ES2022) run once when the class is evaluated, after static field declarations. They provide: (1) complex static initialization logic (try/catch, loops, conditionals), (2) access to private static fields, (3) initialization that can't be done with field declarations. Multiple static blocks execute in declaration order. They can share private state between instances and static methods:

```javascript
class MyClass {
  static #privateField;
  static {
    try { MyClass.#privateField = loadConfig(); }
    catch { MyClass.#privateField = 'default'; }
  }
}
```

Static blocks replace the pattern of using an IIFE after class definition.

## Q72: How does JavaScript's `Shadow DOM` encapsulation work?
**A:** Shadow DOM provides DOM encapsulation by attaching a hidden DOM tree to an element. `element.attachShadow({mode: 'open'|'closed'})` creates a shadow root. Features: (1) style scoping — CSS in the shadow tree doesn't leak out or in, (2) DOM encapsulation — shadow DOM contents are hidden from main DOM queries, (3) event retargeting — events from shadow DOM appear to come from the host element. `mode: 'open'` allows JS access with `element.shadowRoot`, `'closed'` prevents it. `slot` elements project light DOM content into shadow DOM. `::part()` CSS pseudo-element allows styling shadow parts. Used in web components for true encapsulation.

## Q73: Explain the difference between `for...of` and `forEach()` on arrays.
**A:** `for...of` loops can use `break`, `continue`, `return`, and `await`. `forEach()` cannot be broken or stopped — it always iterates all elements. `for...of` works with any iterable (not just arrays). `forEach()` is array-only (but also works on typed arrays, NodeLists via `.call()`). `for...of` doesn't provide the index by default (use `.entries()`). `forEach()` provides (value, index, array). `for...of` is faster (no function call overhead). `forEach()` creates a new scope per iteration (closure behavior differs). `for...of` with `await` works naturally; `forEach()` with async callbacks doesn't wait. For regular iteration, `for...of` is preferred. For functional chains, `forEach()` works.

## Q74: How does JavaScript's `Array.prototype.toSorted()`, `toReversed()`, and `toSpliced()` work?
**A:** These methods (ES2023) are immutable alternatives to the mutating `sort()`, `reverse()`, and `splice()`. `toSorted(compareFn)` returns a new sorted array without modifying the original. `toReversed()` returns a new reversed array. `toSpliced(start, deleteCount, ...items)` returns a new array with elements removed/inserted. `with(index, value)` returns a new array with one element changed. These methods (plus `Array.fromAsync` in ES2024) are part of the "change array by copy" proposal. They're available in Node.js 20+ and modern browsers. They follow the same API as their mutating counterparts but return new arrays.

## Q75: What are JavaScript's well-known symbols for `Symbol.toStringTag`?
**A:** `Symbol.toStringTag` customizes the output of `Object.prototype.toString.call(obj)`. Built-in types return: `[object Array]`, `[object Map]`, `[object Set]`, `[object Promise]`, `[object Generator]`, etc. Custom classes can set:

```javascript
class CustomClass {
  get [Symbol.toStringTag]() { return 'CustomClass'; }
}
```

This affects: `Object.prototype.toString`, error messages, and some debugging tools. It's a getter, not a data property. Built-in types like `Math[Symbol.toStringTag]` returns `'Math'`. It doesn't affect `typeof` or `instanceof`. Primarily useful for creating custom types that integrate with the `toString()` convention.

## Q76: How does JavaScript's `FinalizationRegistry` help with memory management?
**A:** `FinalizationRegistry` (ES2021) registers cleanup callbacks that run after objects are garbage collected. Usage:

```javascript
const registry = new FinalizationRegistry((heldValue) => {
  console.log(`${heldValue} was garbage collected`);
});
registry.register(target, 'myObject');
registry.unregister target' with unregisterToken when no longer needed.
```

Use cases: (1) closing file handles or network connections when objects are collected, (2) cleaning up external resources (WebGL textures, WASM memory), (3) cache eviction tracking, (4) monitoring memory leaks during development. Limitations: callbacks are best-effort, timing is unpredictable, callbacks run on the microtask queue, and the registry itself should not hold strong references to registered objects (pass a separate unregister token). Never depend on callbacks for critical program logic.

## Q77: How do JavaScript's `Intl.DateTimeFormat` handle timezone formatting?
**A:** `Intl.DateTimeFormat` supports IANA timezone names: `timeZone: 'America/New_York'`, `'Europe/London'`, `'Asia/Tokyo'`. Without `timeZone`, the runtime's default timezone is used. Options: `timeZoneName` ('short': EST, 'long': Eastern Standard Time, 'shortOffset': GMT-5, 'longOffset': GMT-05:00, 'shortGeneric': ET, 'longGeneric': Eastern Time). `timeStyle` ('full', 'long', 'medium', 'short') provides time-specific formatting. `formatToParts()` returns timezone components separately. `format(date)` converts the Date to the target timezone. Use `Temporal.ZonedDateTime` (future) for more robust timezone handling. `Intl.DateTimeFormat` doesn't handle historical timezone changes — it uses current rules.

## Q78: What are JavaScript's `Array.fromAsync()` method?
**A:** `Array.fromAsync(asyncIterable, mapFn, thisArg)` (ES2024) creates an array from an async iterable, sync iterable, or promise-like object. It awaits each element and applies the optional map function. Returns a Promise<Array>. Useful for: (1) converting async generators to arrays, (2) parallel processing of async data with mapping, (3) collecting results from `ReadableStream`, (4) handling mixed sync/async iterables. Unlike `Promise.all(Array.from(iter).map(fn))`, `fromAsync` processes sequentially (one at a time), but parallel processing can be done with `Promise.all(await Array.fromAsync(iter, async x => x))`.

## Q79: How does JavaScript's `Error.prototype.stack` differ across environments?
**A:** Stack trace format varies: V8 (Chrome, Node.js): `at functionName (file:line:col)`, SpiderMonkey (Firefox): `functionName@file:line:col`, JavaScriptCore (Safari): `functionName@file:line:col` with different formatting. V8 async stacks (since Node.js 12): includes async boundaries with `async` prefix. Stack trace depth is limited (typically 10 frames by default in V8). `Error.stackTraceLimit` (V8 only) controls max frames. `sourceURL` pragma (`//# sourceURL=...`) renames stack traces. Source maps (`.map` files) translate minified stacks. For cross-environment compatibility, parse stacks carefully or use libraries like `stacktrace.js`.

## Q80: What is JavaScript's `Intl.PluralRules` and when is it used?
**A:** `Intl.PluralRules(locales, options)` determines pluralization categories for numbers. Returns 'zero', 'one', 'two', 'few', 'many', or 'other'. Options: `type` ('cardinal' — 1 item, 2 items; 'ordinal' — 1st, 2nd, 3rd). Essential for internationalization: generating correct plural forms based on locale rules. Example:

```javascript
const pr = new Intl.PluralRules('en');
pr.select(1); // 'one'
pr.select(2); // 'other'
```

Languages have different rules: Arabic has 6 categories, Japanese has 1 (no plural distinction). Combined with `Intl.ListFormat` for complete i18n message formatting. Usually used with ICU message format or a template system.

## Q81: How do JavaScript's `CustomEvent` and event dispatch work?
**A:** `CustomEvent(type, options)` creates custom events with `detail` property for data. Options: `bubbles`, `cancelable`, `composed` (pierces shadow DOM boundaries). Dispatch with `element.dispatchEvent(event)`. `event.preventDefault()` sets `event.defaultPrevented` if cancelable. Custom events enable: (1) component communication (publish/subscribe patterns), (2) web component events, (3) decoupled architecture. `composed: true` allows events to bubble out of shadow DOM. `isTrusted` is `false` for synthetic events (distinguishes from user-initiated events). Event listeners use `addEventListener(type, handler)` on the dispatching element or ancestors.

## Q82: Explain JavaScript's `Object.groupBy` and `Map.groupBy` differences.
**A:** `Object.groupBy(items, callback)` (ES2024) returns a plain object with groups as arrays. Keys are always strings. `Map.groupBy()` returns a Map, preserving key types. Use `Object.groupBy` when keys are naturally strings and you want simple object access. Use `Map.groupBy` when keys should be objects, symbols, or other non-string types. Both use the callback to determine the group key. The callback receives (element, index). Example:

```javascript
const positive = Object.groupBy([1, -2, 3], n => n > 0 ? 'yes' : 'no');
// { yes: [1, 3], no: [-2] }
```

Missing from older environments — polyfill with `reduce` if needed.

## Q83: How does JavaScript's `Intl.Collator` handle search and matching?
**A:** `Intl.Collator` with `usage: 'search'` is optimized for string matching (finding all matches, not just sorting). Combined with `sensitivity`, it controls what differences matter: 'base' (a ≠ b, but a = á = A), 'accent' (a ≠ á, but a = A), 'case' (a ≠ A, but a = á), 'variant' (all differences matter). `ignorePunctuation: true` ignores punctuation for fuzzy matching. Example: searching "cote" should match "côte" with `sensitivity: 'base'`. `collator.compare('cote', 'côte')` returns 0. Use for case-insensitive searching, accent-insensitive matching, and locale-aware search features.

## Q84: What are JavaScript's `Promise.withResolvers()`?
**A:** `Promise.withResolvers()` (ES2024) returns an object with `promise`, `resolve`, and `reject` properties — equivalent to `new Promise((resolve, reject) => ({resolve, reject}))` but without nesting the callbacks inside the executor. It's useful for: (1) promise creation outside of executor callbacks, (2) event-driven promise resolution, (3) callback-to-promise conversion, (4) implementing queues with backpressure. Example:

```javascript
const {promise, resolve, reject} = Promise.withResolvers();
button.onclick = () => resolve('clicked');
const result = await promise;
```

This avoids the common pattern of storing resolve/reject in external variables.

## Q85: How does JavaScript's `Intl.supportedValuesOf()` work?
**A:** `Intl.supportedValuesOf(key)` (ES2022) returns a sorted array of supported locale-sensitive values for the given key. Keys: 'calendar', 'collation', 'currency', 'numberingSystem', 'timeZone', 'unit'. Example: `Intl.supportedValuesOf('calendar')` returns ['buddhist', 'chinese', 'coptic', ...]. `Intl.supportedValuesOf('timeZone')` returns like ['America/New_York', 'Asia/Tokyo', ...]. This enables feature detection and UI building — dynamically populating locale-preference UIs, detecting available calendars, or determining supported currencies. It eliminates the need for hard-coded lists of supported values.

## Q86: What are JavaScript's `Atomics` methods for synchronization?
**A:** `Atomics` provides low-level synchronization: `Atomics.wait(typedArray, index, value, timeout)` — blocks the current thread until the array position changes (returns 'ok', 'not-equal', 'timed-out'). `Atomics.notify(typedArray, index, count)` — wakes waiting threads. `Atomics.waitAsync(index, value, timeout)` — non-blocking wait returning a promise. These are the building blocks for higher-level synchronization: mutexes, semaphores, barriers, and condition variables. Only works on `Int32Array` views of `SharedArrayBuffer`. `Atomics.isLockFree(size)` checks if atomic operations on a given byte size are lock-free (hardware-supported). Proper use requires careful avoidance of deadlocks and data races.

## Q87: How do JavaScript's `Intl.DurationFormat` work?
**A:** `Intl.DurationFormat(locales, options)` (ES2024) formats duration objects `{hours: 2, minutes: 30}` into locale-appropriate strings. Options: `style` ('long', 'short', 'narrow', 'digital'), `years`, `months`, `weeks`, `days`, `hours`, `minutes`, `seconds`, `milliseconds`, `microseconds`, `nanoseconds` display options. Example: `new Intl.DurationFormat('en', {style: 'digital'}).format({hours: 25, minutes: 30})` → "25:30:00". Supports fractional digits. The duration object uses Temporal's Duration structure. This provides standard-compliant duration formatting without manual string construction.

## Q88: Explain the difference between `class` fields and `constructor` assignments.
**A:** Class field declarations (`count = 0`) define instance properties differently than `constructor` assignments (`this.count = 0`). Fields are defined using `Object.defineProperty` at the start of construction (before the constructor body). Constructor assignments are regular property assignments during construction. Fields defined in subclass run after `super()` and after parent class fields. Field declarations are not hoisted — they're executed in definition order. Fields can be private (`#field`). Constructor assignments can be conditional (if/else, computed values). Fields cannot reference `this` before `super()` in subclasses. Fields provide clearer intent for simple defaults.

## Q89: How does JavaScript's `Error.captureStackTrace()` work in V8?
**A:** `Error.captureStackTrace(target, constructorOpt)` (V8-only) captures a stack trace in `target.stack` without creating an Error object. `constructorOpt` is optional — if provided, frames from that constructor are excluded from the stack (making the error appear to originate from the caller). Used internally in V8 for `Error` subclassing:

```javascript
function CustomError(message) {
  this.message = message;
  this.name = 'CustomError';
  Error.captureStackTrace(this, CustomError);
}
```

The second argument makes the stack start at the caller of the function that creates the error. Without `captureStackTrace`, `new Error().stack` is the standard approach. `Error.prepareStackTrace(error, structuredStackTrace)` allows custom stack formatting (V8-only).

## Q90: What are JavaScript `Promise` combinators (`race`, `all`, `allSettled`, `any`)?
**A:** The four combinators cover different concurrency patterns: `Promise.all([p1, p2, p3])` — resolves when all resolve, rejects on first rejection (short-circuits). `Promise.race([p1, p2, p3])` — resolves/rejects with the first settled promise (any outcome). `Promise.allSettled([p1, p2, p3])` — resolves when all settle, never rejects, returns status objects. `Promise.any([p1, p2, p3])` — resolves on first fulfillment, rejects with `AggregateError` if all reject. Use cases: `all` for parallel independent tasks, `race` for timeouts, `allSettled` for batch results with failures, `any` for first-success scenarios. All accept iterables and return a single Promise.

## Q91: How does JavaScript's `import` work with JSON modules and assertion?
**A:** Import assertions (ES2023) allow specifying module type: `import data from './data.json' assert { type: 'json' }`. This is required for importing non-JS modules. Dynamic import: `import('./data.json', {assert: {type: 'json'}})`. The assertion ensures the module is treated as the specified type. JSON modules export a single default export (the parsed JSON). Other types: CSS modules, WebAssembly modules. Without assertions, JSON imports aren't allowed for security (to prevent MIME type confusion). Node.js requires `--experimental-json-modules` (older) or just works with assertions. Browsers require the `Content-Type` header to match the asserted type.

## Q92: Explain JavaScript's `Error.prototype.name` vs `Error.prototype.constructor.name`.
**A:** `Error.prototype.name` is an own property (on each Error instance) that can be set independently. `Error.prototype.constructor.name` follows prototype chain. For standard errors, both give the same result. For custom errors, setting `.name` explicitly is crucial because minification might change `constructor.name`. Example: `class MyError extends Error { constructor() { super(); this.name = 'MyError'; } }` ensures the name is correct even after minification. `.name` affects stack trace output. `TypeError.name === 'TypeError'`, `SyntaxError.name === 'SyntaxError'`, etc. Custom errors without `.name` set show `'Error'` after minification.

## Q93: How do JavaScript's `Intl.DateTimeFormat` handle calendar systems?
**A:** `Intl.DateTimeFormat` supports non-Gregorian calendars via `calendar` option: 'buddhist', 'chinese', 'coptic', 'dangi', 'ethioaa', 'ethiopic', 'gregory', 'hebrew', 'indian', 'islamic', 'islamic-umalqura', 'islamic-tbla', 'islamic-civil', 'islamic-rgsa', 'iso8601', 'japanese', 'persian', 'roc', 'islamicc'. Example: `new Intl.DateTimeFormat('en-US-u-ca-hebrew')` formats dates in the Hebrew calendar. The calendar affects year numbering, month names, and era indicators. The JavaScript `Date` object always represents UTC milliseconds — the calendar is a formatting layer. `formatToParts()` returns calendar-specific parts including `era` and `yearName` for non-Gregorian calendars.

## Q94: What are JavaScript `ReadableStream`, `WritableStream`, and `TransformStream`?
**A:** The Streams API provides standard streaming primitives: `ReadableStream` — source of data (pull: fetch response, push: custom source). `WritableStream` — sink for data (file writer, network). `TransformStream` — transforms data (compress, encrypt, parse). Features: backpressure (consumer signals producer to slow down), piping (`readableStream.pipeThrough(transform).pipeTo(writable)`), teeing (`readableStream.tee()` splits into two). `ReadableStream` has `getReader()` for locked access. 'BYOB' readers (bring your own buffer) minimize copies. `WritableStream.getWriter()` for writing. `TransformStream` uses `{start, transform, flush}` controller. Used by `Response.body`, `File.stream()`, and `Blob.stream()`. Essential for processing large data incrementally.

## Q95: How does JavaScript's `Intl.DateTimeFormat` handle era and season?
**A:** `Intl.DateTimeFormat` with `era: 'short'` (e.g., "AD", "2020 AD") or `era: 'long'` ("Anno Domini") formats the era for calendars that support it (Japanese, Buddhist, Gregorian). Options combine: `year: 'numeric'`, `month: 'long'`, `day: 'numeric'`, `era: 'long'`, `calendar: 'japanese'`. There's no built-in season formatting — seasons depend on hemisphere and culture. For seasons, use `Intl.DateTimeFormat` with month/day and custom mapping. `dayPeriod` option formats morning/afternoon/evening/night. `hourCycle: 'h11'|'h12'|'h23'|'h24'` controls 12/24-hour display. `hour12: true|false` is a convenience option. Some locales use different day periods (6 periods in Japanese).

## Q96: What are JavaScript `Atomics` memory ordering guarantees?
**A:** `Atomics` operations in JavaScript follow the same memory model as C++11 atomics. Operations are sequentially consistent by default — all threads observe operations in the same order. This prevents both compiler reordering and CPU memory reordering. For performance, `Atomics.load` and `Atomics.store` in some engines might be cheaper than read-modify-write operations. The memory model ensures: (1) no data races (undefined behavior in C++ is defined in JavaScript), (2) happens-before relationships between `Atomics.notify` and `Atomics.wait`, (3) `Atomics` operations synchronize with each other across threads, (4) non-atomic accesses to shared memory are data races (avoid). For complex synchronization, build mutexes and semaphores with `Atomics`.

## Q97: Explain JavaScript's `new Function()` and its scope behavior.
**A:** `new Function(...args, body)` creates a function dynamically from string code. Unlike `eval()`, it creates a function object rather than executing in the current scope. The created function has global scope — it doesn't close over the creating scope (except global variables). This makes it useful for: (1) creating functions from strings received at runtime (templates), (2) implementing REPLs and code sandboxes, (3) dynamically generating optimized functions. Security: `new Function` can access global scope, so it's not a security boundary. Performance: code is compiled, not cached like JIT-optimized functions. Use sparingly — prefer closures or `eval()` with scope access.

## Q98: How does JavaScript's `Temporal.Instant` differ from `Date`?
**A:** `Temporal.Instant` (ES2024+) represents an exact point in time (nanosecond precision, UTC). Unlike `Date` (millisecond precision, mutable, confusing API), `Temporal.Instant` is immutable, has nanosecond precision, and is unambiguous (always UTC). Creation: `Temporal.Instant.from('2024-01-01T00:00:00Z')`, `Temporal.Instant.fromEpochMilliseconds(ms)`, `Temporal.Now.instant()`. Comparison: `.equals()`, `.since()`, `.until()`. Arithmetic: `.add()`, `.subtract()`, `.round()`. Conversion: `.toZonedDateTimeISO(timezone)`, `.toLocaleString()`. `Temporal.Instant` disallows: (1) wall-clock arithmetic (no "add a month" — use ZonedDateTime), (2) ambiguous interpretations, (3) mutable operations.

## Q99: What are JavaScript's `Intl.Locale` and its advanced features?
**A:** `Intl.Locale` (ES2021) provides a structured representation of BCP 47 locale identifiers. Constructor: `new Intl.Locale('en-US-u-hc-h24-ca-gregory')`. Properties: `.language`, `.script`, `.region`, `.baseName`, `.calendar`, `.collation`, `.hourCycle`, `.caseFirst`, `.numeric`, `.numberingSystem`, `.minimize()`, `.maximize()`. `minimize()` transforms 'en-Latn-US' → 'en-US' (removes likely subtags). `maximize()` does the reverse. Extensions: Unicode extensions ('-u-...'), transformed extensions ('-t-...'), private use ('-x-...'). Used for: locale negotiation, locale data access, custom locale construction, and locale comparison. Enables programmatic locale manipulation without string parsing.

## Q100: How does JavaScript's `Temporal.Duration` handle date/time arithmetic?
**A:** `Temporal.Duration` (ES2024+) represents a duration of time with: years, months, weeks, days, hours, minutes, seconds, milliseconds, microseconds, nanoseconds. Created via: `Temporal.Duration.from({hours: 1, minutes: 30})`, `Temporal.Duration.from('PT1H30M')`. Arithmetic: `.add()`, `.subtract()`, `.negated()`, `.abs()`, `.round()`, `.total()`. Duration balancing: `.round({largestUnit: 'days'})` converts hours to days. `.total({unit: 'minutes'})` returns total minutes. Durations are relative — `duration.total({unit: 'months', relativeTo: date})` requires a reference point for variable-length units. `.sign` indicates negative durations. `.blank` checks if duration is zero. `Temporal.Duration` supports `from()` with partial fields (defaults to 0) and string ISO 8601 duration format.
