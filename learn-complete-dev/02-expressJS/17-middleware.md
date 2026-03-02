## 17. Middleware — What and Why?

### Definition

**Middleware in Express.js** is a function that executes **during the request–response cycle**, before the final response is sent to the client.

Middleware functions have access to:

* `req` → Request object
* `res` → Response object
* `next()` → Function to pass control to the next middleware

Basic structure:

```js
function middleware(req, res, next) {
   // logic
   next();
}
```

Usage:

```js
app.use(middleware);
```

---

## Where Middleware Runs

Middleware runs **between the incoming request and outgoing response.**

Request flow:

```
Client Request
      ↓
Middleware 1
      ↓
Middleware 2
      ↓
Middleware 3
      ↓
Route Handler
      ↓
Response
```

Example:

```js
app.use((req,res,next)=>{
 console.log("Middleware 1");
 next();
});

app.use((req,res,next)=>{
 console.log("Middleware 2");
 next();
});

app.get('/',(req,res)=>{
 res.send("Hello");
});
```

Output:

```
Middleware 1
Middleware 2
Hello
```

---

## Middleware Function Signature

Standard middleware:

```js
(req, res, next)
```

Parameters:

### req

Contains request data:

Examples:

```
req.body
req.params
req.query
req.headers
req.method
req.url
```

---

### res

Used to send response:

Examples:

```
res.send()
res.json()
res.status()
res.end()
```

---

### next()

Transfers control to the next middleware.

Example:

```js
app.use((req,res,next)=>{
 console.log("Step 1");
 next();
});
```

Without `next()`:

```js
app.use((req,res)=>{
 console.log("Stops request");
});
```

Request **never completes**.

---

## Why Middleware is Used

Middleware allows separating logic into reusable components.

Instead of writing everything inside routes:

Bad design:

```js
app.get('/users',(req,res)=>{

 console.log("Request");

 if(!req.headers.token)
   return res.status(401).send();

 const users = getUsers();

 res.json(users);

});
```

Better:

```js
app.use(logger);
app.use(auth);

app.get('/users',(req,res)=>{
 res.json(getUsers());
});
```

Middleware makes code:

* Modular
* Reusable
* Maintainable
* Scalable

---

## Common Uses of Middleware

### 1) Logging Middleware

Tracks requests.

Example:

```js
function logger(req,res,next){

 console.log(
   req.method,
   req.url,
   new Date()
 );

 next();
}
```

Usage:

```js
app.use(logger);
```

Output:

```
GET /users
POST /login
```

---

### 2) Authentication Middleware

Protects routes.

Example:

```js
function auth(req,res,next){

 const token = req.headers.authorization;

 if(!token)
   return res.status(401).send("Unauthorized");

 next();
}
```

Usage:

```js
app.use('/api',auth);
```

Protects:

```
/api/*
```

---

### 3) Body Parsing Middleware

Parses request body.

Example:

```js
app.use(express.json());
```

Without it:

```
req.body = undefined
```

---

### 4) Validation Middleware

Validates input.

Example:

```js
function validateUser(req,res,next){

 if(!req.body.email)
   return res.status(400).send("Email required");

 next();
}
```

---

### 5) Security Middleware

Example:

```
Helmet
CORS
Rate Limit
```

Example:

```js
app.use(cors());
```

---

### 6) Error Handling Middleware

Handles application errors.

Example:

```js
app.use((err,req,res,next)=>{

 res.status(500).json({
   error:err.message
 });

});
```

---

## Middleware Execution Order

Middleware runs **in the order defined.**

Example:

```js
app.use(A);
app.use(B);
app.use(C);
```

Execution:

```
A → B → C
```

---

### Example

```js
app.use((req,res,next)=>{
 console.log("First");
 next();
});

app.use((req,res,next)=>{
 console.log("Second");
 next();
});

app.get('/',(req,res)=>{
 res.send("Done");
});
```

Output:

```
First
Second
Done
```

---

## Middleware Can End Request

Middleware does not always call `next()`.

Example:

```js
function block(req,res,next){

 res.status(403).send("Blocked");

}
```

Stops execution.

---

## Middleware Can Modify Request

Example:

```js
app.use((req,res,next)=>{

 req.user = {
   id:1,
   name:"Aayush"
 };

 next();
});
```

Route:

```js
app.get('/profile',(req,res)=>{
 res.json(req.user);
});
```

Output:

```
{id:1,name:"Aayush"}
```

---

## Middleware Can Modify Response

Example:

```js
app.use((req,res,next)=>{

 res.setHeader(
   "X-Powered-By",
   "Express"
 );

 next();
});
```

---

## Types of Middleware Execution

### Global Middleware

Runs for every request.

```js
app.use(logger);
```

---

### Route Middleware

Runs for specific route.

```js
app.get('/users', auth, handler);
```

---

### Router Middleware

Runs for router group.

```js
app.use('/api', auth);
```

---

## Middleware Chain Internals

Express stores middleware in a stack:

Conceptually:

```
[
 logger,
 auth,
 parser,
 routeHandler
]
```

Express executes sequentially.

Pseudo:

```
execute middleware[i]
if next()
   i++
else
   stop
```

---

## Important Interview Concepts

### Middleware vs Route Handler

Middleware:

```
(req,res,next)
```

Route Handler:

```
(req,res)
```

Example:

Middleware:

```js
(req,res,next)
```

Route:

```js
(req,res)
```

---

### next() vs next(err)

next():

```
Normal flow
```

next(err):

```
Error middleware
```

Example:

```js
next(new Error("DB error"));
```

---

## Real Production Middleware Stack

Typical backend:

```js
app.use(cors());

app.use(helmet());

app.use(express.json());

app.use(rateLimit());

app.use(logger);

app.use(auth);

app.use(routes);

app.use(errorHandler);
```

Flow:

```
Request
↓
CORS
↓
Security
↓
Parser
↓
Rate Limit
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

## Interview-Level Answer (Best Version)

**Middleware in Express.js is a function that executes during the request-response lifecycle and has access to the request object, response object, and the next middleware function. It is used to process requests before reaching route handlers for tasks like authentication, logging, validation, parsing, and security. Middleware enables modular and reusable backend architecture.**

---

Next important topic interviewers usually ask:

**"Explain types of middleware in Express."**
