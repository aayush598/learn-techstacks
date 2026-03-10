Below is a **deep technical explanation of Express.js (Full Stack Node.js Interview Level)** covering each topic in detail.

---

# BASICS

## 16. What is Express.js?

**Express.js** is a **minimal and flexible web framework for Node.js** used to build web applications and APIs. It provides a thin layer over Node.js HTTP module and simplifies server development.

Without Express:

```js
const http = require('http');

http.createServer((req, res) => {
  res.writeHead(200);
  res.end("Hello");
}).listen(3000);
```

With Express:

```js
const express = require('express');
const app = express();

app.get('/', (req,res)=>{
  res.send("Hello");
});

app.listen(3000);
```

### Key Features

#### 1. Routing

Maps HTTP requests to handlers.

Example:

```js
app.get('/users', handler)
app.post('/users', handler)
```

#### 2. Middleware Support

Chainable request processors:

```js
app.use(authMiddleware);
app.use(loggerMiddleware);
```

#### 3. HTTP Utilities

Express simplifies:

* Headers
* Cookies
* Query parsing
* Body parsing

Example:

```js
res.status(200).json({message:"OK"});
```

#### 4. REST API Friendly

Express is widely used for:

* REST APIs
* Microservices
* Backend servers

---

### Express Architecture

Flow:

```
Client Request
      ↓
Express App
      ↓
Middleware 1
      ↓
Middleware 2
      ↓
Route Handler
      ↓
Response
```

---

### Why Express is Popular

Reasons:

* Minimal and fast
* Huge ecosystem
* Middleware-based design
* Easy learning curve
* Production proven

---

### Express Internals

Express wraps Node's HTTP module:

Node object:

```
IncomingMessage
ServerResponse
```

Express extends them:

```
req → Extended IncomingMessage
res → Extended ServerResponse
```

---

## 17. Middleware — What and Why?

### Definition

Middleware is a function that runs **between request and response**.

Structure:

```js
(req, res, next) => {}
```

Example:

```js
function logger(req,res,next){
  console.log(req.method, req.url);
  next();
}
```

Used:

```js
app.use(logger);
```

---

### Middleware Flow

```
Request
  ↓
Middleware1
  ↓
Middleware2
  ↓
Middleware3
  ↓
Route Handler
  ↓
Response
```

---

### next() Function

Passes control to next middleware.

Example:

```js
app.use((req,res,next)=>{
  console.log("Step1");
  next();
});

app.use((req,res)=>{
  res.send("Done");
});
```

---

### Without next()

Request hangs:

```js
app.use((req,res)=>{
 console.log("Stops here");
});
```

No response returned.

---

### Why Middleware is Used

Used for:

* Authentication
* Logging
* Validation
* Parsing body
* Caching
* Security

Example:

Auth middleware:

```js
function auth(req,res,next){

 if(!req.headers.token)
   return res.status(401).send();

 next();
}
```

---

### Middleware Chain Example

```js
app.use(logger);
app.use(auth);
app.use(parser);
```

Execution:

```
logger → auth → parser → route
```

---

## 18. Types of Middleware

### 1) Application Middleware

Applied globally.

```js
app.use(logger);
```

Runs for every request.

---

### 2) Router Middleware

Applied to specific routes.

```js
router.use(auth);
```

Example:

```
/api/users/*
```

---

### 3) Built-in Middleware

Provided by Express.

Examples:

### JSON parser

```js
app.use(express.json());
```

### URL encoded

```js
app.use(express.urlencoded());
```

### Static files

```js
app.use(express.static('public'));
```

---

### 4) Third-party Middleware

External libraries.

Examples:

Helmet:

```js
app.use(helmet());
```

Cors:

```js
app.use(cors());
```

Multer:

```js
app.use(multer());
```

---

### 5) Error Middleware

Handles errors.

Signature:

```
(err, req, res, next)
```

Example:

```js
app.use((err,req,res,next)=>{
 res.status(500).send(err.message);
});
```

---

## 19. Application vs Router Middleware

### Application Middleware

Defined on app.

```js
app.use(auth);
```

Applies to:

```
ALL ROUTES
```

---

Example:

```
/users
/products
/admin
```

Auth runs everywhere.

---

### Router Middleware

Defined on router.

```js
const router = express.Router();

router.use(auth);
```

Mounted:

```js
app.use('/api', router);
```

