# Map in JavaScript (Detailed Interview Explanation)

## Definition

A **Map** is a built-in JavaScript object used to store **key–value pairs**, where **keys can be of any type**.

```js
const map = new Map();
```

Map is a:

* Reference type
* Iterable collection
* Ordered key-value structure
* Stored in heap memory
* Mutable object

Introduced in **ES6 (ES2015)**.

---

# 1. Why Map Exists

Before ES6, developers used objects for key-value storage:

```js
const obj = {
  name: "John"
};
```

Problems with objects:

* Keys must be strings or symbols
* No guaranteed order (historically)
* Prototype properties interfere
* Harder iteration
* Less efficient for frequent updates

Map solves these issues.

---

# 2. Creating Maps

## Empty Map

```js
const map = new Map();
```

---

## Map with Initial Values

```js
const map = new Map([
  ["name", "John"],
  ["age", 25]
]);
```

Format:

```
[key, value]
```

---

# 3. Adding Values

## set()

```js
map.set("name", "John");
map.set("age", 25);
```

---

## Chaining

```js
map.set("a",1)
   .set("b",2);
```

---

# 4. Getting Values

## get()

```js
map.get("name");
```

Result:

```
John
```

---

## Missing Key

```js
map.get("city");
```

Result:

```
undefined
```

---

# 5. Checking Keys

## has()

```js
map.has("name");
```

Result:

```
true
```

---

# 6. Removing Values

## delete()

```js
map.delete("age");
```

---

## clear()

Removes all entries.

```js
map.clear();
```

---

# 7. Map Size

```js
map.size
```

Example:

```
2
```

Unlike objects:

```js
Object.keys(obj).length
```

Map has direct property.

---

# 8. Map Keys Can Be Any Type (Very Important)

---

## Number Keys

```js
map.set(1,"one");
```

---

## Boolean Keys

```js
map.set(true,"yes");
```

---

## Object Keys

```js
const keyObj = {};

map.set(keyObj,"value");
```

Valid.

Objects cannot do this reliably:

```js
const obj = {};

obj[keyObj] = "value";
```

Converted to:

```
"[object Object]"
```

---

# 9. Iterating Maps

---

## for...of

```js
for(const [key,value] of map){
 console.log(key,value);
}
```

---

## keys()

```js
map.keys();
```

Returns iterator.

---

## values()

```js
map.values();
```

---

## entries()

```js
map.entries();
```

Default iteration.

---

## forEach()

```js
map.forEach((value,key)=>{
 console.log(key,value);
});
```

---

# 10. Map vs Object (Very Important Interview Question)

| Feature     | Object                      | Map       |
| ----------- | --------------------------- | --------- |
| Key types   | String/Symbol               | Any type  |
| Order       | Not guaranteed historically | Preserved |
| Iteration   | Harder                      | Easier    |
| Size        | Manual calculation          | map.size  |
| Performance | Slower for dynamic data     | Faster    |

---

# 11. Map Equality Behavior

Keys use reference equality.

---

## Example

```js
const map = new Map();

map.set({}, "value");

map.get({});
```

Result:

```
undefined
```

Because different object references.

---

## Correct Way

```js
const key = {};

map.set(key,"value");

map.get(key);
```

Result:

```
value
```

---

# 12. Map is Iterable

```js
const map = new Map([
 ["a",1],
 ["b",2]
]);
```

Spread:

```js
[...map]
```

Result:

```
[["a",1],["b",2]]
```

---

# 13. Converting Map to Object

```js
Object.fromEntries(map);
```

Example:

```js
const map = new Map([
 ["a",1],
 ["b",2]
]);
```

Result:

```
{a:1,b:2}
```

---

# 14. Converting Object to Map

```js
new Map(Object.entries(obj));
```

Example:

```js
const obj = {a:1,b:2};

const map = new Map(Object.entries(obj));
```

---

# 15. Reference Behavior

Maps are reference types.

```js
const m1 = new Map();
const m2 = m1;

m2.set("x",1);
```

Both affected.

---

# 16. Map Memory Model

```id="dz8zv2"
Stack:
map → 0x789

Heap:
0x789 → Map object
```

Copying:

```id="tw9tl6"
map2 → 0x789
```

Same object.

---

# 17. WeakMap (Interview Bonus)

WeakMap keys must be objects.

```js
const wm = new WeakMap();

const obj = {};

wm.set(obj,"data");
```

Advantages:

* Garbage collectible
* Prevents memory leaks

---

# 18. Important Interview Edge Cases

---

## Case 1

```js
typeof new Map()
```

Result:

```
object
```

---

## Case 2

```js
new Map().size
```

Result:

```
0
```

---

## Case 3

```js
const map = new Map();

map.set(1,"a");
map.set(1,"b");
```

Result:

```
{1:"b"}
```

Keys overwrite.

---

## Case 4

```js
map.get("missing")
```

Result:

```
undefined
```

---

## Case 5

```js
const map = new Map();

map.set(NaN,"value");

map.get(NaN);
```

Result:

```
"value"
```

Special behavior.

---

# 19. Real-World Use Cases

---

## 1. Caching

```js
const cache = new Map();
```

---

## 2. Fast Lookup Tables

---

## 3. Storing Object Keys

---

## 4. Counting Elements

```js
const counts = new Map();
```

---

# 20. Common Interview Questions

### Q1: Difference between Map and Object?

Main difference:

> Map allows any key type and provides better iteration and performance.

---

### Q2: When to use Map?

Answer:

> Use Map when keys are dynamic or not strings.

---

### Q3: Is Map iterable?

Yes.

---

### Q4: Is Map reference type?

Yes.

---

# Final Interview Summary (Strong Answer)

> Map is a reference type that stores key-value pairs where keys can be any type. Unlike objects, Maps preserve insertion order and provide efficient operations for dynamic data. Maps are iterable and use reference equality for object keys.

---

Next reference type:

**Set (final reference type)**

After that:

**Primitive vs Reference Types (most important interview question)**
