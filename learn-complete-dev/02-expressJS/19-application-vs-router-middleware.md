## 19. Application vs Router Middleware in Express.js

Application middleware and router middleware are two fundamental ways to apply middleware in Express. The difference lies in **where middleware is attached and which routes it affects.**

---

# 1. Application Middleware

## Definition

**Application middleware** is middleware attached to the **Express application object (`app`)** and typically applies to **all routes or a specified path prefix.**

Syntax:

```js
app.use(middlewareFunction)
```

Example:

```js
const express = require('express');
const app = express();

app.use((req, res, next) => {
  console.log("Application middleware");
  next();
});
```

This middleware runs for:

```
GET /users
POST /login
DELETE /products
GET /orders/10
```

It executes for **every request** unless restricted by a path.

---

## Path-Based Application Middleware

Application middleware can be limited to a specific path.

Example:

```js
app.use('/api', (req, res, next) => {
  console.log("API middleware");
  next();
});
```

Runs only for:

```
/api/users
/api/products
/api/orders
```

Does not run for:

```
/login
/register
/home
```

---

## Typical Uses of Application Middleware

Application middleware is used for **global concerns**.

Examples:

### Logging

```js
app.use(logger);
```

### Body Parsing

```js
app.use(express.json());
```

### Security

```js
app.use(helmet());
```

### CORS

```js
app.use(cors());
```

### Rate Limiting

```js
app.use(rateLimiter);
```

---

## Execution Scope

Application middleware scope:

```
Entire application
```

Flow:

```
Request → Application Middleware → Route → Response
```

---

# 2. Router Middleware

## Definition

**Router middleware** is middleware attached to an **Express Router object** and applies only to routes handled by that router.

Router creation:

```js
const router = express.Router();
```

Middleware applied:

```js
router.use(middlewareFunction);
```

Mounted on app:

```js
app.use('/users', router);
```

---

## Example

```js
const express = require('express');

const router = express.Router();

router.use((req, res, next) => {
  console.log("Router middleware");
  next();
});

router.get('/', (req,res)=>{
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

## Typical Uses of Router Middleware

Router middleware is used for **feature-specific logic.**

Examples:

### Authentication

```js
router.use(authMiddleware);
```

Protects:

```
/users/*
```

---

### Role Authorization

```js
router.use(adminMiddleware);
```

Protects:

```
/admin/*
```

---

### Module-specific Logging

```js
router.use(userLogger);
```

---

## Execution Scope

Router middleware scope:

```
Specific route group
```

Flow:

```
Request
 ↓
Application Middleware
 ↓
Router Middleware
 ↓
Route Handler
 ↓
Response
```

---

# Execution Order Example

```js
app.use(globalLogger);

const router = express.Router();

router.use(auth);

router.get('/', handler);

app.use('/users', router);
```

Request:

```
GET /users
```

Execution:

```
globalLogger
   ↓
auth
   ↓
handler
```

---

# Route-Level Middleware (Related Concept)

Route middleware applies to a **single route only.**

Example:

```js
router.get(
 '/profile',
 authMiddleware,
 handler
);
```

Runs only for:

```
/profile
```

Not:

```
/users
/users/10
```

---

# Code Structure Comparison

## Application Middleware Example

```js
app.use(auth);
```

Structure:

```
auth → all routes
```

---

## Router Middleware Example

```js
app.use('/api/users', userRouter);
```

Inside router:

```js
router.use(auth);
```

Structure:

```
auth → /api/users/*
```

---

# Real Production Example

Typical production Express app:

```js
app.use(cors());

app.use(express.json());

app.use(logger);

app.use('/api/users', userRouter);

app.use('/api/orders', orderRouter);

app.use(errorHandler);
```

userRouter.js:

```js
router.use(auth);

router.get('/', getUsers);
router.post('/', createUser);
```

Execution:

```
Request
 ↓
CORS
 ↓
JSON Parser
 ↓
Logger
 ↓
Auth (only users)
 ↓
Route
 ↓
Error Handler
```

---

# Key Differences

| Feature    | Application Middleware | Router Middleware    |
| ---------- | ---------------------- | -------------------- |
| Applied On | app                    | router               |
| Scope      | Entire app or prefix   | Specific route group |
| Setup      | app.use()              | router.use()         |
| Use Case   | Global logic           | Feature logic        |
| Example    | CORS                   | Auth                 |

---

# When to Use Application Middleware

Use when logic applies globally:

* Logging
* Security headers
* CORS
* Rate limiting
* JSON parsing

Example:

```js
app.use(cors());
```

---

# When to Use Router Middleware

Use when logic applies to specific modules:

* User authentication
* Admin routes
* API modules

Example:

```js
app.use('/admin', adminRouter);
```

adminRouter.js:

```js
router.use(adminAuth);
```

---

# Interview Trick Question

### Question

Which runs first — Application middleware or Router middleware?

### Answer

**Application middleware runs first, then router middleware.**

Example:

```js
app.use(A);

app.use('/users', router);
```

router:

```js
router.use(B);
```

Execution:

```
A → B → Route Handler
```

---

# Interview-Level Answer

**Application middleware is middleware attached to the Express application object and applies globally or to a path prefix, while router middleware is attached to an Express Router instance and applies only to routes handled by that router. Application middleware is used for global concerns like logging and security, whereas router middleware is used for module-specific logic such as authentication or authorization.**