Applies only to:

```
/api/*
```

---

### Example

Application:

```js
app.use(logger);
```

Router:

```js
router.use(auth);
```

Execution:

```
logger → auth → route
```

---

### When to Use

Application middleware:

* Logging
* Global error handling
* Security headers

Router middleware:

* Authentication
* Role based access
* API specific logic

---

## 20. Error-Handling Middleware Signature

### Signature

```
(err, req, res, next)
```

4 parameters required.

Example:

```js
app.use((err, req, res, next) => {

 res.status(500).json({
   error: err.message
 });

});
```

---

### How Errors Reach Middleware

#### Throw error

```js
app.get('/',(req,res)=>{
 throw new Error("Crash");
});
```

---

#### next(error)

```js
app.get('/',(req,res,next)=>{
 next(new Error("Fail"));
});
```

---

### Async Errors

Incorrect:

```js
app.get('/', async(req,res)=>{
 throw new Error("Fail");
});
```

Express 4 will crash.

Correct:

```js
app.get('/', async(req,res,next)=>{
 try{
   throw new Error("Fail");
 }catch(err){
   next(err);
 }
});
```

---

### Error Middleware Order

Must be last.

Correct:

```
Routes
↓
Error Middleware
```

Wrong:

```
Error Middleware
↓
Routes
```

---

# ROUTING

## 21. Route Parameters vs Query Params

### Route Parameters

Defined in URL path.

Example:

```
/users/:id
```

Code:

```js
app.get('/users/:id',(req,res)=>{
 console.log(req.params.id);
});
```

URL:

```
/users/25
```

Output:

```
25
```

---

### Query Parameters

After `?`

Example:

```
/users?page=2&limit=10
```

Code:

```js
app.get('/users',(req,res)=>{
 console.log(req.query.page);
});
```

Output:

```
2
```

---

### Differences

| Feature  | Route Params | Query Params |
| -------- | ------------ | ------------ |
| Location | Path         | URL query    |
| Example  | /users/1     | /users?id=1  |
| Use      | Resource ID  | Filters      |

---

### Best Practice

Route param:

```
GET /users/10
```

Query:

```
GET /users?page=2
```

---

## 22. Route Grouping Best Practices

Large projects must avoid:

```
app.js → 2000 lines
```

---

### Best Structure

```
src/
  routes/
    userRoutes.js
    authRoutes.js
  controllers/
  services/
```

---

### Router Example

userRoutes.js

```js
const router = require('express').Router();

router.get('/', getUsers);
router.post('/', createUser);

module.exports = router;
```

app.js:

```js
app.use('/users', userRoutes);
```

---

### Controller Pattern

Better:

```
Routes → Controller → Service → DB
```

Example:

Route:

```js
router.get('/', userController.getUsers);
```

Controller:

```js
exports.getUsers = async(req,res)=>{
 const users = await userService.getUsers();
 res.json(users);
}
```

---

### Advantages

* Clean code
* Scalable
* Maintainable
* Testable

---

## 23. Versioned APIs in Express

### Why Version APIs?

Breaking changes.

Example:

V1:

```
GET /users
```

V2:

```
GET /users?page=1
```

---

### URL Versioning

Most common:

```
/api/v1/users
/api/v2/users
```

Example:

```js
app.use('/api/v1', v1Routes);
app.use('/api/v2', v2Routes);
```

---

### Folder Structure

```
routes/
 v1/
   users.js
 v2/
   users.js
```

---

### Header Versioning

Less common.

```
Accept: application/v1
```

Example:

```js
req.headers.version
```

---

### Query Versioning

```
/users?version=1
```

Not recommended.

---

### Best Practice

Use:

```
/api/v1/
```

---

# REQUEST / RESPONSE

## 24. How Body Parsing Works

HTTP request body arrives as **streamed raw data**.

Example raw body:

```
{"name":"Aayush"}
```

Express must convert into object.

---

### express.json()

```js
app.use(express.json());
```

Internally:

1 Request arrives
2 Read stream
3 Parse JSON
4 Attach to req.body

Result:

```js
req.body.name
```

---

### URL Encoded

```
name=Aayush&age=22
```

Parser:

```js
app.use(express.urlencoded({extended:true}));
```

---

### Without Body Parser

```
req.body = undefined
```

---

### Limit Setting

```js
app.use(express.json({
 limit:"1mb"
}));
```

