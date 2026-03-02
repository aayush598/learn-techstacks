## `undefined` Primitive Type in JavaScript (Detailed Interview Explanation)

### Definition

`undefined` is a primitive type that represents a **variable that has been declared but not assigned a value**.

```js
let x;
console.log(x);
```

Output:

```
undefined
```

This means:

> The variable exists in memory but has no value assigned.

---

# 1. Type of Undefined

```js
typeof undefined
```

Output:

```
"undefined"
```

Unlike `null`, this is correct and consistent.

---

# 2. When `undefined` Occurs (Very Important)

Interviewers frequently ask this.

---

## 1️⃣ Declared but Not Initialized

```js
let a;
console.log(a);
```

Output:

```
undefined
```

Memory behavior:

```
a → undefined
```

---

## 2️⃣ Function Without Return

```js
function test() {}

console.log(test());
```

Output:

```
undefined
```

Because no value is returned.

---

## 3️⃣ Missing Function Argument

```js
function greet(name){
 console.log(name);
}

greet();
```

Output:

```
undefined
```

Argument not passed → undefined.

---

## 4️⃣ Accessing Non-Existing Object Property

```js
const user = {
 name: "John"
};

console.log(user.age);
```

Output:

```
undefined
```

Property does not exist.

---

## 5️⃣ Array Index That Does Not Exist

```js
const arr = [1,2,3];

console.log(arr[10]);
```

Output:

```
undefined
```

---

## 6️⃣ Explicit Assignment

You can assign undefined manually.

```js
let x = undefined;
```

But this is **not recommended**.

Better:

```
null
```

For intentional emptiness.

---

# 3. Undefined vs Not Defined (Interview Trap)

Very common confusion.

---

## Undefined

Variable exists but has no value.

```js
let a;

console.log(a);
```

Output:

```
undefined
```

---

## Not Defined

Variable does not exist.

```js
console.log(b);
```

Output:

```
ReferenceError: b is not defined
```

---

## Interview Explanation

> Undefined means declared but not assigned. Not defined means the variable does not exist.

---

# 4. Undefined and Hoisting

With `var`:

```js
console.log(a);

var a = 10;
```

Output:

```
undefined
```

Because hoisting happens:

Behind the scenes:

```js
var a;
console.log(a);
a = 10;
```

---

With `let`:

```js
console.log(a);

let a = 10;
```

Output:

```
ReferenceError
```

Because of **Temporal Dead Zone**.

---

# 5. Undefined in JSON (Interview Level)

Undefined is **not valid in JSON**.

Example:

```js
JSON.stringify({
 a: undefined
});
```

Output:

```
{}
```

Undefined values are removed.

---

# 6. Undefined vs Null (Preview)

| undefined            | null                   |
| -------------------- | ---------------------- |
| Default value        | Assigned intentionally |
| Automatic            | Manual                 |
| Means "not assigned" | Means "empty value"    |

Example:

```js
let a;
let b = null;
```

---

# 7. Checking for Undefined

---

## Method 1 (Recommended)

```js
value === undefined
```

---

## Method 2

```js
typeof value === "undefined"
```

Safe if variable may not exist.

Example:

```js
typeof x === "undefined"
```

Does NOT throw error.

---

## Dangerous Method

```js
x === undefined
```

Throws error if `x` not declared.

---

# 8. Undefined in Objects

```js
const obj = {
 name: undefined
};

console.log(obj.name);
```

Output:

```
undefined
```

But property exists.

Check:

```js
"name" in obj
```

Output:

```
true
```

---

Compare with missing property:

```js
const obj = {};

console.log(obj.name);
```

Output:

```
undefined
```

Check:

```js
"name" in obj
```

Output:

```
false
```

---

# 9. Undefined in Default Parameters

```js
function greet(name = "Guest"){
 console.log(name);
}

greet(undefined);
```

Output:

```
Guest
```

Because undefined triggers default value.

---

But:

```js
greet(null);
```

Output:

```
null
```

Because null is a value.

---

# 10. Undefined in Comparisons

---

## Loose Equality

```js
undefined == null
```

Output:

```
true
```

---

## Strict Equality

```js
undefined === null
```

Output:

```
false
```

---

# 11. Boolean Conversion

```js
Boolean(undefined)
```

Output:

```
false
```

Undefined is falsy.

---

# 12. Memory Representation

```
let a;
```

Memory:

```
a → undefined
```

---

Assignment:

```js
let b = a;
```

Memory:

```
a → undefined
b → undefined
```

Stored by value.

---

# 13. Important Interview Edge Cases

---

## Case 1

```js
typeof undefined
```

Result:

```
"undefined"
```

---

## Case 2

```js
undefined == null
```

Result:

```
true
```

---

## Case 3

```js
undefined === null
```

Result:

```
false
```

---

## Case 4

```js
Boolean(undefined)
```

Result:

```
false
```

---

## Case 5

```js
Number(undefined)
```

Result:

```
NaN
```

---

## Case 6

```js
String(undefined)
```

Result:

```
"undefined"
```

---

# 14. Best Practices

### Avoid Assigning Undefined Manually

Bad:

```js
let x = undefined;
```

Better:

```js
let x = null;
```

---

### Use Undefined Checks Carefully

Best:

```js
typeof x === "undefined"
```

---

### Use Default Values

```js
let value = input ?? "default";
```

---

# Final Interview Summary (Strong Answer)

> Undefined is a primitive type representing a variable that has been declared but not assigned a value. It occurs automatically in situations like uninitialized variables, missing function arguments, and non-existing object properties. Undefined is falsy and stored by value.

---

Next most important primitive topic:

**null (very commonly paired with undefined in interviews)**
