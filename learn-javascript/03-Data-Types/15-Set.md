# Set in JavaScript (Detailed Interview Explanation)

## Definition

A **Set** is a built-in JavaScript object that stores a **collection of unique values**.

```js
const set = new Set();
```

Set is a:

* Reference type
* Iterable collection
* Mutable object
* Stored in heap memory
* Introduced in ES6

The main feature of Set:

> **It automatically removes duplicate values.**

Example:

```js
const set = new Set([1,2,2,3]);
```

Result:

```
{1,2,3}
```

---

# 1. Creating Sets

## Empty Set

```js
const set = new Set();
```

---

## Set with Values

```js
const set = new Set([1,2,3]);
```

Input must be iterable.

---

## From String

```js
new Set("hello")
```

Result:

```
{"h","e","l","o"}
```

Duplicates removed.

---

# 2. Adding Values

## add()

```js
set.add(1);
set.add(2);
```

---

## Chaining

```js
set.add(1)
   .add(2)
   .add(3);
```

---

## Duplicate Ignored

```js
set.add(2);
```

Still:

```
{1,2,3}
```

---

# 3. Removing Values

## delete()

```js
set.delete(2);
```

---

## clear()

Removes all values.

```js
set.clear();
```

---

# 4. Checking Values

## has()

```js
set.has(1);
```

Result:

```
true
```

Fast lookup.

---

# 5. Set Size

```js
set.size
```

Example:

```
3
```

---

# 6. Iterating Sets

Sets are iterable.

---

## for...of

```js
for(const value of set){
 console.log(value);
}
```

---

## forEach()

```js
set.forEach(value=>{
 console.log(value);
});
```

---

## values()

```js
set.values();
```

Iterator.

---

## keys()

Same as values.

```js
set.keys();
```

Because only values exist.

---

## entries()

```js
set.entries();
```

Returns:

```
[value,value]
```

Example:

```
[1,1]
[2,2]
```

Maintains Map-like structure.

---

# 7. Converting Set to Array

Very common interview use case.

---

## Using Spread

```js
const arr = [...set];
```

---

## Using Array.from()

```js
Array.from(set);
```

---

# 8. Removing Duplicates from Array (Very Common Interview Question)

```js
const arr = [1,2,2,3,3];

const unique = [...new Set(arr)];
```

Result:

```
[1,2,3]
```

Very popular interview example.

---

# 9. Set vs Array (Important Interview Question)

| Feature          | Set         | Array     |
| ---------------- | ----------- | --------- |
| Duplicate values | Not allowed | Allowed   |
| Index access     | No          | Yes       |
| Order            | Preserved   | Preserved |
| Search speed     | Faster      | Slower    |
| Methods          | Few         | Many      |

---

# 10. Set vs Object

| Feature          | Set         | Object          |
| ---------------- | ----------- | --------------- |
| Stores           | Values only | Key-value pairs |
| Duplicate values | No          | Yes             |
| Iteration        | Easy        | Harder          |

---

# 11. Equality Rules (Important)

Set uses **SameValueZero equality**.

Meaning:

---

## Numbers

```js
new Set([1,1])
```

Result:

```
{1}
```

---

## NaN Special Case

```js
new Set([NaN,NaN])
```

Result:

```
{NaN}
```

Unlike:

```js
NaN === NaN
```

Result:

```
false
```

---

## Objects

Objects compared by reference.

```js
new Set([{},{}])
```

Result:

```
{{},{}}
```

Both stored because references differ.

---

# 12. Reference Behavior

Sets are reference types.

```js
const s1 = new Set([1]);
const s2 = s1;

s2.add(2);
```

Result:

```
s1 = {1,2}
```

Both reference same Set.

---

# 13. typeof Set

```js
typeof new Set()
```

Result:

```
"object"
```

---

# 14. Spread Operator with Set

```js
const set = new Set([1,2,3]);

[...set]
```

Result:

```
[1,2,3]
```

---

# 15. Set Operations (Interview Bonus)

---

## Union

```js
const a = new Set([1,2]);
const b = new Set([2,3]);

const union = new Set([...a,...b]);
```

Result:

```
{1,2,3}
```

---

## Intersection

```js
const intersection =
 new Set([...a].filter(x=>b.has(x)));
```

Result:

```
{2}
```

---

## Difference

```js
const difference =
 new Set([...a].filter(x=>!b.has(x)));
```

Result:

```
{1}
```

---

# 16. WeakSet (Interview Bonus)

WeakSet stores only objects.

```js
const ws = new WeakSet();

const obj = {};

ws.add(obj);
```

Features:

* Objects only
* Garbage collected
* Not iterable

---

# 17. Important Interview Edge Cases

---

## Case 1

```js
typeof new Set()
```

Result:

```
object
```

---

## Case 2

```js
new Set([1,1,1]).size
```

Result:

```
1
```

---

## Case 3

```js
new Set([NaN,NaN]).size
```

Result:

```
1
```

---

## Case 4

```js
new Set([{},{}]).size
```

Result:

```
2
```

Because references differ.

---

## Case 5

```js
const set = new Set();

set.add(1);
set.add(1);
```

Result:

```
{1}
```

---

# 18. Real-World Use Cases

---

## Remove Duplicates

Most common.

---

## Fast Lookup

```js
const visited = new Set();
```

---

## Unique IDs

---

## Filtering Data

---

# 19. Common Interview Questions

### Q1: What is Set?

Answer:

> Set is a collection of unique values.

---

### Q2: Does Set allow duplicates?

No.

---

### Q3: Difference between Set and Array?

Set stores unique values and has faster lookup.

---

### Q4: Is Set reference type?

Yes.

---

# Final Interview Summary (Strong Answer)

> Set is a reference type that stores unique values. It automatically removes duplicates and preserves insertion order. Sets are iterable and useful for fast lookups and removing duplicates from arrays.

---

You have now **fully covered Primitive + Reference Types.**

Next **VERY IMPORTANT interview topic:**

**Primitive vs Reference Types (Deep Comparison)** — this question is asked in almost every JavaScript interview.
