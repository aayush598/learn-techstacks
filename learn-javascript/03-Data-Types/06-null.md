## `null` Primitive Type in JavaScript (Detailed Interview Explanation)

### Definition

`null` is a primitive value that represents an **intentional absence of a value**.

```js
let user = null;
```

Meaning:

> The variable exists but currently has **no meaningful value assigned intentionally**.

This is different from `undefined`, where a value was **never assigned**.

---

# 1. Type of Null (Important Interview Trap)

```js
typeof null
```

Output:

```
"object"
```

This is **incorrect logically**, but it exists due to a **historical bug in JavaScript**.

### Interview Explanation

> `typeof null` returns `"object"` due to a legacy bug in JavaScript, but null is actually a primitive type.

---

# 2. Why Null Exists

`null` is used when we **intentionally want to represent an empty value**.

Example:

```js
let selectedUser = null;
```

Meaning:

* User will be assigned later
* Currently empty

---

## Real-world Example

### API Response

```js
{
  name: "John",
  address: null
}
```

Meaning:

> Address exists but is empty.

---

# 3. Null vs Undefined (Very Important)

This is one of the **most common interview questions**.

| Feature       | null                    | undefined    |
| ------------- | ----------------------- | ------------ |
| Meaning       | Intentional empty value | Not assigned |
| Assigned by   | Developer               | JavaScript   |
| Type          | Primitive               | Primitive    |
| typeof        | "object" ❌              | "undefined"  |
| Default value | No                      | Yes          |

---

## Example

```js
let a;
let b = null;

console.log(a);
console.log(b);
```

Output:

```
undefined
null
```

---

## Interview Explanation

> Undefined means a variable was declared but not assigned, while null represents an intentional absence of value.

---

# 4. Equality Behavior

Very important interview topic.

---

## Loose Equality

```js
null == undefined
```

Output:

```
true
```

Because loose equality treats them as similar.

---

## Strict Equality

```js
null === undefined
```

Output:

```
false
```

Because types differ.

---

## Comparison with Other Values

```js
null == 0
```

Output:

```
false
```

---

```js
null > 0
```

Output:

```
false
```

---

```js
null >= 0
```

Output:

```
true
```

Interview explanation:

> Comparisons convert null to number (0), but equality does not.

---

# 5. Boolean Conversion

```js
Boolean(null)
```

Output:

```
false
```

`null` is a falsy value.

Falsy values:

```
false
0
""
null
undefined
NaN
```

---

# 6. Number Conversion

```js
Number(null)
```

Output:

```
0
```

---

## Comparison

```js
Number(undefined)
```

Output:

```
NaN
```

This difference is often asked.

---

# 7. String Conversion

```js
String(null)
```

Output:

```
"null"
```

---

# 8. Null in Objects

```js
const user = {
 name: "John",
 age: null
};
```

Meaning:

* Property exists
* Value intentionally empty

Check:

```js
"user" in obj
```

Property exists → true.

---

# 9. Null in JSON

Unlike undefined, `null` is valid JSON.

Example:

```js
JSON.stringify({
 a: null
});
```

Output:

```
{"a":null}
```

Compare:

```js
JSON.stringify({
 a: undefined
});
```

Output:

```
{}
```

Undefined removed.

---

# 10. Null in DOM (Common Example)

```js
document.getElementById("missing")
```

Output:

```
null
```

Meaning:

> Element does not exist.

---

# 11. Default Values Behavior

```js
function greet(name = "Guest") {
 console.log(name);
}

greet(null);
```

Output:

```
null
```

Because null is considered a value.

---

But:

```js
greet(undefined);
```

Output:

```
Guest
```

Undefined triggers default.

---

# 12. Nullish Coalescing (Modern JS)

Operator:

```
??
```

Example:

```js
let name = null ?? "Guest";
```

Output:

```
Guest
```

---

Comparison:

```js
let name = "" || "Guest";
```

Output:

```
Guest
```

But:

```js
let name = "" ?? "Guest";
```

Output:

```
""
```

Important difference:

| Operator | Checks            |   |              |
| -------- | ----------------- | - | ------------ |
| `        |                   | ` | falsy values |
| `??`     | null or undefined |   |              |

---

# 13. Memory Behavior

Null is stored by value.

```js
let a = null;
let b = a;

b = 10;
```

Result:

```
a = null
b = 10
```

Independent copies.

---

# 14. Important Interview Edge Cases

---

## Case 1

```js
typeof null
```

Result:

```
"object"
```

---

## Case 2

```js
null == undefined
```

Result:

```
true
```

---

## Case 3

```js
null === undefined
```

Result:

```
false
```

---

## Case 4

```js
Boolean(null)
```

Result:

```
false
```

---

## Case 5

```js
Number(null)
```

Result:

```
0
```

---

## Case 6

```js
String(null)
```

Result:

```
"null"
```

---

## Case 7

```js
null + 1
```

Result:

```
1
```

Because null → 0.

---

# 15. Best Practices

## Use Null for Intentional Empty Values

Good:

```js
let selectedUser = null;
```

Bad:

```js
let selectedUser = undefined;
```

---

## Always Use Strict Equality

Good:

```js
value === null
```

Avoid:

```js
value == null
```

(unless intentional)

---

# Final Interview Summary (Strong Answer)

> Null is a primitive value that represents an intentional absence of value. Unlike undefined, which is assigned automatically by JavaScript, null is assigned manually by developers. Although typeof null returns "object" due to a historical bug, null is actually a primitive type and is commonly used to represent empty or missing values.

---

Next primitive types:

**Symbol (advanced but asked)**
**BigInt (sometimes asked)**

After that we move to:

**Primitive vs Reference Types (very important interview topic)**
