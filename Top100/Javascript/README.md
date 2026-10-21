# JavaScript Interview Questions and Answers

## Q1: What is JavaScript?
**A:** JavaScript is a high-level, interpreted programming language primarily used for web development. It's a core technology of the web alongside HTML and CSS, enabling dynamic, interactive web pages. It supports event-driven, functional, and object-oriented programming paradigms.

## Q2: What is the difference between `var`, `let`, and `const`?
**A:** `var` has function scope and hoisting with undefined initialization. `let` and `const` have block scope and hoisting without initialization (Temporal Dead Zone). `const` cannot be reassigned but its properties can be mutated. `let` allows reassignment. Prefer `const` by default, `let` when reassignment is needed.

## Q3: Explain hoisting in JavaScript.
**A:** Hoisting moves declarations to the top of their scope during compilation. `var` declarations are hoisted and initialized to `undefined`. `let` and `const` are hoisted but not initialized (ReferenceError if accessed before declaration). Function declarations are fully hoisted; function expressions are not.

## Q4: What is the difference between `==` and `===`?
**A:** `==` (abstract equality) performs type coercion before comparing values. `===` (strict equality) checks both value and type without coercion. Example: `5 == "5"` is true, `5 === "5"` is false. Always prefer `===` to avoid unexpected type coercion bugs.

## Q5: What is closure in JavaScript?
**A:** A closure is a function that retains access to its lexical scope even when executed outside that scope. Inner functions "close over" variables from outer functions. Closures enable data privacy, factory functions, and callbacks. Example: function factories that preserve state across calls.

## Q6: Explain the event loop in JavaScript.
**A:** The event loop enables JavaScript's non-blocking concurrency despite being single-threaded. It continuously checks the call stack and task queues. When the stack is empty, it processes microtasks (Promise callbacks, MutationObserver), then macrotasks (setTimeout, DOM events, I/O). This ensures asynchronous operations don't block execution.

## Q7: What is `this` in JavaScript?
**A:** `this` refers to the execution context. Its value depends on how a function is called: global context (window/global), object method (the object), constructor (new instance), arrow functions (lexical `this` from enclosing scope), or explicit binding with `call`/`apply`/`bind`.

## Q8: How does `call`, `apply`, and `bind` differ?
**A:** `call(thisArg, arg1, arg2, ...)` invokes a function with given `this` and arguments spread. `apply(thisArg, [argsArray])` is similar but accepts arguments as an array. `bind(thisArg, ...)` returns a new function permanently bound to `this`, without immediate invocation. All three set `this` explicitly.

## Q9: What is prototypal inheritance?
**A:** JavaScript uses prototypal inheritance where objects inherit from other objects via the prototype chain. Each object has an internal `[[Prototype]]` (accessed via `Object.getPrototypeOf()` or `__proto__`). When a property is not found on the object, JS looks up the chain. `Object.create()` sets prototypes explicitly.

## Q10: What is the difference between `null` and `undefined`?
**A:** `undefined` means a variable has been declared but not assigned a value. `null` is an intentional absence of any object value. `typeof null` returns "object" (a known bug). `typeof undefined` returns "undefined". `null == undefined` is true, `null === undefined` is false.

## Q11: Explain Promises in JavaScript.
**A:** A Promise represents an asynchronous operation's eventual completion or failure. It has three states: pending, fulfilled, resolved. `.then()` handles resolution, `.catch()` handles rejection, `.finally()` runs regardless. Promises chain to avoid callback hell. `Promise.all()`, `Promise.race()`, `Promise.allSettled()` handle multiple promises.

## Q12: What is async/await and how does it work?
**A:** `async/await` is syntactic sugar over Promises. An `async` function returns a Promise. `await` pauses execution until a Promise settles, then resumes with the resolved value. `await` can only be used inside `async` functions. Error handling uses try/catch blocks. It makes asynchronous code read synchronously.

## Q13: Explain event delegation.
**A:** Event delegation leverages event bubbling by attaching a single event listener to a parent element to handle events from multiple children. The event target (`event.target`) identifies which child triggered the event. Benefits: improved performance (fewer listeners), dynamic element handling, and cleaner code.

