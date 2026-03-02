# Object in JavaScript (Detailed Interview Explanation)

## Definition

An **object** in JavaScript is a collection of **key–value pairs**, where:

* Keys are strings or symbols
* Values can be any type (primitive or reference)

```js
const user = {
  name: "John",
  age: 25
};
```

Objects are:

* Reference types
* Mutable
* Stored in heap memory
* Compared by reference

---

# 1. How Objects Work in Memory

When you create an object:

```js
const user = { name: "John" };
```

Memory model:

```
Stack:
user → 0x123

Heap:
0x123 → { name: "John" }
```

When copied:

```js
const another = user;
```

Both point to same memory address:

```
another → 0x123
```

Modifying one modifies the same object:

```js
another.name = "Alice";
```

Now:

```
user.name → "Alice"
```

---

# 2. Creating Objects

## 1. Object Literal (Most Common)

```js
const obj = {
  key: "value"
};
```

Preferred method.

---

## 2. Using new Object()

```js
const obj = new Object();
obj.name = "John";
```

Rarely used.

---

## 3. Constructor Function

```js
function User(name) {
  this.name = name;
}

const u = new User("John");
```

Old pattern before classes.

---

## 4. Using Object.create()

```js
const proto = {
  greet() {
    console.log("Hi");
  }
};

const obj = Object.create(proto);
```

Used for prototype-based inheritance.

---

# 3. Accessing Properties

## Dot Notation

```js
user.name
```

Most common.

---

## Bracket Notation

```js
user["name"]
```

Required when:

* Key has spaces
* Key is dynamic

Example:

```js
const key = "age";
user[key];
```

---

# 4. Adding, Updating, Deleting Properties

## Add

```js
user.city = "Delhi";
```

---

## Update

```js
user.age = 30;
```

---

## Delete

```js
delete user.city;
```

---

# 5. Object Methods

Objects can store functions.

```js
const user = {
  name: "John",
  greet() {
    console.log("Hello");
  }
};
```

Functions inside objects are called **methods**.

---

# 6. Object Property Keys

Keys are:

* Strings (default)
* Symbols

Even numbers become strings:

```js
const obj = {
  1: "one"
};

console.log(Object.keys(obj));
```

Output:

```
["1"]
```

---

# 7. Checking Properties

## Using in Operator

```js
"name" in user
```

Returns true if property exists.

---

## Using hasOwnProperty

```js
user.hasOwnProperty("name");
```

Checks only own properties.

---

# 8. Iterating Over Objects

## for...in

```js
for (let key in user) {
  console.log(key);
}
```

Includes inherited properties.

---

## Object.keys()

```js
Object.keys(user);
```

Returns array of keys.

---

## Object.values()

```js
Object.values(user);
```

---

## Object.entries()

```js
Object.entries(user);
```

Returns:

```
[["name","John"],["age",25]]
```

---

# 9. Object Destructuring

```js
const { name, age } = user;
```

With renaming:

```js
const { name: userName } = user;
```

With default value:

```js
const { country = "India" } = user;
```

---

# 10. Shallow Copy vs Deep Copy (Very Important)

## Shallow Copy

```js
const copy = { ...user };
```

or

```js
Object.assign({}, user);
```

Problem with nested objects:

```js
const obj = {
  address: { city: "Delhi" }
};

const copy = { ...obj };

copy.address.city = "Mumbai";
```

Both change because nested object still shared.

---

## Deep Copy

```js
const deepCopy = JSON.parse(JSON.stringify(obj));
```

Limitations:

* Removes functions
* Removes undefined
* Removes Symbol
* Converts Date to string

Modern approach:

```js
structuredClone(obj);
```

---

# 11. Object Equality (Interview Favorite)

```js
{} === {}
```

Result:

```
false
```

Because different memory references.

---

Correct comparison requires:

* Manual deep comparison
* Or utility library

---

# 12. Freezing and Sealing Objects

## Object.freeze()

Prevents:

* Adding
* Deleting
* Modifying

```js
Object.freeze(user);
```

---

## Object.seal()

Prevents:

* Adding
* Deleting

But allows modification.

```js
Object.seal(user);
```

---

# 13. Object Prototype (Very Important)

Every object has a hidden property:

```
[[Prototype]]
```

Example:

```js
const obj = {};
```

Behind the scenes:

```
obj → Object.prototype
```

This enables inheritance.

---

## Access Prototype

```js
Object.getPrototypeOf(obj);
```

---

# 14. this in Objects

```js
const user = {
  name: "John",
  greet() {
    console.log(this.name);
  }
};
```

`this` refers to the object before the dot.

---

Arrow function trap:

```js
const user = {
  name: "John",
  greet: () => {
    console.log(this.name);
  }
};
```

Here `this` does NOT refer to object.

---

# 15. Object vs Map (Interview Question)

| Object                              | Map                     |
| ----------------------------------- | ----------------------- |
| Keys mostly strings                 | Any type keys           |
| Less optimized for frequent changes | Better for dynamic data |
| Prototype inheritance               | No prototype issues     |

---

# 16. Important Interview Edge Cases

---

## Case 1

```js
typeof {}
```

Result:

```
"object"
```

---

## Case 2

```js
typeof []
```

Result:

```
"object"
```

Check array properly:

```js
Array.isArray([])
```

---

## Case 3

```js
Object.keys({a:1})
```

Result:

```
["a"]
```

---

## Case 4

```js
const obj = {};
obj.x = 10;
delete obj.x;
```

Works.

---

## Case 5

```js
const obj = {};
obj.toString();
```

Works because inherited from prototype.

---

# 17. Memory Model (Interview-Level Explanation)

Objects live in:

```
Heap memory
```

Variables store:

```
Reference (memory address)
```

Copying variable copies reference, not object.

---

# 18. Common Interview Questions

### Q1: Are objects mutable?

Yes.

---

### Q2: Are objects stored by value?

No, stored by reference.

---

### Q3: Why {} === {} is false?

Because they reference different memory locations.

---

### Q4: How to clone an object?

Shallow: spread operator
Deep: structuredClone or manual recursion

---

# Final Interview Summary (Strong Answer)

> Objects in JavaScript are mutable reference types that store key-value pairs. They are stored in heap memory and accessed through references. When assigned or copied, only the reference is copied, not the actual object, which is why modifying one reference affects the other.

---

Next important reference types:

* Array (very important)
* Function (critical for interviews)
* Map
* Set

Tell me which one to go deep into next.
