## 21. Route Parameters vs Query Parameters in Express.js

Route parameters and query parameters are two ways to send data from the client to the server through the URL. Both are accessible in Express through the request object but are used for **different purposes and follow different patterns.**

---

# 1. Route Parameters

## Definition

**Route parameters** are variables embedded directly in the **URL path**. They represent **specific resources** and are typically required values.

Syntax:

```text
/path/:parameterName
```

Example route:

```js
app.get('/users/:id', (req, res) => {
  res.send(req.params.id);
});
```

Request:

```text
GET /users/25
```

Result:

```text
25
```

Express stores route parameters inside:

```js
req.params
```

Example:

```js
req.params.id
```

Result:

```text
25
```

---

## Multiple Route Parameters

Example:

```js
app.get('/users/:userId/orders/:orderId', (req, res) => {
  res.json(req.params);
});
```

Request:

```text
GET /users/10/orders/200
```

Result:

```json
{
  "userId": "10",
  "orderId": "200"
}
```

---

## Characteristics of Route Parameters

### 1. Required Values

If parameter missing → route does not match.

Example route:

```text
/users/:id
```

Works:

```text
/users/5
```

Fails:

```text
/users
```

---

### 2. Used for Resource Identification

Example:

```text
GET /users/10
GET /products/50
GET /orders/200
```

Each URL points to a **specific resource**.

---

### 3. Position Matters

Example route:

```text
/users/:id
```

Correct:

```text
/users/10
```

Wrong:

```text
/users?id=10
```

---

## Route Parameter Validation

Example:

```js
app.get('/users/:id', (req,res)=>{

 if(isNaN(req.params.id)){
   return res.status(400).send("Invalid ID");
 }

 res.send("OK");
});
```

---

## Route Parameter Regex

Example:

```js
app.get('/users/:id(\\d+)', (req,res)=>{
 res.send("Valid ID");
});
```

Accepts only:

```text
/users/123
```

Rejects:

```text
/users/abc
```

---

# 2. Query Parameters

## Definition

**Query parameters** are key-value pairs appended to the URL after a `?`. They are typically **optional** and used for filtering or modifying responses.

Syntax:

```text
/path?key=value
```

Example route:

```js
app.get('/users', (req,res)=>{
 res.json(req.query);
});
```

Request:

```text
GET /users?page=2&limit=10
```

Result:

```json
{
 "page":"2",
 "limit":"10"
}
```

Query parameters are stored in:

```js
req.query
```

Example:

```js
req.query.page
req.query.limit
```

---

## Multiple Query Parameters

Example:

```text
/users?page=2&limit=10&sort=asc
```

Parsed as:

```json
{
 "page":"2",
 "limit":"10",
 "sort":"asc"
}
```

---

## Characteristics of Query Parameters

### 1. Optional

Example route:

```text
/users
```

Works:

```text
/users
/users?page=1
/users?page=1&limit=10
```

---

### 2. Used for Filtering

Example:

```text
GET /products?category=electronics
```

---

### 3. Used for Pagination

Example:

```text
GET /users?page=2&limit=20
```

---

### 4. Used for Sorting

Example:

```text
GET /products?sort=price
```

---

### 5. Used for Searching

Example:

```text
GET /users?name=aayush
```

---

# Comparison Example

## Route Parameter Example

```js
app.get('/users/:id',(req,res)=>{
 res.send("User ID: " + req.params.id);
});
```

Request:

```text
GET /users/10
```

Result:

```text
User ID: 10
```

---

## Query Parameter Example

```js
app.get('/users',(req,res)=>{
 res.send("Page: " + req.query.page);
});
```

Request:

```text
GET /users?page=2
```

Result:

```text
Page: 2
```

---

# Major Differences

| Feature  | Route Parameters  | Query Parameters      |
| -------- | ----------------- | --------------------- |
| Location | URL path          | After `?`             |
| Example  | `/users/10`       | `/users?id=10`        |
| Storage  | `req.params`      | `req.query`           |
| Required | Usually required  | Usually optional      |
| Purpose  | Identify resource | Filter/modify results |

---

# REST API Best Practices

## Use Route Parameters For

### Resource Identification

Correct:

```text
GET /users/10
GET /orders/100
GET /products/50
```

Incorrect:

```text
GET /users?id=10
```

Because resource ID should be part of path.

---

## Use Query Parameters For

### Filtering

```text
GET /users?age=25
```

---

### Pagination

```text
GET /users?page=2&limit=20
```

---

### Sorting

```text
GET /users?sort=name
```

---

### Searching

```text
GET /users?search=aayush
```

---

# Combining Both

Very common in real APIs.

Example:

```js
app.get('/users/:id/orders',(req,res)=>{

 const userId = req.params.id;

 const page = req.query.page;

 res.send("User " + userId + " Page " + page);

});
```

Request:

```text
GET /users/10/orders?page=2
```

Result:

```text
User 10 Page 2
```

---

# Edge Cases (Important for Interviews)

## Query Parameters Are Strings

Example:

```text
/users?page=2
```

Value:

```js
typeof req.query.page
```

Result:

```text
string
```

Convert:

```js
const page = Number(req.query.page);
```

---

## Route Parameters Are Also Strings

Example:

```text
/users/10
```

Value:

```js
typeof req.params.id
```

Result:

```text
string
```

Convert:

```js
const id = Number(req.params.id);
```

---

# Performance Difference

Very small difference.

Route params slightly faster because:

```text
Direct path match
```

But practically negligible.

---

# Interview Trick Questions

## Question 1

Which is better for IDs?

Answer:

```text
Route parameters
```

Example:

```text
/users/10
```

---

## Question 2

Which is better for pagination?

Answer:

```text
Query parameters
```

Example:

```text
/users?page=2
```

---

## Question 3

Can we use both?

Answer:

Yes.

Example:

```text
/users/10/orders?page=2
```

---

# Interview-Level Answer

**Route parameters are variables defined in the URL path and accessed using `req.params`, typically used to identify a specific resource like `/users/10`. Query parameters are key-value pairs appended to the URL after `?` and accessed using `req.query`, typically used for filtering, pagination, sorting, or searching such as `/users?page=2&limit=10`. Route parameters are usually required, while query parameters are usually optional.**
