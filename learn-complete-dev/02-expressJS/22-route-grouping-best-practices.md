## 22. Route Grouping Best Practices in Express.js

**Route grouping** means organizing routes into logical modules instead of defining all routes in one file. This is essential for building **scalable and maintainable Express applications**, especially in real production systems.

Without proper route grouping, applications become difficult to maintain.

---

# 1. The Problem Without Route Grouping

Bad practice example:

```js
app.get('/users', getUsers);
app.post('/users', createUser);
app.get('/users/:id', getUser);

app.get('/orders', getOrders);
app.post('/orders', createOrder);

app.get('/products', getProducts);
app.post('/products', createProducts);
```

Problems:

* One file becomes very large (1000+ lines)
* Hard to maintain
* Hard to debug
* Hard to scale
* Hard to test

Large projects should avoid this structure.

---

# 2. Basic Route Grouping Using Express Router

Express provides **Router** for grouping routes.

### Step 1 — Create Router

userRoutes.js:

```js
const express = require('express');

const router = express.Router();

router.get('/', getUsers);

router.post('/', createUser);

router.get('/:id', getUser);

module.exports = router;
```

---

### Step 2 — Mount Router

app.js:

```js
const userRoutes = require('./routes/userRoutes');

app.use('/users', userRoutes);
```

Final routes:

```text
GET /users
POST /users
GET /users/:id
```

---

# 3. Recommended Folder Structure

Professional Express structure:

```
src/
 ├── routes/
 │     userRoutes.js
 │     orderRoutes.js
 │     authRoutes.js
 │
 ├── controllers/
 │     userController.js
 │     orderController.js
 │
 ├── services/
 │     userService.js
 │
 ├── middleware/
 │     auth.js
 │
 ├── models/
 │
 └── app.js
```

This structure is used in **real production Node.js backends.**

---

# 4. Route → Controller → Service Pattern

Best practice architecture:

```
Route → Controller → Service → Database
```

### Route

userRoutes.js

```js
router.get('/', userController.getUsers);
```

---

### Controller

userController.js

```js
exports.getUsers = async (req,res)=>{

 const users = await userService.getUsers();

 res.json(users);

}
```

---

### Service

userService.js

```js
exports.getUsers = async ()=>{

 return db.users.find();

}
```

---

## Advantages

### Clean Separation

Routes:

```text
Handle URLs
```

Controllers:

```text
Handle HTTP logic
```

Services:

```text
Handle business logic
```

Database:

```text
Handle data
```

---

# 5. Grouping by Feature (Best Practice)

Group routes by **feature/module**, not by HTTP method.

Correct:

```
routes/
 userRoutes.js
 orderRoutes.js
 productRoutes.js
```

Wrong:

```
routes/
 getRoutes.js
 postRoutes.js
 deleteRoutes.js
```

Feature-based grouping is scalable.

---

# 6. Route Prefixing

Use route prefixes.

Example:

```js
app.use('/api/users', userRoutes);
```

Result:

```
/api/users
/api/users/:id
```

Better than:

```
/users
```

Because:

* APIs clearly separated
* Easy versioning

---

# 7. Nested Route Grouping

Example:

```
Users → Orders
```

Routes:

```
/users/:id/orders
```

Example:

```js
router.get('/:id/orders', getUserOrders);
```

---

# 8. Versioned Route Grouping

Best practice for production APIs.

Example:

```
routes/
 v1/
   userRoutes.js
   orderRoutes.js

 v2/
   userRoutes.js
```

app.js:

```js
app.use('/api/v1', v1Routes);

app.use('/api/v2', v2Routes);
```

Result:

```
/api/v1/users
/api/v2/users
```

Prevents breaking existing clients.

---

# 9. Middleware-Based Route Groups

Routes can share middleware.

Example:

```js
app.use('/api', authMiddleware);
```

Protects:

```
/api/users
/api/orders
```

---

### Router-level Middleware

Example:

userRoutes.js

```js
router.use(authMiddleware);
```

Protects:

```
/users/*
```

---

# 10. Keep Routes Thin (Very Important)

Routes should be small.

Bad:

```js
router.get('/', async(req,res)=>{

 const users = await db.users.find();

 const filtered = users.filter(u=>u.age>20);

 res.json(filtered);

});
```

Good:

```js
router.get('/', userController.getUsers);
```

---

# 11. Use RESTful Naming

Correct:

```
GET /users
GET /users/:id
POST /users
PUT /users/:id
DELETE /users/:id
```

Wrong:

```
GET /getUsers
POST /createUser
```

---

# 12. Keep One Router Per Resource

Best practice:

```
userRoutes.js → users
orderRoutes.js → orders
authRoutes.js → auth
```

Avoid:

```
allRoutes.js
```

---

# 13. Central Route Index File (Advanced)

Better structure:

```
routes/
 index.js
 userRoutes.js
 orderRoutes.js
```

routes/index.js:

```js
const express = require('express');

const router = express.Router();

router.use('/users', require('./userRoutes'));

router.use('/orders', require('./orderRoutes'));

module.exports = router;
```

app.js:

```js
app.use('/api', routes);
```

Final routes:

```
/api/users
/api/orders
```

---

# 14. Avoid Deep Nesting

Bad:

```
routes/api/v1/admin/users/routes.js
```

Better:

```
routes/v1/users.js
```

---

# 15. Use Meaningful Route Names

Good:

```
/users
/orders
/products
```

Bad:

```
/data
/api1
/x
```

---

# 16. Example Production Route Structure

```
src/
 ├── routes/
 │     index.js
 │
 │     v1/
 │       authRoutes.js
 │       userRoutes.js
 │       orderRoutes.js
 │
 ├── controllers/
 ├── services/
 ├── middleware/
 └── app.js
```

app.js:

```js
app.use('/api/v1', require('./routes/v1'));
```

---

# 17. Common Interview Questions

## Question

Why do we use Express Router?

Answer:

* Modular code
* Scalability
* Clean structure
* Reusability

---

## Question

Best architecture pattern?

Answer:

```
Route → Controller → Service → DB
```

---

## Question

Why keep routes thin?

Answer:

* Separation of concerns
* Testable
* Clean code

---

# Interview-Level Answer

**Route grouping in Express.js is the practice of organizing routes into modular routers using `express.Router()` instead of defining all routes in one file. Best practices include grouping routes by feature, using a Route → Controller → Service architecture, applying route prefixes like `/api/v1`, keeping routes thin, and maintaining a scalable folder structure. This improves maintainability, scalability, and code organization.**
