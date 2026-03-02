# Date in JavaScript (Detailed Interview Explanation)

## Definition

The **`Date`** object in JavaScript represents **date and time values**. It is a **reference type** used to work with:

* Current time
* Specific dates
* Timestamps
* Time calculations

```js
const now = new Date();
```

Date objects are:

* Reference types
* Mutable
* Stored in heap memory
* Based on timestamps

---

# 1. Internal Representation

JavaScript Date stores time as:

> **Milliseconds since January 1, 1970 (UTC)**

This is called the **Unix Timestamp**.

Example:

```js
new Date(0)
```

Result:

```
Jan 1 1970 UTC
```

---

## Timestamp Example

```js
Date.now()
```

Example output:

```
1700000000000
```

Milliseconds since 1970.

---

# 2. Creating Date Objects

## 1️⃣ Current Date and Time

```js
const now = new Date();
```

Example:

```
Mon Mar 02 2026 10:30:00
```

Most common usage.

---

## 2️⃣ Using Timestamp

```js
const date = new Date(0);
```

Result:

```
Jan 1 1970
```

---

## 3️⃣ Using Date String

```js
const date = new Date("2024-01-01");
```

---

## 4️⃣ Using Components

```js
const date = new Date(2024, 0, 1);
```

Format:

```
new Date(year, monthIndex, day)
```

Important:

Months are **zero-based**:

| Month | Index |
| ----- | ----- |
| Jan   | 0     |
| Feb   | 1     |
| Dec   | 11    |

Example:

```js
new Date(2024, 11, 25)
```

December 25.

---

# 3. Getting Date Values

---

## getFullYear()

```js
const date = new Date();

date.getFullYear();
```

Example:

```
2026
```

---

## getMonth()

```js
date.getMonth();
```

Range:

```
0–11
```

---

## getDate()

```js
date.getDate();
```

Day of month:

```
1–31
```

---

## getDay()

```js
date.getDay();
```

Day of week:

| Day    | Value |
| ------ | ----- |
| Sunday | 0     |
| Monday | 1     |

---

## getHours()

```js
date.getHours();
```

Range:

```
0–23
```

---

## getMinutes()

```js
date.getMinutes();
```

---

## getSeconds()

```js
date.getSeconds();
```

---

# 4. Setting Date Values

Date objects are mutable.

---

## setFullYear()

```js
const date = new Date();

date.setFullYear(2030);
```

---

## setMonth()

```js
date.setMonth(5);
```

June.

---

## setDate()

```js
date.setDate(10);
```

---

## setHours()

```js
date.setHours(12);
```

---

# 5. Date Formatting

---

## toString()

```js
new Date().toString();
```

Example:

```
Mon Mar 02 2026 10:30:00 GMT+0530
```

---

## toDateString()

```js
new Date().toDateString();
```

Example:

```
Mon Mar 02 2026
```

---

## toISOString()

```js
new Date().toISOString();
```

Example:

```
2026-03-02T05:00:00.000Z
```

Very common in APIs.

---

## toLocaleString()

```js
new Date().toLocaleString();
```

Example:

```
02/03/2026, 10:30:00
```

---

# 6. Date.now() (Very Important)

Returns timestamp.

```js
Date.now()
```

Used for:

* Performance measurement
* Unique IDs
* Time differences

---

## Example

```js
const start = Date.now();

/* code */

const end = Date.now();

console.log(end - start);
```

Time taken in milliseconds.

---

# 7. Date Comparison

Compare timestamps.

---

## Example

```js
const d1 = new Date("2024-01-01");
const d2 = new Date("2025-01-01");

d1 < d2
```

Result:

```
true
```

Because timestamps compared.

---

## Equality Trap

```js
new Date("2024") === new Date("2024")
```

Result:

```
false
```

Different references.

---

Correct:

```js
d1.getTime() === d2.getTime()
```

---

# 8. getTime()

Returns timestamp.

```js
const date = new Date();

date.getTime();
```

Same as:

```js
Date.now();
```

---

# 9. Date Arithmetic

---

## Difference Between Dates

```js
const d1 = new Date("2024-01-01");
const d2 = new Date("2024-01-03");

d2 - d1
```

Result:

```
172800000
```

Milliseconds.

---

## Convert to Days

```js
(d2 - d1) / (1000*60*60*24)
```

Result:

```
2
```

---

# 10. Date Mutability

Date objects are mutable.

```js
const d = new Date();

d.setFullYear(2030);
```

Original object changed.

---

# 11. Reference Behavior

```js
const d1 = new Date();
const d2 = d1;

d2.setFullYear(2030);
```

Both change.

---

# 12. Timezones (Interview-Level Topic)

JavaScript Date uses:

* Local timezone
* UTC internally

---

## Local Time

```js
new Date().toString()
```

---

## UTC Time

```js
new Date().toUTCString()
```

---

# 13. typeof Date

```js
typeof new Date()
```

Result:

```
"object"
```

---

# 14. Date Parsing Issues

Bad:

```js
new Date("01/02/2024")
```

Ambiguous.

Better:

```js
new Date("2024-02-01")
```

ISO format.

---

# 15. Important Interview Edge Cases

---

## Case 1

```js
Date.now()
```

Returns timestamp.

---

## Case 2

```js
new Date() instanceof Date
```

Result:

```
true
```

---

## Case 3

```js
typeof new Date()
```

Result:

```
object
```

---

## Case 4

```js
new Date(0)
```

Result:

```
1970
```

---

## Case 5

```js
new Date(2024,0,1)
```

Month 0 = January.

---

# 16. Memory Model

Date stored in heap.

Variable stores reference.

```
Stack:
d → 0x567

Heap:
0x567 → Date object
```

---

# 17. Common Interview Questions

### Q1: Is Date primitive?

No. Date is a reference type.

---

### Q2: How is Date stored internally?

Milliseconds since Jan 1 1970 UTC.

---

### Q3: Why new Date() === new Date() is false?

Different references.

---

### Q4: How to compare dates?

Using timestamps.

---

# Final Interview Summary (Strong Answer)

> Date is a reference type used to represent date and time values in JavaScript. Internally, it stores time as milliseconds since January 1, 1970 UTC. Date objects are mutable and compared by reference, so timestamps must be used for equality checks.

---

Next reference types:

**Map** (very common interview question)
**Set**

Then we finish **Reference Types**, and move to:

**Primitive vs Reference Types (most asked interview topic).**
