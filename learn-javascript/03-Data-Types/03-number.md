## `number` Primitive Type in JavaScript (Detailed Interview Explanation)

### Definition

The **`number`** type represents **numeric values** in JavaScript, including both **integers and floating-point numbers**.

```js
let age = 25;
let price = 99.99;
let temperature = -10;
```

JavaScript has **only one numeric type**:

> All numbers are stored as **64-bit floating-point values (IEEE 754 standard)**.

Unlike many languages, JavaScript does **not have separate types** for:

* int
* float
* double

Everything is a `number`.

---

# 1. How Numbers Are Stored Internally

JavaScript uses **IEEE 754 double precision floating point format**.

A number consists of:

* Sign bit
* Exponent
* Fraction (Mantissa)

This causes precision limitations.

---

## Floating Point Precision Problem (Very Common Interview Question)

```js
0.1 + 0.2
```

Result:

```
0.30000000000000004
```

### Why This Happens

Because decimal numbers cannot always be represented exactly in binary.

Example:

```
0.1 = infinite binary fraction
```

### Correct Way to Compare

```js
Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON
```

Interview explanation:

> JavaScript uses binary floating-point representation which causes precision errors.

---

# 2. Integer Limits

JavaScript can safely represent integers between:

```
-(2^53 - 1)  to  (2^53 - 1)
```

Maximum safe integer:

```js
Number.MAX_SAFE_INTEGER
```

Value:

```
9007199254740991
```

Minimum safe integer:

```js
Number.MIN_SAFE_INTEGER
```

Value:

```
-9007199254740991
```

---

## Precision Loss Example

```js
9007199254740991 + 1 === 9007199254740991 + 2
```

Result:

```
true ❌
```

This happens due to precision loss.

---

## Solution → BigInt

```js
9007199254740991n + 1n
```

BigInt avoids precision issues.

---

# 3. Special Number Values

JavaScript has special numeric values.

---

## 1️⃣ NaN (Not a Number)

### Definition

Represents an invalid number result.

```js
0 / 0
```

Result:

```
NaN
```

---

## Common Ways NaN Occurs

```js
Number("hello")
```

```js
Math.sqrt(-1)
```

```js
parseInt("abc")
```

---

## NaN Comparison Trap

```js
NaN === NaN
```

Result:

```
false
```

### Correct Way

```js
Number.isNaN(NaN)
```

Result:

```
true
```

---

## typeof NaN

```js
typeof NaN
```

Result:

```
"number"
```

Interview explanation:

> NaN is still considered a number type.

---

# 2️⃣ Infinity

### Positive Infinity

```js
1 / 0
```

Result:

```
Infinity
```

---

### Negative Infinity

```js
-1 / 0
```

Result:

```
-Infinity
```

---

### typeof Infinity

```js
typeof Infinity
```

Result:

```
"number"
```

---

# 4. Creating Numbers

## 1. Literal Form

```js
let x = 10;
```

Most common.

---

## 2. Number Constructor

```js
let x = Number(10);
```

Avoid:

```js
let x = new Number(10);
```

Because:

```js
typeof new Number(10)
```

Result:

```
object
```

Primitive number:

```js
typeof 10
```

Result:

```
number
```

---

# 5. Number Conversion

## Convert String to Number

### Method 1

```js
Number("10")
```

Result:

```
10
```

---

### Method 2

```js
parseInt("10")
```

---

### Method 3

```js
parseFloat("10.5")
```

---

### Method 4

```js
+"10"
```

Result:

```
10
```

---

## Conversion Failures

```js
Number("abc")
```

Result:

```
NaN
```

---

# 6. Number Methods (Important)

---

## toFixed()

Rounds decimals.

```js
let price = 10.567;

price.toFixed(2);
```

Result:

```
"10.57"
```

Returns string.

---

## toString()

```js
let num = 10;

num.toString();
```

Result:

```
"10"
```

---

## isInteger()

```js
Number.isInteger(10)
```

Result:

```
true
```

---

## isFinite()

```js
Number.isFinite(10)
```

Result:

```
true
```

---

# 7. Math Object (Frequently Asked)

---

## Common Methods

### Math.round()

```js
Math.round(4.6)
```

Result:

```
5
```

---

### Math.floor()

```js
Math.floor(4.9)
```

Result:

```
4
```

---

### Math.ceil()

```js
Math.ceil(4.1)
```

Result:

```
5
```

---

### Math.random()

```js
Math.random()
```

Returns:

```
0 → 1
```

---

### Random Number Example

```js
Math.floor(Math.random() * 10)
```

Range:

```
0–9
```

---

# 8. Number Comparison Issues

## Example

```js
0.1 + 0.2 === 0.3
```

Result:

```
false
```

---

## Safe Comparison

```js
Math.abs(a - b) < Number.EPSILON
```

---

# 9. Arithmetic Behavior

---

## Division by Zero

```js
10 / 0
```

Result:

```
Infinity
```

Unlike many languages.

---

## Invalid Arithmetic

```js
"hello" * 2
```

Result:

```
NaN
```

---

## Automatic Conversion

```js
"5" * 2
```

Result:

```
10
```

Because multiplication converts to number.

---

But:

```js
"5" + 2
```

Result:

```
"52"
```

Because `+` concatenates strings.

---

# 10. Important Interview Edge Cases

---

## Case 1

```js
typeof 10
```

Result:

```
number
```

---

## Case 2

```js
typeof NaN
```

Result:

```
number
```

---

## Case 3

```js
Infinity > 100000000
```

Result:

```
true
```

---

## Case 4

```js
Number(true)
```

Result:

```
1
```

---

## Case 5

```js
Number(false)
```

Result:

```
0
```

---

## Case 6

```js
Number(null)
```

Result:

```
0
```

---

## Case 7

```js
Number(undefined)
```

Result:

```
NaN
```

---

# 11. Memory Behavior

Numbers are stored **by value**.

```js
let a = 10;
let b = a;

b = 20;
```

Result:

```
a = 10
b = 20
```

Independent copies.

---

# Final Interview Summary (Strong Answer)

> JavaScript has a single numeric type called number, which uses 64-bit floating-point representation. It supports integers and decimals but has precision limitations, which is why values like 0.1 + 0.2 do not equal 0.3 exactly. Special numeric values include NaN and Infinity, and numbers are stored as immutable primitive values.

---

Next important primitive types:

* **boolean**
* **undefined vs null (extremely important interview topic)**
* **symbol**
* **bigint**