## Q14: What is the difference between `event.preventDefault()` and `event.stopPropagation()`?
**A:** `preventDefault()` prevents the browser's default behavior (like link navigation or form submission). `stopPropagation()` prevents the event from bubbling up the DOM tree. `stopImmediatePropagation()` also prevents other listeners on the same element from firing. Neither stops other element handlers.

## Q15: What are arrow functions and how are they different from regular functions?
**A:** Arrow functions (`() => {}`) are shorter syntax and do not have their own `this` (inherit lexically). They cannot be used as constructors (no `new`), don't have `arguments` object (use rest params), and can't be used as generators. They're ideal for callbacks and functional programming.

## Q16: Explain destructuring in JavaScript.
**A:** Destructuring unpacks values from arrays or properties from objects into distinct variables. Examples: `const [a, b] = [1, 2]` for arrays, `const {name, age} = obj` for objects. Supports default values, rest patterns (`...rest`), and nested destructuring. Works in function parameters too.

## Q17: What is the spread operator and rest parameter?
**A:** Spread (`...`) expands iterables into individual elements. Use: array/object copying (`[...arr]`, `{...obj}`), function calls (`func(...args)`), and array concatenation. Rest parameter collects multiple elements into an array in function definitions (`function(...args)`) and destructuring patterns.

## Q18: How does `Array.prototype.map` work?
**A:** `map()` creates a new array by applying a callback to each element. It doesn't mutate the original array. Callback receives `(element, index, array)`. Returns new array of same length. Chainable with other array methods. Example: `[1,2,3].map(x => x * 2)` returns `[2,4,6]`.

## Q19: What is the difference between `map`, `filter`, and `reduce`?
**A:** `map` transforms each element and returns new array (same length). `filter` returns a subset based on a condition. `reduce` accumulates values into a single result (any type). They're all array methods supporting functional programming. `reduce` is most flexible; `map` and `filter` are specialized cases.

## Q20: Explain `Array.prototype.reduce` with examples.
**A:** `reduce(callback, initialValue)` processes array elements left-to-right, accumulating a result. Callback receives `(accumulator, current, index, array)`. Without initialValue, first element is accumulator. Examples: sum `arr.reduce((a,b) => a+b, 0)`, flatten `arr.reduce((a,b) => a.concat(b), [])`, group by property.

## Q21: What is the difference between `for...in` and `for...of`?
**A:** `for...in` iterates over enumerable property keys (includes prototype chain) — use for objects. `for...of` iterates over iterable values — use for arrays, strings, Maps, Sets. `for...of` requires Symbol.iterator. `for...in` on arrays iterates indices as strings.

## Q22: What is `Symbol` in JavaScript?
**A:** Symbol is a unique, immutable primitive introduced in ES6. Created via `Symbol('description')`. Guaranteed to be unique (even with same description). Used as object property keys to avoid naming collisions, for private-like properties, and for defining well-known symbols (Symbol.iterator, Symbol.toStringTag).

## Q23: Explain the Temporal Dead Zone (TDZ).
**A:** TDZ is the time between entering a scope and a `let`/`const` variable being declared. Accessing the variable during TDZ throws `ReferenceError`. This prevents accessing uninitialized variables. `var` doesn't have TDZ because it's initialized to `undefined` on hoisting. TDZ also applies to `class` declarations.

## Q24: What is a `Map` in JavaScript?
**A:** `Map` is a collection of key-value pairs where keys can be any type (objects, functions, primitives). Preserves insertion order. Provides `set`, `get`, `has`, `delete`, `size`, `clear` methods. Better than plain objects for frequent additions/deletions and non-string keys. `WeakMap` allows garbage collection of keys.

## Q25: What is a `Set` in JavaScript?
**A:** `Set` is a collection of unique values of any type. Preserves insertion order. Provides `add`, `has`, `delete`, `size`, `clear`. Useful for deduplication (`[...new Set(arr)]`), intersection, and difference. `WeakSet` stores objects only and allows garbage collection.

## Q26: How does `Object.assign` work?
**A:** `Object.assign(target, ...sources)` copies enumerable own properties from source objects to target (shallow copy). Later sources overwrite earlier ones. Returns the target object. Used for object merging, cloning, and default options. For deep cloning, use `structuredClone` or libraries.