---

## 25. req.params vs req.query vs req.body

### req.params

From route.

```
/users/:id
```

```
req.params.id
```

---

### req.query

From URL.

```
?sort=asc
```

```
req.query.sort
```

---

### req.body

From request body.

POST:

```
{name:"Aayush"}
```

```
req.body.name
```

---

### Comparison Table

| Source | Example       |
| ------ | ------------- |
| params | /users/10     |
| query  | /users?page=1 |
| body   | POST data     |

---

## 26. File Uploads in Express

Express does not support file upload natively.

Use **Multer**.

Install:

```
npm install multer
```

---

### Basic Upload

```js
const multer = require('multer');

const upload = multer({
 dest:"uploads/"
});

app.post('/upload',
 upload.single('file'),
(req,res)=>{
 res.send("Uploaded");
});
```

---

### Memory Storage

```js
multer.memoryStorage()
```

Used for:

* S3 uploads
* Cloudinary

---

### Disk Storage

```js
multer.diskStorage({
 destination:'uploads',
 filename:(req,file,cb)=>{
   cb(null,file.originalname);
 }
});
```

---

### Multiple Files

```js
upload.array('files',5)
```

---

### File Filter

```js
fileFilter:(req,file,cb)=>{

 if(file.mimetype==="image/png")
   cb(null,true);
 else
   cb(null,false);
}
```

---

# ADVANCED

## 27. Rate Limiting

Limits requests per IP.

Prevents:

* DDoS
* Brute force

---

### Library

```
express-rate-limit
```

Example:

```js
const rateLimit=require('express-rate-limit');

const limiter=rateLimit({

 windowMs:15*60*1000,
 max:100

});

app.use(limiter);
```

---

### Custom Rate Limiter (Redis)

Key:

```
IP address
```

Flow:

```
Check Redis count
Increment
Block if limit reached
```

Example pseudo:

```js
const count = await redis.incr(ip);

if(count>100)
 res.status(429);
```

---

## 28. Handling Large Payloads

Problem:

Large JSON:

```
50MB request
```

Problems:

* Memory crash
* Slow parsing

---

### Limit Size

```js
app.use(express.json({
 limit:"2mb"
}));
```

---

### Stream Instead

Example:

```
File uploads
Video
CSV
```

Use streams.

---

### Compression

Use gzip.

```js
app.use(compression());
```

---

### Reverse Proxy Limits

NGINX:

```
client_max_body_size 10M;
```

---

## 29. Streaming Responses in Express

Instead of sending full response.

Send chunks.

---

### Normal Response

```
Server builds response
Then sends
```

Slow for big data.

---

### Streaming

Send piece-by-piece.

Example:

```js
app.get('/stream',(req,res)=>{

 res.write("Part1\n");

 setTimeout(()=>{
   res.write("Part2\n");
   res.end();
 },2000);

});
```

---

### File Streaming

```js
const fs=require('fs');

app.get('/video',(req,res)=>{

 const stream=fs.createReadStream("video.mp4");

 stream.pipe(res);

});
```

---

### Benefits

* Low memory
* Fast start
* Scalable

---

### Use Cases

* Video streaming
* Logs
* CSV export
* AI responses

---

## 30. Handling Timeouts and Retries

### Timeout Problem

Slow API:

```
DB takes 30 sec
```

Client waits forever.

---

### Server Timeout

Example:

```js
app.use((req,res,next)=>{

 res.setTimeout(5000,()=>{
   res.status(408).send();
 });

 next();

});
```

---

### Abort Controller

Cancel requests.

---

### Retry Logic (Client)

Example:

```
Try 3 times
```

Pseudo:

```
Attempt1
Attempt2
Attempt3
Fail
```

---

### Retry Middleware Example

```js
async function retry(fn,retries=3){

 try{
   return await fn();
 }
 catch(err){

  if(retries===0)
   throw err;

  return retry(fn,retries-1);

 }

}
```

---

### Best Practices

Timeout:

```
5–10 sec APIs
```

Retry:

```
Network failures only
```

---

If you master this section, you will perform **very strongly in Node.js interviews**, because **Express deep knowledge is one of the most tested backend topics.**

Next recommended deep-dive:

* Authentication (JWT + OAuth)
* Redis caching
* Advanced Node internals (Event loop deep dive)
* System design for APIs
