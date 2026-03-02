## `boolean` Primitive Type in JavaScript (Detailed Interview Explanation)

### Definition

A **boolean** represents a logical value in JavaScript. It can have only two possible values:

```js
true
false
```

Booleans are used for **decision making, comparisons, and control flow**.

```js
let isLoggedIn = true;
let hasPermission = false;
```

Booleans are:

* Primitive values
* Immutable
* Stored by value
* Used in conditions and logical operations

---

# 1. Boolean Values

### Literal Booleans

```js
let a = true;
let b = false;
```

### Boolean from Expressions

```js
let result = 10 > 5;

console.log(result);
```

Output:

```
true
```

Comparison operations return booleans.

---

# 2. Boolean Conversion

JavaScript automatically converts values into boolean when needed.

This happens in:

* `if` statements
* loops
* logical operators

Example:

```js
if (1) {
 console.log("runs");
}
```

Because `1` converts to `true`.

---

## Explicit Boolean Conversion

### Using Boolean()

```js
Boolean(1)     // true
Boolean(0)     // false
Boolean("hi")  // true
Boolean("")    // false
```

---

## Using Double NOT (!!)

Very common in real projects.

```js
!!1      // true
!!0      // false
!!"hi"   // true
!!""     // false
```

Explanation:

* First `!` converts to boolean and reverses
* Second `!` reverses again

Example:

```js
!!"hello"
```

Result:

```
true
```

---

# 3. Truthy and Falsy Values (Very Important)

JavaScript does not require explicit booleans.

Values automatically convert to true or false.

---

## Falsy Values (Memorize These)

There are exactly **6 falsy values**:

```
false
0
""
null
undefined
NaN
```

Example:

```js
if (0) {
 console.log("runs");
}
```

Does NOT run.

---

## Truthy Values

Everything else is truthy.

Examples:

```
true
1
-1
"hello"
[]
{}
"false"
"0"
```

---

## Interview Trap

```js
Boolean("false")
```

Result:

```
true
```

Because non-empty string.

---

Another trap:

```js
Boolean([])
```

Result:

```
true
```

Empty arrays are truthy.

---

Another trap:

```js
Boolean({})
```

Result:

```
true
```

Empty objects are truthy.

---

# 4. Boolean Operators

---

## AND Operator `&&`

Returns true if both operands are true.

```js
true && true
```

Result:

```
true
```

Example:

```js
5 > 2 && 10 > 5
```

Result:

```
true
```

---

## OR Operator `||`

Returns true if at least one operand is true.

```js
true || false
```

Result:

```
true
```

---

## NOT Operator `!`

Reverses boolean.

```js
!true
```

Result:

```
false
```

---

# 5. Logical Operators Return Values (Important Interview Topic)

Logical operators do not always return booleans.

---

## AND Returns First Falsy or Last Truthy

```js
true && "Hello"
```

Result:

```
Hello
```

Example:

```js
0 && 5
```

Result:

```
0
```

---

## OR Returns First Truthy Value

```js
0 || 10
```

Result:

```
10
```

Example:

```js
"hi" || "hello"
```

Result:

```
hi
```

---

## Real World Usage

Default values:

```js
let username = input || "Guest";
```

If `input` falsy → "Guest".

---

# 6. Boolean vs Boolean Object (Interview Trap)

Primitive boolean:

```js
let a = true;
```

Boolean object:

```js
let b = new Boolean(true);
```

---

## Difference

```js
typeof a
```

Result:

```
boolean
```

```js
typeof b
```

Result:

```
object
```

---

## Dangerous Behavior

```js
if (new Boolean(false)) {
 console.log("runs");
}
```

It runs because objects are truthy.

---

## Interview Rule

> Never use `new Boolean()`.

---

# 7. Comparison Operators Returning Boolean

These return boolean values.

---

## Equality

```js
5 == "5"
```

Result:

```
true
```

Type coercion occurs.

---

## Strict Equality

```js
5 === "5"
```

Result:

```
false
```

No type conversion.

---

## Inequality

```js
5 != 6
```

Result:

```
true
```

---

## Strict Inequality

```js
5 !== "5"
```

Result:

```
true
```

---

## Greater/Less

```js
10 > 5
```

Result:

```
true
```

---

# 8. Boolean in Conditions

---

## if Statement

```js
let isAdmin = true;

if (isAdmin) {
 console.log("Access granted");
}
```

---

## Ternary Operator

```js
let result = isAdmin ? "Yes" : "No";
```

---

## While Loop

```js
let i = 0;

while(i < 3){
 i++;
}
```

---

# 9. Memory Behavior

Boolean values are stored **by value**.

```js
let a = true;
let b = a;

b = false;
```

Result:

```
a = true
b = false
```

Independent copies.

---

# 10. Important Interview Edge Cases

---

## Case 1

```js
Boolean("0")
```

Result:

```
true
```

---

## Case 2

```js
Boolean(" ")
```

Result:

```
true
```

Space is truthy.

---

## Case 3

```js
Boolean(null)
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
Boolean(NaN)
```

Result:

```
false
```

---

## Case 6

```js
!![]
```

Result:

```
true
```

---

## Case 7

```js
!!{}
```

Result:

```
true
```

---

# Final Interview Summary (Strong Answer)

> Boolean is a primitive type representing true or false values. JavaScript automatically converts values into booleans in conditions, where falsy values include false, 0, empty string, null, undefined, and NaN, while all other values are truthy. Boolean values are immutable and stored by value.

---

Next most important primitive topic:

**undefined vs null (extremely common interview question)**
