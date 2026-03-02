## 23. Versioned APIs in Express.js

**API versioning** is the practice of maintaining multiple versions of an API so that **new changes do not break existing clients**. It is essential for production systems because APIs evolve over time.

Example problem without versioning:

Old API:

```text
GET /users
```

Response:

```json
{
  "name": "Aayush"
}
```

New API change:

```json
{
  "firstName": "Aayush",
  "lastName": "Gid"
}
```

This breaks existing frontend or mobile apps.

Versioning solves this problem.

---

# Why API Versioning is Important

## 1. Backward Compatibility

Old clients continue working.

Example:

```text
/api/v1/users
/api/v2/users
```

v1 works for old apps.

v2 works for new apps.

---

## 2. Safe Feature Updates

You can:

* Add new fields
* Change response format
* Improve performance

Without breaking clients.

---

## 3. Production Stability

Large companies maintain APIs for years.

Example lifecycle:

```text
v1 → supported
v2 → active
v3 → development
```

---

# Versioning Methods

There are **three main methods.**

---

# 1. URL Versioning (Best Practice)

Most common approach.

Example:

```text
/api/v1/users
/api/v2/users
```

---

## Implementation in Express

### Folder Structure

```text
src/
 routes/
   v1/
     userRoutes.js
   v2/
     userRoutes.js
```

---

### v1 Routes

```js
const router = require('express').Router();

router.get('/users', (req,res)=>{
 res.json({
  name:"Aayush"
 });
});

module.exports = router;
```

---

### v2 Routes

```js
const router = require('express').Router();

router.get('/users', (req,res)=>{
 res.json({
  firstName:"Aayush",
  lastName:"Gid"
 });
});

module.exports = router;
```

---

### app.js

```js
app.use('/api/v1', require('./routes/v1'));

app.use('/api/v2', require('./routes/v2'));
```

---

## Final Endpoints

```text
GET /api/v1/users
GET /api/v2/users
```

---

## Advantages

* Clear structure
* Easy to maintain
* Easy debugging
* Industry standard

---

## Disadvantages

* Duplicate code possible

---

# 2. Header Versioning

Version passed in headers.

Example request:

```text
GET /users
API-Version: 1
```

---

## Implementation

Middleware:

```js
app.use((req,res,next)=>{

 req.apiVersion = req.headers['api-version'];

 next();

});
```

Route:

```js
app.get('/users',(req,res)=>{

 if(req.apiVersion === '1'){

   res.json({name:"Aayush"});

 }
 else if(req.apiVersion === '2'){

   res.json({
    firstName:"Aayush",
    lastName:"Gid"
   });

 }

});
```

---

## Advantages

* Clean URLs
* Flexible

---

## Disadvantages

* Harder to debug
* Harder to test
* Less visible

---

# 3. Query Versioning

Version passed as query parameter.

Example:

```text
GET /users?version=1
```

---

## Implementation

```js
app.get('/users',(req,res)=>{

 const version = req.query.version;

 if(version === '1'){
   res.json({name:"Aayush"});
 }
 else{
   res.json({
    firstName:"Aayush",
    lastName:"Gid"
   });
 }

});
```

---

## Disadvantages

Not recommended because:

* Hard to maintain
* Not RESTful
* Confusing

---

# Best Practice Approach

Use **URL versioning**.

Example:

```text
/api/v1/
/api/v2/
```

Most production APIs use this.

---

# Advanced Versioning Structure

Professional structure:

```text
src/
 routes/
   v1/
     index.js
     userRoutes.js
     orderRoutes.js

   v2/
     index.js
     userRoutes.js
```

---

## v1 index.js

```js
const router = require('express').Router();

router.use('/users', require('./userRoutes'));

router.use('/orders', require('./orderRoutes'));

module.exports = router;
```

---

## app.js

```js
app.use('/api/v1', require('./routes/v1'));

app.use('/api/v2', require('./routes/v2'));
```

---

# When to Create New Version

Create new version when:

### 1. Breaking Changes

Example:

```text
Change response structure
```

---

### 2. Remove Fields

Example:

```text
Remove "email"
```

---

### 3. Change Authentication

Example:

```text
Session → JWT
```

---

### 4. Change Request Format

Example:

```text
POST body structure changes
```

---

# When NOT to Version

No version required when:

### Add Optional Fields

Example:

```json
{
 "name":"Aayush",
 "age":22
}
```

Old clients still work.

---

### Fix Bugs

Example:

```text
Performance improvement
```

---

# Version Deprecation Strategy

Typical lifecycle:

```text
v1 → deprecated
v2 → active
v3 → development
```

Example:

```text
v1 supported until 2027
```

---

# Example Real Production API

```text
/api/v1/auth/login
/api/v1/users
/api/v1/orders

/api/v2/auth/login
/api/v2/users
```

---

# Common Interview Questions

## Question 1

Which versioning method is best?

Answer:

```text
URL Versioning
```

Because:

* Easy debugging
* Easy testing
* Clear structure

---

## Question 2

Where should version be placed?

Answer:

```text
/api/v1/
```

Not:

```text
/v1/api/
```

---

## Question 3

Can we remove old versions?

Answer:

Yes, after deprecation period.

---

# Interview-Level Answer

**API versioning in Express is the practice of maintaining multiple API versions to prevent breaking existing clients. The most common method is URL versioning such as `/api/v1/users` and `/api/v2/users`, implemented by mounting different route modules. Versioning ensures backward compatibility and allows safe evolution of APIs without affecting existing users.**

---

Next section:

**Request/Response**

24. How does body parsing work?
25. req.params vs req.query vs req.body
26. File uploads in Express

These are also **very commonly asked Node.js interview topics.**
