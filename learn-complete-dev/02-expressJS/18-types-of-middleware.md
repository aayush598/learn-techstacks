## 18. Types of Middleware in Express.js

Express middleware can be classified into **five main types**. Understanding these types is a **very common technical interview topic** because Express architecture is middleware-driven.

The main types are:

1. Application-level middleware
2. Router-level middleware
3. Built-in middleware
4. Third-party middleware
5. Error-handling middleware

---

# 1. Application-Level Middleware

## Definition

**Application middleware** is middleware attached to the Express **application object (`app`)**. It executes for **every request** or for a specified path.

Basic syntax:

```js
app.use(middlewareFunction)
```

Example:

```js
const express = require('express');
const app = express();

app.use((req,res,next)=>{
 console.log("Request received");
 next();
});
```

This middleware runs for:

```
GET /users
POST /login
DELETE /products
```

---

## Path-Based Application Middleware

Middleware can run only for specific paths.

Example:

```js
app.use('/api',(req,res,next)=>{
 console.log("API Request");
 next();
});
```

Runs only for:

```
/api/users
/api/products
```

Not for:

```
/login
/home
```

---

## Example: Logging Middleware

```js
function logger(req,res,next){

 console.log(
   req.method,
   req.url
 );

 next();
}

app.use(logger);
```

---

## Use Cases

Application middleware is used for:

* Logging
* Security headers
* CORS
* Body parsing
* Rate limiting

Example production setup:

```js
app.use(cors());
app.use(express.json());
app.use(rateLimit());
app.use(logger);
```

---

## Execution Scope

```
Entire application
```

---

# 2. Router-Level Middleware

## Definition

**Router middleware** is middleware applied to an **Express Router instance** instead of the main app.

Router is created using:

```js
const router = express.Router();
```

Middleware applied:

```js
router.use(middleware)
```

Mounted on app:

```js
app.use('/users', router);
```

---

## Example

```js
const router = express.Router();

router.use((req,res,next)=>{
 console.log("User Route Middleware");
 next();
});

router.get('/',(req,res)=>{
 res.send("Users");
});

app.use('/users', router);
```

Runs for:

```
/users
/users/10
/users/profile
```

Does NOT run for:

```
/products
/login
```

---

## Example: Auth Middleware

```js
router.use(authMiddleware);
```

Protects:

```
/users/*
```

---

## Route-Specific Middleware

Middleware applied to a single route.

Example:

```js
router.get('/profile',
 authMiddleware,
(req,res)=>{
 res.send("Profile");
});
```

Runs only for:

```
/profile
```

---

## Use Cases

Router middleware is used for:

* Authentication
* Role-based access
* API modules
* Microservices structure

Example:

```
/api/users
/api/orders
/api/payments
```

Each router has separate middleware.

---

## Execution Scope

```
Specific group of routes
```

---

# 3. Built-in Middleware

## Definition

Built-in middleware is middleware **provided by Express itself**.

No installation required.

---

## 3.1 express.json()

Parses JSON request body.

Example:

```js
app.use(express.json());
```

Incoming request:

```
POST /users
Content-Type: application/json

{
 "name":"Aayush"
}
```

Result:

```js
req.body.name
```

Without it:

```
req.body = undefined
```

---

## 3.2 express.urlencoded()

Parses HTML form data.

Example:

```js
app.use(express.urlencoded({
 extended:true
}));
```

Form data:

```
name=Aayush&age=22
```

Result:

```
req.body.name
```

---

## extended:true vs false

### extended:false

Uses simple querystring parser.

Supports:

```
name=Aayush
```

---

### extended:true

Uses qs library.

Supports nested objects:

```
user[name]=Aayush
```

Parsed:

```js
{
 user:{
  name:"Aayush"
 }
}
```

---

## 3.3 express.static()

Serves static files.

Example:

```js
app.use(express.static('public'));
```

Folder:

```
public/
  index.html
  style.css
  logo.png
```

Access:

```
http://localhost:3000/index.html
```

---

## Use Cases

Built-in middleware is used for:

* Parsing request bodies
* Serving frontend
* Static assets

---

# 4. Third-Party Middleware

## Definition

Middleware installed from npm packages.

Example:

```
npm install cors helmet multer
```

---

## Examples

### 4.1 CORS Middleware

Allows cross-origin requests.

Example:

```js
const cors = require('cors');

app.use(cors());
```

Without CORS:

```
Frontend blocked by browser
```

---

### 4.2 Helmet Middleware

Security headers.

Example:

```js
const helmet=require('helmet');

app.use(helmet());
```

Adds:

```
X-Frame-Options
X-Content-Type-Options
```

---

### 4.3 Rate Limiter

Example:

```js
const rateLimit=require('express-rate-limit');

app.use(rateLimit({
 windowMs:15*60*1000,
 max:100
}));
```

Limits:

```
100 requests per 15 minutes
```

---

### 4.4 Multer

Handles file uploads.

Example:

```js
const multer=require('multer');

const upload=multer({
 dest:'uploads/'
});

app.post('/upload',
 upload.single('file'),
(req,res)=>{

 res.send("Uploaded");

});
```

---

## Use Cases

Third-party middleware is used for:

* Authentication
* Security
* Uploads
* Validation
* Logging

---

# 5. Error-Handling Middleware

## Definition

Special middleware used to handle errors.

Signature:

```js
(err, req, res, next)
```

Must have **4 parameters**.

---

## Example

```js
app.use((err,req,res,next)=>{

 res.status(500).json({
   error:err.message
 });

});
```

---

## How Errors Reach Middleware

### Using next(err)

```js
app.get('/',(req,res,next)=>{

 next(new Error("Database error"));

});
```

---

### Throw Error

```js
app.get('/',(req,res)=>{
 throw new Error("Crash");
});
```

---

## Execution Order

Error middleware must be last.

Correct:

```js
app.use(routes);

app.use(errorHandler);
```

Wrong:

```js
app.use(errorHandler);

app.use(routes);
```

---

## Use Cases

Error middleware is used for:

* Centralized error handling
* Logging errors
* Sending consistent responses

Example response:

```json
{
 "error":"Invalid user"
}
```

---

# Summary Table

| Middleware Type | Applied On | Scope          |
| --------------- | ---------- | -------------- |
| Application     | app        | Entire app     |
| Router          | router     | Route group    |
| Built-in        | Express    | Core features  |
| Third-party     | npm        | Extra features |
| Error           | app        | Error handling |

---

# Execution Order Example

```js
app.use(cors());

app.use(express.json());

app.use(logger);

app.use('/api',auth);

app.use(routes);

app.use(errorHandler);
```

Flow:

```
Request
 ↓
CORS
 ↓
JSON Parser
 ↓
Logger
 ↓
Auth
 ↓
Routes
 ↓
Error Handler
 ↓
Response
```

---

# Interview-Level Answer

**Express middleware is categorized into application middleware, router middleware, built-in middleware, third-party middleware, and error-handling middleware. Application middleware runs globally, router middleware runs for specific route groups, built-in middleware provides core features like body parsing, third-party middleware adds extra functionality like CORS or file uploads, and error middleware handles application errors centrally.**

---

Next logical deep interview question:

**19. Application vs Router Middleware (very frequently asked).**