## Q27: What is `JSON.stringify` and `JSON.parse`?
**A:** `JSON.stringify(obj)` converts a JavaScript object to a JSON string. `JSON.parse(str)` converts a JSON string back to an object. `stringify` accepts replacer (function/array to filter) and space for formatting. `parse` accepts reviver to transform values. Both throw on circular references.

## Q28: Explain the concept of immutability in JavaScript.
**A:** Immutability means data cannot be changed after creation. Primitive values are immutable. Objects/arrays are mutable but can be treated immutably by creating copies (`Object.assign`, spread, `toSorted`, `toReversed`, `toSpliced`). Immutability prevents side effects, simplifies debugging, and is essential in React/Redux.

## Q29: What is `Object.freeze` vs `Object.seal`?
**A:** `Object.freeze(obj)` makes all properties read-only and prevents adding/removing properties (deep freeze not automatic). `Object.seal(obj)` prevents adding/removing properties but allows changing existing property values. `Object.isFrozen()` and `Object.isSealed()` check status.

## Q30: How do you check if an object has a property?
**A:** Three ways: `'prop' in obj` (checks prototype chain), `obj.hasOwnProperty('prop')` (own properties only, deprecated if obj overrides it), `Object.hasOwn(obj, 'prop')` (ES2022, recommended). `obj.prop !== undefined` can be misleading if the value is intentionally undefined.

## Q31: What is `try...catch...finally` in JavaScript?
**A:** Error handling block. `try` contains code that may throw. `catch(err)` handles the error (catch binding is optional in ES2022). `finally` always executes regardless of error. Thrown errors can be any type. Custom errors extend `Error` class. Uncaught errors propagate up the call stack.

## Q32: What is the difference between `throw` and `throw new Error()`?
**A:** `throw` can throw any expression (strings, numbers, objects). `throw new Error('msg')` throws an Error instance with proper stack trace, name, and message. Always prefer throwing Error objects for proper debugging. `throw` without try/catch terminates the script.

## Q33: Explain JavaScript's `strict mode`.
**A:** `"use strict"` enables stricter parsing and error handling. Changes: prevents accidental globals, eliminates `this` coercion (undefined instead of window), disallows duplicate parameters, makes eval safer, and disables `with` and `arguments.callee`. Can be file-level or function-level. ES Modules are strict by default.

