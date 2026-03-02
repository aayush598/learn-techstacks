## 20. Error-Handling Middleware Signature (Express.js)

Error-handling middleware is a **special type of middleware used to catch and handle errors centrally** in an Express application. Instead of handling errors inside every route, Express allows defining a **single global error handler**.

---

# Error-Handling Middleware Signature

The signature must have **four parameters**:

```js
(err, req, res, next)
```

Example:

```js
app.use((err, req, res, next) => {
  res.status(500).json({
    message: err.message
  });
});
```

### Parameters Explained

## 1. err

Contains the error object.

Example:

```js
next(new Error("Database error"));
```

Inside middleware:

```js
err.message
err.stack
err.name
```

Example:

```js
app.use((err,req,res,next)=>{
 console.log(err.message);
 res.status(500).send("Server Error");
});
```

---

## 2. req (Request Object)

Contains request details.

Example:

```js
req.url
req.method
req.headers
```

Useful for logging:

```js
app.use((err,req,res,next)=>{
 console.log(req.method, req.url);
 res.status(500).send();
});
```

---

## 3. res (Response Object)

Used to send error response.

Example:

```js
res.status(500).json({
 error:"Internal Server Error"
});
```

---

## 4. next (Next Function)

Used to pass error to next error middleware.

Example:

```js
next(err);
```

Multiple error handlers:

```js
app.use(errorLogger);
app.use(errorResponder);
```

---

# Why 4 Parameters Are Required

Express detects error middleware **only if it has 4 arguments.**

Correct:

```js
(err,req,res,next)
```

Incorrect:

```js
(req,res,next)
```

If 4 parameters are missing → Express treats it as normal middleware.

---

# Example Complete Flow

Route:

```js
app.get('/users',(req,res,next)=>{

 const error = new Error("Users not found");

 next(error);

});
```

Error middleware:

```js
app.use((err,req,res,next)=>{

 res.status(404).json({
   error:err.message
 });

});
```

Response:

```json
{
 "error":"Users not found"
}
```

---

# How Errors Reach Error Middleware

There are **three main ways**.

---

## 1. Using next(error)

Most common.

```js
app.get('/',(req,res,next)=>{

 next(new Error("Database Failed"));

});
```

Flow:

```text
Route → next(error) → Error Middleware
```

---

## 2. Throwing Errors (Synchronous)

Express automatically catches synchronous errors.

Example:

```js
app.get('/',(req,res)=>{
 throw new Error("Crash");
});
```

Express sends error to middleware.

---

## 3. Async Errors (Important Interview Question)

Express 4 **does NOT automatically catch async errors.**

Wrong:

```js
app.get('/', async(req,res)=>{
 throw new Error("Async error");
});
```

Server crashes.

Correct:

```js
app.get('/', async(req,res,next)=>{
 try{

  throw new Error("Async error");

 }catch(err){

  next(err);

 }
});
```

---

## Async Wrapper (Best Practice)

```js
const asyncHandler =
 fn => (req,res,next)=>{
   Promise.resolve(fn(req,res,next))
   .catch(next);
 };
```

Usage:

```js
app.get('/users',
 asyncHandler(async(req,res)=>{

   throw new Error("DB Error");

 })
);
```

---

# Error Middleware Must Be Last

Correct order:

```js
app.use(routes);

app.use(errorHandler);
```

Wrong order:

```js
app.use(errorHandler);

app.use(routes);
```

If error middleware comes first → errors not caught.

---

# Multiple Error Middleware

Express supports multiple error handlers.

Example:

### Error Logger

```js
app.use((err,req,res,next)=>{

 console.error(err.stack);

 next(err);

});
```

---

### Error Response

```js
app.use((err,req,res,next)=>{

 res.status(500).json({
   error:err.message
 });

});
```

Flow:

```text
Error → Logger → Responder
```

---

# Production-Level Error Handler

Example:

```js
app.use((err,req,res,next)=>{

 console.error(err);

 const status = err.status || 500;

 res.status(status).json({

   success:false,

   message:err.message || "Server Error"

 });

});
```

---

# Custom Error Class

Better design.

Example:

```js
class ApiError extends Error{

 constructor(status,message){

   super(message);

   this.status=status;

 }

}
```

Usage:

```js
next(new ApiError(404,"User not found"));
```

Handler:

```js
app.use((err,req,res,next)=>{

 res.status(err.status || 500)
 .json({
   error:err.message
 });

});
```

---

# Common Interview Questions

## Q1: Why use centralized error handling?

Answer:

* Avoid duplicate try/catch
* Consistent responses
* Easier debugging
* Clean code

---

## Q2: Difference between next() and next(err)

### next()

```text
Continue normal middleware chain
```

### next(err)

```text
Jump to error middleware
```

---

## Q3: What happens if next() is not called?

Request hangs.

---

## Q4: Can middleware send response and call next()?

Bad practice.

Example:

```js
res.send("OK");
next();
```

May cause:

```text
Cannot set headers after they are sent
```

---

# Express Error Flow Internals

Normal flow:

```text
Request
 ↓
Middleware
 ↓
Route
 ↓
Response
```

Error flow:

```text
Request
 ↓
Middleware
 ↓
Error occurs
 ↓
Error Middleware
 ↓
Response
```

---

# Interview-Level Answer

**Error-handling middleware in Express is a special middleware function defined with four parameters `(err, req, res, next)` that is used to handle application errors centrally. When an error occurs in routes or middleware and is passed using `next(err)` or thrown synchronously, Express forwards it to the error middleware which sends a consistent error response.**

---

Next section is **Routing**, typically asked in depth:

21. Route parameters vs query params
22. Route grouping best practices
23. Versioned APIs in Express

We can go question-by-question like this.
