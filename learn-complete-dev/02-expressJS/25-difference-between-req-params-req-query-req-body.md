## 25. Difference Between `req.params`, `req.query`, and `req.body` (Express.js)

In Express.js, data sent from the client to the server can come from **three main sources**:

* `req.params` → Route parameters (URL path variables)
* `req.query` → Query string parameters
* `req.body` → Request body data

These are stored inside the **request object (`req`)** and serve different purposes.

---

# 1. req.params

## Definition

`req.params` contains **route parameters** defined in the URL path. These parameters usually identify a **specific resource**.

Route example:

```js
app.get('/users/:id', (req,res)=>{
 console.log(req.params);
});
```

Request:

```text
GET /users/10
```

Result:

```js
req.params = {
 id: "10"
}
```

Access:

```js
req.params.id
```

---

## Characteristics

### Used For Resource Identification

Examples:

```text
GET /users/10
GET /orders/25
GET /products/5
```

Each URL points to a **specific item**.

---

### Required Values

Route:

```text
/users/:id
```

Valid:

```text
/users/10
```

Invalid:

```text
/users
```

Route will not match.

---

### Always Strings

Example:

```js
typeof req.params.id
```

Result:

```text
string
```

Convert if needed:

```js
const id = Number(req.params.id);
```

---

# 2. req.query

## Definition

`req.query` contains **query string parameters** appended to the URL after `?`. They are typically **optional** and used for filtering or modifying results.

Route example:

```js
app.get('/users', (req,res)=>{
 console.log(req.query);
});
```

Request:

```text
GET /users?page=2&limit=10
```

Result:

```js
req.query = {
 page: "2",
 limit: "10"
}
```

Access:

```js
req.query.page
req.query.limit
```

---

## Characteristics

### Optional Values

Works:

```text
/users
/users?page=1
/users?page=1&limit=10
```

---

### Used for Filtering

Example:

```text
GET /products?category=electronics
```

---

### Used for Pagination

Example:

```text
GET /users?page=2&limit=20
```

---

### Used for Sorting

Example:

```text
GET /users?sort=name
```

---

### Always Strings

Example:

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

# 3. req.body

## Definition

`req.body` contains data sent in the **HTTP request body**, typically used with:

* POST
* PUT
* PATCH

Route example:

```js
app.post('/users',(req,res)=>{
 console.log(req.body);
});
```

Request:

```http
POST /users
Content-Type: application/json

{
 "name":"Aayush",
 "age":22
}
```

Result:

```js
req.body = {
 name:"Aayush",
 age:22
}
```

---

## Characteristics

### Used for Creating or Updating Data

Examples:

```text
POST /users
PUT /users/10
PATCH /users/10
```

---

### Requires Body Parser Middleware

Example:

```js
app.use(express.json());
```

Without parser:

```text
req.body = undefined
```

---

### Supports Complex Objects

Example:

```json
{
 "user":{
  "name":"Aayush",
  "age":22
 }
}
```

Access:

```js
req.body.user.name
```

---

# Comparison Example

## Example Route

```js
app.put('/users/:id', (req,res)=>{

 console.log("Params:", req.params);
 console.log("Query:", req.query);
 console.log("Body:", req.body);

 res.send("OK");

});
```

Request:

```http
PUT /users/10?admin=true
Content-Type: application/json

{
 "name":"Aayush"
}
```

Result:

```text
Params: { id: "10" }

Query: { admin: "true" }

Body: { name: "Aayush" }
```

---

# Major Differences

| Feature   | req.params       | req.query        | req.body         |
| --------- | ---------------- | ---------------- | ---------------- |
| Source    | URL Path         | URL Query String | Request Body     |
| Example   | `/users/10`      | `/users?page=2`  | JSON Data        |
| Access    | req.params.id    | req.query.page   | req.body.name    |
| Required  | Usually required | Usually optional | Usually required |
| Data Type | String           | String           | Any type         |
| Methods   | Mostly GET       | Mostly GET       | POST/PUT/PATCH   |

---

# Real REST API Example

## Get Specific User

```text
GET /users/10
```

Uses:

```js
req.params.id
```

---

## Get Users With Pagination

```text
GET /users?page=2&limit=10
```

Uses:

```js
req.query.page
req.query.limit
```

---

## Create User

```text
POST /users
```

Uses:

```js
req.body.name
req.body.email
```

---

# Combined Example (Very Common)

Example route:

```js
app.post('/users/:id/orders',(req,res)=>{

 const userId = req.params.id;

 const page = req.query.page;

 const orderData = req.body;

 res.json({
  userId,
  page,
  orderData
 });

});
```

Request:

```http
POST /users/10/orders?page=2
Content-Type: application/json

{
 "productId":5,
 "quantity":2
}
```

Result:

```json
{
 "userId":"10",
 "page":"2",
 "orderData":{
  "productId":5,
  "quantity":2
 }
}
```

---

# Typical Usage Pattern

### req.params → Resource

```text
/users/10
```

---

### req.query → Options

```text
/users?page=2
```

---

### req.body → Data

```text
{
 "name":"Aayush"
}
```

---

# Common Interview Mistakes

## Mistake 1

Using query for IDs.

Wrong:

```text
/users?id=10
```

Correct:

```text
/users/10
```

---

## Mistake 2

Expecting numbers.

Example:

```js
req.query.page + 1
```

Result:

```text
"21"
```

Because string.

Correct:

```js
Number(req.query.page) + 1
```

---

# Interview-Level Answer

**`req.params`, `req.query`, and `req.body` are different sources of client data in Express. `req.params` contains route parameters from the URL path such as `/users/10`, `req.query` contains query string parameters such as `/users?page=2`, and `req.body` contains request data sent in the HTTP body such as JSON in POST or PUT requests. Route parameters identify resources, query parameters modify or filter results, and request body contains data for creating or updating resources.**