## Q34: What are template literals?
**A:** Template literals use backticks (`` ` ``) instead of quotes. Support: string interpolation (`${expr}`), multi-line strings (preserve newlines), and tagged templates (function`str`). Tagged templates process template literal parts for escaping, i18n, or custom formatting. Available since ES6.

## Q35: What is `Proxy` in JavaScript?
**A:** `Proxy` wraps an object to intercept and customize fundamental operations (get, set, has, deleteProperty, apply, construct, etc.). Example: validation, logging, caching, reactive programming. The handler object defines traps. `Reflect` API complements Proxy by providing default behavior for each trap.

## Q36: How does `Reflect` API work?
**A:** `Reflect` provides methods for interceptable JavaScript operations (same names as Proxy traps). Examples: `Reflect.get()`, `Reflect.set()`, `Reflect.has()`, `Reflect.ownKeys()`. Unlike older APIs: returns Boolean for success/failure and throws fewer exceptions. Used inside Proxy traps for default behavior.

## Q37: What is the difference between `slice` and `splice`?
**A:** `slice(begin, end)` returns a new array (shallow copy) from indices begin to end-1. Original unchanged. `splice(start, deleteCount, ...items)` modifies the original array (adds/removes items) and returns deleted elements. `slice` is non-mutating; `splice` is mutating.

## Q38: Explain `Array.from` and `Array.of`.
**A:** `Array.from(arrayLike, mapFn?)` converts iterables or array-like objects to arrays. Works with strings, NodeLists, Sets, Maps, arguments. Optional map function. `Array.of(...elements)` creates array from arguments (differs from `Array()`: `Array.of(3)` is `[3]`, `Array(3)` is `[,,,]`).

## Q39: What is the difference between `Array.isArray` and `instanceof Array`?
**A:** `Array.isArray(value)` reliably checks if a value is an array, even across realms (iframes, different windows). `instanceof Array` may fail across execution contexts. `Array.isArray` is the recommended method. `typeof` is useless (`typeof []` is "object").

## Q40: How do you deep clone an object in JavaScript?
**A:** Modern: `structuredClone(obj)` (available in most runtimes). Alternatives: `JSON.parse(JSON.stringify(obj))` (fails on functions, Dates become strings, circular refs), recursive cloning function, or libraries like Lodash `cloneDeep`. `structuredClone` handles Dates, Maps, Sets, arrays, and circular references.

## Q41: What are JavaScript generators?
**A:** Generator functions (`function*`) return a Generator object that can be exited and re-entered, preserving state. `yield` produces values lazily. `next()` returns `{value, done}`. Generators enable custom iteration, infinite sequences, and async programming (with `yield` + Promises).

## Q42: What is the difference between `async/await` and Generators?
**A:** `async/await` returns Promises automatically, has built-in error handling (try/catch), and is simpler syntax. Generators (`function*`) require manual Promise handling (or libraries like `co`) for async control flow. Generators are more flexible (can pause/resume for any reason). `async/await` is built on Promises.

## Q43: Explain `String.prototype` methods for searching.
**A:** `indexOf(substr)` returns first index (-1 if not found). `includes(substr)` returns boolean (ES6). `startsWith(substr)` / `endsWith(substr)` check prefix/suffix. `search(regex)` returns index. `match(regex)` returns array of matches or null. `matchAll(regex)` returns iterator of all matches. `replace` / `replaceAll` substitute matches.

## Q44: What is `Intl` in JavaScript?
**A:** The `Intl` object provides internationalization: `Intl.DateTimeFormat` (date/time formatting), `Intl.NumberFormat` (numbers, currencies, units), `Intl.Collator` (string comparison), `Intl.ListFormat` (list formatting), `Intl.RelativeTimeFormat` (relative time). Uses locale-aware formatting.

## Q45: What is `requestAnimationFrame`?
**A:** `requestAnimationFrame(callback)` tells the browser to call a function before the next repaint. It's the standard way for JS animations (60fps sync). Provides timestamp argument. Pauses automatically when tab is inactive (saves battery/CPU). More efficient than setTimeout-based animations. Returns ID for cancellation.

## Q46: How does `setTimeout` and `setInterval` work?
**A:** `setTimeout(cb, delay)` fires callback once after delay. `setInterval(cb, interval)` fires repeatedly. Both return integer IDs cleared by `clearTimeout(id)` / `clearInterval(id)`. Minimum delay is 4ms (nested 5+ deep). Inactive tabs throttle to 1000ms. For animation, use `requestAnimationFrame`.

## Q47: What is `fetch` API and how is it used?
**A:** `fetch(url, options)` returns a Promise that resolves to the Response object. Options: method, headers, body, credentials. Response methods: `.json()`, `.text()`, `.blob()`, `.formData()`. Check `response.ok` (200-299) or `response.status`. Error handling: `.catch()` for network errors; check status manually for HTTP errors.

## Q48: Explain CORS in JavaScript.
**A:** CORS (Cross-Origin Resource Sharing) is a browser security mechanism restricting cross-origin requests. The server must include headers: `Access-Control-Allow-Origin: *` (or specific origin), methods, and headers. Preflight requests (OPTIONS) check permissions for non-simple requests. Credentials require specific `Access-Control-Allow-Credentials`.

## Q49: What is the difference between `localStorage`, `sessionStorage`, and `cookies`?
**A:** `localStorage` persists until manually cleared (~5-10MB), no expiration. `sessionStorage` clears when tab closes. Cookies are sent with every HTTP request (~4KB), have expiration, can be HttpOnly/Secure/SameSite. `localStorage`/`sessionStorage` are client-only; cookies support server-side access.

## Q50: What is IndexedDB?
**A:** IndexedDB is a low-level NoSQL database in browsers for storing large amounts of structured data. Supports indexes, transactions, versioning, and key-value storage. Asynchronous API. Object stores are like tables; indexes enable fast lookups. Used for offline apps, caches, and complex client-side data.

## Q51: Explain the DOM (Document Object Model).
**A:** DOM is a programming interface for HTML/XML documents, representing the page as a tree of nodes. JavaScript can access and modify the DOM via methods like `getElementById`, `querySelector`, `createElement`, `appendChild`. DOM manipulation is expensive (triggers layout/reflow). Minimize direct DOM changes.

## Q52: What is event bubbling and capturing?
**A:** Event propagation has three phases: capturing (window -> target), target, bubbling (target -> window). Default listeners fire during bubbling. `addEventListener(type, handler, {capture: true})` switches to capturing phase. `event.stopPropagation()` stops propagation. Most events bubble, but `focus`, `blur`, `load` don't.

## Q53: What is `document.createDocumentFragment`?
**A:** `DocumentFragment` is a lightweight DOM node that exists outside the document tree. Batch DOM operations on a fragment, then append it once. This minimizes reflows/repaints. Example: building a list of 1000 items in a fragment, then appending once is much faster than appending each individually.

## Q54: Explain `MutationObserver`.
**A:** `MutationObserver` watches DOM changes (childList, attributes, characterData, subtree). Callback receives mutations array. More efficient than DOM mutation events (deprecated). Uses: detecting content changes, custom element polyfills, monitoring third-party scripts. Disconnect with `observer.disconnect()`.

## Q55: What is `IntersectionObserver`?
**A:** `IntersectionObserver` asynchronously observes visibility of elements relative to a parent or viewport. Used for lazy loading images, infinite scroll, animation triggers, ad tracking. Options: root, rootMargin, threshold. Callback receives entries with `isIntersecting`, `intersectionRatio`. More efficient than scroll event listeners.

## Q56: What is `ResizeObserver`?
**A:** `ResizeObserver` reports changes to an element's content or border box. Unlike window resize events, it watches specific elements. Callback receives entries with `contentRect` (new size). Used for responsive components, canvas resizing, and adaptive layouts. Supported in modern browsers.

## Q57: What is the difference between `display: none` and `visibility: hidden`?
**A:** `display: none` removes the element from the document flow (no space occupied, not rendered). `visibility: hidden` hides the element visually but it still occupies space in the layout. `display: none` affects layout; `visibility: hidden` doesn't. Accessibility: both hide from screen readers.

## Q58: What are Web Workers?
**A:** Web Workers run JavaScript in background threads with no DOM access. Communication with main thread via `postMessage()` and `onmessage` events. Workers can use `importScripts()` for dependencies. Types: dedicated (single parent), shared (multiple parents, more complex). Use for CPU-intensive tasks.

## Q59: What is Service Worker?
**A:** Service Worker is a script that runs in the background, separate from web pages, enabling intercept and control of network requests. Essential for Progressive Web Apps (offline support), caching strategies (Cache First, Network First), push notifications, and background sync. Lifecycle: install -> activate -> fetch.

## Q60: Explain the module pattern in JavaScript.
**A:** The module pattern uses closures to create private and public scopes. IIFE returns an object with public methods that have access to private variables. ES6 introduced native modules: `export` and `import`. Module-based code is better organized, avoids global pollution, and enables tree-shaking.

## Q61: What are ES6 modules and how do they differ from CommonJS?
**A:** ES6 modules (`import`/`export`) are static (imports are hoisted, tree-shakable), have named and default exports, and are asynchronous. CommonJS (`require()`/`module.exports`) is dynamic (can import conditionally), synchronous, used in Node.js. ES6 modules are statically analyzable, enabling better optimization.

## Q62: What is tree-shaking?
**A:** Tree-shaking is dead code elimination based on ES module static structure. Bundlers (Webpack, Rollup, esbuild) remove unused exports during build. Only ES module syntax enables tree-shaking, not CommonJS. Proper tree-shaking requires side-effect-free imports and production mode.

## Q63: What is the difference between `default export` and `named export`?
**A:** Named exports: `export const foo = ...`; import with same name: `import { foo }`. Default export: `export default ...`; import with any name: `import anyName`. A module can have multiple named exports but only one default export. Named exports are explicit; default export is the module's main feature.

## Q64: Explain `import()` dynamic imports.
**A:** Dynamic `import()` returns a Promise for lazy-loading modules. Useful for code-splitting (loading code on demand), route-based splitting in frameworks, and conditional imports. Syntax: `const module = await import('./path')`. Webpack/Rollup create separate chunks for dynamically imported modules.

## Q65: What is `this` binding in arrow functions?
**A:** Arrow functions don't have their own `this`. They inherit `this` from the enclosing lexical scope (where they're defined, not called). This makes arrow functions ideal for callbacks, event handlers in classes, and setTimeout/setInterval, as `this` is predictable and doesn't change.

## Q66: How does `Function.prototype.bind` work?
**A:** `bind(thisArg, ...args)` creates a new function with `this` permanently set to `thisArg` and optionally partial arguments applied (currying). The bound function can't be re-bound. Useful for preserving context in callbacks, event handlers, and creating partially applied functions.

## Q67: What is currying in JavaScript?
**A:** Currying transforms a function taking multiple arguments into a sequence of functions each taking one argument. Example: `const add = a => b => a + b`. Benefits: partial application, function composition, creating specialized functions from general ones. Can be implemented manually or with libraries.

## Q68: Explain function composition.
**A:** Composition combines functions where output of one becomes input of another. `const compose = (f, g) => x => f(g(x))`. Usually applied right-to-left (compose) or left-to-right (pipe). Libraries like Lodash provide `flow` (left-to-right). Composition enables building complex operations from simple functions.

## Q69: What is `reduceRight`?
**A:** `Array.prototype.reduceRight(callback, initialValue)` is like `reduce` but processes array from right to left. Useful for operations where order matters (like nested HTML element building or right-associative operations). Example: `[[1,2],[3,4]].reduceRight((a,b) => a.concat(b), [])`.

## Q70: Explain `flat` and `flatMap`.
**A:** `arr.flat(depth)` flattens nested arrays to specified depth (default 1). `Infinity` flattens completely. `arr.flatMap(fn)` maps each element then flattens result by 1 level. More efficient than `map` + `flat(1)`. Example: `["a b", "c d"].flatMap(s => s.split(" "))` returns `["a","b","c","d"]`.

## Q71: What are tagged template literals?
**A:** Tagged templates process template literals with a function. The function receives: string literals array (split by interpolations), and interpolated values as separate args. Used for: escaping HTML, styled-components (CSS-in-JS), GraphQL queries, and i18n. Example: `html`<div>${user}</div>`` sanitizes user input.

## Q72: What is `BigInt` in JavaScript?
**A:** `BigInt` represents integers larger than `Number.MAX_SAFE_INTEGER` (2^53 - 1). Created by appending `n` or `BigInt()`. Example: `9007199254740993n`. Can't mix with regular numbers in operations (must explicitly convert). `typeof` returns "bigint". No support for `Math` methods or `JSON.stringify`.

## Q73: What is `Optional Chaining` operator?
**A:** `?.` allows accessing nested object properties without checking each level for null/undefined. Returns `undefined` if any intermediate value is `null`/`undefined`. Examples: `obj?.prop`, `obj?.[expr]`, `func?.()`. Short-circuits evaluation. Prevents "Cannot read property of undefined" errors.

## Q74: What is the `Nullish Coalescing` operator?
**A:** `??` returns the right-hand side only when the left-hand side is `null` or `undefined`. Unlike `||`, it doesn't treat `0`, `""`, or `false` as falsy. Example: `const name = input ?? "default"`. Useful for providing defaults when a value might be null/undefined but not other falsy values.

## Q75: Explain `Promise.all`, `Promise.race`, `Promise.allSettled`, `Promise.any`.
**A:** `Promise.all(iterable)` resolves when all settle (rejects if any reject). `Promise.race` settles when first settles (resolve or reject). `Promise.allSettled` resolves when all settle with status/reason/value (never rejects). `Promise.any` resolves when first fulfills; rejects only if all reject (AggregateError).

## Q76: What is `AbortController` and how is it used with fetch?
**A:** `AbortController` cancels fetch requests (and other async operations). Create controller, pass `signal` to fetch options. Call `controller.abort()` to cancel. Fetch promise rejects with `AbortError`. Used for: canceling stale requests, timeout implementation, user-triggered cancellation.

## Q77: What is `EventSource` (Server-Sent Events)?
**A:** `EventSource` establishes a persistent HTTP connection for receiving server events (text/event-stream). Easier than WebSocket for one-way data flow (server to client). Automatic reconnection. Supports named events. Limitations: only GET, no binary data. Used for real-time feeds, notifications.

## Q78: Explain WebSocket.
**A:** WebSocket provides full-duplex communication over a single TCP connection. Initiated via HTTP upgrade handshake (ws:// or wss://). `socket.send()`, `socket.onmessage`, `socket.onclose`, `socket.onerror`. Used for real-time apps (chat, games, collaborative editing). No reconnection built-in (implement manually).

## Q79: What is `FormData` in JavaScript?
**A:** `FormData` captures form data for AJAX submission. `new FormData(formElement)` or `new FormData()` then `.append(key, value)`. Supports file uploads. Used with `fetch` (body: formData, no Content-Type header needed). Methods: append, delete, get, getAll, has, set, forEach, entries, keys, values.

## Q80: How do you handle errors in async/await?
**A:** Wrap await calls in try/catch. The catch block catches both synchronous and asynchronous errors. Multiple awaits can share one try/catch. For fine-grained handling, wrap each await individually. Alternatively, use `.catch()` on the promise returned by async functions.

## Q81: What is `debugger` statement?
**A:** `debugger;` halts JavaScript execution and opens debugger if available (browser DevTools or Node inspector). Acts like a breakpoint. Usually removed in production builds (linters/configs strip them). Useful for development debugging when you can't easily set breakpoints through the UI.

## Q82: What are `getters` and `setters` in JavaScript?
**A:** Getters (`get`) and setters (`set`) are special methods that behave like properties. Defined in object literals (`get prop() {}`) or classes. Getters compute values on access; setters validate/process values on assignment. `Object.defineProperty(obj, 'prop', {get, set})` adds them dynamically.

## Q83: Explain `Object.defineProperty` vs `Object.defineProperties`.
**A:** `Object.defineProperty(obj, prop, descriptor)` defines or modifies a single property. `Object.defineProperties(obj, props)` defines multiple. Descriptors: `value`, `writable`, `enumerable`, `configurable`, `get`, `set`. `value`/`writable` vs `get`/`set` are mutually exclusive. Configurable: true allows later descriptor changes.

## Q84: What is the difference between property descriptors: enumerable, writable, configurable?
**A:** `writable`: can value be changed (for data descriptors). `enumerable`: appears in `for...in` loops and `Object.keys()`. `configurable`: can descriptor be modified or property deleted. If not configurable: can't change descriptor type, can't delete, can't change configurable/writable flags.

## Q85: What is `Object.keys`, `Object.values`, `Object.entries`?
**A:** `Object.keys(obj)` returns array of enumerable own property names. `Object.values(obj)` returns values. `Object.entries(obj)` returns `[key, value]` pairs. All skip prototype chain. ES2017 introduced `values`/`entries`. Useful for iteration with `for...of`, `map`, `Object.fromEntries` reverses entries.

## Q86: What is `Object.fromEntries`?
**A:** `Object.fromEntries(iterable)` converts a list of key-value pairs into an object. Reverse of `Object.entries()`. Works with Map and arrays. Example: `Object.fromEntries([['a', 1], ['b', 2]])` returns `{a: 1, b: 2}`. Useful for transforming objects (entries -> filter/map -> fromEntries).

## Q87: What is `structuredClone`?
**A:** `structuredClone(value)` (ES2022+) creates a deep clone of a value. Handles objects, arrays, Maps, Sets, Dates, RegExps, Blobs, ArrayBuffers, and circular references. Cannot clone functions, DOM nodes, or prototypes. Throws `DataCloneError` if a value is not cloneable.

## Q88: Explain `at()` method for arrays and strings.
**A:** `arr.at(index)` returns element at index (supports negative indexing: -1 for last, -2 for second-to-last). Available for Array, String, and TypedArray prototypes. ES2022. Simpler than `arr[arr.length - 1]`. `-1` is more readable than `length - 1`.

## Q89: What is `Array.prototype.toSorted`, `toReversed`, `toSpliced`, `with`?
**A:** These are ES2023 non-mutating alternatives to their mutating counterparts. `toSorted()` returns sorted copy (vs `sort()`). `toReversed()` returns reversed copy (vs `reverse()`). `toSpliced()` returns copy with splice applied (vs `splice()`). `with(index, value)` returns copy with one changed value.

## Q90: What is `Array.prototype.find` and `findLast`?
**A:** `find(callback)` returns first element where callback returns truthy (or undefined). `findLast(callback)` (ES2023) searches from end. `findIndex` / `findLastIndex` return index or -1. `find` is better than `filter`[0] because it stops at first match.

## Q91: What is `Array.prototype.group` (or `Object.groupBy`)?
**A:** `Object.groupBy(items, callback)` (ES2024) groups array elements by string keys from callback. Returns object (no prototype). Example: `Object.groupBy(users, user => user.role)`. `Map.groupBy` returns a Map (supports non-string keys). Replaces manual reduce-based grouping.

## Q92: What is `Promise.withResolvers`?
**A:** `Promise.withResolvers()` (ES2024) returns an object with `promise`, `resolve`, and `reject` properties. Exposes the promise's resolve/reject externally without nesting callback constructs. Useful for converting callback-based APIs to promises, or creating resolvable promises outside executor scope.

## Q93: Explain `Intl.Segmenter`.
**A:** `Intl.Segmenter` (ES2024) segments text by grapheme, word, or sentence according to locale. Respects Unicode rules and locale-specific segmentation. Example: `new Intl.Segmenter('en', { granularity: 'word' }).segment(text)`. Returns iterable of segments with position metadata.

## Q94: What are Temporal objects in JavaScript?
**A:** Temporal is the modern date/time API (stage 3, polyfill available) replacing `Date`. Provides: `Temporal.Instant` (UTC instant), `Temporal.PlainDate` (date without time), `Temporal.PlainTime` (time without date), `Temporal.PlainDateTime` (date+time), `Temporal.ZonedDateTime` (with timezone), `Temporal.Duration`, `Temporal.Now`.

## Q95: What are `Atomics` and `SharedArrayBuffer`?
**A:** `SharedArrayBuffer` allows shared memory between Web Workers. `Atomics` provides atomic operations (add, load, store, compareExchange, wait, notify) for synchronization. Essential for concurrent shared memory access. Requires specific security headers (COOP, COEP) due to Spectre vulnerability.

## Q96: Explain the `Error` class hierarchy.
**A:** Built-in error types: `Error` (base), `SyntaxError` (parse errors), `ReferenceError` (undefined variables), `TypeError` (wrong type operations), `RangeError` (out of range), `URIError` (bad URI), `EvalError` (eval errors, rarely used). Custom errors: `class MyError extends Error {}`. Always set `this.name`.

## Q97: What are `CustomEvent`s?
**A:** `CustomEvent` creates user-defined events with custom data in the `detail` property. Example: `new CustomEvent('user-login', { detail: { userId: 123 } })`. Dispatch with `element.dispatchEvent(event)`. Listen with `addEventListener('user-login', handler)`. Events bubble by default (configurable).

## Q98: What is `Shadow DOM`?
**A:** Shadow DOM enables encapsulation of DOM subtrees (styles, markup) within a hidden boundary. Used in Web Components with `element.attachShadow({ mode: 'open' })`. Styles inside shadow DOM don't leak out; external styles don't leak in. `mode: 'closed'` prevents external access.

## Q99: What are Web Components?
**A:** Web Components are reusable custom elements built with three technologies: Custom Elements (define HTML tags), Shadow DOM (encapsulation), and HTML Templates (`<template>` element). Define with `class MyElement extends HTMLElement` and `customElements.define('my-element', MyElement)`. Lifecycle: connectedCallback, disconnectedCallback, attributeChangedCallback.

## Q100: What is `document.querySelector` vs `document.querySelectorAll`?
**A:** `querySelector(selector)` returns the first matching element (or null). `querySelectorAll(selector)` returns a static NodeList of all matches (not live, unlike `getElementsBy*`). Accepts any CSS selector (`#id`, `.class`, `[attr]`, `div > p`). More flexible than `getElementById`/`getElementsByClassName`.
