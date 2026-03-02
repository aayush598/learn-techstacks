# Array in JavaScript (Detailed Interview Explanation)

## Definition

An **array** is a special type of object used to store an **ordered collection of values**.

```js
const arr = [10, 20, 30];
```

Arrays are:

* Reference types
* Mutable
* Zero-indexed
* Dynamically sized
* Stored in heap memory

---

# 1. Array Characteristics

### Ordered Collection

Elements maintain insertion order.

```js
const arr = [10, 20, 30];

console.log(arr[0]); // 10
```

---

### Zero-Based Indexing

First element:

```js
arr[0]
```

Last element:

```js
arr[arr.length - 1]
```

---

### Dynamic Size

Arrays grow automatically.

```js
const arr = [1,2];

arr.push(3);
```

Result:

```
[1,2,3]
```

---

### Mixed Types Allowed

```js
const arr = [1, "hello", true, {a:1}];
```

Allowed because JavaScript is dynamically typed.

---

# 2. Array in Memory (Important)

Arrays are reference types.

```js
const a = [1,2];
const b = a;

b.push(3);
```

Result:

```
a = [1,2,3]
b = [1,2,3]
```

Memory:

```
a → 0x123
b → 0x123
```

Same reference.

---

# 3. Creating Arrays

## 1. Array Literal (Best Method)

```js
const arr = [1,2,3];
```

Most common.

---

## 2. Array Constructor

```js
const arr = new Array(1,2,3);
```

Avoid unless needed.

---

### Constructor Trap

```js
new Array(5)
```

Creates empty array with length 5:

```
[empty × 5]
```

Not:

```
[5]
```

Correct way:

```js
[5]
```

---

# 4. Array Length Property

```js
const arr = [1,2,3];

arr.length
```

Result:

```
3
```

---

## Changing Length

```js
arr.length = 2;
```

Result:

```
[1,2]
```

Array truncated.

---

# 5. Accessing Elements

```js
const arr = [10,20,30];

arr[1]
```

Result:

```
20
```

---

## Access Non-existing Index

```js
arr[10]
```

Result:

```
undefined
```

---

# 6. Important Array Methods (Interview Critical)

---

## 1. push()

Adds element to end.

```js
arr.push(4);
```

Mutates array.

---

## 2. pop()

Removes last element.

```js
arr.pop();
```

---

## 3. shift()

Removes first element.

```js
arr.shift();
```

Slow operation.

---

## 4. unshift()

Adds element at beginning.

```js
arr.unshift(0);
```

---

# 7. Iteration Methods (Very Important)

---

## for Loop

```js
for(let i=0;i<arr.length;i++){
 console.log(arr[i]);
}
```

---

## for...of

```js
for(const value of arr){
 console.log(value);
}
```

---

## forEach()

```js
arr.forEach(x => console.log(x));
```

Returns undefined.

---

# 8. Transformation Methods (Very Important)

---

## map()

Creates new array.

```js
const arr = [1,2,3];

const result = arr.map(x => x*2);
```

Result:

```
[2,4,6]
```

Does NOT modify original.

---

## filter()

Filters values.

```js
const result = arr.filter(x => x>1);
```

Result:

```
[2,3]
```

---

## reduce()

Reduces to single value.

```js
arr.reduce((sum,x)=>sum+x,0);
```

Result:

```
6
```

---

# 9. Search Methods

---

## find()

Returns first match.

```js
arr.find(x => x>1);
```

---

## findIndex()

Returns index.

```js
arr.findIndex(x => x>1);
```

---

## includes()

```js
arr.includes(2);
```

Result:

```
true
```

---

## indexOf()

```js
arr.indexOf(2);
```

Returns index.

---

# 10. Mutating vs Non-Mutating Methods

### Mutating Methods

Modify original array:

* push
* pop
* shift
* unshift
* splice
* sort
* reverse

---

### Non-Mutating Methods

Return new array:

* map
* filter
* slice
* concat

---

# 11. slice vs splice (Interview Favorite)

---

## slice()

Does NOT modify original.

```js
const arr = [1,2,3,4];

arr.slice(1,3);
```

Result:

```
[2,3]
```

---

## splice()

Modifies original.

```js
arr.splice(1,2);
```

Result:

```
[1,4]
```

---

# 12. Spread Operator with Arrays

```js
const arr1 = [1,2];
const arr2 = [...arr1];
```

Creates shallow copy.

---

## Merge Arrays

```js
const merged = [...arr1,...arr2];
```

---

# 13. Array Destructuring

```js
const [a,b] = [1,2];
```

Result:

```
a=1
b=2
```

---

## Skip Elements

```js
const [a,,b] = [1,2,3];
```

Result:

```
a=1
b=3
```

---

# 14. Array Equality (Important)

```js
[1,2] === [1,2]
```

Result:

```
false
```

Because different references.

---

## Same Reference

```js
const a = [1];
const b = a;

a === b
```

Result:

```
true
```

---

# 15. Array Checking (Interview Trap)

```js
typeof []
```

Result:

```
"object"
```

Correct check:

```js
Array.isArray([])
```

Result:

```
true
```

---

# 16. Sparse Arrays

```js
const arr = [];

arr[5] = 10;
```

Result:

```
[empty × 5, 10]
```

Length:

```
6
```

---

# 17. Flattening Arrays

```js
[1,[2,[3]]].flat(2)
```

Result:

```
[1,2,3]
```

---

# 18. Sorting Arrays (Interview Trap)

Default sorting is string-based.

```js
[1,10,2].sort()
```

Result:

```
[1,10,2]
```

Correct:

```js
[1,10,2].sort((a,b)=>a-b)
```

Result:

```
[1,2,10]
```

---

# 19. Important Interview Edge Cases

---

## Case 1

```js
[] + []
```

Result:

```
""
```

String conversion.

---

## Case 2

```js
[] == false
```

Result:

```
true
```

Type coercion.

---

## Case 3

```js
[1] + [2]
```

Result:

```
"12"
```

Converted to string.

---

## Case 4

```js
Array(3).map(x=>1)
```

Result:

```
[empty × 3]
```

Because empty slots.

Correct:

```js
Array(3).fill(1)
```

---

# 20. Performance Notes

Fast operations:

* push
* pop

Slow operations:

* shift
* unshift

Because elements reindexed.

---

# Final Interview Summary (Strong Answer)

> Arrays in JavaScript are ordered, mutable reference types used to store collections of values. They are stored in heap memory and copied by reference. Arrays support many built-in methods such as map, filter, and reduce, and care must be taken to distinguish between mutating and non-mutating methods.

---

Next **critical interview topic**:

**Function (Reference Type)** — one of the **most important JavaScript topics for React interviews.**
