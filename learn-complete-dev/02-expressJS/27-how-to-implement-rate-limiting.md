## 27. How to Implement Rate Limiting in Express.js

**Rate limiting** is the technique of controlling how many requests a client can make to an API within a specific time period. It protects the server from:

* DDoS attacks
* Brute-force login attempts
* API abuse
* Excessive traffic
* Resource exhaustion

Example:

```text
100 requests per 15 minutes per IP
```

If the limit is exceeded:

```http
HTTP 429 Too Many Requests
```

---

# 1. Why Rate Limiting is Important

Without rate limiting:

```text
Attacker → 10,000 requests/sec → Server crash
```

With rate limiting:

```text
Attacker → blocked after 100 requests
```

---

# 2. Basic Rate Limiting Using express-rate-limit

Most common method.

Install:

```bash
npm install express-rate-limit
```

---

## Basic Implementation

```js
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({

 windowMs: 15 * 60 * 1000, // 15 minutes

 max: 100 // max requests

});

app.use(limiter);
```

Meaning:

```text
Each IP allowed 100 requests per 15 minutes
```

After limit:

```http
429 Too Many Requests
```

---

## How It Works Internally

Steps:

### Step 1

Client sends request:

```text
IP = 192.168.1.10
```

---

### Step 2

Limiter checks count:

```text
Current requests = 50
Limit = 100
```

Allowed.

---

### Step 3

Count increases:

```text
Requests = 51
```

---

### Step 4

If exceeds:

```text
Requests = 101
```

Blocked.

---

# 3. Customizing Rate Limiting

Example:

```js
const limiter = rateLimit({

 windowMs: 10 * 60 * 1000,

 max: 50,

 message: "Too many requests",

 standardHeaders: true,

 legacyHeaders: false

});
```

---

## Configuration Explained

### windowMs

Time window.

Example:

```js
windowMs: 60000
```

Meaning:

```text
1 minute
```

---

### max

Maximum requests.

Example:

```js
max: 10
```

Meaning:

```text
10 requests per window
```

---

### message

Response message.

Example:

```js
message:"Too many requests"
```

---

### Headers

Example headers:

```http
RateLimit-Limit: 100
RateLimit-Remaining: 50
RateLimit-Reset: 900
```

Helps client track limits.

---

# 4. Route-Specific Rate Limiting

Instead of entire app.

Example login protection:

```js
app.post('/login',
 rateLimit({
   windowMs: 10 * 60 * 1000,
   max: 5
 }),
 loginController
);
```

Meaning:

```text
5 login attempts per 10 minutes
```

Prevents:

```text
Password brute force
```

---

# 5. Different Limits for Different Routes

Example:

### Public APIs

```js
app.use('/api',
 rateLimit({
  windowMs: 15*60*1000,
  max:200
 }));
```

---

### Login API

```js
app.post('/login',
 rateLimit({
  windowMs:15*60*1000,
  max:5
 }));
```

---

### Admin APIs

```js
app.use('/admin',
 rateLimit({
  windowMs:60*1000,
  max:1000
 }));
```

---

# 6. Memory-Based Rate Limiting (Default)

Default storage:

```text
Server memory
```

Problem:

```text
Server restart → counters reset
```

Problem:

```text
Multiple servers → inconsistent limits
```

Not ideal for production scaling.

---

# 7. Redis-Based Rate Limiting (Production)

Best practice for scalable apps.

Install:

```bash
npm install ioredis
```

---

## Example Concept

```js
const Redis = require('ioredis');

const redis = new Redis();
```

---

## Custom Rate Limiter

Example logic:

```js
async function rateLimiter(req,res,next){

 const ip = req.ip;

 const requests = await redis.incr(ip);

 if(requests === 1){
   await redis.expire(ip,60);
 }

 if(requests > 100){
   return res.status(429)
   .send("Too many requests");
 }

 next();

}
```

Usage:

```js
app.use(rateLimiter);
```

---

## How Redis Limiting Works

Flow:

```text
Request arrives
 ↓
Get IP
 ↓
Increment counter in Redis
 ↓
Check limit
 ↓
Allow or block
```

---

# 8. Rate Limiting Strategies

## 1. Fixed Window

Example:

```text
100 requests per minute
```

Problem:

```text
User sends 100 requests at 59 sec
Then 100 at 61 sec
Total = 200
```

Burst allowed.

---

## 2. Sliding Window

Better approach.

Example:

```text
Last 60 seconds
```

More accurate.

---

## 3. Token Bucket

Tokens refill gradually.

Example:

```text
10 requests per second
```

Better for APIs.

---

# 9. Identifying Clients

Usually:

```text
IP Address
```

Example:

```js
req.ip
```

---

## Alternative Identifiers

### API Key

Example:

```js
req.headers['x-api-key']
```

---

### User ID

Example:

```js
req.user.id
```

Better for authenticated APIs.

---

# 10. Reverse Proxy Issue

If using NGINX or load balancer:

Wrong IP:

```text
127.0.0.1
```

Fix:

```js
app.set('trust proxy', 1);
```

Then:

```js
req.ip
```

Returns real IP.

---

# 11. Distributed System Rate Limiting

Multiple servers:

```text
Server 1
Server 2
Server 3
```

Need shared storage:

```text
Redis
```

Otherwise:

```text
User bypass limits
```

---

# 12. Production Example

Typical production setup:

```js
app.set('trust proxy', 1);

app.use(rateLimit({

 windowMs:15*60*1000,

 max:100,

 standardHeaders:true

}));
```

Login limiter:

```js
app.post('/login',
 rateLimit({
   windowMs:15*60*1000,
   max:5
 }),
 loginHandler
);
```

---

# 13. Best Practices

## Use Different Limits

Example:

```text
Login → strict
API → moderate
Admin → relaxed
```

---

## Use Redis in Production

Better than memory store.

---

## Combine with Auth

Example:

```text
Rate limit per user
```

Better than per IP.

---

## Return Proper Status

```http
429 Too Many Requests
```

---

# 14. Common Interview Questions

## Question 1

Why rate limiting required?

Answer:

* Prevent abuse
* Prevent DDoS
* Protect server

---

## Question 2

Best production approach?

Answer:

```text
Redis-based rate limiting
```

---

## Question 3

Why memory limiter not good?

Answer:

* Not shared across servers
* Reset on restart

---

## Question 4

Where apply rate limiter?

Answer:

* Login routes
* Public APIs
* Auth endpoints

---

# Rate Limiting Flow

```text
Client Request
     ↓
Rate Limiter Middleware
     ↓
Check Request Count
     ↓
Allowed → Route Handler
Blocked → 429 Response
```

---

# Interview-Level Answer

**Rate limiting in Express.js is implemented using middleware such as `express-rate-limit` or custom logic to restrict the number of requests a client can make within a time window. The middleware tracks requests by IP address or user ID and returns HTTP 429 when the limit is exceeded. In production systems, Redis is commonly used as a shared store to support distributed rate limiting across multiple servers.**
