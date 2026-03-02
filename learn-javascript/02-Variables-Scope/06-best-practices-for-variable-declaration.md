## Best Practices for Variable Declaration

Best practices for variable declaration help ensure **readable, maintainable, and bug-free JavaScript code**. Interviewers often ask this to evaluate whether you follow **modern JavaScript standards**.

---

# 1. Prefer `const` by Default

### Rule

Use **`const` unless the variable needs to change**.

```js
const API_URL = "https://api.example.com";
const user = { name: "John" };
```

### Why?

* Prevents accidental reassignment
* Makes code predictable
* Improves readability
* Signals intent clearly

Example problem:

```js
let taxRate = 0.1;
taxRate = 0.5; // accidental change
```

Better:

```js
const taxRate = 0.1;
```

---

# 2. Use `let` Only When Reassignment is Needed

### Rule

Use `let` when the variable **value will change**.

Example:

```js
let counter = 0;

counter++;
```

Common use cases:

* Counters
* Loops
* State updates
* Temporary values

Example:

```js
let total = 0;

for (let i = 0; i < items.length; i++) {
  total += items[i];
}
```

---

# 3. Avoid `var`

### Rule

Do not use `var` in modern JavaScript.

Problems with `var`:

* Function-scoped instead of block-scoped
* Hoisting confusion
* Global pollution risk
* Redeclaration allowed

Example problem:

```js
if (true) {
  var x = 10;
}

console.log(x); // 10 (unexpected)
```

Better:

```js
if (true) {
  let x = 10;
}
```

---

# 4. Always Declare Variables

### Rule

Never create variables without `let`, `const`, or `var`.

Bad:

```js
x = 10;
```

Creates global variable.

Good:

```js
let x = 10;
```

---

# 5. Keep Scope as Small as Possible

### Rule

Declare variables **inside the smallest scope needed**.

Bad:

```js
let result;

function calculate() {
  result = 10;
}
```

Good:

```js
function calculate() {
  let result = 10;
}
```

Benefits:

* Avoids conflicts
* Easier debugging
* Better memory usage

---

# 6. Declare Variables Close to Usage

### Rule

Declare variables where they are needed.

Bad:

```js
let total;
let tax;
let finalAmount;

total = 100;
tax = 10;
finalAmount = total + tax;
```

Better:

```js
const total = 100;
const tax = 10;
const finalAmount = total + tax;
```

Improves readability.

---

# 7. Use Meaningful Variable Names

### Rule

Variable names should describe their purpose.

Bad:

```js
let x = 10;
let y = 20;
```

Good:

```js
let width = 10;
let height = 20;
```

---

# 8. Use Consistent Naming Conventions

### Rule

Use **camelCase** for variables.

Good:

```js
let userName;
let totalAmount;
let isLoggedIn;
```

Bad:

```js
let username;
let TOTAL;
let user_name;
```

---

# 9. Initialize Variables When Declaring

### Rule

Initialize variables immediately if possible.

Bad:

```js
let total;
total = 100;
```

Better:

```js
let total = 100;
```

Benefits:

* Reduces undefined errors
* Cleaner code

---

# 10. Avoid Unnecessary Variables

### Rule

Do not create variables that are used only once.

Bad:

```js
const sum = a + b;
return sum;
```

Better:

```js
return a + b;
```

---

# 11. Use Destructuring When Appropriate

Better readability.

Example:

```js
const user = {
  name: "John",
  age: 25
};

const { name, age } = user;
```

Instead of:

```js
const name = user.name;
const age = user.age;
```

---

# 12. Use Uppercase for Constants

Convention for fixed values.

Example:

```js
const MAX_USERS = 100;
const PI = 3.14;
```

Signals that value should not change.

---

# 13. Avoid Reassigning Different Types

Bad:

```js
let data = 10;

data = "Hello";
```

Hard to maintain.

Better:

```js
let count = 10;
let message = "Hello";
```

---

# 14. Prefer Immutable Patterns

Avoid mutating values unnecessarily.

Bad:

```js
let numbers = [1,2,3];
numbers.push(4);
```

Better:

```js
const numbers = [1,2,3];
const newNumbers = [...numbers, 4];
```

Common in React development.

---

# 15. Perfect Interview Answer

> Best practices for variable declaration include using `const` by default, using `let` only when reassignment is required, avoiding `var`, declaring variables in the smallest possible scope, always initializing variables, and using meaningful names. These practices improve code reliability and maintainability.

---

Next major topic:

**3. Data Types**

This includes:

* Primitive vs Reference types
* Pass by value vs reference
* Mutability vs immutability
* typeof quirks (important interview traps)

This is one of the **most asked JavaScript topics after closures and event loop**.
